# Selfwork FastAPI – PowerGym API

Replica del progetto FastAPI della video-lezione con un dominio originale: l'**API REST della palestra PowerGym** (corsi, schede di allenamento, iscritti).
Ogni endpoint mette in pratica un capitolo del materiale del corso.

| Capitolo | Endpoint | Cosa mostra |
|---|---|---|
| 1. Introduzione | `GET /` | prima API, documentazione su `/docs` e `/redoc` |
| 2. Path Parameters | `GET /corsi/{corso_id}` | parametro tipizzato `int`, conversione ed errore `int_parsing` |
| | `GET /iscritti/me` prima di `/iscritti/{id}` | l'ordine dei percorsi conta |
| | `GET /livelli/{livello}` | valori ammessi con `Enum` |
| | `GET /schede/{percorso:path}` | parametro che contiene un percorso |
| 3. Query Parameters | `GET /corsi?skip=0&limit=10` | valori di default |
| | `GET /corsi/{id}?breve=true` | query `bool` opzionale |
| | `GET /cerca?q=...` | query obbligatorio |
| 4. Request Body | `POST /iscritti` | modello Pydantic con `Field`, risposta con campi calcolati, `201 Created` |
| | `PUT /iscritti/{id}?notifica=true` | body + path + query insieme |
| 5. Validation | `GET /cerca?q=` | `Query(min_length, max_length)` |
| | `GET /corsi/{corso_id}` | `Path(ge=1, le=1000)` |
| | `GET /corsi/filtra?...` | query in un modello Pydantic con `extra="forbid"` e `pattern` |

Oltre al materiale: `HTTPException` (404, 409, 422) per le regole di business (email duplicata, corsi inesistenti, abbonamento student solo under 26), `DELETE` con `204`, router separati (`APIRouter`) e **19 test automatici** con `TestClient`.

## Struttura

```
app/
    main.py            # istanza FastAPI + router
    models.py          # modelli Pydantic ed Enum
    db.py              # database finto in memoria
    routers/
        corsi.py       # corsi, livelli, schede, ricerca, filtri
        iscritti.py    # CRUD iscritti
tests/test_api.py      # test con TestClient
```

## Avvio

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

Apri http://127.0.0.1:8000/docs e prova gli endpoint con **Try it out**.

## Test

```bash
poetry run pytest -v
```

## Esempio di request body

```json
{
  "nome": "Luca Rossi",
  "email": "luca@example.com",
  "eta": 22,
  "abbonamento": "student",
  "corsi": [1, 3],
  "note": "Primo ingresso"
}
```
