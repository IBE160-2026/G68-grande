"""En falsk Anthropic-API for testene (NFR-11, AD-13). Dette er ikke en testfil, så pytest
samler den ikke inn, og testfilene henter hjelperen herfra i stedet for fra hverandre.

klient_med_svar gir en ekte Anthropic-klient, så kallet i EkteKI går gjennom det ekte
SDK-et (parameternavn, JSON og headere). Bare transporten er falsk: httpx2.MockTransport
svarer uten nettverk."""

import json

import httpx2
from anthropic import Anthropic

from soknad.kjerne.ki_svar import FELT

# Nøkkelen den falske klienten sender (anthropic 2.4.0 sender den i authorization). Det er
# ingen ekte nøkkel.
FALSK_NOKKEL = "sk-test-falsk"


def oppgave_i(innhold: dict) -> str:
    """Oppgaven (nokkelord, gap eller brev) ut fra feltene i JSON-skjemaet i forespørselen.
    innhold er JSON-en i forespørselen (sendt[n]["json"])."""
    felt = set(innhold["output_config"]["format"]["schema"]["properties"])
    return next(oppgave for oppgave, navn in FELT.items() if navn == felt)


def klient_med_svar(svar: dict[str, dict], sendt: list[dict]) -> Anthropic:
    """En ekte Anthropic-klient med MockTransport og max_retries=0. Hver forespørsel legges i
    sendt som {"json": ..., "headers": ...}, og svaret er svar[oppgave] som JSON-tekst med
    stop_reason end_turn. Oppgaven finnes ut fra JSON-skjemaet i forespørselen."""

    def svar_pa(foresporsel: httpx2.Request) -> httpx2.Response:
        innhold = json.loads(foresporsel.content)
        sendt.append({"json": innhold, "headers": foresporsel.headers})
        return httpx2.Response(
            200,
            json={
                "id": "msg_falsk",
                "type": "message",
                "role": "assistant",
                "model": innhold["model"],
                "content": [{"type": "text", "text": json.dumps(svar[oppgave_i(innhold)])}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 812, "output_tokens": 143},
            },
        )

    return Anthropic(
        api_key=FALSK_NOKKEL,
        max_retries=0,
        http_client=httpx2.Client(transport=httpx2.MockTransport(svar_pa)),
    )
