"""Sjekk av det brukeren skriver inn i skjemaene."""

import re
from collections.abc import Iterable

from soknad.innstillinger import (
    MAKS_FILSTORRELSE,
    MAKS_TEGN,
    MAKS_TEGN_EGET_BREV,
    MIN_BOKSTAVER_PDF,
    MIN_PASSORD_LENGDE,
)
from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.okt import Modus
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


# Alle feltene på innleggingen, i den rekkefølgen de står på siden. eget_brev står bare på
# siden i Korrektur (felt_for_modus).
INNLEGGINGSFELT = ("cv", "eget_brev", "annonse")


def felt_for_modus(modus: Modus | None) -> tuple[str, ...]:
    """Feltene på innleggingen for modusen, i rekkefølgen på siden og i feilboksen: CV og
    annonse i Full generering, og CV, eget brev og annonse i Korrektur (FR-8). Sjekken, ruten
    og malen bruker alle denne, så rekkefølgen alltid er lik."""
    if modus == Modus.KORREKTUR:
        return INNLEGGINGSFELT
    return tuple(navn for navn in INNLEGGINGSFELT if navn != "eget_brev")


def antall_tegn(tekst: str) -> int:
    """Antall Unicode-tegn (kodepunkter) i teksten. Et linjeskift som nettleseren sender som
    \\r\\n, telles som ett tegn (NFR-11)."""
    return len(tekst.replace("\r\n", "\n"))


def maks_tegn(felt: str) -> int:
    """Høyeste antall tegn feltet godtar (NFR-11). Brevfeltet i Korrektur har en lavere grense
    enn CV og annonse (retro 5, runde B)."""
    return MAKS_TEGN_EGET_BREV if felt == "eget_brev" else MAKS_TEGN


# Starten på hver PDF-fil. Den må stå blant de første PDF_START_BYTES bytene.
PDF_MERKE = b"%PDF-"
PDF_START_BYTES = 1024


def sjekk_fil(filnavn: str, innhold: bytes) -> FeilType | None:
    """Sjekken av en ny opplastet fil før den leses (FR-10, FR-12, story 6.2). Først
    feil_filtype når navnet ikke slutter på .pdf (uansett store og små bokstaver), eller når
    %PDF- ikke står i de første 1 024 bytene (for eksempel en .docx som er omdøpt til .pdf).
    Så for_stor når fila er over MAKS_FILSTORRELSE. Ellers None, og fila kan leses. Kjernen får
    bare navnet og bytene og leser aldri filer selv."""
    if not filnavn.lower().endswith(".pdf") or PDF_MERKE not in innhold[:PDF_START_BYTES]:
        return FeilType.FEIL_FILTYPE
    if len(innhold) > MAKS_FILSTORRELSE:
        return FeilType.FOR_STOR
    return None


def er_uleselig(tekst: str) -> bool:
    """Teksten fra en PDF har færre enn MIN_BOKSTAVER_PDF bokstaver, så PDF-en regnes som
    uleselig, for eksempel skannet (FR-11, story 6.2). En PDF pypdf ikke klarer å lese, gir tom
    tekst og dermed også uleselig."""
    return sum(tegn.isalpha() for tegn in tekst) < MIN_BOKSTAVER_PDF


def sjekk_innlegging(
    cv: str,
    annonse: str,
    caser: list[Testcase] | None,
    eget_brev: str | None = None,
    filfeil: Iterable[InndataFeil] = (),
) -> list[InndataFeil]:
    """Finner feil i innleggingen. eget_brev er None i Full generering, og er teksten i
    brevfeltet i Korrektur (FR-8). Alle feilene kommer samtidig, høyst én per felt og i
    rekkefølgen fra felt_for_modus.

    Rekkefølgen per felt er tom → feil_filtype → for_stor → uleselig → for_lang →
    ikke_testdata. Et felt med bare mellomrom er tomt. filfeil er feilene for nye filer, som
    ruten har funnet med sjekk_fil og er_uleselig (story 6.2). Et felt med en filfeil er aldri
    tomt (det kom en fil), selv om teksten er tom etter feilen, så filfeilen tas først. Feltet
    får den feilen og ingen annen: det hoppes over i sjekken av tomt og for lang og i
    testdatasjekken.
    For lang (mer enn maks_tegn(felt) tegn, NFR-11) står etter filfeilene, siden den trenger
    lesbar tekst. Testdata sjekkes når caser ikke er None (testmodus, FR-34). finn_case gir ikke
    ikke_testdata på et tomt felt (AD-9), og et felt med for lang tekst får heller ikke
    ikke_testdata."""
    tekster = {"cv": cv, "annonse": annonse, "eget_brev": eget_brev}
    felt = felt_for_modus(Modus.FULL_GENERERING if eget_brev is None else Modus.KORREKTUR)
    med_filfeil = {f.felt: f for f in filfeil if f.felt in felt}
    feil = []
    for navn in felt:
        tekst = tekster[navn]
        if navn in med_filfeil:
            feil.append(med_filfeil[navn])
        elif not tekst.strip():
            feil.append(InndataFeil(navn, FeilType.TOM))
        elif antall_tegn(tekst) > maks_tegn(navn):
            feil.append(InndataFeil(navn, FeilType.FOR_LANG))
    if caser is not None:
        _, testdatafeil = finn_case(cv, annonse, caser, eget_brev=eget_brev)
        har_feil = {f.felt for f in feil}
        feil += [f for f in testdatafeil if f.felt not in har_feil]
    return sorted(feil, key=lambda f: felt.index(f.felt))
