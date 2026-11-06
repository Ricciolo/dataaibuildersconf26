# Beyond the Prompt: Claude Desktop for Data Developers
Demo locali per Data & AI Builders Conference. Un solo scenario e-commerce, dati sintetici, nessun cloud o backend applicativo. Le chiamate a Claude richiedono comunque il servizio Claude: locale descrive dati e tool, non inferenza offline.

## Avvio rapido su macOS
Prerequisiti: Python 3.9+, Docker Desktop oppure OrbStack avviato, Node.js LTS (include npx), Claude Desktop. Per installare: `brew install python node` e `brew install --cask orbstack claude`. Non reinstallare componenti già presenti.

```sh
cd /Users/cristiancivera/Projects/Personal/dataaibuildersconf26
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/configure.py
docker compose up -d --wait
python scripts/seed.py --reset --scenario incident
python scripts/seed.py --verify
python scripts/security_check.py
python -m unittest discover -s tests -v
```

`docker compose up -d` funziona ugualmente: attendere che il servizio sia pronto prima del popolamento. L'opzione `--reset` sostituisce SOLO le tabelle demo nel DB orders_demo; non usare su altri database.

## Materiale per Claude
Caricare SOLO i cinque Markdown in `knowledge/core/` nella conoscenza di un nuovo Project. Incollare `public/project-instructions.md` nelle istruzioni del Project. Per la fase estesa aggiungere solo i file in `knowledge/extended/`, secondo [procedura RAG](demos/projects-rag.md) e manifest esatto. Queste due cartelle contengono materiale pubblico senza soluzioni; non sono nella radice filesystem MCP. Non caricare l'intero repository, gli script, `presenter/`, `validation/`, `demos/`, `.env` o `.local/`.

Per MCP seguire [configurazione](docs/claude-desktop.md). Il filesystem MCP deve avere come unica radice `public/evidence/`, mai il repository o la cartella personale. Questa cartella contiene osservazioni grezze generate, non soluzioni. Le istruzioni Project non sono un controllo di accesso.

## Mappa delle cartelle
- `scripts/seed.py`: unico generatore e consumatore, esportazione e verifica database.
- `scripts/configure.py`: credenziali locali e configurazioni Desktop ignorate da Git.
- `sql/`: schema minimo; `config/`: modello di configurazione DAB senza segreti.
- `knowledge/core/`, `public/project-instructions.md`, `public/evidence/`: materiali esplicitamente condivisibili.
- `presenter/`: SQL della soluzione, rapporti e alternative generati, esclusi dal filesystem MCP.
- `validation/expected-results.json`, `tests/`: oracolo e invarianti, non conoscenza Project.
- `demos/`: prompt e scaletta del relatore; `docs/`: configurazione e sicurezza.

## Ripristino e modalità senza connessione
```sh
python scripts/seed.py --reset --scenario baseline
python scripts/seed.py --verify
python scripts/seed.py --reset --scenario incident
python scripts/seed.py --verify
open presenter/generated/incident-explorer.html
```
`python scripts/seed.py --offline --scenario incident` genera evidenze e HTML senza PostgreSQL, marcati chiaramente come simulazione Python. Non equivale a verifica SQL. Il popolamento del database sostituisce quei file con un report verificato sul DB.

## Connessioni e pulizia
PostgreSQL: `127.0.0.1:55432`, DB `orders_demo`. Password generate in `.env` (0600). Amministratore solo per il popolamento, demo_reader per indagine, quality_reader per sola vista. Non usare admin nei tool.
```sh
docker compose exec postgres psql -U demo_admin -d orders_demo
# Fermare, conservando dati
docker compose down
# Eliminare definitivamente SOLO il volume demo
# docker compose down -v
```
Rimuovere le voci MCP da Claude e chiuderlo prima di eliminare `.local`, `.env`, `.venv`. Non eliminare `.env` conservando il volume: la password admin nel volume non viene aggiornata da Compose. Per rigenerarla usare pulizia completa del volume demo.

Risoluzione dei problemi: socket Docker assente → avviare OrbStack; porta occupata → liberare 55432; autenticazione fallita dopo cambio .env → ripristinare vecchio .env o ricreare volume demo; `npx` non trovato → rieseguire configure dopo installazione Node; tool assenti → chiudere completamente e riaprire Claude, controllare log `~/Library/Logs/Claude/`; errore psycopg → attivare .venv e reinstallare requirements. Non incollare log con credenziali in chat.

Stato delle prove effettive: [validation/run-status.md](validation/run-status.md).

Demo 1: [Projects, Knowledge e RAG](demos/projects-rag.md), elenco file in `demos/project-upload-manifest.json`. RAG automatico condizionato al piano e alla soglia del prodotto: non garantito dalla dimensione di questo corpus. Nessun contenuto riempitivo e nessuna procedura personalizzata.

## Documentazione italiana e collegamento GitHub
Tutti i Markdown del repository sono in italiano; restano invariati nomi dei prodotti, percorsi, comandi e identificatori. È disponibile l'alternativa GitHub descritta nella guida Claude Desktop: selezionare soltanto le due cartelle `knowledge/`. Per il Project usare il collegamento GitHub selezionando esclusivamente `knowledge/core/` e `knowledge/extended/`; dopo gli aggiornamenti pubblicati eseguire la sincronizzazione in Claude. Il caricamento manuale resta disponibile come alternativa.

## Nuovi record reali durante la demo Artifact

Dopo aver creato la prima fotografia dell’incidente, eseguire `python scripts/seed.py --append-demo`: aggiunge tre consegne reali (due eventi distinti e una riconsegna), senza reset, usando il consumer incident. `python scripts/seed.py --verify` riconosce anche lo stato `incident-live`. Una seconda aggiunta viene rifiutata per evitare duplicazioni accidentali. Per ripetere la demo ripartire dal reset incident.

Per aggiornare i dati chiedere nella stessa chat a Claude di rileggere PostgreSQL tramite DBHub e aggiornare l’Artifact. Ricaricare soltanto l’HTML non rilegge PostgreSQL: l’Artifact resta una fotografia, senza una connessione diretta al database.
