"""Formen på øktdataene (AD-7). Øktlageret i adaptere/oktlager.py lagrer bare disse.

Søknaden endres bare gjennom funksjonene nederst, som lager en ny Soknad (AD-8)."""

from dataclasses import dataclass, field, replace
from enum import StrEnum

from soknad.kjerne.steg import Steg
from soknad.kjerne.testdata_match import vask


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

    korrektur og forslag legges til i Epic 5 og Epic 7, med de navnene."""

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
    # Søknadsbrevet fra KI-en, i formen fra AD-4 ({avsnitt: [str]}). Bare i minnet.
    brev: dict | None = None
    # Sann når brevet er lastet ned som Word (FR-29). Gjelder bare brevet som er der nå.
    lastet_ned: bool = False
    opptatt: bool = False


def begynn(soknad: Soknad, samtykke: bool = False) -> Soknad:
    """«Begynn å lage søknad»: steget blir minst modus, og samtykket lagres (FR-36). Et
    samtykke som alt er gitt, fjernes ikke, så en POST fra en gammel fane mens søknaden er
    lenger fram, endrer ikke søknaden."""
    return replace(soknad, steg=max(soknad.steg, Steg.MODUS), samtykke=soknad.samtykke or samtykke)


def velg_modus(soknad: Soknad, modus: Modus) -> Soknad:
    """Et trykk på et modus-kort. Steget blir innlegging, og gap-analysen og brevet (og om det
    er lastet ned) gjelder ikke lenger, fordi analysen kjøres på nytt før resultatsiden. CV,
    annonse og nøkkelordlisten beholdes."""
    return replace(soknad, modus=modus, steg=Steg.INNLEGGING, gap=None, brev=None, lastet_ned=False)


def sett_inndata(soknad: Soknad, *, cv: Tekstfelt, annonse: Tekstfelt) -> Soknad:
    """Lagrer det brukeren har lagt inn («Sjekk CV-en min» og «Tilbake»). Er begge feltene
    like som før, er søknaden uendret. Ellers gjelder ikke resultatene lenger: nøkkelordlisten,
    arbeidsgiveren, gap-analysen, brevet og lastet_ned nullstilles, og steget blir høyst
    innlegging, så resultatsiden ikke vises før analysen har lyktes igjen (AD-8). Gjenbruk av
    nøkkelordlisten når bare CV-en er endret, kommer i Epic 7."""
    if soknad.cv == cv and soknad.annonse == annonse:
        return soknad
    return replace(
        soknad,
        cv=cv,
        annonse=annonse,
        nokkelord=None,
        nokkelord_annonse=None,
        arbeidsgiver=None,
        gap=None,
        brev=None,
        lastet_ned=False,
        steg=min(soknad.steg, Steg.INNLEGGING),
    )


def sett_opptatt(soknad: Soknad, opptatt: bool) -> Soknad:
    """Settes rundt et KI-kall. Mens opptatt er sann, startes ikke et nytt kall (AD-8, FR-27).
    Resten av søknaden er uendret."""
    return replace(soknad, opptatt=opptatt)


def sett_analyse(soknad: Soknad, *, nokkelord: dict, gap: dict) -> Soknad:
    """Lagrer analysen når begge KI-kallene har lyktes («Sjekk CV-en min»). nokkelord og gap
    har formen fra AD-4. Annonseteksten listen ble laget fra, lagres vasket (samme vask som
    AD-10), så Epic 7 kan se om annonsen er endret. Steget blir minst resultat (AD-8)."""
    return replace(
        soknad,
        nokkelord=tuple(nokkelord["nokkelord"]),
        nokkelord_annonse=vask(soknad.annonse.tekst),
        arbeidsgiver=nokkelord["arbeidsgiver"],
        gap=gap,
        steg=max(soknad.steg, Steg.RESULTAT),
    )


def sett_brev(soknad: Soknad, brev: dict) -> Soknad:
    """Lagrer brevet når KI-kallet har lyktes («Lag søknadsbrevet mitt»). brev har formen fra
    AD-4. Steget blir minst brev (AD-8). Et nytt brev er ikke lastet ned ennå."""
    return replace(soknad, brev=brev, lastet_ned=False, steg=max(soknad.steg, Steg.BREV))


def sett_lastet_ned(soknad: Soknad) -> Soknad:
    """Brevet er lastet ned (FR-29). Resten av søknaden er uendret."""
    return replace(soknad, lastet_ned=True)
