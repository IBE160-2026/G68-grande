"""Tester for resultatsiden: gap-analysen, nøkkelordtreffet, forklaringene og «Tilbake»
(FR-6, FR-14–FR-20, NFR-4, NFR-6, NFR-7, AD-1, AD-6, AD-7, AD-8, suksesskriterium 2 og 8).
Story 2.5.2 og 2.6."""

import html as html_modul
import json
import re

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from soknad.web.innlogging import OKT_ID
from tests.web.hjelpere import STIL, css_blokk, main, sett_soknad, soknaden, tagger_i

CASE = TESTDATA_MAPPE / "case-1-utvikler"
CV = (CASE / "cv.txt").read_text(encoding="utf-8")
ANNONSE = (CASE / "annonse.txt").read_text(encoding="utf-8")
FASIT = (CASE / "fasit.md").read_text(encoding="utf-8")
GAP_SVAR = json.loads((CASE / "ki-svar" / "gap.json").read_text(encoding="utf-8"))
NOKKELORD_SVAR = json.loads((CASE / "ki-svar" / "nokkelord.json").read_text(encoding="utf-8"))


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
    """Punktene i listen med denne id-en, uten pynteikonet og med HTML-escapingen fjernet.
    En tom liste er en <p> med teksten for tom liste, og gir []."""
    innhold = re.search(rf'<ul class="resultatliste" id="{id_}">(.*?)</ul>', html, re.S)
    if innhold is None:
        assert re.search(rf'<p class="tom-liste" id="{id_}">', html), f"Fant ikke {id_}"
        return []
    punkter = re.findall(r"<li>(.*?)</li>", innhold.group(1), re.S)
    return [html_modul.unescape(re.sub(r"<span[^>]*>[^<]*</span>", "", p)) for p in punkter]


def tom_tekst(html, id_):
    """Teksten for tom liste med denne id-en, uten taggene rundt pynteikonet."""
    innhold = re.search(rf'<p class="tom-liste" id="{id_}">(.*?)</p>', html, re.S).group(1)
    return html_modul.unescape(re.sub(r"<[^>]+>", "", innhold))


def nokkelordtreff(html):
    treff = re.search(r'<strong id="nokkelordtreff">([^<]*)</strong>', html).group(1)
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
        ("h3", "Står i CV-en (7)"),
        ("h3", "Står ikke i CV-en (4)"),
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


def test_fr14_ett_punkt_per_krav_og_nokkelord(paa_resultat):
    """FR-14/FR-16: listene har ett punkt per krav i gap.json og ett per nøkkelord, og ingen
    andre punkter."""
    html = html_av(paa_resultat.get("/resultat"))
    tagger = [t for t, _ in tagger_i(main(html))]
    krav = len(GAP_SVAR["dekker"]) + len(GAP_SVAR["mangler"])
    assert tagger.count("li") == krav + len(NOKKELORD_SVAR["nokkelord"])


# --- Story 2.6: hele resultatsiden ---


def resultat_med(app, client, *, cv, nokkelord, dekker, mangler):
    """Resultatsiden for en søknad med egne lister (ikke fra testdata/)."""
    sett_soknad(
        app,
        client,
        Soknad(
            steg=Steg.RESULTAT,
            modus=Modus.FULL_GENERERING,
            cv=Tekstfelt(cv),
            annonse=Tekstfelt("annonse"),
            nokkelord=nokkelord,
            nokkelord_annonse="annonse",
            gap={"dekker": dekker, "mangler": mangler},
        ),
    )
    return html_av(client.get("/resultat"))


def h3_tekster(html):
    return [html_modul.unescape(t) for t in re.findall(r"<h3>([^<]*)</h3>", main(html))]


def test_fr16_nokkelordlistene_som_i_fasiten(paa_resultat):
    """FR-16/FR-17: «Står i CV-en (7)» og «Står ikke i CV-en (4)» har nøkkelordene fra
    tabellen i fasit.md, i listens rekkefølge."""
    rader = re.findall(r"^\| (.+?) \| (Ja|Nei) \|$", FASIT, re.M)
    ja = [ord_ for ord_, svar in rader if svar == "Ja"]
    nei = [ord_ for ord_, svar in rader if svar == "Nei"]
    html = html_av(paa_resultat.get("/resultat"))
    assert liste(html, "nokkelord-treff") == ja
    assert liste(html, "nokkelord-ikke-treff") == nei
    assert f"Står i CV-en ({len(ja)})" in h3_tekster(html)
    assert f"Står ikke i CV-en ({len(nei)})" in h3_tekster(html)


def test_ux_dr13_tom_dekker_gir_teksten(app, innlogget_client):
    """UX-DR13: tom «Dette dekker CV-en din» gir teksten fra EXPERIENCE."""
    html = resultat_med(
        app, innlogget_client, cv="Python", nokkelord=("Python",), dekker=[], mangler=["SQL"]
    )
    assert liste(html, "gap-dekker") == []
    assert tom_tekst(html, "gap-dekker") == (
        "CV-en din dekker ingen av kravene ennå. Se hva du kan jobbe videre med."
    )
    assert liste(html, "gap-mangler") == ["SQL"]


def test_ux_dr13_tom_mangler_gir_teksten_med_skjult_ikon(app, innlogget_client):
    """UX-DR13/UX-DR21: tom «Dette kan du jobbe videre med» gir «Bra jobbet! …» med 🎉,
    og 🎉 er skjult for skjermlesere."""
    html = resultat_med(
        app, innlogget_client, cv="Python", nokkelord=("Python",), dekker=["Python"], mangler=[]
    )
    assert tom_tekst(html, "gap-mangler") == (
        "Bra jobbet! CV-en din dekker alle kravene i annonsen. 🎉"
    )
    assert '<span aria-hidden="true">🎉</span>' in html


def test_ux_dr13_ingen_treff_gir_teksten(app, innlogget_client):
    """UX-DR13/FR-17: ingen nøkkelord i CV-en gir «Står i CV-en (0)», teksten og 0 %."""
    html = resultat_med(
        app, innlogget_client, cv="Python", nokkelord=("Docker",), dekker=[], mangler=["x"]
    )
    assert "Står i CV-en (0)" in h3_tekster(html)
    assert tom_tekst(html, "nokkelord-treff") == "Ingen av nøkkelordene står i CV-en ennå."
    assert liste(html, "nokkelord-ikke-treff") == ["Docker"]
    assert nokkelordtreff(html) == "0 av 1 = 0 %"
    assert '<rect class="fyll" width="0" height="12">' in html


def test_ux_dr13_alle_treff_gir_teksten(app, innlogget_client):
    """UX-DR13/FR-17: alle nøkkelordene i CV-en gir «Står ikke i CV-en (0)», teksten og
    100 %."""
    html = resultat_med(
        app,
        innlogget_client,
        cv="Python og SQL",
        nokkelord=("Python", "SQL"),
        dekker=["x"],
        mangler=[],
    )
    assert "Står ikke i CV-en (0)" in h3_tekster(html)
    assert tom_tekst(html, "nokkelord-ikke-treff") == "Alle nøkkelordene står i CV-en din!"
    assert liste(html, "nokkelord-treff") == ["Python", "SQL"]
    assert nokkelordtreff(html) == "2 av 2 = 100 %"
    assert '<rect class="fyll" width="100" height="12">' in html


def test_fr18_rekkefolgen_pa_siden(paa_resultat):
    """FR-14–FR-19 (EXPERIENCE): gap-analysen, linjen om at de kan si forskjellig,
    nøkkelordtreffet, ATS-forklaringen og til slutt «Tilbake»."""
    innhold = main(html_av(paa_resultat.get("/resultat")))
    deler = [
        'id="gap-overskrift"',
        'id="kan-si-forskjellig"',
        'id="nokkelord-overskrift"',
        'id="ats"',
        'href="/innlegging"',
    ]
    plasser = [innhold.index(del_) for del_ in deler]
    assert plasser == sorted(plasser)


def test_fr14_gap_analysen_er_merket_og_forklart(paa_resultat):
    """FR-14/UX-DR13: «Gap-analyse» har merket «Laget av KI» ved siden av overskriften (ikke
    inne i den) og underteksten."""
    innhold = main(html_av(paa_resultat.get("/resultat")))
    gap = re.search(r'aria-labelledby="gap-overskrift">(.*?)</section>', innhold, re.S).group(1)
    assert '<h2 class="boks-overskrift" id="gap-overskrift">Gap-analyse</h2>' in gap
    assert '<span class="merkelapp">Laget av KI</span>' in gap
    assert "Kravene fra annonsen, sammenlignet med CV-en din." in gap


def test_fr18_linjen_om_at_de_kan_si_forskjellig(paa_resultat):
    """FR-18: linjen mellom gap-analysen og nøkkelordtreffet."""
    html = html_av(paa_resultat.get("/resultat"))
    linje = re.search(r'<p class="kan-si-forskjellig"[^>]*>([^<]*)</p>', html).group(1)
    assert html_modul.unescape(linje) == (
        "Gap-analysen og nøkkelordtreffet kan si litt forskjellig. Gap-analysen er en "
        "vurdering KI-en gjør, mens nøkkelordtreffet bare teller ord."
    )


def test_fr17_tallet_har_forklaringen_ved_siden_av(paa_resultat):
    """FR-17: «X av Y = Z %» med «av nøkkelordene står i CV-en din»."""
    html = html_av(paa_resultat.get("/resultat"))
    assert re.search(
        r'<strong id="nokkelordtreff">[^<]*</strong> <span>av nøkkelordene står i CV-en '
        r"din</span>",
        html,
    )


def test_fr17_prosentlinjen_er_pynt_og_fylt_til_prosenten(paa_resultat):
    """FR-17/UX-DR13: prosentlinjen er skjult for skjermlesere, 12 px høy og fylt til 64 %
    av 100 uten animasjon."""
    html = html_av(paa_resultat.get("/resultat"))
    linje = next(a for t, a in tagger_i(main(html)) if t == "svg")
    assert linje["class"] == "prosentlinje"
    assert linje["aria-hidden"] == "true"
    assert linje["focusable"] == "false"
    assert linje["viewbox"] == "0 0 100 12"
    assert linje["height"] == "12"
    rect = [a for t, a in tagger_i(main(html)) if t == "rect"]
    assert rect == [
        {"class": "spor", "width": "100", "height": "12"},
        {"class": "fyll", "width": "64", "height": "12"},
    ]
    css = STIL.read_text(encoding="utf-8")
    for velger in (".prosentlinje", ".prosentlinje .spor", ".prosentlinje .fyll"):
        assert "transition" not in css_blokk(css, velger)
        assert "animation" not in css_blokk(css, velger)


@pytest.mark.parametrize(
    ("navn", "skjermleser", "tekst"),
    [
        (
            "gap",
            "Hva er en gap-analyse?",
            "En KI-vurdering av hvilke krav i annonsen CV-en dekker, og hvilke du kan jobbe "
            "videre med.",
        ),
        (
            "nokkelord",
            "Hva er nøkkelordtreff?",
            "En ordtelling av hvor mange av annonsens nøkkelord som står i CV-en. Det er bare "
            "en pekepinn på hvordan et ATS kan vurdere CV-en, ikke en garanti.",
        ),
    ],
)
def test_ux_dr11_i_knappen(paa_resultat, navn, skjermleser, tekst):
    """UX-DR11: «i»-knappen har tekst for skjermlesere, aria-expanded="false" og
    aria-controls til boksen, som står rett etter knappen og er skjult når siden åpnes.
    Bokstaven «i» er bare pynt."""
    html = html_av(paa_resultat.get("/resultat"))
    tagger = tagger_i(main(html))
    plass, knapp = next(
        (i, a)
        for i, (t, a) in enumerate(tagger)
        if t == "button" and a.get("aria-controls") == f"info-{navn}"
    )
    assert knapp["type"] == "button"
    assert knapp["class"] == "info-knapp"
    assert tagger[plass - 1] == ("div", {"class": "info"})
    assert knapp["aria-label"] == skjermleser
    assert knapp["aria-expanded"] == "false"
    assert tagger[plass + 1] == ("span", {"aria-hidden": "true"})
    assert tagger[plass + 2] == ("p", {"class": "info-boks", "id": f"info-{navn}", "hidden": None})
    boks = re.search(rf'<p class="info-boks" id="info-{navn}" hidden>([^<]*)</p>', html)
    assert html_modul.unescape(boks.group(1)) == tekst


def test_fr18_ats_forklaringen_er_lukket(paa_resultat):
    """FR-18/UX-DR13: «Hva er ATS og hva betyr det for deg?» er en <details> som er lukket
    når siden åpnes, med de to avsnittene fra EXPERIENCE."""
    html = html_av(paa_resultat.get("/resultat"))
    details = next(a for t, a in tagger_i(main(html)) if t == "details")
    assert "open" not in details
    ats = re.search(r'<details class="ats" id="ats">(.*?)</details>', html, re.S).group(1)
    assert "<summary>Hva er ATS og hva betyr det for deg?</summary>" in ats
    avsnitt = [html_modul.unescape(a) for a in re.findall(r"<p>([^<]*)</p>", ats)]
    assert avsnitt == [
        "Mange arbeidsgivere sender søknadene gjennom et ATS før et menneske leser dem. Et ATS "
        "er et dataprogram som blant annet ser etter ord fra annonsen.",
        "Står flere av nøkkelordene i CV-en din, er det større sjanse for at den blir lest. Men "
        "prosenten over er bare en pekepinn, ikke en garanti.",
    ]


def test_ux_dr21_pynteikonene_er_skjult_for_skjermlesere(app, innlogget_client):
    """UX-DR21: hver ✓, →, ○ og 🎉 står i en <span aria-hidden="true">."""
    forste = resultat_med(
        app,
        innlogget_client,
        cv="Python",
        nokkelord=("Python", "Docker"),
        dekker=["Python"],
        mangler=[],
    )
    andre = resultat_med(
        app, innlogget_client, cv="x", nokkelord=("x",), dekker=[], mangler=["SQL"]
    )
    for html, ikoner in ((forste, ("✓", "○", "🎉")), (andre, ("→",))):
        innhold = main(html)
        for ikon in ikoner:
            skjult = re.findall(rf'<span[^>]*aria-hidden="true">{ikon}</span>', innhold)
            assert innhold.count(ikon) >= 1
            assert len(skjult) == innhold.count(ikon)


def test_fr19_tilbake_er_en_lenke_til_innleggingen(paa_resultat):
    """FR-19/UX-DR4: «Tilbake» er en sekundærknapp nederst, en lenke til innleggingen."""
    innhold = main(html_av(paa_resultat.get("/resultat")))
    knapperad = re.search(r'<div class="knapperad">(.*?)</div>', innhold, re.S).group(1)
    assert '<a class="sekundaerknapp" href="/innlegging">Tilbake</a>' in knapperad


def test_fr19_tilbake_gir_feltene_fylt_ut(paa_resultat):
    """FR-19: etter «Tilbake» står CV-en og annonsen fortsatt i feltene."""
    html = html_av(paa_resultat.get("/innlegging"))
    for navn, tekst in (("cv", CV), ("annonse", ANNONSE)):
        felt = re.search(rf'<textarea id="{navn}-tekst"[^>]*>\n?(.*?)</textarea>', html, re.S)
        assert html_modul.unescape(felt.group(1)) == tekst


def test_fr15_kriterium_8_samme_treff_etter_tilbake(app, paa_resultat):
    """FR-15, suksesskriterium 8: samme CV og annonse kjørt to ganger i samme søknad, med
    «Tilbake» imellom, gir samme nøkkelordtreff. Analysen kjøres på nytt."""
    forste = nokkelordtreff(html_av(paa_resultat.get("/resultat")))
    assert paa_resultat.get("/innlegging").status_code == 200
    svar = paa_resultat.post(
        "/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"}
    )
    assert svar.location == "/resultat"
    assert nokkelordtreff(html_av(paa_resultat.get("/resultat"))) == forste
    assert soknaden(app, paa_resultat).steg == Steg.RESULTAT


def test_fr19_endret_cv_via_tilbake_til_modusvalget_nullstiller(app, paa_resultat):
    """FR-19/AD-8: «Tilbake» fra resultatsiden, endret CV og «Tilbake» til modusvalget gir
    steg innlegging uten analyse, og /resultat sender til /innlegging."""
    paa_resultat.get("/innlegging")
    svar = paa_resultat.post(
        "/innlegging", data={"cv": "Ny CV", "annonse": ANNONSE, "handling": "tilbake"}
    )
    assert svar.location == "/modus"
    soknad = soknaden(app, paa_resultat)
    assert soknad.steg == Steg.INNLEGGING
    assert soknad.nokkelord is None
    assert soknad.gap is None
    assert paa_resultat.get("/resultat").location == "/innlegging"


def test_fr14_alle_nye_tekster_ligger_i_tekster_py():
    """FR-14–FR-18/UX-DR13: tekstene på resultatsiden står i web/tekster.py, ordrett fra
    EXPERIENCE."""
    assert tekster.LAGET_AV_KI == "Laget av KI"
    assert tekster.GAP_UNDERTEKST == "Kravene fra annonsen, sammenlignet med CV-en din."
    assert tekster.GAP_INFO_SKJERMLESER == "Hva er en gap-analyse?"
    assert tekster.NOKKELORD_INFO_SKJERMLESER == "Hva er nøkkelordtreff?"
    assert tekster.NOKKELORDTREFF_FORKLARING == "av nøkkelordene står i CV-en din"
    assert tekster.ATS_OVERSKRIFT == "Hva er ATS og hva betyr det for deg?"
    assert tekster.nokkelord_treff_overskrift(7) == "Står i CV-en (7)"
    assert tekster.nokkelord_ikke_treff_overskrift(4) == "Står ikke i CV-en (4)"
    assert tekster.GAP_MANGLER_TOM_IKON == "🎉"


def test_ux_dr11_info_skriptet_lastes_pa_resultatsiden(paa_resultat):
    """UX-DR11: info.js lastes på resultatsiden, ikke på innleggingen."""
    assert "js/info.js" in html_av(paa_resultat.get("/resultat"))
    assert "js/info.js" not in html_av(paa_resultat.get("/innlegging"))


def test_ux_dr11_info_skriptet():
    """UX-DR11/AD-1: info.js lukker med Esc, setter aria-expanded, bruker hover bare med mus,
    åpner ikke ved fokus og sender ingenting til serveren."""
    js = (STIL.parents[1] / "js" / "info.js").read_text(encoding="utf-8")
    assert '"Escape"' in js
    assert '"aria-expanded"' in js
    assert 'pointerType === "mouse"' in js
    assert not re.search(r'addEventListener\("(focus|focusin)"', js)
    for forbudt in ("fetch(", "XMLHttpRequest", ".submit(", "sendBeacon", "location"):
        assert forbudt not in js


def test_nfr7_listene_side_om_side_fra_700_px():
    """NFR-7/UX-DR19: gap-listene og nøkkelordlistene står under hverandre, og side om side
    fra 700 px."""
    css = STIL.read_text(encoding="utf-8")
    bred = re.search(r"@media \(min-width: 700px\)\s*\{\s*\.to-lister\s*\{(.*?)\}", css, re.S)
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in bred.group(1)
    assert "grid-template-columns" not in css_blokk(css, ".to-lister")


def test_ux_dr13_jobbe_videre_med_er_aldri_rod():
    """UX-DR13: «Dette kan du jobbe videre med» er varm fersken, aldri rød."""
    css = STIL.read_text(encoding="utf-8")
    assert "var(--work-on-tint)" in css_blokk(css, ".gap-liste.mangler")
    assert "--error" not in css_blokk(css, ".gap-liste.mangler")


def test_nfr7_lange_ord_brytes_i_listene():
    """NFR-7: et langt ord i en liste brytes i stedet for å gjøre siden bredere på mobil."""
    css = STIL.read_text(encoding="utf-8")
    assert "overflow-wrap: anywhere" in css_blokk(css, ".resultatliste li")


def test_ux_dr13_ats_pila_er_til_hoyre_og_skjult_for_skjermlesere():
    """UX-DR13/UX-DR21: ATS-overskriften har ▾ til høyre i stedet for nettleserens pil, og
    pila er skjult for skjermlesere."""
    css = STIL.read_text(encoding="utf-8")
    assert "list-style: none" in css_blokk(css, ".ats summary")
    assert 'content: "▾" / "";' in css_blokk(css, ".ats summary::after")
    assert "rotate(180deg)" in css_blokk(css, ".ats[open] summary::after")


def test_ux_dr11_trykk_utenfor_lukker_boksen():
    """UX-DR11: info.js lukker boksen ved et trykk utenfor knappen og boksen."""
    js = (STIL.parents[1] / "js" / "info.js").read_text(encoding="utf-8")
    assert "!info.contains(hendelse.target)" in js


def test_ux_dr21_pynteikonene_ligger_i_tekster_py():
    """UX-DR21: pynteikonene i listene står i tekster.py, ikke i malen."""
    assert (tekster.IKON_DEKKER, tekster.IKON_MANGLER) == ("✓", "→")
    assert (tekster.IKON_TREFF, tekster.IKON_IKKE_TREFF) == ("✓", "○")
    mal = (STIL.parents[2] / "templates" / "resultat.html").read_text(encoding="utf-8")
    for ikon in ("✓", "→", "○"):
        assert ikon not in mal
