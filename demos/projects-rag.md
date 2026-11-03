# Demo 1 — Chat, Knowledge e RAG nativo
## Cosa è verificato nelle fonti, 2026-11-03
Anthropic descrive attivazione automatica quando la conoscenza si avvicina o supera la finestra di contesto, capacità fino a 10 volte, indicatore visivo di attivazione RAG e uso di un strumento di ricerca nella conoscenza del progetto. Non pubblica una soglia numerica stabile e non offre un interruttore per forzarla. La pagina specifica RAG elenca piani a pagamento Pro, Max, Ultra, Team ed Enterprise; la pagina generale Projects elenca Pro, Max, Team ed Enterprise senza Ultra. Verificare disponibilità nel proprio account: l'interfaccia può variare per piano e distribuzione graduale. Non fare affidamento su soglie raccontate da utenti o sul numero di file.

Fonti ufficiali:
- https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects
- https://support.claude.com/en/articles/9517075-what-are-projects
- https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- https://support.claude.com/en/articles/8241126-what-kinds-of-documents-can-i-upload-to-claude-ai

## Limiti file
La pagina sul caricamento dei file distingue Project (30 MB per file, nessun tetto numerico di file dichiarato, limiti di contenuto estratto/contesto) e chat (500 MB per file, fino a 20 file): non trasferire i limiti chat ai Projects. La pagina RAG descrive capacità estesa fino a 10×; non è una quota universale in MB né una soglia garantita. Tutti i 17 Markdown di questo corpus sono molto sotto 30 MB (23.798 byte complessivi nella versione italiana). Non sono un corpus prossimo al limite di contesto: l’alternativa è un esito previsto, non un errore da nascondere. Se il caricatore non accetta .md, esportare la stessa identica versione come testo .txt, annotando il nome nel registro; non caricare due copie.

## Corpus e limite esplicito
Il corpus comprende cinque documenti essenziali e dodici documenti estesi distinti: API di riferimento, mapping approvato, ciclo di vita, cronologia delle modifiche, rielaborazione, diagnostica, validazioni, accesso, SQL, vista, risoluzione dei problemi e rilascio. Le specifiche API/retention sono requisiti di riferimento: non aggiungono servizi al demo. Nessun documento dichiara l'incidente o i suoi totali. Le regole descrivono comportamento previsto, non confermano che il consumatore lo implementi.

Questo corpus volutamente compatto NON garantisce la soglia RAG. Aumentarlo con ripetizioni o dati inutili falserebbe la dimostrazione. Se non basta e non esiste altra documentazione reale autorizzata, usare l’alternativa. Un prompt che dice «cerca» e una risposta corretta non provano il recupero documentale.

## Un solo Project, configurazione preferita
1. In Claude Desktop, area Chat → Projects, creare «Data & AI Builders Conference 2026». Non usare una funzione omonima di Claude Code/beta come sostituto della conoscenza Chat.
2. Disabilitare web, MCP e altri connettori per questa prova. Ridurre contaminazione da memoria/chat pregresse, usando chat nuova o temporanea fuori Project per il confronto iniziale, dove disponibile. Annotare modello, piano e versione app.
3. Incollare le istruzioni da public/project-instructions.md. Caricare esattamente i file elencati nella chiave `core` di project-upload-manifest.json. Attendere completamento elaborazione. Non caricare manifest, demos, script, expected-results o report.
4. In una chat nuova eseguire il prompt core sotto, confrontandolo con la Chat senza contesto.
5. Aggiungere gli esatti dodici file nella chiave `extended` del manifest, attendere elaborazione. Aprire una chat nuova e osservare l'indicatore RAG. Eseguire il prompt esteso e aprire il dettaglio del tool di ricerca, se mostrato.
6. Non rimuovere file durante la dimostrazione dal vivo: Anthropic segnala che tornando sotto soglia il Project può riconvertirsi al contesto.

Per il palco preparare tutto in anticipo. Un singolo Project permette il confronto in sequenza durante la prova generale, ma non congela due stati dal vivo: mostrare il confronto core già registrato dichiarandolo, poi usare lo stato esteso dal vivo. Se occorrono entrambi gli stati dal vivo, usare due Projects identici nelle istruzioni: «Eventi ordine — documenti essenziali» carica solo core; «Eventi ordine — documentazione estesa» carica core + extended. Questa è un'opzione per ripetibilità, non un requisito RAG. Non abilitare MCP fino alla Demo 2.

## Prompt copiabili e risposte attese private
### Chat senza contesto e Project core — identico
«Per il nostro sistema order-event, quale campo rappresenta il cliente in ogni versione, come vanno trattati retry e timestamp, e quali informazioni ti mancano? Cita solo documenti realmente disponibili e non ipotizzare risultati del database.»
Chat: non conosce le convenzioni interne; deve dichiarare che mancano contratti/regole. Non penalizzare conoscenza generale corretta. Core: customerId in v1, customer.id in v2, una materializzazione per eventId e istante preservato con offset; fonti contract-v1.md, contract-v2.md, business-rules.md. Non deve diagnosticare l'incidente senza misure.

### Documentazione estesa — prova del recupero documentale
«Cerca nella conoscenza del Project le regole API-RET-17, RB-REPLAY-23 e RET-RAW-18. Per ciascuna riporta procedura, eccezioni e documento/sezione di origine. Distingui specifiche di riferimento da capacità effettivamente implementate nel demo. Se non trovi una regola dillo; non usare web o tool esterni.»
Atteso: solo 429/503/ack ignoto, quattro retry aggiuntivi 1/2/4/8 secondi, Retry-After prioritario con limite di 30 secondi (api-delivery-spec.md); replay con intervallo, impronta, mapping, ambiente, prova senza scritture e ruoli distinti (runbook-replay.md); conservazione 30/14/90 giorni e vincolo legale che sospende cancellazione del perimetro (operations-access.md). API, replay operativo e conservazione automatica non sono implementati nel demo.

### Controllo di assenza
«Qual è il requisito ufficiale per schemaVersion 3? Cita una fonte, oppure dichiara che non è definito.»
Atteso: non definito, contract-versioning.md. Non inventare un v3.

## Verifica della prova generale
Registrare in presenter/rag-rehearsal.md data, piano/modello/app, nomi file dal manifest, stato elaborazione, indicatore visivo, domanda, tool di ricerca osservato e riferimenti restituiti. Salvare immagini dello schermo depurate dai dati riservati se utile, senza credenziali. Ripetere domanda estesa in chat nuova una seconda volta e provare il controllo di assenza. Non basarsi su autoaffermazioni del modello («ho usato RAG»).

Verifica RAG superata: indicatore abilitato e chiamata visibile al strumento di ricerca nella conoscenza del progetto per la domanda, con fonti pertinenti e risposta coerente. Indicatore da solo prova modalità abilitata ma non recupero documentale per quella risposta. Se il tool non è ispezionabile nell'interfaccia disponibile, dichiarare che il recupero documentale della singola risposta non è verificabile. Citazioni senza tool = uso delle fonti documentali osservato, non prova RAG. Non esiste qui accesso automatico al piano o allo stato Claude del relatore.

## Alternativa corretta
Se il corpus non attiva RAG, mostrare il confronto Chat/core e la domanda estesa come ricerca documentale con Knowledge, dicendo: «La knowledge è stata utilizzata; questa sessione non dimostra il recupero documentale RAG. Il prodotto lo attiva automaticamente alla propria soglia». Mostrare la fonte ufficiale per spiegare la funzionalità. Nessuna animazione di tool finta, nessuna pretesa che aprire un Markdown equivalga a RAG. Conservare i dieci minuti tagliando la domanda aggiuntiva, non aggiungendo infrastruttura.
