"""Tester for vinduet «Du har ikke lastet ned brevet.» før utlogging på brevsiden (FR-6, NFR-4,
UX-DR17, UX-DR22, AD-1). Story 7.5. Selve vinduet åpnes i nettleseren (bekreft.js, det samme
skriptet som vinduet «Nytt forslag»), så her testes at vinduet, knappene og skriptene er på
plass, at «Logg ut» nede til høyre bare spør før brevet er lastet ned, og at POST /logg-ut
virker som før. Skriptene prøves for hånd i PR-en (nettlesertester hører til issue #16)."""

import re

import pytest

from soknad.kjerne.okt import Modus
from soknad.web import tekster
from tests.web.hjelpere import (
    NEDLASTING,
    NEDLASTING_PDF,
    STIL,
    FeilendeKI,
    css_blokk,
    element,
    footer,
    html_av,
    main,
    okt_id,
    soknaden,
    tagger_i,
)

# Fiksturene paa_innlegging, paa_resultat, paa_brev og paa_brev_korrektur står i conftest.py.

MALER = STIL.parents[2] / "templates"
JS = STIL.parents[1] / "js"


def vinduet(html):
    """HTML-en til vinduet «Du har ikke lastet ned brevet.», fra <dialog> til </dialog>."""
    return re.search(r'<dialog [^>]*id="vindu-logg-ut".*?</dialog>', html, re.S).group(0)


def logg_ut_knapp(html):
    """Attributtene til «Logg ut»-knappen nede til høyre (i hjørneraden)."""
    knapper = [a for t, a in tagger_i(footer(html)) if t == "button"]
    assert len(knapper) == 1
    return knapper[0]


def klient_paa_brev(request, modus):
    if modus == Modus.KORREKTUR:
        return request.getfixturevalue("paa_brev_korrektur")
    return request.getfixturevalue("paa_brev")


# --- Før nedlasting ---


@pytest.mark.parametrize("modus", list(Modus))
def test_ux_dr17_logg_ut_spor_forst_foer_nedlasting(request, modus):
    """FR-6/UX-DR17: på brevsiden før brevet er lastet ned, i begge modusene, har «Logg ut» nede
    til høyre data-bekreft="vindu-logg-ut", og siden har vinduet etter <main>, lukket.
    Utloggingsskjemaet er som før (POST /logg-ut), og knappen viser ikke ventetegnet."""
    client = klient_paa_brev(request, modus)
    html = html_av(client.get("/brev"))
    assert logg_ut_knapp(html) == {
        "class": "sekundaerknapp liten",
        "type": "submit",
        "data-bekreft": "vindu-logg-ut",
    }
    skjemaer = [a for t, a in tagger_i(footer(html)) if t == "form"]
    assert skjemaer == [{"class": "utlogging", "method": "post", "action": "/logg-ut"}]
    assert "<dialog" not in main(html)
    assert html.index("</main>") < html.index('id="vindu-logg-ut"')
    assert re.search(r"<dialog[^>]*\bopen\b", vinduet(html)) is None
    assert '<script src="/static/js/bekreft.js" defer></script>' in html
    assert '<script src="/static/js/nedlasting.js" defer></script>' in html


def test_ux_dr17_vinduet_har_tekstene_og_aria(paa_brev):
    """UX-DR17/UX-DR22: vinduet har overskriften «Du har ikke lastet ned brevet.» og teksten
    «Vil du logge ut likevel? Brevet blir slettet.». aria-labelledby peker på overskriften og
    aria-describedby på teksten."""
    html = html_av(paa_brev.get("/brev"))
    assert element(html, "vindu-logg-ut") == {
        "class": "vindu",
        "id": "vindu-logg-ut",
        "aria-labelledby": "vindu-logg-ut-overskrift",
        "aria-describedby": "vindu-logg-ut-tekst",
    }
    boks = vinduet(html)
    overskrift = tekster.VINDU_LOGG_UT_OVERSKRIFT
    assert f'<h2 id="vindu-logg-ut-overskrift">{overskrift}</h2>' in boks
    assert f'<p id="vindu-logg-ut-tekst">{tekster.VINDU_LOGG_UT_TEKST}</p>' in boks
    assert (
        boks.index('id="vindu-logg-ut-overskrift"')
        < boks.index('id="vindu-logg-ut-tekst"')
        < boks.index("vindu-knapper")
    )


def test_ux_dr17_knappene_i_vinduet(paa_brev):
    """UX-DR17: «Logg ut» er en hovedknapp med type="button" og data-bekreft-ja (skriptet sender
    utloggingsskjemaet), og «Avbryt» er en sekundærknapp med autofocus i et skjema med
    method="dialog", som lukker vinduet. Ingen andre knapper eller lenker."""
    boks = vinduet(html_av(paa_brev.get("/brev")))
    tagger = tagger_i(boks)
    assert [a for t, a in tagger if t == "button"] == [
        {"class": "hovedknapp", "type": "button", "data-bekreft-ja": None},
        {"class": "sekundaerknapp", "id": "logg-ut-avbryt", "autofocus": None},
    ]
    assert [a for t, a in tagger if t == "form"] == [{"method": "dialog"}]
    assert [t for t, _ in tagger if t == "a"] == []
    assert re.search(rf"<button [^>]*data-bekreft-ja>{tekster.LOGG_UT_KNAPP}</button>", boks)
    assert re.search(
        rf'<button [^>]*id="logg-ut-avbryt"[^>]*>{tekster.AVBRYT_KNAPP}</button>', boks
    )
    assert boks.index("data-bekreft-ja") < boks.index('id="logg-ut-avbryt"')


# --- Etter nedlasting ---


@pytest.mark.parametrize("modus", list(Modus))
@pytest.mark.parametrize("adresse", [NEDLASTING, NEDLASTING_PDF])
def test_nfr4_etter_nedlasting_logges_brukeren_ut_med_en_gang(request, modus, adresse):
    """NFR-4/UX-DR17: er brevet lastet ned (Word eller PDF), i begge modusene, har «Logg ut»
    ingen data-bekreft, og siden har ikke vinduet. Vinduet etter nedlasting er der fortsatt."""
    client = klient_paa_brev(request, modus)
    assert client.get(adresse).status_code == 200
    html = html_av(client.get("/brev"))
    assert "data-bekreft" not in logg_ut_knapp(html)
    assert "vindu-logg-ut" not in html
    assert tekster.VINDU_LOGG_UT_OVERSKRIFT not in html
    assert 'id="vindu-nedlastet"' in html


def test_ux_dr17_nytt_forslag_gir_vinduet_tilbake(app, paa_brev):
    """FR-25/UX-DR17: etter nedlasting og «Nytt forslag» er lastet_ned tom igjen, og «Logg ut»
    spør først på nytt."""
    paa_brev.get(NEDLASTING)
    assert "vindu-logg-ut" not in html_av(paa_brev.get("/brev"))
    assert paa_brev.post("/brev", data={"handling": "nytt_forslag"}).location == "/brev"
    assert soknaden(app, paa_brev).lastet_ned == frozenset()
    html = html_av(paa_brev.get("/brev"))
    assert logg_ut_knapp(html)["data-bekreft"] == "vindu-logg-ut"
    assert 'id="vindu-logg-ut"' in html


def test_ux_dr17_ki_feil_fra_nytt_forslag_beholder_nedlastingen(app, paa_brev):
    """FR-28/UX-DR17: feiler KI-en ved «Nytt forslag» etter nedlasting, er det gamle brevet og
    lastet_ned beholdt, så «Logg ut» spør ikke."""
    paa_brev.get(NEDLASTING)
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave="brev")
    html = html_av(paa_brev.post("/brev", data={"handling": "nytt_forslag"}))
    assert soknaden(app, paa_brev).lastet_ned == {"docx"}
    assert "data-bekreft" not in logg_ut_knapp(html)
    assert "vindu-logg-ut" not in html


def test_ux_dr17_filfeil_spor_fortsatt(paa_brev, filfeil):
    """UX-DR17: kan filen ikke lages, er brevet ikke lastet ned, og «Logg ut» spør fortsatt."""
    html = html_av(paa_brev.get(NEDLASTING))
    assert logg_ut_knapp(html)["data-bekreft"] == "vindu-logg-ut"
    assert 'id="vindu-logg-ut"' in html


# --- Andre sider ---


@pytest.mark.parametrize("side", ["/", "/innlegging", "/resultat", "/resultat-med-brev"])
def test_ux_dr17_andre_sider_logger_ut_som_for(request, side):
    """FR-6/UX-DR17: på startsiden, innleggingen og resultatsiden (også med et brev, der
    bekreft.js er lastet for «Nytt forslag») har «Logg ut» ingen data-bekreft, og siden har
    ikke vinduet."""
    if side == "/":
        client, adresse = request.getfixturevalue("innlogget_client"), "/"
    elif side == "/innlegging":
        client, adresse = request.getfixturevalue("paa_innlegging"), "/innlegging"
    elif side == "/resultat":
        client, adresse = request.getfixturevalue("paa_resultat"), "/resultat"
    else:
        client, adresse = request.getfixturevalue("paa_brev"), "/resultat"
    svar = client.get(adresse)
    assert svar.status_code == 200
    html = html_av(svar)
    assert logg_ut_knapp(html) == {"class": "sekundaerknapp liten", "type": "submit"}
    assert "vindu-logg-ut" not in html
    assert tekster.VINDU_LOGG_UT_OVERSKRIFT not in html


# --- Logg ut likevel ---


def test_fr6_logg_ut_fra_brevsiden_virker_som_for(app, paa_brev):
    """FR-6/NFR-4: «Logg ut» i vinduet sender det samme skjemaet (POST /logg-ut): 302 til
    innloggingen, og økten og søknaden er borte."""
    gammel = okt_id(paa_brev)
    assert app.extensions["oktlager"].hent_soknad(gammel) is not None
    svar = paa_brev.post("/logg-ut")
    assert svar.status_code == 302
    assert svar.location == "/logg-inn"
    assert app.extensions["oktlager"].hent(gammel) is None
    assert app.extensions["oktlager"].hent_soknad(gammel) is None
    assert okt_id(paa_brev) is None


# --- Tekstene, skriptene og CSS-en ---


def test_ux_dr22_tekstene_ligger_i_tekster_py():
    """UX-DR17/UX-DR22: tekstene står ordrett fra skissen i tekster.py, og ikke i malene.
    Knappene gjenbruker «Logg ut» og «Avbryt». Ingen style=."""
    assert tekster.VINDU_LOGG_UT_OVERSKRIFT == "Du har ikke lastet ned brevet."
    assert tekster.VINDU_LOGG_UT_TEKST == "Vil du logge ut likevel? Brevet blir slettet."
    assert tekster.LOGG_UT_KNAPP == "Logg ut"
    assert tekster.AVBRYT_KNAPP == "Avbryt"
    for mal in ("vindu_logg_ut.html", "base.html", "brev.html"):
        innhold = re.sub(r"\{#.*?#\}", "", (MALER / mal).read_text(encoding="utf-8"), flags=re.S)
        for tekst in ("Logg ut", "Avbryt", "ikke lastet ned", "likevel", "blir slettet"):
            assert tekst not in innhold, (mal, tekst)
        assert "style=" not in innhold


def test_ux_dr17_nedlasting_js_tar_bort_sporsmaalet():
    """NFR-4/UX-DR17/AD-1: når en nedlastingslenke trykkes, tar nedlasting.js bort
    data-bekreft fra «Logg ut», så brukeren logges ut med en gang, også før siden lastes på
    nytt. Skriptet henter ingenting og lagrer ingenting."""
    skript = (JS / "nedlasting.js").read_text(encoding="utf-8")
    assert """document.querySelector('[data-bekreft="vindu-logg-ut"]')""" in skript
    assert 'removeAttribute("data-bekreft")' in skript
    # Det skjer inne i klikket på en nedlastingslenke.
    assert skript.index('closest("a[data-nedlasting]")') < skript.index("removeAttribute")
    for forbudt in ("fetch", "XMLHttpRequest", "localStorage", "sessionStorage", ".submit()"):
        assert forbudt not in skript, forbudt


def test_ux_dr17_bekreft_js_virker_for_alle_vinduene():
    """UX-DR17/AD-1: bekreft.js er det samme skriptet for begge vinduene. Det finner vinduet fra
    data-bekreft på knappen, gir «Avbryt» fokus, sender skjemaet med knappen som åpnet etter
    «Ja» (data-bekreft-ja), og sender fokus tilbake når vinduet lukkes. Ingenting er skrevet
    bare for «Nytt forslag»."""
    skript = (JS / "bekreft.js").read_text(encoding="utf-8")
    kode = re.sub(r"^\s*//.*$", "", skript, flags=re.M)
    assert 'getElementById(knapp.getAttribute("data-bekreft"))' in kode
    assert '"[autofocus]"' in kode
    assert "sender.form.requestSubmit(sender)" in kode
    assert "apner.focus()" in kode
    for navn in ("nytt-forslag", "logg-ut", "vente"):
        assert navn not in kode, navn


def test_nfr7_css_fokus_paa_avbryt_og_logg_ut():
    """NFR-7/UX-DR17: «Avbryt» i vinduet og «Logg ut» (data-bekreft) som får fokus tilbake,
    viser fokusringen også etter et museklikk (:focus). Vinduet bruker samme .vindu som de andre
    vinduene, med ramme i høykontrastmodus."""
    css = STIL.read_text(encoding="utf-8")
    velger = "#logg-ut-avbryt:focus,\n#nytt-forslag-avbryt:focus,\n[data-bekreft]:focus"
    fokus = css_blokk(css, velger)
    assert "outline: 3px solid var(--focus-ring);" in fokus
    assert "height" not in fokus
    assert "nowrap" not in fokus
    hoykontrast = re.search(r"@media \(forced-colors: active\) \{(.*?)\n\}", css, re.S).group(1)
    vindu = re.search(r"^\s*\.vindu\s*\{(.*?)\}", hoykontrast, re.S | re.M).group(1)
    assert "border: 1px solid CanvasText;" in vindu
