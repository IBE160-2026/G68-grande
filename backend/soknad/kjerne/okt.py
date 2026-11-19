"""Formen på øktdataene (AD-7). Øktlageret i adaptere/oktlager.py lagrer bare disse.

Søknaden endres bare gjennom funksjonene nederst, som lager en ny Soknad (AD-8)."""

from dataclasses import dataclass, field, replace
from enum import StrEnum

from soknad.innstillinger import MAKS_KI_KALL
from soknad.kjerne.ki_svar import hele_brevet, korrigert_brev
from soknad.kjerne.steg import Steg
from soknad.kjerne.testdata_match import vask


@dataclass(frozen=True)
class Innlogging:
    """Varer til brukeren logger ut."""

    bruker_id: int
    testmodus: bool


class Modus(StrEnum):
    """Modusene på modusvalget, i den rekkefølgen kortene står i (FR-20)."""

    FULL_GENERERING = "full_generering"
    KORREKTUR = "korrektur"


@dataclass(frozen=True)
class Tekstfelt:
    """Det brukeren har lagt inn i ett felt: teksten og navnet på PDF-en, hvis det var en."""

    tekst: str = ""
    filnavn: str | None = None


@dataclass(frozen=True)
class Soknad:
    """Varer én søknad. Å komme til startsiden lager alltid en ny.

    eget_brev er brevet brukeren har skrevet selv, og brukes bare i Korrektur (FR-8). Det
    beholdes også i Full generering, så det ikke er borte når brukeren bytter modus.
    korrektur er det forbedrede brevet i Korrektur (story 5.2.1). forslag er nummeret på
    brevforslaget («Nytt forslag», FR-25). Bare TestKI bruker nummeret. Ekte KI får det, men
    sender det ikke, for hvert kall gir et nytt brev."""

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
    # Søknadsbrevet fra KI-en, i formen fra AD-4 ({avsnitt: [str], navn: str | None}), uten
    # hilsen og navn i avsnittene. ki_svar.hele_brevet setter dem inn. Bare i minnet.
    brev: dict | None = None
    # Det forbedrede brevet i Korrektur, i formen fra kontroller() ({setninger: [{ny, gammel,
    # nytt_avsnitt}]}). ki_svar.korrigert_brev setter det sammen. Bare i minnet.
    korrektur: dict | None = None
    # Nummeret på brevforslaget (FR-25). Det første brevet er forslag 1, og hvert «Nytt
    # forslag» øker det med 1. TestKI gir brev-1 ved oddetall og brev-2 ved partall. Ekte KI
    # sender ikke nummeret, for hvert kall gir et nytt brev.
    forslag: int = 1
    # Formatene brevet er lastet ned i («docx», «pdf», FR-29). Gjelder bare brevet som er der
    # nå. Tom mengde er usann, så «lastet ned i noe format» er bare bool(lastet_ned).
    lastet_ned: frozenset[str] = frozenset()
    opptatt: bool = False
    # KI-kallene søknaden har brukt med ekte KI (NFR-11). En ny søknad begynner på 0.
    ki_kall: int = 0


def begynn(soknad: Soknad, samtykke: bool = False) -> Soknad:
    """«Begynn å lage søknad»: steget blir minst modus, og samtykket lagres (FR-36). Et
    samtykke som alt er gitt, fjernes ikke, så en POST fra en gammel fane mens søknaden er
    lenger fram, endrer ikke søknaden."""
    return replace(soknad, steg=max(soknad.steg, Steg.MODUS), samtykke=soknad.samtykke or samtykke)


def velg_modus(soknad: Soknad, modus: Modus) -> Soknad:
    """Et trykk på et modus-kort. Steget blir innlegging, og gap-analysen og brevet (også det
    forbedrede brevet i Korrektur, og om det er lastet ned) gjelder ikke lenger, fordi analysen
    kjøres på nytt før resultatsiden. forslag blir 1, så det første brevet etterpå er forslag 1
    igjen (FR-25). CV, annonse, eget brev og nøkkelordlisten beholdes."""
    return replace(
        soknad,
        modus=modus,
        steg=Steg.INNLEGGING,
        gap=None,
        brev=None,
        korrektur=None,
        forslag=1,
        lastet_ned=frozenset(),
    )


def sett_inndata(
    soknad: Soknad, *, cv: Tekstfelt, annonse: Tekstfelt, eget_brev: Tekstfelt | None = None
) -> Soknad:
    """Lagrer det brukeren har lagt inn («Sjekk CV-en min» og «Tilbake»). eget_brev er None i
    Full generering, og da er brevet i søknaden uendret. Bare teksten i feltene avgjør om noe
    er endret, ikke filnavnet (retro 2, A9). Er teksten i alle feltene lik som før, lagres
    feltene (med et nytt filnavn, hvis brukeren lastet opp samme tekst som PDF), og resten av
    søknaden er uendret. Er teksten i ett av dem endret, også bare i det egne brevet (FR-8),
    gjelder ikke resultatene lenger: gap-analysen, brevet, det forbedrede brevet i Korrektur og
    lastet_ned nullstilles, forslag blir 1 (FR-25), og steget blir høyst innlegging, så
    resultatsiden ikke vises før analysen har lyktes igjen med et brev som har bestått sjekken
    (AD-8). Nøkkelordlisten, den vaskede annonseteksten den ble laget fra og arbeidsgiveren
    beholdes sammen når den vaskede annonseteksten er lik den listen ble laget fra (samme vask
    som AD-10, så ekstra mellomrom og tegnsetting regnes som likt). Da kjøres bare
    gap-analysen på nytt, og prosenten regnes fra samme liste (FR-15, FR-19). Ellers
    nullstilles alle tre, og listen hentes på nytt."""
    if eget_brev is None:
        eget_brev = soknad.eget_brev
    if (soknad.cv.tekst, soknad.annonse.tekst, soknad.eget_brev.tekst) == (
        cv.tekst,
        annonse.tekst,
        eget_brev.tekst,
    ):
        if (soknad.cv, soknad.annonse, soknad.eget_brev) == (cv, annonse, eget_brev):
            return soknad
        return replace(soknad, cv=cv, annonse=annonse, eget_brev=eget_brev)
    # En annonse uten bokstaver og tall vaskes til "", og den skal ikke regnes som lik en annen.
    behold = bool(soknad.nokkelord_annonse) and vask(annonse.tekst) == soknad.nokkelord_annonse
    return replace(
        soknad,
        cv=cv,
        annonse=annonse,
        eget_brev=eget_brev,
        nokkelord=soknad.nokkelord if behold else None,
        nokkelord_annonse=soknad.nokkelord_annonse if behold else None,
        arbeidsgiver=soknad.arbeidsgiver if behold else None,
        gap=None,
        brev=None,
        korrektur=None,
        forslag=1,
        lastet_ned=frozenset(),
        steg=min(soknad.steg, Steg.INNLEGGING),
    )


def sett_opptatt(soknad: Soknad, opptatt: bool) -> Soknad:
    """Settes rundt et KI-kall. Mens opptatt er sann, startes ikke et nytt kall (AD-8, FR-27).
    Resten av søknaden er uendret."""
    return replace(soknad, opptatt=opptatt)


def sett_analyse(soknad: Soknad, *, nokkelord: dict, gap: dict) -> Soknad:
    """Lagrer analysen når KI-kallene har lyktes («Sjekk CV-en min»). nokkelord og gap har
    formen fra AD-4. Når nøkkelordlisten gjenbrukes (FR-15), gir ruten den lagrede listen og
    arbeidsgiveren i formen fra AD-4, så de skrives tilbake uendret. Annonseteksten listen ble
    laget fra, lagres vasket (samme vask som AD-10), så sett_inndata kan se om annonsen er
    endret (FR-19). Steget blir minst resultat (AD-8)."""
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
    return replace(soknad, brev=brev, lastet_ned=frozenset(), steg=max(soknad.steg, Steg.BREV))


def sett_korrektur(soknad: Soknad, korrektur: dict) -> Soknad:
    """Lagrer det forbedrede brevet når KI-kallet har lyktes («Oppdater søknadsbrevet mitt» i
    Korrektur). korrektur har formen fra kontroller(). Steget blir minst brev (AD-8). Et nytt
    brev er ikke lastet ned ennå."""
    return replace(
        soknad, korrektur=korrektur, lastet_ned=frozenset(), steg=max(soknad.steg, Steg.BREV)
    )


def ferdig_brev(soknad: Soknad) -> list[str] | None:
    """Brevet som vises på brevsiden og lastes ned, som avsnitt: korrigert_brev i Korrektur,
    hele_brevet ellers, og None når det ikke finnes noe brev ennå. Dette er det eneste stedet
    som velger mellom brev og korrektur, så siden og Word-fila alltid har det samme brevet."""
    if soknad.modus == Modus.KORREKTUR:
        return None if soknad.korrektur is None else korrigert_brev(soknad.korrektur)
    return None if soknad.brev is None else hele_brevet(soknad.brev)


def nytt_forslag(soknad: Soknad) -> Soknad:
    """«Ja, lag nytt forslag» (FR-25): forslag øker med 1, og brevet, det forbedrede brevet i
    Korrektur og lastet_ned nullstilles, så nedlastingsknappen og filnavn-linjen er som før
    nedlasting. Det egne brevet beholdes, så KI-en i Korrektur alltid får det opprinnelige
    brevet. Steget og resten av søknaden er uendret. Ruten bruker den inni KI-kallet, så det
    gamle brevet står igjen når kallet feiler (AD-8)."""
    return replace(
        soknad, forslag=soknad.forslag + 1, brev=None, korrektur=None, lastet_ned=frozenset()
    )


def sett_lastet_ned(soknad: Soknad, format: str) -> Soknad:
    """Brevet er lastet ned i format («docx» eller «pdf», FR-29): formatet legges til
    lastet_ned, og formatene som alt er der, beholdes. Resten av søknaden er uendret."""
    return replace(soknad, lastet_ned=soknad.lastet_ned | {format})


def har_plass_til(soknad: Soknad, antall: int) -> bool:
    """Sann når søknaden kan bruke antall KI-kall til uten å gå over MAKS_KI_KALL (NFR-11).
    En handling startes bare når alle kallene den trenger, får plass (analysen trenger 2, eller
    1 når nøkkelordlisten gjenbrukes, brevet 1), så grensen aldri passeres."""
    return soknad.ki_kall + antall <= MAKS_KI_KALL


def tell_ki_kall(soknad: Soknad, antall: int) -> Soknad:
    """Legger antall KI-kall til telleren (NFR-11). Hvert kall telles når det startes, også
    når det feiler. Resten av søknaden er uendret. har_plass_til må kalles først. Begge brukes
    av hjelperen for KI-kallet i web/ruter.py (_med_ki), som alle KI-kallene går gjennom, også
    Korrektur og «Nytt forslag»."""
    return replace(soknad, ki_kall=soknad.ki_kall + antall)
