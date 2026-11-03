# Convenzioni per le interrogazioni PostgreSQL
## SQL-AGG-19 — ispezione delimitata
Preferire conteggi aggregati e distribuzioni prima dei campioni di righe. Usare elenchi espliciti di colonne e `LIMIT` per i campioni. Una query non è corretta solo perché viene eseguita. Un conteggio con funzione finestra per evento comprende tutte le consegne dell'evento; una misura delle righe in eccesso sottrae le identità evento distinte dal totale delle righe. Sono quantità diverse.

## Percorsi JSONB
In PostgreSQL `->` restituisce JSON, mentre `->>` restituisce testo. Un percorso annidato può essere estratto con `#>>`. I percorsi mancanti restituiscono SQL NULL. Validare la versione prima di scegliere il percorso. Non sostituire NULL con un identificativo cliente inventato. In un sistema di acquisizione, convertire `occurredAt` in `timestamptz` solo dopo averne verificato la validità rispetto al contratto.

## Fusi orari
`SET TIME ZONE` influisce sulla visualizzazione e su alcune operazioni di troncamento delle date. `AT TIME ZONE` cambia rappresentazione in base al tipo dell'operando: esaminare i tipi esplicitamente. Per confrontare istanti, mantenere entrambi gli operandi come `timestamptz`. Per una data aziendale, estrarre la data dopo la conversione in `Europe/Rome`.

## Revisione sicura
La sola lettura è un confine di autorizzazione, non una garanzia di basso costo delle query. Mantenere limiti di tempo per le istruzioni e contenere le unioni tra grandi tabelle. `EXPLAIN ANALYZE` esegue l'istruzione: non usarlo con leggerezza su scritture. Le sessioni diagnostiche della demo usano un limite di cinque secondi per istruzione.
