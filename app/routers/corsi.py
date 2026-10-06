"""Corsi: path parameters, query parameters e validazione."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from app.db import CORSI, SCHEDE
from app.models import Corso, FiltroCorsi, Livello

router = APIRouter(tags=["corsi"])

MESSAGGI_LIVELLO = {
    Livello.principiante: "Perfetto per iniziare: lo staff ti segue passo passo.",
    Livello.intermedio: "Serve già un po' di base atletica.",
    Livello.avanzato: "Alta intensità: consigliata una lezione di prova.",
}


# --- Query parameters con valori di default (capitolo 3.1 e 3.2) ---
@router.get("/corsi", response_model=list[Corso])
async def lista_corsi(skip: int = 0, limit: int = 10):
    return list(CORSI.values())[skip: skip + limit]


# --- Gruppo di query parameters in un modello Pydantic con extra="forbid" (capitolo 5.3) ---
# Dichiarato PRIMA di /corsi/{corso_id}: l'ordine dei percorsi conta (capitolo 2.4)
@router.get("/corsi/filtra", response_model=list[Corso])
async def filtra_corsi(filtro: Annotated[FiltroCorsi, Query()]):
    risultati = list(CORSI.values())
    if filtro.livello:
        risultati = [c for c in risultati if c.livello == filtro.livello]
    if filtro.prezzo_max:
        risultati = [c for c in risultati if c.prezzo_mensile <= filtro.prezzo_max]
    if filtro.durata_max:
        risultati = [c for c in risultati if c.durata_min <= filtro.durata_max]
    risultati.sort(key=lambda c: getattr(c, filtro.ordina_per))
    return risultati[filtro.offset: filtro.offset + filtro.limit]


# --- Query parameter obbligatorio con validazione Query (capitolo 3.6 e 5.1) ---
@router.get("/cerca")
async def cerca_corsi(q: Annotated[str, Query(min_length=3, max_length=30, description="Testo da cercare")]):
    q_low = q.lower()
    trovati = [c for c in CORSI.values() if q_low in c.nome.lower() or q_low in c.descrizione.lower()]
    return {"q": q, "risultati": len(trovati), "corsi": trovati}


# --- Path parameter tipizzato e validato con Path + query bool opzionale (cap. 2.2, 3.4, 5.2) ---
@router.get("/corsi/{corso_id}")
async def dettaglio_corso(
    corso_id: Annotated[int, Path(title="ID del corso", ge=1, le=1000)],
    breve: bool = False,
):
    corso = CORSI.get(corso_id)
    if corso is None:
        raise HTTPException(status_code=404, detail=f"Corso {corso_id} non trovato")
    if breve:
        return {"id": corso.id, "nome": corso.nome}
    return corso


# --- Path parameter con valori predefiniti tramite Enum (capitolo 2.5) ---
@router.get("/livelli/{livello}")
async def corsi_per_livello(livello: Livello):
    corsi = [c.nome for c in CORSI.values() if c.livello is livello]
    return {"livello": livello, "messaggio": MESSAGGI_LIVELLO[livello], "corsi": corsi}


# --- Path parameter che contiene un percorso (capitolo 2.6) ---
@router.get("/schede/{percorso:path}")
async def scheda_allenamento(percorso: str):
    if percorso not in SCHEDE:
        raise HTTPException(status_code=404, detail=f"Scheda '{percorso}' non trovata. Disponibili: {list(SCHEDE)}")
    return {"percorso": percorso, "contenuto": SCHEDE[percorso]}
