# Matrice per la risoluzione dei problemi
## Livello di connessione
L'assenza del socket Docker locale può indicare che il motore dei contenitori non è in esecuzione. Una connessione TCP rifiutata può dipendere dal database non pronto o da una porta errata. Un errore di autenticazione è distinto: confrontare la generazione delle credenziali locali e il ciclo di vita del volume senza mostrare segreti. Modificare la password in Compose non ruota automaticamente quella di un volume PostgreSQL già inizializzato.

## Livello degli strumenti
Uno strumento assente in Claude può dipendere da un percorso di comando non valido, un'installazione fallita del pacchetto o un processo che ha scritto testo estraneo al protocollo su `stdout`. Riavviare il client Desktop dopo modifiche alla configurazione dei server `stdio`. Usare `stderr` per la diagnostica. Un'interrogazione diretta del database riuscita non dimostra che sia riuscita anche una chiamata MCP.

## Livello documentale — KB-INDEX-24
Attendere l'elaborazione dei file prima di provare domande sulla conoscenza. Usare una chat nuova dopo l'aggiunta dei documenti e verificare i nomi delle fonti nella risposta. Una citazione corretta non dimostra da sola il recupero documentale: può derivare da documenti già nel contesto. Se non sono visibili un'operazione di ricerca o un indicatore RAG attivo, descrivere la demo solo come uso della conoscenza documentale.

## Informazioni per la richiesta di assistenza
Riportare versione dell'applicazione, struttura della configurazione con valori segreti rimossi, comando di riproduzione ed errore depurato dai dati riservati. Non allegare l'intera cartella personale o lo script di connessione. Non diagnosticare problemi di trasformazione dei dati soltanto da un errore di avvio degli strumenti.
