"""Tester for teksten fra en opplastet PDF (FR-8, kriterium 5, story 6.1). PDF-ene i testdataene
er lagret fra Word med scripts/lag_testpdf.ps1."""

import re
from pathlib import Path

import pytest

from soknad.adaptere import pdf_inn
from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.adaptere.pdf_inn import les_pdf, normaliser
from soknad.kjerne.testdata_match import vask

SOKNAD = Path(pdf_inn.__file__).resolve().parents[1]
PDF_ER = sorted(TESTDATA_MAPPE.glob("case-*/*.pdf"))


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
def test_fr8_fil_som_ikke_kan_leses_gir_tom_tekst(innhold):
    """FR-8 (story 6.1, til 6.2): en fil pypdf ikke kan lese, eller som ikke er en PDF, gir
    tom tekst uten krasj, så feltet får feilen «tom»."""
    assert les_pdf(innhold) == ""


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
