# Riferimento per le corrispondenze verso il modello di destinazione
## MAP-ORDER-01 — trasformazione approvata
Le versioni v1 e v2 rappresentano lo stesso formato di record di destinazione. `eventId` corrisponde a `event_id`; `orderId` a `order_id`; `amountCents` a `amount_cents`. `schemaVersion` seleziona il formato sorgente: la versione 1 usa `customerId`, la versione 2 usa `customer.id`. La trasformazione approvata accetta entrambe le versioni documentate. Se sono presenti entrambi i formati, prevale la versione dichiarata; un identificativo in conflitto richiede l'isolamento del record. Non scegliere silenziosamente la prima stringa non vuota.

## MAP-TIME-04 — semantica temporale
Interpretare lo scostamento dal fuso UTC esplicito prima della conversione in UTC. Conservare la stringa originale in `raw_events.payload`, così da poter ricalcolare l'istante in modo indipendente. Il campo di destinazione `occurred_at` è di tipo `timestamptz`. Il fuso della sessione influisce sulla visualizzazione SQL, ma l'istante non deve cambiare. Un orario locale visualizzato, da solo, non dimostra un errore di conversione. Confrontare valori `timestamptz`, non prefissi di stringhe.

## Valori mancanti e sconosciuti
La colonna fisica `customer_id` ammette NULL per consentire l'ispezione di consegne materializzate parzialmente. L'accettazione di business richiede comunque l'identità del cliente. Non sostituirla con `orderId`, con il cliente del record precedente o con una stringa come `UNKNOWN`. Ogni correzione proposta deve indicare la propria fonte ed essere revisionata prima di modificare le righe persistite.

## Fonte autorevole
Questo documento descrive il comportamento richiesto, non dimostra cosa faccia attualmente un consumatore. La diagnosi deve esaminare righe e contenuti effettivi. La demo locale mantiene intenzionalmente SQL essenziale e non installa un motore di trasformazione.
