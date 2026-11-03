# Specifica API di consegna — interfaccia di riferimento
Stato: contratto di progettazione per un'integrazione e-commerce. L'implementazione della conferenza usa un solo script Python; non è distribuito alcun servizio HTTP.

## Struttura del messaggio e conferma di ricezione
Un adattatore di produzione accetterebbe `POST /order-events` con un singolo oggetto JSON. `Content-Type` è `application/json`, con codifica UTF-8. La conferma indica l'accettazione persistente della consegna, non il completamento delle analisi a valle. `eventId` è l'identità semantica immutabile assegnata dal produttore; `delivery_id` è assegnato dall'archivio. Riutilizzare un `eventId` con un contenuto diverso è un conflitto da esaminare. `orderId` è un riferimento di business, non l'identificativo della conferma di trasporto.

## Classificazione delle risposte di riferimento
202 indica accettazione per elaborazione asincrona; 400 indica JSON malformato o un tipo obbligatorio non supportato; 409 indica un conflitto di identità; 413 un contenuto troppo grande; 429 una limitazione delle richieste; 503 un'indisponibilità temporanea. Questi stati sono specifiche per un futuro adattatore, non codici di registro emessi da `seed.py`. Non dedurre un errore HTTP dalla simulazione locale.

## Limite dei tentativi — API-RET-17
Il produttore di riferimento ritenta soltanto in caso di 429/503 o conferma di ricezione incerta, per un massimo di quattro tentativi aggiuntivi con attese di 1, 2, 4 e 8 secondi. L'intestazione `Retry-After` ha precedenza, con un limite massimo di 30 secondi. Il consumatore deve preservare l'identità dell'evento durante i tentativi. Un 400 o 409 non deve avviare questo ciclo. L'esecuzione locale non introduce attese reali o un servizio HTTP di riconsegna.

## Gestione del contenuto
Gli importi sono interi di centesimi; le rappresentazioni monetarie decimali non rientrano nel contratto. Le proprietà facoltative sconosciute possono restare nel JSON originale, ma non devono diventare colonne SQL senza revisione. Nessun token di autenticazione deve essere inserito nel corpo dell'evento. Se implementata, l'interfaccia di riferimento richiede TLS e autenticazione del servizio; la demo non espone indirizzi pubblici e non usa chiavi API.
