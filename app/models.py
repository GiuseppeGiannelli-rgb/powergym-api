"""Modelli Pydantic: request body, risposte e validazione (capitoli 4 e 5)."""

from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Livello(str, Enum):
    """Valori ammessi per un path parameter (capitolo 2.5)."""

    principiante = "principiante"
    intermedio = "intermedio"
    avanzato = "avanzato"


class Abbonamento(str, Enum):
    mensile = "mensile"
    trimestrale = "trimestrale"
    annuale = "annuale"
    student = "student"


PREZZI_ABBONAMENTI = {
    Abbonamento.mensile: 59.0,
    Abbonamento.trimestrale: 159.0,
    Abbonamento.annuale: 549.0,
    Abbonamento.student: 45.0,
}


class Corso(BaseModel):
    id: int
    nome: str
    descrizione: str
    livello: Livello
    durata_min: int
    prezzo_mensile: float
    posti: int


class IscrittoIn(BaseModel):
    """Request body per creare/aggiornare un iscritto, con vincoli di validazione."""

    nome: str = Field(..., min_length=2, max_length=50, description="Nome e cognome")
    email: EmailStr
    eta: int = Field(..., ge=14, le=99, description="Età (minimo 14 anni)")
    abbonamento: Abbonamento
    corsi: list[int] = Field(default=[], max_length=5, description="ID dei corsi scelti (max 5)")
    note: str | None = Field(None, max_length=300)


class Iscritto(IscrittoIn):
    """Risposta: i dati inviati + i campi calcolati dal server."""

    id: int
    prezzo_abbonamento: float


class FiltroCorsi(BaseModel):
    """Gruppo di query parameters in un modello Pydantic (capitolo 5.3)."""

    model_config = {"extra": "forbid"}  # rifiuta parametri non previsti

    livello: Livello | None = None
    prezzo_max: float | None = Field(None, gt=0)
    durata_max: int | None = Field(None, gt=0, le=180)
    ordina_per: str = Field("nome", pattern="^(nome|prezzo_mensile|durata_min)$")
    limit: int = Field(10, gt=0, le=50)
    offset: int = Field(0, ge=0)
