"""Tester for kontrollen av KI-svar (FR-28, AD-4). Hvert tilfelle av ubrukelig svar gir
KIFeil(ubrukelig_svar)."""

import copy
import json
import pickle

import pytest

from soknad.innstillinger import MAKS_NOKKELORD
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.ki_svar import kontroller


def test_fr28_gyldig_nokkelordsvar_gis_tilbake():
    """FR-28: et gyldig svar gis tilbake i formen fra AD-4."""
    tekst = '{"nokkelord": ["Python", "SQL"], "arbeidsgiver": "Testvik AS"}'
    assert kontroller("nokkelord", tekst) == {
        "nokkelord": ["Python", "SQL"],
        "arbeidsgiver": "Testvik AS",
    }


def test_fr28_arbeidsgiver_kan_vaere_null():
    """FR-28: mangler arbeidsgiveren, sender KI-en null (AD-4)."""
    svar = kontroller("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": null}')
    assert svar["arbeidsgiver"] is None


def test_fr28_gyldig_gapsvar_med_en_tom_liste():
    """FR-28: én tom liste er lov, så lenge ikke begge er tomme."""
    assert kontroller("gap", '{"dekker": [], "mangler": ["SQL"]}') == {
        "dekker": [],
        "mangler": ["SQL"],
    }


@pytest.mark.parametrize(
    ("oppgave", "tekst"),
    [
        # Ugyldig JSON
        ("nokkelord", ""),
        ("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": null'),
        ("gap", "ikke json"),
        # Tom nøkkelordliste
        ("nokkelord", '{"nokkelord": [], "arbeidsgiver": "Testvik AS"}'),
        # Både dekker og mangler tomme
        ("gap", '{"dekker": [], "mangler": []}'),
        # Bare tomme tekster regnes som tomt
        ("nokkelord", '{"nokkelord": ["", "  "], "arbeidsgiver": null}'),
        ("gap", '{"dekker": [""], "mangler": [" \\n"]}'),
        # JSON som er nøstet så dypt at Python gir opp
        ("gap", "[" * 100_000 + "]" * 100_000),
        # Feil form: ikke et objekt, felt som mangler eller er i tillegg, feil type
        ("nokkelord", '["Python"]'),
        ("nokkelord", '{"nokkelord": ["Python"]}'),
        ("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": null, "ekstra": 1}'),
        ("nokkelord", '{"nokkelord": "Python", "arbeidsgiver": null}'),
        ("nokkelord", '{"nokkelord": ["Python", 3], "arbeidsgiver": null}'),
        ("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": 3}'),
        ("gap", '{"dekker": ["Python"]}'),
        ("gap", '{"dekker": "Python", "mangler": []}'),
        ("gap", '{"dekker": ["Python"], "mangler": [null]}'),
        ("gap", "null"),
        # Brev uten tekst (story 3.1)
        ("brev", '{"avsnitt": []}'),
        ("brev", '{"avsnitt": ["  "]}'),
        ("brev", '{"avsnitt": ["", " \\n"]}'),
        # Brev med feil form
        ("brev", '{"avsnitt": "Hei"}'),
        ("brev", '{"avsnitt": ["Hei", 3]}'),
        ("brev", '{"avsnitt": ["Hei"], "forslag": 1}'),
        ("brev", '{"tekst": "Hei"}'),
        ("brev", '["Hei"]'),
    ],
)
def test_fr28_ubrukelig_svar_gir_kifeil(oppgave, tekst):
    """FR-28: ugyldig JSON, tom nøkkelordliste, tomme dekker og mangler og feil form gir
    KIFeil(ubrukelig_svar)."""
    with pytest.raises(KIFeil) as feil:
        kontroller(oppgave, tekst)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def test_fr28_kifeil_beholder_typen_ved_kopi():
    """FR-28: en kopi av KIFeil (copy eller pickle) har samme type som originalen."""
    original = KIFeil(KIFeilType.UBRUKELIG_SVAR)
    for kopi in (copy.copy(original), pickle.loads(pickle.dumps(original))):
        assert kopi.type == KIFeilType.UBRUKELIG_SVAR


def test_fr28_ukjent_oppgave_er_en_programfeil():
    """FR-28: korrektur kommer i Epic 5. En ukjent oppgave er en feil i koden."""
    with pytest.raises(ValueError):
        kontroller("korrektur", '{"avsnitt": ["Hei"]}')


def test_fr22_gyldig_brev_gis_tilbake():
    """FR-22/FR-28: et brev med minst ett avsnitt med tekst gis tilbake i formen fra AD-4."""
    tekst = '{"avsnitt": ["Jeg søker stillingen.", "Med vennlig hilsen", "Sara"]}'
    assert kontroller("brev", tekst) == {
        "avsnitt": ["Jeg søker stillingen.", "Med vennlig hilsen", "Sara"]
    }


def test_fr22_tomme_avsnitt_i_brevet_fjernes():
    """FR-22/FR-28: avsnitt som er tomme eller bare har mellomrom, fjernes fra brevet."""
    assert kontroller("brev", '{"avsnitt": ["Hei", "", "  "]}') == {"avsnitt": ["Hei"]}


@pytest.mark.parametrize("stop_reason", ["max_tokens", "refusal", "pause_turn", None])
def test_fr28_stop_reason_som_ikke_er_end_turn_gir_ubrukelig_svar(stop_reason):
    """FR-28/AD-4: et avkuttet eller avvist svar gir KIFeil(ubrukelig_svar) før JSON-en leses,
    også når JSON-en er gyldig. Uten stop_reason gjelder end_turn (TestKI)."""
    tekst = '{"dekker": ["Python"], "mangler": []}'
    assert kontroller("gap", tekst) == kontroller("gap", tekst, "end_turn")
    with pytest.raises(KIFeil) as feil:
        kontroller("gap", tekst, stop_reason)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def _nokkelord(antall: int) -> str:
    return json.dumps({"nokkelord": [f"ord{n}" for n in range(antall)], "arbeidsgiver": None})


def test_fr15_grensen_er_maks_nokkelord():
    """FR-15: grensen for antall nøkkelord er MAKS_NOKKELORD, som er 30."""
    assert MAKS_NOKKELORD == 30


def test_fr15_fr28_akkurat_30_nokkelord_godtas():
    """FR-15/FR-28: et svar med akkurat MAKS_NOKKELORD nøkkelord godtas."""
    svar = kontroller("nokkelord", _nokkelord(MAKS_NOKKELORD))
    assert len(svar["nokkelord"]) == MAKS_NOKKELORD


@pytest.mark.parametrize("antall", [MAKS_NOKKELORD + 1, 100])
def test_fr15_fr28_flere_enn_30_nokkelord_gir_ubrukelig_svar(antall):
    """FR-15/FR-28: flere enn MAKS_NOKKELORD nøkkelord gir KIFeil(ubrukelig_svar)."""
    with pytest.raises(KIFeil) as feil:
        kontroller("nokkelord", _nokkelord(antall))
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR
