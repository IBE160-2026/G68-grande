"""Lukkede feiltyper. Tekstene til feilene ligger i web/tekster.py."""

from dataclasses import dataclass
from enum import StrEnum


class FeilType(StrEnum):
    """Alle typer inndatafeil i Epic 1."""

    TOM = "tom"
    EPOST_FINNES = "epost_finnes"
    EPOST_UGYLDIG = "epost_ugyldig"
    PASSORD_KORT = "passord_kort"
    PASSORD_ULIKE = "passord_ulike"
    FEIL_INNLOGGING = "feil_innlogging"


@dataclass(frozen=True)
class InndataFeil:
    """En feil i et skjema. felt=None betyr hele skjemaet (for eksempel feil innlogging)."""

    felt: str | None
    type: FeilType
