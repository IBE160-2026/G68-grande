"""Tester for vinduet etter nedlasting på brevsiden (FR-31, FR-6, AD-7, UX-DR16, UX-DR17).
Story 3.3. Selve åpningen og fokusen skjer i nettleseren (nedlasting.js), så her testes at
vinduet, knappene og skriptet er på plass, og at «Lag ny søknad» og «Logg ut» virker."""

import re

import pytest

from soknad.kjerne.okt import Soknad
from soknad.web import tekster
from tests.web.hjelpere import (
    NEDLASTING,
    STIL,
    css_blokk,
    element,
    filnavn_i_dag,
    html_av,
    main,
    med_autofocus,
    okt_id,
    sett_soknad,
    sett_testmodus,
    soknaden,
    tagger_i,
)

# Fiksturene paa_brev (innlogget på brevsiden med case 1) og filfeil (Word-filen kan ikke
# lages) står i conftest.py.

SKRIPT = STIL.parents[1] / "js" / "nedlasting.js"
MAL = STIL.parents[2] / "templates" / "brev.html"


def vinduet(html):
    """HTML-en til vinduet etter nedlasting, fra <dialog> til </dialog>."""
    return re.search(r'<dialog [^>]*id="vindu-nedlastet".*?</dialog>', html, re.S).group(0)


def tekst_i(html, id_):
    return re.search(rf'id="{id_}"[^>]*>(.*?)<', html, re.S).group(1)


# --- Vinduet i siden ---


def test_fr31_vinduet_staar_utenfor_main_med_tekstene_og_aria(paa_brev):
    """FR-31/UX-DR17: brevsiden har vinduet (<dialog>) etter <main>, med «Brevet er lastet
    ned!», dagens filnavn og spørsmålet. aria-labelledby peker på overskriften og
    aria-describedby på filnavnet og spørsmålet."""
    html = html_av(paa_brev.get("/brev"))
    assert "<dialog" not in main(html)
    assert html.index("</main>") < html.index('id="vindu-nedlastet"')
    attr = element(html, "vindu-nedlastet")
    assert "vindu" in attr["class"].split()
    assert attr["aria-labelledby"] == "vindu-nedlastet-overskrift"
    assert attr["aria-describedby"].split() == ["vindu-nedlastet-filnavn", "vindu-nedlastet-tekst"]
    boks = vinduet(html)
    overskrift = re.escape(tekster.VINDU_NEDLASTET_OVERSKRIFT)
    assert re.search(rf'<h2 id="vindu-nedlastet-overskrift">{overskrift}</h2>', boks)
    assert tekst_i(boks, "vindu-nedlastet-filnavn") == tekster.filnavn_linje(filnavn_i_dag())
    assert tekst_i(boks, "vindu-nedlastet-tekst") == tekster.VINDU_NEDLASTET_TEKST
    # Rekkefølgen: overskriften, filnavnet, spørsmålet, så knappene.
    assert (
        boks.index('id="vindu-nedlastet-overskrift"')
        < boks.index('id="vindu-nedlastet-filnavn"')
        < boks.index('id="vindu-nedlastet-tekst"')
        < boks.index("vindu-knapper")
    )


def test_fr31_knappene_i_vinduet(paa_brev):
    """FR-31/FR-6/UX-DR17: «Lag ny søknad» er en hovedknapp-lenke til startsiden, «Logg ut» er
    et POST-skjema til /logg-ut, og «Bli her» lukker vinduet (method="dialog")."""
    boks = vinduet(html_av(paa_brev.get("/brev")))
    tagger = tagger_i(boks)
    lenker = [a for t, a in tagger if t == "a"]
    assert len(lenker) == 1
    assert lenker[0]["href"] == "/"
    assert "hovedknapp" in lenker[0]["class"].split()
    assert "data-nedlasting" not in lenker[0]
    assert re.search(rf'<a [^>]*href="/"[^>]*>{re.escape(tekster.LAG_NY_SOKNAD_KNAPP)}</a>', boks)

    skjemaer = [a for t, a in tagger if t == "form"]
    assert skjemaer == [{"method": "post", "action": "/logg-ut"}, {"method": "dialog"}]
    knapper = [a for t, a in tagger if t == "button"]
    assert knapper[0] == {"class": "sekundaerknapp", "type": "submit"}
    assert knapper[1] == {"class": "lenkeknapp", "id": "bli-her"}
    assert re.search(rf"<button [^>]*>{re.escape(tekster.LOGG_UT_KNAPP)}</button>", boks)
    assert re.search(
        rf'<button [^>]*id="bli-her"[^>]*>{re.escape(tekster.BLI_HER_KNAPP)}</button>', boks
    )


@pytest.mark.parametrize("tilstand", ["for-nedlasting", "lastet-ned", "filfeil"])
def test_fr31_vinduet_aapnes_aldri_av_seg_selv(request, paa_brev, tilstand):
    """FR-31/UX-DR17: vinduet er lukket når siden lastes, også etter nedlasting (lastet_ned
    sann) og ved FilFeil. Ingen open og ingen autofocus i vinduet. Sidens autofocus står på
    overskriften eller feilboksen."""
    if tilstand == "for-nedlasting":
        html = html_av(paa_brev.get("/brev"))
        assert med_autofocus(html) == [None]
    elif tilstand == "lastet-ned":
        paa_brev.get(NEDLASTING)
        html = html_av(paa_brev.get("/brev"))
        assert med_autofocus(html) == [None]
    else:
        request.getfixturevalue("filfeil")
        html = html_av(paa_brev.get(NEDLASTING))
        assert med_autofocus(html) == ["feilboks"]
    assert "open" not in element(html, "vindu-nedlastet")
    boks = vinduet(html)
    assert "autofocus" not in boks
    assert re.search(r"<dialog[^>]*\bopen\b", boks) is None


# --- Knappene virker ---


@pytest.mark.parametrize("testmodus", [True, False], ids=["testmodus-paa", "testmodus-av"])
def test_fr31_lag_ny_soknad_gir_tom_soknad_og_beholder_testmodus(app, paa_brev, testmodus):
    """FR-31/AD-7: «Lag ny søknad» etter nedlasting går til startsiden, som gir en tom søknad.
    Økten er den samme, og testmodus er beholdt (både på og av)."""
    soknad = soknaden(app, paa_brev)
    sett_testmodus(app, paa_brev, testmodus)
    sett_soknad(app, paa_brev, soknad)
    assert paa_brev.get(NEDLASTING).status_code == 200
    html = html_av(paa_brev.get("/brev"))
    lenke = next(a for t, a in tagger_i(vinduet(html)) if t == "a")

    lager = app.extensions["oktlager"]
    id_ = okt_id(paa_brev)
    innlogging = lager.hent(id_)
    svar = paa_brev.get(lenke["href"])
    assert svar.status_code == 200
    assert soknaden(app, paa_brev) == Soknad()
    assert okt_id(paa_brev) == id_
    assert lager.hent(id_) == innlogging
    assert lager.hent(id_).testmodus is testmodus


def test_fr6_logg_ut_i_vinduet_logger_ut(app, paa_brev):
    """FR-6/FR-31: «Logg ut» i vinduet logger ut som i story 1.4: til innloggingen, økten og
    søknaden er slettet."""
    paa_brev.get(NEDLASTING)
    skjema = next(a for t, a in tagger_i(vinduet(html_av(paa_brev.get("/brev")))) if t == "form")
    gammel = okt_id(paa_brev)
    svar = paa_brev.post(skjema["action"])
    assert svar.status_code == 302
    assert svar.location == "/logg-inn"
    assert app.extensions["oktlager"].hent(gammel) is None
    assert app.extensions["oktlager"].hent_soknad(gammel) is None
    assert okt_id(paa_brev) is None


# --- Skriptet, tekstene og CSS-en ---


def test_fr31_skriptet_aapner_vinduet_og_flytter_fokus():
    """FR-31/UX-DR17: nedlasting.js åpner vinduet med showModal() (så bare vinduet kan nås),
    gir «Bli her» fokus og sender fokus tilbake til knappen når vinduet lukkes. Det stopper
    ikke nedlastingen og henter ingenting (AD-1)."""
    skript = SKRIPT.read_text(encoding="utf-8")
    assert 'getElementById("vindu-nedlastet")' in skript
    assert ".showModal()" in skript
    assert "!vindu.open" in skript
    assert 'getElementById("bli-her")' in skript
    assert "bliHer.focus()" in skript
    assert skript.count('addEventListener("close"') == 1
    assert "tilbakeTil.focus()" in skript
    assert "preventDefault" not in skript
    assert "fetch" not in skript


def test_fr31_tekstene_ligger_i_tekster_py():
    """FR-31/UX-DR17: tekstene står i web/tekster.py, ordrett fra EXPERIENCE, og ikke i malen."""
    assert tekster.VINDU_NEDLASTET_OVERSKRIFT == "Brevet er lastet ned!"
    assert tekster.VINDU_NEDLASTET_TEKST == "Vil du lage en ny søknad eller logge ut?"
    assert tekster.LAG_NY_SOKNAD_KNAPP == "Lag ny søknad"
    assert tekster.BLI_HER_KNAPP == "Bli her"
    assert tekster.LOGG_UT_KNAPP == "Logg ut"
    innhold = re.sub(r"\{#.*?#\}", "", MAL.read_text(encoding="utf-8"), flags=re.S)
    for tekst in ("Brevet er", "Vil du", "Lag ny", "Logg ut", "Bli her", "Filnavn"):
        assert tekst not in innhold, tekst


def test_fr31_vinduet_i_css():
    """FR-31/NFR-7/UX-DR17: vinduet er høyst 420 px bredt og følger skjermen, har mørkt slør,
    knapperaden brytes, og «Bli her» er en lenkeknapp. Ingen fast høyde og ingen nowrap."""
    css = STIL.read_text(encoding="utf-8")
    vindu = css_blokk(css, ".vindu")
    assert "max-width: 420px;" in vindu
    assert "width: calc(100% - 2 * var(--space-4));" in vindu
    assert "border: none;" in vindu
    assert "background: var(--veil);" in css_blokk(css, ".vindu::backdrop")
    assert "--veil: rgba(58, 37, 48, 0.45);" in css_blokk(css, ":root")
    knapper = css_blokk(css, ".vindu-knapper")
    assert "flex-wrap: wrap;" in knapper
    assert "margin: 0;" in css_blokk(css, ".vindu-knapper form")
    hoved = css_blokk(css, ".vindu .hovedknapp")
    assert "width: auto;" in hoved
    lenkeknapp = css_blokk(css, ".lenkeknapp")
    assert "text-decoration: underline;" in lenkeknapp
    assert "border: none;" in lenkeknapp
    # «Bli her» viser fokusringen også når vinduet ble åpnet med musa (bare :focus-visible
    # gir ingen ring etter et museklikk).
    bli_her = css_blokk(css, "#bli-her:focus")
    assert "outline: 3px solid var(--focus-ring);" in bli_her
    # Høykontrastmodus: vinduet får en ramme, siden skyggen og sløret forsvinner.
    hoykontrast = re.search(r"@media \(forced-colors: active\) \{(.*?)\n\}", css, re.S).group(1)
    vindu_hoykontrast = re.search(r"^\s*\.vindu\s*\{(.*?)\}", hoykontrast, re.S | re.M).group(1)
    assert "border: 1px solid CanvasText;" in vindu_hoykontrast
    for blokk in (vindu, knapper, hoved, lenkeknapp):
        assert "height" not in blokk
        assert "nowrap" not in blokk
