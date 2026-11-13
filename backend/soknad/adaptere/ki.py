"""KI-grensesnittet (AD-3). Web-laget bruker bare grensesnittet og vet ikke hvilken utgave
det får. TestKI gir de håndlagde svarene fra testdata/. EkteKI sender teksten til Claude.
anthropic importeres bare her, aldri i kjerne/."""

import logging
from pathlib import Path
from typing import Protocol

from anthropic import Anthropic, AnthropicError, APIConnectionError, APITimeoutError

from soknad.innstillinger import (
    KI_INNSATS,
    KI_MAKS_TOKENS,
    KI_NYE_FORSOK,
    KI_PRIS_INN,
    KI_PRIS_UT,
    KI_TIDSGRENSE,
    KRONER_PER_DOLLAR,
)
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.ki_svar import kontroller
from soknad.kjerne.testdata_match import Testcase, case_for_annonse, finn_case, lag_testcase

# backend/testdata/, med én mappe per testcase.
TESTDATA_MAPPE = Path(__file__).resolve().parents[2] / "testdata"

# backend/prompts/, med én prompt-fil per KI-oppgave (i Git).
PROMPT_MAPPE = Path(__file__).resolve().parents[2] / "prompts"

# Loggen viser bare oppgave, tokens, pris og feiltype, aldri CV, annonse, nøkkel eller svar.
logger = logging.getLogger(__name__)

_TEKSTLISTE = {"type": "array", "items": {"type": "string"}}

# JSON-skjemaet for hver oppgave, sendt med output_config.format (AD-4). Alle felt er påkrevd,
# og ingen andre felt er lov. arbeidsgiver er null når annonsen ikke har noe navn.
SKJEMA = {
    "nokkelord": {
        "type": "object",
        "properties": {
            "nokkelord": _TEKSTLISTE,
            "arbeidsgiver": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        },
        "required": ["nokkelord", "arbeidsgiver"],
        "additionalProperties": False,
    },
    "gap": {
        "type": "object",
        "properties": {"dekker": _TEKSTLISTE, "mangler": _TEKSTLISTE},
        "required": ["dekker", "mangler"],
        "additionalProperties": False,
    },
    "brev": {
        "type": "object",
        "properties": {"avsnitt": _TEKSTLISTE},
        "required": ["avsnitt"],
        "additionalProperties": False,
    },
}


class KI(Protocol):
    """Faste signaturer. korrektur kommer i Epic 5."""

    def nokkelord(self, annonse: str) -> dict: ...

    def gap(self, cv: str, annonse: str) -> dict: ...

    def brev(self, cv: str, annonse: str, forslag: int) -> dict: ...


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

    def brev(self, cv: str, annonse: str, forslag: int) -> dict:
        """Caset finnes som i gap. Oddetall for forslag gir brev-1.json, partall brev-2.json
        (brukes først i Epic 7). I Epic 3 er forslag alltid 1."""
        case, _ = finn_case(cv, annonse, self.caser)
        return self._svar(case, "brev", f"brev-{1 if forslag % 2 else 2}")

    def _svar(self, case: str | None, oppgave: str, filnavn: str | None = None) -> dict:
        """Leser ki-svar/<filnavn>.json i caset. Uten filnavn heter fila det samme som
        oppgaven."""
        # Inndataene sjekkes før KI-en kalles (story 2.5). Dette er bare en sikring.
        if case is None:
            raise KIFeil(KIFeilType.ANNET)
        try:
            tekst = (self.mappe / case / "ki-svar" / f"{filnavn or oppgave}.json").read_text(
                encoding="utf-8"
            )
        except OSError as feil:
            raise KIFeil(KIFeilType.ANNET) from feil
        except UnicodeDecodeError as feil:
            raise KIFeil(KIFeilType.UBRUKELIG_SVAR) from feil
        return kontroller(oppgave, tekst)


def _anslatt_pris(tokens_inn: int, tokens_ut: int) -> float:
    """Anslått pris i dollar, med prisene for claude-opus-5-5."""
    return (tokens_inn * KI_PRIS_INN + tokens_ut * KI_PRIS_UT) / 1_000_000


def _desimalkomma(tall: float, desimaler: int) -> str:
    return f"{tall:.{desimaler}f}".replace(".", ",")


def _logg_feil(oppgave: str, type: KIFeilType) -> None:
    """Logger oppgaven og feiltypen, aldri feilmeldingen fra API-et."""
    logger.warning("KI-kall %s feilet: %s", oppgave, type.value)


def _kifeil(oppgave: str, type: KIFeilType) -> KIFeil:
    _logg_feil(oppgave, type)
    return KIFeil(type)


def _cv_og_annonse(cv: str, annonse: str) -> str:
    """Brukermeldingen med CV-en og annonsen i merker, for gap og brev."""
    return f"<cv>\n{cv}\n</cv>\n\n<annonse>\n{annonse}\n</annonse>"


class EkteKI:
    """Claude via API-et (AD-13). Samme signaturer og svarformer som TestKI. klient brukes av
    testene, som sender inn en falsk klient."""

    def __init__(self, api_nokkel: str, modell: str, klient=None):
        self.modell = modell
        # Begge verdiene settes uttrykkelig. Tidsgrensen gjelder hver del av kallet (tilkobling,
        # lesing, skriving) og ikke hele kallet, og før det nye forsøket venter biblioteket litt
        # (opptil ca. 8 s, eller så lenge API-et ber om med retry-after). Hvor lang tid et kall
        # faktisk tar, måles i story 4.3.
        if klient is None:
            klient = Anthropic(api_key=api_nokkel, timeout=KI_TIDSGRENSE, max_retries=KI_NYE_FORSOK)
        self.klient = klient
        self.prompter = {
            oppgave: (PROMPT_MAPPE / f"{oppgave}.md").read_text(encoding="utf-8")
            for oppgave in SKJEMA
        }

    def nokkelord(self, annonse: str) -> dict:
        return self._kall("nokkelord", f"<annonse>\n{annonse}\n</annonse>")

    def gap(self, cv: str, annonse: str) -> dict:
        return self._kall("gap", _cv_og_annonse(cv, annonse))

    def brev(self, cv: str, annonse: str, forslag: int) -> dict:
        """Bare CV-en og annonsen sendes (FR-37). forslag sendes ikke, fordi hvert kall gir et
        nytt brev. Parameteren er med for at signaturen skal være lik den i TestKI."""
        return self._kall("brev", _cv_og_annonse(cv, annonse))

    def _kall(self, oppgave: str, brukermelding: str) -> dict:
        """Sender ett kall til Claude og gir det kontrollerte svaret. Ingen temperature og
        ingen thinking-parameter: Claude Opus 5.5 tenker alltid, og effort styrer hvor mye."""
        try:
            svar = self.klient.messages.create(
                model=self.modell,
                max_tokens=KI_MAKS_TOKENS,
                system=self.prompter[oppgave],
                messages=[{"role": "user", "content": brukermelding}],
                output_config={
                    "format": {"type": "json_schema", "schema": SKJEMA[oppgave]},
                    "effort": KI_INNSATS,
                },
            )
        # APITimeoutError er en underklasse av APIConnectionError, så den må fanges først.
        # Ellers blir et tidsavbrudd feilaktig «Nettverksfeil».
        except APITimeoutError as feil:
            raise _kifeil(oppgave, KIFeilType.ANNET) from feil
        except APIConnectionError as feil:
            raise _kifeil(oppgave, KIFeilType.NETTVERK) from feil
        # Alle andre feil fra biblioteket (API-feil og for eksempel manglende nøkkel).
        except AnthropicError as feil:
            raise _kifeil(oppgave, KIFeilType.ANNET) from feil

        tokens_inn, tokens_ut = svar.usage.input_tokens, svar.usage.output_tokens
        pris = _anslatt_pris(tokens_inn, tokens_ut)
        logger.info(
            "KI-kall %s (%s): %d tokens inn, %d ut, stopp %s, anslått %s dollar (ca. %s kr)",
            oppgave,
            self.modell,
            tokens_inn,
            tokens_ut,
            svar.stop_reason,
            _desimalkomma(pris, 4),
            _desimalkomma(pris * KRONER_PER_DOLLAR, 2),
        )
        # Svaret kan ha tomme thinking-blokker før teksten, så bare tekstblokkene tas med.
        tekst = "".join(blokk.text for blokk in svar.content if blokk.type == "text")
        try:
            return kontroller(oppgave, tekst, svar.stop_reason)
        except KIFeil as feil:
            _logg_feil(oppgave, feil.type)
            raise
