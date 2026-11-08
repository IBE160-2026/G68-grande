"""Telleregelen for nøkkelordtreff. Dette er den eneste koden som avgjør treff og prosent
(AD-6), så samme nøkkelordliste og CV alltid gir samme svar."""

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

# Alle mellomrom (også linjeskift og tabulator), som gjøres om til ett vanlig mellomrom.
MELLOMROM = re.compile(r"\s+")

# Nøkkelord kortere enn dette må stå som eget ord i CV-en.
MIN_LENGDE_DEL_AV_ORD = 4


@dataclass(frozen=True)
class Nokkelordtreff:
    """Resultatet av tellingen. Nøkkelordene står slik de er skrevet, i listens rekkefølge."""

    treff: tuple[str, ...]
    ikke_treff: tuple[str, ...]
    antall_treff: int
    antall: int
    prosent: int


def _vask(tekst: str) -> str:
    """Gjør alle mellomrom til ett vanlig mellomrom og fjerner store bokstaver."""
    return MELLOMROM.sub(" ", tekst).strip().casefold()


def _finnes_i(vasket: str, cv: str) -> bool:
    """Ord på 4 tegn eller mer (etter strip() og casefold()) gir treff også inne i et lengre
    ord. Kortere ord må stå som eget ord, uten bokstav, tall eller _ rett foran eller bak."""
    if len(vasket) >= MIN_LENGDE_DEL_AV_ORD:
        return vasket in cv
    return re.search(rf"(?<!\w){re.escape(vasket)}(?!\w)", cv) is not None


def tell_treff(nokkelord: list[str], cv: str) -> Nokkelordtreff:
    """Teller hvor mange av nøkkelordene som står i CV-en. Hvert nøkkelord telles én gang.
    Tomme nøkkelord hoppes over, og like nøkkelord telles som ett (den første skrivemåten
    beholdes). En tom liste gir ValueError."""
    unike: dict[str, str] = {}
    for ord_ in nokkelord:
        vasket = _vask(ord_)
        if vasket and vasket not in unike:
            unike[vasket] = ord_
    if not unike:
        raise ValueError("Nøkkelordlisten er tom.")

    cv_vasket = _vask(cv)
    treff, ikke_treff = [], []
    for vasket, ord_ in unike.items():
        (treff if _finnes_i(vasket, cv_vasket) else ikke_treff).append(ord_)

    antall = len(unike)
    prosent = (Decimal(len(treff) * 100) / Decimal(antall)).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return Nokkelordtreff(
        treff=tuple(treff),
        ikke_treff=tuple(ikke_treff),
        antall_treff=len(treff),
        antall=antall,
        prosent=int(prosent),
    )
