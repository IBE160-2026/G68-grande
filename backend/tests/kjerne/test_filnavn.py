"""Enhetstester for filnavnet ved nedlasting (FR-29, AD-11). Story 3.2."""

from datetime import date

import pytest

from soknad.kjerne.filnavn import lag_filnavn


@pytest.mark.parametrize(
    ("dato", "endelse", "forventet"),
    [
        (date(2026, 11, 11), "docx", "Soknad_2026-11-11.docx"),
        (date(2027, 1, 5), "docx", "Soknad_2027-01-05.docx"),
        (date(2026, 12, 31), "pdf", "Soknad_2026-12-31.pdf"),
    ],
)
def test_fr29_filnavnet_har_datoen(dato, endelse, forventet):
    """FR-29/AD-11: filnavnet er Soknad_<ÅÅÅÅ-MM-DD> med endelsen, og datoen har to sifre for
    måned og dag. Arbeidsgiveren i filnavnet kommer i Epic 7."""
    assert lag_filnavn(dato, endelse) == forventet


def test_fr29_filnavnet_er_bare_ascii_uten_mellomrom():
    """FR-29/AD-11: filnavnet har bare [A-Za-z0-9-_.], så det virker på alle maskiner."""
    navn = lag_filnavn(date(2026, 11, 11), "docx")
    assert navn.isascii()
    assert all(tegn.isalnum() or tegn in "-_." for tegn in navn)
