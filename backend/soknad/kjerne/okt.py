"""Formen på øktdataene (AD-7). Øktlageret i adaptere/oktlager.py lagrer bare disse.

Søknaden endres bare gjennom funksjonene nederst, som lager en ny Soknad (AD-8)."""

from dataclasses import dataclass, field, replace
from enum import StrEnum

from soknad.kjerne.steg import Steg


@dataclass(frozen=True)
class Innlogging:
    """Varer til brukeren logger ut."""

    bruker_id: int
    testmodus: bool


class Modus(StrEnum):
    """Modusene på modusvalget. Korrektur kommer i Epic 5."""

    FULL_GENERERING = "full_generering"


@dataclass(frozen=True)
class Tekstfelt:
    """Det brukeren har lagt inn i ett felt: teksten og navnet på PDF-en, hvis det var en."""

    tekst: str = ""
    filnavn: str | None = None


@dataclass(frozen=True)
class Soknad:
    """Varer én søknad. Å komme til startsiden lager alltid en ny.

    brev, korrektur, forslag og lastet_ned legges til i Epic 3 og 5, med de navnene."""

    steg: Steg = Steg.START
    modus: Modus | None = None
    samtykke: bool = False
    cv: Tekstfelt = field(default_factory=Tekstfelt)
    annonse: Tekstfelt = field(default_factory=Tekstfelt)
    eget_brev: Tekstfelt = field(default_factory=Tekstfelt)
    # Nøkkelordlisten fra KI-en og den vaskede annonseteksten den ble laget fra (FR-19).
    nokkelord: tuple[str, ...] | None = None
    nokkelord_annonse: str | None = None
    arbeidsgiver: str | None = None
    gap: dict | None = None
    opptatt: bool = False


def begynn(soknad: Soknad) -> Soknad:
    """«Begynn å lage søknad»: steget blir minst modus."""
    return replace(soknad, steg=max(soknad.steg, Steg.MODUS))


def velg_modus(soknad: Soknad, modus: Modus) -> Soknad:
    """Et trykk på et modus-kort. Steget blir innlegging, og gap-analysen gjelder ikke lenger,
    fordi analysen kjøres på nytt før resultatsiden. CV, annonse og nøkkelordlisten beholdes."""
    return replace(soknad, modus=modus, steg=Steg.INNLEGGING, gap=None)
