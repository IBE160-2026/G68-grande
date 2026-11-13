"""Kontroll av KI-svar (AD-4, FR-28). Både TestKI og EkteKI sender svaret hit, så et
ubrukelig svar stoppes på samme sted uansett utgave."""

import json
import unicodedata

from soknad.innstillinger import MAKS_NOKKELORD
from soknad.kjerne.feil import KIFeil, KIFeilType

# Feltene hver oppgave skal ha, og nøyaktig disse (AD-4).
FELT = {
    "nokkelord": {"nokkelord", "arbeidsgiver"},
    "gap": {"dekker", "mangler"},
    "brev": {"avsnitt"},
}


def _er_tekstliste(verdi) -> bool:
    return isinstance(verdi, list) and all(isinstance(element, str) for element in verdi)


def _riktig_form(oppgave: str, svar) -> bool:
    if not isinstance(svar, dict) or set(svar) != FELT[oppgave]:
        return False
    if oppgave == "nokkelord":
        arbeidsgiver = svar["arbeidsgiver"]
        return _er_tekstliste(svar["nokkelord"]) and (
            arbeidsgiver is None or isinstance(arbeidsgiver, str)
        )
    if oppgave == "brev":
        return _er_tekstliste(svar["avsnitt"])
    return _er_tekstliste(svar["dekker"]) and _er_tekstliste(svar["mangler"])


# Tegnene Word (XML) ikke tåler, fjernes fra brevet: kontrolltegn (kategori Cc), enslige
# surrogater (Cs, kan komme fra for eksempel \ud800 i JSON) og U+FFFE og U+FFFF. Tab,
# linjeskift og vognretur er også kontrolltegn, men de blir mellomrom i stedet.
_MELLOMROM_KONTROLLTEGN = "\t\n\r"
_IKKE_TEGN = "\ufffe\uffff"


def _word_taler(tegn: str) -> bool:
    if tegn in _MELLOMROM_KONTROLLTEGN:
        return True
    return unicodedata.category(tegn) not in ("Cc", "Cs") and tegn not in _IKKE_TEGN


def _rens_avsnitt(avsnitt: str) -> str:
    """Fjerner tegnene Word ikke tåler, og gjør alt mellomrom (også linjeskift og tab) om til
    ett mellomrom. Nettleseren viser flere mellomrom som ett, så da blir Word-fila lik siden."""
    return " ".join("".join(tegn for tegn in avsnitt if _word_taler(tegn)).split())


def _uten_tomme(liste: list[str]) -> list[str]:
    """Listen uten punkter som er tomme eller bare har mellomrom."""
    return [element for element in liste if element.strip()]


def _rens(oppgave: str, svar: dict) -> dict:
    """Svaret uten tomme punkter. Tom arbeidsgiver blir None, og brevteksten renses."""
    if oppgave == "nokkelord":
        arbeidsgiver = svar["arbeidsgiver"]
        if arbeidsgiver is not None and not arbeidsgiver.strip():
            arbeidsgiver = None
        return {"nokkelord": _uten_tomme(svar["nokkelord"]), "arbeidsgiver": arbeidsgiver}
    if oppgave == "brev":
        return {"avsnitt": _uten_tomme([_rens_avsnitt(avsnitt) for avsnitt in svar["avsnitt"]])}
    return {"dekker": _uten_tomme(svar["dekker"]), "mangler": _uten_tomme(svar["mangler"])}


def _bare_tomme(liste: list[str]) -> bool:
    """Sann når listen er tom eller bare har tomme tekster (også bare mellomrom)."""
    return not any(element.strip() for element in liste)


def _tomt(oppgave: str, svar: dict) -> bool:
    if oppgave == "nokkelord":
        return _bare_tomme(svar["nokkelord"])
    if oppgave == "brev":
        return _bare_tomme(svar["avsnitt"])
    return _bare_tomme(svar["dekker"] + svar["mangler"])


def kontroller(oppgave: str, tekst: str, stop_reason: str | None = "end_turn") -> dict:
    """Gir svaret i formen fra AD-4. Ugyldig JSON, feil form, tom nøkkelordliste, både
    dekker og mangler tomme eller et brev uten tekst gir KIFeil(ubrukelig_svar). Oppgavene er
    nokkelord, gap og brev.

    Før tom-sjekken renses svaret (FR-28, FR-30), både for TestKI og EkteKI:
    - Punkter som er tomme eller bare har mellomrom, fjernes i nokkelord, dekker, mangler og
      avsnitt, så siden ikke viser tomme punkter. En liste med bare slike punkter er tom.
    - Tom arbeidsgiver (eller bare mellomrom) blir None.
    - I hvert avsnitt i brevet fjernes kontrolltegn og andre tegn Word ikke tåler, og alt
      mellomrom (også linjeskift og tab) blir ett mellomrom, så Word-fila blir lik siden. Et
      brev som blir tomt av dette, gir KIFeil(ubrukelig_svar).

    En nøkkelordliste med flere enn MAKS_NOKKELORD (30) nøkkelord (tomme punkter ikke
    medregnet) gir også KIFeil(ubrukelig_svar) (FR-15).

    stop_reason kommer fra Claude. Alt annet enn end_turn (for eksempel max_tokens eller
    refusal) betyr at svaret er avkuttet eller avvist, og gir KIFeil(ubrukelig_svar) før
    JSON-en leses. TestKI sender den ikke, og da gjelder standarden end_turn."""
    if oppgave not in FELT:
        raise ValueError(f"Ukjent KI-oppgave: {oppgave}")
    if stop_reason != "end_turn":
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    try:
        svar = json.loads(tekst)
    except (json.JSONDecodeError, RecursionError) as feil:
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR) from feil
    if not _riktig_form(oppgave, svar):
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    svar = _rens(oppgave, svar)
    if _tomt(oppgave, svar):
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    if oppgave == "nokkelord" and len(svar["nokkelord"]) > MAKS_NOKKELORD:
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    return svar
