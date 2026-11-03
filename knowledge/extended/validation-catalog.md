# Catalogo delle validazioni
## VAL-ID-02 — identità
Un evento semantico ha un unico `eventId` stabile. Gli identificativi delle consegne di trasporto possono variare tra tentativi. L'identità distinta dell'evento e il valore distinto di `orderId` sono misure diverse: futuri eventi del ciclo di vita di un ordine potrebbero condividere legittimamente `orderId`. Il campione della conferenza è limitato a un evento ordine per ordine.

## VAL-MONEY-05 — importi
`amountCents` deve essere un intero positivo. La valuta è fissa per questa demo e non è un campo separato. Esporre i totali in centesimi oppure dichiarare la conversione in fase di presentazione. NULL, numeri in virgola mobile e valori negativi non rispettano il contratto. Non aggiungere regole sui rimborsi senza una nuova decisione contrattuale.

## VAL-CUSTOMER-06 — formato dell'identità
L'identificativo cliente obbligatorio è una stringa non vuota nel percorso definito da `schemaVersion`. La destinazione ammette NULL per agevolare la diagnostica, ma questo non autorizza ad accettare come validi dati di business senza identità. In questo ambiente non è disponibile un servizio di arricchimento.

## VAL-TIME-07 — data e ora
Lo scostamento dal fuso UTC deve essere esplicito. Confrontare gli istanti dopo l'interpretazione e usare `Europe/Rome` per raggruppare per data aziendale. Il giorno UTC e quello aziendale locale possono differire. L'ora legale deve seguire il database dei fusi IANA, senza assumere uno scostamento fisso `+01:00`.

## VAL-COVERAGE-11 — accettazione del rilascio
Validare ogni versione supportata del contratto, almeno uno scostamento non nullo e le consegne ripetute. I test di accettazione devono confrontare le osservazioni con un riferimento atteso mantenuto separatamente. I risultati dell'accettazione devono restare separati dai requisiti ed essere approvati dal responsabile del rilascio.
