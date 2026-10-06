"""Test automatici: poetry run pytest -v"""

import pytest
from fastapi.testclient import TestClient

from app.db import ISCRITTI
from app.main import app

client = TestClient(app)

NUOVO = {"nome": "Luca Rossi", "email": "luca@example.com", "eta": 22, "abbonamento": "student", "corsi": [1, 3]}


@pytest.fixture(autouse=True)
def db_pulito():
    ISCRITTI.clear()
    yield
    ISCRITTI.clear()


def test_root():
    assert client.get("/").json()["message"] == "Benvenuto in PowerGym API"


# --- Path parameters ---
def test_corso_tipizzato():
    assert client.get("/corsi/3").json()["nome"] == "Yoga"


def test_corso_id_non_intero():
    r = client.get("/corsi/yoga")
    assert r.status_code == 422
    assert r.json()["detail"][0]["type"] == "int_parsing"


def test_corso_id_fuori_range():
    assert client.get("/corsi/0").status_code == 422


def test_corso_inesistente():
    assert client.get("/corsi/99").status_code == 404


def test_livello_enum():
    r = client.get("/livelli/avanzato").json()
    assert set(r["corsi"]) == {"CrossFit", "Boxe"}
    assert client.get("/livelli/esperto").status_code == 422


def test_scheda_path():
    r = client.get("/schede/avanzato/forza/5x5.txt")
    assert r.status_code == 200 and "5x5" in r.json()["contenuto"]


def test_ordine_percorsi_me():
    assert "messaggio" in client.get("/iscritti/me").json()


# --- Query parameters ---
def test_skip_limit():
    assert len(client.get("/corsi?skip=2&limit=3").json()) == 3


def test_query_bool():
    assert client.get("/corsi/2?breve=true").json() == {"id": 2, "nome": "CrossFit"}


def test_query_obbligatorio_e_validato():
    assert client.get("/cerca").status_code == 422
    assert client.get("/cerca?q=yo").status_code == 422  # min_length=3
    assert client.get("/cerca?q=ciclismo").json()["risultati"] == 1


def test_filtro_modello():
    r = client.get("/corsi/filtra?livello=intermedio&ordina_per=prezzo_mensile")
    assert [c["nome"] for c in r.json()] == ["Spinning", "Pilates"]


def test_filtro_parametro_extra_vietato():
    assert client.get("/corsi/filtra?colore=rosso").status_code == 422


def test_filtro_pattern():
    assert client.get("/corsi/filtra?ordina_per=posti").status_code == 422


# --- Request body ---
def test_crea_iscritto():
    r = client.post("/iscritti", json=NUOVO)
    assert r.status_code == 201
    assert r.json()["id"] == 1 and r.json()["prezzo_abbonamento"] == 45.0


def test_validazione_body():
    errato = {**NUOVO, "email": "non-una-email", "eta": 10}
    campi = {e["loc"][-1] for e in client.post("/iscritti", json=errato).json()["detail"]}
    assert campi == {"email", "eta"}


def test_regole_business():
    assert client.post("/iscritti", json={**NUOVO, "eta": 30}).status_code == 422  # student over 26
    assert client.post("/iscritti", json={**NUOVO, "corsi": [42]}).status_code == 422
    client.post("/iscritti", json=NUOVO)
    assert client.post("/iscritti", json=NUOVO).status_code == 409  # email duplicata


def test_aggiorna_con_query():
    client.post("/iscritti", json=NUOVO)
    r = client.put("/iscritti/1?notifica=true", json={**NUOVO, "abbonamento": "annuale"})
    assert r.json()["prezzo_abbonamento"] == 549.0 and "notifica" in r.json()


def test_elimina():
    client.post("/iscritti", json=NUOVO)
    assert client.delete("/iscritti/1").status_code == 204
    assert client.get("/iscritti/1").status_code == 404
