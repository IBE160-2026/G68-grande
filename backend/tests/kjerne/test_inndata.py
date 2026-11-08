"""Tester for kjernen: feiltypene, økten og sjekken av innloggingen og registreringen
(FR-1, FR-2, FR-3, FR-4, NFR-5)."""

import ast
import dataclasses
from pathlib import Path

import pytest

from soknad.innstillinger import MIN_PASSORD_LENGDE
from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.inndata import normaliser_epost, sjekk_innlogging, sjekk_registrering
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


# --- Registrering ---


def _feil(*par):
    return [InndataFeil(felt, type_) for felt, type_ in par]


def test_fr1_minste_passordlengde_er_8():
    """FR-1: passordet må ha minst 8 tegn."""
    assert MIN_PASSORD_LENGDE == 8


def test_fr1_riktig_utfylt_registrering_gir_ingen_feil():
    """FR-1: gyldig e-post og like passord på minst 8 tegn gir ingen feil."""
    assert sjekk_registrering("ola@x.no", "passord12", "passord12") == []
    assert sjekk_registrering("  Ola@X.no ", "passord12", "passord12") == []


@pytest.mark.parametrize("epost", ["", "   "])
def test_fr1_fr4_alt_tomt_gir_tre_feil_i_rekkefolgen_epost_passord_gjenta(epost):
    """FR-1/FR-4: tre tomme felt gir tre feil samtidig, i feltenes rekkefølge."""
    assert sjekk_registrering(epost, "", "") == _feil(
        ("epost", FeilType.TOM), ("passord", FeilType.TOM), ("gjenta", FeilType.TOM)
    )


@pytest.mark.parametrize(
    "epost",
    ["ola@", "ola", "@x.no", "ola@x", "ola@x.", "ola@@x.no", "ola@x@y.no", "o la@x.no"],
)
def test_fr1_ugyldig_epost(epost):
    """FR-1: e-posten må ha formen noe@noe.noe, uten mellomrom og med bare én @."""
    assert sjekk_registrering(epost, "passord12", "passord12") == _feil(
        ("epost", FeilType.EPOST_UGYLDIG)
    )


@pytest.mark.parametrize("epost", ["ola@x.no", "a@b.c", "ola.nordmann+jobb@post.uio.no"])
def test_fr1_gyldig_epost(epost):
    """FR-1: vanlige e-poster er gyldige."""
    assert sjekk_registrering(epost, "passord12", "passord12") == []


def test_fr1_passord_paa_7_tegn_er_for_kort_og_8_er_nok():
    """FR-1: minst 8 tegn betyr len(passord) >= 8."""
    assert sjekk_registrering("ola@x.no", "1234567", "1234567") == _feil(
        ("passord", FeilType.PASSORD_KORT)
    )
    assert sjekk_registrering("ola@x.no", "12345678", "12345678") == []


def test_fr1_passordet_endres_aldri():
    """FR-1: mellomrom i passordet telles med; bare et helt tomt passord er tomt."""
    assert sjekk_registrering("ola@x.no", "        ", "        ") == []
    assert sjekk_registrering("ola@x.no", "passord12", "passord12 ") == _feil(
        ("gjenta", FeilType.PASSORD_ULIKE)
    )


def test_fr1_ulike_passord_gir_feil_ved_gjenta():
    """FR-1: ulike passord gir feilen ved «Gjenta passord»."""
    assert sjekk_registrering("ola@x.no", "passord12", "passord13") == _feil(
        ("gjenta", FeilType.PASSORD_ULIKE)
    )


def test_fr1_ulike_sjekkes_bare_naar_begge_er_fylt():
    """FR-1: passord tomt og gjenta fylt gir bare «tom» ved passord, og omvendt."""
    assert sjekk_registrering("ola@x.no", "", "passord12") == _feil(("passord", FeilType.TOM))
    assert sjekk_registrering("ola@x.no", "passord12", "") == _feil(("gjenta", FeilType.TOM))


def test_fr1_flere_feil_kommer_samtidig_med_hoyst_en_per_felt():
    """FR-1/FR-4: ugyldig e-post, kort passord og ulike passord gir tre feil samtidig."""
    assert sjekk_registrering("ola@", "kort", "annet") == _feil(
        ("epost", FeilType.EPOST_UGYLDIG),
        ("passord", FeilType.PASSORD_KORT),
        ("gjenta", FeilType.PASSORD_ULIKE),
    )


def test_fr2_kjernen_sjekker_ikke_om_eposten_finnes():
    """FR-2: om e-posten finnes, sjekkes i databasen, så kjernen gir aldri den feilen."""
    assert sjekk_registrering("test@example.com", "passord12", "passord12") == []


FORBUDT_I_KJERNEN = (
    "flask",
    "werkzeug",
    "sqlite3",
    "os",
    "pathlib",
    "io",
    "shutil",
    "subprocess",
    "socket",
    "urllib",
    "http",
    "requests",
    "httpx",
    "anthropic",
    "pypdf",
    "docx",
    "soknad.adaptere",
    "soknad.web",
)


def _importerte_moduler(kilde):
    """Hele navnet på alt kildeteksten importerer. «from a import b» gir både a og a.b, så
    «from soknad import web» også blir funnet. Relative importer regnes fra soknad.kjerne."""
    for node in ast.walk(ast.parse(kilde)):
        if isinstance(node, ast.Import):
            yield from (navn.name for navn in node.names)
        elif isinstance(node, ast.ImportFrom):
            pakke = ["soknad", "kjerne"][: 3 - node.level] if node.level else []
            modul = ".".join([*pakke, *([node.module] if node.module else [])])
            yield modul
            yield from (f"{modul}.{navn.name}" for navn in node.names)


def _forbudte_importer(kilde):
    return {
        modul
        for modul in _importerte_moduler(kilde)
        if any(modul == f or modul.startswith(f + ".") for f in FORBUDT_I_KJERNEN)
    }


def test_nfr5_kjernen_importerer_ikke_io_adaptere_eller_web():
    """NFR-5: kjernen er regler uten I/O og importerer aldri I/O-biblioteker (flask, os,
    pathlib, anthropic og de andre i FORBUDT_I_KJERNEN), soknad.adaptere eller soknad.web."""
    filer = sorted(KJERNE.glob("*.py"))
    assert filer
    for fil in filer:
        forbudt = _forbudte_importer(fil.read_text(encoding="utf-8"))
        assert not forbudt, (fil.name, forbudt)


@pytest.mark.parametrize(
    "kilde",
    [
        "import flask",
        "import os",
        "from anthropic import Anthropic",
        "from pathlib import Path",
        "from werkzeug.security import generate_password_hash",
        "import sqlite3",
        "from soknad.adaptere.db import finn_bruker",
        "import soknad.web.tekster",
        "from soknad import web",
        "from soknad.adaptere import oktlager",
        "from ..web import tekster",
        "from .. import adaptere",
    ],
)
def test_nfr5_lagsjekken_slaar_til(kilde):
    """NFR-5: lagsjekken over finner faktisk forbudte importer, også i soknad-pakken."""
    assert _forbudte_importer(kilde)


def test_nfr5_lagsjekken_godtar_kjernens_egne_importer():
    """NFR-5: kjernens egne importer og soknad.innstillinger er lov."""
    kilde = (
        "import re\nfrom dataclasses import dataclass\nfrom soknad.innstillinger import X\n"
        "from soknad.kjerne.feil import FeilType\nfrom .okt import Innlogging"
    )
    assert _forbudte_importer(kilde) == set()
