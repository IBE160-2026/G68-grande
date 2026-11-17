"""Tester for «Nytt forslag» på brevsiden og vinduet som spør først, også på resultatsiden når
et brev finnes (FR-25, FR-27, FR-28, FR-36, NFR-11, AD-1, AD-8, UX-DR17). Story 7.1. Testene
er i en egen fil, så test_brev.py ikke vokser (retro 5, A6). Selve vinduet åpnes i nettleseren
(bekreft.js), så her testes at vinduet, knappene, skriptet og CSS-en er på plass, og at
POST-en lager neste forslag."""

import json
import re

import pytest

from soknad.innstillinger import MAKS_KI_KALL
from soknad.kjerne.feil import KIFeilType
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from tests.web.hjelpere import (
    ANNONSE,
    CASE,
    CV,
    EGET_BREV,
    GAP_SVAR,
    NEDLASTING,
    NOKKELORD_SVAR,
    STIL,
    FeilendeKI,
    brevtekst,
    css_blokk,
    element,
    html_av,
    korrektur_brev,
    korrektur_svar,
    main,
    med_autofocus,
    sett_soknad,
    soknaden,
    tagger_i,
)

# Fiksturene paa_brev, paa_brev_korrektur, korrektur_ki og med_nokkel står i conftest.py.

BREV_1 = json.loads((CASE / "ki-svar" / "brev-1.json").read_text(encoding="utf-8"))
BREV_2 = json.loads((CASE / "ki-svar" / "brev-2.json").read_text(encoding="utf-8"))
MALER = STIL.parents[2] / "templates"
SKRIPT = STIL.parents[1] / "js" / "bekreft.js"
NYTT_FORSLAG = {"handling": "nytt_forslag"}


def nytt_forslag(client, data=None):
    """«Ja, lag nytt forslag»: POST til /brev med handling=nytt_forslag."""
    return client.post("/brev", data=NYTT_FORSLAG if data is None else data)


def vinduet(html):
    """HTML-en til vinduet «Vil du ha et nytt forslag?», fra <dialog> til </dialog>."""
    return re.search(r'<dialog [^>]*id="vindu-nytt-forslag".*?</dialog>', html, re.S).group(0)


def feilboks(html):
    return re.search(r'<div class="feilboks"[^>]*>(.*?)</div>', html, re.S).group(1)


def brevet(avsnitt, navn):
    """Brevet slik det står på siden: avsnittene, hilsenen og navnet."""
    return [*avsnitt, "Med vennlig hilsen", *([navn] if navn else [])]


def paa_brev_med_ekte_ki(app, client, ki_kall=0):
    """Søknaden på brevsiden med case 1, samtykke og ki_kall brukt, for testene med ekte KI."""
    soknad = Soknad(
        steg=Steg.BREV,
        modus=Modus.FULL_GENERERING,
        samtykke=True,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        nokkelord=tuple(NOKKELORD_SVAR["nokkelord"]),
        gap=GAP_SVAR,
        brev=BREV_1,
        ki_kall=ki_kall,
    )
    sett_soknad(app, client, soknad)
    return soknad


class OpptakerKI:
    """Samme svar som TestKI, men hvert kall skrives i kalt med oppgaven og argumentene."""

    def __init__(self, test_ki):
        self.test_ki = test_ki
        self.caser = test_ki.caser
        self.kalt = []

    def brev(self, cv, annonse, forslag):
        self.kalt.append(("brev", cv, annonse, forslag))
        return self.test_ki.brev(cv, annonse, forslag)

    def korrektur(self, cv, annonse, eget_brev, forslag):
        self.kalt.append(("korrektur", cv, annonse, eget_brev, forslag))
        return self.test_ki.korrektur(cv, annonse, eget_brev, forslag)


# --- Brevsiden: knappen og vinduet ---


def test_fr25_nytt_forslag_staar_under_nedlastingen(paa_brev):
    """FR-25/UX-DR16: «Nytt forslag» står under nedlastingsknappene, som en lenkeknapp i et
    skjema som sender POST til /brev. Knappen sender handling=nytt_forslag, viser ventetegnet
    med brevteksten og åpner vinduet først (data-bekreft)."""
    html = html_av(paa_brev.get("/brev"))
    innhold = main(html)
    assert innhold.index('id="last-ned-docx"') < innhold.index('id="nytt-forslag-skjema"')
    assert innhold.index('id="filnavn-docx"') < innhold.index('id="nytt-forslag-skjema"')
    assert element(html, "nytt-forslag-skjema") == {
        "class": "nytt-forslag",
        "method": "post",
        "action": "/brev",
        "id": "nytt-forslag-skjema",
    }
    assert element(html, "nytt-forslag") == {
        "class": "lenkeknapp",
        "id": "nytt-forslag",
        "type": "submit",
        "name": "handling",
        "value": "nytt_forslag",
        "data-vente": tekster.VENTE_BREV,
        "data-bekreft": "vindu-nytt-forslag",
    }
    knapp = re.search(r'<button [^>]*id="nytt-forslag"[^>]*>(.*?)</button>', html, re.S)
    assert knapp.group(1) == tekster.NYTT_FORSLAG_KNAPP


def test_fr25_vinduet_er_lukket_og_har_tekstene_og_aria(paa_brev):
    """FR-25/UX-DR17: vinduet står etter <main>, er lukket når siden lastes, og har
    overskriften og teksten fra EXPERIENCE. aria-labelledby peker på overskriften og
    aria-describedby på teksten. Sidens autofocus står på overskriften."""
    html = html_av(paa_brev.get("/brev"))
    assert "<dialog" not in main(html)
    assert html.index("</main>") < html.index('id="vindu-nytt-forslag"')
    attr = element(html, "vindu-nytt-forslag")
    assert attr == {
        "class": "vindu",
        "id": "vindu-nytt-forslag",
        "aria-labelledby": "vindu-nytt-forslag-overskrift",
        "aria-describedby": "vindu-nytt-forslag-tekst",
    }
    boks = vinduet(html)
    overskrift = tekster.VINDU_NYTT_FORSLAG_OVERSKRIFT
    assert f'<h2 id="vindu-nytt-forslag-overskrift">{overskrift}</h2>' in boks
    assert f'<p id="vindu-nytt-forslag-tekst">{tekster.VINDU_NYTT_FORSLAG_TEKST}</p>' in boks
    assert boks.index('vindu-nytt-forslag-tekst">') < boks.index("vindu-knapper")
    assert re.search(r"<dialog[^>]*\bopen\b", html) is None
    assert med_autofocus(html) == [None, "nytt-forslag-avbryt"]


def test_fr25_knappene_i_vinduet(paa_brev):
    """FR-25/UX-DR17: «Ja, lag nytt forslag» er en hovedknapp med type="button" (skriptet
    sender skjemaet), og «Avbryt» er en sekundærknapp i et skjema med method="dialog", som
    lukker vinduet. «Avbryt» har autofocus, så fokus går til det trygge valget når vinduet
    åpnes. Ingen andre knapper eller lenker."""
    boks = vinduet(html_av(paa_brev.get("/brev")))
    tagger = tagger_i(boks)
    knapper = [a for t, a in tagger if t == "button"]
    assert knapper == [
        {"class": "hovedknapp", "type": "button", "data-bekreft-ja": None},
        {"class": "sekundaerknapp", "id": "nytt-forslag-avbryt", "autofocus": None},
    ]
    assert [a for t, a in tagger if t == "form"] == [{"method": "dialog"}]
    assert [t for t, _ in tagger if t == "a"] == []
    assert re.search(
        rf"<button [^>]*data-bekreft-ja>{tekster.JA_NYTT_FORSLAG_KNAPP}</button>", boks
    )
    assert re.search(
        rf'<button [^>]*id="nytt-forslag-avbryt"[^>]*>{tekster.AVBRYT_KNAPP}</button>', boks
    )
    assert boks.index("data-bekreft-ja") < boks.index('id="nytt-forslag-avbryt"')


def test_fr25_brevsiden_har_ventetegnet_og_skriptene(paa_brev):
    """FR-25/FR-27/AD-1: brevsiden laster bekreft.js og vente.js og har ventetegnet utenfor
    <main>, lukket."""
    html = html_av(paa_brev.get("/brev"))
    assert '<script src="/static/js/bekreft.js" defer></script>' in html
    assert '<script src="/static/js/vente.js" defer></script>' in html
    assert "hidden" in element(html, "ventetegn")
    assert element(html, "vente-status")["role"] == "status"
    assert 'id="vente"' not in main(html)


@pytest.mark.parametrize("modus", list(Modus))
def test_fr25_knappen_og_vinduet_i_begge_modusene(app, request, modus):
    """FR-25: «Nytt forslag» og vinduet står på brevsiden både i Full generering og i
    Korrektur."""
    if modus == Modus.KORREKTUR:
        client = request.getfixturevalue("paa_brev_korrektur")
    else:
        client = request.getfixturevalue("paa_brev")
    html = html_av(client.get("/brev"))
    assert element(html, "nytt-forslag")["data-bekreft"] == "vindu-nytt-forslag"
    assert 'id="vindu-nytt-forslag"' in html


# --- Nytt forslag ---


def test_fr25_nytt_forslag_gir_neste_brev_og_nullstiller_nedlastingen(app, paa_brev):
    """FR-25/FR-29/AD-8: etter nedlasting gir «Ja, lag nytt forslag» brevsiden med forslag 2
    (brev-2.json). lastet_ned er usann, så «Last ned som Word» er blå igjen og filnavn-linjen
    er skjult. Steget er fortsatt brev."""
    assert paa_brev.get(NEDLASTING).status_code == 200
    assert soknaden(app, paa_brev).lastet_ned is True
    svar = nytt_forslag(paa_brev)
    assert svar.status_code == 302
    assert svar.location == "/brev"
    soknad = soknaden(app, paa_brev)
    assert soknad.forslag == 2
    assert soknad.brev == BREV_2
    assert soknad.lastet_ned is False
    assert soknad.steg == Steg.BREV
    assert soknad.opptatt is False
    html = html_av(paa_brev.get("/brev"))
    assert brevtekst(html) == brevet(BREV_2["avsnitt"], BREV_2["navn"])
    assert element(html, "last-ned-docx")["class"].split() == ["hovedknapp"]
    assert "hidden" in element(html, "filnavn-docx")
    assert med_autofocus(html) == [None, "nytt-forslag-avbryt"]
    assert "feilboks" not in main(html)


def test_fr25_forslag_1_og_2_gir_ulike_brev_og_3_gir_det_forste_igjen(app, paa_brev):
    """FR-25: i testmodus gir forslag 1 og 2 ulike brev, og forslag 3 gir brev-1.json igjen
    (oddetall og partall)."""
    assert BREV_1 != BREV_2
    assert soknaden(app, paa_brev).brev == BREV_1
    nytt_forslag(paa_brev)
    assert soknaden(app, paa_brev).brev == BREV_2
    nytt_forslag(paa_brev)
    soknad = soknaden(app, paa_brev)
    assert soknad.forslag == 3
    assert soknad.brev == BREV_1


def test_fr25_ki_en_faar_cv_annonse_og_neste_forslag(app, paa_brev):
    """FR-25/FR-37: KI-en kalles én gang med CV-en og annonsen fra søknaden og forslag 2."""
    opptaker = OpptakerKI(app.extensions["test_ki"])
    app.extensions["test_ki"] = opptaker
    assert nytt_forslag(paa_brev).location == "/brev"
    assert opptaker.kalt == [("brev", CV, ANNONSE, 2)]


def test_fr25_korrektur_lager_neste_forslag_fra_det_opprinnelige_brevet(
    app, paa_brev_korrektur, korrektur_ki
):
    """FR-25/FR-23: i Korrektur får KI-en det opprinnelige egne brevet (ikke det forbedrede)
    og forslag 2. Brevsiden viser korrektur-2, og det egne brevet i søknaden er uendret."""
    opptaker = OpptakerKI(korrektur_ki)
    app.extensions["test_ki"] = opptaker
    paa_brev_korrektur.get(NEDLASTING)
    assert nytt_forslag(paa_brev_korrektur).location == "/brev"
    assert opptaker.kalt == [("korrektur", CV, ANNONSE, EGET_BREV, 2)]
    soknad = soknaden(app, paa_brev_korrektur)
    assert soknad.forslag == 2
    assert soknad.korrektur == korrektur_svar(2)
    assert soknad.eget_brev.tekst == EGET_BREV
    assert soknad.lastet_ned is False
    html = html_av(paa_brev_korrektur.get("/brev"))
    assert brevtekst(html) == korrektur_brev(2)
    # Forslag 3 lages også fra det opprinnelige brevet.
    nytt_forslag(paa_brev_korrektur)
    assert opptaker.kalt[-1] == ("korrektur", CV, ANNONSE, EGET_BREV, 3)
    assert soknaden(app, paa_brev_korrektur).korrektur == korrektur_svar(1)


def test_fr25_ny_modus_gir_forslag_1_igjen(app, paa_brev):
    """FR-25/AD-8: velges modus på nytt etter et nytt forslag, er brevet borte, og forslag er
    1, så det første brevet etterpå er brev-1.json."""
    nytt_forslag(paa_brev)
    assert paa_brev.post("/modus", data={"modus": "full_generering"}).location == "/innlegging"
    soknad = soknaden(app, paa_brev)
    assert soknad.forslag == 1
    assert soknad.brev is None
    data = {"cv": CV, "annonse": ANNONSE, "handling": "sjekk"}
    assert paa_brev.post("/innlegging", data=data).location == "/resultat"
    assert paa_brev.post("/resultat", data={"handling": "brev"}).location == "/brev"
    soknad = soknaden(app, paa_brev)
    assert soknad.forslag == 1
    assert soknad.brev == BREV_1


# --- KI-feil og grensen ---


@pytest.mark.parametrize("feiltype", list(KIFeilType))
def test_fr28_ki_feil_beholder_det_gamle_brevet(app, paa_brev, feiltype):
    """FR-25/FR-28/AD-8: feiler KI-en, vises brevsiden med det gamle brevet, uten redirect.
    forslag, brevet og lastet_ned er uendret. Feilboksen har feilteksten, «Brevet du hadde, er
    beholdt.» og «Prøv på nytt», og den har fokus."""
    paa_brev.get(NEDLASTING)
    for_ = soknaden(app, paa_brev)
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], "brev", feiltype)
    svar = nytt_forslag(paa_brev)
    assert svar.status_code == 200
    html = html_av(svar)
    assert soknaden(app, paa_brev) == for_
    assert for_.forslag == 1
    assert for_.lastet_ned is True
    assert brevtekst(html) == brevet(BREV_1["avsnitt"], BREV_1["navn"])
    boks = feilboks(html)
    assert f'<p class="feilboks-overskrift">{tekster.KI_FEILTEKSTER[feiltype]}</p>' in boks
    assert f'<p class="feilboks-tekst">{tekster.KI_FEIL_BEHOLDT_BREV}</p>' in boks
    assert tekster.PROV_PA_NYTT_KNAPP in boks
    # Ingen nedlastingslenke, så nedlasting.js skjuler ikke KI-feilboksen.
    assert not [a for t, a in tagger_i(boks) if t == "a" and "data-nedlasting" in a]
    assert med_autofocus(html) == ["feilboks", "nytt-forslag-avbryt"]
    # Knappen er fortsatt grønn, for det gamle brevet er lastet ned.
    assert "ferdig" in element(html, "last-ned-docx")["class"].split()


def test_fr28_prov_paa_nytt_sender_nytt_forslag_uten_aa_sporre(app, paa_brev):
    """FR-25/FR-27/FR-28: «Prøv på nytt» står utenfor skjemaet, men sender det med form= og
    handling=nytt_forslag, med ventetegnet. Den spør ikke på nytt (ingen data-bekreft).
    Virker KI-en igjen, gir den forslag 2."""
    ekte = app.extensions["test_ki"]
    app.extensions["test_ki"] = FeilendeKI(ekte, oppgave="brev")
    html = html_av(nytt_forslag(paa_brev))
    knapp = next(a for t, a in tagger_i(feilboks(html)) if t == "button")
    assert knapp == {
        "class": "hovedknapp",
        "type": "submit",
        "form": "nytt-forslag-skjema",
        "name": "handling",
        "value": "nytt_forslag",
        "data-vente": tekster.VENTE_BREV,
    }
    app.extensions["test_ki"] = ekte
    svar = paa_brev.post("/brev", data={knapp["name"]: knapp["value"]})
    assert svar.location == "/brev"
    soknad = soknaden(app, paa_brev)
    assert soknad.forslag == 2
    assert soknad.brev == BREV_2


def test_fr28_ki_feil_i_korrektur_beholder_det_forbedrede_brevet(
    app, paa_brev_korrektur, korrektur_ki
):
    """FR-25/FR-28: feiler KI-en i Korrektur, står det forbedrede brevet (forslag 1) igjen."""
    for_ = soknaden(app, paa_brev_korrektur)
    app.extensions["test_ki"] = FeilendeKI(korrektur_ki, oppgave="korrektur")
    html = html_av(nytt_forslag(paa_brev_korrektur))
    assert soknaden(app, paa_brev_korrektur) == for_
    assert brevtekst(html) == korrektur_brev(1)
    assert tekster.KI_FEIL_BEHOLDT_BREV in feilboks(html)


def test_nfr11_nytt_forslag_med_ekte_ki_telles(med_nokkel):
    """NFR-11/FR-25: med ekte KI og samtykke kaller «Nytt forslag» brev én gang, og kallet
    telles."""
    app, client, kalt = med_nokkel
    paa_brev_med_ekte_ki(app, client, ki_kall=3)
    assert nytt_forslag(client).location == "/brev"
    assert kalt == ["brev"]
    soknad = soknaden(app, client)
    assert soknad.ki_kall == 4
    assert soknad.forslag == 2


def test_nfr11_ki_feil_med_ekte_ki_telles_ogsaa(med_nokkel):
    """NFR-11/FR-28: et kall som feiler, telles også, men det gamle brevet og forslag står
    igjen."""
    app, client, _ = med_nokkel
    for_ = paa_brev_med_ekte_ki(app, client, ki_kall=3)
    app.extensions["ekte_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave="brev")
    assert nytt_forslag(client).status_code == 200
    soknad = soknaden(app, client)
    assert soknad == Soknad(**{**for_.__dict__, "ki_kall": 4})


def test_nfr11_alle_kall_brukt_gir_feilboksen_uten_prov_paa_nytt(med_nokkel):
    """NFR-11: med ekte KI og alle KI-kallene brukt kalles ikke KI-en. Brevsiden viser
    feilboksen med meldingen om det og «Brevet du hadde, er beholdt.», uten «Prøv på nytt»,
    og søknaden er uendret."""
    app, client, kalt = med_nokkel
    for_ = paa_brev_med_ekte_ki(app, client, ki_kall=MAKS_KI_KALL)
    svar = nytt_forslag(client)
    assert svar.status_code == 200
    html = html_av(svar)
    assert kalt == []
    assert soknaden(app, client) == for_
    boks = feilboks(html)
    assert f'<p class="feilboks-overskrift">{tekster.KI_KALL_BRUKT}</p>' in boks
    assert tekster.KI_FEIL_BEHOLDT_BREV in boks
    assert tekster.PROV_PA_NYTT_KNAPP not in boks
    assert "<button" not in boks
    assert brevtekst(html) == brevet(BREV_1["avsnitt"], BREV_1["navn"])


def test_fr36_nytt_forslag_uten_samtykke_gir_startsiden(med_nokkel):
    """FR-36/AD-12: testmodus av og samtykket mangler: KI-en kalles ikke, og brukeren sendes
    til startsiden."""
    app, client, kalt = med_nokkel
    soknad = paa_brev_med_ekte_ki(app, client)
    soknad = Soknad(**{**soknad.__dict__, "samtykke": False})
    sett_soknad(app, client, soknad)
    assert nytt_forslag(client).location == "/"
    assert kalt == []
    assert soknaden(app, client) == soknad


# --- Opptatt, ukjent knapp og uten brev ---


def test_fr27_nytt_forslag_mens_opptatt_sender_til_steget(app, paa_brev):
    """FR-27/AD-8: mens søknaden er opptatt, sendes POST til siden for steget, uten KI-kall,
    og søknaden er uendret."""
    soknad = Soknad(**{**soknaden(app, paa_brev).__dict__, "opptatt": True})
    sett_soknad(app, paa_brev, soknad)
    opptaker = OpptakerKI(app.extensions["test_ki"])
    app.extensions["test_ki"] = opptaker
    svar = nytt_forslag(paa_brev)
    assert svar.status_code == 302
    assert svar.location == "/brev"
    assert opptaker.kalt == []
    assert soknaden(app, paa_brev) == soknad


@pytest.mark.parametrize("data", [{}, {"handling": "brev"}, {"handling": "noe-annet"}])
def test_fr25_ukjent_knapp_gir_400_og_uendret_soknad(app, paa_brev, data):
    """FR-25/AD-8: en POST uten handling=nytt_forslag gir brevsiden med 400, uten KI-kall, og
    søknaden er uendret."""
    for_ = soknaden(app, paa_brev)
    svar = nytt_forslag(paa_brev, data)
    assert svar.status_code == 400
    assert brevtekst(html_av(svar)) == brevet(BREV_1["avsnitt"], BREV_1["navn"])
    assert soknaden(app, paa_brev) == for_


def test_fr25_uten_brev_sendes_til_resultatsiden(app, paa_brev):
    """FR-25/AD-8: finnes det ikke noe brev, sendes POST til resultatsiden, uten KI-kall."""
    soknad = Soknad(**{**soknaden(app, paa_brev).__dict__, "brev": None})
    sett_soknad(app, paa_brev, soknad)
    svar = nytt_forslag(paa_brev)
    assert svar.status_code == 302
    assert svar.location == "/resultat"
    assert soknaden(app, paa_brev) == soknad


def test_fr25_for_tidlig_sendes_til_steget(app, paa_resultat):
    """AD-8: på steg resultat slipper /brev ikke inn, heller ikke ved POST."""
    svar = nytt_forslag(paa_resultat)
    assert svar.location == "/resultat"
    assert soknaden(app, paa_resultat).brev is None


# --- Resultatsiden ---


def test_fr25_resultatsiden_uten_brev_spor_ikke(paa_resultat):
    """FR-21/FR-25: uten brev sender «Lag søknadsbrevet mitt» skjemaet med en gang. Siden har
    ikke vinduet og ikke bekreft.js."""
    html = html_av(paa_resultat.get("/resultat"))
    knapp = next(a for t, a in tagger_i(html) if t == "button" and a.get("value") == "brev")
    assert "data-bekreft" not in knapp
    assert "vindu-nytt-forslag" not in html
    assert "js/bekreft.js" not in html


@pytest.mark.parametrize("modus", list(Modus))
def test_fr25_resultatsiden_med_brev_spor_forst(app, request, modus):
    """FR-25 (retro 3): med et brev (nettleserens tilbakeknapp fra brevsiden) åpner knappen
    videre vinduet «Vil du ha et nytt forslag?» først, i begge modusene. Siden har vinduet
    etter <main> og bekreft.js."""
    if modus == Modus.KORREKTUR:
        client = request.getfixturevalue("paa_brev_korrektur")
    else:
        client = request.getfixturevalue("paa_brev")
    html = html_av(client.get("/resultat"))
    knapp = next(a for t, a in tagger_i(html) if t == "button" and a.get("value") == "brev")
    assert knapp["data-bekreft"] == "vindu-nytt-forslag"
    assert knapp["data-vente"] == tekster.VENTE_BREV
    assert "<dialog" not in main(html)
    assert html.index("</main>") < html.index('id="vindu-nytt-forslag"')
    assert tekster.VINDU_NYTT_FORSLAG_OVERSKRIFT in vinduet(html)
    assert '<script src="/static/js/bekreft.js" defer></script>' in html
    assert med_autofocus(html) == [None, "nytt-forslag-avbryt"]


def test_fr25_ja_paa_resultatsiden_gir_neste_forslag(app, paa_brev):
    """FR-25 (retro 3): «Ja» på resultatsiden sender skjemaet, og brevet er neste forslag.
    lastet_ned er usann."""
    paa_brev.get(NEDLASTING)
    assert paa_brev.post("/resultat", data={"handling": "brev"}).location == "/brev"
    soknad = soknaden(app, paa_brev)
    assert soknad.forslag == 2
    assert soknad.brev == BREV_2
    assert soknad.lastet_ned is False


def test_fr28_ki_feil_paa_resultatsiden_beholder_brevet(app, paa_brev):
    """FR-25/FR-28: feiler KI-en etter «Ja» på resultatsiden, er det gamle brevet og forslag
    uendret. «Prøv på nytt» spør ikke, men knappen videre gjør det fortsatt."""
    for_ = soknaden(app, paa_brev)
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave="brev")
    html = html_av(paa_brev.post("/resultat", data={"handling": "brev"}))
    assert soknaden(app, paa_brev) == for_
    prov = next(a for t, a in tagger_i(html) if t == "button" and a.get("form"))
    assert "data-bekreft" not in prov
    videre = [
        a
        for t, a in tagger_i(html)
        if t == "button" and a.get("value") == "brev" and "form" not in a
    ]
    assert videre[0]["data-bekreft"] == "vindu-nytt-forslag"


# --- Tekstene, skriptet og CSS-en ---


def test_fr25_tekstene_ligger_i_tekster_py():
    """FR-25: tekstene står ordrett fra EXPERIENCE i tekster.py, og ikke i malene."""
    assert tekster.NYTT_FORSLAG_KNAPP == "Nytt forslag"
    assert tekster.VINDU_NYTT_FORSLAG_OVERSKRIFT == "Vil du ha et nytt forslag?"
    assert tekster.VINDU_NYTT_FORSLAG_TEKST == (
        "Brevet du ser nå, blir slettet. Har du ikke lastet det ned, er det borte."
    )
    assert tekster.JA_NYTT_FORSLAG_KNAPP == "Ja, lag nytt forslag"
    assert tekster.AVBRYT_KNAPP == "Avbryt"
    assert tekster.KI_FEIL_BEHOLDT_BREV == "Brevet du hadde, er beholdt."
    assert tekster.VENTE_BREV == "Vi lager brevet ditt – det kan ta en liten stund."
    for mal in ("brev.html", "resultat.html", "vindu_nytt_forslag.html"):
        innhold = re.sub(r"\{#.*?#\}", "", (MALER / mal).read_text(encoding="utf-8"), flags=re.S)
        for tekst in ("Nytt forslag", "Vil du ha", "blir slettet", "Ja, lag", "Avbryt", "beholdt"):
            assert tekst not in innhold, (mal, tekst)
        assert "style=" not in innhold


def test_fr25_skriptet_spor_for_skjemaet_sendes():
    """FR-25/UX-DR17/AD-1: bekreft.js stopper trykket på en knapp med data-bekreft og åpner
    vinduet med showModal() med fokus på «Avbryt» (autofocus). «Ja» lukker vinduet og sender
    skjemaet med knappen (requestSubmit), så vente.js viser ventetegnet. Når vinduet lukkes,
    får knappen fokus tilbake. Skriptet henter ingenting og lagrer ingenting."""
    skript = SKRIPT.read_text(encoding="utf-8")
    assert 'closest("[data-bekreft]")' in skript
    assert 'getAttribute("data-bekreft")' in skript
    assert "hendelse.preventDefault()" in skript
    assert ".showModal()" in skript
    assert '"[autofocus]"' in skript
    assert 'closest("[data-bekreft-ja]")' in skript
    assert "apentVindu.close()" in skript
    assert "sender.form.requestSubmit(sender)" in skript
    assert skript.count('addEventListener("close"') == 1
    assert "apner.focus()" in skript
    assert 'aria-disabled") === "true"' in skript
    for forbudt in ("fetch", "XMLHttpRequest", "localStorage", "sessionStorage", ".submit()"):
        assert forbudt not in skript, forbudt


def test_fr25_css_for_knappen_og_vinduet():
    """FR-25/NFR-7/UX-DR17: «Nytt forslag» står i midten under nedlastingen. «Avbryt» og
    knappen som åpnet vinduet viser fokusringen også etter et museklikk (:focus, som «Bli
    her»). I høykontrastmodus har vinduet ramme (samme .vindu som vinduet etter nedlasting).
    Ingen fast høyde og ingen nowrap."""
    css = STIL.read_text(encoding="utf-8")
    knapp = css_blokk(css, ".nytt-forslag")
    assert "justify-content: center;" in knapp
    fokus = css_blokk(css, "#nytt-forslag-avbryt:focus,\n[data-bekreft]:focus")
    assert "outline: 3px solid var(--focus-ring);" in fokus
    hoykontrast = re.search(r"@media \(forced-colors: active\) \{(.*?)\n\}", css, re.S).group(1)
    vindu = re.search(r"^\s*\.vindu\s*\{(.*?)\}", hoykontrast, re.S | re.M).group(1)
    assert "border: 1px solid CanvasText;" in vindu
    for blokk in (knapp, fokus, css_blokk(css, ".nedlasting")):
        assert "height" not in blokk
        assert "nowrap" not in blokk
