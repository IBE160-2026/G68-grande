"""KI-grensesnittet (AD-3). Web-laget bruker bare grensesnittet og vet ikke hvilken utgave
det får. TestKI gir de ferdige svarene fra testdata/ (ekte KI-svar, laget med
scripts/lag_testsvar.py). EkteKI sender teksten til Claude.
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
# og ingen andre felt er lov. arbeidsgiver er null når annonsen ikke har noe navn, og navn i
# brevet er null når CV-en ikke har noe navn. I korrektur er ny null når setningen er fjernet.
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
        "properties": {
            "avsnitt": _TEKSTLISTE,
            "navn": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        },
        "required": ["avsnitt", "navn"],
        "additionalProperties": False,
    },
    "korrektur": {
        "type": "object",
        "properties": {
            "setninger": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "ny": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "gammel": _TEKSTLISTE,
                        "nytt_avsnitt": {"type": "boolean"},
                    },
                    "required": ["ny", "gammel", "nytt_avsnitt"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["setninger"],
        "additionalProperties": False,
    },
}


class KI(Protocol):
    """Faste signaturer."""

    def nokkelord(self, annonse: str) -> dict: ...

    def gap(self, cv: str, annonse: str) -> dict: ...

    def brev(self, cv: str, annonse: str, forslag: int) -> dict: ...

    def korrektur(self, cv: str, annonse: str, eget_brev: str, forslag: int) -> dict: ...


class TestdataFeil(Exception):
    """Testdataene i testdata/ mangler eller henger ikke sammen. Gis ved oppstart, så feilen
    merkes med en gang og ikke som en KI-feil midt i flyten (story 4.5)."""

    # Navnet begynner på Test, men dette er ikke en testklasse for pytest.
    __test__ = False


def _les_fil(case: Path, navn: str) -> str:
    fil = case / navn
    if not fil.is_file():
        raise TestdataFeil(f"Testcaset {case.name} mangler fila {navn} (i {case}).")
    return fil.read_text(encoding="utf-8")


def _sjekk_unike(caser: list[Testcase]) -> None:
    """To caser med samme vaskede CV, annonse eller eget brev gir TestdataFeil. CV-en avgjør
    caset, og nokkelord finner caset ut fra annonsen, så begge må være unike. Da gir nokkelord
    og gap alltid svar fra samme case. Caser uten eget brev telles ikke med for brevet."""
    for felt, navn in (("cv", "CV"), ("annonse", "annonse"), ("eget_brev", "eget brev")):
        sett: dict[str, str] = {}
        for case in caser:
            tekst = getattr(case, felt)
            if tekst is None:
                continue
            if tekst in sett:
                raise TestdataFeil(
                    f"Testcasene {sett[tekst]} og {case.navn} har samme {navn}. "
                    "Hvert testcase må ha sin egen CV og annonse, "
                    "og sitt eget brev hvis det har et."
                )
            sett[tekst] = case.navn


def _les_valgfri_fil(case: Path, navn: str) -> str | None:
    """Teksten i fila, eller None når caset ikke har den."""
    fil = case / navn
    return fil.read_text(encoding="utf-8") if fil.is_file() else None


def les_testcaser(mappe: Path = TESTDATA_MAPPE) -> list[Testcase]:
    """Leser cv.txt og annonse.txt i hver case-mappe, sortert på navn, og eget-brev.txt når
    caset har den (brevet til Korrektur, bare i case 1, story 5.1). Mangler mappen, en
    case-mappe, cv.txt eller annonse.txt, eller er to CV-er, annonser eller egne brev like,
    gis TestdataFeil."""
    mapper = sorted(case for case in mappe.glob("case-*") if case.is_dir())
    if not mapper:
        raise TestdataFeil(f"Fant ingen testcaser (mapper som heter case-…) i {mappe}.")
    caser = [
        lag_testcase(
            case.name,
            _les_fil(case, "cv.txt"),
            _les_fil(case, "annonse.txt"),
            _les_valgfri_fil(case, "eget-brev.txt"),
        )
        for case in mapper
    ]
    _sjekk_unike(caser)
    return caser


class TestKI:
    """Testmodus: finner testcaset og leser svaret fra testdata/<case>/ki-svar/."""

    # Navnet begynner på Test, men dette er ikke en testklasse for pytest.
    __test__ = False

    def __init__(self, mappe: Path = TESTDATA_MAPPE):
        self.mappe = mappe
        self.caser = les_testcaser(mappe)

    def nokkelord(self, annonse: str) -> dict:
        """Signaturen har bare annonsen, så caset finnes ut fra den. Annonsene er unike
        (les_testcaser), så det er samme case som gap og brev finner ut fra CV-en."""
        return self._svar(case_for_annonse(annonse, self.caser), "nokkelord")

    def gap(self, cv: str, annonse: str) -> dict:
        """CV-en avgjør caset, og annonsen må høre til samme case."""
        case, _ = finn_case(cv, annonse, self.caser)
        return self._svar(case, "gap")

    def brev(self, cv: str, annonse: str, forslag: int) -> dict:
        """Caset finnes som i gap. Oddetall for forslag gir brev-1.json, partall brev-2.json,
        så «Nytt forslag» (story 7.1) gir et annet brev enn det forrige."""
        case, _ = finn_case(cv, annonse, self.caser)
        return self._svar(case, "brev", f"brev-{1 if forslag % 2 else 2}")

    def korrektur(self, cv: str, annonse: str, eget_brev: str, forslag: int) -> dict:
        """Caset finnes ut fra CV-en, og annonsen og det egne brevet må høre til samme case.
        Oddetall for forslag gir korrektur-1.json, partall korrektur-2.json («Nytt forslag»,
        story 7.1). Svaret kontrolleres mot casets egen eget-brev.txt, ikke mot det brukeren limte
        inn. Caset er funnet med vasken, så den innlimte teksten kan ha andre store bokstaver
        eller mellomrom (eller komme fra en PDF, Epic 6), mens gammel i svarfila er ordrett fra
        fila (retro 5). I testmodus viser «Du skrev» derfor teksten i fila. Kan fila ikke
        leses, gis KIFeil(annet), som for svarfilene."""
        case, _ = finn_case(cv, annonse, self.caser, eget_brev=eget_brev)
        # Inndataene sjekkes før KI-en kalles (story 2.5). Dette er bare en sikring.
        if case is None:
            raise KIFeil(KIFeilType.ANNET)
        try:
            original = (self.mappe / case / "eget-brev.txt").read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as feil:
            raise KIFeil(KIFeilType.ANNET) from feil
        return self._svar(
            case, "korrektur", f"korrektur-{1 if forslag % 2 else 2}", eget_brev=original
        )

    def _svar(
        self,
        case: str | None,
        oppgave: str,
        filnavn: str | None = None,
        eget_brev: str | None = None,
    ) -> dict:
        """Leser ki-svar/<filnavn>.json i caset. Uten filnavn heter fila det samme som
        oppgaven. eget_brev gis videre til kontroller() (bare korrektur)."""
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
        return kontroller(oppgave, tekst, eget_brev=eget_brev)


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
    """Brukermeldingen med CV-en og annonsen i merker, for gap, brev og korrektur."""
    return f"<cv>\n{cv}\n</cv>\n\n<annonse>\n{annonse}\n</annonse>"


class EkteKI:
    """Claude via API-et (AD-13). Samme signaturer og svarformer som TestKI. klient brukes av
    testene, som sender inn en falsk klient."""

    def __init__(self, api_nokkel: str, modell: str, klient=None):
        self.modell = modell
        # Begge verdiene settes uttrykkelig. Tidsgrensen gjelder hver del av kallet (tilkobling,
        # lesing, skriving) og ikke hele kallet, og før det nye forsøket venter biblioteket litt
        # (opptil ca. 8 s, eller så lenge API-et ber om med retry-after), så et kall kan ta lenger
        # enn 2 x 90 s. Hva som er målt, står ved KI_TIDSGRENSE i innstillinger.py.
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

    def korrektur(self, cv: str, annonse: str, eget_brev: str, forslag: int) -> dict:
        """Bare CV-en, annonsen og det egne brevet sendes (FR-37). forslag sendes ikke, som i
        brev. Svaret kontrolleres mot det egne brevet."""
        brukermelding = f"{_cv_og_annonse(cv, annonse)}\n\n<eget_brev>\n{eget_brev}\n</eget_brev>"
        return self._kall("korrektur", brukermelding, eget_brev=eget_brev)

    def _kall(self, oppgave: str, brukermelding: str, eget_brev: str | None = None) -> dict:
        """Sender ett kall til Claude og gir det kontrollerte svaret. Ingen temperature og
        ingen thinking-parameter: Claude Opus 5.5 tenker alltid, og effort styrer hvor mye.
        eget_brev gis videre til kontroller() (bare korrektur)."""
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
            return kontroller(oppgave, tekst, svar.stop_reason, eget_brev=eget_brev)
        except KIFeil as feil:
            _logg_feil(oppgave, feil.type)
            raise
