"""Tester for TestKI, som gir de håndlagde KI-svarene i testmodus (FR-28, FR-32, FR-34, AD-3).
Testene bruker de ekte testdataene i testdata/, eller en kopi i tmp_path når et svar skal
ødelegges."""

import json
import shutil

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE, TestKI, les_testcaser
from soknad.kjerne.feil import KIFeil, KIFeilType

CASE = TESTDATA_MAPPE / "case-1-utvikler"


def _les(navn: str) -> str:
    return (CASE / navn).read_text(encoding="utf-8")


def _rotete(tekst: str) -> str:
    """Samme tekst med ekstra mellomrom, linjeskift og store bokstaver."""
    return "\n  " + tekst.upper().replace(" ", "  ").replace("\n", "\r\n\n") + "  \n"


@pytest.fixture
def kopi(tmp_path):
    """En kopi av testdata/ som testen kan ødelegge."""
    mappe = tmp_path / "testdata"
    shutil.copytree(TESTDATA_MAPPE, mappe)
    return mappe


def test_fr34_testcasene_leses_fra_testdata():
    """FR-34: alle case-mappene i testdata/ leses, sortert på navn."""
    navn = [case.navn for case in les_testcaser()]
    assert "case-1-utvikler" in navn
    assert navn == sorted(navn)


def test_fr32_testki_gir_de_handlagde_svarene():
    """FR-32: TestKI gir nøyaktig svarene i ki-svar/, uten API-nøkkel."""
    ki = TestKI()
    cv, annonse = _les("cv.txt"), _les("annonse.txt")
    assert ki.nokkelord(annonse) == json.loads(_les("ki-svar/nokkelord.json"))
    assert ki.gap(cv, annonse) == json.loads(_les("ki-svar/gap.json"))


def test_fr22_testki_gir_testbrevet():
    """FR-22/FR-32: TestKI.brev gir brev-1.json for forslag 1, også med rotete tekst."""
    ki = TestKI()
    forventet = json.loads(_les("ki-svar/brev-1.json"))
    assert ki.brev(_les("cv.txt"), _les("annonse.txt"), forslag=1) == forventet
    assert ki.brev(_rotete(_les("cv.txt")), _rotete(_les("annonse.txt")), 1) == forventet


def test_fr22_brev_oddetall_gir_brev_1_og_partall_brev_2(kopi):
    """FR-22/FR-25: oddetall for forslag leser brev-1.json, partall brev-2.json."""
    svar = kopi / "case-1-utvikler" / "ki-svar"
    (svar / "brev-2.json").write_text('{"avsnitt": ["Forslag to"]}', encoding="utf-8")
    ki = TestKI(kopi)
    cv, annonse = _les("cv.txt"), _les("annonse.txt")
    forste = json.loads(_les("ki-svar/brev-1.json"))
    assert ki.brev(cv, annonse, forslag=1) == forste
    assert ki.brev(cv, annonse, forslag=3) == forste
    assert ki.brev(cv, annonse, forslag=2) == {"avsnitt": ["Forslag to"]}
    assert ki.brev(cv, annonse, forslag=4) == {"avsnitt": ["Forslag to"]}


def test_fr28_brevfil_som_mangler_gir_kifeil_annet(kopi):
    """FR-28: mangler brevfila (brev-2.json finnes ikke ennå), gir det KIFeil(annet)."""
    ki = TestKI(kopi)
    with pytest.raises(KIFeil) as feil:
        ki.brev(_les("cv.txt"), _les("annonse.txt"), forslag=2)
    assert feil.value.type == KIFeilType.ANNET
    (kopi / "case-1-utvikler" / "ki-svar" / "brev-1.json").unlink()
    with pytest.raises(KIFeil) as feil:
        ki.brev(_les("cv.txt"), _les("annonse.txt"), forslag=1)
    assert feil.value.type == KIFeilType.ANNET


@pytest.mark.parametrize("innhold", ['{"avsnitt": []}', '{"avsnitt": ["  "]}', "ikke json"])
def test_fr28_tomt_brev_gir_ubrukelig_svar(kopi, innhold):
    """FR-28: et tomt eller ødelagt brev går gjennom kontroller() og gir
    KIFeil(ubrukelig_svar)."""
    (kopi / "case-1-utvikler" / "ki-svar" / "brev-1.json").write_text(innhold, encoding="utf-8")
    with pytest.raises(KIFeil) as feil:
        TestKI(kopi).brev(_les("cv.txt"), _les("annonse.txt"), forslag=1)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def test_fr22_brev_uten_testdata_gir_kifeil_annet():
    """FR-22/FR-34: tekst som ikke er testdata, gir KIFeil(annet), som i gap."""
    with pytest.raises(KIFeil) as feil:
        TestKI().brev(_les("cv.txt"), "Min egen annonse", forslag=1)
    assert feil.value.type == KIFeilType.ANNET


def test_fr34_testki_kjenner_igjen_rotete_tekst():
    """FR-34: samme tekst med ekstra mellomrom, linjeskift og store bokstaver gir samme svar."""
    ki = TestKI()
    cv, annonse = _rotete(_les("cv.txt")), _rotete(_les("annonse.txt"))
    assert ki.nokkelord(annonse) == json.loads(_les("ki-svar/nokkelord.json"))
    assert ki.gap(cv, annonse) == json.loads(_les("ki-svar/gap.json"))


def test_fr34_testki_uten_testdata_gir_kifeil_annet():
    """FR-34: tekst som ikke er testdata, gir KIFeil(annet). Inndataene sjekkes før
    KI-en kalles (story 2.5), så dette er bare en sikring."""
    ki = TestKI()
    with pytest.raises(KIFeil) as feil:
        ki.nokkelord("Min egen annonse")
    assert feil.value.type == KIFeilType.ANNET
    with pytest.raises(KIFeil) as feil:
        ki.gap(_les("cv.txt"), "Min egen annonse")
    assert feil.value.type == KIFeilType.ANNET


@pytest.mark.parametrize(
    ("oppgave", "innhold"),
    [
        ("nokkelord", "ikke json"),
        ("nokkelord", '{"nokkelord": [], "arbeidsgiver": null}'),
        ("gap", '{"dekker": [], "mangler": []}'),
        ("gap", '{"dekker": ["Python"]}'),
    ],
)
def test_fr28_odelagt_svarfil_gir_ubrukelig_svar(kopi, oppgave, innhold):
    """FR-28: TestKI sender svaret gjennom kontroller(), så en ødelagt svarfil gir
    KIFeil(ubrukelig_svar)."""
    (kopi / "case-1-utvikler" / "ki-svar" / f"{oppgave}.json").write_text(innhold, encoding="utf-8")
    ki = TestKI(kopi)
    with pytest.raises(KIFeil) as feil:
        if oppgave == "nokkelord":
            ki.nokkelord(_les("annonse.txt"))
        else:
            ki.gap(_les("cv.txt"), _les("annonse.txt"))
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def test_fr28_svarfil_som_ikke_er_utf8_gir_ubrukelig_svar(kopi):
    """FR-28: en svarfil som ikke er utf-8, er et ubrukelig svar."""
    (kopi / "case-1-utvikler" / "ki-svar" / "gap.json").write_bytes(b'{"dekker": ["\xff"]}')
    with pytest.raises(KIFeil) as feil:
        TestKI(kopi).gap(_les("cv.txt"), _les("annonse.txt"))
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def test_fr28_svarfil_som_mangler_gir_kifeil_annet(kopi):
    """FR-28: mangler svarfila, gir det KIFeil(annet)."""
    (kopi / "case-1-utvikler" / "ki-svar" / "gap.json").unlink()
    with pytest.raises(KIFeil) as feil:
        TestKI(kopi).gap(_les("cv.txt"), _les("annonse.txt"))
    assert feil.value.type == KIFeilType.ANNET
