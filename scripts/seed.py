#!/usr/bin/env python3
"""Deterministic producer and deliberately faulty incident consumer. No network except PostgreSQL."""
import argparse
import html
import json
import os
from pathlib import Path
import random
from datetime import datetime, timedelta, timezone
ROOT = Path(__file__).resolve().parents[1]

def generate(scenario):
    rng = random.Random(260603)
    events = []
    for i in range(3000):
        version = 2 if i >= 1500 else 1
        offset = timezone(timedelta(hours=2 if i % 3 == 0 else 0))
        stamp = (datetime(2026, 6, 3, tzinfo=timezone.utc) + timedelta(seconds=i*30)).astimezone(offset)
        e = dict(eventId=f'evt-{i:04}', orderId=f'ord-{i:04}', schemaVersion=version,
                 amountCents=rng.randint(100, 25000), occurredAt=stamp.isoformat())
        e.update({'customerId': f'cust-{i%400:03}'} if version == 1 else {'customer': {'id': f'cust-{i%400:03}'}})
        events.append(e)
    # Retries retain event identity and payload, but have distinct delivery identities.
    if scenario == 'incident':
        events.extend(dict(events[i]) for i in range(0, 3000, 50))
    return events

def consume(events, scenario):
    rows, errors, seen = [], [], set()
    for delivery, e in enumerate(events, 1):
        if scenario == 'baseline' and e['eventId'] in seen:
            continue
        seen.add(e['eventId'])
        customer = e.get('customerId') if scenario == 'incident' else e.get('customerId', e.get('customer', {}).get('id'))
        stamp = datetime.fromisoformat(e['occurredAt'])
        if scenario == 'incident':
            stamp = stamp.replace(tzinfo=timezone.utc)
        rows.append((delivery, e['eventId'], e['orderId'], customer, e['amountCents'], stamp))
        if customer is None:
            errors.append((delivery, 'CUSTOMER_MAPPING', 'customerId missing; persisted nullable field'))
    return rows, errors

def metrics(events, rows, errors):
    return dict(raw_events=len(events), orders=len(rows), distinct_events=len({r[1] for r in rows}),
                missing_customer=sum(r[3] is None for r in rows), duplicate_excess=len(rows)-len({r[1] for r in rows}),
                timestamp_shifted=sum(r[5] != datetime.fromisoformat(events[r[0]-1]['occurredAt']) for r in rows),
                ingestion_errors=len(errors))

def connect():
    import psycopg
    # Read generated local credentials without exporting them to logs or shell history.
    env = dict(line.split('=',1) for line in (ROOT/'.env').read_text().splitlines() if '=' in line and not line.startswith('#'))
    return psycopg.connect(host='127.0.0.1', port=55432, dbname='orders_demo', user='demo_admin', password=env['POSTGRES_PASSWORD'])

def export(events, rows, errors, scenario, measured, origin):
    evidence=ROOT/'public/evidence'; evidence.mkdir(parents=True,exist_ok=True)
    (evidence/'events.jsonl').write_text(''.join(json.dumps(dict(deliveryId=i,payload=e))+'\n' for i,e in enumerate(events,1)))
    (evidence/'ingestion.log').write_text(''.join(f'delivery={i} code={code} detail={detail}\n' for i,code,detail in errors) or 'ingestion completed\n')
    dest=ROOT/'presenter/generated'; dest.mkdir(parents=True,exist_ok=True)
    report=dict(scenario=scenario, origin=origin, metrics=measured, samples=[dict(delivery_id=r[0],event_id=r[1],customer_id=r[3],occurred_at=r[5].isoformat(),payload=events[r[0]-1]) for r in rows if r[0] in (1,1501,3001)],
                schema_diff={'v1':'customerId: string','v2':'customer.id: string'}, sql=(ROOT/'presenter/queries.sql').read_text() if origin.startswith('PostgreSQL') else 'SQL non eseguito in modalità offline')
    (dest/'report.json').write_text(json.dumps(report,indent=2))
    blob=json.dumps(report).replace('<', '\\u003c')
    template=(ROOT/'presenter/explorer-template.html').read_text()
    (dest/'incident-explorer.html').write_text(template.replace('__REPORT__',blob))

def db_metrics(conn):
    with conn.cursor() as c:
        c.execute('SELECT (SELECT count(*) FROM raw_events), count(*),count(DISTINCT event_id),count(*) FILTER(WHERE missing_customer),count(*)-count(DISTINCT event_id),count(*) FILTER(WHERE timestamp_delta_seconds<>0),(SELECT count(*) FROM ingestion_errors) FROM v_order_quality')
        return dict(zip(['raw_events','orders','distinct_events','missing_customer','duplicate_excess','timestamp_shifted','ingestion_errors'],c.fetchone()))

def live_events():
    """Due nuovi eventi e una riconsegna identica, con importi noti."""
    first = dict(eventId='live-A', orderId='live-order-A', schemaVersion=1,
                 customerId='live-customer-A', amountCents=1000,
                 occurredAt='2026-06-04T12:00:00+00:00')
    second = dict(eventId='live-B', orderId='live-order-B', schemaVersion=2,
                  customer={'id': 'live-customer-B'}, amountCents=2000,
                  occurredAt='2026-06-04T12:00:00+02:00')
    return [first, second, dict(second)]


def live_expected(expected):
    delta = dict(raw_events=3, orders=3, distinct_events=2, missing_customer=2,
                 duplicate_excess=1, timestamp_shifted=2, ingestion_errors=2)
    return {key: value + delta[key] for key, value in expected['incident'].items()}


def append_demo(expected):
    """Aggiunge tre consegne atomiche; nessun reset e nessuna replica accidentale."""
    events = live_events()
    rows, errors = consume(events, 'incident')
    with connect() as conn:
        with conn.cursor() as c:
            c.execute('LOCK TABLE raw_events, orders, ingestion_errors IN EXCLUSIVE MODE')
            if db_metrics(conn) != expected['incident']:
                raise SystemExit('Append annullato: serve lo scenario incident iniziale; nessun dato modificato.')
            c.execute("SELECT count(*) FROM raw_events WHERE payload->>'eventId' IN ('live-A','live-B')")
            if c.fetchone()[0]:
                raise SystemExit('Append annullato: eventi live già presenti.')
            c.execute('SELECT coalesce(max(delivery_id), 0) FROM raw_events')
            start = c.fetchone()[0]
            c.executemany('INSERT INTO raw_events VALUES (%s,%s::jsonb)',
                          [(start+i, json.dumps(e)) for i,e in enumerate(events, 1)])
            c.executemany('INSERT INTO orders VALUES (%s,%s,%s,%s,%s,%s)',
                          [(start+r[0], *r[1:]) for r in rows])
            c.executemany('INSERT INTO ingestion_errors VALUES (%s,%s,%s)',
                          [(start+r[0], *r[1:]) for r in errors])
            measured = db_metrics(conn)
            if measured != live_expected(expected):
                raise RuntimeError('Metriche inattese: transazione annullata')
            c.execute('SELECT delivery_id,payload FROM raw_events ORDER BY delivery_id')
            deliveries = c.fetchall()
            c.execute('SELECT delivery_id,event_id,order_id,customer_id,amount_cents,occurred_at FROM orders ORDER BY delivery_id')
            all_rows = c.fetchall()
            c.execute('SELECT delivery_id,code,detail FROM ingestion_errors ORDER BY delivery_id')
            all_errors = c.fetchall()
            if [i for i,_ in deliveries] != list(range(1, len(deliveries)+1)):
                raise RuntimeError('Identificativi non contigui: transazione annullata')
    export([e for _,e in deliveries], all_rows, all_errors, 'incident-live', measured,
           'PostgreSQL append committed and metrics verified')
    print(json.dumps(dict(scenario='incident-live', added_delivery_ids=[start+i for i in range(1,4)],
                         metrics=measured), indent=2))


def main():
    p=argparse.ArgumentParser(); p.add_argument('--reset',action='store_true'); p.add_argument('--scenario',choices=['baseline','incident'],default='incident'); p.add_argument('--verify',action='store_true'); p.add_argument('--offline',action='store_true',help='Generate Python-only evidence; never claim DB verification')
    p.add_argument('--append-demo', action='store_true', help='Aggiunge tre consegne reali allo scenario incident, senza reset')
    a=p.parse_args()
    if a.append_demo and (a.reset or a.offline or a.verify or a.scenario != 'incident'):
        p.error('--append-demo va usato da solo')
    expected=json.loads((ROOT/'validation/expected-results.json').read_text())
    if a.append_demo:
        append_demo(expected); return
    if a.verify:
        with connect() as conn:
            actual=db_metrics(conn)
        known = dict(expected, **{'incident-live': live_expected(expected)})
        matches=[name for name,value in known.items() if value==actual]
        if not matches: raise SystemExit('FAIL: '+json.dumps(actual))
        print('PASS database scenario='+matches[0]+' '+json.dumps(actual)); return
    if not a.reset and not a.offline: p.error('Use --reset to replace demo tables, or --verify')
    events=generate(a.scenario); rows,errors=consume(events,a.scenario)
    measured=metrics(events,rows,errors)
    assert measured==expected[a.scenario], (measured,expected[a.scenario])
    if not a.offline:
        from psycopg import sql
        env=dict(line.split('=',1) for line in (ROOT/'.env').read_text().splitlines() if '=' in line)
        with connect() as conn:
            with conn.cursor() as c:
                for role,key in [('demo_reader','READER_PASSWORD'),('quality_reader','QUALITY_PASSWORD')]:
                    c.execute('SELECT 1 FROM pg_roles WHERE rolname=%s',(role,))
                    if not c.fetchone(): c.execute(sql.SQL('CREATE ROLE {} LOGIN').format(sql.Identifier(role)))
                    c.execute(sql.SQL('ALTER ROLE {} PASSWORD {}').format(sql.Identifier(role),sql.Literal(env[key])))
                    c.execute(sql.SQL('ALTER ROLE {} SET default_transaction_read_only = on').format(sql.Identifier(role)))
                    c.execute(sql.SQL('ALTER ROLE {} SET statement_timeout = \'5s\'').format(sql.Identifier(role)))
                c.execute((ROOT/'sql/schema.sql').read_text())
                c.executemany('INSERT INTO raw_events VALUES (%s,%s::jsonb)',[(i,json.dumps(e)) for i,e in enumerate(events,1)])
                c.executemany('INSERT INTO orders VALUES (%s,%s,%s,%s,%s,%s)',rows)
                c.executemany('INSERT INTO ingestion_errors VALUES (%s,%s,%s)',errors)
            assert db_metrics(conn)==expected[a.scenario]
            # Check persisted records and JSON against the producer/consumer output,
            # so HTML samples are evidence of committed storage, not just intentions.
            with conn.cursor() as c:
                c.execute('SELECT delivery_id,event_id,order_id,customer_id,amount_cents,occurred_at FROM orders ORDER BY delivery_id')
                assert c.fetchall()==rows
                c.execute('SELECT delivery_id,payload FROM raw_events ORDER BY delivery_id')
                assert c.fetchall()==list(enumerate(events,1))
        origin='PostgreSQL queries verified against expected-results'
    else: origin='OFFLINE Python simulation; PostgreSQL NOT verified'
    export(events,rows,errors,a.scenario,measured,origin)
    print(json.dumps(dict(origin=origin,scenario=a.scenario,metrics=measured),indent=2))
if __name__=='__main__': main()
