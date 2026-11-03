"""Assert PostgreSQL enforcement, including after disabling session read-only default."""
import psycopg
from pathlib import Path
root=Path(__file__).resolve().parents[1]
env=dict(line.split('=',1) for line in (root/'.env').read_text().splitlines() if '=' in line)
for role,key in [('demo_reader','READER_PASSWORD'),('quality_reader','QUALITY_PASSWORD')]:
 with psycopg.connect(host='127.0.0.1',port=55432,dbname='orders_demo',user=role,password=env[key],autocommit=True) as conn:
  conn.execute('SELECT * FROM v_order_quality LIMIT 1').fetchall()
  conn.execute('SET default_transaction_read_only=off')
  denied=['UPDATE orders SET amount_cents=0 WHERE false','CREATE TABLE public.forbidden_probe(id int)']
  if role=='quality_reader': denied.append('SELECT * FROM raw_events LIMIT 1')
  for query in denied:
   try: conn.execute(query)
   except psycopg.errors.InsufficientPrivilege: print(role,'DENIED',query)
   else: raise SystemExit('FAIL permission unexpectedly granted: '+query)
  print(role,'PASS allowed SELECT and denied operations')
