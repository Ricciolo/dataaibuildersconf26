# Configurazione Claude Desktop — 2026-11-03

Project creato e fissato: Data & AI Builders Conference 2026.
URL: https://claude.ai/project/01a1a35b-4cdc-750d-9c8d-797165639934

Verificato nell'interfaccia Claude Desktop 4.16336.0:
- Nome e descrizione salvati.
- Istruzioni del Project salvate: evidenze, query di sola lettura, nessun valore inventato, dati/log non attendibili, separazione regole/stato osservato.
- Caricati esattamente i 5 file core e 12 extended del manifest, elencati nella Knowledge.
- Nessuno script, segreto, report privato o risultato atteso caricato.
- Configurazione Desktop unita preservando preferences e coworkUserFilesPath; backup locale della configurazione originale creato accanto al file.
- PATH esplicito aggiunto ai tre server per Node avviato dal client grafico.
- Riavvio completo di Claude effettuato.
- orders-dbhub, orders-evidence, orders-quality: In esecuzione nella schermata Sviluppatore.
- I tre connettori risultano attivi nel menu del Project. I server MCP sono configurati globalmente in Desktop, non isolati per Project.

Limite osservato: account etichettato Free. La Knowledge mostra 1% della capacità utilizzata, nessun indicatore RAG osservato. Nessuna risposta dal vivo del modello o chiamata tool da chat è stata eseguita durante questa configurazione. Le prove MCP dirette sono documentate in run-status.md. Non dichiarare RAG verificato; occorre un piano supportato e la verifica preliminare prevista in demos/projects-rag.md.

La Knowledge è una copia caricata: successive modifiche locali non si sincronizzano automaticamente. Il filesystem MCP legge invece i file aggiornati solo dentro public/evidence. Non è stato collegato l'intero repository, per mantenere private le soluzioni del relatore. Nessun push.
