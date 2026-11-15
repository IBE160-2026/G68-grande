"""Gjenkjenning av testdata i testmodus (AD-10, FR-34). Kjernen leser ingen filer, så de
kjente testcasene kommer inn som data fra adaptere/ki.py."""

import unicodedata
from dataclasses import dataclass

from soknad.kjerne.feil import FeilType, InndataFeil


def vask(tekst: str) -> str:
    """Unicode NFKC, så casefold(), og bare bokstaver og tall beholdes. Da gir samme tekst
    med andre mellomrom, linjeskift og store bokstaver samme resultat."""
    tekst = unicodedata.normalize("NFKC", tekst).casefold()
    return "".join(tegn for tegn in tekst if tegn.isalnum())


@dataclass(frozen=True)
class Testcase:
    """Et kjent testcase med vasket CV, vasket annonse og vasket eget brev. eget_brev er None
    når caset ikke har noe brev til Korrektur (story 5.1)."""

    navn: str
    cv: str
    annonse: str
    eget_brev: str | None = None


def lag_testcase(navn: str, cv: str, annonse: str, eget_brev: str | None = None) -> Testcase:
    """Lager et testcase av teksten i testfilene."""
    return Testcase(navn, vask(cv), vask(annonse), None if eget_brev is None else vask(eget_brev))


def case_for_annonse(annonse: str, caser: list[Testcase]) -> str | None:
    """Navnet på første case som har denne annonsen, eller None."""
    vasket = vask(annonse)
    return next((case.navn for case in caser if case.annonse == vasket), None)


def finn_case(
    cv: str, annonse: str, caser: list[Testcase], eget_brev: str | None = None
) -> tuple[str | None, list[InndataFeil]]:
    """CV-en avgjør testcaset. Gir (navnet på caset, []) når CV og annonse (og eget_brev når
    det ikke er None, i Korrektur) hører til samme case, ellers (None, feilene). Alle feilene
    kommer samtidig, i rekkefølgen cv, eget_brev, annonse. Et tomt felt får ingen
    ikke_testdata, fordi tom sjekkes først (AD-9). Er annonsen annonsen i et annet case enn
    CV-en, får den annen_case i stedet for ikke_testdata (story 4.5).

    Et eget brev som ikke er brevet i caset til CV-en, får ikke_testdata, også når caset ikke
    har noe brev (case 2, bestemt av Kristine 15. november 2026). Er CV-en ukjent, får brevet
    feil bare hvis det ikke er brevet i noe case, som annonsen (story 5.1)."""
    feil = []
    cv_tom = not cv.strip()
    annonse_tom = not annonse.strip()
    brev_tom = eget_brev is not None and not eget_brev.strip()
    vasket_cv = vask(cv)
    vasket_annonse = vask(annonse)
    vasket_brev = None if eget_brev is None else vask(eget_brev)
    case = next((c for c in caser if c.cv == vasket_cv), None)
    sjekk_brev = eget_brev is not None and not brev_tom

    if case is None:
        if not cv_tom:
            feil.append(InndataFeil("cv", FeilType.IKKE_TESTDATA))
        if sjekk_brev and not any(c.eget_brev == vasket_brev for c in caser):
            feil.append(InndataFeil("eget_brev", FeilType.IKKE_TESTDATA))
        # Uten case fra CV-en får annonsen feil bare hvis den ikke er annonsen i noe case.
        if not annonse_tom and not any(c.annonse == vasket_annonse for c in caser):
            feil.append(InndataFeil("annonse", FeilType.IKKE_TESTDATA))
    else:
        if sjekk_brev and case.eget_brev != vasket_brev:
            feil.append(InndataFeil("eget_brev", FeilType.IKKE_TESTDATA))
        if not annonse_tom and case.annonse != vasket_annonse:
            annen_case = any(c.annonse == vasket_annonse for c in caser)
            feiltype = FeilType.ANNEN_CASE if annen_case else FeilType.IKKE_TESTDATA
            feil.append(InndataFeil("annonse", feiltype))

    if feil or cv_tom or annonse_tom or brev_tom:
        return None, feil
    return case.navn, []
