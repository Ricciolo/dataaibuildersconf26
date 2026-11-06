# Scaletta operativa — 60 minuti

## Prima della sessione

```sh
cd /Users/cristiancivera/Projects/Personal/dataaibuildersconf26
source .venv/bin/activate
docker compose up -d --wait
python scripts/seed.py --reset --scenario incident
python scripts/seed.py --verify
python scripts/security_check.py
python -m unittest discover -s tests -v
```

- Aprire slide, Claude Desktop e DBeaver.
- In Claude aprire **Data & AI Builders Conference 2026**.
- Verificare il collegamento GitHub: solo `knowledge/core/` e `knowledge/extended/`. Sincronizzare se necessario.
- Aprire [prompts.md](prompts.md) per copiare i testi dei blocchi.
- Tenere [queries.sql](../presenter/queries.sql) e [expected-results.json](../validation/expected-results.json) solo nella finestra del relatore.
- Non eseguire altri reset durante l’indagine.

DBeaver:

```text
Tipo: PostgreSQL
URL: jdbc:postgresql://127.0.0.1:55432/orders_demo
Utente: demo_reader
Password: valore READER_PASSWORD nel file .env locale
```

## 00–07 — Introduzione

- Presentare il caso: eventi ordine e-commerce, contratti v1/v2, PostgreSQL locale.
- Spiegare: Project = documentazione, MCP = accesso ai dati, Artifact = esplorazione dei risultati.
- Precisare che i dati sono sintetici e i risultati dei tool entrano nella conversazione Claude.

## 07–17 — Demo 1: Project e Knowledge

1. Aprire una chat fuori dal Project. Disattivare web e connettori; escludere la memoria delle chat precedenti dove possibile.
2. Lanciare **1.1** da [prompts.md](prompts.md#11--stesso-prompt-in-chat-e-nel-project).
3. Aprire una nuova chat nel Project. Tenere web e MCP disattivati.
4. Lanciare lo stesso **1.1**. Mostrare i riferimenti ai contratti.
5. Lanciare **1.2**. Mostrare i documenti e le sezioni citati.
6. Se resta tempo, lanciare **1.3**: la versione 3 non è definita.

**RAG:** chiamarlo dimostrato solo con indicatore attivo e ricerca nella Knowledge osservata. Altrimenti presentare questa fase come uso della Knowledge. Il Project attuale contiene tutti i 17 documenti; per confrontare separatamente i soli cinque documenti essenziali preparare un secondo Project prima della sessione. Dettagli in [projects-rag.md](projects-rag.md).

## 17–20 — Introduzione MCP

- Aprire **Impostazioni → Sviluppatore** e mostrare i tre server in esecuzione.
- Mostrare **+ → Connettori** nella chat.
- Spiegare che i server sono globali in Desktop e si attivano per conversazione.
- Non mostrare `.env` o gli script `.local/` sul proiettore.

## 20–36 — Demo 2: indagine

1. Aprire una nuova chat nel Project.
2. Attivare **orders-dbhub** e **orders-evidence**. Disattivare **orders-quality**, web e connettori estranei.
3. Lanciare **2.1**.
4. Se Claude si ferma senza verificare le regole, lanciare **2.2**.
5. Lanciare **2.3** per raccogliere le evidenze che serviranno all’Artifact.
6. In DBeaver eseguire la query seguente e confrontare i risultati.
7. Tenere aperta questa chat: servirà nella Demo 4.

```sql
SELECT
    count(*) AS righe_ordini,
    count(DISTINCT event_id) AS eventi_distinti,
    count(*) FILTER (WHERE missing_customer) AS righe_senza_cliente,
    count(*) - count(DISTINCT event_id) AS righe_in_eccesso,
    count(*) FILTER (WHERE timestamp_delta_seconds <> 0) AS timestamp_alterati
FROM v_order_quality;
```

Risultato incident: `3060 | 3000 | 1530 | 60 | 1020`. Le categorie si sovrappongono.

```sql
SELECT o.*, r.payload
FROM orders AS o
JOIN raw_events AS r USING (delivery_id)
WHERE delivery_id IN (1, 1501, 3001)
ORDER BY delivery_id;
```

## 36–44 — Demo 3: sicurezza

### DBHub

1. Aprire una nuova chat nel Project con il solo **orders-dbhub** attivo.
2. Lanciare **3.1**: lettura riuscita, risultato `3060`.
3. Lanciare **3.2**: scrittura rifiutata da DBHub, `READONLY_VIOLATION`.

Per mostrare anche i permessi PostgreSQL indipendentemente dal tool:

```sh
python scripts/security_check.py
```

### DAB

1. Aprire una nuova chat nel Project con il solo **orders-quality** attivo.
2. Lanciare **3.3**: compare soltanto `OrderQuality`, con permesso di lettura.
3. Lanciare **3.4**: `raw_events` non è esposta, esito `EntityNotFound`.

Se DAB non funziona, mantenere la dimostrazione DBHub e lo script dei permessi. Dichiarare che la chiamata DAB non è stata dimostrata.

## 44–53 — Demo 4: Artifact

1. Tornare alla **chat dell’indagine della Demo 2**.
2. Disattivare i connettori: usare le evidenze già raccolte.
3. Lanciare **4.1**.
4. Controllare numeri, filtri, record e query rispetto ai risultati SQL della sessione.
5. Lanciare **4.2** per aggiungere «Simula un evento». In una chat nuova lasciare DBHub attivo per raccogliere prima le evidenze.
6. Provare v2, 1000 centesimi, due retry e `2026-06-03T12:00:00+02:00`. Attivare i tre interruttori: cliente assente, tre righe, 3000 centesimi, UTC 12:00 anziché 10:00, differenza +7200 secondi. Disattivarli: cliente presente, una riga e 1000 centesimi. I KPI osservati devono restare invariati.
7. Provare offset `+00:00` (zero), `-05:00` (−18000 secondi), importo decimale e timestamp senza offset (rifiutati). Premere «Ripristina esempio».
8. Dichiarare «simulazione locale su stato vuoto»: nessun ordine viene inserito in PostgreSQL. Usare gli ultimi tre minuti della demo.
9. Se non funziona entro due minuti, aprire l’alternativa HTML locale (evidenze, senza simulatore):

```sh
open presenter/generated/incident-explorer.html
```

## 53–56 — Limiti

- Citazioni corrette non dimostrano da sole il RAG.
- Permessi di sola lettura non impediscono la divulgazione di dati leggibili.
- Verificare SQL, conteggi e provenienza anche quando l’Artifact sembra convincente.
- Menzione facoltativa di Claude Dashboards, senza demo dal vivo.

## 56–60 — Domande

- Mostrare il repository: https://github.com/Ricciolo/dataaibuildersconf26
- Aprire README solo se serve indicare come ripetere la demo.

## Comandi di riserva

### Ripristinare l’incidente

```sh
python scripts/seed.py --reset --scenario incident
python scripts/seed.py --verify
```

### Tornare alla baseline dopo la sessione

```sh
python scripts/seed.py --reset --scenario baseline
python scripts/seed.py --verify
```

### Docker indisponibile: simulazione senza verifica SQL

```sh
python scripts/seed.py --offline --scenario incident
open presenter/generated/incident-explorer.html
```

Dichiarare «simulazione Python, PostgreSQL non verificato». Non presentare questi risultati come query eseguite sul database.

### Claude o MCP indisponibili

- Eseguire in DBeaver le query di [queries.sql](../presenter/queries.sql).
- Se Claude funziona, incollare i risultati misurati nella chat dichiarando che provengono da DBeaver.
- Se Claude non funziona, usare slide e HTML locale senza simulare risposte o chiamate live.

## Preparare la Skill per aggiornare l’Artifact

1. In Claude aprire **Personalizzazione → Skills → Aggiungi**, scegliere il caricamento di una Skill e importare `public/skills/aggiorna-data-incident-explorer.zip`. Abilitarla. Se richiesto, abilitare l’esecuzione del codice nelle funzionalità di Claude; la disponibilità può dipendere dalle impostazioni dell’organizzazione.
2. Nella chat che contiene l’Artifact attivare **orders-dbhub** e lanciare l’ultimo prompt di `prompts.md`, «Aggiornare l’Artifact dopo nuovi inserimenti nel database».
3. Verificare che Claude carichi la Skill, esegua nuove query e produca la nuova versione dell’Artifact. Il nome nel prompt è una richiesta esplicita in linguaggio naturale, non un comando slash.
4. La Skill non aggiunge accesso diretto al database dentro l’HTML. Non caricare questa procedura nella Knowledge dei contratti: importarla come Skill.

Prova manuale: dopo una fotografia iniziale, aggiungere le tre consegne con `python scripts/seed.py --append-demo`, poi lanciare il prompt breve. Confrontare i risultati con `python scripts/seed.py --verify`. La Skill non contiene conteggi attesi né soluzioni dell’incidente.
