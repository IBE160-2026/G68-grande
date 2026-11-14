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
    """Et kjent testcase med vasket CV og vasket annonse."""

    navn: str
    cv: str
    annonse: str


def lag_testcase(navn: str, cv: str, annonse: str) -> Testcase:
    """Lager et testcase av teksten i testfilene."""
    return Testcase(navn, vask(cv), vask(annonse))


def case_for_annonse(annonse: str, caser: list[Testcase]) -> str | None:
    """Navnet på første case som har denne annonsen, eller None."""
    vasket = vask(annonse)
    return next((case.navn for case in caser if case.annonse == vasket), None)


def finn_case(cv: str, annonse: str, caser: list[Testcase]) -> tuple[str | None, list[InndataFeil]]:
    """CV-en avgjør testcaset. Gir (navnet på caset, []) når CV og annonse hører til samme
    case, ellers (None, feilene). Alle feilene kommer samtidig, cv først. Et tomt felt får
    ingen ikke_testdata, fordi tom sjekkes først (AD-9). Er annonsen annonsen i et annet case
    enn CV-en, får den annen_case i stedet for ikke_testdata (story 4.5)."""
    feil = []
    cv_tom = not cv.strip()
    annonse_tom = not annonse.strip()
    vasket_cv = vask(cv)
    vasket_annonse = vask(annonse)
    case = next((c for c in caser if c.cv == vasket_cv), None)

    if case is None:
        if not cv_tom:
            feil.append(InndataFeil("cv", FeilType.IKKE_TESTDATA))
        # Uten case fra CV-en får annonsen feil bare hvis den ikke er annonsen i noe case.
        if not annonse_tom and not any(c.annonse == vasket_annonse for c in caser):
            feil.append(InndataFeil("annonse", FeilType.IKKE_TESTDATA))
    elif not annonse_tom and case.annonse != vasket_annonse:
        annen_case = any(c.annonse == vasket_annonse for c in caser)
        feiltype = FeilType.ANNEN_CASE if annen_case else FeilType.IKKE_TESTDATA
        feil.append(InndataFeil("annonse", feiltype))

    if feil or cv_tom or annonse_tom:
        return None, feil
    return case.navn, []
