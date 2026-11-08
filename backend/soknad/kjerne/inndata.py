"""Sjekk av det brukeren skriver inn i skjemaene."""

import re

from soknad.innstillinger import MIN_PASSORD_LENGDE
from soknad.kjerne.feil import FeilType, InndataFeil

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
