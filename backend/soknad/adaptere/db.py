"""Den lokale databasen med brukerne (SQLite). Passord lagres bare som hash."""

import sqlite3
from contextlib import closing
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash

from soknad.innstillinger import TESTBRUKER_EPOST, TESTBRUKER_PASSORD
from soknad.kjerne.inndata import normaliser_epost


def _koble_til(sti):
    return closing(sqlite3.connect(sti))


def lag_database(sti):
    """Lager mappen, databasen og tabellen hvis de mangler, og testbrukeren hvis
    e-posten ikke finnes fra før. Kan kjøres ved hver oppstart."""
    sti = Path(sti)
    sti.parent.mkdir(parents=True, exist_ok=True)
    epost = normaliser_epost(TESTBRUKER_EPOST)
    with _koble_til(sti) as db, db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS brukere ("
            " id INTEGER PRIMARY KEY,"
            " epost TEXT NOT NULL UNIQUE,"
            " passord_hash TEXT NOT NULL)"
        )
        finnes = db.execute("SELECT 1 FROM brukere WHERE epost = ?", (epost,)).fetchone()
        if finnes is None:
            db.execute(
                "INSERT INTO brukere (epost, passord_hash) VALUES (?, ?)",
                (epost, generate_password_hash(TESTBRUKER_PASSORD)),
            )


def finn_bruker(sti, epost, passord) -> int | None:
    """Gir bruker-id-en når e-post og passord stemmer, ellers None."""
    with _koble_til(sti) as db:
        rad = db.execute(
            "SELECT id, passord_hash FROM brukere WHERE epost = ?", (normaliser_epost(epost),)
        ).fetchone()
    if rad is None or not check_password_hash(rad[1], passord):
        return None
    return rad[0]


def epost_finnes(sti, epost) -> bool:
    """Sier om e-posten (normalisert) er registrert fra før."""
    with _koble_til(sti) as db:
        rad = db.execute(
            "SELECT 1 FROM brukere WHERE epost = ?", (normaliser_epost(epost),)
        ).fetchone()
    return rad is not None


def lag_bruker(sti, epost, passord) -> int | None:
    """Lagrer en ny bruker med normalisert e-post og bare hashen av passordet, og gir
    id-en. Gir None hvis e-posten finnes (for eksempel kom den inn i mellomtiden)."""
    try:
        with _koble_til(sti) as db, db:
            markor = db.execute(
                "INSERT INTO brukere (epost, passord_hash) VALUES (?, ?)",
                (normaliser_epost(epost), generate_password_hash(passord)),
            )
            return markor.lastrowid
    except sqlite3.IntegrityError:
        return None
