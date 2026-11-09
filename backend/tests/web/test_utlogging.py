"""Tester for utloggingen, hjørneraden og «Du må logge inn først» (FR-6, FR-7, NFR-6, NFR-7)."""

import re

from soknad.web import tekster
from tests.web.hjelpere import STIL, er_innlogget, logg_inn, med_autofocus, okt_id, tagger_i


def footer(html):
    return re.search(r"<footer[^>]*>(.*?)</footer>", html, re.S).group(1)


def css_blokk(css, velger):
    """Innholdet i den første regelen øverst i fila (ikke i @media) med akkurat denne velgeren."""
    return re.search(rf"^{re.escape(velger)}\s*\{{(.*?)\}}", css, re.S | re.M).group(1)


# --- Logge ut ---


def test_fr6_logg_ut_sletter_okten_og_sender_til_innloggingen(app, innlogget_client):
    """FR-6: POST /logg-ut gir 302 til /logg-inn, økten er borte og okt_id er ute av cookien."""
    gammel = okt_id(innlogget_client)
    assert app.extensions["oktlager"].hent(gammel) is not None
    svar = innlogget_client.post("/logg-ut")
    assert svar.status_code == 302
    assert svar.location == "/logg-inn"
    assert app.extensions["oktlager"].hent(gammel) is None
    assert okt_id(innlogget_client) is None


def test_fr6_logg_ut_sletter_ogsaa_soknaden(app, innlogget_client):
    """FR-6/AD-7: utloggingen sletter søknaden, og etter ny innlogging er det ingen søknad."""
    innlogget_client.post("/")
    gammel = okt_id(innlogget_client)
    assert app.extensions["oktlager"].hent_soknad(gammel) is not None
    innlogget_client.post("/logg-ut")
    assert app.extensions["oktlager"].hent_soknad(gammel) is None
    logg_inn(innlogget_client)
    assert app.extensions["oktlager"].hent_soknad(okt_id(innlogget_client)) is None
    assert innlogget_client.get("/modus").location == "/"


def test_fr6_etter_utlogging_kreves_innlogging_igjen(innlogget_client):
    """FR-6/FR-7: etter utlogging gir GET / 302 til /logg-inn?ikke_innlogget=1."""
    innlogget_client.post("/logg-ut")
    svar = innlogget_client.get("/")
    assert svar.status_code == 302
    assert svar.location == "/logg-inn?ikke_innlogget=1"


def test_fr6_ingen_melding_etter_utlogging(innlogget_client):
    """FR-6: innloggingen etter utlogging har ingen skjemafeil-boks og ingen hjørnerad."""
    svar = innlogget_client.post("/logg-ut", follow_redirects=True)
    html = svar.get_data(as_text=True)
    assert svar.status_code == 200
    assert "skjemafeil" not in html
    assert tekster.MA_LOGGE_INN not in html
    assert "<form" not in footer(html)


def test_fr6_ny_innlogging_etter_utlogging_gir_startsiden_og_ny_okt_id(innlogget_client):
    """FR-6: logger man inn igjen etter utlogging, kommer man til startsiden med ny økt-id."""
    gammel = okt_id(innlogget_client)
    innlogget_client.post("/logg-ut")
    svar = logg_inn(innlogget_client)
    assert svar.location == "/"
    assert okt_id(innlogget_client) not in (None, gammel)
    assert er_innlogget(innlogget_client)


def test_fr6_logg_ut_uten_okt_sender_til_innloggingen(client):
    """FR-6/FR-7: POST /logg-ut uten innlogging gir 302 til /logg-inn?ikke_innlogget=1."""
    svar = client.post("/logg-ut")
    assert svar.status_code == 302
    assert svar.location == "/logg-inn?ikke_innlogget=1"


def test_fr6_get_logg_ut_gir_405(app, innlogget_client):
    """FR-6: utloggingen er bare POST. GET /logg-ut gir 405, også når man er innlogget."""
    assert app.test_client().get("/logg-ut").status_code == 405
    assert innlogget_client.get("/logg-ut").status_code == 405
    assert er_innlogget(innlogget_client)


# --- Hjørneraden ---


def test_fr6_hjornerad_med_logg_ut_etter_innlogging(innlogget_client):
    """FR-6: footer har skjemaet med method="post" mot /logg-ut og én knapp «Logg ut»."""
    html = innlogget_client.get("/").get_data(as_text=True)
    rad = footer(html)
    tagger = tagger_i(rad)
    skjemaer = [a for t, a in tagger if t == "form"]
    knapper = [a for t, a in tagger if t == "button"]
    assert len(skjemaer) == 1
    assert skjemaer[0]["method"] == "post"
    assert skjemaer[0]["action"] == "/logg-ut"
    assert len(knapper) == 1
    assert knapper[0]["type"] == "submit"
    assert "sekundaerknapp" in knapper[0]["class"].split()
    assert re.search(r"<button[^>]*>\s*Logg ut\s*</button>", rad)
    assert html.count(tekster.LOGG_UT_KNAPP) == 1
    assert re.search(r'<footer class="bunn hjornerad"', html)
    assert "<script" not in rad


def test_fr6_ingen_hjornerad_uten_innlogging(client):
    """FR-6: innloggingen og registreringen uten innlogging har ingen hjørnerad."""
    for side in ("/logg-inn", "/registrer"):
        html = client.get(side).get_data(as_text=True)
        assert "<form" not in footer(html), side
        assert "hjornerad" not in html, side
        assert tekster.LOGG_UT_KNAPP not in footer(html), side


# --- Du må logge inn først ---


def test_fr7_ikke_innlogget_gir_meldingen_med_fokus(client):
    """FR-7: GET / uten cookie sender til innloggingen, som viser «Du må logge inn først»
    i skjemafeil-boksen med autofocus."""
    svar = client.get("/")
    assert svar.location == "/logg-inn?ikke_innlogget=1"
    html = client.get(svar.location).get_data(as_text=True)
    boks = next(a for _, a in tagger_i(html) if a.get("id") == "skjemafeil")
    assert boks["tabindex"] == "-1"
    assert "autofocus" in boks
    assert re.search(r'id="skjemafeil"[^>]*>\s*Du må logge inn først\s*<', html)
    assert med_autofocus(html) == ["skjemafeil"]
    assert "aria-invalid" not in html


def test_fr7_meldingen_ligger_i_tekster():
    """FR-6/FR-7: tekstene ligger i web/tekster.py."""
    assert tekster.MA_LOGGE_INN == "Du må logge inn først"
    assert tekster.LOGG_UT_KNAPP == "Logg ut"


def test_fr7_gammel_cookie_gir_meldingen_og_tommes(app, innlogget_client):
    """FR-7: etter omstart (økten ikke i minnet) er det som ikke innlogget, og cookien tømmes."""
    app.extensions["oktlager"].slett(okt_id(innlogget_client))
    svar = innlogget_client.get("/")
    assert svar.location == "/logg-inn?ikke_innlogget=1"
    assert okt_id(innlogget_client) is None


def test_fr7_feil_innlogging_fra_meldingssiden_gir_bare_feil_innlogging(client):
    """FR-7: feil passord fra siden med meldingen gir bare «Feil e-post eller passord»."""
    html = client.get("/logg-inn?ikke_innlogget=1").get_data(as_text=True)
    skjema = next(a for t, a in tagger_i(html) if t == "form")
    assert skjema["action"] == "/logg-inn"
    for adresse in ("/logg-inn", "/logg-inn?ikke_innlogget=1"):
        svar = client.post(adresse, data={"epost": "test@example.com", "passord": "feilpassord"})
        html = svar.get_data(as_text=True)
        assert "Feil e-post eller passord" in html
        assert tekster.MA_LOGGE_INN not in html


def test_fr7_innlogging_fra_meldingssiden_gir_startsiden(client):
    """FR-7: innlogging etter meldingen gir startsiden (next= brukes ikke)."""
    client.get("/")
    svar = logg_inn(client)
    assert svar.location == "/"


def test_fr7_ingen_melding_naar_man_alt_er_innlogget(innlogget_client):
    """FR-7: tilbake til /logg-inn?ikke_innlogget=1 etter innlogging gir startsiden
    i stedet for meldingen."""
    svar = innlogget_client.get("/logg-inn?ikke_innlogget=1")
    assert svar.status_code == 302
    assert svar.location == "/"
    assert er_innlogget(innlogget_client)


def test_fr7_bare_ikke_innlogget_1_gir_meldingen(client):
    """FR-7: ?ikke_innlogget=0 eller tom verdi gir ingen melding."""
    for adresse in ("/logg-inn?ikke_innlogget=0", "/logg-inn?ikke_innlogget="):
        html = client.get(adresse).get_data(as_text=True)
        assert tekster.MA_LOGGE_INN not in html, adresse


def test_fr7_gammel_cookie_gir_ingen_hjornerad_paa_aapne_sider(app, client):
    """FR-7: cookie med økt-id som ikke finnes i minnet gir ingen hjørnerad."""
    logg_inn(client)
    app.extensions["oktlager"].slett(okt_id(client))
    for side in ("/logg-inn", "/registrer"):
        svar = client.get(side)
        assert svar.status_code == 200, side
        html = svar.get_data(as_text=True)
        assert "hjornerad" not in html, side
        assert "<form" not in footer(html), side


def test_fr7_vanlig_innlogging_har_ingen_melding(client):
    """FR-7: GET /logg-inn uten ikke_innlogget har ingen skjemafeil-boks og ingen hjørnerad."""
    html = client.get("/logg-inn").get_data(as_text=True)
    assert "skjemafeil" not in html
    assert tekster.MA_LOGGE_INN not in html
    assert "<form" not in footer(html)


# --- Tilbakeknappen ---


def test_fr6_sider_med_innlogging_lagres_ikke_i_nettleseren(innlogget_client):
    """FR-6: sider med login_required har Cache-Control: no-store."""
    svar = innlogget_client.get("/")
    assert svar.status_code == 200
    assert svar.headers["Cache-Control"] == "no-store"


def test_fr6_skriptet_for_tilbakeknappen_bare_etter_innlogging(app, innlogget_client):
    """FR-6: sidene etter innlogging har tilbake.js, som laster siden på nytt når
    nettleseren viser den fra minnet. Innloggingen og registreringen har det ikke."""
    html = innlogget_client.get("/").get_data(as_text=True)
    assert '<script src="/static/js/tilbake.js" defer></script>' in html
    utlogget = app.test_client()
    for side in ("/logg-inn", "/registrer"):
        assert "tilbake.js" not in utlogget.get(side).get_data(as_text=True), side
    skript = innlogget_client.get("/static/js/tilbake.js")
    assert skript.status_code == 200
    tekst = skript.get_data(as_text=True)
    assert re.search(r'addEventListener\("pageshow",\s*function\s*\(\s*hendelse\s*\)', tekst)
    # Siden lastes på nytt bare når hendelse.persisted er sann (ellers en evig løkke).
    assert re.search(
        r"if\s*\(\s*hendelse\.persisted\s*\)\s*\{\s*window\.location\.reload\(\);\s*\}", tekst
    )
    assert tekst.count("location.reload()") == 1


# --- Stilen ---


def test_nfr7_hjornerad_er_festet_nederst_og_dekker_ikke_innhold():
    """NFR-6/NFR-7: raden er sticky nederst, html har scroll-padding-bottom, og under
    500 px skjermhøyde står raden nederst på siden i stedet."""
    css = STIL.read_text(encoding="utf-8")
    rad = css_blokk(css, ".hjornerad")
    assert "position: sticky" in rad
    assert "bottom: 0" in rad
    assert "background: var(--background)" in rad
    assert "border-top: 1px solid var(--border)" in rad
    assert re.search(r"scroll-padding-bottom:\s*[\d.]+rem", css_blokk(css, "html"))
    lav = re.search(r"@media \(max-height: 500px\)\s*\{(.*?)\n\}", css, re.S).group(1)
    assert re.search(r"\.hjornerad\s*\{[^}]*position: static", lav)
    assert re.search(r"html\s*\{[^}]*scroll-padding-bottom: 0", lav)


def test_nfr7_sekundaerknappen_har_tokens_og_redusert_bevegelse():
    """NFR-6/NFR-7: sekundærknappen er hvit med primary, har hover og trykk, og står i
    prefers-reduced-motion-blokken."""
    css = STIL.read_text(encoding="utf-8")
    knapp = css_blokk(css, ".sekundaerknapp")
    assert "background: var(--surface)" in knapp
    assert "color: var(--primary)" in knapp
    assert "border: 2px solid var(--primary)" in knapp
    assert "border-radius: var(--rounded-lg)" in knapp
    assert "translateY(-2px)" in css_blokk(css, ".sekundaerknapp:hover")
    assert "scale(0.96)" in css_blokk(css, ".sekundaerknapp:active")
    redusert = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", css, re.S)
    assert ".sekundaerknapp:hover" in redusert.group(1)
    assert ".sekundaerknapp:active" in redusert.group(1)
