"""Teksten fra en opplastet PDF (FR-8, story 6.1). pypdf brukes bare her, og kjerne/ leser
aldri filer.

Fila leses i minnet ved forespørselen og skrives aldri til disk. Verken fila eller teksten
logges (NFR-4)."""

import re
import unicodedata
from io import BytesIO

from pypdf import PdfReader

# Myk bindestrek (U+00AD) og usynlige tegn uten bredde: U+200B (mellomrom uten bredde), U+200C
# og U+200D (skjøter), U+2060 (ordskjøter) og U+FEFF (BOM). NFKC fjerner dem ikke, og
# telleregelen gir ikke treff på et ord med et slikt tegn inni (utsatt fra story 2.1).
USYNLIGE = re.compile("[\u00ad\u200b-\u200d\u2060\ufeff]")


def normaliser(tekst: str) -> str:
    """Unicode NFKC (æøå som ett tegn også når PDF-en har dem som to), og uten myke
    bindestreker og usynlige tegn. Da gir telleregelen samme treff som for den samme teksten
    fra en .txt-fil."""
    return USYNLIGE.sub("", unicodedata.normalize("NFKC", tekst))


def les_pdf(innhold: bytes) -> str:
    """Teksten i PDF-en, side for side med linjeskift mellom, normalisert. Ruten sjekker
    filtypen og størrelsen før fila leses (inndata.sjekk_fil). En fil pypdf ikke kan lese, gir
    tom tekst, og tom tekst har under MIN_BOKSTAVER_PDF bokstaver, så feltet får feilen
    uleselig (inndata.er_uleselig, story 6.2)."""
    try:
        leser = PdfReader(BytesIO(innhold))
        tekst = "\n".join(side.extract_text() or "" for side in leser.pages)
    except Exception:
        # pypdf kan kaste mange slags unntak for ødelagte filer. Tom tekst gir uleselig.
        return ""
    return normaliser(tekst)
