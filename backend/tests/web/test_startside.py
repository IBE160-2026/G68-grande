"""Tester for startsiden: ny søknad og «Begynn å lage søknad» (FR-5, FR-20, AD-7, AD-8)."""

import re

from soknad.kjerne.okt import Innlogging, Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from tests.web.hjelpere import STIL, okt_id, sett_soknad, soknaden, tagger_i


def test_fr5_startsiden_lager_ny_soknad_og_beholder_innloggingen(app, innlogget_client):
    """FR-5/AD-7: GET / lager alltid en ny søknad på steg start. Innloggingen (og testmodus)
    er den samme, og økt-id-en er den samme."""
    lager = app.extensions["oktlager"]
    gammel_id = okt_id(innlogget_client)
    innlogging = lager.hent(gammel_id)
    sett_soknad(
        app,
        innlogget_client,
        Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, cv=Tekstfelt("cv")),
    )
    assert innlogget_client.get("/").status_code == 200
    assert soknaden(app, innlogget_client) == Soknad()
    assert okt_id(innlogget_client) == gammel_id
    assert lager.hent(gammel_id) == innlogging == Innlogging(innlogging.bruker_id, True)


def test_fr5_begynn_gir_steg_modus_og_redirect_til_modusvalget(app, innlogget_client):
    """FR-5/AD-8: POST / flytter steget til modus og sender videre med redirect."""
    innlogget_client.get("/")
    svar = innlogget_client.post("/")
    assert svar.status_code == 302
    assert svar.location == "/modus"
    assert soknaden(app, innlogget_client) == Soknad(steg=Steg.MODUS)


def test_fr5_begynn_uten_soknad_i_okten(app, innlogget_client):
    """FR-5/AD-7: mangler søknaden i økten (POST / uten GET / først), regnes den som ny."""
    assert soknaden(app, innlogget_client) is None
    svar = innlogget_client.post("/")
    assert svar.location == "/modus"
    assert soknaden(app, innlogget_client) == Soknad(steg=Steg.MODUS)


def test_fr5_begynn_setter_ikke_steget_tilbake(app, innlogget_client):
    """FR-5/AD-8: POST / fra en gammel fane mens søknaden er lenger fram, beholder søknaden."""
    soknad = Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, cv=Tekstfelt("cv"))
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.post("/")
    assert svar.location == "/modus"
    assert soknaden(app, innlogget_client) == soknad


def test_fr5_startsiden_har_knappen_i_et_post_skjema(innlogget_client):
    """FR-5: «Begynn å lage søknad» er den eneste knappen i hovedinnholdet, i et POST-skjema
    mot /, med klassen stor-knapp."""
    html = innlogget_client.get("/").get_data(as_text=True)
    main = re.search(r"<main[^>]*>(.*?)</main>", html, re.S).group(1)
    tagger = tagger_i(main)
    skjemaer = [a for t, a in tagger if t == "form"]
    knapper = [a for t, a in tagger if t == "button"]
    assert skjemaer == [{"class": "begynn", "method": "post", "action": "/"}]
    assert knapper == [{"class": "stor-knapp", "type": "submit"}]
    assert tekster.START_KNAPP == "Begynn å lage søknad"
    assert re.search(r"<button[^>]*>\s*Begynn å lage søknad\s*</button>", main)


def test_fr5_stor_knapp_er_storst_og_hele_bredden_paa_mobil():
    """FR-5/UX-DR4: stor-knapp har 1,5rem og 24px 64px, og under 700 px 1,25rem og hele
    bredden."""
    css = STIL.read_text(encoding="utf-8")
    knapp = re.search(r"^\.stor-knapp\s*\{(.*?)\}", css, re.S | re.M).group(1)
    assert "font-size: var(--size-button-hero)" in knapp
    assert "padding: var(--space-6) calc(2 * var(--space-7))" in knapp
    assert "--size-button-hero: 1.5rem;" in css
    mobil = re.findall(r"@media \(max-width: 699px\)\s*\{(.*?)\n\}", css, re.S)
    blokk = next(m for m in mobil if ".stor-knapp" in m)
    assert "width: 100%" in blokk
    assert "font-size: var(--size-button-hero-mobile)" in blokk
    redusert = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", css, re.S)
    assert ".stor-knapp:hover" in redusert.group(1)
