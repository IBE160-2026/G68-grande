"""Tester for samtykket på startsiden, KI-merknaden i hjørneraden og valget mellom EkteKI og
TestKI (FR-32, FR-35, FR-36, AD-3, AD-12, UX-DR10, UX-DR11). Ingen test kaller det ekte
API-et: EkteKI byttes ut med TellendeKI før noe kalles."""

import re
from dataclasses import replace

import pytest

from soknad.adaptere.ki import EkteKI
from soknad.kjerne.feil import KIFeilType
from soknad.kjerne.okt import Innlogging, Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import ruter, tekster
from soknad.web.flyt import ki
from tests.web.hjelpere import (
    ANNONSE,
    CV,
    GAP_SVAR,
    NOKKELORD_SVAR,
    STIL,
    FeilendeKI,
    TellendeKI,
    app_med_nokkel,
    css_blokk,
    element,
    footer,
    html_av,
    logg_inn,
    main,
    med_autofocus,
    okt_id,
    sett_soknad,
    soknaden,
    tagger_i,
)


@pytest.fixture
def med_nokkel():
    """(app, klient, kalt): innlogget i en app med API-nøkkel, så testmodus er av. EkteKI er
    byttet ut med TellendeKI, og kalt viser hvilke oppgaver den har fått."""
    app = app_med_nokkel()
    kalt = []
    app.extensions["ekte_ki"] = TellendeKI(app.extensions["test_ki"], kalt=kalt)
    client = app.test_client()
    assert logg_inn(client).status_code == 302
    return app, client, kalt


def avkrysningsboks(html):
    """Attributtene til avkrysningsboksen for samtykket, eller None."""
    return next((a for t, a in tagger_i(html) if t == "input" and a.get("id") == "samtykke"), None)


# --- Matrisen ---


def test_fr36_begynn_uten_samtykke_gir_feilen_ved_boksen(med_nokkel):
    """FR-36/UX-DR10: «Begynn å lage søknad» uten avkryssing når testmodus er av gir
    startsiden på nytt uten redirect: rød ramme (aria-invalid), «Du må samtykke før du kan
    begynne» koblet til boksen og fokus på boksen. Steget er fortsatt start."""
    app, client, kalt = med_nokkel
    client.get("/")
    svar = client.post("/")
    assert svar.status_code == 200
    html = html_av(svar)
    boks = avkrysningsboks(html)
    assert boks["aria-invalid"] == "true"
    assert boks["aria-describedby"] == "samtykke-feil"
    assert "checked" not in boks
    assert med_autofocus(html) == ["samtykke"]
    feil = re.search(r'<p class="feiltekst" id="samtykke-feil">(.*?)</p>', html)
    assert feil.group(1) == tekster.SAMTYKKE_FEIL == "Du må samtykke før du kan begynne"
    # Ingen role="alert": teksten leses opp når boksen får fokus.
    assert 'role="alert"' not in html
    assert soknaden(app, client) == Soknad()
    assert kalt == []


def test_fr36_annen_verdi_enn_ja_gir_samtykkefeilen(med_nokkel):
    """FR-36: bare samtykke=ja er et samtykke. «on» (det nettleseren sender uten value) gir
    feilen, og steget er fortsatt start."""
    app, client, _ = med_nokkel
    client.get("/")
    svar = client.post("/", data={"samtykke": "on"})
    assert svar.status_code == 200
    assert avkrysningsboks(html_av(svar))["aria-invalid"] == "true"
    assert soknaden(app, client) == Soknad()


def test_fr36_samtykke_lagres_ikke_i_testmodus(app, innlogget_client):
    """FR-36/AD-12: i testmodus vises ingen boks, så en POST med samtykke=ja lagrer ikke
    samtykket."""
    innlogget_client.get("/")
    assert innlogget_client.post("/", data={"samtykke": "ja"}).location == "/modus"
    assert soknaden(app, innlogget_client) == Soknad(steg=Steg.MODUS)


def test_fr7_utlogget_for_begynn_gir_innloggingen(med_nokkel, monkeypatch):
    """FR-7/AD-8: logges brukeren ut i en annen fane etter login_required, men før «Begynn å
    lage søknad» sjekker testmodus, sendes hen til innloggingen med «Du må logge inn først».
    Ingen feilside, og ingen søknad blir liggende."""
    app, client, _ = med_nokkel
    lager = app.extensions["oktlager"]
    id_ = okt_id(client)
    ekte_hent = ruter.gjeldende_soknad

    def hent_og_logg_ut():
        soknad = ekte_hent()
        lager.slett(id_)
        return soknad

    monkeypatch.setattr(ruter, "gjeldende_soknad", hent_og_logg_ut)
    svar = client.post("/", data={"samtykke": "ja"})
    assert svar.status_code == 302
    assert svar.location == "/logg-inn?ikke_innlogget=1"
    assert okt_id(client) is None
    assert lager.hent_soknad(id_) is None


def test_fr36_begynn_med_samtykke_lagrer_samtykket(med_nokkel):
    """FR-36/AD-7: med avkryssing lagres samtykket, og brukeren sendes til modusvalget."""
    app, client, _ = med_nokkel
    client.get("/")
    svar = client.post("/", data={"samtykke": "ja"})
    assert svar.status_code == 302
    assert svar.location == "/modus"
    assert soknaden(app, client) == Soknad(steg=Steg.MODUS, samtykke=True)


def test_fr36_begynn_i_testmodus_uten_samtykke(app, innlogget_client):
    """FR-36: i testmodus finnes ingen avkrysningsboks, og «Begynn å lage søknad» sender til
    modusvalget uten samtykke."""
    html = html_av(innlogget_client.get("/"))
    assert avkrysningsboks(html) is None
    assert tekster.SAMTYKKE_LINJE not in html
    svar = innlogget_client.post("/")
    assert svar.location == "/modus"
    assert soknaden(app, innlogget_client) == Soknad(steg=Steg.MODUS)


def test_fr36_boksen_er_tom_etter_av_paa_av(med_nokkel):
    """FR-36: boksen er alltid tom når startsiden åpnes, også etter at testmodus er slått på
    og av igjen, og etter et samtykke i samme økt."""
    app, client, _ = med_nokkel
    client.get("/")
    client.post("/", data={"samtykke": "ja"})
    assert soknaden(app, client).samtykke is True
    html = html_av(client.get("/"))
    assert "checked" not in avkrysningsboks(html)
    assert soknaden(app, client).samtykke is False
    client.post("/testmodus", data={"testmodus": "paa"})
    assert avkrysningsboks(html_av(client.get("/?bryter=1"))) is None
    client.post("/testmodus", data={"testmodus": "av"})
    html = html_av(client.get("/?bryter=1"))
    boks = avkrysningsboks(html)
    assert boks == {"type": "checkbox", "id": "samtykke", "name": "samtykke", "value": "ja"}
    assert soknaden(app, client) == Soknad()


def test_fr36_samtykke_som_alt_er_gitt_beholdes(med_nokkel):
    """FR-36/AD-8: POST / fra en gammel fane mens søknaden er lenger fram, endrer ikke
    søknaden, heller ikke samtykket."""
    app, client, _ = med_nokkel
    soknad = Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, samtykke=True)
    sett_soknad(app, client, soknad)
    assert client.post("/").location == "/modus"
    assert soknaden(app, client) == soknad


def test_fr36_ingen_ki_kall_fra_innleggingen_uten_samtykke(med_nokkel):
    """AD-12/FR-36: testmodus av og samtykke=False på innleggingen: «Sjekk CV-en min» kaller
    ikke KI-en, og brukeren sendes til startsiden."""
    app, client, kalt = med_nokkel
    sett_soknad(app, client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.status_code == 302
    assert svar.location == "/"
    assert kalt == []
    assert soknaden(app, client).nokkelord is None


def test_fr36_ingen_ki_kall_fra_resultatsiden_uten_samtykke(med_nokkel):
    """AD-12/FR-36: testmodus av og samtykke=False på resultatsiden: «Lag søknadsbrevet mitt»
    kaller ikke KI-en, og brukeren sendes til startsiden."""
    app, client, kalt = med_nokkel
    soknad = Soknad(
        steg=Steg.RESULTAT,
        modus=Modus.FULL_GENERERING,
        nokkelord=tuple(NOKKELORD_SVAR["nokkelord"]),
        gap=GAP_SVAR,
    )
    sett_soknad(app, client, soknad)
    svar = client.post("/resultat", data={"handling": "brev"})
    assert svar.status_code == 302
    assert svar.location == "/"
    assert kalt == []
    assert soknaden(app, client) == soknad


# --- Valget av KI (AD-3) ---


def gjennom_flyten(client):
    """Fra startsiden til brevet med samtykke og testdataene fra case 1."""
    client.get("/")
    assert client.post("/", data={"samtykke": "ja"}).location == "/modus"
    assert client.post("/modus", data={"modus": "full_generering"}).location == "/innlegging"
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.location == "/resultat"
    assert client.post("/resultat", data={"handling": "brev"}).location == "/brev"


def test_fr32_testmodus_av_bruker_ekte_ki_etter_samtykke(med_nokkel):
    """FR-32/AD-3: med nøkkel, testmodus av og samtykke kalles EkteKI (her TellendeKI) for
    «Sjekk CV-en min» og «Lag søknadsbrevet mitt», og TestKI kalles ikke."""
    app, client, kalt = med_nokkel
    test_kalt = []
    app.extensions["test_ki"] = TellendeKI(app.extensions["test_ki"], kalt=test_kalt)
    gjennom_flyten(client)
    assert kalt == ["nokkelord", "gap", "brev"]
    assert test_kalt == []


def test_fr32_testmodus_paa_bruker_test_ki(med_nokkel):
    """FR-32/AD-3: med nøkkel og testmodus slått på kalles TestKI, og EkteKI kalles ikke."""
    app, client, kalt = med_nokkel
    test_kalt = []
    app.extensions["test_ki"] = TellendeKI(app.extensions["test_ki"], kalt=test_kalt)
    client.get("/")
    client.post("/testmodus", data={"testmodus": "paa"})
    client.get("/")
    assert client.post("/").location == "/modus"
    client.post("/modus", data={"modus": "full_generering"})
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.location == "/resultat"
    assert client.post("/resultat", data={"handling": "brev"}).location == "/brev"
    assert test_kalt == ["nokkelord", "gap", "brev"]
    assert kalt == []


class ByttendeKI(TellendeKI):
    """TellendeKI som kaller bytt() i nokkelord, før svaret, for eksempel for å slå av
    testmodus som fra en annen fane mens KI-en jobber."""

    def __init__(self, test_ki, bytt, kalt):
        super().__init__(test_ki, kalt=kalt)
        self.bytt = bytt

    def nokkelord(self, annonse):
        self.bytt()
        return super().nokkelord(annonse)


def test_fr32_testmodus_av_midt_i_analysen_gir_ikke_ekte_ki(med_nokkel):
    """AD-12/FR-36: slås testmodus av (fra på) i en annen fane mens nøkkelordene hentes, går
    også gap til TestKI. EkteKI kalles aldri, for samtykket mangler."""
    app, client, kalt = med_nokkel
    lager = app.extensions["oktlager"]
    client.get("/")
    client.post("/testmodus", data={"testmodus": "paa"})
    client.get("/")
    assert client.post("/").location == "/modus"
    client.post("/modus", data={"modus": "full_generering"})
    id_ = okt_id(client)

    def slaa_av():
        lager.bytt_innlogging(id_, Innlogging(lager.hent(id_).bruker_id, testmodus=False))

    test_kalt = []
    app.extensions["test_ki"] = ByttendeKI(app.extensions["test_ki"], slaa_av, test_kalt)
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.location == "/resultat"
    assert lager.hent(id_).testmodus is False
    assert test_kalt == ["nokkelord", "gap"]
    assert kalt == []


def i_testmodus_til_innleggingen(app, client):
    """Slår på testmodus, begynner uten samtykke og velger Full generering. Gir økt-id-en og
    listen over kallene til TestKI, som er byttet ut med TellendeKI."""
    client.get("/")
    client.post("/testmodus", data={"testmodus": "paa"})
    client.get("/")
    assert client.post("/").location == "/modus"
    client.post("/modus", data={"modus": "full_generering"})
    test_kalt = []
    app.extensions["test_ki"] = TellendeKI(app.extensions["test_ki"], kalt=test_kalt)
    return okt_id(client), test_kalt


def slaa_av_etter_samtykket(monkeypatch, app, id_):
    """Slår av testmodus (fra på) som fra en annen fane rett etter samtykkesjekken, før KI-en
    velges. Svaret fra sjekken er det samme som før."""
    lager = app.extensions["oktlager"]
    ekte_sjekk = ruter.til_start_uten_samtykke

    def sjekk_og_slaa_av(soknad, innlogging):
        svar = ekte_sjekk(soknad, innlogging)
        lager.bytt_innlogging(id_, Innlogging(lager.hent(id_).bruker_id, testmodus=False))
        return svar

    monkeypatch.setattr(ruter, "til_start_uten_samtykke", sjekk_og_slaa_av)


def test_fr36_testmodus_av_mellom_samtykket_og_valget_gir_ikke_ekte_ki_i_analysen(
    med_nokkel, monkeypatch
):
    """AD-12/FR-36: slås testmodus av (fra på) i en annen fane etter at samtykket er sjekket,
    men før KI-en velges, går analysen til TestKI, som sjekken gjaldt for. EkteKI kalles
    aldri, for samtykket mangler."""
    app, client, kalt = med_nokkel
    id_, test_kalt = i_testmodus_til_innleggingen(app, client)
    slaa_av_etter_samtykket(monkeypatch, app, id_)
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.location == "/resultat"
    assert app.extensions["oktlager"].hent(id_).testmodus is False
    assert test_kalt == ["nokkelord", "gap"]
    assert kalt == []
    assert soknaden(app, client).samtykke is False
    assert soknaden(app, client).ki_kall == 0


def test_fr36_testmodus_av_etter_feltsjekken_gir_ikke_ekte_ki_i_analysen(med_nokkel, monkeypatch):
    """AD-12/FR-36: slås testmodus av (fra på) i en annen fane etter at feltene er sjekket mot
    testcasene, går analysen til TestKI. Innleggingen bruker samme innlogging til testcasene,
    samtykket og valget av KI, så EkteKI kalles aldri, for samtykket mangler."""
    app, client, kalt = med_nokkel
    lager = app.extensions["oktlager"]
    id_, test_kalt = i_testmodus_til_innleggingen(app, client)
    ekte_sjekk = ruter.sjekk_innlegging

    def sjekk_og_slaa_av(cv, annonse, caser):
        feil = ekte_sjekk(cv, annonse, caser)
        lager.bytt_innlogging(id_, Innlogging(lager.hent(id_).bruker_id, testmodus=False))
        return feil

    monkeypatch.setattr(ruter, "sjekk_innlegging", sjekk_og_slaa_av)
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.location == "/resultat"
    assert lager.hent(id_).testmodus is False
    assert test_kalt == ["nokkelord", "gap"]
    assert kalt == []


def test_fr36_testmodus_av_mellom_samtykket_og_valget_gir_ikke_ekte_ki_i_brevet(
    med_nokkel, monkeypatch
):
    """AD-12/FR-36: det samme for «Lag søknadsbrevet mitt»: slås testmodus av etter at
    samtykket er sjekket, men før KI-en velges, lages brevet av TestKI, og EkteKI kalles
    aldri."""
    app, client, kalt = med_nokkel
    id_, test_kalt = i_testmodus_til_innleggingen(app, client)
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.location == "/resultat"
    slaa_av_etter_samtykket(monkeypatch, app, id_)
    assert client.post("/resultat", data={"handling": "brev"}).location == "/brev"
    assert app.extensions["oktlager"].hent(id_).testmodus is False
    assert test_kalt == ["nokkelord", "gap", "brev"]
    assert kalt == []
    assert soknaden(app, client).samtykke is False
    assert soknaden(app, client).ki_kall == 0


def test_fr28_ki_feil_fra_ekte_ki_vises_paa_innleggingen(med_nokkel):
    """FR-28: gir EkteKI en KIFeil (testmodus av, samtykke gitt), vises feilteksten på
    innleggingen, og søknaden har feltene, men ingen analyse og er ikke opptatt. Kallet som
    feilet, er telt (NFR-11)."""
    app, client, _ = med_nokkel
    app.extensions["ekte_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave="nokkelord")
    soknad = Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, samtykke=True)
    sett_soknad(app, client, soknad)
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.status_code == 200
    html = html_av(svar)
    assert tekster.KI_FEILTEKSTER[KIFeilType.ANNET] in html
    assert tekster.KI_FEIL_BEHOLDT_INNLEGGING in html
    assert soknaden(app, client) == replace(
        soknad, cv=Tekstfelt(CV), annonse=Tekstfelt(ANNONSE), ki_kall=1
    )


@pytest.mark.parametrize(
    ("testmodus", "forventet"),
    [(False, "ekte_ki"), (True, "test_ki")],
    ids=["testmodus-av", "testmodus-paa"],
)
def test_fr32_ki_velger_utgave_ut_fra_testmodus(testmodus, forventet):
    """FR-32/AD-3: ki() gir EkteKI når testmodus er av, og TestKI når den er på."""
    app = app_med_nokkel()
    assert isinstance(app.extensions["ekte_ki"], EkteKI)
    with app.test_request_context():
        assert ki(Innlogging(1, testmodus=testmodus)) is app.extensions[forventet]


def test_fr32_ki_uten_ekte_ki_gir_test_ki(app):
    """FR-32/AD-3: uten nøkkel finnes ingen EkteKI, og ki() gir TestKI, også om testmodus
    skulle være av. Utlogget gir også TestKI."""
    assert app.extensions["ekte_ki"] is None
    with app.test_request_context():
        assert ki(None) is app.extensions["test_ki"]
        assert ki(Innlogging(1, testmodus=False)) is app.extensions["test_ki"]


# --- Samtykket på siden ---


def test_fr36_samtykket_i_begynn_skjemaet_med_linjen_over(med_nokkel):
    """FR-36/UX-DR11: linjen «Teksten din sendes til ekstern KI.» står over boksen «Jeg
    samtykker til bruk av KI», og begge står i «Begynn»-skjemaet før knappen. Uten feil har
    boksen verken aria-invalid, feiltekst eller fokus."""
    _, client, _ = med_nokkel
    html = html_av(client.get("/"))
    innhold = main(html)
    skjema = re.search(r'<form class="begynn"[^>]*>(.*?)</form>', innhold, re.S).group(1)
    assert tekster.SAMTYKKE_LINJE == "Teksten din sendes til ekstern KI."
    assert tekster.SAMTYKKE_ETIKETT == "Jeg samtykker til bruk av KI"
    linje = skjema.index(f'<p class="samtykke-linje">{tekster.SAMTYKKE_LINJE}</p>')
    assert linje < skjema.index('id="samtykke"') < skjema.index('class="stor-knapp"')
    assert re.search(
        r'<label class="avkrysning"><input [^>]*id="samtykke"[^>]*>\s*Jeg samtykker til bruk av KI'
        r"</label>",
        skjema,
    )
    boks = avkrysningsboks(html)
    assert "aria-invalid" not in boks
    assert "aria-describedby" not in boks
    assert 'id="samtykke-feil"' not in html
    assert med_autofocus(html) == []


def test_fr36_info_boksen_har_de_fire_punktene_og_aria(med_nokkel):
    """FR-36/UX-DR11: «i»-knappen har «Hva betyr samtykket?» for skjermlesere,
    aria-expanded og aria-controls, og «i»-boksen (skjult) har de fire punktene med fet
    overskrift. info.js lastes."""
    _, client, _ = med_nokkel
    html = html_av(client.get("/"))
    knapp = next(a for t, a in tagger_i(html) if a.get("class") == "info-knapp")
    assert knapp == {
        "class": "info-knapp",
        "type": "button",
        "aria-label": "Hva betyr samtykket?",
        "aria-expanded": "false",
        "aria-controls": "info-samtykke",
    }
    assert "hidden" in element(html, "info-samtykke")
    boks = re.search(r'<div class="info-boks" id="info-samtykke" hidden>(.*?)</div>', html, re.S)
    punkter = re.findall(r"<p><strong>(.*?)</strong> (.*?)</p>", boks.group(1))
    assert punkter == [
        (
            "Hva samtykker jeg til?",
            "Teksten du legger inn, altså CV, brev og stillingsannonse, sendes til KI-tjenesten "
            "Claude fra selskapet Anthropic.",
        ),
        (
            "Hvorfor sendes teksten?",
            "KI-tjenesten trenger teksten for å finne kravene i annonsen og skrive brevet.",
        ),
        ("Lagres noe?", "Nei. Nettsiden lagrer ingenting du legger inn etter at du logger ut."),
        (
            "Personopplysninger:",
            "Vi anbefaler at du fjerner adresse, telefonnummer og fødselsdato fra CV-en først. "
            "Det er ditt valg.",
        ),
    ]
    assert "/static/js/info.js" in html


def test_fr36_info_js_lastes_ikke_i_testmodus(innlogget_client):
    """FR-36: i testmodus finnes ingen «i»-knapp på startsiden, og info.js lastes ikke."""
    html = html_av(innlogget_client.get("/"))
    assert "info.js" not in html
    assert "info-knapp" not in html


# --- KI-merknaden (FR-35) ---


@pytest.mark.parametrize("side", ["/", "/modus"])
def test_fr35_ki_merknaden_i_hjornraden_naar_testmodus_er_av(med_nokkel, side):
    """FR-35/UX-DR3: når testmodus er av, står «ⓘ Teksten behandles av ekstern KI» i
    hjørneraden før «Logg ut» (til venstre). ⓘ er skjult for skjermlesere."""
    app, client, _ = med_nokkel
    sett_soknad(app, client, Soknad(steg=Steg.MODUS, samtykke=True))
    rad = footer(html_av(client.get(side)))
    assert tekster.KI_MERKNAD == "Teksten behandles av ekstern KI"
    merknad = (
        '<p class="ki-merknad"><span aria-hidden="true">ⓘ</span> '
        "Teksten behandles av ekstern KI</p>"
    )
    assert merknad in rad
    assert rad.index('class="ki-merknad"') < rad.index('class="utlogging"')


@pytest.mark.parametrize("side", ["/", "/modus"])
def test_fr35_ingen_ki_merknad_i_testmodus(app, innlogget_client, side):
    """FR-35: i testmodus er KI-merknaden skjult."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.MODUS))
    html = html_av(innlogget_client.get(side))
    assert "ki-merknad" not in html
    assert tekster.KI_MERKNAD not in html


@pytest.mark.parametrize("side", ["/logg-inn", "/registrer"])
def test_fr35_ingen_ki_merknad_uten_innlogging(client, side):
    """FR-35: innloggingen og registreringen har ingen hjørnerad og ingen KI-merknad."""
    assert "ki-merknad" not in html_av(client.get(side))


# --- CSS (testene tegner ikke siden) ---


def test_ux_dr10_avkrysningsboksen_er_22_px_uten_fast_hoyde():
    """UX-DR10: boksen er 22 × 22 px (bredde og aspect-ratio, ingen fast høyde), med ramme i
    primary og primary-bakgrunn når den er krysset av."""
    css = STIL.read_text(encoding="utf-8")
    boks = css_blokk(css, ".avkrysning input")
    for verdi in ("width: 22px", "min-height: 22px", "aspect-ratio: 1", "var(--primary)"):
        assert verdi in boks
    assert "var(--primary)" in css_blokk(css, ".avkrysning input:checked")


def test_ux_dr10_rod_ramme_ved_feil_og_fokusring_ved_focus():
    """UX-DR10: ved feil får boksen rød ramme (2 px error med 2 px avstand). Boksen får fokus
    fra autofocus etter et museklikk, så ringen vises for :focus, ikke bare :focus-visible."""
    css = STIL.read_text(encoding="utf-8")
    feil = css_blokk(css, '.avkrysning input[aria-invalid="true"]')
    assert "outline: 2px solid var(--error)" in feil
    assert "outline-offset: 2px" in feil
    fokus = css_blokk(css, ".avkrysning input:focus")
    assert "outline: 3px solid var(--focus-ring)" in fokus
    # Fokusregelen står etter feilregelen, så ringen vinner når boksen har fokus.
    assert css.index(".avkrysning input:focus {") > css.index(
        '.avkrysning input[aria-invalid="true"] {'
    )


def test_fr35_ki_merknaden_er_liten_dempet_og_logg_ut_til_hoyre():
    """FR-35/UX-DR3: KI-merknaden har caption-størrelse og dempet farge. «Logg ut» har
    margin-left: auto, så merknaden står til venstre."""
    css = STIL.read_text(encoding="utf-8")
    merknad = css_blokk(css, ".ki-merknad")
    assert "var(--size-caption)" in merknad
    assert "var(--text-muted)" in merknad
    assert "margin: 0 0 0 auto" in css_blokk(css, ".utlogging")


def test_nfr6_hoykontrast_for_feilrammen_info_boksen_og_ki_merknaden():
    """NFR-6/UX-DR10: i høykontrastmodus får feilrammen en tykkere ramme i CanvasText,
    «i»-boksen en ramme og KI-merknaden vanlig tekstfarge."""
    css = STIL.read_text(encoding="utf-8")
    hoykontrast = re.search(r"@media \(forced-colors: active\)\s*\{(.*?)\n\}", css, re.S).group(1)
    feil = re.search(
        r'\.avkrysning input\[aria-invalid="true"\] \{(.*?)\}', hoykontrast, re.S
    ).group(1)
    assert "outline: 2px solid CanvasText" in feil
    assert "border-width: 3px" in feil
    assert re.search(r"\.info-boks \{\s*border: 1px solid CanvasText;", hoykontrast)
    assert re.search(r"\.ki-merknad \{\s*color: CanvasText;", hoykontrast)
    assert re.search(r"\.avkrysning input:focus \{\s*outline: 3px solid Highlight;", hoykontrast)
