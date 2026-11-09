"""Kontroll av KI-svar (AD-4, FR-28). Både TestKI og senere EkteKI sender svaret hit, så et
ubrukelig svar stoppes på samme sted uansett utgave."""

import json

from soknad.kjerne.feil import KIFeil, KIFeilType

# Feltene hver oppgave skal ha, og nøyaktig disse (AD-4).
FELT = {
    "nokkelord": {"nokkelord", "arbeidsgiver"},
    "gap": {"dekker", "mangler"},
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
    return _er_tekstliste(svar["dekker"]) and _er_tekstliste(svar["mangler"])


def _bare_tomme(liste: list[str]) -> bool:
    """Sann når listen er tom eller bare har tomme tekster (også bare mellomrom)."""
    return not any(element.strip() for element in liste)


def _tomt(oppgave: str, svar: dict) -> bool:
    if oppgave == "nokkelord":
        return _bare_tomme(svar["nokkelord"])
    return _bare_tomme(svar["dekker"] + svar["mangler"])


def kontroller(oppgave: str, tekst: str) -> dict:
    """Gir svaret i formen fra AD-4. Ugyldig JSON, feil form, tom nøkkelordliste eller både
    dekker og mangler tomme gir KIFeil(ubrukelig_svar). En liste med bare tomme tekster
    regnes som tom. Oppgavene er nokkelord og gap."""
    if oppgave not in FELT:
        raise ValueError(f"Ukjent KI-oppgave: {oppgave}")
    try:
        svar = json.loads(tekst)
    except (json.JSONDecodeError, RecursionError) as feil:
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR) from feil
    if not _riktig_form(oppgave, svar) or _tomt(oppgave, svar):
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    return svar
