"""Tester for kjernen: feiltypene, økten og sjekken av innloggingen (FR-3, FR-4, NFR-5)."""

import ast
import dataclasses
from pathlib import Path

import pytest

from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.inndata import normaliser_epost, sjekk_innlogging
from soknad.kjerne.okt import Innlogging

KJERNE = Path(__file__).resolve().parents[2] / "soknad" / "kjerne"


def test_fr3_epost_normaliseres_uten_mellomrom_og_store_bokstaver():
    """FR-3: e-post sammenlignes med strip() og casefold()."""
    assert normaliser_epost("  Test@Example.COM \t") == "test@example.com"
    assert normaliser_epost("   ") == ""


def test_fr4_tomme_felt_gir_begge_feilene_samtidig():
    """FR-4: begge felt tomme gir to feil, i rekkefølgen e-post, passord."""
    assert sjekk_innlogging("", "") == [
        InndataFeil("epost", FeilType.TOM),
        InndataFeil("passord", FeilType.TOM),
    ]


def test_fr4_epost_med_bare_mellomrom_er_tom():
    """FR-4: en e-post med bare mellomrom regnes som tom."""
    assert sjekk_innlogging("   ", "testpassord1") == [InndataFeil("epost", FeilType.TOM)]


def test_fr4_passord_med_bare_mellomrom_er_ikke_tomt():
    """FR-4: passordet endres aldri, så mellomrom er et passord (som så sjekkes mot databasen)."""
    assert sjekk_innlogging("test@example.com", "   ") == []
    assert sjekk_innlogging("test@example.com", "") == [InndataFeil("passord", FeilType.TOM)]


def test_fr3_utfylt_skjema_gir_ingen_feil():
    """FR-3: utfylte felt gir ingen inndatafeil."""
    assert sjekk_innlogging("test@example.com", "testpassord1") == []


def test_fr3_feiltypene_er_lukket_liste():
    """FR-3/FR-4: feiltypene i Epic 1 er nøyaktig disse."""
    assert [t.value for t in FeilType] == [
        "tom",
        "epost_finnes",
        "epost_ugyldig",
        "passord_kort",
        "passord_ulike",
        "feil_innlogging",
    ]
    assert FeilType.FEIL_INNLOGGING == "feil_innlogging"


def test_fr3_inndatafeil_og_innlogging_er_frosne():
    """FR-3: InndataFeil og Innlogging kan ikke endres etter at de er laget."""
    feil = InndataFeil(None, FeilType.FEIL_INNLOGGING)
    innlogging = Innlogging(1, testmodus=True)
    with pytest.raises(dataclasses.FrozenInstanceError):
        feil.felt = "epost"
    with pytest.raises(dataclasses.FrozenInstanceError):
        innlogging.bruker_id = 2


def test_fr3_innlogging_maa_ha_bruker_id_og_testmodus():
    """FR-3: Innlogging har ingen standardverdi for testmodus; begge feltene må gis."""
    with pytest.raises(TypeError):
        Innlogging(7)
    assert Innlogging(7, False) == Innlogging(bruker_id=7, testmodus=False)


def _importerte_moduler(fil):
    tre = ast.parse(fil.read_text(encoding="utf-8"))
    for node in ast.walk(tre):
        if isinstance(node, ast.Import):
            yield from (navn.name.split(".")[0] for navn in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module.split(".")[0]


def test_nfr5_kjernen_importerer_ikke_flask_werkzeug_eller_sqlite3():
    """NFR-5: kjernen er regler uten I/O og importerer aldri flask, werkzeug eller sqlite3."""
    filer = sorted(KJERNE.glob("*.py"))
    assert filer
    for fil in filer:
        forbudt = set(_importerte_moduler(fil)) & {"flask", "werkzeug", "sqlite3"}
        assert not forbudt, (fil.name, forbudt)
