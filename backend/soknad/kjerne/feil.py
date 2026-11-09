"""Lukkede feiltyper. Tekstene til feilene ligger i web/tekster.py."""

from dataclasses import dataclass
from enum import StrEnum


class FeilType(StrEnum):
    """Alle typer inndatafeil så langt."""

    TOM = "tom"
    EPOST_FINNES = "epost_finnes"
    EPOST_UGYLDIG = "epost_ugyldig"
    PASSORD_KORT = "passord_kort"
    PASSORD_ULIKE = "passord_ulike"
    FEIL_INNLOGGING = "feil_innlogging"
    IKKE_TESTDATA = "ikke_testdata"


@dataclass(frozen=True)
class InndataFeil:
    """En feil i et skjema. felt=None betyr hele skjemaet (for eksempel feil innlogging)."""

    felt: str | None
    type: FeilType


class KIFeilType(StrEnum):
    """Alle typer feil fra KI-en (AD-9)."""

    NETTVERK = "nettverk"
    ANNET = "annet"
    UBRUKELIG_SVAR = "ubrukelig_svar"


class KIFeil(Exception):
    """KI-en svarte ikke, eller svaret kan ikke brukes (FR-28)."""

    def __init__(self, type: KIFeilType):
        # type sendes videre (ikke type.value), så en kopi av feilen får samme type.
        super().__init__(type)
        self.type = type
