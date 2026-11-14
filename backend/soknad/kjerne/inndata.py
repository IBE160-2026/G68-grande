"""Sjekk av det brukeren skriver inn i skjemaene."""

import re

from soknad.innstillinger import MAKS_TEGN, MIN_PASSORD_LENGDE
from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.testdata_match import Testcase, finn_case

# Gyldig form på e-post: noe@noe.noe, uten mellomrom og med bare én @.
GYLDIG_EPOST = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def normaliser_epost(epost: str) -> str:
    """E-post lagres og sammenlignes uten mellomrom foran og bak og uten store bokstaver."""
    return epost.strip().casefold()


def sjekk_innlogging(epost: str, passord: str) -> list[InndataFeil]:
    """Finner tomme felt i innloggingen. Alle feilene kommer samtidig.
    Passordet endres aldri, så bare et helt tomt passord regnes som tomt."""
    feil = []
    if not normaliser_epost(epost):
        feil.append(InndataFeil("epost", FeilType.TOM))
    if not passord:
        feil.append(InndataFeil("passord", FeilType.TOM))
    return feil


def sjekk_registrering(epost: str, passord: str, gjenta: str) -> list[InndataFeil]:
    """Finner feil i registreringen, høyst én per felt og i rekkefølgen e-post, passord,
    gjenta. Om e-posten finnes fra før, sjekkes i databasen (ikke her).
    Passordet endres aldri, så bare et helt tomt passord regnes som tomt."""
    feil = []
    epost = normaliser_epost(epost)
    if not epost:
        feil.append(InndataFeil("epost", FeilType.TOM))
    elif not GYLDIG_EPOST.fullmatch(epost):
        feil.append(InndataFeil("epost", FeilType.EPOST_UGYLDIG))
    if not passord:
        feil.append(InndataFeil("passord", FeilType.TOM))
    elif len(passord) < MIN_PASSORD_LENGDE:
        feil.append(InndataFeil("passord", FeilType.PASSORD_KORT))
    if not gjenta:
        feil.append(InndataFeil("gjenta", FeilType.TOM))
    elif passord and gjenta != passord:
        # Ulike sjekkes bare når begge passordfeltene er fylt.
        feil.append(InndataFeil("gjenta", FeilType.PASSORD_ULIKE))
    return feil


# Feltene på innleggingen, i den rekkefølgen de står på siden.
INNLEGGINGSFELT = ("cv", "annonse")


def antall_tegn(tekst: str) -> int:
    """Antall Unicode-tegn (kodepunkter) i teksten. Et linjeskift som nettleseren sender som
    \\r\\n, telles som ett tegn (NFR-11)."""
    return len(tekst.replace("\r\n", "\n"))


def sjekk_innlegging(cv: str, annonse: str, caser: list[Testcase] | None) -> list[InndataFeil]:
    """Finner feil i innleggingen. Alle feilene kommer samtidig, høyst én per felt og i
    rekkefølgen cv, annonse. Et felt med bare mellomrom er tomt. Tomt sjekkes først, så for
    lang (mer enn MAKS_TEGN tegn, NFR-11), så testdata når caser ikke er None (testmodus,
    FR-34). finn_case gir ikke ikke_testdata på et tomt felt (AD-9), og et felt med for lang
    tekst får heller ikke ikke_testdata."""
    feil = []
    for navn, tekst in zip(INNLEGGINGSFELT, (cv, annonse), strict=True):
        if not tekst.strip():
            feil.append(InndataFeil(navn, FeilType.TOM))
        elif antall_tegn(tekst) > MAKS_TEGN:
            feil.append(InndataFeil(navn, FeilType.FOR_LANG))
    if caser is not None:
        _, testdatafeil = finn_case(cv, annonse, caser)
        har_feil = {f.felt for f in feil}
        feil += [f for f in testdatafeil if f.felt not in har_feil]
    return sorted(feil, key=lambda f: INNLEGGINGSFELT.index(f.felt))
