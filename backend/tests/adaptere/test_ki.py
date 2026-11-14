"""Tester for TestKI, som gir de ferdige KI-svarene i testmodus (FR-28, FR-32, FR-34, AD-3).
Testene bruker de ekte testdataene i testdata/, eller en kopi i tmp_path når et svar skal
ødelegges."""

import json
import shutil

import pytest

import soknad
from soknad.adaptere.ki import TESTDATA_MAPPE, TestdataFeil, TestKI, les_testcaser
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


def _case(mappe, navn, cv, annonse):
    """En case-mappe med cv.txt og annonse.txt."""
    (mappe / navn).mkdir(parents=True)
    (mappe / navn / "cv.txt").write_text(cv, encoding="utf-8")
    (mappe / navn / "annonse.txt").write_text(annonse, encoding="utf-8")


def test_fr34_testdata_som_mangler_gir_tydelig_feil(tmp_path):
    """FR-34 (story 4.5): mangler testdata/, eller har den ingen case-mapper, gir
    les_testcaser TestdataFeil som nevner mappen."""
    for mappe in (tmp_path / "finnes-ikke", tmp_path):
        with pytest.raises(TestdataFeil, match="Fant ingen testcaser") as feil:
            les_testcaser(mappe)
        assert str(mappe) in str(feil.value)


@pytest.mark.parametrize("fil", ["cv.txt", "annonse.txt"])
def test_fr34_fil_som_mangler_gir_tydelig_feil(tmp_path, fil):
    """FR-34 (story 4.5): mangler cv.txt eller annonse.txt i en case-mappe, nevner feilen
    caset og fila."""
    _case(tmp_path, "case-1-a", "CV a", "Annonse a")
    (tmp_path / "case-1-a" / fil).unlink()
    with pytest.raises(TestdataFeil, match=f"case-1-a mangler fila {fil}"):
        les_testcaser(tmp_path)


@pytest.mark.parametrize(
    ("cv_b", "annonse_b", "navn"),
    [("  cv A\n", "Annonse b", "CV"), ("CV b", "ANNONSE  a", "annonse")],
)
def test_fr34_like_caser_gir_tydelig_feil(tmp_path, cv_b, annonse_b, navn):
    """FR-34/AD-10 (story 4.5): to caser med samme vaskede CV eller annonse gir TestdataFeil
    som nevner begge casene. Da kan nokkelord (annonsen) og gap (CV-en) aldri finne hvert sitt
    case."""
    _case(tmp_path, "case-1-a", "CV a", "Annonse a")
    _case(tmp_path, "case-2-b", cv_b, annonse_b)
    with pytest.raises(TestdataFeil, match=f"case-1-a og case-2-b har samme {navn}"):
        les_testcaser(tmp_path)


def test_fr34_appen_starter_ikke_med_feil_i_testdata(monkeypatch, tmp_path):
    """FR-34 (story 4.5): create_app stopper med TestdataFeil når testdataene mangler."""
    monkeypatch.setattr(soknad, "TestKI", lambda: TestKI(tmp_path / "finnes-ikke"))
    with pytest.raises(TestdataFeil):
        soknad.create_app({"TESTING": True, "DATABASE": str(tmp_path / "brukere.db")})


def test_fr34_testki_gir_svarene_fra_hvert_case():
    """FR-34/FR-38 (story 4.5): med to caser gir nokkelord, gap og brev svarene fra caset CV-en
    og annonsen hører til."""
    ki = TestKI()
    for case in sorted(mappe for mappe in TESTDATA_MAPPE.glob("case-*") if mappe.is_dir()):
        cv = (case / "cv.txt").read_text(encoding="utf-8")
        annonse = (case / "annonse.txt").read_text(encoding="utf-8")
        svar = case / "ki-svar"
        assert ki.nokkelord(annonse) == json.loads((svar / "nokkelord.json").read_text("utf-8"))
        assert ki.gap(cv, annonse) == json.loads((svar / "gap.json").read_text("utf-8"))
        assert ki.brev(cv, annonse, 1) == json.loads((svar / "brev-1.json").read_text("utf-8"))
        assert ki.brev(cv, annonse, 2) == json.loads((svar / "brev-2.json").read_text("utf-8"))


def test_fr32_testki_gir_de_ferdige_svarene():
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
    """FR-28: mangler brevfila, gir det KIFeil(annet), både for brev-2.json og brev-1.json."""
    (kopi / "case-1-utvikler" / "ki-svar" / "brev-2.json").unlink(missing_ok=True)
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
