"""Tabellprøven i story 6.1: en fiktiv CV med ferdighetene i en tabell.

Skriptet lager tabell-cv.docx med python-docx (fila er ikke i Git, fordi .gitignore har
*.docx). Word lagrer den som tabell-cv.pdf (Fil > Lagre som > PDF, eller med Word gjennom
PowerShell som scripts/lag_testpdf.ps1). Med --les leses teksten med les_pdf fra
backend/soknad/adaptere/pdf_inn.py og skrives i tabell-cv-lest.txt. Alle opplysningene er
oppdiktet.

Kjøres fra backend/:

    uv run python ../my-project/testkjoringer/6-1/lag_tabellprove.py
    uv run python ../my-project/testkjoringer/6-1/lag_tabellprove.py --les
"""

import sys
from pathlib import Path

MAPPE = Path(__file__).resolve().parent
DOCX = MAPPE / "tabell-cv.docx"
PDF = MAPPE / "tabell-cv.pdf"
TEKST = MAPPE / "tabell-cv-lest.txt"

FERDIGHETER = [
    ("Ferdighet", "Nivå", "Brukt i"),
    ("Python", "God", "Bacheloroppgave og deltidsjobb"),
    ("JavaScript", "Middels", "Nettside for idrettslaget"),
    ("SQL", "Middels", "Emnet databaser"),
    ("Git", "God", "Alle prosjektene"),
]


def lag_docx():
    from docx import Document

    dokument = Document()
    dokument.add_paragraph("Tobias Tabellsen")
    dokument.add_paragraph("E-post: tobias.tabellsen@example.com")
    dokument.add_paragraph("Om meg")
    dokument.add_paragraph("Jeg er student i andre år på bachelor i IT og liker å lage nettsider.")
    dokument.add_paragraph("Ferdigheter")
    tabell = dokument.add_table(rows=len(FERDIGHETER), cols=3)
    tabell.style = "Table Grid"
    for rad, verdier in zip(tabell.rows, FERDIGHETER, strict=True):
        for celle, verdi in zip(rad.cells, verdier, strict=True):
            celle.text = verdi
    dokument.add_paragraph("Erfaring")
    dokument.add_paragraph("2025–2026: Deltidsjobb som kundeservicemedarbeider, Eksempel AS")
    dokument.save(DOCX)
    print(f"Laget {DOCX.name}")


def les():
    sys.path.insert(0, str(Path.cwd()))
    from soknad.adaptere.pdf_inn import les_pdf

    tekst = les_pdf(PDF.read_bytes())
    TEKST.write_text(tekst, encoding="utf-8")
    print(tekst)


if __name__ == "__main__":
    les() if "--les" in sys.argv else lag_docx()
