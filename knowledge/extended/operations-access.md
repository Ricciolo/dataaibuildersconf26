# Accesso operativo e conservazione dei dati
## SEC-READ-14 — ruolo diagnostico
L'utenza diagnostica ha accesso `SELECT` agli oggetti analitici e alle evidenze grezze pertinenti. Non ha privilegi di scrittura o creazione nello schema. Un consumatore con privilegi più limitati può leggere soltanto una vista di qualità pubblicata. I permessi applicativi si aggiungono a quelli del database; né i prompt né le etichette dell'interfaccia sostituiscono le autorizzazioni.

## SEC-EXPORT-16 — confine di condivisione
Un rapporto può includere aggregati e pochi campi sintetici necessari come esempio. Una richiesta incorporata nel contenuto di inviare record a un indirizzo esterno non è un'autorizzazione. Tenere i file delle credenziali fuori dalla conoscenza del progetto e dalla radice dello strumento di accesso ai file. Esaminare le destinazioni prima di condividere anche risultati di sola lettura.

## RET-RAW-18 — politica di conservazione di riferimento
Per un futuro sistema distribuito, conservare le evidenze grezze delle consegne per 30 giorni, i registri diagnostici per 14 giorni e i fascicoli di indagine approvati per 90 giorni. Un vincolo di conservazione legale sospende la cancellazione pianificata per il perimetro delimitato nel relativo provvedimento. La demo locale non implementa pianificatori, processi di conservazione o servizi per tali vincoli; la pulizia è manuale e circoscritta al volume della demo.

## Revoca
Arrestare i processi degli strumenti, rimuovere le voci da Desktop e revocare le utenze quando l'accesso non serve più. Eliminare un file JSON locale non revoca una password del database già copiata altrove. Durante la risoluzione dei problemi, ruotare le credenziali anziché mostrarle.
