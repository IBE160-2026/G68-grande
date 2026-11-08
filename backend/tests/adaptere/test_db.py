"""Tester for databasen og testbrukeren (FR-3, NFR-1, NFR-5, NFR-8)."""

import sqlite3
from contextlib import closing

import pytest
import werkzeug.security
from werkzeug.security import check_password_hash

from soknad import create_app
from soknad.adaptere import db
from soknad.adaptere.db import finn_bruker, lag_database
from soknad.innstillinger import TESTBRUKER_EPOST, TESTBRUKER_PASSORD


@pytest.fixture
def db_sti(tmp_path):
    sti = tmp_path / "ny-mappe" / "brukere.db"
    lag_database(sti)
    return sti


def _rader(sti):
    with closing(sqlite3.connect(sti)) as tilkobling:
        return tilkobling.execute("SELECT id, epost, passord_hash FROM brukere").fetchall()


def test_nfr8_testbrukeren_fra_readme():
    """NFR-8: testbrukeren er test@example.com / testpassord1."""
    assert TESTBRUKER_EPOST == "test@example.com"
    assert TESTBRUKER_PASSORD == "testpassord1"


def test_nfr8_forste_oppstart_lager_mappe_database_og_testbruker(tmp_path):
    """NFR-8: uten instance/ lager create_app mappen, brukere.db, tabellen og testbrukeren."""
    instance = tmp_path / "instance"
    assert not instance.exists()
    app = create_app()
    assert app.instance_path == str(instance)
    assert app.config["DATABASE"] == str(instance / "brukere.db")
    assert (instance / "brukere.db").is_file()
    rader = _rader(instance / "brukere.db")
    assert [epost for _, epost, _ in rader] == ["test@example.com"]


def test_nfr8_ny_oppstart_lager_ikke_testbrukeren_paa_nytt(db_sti):
    """NFR-8: testbrukeren lages bare én gang, og hashen er uendret ved ny oppstart."""
    for_oppstart = _rader(db_sti)
    lag_database(db_sti)
    create_app({"DATABASE": str(db_sti)})
    assert _rader(db_sti) == for_oppstart
    assert len(for_oppstart) == 1


def test_nfr1_passordet_lagres_bare_som_hash(db_sti):
    """NFR-1: passordet står aldri i klartekst, verken i tabellen eller i databasefilen."""
    ((_, _, passord_hash),) = _rader(db_sti)
    assert passord_hash != TESTBRUKER_PASSORD
    assert check_password_hash(passord_hash, TESTBRUKER_PASSORD)
    assert TESTBRUKER_PASSORD.encode("utf-8") not in db_sti.read_bytes()


def test_nfr1_ekte_oppstart_bruker_werkzeugs_vanlige_hash(tmp_path, monkeypatch):
    """NFR-1: utenfor testene brukes werkzeugs vanlige hash (scrypt), ikke testenes raske."""
    monkeypatch.setattr(db, "generate_password_hash", werkzeug.security.generate_password_hash)
    sti = tmp_path / "brukere.db"
    lag_database(sti)
    ((_, _, passord_hash),) = _rader(sti)
    assert passord_hash.startswith("scrypt:")
    assert finn_bruker(sti, TESTBRUKER_EPOST, TESTBRUKER_PASSORD) is not None


def test_fr3_riktig_epost_og_passord_gir_bruker_id(db_sti):
    """FR-3: riktig e-post og passord gir id-en til testbrukeren."""
    ((bruker_id, _, _),) = _rader(db_sti)
    assert finn_bruker(db_sti, TESTBRUKER_EPOST, TESTBRUKER_PASSORD) == bruker_id


def test_fr3_epost_med_store_bokstaver_og_mellomrom_virker(db_sti):
    """FR-3: e-post sammenlignes uten mellomrom og uten forskjell på store og små bokstaver."""
    assert finn_bruker(db_sti, "  Test@Example.COM ", TESTBRUKER_PASSORD) is not None


@pytest.mark.parametrize(
    ("epost", "passord"),
    [
        ("test@example.com", "feilpassord"),
        ("test@example.com", " testpassord1"),
        ("test@example.com", "TESTPASSORD1"),
        ("ukjent@example.com", "testpassord1"),
    ],
)
def test_fr3_feil_passord_eller_ukjent_epost_gir_none(db_sti, epost, passord):
    """FR-3: feil passord (også med mellomrom eller store bokstaver) eller ukjent e-post."""
    assert finn_bruker(db_sti, epost, passord) is None
