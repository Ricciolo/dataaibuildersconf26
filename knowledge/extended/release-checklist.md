# Lista di verifica per il rilascio
## REL-GATE-27 — responsabile del rilascio
Il responsabile della piattaforma dati approva la trasformazione; il responsabile del produttore approva la compatibilità del messaggio; il responsabile delle analisi clienti accetta le variazioni nella semantica dei rapporti. La registrazione del rilascio collega versione del contratto, evidenze dei test, piano di ripristino e perimetro delimitato della distribuzione.

## Prima della distribuzione
Confermare l'accettazione di entrambe le versioni supportate indipendentemente dall'ordine di arrivo. Verificare la stabilità dell'identità evento in caso di consegna ripetuta. Confermare interpretazione temporale che preserva lo scostamento UTC, importi interi e obbligatorietà del cliente. Confrontare l'uscita misurata con un riferimento di accettazione riservato. L'immagine di una risposta del modello non costituisce evidenza di rilascio.

## Durante l'osservazione
Separare le misure dell'accettazione alla sorgente da quelle della materializzazione. Documentare il denominatore di ogni tasso. Il campionamento deve includere versioni del contratto e varianti di scostamento UTC, ma un solo campione non dimostra la correttezza dell'intero sistema. Le variazioni di volume possono dipendere dal business e richiedono riconciliazione.

## Dopo l'approvazione
Registrare le versioni effettive di strumenti e pacchetti. Congelare l'ambiente della conferenza dopo la prova generale. Se un componente fallisce una verifica essenziale, scegliere l'alternativa documentata senza sostituire silenziosamente i risultati con una simulazione. Per eseguire la demo locale non è necessario aggiornare il repository remoto.
