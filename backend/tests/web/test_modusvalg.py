"""Tester for modusvalget, innleggingssiden og stegsjekken (FR-20, AD-8, UX-DR4, UX-DR12)."""

import re

import pytest

from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from soknad.web.flyt import SIDE_FOR_STEG
from tests.web.hjelpere import STIL, sett_soknad, soknaden, tagger_i


@pytest.fixture
def paa_modus(app, innlogget_client):
    """En innlogget klient som har trykket «Begynn å lage søknad»."""
    innlogget_client.get("/")
    innlogget_client.post("/")
    assert soknaden(app, innlogget_client).steg == Steg.MODUS
    return innlogget_client


def main(html):
    return re.search(r"<main[^>]*>(.*?)</main>", html, re.S).group(1)


# --- Matrisen ---


def test_fr20_velg_modus_gir_steg_innlegging_og_redirect(app, paa_modus):
    """FR-20/AD-8: POST /modus med full_generering lagrer modusen, flytter steget til
    innlegging og sender videre med redirect."""
    svar = paa_modus.post("/modus", data={"modus": "full_generering"})
    assert svar.status_code == 302
    assert svar.location == "/innlegging"
    assert soknaden(app, paa_modus) == Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING)
    assert paa_modus.get("/innlegging").status_code == 200


@pytest.mark.parametrize("side", ["/modus", "/innlegging"])
def test_fr20_kan_ikke_hoppe_over_steg_med_adresselinjen(app, innlogget_client, side):
    """FR-20/AD-8: på steg start sender GET /modus og /innlegging til startsiden."""
    innlogget_client.get("/")
    svar = innlogget_client.get(side)
    assert svar.status_code == 302
    assert svar.location == "/"
    assert soknaden(app, innlogget_client) == Soknad()


def test_fr20_rett_etter_innlogging_uten_soknad_sendes_til_startsiden(app, innlogget_client):
    """FR-20/AD-8: uten søknad i økten er man på steg start."""
    assert soknaden(app, innlogget_client) is None
    assert innlogget_client.get("/innlegging").location == "/"
    assert innlogget_client.get("/modus").location == "/"


def test_fr20_innlegging_fra_modusvalget_sender_til_modusvalget(paa_modus):
    """FR-20/AD-8: på steg modus sender GET /innlegging til modusvalget."""
    svar = paa_modus.get("/innlegging")
    assert svar.status_code == 302
    assert svar.location == "/modus"


def test_fr20_post_for_tidlig_endrer_ingenting(app, innlogget_client):
    """FR-20/AD-8: POST /modus på steg start sender til startsiden, og søknaden er uendret."""
    innlogget_client.get("/")
    svar = innlogget_client.post("/modus", data={"modus": "full_generering"})
    assert svar.status_code == 302
    assert svar.location == "/"
    assert soknaden(app, innlogget_client) == Soknad()


@pytest.mark.parametrize("data", [{"modus": "tull"}, {"modus": ""}, {}])
def test_fr20_ukjent_modus_gir_samme_side_med_400(app, paa_modus, data):
    """FR-20/AD-8: ukjent eller manglende modus gir modusvalget på nytt uten redirect,
    status 400, og søknaden er uendret."""
    svar = paa_modus.post("/modus", data=data)
    assert svar.status_code == 400
    assert tekster.MODUS_OVERSKRIFT in svar.get_data(as_text=True)
    assert soknaden(app, paa_modus) == Soknad(steg=Steg.MODUS)


# --- Mer om stegene ---


def test_fr20_tidligere_sider_kan_vises_uten_at_steget_endres(app, innlogget_client):
    """FR-20/AD-8: på steg innlegging kan modusvalget vises, og steget er uendret."""
    soknad = Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, cv=Tekstfelt("cv"))
    sett_soknad(app, innlogget_client, soknad)
    assert innlogget_client.get("/modus").status_code == 200
    assert innlogget_client.get("/innlegging").status_code == 200
    assert soknaden(app, innlogget_client) == soknad


def test_fr20_velge_modus_paa_nytt_beholder_tekstene(app, innlogget_client):
    """FR-20/AD-8: velger man modus igjen fra innleggingen, beholdes CV og annonse."""
    soknad = Soknad(
        steg=Steg.INNLEGGING,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt("cv"),
        annonse=Tekstfelt("annonse"),
    )
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.post("/modus", data={"modus": "full_generering"})
    assert svar.location == "/innlegging"
    assert soknaden(app, innlogget_client) == soknad


def test_fr20_hele_flyten_fra_startsiden(innlogget_client):
    """FR-5/FR-20: startsiden → modusvalget → innleggingen med redirect hele veien."""
    svar = innlogget_client.post("/", follow_redirects=True)
    assert svar.request.path == "/modus"
    svar = innlogget_client.post("/modus", data={"modus": "full_generering"}, follow_redirects=True)
    assert svar.request.path == "/innlegging"
    assert svar.status_code == 200


def test_fr20_hvert_steg_som_kan_naas_har_en_side(app):
    """AD-8: stegene som kan nås i denne storyen, har en side, og sidene finnes."""
    assert set(SIDE_FOR_STEG) == {Steg.START, Steg.MODUS, Steg.INNLEGGING}
    endepunkter = {regel.endpoint for regel in app.url_map.iter_rules()}
    assert set(SIDE_FOR_STEG.values()) <= endepunkter


def test_fr6_sidene_lagres_ikke_i_nettleseren(paa_modus):
    """FR-6/AD-8: modusvalget og innleggingen har Cache-Control: no-store."""
    assert paa_modus.get("/modus").headers["Cache-Control"] == "no-store"
    paa_modus.post("/modus", data={"modus": "full_generering"})
    assert paa_modus.get("/innlegging").headers["Cache-Control"] == "no-store"


# --- Modusvalget ---


def test_fr20_modusvalget_har_overskrift_og_tittel(paa_modus):
    """FR-20/NFR-6: h1 «Hva vil du gjøre i dag?» og egen sidetittel."""
    html = paa_modus.get("/modus").get_data(as_text=True)
    assert re.search(r"<h1[^>]*>\s*Hva vil du gjøre i dag\?\s*</h1>", html)
    assert "<title>Velg modus – Søknadsassistenten</title>" in html
    assert [t for t, _ in tagger_i(html)].count("h1") == 1


def test_fr20_kortet_full_generering_er_en_knapp(paa_modus):
    """FR-20/UX-DR12: kortet er én submit-knapp med modus=full_generering, med ikon (skjult
    for skjermlesere), modusnavn, handling og forklaring. Ingen egen «Velg»-knapp."""
    html = main(paa_modus.get("/modus").get_data(as_text=True))
    tagger = tagger_i(html)
    skjema = next(a for t, a in tagger if t == "form")
    assert skjema["method"] == "post"
    assert skjema["action"] == "/modus"
    knapper = [a for t, a in tagger if t == "button"]
    assert knapper == [
        {"class": "modus-kort", "type": "submit", "name": "modus", "value": "full_generering"}
    ]
    kort = re.search(r'<button class="modus-kort"[^>]*>(.*?)</button>', html, re.S).group(1)
    assert re.search(r'<span class="ikon" aria-hidden="true">✨</span>', kort)
    assert re.search(r'<span class="navn">Full generering</span>', kort)
    assert re.search(r'<span class="handling">Skriv nytt brev</span>', kort)
    assert re.search(
        r'<span class="forklaring">Du legger inn CV-en og annonsen, så skriver vi et brev '
        r"til deg\.</span>",
        kort,
    )


def test_fr20_hver_modus_har_et_kort_med_tekst():
    """FR-20: hver modus i kjernen har et kort i web/tekster.py, så ingen modus mangler tekst."""
    assert set(tekster.MODUS_KORT) == set(Modus)
    for kort in tekster.MODUS_KORT.values():
        assert all(kort)


def test_fr20_tilbake_er_en_lenke_til_startsiden(paa_modus):
    """FR-20/UX-DR4: «Tilbake» er en sekundærknapp-lenke til / i knapperaden, etter kortene."""
    html = main(paa_modus.get("/modus").get_data(as_text=True))
    lenker = [a for t, a in tagger_i(html) if t == "a"]
    assert lenker == [{"class": "sekundaerknapp", "href": "/"}]
    assert re.search(r'<div class="knapperad">\s*<a[^>]*>Tilbake</a>\s*</div>', html)
    assert html.index("modus-kort") < html.index("knapperad")


def test_fr20_modus_kortene_har_tokens_og_bruddpunkt():
    """FR-20/UX-DR12: kortet er hvitt med ramme, løfter seg 4 px ved hover og krymper til 97 %
    ved trykk. Fra 700 px står kortene side om side. Knapperaden sentrerer ikke, så «Tilbake»
    står til venstre."""
    css = STIL.read_text(encoding="utf-8")

    def blokk(velger):
        return re.search(rf"^{re.escape(velger)}\s*\{{(.*?)\}}", css, re.S | re.M).group(1)

    kort = blokk(".modus-kort")
    assert "background: var(--surface)" in kort
    assert "border: 2px solid var(--border)" in kort
    assert "border-radius: var(--rounded-lg)" in kort
    hover = blokk(".modus-kort:hover")
    assert "translateY(-4px)" in hover
    assert "border-color: var(--primary)" in hover
    assert "box-shadow: var(--shadow-hover)" in hover
    assert "scale(0.97)" in blokk(".modus-kort:active")
    assert "flex-wrap: wrap" in blokk(".modus-liste")
    bred = re.search(r"@media \(min-width: 700px\)\s*\{(.*?)\n\}", css, re.S).group(1)
    assert ".modus-kort" in bred
    assert "justify-content" not in blokk(".knapperad")
    redusert = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", css, re.S)
    assert ".modus-kort:hover" in redusert.group(1)


# --- Innleggingen ---


def test_fr20_innleggingen_har_bare_overskriften(app, innlogget_client):
    """FR-20: innleggingen har h1 «Legg inn CV-en din og stillingsannonsen» og ingen skjema
    ennå (story 2.5)."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))
    html = innlogget_client.get("/innlegging").get_data(as_text=True)
    assert re.search(r"<h1[^>]*>\s*Legg inn CV-en din og stillingsannonsen\s*</h1>", html)
    assert [t for t, _ in tagger_i(html)].count("h1") == 1
    assert "<form" not in main(html)
    assert f"<title>{tekster.INNLEGGING_TITTEL} – Søknadsassistenten</title>" in html
