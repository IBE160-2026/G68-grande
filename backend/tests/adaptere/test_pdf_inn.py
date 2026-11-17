"""Tester for teksten fra en opplastet PDF (FR-8, FR-11, kriterium 5, story 6.1). PDF-ene i
testdataene er lagret fra Word med scripts/lag_testpdf.ps1. Prøven av grensen på 50 bokstaver med
testdata/feil/skannet.pdf (laget med scripts/lag_feilfiler.ps1) kom i story 6.2."""

import logging
import re
from pathlib import Path

import pytest

from soknad.adaptere import pdf_inn
from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.adaptere.pdf_inn import les_pdf, normaliser
from soknad.innstillinger import MIN_BOKSTAVER_PDF
from soknad.kjerne.inndata import er_uleselig
from soknad.kjerne.testdata_match import vask

SOKNAD = Path(pdf_inn.__file__).resolve().parents[1]
PDF_ER = sorted(TESTDATA_MAPPE.glob("case-*/*.pdf"))
FEIL = TESTDATA_MAPPE / "feil"


def test_fr8_testdataene_har_pdf_ene():
    """FR-8 (story 6.1): hvert testcase har cv.pdf og annonse.pdf, og case 1 også
    eget-brev.pdf."""
    navn = {(pdf.parent.name, pdf.name) for pdf in PDF_ER}
    assert {
        ("case-1-utvikler", "cv.pdf"),
        ("case-1-utvikler", "annonse.pdf"),
        ("case-1-utvikler", "eget-brev.pdf"),
        ("case-2-okonomi", "cv.pdf"),
        ("case-2-okonomi", "annonse.pdf"),
    } <= navn


@pytest.mark.parametrize("pdf", PDF_ER, ids=[f"{p.parent.name}/{p.name}" for p in PDF_ER])
def test_fr8_pdf_fra_word_gir_samme_tekst_som_txt(pdf):
    """FR-8 (kriterium 5): teksten fra PDF-en er den samme som i .txt-fila etter vasken, og
    den er normalisert (NFKC, uten myke bindestreker og usynlige tegn)."""
    tekst = les_pdf(pdf.read_bytes())
    assert vask(tekst) == vask(pdf.with_suffix(".txt").read_text(encoding="utf-8"))
    assert tekst == normaliser(tekst)


@pytest.mark.parametrize(
    "innhold",
    [
        b"",
        b"ikke en pdf",
        # Starten på en Word-fil (zip).
        b"PK\x03\x04\x14\x00\x06\x00",
        b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\nnoe som er \xff\xfe \xc3\xb8delagt",
    ],
)
def test_fr11_fil_som_ikke_kan_leses_gir_tom_tekst_og_uleselig(innhold):
    """FR-8/FR-11 (story 6.1 og 6.2): en fil pypdf ikke kan lese, eller som ikke er en PDF, gir
    tom tekst uten krasj, og tom tekst er uleselig."""
    assert les_pdf(innhold) == ""
    assert er_uleselig(les_pdf(innhold))


def test_fr11_bare_skannet_pdf_er_under_grensen_paa_50_bokstaver():
    """FR-11 (story 6.2): grensen på MIN_BOKSTAVER_PDF bokstaver skiller den skannede PDF-en fra
    PDF-ene i testdataene. skannet.pdf er bare et bilde og har ingen bokstaver, og alle PDF-ene i
    testdata/case-*/ har langt flere enn grensen (målt 16. november 2026: 0 og 896–1 038)."""
    skannet = les_pdf((FEIL / "skannet.pdf").read_bytes())
    assert sum(tegn.isalpha() for tegn in skannet) < MIN_BOKSTAVER_PDF
    assert er_uleselig(skannet)
    for pdf in PDF_ER:
        tekst = les_pdf(pdf.read_bytes())
        assert sum(tegn.isalpha() for tegn in tekst) >= MIN_BOKSTAVER_PDF, pdf
        assert not er_uleselig(tekst), pdf


def test_fr8_avkuttet_pdf_gir_ingen_krasj():
    """FR-8 (story 6.1): en PDF som er kuttet av halvveis, gir ingen krasj."""
    innhold = PDF_ER[0].read_bytes()
    assert isinstance(les_pdf(innhold[: len(innhold) // 2]), str)


def test_fr8_normaliser_gjor_nfd_om_til_ett_tegn():
    """FR-8 (utsatt fra story 2.1): å og é som to tegn (NFD, bokstav og aksent) blir ett tegn,
    som i .txt. (æ og ø har ingen slik oppdeling i Unicode.)"""
    nfd = "Pa\u030a kafe\u0301 i A\u030asane"
    assert len(nfd) == len("På kafé i Åsane") + 3
    assert normaliser(nfd) == "På kafé i Åsane"


@pytest.mark.parametrize("tegn", ["\u00ad", "\u200b", "\u200c", "\u200d", "\u2060", "\ufeff"])
def test_fr8_normaliser_fjerner_myk_bindestrek_og_usynlige_tegn(tegn):
    """FR-8 (utsatt fra story 2.1): myk bindestrek og usynlige tegn uten bredde fjernes, så
    telleregelen finner ordet."""
    assert normaliser(f"Java{tegn}Script og {tegn}SQL") == "JavaScript og SQL"


def test_fr8_normaliser_beholder_vanlige_tegn():
    """FR-8: linjeskift, mellomrom, tankestrek og «sitattegn» står igjen."""
    tekst = "Linje én – «sitat»\nLinje to"
    assert normaliser(tekst) == tekst


def test_fr8_les_pdf_normaliserer_teksten(monkeypatch):
    """FR-8: les_pdf normaliserer teksten fra hver side og setter linjeskift mellom sidene."""

    class Side:
        def __init__(self, tekst):
            self.tekst = tekst

        def extract_text(self):
            return self.tekst

    class Leser:
        def __init__(self, fil):
            self.pages = [Side("a\u030aker\u00adbruk"), Side(None), Side("side\u200b tre")]

    monkeypatch.setattr(pdf_inn, "PdfReader", Leser)
    assert les_pdf(b"%PDF") == "åkerbruk\n\nside tre"


class Side:
    """En side for den falske PdfReader: teksten, eller et unntak fra extract_text()."""

    def __init__(self, tekst):
        self.tekst = tekst

    def extract_text(self):
        if isinstance(self.tekst, Exception):
            raise self.tekst
        return self.tekst


def falsk_leser(monkeypatch, *sider):
    """Bytter PdfReader i pdf_inn med en leser som har sidene, og gir lista over sidene som er
    lest."""
    lest = []

    class LestSide(Side):
        def extract_text(self):
            lest.append(self.tekst)
            return super().extract_text()

    class Leser:
        def __init__(self, fil):
            self.pages = [LestSide(tekst) for tekst in sider]

    monkeypatch.setattr(pdf_inn, "PdfReader", Leser)
    return lest


def test_fr8_normaliser_fjerner_mellomrom_foran_linjeskift():
    """FR-8/NFR-11 (retro 6 A2): mellomrom og tabulatorer foran et linjeskift fjernes (PDF-er
    fra Word har ett på slutten av hver linje), så tegntellingen blir som for innlimt tekst.
    Mellomrom inni linjene og innrykk står igjen."""
    assert normaliser("Linje én \nLinje to\t \n  innrykk  her \n") == (
        "Linje én\nLinje to\n  innrykk  her\n"
    )
    assert normaliser("Windows \r\nlinje") == "Windows\nlinje"


@pytest.mark.parametrize("pdf", PDF_ER, ids=[f"{p.parent.name}/{p.name}" for p in PDF_ER])
def test_fr8_pdf_fra_word_har_ikke_mellomrom_foran_linjeskift(pdf):
    """FR-8 (retro 6 A2): teksten fra PDF-ene i testdataene har ingen " \\n" (cv.pdf fra case 1
    hadde 39 før rettingen)."""
    tekst = les_pdf(pdf.read_bytes())
    assert " \n" not in tekst
    assert "\t\n" not in tekst


def test_fr8_mellomrom_paa_slutten_av_en_side_fjernes(monkeypatch):
    """FR-8 (retro 6 A2): et mellomrom på slutten av en side står foran linjeskiftet mellom
    sidene og fjernes også."""
    falsk_leser(monkeypatch, "side en \n", "side to ", "side tre")
    assert les_pdf(b"%PDF") == "side en\n\nside to\nside tre"


def test_fr11_en_side_som_feiler_gir_teksten_fra_de_andre(monkeypatch):
    """FR-11 (retro 6 A5): kaster extract_text() et unntak på én side, brukes teksten fra de
    andre sidene. PDF-en er bare uleselig hvis den har for få bokstaver."""
    falsk_leser(monkeypatch, "Side en med nok tekst. " * 3, ValueError("ødelagt"), "Side tre")
    tekst = les_pdf(b"%PDF")
    assert tekst == "Side en med nok tekst. " * 2 + "Side en med nok tekst.\n\nSide tre"
    assert not er_uleselig(tekst)
    falsk_leser(monkeypatch, "Bare litt", ValueError("ødelagt"))
    assert er_uleselig(les_pdf(b"%PDF"))


@pytest.mark.parametrize("maks", [0, 1, 5, 9, 10, 11, 25])
def test_nfr11_les_pdf_kutter_rett_over_maks(monkeypatch, maks):
    """NFR-11/NFR-4 (retro 6 A1): med maks kuttes teksten til høyst maks + 1 tegn, så feltet
    fortsatt får for_lang, men økten aldri lagrer mer. Er teksten ikke lengre enn maks, er den
    uendret."""
    falsk_leser(monkeypatch, "0123456789", "abcdefghij")
    hele = "0123456789\nabcdefghij"
    tekst = les_pdf(b"%PDF", maks=maks)
    assert tekst == hele[: maks + 1]
    assert (len(tekst) > maks) == (len(hele) > maks)


def test_nfr11_les_pdf_slutter_aa_lese_sider_over_maks(monkeypatch):
    """NFR-11 (retro 6 A1): lesingen stopper når teksten er over maks, så resten av sidene ikke
    pakkes ut."""
    lest = falsk_leser(monkeypatch, *(f"side {nummer:02}" for nummer in range(10)))
    assert les_pdf(b"%PDF", maks=14) == "side 00\nside 01"
    assert lest == ["side 00", "side 01"]
    lest.clear()
    assert les_pdf(b"%PDF") == "\n".join(f"side {nummer:02}" for nummer in range(10))
    assert len(lest) == 10


def test_nfr11_les_pdf_kutter_pdf_ene_i_testdataene():
    """NFR-11 (retro 6 A1): med maks under lengden gir en ekte PDF maks + 1 tegn, og med maks
    over lengden er teksten den samme som uten maks."""
    for pdf in PDF_ER:
        hele = les_pdf(pdf.read_bytes())
        assert les_pdf(pdf.read_bytes(), maks=100) == hele[:101]
        assert les_pdf(pdf.read_bytes(), maks=len(hele)) == hele


def test_nfr4_pypdf_logger_bare_feil():
    """NFR-4 (retro 6 A6): pypdf logger advarsler med rå linjer fra fila. Loggeren til pypdf
    viser bare feil, så advarslene ikke havner i loggen."""
    assert logging.getLogger("pypdf").level == logging.ERROR
    assert not logging.getLogger("pypdf").isEnabledFor(logging.WARNING)


def test_fr8_bare_pdf_inn_importerer_pypdf():
    """FR-8/AD (story 6.1): pypdf importeres bare i adaptere/pdf_inn.py, og kjerne/ leser
    aldri filer."""
    med_pypdf = sorted(
        str(fil.relative_to(SOKNAD))
        for fil in SOKNAD.rglob("*.py")
        if re.search(r"^\s*(import|from)\s+pypdf", fil.read_text(encoding="utf-8"), re.M)
    )
    assert med_pypdf == [str(Path("adaptere") / "pdf_inn.py")]
    for fil in (SOKNAD / "kjerne").glob("*.py"):
        tekst = fil.read_text(encoding="utf-8")
        for forbudt in ("open(", "read_bytes", "read_text", "pdf_inn"):
            assert forbudt not in tekst, f"{fil.name}: {forbudt}"
