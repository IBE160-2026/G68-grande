"""Tester for innleggingssiden: feltene, sjekken av det som er lagt inn, feilboksen og
«Tilbake» (FR-8, FR-9, FR-13, FR-19, FR-34, NFR-4, NFR-6, NFR-7, AD-1, AD-8, AD-9,
UX-DR7, UX-DR8, UX-DR9, UX-DR21). Story 2.5.1. Analysen og KI-feilen (FR-15, FR-21,
FR-28) kom i story 2.5.2."""

import html as html_modul
import json
import re

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.kjerne import inndata
from soknad.kjerne.feil import FeilType, InndataFeil, KIFeil, KIFeilType
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.kjerne.testdata_match import vask
from soknad.web import ruter, tekster
from soknad.web.innlogging import OKT_ID
from tests.web.hjelpere import (
    STIL,
    FeilendeKI,
    css_blokk,
    main,
    okt_id,
    sett_soknad,
    sett_testmodus,
    soknaden,
    tagger_i,
)

CASE = TESTDATA_MAPPE / "case-1-utvikler"
CV = (CASE / "cv.txt").read_text(encoding="utf-8")
ANNONSE = (CASE / "annonse.txt").read_text(encoding="utf-8")

TOM_CV = "CV: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
TOM_ANNONSE = "Stillingsannonse: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
IKKE_TESTDATA_CV = "CV: I testmodus fungerer bare testdataene fra mappen testdata/."
IKKE_TESTDATA_ANNONSE = (
    "Stillingsannonse: I testmodus fungerer bare testdataene fra mappen testdata/."
)


NOKKELORD_SVAR = json.loads((CASE / "ki-svar" / "nokkelord.json").read_text(encoding="utf-8"))
GAP_SVAR = json.loads((CASE / "ki-svar" / "gap.json").read_text(encoding="utf-8"))


def til_innlegging(app, client):
    sett_soknad(app, client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))


def uten_testmodus(app, client):
    """Slår av testmodus. Det lager en ny økt uten søknad, så søknaden settes på nytt."""
    sett_testmodus(app, client, False)
    til_innlegging(app, client)


@pytest.fixture
def paa_innlegging(app, innlogget_client):
    """En innlogget klient på innleggingen for Full generering."""
    til_innlegging(app, innlogget_client)
    return innlogget_client


def send(client, cv, annonse, handling="sjekk"):
    return client.post("/innlegging", data={"cv": cv, "annonse": annonse, "handling": handling})


def html_av(svar):
    return svar.get_data(as_text=True)


def element(html, id_):
    """Attributtene til elementet med denne id-en."""
    return next(a for _, a in tagger_i(html) if a.get("id") == id_)


def feilboks_lenker(html):
    """(href, tekst) for hver lenke i feilboksen."""
    boks = re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)
    return re.findall(r'<a href="([^"]+)">([^<]+)</a>', boks)


def tekstboks(html, navn):
    """Teksten i tekstboksen for feltet, uten linjeskiftet rett etter <textarea>."""
    innhold = re.search(rf'<textarea id="{navn}-tekst"[^>]*>(.*?)</textarea>', html, re.S)
    return innhold.group(1).removeprefix("\n")


# --- Matrisen ---


def test_fr9_begge_tomme_gir_to_feil_cv_forst(app, paa_innlegging):
    """FR-9/UX-DR7: tom CV og annonse med bare mellomrom gir samme side (200, ingen redirect)
    med to feil i feilboksen, CV først. Tekstene er lagret i søknaden."""
    svar = send(paa_innlegging, "", "  \n")
    assert svar.status_code == 200
    html = html_av(svar)
    assert feilboks_lenker(html) == [("#cv-felt", TOM_CV), ("#annonse-felt", TOM_ANNONSE)]
    assert soknaden(app, paa_innlegging).annonse == Tekstfelt("  \n")
    assert soknaden(app, paa_innlegging).steg == Steg.INNLEGGING


def test_fr34_egen_cv_gir_feil_og_annonsen_star_igjen(paa_innlegging):
    """FR-34/AD-9: en CV som ikke er testdata, gir feil på CV-en. Begge tekstene står igjen i
    feltene."""
    html = html_av(send(paa_innlegging, "Min egen CV", ANNONSE))
    assert feilboks_lenker(html) == [("#cv-felt", IKKE_TESTDATA_CV)]
    assert tekstboks(html, "cv") == "Min egen CV"
    assert tekstboks(html, "annonse") == ANNONSE


def test_fr9_fr34_tom_cv_og_egen_annonse(paa_innlegging):
    """FR-9/FR-34: tom CV og egen annonse gir én feil per felt."""
    html = html_av(send(paa_innlegging, "", "Min egen annonse"))
    assert feilboks_lenker(html) == [
        ("#cv-felt", TOM_CV),
        ("#annonse-felt", IKKE_TESTDATA_ANNONSE),
    ]


def test_fr15_testdata_gir_analysen_og_resultatsiden(app, paa_innlegging):
    """FR-15/FR-21/FR-34: cv.txt og annonse.txt fra case 1 gir ingen feil. Nøkkelordlisten,
    den vaskede annonsen, arbeidsgiveren og gap-analysen lagres, steget blir resultat, og
    brukeren sendes til resultatsiden (story 2.5.2)."""
    svar = send(paa_innlegging, CV, ANNONSE)
    assert svar.status_code == 302
    assert svar.location == "/resultat"
    soknad = soknaden(app, paa_innlegging)
    assert soknad.cv == Tekstfelt(CV)
    assert soknad.annonse == Tekstfelt(ANNONSE)
    assert soknad.nokkelord == tuple(NOKKELORD_SVAR["nokkelord"])
    assert soknad.nokkelord_annonse == vask(ANNONSE)
    assert soknad.arbeidsgiver == NOKKELORD_SVAR["arbeidsgiver"]
    assert soknad.gap == GAP_SVAR
    assert soknad.steg == Steg.RESULTAT


def test_fr15_forst_nokkelord_saa_gap(app, paa_innlegging):
    """FR-15/AD-8: KI-en kalles med nøkkelord først og gap etterpå. Feiler nøkkelordene,
    kalles ikke gap."""
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    send(paa_innlegging, CV, ANNONSE)
    assert kalt == ["nokkelord", "gap"]
    kalt.clear()
    til_innlegging(app, paa_innlegging)
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"].test_ki, kalt=kalt)
    send(paa_innlegging, CV, ANNONSE)
    assert kalt == ["nokkelord"]


def test_fr9_inndatafeil_gir_ingen_ki_kall(app, paa_innlegging):
    """FR-9/AD-9: med feil i feltene kalles ikke KI-en, og steget flyttes ikke."""
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], kalt=kalt)
    svar = send(paa_innlegging, "", ANNONSE)
    assert svar.status_code == 200
    assert kalt == []
    assert soknaden(app, paa_innlegging).steg == Steg.INNLEGGING


@pytest.mark.parametrize("oppgave", ["nokkelord", "gap"])
@pytest.mark.parametrize(
    ("feiltype", "tekst"),
    [
        (KIFeilType.NETTVERK, "Nettverksfeil, sjekk nettverkstilgangen."),
        (KIFeilType.ANNET, "Noe gikk galt hos KI-tjenesten. Prøv på nytt."),
        (KIFeilType.UBRUKELIG_SVAR, "Noe gikk galt hos KI-tjenesten. Prøv på nytt."),
    ],
)
def test_fr28_ki_feil_gir_innleggingen_med_feilteksten(
    app, paa_innlegging, oppgave, feiltype, tekst
):
    """FR-28/AD-9/UX-DR7: en KIFeil gir innleggingen på nytt (200, ingen redirect) med
    feilteksten øverst i feilboksen, uten lenker, feltene fylt ut og steget uendret. Ingenting
    fra analysen lagres."""
    app.extensions["test_ki"] = FeilendeKI(
        app.extensions["test_ki"], oppgave=oppgave, feiltype=feiltype
    )
    svar = send(paa_innlegging, CV, ANNONSE)
    assert svar.status_code == 200
    html = html_av(svar)
    boks = re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)
    assert re.match(rf'\s*<p class="feilboks-overskrift">{re.escape(tekst)}</p>', boks)
    assert "<a " not in boks
    assert tekster.FEILBOKS_OVERSKRIFT not in html
    assert element(html, "feilboks")["tabindex"] == "-1"
    assert "autofocus" in element(html, "feilboks")
    assert html_modul.unescape(tekstboks(html, "cv")) == CV
    assert html_modul.unescape(tekstboks(html, "annonse")) == ANNONSE
    soknad = soknaden(app, paa_innlegging)
    assert soknad.steg == Steg.INNLEGGING
    assert (soknad.nokkelord, soknad.nokkelord_annonse, soknad.arbeidsgiver, soknad.gap) == (
        (None,) * 4
    )
    assert soknad.cv == Tekstfelt(CV)


def ki_feil_boks(app, client, feiltype=KIFeilType.ANNET):
    """Sender case 1 med en KI som feiler, og gir HTML-en og innholdet i feilboksen."""
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], feiltype=feiltype)
    html = html_av(send(client, CV, ANNONSE))
    return html, re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)


@pytest.mark.parametrize("feiltype", list(KIFeilType))
def test_fr28_ki_feil_sier_at_ingenting_er_borte_og_har_prov_paa_nytt(
    app, paa_innlegging, feiltype
):
    """FR-28/UX-DR7: under feilteksten står «Det du har lagt inn, er ikke borte.» og hovedknappen
    «Prøv på nytt», for hver type KIFeil. Boksen har ingen role="alert"."""
    html, boks = ki_feil_boks(app, paa_innlegging, feiltype)
    tekst = tekster.ki_feiltekst(KIFeil(feiltype))
    assert re.search(
        rf"{re.escape(tekst)}</p>"
        r'\s*<p class="feilboks-tekst">Det du har lagt inn, er ikke borte\.</p>'
        r'\s*<p class="feilboks-knapp">\s*<button class="hovedknapp"[^>]*>Prøv på nytt</button>',
        boks,
    )
    assert "role=" not in boks
    assert 'role="alert"' not in html


def test_fr28_prov_paa_nytt_sender_skjemaet_som_sjekk(app, paa_innlegging):
    """FR-27/FR-28: «Prøv på nytt» står utenfor skjemaet, men sender det med form= som
    «Sjekk CV-en min», og viser ventetegnet med samme ventesetning."""
    html, _ = ki_feil_boks(app, paa_innlegging)
    knapp = next(a for t, a in tagger_i(html) if t == "button" and a.get("form"))
    assert knapp == {
        "class": "hovedknapp",
        "type": "submit",
        "form": "innlegging-skjema",
        "name": "handling",
        "value": "sjekk",
        "data-vente": tekster.VENTE_SJEKKER,
    }
    skjema = next(a for t, a in tagger_i(html) if t == "form")
    assert skjema["id"] == "innlegging-skjema"
    vente = [a["data-vente"] for t, a in tagger_i(html) if "data-vente" in a]
    assert vente == [tekster.VENTE_SJEKKER] * 2


def test_fr28_prov_paa_nytt_med_ki_som_virker_gir_resultatsiden(app, paa_innlegging):
    """FR-28/AD-8: virker KI-en igjen, gir «Prøv på nytt» resultatsiden, og analysen lagres.
    POST-en bygges fra feilsiden: knappens name/value og teksten i tekstboksene."""
    ekte = app.extensions["test_ki"]
    html, _ = ki_feil_boks(app, paa_innlegging)
    assert soknaden(app, paa_innlegging).steg == Steg.INNLEGGING
    app.extensions["test_ki"] = ekte
    knapp = next(a for t, a in tagger_i(html) if t == "button" and a.get("form"))
    data = {navn: html_modul.unescape(tekstboks(html, navn)) for navn in ("cv", "annonse")}
    data[knapp["name"]] = knapp["value"]
    svar = paa_innlegging.post("/innlegging", data=data)
    assert svar.status_code == 302
    assert svar.location == "/resultat"
    soknad = soknaden(app, paa_innlegging)
    assert soknad.steg == Steg.RESULTAT
    assert soknad.gap == GAP_SVAR


def test_ux_dr7_prov_paa_nytt_er_ikke_hele_bredden():
    """UX-DR7: knappen i feilboksen er bare så bred som teksten, som i skissen."""
    blokk = css_blokk(STIL.read_text(encoding="utf-8"), ".feilboks-knapp .hovedknapp")
    assert "display: inline-block;" in blokk
    assert "width: auto;" in blokk


def test_fr19_tilbake_lagrer_uten_feil_og_sender_til_modusvalget(app, paa_innlegging):
    """FR-19/AD-8: «Tilbake» lagrer også tekst som ikke er testdata, uten å vise feil, og
    sender til modusvalget. Innleggingen viser tekstene igjen."""
    svar = send(paa_innlegging, "Min egen CV", "Min egen annonse", handling="tilbake")
    assert svar.status_code == 302
    assert svar.location == "/modus"
    assert soknaden(app, paa_innlegging).cv == Tekstfelt("Min egen CV")
    html = html_av(paa_innlegging.get("/innlegging"))
    assert 'class="feilboks"' not in html
    assert tekstboks(html, "cv") == "Min egen CV"
    assert tekstboks(html, "annonse") == "Min egen annonse"


def test_fr19_samme_tekster_igjen_endrer_ikke_soknaden(app, innlogget_client):
    """FR-19/AD-8: sendes de samme tekstene på nytt, er søknaden den samme, også steget og
    nøkkelordlisten."""
    soknad = Soknad(
        steg=Steg.RESULTAT,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        nokkelord=("Python",),
        nokkelord_annonse="annonse",
        gap={"dekker": ["Python"], "mangler": []},
    )
    sett_soknad(app, innlogget_client, soknad)
    send(innlogget_client, CV, ANNONSE, handling="tilbake")
    assert soknaden(app, innlogget_client) == soknad


def test_fr19_endret_tekst_nullstiller_og_gir_steg_innlegging(app, innlogget_client):
    """FR-19/AD-8: ny CV etter resultatet nullstiller nøkkelordlisten og gap-analysen, og
    steget blir innlegging."""
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
            arbeidsgiver="Testvik Utvikling AS",
            gap={"dekker": ["Python"], "mangler": []},
        ),
    )
    send(innlogget_client, "Ny CV", ANNONSE, handling="tilbake")
    ny = soknaden(app, innlogget_client)
    assert ny.steg == Steg.INNLEGGING
    assert (ny.nokkelord, ny.nokkelord_annonse, ny.arbeidsgiver, ny.gap) == (None,) * 4


@pytest.mark.parametrize("data", [{"handling": "noe"}, {}])
def test_fr8_ukjent_handling_gir_400_og_uendret_soknad(app, paa_innlegging, data):
    """AD-8: en ukjent eller manglende handling gir 400 og samme side, og søknaden er uendret."""
    for_ = soknaden(app, paa_innlegging)
    svar = paa_innlegging.post("/innlegging", data={"cv": "x", "annonse": "y", **data})
    assert svar.status_code == 400
    assert tekster.INNLEGGING_OVERSKRIFT in html_av(svar)
    assert soknaden(app, paa_innlegging) == for_


def test_fr20_post_for_tidlig_endrer_ingenting(app, innlogget_client):
    """FR-20/AD-8: POST /innlegging på steg modus sender til modusvalget, og ingenting lagres."""
    soknad = Soknad(steg=Steg.MODUS)
    sett_soknad(app, innlogget_client, soknad)
    svar = send(innlogget_client, CV, ANNONSE, handling="tilbake")
    assert svar.status_code == 302
    assert svar.location == "/modus"
    assert soknaden(app, innlogget_client) == soknad


# --- Siden ---


def test_fr9_feltene_star_i_samme_rekkefolge_som_feilene():
    """FR-9: feltene på siden (tekster.py) og rekkefølgen på feilene (inndata.py) er de samme,
    så feilboksen og feltene ikke kommer i ulik rekkefølge når flere felt legges til."""
    assert tuple(tekster.INNLEGGINGSFELT) == inndata.INNLEGGINGSFELT


def test_fr8_tomme_felt_viser_bare_lim_inn_tekst(paa_innlegging):
    """FR-8/UX-DR8: tomme felt viser «Lim inn tekst», og tekstboksen er skjult, men står i
    skjemaet med riktig navn."""
    html = html_av(paa_innlegging.get("/innlegging"))
    for navn in ("cv", "annonse"):
        felt = re.search(rf'<section[^>]*id="{navn}-felt".*?</section>', html, re.S).group(0)
        assert re.search(
            r'<div class="tom-tilstand">\s*<button[^>]*id="' + navn + '-lim-inn"', felt
        )
        assert '<div class="limeboks" hidden>' in felt
        assert element(html, f"{navn}-tekst")["name"] == navn
    # Ingen «Last opp PDF» før Epic 6.
    assert "Last opp PDF" not in main(html)


def test_fr8_fylt_felt_viser_tekstboksen(app, innlogget_client):
    """FR-8/UX-DR8: et felt med tekst viser tekstboksen med søppelbøtta, og «Lim inn tekst» er
    skjult. Et tomt felt ved siden av viser «Lim inn tekst»."""
    sett_soknad(
        app,
        innlogget_client,
        Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, cv=Tekstfelt("Min CV")),
    )
    html = html_av(innlogget_client.get("/innlegging"))
    cv_felt = re.search(r'<section[^>]*id="cv-felt".*?</section>', html, re.S).group(0)
    annonse_felt = re.search(r'<section[^>]*id="annonse-felt".*?</section>', html, re.S).group(0)
    assert re.search(r'<div class="tom-tilstand" hidden>', cv_felt)
    assert re.search(r'<div class="limeboks">', cv_felt)
    assert re.search(r'<div class="tom-tilstand">', annonse_felt)
    assert re.search(r'<div class="limeboks" hidden>', annonse_felt)


def test_fr8_feltnavn_ikoner_og_knapper(paa_innlegging):
    """FR-8/UX-DR8/UX-DR21: feltene «📄 CV» og «📢 Stillingsannonse» som h2, ikonene skjult for
    skjermlesere, og knappene «Tilbake» og «Sjekk CV-en min» nederst."""
    html = html_av(paa_innlegging.get("/innlegging"))
    navn = re.findall(r'<h2 class="feltnavn"[^>]*>(.*?)</h2>', html, re.S)
    assert navn == [
        '<span aria-hidden="true">📄</span> CV',
        '<span aria-hidden="true">📢</span> Stillingsannonse',
    ]
    knapper = [
        (a.get("value"), a.get("type")) for t, a in tagger_i(html) if t == "button" and "name" in a
    ]
    assert knapper == [("tilbake", "submit"), ("sjekk", "submit")]
    assert re.search(r'value="tilbake">\s*Tilbake\s*</button>', html)
    assert re.search(r'value="sjekk"[^>]*>\s*Sjekk CV-en min\s*</button>', html)


def test_fr34_hjelpeteksten_om_testdata_bare_i_testmodus(app, paa_innlegging):
    """FR-34/UX-DR9: «Testmodus: bruk filene i mappen backend/testdata/ i prosjektet.» står
    over feltene i testmodus, og ikke ellers."""
    html = html_av(paa_innlegging.get("/innlegging"))
    hjelp = (
        '<p class="testhjelp">Testmodus: bruk filene i mappen backend/testdata/ i prosjektet.</p>'
    )
    assert hjelp in html
    assert html.index(hjelp) < html.index('id="cv-felt"')
    uten_testmodus(app, paa_innlegging)
    svar = paa_innlegging.get("/innlegging")
    assert svar.status_code == 200
    assert "testhjelp" not in html_av(svar)


def test_fr7_utlogget_for_testmodus_sjekken_gir_innloggingen(app, paa_innlegging, monkeypatch):
    """FR-7/AD-8: logges brukeren ut i en annen fane etter login_required, men før
    innleggingen sjekker testmodus, sendes hen til innloggingen med «Du må logge inn først».
    Ingen feilside, cookien tømmes, og KI-en kalles ikke."""
    lager = app.extensions["oktlager"]
    id_ = okt_id(paa_innlegging)
    ekte_lagre = ruter.lagre_soknad

    def lagre_og_logg_ut(soknad):
        ekte_lagre(soknad)
        lager.slett(id_)

    monkeypatch.setattr(ruter, "lagre_soknad", lagre_og_logg_ut)
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    svar = send(paa_innlegging, CV, ANNONSE)
    assert svar.status_code == 302
    assert svar.location == "/logg-inn?ikke_innlogget=1"
    assert okt_id(paa_innlegging) is None
    assert kalt == []
    assert lager.hent_soknad(id_) is None


def test_fr34_uten_testmodus_godtas_egen_tekst(app, paa_innlegging):
    """FR-34: uten testmodus gir egen tekst ingen ikke_testdata (bare tomme felt sjekkes)."""
    uten_testmodus(app, paa_innlegging)
    html = html_av(send(paa_innlegging, "Min egen CV", ""))
    assert feilboks_lenker(html) == [("#annonse-felt", TOM_ANNONSE)]


def test_nfr6_skjermlesertekstene(paa_innlegging):
    """NFR-6/UX-DR8/UX-DR21: knappene og tekstboksen har feltnavnet med for skjermlesere, og
    søppelbøtta har «Tøm CV-feltet» og sier «CV-feltet er tømt». Statusområdet finnes alltid."""
    html = html_av(paa_innlegging.get("/innlegging"))
    assert element(html, "cv-lim-inn")["aria-label"] == "Lim inn tekst, CV"
    assert element(html, "annonse-lim-inn")["aria-label"] == "Lim inn tekst, Stillingsannonse"
    assert '<label for="cv-tekst"><span class="skjult">CV: </span>Lim inn teksten her</label>' in (
        html
    )
    soppel = [a for t, a in tagger_i(html) if a.get("class") == "soppelbotte"]
    assert [(a["aria-label"], a["data-tomt"], a["type"]) for a in soppel] == [
        ("Tøm CV-feltet", "CV-feltet er tømt", "button"),
        ("Tøm annonsefeltet", "Annonsefeltet er tømt", "button"),
    ]
    assert re.search(r'<button class="soppelbotte"[^>]*><span aria-hidden="true">🗑️</span>', html)
    assert element(html, "innlegging-status")["role"] == "status"


def test_ux_dr7_feilboksen_far_fokus_uten_role_alert(paa_innlegging):
    """UX-DR7: feilboksen har overskriften, tabindex="-1" og autofocus, men ikke
    role="alert". Den står over feltene."""
    html = html_av(send(paa_innlegging, "", ""))
    boks = element(html, "feilboks")
    assert boks["tabindex"] == "-1"
    assert "autofocus" in boks
    assert "role" not in boks
    assert "Noe må fikses før du kan gå videre:" in html
    assert html.index('id="feilboks"') < html.index('id="cv-felt"')
    # Lenkene peker på feltene, som kan få fokus.
    assert element(html, "cv-felt")["tabindex"] == "-1"


def test_ux_dr8_feltet_med_feil_er_merket_og_koblet(paa_innlegging):
    """UX-DR8: feltet med feil får rød ramme (har-feil), feilteksten under feltnavnet, og
    knappen og tekstboksen er koblet til den. Tekstboksen får aria-invalid. Feltet uten feil
    har ingen av delene."""
    html = html_av(send(paa_innlegging, "Min egen CV", ANNONSE))
    assert element(html, "cv-felt")["class"] == "innleggingsfelt har-feil"
    assert element(html, "cv-feil")["class"] == "feiltekst"
    assert re.search(r'id="cv-feil">CV: I testmodus fungerer bare testdataene', html)
    assert element(html, "cv-lim-inn")["aria-describedby"] == "cv-feil"
    assert element(html, "cv-tekst")["aria-describedby"] == "cv-feil"
    assert element(html, "cv-tekst")["aria-invalid"] == "true"
    assert element(html, "annonse-felt")["class"] == "innleggingsfelt"
    assert "aria-describedby" not in element(html, "annonse-tekst")
    assert "aria-invalid" not in element(html, "annonse-tekst")
    assert 'id="annonse-feil"' not in html


def test_fr8_linjeskift_forst_i_teksten_blir_ikke_borte(paa_innlegging):
    """FR-8: et linjeskift først i teksten står igjen, og tekst med < og & escapes."""
    html = html_av(send(paa_innlegging, "\nFørste linje <b>&", "annonse"))
    assert tekstboks(html, "cv") == "\nFørste linje &lt;b&gt;&amp;"


def test_nfr4_cookien_har_bare_okt_id(paa_innlegging):
    """NFR-4/AD-7: CV og annonse ligger bare i øktlageret, aldri i cookien."""
    send(paa_innlegging, CV, ANNONSE)
    with paa_innlegging.session_transaction() as okt:
        assert set(okt) == {OKT_ID}


def test_fr8_skriptet_lastes_bare_pa_innleggingen(paa_innlegging):
    """AD-1: innlegging.js lastes på innleggingen, ikke på modusvalget."""
    assert "js/innlegging.js" in html_av(paa_innlegging.get("/innlegging"))
    assert "js/innlegging.js" not in html_av(paa_innlegging.get("/modus"))


def test_ad1_skriptet_sender_ingenting_til_serveren():
    """AD-1: innlegging.js endrer bare skjemaet i nettleseren og sender ingenting selv."""
    js = (STIL.parents[1] / "js" / "innlegging.js").read_text(encoding="utf-8")
    for forbudt in ("fetch(", "XMLHttpRequest", ".submit(", "sendBeacon", "location"):
        assert forbudt not in js


@pytest.mark.parametrize("felt", ["cv", "annonse"])
@pytest.mark.parametrize("type", [FeilType.TOM, FeilType.IKKE_TESTDATA])
def test_fr9_alle_feil_pa_innleggingen_har_tekst(felt, type):
    """FR-9/FR-34/AD-9: hver feil kjernen kan gi på innleggingen, har en tekst som begynner
    med feltnavnet."""
    navn = tekster.INNLEGGINGSFELT[felt].navn
    assert tekster.feiltekst(InndataFeil(felt, type)).startswith(f"{navn}: ")


# --- CSS ---


def test_nfr7_feltene_side_om_side_fra_1000_px():
    """NFR-7/UX-DR19: feltene står under hverandre og side om side først fra 1000 px."""
    css = STIL.read_text(encoding="utf-8")
    bred = re.search(r"@media \(min-width: 1000px\)\s*\{(.*?)\n\}", css, re.S).group(1)
    assert ".felt-rad" in bred
    assert "grid-template-columns: repeat(2" in bred
    assert "grid-template-columns" not in css_blokk(css, ".felt-rad")


def test_nfr7_tekstboksen_kan_dras_storre():
    """NFR-7/UX-DR8: tekstboksen kan dras større, ca. 160 px høy på PC og 200 px på mobil,
    uten fast høyde."""
    css = STIL.read_text(encoding="utf-8")
    blokk = css_blokk(css, ".limeboks textarea")
    assert "resize: vertical" in blokk
    assert "min-height: 160px" in blokk
    assert re.search(
        r"@media \(max-width: 699px\)\s*\{\s*\.limeboks textarea\s*\{\s*min-height: 200px", css
    )


def test_ux_dr8_soppelbotta_er_minst_24_px_og_feil_er_rode():
    """UX-DR8/WCAG 2.5.8: søppelbøtta er minst 24 × 24 px. Felt med feil og feilboksen bruker
    error-fargene, og hidden skjuler alltid."""
    css = STIL.read_text(encoding="utf-8")
    soppel = css_blokk(css, ".soppelbotte")
    assert "min-width: 24px" in soppel
    assert "min-height: 24px" in soppel
    assert "var(--error)" in css_blokk(css, ".innleggingsfelt.har-feil")
    assert "var(--error-tint)" in css_blokk(css, ".feilboks")
    assert "dashed" in css_blokk(css, ".testhjelp")
    assert "display: none !important" in css_blokk(css, "[hidden]")


def test_ux_dr7_lim_inn_viser_fokusringen_ogsa_etter_museklikk():
    """UX-DR7: en lenke i feilboksen gir fokus til «Lim inn tekst». Ringen vises med :focus,
    ikke bare :focus-visible, så den synes også når lenken ble trykket med musa."""
    blokk = css_blokk(STIL.read_text(encoding="utf-8"), ".lim-inn:focus")
    assert "outline: 3px solid var(--focus-ring)" in blokk
