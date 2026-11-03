# Claude Desktop su Mac
1. Completare avvio rapido e `python scripts/configure.py`. Gli script non toccano le impostazioni Desktop.
2. In Claude Desktop: Impostazioni → Sviluppatore → Modifica configurazione. File macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`.
3. Fare backup della configurazione esistente. Unire le due voci in `.local/claude_desktop_config.json` al suo oggetto `mcpServers`, senza cancellare server esistenti. I path sono assoluti e generati dal repository reale, anche su Mac Intel/Apple Silicon. Le credenziali sono solo nei wrapper .local 0700, non in Git. Non usare `${VAR}` nel JSON Desktop aspettandosi espansione shell.
4. Chiudere Claude con Cmd-Q e riaprire. Abilitare solo DBHub e filesystem evidence per la demo 2.
5. Chiedere elenco tool: DBHub deve esporre strumenti di introspezione e SQL; filesystem deve riportare SOLO la radice evidence con `list_allowed_directories`. Provare SELECT count(*) FROM orders e lettura delle prime righe dei file. Una richiesta di leggere `presenter/queries.sql` deve fallire: se riesce, fermare demo e correggere radici/connector.

Il server filesystem ufficiale include anche operazioni di scrittura: la radice limita il perimetro, non rende i file immutabili. Non autorizzare scritture, tenere una copia e rigenerare con seed in caso di modifiche. Non aggiungere altri connettori con accesso al repository. Il DB di sola lettura è imposto da GRANT PostgreSQL, indipendentemente dal prompt. Il wrapper DBHub usa DSN da ambiente e config/dbhub.toml: readonly=true, max_rows=100, timeout 5 secondi, trasporto stdio, nessuna porta HTTP.

Installazione server via npx al primo avvio: richiede rete. Sono fissate le versioni DBHub 1.5.1 e filesystem 2.1.0 nei file generati. Per controllare nuove versioni (senza aggiornare automaticamente) usare `npm view @bytebase/dbhub version` e `npm view @modelcontextprotocol/server-filesystem version`, poi fissare quelle versioni nei wrapper/config generati e provarle nuovamente. Non aggiornare pacchetti prima della sessione.

## DAB 2.0: percorso opzionale con verifica preliminare
```sh
dotnet tool install Microsoft.DataApiBuilder --tool-path .local/tools --version 2.0.12
.local/tools/dab --version
python scripts/validate_dab.py
```
`scripts/validate_dab.py` carica la variabile richiesta senza stamparne il valore. Il template usa lo stesso PostgreSQL, quality_reader, sola vista, chiave delivery_id e azione read. `key-fields` è deprecato ma è stato accettato dalla versione 2.0.12; `custom-tool: false` è esplicito per evitare l'errore allOf del validatore sulla vista. I prove locali hanno verificato initialize, tools/list, describe_entities, read_records e rifiuto dell'entità raw_events. Ripetere prima dell’intervento e verificare anche nel client Desktop.

Unire `.local/claude-dab-fragment.json` al JSON Desktop solo dopo la verifica preliminare. La documentazione Microsoft usa `dab start --mcp-stdio role:anonymous --config ... --LogLevel Error`; stdio non apre HTTP e usa autenticazione Simulator locale. Non presentarlo come autenticazione di produzione.

Fonti ufficiali consultate 2026-11-03:
- https://github.com/bytebase/dbhub/blob/main/docs/config/command-line.mdx (DSN ambiente e stdio)
- https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem (radici e tool)
- https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/stdio-transport
- https://learn.microsoft.com/en-us/azure/data-api-builder/configuration/entities
- https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/overview
La documentazione descrive DAB con PostgreSQL come fornitore, ma ciò non prova il funzionamento della specifica combinazione MCP/view. In assenza di prova locale usare l’alternativa per la sicurezza documentato.

### Ambiente di esecuzione DAB e prove riproducibili
DAB 2.0.12 richiede .NET/ASP.NET Core 8. Il wrapper imposta DOTNET_ROOT=.local/dotnet. Se .NET 8 non è già disponibile:
```sh
mkdir -p .local/dotnet
curl -fsSL https://dot.net/v1/dotnet-install.sh -o .local/dotnet-install.sh
sh .local/dotnet-install.sh --channel 8.0 --runtime aspnetcore --install-dir .local/dotnet --no-path
python scripts/configure.py
python scripts/mcp_probe.py dab --call describe_entities --arguments '{}'
python scripts/mcp_probe.py dab --call read_records --arguments '{"entity":"OrderQuality","first":3}'
python scripts/mcp_probe.py dab --call read_records --arguments '{"entity":"raw_events","first":1}'
python scripts/mcp_probe.py dbhub --call execute_sql --arguments '{"sql":"SELECT count(*) FROM orders"}'
python scripts/mcp_probe.py dbhub --call execute_sql --arguments '{"sql":"UPDATE orders SET amount_cents=0 WHERE false"}'
python scripts/mcp_probe.py filesystem --call list_allowed_directories
```
Lo strumento di prova stampa risposte JSON-RPC; una chiamata MCP negata è un esito previsto, non un successo di lettura. La prova in Claude Desktop rimane manuale.

## Conoscenza del progetto collegata a GitHub
In alternativa al caricamento manuale, nel progetto «Data & AI Builders Conference 2026» scegliere Contesto → Aggiungi file → GitHub e selezionare il repository `Ricciolo/dataaibuildersconf26` e il ramo di riferimento. Includere esclusivamente `knowledge/core/` e `knowledge/extended/`. Le istruzioni del progetto restano nel campo dedicato; i dati e i registri locali restano accessibili tramite MCP.

La connessione importa i contenuti selezionati nella conoscenza del progetto. Le modifiche devono prima essere pubblicate su GitHub; usare poi il comando di sincronizzazione di Claude per acquisirle. Non viene letto il repository locale e la sincronizzazione non è una prova di attivazione RAG. Non selezionare l'intero repository o le cartelle del relatore e della validazione.

I Markdown sono in italiano. Per passare dal caricamento manuale a GitHub, verificare prima il collegamento e il contenuto selezionato; rimuovere poi dal contesto le copie caricate in precedenza, conservandone gli originali locali. Evitare due versioni attive nella configurazione finale.

Riferimento: https://support.claude.com/en/articles/10167454-use-the-github-integration
