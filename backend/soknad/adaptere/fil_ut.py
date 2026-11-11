"""Filene til nedlastingen (FR-29, FR-30, AD-11). Word lages bare her. PDF kommer i Epic 7.

Filen lages i minnet ved forespørselen og skrives aldri til disk (NFR-4)."""

from io import BytesIO

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Mm

from soknad.kjerne.feil import FilFeil

# Medietypen til en Word-fil (.docx).
DOCX_MEDIETYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
A4_BREDDE = Mm(210)
A4_HOYDE = Mm(297)
# Språket i Word, så stavekontrollen er norsk.
SPRAK = "nb-NO"


def lag_docx(avsnitt: list[str]) -> bytes:
    """Word-filen med brevet: ett avsnitt per element, uten topp- og bunntekst og uten
    markeringer (FR-30). Forfatter og tittel i filens egenskaper er tomme, så filen ikke sier
    «python-docx». Går noe galt (for eksempel et tegn Word ikke tåler), gir den FilFeil."""
    try:
        dokument = Document()
        # Malen i python-docx er amerikansk: Letter-papir og engelsk språk. Brevet får A4 og
        # norsk bokmål, så Word ikke markerer hele brevet som stavefeil.
        for seksjon in dokument.sections:
            seksjon.page_width = A4_BREDDE
            seksjon.page_height = A4_HOYDE
        for sprak in dokument.styles.element.iter(qn("w:lang")):
            sprak.set(qn("w:val"), SPRAK)
        egenskaper = dokument.core_properties
        egenskaper.author = ""
        egenskaper.last_modified_by = ""
        egenskaper.title = ""
        egenskaper.comments = ""
        for tekst in avsnitt:
            dokument.add_paragraph(tekst)
        fil = BytesIO()
        dokument.save(fil)
        return fil.getvalue()
    except Exception as feil:
        raise FilFeil() from feil
