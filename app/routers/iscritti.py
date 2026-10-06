"""Iscritti: request body con Pydantic, combinato con path e query parameters."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from app.db import CORSI, ISCRITTI
from app.models import PREZZI_ABBONAMENTI, Abbonamento, Iscritto, IscrittoIn

router = APIRouter(prefix="/iscritti", tags=["iscritti"])

IscrittoId = Annotated[int, Path(title="ID dell'iscritto", ge=1)]


def _crea_o_aggiorna(iscritto_id: int, dati: IscrittoIn) -> Iscritto:
    """Regole di business che Pydantic da solo non può verificare."""
    corsi_inesistenti = [c for c in dati.corsi if c not in CORSI]
    if corsi_inesistenti:
        raise HTTPException(status_code=422, detail=f"Corsi inesistenti: {corsi_inesistenti}")
    if dati.abbonamento is Abbonamento.student and dati.eta >= 26:
        raise HTTPException(status_code=422, detail="L'abbonamento student è riservato agli under 26")
    for altro in ISCRITTI.values():
        if altro.id != iscritto_id and altro.email == dati.email:
            raise HTTPException(status_code=409, detail="Email già registrata")

    return Iscritto(id=iscritto_id, prezzo_abbonamento=PREZZI_ABBONAMENTI[dati.abbonamento], **dati.model_dump())


# --- "users/me" prima di "users/{user_id}": l'ordine conta (capitolo 2.4) ---
@router.get("/me")
async def iscritto_corrente():
    return {"messaggio": "In un'app reale qui ci sarebbe l'utente autenticato", "iscritti_totali": len(ISCRITTI)}


@router.get("", response_model=list[Iscritto])
async def lista_iscritti():
    return list(ISCRITTI.values())


@router.get("/{iscritto_id}", response_model=Iscritto)
async def dettaglio_iscritto(iscritto_id: IscrittoId):
    if iscritto_id not in ISCRITTI:
        raise HTTPException(status_code=404, detail="Iscritto non trovato")
    return ISCRITTI[iscritto_id]


# --- Request body (capitolo 4) ---
@router.post("", response_model=Iscritto, status_code=status.HTTP_201_CREATED)
async def crea_iscritto(dati: IscrittoIn):
    nuovo_id = max(ISCRITTI, default=0) + 1
    iscritto = _crea_o_aggiorna(nuovo_id, dati)
    ISCRITTI[nuovo_id] = iscritto
    return iscritto


# --- Request body + path + query parameters (capitolo 4.8) ---
@router.put("/{iscritto_id}")
async def aggiorna_iscritto(iscritto_id: IscrittoId, dati: IscrittoIn, notifica: bool = False):
    if iscritto_id not in ISCRITTI:
        raise HTTPException(status_code=404, detail="Iscritto non trovato")
    iscritto = _crea_o_aggiorna(iscritto_id, dati)
    ISCRITTI[iscritto_id] = iscritto
    risposta = iscritto.model_dump()
    if notifica:
        risposta["notifica"] = f"Email di conferma inviata a {iscritto.email}"
    return risposta


@router.delete("/{iscritto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def elimina_iscritto(iscritto_id: IscrittoId):
    if ISCRITTI.pop(iscritto_id, None) is None:
        raise HTTPException(status_code=404, detail="Iscritto non trovato")
