# Procedura operativa — approvazione della rielaborazione
## Ambito
Rielaborare significa processare nuovamente dati sorgente già accettati, non modificare l'evento originale per ottenere un risultato analitico desiderato. Lo script della demo è un simulatore ripristinabile e non implementa un comando di rielaborazione di produzione.

## RB-REPLAY-23 — registrazione dell'approvazione
La richiesta deve indicare un intervallo delimitato di consegne, l'impronta della copia sorgente, la versione della trasformazione, l'ambiente di destinazione e la riconciliazione della prova senza scritture. Approva il responsabile della piattaforma dati; esegue un operatore distinto. Il responsabile delle analisi clienti approva se cambiano i totali per giornata aziendale. Un messaggio Slack privo di questi campi non costituisce una registrazione di approvazione.

## Prova senza scritture
Calcolare il numero di consegne ricevute e di eventi distinti prima di proporre scritture. Conservare le consegne duplicate come evidenza; definire la politica dell'evento canonico separatamente dalla storia del trasporto. Verificare se una trasformazione cambia l'identità cliente o l'attribuzione temporale. La prova non deve modificare `raw_events`.

## Ripristino e completamento
Documentare come ripristinare lo stato analitico e quali rapporti a valle ricalcolare. Confrontare gli aggregati prima e dopo, conservare l'elenco dei record rifiutati e ottenere l'approvazione. Il solo completamento del comando senza errori non dimostra il recupero. Nell'ambiente della conferenza usare i ripristini documentati degli scenari `baseline` e `incident`, senza invocare procedure non implementate.
