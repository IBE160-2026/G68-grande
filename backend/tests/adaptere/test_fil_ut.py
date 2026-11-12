"""Tester for Word-filen til nedlastingen (FR-29, FR-30, NFR-9, AD-11). Story 3.2. Filen
åpnes med python-docx, som Word-filen brukeren laster ned."""

from io import BytesIO

import pytest
from docx import Document
from docx.oxml.ns import qn

from soknad.adaptere.fil_ut import lag_docx
from soknad.kjerne.feil import FilFeil

AVSNITT = [
    "Jeg søker stillingen som junior utvikler.",
    "Jeg har æ, ø og å, «sitattegn» og – tankestrek.",
    "Med vennlig hilsen",
    "Sara Eksempel",
]


def _apne(innhold: bytes):
    return Document(BytesIO(innhold))


def test_fr30_filen_har_bare_avsnittene_fra_brevet():
    """FR-30/NFR-9: ett avsnitt per element, i samme rekkefølge og med samme tekst (også æøå),
    og ingen tabeller eller andre avsnitt."""
    dokument = _apne(lag_docx(AVSNITT))
    assert [p.text for p in dokument.paragraphs] == AVSNITT
    assert dokument.tables == []


def test_fr30_filen_har_ingen_topp_eller_bunntekst():
    """FR-30/NFR-9: ingen seksjon har egen topp- eller bunntekst, og de er tomme."""
    dokument = _apne(lag_docx(AVSNITT))
    for seksjon in dokument.sections:
        for del_ in (
            seksjon.header,
            seksjon.footer,
            seksjon.first_page_header,
            seksjon.first_page_footer,
            seksjon.even_page_header,
            seksjon.even_page_footer,
        ):
            assert del_.is_linked_to_previous
            assert all(not p.text for p in del_.paragraphs)


def test_fr30_filen_har_ingen_markeringer():
    """FR-30: teksten er vanlig tekst, uten fet, kursiv, understreking eller farge."""
    dokument = _apne(lag_docx(AVSNITT))
    for avsnitt in dokument.paragraphs:
        for bit in avsnitt.runs:
            assert not bit.bold
            assert not bit.italic
            assert not bit.underline
            assert bit.font.color.rgb is None


def test_nfr4_filens_egenskaper_er_tomme():
    """NFR-4/FR-30: forfatter, tittel og kommentar i filens egenskaper er tomme."""
    egenskaper = _apne(lag_docx(AVSNITT)).core_properties
    assert egenskaper.author == ""
    assert egenskaper.last_modified_by == ""
    assert egenskaper.title == ""
    assert egenskaper.comments == ""


def test_fr29_filen_er_a4_og_norsk():
    """FR-29: siden er A4 (ikke amerikansk Letter), og språket er norsk bokmål, så Word ikke
    markerer brevet som stavefeil."""
    dokument = _apne(lag_docx(AVSNITT))
    for seksjon in dokument.sections:
        assert round(seksjon.page_width.mm) == 210
        assert round(seksjon.page_height.mm) == 297
    sprak = [e.get(qn("w:val")) for e in dokument.styles.element.iter(qn("w:lang"))]
    assert sprak
    assert set(sprak) == {"nb-NO"}


def test_fr29_filen_har_2_5_cm_marger():
    """FR-29: margen er 2,5 cm (25 mm) oppe, nede, til venstre og til høyre, ikke de
    amerikanske margene fra malen (25,4 mm og 31,75 mm). Kristine bestemte 2,5 cm 2026-11-12
    i retrospektiven for epic 3."""
    dokument = _apne(lag_docx(AVSNITT))
    assert dokument.sections
    for seksjon in dokument.sections:
        marger = (
            seksjon.top_margin,
            seksjon.bottom_margin,
            seksjon.left_margin,
            seksjon.right_margin,
        )
        assert [round(m.mm, 1) for m in marger] == [25.0, 25.0, 25.0, 25.0]


@pytest.mark.parametrize("tekst", ["null\x00tegn", "kontroll\x0btegn"])
def test_fr29_tegn_word_ikke_taler_gir_filfeil(tekst):
    """FR-29/AD-9: et tegn Word ikke tåler, gir FilFeil, ikke et annet unntak."""
    with pytest.raises(FilFeil):
        lag_docx(["Første avsnitt.", tekst])
