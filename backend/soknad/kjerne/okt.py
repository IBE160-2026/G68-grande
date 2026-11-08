"""Formen på øktdataene. Øktlageret i adaptere/oktlager.py lagrer bare disse."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Innlogging:
    """Varer til brukeren logger ut."""

    bruker_id: int
    testmodus: bool
