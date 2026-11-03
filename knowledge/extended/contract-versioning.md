# Ciclo di vita e compatibilità dei contratti
## CV-12 — selezione della versione
`schemaVersion` è un intero contenuto in ogni evento. La versione si seleziona per evento, mai in base al nome del file o alla data di acquisizione. I file possono contenere versioni alternate. Durante la coesistenza v1/v2 i lettori supportano entrambe. L'assenza di `schemaVersion` è un errore di validazione del contratto, non equivale implicitamente alla versione 1.

## Compatibilità con le versioni precedenti
L'aggiunta di un campo facoltativo è compatibile se i lettori esistenti preservano le proprietà sorgente sconosciute. Lo spostamento di un campo obbligatorio richiede una nuova versione e una trasformazione capace di leggere entrambi i formati durante la coesistenza. Il rilascio di produttore e consumatore è coordinato tramite una lista di accettazione, non dedotto da una data e ora.

## Registro delle versioni
v1: stringa `customerId` al primo livello; v2: stringa annidata `customer.id`. `eventId`, `orderId`, `amountCents` e `occurredAt` mantengono il proprio significato. La versione 3 non è definita. I dati locali contengono solo le versioni 1 e 2. Le voci nella cronologia dei contratti non implicano incidenti di produzione.

## Regola di dismissione — CV-RET-09
Prima di dismettere un lettore, osservare quattordici finestre giornaliere consecutive di validazione con zero consegne della versione da ritirare; ottenere poi l'approvazione del responsabile della piattaforma dati e del responsabile delle analisi clienti. È una regola di governo del sistema, non un'affermazione sulle date fisse o sulla breve durata del campione locale. Una rielaborazione può reintrodurre una versione precedente dopo la migrazione dell'ultimo produttore attivo.
