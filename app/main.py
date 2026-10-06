"""PowerGym API – applicazione FastAPI.

Avvio:  poetry run uvicorn app.main:app --reload
Docs:   http://127.0.0.1:8000/docs  (Swagger)  –  http://127.0.0.1:8000/redoc
"""

from fastapi import FastAPI

from app.routers import corsi, iscritti

app = FastAPI(
    title="PowerGym API",
    description="API della palestra PowerGym: corsi, schede di allenamento e iscritti.",
    version="1.0.0",
)

app.include_router(corsi.router)
app.include_router(iscritti.router)


# --- Il codice più semplice (capitolo 1) ---
@app.get("/", tags=["home"])
async def root():
    return {"message": "Benvenuto in PowerGym API", "docs": "/docs"}
