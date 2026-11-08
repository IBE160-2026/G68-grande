"""Tester for telleregelen for nøkkelordtreff i kjerne/telleregel.py (FR-16, FR-17)."""

import dataclasses

import pytest

from soknad.kjerne.telleregel import Nokkelordtreff, tell_treff


def test_fr17_2_av_3_gir_67_prosent():
    """FR-16/FR-17: 2 av 3 nøkkelord i CV-en gir 67 %, og nøkkelordene merkes som treff
    eller ikke treff."""
    resultat = tell_treff(["Python", "SQL", "førerkort"], "Jeg kan Python og SQL.")
    assert resultat.antall_treff == 2
    assert resultat.antall == 3
    assert resultat.prosent == 67
    assert resultat.treff == ("Python", "SQL")
    assert resultat.ikke_treff == ("førerkort",)


def test_fr17_1_av_8_gir_13_prosent_ikke_12():
    """FR-17: 1 av 8 er 12,5 %, som rundes opp til 13. round() ville gitt 12 (rundes mot
    partall), og derfor brukes Decimal med ROUND_HALF_UP."""
    nokkelord = ["Python", "Java", "Kotlin", "Rust", "Haskell", "Erlang", "Scala", "Elixir"]
    resultat = tell_treff(nokkelord, "Jeg har jobbet med Python.")
    assert resultat.antall_treff == 1
    assert resultat.antall == 8
    assert resultat.prosent == 13
    assert round(1 * 100 / 8) == 12


def test_fr17_0_av_y_gir_0_prosent():
    """FR-17: ingen nøkkelord i CV-en gir 0 %, og alle står i ikke_treff."""
    resultat = tell_treff(["SQL", "førerkort", "Excel"], "Jeg liker å lese bøker.")
    assert resultat.antall_treff == 0
    assert resultat.prosent == 0
    assert resultat.treff == ()
    assert resultat.ikke_treff == ("SQL", "førerkort", "Excel")


def test_fr17_kort_ord_gir_ikke_treff_inne_i_et_annet_ord():
    """FR-17: nøkkelord på 1–3 tegn må stå som eget ord, så «C» er ikke et treff i «Center»."""
    assert tell_treff(["C"], "Jeg jobbet på et Center.").antall_treff == 0


def test_fr17_grensen_paa_4_tegn():
    """FR-17: «Java» (4 tegn) gir treff i «JavaScript», den kjente begrensningen i README,
    mens «SQL» (3 tegn) ikke gir treff i «MySQL»."""
    assert tell_treff(["Java"], "Jeg kan JavaScript.").antall_treff == 1
    assert tell_treff(["SQL"], "Jeg kan MySQL.").antall_treff == 0


def test_fr17_kort_ord_gir_ikke_treff_bak_i_et_annet_ord():
    """FR-17: et kort nøkkelord må stå som eget ord også foran, så «SQL» er ikke et treff
    i «MySQL», og «C» er ikke et treff i «ABC»."""
    assert tell_treff(["SQL"], "MySQL").antall_treff == 0
    assert tell_treff(["C"], "ABC").antall_treff == 0


def test_fr17_korte_ord_med_tegn_gir_treff():
    """FR-17: «C#» og «C++» gir treff når de står i CV-en."""
    resultat = tell_treff(["C#", "C++"], "C#, C++ og SQL")
    assert resultat.treff == ("C#", "C++")


def test_fr17_tegn_i_nokkelord_leses_som_vanlige_tegn():
    """FR-17: «+» i «C++» er et vanlig tegn, ikke en regel i søket, så «C++» gir ikke treff
    når CV-en bare har «C»."""
    assert tell_treff(["C++"], "Jeg kan C og Java.").antall_treff == 0


def test_fr17_kjent_begrensning_c_gir_treff_i_c_sharp_og_c_plus_plus():
    """FR-17: «C» gir treff i «C# og C++», fordi tegnet etter «C» ikke er en bokstav
    (kjent begrensning i README)."""
    assert tell_treff(["C"], "C# og C++").antall_treff == 1


def test_fr17_bindestrek_gir_treff():
    """FR-17: «python» treffer i «python-utvikler», og det korte «år» i «år-tall»."""
    assert tell_treff(["python"], "Jeg er python-utvikler.").antall_treff == 1
    assert tell_treff(["år"], "år-tall").antall_treff == 1


def test_fr17_aeoeaa_gir_treff_inne_i_lengre_ord():
    """FR-17: «Søknad» treffer i «søknadsbrev», også med æøå og store bokstaver."""
    assert tell_treff(["Søknad"], "Jeg skrev et søknadsbrev.").antall_treff == 1


def test_fr17_store_og_smaa_bokstaver_spiller_ingen_rolle():
    """FR-17: nøkkelord og CV sammenlignes med casefold()."""
    assert tell_treff(["SQL"], "sql").antall_treff == 1
    assert tell_treff(["python"], "PYTHON").antall_treff == 1


def test_fr17_nokkelord_som_staar_flere_ganger_telles_en_gang():
    """FR-17: hvert nøkkelord telles én gang, også om det står flere ganger i CV-en."""
    resultat = tell_treff(["SQL"], "SQL i jobben, SQL på fritiden.")
    assert resultat.antall_treff == 1
    assert resultat.antall == 1
    assert resultat.prosent == 100


def test_fr17_linjeskift_regnes_som_mellomrom():
    """FR-17: «Microsoft Office» treffer også når CV-en har linjeskift mellom ordene."""
    assert tell_treff(["Microsoft Office"], "Microsoft\nOffice").antall_treff == 1
    assert tell_treff(["Microsoft\tOffice"], "Microsoft  Office").antall_treff == 1


def test_fr17_like_nokkelord_telles_som_ett_med_forste_skrivemaate():
    """FR-17: «SQL» og «sql» er samme nøkkelord, telles én gang og vises som «SQL»."""
    resultat = tell_treff(["SQL", "sql"], "sql")
    assert resultat.antall == 1
    assert resultat.treff == ("SQL",)


@pytest.mark.parametrize("nokkelord", [[], ["  "], ["", " \n "]])
def test_fr17_tom_liste_gir_valueerror(nokkelord):
    """FR-17: en tom nøkkelordliste, også etter at tomme nøkkelord er fjernet, gir ValueError."""
    with pytest.raises(ValueError):
        tell_treff(nokkelord, "Jeg kan SQL.")


def test_fr17_tomme_nokkelord_i_listen_hoppes_over():
    """FR-17: tomme nøkkelord i en liste som ellers har nøkkelord, telles ikke med."""
    resultat = tell_treff(["SQL", "", "  "], "SQL")
    assert resultat.antall == 1
    assert resultat.prosent == 100
    assert resultat.treff == ("SQL",)


@pytest.mark.parametrize("cv", ["", " \n "])
def test_fr17_tom_cv_gir_0_prosent(cv):
    """FR-17: en tom CV, også en med bare mellomrom, gir 0 av 1 = 0 %."""
    resultat = tell_treff(["SQL"], cv)
    assert resultat.antall_treff == 0
    assert resultat.antall == 1
    assert resultat.prosent == 0


def test_fr17_samme_liste_og_cv_gir_samme_resultat():
    """FR-17 (AD-6): samme nøkkelordliste og CV to ganger gir likt resultat."""
    nokkelord = ["Python", "SQL", "førerkort", "C"]
    cv = "Python-utvikler med SQL og C#."
    assert tell_treff(nokkelord, cv) == tell_treff(nokkelord, cv)


def test_fr17_resultatet_er_frosset():
    """FR-17: Nokkelordtreff kan ikke endres etter at det er laget."""
    resultat = tell_treff(["SQL"], "SQL")
    assert isinstance(resultat, Nokkelordtreff)
    with pytest.raises(dataclasses.FrozenInstanceError):
        resultat.prosent = 0
