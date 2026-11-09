"""KI-grensesnittet (AD-3). Web-laget bruker bare grensesnittet og vet ikke hvilken utgave
det får. TestKI gir de håndlagde svarene fra testdata/. EkteKI (Claude) kommer i Epic 4."""

from pathlib import Path
from typing import Protocol

from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.ki_svar import kontroller
from soknad.kjerne.testdata_match import Testcase, case_for_annonse, finn_case, lag_testcase

# backend/testdata/, med én mappe per testcase.
TESTDATA_MAPPE = Path(__file__).resolve().parents[2] / "testdata"


class KI(Protocol):
    """Faste signaturer. brev og korrektur kommer i Epic 3 og 5."""

    def nokkelord(self, annonse: str) -> dict: ...

    def gap(self, cv: str, annonse: str) -> dict: ...


def les_testcaser(mappe: Path = TESTDATA_MAPPE) -> list[Testcase]:
    """Leser cv.txt og annonse.txt i hver case-mappe, sortert på navn."""
    return [
        lag_testcase(
            case.name,
            (case / "cv.txt").read_text(encoding="utf-8"),
            (case / "annonse.txt").read_text(encoding="utf-8"),
        )
        for case in sorted(mappe.glob("case-*"))
        if case.is_dir()
    ]


class TestKI:
    """Testmodus: finner testcaset og leser svaret fra testdata/<case>/ki-svar/."""

    # Navnet begynner på Test, men dette er ikke en testklasse for pytest.
    __test__ = False

    def __init__(self, mappe: Path = TESTDATA_MAPPE):
        self.mappe = mappe
        self.caser = les_testcaser(mappe)

    def nokkelord(self, annonse: str) -> dict:
        """Signaturen har bare annonsen, så caset finnes ut fra den."""
        return self._svar(case_for_annonse(annonse, self.caser), "nokkelord")

    def gap(self, cv: str, annonse: str) -> dict:
        """CV-en avgjør caset, og annonsen må høre til samme case."""
        case, _ = finn_case(cv, annonse, self.caser)
        return self._svar(case, "gap")

    def _svar(self, case: str | None, oppgave: str) -> dict:
        # Inndataene sjekkes før KI-en kalles (story 2.5). Dette er bare en sikring.
        if case is None:
            raise KIFeil(KIFeilType.ANNET)
        try:
            tekst = (self.mappe / case / "ki-svar" / f"{oppgave}.json").read_text(encoding="utf-8")
        except OSError as feil:
            raise KIFeil(KIFeilType.ANNET) from feil
        except UnicodeDecodeError as feil:
            raise KIFeil(KIFeilType.UBRUKELIG_SVAR) from feil
        return kontroller(oppgave, tekst)
