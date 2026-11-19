"""Tester for «Lag søknadsbrevet mitt» og brevsiden (FR-21, FR-22, FR-26, FR-27, FR-28, NFR-4,
NFR-6, NFR-7, AD-1, AD-8, UX-DR7, UX-DR14). Story 3.1. «Oppdater søknadsbrevet mitt» og
brevsiden i Korrektur kom i story 5.2.1 (FR-23, FR-24, FR-36, FR-37)."""

import html as html_modul
import json
import re
import shutil

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE, TestKI
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.ki_svar import kontroller, korrigert_brev
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import ruter, tekster
from soknad.web.innlogging import OKT_ID
from tests.web.hjelpere import (
    ANNONSE,
    CASE,
    CV,
    EGET_BREV,
    GAP_SVAR,
    NOKKELORD_SVAR,
    STIL,
    FeilendeKI,
    brevtekst,
    css_blokk,
    element,
    footer,
    html_av,
    korrektur_brev,
    korrektur_svar,
    korrektur_testki,
    main,
    med_autofocus,
    okt_id,
    sett_soknad,
    soknaden,
    tagger_i,
)

# Fiksturene paa_resultat og paa_brev står i conftest.py.

BREV_SVAR = json.loads((CASE / "ki-svar" / "brev-1.json").read_text(encoding="utf-8"))
BREV_SVAR_2 = json.loads((CASE / "ki-svar" / "brev-2.json").read_text(encoding="utf-8"))


def lag_brev(client, handling="brev"):
    data = {} if handling is None else {"handling": handling}
    return client.post("/resultat", data=data)


def feilboks(html):
    return re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)


def avsnitt(html):
    """Teksten i hvert <p> i brevarket, med HTML-escapingen fjernet, uten de skjulte tekstene
    og uten «Du skrev» i Korrektur (story 5.3)."""
    return brevtekst(html)


# Den første linjen i det egne brevet i case 1, som korrektur_svar(1) har endret.
_LINJE_1 = "Søknad på jobb som junior utvikler"


def forklaring(html):
    """Den synlige teksten i hver forklaringsboks over brevet i Korrektur (story 5.3)."""
    bokser = re.findall(r'<p class="korrektur-forklaring">(.*?)</p>', html, re.S)
    return [
        html_modul.unescape(re.sub(r'<span class="skjult">.*?</span>', "", boks)).strip()
        for boks in bokser
    ]


def knapper(html):
    """Attributtene til hver endrede setning (et <span> med role="button") i brevet, i
    rekkefølge."""
    return [a for t, a in tagger_i(html) if t == "span" and a.get("class") == "endret-setning"]


def du_skrev(html, id_):
    """De gamle setningene i «Du skrev» med denne id-en, én per linje. Overskriften må være
    «Du skrev»."""
    treff = re.search(
        rf'<span class="du-skrev" id="{id_}" hidden>'
        r'<span class="du-skrev-overskrift">(.*?)</span>((?:<span>.*?</span>)*)</span>',
        html,
    )
    assert treff.group(1) == tekster.DU_SKREV
    return [html_modul.unescape(s) for s in re.findall(r"<span>(.*?)</span>", treff.group(2))]


def fjernet_linje(html):
    """Teksten i linjen om fjernede setninger under brevet, eller None."""
    treff = re.search(r'<p class="fjernet-linje">(.*?)</p>', html, re.S)
    return None if treff is None else treff.group(1)


def paa_brevsiden_med(app, client, *setninger):
    """Brevsiden i Korrektur for et forbedret brev med disse setningene, i formen fra
    kontroller()."""
    korrektur = {"setninger": list(setninger)}
    sett_soknad(app, client, Soknad(steg=Steg.BREV, modus=Modus.KORREKTUR, korrektur=korrektur))
    return html_av(client.get("/brev"))


def _setning(ny, gammel, nytt_avsnitt=False):
    return {"ny": ny, "gammel": gammel, "nytt_avsnitt": nytt_avsnitt}


class SpionKI:
    """Samme svar som TestKI, men ser om søknaden er opptatt under brevkallet. Er under satt,
    kalles den først i kallet (for eksempel startsiden i en annen fane). Er unntak satt,
    kastes det i stedet for svaret."""

    def __init__(self, test_ki, app, client, under=None, unntak=None):
        self.test_ki = test_ki
        self.caser = test_ki.caser
        self.app = app
        self.client = client
        self.under = under
        self.unntak = unntak
        self.opptatt_under = []

    def brev(self, cv, annonse, forslag):
        if self.under is not None:
            self.under()
        # Etter utlogging finnes ingen søknad, og da skrives None.
        self.opptatt_under.append(getattr(soknaden(self.app, self.client), "opptatt", None))
        if self.unntak is not None:
            raise self.unntak
        return self.test_ki.brev(cv, annonse, forslag)


# --- Matrisen ---


def test_fr22_brevet_lages_og_sender_til_brevsiden(app, paa_resultat):
    """FR-21/FR-22/AD-8: POST handling=brev lagrer brev-1.json i søknaden, flytter steget til
    brev og sender til /brev. Søknaden er ikke opptatt etterpå."""
    for_ = soknaden(app, paa_resultat)
    assert for_.brev is None
    svar = lag_brev(paa_resultat)
    assert svar.status_code == 302
    assert svar.location == "/brev"
    soknad = soknaden(app, paa_resultat)
    assert soknad.brev == BREV_SVAR
    assert soknad.steg == Steg.BREV
    assert soknad.opptatt is False
    assert paa_resultat.get("/brev").status_code == 200


def test_fr22_brevet_hentes_med_cv_annonse_og_forslag_1(app, paa_resultat):
    """FR-22: KI-en får CV-en og annonsen fra søknaden og forslag 1, og kalles én gang."""
    kall = []

    class LoggendeKI:
        caser = app.extensions["test_ki"].caser

        def brev(self, cv, annonse, forslag):
            kall.append((cv, annonse, forslag))
            return BREV_SVAR

    app.extensions["test_ki"] = LoggendeKI()
    lag_brev(paa_resultat)
    assert kall == [(CV, ANNONSE, 1)]


def test_fr27_opptatt_er_sann_under_brevkallet(app, paa_resultat):
    """FR-27/AD-8: søknaden er opptatt i øktlageret mens brevet lages."""
    spion = SpionKI(app.extensions["test_ki"], app, paa_resultat)
    app.extensions["test_ki"] = spion
    lag_brev(paa_resultat)
    assert spion.opptatt_under == [True]


@pytest.mark.parametrize("feiltype", list(KIFeilType))
def test_fr28_ki_feil_gir_resultatsiden_med_feilboksen(app, paa_resultat, feiltype):
    """FR-28/UX-DR7: en KIFeil gir resultatsiden på nytt (200, ingen redirect) med feilteksten
    for typen, «Resultatet og det du har lagt inn, er ikke borte.» og «Prøv på nytt».
    Søknaden er uendret, også steget, og ikke opptatt."""
    for_ = soknaden(app, paa_resultat)
    app.extensions["test_ki"] = FeilendeKI(
        app.extensions["test_ki"], oppgave="brev", feiltype=feiltype
    )
    svar = lag_brev(paa_resultat)
    assert svar.status_code == 200
    assert svar.location is None
    html = html_av(svar)
    tekst = tekster.ki_feiltekst(KIFeil(feiltype))
    assert re.search(
        rf'\s*<p class="feilboks-overskrift">{re.escape(tekst)}</p>'
        r'\s*<p class="feilboks-tekst">Resultatet og det du har lagt inn, er ikke borte\.</p>'
        r'\s*<p class="feilboks-knapp">\s*<button class="hovedknapp"[^>]*>Prøv på nytt</button>',
        feilboks(html),
    )
    assert "<a " not in feilboks(html)
    assert 'role="alert"' not in html
    # Resultatet står fortsatt på siden.
    assert 'id="gap-dekker"' in html
    soknad = soknaden(app, paa_resultat)
    assert soknad == for_
    assert soknad.steg == Steg.RESULTAT
    assert soknad.brev is None
    assert soknad.opptatt is False


def test_ux_dr7_ki_feil_gir_fokus_til_feilboksen(app, paa_resultat):
    """UX-DR7/UX-DR14: ved KI-feil har feilboksen autofocus og tabindex="-1", og h1 har ikke
    autofocus. Uten feil har bare h1 autofocus."""
    assert med_autofocus(html_av(paa_resultat.get("/resultat"))) == [None]
    h1 = next(a for t, a in tagger_i(html_av(paa_resultat.get("/resultat"))) if t == "h1")
    assert "autofocus" in h1
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave="brev")
    html = html_av(lag_brev(paa_resultat))
    assert med_autofocus(html) == ["feilboks"]
    assert element(html, "feilboks")["tabindex"] == "-1"
    assert html.index('id="feilboks"') < html.index('id="gap-dekker"')


@pytest.mark.parametrize(
    "innhold",
    [
        '{"avsnitt": [], "navn": "Sara"}',
        '{"avsnitt": ["  "], "navn": null}',
        '{"avsnitt": ["Med vennlig hilsen", "Sara Eksempel"], "navn": "Sara Eksempel"}',
    ],
)
def test_fr28_tomt_brev_gir_feilboksen(app, paa_resultat, tmp_path, innhold):
    """FR-28: et tomt brev (ingen avsnitt, bare mellomrom eller bare hilsen og navn) gir
    KIFeil(ubrukelig_svar) og resultatsiden med feilboksen, aldri en tom brevside."""
    kopi = tmp_path / "testdata"
    shutil.copytree(TESTDATA_MAPPE, kopi)
    (kopi / "case-1-utvikler" / "ki-svar" / "brev-1.json").write_text(innhold, encoding="utf-8")
    app.extensions["test_ki"] = TestKI(kopi)
    svar = lag_brev(paa_resultat)
    assert svar.status_code == 200
    tekst = tekster.ki_feiltekst(KIFeil(KIFeilType.UBRUKELIG_SVAR))
    assert tekst in feilboks(html_av(svar))
    soknad = soknaden(app, paa_resultat)
    assert soknad.brev is None
    assert soknad.steg == Steg.RESULTAT
    assert paa_resultat.get("/brev").location == "/resultat"


@pytest.mark.parametrize(("steg", "side"), [(Steg.RESULTAT, "/resultat"), (Steg.BREV, "/brev")])
@pytest.mark.parametrize("handling", ["brev", "noe", None])
def test_fr27_post_mens_opptatt_sender_til_steget(app, paa_resultat, steg, side, handling):
    """FR-27/AD-8: kommer en POST mens søknaden er opptatt, sendes brukeren til siden for
    steget. KI-en kalles ikke, og søknaden er uendret."""
    soknad = Soknad(
        steg=steg,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        nokkelord=("Python",),
        gap={"dekker": ["Python"], "mangler": []},
        brev=BREV_SVAR if steg == Steg.BREV else None,
        opptatt=True,
    )
    sett_soknad(app, paa_resultat, soknad)
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    svar = lag_brev(paa_resultat, handling)
    assert svar.status_code == 302
    assert svar.location == side
    assert kalt == []
    assert soknaden(app, paa_resultat) is soknad


@pytest.mark.parametrize(
    ("steg", "side"),
    [
        (Steg.START, "/"),
        (Steg.MODUS, "/modus"),
        (Steg.INNLEGGING, "/innlegging"),
        (Steg.RESULTAT, "/resultat"),
    ],
)
def test_fr22_brevsiden_for_tidlig_sender_til_steget(app, innlogget_client, steg, side):
    """FR-22/AD-8: før brevet er laget, sendes /brev til siden for steget, og søknaden er
    uendret."""
    soknad = Soknad(steg=steg)
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.get("/brev")
    assert svar.status_code == 302
    assert svar.location == side
    assert soknaden(app, innlogget_client) is soknad


def test_fr22_brevsiden_uten_brev_sender_til_resultatsiden(app, innlogget_client):
    """FR-22/AD-8: står søknaden på steg brev uten brev, sendes /brev til /resultat."""
    soknad = Soknad(
        steg=Steg.BREV,
        cv=Tekstfelt("cv"),
        nokkelord=("cv",),
        gap={"dekker": ["cv"], "mangler": []},
    )
    sett_soknad(app, innlogget_client, soknad)
    assert innlogget_client.get("/brev").location == "/resultat"


@pytest.mark.parametrize("steg", [Steg.RESULTAT, Steg.BREV])
@pytest.mark.parametrize(
    ("nokkelord", "gap"),
    [(None, {"dekker": ["cv"], "mangler": []}), (("cv",), None), (None, None)],
)
def test_fr20_resultatsiden_uten_analyse_sender_til_innleggingen(
    app, innlogget_client, steg, nokkelord, gap
):
    """FR-20/AD-8 (retrospektiven for Epic 2): mangler analysen, sender både GET og POST
    /resultat til /innlegging, uten KI-kall og uten at søknaden endres."""
    soknad = Soknad(steg=steg, cv=Tekstfelt("cv"), nokkelord=nokkelord, gap=gap)
    sett_soknad(app, innlogget_client, soknad)
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    assert innlogget_client.get("/resultat").location == "/innlegging"
    assert lag_brev(innlogget_client).location == "/innlegging"
    assert kalt == []
    assert soknaden(app, innlogget_client) is soknad


@pytest.mark.parametrize("handling", [None, "noe", "sjekk"])
def test_fr21_ukjent_handling_gir_400_og_uendret_soknad(app, paa_resultat, handling):
    """FR-21/AD-8: en POST uten handling=brev gir resultatsiden med 400. KI-en kalles ikke,
    og søknaden er uendret."""
    soknad = soknaden(app, paa_resultat)
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    svar = lag_brev(paa_resultat, handling)
    assert svar.status_code == 400
    assert 'id="gap-dekker"' in html_av(svar)
    assert kalt == []
    assert soknaden(app, paa_resultat) is soknad


# --- Uventede ting under kallet ---


def test_ad8_startsiden_midt_i_brevkallet_vinner(app, paa_resultat):
    """AD-8/FR-27: åpnes startsiden i en annen fane mens brevet lages, blir den nye søknaden
    stående, og brevet kastes."""
    startsiden = []
    app.extensions["test_ki"] = SpionKI(
        app.extensions["test_ki"],
        app,
        paa_resultat,
        under=lambda: startsiden.append(paa_resultat.get("/").status_code),
    )
    lag_brev(paa_resultat)
    assert startsiden == [200]
    assert soknaden(app, paa_resultat) == Soknad()


def test_fr7_utlogget_midt_i_brevkallet_gir_innloggingen(app, paa_resultat):
    """FR-7/AD-8: logges brukeren ut i en annen fane mens brevet lages, gir POST-en ingen
    feilside. Neste side sender til innloggingen, og ingen søknad blir liggende igjen for den
    gamle økt-id-en."""
    gammel_id = okt_id(paa_resultat)
    utlogging = []
    app.extensions["test_ki"] = SpionKI(
        app.extensions["test_ki"],
        app,
        paa_resultat,
        under=lambda: utlogging.append(paa_resultat.post("/logg-ut").status_code),
    )
    svar = lag_brev(paa_resultat)
    assert utlogging == [302]
    assert svar.status_code == 302
    neste = paa_resultat.get(svar.location)
    assert neste.location == "/logg-inn?ikke_innlogget=1"
    assert app.extensions["oktlager"].hent_soknad(gammel_id) is None


def test_fr7_utlogget_for_brevkallet_gir_innloggingen(app, paa_resultat, monkeypatch):
    """FR-7/AD-8: logges brukeren ut i en annen fane etter login_required, men før «Lag
    søknadsbrevet mitt» henter brevet, sendes hen til innloggingen med «Du må logge inn
    først». Ingen feilside og ingen KI-feil, cookien tømmes, KI-en kalles ikke, og ingen
    søknad lagres for den gamle økt-id-en."""
    lager = app.extensions["oktlager"]
    id_ = okt_id(paa_resultat)
    ekte_hent = ruter.gjeldende_soknad

    def hent_og_logg_ut():
        soknad = ekte_hent()
        lager.slett(id_)
        return soknad

    monkeypatch.setattr(ruter, "gjeldende_soknad", hent_og_logg_ut)
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    svar = lag_brev(paa_resultat)
    assert svar.status_code == 302
    assert svar.location == "/logg-inn?ikke_innlogget=1"
    assert okt_id(paa_resultat) is None
    assert kalt == []
    assert lager.hent_soknad(id_) is None


def test_fr27_uventet_feil_gir_opptatt_usann(app, paa_resultat):
    """FR-27/AD-8: et uventet unntak under brevkallet gir søknaden fra før, ikke opptatt."""
    for_ = soknaden(app, paa_resultat)
    app.extensions["test_ki"] = SpionKI(
        app.extensions["test_ki"], app, paa_resultat, unntak=RuntimeError("uventet")
    )
    with pytest.raises(RuntimeError):
        lag_brev(paa_resultat)
    assert soknaden(app, paa_resultat) == for_


# --- Resultatsiden: knappen ---


def test_fr21_knappene_nederst_tilbake_til_venstre_lag_brev_til_hoyre(paa_resultat):
    """FR-21/UX-DR4: nederst står «Tilbake» (lenke) og så hovedknappen «Lag søknadsbrevet
    mitt» i en knapperad med mellomrom, inne i skjemaet som sender POST til /resultat. Brevet
    er ikke laget ennå."""
    innhold = main(html_av(paa_resultat.get("/resultat")))
    skjema = re.search(
        r'<form method="post" action="/resultat" id="resultat-skjema">(.*?)</form>', innhold, re.S
    )
    assert skjema
    rad = re.search(r'<div class="knapperad mellomrom">(.*?)</div>', skjema.group(1), re.S)
    assert re.fullmatch(
        r'\s*<a class="sekundaerknapp" href="/innlegging">Tilbake</a>'
        r'\s*<button class="hovedknapp"[^>]*>Lag søknadsbrevet mitt</button>\s*',
        rad.group(1),
    )
    assert innhold.index('id="ats"') < innhold.index('id="resultat-skjema"')


def test_fr27_knappen_viser_ventetegnet_med_brevteksten(paa_resultat):
    """FR-27/UX-DR14: knappen sender handling=brev og har data-vente med «Vi lager brevet
    ditt – det kan ta en liten stund.». Ventetegnet og vente.js er på siden."""
    html = html_av(paa_resultat.get("/resultat"))
    knapp = next(a for t, a in tagger_i(html) if t == "button" and a.get("value") == "brev")
    assert knapp == {
        "class": "hovedknapp",
        "type": "submit",
        "name": "handling",
        "value": "brev",
        "data-vente": "Vi lager brevet ditt – det kan ta en liten stund.",
    }
    assert "js/vente.js" in html
    assert element(html, "vente-status")["role"] == "status"
    assert "hidden" in element(html, "ventetegn")
    assert 'id="vente"' not in main(html)


def test_fr28_prov_paa_nytt_sender_skjemaet_som_lag_brev(app, paa_resultat):
    """FR-27/FR-28: «Prøv på nytt» står utenfor skjemaet, men sender det med form= og
    handling=brev, og viser ventetegnet med samme ventesetning. Virker KI-en igjen, gir den
    brevsiden."""
    ekte = app.extensions["test_ki"]
    app.extensions["test_ki"] = FeilendeKI(ekte, oppgave="brev")
    html = html_av(lag_brev(paa_resultat))
    knapp = next(a for t, a in tagger_i(html) if t == "button" and a.get("form"))
    assert knapp == {
        "class": "hovedknapp",
        "type": "submit",
        "form": "resultat-skjema",
        "name": "handling",
        "value": "brev",
        "data-vente": tekster.VENTE_BREV,
    }
    vente = [a["data-vente"] for t, a in tagger_i(html) if "data-vente" in a]
    assert vente == [tekster.VENTE_BREV] * 2
    app.extensions["test_ki"] = ekte
    svar = paa_resultat.post("/resultat", data={knapp["name"]: knapp["value"]})
    assert svar.location == "/brev"
    assert soknaden(app, paa_resultat).brev == BREV_SVAR


def test_fr22_lag_brev_igjen_fra_resultatsiden_gir_brevsiden(app, paa_brev):
    """FR-22/FR-25/AD-8: tilbake til resultatsiden (nettleserens tilbakeknapp) og «Lag
    søknadsbrevet mitt» igjen gir brevsiden på nytt, og steget er fortsatt brev. Brevet er
    neste forslag (story 7.1, retro 3), altså brev-2.json."""
    assert paa_brev.get("/resultat").status_code == 200
    assert lag_brev(paa_brev).location == "/brev"
    soknad = soknaden(app, paa_brev)
    assert soknad.steg == Steg.BREV
    assert soknad.forslag == 2
    assert soknad.brev == BREV_SVAR_2
    assert paa_brev.get("/brev").status_code == 200


# --- Brevsiden ---


def test_fr22_brevsiden_har_overskrift_tittel_og_fokus(paa_brev):
    """FR-22/NFR-6/UX-DR14: én h1 «Din ferdigstilte søknad!» med tabindex="-1" og autofocus,
    og sidetittelen «Søknadsbrev – Søknadsassistenten»."""
    html = html_av(paa_brev.get("/brev"))
    assert "<title>Søknadsbrev – Søknadsassistenten</title>" in html
    h1 = [a for t, a in tagger_i(html) if t == "h1"]
    assert h1 == [{"class": "brev-overskrift", "tabindex": "-1", "autofocus": None}]
    assert re.search(r"<h1[^>]*>Din ferdigstilte søknad!</h1>", html)
    # «Avbryt» i vinduet «Nytt forslag» har også autofocus, men den gjelder bare når vinduet
    # åpnes (story 7.1).
    assert med_autofocus(html) == [None, "nytt-forslag-avbryt"]


def test_fr22_ett_avsnitt_per_element(paa_brev):
    """FR-22: brevarket har ett <p> per element i avsnitt, i samme rekkefølge, og så
    «Med vennlig hilsen» og navnet som to egne avsnitt."""
    assert avsnitt(html_av(paa_brev.get("/brev"))) == [
        *BREV_SVAR["avsnitt"],
        "Med vennlig hilsen",
        BREV_SVAR["navn"],
    ]


@pytest.mark.parametrize("case", sorted(TESTDATA_MAPPE.glob("case-*")), ids=lambda c: c.name)
def test_fr22_brevet_i_testmodus_slutter_med_hilsen_og_navn(app, innlogget_client, case):
    """FR-22: for hvert testcase viser brevsiden avsnittene fra brev-1.json og så «Med vennlig
    hilsen» og navnet fra CV-en (den første linjen), slik brevet var før navnet fikk et eget
    felt. Hilsenen står bare én gang."""
    brev = kontroller("brev", (case / "ki-svar" / "brev-1.json").read_text(encoding="utf-8"))
    navn = (case / "cv.txt").read_text(encoding="utf-8").splitlines()[0]
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.BREV, brev=brev))
    vist = avsnitt(html_av(innlogget_client.get("/brev")))
    assert vist == [*brev["avsnitt"], "Med vennlig hilsen", navn]
    assert vist.count("Med vennlig hilsen") == 1


def test_fr22_brevet_uten_navn_slutter_med_hilsenen(app, innlogget_client):
    """FR-22: uten navn i CV-en slutter brevet på siden med «Med vennlig hilsen»."""
    brev = {"avsnitt": ["Søknad på stillingen", "Jeg søker."], "navn": None}
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.BREV, brev=brev))
    vist = avsnitt(html_av(innlogget_client.get("/brev")))
    assert vist == ["Søknad på stillingen", "Jeg søker.", "Med vennlig hilsen"]


def test_nfr6_brevteksten_escapes(app, innlogget_client):
    """NFR-6: tekst fra KI-en escapes, også navnet, så den aldri blir HTML."""
    brev = {"avsnitt": ["<b>fet</b> & <script>x</script>"], "navn": "<i>Sara</i>"}
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.BREV, brev=brev))
    html = main(html_av(innlogget_client.get("/brev")))
    assert "<b>" not in html
    assert "<i>" not in html
    assert "<script>" not in html
    assert "&lt;b&gt;fet&lt;/b&gt; &amp; &lt;script&gt;" in html
    assert avsnitt(html) == [*brev["avsnitt"], "Med vennlig hilsen", "<i>Sara</i>"]


def test_fr26_brevet_kan_ikke_redigeres_og_har_ingen_tilbake(paa_brev):
    """FR-26: brevsiden har ingen «Tilbake», ingen tekstfelt og ingen contenteditable. I
    <main> er det eneste skjemaet og den eneste knappen «Nytt forslag» (story 7.1), og de
    eneste lenkene er «Last ned som Word» (story 3.2) og «Last ned som PDF» (story 7.2)."""
    html = html_av(paa_brev.get("/brev"))
    innhold = main(html)
    assert tekster.TILBAKE_KNAPP not in innhold
    assert "contenteditable" not in html
    tagger = [(t, a.get("id")) for t, a in tagger_i(innhold)]
    assert {t for t, _ in tagger}.isdisjoint({"textarea", "input"})
    assert [a for a in tagger if a[0] in ("form", "button")] == [
        ("form", "nytt-forslag-skjema"),
        ("button", "nytt-forslag"),
    ]
    lenker = [a["href"] for t, a in tagger_i(innhold) if t == "a"]
    assert lenker == ["/last-ned/docx", "/last-ned/pdf"]


def test_fr22_brevsiden_har_logg_ut_og_ingen_ventetegn(paa_brev):
    """FR-22/FR-6/NFR-4: «Logg ut» står i hjørneraden: nøyaktig ett skjema der, til
    /logg-ut. Vinduet etter nedlasting (story 3.3) har også et skjema til /logg-ut, så
    testen ser bare på <footer>. «Nytt forslag» er et KI-kall (story 7.1), så brevsiden har
    ventetegnet, utenfor <main>."""
    html = html_av(paa_brev.get("/brev"))
    hjornerad = footer(html)
    skjemaer = [a for t, a in tagger_i(hjornerad) if t == "form"]
    assert skjemaer == [{"class": "utlogging", "method": "post", "action": "/logg-ut"}]
    assert tekster.LOGG_UT_KNAPP in hjornerad
    assert 'id="vente"' in html
    assert 'id="vente"' not in main(html)


def test_nfr4_brevet_bare_i_minnet(paa_brev):
    """NFR-4/AD-7: cookien har bare økt-id-en, og brevsiden lagres ikke i nettleseren."""
    svar = paa_brev.get("/brev")
    assert svar.headers["Cache-Control"] == "no-store"
    with paa_brev.session_transaction() as okt:
        assert set(okt) == {OKT_ID}


# --- Nullstilling ---


def test_fr22_endret_cv_gjor_brevet_borte(app, paa_brev):
    """FR-19/FR-22/AD-8: endres CV-en, er det gamle brevet borte, og /brev sender til
    innleggingen."""
    paa_brev.post("/innlegging", data={"cv": "Ny CV", "annonse": ANNONSE, "handling": "tilbake"})
    soknad = soknaden(app, paa_brev)
    assert soknad.brev is None
    assert soknad.steg == Steg.INNLEGGING
    assert paa_brev.get("/brev").location == "/innlegging"


def test_fr22_modus_paa_nytt_gjor_brevet_borte(app, paa_brev):
    """FR-20/FR-22/AD-8: velges modus på nytt, er det gamle brevet borte."""
    paa_brev.post("/modus", data={"modus": "full_generering"})
    soknad = soknaden(app, paa_brev)
    assert soknad.brev is None
    assert soknad.steg == Steg.INNLEGGING


# --- Korrektur (story 5.2.1) ---


def test_fr23_oppdater_gir_brevsiden_med_det_forbedrede_brevet(app, paa_brev_korrektur):
    """FR-23/FR-24/AD-8: «Oppdater søknadsbrevet mitt» i Korrektur lagrer det forbedrede
    brevet (korrektur-1.json) og sender til brevsiden. Brevet i Full generering er ikke laget,
    steget er brev, og søknaden er ikke opptatt."""
    soknad = soknaden(app, paa_brev_korrektur)
    assert soknad.korrektur == korrektur_svar(1)
    assert soknad.brev is None
    assert soknad.steg == Steg.BREV
    assert soknad.opptatt is False
    assert paa_brev_korrektur.get("/brev").status_code == 200


def test_fr23_brevsiden_i_korrektur_har_overskriften_brevet_og_markeringene(
    paa_brev_korrektur,
):
    """FR-23/FR-30 (story 5.2.1 og 5.3): brevsiden i Korrektur har h1 «Din oppdaterte søknad er
    ferdig!» med fokus, og brevet er alle ny som ikke er null, ett avsnitt per avsnitt. «Hei!»
    er fjernet, og hilsenen og navnet står én gang, slik brukeren skrev dem. Den første linjen
    i brevet («Søknad på …») er endret: forklaringen står over brevet, den første linjen er en
    lukket knapp med «Du skrev» og den gamle linjen, og «1 setning er fjernet.» står under
    brevet. De uendrede setningene er vanlig tekst, og endringer.js lastes."""
    html = html_av(paa_brev_korrektur.get("/brev"))
    h1 = [a for t, a in tagger_i(html) if t == "h1"]
    assert h1 == [{"class": "brev-overskrift", "tabindex": "-1", "autofocus": None}]
    assert re.search(r"<h1[^>]*>Din oppdaterte søknad er ferdig!</h1>", html)
    assert tekster.BREV_OVERSKRIFT not in html
    vist = avsnitt(html)
    assert vist == korrektur_brev(1)
    assert "Hei!" not in vist
    assert vist[-2:] == ["Med vennlig hilsen", "Sara Eksempel"]
    assert vist.count("Med vennlig hilsen") == 1
    assert forklaring(html) == [tekster.KORREKTUR_FORKLARING]
    assert (
        f'<p class="korrektur-forklaring">{tekster.KORREKTUR_FORKLARING} '
        f'<span class="skjult">{tekster.KORREKTUR_FORKLARING_SKJERMLESER}</span></p>'
    ) in html
    assert html.index('class="korrektur-forklaring"') < html.index('<article class="brevark">')
    assert (
        f'<span class="skjult">{tekster.ENDRET_SETNING_SKJERMLESER} </span>'
        f"{korrektur_brev(1)[0]}</span>"
    ) in html
    assert knapper(html) == [
        {
            "class": "endret-setning",
            "role": "button",
            "tabindex": "0",
            "aria-expanded": "false",
            "aria-controls": "du-skrev-1-1",
        }
    ]
    assert du_skrev(html, "du-skrev-1-1") == [_LINJE_1]
    assert "hidden" in element(html, "du-skrev-1-1")
    assert fjernet_linje(html) == "1 setning er fjernet."
    assert "js/endringer.js" in html


def test_fr23_korrektur_uten_hilsen_legger_ikke_til_hilsen(app, innlogget_client):
    """FR-23 (bestemt av Kristine 15. november 2026): mangler hilsenen og navnet i det egne
    brevet, legger nettsiden ikke til noe i Korrektur."""
    korrektur = {
        "setninger": [
            {"ny": "Søknad på stillingen", "gammel": ["Søknad på jobb"], "nytt_avsnitt": True},
            {"ny": "Jeg søker.", "gammel": ["Jeg søker"], "nytt_avsnitt": True},
        ]
    }
    soknad = Soknad(steg=Steg.BREV, modus=Modus.KORREKTUR, korrektur=korrektur)
    sett_soknad(app, innlogget_client, soknad)
    assert avsnitt(html_av(innlogget_client.get("/brev"))) == ["Søknad på stillingen", "Jeg søker."]


def test_fr37_korrektur_far_cv_annonse_eget_brev_og_forslag_1(app, paa_resultat_korrektur):
    """FR-23/FR-37: KI-en får CV-en, annonsen og det egne brevet fra søknaden og forslag 1, og
    kalles én gang. brev kalles ikke."""
    kall = []

    class LoggendeKI:
        caser = app.extensions["test_ki"].caser

        def brev(self, cv, annonse, forslag):
            raise AssertionError("brev skal ikke kalles i Korrektur")

        def korrektur(self, cv, annonse, eget_brev, forslag):
            kall.append((cv, annonse, eget_brev, forslag))
            return korrektur_svar(1)

    app.extensions["test_ki"] = LoggendeKI()
    assert lag_brev(paa_resultat_korrektur).location == "/brev"
    assert kall == [(CV, ANNONSE, EGET_BREV, 1)]


@pytest.mark.parametrize(
    "innhold",
    [
        # Alle ny er null
        {"setninger": [{**s, "ny": None} for s in korrektur_svar(1)["setninger"]]},
        # gammel stemmer ikke med det egne brevet: en setning mangler
        {"setninger": korrektur_svar(1)["setninger"][:-1]},
        # Feil form
        {"setninger": []},
        {"setninger": [{"ny": "Hei", "gammel": ["Hei"], "nytt_avsnitt": 1}]},
        "ikke json",
    ],
)
def test_fr28_ubrukelig_korrektur_gir_feilboksen(app, tmp_path, paa_resultat_korrektur, innhold):
    """FR-28 (story 5.2.1): alle ny null, gammel som ikke stemmer med det egne brevet, eller
    feil form gir KI-feilboksen på resultatsiden (200, ingen redirect), og resultatet og det
    brukeren har lagt inn, er der fortsatt. Søknaden er uendret."""
    app.extensions["test_ki"] = korrektur_testki(tmp_path, svar1=innhold)
    for_ = soknaden(app, paa_resultat_korrektur)
    svar = lag_brev(paa_resultat_korrektur)
    assert svar.status_code == 200
    assert svar.location is None
    html = html_av(svar)
    assert tekster.ki_feiltekst(KIFeil(KIFeilType.UBRUKELIG_SVAR)) in feilboks(html)
    assert tekster.KI_FEIL_BEHOLDT_RESULTAT in feilboks(html)
    assert 'id="gap-dekker"' in html
    assert soknaden(app, paa_resultat_korrektur) == for_
    assert soknaden(app, paa_resultat_korrektur).korrektur is None


def test_fr28_prov_paa_nytt_i_korrektur_gir_brevsiden(app, paa_resultat_korrektur, korrektur_ki):
    """FR-27/FR-28 (story 5.2.1): etter en KI-feil i Korrektur sender «Prøv på nytt» samme
    skjema, og virker KI-en igjen, gir den brevsiden med det forbedrede brevet."""
    app.extensions["test_ki"] = FeilendeKI(korrektur_ki, oppgave="korrektur")
    html = html_av(lag_brev(paa_resultat_korrektur))
    knapp = next(a for t, a in tagger_i(html) if t == "button" and a.get("form"))
    assert (knapp["name"], knapp["value"]) == ("handling", "brev")
    app.extensions["test_ki"] = korrektur_ki
    svar = paa_resultat_korrektur.post("/resultat", data={knapp["name"]: knapp["value"]})
    assert svar.location == "/brev"
    assert soknaden(app, paa_resultat_korrektur).korrektur == korrektur_svar(1)


def test_fr36_korrektur_uten_samtykke_gir_startsiden(med_nokkel):
    """FR-36/AD-12 (story 5.2.1): testmodus av og samtykket mangler: «Oppdater søknadsbrevet
    mitt» kaller ikke KI-en, og brukeren sendes til startsiden."""
    app, client, kalt = med_nokkel
    soknad = Soknad(
        steg=Steg.RESULTAT,
        modus=Modus.KORREKTUR,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        eget_brev=Tekstfelt(EGET_BREV),
        nokkelord=tuple(NOKKELORD_SVAR["nokkelord"]),
        gap=GAP_SVAR,
    )
    sett_soknad(app, client, soknad)
    svar = lag_brev(client)
    assert svar.location == "/"
    assert kalt == []
    assert soknaden(app, client) == soknad


def test_nfr11_korrektur_med_ekte_ki_telles_som_ett_kall(med_nokkel, tmp_path):
    """NFR-11 (story 5.2.1): med ekte KI og samtykke kaller «Oppdater søknadsbrevet mitt»
    korrektur én gang, og kallet telles."""
    app, client, kalt = med_nokkel
    app.extensions["ekte_ki"].test_ki = korrektur_testki(tmp_path)
    soknad = Soknad(
        steg=Steg.RESULTAT,
        modus=Modus.KORREKTUR,
        samtykke=True,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        eget_brev=Tekstfelt(EGET_BREV),
        nokkelord=tuple(NOKKELORD_SVAR["nokkelord"]),
        gap=GAP_SVAR,
    )
    sett_soknad(app, client, soknad)
    assert lag_brev(client).location == "/brev"
    assert kalt == ["korrektur"]
    assert soknaden(app, client).ki_kall == 1


def test_fr22_korrektur_paa_nytt_fra_resultatsiden_gir_brevsiden(app, paa_brev_korrektur):
    """FR-22/FR-25/AD-8: tilbake til resultatsiden og «Oppdater søknadsbrevet mitt» igjen
    gir brevsiden på nytt, og steget er fortsatt brev. Brevet er neste forslag (story 7.1,
    retro 3)."""
    assert paa_brev_korrektur.get("/resultat").status_code == 200
    assert lag_brev(paa_brev_korrektur).location == "/brev"
    assert soknaden(app, paa_brev_korrektur).steg == Steg.BREV
    assert avsnitt(html_av(paa_brev_korrektur.get("/brev"))) == korrektur_brev(2)


def test_fr23_brevsiden_i_korrektur_uten_forbedret_brev_sender_til_resultatsiden(
    app, innlogget_client
):
    """FR-23/AD-8: i Korrektur uten det forbedrede brevet sendes brukeren til resultatsiden,
    også når søknaden har et brev fra Full generering."""
    brev = {"avsnitt": ["Søknad på stillingen"], "navn": None}
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.BREV, modus=Modus.KORREKTUR, brev=brev))
    svar = innlogget_client.get("/brev")
    assert svar.status_code == 302
    assert svar.location == "/resultat"


def test_fr38_korrektur_i_testmodus_med_de_ekte_svarene_gir_brevsiden(app, paa_resultat_korrektur):
    """FR-23/FR-38 (story 5.2.1): i testmodus med case 1 og de ekte svarfilene gir «Oppdater
    søknadsbrevet mitt» brevsiden med «Din oppdaterte søknad er ferdig!» og brevet fra
    korrektur-1.json."""
    assert lag_brev(paa_resultat_korrektur).location == "/brev"
    html = html_av(paa_resultat_korrektur.get("/brev"))
    assert tekster.BREV_OVERSKRIFT_KORREKTUR in html
    tekst = (CASE / "ki-svar" / "korrektur-1.json").read_text(encoding="utf-8")
    svar = kontroller("korrektur", tekst, eget_brev=EGET_BREV)
    assert avsnitt(html) == korrigert_brev(svar)


def test_fr23_tekstene_i_korrektur_ligger_i_tekster_py():
    """FR-23 (story 5.2.1): knappen og overskriften i Korrektur står i web/tekster.py, ordrett
    fra EXPERIENCE, og ikke i malene."""
    assert tekster.OPPDATER_BREV_KNAPP == "Oppdater søknadsbrevet mitt"
    assert tekster.BREV_OVERSKRIFT_KORREKTUR == "Din oppdaterte søknad er ferdig!"
    maler = STIL.parents[2] / "templates"
    for mal in ("resultat.html", "brev.html"):
        innhold = re.sub(r"\{#.*?#\}", "", (maler / mal).read_text(encoding="utf-8"), flags=re.S)
        for tekst in ("Oppdater søknadsbrevet", "oppdaterte søknad"):
            assert tekst not in innhold, (mal, tekst)


# --- Markeringene i Korrektur (story 5.3) ---


def test_fr23_endret_setning_er_en_knapp_med_lukket_du_skrev(app, innlogget_client):
    """FR-23/UX-DR15: en endret setning (gammel != [ny]) er en knapp med den skjulte teksten
    «Endret setning» først og aria-expanded="false". Rett etter står «Du skrev» skjult (hidden)
    med den gamle setningen, og knappen peker på den med aria-controls."""
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning("Søknad", ["Søknad"], True),
        _setning("Jeg ønsker å jobbe her.", ["Jeg vil jobbe her"], True),
        _setning("Jeg kan begynne.", ["Jeg kan begynne."]),
    )
    assert knapper(html) == [
        {
            "class": "endret-setning",
            "role": "button",
            "tabindex": "0",
            "aria-expanded": "false",
            "aria-controls": "du-skrev-2-1",
        }
    ]
    assert (
        '<p><span class="endret-setning" role="button" tabindex="0" aria-expanded="false" '
        'aria-controls="du-skrev-2-1"><span class="skjult">Endret setning </span>'
        "Jeg ønsker å jobbe her.</span>"
        '<span class="du-skrev" id="du-skrev-2-1" hidden>'
        '<span class="du-skrev-overskrift">Du skrev</span><span>Jeg vil jobbe her</span></span>'
        " Jeg kan begynne.</p>"
    ) in html
    assert du_skrev(html, "du-skrev-2-1") == ["Jeg vil jobbe her"]
    assert avsnitt(html) == ["Søknad", "Jeg ønsker å jobbe her. Jeg kan begynne."]


def test_fr23_sammenslaatt_setning_viser_begge_de_gamle(app, innlogget_client):
    """FR-23/UX-DR15: er to setninger slått sammen, viser «Du skrev» begge, hver på sin linje
    (hver i sin span)."""
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning(
            "Det var lærerikt, og jeg fikk ansvar.", ["Det var lærerikt.", "Jeg fikk ansvar."]
        ),
    )
    assert du_skrev(html, "du-skrev-1-1") == ["Det var lærerikt.", "Jeg fikk ansvar."]


def test_fr23_ny_setning_viser_ny_setning_i_du_skrev(app, innlogget_client):
    """FR-23/UX-DR15: en ny setning (gammel == []) er en grønn knapp, og «Du skrev» viser
    «(Ny setning)»."""
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning("Jeg søker.", ["Jeg søker."], True),
        _setning("Jeg kommer gjerne på intervju.", []),
    )
    assert [k["aria-controls"] for k in knapper(html)] == ["du-skrev-1-2"]
    assert du_skrev(html, "du-skrev-1-2") == [tekster.NY_SETNING]
    assert avsnitt(html) == ["Jeg søker. Jeg kommer gjerne på intervju."]


def test_fr23_uendret_setning_er_vanlig_tekst(app, innlogget_client):
    """FR-23: en uendret setning (gammel == [ny]) er vanlig tekst, uten knapp og uten «Du
    skrev». Er ingenting endret og ingenting fjernet, står «Vi fant ingenting å endre. Brevet
    ditt er bra som det er.» i stedet for forklaringen, og ingen linje om fjernede setninger."""
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning("Søknad", ["Søknad"], True),
        _setning("Jeg søker.", ["Jeg søker."], True),
    )
    assert knapper(html) == []
    assert "du-skrev" not in main(html)
    assert forklaring(html) == [tekster.INGENTING_ENDRET]
    assert tekster.KORREKTUR_FORKLARING not in html
    assert tekster.KORREKTUR_FORKLARING_SKJERMLESER not in html
    assert fjernet_linje(html) is None
    assert re.search(r'<article class="brevark">\s*<p>Søknad</p>\s*<p>Jeg søker\.</p>', html)


@pytest.mark.parametrize(
    ("antall", "tekst"), [(1, "1 setning er fjernet."), (2, "2 setninger er fjernet.")]
)
def test_fr23_fjernede_setninger_vises_ikke_men_telles_under_brevet(
    app, innlogget_client, antall, tekst
):
    """FR-23/UX-DR15: setninger med ny null vises ikke i brevet. Under brevet står «1 setning
    er fjernet.» eller «2 setninger er fjernet.». Er en annen setning endret, står
    forklaringen over brevet som vanlig."""
    fjernet = [_setning(None, [f"Fjernet {nr}."]) for nr in range(antall)]
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning("Jeg ønsker å jobbe her.", ["Jeg vil jobbe her"], True),
        *fjernet,
        _setning("Jeg kan begynne.", ["Jeg kan begynne."]),
    )
    assert fjernet_linje(html) == tekst
    assert "Fjernet" not in main(html).replace(tekst, "")
    assert avsnitt(html) == ["Jeg ønsker å jobbe her. Jeg kan begynne."]
    assert forklaring(html) == [tekster.KORREKTUR_FORKLARING]
    assert html.index("</article>") < html.index('class="fjernet-linje"')


def test_fr23_bare_fjernet_gir_ingen_forklaring(app, innlogget_client):
    """FR-23 (bestemt av Kristine 15. november 2026): er ingen setning endret, men én fjernet,
    står ingen forklaring over brevet (heller ikke «Vi fant ingenting å endre»), bare «1
    setning er fjernet.» under brevet."""
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning("Søknad", ["Søknad"], True),
        _setning(None, ["Hei!"], True),
        _setning("Jeg søker.", ["Jeg søker."]),
    )
    assert forklaring(html) == []
    assert tekster.INGENTING_ENDRET not in html
    assert knapper(html) == []
    assert fjernet_linje(html) == "1 setning er fjernet."
    assert avsnitt(html) == ["Søknad", "Jeg søker."]


def test_fr23_flere_endrede_setninger_har_unike_id_er(app, innlogget_client):
    """FR-23/UX-DR15: hver endrede setning har sin egen «Du skrev» med en unik id
    (du-skrev-avsnitt-setning), og aria-controls på hver knapp peker på nettopp den. Så kan
    flere være åpne samtidig."""
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning("En ny.", ["En."], True),
        _setning("To ny.", ["To."]),
        _setning("Tre.", ["Tre."], True),
        _setning("Fire ny.", ["Fire."]),
        _setning("Fem ny.", [], True),
    )
    styrer = [k["aria-controls"] for k in knapper(html)]
    assert styrer == ["du-skrev-1-1", "du-skrev-1-2", "du-skrev-2-2", "du-skrev-3-1"]
    bokser = [a for _, a in tagger_i(html) if a.get("class") == "du-skrev"]
    assert [b["id"] for b in bokser] == styrer
    assert all("hidden" in b for b in bokser)
    alle_id = [a["id"] for _, a in tagger_i(html) if "id" in a]
    assert len(alle_id) == len(set(alle_id))
    assert du_skrev(html, "du-skrev-2-2") == ["Fire."]
    assert avsnitt(html) == ["En ny. To ny.", "Tre. Fire ny.", "Fem ny."]


def test_fr23_ny_og_gammel_escapes(app, innlogget_client):
    """FR-23/NFR-6: <script> i ny eller gammel vises som tekst og escapes, både i knappen, i
    «Du skrev» og i vanlig tekst."""
    html = paa_brevsiden_med(
        app,
        innlogget_client,
        _setning("<script>ny()</script>", ["<script>gammel()</script>"], True),
        _setning("<b>uendret</b>", ["<b>uendret</b>"]),
    )
    assert "<script>ny()" not in html
    assert "<script>gammel()" not in html
    assert "<b>uendret" not in html
    assert "&lt;script&gt;ny()&lt;/script&gt;</span>" in html
    assert du_skrev(html, "du-skrev-1-1") == ["<script>gammel()</script>"]
    assert avsnitt(html) == ["<script>ny()</script> <b>uendret</b>"]


def test_fr23_full_generering_har_ingen_markeringer(paa_brev):
    """FR-22/FR-23: i Full generering er brevsiden som før: ingen forklaring, ingen knapper i
    brevet, ingen «Du skrev», ingen linje om fjernede setninger, og endringer.js lastes ikke."""
    html = html_av(paa_brev.get("/brev"))
    assert forklaring(html) == []
    assert tekster.INGENTING_ENDRET not in html
    assert knapper(html) == []
    assert "du-skrev" not in html
    assert fjernet_linje(html) is None
    assert "js/endringer.js" not in html
    assert "js/nedlasting.js" in html


def test_fr23_endringer_js_lastes_bare_paa_brevsiden_i_korrektur(paa_brev_korrektur):
    """FR-23/AD-1: endringer.js lastes på brevsiden i Korrektur, ikke på resultatsiden."""
    assert "js/endringer.js" in html_av(paa_brev_korrektur.get("/brev"))
    assert "js/endringer.js" not in html_av(paa_brev_korrektur.get("/resultat"))


def test_fr23_endringer_skriptet():
    """FR-23/UX-DR15/AD-1: endringer.js bytter aria-expanded og hidden på boksen i
    aria-controls for hver endrede setning ved trykk (click) og med Enter og mellomrom
    (keydown, siden setningen er et <span> med role="button"), og mellomrom ruller ikke siden.
    Det lukker ikke de andre (flere kan være åpne), har ingen Esc, åpner ikke ved hover eller
    fokus og sender ingenting til serveren."""
    js = (STIL.parents[1] / "js" / "endringer.js").read_text(encoding="utf-8")
    assert '".endret-setning"' in js
    assert '"aria-controls"' in js
    assert '"aria-expanded"' in js
    assert ".hidden" in js
    assert 'addEventListener("click"' in js
    assert 'addEventListener("keydown"' in js
    assert '"Enter"' in js
    assert '" "' in js
    assert "preventDefault()" in js
    assert "Escape" not in js
    assert not re.search(r'addEventListener\("(focus|focusin|pointerenter|mouseenter)"', js)
    assert 'document.addEventListener("click"' not in js
    for forbudt in ("fetch(", "XMLHttpRequest", ".submit(", "sendBeacon", "location", "innerHTML"):
        assert forbudt not in js


def test_fr23_tekstene_for_markeringene_ligger_i_tekster_py():
    """FR-23/UX-DR15: tekstene for markeringene står i web/tekster.py, ordrett fra EXPERIENCE,
    og ikke i brev.html."""
    assert tekster.KORREKTUR_FORKLARING == (
        "Grønn og understreket = endret. Trykk på setningen for å se det du skrev."
    )
    assert tekster.KORREKTUR_FORKLARING_SKJERMLESER == "Endrede setninger er knapper."
    assert tekster.ENDRET_SETNING_SKJERMLESER == "Endret setning"
    assert tekster.DU_SKREV == "Du skrev"
    assert tekster.NY_SETNING == "(Ny setning)"
    assert tekster.INGENTING_ENDRET == "Vi fant ingenting å endre. Brevet ditt er bra som det er."
    assert tekster.fjernet(1) == "1 setning er fjernet."
    assert tekster.fjernet(2) == "2 setninger er fjernet."
    assert tekster.fjernet(5) == "5 setninger er fjernet."
    mal = STIL.parents[2] / "templates" / "brev.html"
    innhold = re.sub(r"\{#.*?#\}", "", mal.read_text(encoding="utf-8"), flags=re.S)
    for tekst in ("Grønn og", "Endrede setninger", "Endret setning", "Du skrev", "Ny setning"):
        assert tekst not in innhold, tekst
    for tekst in ("ingenting å endre", "er fjernet", "style="):
        assert tekst not in innhold, tekst


def test_fr23_css_for_markeringene():
    """FR-23/UX-DR15/NFR-7: forklaringsboksen er hvit og høyst 720 px. Den endrede setningen
    har vanlig tekstfarge, lys grønn bakgrunn, 2 px grønn understreking og ingen ramme, og
    changed-active ved hover og når den er åpen, og fokusringen. «Du skrev» er dempet med 4 px
    strek til venstre, og [hidden] skjuler den. I høykontrast har setningene, «Du skrev» og
    forklaringsboksen en ramme i CanvasText, og en åpen setning en tykkere ramme. Ingen faste
    høyder."""
    css = STIL.read_text(encoding="utf-8")
    boks = css_blokk(css, ".korrektur-forklaring")
    assert "max-width: var(--letter-max);" in boks
    assert "background: var(--surface);" in boks
    assert "margin: 0 auto" in boks
    setning = css_blokk(css, ".endret-setning")
    for regel in (
        "color: var(--text);",
        "background: var(--success-tint);",
        "text-decoration-color: var(--success);",
        "text-decoration-thickness: 2px;",
        "cursor: pointer;",
        "box-decoration-break: clone;",
    ):
        assert regel in setning, regel
    # Setningen skal brytes over linjer som resten av avsnittet (retro 5, runde B), så den
    # får ingen display som gjør den til en boks.
    assert "display" not in setning
    aktiv = css_blokk(css, '.endret-setning:hover,\n.endret-setning[aria-expanded="true"]')
    assert "background: var(--changed-active);" in aktiv
    assert "outline: 3px solid var(--focus-ring);" in css_blokk(
        css, ".endret-setning:focus-visible"
    )
    # Den skjulte «Endret setning» blir ikke med når brevteksten kopieres fra siden.
    assert "user-select: none;" in css_blokk(css, ".endret-setning .skjult")
    gammel = css_blokk(css, ".du-skrev")
    assert "display: block;" in gammel
    assert "color: var(--text-muted);" in gammel
    assert "background: var(--background);" in gammel
    assert "border-left: 4px solid var(--text-muted);" in gammel
    assert "display: none;" in css_blokk(css, ".du-skrev[hidden]")
    assert "text-transform: uppercase;" in css_blokk(css, ".du-skrev-overskrift")
    for blokk in (boks, setning, gammel, css_blokk(css, ".fjernet-linje")):
        assert "height" not in blokk
    hoykontrast = re.search(r"@media \(forced-colors: active\) \{(.*?)\n\}", css, re.S).group(1)
    for velger in (".endret-setning", ".du-skrev", ".korrektur-forklaring"):
        regel = re.search(rf"^\s*{re.escape(velger)}\s*\{{(.*?)\}}", hoykontrast, re.S | re.M)
        assert "border: 1px solid CanvasText;" in regel.group(1), velger
    apen = re.search(
        r'^\s*\.endret-setning\[aria-expanded="true"\]\s*\{(.*?)\}', hoykontrast, re.S | re.M
    )
    assert "border-width: 3px;" in apen.group(1)


# --- Tekster og CSS ---


def test_fr21_fr22_tekstene_ligger_i_tekster_py():
    """FR-21/FR-22/FR-28: tekstene står i web/tekster.py, ordrett fra EXPERIENCE."""
    assert tekster.LAG_BREV_KNAPP == "Lag søknadsbrevet mitt"
    assert tekster.VENTE_BREV == "Vi lager brevet ditt – det kan ta en liten stund."
    assert tekster.KI_FEIL_BEHOLDT_RESULTAT == "Resultatet og det du har lagt inn, er ikke borte."
    assert tekster.BREV_TITTEL == "Søknadsbrev"
    assert tekster.BREV_OVERSKRIFT == "Din ferdigstilte søknad!"
    maler = STIL.parents[2] / "templates"
    for mal in ("resultat.html", "brev.html"):
        # Kommentarene ({# … #}) kan nevne tekstene. Det som vises, kan ikke.
        innhold = re.sub(r"\{#.*?#\}", "", (maler / mal).read_text(encoding="utf-8"), flags=re.S)
        for tekst in (
            "Lag søknadsbrevet",
            "Vi lager",
            "er ikke borte",
            "Prøv på nytt",
            "Søknadsbrev",
            "ferdigstilte",
        ):
            assert tekst not in innhold, (mal, tekst)


def test_nfr7_brevarket_er_hoyst_720_px_og_bryter_lange_ord():
    """NFR-7/UX-DR15: brevarket er hvitt med kant, rounded.md og skygge, høyst 720 px bredt, i
    midten, og bryter lange ord. Ingen fast høyde og ingen nowrap."""
    css = STIL.read_text(encoding="utf-8")
    assert "--letter-max: 720px;" in css_blokk(css, ":root")
    ark = css_blokk(css, ".brevark")
    for linje in (
        "max-width: var(--letter-max);",
        "background: var(--surface);",
        "border: 1px solid var(--border);",
        "border-radius: var(--rounded-md);",
        "box-shadow: var(--shadow);",
        "padding: var(--space-6) var(--space-7);",
        "overflow-wrap: anywhere;",
    ):
        assert linje in ark
    assert re.search(r"margin: 0 auto\b", ark)
    assert "height" not in ark
    assert "nowrap" not in ark


def test_nfr7_brevoverskriften_og_arket_er_mindre_paa_mobil():
    """NFR-7: brevoverskriften har heading-letter, og under 700 px heading-letter-mobile og
    mindre luft i arket."""
    css = STIL.read_text(encoding="utf-8")
    assert "font-size: var(--size-heading-letter);" in css_blokk(css, ".brev-overskrift")
    mobil = re.findall(r"@media \(max-width: 699px\) \{(.*?)\n\}", css, re.S)
    mobil_brev = next(m for m in mobil if ".brevark" in m)
    assert "font-size: var(--size-heading-letter-mobile);" in mobil_brev
    assert "padding: var(--space-4);" in mobil_brev
