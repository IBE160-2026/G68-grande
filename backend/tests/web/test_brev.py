"""Tester for «Lag søknadsbrevet mitt» og brevsiden (FR-21, FR-22, FR-26, FR-27, FR-28, NFR-4,
NFR-6, NFR-7, AD-1, AD-8, UX-DR7, UX-DR14). Story 3.1."""

import html as html_modul
import json
import re
import shutil

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE, TestKI
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from soknad.web.innlogging import OKT_ID
from tests.web.hjelpere import (
    ANNONSE,
    CASE,
    CV,
    STIL,
    FeilendeKI,
    css_blokk,
    element,
    footer,
    html_av,
    main,
    med_autofocus,
    okt_id,
    sett_soknad,
    soknaden,
    tagger_i,
)

# Fiksturene paa_resultat og paa_brev står i conftest.py.

BREV_SVAR = json.loads((CASE / "ki-svar" / "brev-1.json").read_text(encoding="utf-8"))


def lag_brev(client, handling="brev"):
    data = {} if handling is None else {"handling": handling}
    return client.post("/resultat", data=data)


def feilboks(html):
    return re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)


def avsnitt(html):
    """Teksten i hvert <p> i brevarket, med HTML-escapingen fjernet."""
    ark = re.search(r'<article class="brevark">(.*?)</article>', html, re.S).group(1)
    return [html_modul.unescape(p) for p in re.findall(r"<p>(.*?)</p>", ark, re.S)]


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


@pytest.mark.parametrize("innhold", ['{"avsnitt": []}', '{"avsnitt": ["  "]}'])
def test_fr28_tomt_brev_gir_feilboksen(app, paa_resultat, tmp_path, innhold):
    """FR-28: et tomt brev (ingen avsnitt eller bare mellomrom) gir KIFeil(ubrukelig_svar) og
    resultatsiden med feilboksen, aldri en tom brevside."""
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
    """FR-22/AD-8: tilbake til resultatsiden (nettleserens tilbakeknapp) og «Lag
    søknadsbrevet mitt» igjen gir brevsiden på nytt, og steget er fortsatt brev."""
    assert paa_brev.get("/resultat").status_code == 200
    assert lag_brev(paa_brev).location == "/brev"
    soknad = soknaden(app, paa_brev)
    assert soknad.steg == Steg.BREV
    assert soknad.brev == BREV_SVAR
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
    assert med_autofocus(html) == [None]


def test_fr22_ett_avsnitt_per_element(paa_brev):
    """FR-22: brevarket har ett <p> per element i avsnitt, i samme rekkefølge."""
    assert avsnitt(html_av(paa_brev.get("/brev"))) == BREV_SVAR["avsnitt"]


def test_nfr6_brevteksten_escapes(app, innlogget_client):
    """NFR-6: tekst fra KI-en escapes, så den aldri blir HTML."""
    brev = {"avsnitt": ["<b>fet</b> & <script>x</script>", "Hilsen"]}
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.BREV, brev=brev))
    html = main(html_av(innlogget_client.get("/brev")))
    assert "<b>" not in html
    assert "<script>" not in html
    assert "&lt;b&gt;fet&lt;/b&gt; &amp; &lt;script&gt;" in html
    assert avsnitt(html) == brev["avsnitt"]


def test_fr26_brevet_kan_ikke_redigeres_og_har_ingen_tilbake(paa_brev):
    """FR-26: brevsiden har ingen «Tilbake», ingen tekstfelt og ingen contenteditable. I
    <main> er det ingen skjema eller knapper, og den eneste lenken er «Last ned som Word»
    (story 3.2)."""
    html = html_av(paa_brev.get("/brev"))
    innhold = main(html)
    assert tekster.TILBAKE_KNAPP not in innhold
    assert "contenteditable" not in html
    tagger = {t for t, _ in tagger_i(innhold)}
    assert tagger.isdisjoint({"textarea", "input", "form", "button"})
    lenker = [a["href"] for t, a in tagger_i(innhold) if t == "a"]
    assert lenker == ["/last-ned/docx"]


def test_fr22_brevsiden_har_logg_ut_og_ingen_ventetegn(paa_brev):
    """FR-22/FR-6/NFR-4: «Logg ut» står i hjørneraden: nøyaktig ett skjema der, til
    /logg-ut. Vinduet etter nedlasting (story 3.3) har også et skjema til /logg-ut, så
    testen ser bare på <footer>. Brevsiden har ingen KI-kall ennå, så den har ikke
    ventetegnet."""
    html = html_av(paa_brev.get("/brev"))
    hjornerad = footer(html)
    skjemaer = [a for t, a in tagger_i(hjornerad) if t == "form"]
    assert skjemaer == [{"class": "utlogging", "method": "post", "action": "/logg-ut"}]
    assert tekster.LOGG_UT_KNAPP in hjornerad
    assert 'id="vente"' not in html


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
