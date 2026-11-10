"""Tester for ventetegnet og «opptatt» rundt KI-kallene (FR-27, FR-28, NFR-6, NFR-7, AD-1,
AD-8, UX-DR14, UX-DR18). Story 2.7.1."""

import re

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.kjerne.feil import KIFeilType
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from tests.web.hjelpere import (
    STIL,
    WEB,
    FeilendeKI,
    css_blokk,
    main,
    med_autofocus,
    sett_soknad,
    soknaden,
    tagger_i,
)

CASE = TESTDATA_MAPPE / "case-1-utvikler"
CV = (CASE / "cv.txt").read_text(encoding="utf-8")
ANNONSE = (CASE / "annonse.txt").read_text(encoding="utf-8")
VENTE_JS = WEB / "static" / "js" / "vente.js"


class SpionKI:
    """Samme svar som TestKI, men ser om søknaden er opptatt under hvert kall. Er unntak satt,
    kastes det fra hvert kall i stedet for svaret (da stopper det første kallet POST-en)."""

    def __init__(self, test_ki, app, client, unntak=None):
        self.test_ki = test_ki
        self.caser = test_ki.caser
        self.app = app
        self.client = client
        self.unntak = unntak
        self.opptatt_under = []

    def _se(self):
        self.opptatt_under.append(soknaden(self.app, self.client).opptatt)
        if self.unntak is not None:
            raise self.unntak

    def nokkelord(self, annonse):
        self._se()
        return self.test_ki.nokkelord(annonse)

    def gap(self, cv, annonse):
        self._se()
        return self.test_ki.gap(cv, annonse)


@pytest.fixture
def paa_innlegging(app, innlogget_client):
    """En innlogget klient på innleggingen for Full generering."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))
    return innlogget_client


def send(client, handling="sjekk"):
    return client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": handling})


def html_av(svar):
    return svar.get_data(as_text=True)


def element(html, id_):
    return next(a for _, a in tagger_i(html) if a.get("id") == id_)


# --- Matrisen: «opptatt» på serveren ---


def test_fr27_vellykket_gir_resultatsiden_og_opptatt_usann(app, paa_innlegging):
    """FR-27/AD-8: case 1 gir resultatsiden, og søknaden er ikke opptatt etterpå."""
    svar = send(paa_innlegging)
    assert svar.status_code == 302
    assert svar.location == "/resultat"
    soknad = soknaden(app, paa_innlegging)
    assert soknad.steg == Steg.RESULTAT
    assert soknad.opptatt is False


def test_fr27_opptatt_er_sann_under_kallet(app, paa_innlegging):
    """FR-27/AD-8: søknaden er opptatt i øktlageret under begge KI-kallene."""
    spion = SpionKI(app.extensions["test_ki"], app, paa_innlegging)
    app.extensions["test_ki"] = spion
    send(paa_innlegging)
    assert spion.opptatt_under == [True, True]


@pytest.mark.parametrize(
    ("steg", "side"), [(Steg.INNLEGGING, "/innlegging"), (Steg.RESULTAT, "/resultat")]
)
@pytest.mark.parametrize("handling", ["sjekk", "tilbake", "noe"])
def test_fr27_ny_post_mens_opptatt_sender_til_steget(app, innlogget_client, steg, side, handling):
    """FR-27/AD-8: kommer en ny POST mens søknaden er opptatt, sendes brukeren til siden for
    steget. KI-en kalles ikke, og ingenting lagres, heller ikke nye tekster."""
    soknad = Soknad(steg=steg, modus=Modus.FULL_GENERERING, cv=Tekstfelt("gammel"), opptatt=True)
    sett_soknad(app, innlogget_client, soknad)
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    svar = send(innlogget_client, handling=handling)
    assert svar.status_code == 302
    assert svar.location == side
    assert kalt == []
    assert soknaden(app, innlogget_client) == soknad


@pytest.mark.parametrize("oppgave", ["nokkelord", "gap"])
@pytest.mark.parametrize("feiltype", list(KIFeilType))
def test_fr28_ki_feil_gir_samme_side_og_opptatt_usann(app, paa_innlegging, oppgave, feiltype):
    """FR-28/AD-8: en KIFeil gir innleggingen på nytt (200) som før, og søknaden er ikke
    opptatt etterpå, så «Sjekk CV-en min» kan trykkes igjen."""
    app.extensions["test_ki"] = FeilendeKI(
        app.extensions["test_ki"], oppgave=oppgave, feiltype=feiltype
    )
    svar = send(paa_innlegging)
    assert svar.status_code == 200
    assert 'id="feilboks"' in html_av(svar)
    soknad = soknaden(app, paa_innlegging)
    assert soknad.opptatt is False
    assert soknad.steg == Steg.INNLEGGING
    assert soknad.cv == Tekstfelt(CV)


def test_fr27_uventet_feil_gir_opptatt_usann(app, paa_innlegging):
    """FR-27/AD-8: et annet unntak enn KIFeil går videre, men søknaden blir ikke stående
    opptatt. Da kan brukeren prøve igjen."""
    app.extensions["test_ki"] = SpionKI(
        app.extensions["test_ki"], app, paa_innlegging, unntak=RuntimeError("uventet")
    )
    with pytest.raises(RuntimeError):
        send(paa_innlegging)
    soknad = soknaden(app, paa_innlegging)
    assert soknad.opptatt is False
    assert soknad.cv == Tekstfelt(CV)
    # Neste forsøk kaller KI-en igjen.
    app.extensions["test_ki"] = app.extensions["test_ki"].test_ki
    assert send(paa_innlegging).location == "/resultat"


# --- Ventetegnet på siden ---


def test_ux_dr14_ventetegnet_star_utenfor_main_og_er_skjult(paa_innlegging):
    """UX-DR14/NFR-6: ventetegnet og statusområdet står etter hjørneraden, utenfor main, så
    de aldri blir inert. Ventetegnet er skjult når siden åpnes, og statusområdet er tomt."""
    html = html_av(paa_innlegging.get("/innlegging"))
    assert 'id="vente"' not in main(html)
    assert html.index("</footer>") < html.index('id="vente"')
    assert re.search(r'<p class="skjult" id="vente-status" role="status"></p>', html)
    assert "hidden" in element(html, "ventetegn")
    assert re.search(r'<p class="vente-tekst" id="vente-tekst"></p>', html)
    # Statusområdet står i beholderen, men utenfor selve ventetegnet.
    beholder = html[html.index('id="vente"') :]
    assert beholder.index('id="vente-status"') < beholder.index('id="ventetegn"')


def test_ux_dr14_overskriften_og_prikkene(paa_innlegging):
    """UX-DR14/UX-DR21: «På vei mot ny jobb» og tre prikker, som er skjult for skjermlesere."""
    html = html_av(paa_innlegging.get("/innlegging"))
    assert '<p class="vente-overskrift">På vei mot ny jobb</p>' in html
    assert re.search(r'<div class="prikker" aria-hidden="true">(<span></span>){3}</div>', html)


def test_fr27_bare_sjekk_knappen_har_ventetekst(paa_innlegging):
    """FR-27: på siden uten feil starter «Sjekk CV-en min» KI-kallet og har ventesetningen.
    «Tilbake» har ingen. Etter en KI-feil har også «Prøv på nytt» den (test_innlegging.py)."""
    html = html_av(paa_innlegging.get("/innlegging"))
    vente = [(a.get("value"), a["data-vente"]) for t, a in tagger_i(html) if "data-vente" in a]
    assert vente == [("sjekk", "Vi sjekker CV-en din – det tar noen sekunder.")]


def test_fr27_tekstene_ligger_i_tekster_py():
    """FR-27: tekstene står ordrett fra EXPERIENCE i tekster.py, ikke i malene."""
    assert tekster.VENTE_OVERSKRIFT == "På vei mot ny jobb"
    assert tekster.VENTE_SJEKKER == "Vi sjekker CV-en din – det tar noen sekunder."
    for mal in ("ventetegn.html", "innlegging.html"):
        innhold = (WEB / "templates" / mal).read_text(encoding="utf-8")
        assert "På vei" not in innhold
        assert "Vi sjekker" not in innhold
    # Feilboksen ved KI-feil (FR-28, story 2.7.2).
    innhold = (WEB / "templates" / "innlegging.html").read_text(encoding="utf-8")
    assert "er ikke borte" not in innhold
    assert "Prøv på nytt" not in innhold


@pytest.mark.parametrize("side", ["/", "/modus", "/resultat"])
def test_ad1_ventetegnet_bare_pa_sider_med_ki_kall(app, innlogget_client, side):
    """AD-1: vente.js og ventetegnet finnes på innleggingen, ikke på sider uten KI-kall."""
    sett_soknad(
        app,
        innlogget_client,
        Soknad(
            steg=Steg.RESULTAT,
            modus=Modus.FULL_GENERERING,
            cv=Tekstfelt(CV),
            annonse=Tekstfelt(ANNONSE),
            nokkelord=("Python",),
            nokkelord_annonse="annonse",
            gap={"dekker": ["Python"], "mangler": []},
        ),
    )
    svar = innlogget_client.get(side)
    assert svar.status_code == 200
    assert "js/vente.js" not in html_av(svar)
    assert 'id="ventetegn"' not in html_av(svar)


def test_ad1_ventetegnet_lastes_pa_innleggingen(paa_innlegging):
    """AD-1: innleggingen har vente.js og ventetegnet."""
    html = html_av(paa_innlegging.get("/innlegging"))
    assert "js/vente.js" in html
    assert 'id="ventetegn"' in html


def test_ux_dr14_resultatsiden_gir_fokus_til_overskriften(app, paa_innlegging):
    """UX-DR14: etter ventetegnet går fokus til h1 på resultatsiden."""
    send(paa_innlegging)
    html = html_av(paa_innlegging.get("/resultat"))
    h1 = next(a for t, a in tagger_i(html) if t == "h1")
    assert h1["tabindex"] == "-1"
    assert "autofocus" in h1
    assert len([t for t, a in tagger_i(html) if "autofocus" in a]) == 1


def test_ux_dr14_overskriften_med_fokus_har_ingen_ring():
    """UX-DR14: overskriften som får fokus, kan ikke nås med Tab og viser ingen fokusring
    (Kristine bestemte 2026-11-10). Vanlige elementer har fortsatt ringen."""
    css = STIL.read_text(encoding="utf-8")
    assert "outline: none" in css_blokk(css, '.side-overskrift[tabindex="-1"]:focus')
    assert "outline: 3px solid var(--focus-ring)" in css_blokk(css, ":focus-visible")


def test_ux_dr14_ki_feil_gir_fokus_til_feilboksen(app, paa_innlegging):
    """UX-DR14: ved KI-feil går fokus til feilboksen, ikke til noe annet."""
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"])
    html = html_av(send(paa_innlegging))
    assert med_autofocus(html) == ["feilboks"]


# --- Skriptet ---


def test_ux_dr14_skriptet_sperrer_med_inert_og_aria_disabled():
    """UX-DR14/AD-1: vente.js reagerer bare på knapper med data-vente, gjør resten inert,
    låser knappen med aria-disabled (ikke disabled, så den beholder fokus), stopper et nytt
    trykk og skriver ventesetningen i statusområdet."""
    js = VENTE_JS.read_text(encoding="utf-8")
    assert 'addEventListener("submit"' in js
    assert "hendelse.submitter" in js
    assert '"data-vente"' in js
    assert ".inert = true" in js
    assert 'setAttribute("aria-disabled", "true")' in js
    assert "preventDefault()" in js
    assert "knapp.focus()" in js
    assert 'getElementById("vente-status").textContent' in js
    assert 'getElementById("ventetegn").hidden = false' in js
    # Bare aria-disabled, aldri disabled.
    assert not re.search(r"(?<!aria-)disabled\s*=|\.disabled\b|\"disabled\"", js)


def test_ad1_vente_skriptet_sender_ingenting_selv():
    """AD-1: vente.js lar nettleseren sende skjemaet som vanlig og sender ingenting selv."""
    js = VENTE_JS.read_text(encoding="utf-8")
    for forbudt in ("fetch(", "XMLHttpRequest", ".submit(", "sendBeacon"):
        assert forbudt not in js
    # Bare bruk av location stoppes, ikke ordet i en kommentar.
    assert not re.search(r"\blocation\s*[.=\[]", js)


# --- CSS ---


def test_ux_dr14_ventetegnet_dekker_skjermen_over_hjorneraden():
    """UX-DR14: ventetegnet dekker hele skjermen med bakgrunnen med 94 %, over hjørneraden."""
    css = STIL.read_text(encoding="utf-8")
    blokk = css_blokk(css, ".ventetegn")
    assert "position: fixed" in blokk
    assert "inset: 0" in blokk
    assert "background: var(--wait-cover)" in blokk
    assert "--wait-cover: rgba(255, 247, 245, 0.94);" in css
    z_vente = int(re.search(r"z-index: (\d+)", blokk).group(1))
    z_hjorne = int(re.search(r"z-index: (\d+)", css_blokk(css, ".hjornerad")).group(1))
    assert z_vente > z_hjorne


def test_ux_dr14_prikkene_hopper_som_i_design():
    """UX-DR14: prikkene er 16 px (uten fast høyde), hopper 14 px, 1 s per hopp, 0,15 s etter
    hverandre, i primary, dot-middle og accent. Overskriften i Baloo 2."""
    css = STIL.read_text(encoding="utf-8")
    prikk = css_blokk(css, ".prikker span")
    assert "min-width: 16px" in prikk
    assert "min-height: 16px" in prikk
    assert "background: var(--primary)" in prikk
    assert "animation: hopp 1s ease-in-out infinite" in prikk
    andre = css_blokk(css, ".prikker span:nth-child(2)")
    assert "var(--dot-middle)" in andre
    assert "animation-delay: 0.15s" in andre
    tredje = css_blokk(css, ".prikker span:nth-child(3)")
    assert "var(--accent)" in tredje
    assert "animation-delay: 0.3s" in tredje
    assert "translateY(-14px)" in re.search(r"@keyframes hopp\s*\{(.*?)\n\}", css, re.S).group(1)
    overskrift = css_blokk(css, ".vente-overskrift")
    assert "var(--font-logo)" in overskrift
    assert "font-weight: 800" in overskrift
    assert "var(--size-wait-title)" in overskrift


def test_ux_dr18_prikkene_star_stille_ved_redusert_bevegelse():
    """UX-DR18: ved prefers-reduced-motion slås alle animasjoner av, også prikkene."""
    css = STIL.read_text(encoding="utf-8")
    redusert = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", css, re.S)
    assert re.search(
        r"\*,\s*\*::before,\s*\*::after\s*\{\s*animation: none !important", redusert.group(1)
    )


def test_ux_dr14_last_knapp_og_hoykontrast():
    """UX-DR14: den låste knappen ser låst ut, og prikkene synes i høykontrastmodus."""
    css = STIL.read_text(encoding="utf-8")
    assert "opacity: 0.55" in css_blokk(css, '.hovedknapp[aria-disabled="true"]')
    hoykontrast = re.search(r"@media \(forced-colors: active\)\s*\{(.*?)\n\}", css, re.S).group(1)
    assert re.search(r"\.prikker span:nth-child\(n\)\s*\{[^}]*background: CanvasText", hoykontrast)
