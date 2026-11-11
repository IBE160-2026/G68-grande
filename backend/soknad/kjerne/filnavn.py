"""Filnavnet ved nedlasting (FR-29, AD-11). Filnavn lages bare her.

Fullt mønster er Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>. Arbeidsgiveren kommer i Epic 7, så fram
til da er filnavnet alltid Soknad_<ÅÅÅÅ-MM-DD>."""

from datetime import date


def lag_filnavn(dato: date, endelse: str) -> str:
    """«Soknad_2026-11-11.docx». Datoen sendes inn, så filnavnet ikke avhenger av når det
    regnes ut."""
    return f"Soknad_{dato.isoformat()}.{endelse}"
