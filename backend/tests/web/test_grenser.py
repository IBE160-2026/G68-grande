"""Tester for grensene for tegn og KI-kall (NFR-11, FR-28, story 4.3.2). Ingen test kaller det
ekte API-et: EkteKI byttes ut med en falsk KI før noe kalles."""

import json
import re

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.innstillinger import MAKS_KI_KALL, MAKS_TEGN, MAKS_TEGN_EGET_BREV
from soknad.kjerne.feil import FeilType, KIFeilType
from soknad.kjerne.inndata import antall_tegn
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt, ferdig_brev
from soknad.kjerne.steg import Steg
from soknad.kjerne.testdata_match import vask
from soknad.web import tekster
from tests.web.hjelpere import (
    ANNONSE,
    CASE,
    CV,
    EGET_BREV,
    GAP_SVAR,
    NOKKELORD_SVAR,
    WEB,
    FeilendeKI,
    TellendeKI,
    brevtekst,
    element,
    html_av,
    korrektur_svar,
    med_autofocus,
    sett_soknad,
    soknaden,
)

FOR_LANG_CV = "CV: Teksten er for lang. Den kan være på høyst 15 000 tegn."
FOR_LANG_ANNONSE = "Stillingsannonse: Teksten er for lang. Den kan være på høyst 15 000 tegn."
KI_KALL_BRUKT = (
    "Du har brukt alle KI-kallene for denne søknaden. Begynn på en ny søknad fra startsiden."
)
# Lenken i feilboksen når alle KI-kallene er brukt, på innleggingen og resultatsiden (NFR-11).
LENKE_NY_SOKNAD = '<a class="hovedknapp" href="/">Lag ny søknad</a>'
# Meldingen og lenken i stedet når søknaden har et brev (retro 8, A1 og A6, bestemt av
# Kristine 22. november 2026).
KI_KALL_BRUKT_BREV = (
    "Du har brukt alle KI-kallene for denne søknaden. Last ned brevet, så kan du lage en ny "
    "søknad i vinduet etter nedlastingen."
)
LENKE_TIL_BREVET = '<a class="hovedknapp" href="/brev">Gå til brevet</a>'
BREV_1 = json.loads((CASE / "ki-svar" / "brev-1.json").read_text(encoding="utf-8"))


class FasteSvarKI(TellendeKI):
    """TellendeKI som svarer med de ferdige svarene fra case 1 uansett tekst, så en CV som
    ikke er testdata (for eksempel 15 000 tegn) også gir en analyse."""

    def nokkelord(self, annonse):
        self.kalt.append("nokkelord")
        return NOKKELORD_SVAR

    def gap(self, cv, annonse):
        self.kalt.append("gap")
        return GAP_SVAR


def legg_paa_innlegging(app, client, ki_kall=0):
    """Legger en søknad på innleggingen med samtykke og ki_kall brukt."""
    soknad = Soknad(
        steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, samtykke=True, ki_kall=ki_kall
    )
    sett_soknad(app, client, soknad)
    return soknad


def legg_paa_resultat(app, client, ki_kall=0):
    """Legger en søknad på resultatsiden med analysen fra case 1, samtykke og ki_kall brukt."""
    soknad = Soknad(
        steg=Steg.RESULTAT,
        modus=Modus.FULL_GENERERING,
        samtykke=True,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        nokkelord=tuple(NOKKELORD_SVAR["nokkelord"]),
        gap=GAP_SVAR,
        ki_kall=ki_kall,
    )
    sett_soknad(app, client, soknad)
    return soknad


def sjekk(client, cv=CV, annonse=ANNONSE):
    """«Sjekk CV-en min» på innleggingen."""
    return client.post("/innlegging", data={"cv": cv, "annonse": annonse, "handling": "sjekk"})


def feilboks(html):
    """Det som står i feilboksen øverst, eller None."""
    treff = re.search(r'<div class="feilboks" id="feilboks"[^>]*>(.*?)</div>', html, re.S)
    return treff.group(1) if treff else None


# --- Tekstene ---


def test_nfr11_feiltekstene_og_meldingen_ligger_i_tekster_py():
    """NFR-11: feiltekstene og meldingen er ordrett som Kristine bestemte 14. november, med
    tallet fra MAKS_TEGN."""
    assert tekster.FEILTEKSTER[("cv", FeilType.FOR_LANG)] == FOR_LANG_CV
    assert tekster.FEILTEKSTER[("annonse", FeilType.FOR_LANG)] == FOR_LANG_ANNONSE
    assert tekster.MAKS_TEGN_TEKST == "15 000"
    assert tekster.KI_KALL_BRUKT == KI_KALL_BRUKT
    assert tekster.KI_KALL_BRUKT_BREV == KI_KALL_BRUKT_BREV
    assert tekster.GA_TIL_BREVET_KNAPP == "Gå til brevet"
    for mal in ("innlegging.html", "resultat.html", "brev.html"):
        innhold = (WEB / "templates" / mal).read_text(encoding="utf-8")
        assert "Teksten er for lang" not in innhold
        assert "Du har brukt alle" not in innhold
        assert "Gå til brevet" not in innhold


def test_nfr11_tekstboksene_har_ikke_maxlength():
    """NFR-11: tekstboksene har ikke maxlength, for da kuttes en lang tekst uten melding."""
    innhold = (WEB / "templates" / "innlegging.html").read_text(encoding="utf-8")
    assert "maxlength" not in innhold


def test_nfr11_testdataene_er_under_tegngrensen():
    """NFR-11: ingen av CV-ene og annonsene i testdataene er over MAKS_TEGN, så flyten i
    testmodus virker som før."""
    filer = sorted(TESTDATA_MAPPE.glob("case-*/*.txt"))
    assert filer
    for fil in filer:
        assert antall_tegn(fil.read_text(encoding="utf-8")) <= MAKS_TEGN, fil
    brevene = sorted(TESTDATA_MAPPE.glob("case-*/eget-brev.txt"))
    assert brevene
    for fil in brevene:
        assert antall_tegn(fil.read_text(encoding="utf-8")) <= MAKS_TEGN_EGET_BREV, fil


# --- Tegngrensen ---


def test_nfr11_akkurat_15000_tegn_godtas(med_nokkel):
    """NFR-11: en CV på akkurat 15 000 tegn godtas, og analysen hentes."""
    app, client, _ = med_nokkel
    kalt = []
    app.extensions["ekte_ki"] = FasteSvarKI(app.extensions["test_ki"], kalt=kalt)
    legg_paa_innlegging(app, client)
    svar = sjekk(client, cv="a" * MAKS_TEGN)
    assert svar.location == "/resultat"
    assert kalt == ["nokkelord", "gap"]


def test_nfr11_linjeskift_som_crlf_telles_som_ett_tegn(med_nokkel):
    """NFR-11: 15 000 tegn der linjeskiftene sendes som \\r\\n, godtas."""
    app, client, _ = med_nokkel
    kalt = []
    app.extensions["ekte_ki"] = FasteSvarKI(app.extensions["test_ki"], kalt=kalt)
    legg_paa_innlegging(app, client)
    cv = ("a" * 99 + "\r\n") * (MAKS_TEGN // 100)
    assert len(cv) > MAKS_TEGN
    svar = sjekk(client, cv=cv)
    assert svar.location == "/resultat"
    assert kalt == ["nokkelord", "gap"]


def test_nfr11_for_lang_cv_og_tom_annonse_gir_begge_feilene(med_nokkel):
    """NFR-11/FR-9: en CV på 15 001 tegn og tom annonse gir feilboksen med begge feilene,
    for lang ved CV-en (aria-invalid og feilteksten), ingen KI-kall, og teksten står igjen."""
    app, client, kalt = med_nokkel
    legg_paa_innlegging(app, client)
    cv = "a" * (MAKS_TEGN + 1)
    svar = sjekk(client, cv=cv, annonse="")
    assert svar.status_code == 200
    html = html_av(svar)
    boks = feilboks(html)
    assert FOR_LANG_CV in boks
    assert tekster.FEILTEKSTER[("annonse", FeilType.TOM)] in boks
    assert boks.index(FOR_LANG_CV) < boks.index("Stillingsannonse")
    tekstboks = element(html, "cv-tekst")
    assert tekstboks["aria-invalid"] == "true"
    assert tekstboks["aria-describedby"] == "cv-feil cv-hjelp"
    assert f'<p class="feiltekst" id="cv-feil">{FOR_LANG_CV}</p>' in html
    assert med_autofocus(html) == ["feilboks"]
    assert cv in html
    assert kalt == []
    lagret = soknaden(app, client)
    assert lagret.cv == Tekstfelt(cv)
    assert lagret.ki_kall == 0


def test_nfr11_for_lang_annonse_gir_feilen_ved_annonsen(med_nokkel):
    """NFR-11: en annonse på 15 001 tegn gir for lang ved annonsen, og ingen KI-kall."""
    app, client, kalt = med_nokkel
    legg_paa_innlegging(app, client)
    svar = sjekk(client, annonse="b" * (MAKS_TEGN + 1))
    html = html_av(svar)
    assert element(html, "annonse-tekst")["aria-invalid"] == "true"
    assert f'<p class="feiltekst" id="annonse-feil">{FOR_LANG_ANNONSE}</p>' in html
    assert "cv-feil" not in html
    assert kalt == []


def test_nfr11_tegngrensen_gjelder_ogsaa_i_testmodus(app, paa_innlegging):
    """NFR-11/FR-34: i testmodus gir en for lang CV bare for lang, ikke også «ikke testdata»,
    og annonsen fra testdataene gir ingen feil."""
    svar = sjekk(paa_innlegging, cv="a" * (MAKS_TEGN + 1))
    assert svar.status_code == 200
    html = html_av(svar)
    assert f'<p class="feiltekst" id="cv-feil">{FOR_LANG_CV}</p>' in html
    assert tekster.FEILTEKSTER[("cv", FeilType.IKKE_TESTDATA)] not in html
    assert "annonse-feil" not in html
    assert soknaden(app, paa_innlegging).nokkelord is None


# --- Telleren for KI-kall ---


def test_nfr11_forste_analyse_gir_to_kall(med_nokkel):
    """NFR-11: med 0 kall brukt kjøres analysen, og telleren blir 2."""
    app, client, kalt = med_nokkel
    legg_paa_innlegging(app, client)
    assert sjekk(client).location == "/resultat"
    assert kalt == ["nokkelord", "gap"]
    assert soknaden(app, client).ki_kall == 2


@pytest.mark.parametrize(("oppgave", "kall"), [("nokkelord", 1), ("gap", 2)])
def test_nfr11_ki_feil_i_analysen_teller_kallene_som_ble_startet(med_nokkel, oppgave, kall):
    """NFR-11/FR-28: feiler nøkkelordene, øker telleren med 1 (gap ble ikke kalt). Feiler gap,
    øker den med 2. KI-feilboksen er som før, med «Prøv på nytt»."""
    app, client, _ = med_nokkel
    kalt = []
    app.extensions["ekte_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave=oppgave, kalt=kalt)
    legg_paa_innlegging(app, client)
    svar = sjekk(client)
    assert svar.status_code == 200
    boks = feilboks(html_av(svar))
    assert tekster.KI_FEILTEKSTER[KIFeilType.ANNET] in boks
    assert tekster.PROV_PA_NYTT_KNAPP in boks
    assert len(kalt) == kall
    lagret = soknaden(app, client)
    assert lagret.ki_kall == kall
    assert lagret.opptatt is False


def test_nfr11_ikke_plass_til_analysen(med_nokkel):
    """NFR-11: med 9 kall brukt er det ikke plass til begge kallene i analysen. KI-en kalles
    ikke, og innleggingen viser meldingen i feilboksen med «Det du har lagt inn, er ikke borte.»
    under, uten «Prøv på nytt». Telleren er uendret, og teksten står igjen."""
    app, client, kalt = med_nokkel
    legg_paa_innlegging(app, client, ki_kall=MAKS_KI_KALL - 1)
    svar = sjekk(client)
    assert svar.status_code == 200
    html = html_av(svar)
    boks = feilboks(html)
    assert KI_KALL_BRUKT in boks
    assert tekster.KI_FEIL_BEHOLDT_INNLEGGING in boks
    assert boks.index(KI_KALL_BRUKT) < boks.index(tekster.KI_FEIL_BEHOLDT_INNLEGGING)
    assert tekster.PROV_PA_NYTT_KNAPP not in html
    assert LENKE_NY_SOKNAD in boks
    assert med_autofocus(html) == ["feilboks"]
    assert kalt == []
    lagret = soknaden(app, client)
    assert lagret.ki_kall == MAKS_KI_KALL - 1
    assert lagret.cv == Tekstfelt(CV)
    assert lagret.annonse == Tekstfelt(ANNONSE)
    assert lagret.opptatt is False


def test_nfr11_ni_analyser_gir_ti_kall_og_den_tiende_gir_meldingen(med_nokkel):
    """NFR-11/FR-15 (story 7.3): den første «Sjekk CV-en min» gir 2 kall. Annonsen er lik, så
    nøkkelordlisten gjenbrukes, og de neste åtte gir 1 kall hver (bare gap), til sammen 10.
    Den tiende gangen gir meldingen uten KI-kall."""
    app, client, kalt = med_nokkel
    legg_paa_innlegging(app, client)
    for _ in range(9):
        assert sjekk(client).location == "/resultat"
    assert soknaden(app, client).ki_kall == MAKS_KI_KALL
    assert kalt == ["nokkelord"] + ["gap"] * 9
    svar = sjekk(client)
    assert svar.status_code == 200
    assert KI_KALL_BRUKT in feilboks(html_av(svar))
    assert len(kalt) == MAKS_KI_KALL


def test_nfr11_brevet_gir_ett_kall(med_nokkel):
    """NFR-11: «Lag søknadsbrevet mitt» bruker ett kall, også med 9 brukt (grensen nås, men
    passeres ikke)."""
    app, client, kalt = med_nokkel
    legg_paa_resultat(app, client, ki_kall=MAKS_KI_KALL - 1)
    assert client.post("/resultat", data={"handling": "brev"}).location == "/brev"
    assert kalt == ["brev"]
    assert soknaden(app, client).ki_kall == MAKS_KI_KALL


def test_nfr11_ki_feil_i_brevet_teller_kallet(med_nokkel):
    """NFR-11/FR-28: feiler brevet, er kallet likevel telt, og KI-feilboksen er som før."""
    app, client, _ = med_nokkel
    app.extensions["ekte_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave="brev")
    legg_paa_resultat(app, client, ki_kall=2)
    svar = client.post("/resultat", data={"handling": "brev"})
    assert svar.status_code == 200
    boks = feilboks(html_av(svar))
    assert tekster.KI_FEILTEKSTER[KIFeilType.ANNET] in boks
    assert tekster.PROV_PA_NYTT_KNAPP in boks
    assert tekster.LAG_NY_SOKNAD_KNAPP not in boks
    lagret = soknaden(app, client)
    assert lagret.ki_kall == 3
    assert lagret.brev is None


def test_nfr11_ikke_plass_til_brevet(med_nokkel):
    """NFR-11: med 10 kall brukt kalles ikke KI-en for «Lag søknadsbrevet mitt» (eller «Prøv
    på nytt», som sender samme skjema). Resultatsiden vises med meldingen og «Resultatet og det
    du har lagt inn, er ikke borte.», uten «Prøv på nytt», og resultatet er ikke borte."""
    app, client, kalt = med_nokkel
    soknad = legg_paa_resultat(app, client, ki_kall=MAKS_KI_KALL)
    svar = client.post("/resultat", data={"handling": "brev"})
    assert svar.status_code == 200
    html = html_av(svar)
    boks = feilboks(html)
    assert KI_KALL_BRUKT in boks
    assert tekster.KI_FEIL_BEHOLDT_RESULTAT in boks
    assert tekster.PROV_PA_NYTT_KNAPP not in html
    assert LENKE_NY_SOKNAD in boks
    assert med_autofocus(html) == ["feilboks"]
    assert 'id="gap-dekker"' in html
    assert 'id="nokkelordtreff"' in html
    assert kalt == []
    assert soknaden(app, client) == soknad


# --- Alle KI-kallene er brukt, og søknaden har et brev (retro 8, A1) ---


def med_brev(modus):
    """En søknad med analysen fra case 1 (også den vaskede annonsen listen ble laget fra),
    samtykke, alle KI-kallene brukt og et brev: brev-1 i Full generering, det forbedrede
    brevet (korrektur_svar) i Korrektur. Steget er brev, som etter nettleserens tilbakeknapp
    fra brevsiden."""
    korrektur = modus == Modus.KORREKTUR
    return Soknad(
        steg=Steg.BREV,
        modus=modus,
        samtykke=True,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        eget_brev=Tekstfelt(EGET_BREV) if korrektur else Tekstfelt(),
        nokkelord=tuple(NOKKELORD_SVAR["nokkelord"]),
        nokkelord_annonse=vask(ANNONSE),
        arbeidsgiver=NOKKELORD_SVAR["arbeidsgiver"],
        gap=GAP_SVAR,
        brev=None if korrektur else BREV_1,
        korrektur=korrektur_svar() if korrektur else None,
        ki_kall=MAKS_KI_KALL,
    )


def sjekk_med_brev(client, soknad, cv=None):
    """«Sjekk CV-en min» med feltene uendret, også det egne brevet i Korrektur. cv gir en
    annen CV i stedet."""
    data = {
        "cv": soknad.cv.tekst if cv is None else cv,
        "annonse": soknad.annonse.tekst,
        "handling": "sjekk",
    }
    if soknad.modus == Modus.KORREKTUR:
        data["eget_brev"] = soknad.eget_brev.tekst
    return client.post("/innlegging", data=data)


def sjekk_boksen_med_brev(boks, beholdt):
    """Feilboksen med brev: meldingen fra brevsiden over beholdt, lenken «Gå til brevet» og
    ingen lenke til startsiden (retro 8, A1, A6)."""
    assert f'<p class="feilboks-overskrift">{KI_KALL_BRUKT_BREV}</p>' in boks
    assert KI_KALL_BRUKT not in boks
    assert boks.index(KI_KALL_BRUKT_BREV) < boks.index(beholdt)
    assert LENKE_TIL_BREVET in boks
    assert LENKE_NY_SOKNAD not in boks
    assert 'href="/"' not in boks
    assert tekster.PROV_PA_NYTT_KNAPP not in boks
    assert "<button" not in boks


def sjekk_at_brevet_er_der(app, client, soknad):
    """Søknaden er uendret, og «Gå til brevet» (GET /brev) viser brevet."""
    assert soknaden(app, client) == soknad
    svar = client.get("/brev")
    assert svar.status_code == 200
    assert brevtekst(html_av(svar)) == ferdig_brev(soknad)
    assert soknaden(app, client) == soknad


@pytest.mark.parametrize("modus", [Modus.FULL_GENERERING, Modus.KORREKTUR])
def test_nfr11_ikke_plass_til_brevet_med_brev_gir_lenken_til_brevet(med_nokkel, modus):
    """NFR-11/FR-25 (retro 8, A1): har søknaden et brev (for eksempel etter tilbakeknappen fra
    brevsiden) og alle KI-kallene er brukt, gir «Lag søknadsbrevet mitt» (eller «Oppdater
    søknadsbrevet mitt») feilboksen med teksten fra brevsiden og «Gå til brevet», ikke «Lag ny
    søknad», som ville slettet brevet. KI-en kalles ikke, brevet er der fortsatt, og lenken
    viser det. Samme regel i Korrektur (ferdig_brev)."""
    app, client, kalt = med_nokkel
    soknad = med_brev(modus)
    sett_soknad(app, client, soknad)
    svar = client.post("/resultat", data={"handling": "brev"})
    assert svar.status_code == 200
    html = html_av(svar)
    sjekk_boksen_med_brev(feilboks(html), tekster.KI_FEIL_BEHOLDT_RESULTAT)
    # Avbryt i vinduet «Vil du ha et nytt forslag?» har også autofocus, men bare når vinduet
    # åpnes (retro 3).
    assert med_autofocus(html) == ["feilboks", "nytt-forslag-avbryt"]
    assert kalt == []
    sjekk_at_brevet_er_der(app, client, soknad)


@pytest.mark.parametrize("modus", [Modus.FULL_GENERERING, Modus.KORREKTUR])
def test_nfr11_ikke_plass_til_analysen_med_brev_gir_lenken_til_brevet(med_nokkel, modus):
    """NFR-11/FR-8 (retro 8, A1): har søknaden et brev, og feltene er uendret, beholder
    sett_inndata brevet. Er det ikke plass til analysen, gir innleggingen feilboksen med
    teksten fra brevsiden og «Gå til brevet», ikke «Lag ny søknad». KI-en kalles ikke, og
    brevet er der fortsatt. Samme regel i Korrektur."""
    app, client, kalt = med_nokkel
    soknad = med_brev(modus)
    sett_soknad(app, client, soknad)
    svar = sjekk_med_brev(client, soknad)
    assert svar.status_code == 200
    html = html_av(svar)
    sjekk_boksen_med_brev(feilboks(html), tekster.KI_FEIL_BEHOLDT_INNLEGGING)
    assert med_autofocus(html) == ["feilboks"]
    assert kalt == []
    sjekk_at_brevet_er_der(app, client, soknad)


@pytest.mark.parametrize("modus", [Modus.FULL_GENERERING, Modus.KORREKTUR])
def test_nfr11_endrede_felt_sletter_brevet_og_gir_lag_ny_soknad(med_nokkel, modus):
    """NFR-11/FR-8 (retro 8, A1): er CV-en endret, sletter sett_inndata brevet før KI-kallene
    telles. Er det da ikke plass til analysen (gap, for annonsen og listen er de samme), er det
    ikke noe brev å miste, og feilboksen har meldingen og «Lag ny søknad» som før. Samme regel
    i Korrektur, der det egne brevet er uendret."""
    app, client, kalt = med_nokkel
    soknad = med_brev(modus)
    sett_soknad(app, client, soknad)
    svar = sjekk_med_brev(client, soknad, cv=CV + " En ny setning.")
    assert svar.status_code == 200
    boks = feilboks(html_av(svar))
    assert f'<p class="feilboks-overskrift">{KI_KALL_BRUKT}</p>' in boks
    assert LENKE_NY_SOKNAD in boks
    assert LENKE_TIL_BREVET not in boks
    assert kalt == []
    lagret = soknaden(app, client)
    assert ferdig_brev(lagret) is None
    assert lagret.nokkelord == soknad.nokkelord
    assert lagret.ki_kall == MAKS_KI_KALL


def test_nfr11_ny_soknad_fra_startsiden_begynner_paa_null(med_nokkel):
    """NFR-11: når grensen er nådd, gir startsiden en ny søknad med telleren på 0, og
    analysen kan kjøres igjen."""
    app, client, kalt = med_nokkel
    legg_paa_resultat(app, client, ki_kall=MAKS_KI_KALL)
    client.get("/")
    assert soknaden(app, client).ki_kall == 0
    assert client.post("/", data={"samtykke": "ja"}).location == "/modus"
    assert client.post("/modus", data={"modus": "full_generering"}).location == "/innlegging"
    assert sjekk(client).location == "/resultat"
    assert kalt == ["nokkelord", "gap"]
    assert soknaden(app, client).ki_kall == 2


def test_nfr11_testmodus_teller_ingen_kall_og_stopper_ingenting(app, innlogget_client):
    """NFR-11: i testmodus telles ingen kall, og ingenting stoppes. Med ki_kall = 10 kjøres
    analysen og brevet som før, og telleren er uendret."""
    kalt = []
    app.extensions["test_ki"] = TellendeKI(app.extensions["test_ki"], kalt=kalt)
    sett_soknad(
        app,
        innlogget_client,
        Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, ki_kall=MAKS_KI_KALL),
    )
    assert sjekk(innlogget_client).location == "/resultat"
    assert soknaden(app, innlogget_client).ki_kall == MAKS_KI_KALL
    assert innlogget_client.post("/resultat", data={"handling": "brev"}).location == "/brev"
    assert kalt == ["nokkelord", "gap", "brev"]
    assert soknaden(app, innlogget_client).ki_kall == MAKS_KI_KALL


class KrasjendeKI(TellendeKI):
    """TellendeKI der nokkelord gir et uventet unntak (ikke KIFeil)."""

    def nokkelord(self, annonse):
        self.kalt.append("nokkelord")
        raise RuntimeError("uventet")


def test_nfr11_uventet_unntak_teller_kallet_og_slipper_opptatt(med_nokkel):
    """NFR-11/AD-8: gir ekte KI et uventet unntak (ikke KIFeil) i analysen, går unntaket
    videre, men kallet som ble startet, er telt, og søknaden er ikke lenger opptatt."""
    app, client, _ = med_nokkel
    kalt = []
    app.extensions["ekte_ki"] = KrasjendeKI(app.extensions["test_ki"], kalt=kalt)
    legg_paa_innlegging(app, client)
    with pytest.raises(RuntimeError):
        sjekk(client)
    assert kalt == ["nokkelord"]
    lagret = soknaden(app, client)
    assert lagret.ki_kall == 1
    assert lagret.opptatt is False


def test_nfr11_feltfeil_vinner_over_meldingen_om_kallene(med_nokkel):
    """NFR-11/FR-9: med 9 kall brukt og tom annonse vises feltfeilen i feilboksen, ikke
    meldingen om at alle KI-kallene er brukt, og KI-en kalles ikke."""
    app, client, kalt = med_nokkel
    legg_paa_innlegging(app, client, ki_kall=MAKS_KI_KALL - 1)
    svar = sjekk(client, annonse="")
    assert svar.status_code == 200
    html = html_av(svar)
    assert tekster.FEILTEKSTER[("annonse", FeilType.TOM)] in feilboks(html)
    assert KI_KALL_BRUKT not in html
    assert kalt == []
    assert soknaden(app, client).ki_kall == MAKS_KI_KALL - 1
