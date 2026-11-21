"""Enhetstester for filnavnet ved nedlasting (FR-29, AD-11). Story 3.2, arbeidsgiveren i
filnavnet i story 7.5."""

import re
from datetime import date

import pytest

from soknad.kjerne.filnavn import MAKS_ARBEIDSGIVER, lag_filnavn

DATO = date(2026, 11, 11)


@pytest.mark.parametrize(
    ("dato", "endelse", "forventet"),
    [
        (date(2026, 11, 11), "docx", "Soknad_2026-11-11.docx"),
        (date(2027, 1, 5), "docx", "Soknad_2027-01-05.docx"),
        (date(2026, 12, 31), "pdf", "Soknad_2026-12-31.pdf"),
    ],
)
def test_fr29_filnavnet_har_datoen(dato, endelse, forventet):
    """FR-29/AD-11: uten arbeidsgiver er filnavnet Soknad_<ÅÅÅÅ-MM-DD> med endelsen, og datoen
    har to sifre for måned og dag."""
    assert lag_filnavn(dato, endelse) == forventet


def test_fr29_filnavnet_er_bare_ascii_uten_mellomrom():
    """FR-29/AD-11: filnavnet har bare [A-Za-z0-9-_.], så det virker på alle maskiner."""
    navn = lag_filnavn(date(2026, 11, 11), "docx")
    assert navn.isascii()
    assert all(tegn.isalnum() or tegn in "-_." for tegn in navn)


@pytest.mark.parametrize(
    ("arbeidsgiver", "endelse", "forventet"),
    [
        # Case 1 og case 2 (matrisen i story 7.5).
        ("Testvik Utvikling AS", "docx", "Soknad_Testvik-Utvikling-AS_2026-11-11.docx"),
        ("Prøvdal Regnskap AS", "pdf", "Soknad_Provdal-Regnskap-AS_2026-11-11.pdf"),
        # Spesialtegn, linjeskift og å.
        ("Café/Bar: Ål\nAS", "docx", "Soknad_CafeBar-Al-AS_2026-11-11.docx"),
        # Flere bindestreker etter hverandre blir én.
        ("Bergen & Co", "docx", "Soknad_Bergen-Co_2026-11-11.docx"),
        # Tab, flere mellomrom og mellomrom først og sist.
        ("  Nord\t\tVest  ", "docx", "Soknad_Nord-Vest_2026-11-11.docx"),
        # Bindestrek først og sist fjernes.
        ("-Sør-Øst-", "docx", "Soknad_Sor-Ost_2026-11-11.docx"),
    ],
)
def test_fr29_filnavnet_har_arbeidsgiveren(arbeidsgiver, endelse, forventet):
    """FR-29/AD-11: filnavnet er Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>, med arbeidsgiveren renset:
    æøå skrevet om, andre tegn til ASCII, mellomrom til bindestrek og resten fjernet."""
    assert lag_filnavn(DATO, endelse, arbeidsgiver) == forventet


@pytest.mark.parametrize(
    ("arbeidsgiver", "forventet"),
    [
        ("æøå", "aeoa"),
        ("ÆØÅ", "AeOA"),
        ("Bærum Kjøkken Åsane", "Baerum-Kjokken-Asane"),
        ("Ærlig Øl Ås", "Aerlig-Ol-As"),
    ],
)
def test_fr29_aeoeaa_skrives_om(arbeidsgiver, forventet):
    """FR-29/AD-11: æ → ae, ø → o, å → a, og store: Æ → Ae, Ø → O, Å → A."""
    assert lag_filnavn(DATO, "docx", arbeidsgiver) == f"Soknad_{forventet}_2026-11-11.docx"


@pytest.mark.parametrize(
    ("arbeidsgiver", "forventet"),
    [
        ("Crème Brûlée Naïve", "Creme-Brulee-Naive"),
        ("Straße Łódź Đakovo", "Strasse-Lodz-Dakovo"),
        ("łđœþ ŒÞ", "ldoeth-OeTh"),
        ("A\u00a0B", "A-B"),
        ("Kontroll\x00\x07tegn", "Kontrolltegn"),
        ("100% «Beste» AS!", "100-Beste-AS"),
        ("Linje\r\nto", "Linje-to"),
    ],
)
def test_fr29_andre_tegn_til_ascii_eller_fjernet(arbeidsgiver, forventet):
    """FR-29/AD-11: andre bokstaver gjøres om til ASCII, alt mellomrom (også hardt mellomrom og
    linjeskift) blir bindestrek, og kontrolltegn og tegnsetting fjernes."""
    assert lag_filnavn(DATO, "pdf", arbeidsgiver) == f"Soknad_{forventet}_2026-11-11.pdf"


def test_fr29_lang_arbeidsgiver_kuttes_til_30_tegn():
    """FR-29/AD-11: en arbeidsgiver på 40 tegn kuttes til høyst 30 tegn."""
    arbeidsgiver = "Abcdefghij" * 4
    assert len(arbeidsgiver) == 40
    navn = lag_filnavn(DATO, "docx", arbeidsgiver)
    assert navn == f"Soknad_{arbeidsgiver[:MAKS_ARBEIDSGIVER]}_2026-11-11.docx"
    assert MAKS_ARBEIDSGIVER == 30


def test_fr29_kuttet_arbeidsgiver_slutter_ikke_med_bindestrek():
    """FR-29/AD-11: står det en bindestrek på plass 30 etter kuttet, fjernes den."""
    arbeidsgiver = "A" * 29 + " Bcdefghij"
    navn = lag_filnavn(DATO, "docx", arbeidsgiver)
    assert navn == f"Soknad_{'A' * 29}_2026-11-11.docx"
    midt = navn.removeprefix("Soknad_").removesuffix("_2026-11-11.docx")
    assert len(midt) <= MAKS_ARBEIDSGIVER
    assert not midt.endswith("-")


@pytest.mark.parametrize("arbeidsgiver", [None, "", "   ", "/:", "\n\t", "«»", "---"])
def test_fr29_uten_arbeidsgiver_er_filnavnet_bare_datoen(arbeidsgiver):
    """FR-29/AD-11: uten arbeidsgiver, eller når ingenting er igjen etter rensingen, er
    filnavnet Soknad_<dato>."""
    assert lag_filnavn(DATO, "docx", arbeidsgiver) == "Soknad_2026-11-11.docx"


@pytest.mark.parametrize(
    "arbeidsgiver",
    [
        "Testvik Utvikling AS",
        "Prøvdal Regnskap AS",
        "Café/Bar: Ål\nAS",
        "C:\\Windows\\..\\fil?.exe",
        "Ω≈ç√∫ 中文 🎉",
        "x" * 100,
    ],
)
def test_fr29_filnavnet_med_arbeidsgiver_har_bare_trygge_tegn(arbeidsgiver):
    """FR-29/AD-11: filnavnet har bare [A-Za-z0-9_.-], også med en arbeidsgiver full av rare
    tegn."""
    navn = lag_filnavn(DATO, "pdf", arbeidsgiver)
    assert re.fullmatch(r"[A-Za-z0-9_.-]+", navn)
    assert re.fullmatch(r"Soknad_([A-Za-z0-9]+(-[A-Za-z0-9]+)*_)?2026-11-11\.pdf", navn)
