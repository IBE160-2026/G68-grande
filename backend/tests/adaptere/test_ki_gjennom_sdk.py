"""Tester for EkteKI gjennom det ekte Anthropic-SDK-et (NFR-11, NFR-10, FR-28, AD-4, AD-13).
Klienten er en ekte Anthropic med httpx2.MockTransport (tests/falsk_api.py), så et
parameternavn eller en verdi som SDK-et ikke godtar, gir en feil her og ikke først ved et
ekte kall. Ingen test går mot nettet, og ingen bruker en ekte API-nøkkel."""

import pytest

from soknad.adaptere.ki import PROMPT_MAPPE, SKJEMA, EkteKI
from soknad.innstillinger import KI_INNSATS, KI_MAKS_TOKENS, KI_NYE_FORSOK, STANDARD_MODELL
from soknad.kjerne.feil import KIFeil, KIFeilType
from tests.falsk_api import FALSK_NOKKEL, klient_med_svar

CV = "Sara Eksempel. Bachelor i IT. Kan Python, Flask og Git."
ANNONSE = "Junior utvikler hos Testvik Utvikling AS. Krav: Python, SQL og Docker."

# Svarene har et tomt punkt og et avsnitt med linjeskift, så testene ser at kontroller()
# brukes på svaret fra SDK-et.
SVAR = {
    "nokkelord": {"nokkelord": ["Python", " ", "SQL"], "arbeidsgiver": "Testvik Utvikling AS"},
    "gap": {"dekker": ["Python", ""], "mangler": ["SQL", "Docker"]},
    "brev": {"avsnitt": ["Jeg søker\nstillingen.", "Med vennlig hilsen", "Sara Eksempel"]},
}
KONTROLLERT = {
    "nokkelord": {"nokkelord": ["Python", "SQL"], "arbeidsgiver": "Testvik Utvikling AS"},
    "gap": {"dekker": ["Python"], "mangler": ["SQL", "Docker"]},
    "brev": {"avsnitt": ["Jeg søker stillingen.", "Med vennlig hilsen", "Sara Eksempel"]},
}
BRUKERMELDING = {
    "nokkelord": f"<annonse>\n{ANNONSE}\n</annonse>",
    "gap": f"<cv>\n{CV}\n</cv>\n\n<annonse>\n{ANNONSE}\n</annonse>",
    "brev": f"<cv>\n{CV}\n</cv>\n\n<annonse>\n{ANNONSE}\n</annonse>",
}


def _kall(ki: EkteKI, oppgave: str) -> dict:
    if oppgave == "nokkelord":
        return ki.nokkelord(ANNONSE)
    if oppgave == "brev":
        return ki.brev(CV, ANNONSE, 1)
    return ki.gap(CV, ANNONSE)


@pytest.mark.parametrize("oppgave", list(SVAR))
def test_nfr11_kallet_gar_gjennom_sdk_et_med_riktig_json(oppgave):
    """NFR-11/NFR-10/AD-4/AD-13: kallet går gjennom det ekte SDK-et. JSON-en som sendes, har
    model, max_tokens, system, messages og output_config med format og effort, og ingen andre
    felt. Nøkkelen sendes (anthropic 2.4.0 sender den i authorization, eldre utgaver i
    x-api-key), og svaret er gått gjennom kontroller()."""
    sendt = []
    ki = EkteKI(
        api_nokkel="brukes-ikke", modell=STANDARD_MODELL, klient=klient_med_svar(SVAR, sendt)
    )
    assert _kall(ki, oppgave) == KONTROLLERT[oppgave]

    (foresporsel,) = sendt
    innhold = foresporsel["json"]
    assert innhold == {
        "model": STANDARD_MODELL,
        "max_tokens": KI_MAKS_TOKENS,
        "system": (PROMPT_MAPPE / f"{oppgave}.md").read_text(encoding="utf-8"),
        "messages": [{"role": "user", "content": BRUKERMELDING[oppgave]}],
        "output_config": {
            "format": {"type": "json_schema", "schema": SKJEMA[oppgave]},
            "effort": KI_INNSATS,
        },
    }
    nokkel = foresporsel["headers"].get("x-api-key") or foresporsel["headers"].get("authorization")
    assert nokkel in (FALSK_NOKKEL, f"Bearer {FALSK_NOKKEL}")


def test_nfr11_ekte_ki_uten_falsk_klient_stoppes_av_sperren(nettsperre):
    """NFR-11/FR-28: EkteKI uten falsk klient når ikke nettet. Sperren i conftest.py kaster
    ConnectError, som EkteKI gjør om til KIFeil(nettverk), og forsøket er notert (ett per
    forsøk, også det nye forsøket). Testen tømmer lista, så sperren ikke feiler den etterpå."""
    ki = EkteKI(api_nokkel="sk-ikke-ekte", modell=STANDARD_MODELL)
    with pytest.raises(KIFeil) as feil:
        ki.gap(CV, ANNONSE)
    forsok = list(nettsperre)
    nettsperre.clear()
    assert feil.value.type == KIFeilType.NETTVERK
    assert forsok == ["POST https://api.anthropic.com/v1/messages"] * (KI_NYE_FORSOK + 1)
