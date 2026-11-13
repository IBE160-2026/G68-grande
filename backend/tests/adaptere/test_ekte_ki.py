"""Tester for EkteKI, som sender CV og annonse til Claude (NFR-11, FR-28, NFR-9, AD-13).
Testene bruker en falsk Anthropic-klient og kaller aldri det ekte API-et."""

import inspect
import json
import logging
import re
from pathlib import Path

import anthropic
import httpx2
import pytest
from anthropic.types import Message

import soknad
from soknad.adaptere.ki import PROMPT_MAPPE, EkteKI, TestKI
from soknad.innstillinger import (
    KI_INNSATS,
    KI_MAKS_TOKENS,
    KI_NYE_FORSOK,
    KI_TIDSGRENSE,
    STANDARD_MODELL,
)
from soknad.kjerne.feil import KIFeil, KIFeilType

CV = "Sara Eksempel. Bachelor i IT. Kan Python, Flask og Git."
ANNONSE = "Junior utvikler hos Testvik Utvikling AS. Krav: Python, SQL og Docker."
NOKKEL = "sk-ant-hemmelig-testnokkel"
API_MELDING = "hemmelig-melding-fra-api-et"

NOKKELORD_SVAR = {"nokkelord": ["Python", "SQL", "Docker"], "arbeidsgiver": "Testvik Utvikling AS"}
GAP_SVAR = {"dekker": ["Python"], "mangler": ["SQL", "Docker"]}

FORESPORSEL = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


def _svar(tekst: str | None, stop_reason: str = "end_turn") -> Message:
    """Et svar fra Claude med en tom thinking-blokk før tekstblokken, slik Claude Opus 5.5
    svarer. tekst=None gir et svar uten tekstblokk."""
    innhold = [{"type": "thinking", "thinking": "", "signature": "sig"}]
    if tekst is not None:
        innhold.append({"type": "text", "text": tekst})
    return Message.model_validate(
        {
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": STANDARD_MODELL,
            "content": innhold,
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 812, "output_tokens": 143},
        }
    )


class FalskKlient:
    """Tar imot kallene og gir et ferdig svar, eller kaster en feil."""

    def __init__(self, svar: Message | None = None, feil: Exception | None = None):
        self.svar = svar
        self.feil = feil
        self.kall: list[dict] = []
        self.messages = self

    def create(self, **argumenter):
        self.kall.append(argumenter)
        if self.feil is not None:
            raise self.feil
        return self.svar


def _ki(klient: FalskKlient) -> EkteKI:
    return EkteKI(api_nokkel=NOKKEL, modell=STANDARD_MODELL, klient=klient)


def _kall(ki: EkteKI, oppgave: str) -> dict:
    if oppgave == "nokkelord":
        return ki.nokkelord(ANNONSE)
    return ki.gap(CV, ANNONSE)


def _statusfeil(status: int) -> anthropic.APIStatusError:
    return anthropic.APIStatusError(
        API_MELDING, response=httpx2.Response(status, request=FORESPORSEL), body=None
    )


def test_nfr11_ekte_ki_har_samme_signaturer_som_testki():
    """NFR-11/AD-3: EkteKI har nokkelord(annonse) og gap(cv, annonse), som TestKI."""
    for metode in ("nokkelord", "gap"):
        ekte = inspect.signature(getattr(EkteKI, metode))
        test = inspect.signature(getattr(TestKI, metode))
        assert list(ekte.parameters) == list(test.parameters)


def test_nfr11_nokkelord_gir_svaret_fra_claude():
    """NFR-11/FR-28: et gyldig nøkkelordsvar gis tilbake i formen fra AD-4."""
    klient = FalskKlient(_svar(json.dumps(NOKKELORD_SVAR)))
    assert _ki(klient).nokkelord(ANNONSE) == NOKKELORD_SVAR


def test_nfr11_nokkelord_uten_arbeidsgiver_gir_none():
    """NFR-11/FR-28: uten navn i annonsen er arbeidsgiver None."""
    klient = FalskKlient(_svar('{"nokkelord": ["Python"], "arbeidsgiver": null}'))
    assert _ki(klient).nokkelord(ANNONSE) == {"nokkelord": ["Python"], "arbeidsgiver": None}


def test_nfr11_gap_gir_svaret_fra_claude():
    """NFR-11/FR-28: et gyldig gap-svar gis tilbake i formen fra AD-4."""
    klient = FalskKlient(_svar(json.dumps(GAP_SVAR)))
    assert _ki(klient).gap(CV, ANNONSE) == GAP_SVAR


@pytest.mark.parametrize("oppgave", ["nokkelord", "gap"])
def test_nfr10_nfr11_kallet_har_modell_prompt_skjema_og_innsats(oppgave):
    """NFR-10/NFR-11/AD-4: kallet har modellen, prompten fra prompts/, max_tokens og
    output_config med JSON-skjemaet og effort. Ingen temperature og ingen thinking."""
    svar = NOKKELORD_SVAR if oppgave == "nokkelord" else GAP_SVAR
    klient = FalskKlient(_svar(json.dumps(svar)))
    _kall(_ki(klient), oppgave)
    (kall,) = klient.kall
    assert kall["model"] == STANDARD_MODELL
    assert kall["max_tokens"] == KI_MAKS_TOKENS
    assert kall["system"] == (PROMPT_MAPPE / f"{oppgave}.md").read_text(encoding="utf-8")
    assert kall["output_config"]["effort"] == KI_INNSATS == "medium"
    format = kall["output_config"]["format"]
    assert format["type"] == "json_schema"
    skjema = format["schema"]
    assert skjema["additionalProperties"] is False
    assert set(skjema["required"]) == set(skjema["properties"]) == set(svar)
    for navn in ("temperature", "thinking", "stream"):
        assert navn not in kall


def test_nfr11_nokkelordskjemaet_tillater_null_for_arbeidsgiver():
    """NFR-11/AD-4: arbeidsgiver er tekst eller null, og nøkkelordene er en tekstliste."""
    klient = FalskKlient(_svar(json.dumps(NOKKELORD_SVAR)))
    _ki(klient).nokkelord(ANNONSE)
    egenskaper = klient.kall[0]["output_config"]["format"]["schema"]["properties"]
    assert egenskaper["arbeidsgiver"] == {"anyOf": [{"type": "string"}, {"type": "null"}]}
    assert egenskaper["nokkelord"] == {"type": "array", "items": {"type": "string"}}


def test_nfr11_modellen_fra_innstillingen_brukes():
    """NFR-11: en annen modell (ANTHROPIC_MODEL) sendes med i kallet."""
    klient = FalskKlient(_svar(json.dumps(GAP_SVAR)))
    EkteKI(api_nokkel=NOKKEL, modell="annen-modell", klient=klient).gap(CV, ANNONSE)
    assert klient.kall[0]["model"] == "annen-modell"


def test_nfr11_cv_og_annonse_sendes_i_merker_i_brukermeldingen():
    """NFR-11: CV-en og annonsen står i <cv>- og <annonse>-merker i brukermeldingen."""
    klient = FalskKlient(_svar(json.dumps(GAP_SVAR)))
    _ki(klient).gap(CV, ANNONSE)
    (melding,) = klient.kall[0]["messages"]
    assert melding["role"] == "user"
    assert f"<cv>\n{CV}\n</cv>" in melding["content"]
    assert f"<annonse>\n{ANNONSE}\n</annonse>" in melding["content"]

    klient = FalskKlient(_svar(json.dumps(NOKKELORD_SVAR)))
    _ki(klient).nokkelord(ANNONSE)
    (melding,) = klient.kall[0]["messages"]
    assert melding["content"] == f"<annonse>\n{ANNONSE}\n</annonse>"


def test_nfr11_klienten_har_tidsgrense_90_og_ett_nytt_forsok(monkeypatch):
    """NFR-11/AD-13: uten falsk klient lages Anthropic med timeout 90 og max_retries 1, og
    ingen nettverkskall gjøres."""

    def ingen_nettverk(*args, **kwargs):
        raise AssertionError("EkteKI skal ikke kalle nettet når den lages")

    monkeypatch.setattr(httpx2.Client, "send", ingen_nettverk)
    ki = EkteKI(api_nokkel="x", modell=STANDARD_MODELL)
    assert isinstance(ki.klient, anthropic.Anthropic)
    assert ki.klient.timeout == KI_TIDSGRENSE == 90
    assert ki.klient.max_retries == KI_NYE_FORSOK == 1
    assert ki.klient.api_key == "x"


@pytest.mark.parametrize("oppgave", ["nokkelord", "gap"])
def test_fr28_nettverksfeil_gir_kifeil_nettverk(oppgave):
    """FR-28/AD-13: APIConnectionError gir KIFeil(nettverk)."""
    klient = FalskKlient(feil=anthropic.APIConnectionError(request=FORESPORSEL))
    with pytest.raises(KIFeil) as feil:
        _kall(_ki(klient), oppgave)
    assert feil.value.type == KIFeilType.NETTVERK


@pytest.mark.parametrize("oppgave", ["nokkelord", "gap"])
def test_fr28_tidsavbrudd_gir_kifeil_annet_ikke_nettverk(oppgave):
    """FR-28/AD-13: APITimeoutError (en underklasse av APIConnectionError) gir KIFeil(annet),
    ikke nettverk."""
    assert issubclass(anthropic.APITimeoutError, anthropic.APIConnectionError)
    klient = FalskKlient(feil=anthropic.APITimeoutError(request=FORESPORSEL))
    with pytest.raises(KIFeil) as feil:
        _kall(_ki(klient), oppgave)
    assert feil.value.type == KIFeilType.ANNET


@pytest.mark.parametrize("status", [400, 401, 429, 500, 529])
def test_fr28_annen_api_feil_gir_kifeil_annet(status):
    """FR-28/AD-13: APIStatusError (for eksempel 401, 429 og 500) gir KIFeil(annet)."""
    klient = FalskKlient(feil=_statusfeil(status))
    with pytest.raises(KIFeil) as feil:
        _ki(klient).gap(CV, ANNONSE)
    assert feil.value.type == KIFeilType.ANNET


@pytest.mark.parametrize(
    "stop_reason", ["max_tokens", "refusal", "stop_sequence", "tool_use", "pause_turn"]
)
def test_fr28_annen_stop_reason_enn_end_turn_gir_ubrukelig_svar(caplog, stop_reason):
    """FR-28/AD-4: et avkuttet eller avvist svar gir KIFeil(ubrukelig_svar), også når
    JSON-en ser gyldig ut. Ingen reservemodell ved refusal. Loggen viser stop_reason, så
    max_tokens (avkuttet) kan skilles fra refusal."""
    caplog.set_level(logging.INFO, logger="soknad.adaptere.ki")
    klient = FalskKlient(_svar(json.dumps(GAP_SVAR), stop_reason=stop_reason))
    with pytest.raises(KIFeil) as feil:
        _ki(klient).gap(CV, ANNONSE)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR
    assert len(klient.kall) == 1
    assert f"stopp {stop_reason}," in caplog.text


@pytest.mark.parametrize(
    ("oppgave", "tekst"),
    [
        ("nokkelord", "ikke json"),
        ("nokkelord", '{"nokkelord": [], "arbeidsgiver": null}'),
        ("nokkelord", '{"nokkelord": ["Python"]}'),
        ("gap", '{"dekker": [], "mangler": []}'),
        ("gap", '{"dekker": ["Python"], "mangler": "SQL"}'),
        ("gap", '{"dekker": ["Python"], "mangler": [], "ekstra": []}'),
        ("gap", None),
    ],
)
def test_fr28_ugyldig_svar_gir_ubrukelig_svar(oppgave, tekst):
    """FR-28/AD-4: ugyldig JSON, feil form, tom liste og svar uten tekstblokk gir
    KIFeil(ubrukelig_svar)."""
    klient = FalskKlient(_svar(tekst))
    with pytest.raises(KIFeil) as feil:
        _kall(_ki(klient), oppgave)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def test_fr28_tekstblokker_settes_sammen():
    """FR-28: svaret kan komme i flere tekstblokker, og de settes sammen før kontrollen."""
    svar = _svar('{"dekker": ["Python"], ')
    svar.content.append(
        svar.content[1].model_copy(update={"text": '"mangler": ["SQL", "Docker"]}'})
    )
    assert _ki(FalskKlient(svar)).gap(CV, ANNONSE) == GAP_SVAR


def test_nfr11_vellykket_kall_logger_oppgave_tokens_og_pris(caplog):
    """NFR-11/AD-12: et vellykket kall logger én INFO-linje med oppgaven, tokens inn og ut
    og anslått pris. CV, annonse, nøkkel og selve svaret står ikke i loggen."""
    caplog.set_level(logging.INFO, logger="soknad.adaptere.ki")
    _ki(FalskKlient(_svar(json.dumps(GAP_SVAR)))).gap(CV, ANNONSE)
    linjer = [post for post in caplog.records if post.name == "soknad.adaptere.ki"]
    assert len(linjer) == 1
    assert linjer[0].levelno == logging.INFO
    assert linjer[0].getMessage() == (
        "KI-kall gap (claude-opus-5-5): 812 tokens inn, 143 ut, stopp end_turn, anslått 0,0061"
        " dollar (ca. 0,07 kr)"
    )
    for hemmelig in (CV, ANNONSE, NOKKEL, "Sara", "Testvik", "Docker"):
        assert hemmelig not in caplog.text


@pytest.mark.parametrize(
    ("feil", "type"),
    [
        (anthropic.APIConnectionError(request=FORESPORSEL), "nettverk"),
        (anthropic.APITimeoutError(request=FORESPORSEL), "annet"),
        (_statusfeil(401), "annet"),
    ],
)
def test_fr28_kifeil_logges_med_oppgave_og_type_uten_api_melding(caplog, feil, type):
    """FR-28/AD-12: en KIFeil logges med oppgaven og feiltypen, uten feilmeldingen fra API-et
    og uten CV, annonse eller nøkkel."""
    caplog.set_level(logging.INFO, logger="soknad.adaptere.ki")
    with pytest.raises(KIFeil):
        _ki(FalskKlient(feil=feil)).nokkelord(ANNONSE)
    assert f"KI-kall nokkelord feilet: {type}" in caplog.text
    for hemmelig in (API_MELDING, "Connection error", ANNONSE, NOKKEL):
        assert hemmelig not in caplog.text


def test_fr28_annen_feil_fra_biblioteket_gir_kifeil_annet(caplog):
    """FR-28/AD-13: en annen feil fra anthropic (for eksempel manglende nøkkel) gir
    KIFeil(annet) og logges med oppgaven og feiltypen, uten feilmeldingen."""
    caplog.set_level(logging.INFO, logger="soknad.adaptere.ki")
    with pytest.raises(KIFeil) as feil:
        _ki(FalskKlient(feil=anthropic.AnthropicError(API_MELDING))).gap(CV, ANNONSE)
    assert feil.value.type == KIFeilType.ANNET
    assert "KI-kall gap feilet: annet" in caplog.text
    assert API_MELDING not in caplog.text


def test_fr28_ubrukelig_svar_logger_tokens_og_feiltype(caplog):
    """FR-28/AD-12: et ubrukelig svar har også kostet tokens, så både prisen og feiltypen
    logges, men ikke selve svaret."""
    caplog.set_level(logging.INFO, logger="soknad.adaptere.ki")
    with pytest.raises(KIFeil):
        _ki(FalskKlient(_svar("hemmelig ugyldig svar"))).gap(CV, ANNONSE)
    assert "KI-kall gap (claude-opus-5-5): 812 tokens inn, 143 ut, stopp end_turn" in caplog.text
    assert "KI-kall gap feilet: ubrukelig_svar" in caplog.text
    assert "hemmelig ugyldig svar" not in caplog.text


def test_nfr10_promptene_ligger_i_prompts_og_er_utf8():
    """NFR-10: prompt-filene for nokkelord og gap ligger i backend/prompts/ og kan leses som
    utf-8."""
    assert PROMPT_MAPPE == Path(soknad.__file__).resolve().parent.parent / "prompts"
    for oppgave in ("nokkelord", "gap"):
        assert (PROMPT_MAPPE / f"{oppgave}.md").read_text(encoding="utf-8").strip()


def test_nfr11_anthropic_importeres_bare_i_adaptere_ki():
    """NFR-11/AD-3: anthropic importeres bare i adaptere/ki.py, aldri i kjerne/ eller web/."""
    pakke = Path(soknad.__file__).resolve().parent
    importerer = re.compile(r"^\s*(?:import|from)\s+anthropic\b", re.M)
    treff = [
        fil.relative_to(pakke).as_posix()
        for fil in sorted(pakke.rglob("*.py"))
        if importerer.search(fil.read_text(encoding="utf-8"))
    ]
    assert treff == ["adaptere/ki.py"]


def test_nfr11_create_app_gir_loggeren_soknad_en_handler(app):
    """NFR-11/AD-12: loggeren soknad skriver INFO til terminalen med én handler, også når
    create_app kalles flere ganger."""
    from soknad import TERMINAL_LOGG, create_app

    create_app({"TESTING": True})
    logger = logging.getLogger("soknad")
    assert logger.level == logging.INFO
    assert logger.handlers.count(TERMINAL_LOGG) == 1
    assert isinstance(TERMINAL_LOGG, logging.StreamHandler)


def test_nfr11_nettsiden_bruker_fortsatt_testki(app):
    """NFR-11: fram til story 4.3 bruker nettsiden TestKI, også uten API-nøkkel."""
    assert isinstance(app.extensions["test_ki"], TestKI)
    assert app.config["ANTHROPIC_API_KEY"] == ""


def test_fr15_svar_med_31_nokkelord_gir_ubrukelig_svar():
    """FR-15/FR-28: et svar fra Claude med 31 nøkkelord gir KIFeil(ubrukelig_svar)."""
    svar = {"nokkelord": [f"ord{n}" for n in range(31)], "arbeidsgiver": None}
    with pytest.raises(KIFeil) as feil:
        _ki(FalskKlient(_svar(json.dumps(svar)))).nokkelord(ANNONSE)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def test_fr15_prompten_ber_om_8_til_20_nokkelord_pa_1_til_3_ord():
    """FR-15: nøkkelordprompten ber om 8–20 nøkkelord på 1–3 ord hver, uten duplikater."""
    prompt = (PROMPT_MAPPE / "nokkelord.md").read_text(encoding="utf-8")
    assert "8–20 nøkkelord" in prompt
    assert "1–3 ord" in prompt
    assert "duplikater" in prompt
