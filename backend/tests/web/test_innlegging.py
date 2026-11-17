"""Tester for innleggingssiden: feltene, sjekken av det som er lagt inn, feilboksen og
«Tilbake» (FR-8, FR-9, FR-13, FR-19, FR-34, NFR-4, NFR-6, NFR-7, AD-1, AD-8, AD-9,
UX-DR7, UX-DR8, UX-DR9, UX-DR21). Story 2.5.1. Analysen og KI-feilen (FR-15, FR-21,
FR-28) kom i story 2.5.2. Brevfeltet i Korrektur (FR-8, FR-9, FR-20, FR-34) kom i story
5.1. Opplasting av PDF, filnavnet, PDF-tipset og hjelpeteksten om tegngrensen (FR-8, FR-13,
NFR-4, NFR-11) kom i story 6.1. Feilmeldingene for filer og 413-håndtereren (FR-10, FR-11,
FR-12) kom i story 6.2."""

import html as html_modul
import re
from io import BytesIO

import pytest

from soknad import create_app
from soknad.adaptere import pdf_inn
from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.adaptere.pdf_inn import les_pdf
from soknad.innstillinger import MAKS_FILSTORRELSE, MAKS_TEGN, MAKS_TEGN_EGET_BREV
from soknad.kjerne import inndata
from soknad.kjerne.feil import FeilType, InndataFeil, KIFeil, KIFeilType
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.kjerne.testdata_match import vask
from soknad.web import ruter, tekster
from soknad.web.innlogging import OKT_ID
from tests.web.hjelpere import (
    ANNONSE,
    CV,
    EGET_BREV,
    GAP_SVAR,
    NOKKELORD_SVAR,
    STIL,
    FeilendeKI,
    css_blokk,
    element,
    html_av,
    logg_inn,
    main,
    okt_id,
    sett_soknad,
    sett_testmodus,
    soknaden,
    tagger_i,
)

TOM_CV = "CV: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
TOM_ANNONSE = "Stillingsannonse: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
IKKE_TESTDATA_CV = "CV: I testmodus fungerer bare testdataene fra mappen backend/testdata/."
IKKE_TESTDATA_ANNONSE = (
    "Stillingsannonse: I testmodus fungerer bare testdataene fra mappen backend/testdata/."
)


def til_innlegging(app, client):
    sett_soknad(app, client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))


def uten_testmodus(app, client):
    """Slår av testmodus på samme økt-id. Søknaden beholdes (sett_testmodus)."""
    sett_testmodus(app, client, False)


def send(client, cv, annonse, handling="sjekk"):
    return client.post("/innlegging", data={"cv": cv, "annonse": annonse, "handling": handling})


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


def test_fr34_cv_og_annonse_fra_ulike_caser_gir_egen_tekst(app, paa_innlegging):
    """FR-34 (story 4.5): CV-en fra case 1 og annonsen fra case 2 gir den egne teksten på
    annonsefeltet, og KI-en kalles ikke (ingen analyse i søknaden)."""
    case_2 = TESTDATA_MAPPE / "case-2-okonomi"
    annonse_2 = (case_2 / "annonse.txt").read_text(encoding="utf-8")
    html = html_av(send(paa_innlegging, CV, annonse_2))
    assert feilboks_lenker(html) == [
        (
            "#annonse-felt",
            "Stillingsannonse: I testmodus må CV-en og annonsen være fra samme mappe i "
            "backend/testdata/.",
        )
    ]
    assert soknaden(app, paa_innlegging).nokkelord is None
    assert soknaden(app, paa_innlegging).steg == Steg.INNLEGGING


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
    """FR-9 (story 5.1): feltene på siden (tekster.py) og rekkefølgen på feilene (inndata.py)
    er de samme, så feilboksen og feltene ikke kommer i ulik rekkefølge. Feltene for hver
    modus står i den samme rekkefølgen."""
    assert tuple(tekster.INNLEGGINGSFELT) == inndata.INNLEGGINGSFELT
    for modus in Modus:
        felter = inndata.felt_for_modus(modus)
        assert felter == tuple(navn for navn in inndata.INNLEGGINGSFELT if navn in felter)


def test_fr8_tomme_felt_viser_last_opp_og_lim_inn_tekst(paa_innlegging):
    """FR-8/UX-DR8 (story 6.1): tomme felt viser «Last opp PDF» og så «Lim inn tekst», og
    tekstboksen og filnavnet er skjult. Tekstboksen står i skjemaet med riktig navn."""
    html = html_av(paa_innlegging.get("/innlegging"))
    for navn in ("cv", "annonse"):
        felt = re.search(rf'<section[^>]*id="{navn}-felt".*?</section>', html, re.S).group(0)
        assert re.search(
            r'<div class="tom-tilstand">\s*<button[^>]*id="'
            + navn
            + r'-last-opp"[^>]*>Last opp PDF</button>\s*<button[^>]*id="'
            + navn
            + '-lim-inn"',
            felt,
        )
        assert '<div class="limeboks" hidden>' in felt
        assert '<div class="filboks" hidden>' in felt
        assert element(html, f"{navn}-tekst")["name"] == navn


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
    # To søppelbøtter per felt: ved filnavnet og ved tekstboksen (story 6.1).
    soppel = [a for t, a in tagger_i(html) if a.get("class") == "soppelbotte"]
    assert [(a["aria-label"], a["data-tomt"], a["type"]) for a in soppel] == [
        ("Tøm CV-feltet", "CV-feltet er tømt", "button"),
        ("Tøm CV-feltet", "CV-feltet er tømt", "button"),
        ("Tøm annonsefeltet", "Annonsefeltet er tømt", "button"),
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
    assert element(html, "cv-tekst")["aria-describedby"] == "cv-feil cv-hjelp"
    assert element(html, "cv-tekst")["aria-invalid"] == "true"
    assert element(html, "annonse-felt")["class"] == "innleggingsfelt"
    assert element(html, "annonse-tekst")["aria-describedby"] == "annonse-hjelp"
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


@pytest.mark.parametrize("felt", ["cv", "eget_brev", "annonse"])
@pytest.mark.parametrize(
    "type",
    [
        FeilType.TOM,
        FeilType.FEIL_FILTYPE,
        FeilType.FOR_STOR,
        FeilType.ULESELIG,
        FeilType.FOR_LANG,
        FeilType.IKKE_TESTDATA,
    ],
)
def test_fr9_alle_feil_pa_innleggingen_har_tekst(felt, type):
    """FR-9/FR-10/FR-11/FR-12/FR-34/AD-9 (story 5.1 og 6.2): hver feil kjernen kan gi på
    innleggingen, også filfeilene og feilene på brevfeltet, har en tekst som begynner med
    feltnavnet."""
    navn = tekster.INNLEGGINGSFELT[felt].navn
    assert tekster.feiltekst(InndataFeil(felt, type)).startswith(f"{navn}: ")


# --- CSS ---


def test_nfr7_feltene_side_om_side_fra_1000_px():
    """NFR-7/UX-DR19 (story 5.1): feltene står under hverandre og side om side først fra
    1000 px, i to kolonner, og i tre kolonner når det er tre felt (Korrektur)."""
    css = STIL.read_text(encoding="utf-8")
    bred = re.search(r"@media \(min-width: 1000px\)\s*\{(.*?)\n\}", css, re.S).group(1)
    assert "grid-template-columns: repeat(2" in css_blokk(bred.replace("\n  ", "\n"), ".felt-rad")
    tre = css_blokk(bred.replace("\n  ", "\n"), ".felt-rad.tre-felt")
    assert "grid-template-columns: repeat(3" in tre
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


# --- Korrektur: brevfeltet (story 5.1, FR-8, FR-9, FR-20, FR-34) ---

TOM_BREV = "Ditt søknadsbrev: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
FOR_LANG_BREV = "Ditt søknadsbrev: Teksten er for lang. Den kan være på høyst 5 000 tegn."
IKKE_TESTDATA_BREV = (
    "Ditt søknadsbrev: I testmodus fungerer bare testdataene fra mappen backend/testdata/."
)
CASE_2 = TESTDATA_MAPPE / "case-2-okonomi"


def send_korrektur(client, cv, eget_brev, annonse, handling="sjekk"):
    data = {"cv": cv, "eget_brev": eget_brev, "annonse": annonse, "handling": handling}
    return client.post("/innlegging", data=data)


def brevfeltet(html):
    """HTML-en for seksjonen med brevfeltet."""
    return re.search(r'<section[^>]*id="eget_brev-felt".*?</section>', html, re.S).group(0)


def test_fr8_korrektur_har_overskriften_og_tre_felt_i_rekkefolge(paa_korrektur):
    """FR-8/FR-20 (story 5.1): innleggingen i Korrektur har overskriften og tittelen for
    Korrektur, og feltene «📄 CV», «✉️ Ditt søknadsbrev» og «📢 Stillingsannonse» i den
    rekkefølgen, i en rad med tre kolonner."""
    html = html_av(paa_korrektur.get("/innlegging"))
    assert re.search(
        r"<h1[^>]*>\s*Legg inn CV-en din, brevet ditt og stillingsannonsen\s*</h1>", html
    )
    assert "<title>Legg inn CV, brev og annonse – Søknadsassistenten</title>" in html
    assert re.findall(r'<h2 class="feltnavn"[^>]*>(.*?)</h2>', html, re.S) == [
        '<span aria-hidden="true">📄</span> CV',
        '<span aria-hidden="true">✉️</span> Ditt søknadsbrev',
        '<span aria-hidden="true">📢</span> Stillingsannonse',
    ]
    seksjoner = [a["id"] for t, a in tagger_i(html) if t == "section"]
    assert seksjoner == ["cv-felt", "eget_brev-felt", "annonse-felt"]
    assert '<div class="felt-rad tre-felt">' in html


def test_fr8_brevfeltet_har_samme_tilstander_og_knapper(app, paa_korrektur):
    """FR-8/UX-DR8/NFR-6 (story 5.1): brevfeltet har samme tom tilstand, «Lim inn tekst»,
    søppelbøtte og skjermlesertekster som de andre feltene. Tekstboksen heter eget_brev."""
    html = html_av(paa_korrektur.get("/innlegging"))
    felt = brevfeltet(html)
    assert re.search(
        r'<div class="tom-tilstand">\s*<button[^>]*id="eget_brev-last-opp".*?'
        r'<button[^>]*id="eget_brev-lim-inn"',
        felt,
        re.S,
    )
    assert '<div class="limeboks" hidden>' in felt
    assert element(html, "eget_brev-tekst")["name"] == "eget_brev"
    assert element(html, "eget_brev-lim-inn")["aria-label"] == "Lim inn tekst, Ditt søknadsbrev"
    etikett = (
        '<label for="eget_brev-tekst"><span class="skjult">Ditt søknadsbrev: </span>'
        "Lim inn teksten her</label>"
    )
    assert etikett in felt
    soppel = [a for t, a in tagger_i(felt) if a.get("class") == "soppelbotte"]
    assert [(a["aria-label"], a["data-tomt"]) for a in soppel] == [
        ("Tøm brevfeltet", "Brevfeltet er tømt")
    ] * 2
    # Et fylt brevfelt viser tekstboksen med teksten, og «Lim inn tekst» er skjult.
    sett_soknad(
        app,
        paa_korrektur,
        Soknad(steg=Steg.INNLEGGING, modus=Modus.KORREKTUR, eget_brev=Tekstfelt("Mitt brev")),
    )
    html = html_av(paa_korrektur.get("/innlegging"))
    assert '<div class="tom-tilstand" hidden>' in brevfeltet(html)
    assert tekstboks(html, "eget_brev") == "Mitt brev"


def test_fr8_full_generering_har_to_felt_og_den_gamle_overskriften(paa_innlegging):
    """FR-8/FR-20 (story 5.1): i Full generering er det to felt og den gamle overskriften og
    tittelen, akkurat som før. Ingen brevfelt og ingen tre kolonner."""
    html = html_av(paa_innlegging.get("/innlegging"))
    assert re.search(r"<h1[^>]*>\s*Legg inn CV-en din og stillingsannonsen\s*</h1>", html)
    assert "<title>Legg inn CV og annonse – Søknadsassistenten</title>" in html
    assert [a["id"] for t, a in tagger_i(html) if t == "section"] == ["cv-felt", "annonse-felt"]
    assert "eget_brev" not in html
    assert "Ditt søknadsbrev" not in html
    assert '<div class="felt-rad">' in html


def test_fr34_korrektur_med_testdata_gir_resultatsiden(app, paa_korrektur):
    """FR-8/FR-34 (story 5.1): CV, eget brev og annonse fra case 1 i testmodus gir analysen og
    resultatsiden. Brevet er lagret i søknaden."""
    svar = send_korrektur(paa_korrektur, CV, EGET_BREV, ANNONSE)
    assert svar.status_code == 302
    assert svar.location == "/resultat"
    soknad = soknaden(app, paa_korrektur)
    assert soknad.eget_brev == Tekstfelt(EGET_BREV)
    assert soknad.gap == GAP_SVAR
    assert soknad.steg == Steg.RESULTAT


def test_fr9_tomt_brev_gir_feil_og_ingen_ki_kall(app, paa_korrektur):
    """FR-9 (story 5.1): CV og annonse fylt ut og brevet tomt gir feilen på brevfeltet, med
    rød ramme og koblet feiltekst, og KI-en kalles ikke."""
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    svar = send_korrektur(paa_korrektur, CV, "  \n", ANNONSE)
    assert svar.status_code == 200
    html = html_av(svar)
    assert feilboks_lenker(html) == [("#eget_brev-felt", TOM_BREV)]
    assert element(html, "eget_brev-felt")["class"] == "innleggingsfelt har-feil"
    assert element(html, "eget_brev-tekst")["aria-invalid"] == "true"
    assert element(html, "eget_brev-tekst")["aria-describedby"] == "eget_brev-feil eget_brev-hjelp"
    assert element(html, "eget_brev-lim-inn")["aria-describedby"] == "eget_brev-feil"
    assert kalt == []
    assert soknaden(app, paa_korrektur).steg == Steg.INNLEGGING


def test_nfr11_for_langt_brev_gir_feil_og_ingen_ki_kall(app, paa_korrektur):
    """NFR-11/FR-9 (story 5.1, retro 5 runde B): et brev på over 5 000 tegn gir feilen på
    brevfeltet, og KI-en kalles ikke."""
    kalt = []
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=None, kalt=kalt)
    html = html_av(send_korrektur(paa_korrektur, CV, "a" * 5_001, ANNONSE))
    assert feilboks_lenker(html) == [("#eget_brev-felt", FOR_LANG_BREV)]
    assert kalt == []


def test_fr34_ukjent_brev_gir_ikke_testdata_pa_brevet(app, paa_korrektur):
    """FR-34 (story 5.1): i testmodus gir CV-en fra case 1 med en egen brevtekst
    ikke_testdata på brevfeltet. Alle tre tekstene står igjen."""
    html = html_av(send_korrektur(paa_korrektur, CV, "Mitt eget brev", ANNONSE))
    assert feilboks_lenker(html) == [("#eget_brev-felt", IKKE_TESTDATA_BREV)]
    assert tekstboks(html, "cv") == CV
    assert tekstboks(html, "eget_brev") == "Mitt eget brev"
    assert tekstboks(html, "annonse") == ANNONSE
    assert soknaden(app, paa_korrektur).nokkelord is None


def test_fr34_case_2_i_korrektur_gir_ikke_testdata_pa_brevet(app, paa_korrektur):
    """FR-34 (story 5.1, bestemt av Kristine 15. november 2026): CV og annonse fra case 2,
    som ikke har noe brev, gir den vanlige teksten på brevfeltet, også med brevet fra case 1."""
    cv_2 = (CASE_2 / "cv.txt").read_text(encoding="utf-8")
    annonse_2 = (CASE_2 / "annonse.txt").read_text(encoding="utf-8")
    html = html_av(send_korrektur(paa_korrektur, cv_2, EGET_BREV, annonse_2))
    assert feilboks_lenker(html) == [("#eget_brev-felt", IKKE_TESTDATA_BREV)]
    assert soknaden(app, paa_korrektur).nokkelord is None


def test_fr9_alle_tomme_i_korrektur_gir_feilene_i_rekkefolgen_cv_brev_annonse(paa_korrektur):
    """FR-9 (story 5.1): alle feltene tomme gir tre feil i feilboksen, i rekkefølgen CV, brev,
    annonse, som feltene på siden."""
    html = html_av(send_korrektur(paa_korrektur, "", "", ""))
    assert feilboks_lenker(html) == [
        ("#cv-felt", TOM_CV),
        ("#eget_brev-felt", TOM_BREV),
        ("#annonse-felt", TOM_ANNONSE),
    ]


def test_fr8_korrektur_uten_testmodus_kjorer_analysen(med_nokkel):
    """FR-8/FR-15 (story 5.1): uten testmodus, med samtykke og alle tre feltene fylt ut, kjøres
    analysen som i Full generering (nøkkelord og gap), og brevet lagres."""
    app, client, kalt = med_nokkel
    sett_soknad(app, client, Soknad(steg=Steg.INNLEGGING, modus=Modus.KORREKTUR, samtykke=True))
    svar = send_korrektur(client, CV, "Mitt eget brev", ANNONSE)
    assert svar.location == "/resultat"
    assert kalt == ["nokkelord", "gap"]
    assert soknaden(app, client).eget_brev == Tekstfelt("Mitt eget brev")


def test_fr8_full_generering_ignorerer_eget_brev_i_skjemaet(app, paa_innlegging):
    """FR-8 (story 5.1): i Full generering ignoreres et eget_brev i skjemaet. Brevet i
    søknaden er uendret, og analysen kjøres som før."""
    lagret = Tekstfelt("Mitt lagrede brev")
    sett_soknad(
        app,
        paa_innlegging,
        Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, eget_brev=lagret),
    )
    svar = send_korrektur(paa_innlegging, CV, "Et brev som ikke skal lagres", ANNONSE)
    assert svar.location == "/resultat"
    assert soknaden(app, paa_innlegging).eget_brev == lagret


def test_fr20_tilbake_til_modusvalget_beholder_alle_tre_feltene(paa_korrektur):
    """FR-20 (story 5.1): Korrektur → «Tilbake» → Full generering → Korrektur: CV, annonse og
    brev står der fortsatt. Full generering viser CV og annonse, men ikke brevet."""
    svar = send_korrektur(paa_korrektur, "Min CV", "Mitt brev", "Min annonse", "tilbake")
    assert svar.location == "/modus"
    svar = paa_korrektur.post("/modus", data={"modus": "full_generering"})
    assert svar.location == "/innlegging"
    html = html_av(paa_korrektur.get("/innlegging"))
    assert tekstboks(html, "cv") == "Min CV"
    assert tekstboks(html, "annonse") == "Min annonse"
    assert "Mitt brev" not in html
    assert send(paa_korrektur, "Min CV", "Min annonse", "tilbake").location == "/modus"
    paa_korrektur.post("/modus", data={"modus": "korrektur"})
    html = html_av(paa_korrektur.get("/innlegging"))
    assert tekstboks(html, "cv") == "Min CV"
    assert tekstboks(html, "eget_brev") == "Mitt brev"
    assert tekstboks(html, "annonse") == "Min annonse"


# --- Laste opp PDF (story 6.1, FR-8, FR-13, FR-34, NFR-4, NFR-6, NFR-7, AD-1) ---

PDF_CV = (TESTDATA_MAPPE / "case-1-utvikler" / "cv.pdf").read_bytes()
PDF_ANNONSE = (TESTDATA_MAPPE / "case-1-utvikler" / "annonse.pdf").read_bytes()
PDF_BREV = (TESTDATA_MAPPE / "case-1-utvikler" / "eget-brev.pdf").read_bytes()


def send_felt(client, handling="sjekk", **felt):
    """Sender innleggingen med hvert felt som tekst (en str) eller som fil (bytes, filnavn).
    En fil får <navn>_kilde=fil, en tekst <navn>_kilde=tekst. None gir kilde=fil uten ny fil
    (filnavnet fra økten står på siden)."""
    data = {"handling": handling}
    for navn, verdi in felt.items():
        if verdi is None:
            data[f"{navn}_kilde"] = "fil"
            data[navn] = ""
        elif isinstance(verdi, tuple):
            innhold, filnavn = verdi
            data[f"{navn}_kilde"] = "fil"
            data[f"{navn}_fil"] = (BytesIO(innhold), filnavn)
            data[navn] = ""
        else:
            data[f"{navn}_kilde"] = "tekst"
            data[navn] = verdi
    return client.post("/innlegging", data=data, content_type="multipart/form-data")


def felt_html(html, navn):
    return re.search(rf'<section[^>]*id="{navn}-felt".*?</section>', html, re.S).group(0)


def test_fr8_tomt_felt_har_last_opp_pdf_med_filvelger(paa_innlegging):
    """FR-8/NFR-6 (story 6.1): «Last opp PDF» er en hovedknapp med feltnavnet for
    skjermlesere og står før «Lim inn tekst». Filvelgeren er skjult, godtar .pdf og heter
    <navn>_fil, og <navn>_kilde er tekst."""
    html = html_av(paa_innlegging.get("/innlegging"))
    for navn, feltnavn in (("cv", "CV"), ("annonse", "Stillingsannonse")):
        knapp = element(html, f"{navn}-last-opp")
        assert knapp["class"] == "hovedknapp last-opp"
        assert knapp["type"] == "button"
        assert knapp["aria-label"] == f"Last opp PDF, {feltnavn}"
        assert "aria-describedby" not in knapp
        fil = element(html, f"{navn}-fil")
        assert (fil["type"], fil["name"], fil["accept"]) == ("file", f"{navn}_fil", ".pdf")
        assert "hidden" in fil
        assert fil["class"] == "filvelger"
        assert fil["data-lastet-opp"] == f"{feltnavn} lastet opp: "
        kilde = next(a for _, a in tagger_i(html) if a.get("name") == f"{navn}_kilde")
        assert (kilde["type"], kilde["value"], kilde["class"]) == ("hidden", "tekst", "kilde")
        assert html.index(f'id="{navn}-last-opp"') < html.index(f'id="{navn}-lim-inn"')


def test_fr9_last_opp_er_koblet_til_feilteksten(paa_innlegging):
    """FR-9/UX-DR8 (story 6.1): i et felt med feil er «Last opp PDF» koblet til feilteksten,
    som «Lim inn tekst»."""
    html = html_av(send(paa_innlegging, "", ANNONSE))
    assert element(html, "cv-last-opp")["aria-describedby"] == "cv-feil"
    assert "aria-describedby" not in element(html, "annonse-last-opp")


@pytest.mark.parametrize("modus", list(Modus))
def test_fr8_pdf_tipset_star_over_feltene_i_begge_modusene(app, innlogget_client, modus):
    """FR-8 (story 6.1): PDF-tipset står over feltene i begge modusene, og skjemaet sender
    filer (multipart/form-data)."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=modus))
    html = html_av(innlogget_client.get("/innlegging"))
    tips = (
        '<p class="pdf-tips">Tips: PDF lagret fra Word leses best. Er CV-en laget i Canva eller '
        "et lignende program, kan teksten komme i feil rekkefølge. Lim den da heller inn.</p>"
    )
    assert tips in html
    assert html.index(tips) < html.index('id="cv-felt"')
    skjema = next(a for t, a in tagger_i(html) if t == "form" and a.get("id"))
    assert skjema["enctype"] == "multipart/form-data"


def test_fr8_pdf_tipset_ogsa_uten_testmodus(app, paa_innlegging):
    """FR-8 (story 6.1): tipset står der også når testmodus er av."""
    uten_testmodus(app, paa_innlegging)
    assert tekster.PDF_TIPS in html_av(paa_innlegging.get("/innlegging"))


def test_fr8_fr34_pdf_fra_case_1_gir_samme_resultat_som_tekst(app, paa_innlegging):
    """FR-8/FR-34 (kriterium 5): cv.pdf og annonse.pdf fra case 1 i testmodus gir
    resultatsiden, med det samme som cv.txt og annonse.txt gir. Teksten fra pdf_inn og
    filnavnet ligger i økten."""
    svar = send_felt(paa_innlegging, cv=(PDF_CV, "cv.pdf"), annonse=(PDF_ANNONSE, "annonse.pdf"))
    assert svar.location == "/resultat"
    soknad = soknaden(app, paa_innlegging)
    assert soknad.cv == Tekstfelt(les_pdf(PDF_CV), "cv.pdf")
    assert soknad.annonse == Tekstfelt(les_pdf(PDF_ANNONSE), "annonse.pdf")
    assert soknad.gap == GAP_SVAR
    pdf_resultat = html_av(paa_innlegging.get("/resultat"))
    til_innlegging(app, paa_innlegging)
    assert send(paa_innlegging, CV, ANNONSE).location == "/resultat"
    assert html_av(paa_innlegging.get("/resultat")) == pdf_resultat


def test_fr8_eget_brev_som_pdf_i_korrektur(app, paa_korrektur):
    """FR-8 (story 6.1): i Korrektur kan også brevet lastes opp som PDF, og CV, brev og annonse
    fra case 1 gir resultatsiden."""
    svar = send_felt(
        paa_korrektur,
        cv=(PDF_CV, "cv.pdf"),
        eget_brev=(PDF_BREV, "eget-brev.pdf"),
        annonse=ANNONSE,
    )
    assert svar.location == "/resultat"
    soknad = soknaden(app, paa_korrektur)
    assert soknad.eget_brev == Tekstfelt(les_pdf(PDF_BREV), "eget-brev.pdf")
    assert soknad.annonse == Tekstfelt(ANNONSE)


@pytest.mark.parametrize("sendt", ["cv.pdf", "mappe/under/cv.pdf"])
def test_fr8_filnavnet_lagres_uten_mappene(app, paa_innlegging, sendt):
    """FR-8 (story 6.1): bare delen etter siste / lagres som filnavn."""
    send_felt(paa_innlegging, cv=(PDF_CV, sendt), annonse=ANNONSE, handling="tilbake")
    assert soknaden(app, paa_innlegging).cv.filnavn == "cv.pdf"


@pytest.mark.parametrize(
    ("sendt", "lagret"),
    [
        ("C:\\Users\\Sara\\Dokumenter\\cv.pdf", "cv.pdf"),
        ("mappe/under\\min cv.pdf", "min cv.pdf"),
        ("Søknad æøå.pdf", "Søknad æøå.pdf"),
        ("mappe/", "mappe/"),
    ],
)
def test_fr8_filnavnet_uten_mappe(sendt, lagret):
    """FR-8 (story 6.1): bare delen etter siste / eller \\ lagres, og æøå og mellomrom står
    igjen. (Werkzeug fjerner selv en \\ som ikke er escapet i forespørselen, så den delen
    prøves her og ikke gjennom skjemaet.)"""
    assert ruter._uten_mappe(sendt) == lagret


def test_fr8_tilbake_og_inn_igjen_viser_filnavnet(app, paa_innlegging):
    """FR-8/FR-19 (story 6.1): etter «Tilbake» med en PDF vises filnavnet fra økten med ✓ og
    søppelbøtta. Tekstboksen er tom og skjult, og kilden er fil."""
    svar = send_felt(paa_innlegging, cv=(PDF_CV, "cv.pdf"), annonse=ANNONSE, handling="tilbake")
    assert svar.location == "/modus"
    html = html_av(paa_innlegging.get("/innlegging"))
    cv = felt_html(html, "cv")
    assert '<div class="tom-tilstand" hidden>' in cv
    assert '<div class="limeboks" hidden>' in cv
    assert re.search(
        r'<div class="filboks">\s*<span aria-hidden="true">✓</span>\s*'
        r'<span class="filnavn" title="cv\.pdf">cv\.pdf</span>\s*<button class="soppelbotte"',
        cv,
    )
    assert tekstboks(html, "cv") == ""
    kilde = next(a for _, a in tagger_i(html) if a.get("name") == "cv_kilde")
    assert kilde["value"] == "fil"
    # Annonsen er limt inn og vises i tekstboksen, uten filnavn.
    annonse = felt_html(html, "annonse")
    assert '<div class="filboks" hidden>' in annonse
    assert '<span class="filnavn" title=""></span>' in annonse


def test_fr8_sjekk_uten_ny_fil_bruker_lagret_tekst(app, paa_innlegging):
    """FR-8 (story 6.1): kilde=fil uten ny fil (siden etter «Tilbake») bruker teksten og
    filnavnet fra økten, både ved «Tilbake» og ved «Sjekk CV-en min»."""
    send_felt(paa_innlegging, cv=(PDF_CV, "cv.pdf"), annonse=ANNONSE, handling="tilbake")
    lagret = soknaden(app, paa_innlegging).cv
    send_felt(paa_innlegging, cv=None, annonse=ANNONSE, handling="tilbake")
    assert soknaden(app, paa_innlegging).cv == lagret
    assert send_felt(paa_innlegging, cv=None, annonse=ANNONSE).location == "/resultat"
    assert soknaden(app, paa_innlegging).cv == lagret


def test_fr8_kilde_tekst_ignorerer_en_fil(app, paa_innlegging):
    """FR-8 (story 6.1): med kilde=tekst brukes tekstboksen, også om en fil er sendt med
    (søppelbøtta, så «Lim inn tekst»)."""
    data = {
        "cv_kilde": "tekst",
        "cv": "Min egen CV",
        "cv_fil": (BytesIO(PDF_CV), "cv.pdf"),
        "annonse": ANNONSE,
        "handling": "tilbake",
    }
    paa_innlegging.post("/innlegging", data=data, content_type="multipart/form-data")
    assert soknaden(app, paa_innlegging).cv == Tekstfelt("Min egen CV")


def test_fr13_soppelbotta_pa_filnavnet_tommer_lagret_fil(app, paa_innlegging):
    """FR-13 (story 6.1): søppelbøtta på filnavnet setter kilden til tekst med tom tekstboks,
    så den lagrede PDF-en er borte etter neste innsending."""
    send_felt(paa_innlegging, cv=(PDF_CV, "cv.pdf"), annonse=ANNONSE, handling="tilbake")
    send_felt(paa_innlegging, cv="", annonse=ANNONSE, handling="tilbake")
    assert soknaden(app, paa_innlegging).cv == Tekstfelt("")


def test_fr9_feil_i_annet_felt_beholder_filnavnet(app, paa_innlegging):
    """FR-9 (story 6.1): PDF i CV-feltet og tom annonse gir siden på nytt med filnavnet i
    CV-feltet og feilen på annonsen. Et nytt forsøk uten ny fil bruker den lagrede CV-en."""
    svar = send_felt(paa_innlegging, cv=(PDF_CV, "cv.pdf"), annonse="")
    assert svar.status_code == 200
    html = html_av(svar)
    assert feilboks_lenker(html) == [("#annonse-felt", TOM_ANNONSE)]
    assert '<span class="filnavn" title="cv.pdf">cv.pdf</span>' in felt_html(html, "cv")
    assert soknaden(app, paa_innlegging).cv.filnavn == "cv.pdf"
    assert send_felt(paa_innlegging, cv=None, annonse=ANNONSE).location == "/resultat"


@pytest.mark.parametrize(
    ("modus", "navn", "lengde"),
    [
        (Modus.FULL_GENERERING, "cv", MAKS_TEGN + 1),
        (Modus.KORREKTUR, "eget_brev", MAKS_TEGN_EGET_BREV + 1),
    ],
)
def test_nfr11_for_lang_tekst_fra_pdf_gir_for_lang(
    app, innlogget_client, monkeypatch, modus, navn, lengde
):
    """NFR-11/FR-9 (story 6.1): en PDF med mer tekst enn grensen for feltet gir den vanlige
    feilen for_lang. Filnavnet står i filboksen, og søppelbøtta ved det er koblet til
    feilteksten."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=modus))
    monkeypatch.setattr(pdf_inn, "les_pdf", lambda innhold: "a" * lengde)
    felt = {"cv": CV, "annonse": ANNONSE}
    if modus == Modus.KORREKTUR:
        felt["eget_brev"] = EGET_BREV
    felt[navn] = (b"%PDF-1.7", "lang.pdf")
    svar = send_felt(innlogget_client, **felt)
    assert svar.status_code == 200
    html = html_av(svar)
    tekst = tekster.feiltekst(InndataFeil(navn, FeilType.FOR_LANG))
    assert feilboks_lenker(html) == [(f"#{navn}-felt", tekst)]
    filboks = re.search(r'<div class="filboks">.*?</div>', felt_html(html, navn), re.S).group(0)
    assert '<span class="filnavn" title="lang.pdf">lang.pdf</span>' in filboks
    assert f'aria-describedby="{navn}-feil"' in filboks


def test_fr8_samme_tekst_med_nytt_filnavn_beholder_analysen(app, innlogget_client):
    """FR-8/FR-19 (story 6.1, retro 2 A9): er teksten fra PDF-en den samme som den lagrede,
    lagres filnavnet, og analysen og steget beholdes."""
    tekst = les_pdf(PDF_CV)
    soknad = Soknad(
        steg=Steg.RESULTAT,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt(tekst),
        annonse=Tekstfelt(ANNONSE),
        nokkelord=("Python",),
        nokkelord_annonse="annonse",
        gap={"dekker": ["Python"], "mangler": []},
    )
    sett_soknad(app, innlogget_client, soknad)
    send_felt(innlogget_client, cv=(PDF_CV, "cv.pdf"), annonse=ANNONSE, handling="tilbake")
    ny = soknaden(app, innlogget_client)
    assert ny.cv == Tekstfelt(tekst, "cv.pdf")
    assert (ny.nokkelord, ny.gap, ny.steg) == (soknad.nokkelord, soknad.gap, Steg.RESULTAT)


def test_nfr4_pdf_teksten_er_bare_i_okten(paa_innlegging, caplog):
    """NFR-4 (story 6.1): teksten fra PDF-en ligger bare i øktlageret, aldri i cookien, og
    verken teksten eller filnavnet logges."""
    caplog.set_level("DEBUG")
    send_felt(paa_innlegging, cv=(PDF_CV, "hemmelig-cv.pdf"), annonse=ANNONSE)
    with paa_innlegging.session_transaction() as okt:
        assert set(okt) == {OKT_ID}
    linjer = [linje for linje in les_pdf(PDF_CV).splitlines() if len(linje.strip()) > 10]
    assert linjer
    assert [linje for linje in linjer if linje in caplog.text] == []
    assert "hemmelig-cv.pdf" not in caplog.text


def test_nfr11_hjelpeteksten_om_tegngrensen_under_tekstboksen(paa_korrektur):
    """NFR-11/NFR-6 (story 6.1, bestemt av Kristine 16. november 2026): under hver tekstboks
    står «Høyst 15 000 tegn.», i brevfeltet «Høyst 5 000 tegn.», med class="hjelpetekst",
    koblet til tekstboksen med aria-describedby."""
    html = html_av(paa_korrektur.get("/innlegging"))
    for navn, tekst in (
        ("cv", "Høyst 15 000 tegn."),
        ("eget_brev", "Høyst 5 000 tegn."),
        ("annonse", "Høyst 15 000 tegn."),
    ):
        assert tekster.maks_tegn_hjelp(navn) == tekst
        assert f'<p class="hjelpetekst" id="{navn}-hjelp">{tekst}</p>' in felt_html(html, navn)
        assert element(html, f"{navn}-tekst")["aria-describedby"] == f"{navn}-hjelp"
        # Hjelpeteksten står under tekstboksen.
        assert html.index(f'id="{navn}-tekst"') < html.index(f'id="{navn}-hjelp"')


def test_fr8_tekstene_for_opplastingen():
    """FR-8/NFR-6 (story 6.1): tekstene for knappen, skjermleserne og hjelpeteksten."""
    assert tekster.LAST_OPP_KNAPP == "Last opp PDF"
    assert tekster.last_opp_skjermleser("cv") == "Last opp PDF, CV"
    assert tekster.last_opp_skjermleser("eget_brev") == "Last opp PDF, Ditt søknadsbrev"
    assert tekster.lastet_opp_skjermleser("cv", "cv.pdf") == "CV lastet opp: cv.pdf"
    assert tekster.lastet_opp_skjermleser("annonse", "a.pdf") == (
        "Stillingsannonse lastet opp: a.pdf"
    )
    assert tekster.maks_tegn_hjelp("cv") == f"Høyst {tekster.MAKS_TEGN_TEKST} tegn."
    assert tekster.maks_tegn_hjelp("eget_brev") == (
        f"Høyst {tekster.MAKS_TEGN_EGET_BREV_TEKST} tegn."
    )


def test_nfr7_ingen_style_i_innleggingen(paa_korrektur):
    """NFR-7 (story 6.1): ingen style= i innleggingen."""
    assert "style=" not in main(html_av(paa_korrektur.get("/innlegging")))


# --- Laste opp PDF: skriptet (story 6.1, FR-8, FR-13, AD-1) ---

JS = (STIL.parents[1] / "js" / "innlegging.js").read_text(encoding="utf-8")


def test_fr8_skriptet_apner_filvelgeren_og_viser_filnavnet():
    """FR-8/NFR-6 (story 6.1): «Last opp PDF» åpner filvelgeren. Når en fil er valgt, vises
    navnet med en gang, kilden blir fil, søppelbøtta får fokus, og statusområdet får «CV
    lastet opp: <filnavn>» (samme ventende-mønster som søppelbøtta)."""
    for tekst in (
        "fil.click();",
        'fil.addEventListener("change"',
        "filnavn.textContent = navn;",
        "filnavn.title = navn;",
        'kilde.value = "fil";',
        'filboks.querySelector(".soppelbotte").focus();',
        "meld(fil.dataset.lastetOpp + navn);",
    ):
        assert tekst in JS, tekst


def test_fr13_soppelbottene_gir_fokus_til_last_opp():
    """FR-13/NFR-6 (story 6.1): begge søppelbøttene tømmer feltet (også filvelgeren), setter
    kilden til tekst og gir fokus til «Last opp PDF» i samme felt. «Lim inn tekst» setter
    kilden til tekst."""
    tom = re.search(r"function tom\(soppelbotte\) \{(.*?)\n    \}", JS, re.S).group(1)
    for tekst in (
        'tekstboks.value = "";',
        'fil.value = "";',
        'kilde.value = "tekst";',
        "lastOpp.focus();",
        "meld(soppelbotte.dataset.tomt);",
    ):
        assert tekst in tom, tekst
    assert 'felt.querySelectorAll(".soppelbotte")' in JS
    assert "limInn.focus()" not in JS
    lim_inn = re.search(r'limInn.addEventListener\("click", function \(\) \{(.*?)\}\);', JS, re.S)
    assert 'kilde.value = "tekst";' in lim_inn.group(1)


def test_ux_dr7_lenken_i_feilboksen_gir_fokus_etter_tilstanden():
    """UX-DR7 (story 6.1): en lenke i feilboksen gir fokus til søppelbøtta når filnavnet vises,
    til tekstboksen når den vises, og ellers til «Last opp PDF»."""
    fokus = re.search(r"function fokusIFeltet\(felt, utenRulling\) \{(.*?)\n  \}", JS, re.S)
    kropp = fokus.group(1)
    assert 'felt.querySelector(".last-opp")' in kropp
    assert 'filboks.querySelector(".soppelbotte")' in kropp
    assert 'limeboks.querySelector("textarea")' in kropp


# --- Laste opp PDF: CSS (story 6.1, NFR-7, UX-DR8) ---


def test_nfr7_filboksen_er_gronn_og_kutter_lange_navn():
    """NFR-7/UX-DR8 (story 6.1): filnavnet står i en grønn stripe med søppelbøtta til høyre. Et
    langt navn kuttes på én linje med line-clamp og brytes hvor som helst, uten fast høyde og
    uten nowrap, så det ikke gir rulling sidelengs."""
    css = STIL.read_text(encoding="utf-8")
    filboks = css_blokk(css, ".filboks")
    for verdi in ("var(--success-tint)", "var(--success)", "var(--rounded-sm)", "display: flex"):
        assert verdi in filboks
    filnavn = css_blokk(css, ".filnavn")
    for verdi in ("-webkit-line-clamp: 1", "overflow-wrap: anywhere", "overflow: hidden"):
        assert verdi in filnavn
    assert "min-width: 0" in filnavn
    assert "margin-left: auto" in css_blokk(css, ".filboks .soppelbotte")
    for blokk in (filboks, filnavn):
        assert not re.search(r"(?<![-\w])height:", blokk)
    assert "nowrap" not in css


def test_nfr7_tom_tilstand_er_en_rad_og_last_opp_er_smal():
    """NFR-7/UX-DR8 (story 6.1): «Last opp PDF» og «Lim inn tekst» står på en rad med luft
    som kan brytes, og «Last opp PDF» er bare så bred som teksten."""
    css = STIL.read_text(encoding="utf-8")
    rad = css_blokk(css, ".tom-tilstand")
    assert "display: flex" in rad
    assert "flex-wrap: wrap" in rad
    assert "gap: var(--space-3)" in rad
    knapp = css_blokk(css, ".hovedknapp.last-opp")
    assert "width: auto" in knapp
    assert "margin-top: 0" in knapp
    assert "var(--text-muted)" in css_blokk(css, ".pdf-tips")


def test_ux_dr7_last_opp_og_soppelbotta_viser_fokusringen_etter_museklikk():
    """UX-DR7 (story 6.1): skriptet gir fokus til «Last opp PDF» og søppelbøtta, også etter et
    museklikk. Ringen vises derfor for :focus, ikke bare :focus-visible."""
    css = STIL.read_text(encoding="utf-8")
    for velger in (".last-opp:focus", ".soppelbotte:focus"):
        assert "outline: 3px solid var(--focus-ring)" in css_blokk(css, velger)


def test_nfr7_filboksen_har_ramme_i_hoykontrast():
    """NFR-7 (story 6.1): i høykontrastmodus forsvinner den grønne bakgrunnen, så filboksen får
    en ramme i CanvasText."""
    css = STIL.read_text(encoding="utf-8")
    hoykontrast = re.search(r"@media \(forced-colors: active\)\s*\{(.*?)\n\}", css, re.S).group(1)
    blokk = css_blokk(hoykontrast.replace("\n  ", "\n"), ".filboks")
    assert "border: 1px solid CanvasText" in blokk


# --- Feilmeldinger for filer (story 6.2, FR-10, FR-11, FR-12, NFR-4, UX-DR7, UX-DR8) ---

FEILFILER = TESTDATA_MAPPE / "feil"
FEIL_TYPE_DOCX = (FEILFILER / "feil-type.docx").read_bytes()
SKANNET = (FEILFILER / "skannet.pdf").read_bytes()
# En ekte PDF fylt opp til 5 MB + 1 byte (for_stor, fila leses ikke).
FOR_STOR_PDF = PDF_CV.ljust(MAKS_FILSTORRELSE + 1, b" ")
FOR_STORE = "Filene er for store. Hver fil kan være på høyst 5 MB."

# Fila som gir hver feil, og navnet den sendes med.
FILFEIL = {
    FeilType.FEIL_FILTYPE: (FEIL_TYPE_DOCX, "feil-type.docx"),
    FeilType.FOR_STOR: (FOR_STOR_PDF, "stor.pdf"),
    FeilType.ULESELIG: (SKANNET, "skannet.pdf"),
}

# Gyldige tekster til feltene, fra case 1 (testdata, så de gir ingen feil i testmodus).
GYLDIG = {"cv": CV, "eget_brev": EGET_BREV, "annonse": ANNONSE}


def feiltekst(navn, type):
    return tekster.feiltekst(InndataFeil(navn, type))


@pytest.fixture
def lest(monkeypatch):
    """Lista over hvert innhold pdf_inn.les_pdf har fått, så testene ser om fila ble lest."""
    lest = []
    ekte = pdf_inn.les_pdf

    def les(innhold):
        lest.append(innhold)
        return ekte(innhold)

    monkeypatch.setattr(pdf_inn, "les_pdf", les)
    return lest


def test_fr10_fr11_fr12_tekstene_for_filfeilene():
    """FR-10/FR-11/FR-12 (story 6.2): tekstene fra UX, med feltnavnet først, og 5 MB fra
    MAKS_FILSTORRELSE. Feilen for hele forespørselen har ikke feltnavn."""
    assert feiltekst("cv", FeilType.FEIL_FILTYPE) == "CV: Feil filtype, prøv PDF."
    assert (
        feiltekst("annonse", FeilType.FOR_STOR)
        == "Stillingsannonse: Filen er for stor. Den kan være på høyst 5 MB."
    )
    assert feiltekst("eget_brev", FeilType.ULESELIG) == (
        "Ditt søknadsbrev: Vi klarer ikke å lese teksten i PDF-en. Den kan være skannet. "
        "Lim inn teksten i stedet."
    )
    assert feiltekst(None, FeilType.FOR_STOR) == FOR_STORE


@pytest.mark.parametrize("testmodus", [True, False], ids=["testmodus", "uten_testmodus"])
@pytest.mark.parametrize("type", list(FILFEIL))
@pytest.mark.parametrize(
    ("modus", "navn"),
    [
        (Modus.FULL_GENERERING, "cv"),
        (Modus.FULL_GENERERING, "annonse"),
        (Modus.KORREKTUR, "cv"),
        (Modus.KORREKTUR, "eget_brev"),
        (Modus.KORREKTUR, "annonse"),
    ],
)
def test_fr10_fr11_fr12_filfeil_i_hvert_felt(
    app, innlogget_client, lest, modus, navn, type, testmodus
):
    """FR-10/FR-11/FR-12/UX-DR7/UX-DR8 (story 6.2): en fil med feil type, over 5 MB eller uten
    lesbar tekst i hvert felt, i begge modusene og med og uten testmodus, gir samme side på nytt
    (200, ingen redirect) med teksten i feilboksen (lenke til feltet) og under feltnavnet. Feltet
    er rødt og tomt («Last opp PDF» og «Lim inn tekst»), og knappene og tekstboksen er koblet
    til feilteksten med aria-describedby. Den avviste fila lagres ikke, og de andre feltene
    beholdes. En fil med feil type eller over 5 MB leses ikke med pypdf."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=modus))
    if not testmodus:
        uten_testmodus(app, innlogget_client)
    felt = {n: GYLDIG[n] for n in inndata.felt_for_modus(modus)}
    felt[navn] = FILFEIL[type]
    svar = send_felt(innlogget_client, **felt)
    assert svar.status_code == 200
    html = html_av(svar)
    tekst = feiltekst(navn, type)
    assert feilboks_lenker(html) == [(f"#{navn}-felt", tekst)]
    feltet = felt_html(html, navn)
    assert 'class="innleggingsfelt har-feil"' in feltet
    assert f'<p class="feiltekst" id="{navn}-feil">{tekst}</p>' in feltet
    assert '<div class="tom-tilstand">' in feltet
    assert '<div class="filboks" hidden>' in feltet
    for knapp in (f"{navn}-last-opp", f"{navn}-lim-inn"):
        assert element(html, knapp)["aria-describedby"] == f"{navn}-feil"
    assert element(html, f"{navn}-tekst")["aria-describedby"] == f"{navn}-feil {navn}-hjelp"
    soknad = soknaden(app, innlogget_client)
    assert getattr(soknad, navn) == Tekstfelt()
    for annet in felt.keys() - {navn}:
        assert getattr(soknad, annet) == Tekstfelt(GYLDIG[annet])
    assert soknad.steg == Steg.INNLEGGING
    assert lest == ([SKANNET] if type == FeilType.ULESELIG else [])


def test_fr10_omdopt_docx_gir_feil_filtype(paa_innlegging, lest):
    """FR-10 (story 6.2): en .docx som er omdøpt til cv.pdf, har ikke %PDF- i starten og gir
    feil_filtype. Den leses ikke med pypdf."""
    html = html_av(send_felt(paa_innlegging, cv=(FEIL_TYPE_DOCX, "cv.pdf"), annonse=ANNONSE))
    assert feilboks_lenker(html) == [("#cv-felt", feiltekst("cv", FeilType.FEIL_FILTYPE))]
    assert lest == []


def test_fr10_navnet_sjekkes_uansett_store_og_smaa_bokstaver(app, paa_innlegging):
    """FR-10 (story 6.2): CV.PDF godtas, og en PDF som heter noe annet enn .pdf, gir
    feil_filtype."""
    svar = send_felt(paa_innlegging, cv=(PDF_CV, "CV.PDF"), annonse=ANNONSE)
    assert svar.location == "/resultat"
    til_innlegging(app, paa_innlegging)
    html = html_av(send_felt(paa_innlegging, cv=(PDF_CV, "cv.txt"), annonse=ANNONSE))
    assert feilboks_lenker(html) == [("#cv-felt", feiltekst("cv", FeilType.FEIL_FILTYPE))]


def test_fr12_akkurat_5_mb_leses(paa_innlegging, lest):
    """FR-12 (story 6.2): en PDF på akkurat 5 MB leses og godtas."""
    akkurat = PDF_CV.ljust(MAKS_FILSTORRELSE, b" ")
    svar = send_felt(paa_innlegging, cv=(akkurat, "cv.pdf"), annonse=ANNONSE)
    assert svar.location == "/resultat"
    assert lest == [akkurat]


def test_fr11_odelagt_pdf_gir_uleselig_uten_krasj(paa_innlegging):
    """FR-11 (story 6.2): en fil som begynner med %PDF-, men er ødelagt, gir uleselig uten
    krasj."""
    svar = send_felt(paa_innlegging, cv=(b"%PDF-1.7\n\xff\xfe odelagt", "cv.pdf"), annonse=ANNONSE)
    assert svar.status_code == 200
    assert feilboks_lenker(html_av(svar)) == [("#cv-felt", feiltekst("cv", FeilType.ULESELIG))]


def test_fr10_fr9_flere_feil_samtidig_i_feltrekkefolgen(paa_innlegging):
    """FR-10/FR-9 (story 6.2): .docx i CV-feltet og tom annonse gir begge feilene samtidig, CV
    først."""
    html = html_av(send_felt(paa_innlegging, cv=FILFEIL[FeilType.FEIL_FILTYPE], annonse=""))
    assert feilboks_lenker(html) == [
        ("#cv-felt", feiltekst("cv", FeilType.FEIL_FILTYPE)),
        ("#annonse-felt", TOM_ANNONSE),
    ]


def test_fr10_fr11_fr12_tre_filfeil_samtidig_i_korrektur(paa_korrektur):
    """FR-10/FR-11/FR-12 (story 6.2): feil filtype, skannet PDF og for stor fil i hvert sitt
    felt i Korrektur gir tre feil samtidig, i rekkefølgen CV, brev, annonse."""
    svar = send_felt(
        paa_korrektur,
        cv=FILFEIL[FeilType.FEIL_FILTYPE],
        eget_brev=FILFEIL[FeilType.ULESELIG],
        annonse=FILFEIL[FeilType.FOR_STOR],
    )
    assert feilboks_lenker(html_av(svar)) == [
        ("#cv-felt", feiltekst("cv", FeilType.FEIL_FILTYPE)),
        ("#eget_brev-felt", feiltekst("eget_brev", FeilType.ULESELIG)),
        ("#annonse-felt", feiltekst("annonse", FeilType.FOR_STOR)),
    ]


def test_fr11_fr34_skannet_cv_i_testmodus_gir_bare_uleselig(paa_innlegging):
    """FR-11/FR-34 (story 6.2): i testmodus gir en skannet CV med testannonsen bare uleselig på
    CV-en, ikke ikke_testdata."""
    html = html_av(send_felt(paa_innlegging, cv=(SKANNET, "skannet.pdf"), annonse=ANNONSE))
    assert feilboks_lenker(html) == [("#cv-felt", feiltekst("cv", FeilType.ULESELIG))]


def test_fr11_felt_uten_feil_beholder_fila(app, paa_innlegging):
    """FR-11/FR-9 (story 6.2): en skannet CV og annonsen som PDF gir feilen på CV-en, og
    annonsen står igjen med filnavnet. Et nytt forsøk med CV-en som tekst og annonsen fra økten
    gir resultatsiden."""
    svar = send_felt(paa_innlegging, cv=(SKANNET, "skannet.pdf"), annonse=(PDF_ANNONSE, "a.pdf"))
    html = html_av(svar)
    assert feilboks_lenker(html) == [("#cv-felt", feiltekst("cv", FeilType.ULESELIG))]
    assert '<span class="filnavn" title="a.pdf">a.pdf</span>' in felt_html(html, "annonse")
    assert soknaden(app, paa_innlegging).annonse == Tekstfelt(les_pdf(PDF_ANNONSE), "a.pdf")
    assert send_felt(paa_innlegging, cv=CV, annonse=None).location == "/resultat"


def test_fr11_filfeil_erstatter_lagret_fil(app, paa_innlegging):
    """FR-11/FR-13 (story 6.2, bestemt av Kristine 16. november 2026): en ny fil med feil
    erstatter den lagrede PDF-en i feltet, så feltet er tomt etterpå, også ved «Tilbake»."""
    send_felt(paa_innlegging, cv=(PDF_CV, "cv.pdf"), annonse=ANNONSE, handling="tilbake")
    paa_innlegging.post("/modus", data={"modus": "full_generering"})
    svar = send_felt(
        paa_innlegging, cv=(SKANNET, "skannet.pdf"), annonse=ANNONSE, handling="tilbake"
    )
    assert svar.location == "/modus"
    assert soknaden(app, paa_innlegging).cv == Tekstfelt()


def test_fr11_lagret_fil_sjekkes_ikke_paa_nytt(paa_innlegging, monkeypatch):
    """FR-11 (story 6.2): bare en ny fil sjekkes. En fil som er lagret i økten fra før, har alt
    passert, så «Sjekk CV-en min» uten ny fil verken sjekker eller leser den igjen."""
    send_felt(paa_innlegging, cv=(PDF_CV, "cv.pdf"), annonse=ANNONSE, handling="tilbake")
    paa_innlegging.post("/modus", data={"modus": "full_generering"})

    def ikke_kall(*args):
        raise AssertionError("Den lagrede fila skal ikke sjekkes på nytt.")

    monkeypatch.setattr(ruter, "sjekk_fil", ikke_kall)
    monkeypatch.setattr(pdf_inn, "les_pdf", ikke_kall)
    assert send_felt(paa_innlegging, cv=None, annonse=ANNONSE).location == "/resultat"


def test_nfr4_avvist_fil_logges_ikke(paa_innlegging, caplog):
    """NFR-4 (story 6.2): verken navnet eller innholdet i en avvist fil står i loggen."""
    caplog.set_level("DEBUG")
    send_felt(paa_innlegging, cv=(FEIL_TYPE_DOCX, "hemmelig-cv.docx"), annonse=ANNONSE)
    send_felt(paa_innlegging, cv=(SKANNET, "hemmelig-skannet.pdf"), annonse=ANNONSE)
    assert "hemmelig" not in caplog.text


# --- Hele forespørselen over MAX_CONTENT_LENGTH (story 6.2, FR-12) ---

LITEN_GRENSE = 10_000


@pytest.fixture
def liten_app():
    """En app med MAX_CONTENT_LENGTH på 10 000 byte, så 413 kan prøves uten 16 MB i testen."""
    return create_app(
        {"TESTING": True, "SECRET_KEY": "test-nokkel", "MAX_CONTENT_LENGTH": LITEN_GRENSE}
    )


def test_fr12_for_stor_foresporsel_gir_innleggingen_med_feilboksen(liten_app):
    """FR-12 (story 6.2): er hele forespørselen over MAX_CONTENT_LENGTH, vises innleggingen med
    «Filene er for store. Hver fil kan være på høyst 5 MB.» i feilboksen, uten lenke og uten
    feltnavn, og status 413. Det som var lagret fra før, står igjen, og ingenting fra
    forespørselen lagres. Ingen feil står ved feltene."""
    client = liten_app.test_client()
    assert logg_inn(client).status_code == 302
    lagret = Soknad(
        steg=Steg.INNLEGGING,
        modus=Modus.FULL_GENERERING,
        cv=Tekstfelt("Lagret CV"),
        annonse=Tekstfelt("tekst", "annonse.pdf"),
    )
    sett_soknad(liten_app, client, lagret)
    svar = send_felt(client, cv=(b"%PDF-1.7" + b" " * LITEN_GRENSE, "stor.pdf"), annonse="Ny")
    assert svar.status_code == 413
    assert svar.headers["Cache-Control"] == "no-store"
    html = html_av(svar)
    boks = re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)
    assert tekster.FEILBOKS_OVERSKRIFT in boks
    assert f"<li>{FOR_STORE}</li>" in boks
    assert "<a " not in boks
    assert "har-feil" not in html
    assert 'class="feiltekst"' not in html
    assert tekstboks(html, "cv") == "Lagret CV"
    assert '<span class="filnavn" title="annonse.pdf">annonse.pdf</span>' in html
    assert soknaden(liten_app, client) == lagret


def test_fr12_skjemafeilen_star_foran_feltfeilene(app):
    """FR-12/UX-DR7 (story 6.2): en feil uten felt står i feilboksen uten lenke, foran feilene
    ved feltene."""
    with app.test_request_context():
        html = ruter._vis_innlegging(
            Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING),
            feil=[InndataFeil(None, FeilType.FOR_STOR), InndataFeil("cv", FeilType.TOM)],
        )
    boks = re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)
    assert boks.index(f"<li>{FOR_STORE}</li>") < boks.index('<a href="#cv-felt">')


def test_fr12_for_stor_foresporsel_paa_en_annen_side_gir_vanlig_413(liten_app):
    """FR-12 (story 6.2): på andre sider enn innleggingen (her innloggingen) gir en for stor
    forespørsel Werkzeugs vanlige 413-side, uten feilboksen."""
    svar = liten_app.test_client().post(
        "/logg-inn", data={"epost": "x" * LITEN_GRENSE, "passord": "p"}
    )
    assert svar.status_code == 413
    html = html_av(svar)
    assert "Request Entity Too Large" in html
    assert FOR_STORE not in html
