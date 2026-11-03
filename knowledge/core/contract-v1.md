# Contratto v1
Campi: `eventId` (stringa stabile), `orderId` (stringa), `schemaVersion=1`, `customerId` (stringa obbligatoria), `amountCents` (intero positivo), `occurredAt` (data e ora ISO 8601 con scostamento dal fuso UTC esplicito). La consegna può essere ritentata mantenendo invariato `eventId`.

Esempio:

```json
{"eventId":"example-1","orderId":"example-order","schemaVersion":1,"customerId":"example-customer","amountCents":1200,"occurredAt":"2026-06-03T02:00:00+02:00"}
```
