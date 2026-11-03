DROP VIEW IF EXISTS v_order_quality;
DROP TABLE IF EXISTS ingestion_errors, orders, raw_events;
CREATE TABLE raw_events (delivery_id integer PRIMARY KEY, payload jsonb NOT NULL);
CREATE TABLE orders (delivery_id integer PRIMARY KEY REFERENCES raw_events, event_id text NOT NULL,
 order_id text NOT NULL, customer_id text, amount_cents integer NOT NULL, occurred_at timestamptz NOT NULL);
CREATE TABLE ingestion_errors (delivery_id integer REFERENCES raw_events, code text NOT NULL, detail text NOT NULL);
CREATE VIEW v_order_quality AS
SELECT o.delivery_id, o.event_id, o.order_id, o.customer_id, o.amount_cents, o.occurred_at,
 o.customer_id IS NULL AS missing_customer,
 count(*) OVER (PARTITION BY o.event_id) AS event_copies,
 extract(epoch FROM (o.occurred_at - (r.payload->>'occurredAt')::timestamptz))::integer AS timestamp_delta_seconds
FROM orders o JOIN raw_events r USING(delivery_id);
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO demo_reader, quality_reader;
GRANT SELECT ON raw_events, orders, ingestion_errors, v_order_quality TO demo_reader;
GRANT SELECT ON v_order_quality TO quality_reader;
