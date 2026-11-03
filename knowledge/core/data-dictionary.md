# Dizionario dei dati

- `raw_events`: `delivery_id` è la chiave primaria; `payload` contiene l'evento originale in formato JSONB.
- `orders`: `delivery_id` è chiave primaria ed esterna; gli altri campi sono `event_id`, `order_id`, `customer_id` (colonna fisica che ammette NULL), `amount_cents` e `occurred_at` di tipo `timestamptz`.
- `ingestion_errors`: `delivery_id`, `code`, `detail`.
- `v_order_quality`: campi dell'ordine più `missing_customer` (booleano), `event_copies` (numero di righe per `event_id`) e `timestamp_delta_seconds` (differenza rispetto all'istante della sorgente).

La possibilità di memorizzare NULL non prevale sui requisiti di business.
