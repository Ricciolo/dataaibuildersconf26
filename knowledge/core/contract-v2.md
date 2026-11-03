# Contratto v2
Campi: `eventId` (stringa stabile), `orderId` (stringa), `schemaVersion=2`, `customer: {id: stringa obbligatoria}`, `amountCents` (intero positivo), `occurredAt` (data e ora ISO 8601 con scostamento dal fuso UTC esplicito). Le versioni v1 e v2 coesistono durante la migrazione. La consegna può essere ritentata mantenendo invariato `eventId`.
