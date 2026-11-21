"""Filnavnet ved nedlasting (FR-29, AD-11). Filnavn lages bare her.

Mønsteret er Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD> (story 7.5). Arbeidsgiveren kommer fra
nøkkelordsvaret og renses først, fordi den kan ha linjeskift, kontrolltegn og tegn som / og :.
Uten arbeidsgiver, eller når ingenting er igjen etter rensingen, er filnavnet
Soknad_<ÅÅÅÅ-MM-DD>."""

import re
import unicodedata
from datetime import date

# Høyst så mange tegn for arbeidsgiveren i filnavnet.
MAKS_ARBEIDSGIVER = 30

# Æ, ø og å skrives om før resten gjøres om til ASCII, så «Prøvdal» blir «Provdal» og ikke
# «Prvdal». Det samme gjelder andre bokstaver som NFKD ikke deler opp («Straße», «Łódź»).
_AEOEAA = str.maketrans(
    {
        "æ": "ae",
        "ø": "o",
        "å": "a",
        "Æ": "Ae",
        "Ø": "O",
        "Å": "A",
        "ß": "ss",
        "ł": "l",
        "Ł": "L",
        "đ": "d",
        "Đ": "D",
        "œ": "oe",
        "Œ": "Oe",
        "þ": "th",
        "Þ": "Th",
    }
)


def _rens_arbeidsgiver(arbeidsgiver: str | None) -> str:
    """Arbeidsgiveren med bare [A-Za-z0-9-], høyst 30 tegn, eller "" når ingenting er igjen.
    Æøå skrives om, andre tegn gjøres om til ASCII (é → e) eller fjernes. Alt mellomrom (også
    linjeskift og tab) blir bindestrek, flere bindestreker etter hverandre blir én, og
    bindestrek først eller sist fjernes, også etter kuttet til 30 tegn."""
    if not arbeidsgiver:
        return ""
    tekst = unicodedata.normalize("NFKD", arbeidsgiver.translate(_AEOEAA))
    tekst = tekst.encode("ascii", "ignore").decode("ascii")
    tekst = re.sub(r"\s+", "-", tekst)
    tekst = re.sub(r"[^A-Za-z0-9-]", "", tekst)
    tekst = re.sub(r"-+", "-", tekst).strip("-")
    return tekst[:MAKS_ARBEIDSGIVER].strip("-")


def lag_filnavn(dato: date, endelse: str, arbeidsgiver: str | None = None) -> str:
    """«Soknad_Testvik-Utvikling-AS_2026-11-11.docx», eller «Soknad_2026-11-11.docx» uten
    arbeidsgiver. Datoen sendes inn, så filnavnet ikke avhenger av når det regnes ut."""
    navn = _rens_arbeidsgiver(arbeidsgiver)
    midt = f"{navn}_" if navn else ""
    return f"Soknad_{midt}{dato.isoformat()}.{endelse}"
