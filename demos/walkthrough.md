# Scaletta 60 minuti
| Minuti | Blocco | Azione e criterio |
|---|---|---|
| 00–07 | Introduzione a Claude Desktop | Scenario e confini |
| 07–17 | Projects, Knowledge, RAG | 2m Chat, 3m core, 3m recupero documentale se osservato, 2m confronto/fallback |
| 17–20 | Introduzione a MCP | Client, server, strumenti e radici |
| 20–36 | Indagine | PostgreSQL, JSON e log con evidenze |
| 36–44 | Sicurezza MCP | Consentito/negato; DAB solo dopo la verifica preliminare |
| 44–53 | Artifact | Dati raccolti, nessun backend |
| 53–56 | Limiti e Dashboards | Limiti e breve riferimento opzionale |
| 56–60 | Domande e risposte | Domande |

## Prima del palco
Eseguire l’avvio rapido README, test e security_check. Tenere in una finestra presenter/queries.sql e validation/expected-results.json; non condividerle con Claude. Verificare connessioni in una chat di prova, poi creare nuove chat dal vivo per evitare contaminazione. Caricare solo la documentazione autorizzata, incollare istruzioni Project. Seguire demos/projects-rag.md per la fase Knowledge e la verifica preliminare RAG osservabile; senza indicatore e tool di ricerca dichiarare l’alternativa Knowledge.

```sh
source .venv/bin/activate
docker compose up -d --wait
python scripts/seed.py --reset --scenario baseline
python scripts/seed.py --verify
python scripts/seed.py --reset --scenario incident
python scripts/seed.py --verify
python scripts/security_check.py
```
Dopo reset incident non rigenerare baseline fino alla fine dell’intervento. Tenere pronto `open presenter/generated/incident-explorer.html`. Il reset aggiorna evidenze e alternativa dello stesso scenario, non la conoscenza Project.

## Regia passo per passo
1. Introduzione: mostrare architettura del Project, nessuna soluzione; esplicitare che il DB è locale ma il contenuto selezionato dai tool può entrare nella conversazione Claude.
2. Demo 1: seguire projects-rag.md; stesso prompt in Chat e core, poi domanda specifica estesa con controllo del tool di ricerca. Preferire un Project aggiornato in prova generale; un secondo Project è solo opzione per confronto dal vivo immediato. Non caricare file sul palco aspettando indicizzazione.
3. MCP: mostrare radice evidence e login di sola lettura, mai .env o wrapper sul proiettore.
4. Indagine: dare prompt aperto; massimo due minuti per il piano, poi 8 minuti di tool e 6 per verifica. Confrontare con query private: 3060 righe, 3000 eventi, 1530 customer NULL, 60 righe in eccesso, 1020 timestamp spostati di +7200s. Sono conteggi di righe incluse retry, non categorie disgiunte. v2 ha 1530 consegne, v1 1530; i retry sono 60, 30 per versione. Log mapping non prova da solo le altre cause. Identificativi di consegna dei campioni 1,1501,3001.
5. Sicurezza: eseguire script e prompt consentito/negato. DAB non è necessario per completare l’intervento: se verifica preliminare fallisce usare alternativa DBHub documentata. Non mostrare una slide come prova dal vivo.
6. Artifact: chiedere prima inventario evidenze, poi prompt; confrontare numeri con query private. Se numeri inventati fermare e correggere dal risultato osservato. Se Artifact non parte entro 2 minuti aprire HTML locale e dichiararne origine. La versione offline è già pronta ma non equivale a SQL.
7. Limiti: RAG non garantisce copertura; MCP non garantisce correttezza o sicurezza; permessi e controllo umano sono separati. Claudedashboards è solo una menzione opzionale di contesto, non demo dal vivo e non dipendenza.

## Alternative e criteri di successo
- Claude indisponibile: documenti e prompt locali, racconto guidato; non fingere risultati dal vivo.
- Tool non disponibile: eseguire SQL via psql e incollare risultati misurati dichiarandone origine.
- Docker indisponibile: seed --offline, etichetta visibile, nessuna dichiarazione di verifica DB.
- DAB non validato: DBHub rifiuto imposto dal ruolo del database; vedere docs/security.md.
- Artifact fallisce: HTML autonomo generato dal seed.
Successo: ogni causa collegata a contratto + query + record, permessi dimostrati, Artifact con numeri della sessione, nessun segreto esposto. La durata resta 60 minuti tagliando domande successive, mai verifiche essenziali.
