"""Filene til nedlastingen (FR-29, FR-30, AD-11). Word og PDF lages bare her.

Filen lages i minnet ved forespørselen og skrives aldri til disk (NFR-4)."""

from io import BytesIO
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Mm
from fpdf import FPDF
from fpdf.enums import XPos, YPos

from soknad.kjerne.feil import FilFeil

# Medietypen til en Word-fil (.docx).
DOCX_MEDIETYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
A4_BREDDE = Mm(210)
A4_HOYDE = Mm(297)
# Margen på alle fire sider. Malen i python-docx har 25,4 mm oppe og nede og 31,75 mm til
# venstre og høyre. Kristine bestemte 2,5 cm rundt hele 2026-11-12 (retrospektiven for epic 3).
MARG = Mm(25)
# Språket i Word og PDF, så stavekontrollen og skjermleseren bruker norsk.
SPRAK = "nb-NO"

# Medietypen til en PDF-fil.
PDF_MEDIETYPE = "application/pdf"
# Skriften i PDF-en: Noto Sans, 11 pt (bestemt av Kristine 19. november 2026). Den har æøå og
# fri lisens (OFL). Lisensen ligger i OFL.txt ved siden av. Word-fila beholder sin skrift.
SKRIFT = Path(__file__).resolve().parents[1] / "fonts" / "NotoSans-Regular.ttf"
SKRIFT_NAVN = "NotoSans"
SKRIFT_STORRELSE = 11
# Margen i PDF-en i millimeter, den samme som MARG i Word-fila.
PDF_MARG_MM = 25
# Høyden på én linje og luften mellom avsnittene, i millimeter.
LINJEHOYDE_MM = 5.5
AVSNITT_LUFT_MM = 4


def lag_docx(avsnitt: list[str]) -> bytes:
    """Word-filen med brevet: ett avsnitt per element, uten topp- og bunntekst og uten
    markeringer (FR-30). Forfatter og tittel i filens egenskaper er tomme, så filen ikke sier
    «python-docx». Går noe galt (for eksempel et tegn Word ikke tåler), gir den FilFeil."""
    try:
        dokument = Document()
        # Malen i python-docx er amerikansk: Letter-papir og engelsk språk. Brevet får A4,
        # margen i MARG og norsk bokmål, så Word ikke markerer hele brevet som stavefeil.
        for seksjon in dokument.sections:
            seksjon.page_width = A4_BREDDE
            seksjon.page_height = A4_HOYDE
            seksjon.top_margin = MARG
            seksjon.bottom_margin = MARG
            seksjon.left_margin = MARG
            seksjon.right_margin = MARG
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


def lag_pdf(avsnitt: list[str]) -> bytes:
    """PDF-filen med brevet: ett avsnitt per element, med luft mellom, uten topp- og bunntekst
    og uten markeringer (FR-30). A4 med margen i PDF_MARG_MM, skriften i SKRIFT og norsk språk,
    som Word-fila. Forfatter, tittel og produsent er tomme, så filen ikke sier «fpdf2». Et tegn
    skriften ikke har (for eksempel emoji), gir ingen feil, men vises ikke. Går noe galt (for
    eksempel at skriften mangler), gir den FilFeil."""
    try:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_margins(PDF_MARG_MM, PDF_MARG_MM, PDF_MARG_MM)
        # Ingen ekstra luft inni cellene, så teksten begynner ved margen, som i Word-fila.
        pdf.c_margin = 0
        pdf.set_auto_page_break(True, margin=PDF_MARG_MM)
        pdf.set_lang(SPRAK)
        pdf.set_author("")
        pdf.set_title("")
        pdf.set_creator("")
        pdf.set_producer("")
        pdf.add_font(SKRIFT_NAVN, "", SKRIFT)
        pdf.set_font(SKRIFT_NAVN, size=SKRIFT_STORRELSE)
        pdf.add_page()
        for nummer, tekst in enumerate(avsnitt):
            if nummer:
                pdf.ln(AVSNITT_LUFT_MM)
            pdf.multi_cell(0, LINJEHOYDE_MM, tekst, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        return bytes(pdf.output())
    except Exception as feil:
        raise FilFeil() from feil
