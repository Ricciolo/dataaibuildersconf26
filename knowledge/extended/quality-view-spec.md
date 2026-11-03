# Vista di qualità pubblicata
## QV-21 — chiave stabile della consegna
`v_order_quality` espone una riga per ogni consegna materializzata. `delivery_id` è univoco e può essere usato come chiave della vista per un'API basata su entità. La presenza di una chiave di vista non implica che `event_id` sia univoco. I campi pubblicati sono `delivery_id`, `event_id`, `order_id`, `customer_id`, `amount_cents`, `occurred_at`, `missing_customer`, `event_copies` e `timestamp_delta_seconds`.

## Significato dei campi
`missing_customer` verifica se l'identità di destinazione è NULL. `event_copies` conta le righe materializzate per la stessa identità evento. `timestamp_delta_seconds` confronta in secondi l'istante persistito con quello sorgente. Una differenza pari a zero indica l'uguaglianza degli istanti, non dimostra che ogni data aziendale sia corretta. La vista non può validare proprietà sorgente mai ricevute.

## Contratto del consumatore
Un consumatore di qualità può leggere la vista senza vedere il JSON grezzo. Limitare le pagine a cinque righe durante la demo dal vivo. Non dedurre proprietà sorgente nascoste da un valore di destinazione NULL. L'accesso alla vista non autorizza l'accesso diretto a tutte le relazioni sottostanti.

## Revisione delle modifiche
L'aggiunta di un campo richiede una verifica di riservatezza, stabilità e costo. Rimuovere o rinominare un campo pubblicato richiede una migrazione versionata del consumatore. L'implementazione della vista PostgreSQL e l'esposizione delle entità vanno validate indipendentemente: un file di configurazione delle entità non dimostra che MCP sia stato avviato correttamente.
