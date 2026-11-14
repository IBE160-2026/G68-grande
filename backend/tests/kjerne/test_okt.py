"""Tester for søknaden i økten (FR-5, FR-20, FR-29, AD-7, AD-8)."""

import dataclasses

import pytest

from soknad.kjerne.okt import (
    Modus,
    Soknad,
    Tekstfelt,
    begynn,
    sett_analyse,
    sett_brev,
    sett_inndata,
    sett_lastet_ned,
    sett_opptatt,
    velg_modus,
)
from soknad.kjerne.steg import Steg
from soknad.kjerne.testdata_match import vask


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
    assert soknad.brev is None
    assert soknad.lastet_ned is False
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
        "brev",
        "lastet_ned",
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
        brev=None,
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


# --- sett_analyse (story 2.5.2) ---

NOKKELORD_SVAR = {"nokkelord": ["Python", "SQL"], "arbeidsgiver": "Firma AS"}
GAP_SVAR = {"dekker": ["Kan Python"], "mangler": ["Kan SQL"]}


def _klar_for_analyse(steg=Steg.INNLEGGING):
    return Soknad(
        steg=steg,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt("min cv"),
        annonse=Tekstfelt("Vi søker en  UTVIKLER!\n"),
    )


def test_fr15_sett_analyse_lagrer_listen_annonsen_arbeidsgiveren_og_gap():
    """FR-15/FR-21/AD-7: nøkkelordlisten lagres som tuple, med den vaskede annonseteksten den
    ble laget fra, arbeidsgiveren og gap-analysen. Steget blir resultat."""
    soknad = _klar_for_analyse()
    ny = sett_analyse(soknad, nokkelord=NOKKELORD_SVAR, gap=GAP_SVAR)
    assert ny == dataclasses.replace(
        soknad,
        nokkelord=("Python", "SQL"),
        nokkelord_annonse=vask("Vi søker en  UTVIKLER!\n"),
        arbeidsgiver="Firma AS",
        gap=GAP_SVAR,
        steg=Steg.RESULTAT,
    )
    assert ny.nokkelord_annonse == "visøkerenutvikler"
    # Den gamle søknaden er uendret.
    assert soknad.nokkelord is None


def test_fr21_sett_analyse_uten_arbeidsgiver():
    """FR-21/AD-4: arbeidsgiver kan være null i KI-svaret."""
    svar = {"nokkelord": ["Python"], "arbeidsgiver": None}
    assert sett_analyse(_klar_for_analyse(), nokkelord=svar, gap=GAP_SVAR).arbeidsgiver is None


@pytest.mark.parametrize(
    ("steg", "forventet"),
    [(Steg.INNLEGGING, Steg.RESULTAT), (Steg.RESULTAT, Steg.RESULTAT), (Steg.BREV, Steg.BREV)],
)
def test_fr20_sett_analyse_gir_minst_steg_resultat(steg, forventet):
    """FR-20/AD-8: steget blir minst resultat, og et steg lenger fram beholdes."""
    ny = sett_analyse(_klar_for_analyse(steg), nokkelord=NOKKELORD_SVAR, gap=GAP_SVAR)
    assert ny.steg == forventet


# --- sett_opptatt (story 2.7.1) ---


def test_fr27_sett_opptatt_endrer_bare_opptatt():
    """FR-27/AD-8: sett_opptatt setter og fjerner opptatt, og resten av søknaden er uendret."""
    soknad = _klar_for_analyse()
    opptatt = sett_opptatt(soknad, True)
    assert opptatt == dataclasses.replace(soknad, opptatt=True)
    assert sett_opptatt(opptatt, False) == soknad
    # Den gamle søknaden er uendret.
    assert soknad.opptatt is False


# --- sett_brev (story 3.1) ---

BREV_SVAR = {"avsnitt": ["Første avsnitt.", "Med vennlig hilsen"]}


@pytest.mark.parametrize(
    ("steg", "forventet"), [(Steg.RESULTAT, Steg.BREV), (Steg.BREV, Steg.BREV)]
)
def test_fr22_sett_brev_lagrer_brevet_og_gir_steg_brev(steg, forventet):
    """FR-22/AD-8: brevet lagres, og steget blir minst brev. Resten er uendret."""
    soknad = _med_resultater(steg)
    ny = sett_brev(soknad, BREV_SVAR)
    assert ny == dataclasses.replace(soknad, brev=BREV_SVAR, steg=forventet)
    # Den gamle søknaden er uendret.
    assert soknad.brev is None


def test_fr22_velg_modus_nullstiller_brevet():
    """FR-22/AD-8: velges modus på nytt, er det gamle brevet borte, og steget er innlegging."""
    ny = velg_modus(sett_brev(_med_resultater(), BREV_SVAR), Modus.FULL_GENERERING)
    assert ny.brev is None
    assert ny.steg == Steg.INNLEGGING


def test_fr22_sett_inndata_med_endret_tekst_nullstiller_brevet():
    """FR-19/FR-22/AD-8: endres CV-en, er det gamle brevet borte, og steget er innlegging."""
    soknad = sett_brev(_med_resultater(), BREV_SVAR)
    ny = sett_inndata(soknad, cv=Tekstfelt("ny cv"), annonse=Tekstfelt("annonsen"))
    assert ny.brev is None
    assert ny.steg == Steg.INNLEGGING


def test_fr22_sett_inndata_med_like_tekster_beholder_brevet():
    """FR-19/FR-22: er tekstene like som før, er søknaden uendret, også brevet."""
    soknad = sett_brev(_med_resultater(), BREV_SVAR)
    assert sett_inndata(soknad, cv=Tekstfelt("min cv"), annonse=Tekstfelt("annonsen")) is soknad


# --- lastet_ned (story 3.2) ---


def _lastet_ned():
    return sett_lastet_ned(sett_brev(_med_resultater(), BREV_SVAR))


def test_fr29_sett_lastet_ned_endrer_bare_lastet_ned():
    """FR-29: sett_lastet_ned gjør lastet_ned sann. Resten av søknaden er uendret."""
    soknad = sett_brev(_med_resultater(), BREV_SVAR)
    assert soknad.lastet_ned is False
    ny = sett_lastet_ned(soknad)
    assert ny == dataclasses.replace(soknad, lastet_ned=True)
    assert soknad.lastet_ned is False


def test_fr29_nytt_brev_er_ikke_lastet_ned():
    """FR-29/AD-8: et nytt brev (sett_brev) er ikke lastet ned ennå."""
    assert sett_brev(_lastet_ned(), BREV_SVAR).lastet_ned is False


def test_fr29_velg_modus_nullstiller_lastet_ned():
    """FR-29/AD-8: velges modus på nytt, er lastet_ned usann."""
    assert velg_modus(_lastet_ned(), Modus.FULL_GENERERING).lastet_ned is False


def test_fr29_sett_inndata_med_endret_tekst_nullstiller_lastet_ned():
    """FR-19/FR-29/AD-8: endres CV-en, er lastet_ned usann."""
    ny = sett_inndata(_lastet_ned(), cv=Tekstfelt("ny cv"), annonse=Tekstfelt("annonsen"))
    assert ny.lastet_ned is False


def test_fr29_sett_inndata_med_like_tekster_beholder_lastet_ned():
    """FR-19/FR-29: er tekstene like som før, er søknaden uendret, også lastet_ned."""
    soknad = _lastet_ned()
    assert sett_inndata(soknad, cv=Tekstfelt("min cv"), annonse=Tekstfelt("annonsen")) is soknad


def test_fr36_begynn_lagrer_samtykket():
    """FR-36/AD-7: begynn(soknad, samtykke=True) lagrer samtykket. Uten samtykke er det usant."""
    assert begynn(Soknad(), samtykke=True) == Soknad(steg=Steg.MODUS, samtykke=True)
    assert begynn(Soknad()).samtykke is False


def test_fr36_begynn_fjerner_aldri_et_samtykke():
    """FR-36/AD-8: et samtykke som alt er gitt, beholdes når begynn kalles uten samtykke."""
    soknad = Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, samtykke=True)
    assert begynn(soknad) == soknad
