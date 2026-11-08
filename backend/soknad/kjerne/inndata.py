"""Sjekk av det brukeren skriver inn i skjemaene."""

from soknad.kjerne.feil import FeilType, InndataFeil


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
