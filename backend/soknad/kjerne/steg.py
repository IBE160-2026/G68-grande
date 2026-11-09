"""Stegene i en søknad (AD-8). Serveren eier hvor i søknaden brukeren er.

Fila importerer ikke okt.py, så okt.py kan bruke Steg uten at filene importerer hverandre."""

from enum import IntEnum


class Steg(IntEnum):
    """Stegene i rekkefølge: start < modus < innlegging < resultat < brev."""

    START = 1
    MODUS = 2
    INNLEGGING = 3
    RESULTAT = 4
    BREV = 5


def kan_vises(side: Steg, steg: Steg) -> bool:
    """En side kan vises når sidens steg ikke er lenger fram enn søknadens steg."""
    return side <= steg
