"""Teksten fra en opplastet PDF (FR-8, story 6.1). pypdf brukes bare her, og kjerne/ leser
aldri filer.

Fila leses i minnet ved forespørselen og skrives aldri til disk. Verken fila eller teksten
logges (NFR-4)."""

import logging
import re
import unicodedata
from io import BytesIO

from pypdf import PdfReader

# pypdf logger advarsler med rå linjer fra fila (for eksempel «Skipping broken line»). Bare
# feil vises, så ingenting fra fila havner i loggen (NFR-4, retro 6 A6).
logging.getLogger("pypdf").setLevel(logging.ERROR)

# Myk bindestrek (U+00AD) og usynlige tegn uten bredde: U+200B (mellomrom uten bredde), U+200C
# og U+200D (skjøter), U+2060 (ordskjøter) og U+FEFF (BOM). NFKC fjerner dem ikke, og
# telleregelen gir ikke treff på et ord med et slikt tegn inni (utsatt fra story 2.1).
USYNLIGE = re.compile("[\u00ad\u200b-\u200d\u2060\ufeff]")

# Mellomrom og tabulatorer foran et linjeskift. PDF-er fra Word har et mellomrom på slutten av
# hver linje (retro 6 A2). \r tas med, så teksten ikke har \r\n, og et kutt på maks + 1 tegn
# alltid gir mer enn maks tegn når de telles med antall_tegn.
MELLOMROM_FOR_LINJESKIFT = re.compile(r"[ \t\r]+\n")


def normaliser(tekst: str) -> str:
    """Unicode NFKC (æøå som ett tegn også når PDF-en har dem som to), uten myke
    bindestreker og usynlige tegn, og uten mellomrom foran linjeskift. Da gir telleregelen
    samme treff som for den samme teksten fra en .txt-fil, og tegntellingen blir den samme som
    for innlimt tekst."""
    tekst = USYNLIGE.sub("", unicodedata.normalize("NFKC", tekst))
    return MELLOMROM_FOR_LINJESKIFT.sub("\n", tekst)


def les_pdf(innhold: bytes, maks: int | None = None) -> str:
    """Teksten i PDF-en, side for side med linjeskift mellom, normalisert. Ruten sjekker
    filtypen og størrelsen før fila leses (inndata.sjekk_fil). En fil pypdf ikke kan lese, gir
    tom tekst, og tom tekst har under MIN_BOKSTAVER_PDF bokstaver, så feltet får feilen
    uleselig (inndata.er_uleselig, story 6.2). En side pypdf ikke kan lese, gir tom tekst for
    den siden, og de andre sidene leses (retro 6 A5).

    Med maks stopper lesingen når teksten er over maks tegn, og svaret kuttes til maks + 1 tegn.
    Da får feltet fortsatt for_lang, men økten lagrer aldri mer enn maks + 1 tegn (retro 6
    A1). Grensen sjekkes mellom sidene: én side leses alltid hel, og den begrenses av grensen
    på 5 MB for fila."""
    try:
        leser = PdfReader(BytesIO(innhold))
        sider = []
        lengde = -1
        for nummer in range(len(leser.pages)):
            try:
                side = leser.pages[nummer].extract_text() or ""
            except Exception:
                # Én side som ikke kan leses, gjør ikke hele PDF-en tom.
                side = ""
            # Hver side normaliseres med linjeskiftet etter seg, så et mellomrom på slutten av
            # siden også fjernes. Da er "\n".join(sider) den normaliserte teksten, og lengden
            # kan telles side for side uten å normalisere alt på nytt.
            sider.append(normaliser(side + "\n")[:-1])
            lengde += len(sider[-1]) + 1
            if maks is not None and lengde > maks:
                break
    except Exception:
        # pypdf kan kaste mange slags unntak for ødelagte filer. Tom tekst gir uleselig.
        return ""
    tekst = "\n".join(sider)
    return tekst if maks is None else tekst[: maks + 1]
