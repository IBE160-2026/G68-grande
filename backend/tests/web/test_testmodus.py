"""Tester for bryteren «Testmodus» på startsiden, teksten om testmodus og merkelappen
«Testmodus» på de andre sidene (FR-32, FR-33, UX-DR9)."""

import re

import pytest

from soknad.kjerne.okt import Modus, Soknad
from soknad.kjerne.steg import Steg
from soknad.web import ruter, tekster
from tests.web.hjelpere import (
    STIL,
    app_med_nokkel,
    css_blokk,
    header,
    logg_inn,
    main,
    med_autofocus,
    okt_id,
    sett_soknad,
    sett_testmodus,
    soknaden,
    tagger_i,
)


def bryter(html):
    """Attributtene til bryteren (role="switch"), eller None."""
    return next((a for t, a in tagger_i(html) if a.get("role") == "switch"), None)


def merkelapper(html):
    return [a for _, a in tagger_i(html) if a.get("class") == "merkelapp"]


def innlogget_med_nokkel(nokkel):
    """En innlogget klient i en app der ANTHROPIC_API_KEY er satt til nokkel."""
    app = app_med_nokkel(nokkel)
    client = app.test_client()
    assert logg_inn(client).status_code == 302
    return client


# --- Matrisen ---


def test_fr32_uten_nokkel_er_bryteren_paa_og_last_med_nokkeltekst(innlogget_client):
    """FR-32: uten API-nøkkel er bryteren på og låst, og «Mangler API-nøkkel, se README» står
    under, koblet med aria-describedby. Teksten om testmodus står i statusområdet."""
    html = innlogget_client.get("/").get_data(as_text=True)
    topp = header(html)
    assert bryter(topp) == {
        "class": "bryter",
        "type": "button",
        "role": "switch",
        "aria-checked": "true",
        "aria-disabled": "true",
        "aria-describedby": "nokkeltekst",
    }
    nokkeltekst = r'<p class="nokkeltekst" id="nokkeltekst">\s*Mangler API-nøkkel, se README'
    assert re.search(nokkeltekst, topp)
    assert tekster.TESTMODUS_STATUS in main(html)


def test_fr32_med_nokkel_er_bryteren_av_og_i_et_eget_skjema():
    """FR-32: med API-nøkkel er testmodus av etter innlogging. Bryteren er ikke låst, står i et
    eget POST-skjema mot /testmodus og sender testmodus=paa. Ingen nøkkeltekst, og
    statusområdet er tomt."""
    html = innlogget_med_nokkel("sk-test").get("/").get_data(as_text=True)
    topp = header(html)
    assert bryter(topp) == {
        "class": "bryter",
        "type": "submit",
        "role": "switch",
        "name": "testmodus",
        "value": "paa",
        "aria-checked": "false",
    }
    skjemaer = [a for t, a in tagger_i(topp) if t == "form"]
    assert skjemaer == [{"class": "bryter-skjema", "method": "post", "action": "/testmodus"}]
    assert re.search(r'<form class="bryter-skjema"[^>]*>\s*<button class="bryter"', topp)
    assert tekster.MANGLER_NOKKEL not in html
    assert 'id="nokkeltekst"' not in html
    assert '<p class="testinfo" role="status"></p>' in main(html)


def test_fr32_nokkel_med_bare_mellomrom_regnes_som_mangler():
    """FR-32: en nøkkel med bare mellomrom gir det samme som ingen nøkkel."""
    html = innlogget_med_nokkel("   ").get("/").get_data(as_text=True)
    assert bryter(header(html))["aria-describedby"] == "nokkeltekst"
    assert tekster.MANGLER_NOKKEL in header(html)


@pytest.mark.parametrize("side", ["/modus", "/innlegging"])
def test_fr33_merkelappen_paa_sidene_etter_startsiden(innlogget_client, side):
    """FR-33: modusvalget og innleggingen har merkelappen «Testmodus» i header, og ingen
    bryter."""
    innlogget_client.get("/")
    innlogget_client.post("/")
    if side == "/innlegging":
        innlogget_client.post("/modus", data={"modus": "full_generering"})
    html = innlogget_client.get(side).get_data(as_text=True)
    topp = header(html)
    assert merkelapper(topp) == [{"class": "merkelapp"}]
    assert re.search(r'<span class="merkelapp">\s*Testmodus\s*</span>', topp)
    assert bryter(html) is None
    assert tekster.MANGLER_NOKKEL not in html


def test_fr33_ingen_merkelapp_paa_startsiden(innlogget_client):
    """FR-33: startsiden har bryteren, ikke merkelappen."""
    html = innlogget_client.get("/").get_data(as_text=True)
    assert merkelapper(html) == []
    assert bryter(html) is not None


@pytest.mark.parametrize("side", ["/logg-inn", "/registrer"])
def test_fr32_fr33_utlogget_har_verken_bryter_merkelapp_eller_statustekst(client, side):
    """FR-32/FR-33: innloggingen og registreringen har ingen bryter, merkelapp eller
    tekst om testmodus."""
    html = client.get(side).get_data(as_text=True)
    assert bryter(html) is None
    assert merkelapper(html) == []
    assert 'class="topplinje"' not in html
    assert tekster.TESTMODUS_STATUS not in html


# --- Resten ---


def test_fr32_last_bryter_star_ikke_i_et_skjema(innlogget_client):
    """FR-32: uten nøkkel står bryteren i header, utenfor alle skjemaer, så et trykk sender
    ingenting. Etiketten «Testmodus» står inne i knappen, og sporet er skjult for skjermlesere."""
    topp = header(innlogget_client.get("/").get_data(as_text=True))
    assert "<form" not in topp
    knapp = re.search(r'<button class="bryter"[^>]*>(.*?)</button>', topp, re.S).group(1)
    assert re.search(r'<span class="spor" aria-hidden="true"></span>\s*Testmodus\s*$', knapp)


def test_fr32_statusomradet_har_role_status_mellom_ingressen_og_knappen(innlogget_client):
    """FR-32/UX-DR9: teksten om testmodus står i et role="status"-område mellom ingressen
    og «Begynn å lage søknad»."""
    innhold = main(innlogget_client.get("/").get_data(as_text=True))
    assert tekster.TESTMODUS_STATUS == (
        "Du er i testmodus. Nettsiden bruker ferdige svar, og ingenting sendes til ekstern KI."
    )
    status = re.search(r'<p class="testinfo" role="status">(.*?)</p>', innhold, re.S)
    assert status.group(1) == tekster.TESTMODUS_STATUS
    assert innhold.index('class="ingress"') < status.start() < innhold.index('class="begynn"')


def test_fr32_fr33_testmodus_av_gir_tom_status_og_ingen_merkelapp(app, innlogget_client):
    """FR-32/FR-33: er testmodus av i innloggingen, er bryteren av, statusområdet tomt og
    merkelappen borte. Appen har ingen nøkkel, så innloggingen byttes med sett_testmodus."""
    sett_testmodus(app, innlogget_client, False)
    html = innlogget_client.get("/").get_data(as_text=True)
    assert bryter(html)["aria-checked"] == "false"
    assert '<p class="testinfo" role="status"></p>' in html
    innlogget_client.post("/", data={"samtykke": "ja"})
    svar = innlogget_client.get("/modus")
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    assert 'class="topplinje"' in html
    assert merkelapper(html) == []


def test_fr32_last_bryter_har_blekt_spor_og_44_x_24():
    """FR-32/UX-DR9: sporet er 44 × 24 px, i primary når bryteren er på, og 60 % synlig når
    den er låst. Etiketten blekes ikke og har text-farge og vekt 600."""
    css = STIL.read_text(encoding="utf-8")
    spor = css_blokk(css, ".bryter .spor")
    assert "width: 44px" in spor
    assert "aspect-ratio: 44 / 24" in spor
    assert "var(--primary)" in css_blokk(css, '.bryter[aria-checked="true"] .spor')
    assert "opacity: 0.6" in css_blokk(css, '.bryter[aria-disabled="true"] .spor')
    etikett = css_blokk(css, ".bryter")
    assert "color: var(--text)" in etikett
    assert "font-weight: 600" in etikett
    last = css_blokk(css, '.bryter[aria-disabled="true"]')
    assert "opacity" not in etikett + last
    assert "color" not in last


def test_fr32_bryteren_synes_i_hoykontrastmodus():
    """FR-32/NFR-6: i høykontrastmodus (forced-colors) fjernes bakgrunn og skygge, så sporet
    får en ramme og knotten en systemfarge."""
    css = STIL.read_text(encoding="utf-8")
    hoykontrast = re.search(r"@media \(forced-colors: active\)\s*\{(.*?)\n\}", css, re.S).group(1)
    assert "border: 1px solid CanvasText" in hoykontrast
    assert "background: CanvasText" in hoykontrast


def test_fr32_fr33_raden_oppe_til_hoyre_og_nokkelteksten_under():
    """FR-32/FR-33: raden står til høyre og brytes, og nøkkelteksten står på egen linje under
    bryteren, høyrestilt og i liten, dempet skrift. Raden står før logoen i header."""
    css = STIL.read_text(encoding="utf-8")
    rad = css_blokk(css, ".topplinje")
    assert "justify-content: flex-end" in rad
    assert "flex-wrap: wrap" in rad
    nokkel = css_blokk(css, ".nokkeltekst")
    for verdi in ("flex-basis: 100%", "var(--size-caption)", "var(--text-muted)", "right"):
        assert verdi in nokkel


def test_fr33_raden_star_for_logoen(innlogget_client):
    """FR-33: raden med bryteren eller merkelappen står før logoen i header (oppe til høyre)."""
    topp = header(innlogget_client.get("/").get_data(as_text=True))
    assert topp.index('class="topplinje"') < topp.index('class="logo"')


def test_fr33_merkelappen_er_fersken_uten_nowrap():
    """FR-33/UX-DR9: merkelappen har accent-bakgrunn, text-farge, rounded-sm, size-tag og
    vekt 600. Ingen nowrap og ingen fast høyde."""
    css = STIL.read_text(encoding="utf-8")
    merkelapp = css_blokk(css, ".merkelapp")
    for verdi in (
        "var(--accent)",
        "var(--text)",
        "var(--rounded-sm)",
        "var(--size-tag)",
        "font-weight: 600",
    ):
        assert verdi in merkelapp
    assert "height" not in merkelapp
    assert "nowrap" not in css


# --- Bryteren slås av og på (story 4.3.1) ---


@pytest.fixture
def med_nokkel():
    """(app, klient): innlogget i en app med API-nøkkel, så testmodus er av."""
    app = app_med_nokkel()
    client = app.test_client()
    assert logg_inn(client).status_code == 302
    return app, client


def innlogging(app, client):
    return app.extensions["oktlager"].hent(okt_id(client))


def test_fr32_slaa_paa_og_av_med_nokkel_gir_startsiden_med_fokus_paa_bryteren(med_nokkel):
    """FR-32: med nøkkel på steg start slår POST /testmodus testmodus på og av igjen, på samme
    økt-id. Brukeren sendes til startsiden med ?bryter=1, og der har bryteren autofocus."""
    app, client = med_nokkel
    id_ = okt_id(client)
    client.get("/")
    svar = client.post("/testmodus", data={"testmodus": "paa"})
    assert svar.status_code == 302
    assert svar.location == "/?bryter=1"
    assert innlogging(app, client).testmodus is True
    assert okt_id(client) == id_
    html = client.get(svar.location).get_data(as_text=True)
    attributter = bryter(header(html))
    assert attributter["aria-checked"] == "true"
    assert attributter["value"] == "av"
    assert "autofocus" in attributter
    assert tekster.TESTMODUS_STATUS in main(html)

    svar = client.post("/testmodus", data={"testmodus": "av"})
    assert svar.location == "/?bryter=1"
    assert innlogging(app, client).testmodus is False
    html = client.get(svar.location).get_data(as_text=True)
    assert bryter(header(html))["aria-checked"] == "false"
    assert 'id="samtykke"' in main(html)


def test_fr32_bryteren_har_ikke_fokus_uten_bryter_i_adressen(med_nokkel):
    """FR-32: vanlig GET / gir ikke bryteren fokus."""
    _, client = med_nokkel
    html = client.get("/").get_data(as_text=True)
    assert med_autofocus(html) == []


def test_fr32_uten_nokkel_endrer_post_ingenting(app, innlogget_client):
    """FR-32: uten nøkkel er testmodus fortsatt på etter POST /testmodus."""
    innlogget_client.get("/")
    svar = innlogget_client.post("/testmodus", data={"testmodus": "av"})
    assert svar.status_code == 302
    assert innlogging(app, innlogget_client).testmodus is True


def test_fr32_nokkel_med_bare_mellomrom_endrer_ingenting():
    """FR-32: en nøkkel med bare mellomrom er ingen nøkkel. Testmodus er på etter innlogging,
    og POST /testmodus endrer ingenting. Det finnes ingen ekte KI."""
    app = app_med_nokkel("   ")
    client = app.test_client()
    logg_inn(client)
    assert app.extensions["ekte_ki"] is None
    client.get("/")
    client.post("/testmodus", data={"testmodus": "av"})
    assert innlogging(app, client).testmodus is True


def test_fr32_ukjent_verdi_endrer_ingenting(med_nokkel):
    """FR-32: uten testmodus=av eller testmodus=paa er testmodus uendret."""
    app, client = med_nokkel
    client.get("/")
    for data in ({}, {"testmodus": "ja"}):
        assert client.post("/testmodus", data=data).location == "/?bryter=1"
        assert innlogging(app, client).testmodus is False


@pytest.mark.parametrize(
    ("soknad", "side"),
    [
        (Soknad(steg=Steg.MODUS), "/modus"),
        (Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING), "/innlegging"),
        (Soknad(steg=Steg.RESULTAT, modus=Modus.FULL_GENERERING), "/resultat"),
        (Soknad(steg=Steg.BREV, modus=Modus.FULL_GENERERING), "/brev"),
        (Soknad(opptatt=True), "/"),
    ],
    ids=["modus", "innlegging", "resultat", "brev", "opptatt"],
)
def test_fr32_bryteren_endres_ikke_etter_startsiden(med_nokkel, soknad, side):
    """FR-32/AD-8: er søknaden forbi steg start, eller opptatt, sendes brukeren til siden for
    steget, og testmodus og søknaden er uendret."""
    app, client = med_nokkel
    sett_soknad(app, client, soknad)
    svar = client.post("/testmodus", data={"testmodus": "paa"})
    assert svar.status_code == 302
    assert svar.location == side
    assert innlogging(app, client).testmodus is False
    assert soknaden(app, client) == soknad


def test_fr32_slaa_av_beholder_soknaden_paa_steg_start(med_nokkel):
    """FR-32: bryteren bytter bare innloggingen. Søknaden på steg start er den samme."""
    app, client = med_nokkel
    client.get("/")
    soknad = soknaden(app, client)
    client.post("/testmodus", data={"testmodus": "paa"})
    assert soknaden(app, client) is soknad


def test_fr32_bryteren_av_og_paa_synes_i_hoykontrastmodus():
    """FR-32/NFR-6: i høykontrastmodus skilles av og på også med farge: sporet er Canvas når
    bryteren er av, og Highlight når den er på."""
    css = STIL.read_text(encoding="utf-8")
    hoykontrast = re.search(r"@media \(forced-colors: active\)\s*\{(.*?)\n\}", css, re.S).group(1)
    assert re.search(
        r'\.bryter\[aria-checked="false"\] \.spor \{\s*background: Canvas;', hoykontrast
    )
    assert re.search(
        r'\.bryter\[aria-checked="true"\] \.spor \{\s*background: Highlight;', hoykontrast
    )
    assert "forced-color-adjust: none" in hoykontrast


def test_fr7_utlogget_for_bryteren_gir_innloggingen(med_nokkel, monkeypatch):
    """FR-7/AD-8: logges brukeren ut i en annen fane etter login_required, men før bryteren
    henter innloggingen, sendes hen til innloggingen med «Du må logge inn først». Ingen
    feilside, og ingen innlogging kommer tilbake."""
    app, client = med_nokkel
    lager = app.extensions["oktlager"]
    id_ = okt_id(client)
    ekte_hent = ruter.gjeldende_soknad

    def hent_og_logg_ut():
        soknad = ekte_hent()
        lager.slett(id_)
        return soknad

    monkeypatch.setattr(ruter, "gjeldende_soknad", hent_og_logg_ut)
    svar = client.post("/testmodus", data={"testmodus": "paa"})
    assert svar.status_code == 302
    assert svar.location == "/logg-inn?ikke_innlogget=1"
    assert okt_id(client) is None
    assert lager.hent(id_) is None
