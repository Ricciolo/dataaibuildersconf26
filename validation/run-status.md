# Prove effettivamente eseguite — 2026-11-03

Repository inizialmente vuoto e pulito; nessun file utente sovrascritto, nessun commit o push. Alla consegna tutti i materiali sono nuovi file locali non tracciati. Credenziali, ambienti, runtime e risultati generati sono ignorati da Git.

## Verifiche locali superate
- Python 3.9.6, psycopg 3.2.13 installato in .venv.
- Docker/OrbStack: PostgreSQL 17.6 avviato su 127.0.0.1:55432, controllo di integrità superato.
- unittest: due test su invarianti baseline/incident, determinismo, confine v1/v2, offset e identità retry.
- Seed baseline + --verify: 3000 righe/eventi, zero anomalie.
- Seed incident + --verify: 3060 raw/orders, 3000 eventi distinti, 1530 customer NULL, 60 righe in eccesso, 1020 timestamp alterati, 1530 diagnostiche.
- Confronto completo delle righe orders e JSON grezzo persistiti con il generatore; non solo conteggi.
- security_check: SELECT vista consentita a entrambi i ruoli; UPDATE e CREATE negati anche disabilitando il default di sola lettura; raw_events negato a quality_reader.
- DBHub 1.5.1 stdio: initialize, tools/list, search_objects restituisce tre tabelle; execute_sql SELECT restituisce 3060, UPDATE WHERE false restituisce READONLY_VIOLATION. Configurazione finale con readonly=true/max_rows=100.
- Filesystem 2.1.0 stdio: initialize, tools/list, radice esclusiva public/evidence, prima riga JSONL leggibile; presenter/queries.sql negato perché fuori radice. Il server espone anche tool di scrittura all'interno della radice.
- DAB 2.0.12 con runtime ASP.NET Core 8.0.33 installato solo in .local: validazione superata; initialize/tools/list PASS; describe_entities espone solo OrderQuality con READ; read_records restituisce righe reali della vista PostgreSQL; raw_events restituisce EntityNotFound. REST/GraphQL disabilitati. Il validatore avvisa che manca una definizione esplicita fields; read_records è stato comunque provato. key-fields è deprecato ma accettato.
- Modalità offline provata e marcata come simulazione Python; poi ripristinato incident su PostgreSQL.
- Manifest: 17 file di conoscenza esistenti, tutti sotto 30 MB; circa 19 KB nella versione originale inglese. Nessuna soluzione/expected-results inclusa nell'elenco upload.
- HTML: report incorporato, tre campioni, sintassi JavaScript verificata con Node, nessuna dipendenza/fetch/URL esterna; Python compileall passato.

## Da provare manualmente
- Unire le voci generate alla configurazione Claude Desktop senza sostituire server esistenti; riavviare e controllare strumenti/permessi nel client.
- Creare Project Chat, caricare core/extended secondo manifest e impostare istruzioni.
- Osservare piano, indicizzazione, indicatore RAG e chiamata reale al strumento di ricerca nella conoscenza del progetto. Nessuna prova nell’interfaccia per RAG è stata eseguita. La soglia non è pubblicata e il corpus compatto NON garantisce attivazione; usare alternativa solo conoscenza documentale finché non passa la verifica preliminare.
- Eseguire prompt dal vivo e Artifact in Claude, controllando risultati e fonti.
- Aprire HTML localmente per controllo visivo e dei filtri: il browser automatizzato ha negato file:// per policy, senza tentativi di aggiramento. I controlli statici non sostituiscono il controllo visivo.

## Stato finale
PostgreSQL resta avviato nello scenario incident. Report verificato e alternativa in presenter/generated. Non sono state modificate impostazioni Claude o risorse remote.
