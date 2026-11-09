"""Tester for den første resultatsiden: gap-analysen og nøkkelordtreffet (FR-6, FR-14,
FR-15, FR-17, FR-19, FR-20, NFR-4, NFR-6, AD-6, AD-7, AD-8, suksesskriterium 2).
Story 2.5.2."""

import html as html_modul
import json
import re

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from soknad.web.innlogging import OKT_ID
from tests.web.hjelpere import main, sett_soknad, soknaden, tagger_i

CASE = TESTDATA_MAPPE / "case-1-utvikler"
CV = (CASE / "cv.txt").read_text(encoding="utf-8")
ANNONSE = (CASE / "annonse.txt").read_text(encoding="utf-8")
FASIT = (CASE / "fasit.md").read_text(encoding="utf-8")
GAP_SVAR = json.loads((CASE / "ki-svar" / "gap.json").read_text(encoding="utf-8"))


@pytest.fixture
def paa_resultat(app, innlogget_client):
    """En innlogget klient som har lagt inn testdataene fra case 1 og fått analysen."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))
    svar = innlogget_client.post(
        "/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"}
    )
    assert svar.location == "/resultat"
    return innlogget_client


def html_av(svar):
    return svar.get_data(as_text=True)


def liste(html, id_):
    """Punktene i listen med denne id-en, med HTML-escapingen fjernet."""
    innhold = re.search(rf'<ul id="{id_}">(.*?)</ul>', html, re.S).group(1)
    return [html_modul.unescape(punkt) for punkt in re.findall(r"<li>([^<]*)</li>", innhold)]


def nokkelordtreff(html):
    treff = re.search(r'<p id="nokkelordtreff">([^<]*)</p>', html).group(1)
    return html_modul.unescape(treff)


def test_fr17_kriterium_2_case_1_gir_prosenten_i_fasiten(paa_resultat):
    """FR-17, suksesskriterium 2: nøkkelordtreffet på resultatsiden er nøyaktig linjen
    «X av Y = Z %» i fasit.md for case 1. Fasiten kan endres i Epic 4, så tallene leses
    fra fila."""
    fasit = re.search(r"^\d+ av \d+ = \d+ %$", FASIT, re.M)
    assert fasit, "Fant ingen linje «X av Y = Z %» i fasit.md"
    svar = paa_resultat.get("/resultat")
    assert svar.status_code == 200
    assert nokkelordtreff(html_av(svar)) == fasit.group(0)


def test_fr15_samme_prosent_naar_siden_lastes_paa_nytt(app, paa_resultat):
    """FR-15/AD-6, suksesskriterium 8: siden lastet to ganger gir samme tekst, og søknaden
    er uendret, fordi prosenten regnes fra den lagrede listen og aldri lagres."""
    forste = html_av(paa_resultat.get("/resultat"))
    soknad = soknaden(app, paa_resultat)
    andre = html_av(paa_resultat.get("/resultat"))
    assert forste == andre
    assert soknaden(app, paa_resultat) == soknad


def test_fr17_prosenten_regnes_fra_den_lagrede_listen(app, innlogget_client):
    """FR-17/AD-6: prosenten kommer fra nøkkelordlisten og CV-en i søknaden, ikke fra
    testdataene."""
    sett_soknad(
        app,
        innlogget_client,
        Soknad(
            steg=Steg.RESULTAT,
            modus=Modus.FULL_GENERERING,
            cv=Tekstfelt("Jeg kan Python og SQL."),
            annonse=Tekstfelt("annonse"),
            nokkelord=("Python", "SQL", "førerkort"),
            nokkelord_annonse="annonse",
            gap={"dekker": ["Kan Python"], "mangler": ["Har førerkort"]},
        ),
    )
    html = html_av(innlogget_client.get("/resultat"))
    assert nokkelordtreff(html) == "2 av 3 = 67 %"


def test_fr14_gap_listene_viser_punktene_fra_ki_svaret(paa_resultat):
    """FR-14: «Dette dekker CV-en din» og «Dette kan du jobbe videre med» viser punktene fra
    gap.json, i samme rekkefølge."""
    html = html_av(paa_resultat.get("/resultat"))
    assert liste(html, "gap-dekker") == GAP_SVAR["dekker"]
    assert liste(html, "gap-mangler") == GAP_SVAR["mangler"]
    assert len(GAP_SVAR["dekker"]) == 6
    assert len(GAP_SVAR["mangler"]) == 4


def test_nfr6_overskriftene_har_riktig_niva_og_sidetittel(paa_resultat):
    """NFR-6: h1 for siden, h2 for «Gap-analyse» og «Nøkkelordtreff», h3 for listene, og
    tittelen «Resultat – Søknadsassistenten»."""
    html = html_av(paa_resultat.get("/resultat"))
    innhold = main(html)
    overskrifter = re.findall(r"<(h[1-6])[^>]*>([^<]*)</h[1-6]>", innhold)
    assert overskrifter == [
        ("h1", "Slik passer CV-en din til stillingen"),
        ("h2", "Gap-analyse"),
        ("h3", "Dette dekker CV-en din"),
        ("h3", "Dette kan du jobbe videre med"),
        ("h2", "Nøkkelordtreff"),
    ]
    assert "<title>Resultat – Søknadsassistenten</title>" in html


def test_fr14_tekstene_ligger_i_tekster_py():
    """FR-14/FR-17: tekstene på resultatsiden står i web/tekster.py."""
    assert tekster.RESULTAT_OVERSKRIFT == "Slik passer CV-en din til stillingen"
    assert tekster.GAP_DEKKER == "Dette dekker CV-en din"
    assert tekster.GAP_MANGLER == "Dette kan du jobbe videre med"
    assert tekster.nokkelordtreff(7, 11, 64) == "7 av 11 = 64 %"


def test_nfr6_ki_svaret_escapes(app, innlogget_client):
    """NFR-6: tekst fra KI-en escapes, så den aldri blir HTML."""
    sett_soknad(
        app,
        innlogget_client,
        Soknad(
            steg=Steg.RESULTAT,
            cv=Tekstfelt("cv"),
            nokkelord=("cv",),
            gap={"dekker": ["<b>fet</b>"], "mangler": []},
        ),
    )
    html = html_av(innlogget_client.get("/resultat"))
    assert "<b>" not in main(html)
    assert "&lt;b&gt;fet&lt;/b&gt;" in main(html)
    assert liste(html, "gap-dekker") == ["<b>fet</b>"]


@pytest.mark.parametrize(
    ("steg", "side"),
    [(Steg.START, "/"), (Steg.MODUS, "/modus"), (Steg.INNLEGGING, "/innlegging")],
)
def test_fr20_resultatsiden_for_analysen_sender_til_steget(app, innlogget_client, steg, side):
    """FR-20/AD-8: før analysen har lyktes, sendes /resultat til siden for steget, og
    søknaden er uendret."""
    soknad = Soknad(steg=steg)
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.get("/resultat")
    assert svar.status_code == 302
    assert svar.location == side
    assert soknaden(app, innlogget_client) == soknad


def test_fr20_resultatsiden_rett_etter_innlogging_sender_til_startsiden(innlogget_client):
    """FR-20/AD-8: uten søknad i økten er steget start."""
    svar = innlogget_client.get("/resultat")
    assert svar.location == "/"


def test_fr19_endret_cv_gir_ikke_resultatsiden(paa_resultat):
    """FR-19/AD-8: endres CV-en via «Tilbake», vises ikke resultatsiden før analysen har lyktes
    igjen."""
    paa_resultat.post(
        "/innlegging", data={"cv": "Ny CV", "annonse": ANNONSE, "handling": "tilbake"}
    )
    assert paa_resultat.get("/resultat").location == "/innlegging"


def test_nfr4_cookien_har_bare_okt_id(paa_resultat):
    """NFR-4/AD-7: nøkkelordlisten, CV og annonse ligger bare i øktlageret, aldri i
    cookien."""
    paa_resultat.get("/resultat")
    with paa_resultat.session_transaction() as okt:
        assert set(okt) == {OKT_ID}


def test_fr6_resultatsiden_lagres_ikke_i_nettleseren(paa_resultat):
    """FR-6/AD-8: resultatsiden har Cache-Control: no-store."""
    assert paa_resultat.get("/resultat").headers["Cache-Control"] == "no-store"


def test_fr14_ett_punkt_per_krav(paa_resultat):
    """FR-14: listene har ett punkt per krav i gap.json, og ingen andre punkter."""
    html = html_av(paa_resultat.get("/resultat"))
    tagger = [t for t, _ in tagger_i(main(html))]
    assert tagger.count("li") == len(GAP_SVAR["dekker"]) + len(GAP_SVAR["mangler"])
