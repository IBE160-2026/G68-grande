"""Tester for søknaden i økten (FR-5, FR-20, AD-7, AD-8)."""

import dataclasses

import pytest

from soknad.kjerne.okt import Modus, Soknad, Tekstfelt, begynn, sett_inndata, velg_modus
from soknad.kjerne.steg import Steg


def test_fr5_ny_soknad_er_tom_og_paa_steg_start():
    """FR-5/AD-7: en ny søknad står på steg start, uten modus, samtykke, tekst eller resultater."""
    soknad = Soknad()
    assert soknad.steg == Steg.START
    assert soknad.modus is None
    assert soknad.samtykke is False
    for felt in (soknad.cv, soknad.annonse, soknad.eget_brev):
        assert felt == Tekstfelt("", None)
    assert soknad.nokkelord is None
    assert soknad.nokkelord_annonse is None
    assert soknad.arbeidsgiver is None
    assert soknad.gap is None
    assert soknad.opptatt is False


def test_fr5_soknaden_har_faste_felt_og_kan_ikke_endres_direkte():
    """AD-7: Soknad og Tekstfelt er frosne og har faste feltnavn (ingen løse strengnøkler)."""
    with pytest.raises(dataclasses.FrozenInstanceError):
        Soknad().steg = Steg.MODUS
    with pytest.raises(dataclasses.FrozenInstanceError):
        Tekstfelt().tekst = "x"
    assert [f.name for f in dataclasses.fields(Soknad)] == [
        "steg",
        "modus",
        "samtykke",
        "cv",
        "annonse",
        "eget_brev",
        "nokkelord",
        "nokkelord_annonse",
        "arbeidsgiver",
        "gap",
        "opptatt",
    ]


def test_fr5_to_nye_soknader_deler_ikke_tekstfelt():
    """AD-7: hver ny søknad får egne tekstfelt (default_factory)."""
    assert Soknad() == Soknad()
    assert Soknad().cv is not Soknad().cv


def test_fr20_modusene():
    """FR-20: Full generering er den eneste modusen fram til Epic 5."""
    assert list(Modus) == [Modus.FULL_GENERERING]
    assert Modus("full_generering") is Modus.FULL_GENERERING


def test_fr5_begynn_gir_steg_modus():
    """FR-5/AD-8: «Begynn å lage søknad» flytter steget fra start til modus."""
    ny = begynn(Soknad())
    assert ny.steg == Steg.MODUS
    assert dataclasses.replace(ny, steg=Steg.START) == Soknad()


def test_fr5_begynn_setter_aldri_steget_lavere():
    """FR-5/AD-8: står søknaden lenger fram enn modus, beholdes steget og resten."""
    soknad = Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, cv=Tekstfelt("cv"))
    assert begynn(soknad) == soknad


def test_fr20_velg_modus_setter_modus_og_steg_innlegging():
    """FR-20/AD-8: velg_modus lagrer modusen og flytter steget til innlegging."""
    ny = velg_modus(begynn(Soknad()), Modus.FULL_GENERERING)
    assert ny.modus is Modus.FULL_GENERERING
    assert ny.steg == Steg.INNLEGGING


def test_fr20_velg_modus_nullstiller_gap_og_beholder_tekstene():
    """FR-20/AD-8: gap-analysen nullstilles, og steget går tilbake til innlegging, men CV,
    annonse og nøkkelordlisten beholdes."""
    soknad = Soknad(
        steg=Steg.RESULTAT,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt("min cv", "cv.pdf"),
        annonse=Tekstfelt("annonsen"),
        nokkelord=("python", "sql"),
        nokkelord_annonse="annonsen",
        arbeidsgiver="Firma AS",
        gap={"dekker": ["python"], "mangler": ["sql"]},
    )
    ny = velg_modus(soknad, Modus.FULL_GENERERING)
    assert ny.steg == Steg.INNLEGGING
    assert ny.gap is None
    assert ny == dataclasses.replace(soknad, steg=Steg.INNLEGGING, gap=None)
    # Den gamle søknaden er uendret.
    assert soknad.steg == Steg.RESULTAT


# --- sett_inndata (story 2.5.1) ---


def _med_resultater(steg=Steg.RESULTAT):
    return Soknad(
        steg=steg,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt("min cv"),
        annonse=Tekstfelt("annonsen"),
        nokkelord=("python", "sql"),
        nokkelord_annonse="annonsen",
        arbeidsgiver="Firma AS",
        gap={"dekker": ["python"], "mangler": ["sql"]},
    )


def test_fr19_sett_inndata_med_like_tekster_endrer_ingenting():
    """FR-19/AD-8: sendes de samme tekstene på nytt, er søknaden den samme, også nøkkelordlisten
    og steget."""
    soknad = _med_resultater()
    assert sett_inndata(soknad, cv=Tekstfelt("min cv"), annonse=Tekstfelt("annonsen")) is soknad


@pytest.mark.parametrize(
    ("cv", "annonse"),
    [("ny cv", "annonsen"), ("min cv", "ny annonse"), ("min cv ", "annonsen")],
)
def test_fr19_sett_inndata_med_endret_tekst_nullstiller_resultatene(cv, annonse):
    """FR-19/AD-8: er en av tekstene endret (også bare et mellomrom), lagres tekstene, og
    nøkkelordlisten, arbeidsgiveren og gap-analysen nullstilles. Steget blir innlegging."""
    soknad = _med_resultater()
    ny = sett_inndata(soknad, cv=Tekstfelt(cv), annonse=Tekstfelt(annonse))
    assert ny == dataclasses.replace(
        soknad,
        cv=Tekstfelt(cv),
        annonse=Tekstfelt(annonse),
        nokkelord=None,
        nokkelord_annonse=None,
        arbeidsgiver=None,
        gap=None,
        steg=Steg.INNLEGGING,
    )
    # Den gamle søknaden er uendret.
    assert soknad.nokkelord == ("python", "sql")


@pytest.mark.parametrize("steg", [Steg.INNLEGGING, Steg.RESULTAT, Steg.BREV])
def test_fr19_sett_inndata_gir_hoyst_steg_innlegging(steg):
    """AD-8: med endret tekst blir steget innlegging, uansett hvor langt søknaden var kommet."""
    ny = sett_inndata(_med_resultater(steg), cv=Tekstfelt("ny"), annonse=Tekstfelt("ny"))
    assert ny.steg == Steg.INNLEGGING


def test_fr13_sett_inndata_kan_tomme_feltene():
    """FR-13: tomme felt lagres også (søppelbøtta, så «Tilbake»)."""
    ny = sett_inndata(_med_resultater(), cv=Tekstfelt(""), annonse=Tekstfelt(""))
    assert ny.cv == Tekstfelt("")
    assert ny.annonse == Tekstfelt("")
