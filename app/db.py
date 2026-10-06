"""Database finto in memoria (come fake_items_db degli esempi)."""

from app.models import Corso, Iscritto, Livello

CORSI: dict[int, Corso] = {
    c.id: c
    for c in [
        Corso(id=1, nome="Sala Pesi", descrizione="Macchine e pesi liberi con scheda personalizzata",
              livello=Livello.principiante, durata_min=90, prezzo_mensile=39.9, posti=40),
        Corso(id=2, nome="CrossFit", descrizione="Allenamento funzionale ad alta intensità",
              livello=Livello.avanzato, durata_min=60, prezzo_mensile=69.9, posti=12),
        Corso(id=3, nome="Yoga", descrizione="Hatha e vinyasa per mobilità e respirazione",
              livello=Livello.principiante, durata_min=75, prezzo_mensile=49.9, posti=15),
        Corso(id=4, nome="Pilates", descrizione="Rinforzo del core e postura, anche con reformer",
              livello=Livello.intermedio, durata_min=50, prezzo_mensile=54.9, posti=10),
        Corso(id=5, nome="Spinning", descrizione="Ciclismo indoor a ritmo di musica",
              livello=Livello.intermedio, durata_min=45, prezzo_mensile=44.9, posti=20),
        Corso(id=6, nome="Boxe", descrizione="Tecnica, sacco e preparazione atletica",
              livello=Livello.avanzato, durata_min=60, prezzo_mensile=59.9, posti=16),
    ]
}

ISCRITTI: dict[int, Iscritto] = {}

SCHEDE = {
    "principiante/full-body.txt": "Giorno A: squat, panca, rematore, plank (3x12)",
    "intermedio/push-pull-legs.txt": "Push / Pull / Legs, 4x10 con progressione settimanale",
    "avanzato/forza/5x5.txt": "Squat, panca, stacco 5x5 al 80% 1RM",
}
