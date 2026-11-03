-- Eseguire con demo_reader. Incident: 3060,3000,1530,60,1020.
SELECT count(*) orders, count(DISTINCT event_id) distinct_events,
 count(*) FILTER(WHERE missing_customer) missing_customer,
 count(*)-count(DISTINCT event_id) duplicate_excess,
 count(*) FILTER(WHERE timestamp_delta_seconds<>0) timestamp_shifted
FROM v_order_quality;
SELECT payload->>'schemaVersion' version, count(*),count(*) FILTER(WHERE o.customer_id IS NULL)
FROM raw_events r JOIN orders o USING(delivery_id) GROUP BY 1;
SELECT event_id,count(*) FROM orders GROUP BY 1 HAVING count(*)>1 ORDER BY 1 LIMIT 5;
SELECT * FROM v_order_quality WHERE timestamp_delta_seconds<>0 ORDER BY delivery_id LIMIT 5;
SELECT o.*,r.payload FROM orders o JOIN raw_events r USING(delivery_id) WHERE delivery_id IN(1,1501,3001);
