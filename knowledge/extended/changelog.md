# Cronologia delle modifiche alle specifiche
Questa è la storia progettuale del sistema sintetico, non la cronologia di un incidente.

## 2026-04-10 · contratto v1
Definiti identità stabile dell'evento, importi interi in centesimi e scostamenti dal fuso UTC espliciti. La prima trasformazione usava `customerId` al primo livello. Stabilita la conservazione del JSON originale per verifiche e rielaborazioni.

## 2026-05-06 · approvazione del contratto v2
Approvato `customer.id` annidato per consentire futuri attributi cliente senza cambiare la struttura esterna dell'ordine. Confermate le identità stabili di evento e ordine. La coesistenza è obbligatoria; nessuna data rigida di passaggio è codificata nei lettori. La verifica di accettazione del consumatore deve coprire entrambi i formati prima del rilascio del produttore.

## 2026-05-20 · standard di riconciliazione REC-08
Richieste tre misure distinte per le verifiche della materializzazione: consegne ricevute, eventi semantici univoci e righe analitiche materializzate. I rapporti devono dichiarare il denominatore. I confronti del fatturato giornaliero devono usare interi di centesimi e lo stesso fuso aziendale. Non arrotondare i singoli eventi in unità monetarie prima della somma.

## 2026-05-27 · gestione delle evidenze
Aggiunto l'obbligo di identificare interrogazioni, chiavi dei campioni e scenario nella pubblicazione dei rapporti diagnostici. Non allegare credenziali, stringhe di connessione o esportazioni complete dei dati. Queste modifiche definiscono i controlli previsti; la conformità effettiva deve essere verificata.
