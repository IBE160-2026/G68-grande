"""Tester for gjenbruken av nøkkelordlisten når bare CV-en er endret (FR-15, FR-19, FR-28,
NFR-11, story 7.3). Når annonsen er lik (etter samme vask som AD-10), brukes listen fra før,
og «Sjekk CV-en min» kaller KI-en bare for gap-analysen. Ingen test kaller det ekte API-et:
EkteKI byttes ut med en falsk KI før noe kalles.

I testmodus må CV-en være lik testdataene, og TestKI finner caset ut fra CV-en. Testene med en
endret CV kjører derfor med testmodus av og FasteSvarKI, som svarer likt uansett CV."""

import pytest

from soknad.innstillinger import MAKS_KI_KALL
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.okt import Modus, Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.kjerne.telleregel import tell_treff
from soknad.kjerne.testdata_match import vask
from soknad.web import tekster
from tests.web.hjelpere import (
    ANNONSE,
    CV,
    GAP_SVAR,
    NOKKELORD_SVAR,
    TellendeKI,
    html_av,
    sett_soknad,
    soknaden,
)

LISTE = tuple(NOKKELORD_SVAR["nokkelord"])
# Et nøkkelord som mangler i CV-en fra case 1, og CV-en med ordet lagt til.
MANGLER = tell_treff(list(LISTE), CV).ikke_treff[0]
NY_CV = f"{CV}\n{MANGLER}\n"


class FasteSvarKI(TellendeKI):
    """TellendeKI som svarer NOKKELORD_SVAR og GAP_SVAR uansett CV og annonse, så en CV som
    ikke er testdata også gir en analyse. Oppgavene i feiler gir KIFeil, etter at de er
    skrevet i kalt."""

    def __init__(self, test_ki, kalt=None, feiler=()):
        super().__init__(test_ki, kalt=kalt)
        self.feiler = set(feiler)

    def _svar(self, oppgave, svar):
        self.kalt.append(oppgave)
        if oppgave in self.feiler:
            raise KIFeil(KIFeilType.ANNET)
        return svar

    def nokkelord(self, annonse):
        return self._svar("nokkelord", NOKKELORD_SVAR)

    def gap(self, cv, annonse):
        return self._svar("gap", GAP_SVAR)


def sjekk_cv(client, cv=CV, annonse=ANNONSE):
    """«Sjekk CV-en min» (og «Prøv på nytt», som sender samme skjema) på innleggingen."""
    return client.post("/innlegging", data={"cv": cv, "annonse": annonse, "handling": "sjekk"})


def treffteksten(cv):
    """Linjen «X av Y = Z %» for listen fra case 1 og cv."""
    treff = tell_treff(list(LISTE), cv)
    return tekster.nokkelordtreff(treff.antall_treff, treff.antall, treff.prosent)


@pytest.fixture
def ekte_ki(med_nokkel):
    """(app, klient, ki): testmodus av, FasteSvarKI som ekte KI, og en søknad med samtykke på
    innleggingen, uten analyse."""
    app, client, _ = med_nokkel
    ki = FasteSvarKI(app.extensions["test_ki"])
    app.extensions["ekte_ki"] = ki
    sett_soknad(
        app, client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING, samtykke=True)
    )
    return app, client, ki


@pytest.fixture
def ekte_paa_resultat(ekte_ki):
    """Som ekte_ki, men etter den første analysen (2 kall) på resultatsiden. kalt er tømt."""
    app, client, ki = ekte_ki
    assert sjekk_cv(client).location == "/resultat"
    assert ki.kalt == ["nokkelord", "gap"]
    assert soknaden(app, client).ki_kall == 2
    ki.kalt.clear()
    return app, client, ki


def med_liste(ki_kall):
    """En søknad på innleggingen med samtykke, case 1 og nøkkelordlisten fra annonsen."""
    return Soknad(
        steg=Steg.INNLEGGING,
        modus=Modus.FULL_GENERERING,
        samtykke=True,
        cv=Tekstfelt(CV),
        annonse=Tekstfelt(ANNONSE),
        nokkelord=LISTE,
        nokkelord_annonse=vask(ANNONSE),
        arbeidsgiver=NOKKELORD_SVAR["arbeidsgiver"],
        ki_kall=ki_kall,
    )


# --- Bare CV-en er endret ---


def test_fr15_ny_cv_gir_samme_liste_hoyere_prosent_og_bare_gap(ekte_paa_resultat):
    """FR-15/FR-19, suksesskriterium 8 (story 7.3): på resultatsiden går brukeren «Tilbake»,
    legger til et manglende nøkkelord i CV-en og trykker «Sjekk CV-en min». Nøkkelordlisten og
    arbeidsgiveren er de samme, prosenten er høyere, og KI-en er bare kalt for gap-analysen."""
    app, client, ki = ekte_paa_resultat
    for_, etter = tell_treff(list(LISTE), CV), tell_treff(list(LISTE), NY_CV)
    assert etter.prosent > for_.prosent
    assert treffteksten(CV) in html_av(client.get("/resultat"))
    assert client.get("/innlegging").status_code == 200
    assert sjekk_cv(client, cv=NY_CV).location == "/resultat"
    assert ki.kalt == ["gap"]
    lagret = soknaden(app, client)
    assert lagret.nokkelord == LISTE
    assert lagret.nokkelord_annonse == vask(ANNONSE)
    assert lagret.arbeidsgiver == NOKKELORD_SVAR["arbeidsgiver"]
    assert lagret.gap == GAP_SVAR
    assert lagret.cv == Tekstfelt(NY_CV)
    assert lagret.steg == Steg.RESULTAT
    assert treffteksten(NY_CV) in html_av(client.get("/resultat"))


def test_fr15_ekstra_mellomrom_i_annonsen_gjenbruker_listen(ekte_paa_resultat):
    """FR-15/FR-19 (story 7.3): samme annonse med ekstra mellomrom og linjeskift regnes som lik.
    Annonsen lagres slik den er sendt, og listen gjenbrukes."""
    app, client, ki = ekte_paa_resultat
    annonse = "  " + ANNONSE.replace("\n", "\n\n") + "  \n"
    assert sjekk_cv(client, cv=NY_CV, annonse=annonse).location == "/resultat"
    assert ki.kalt == ["gap"]
    lagret = soknaden(app, client)
    assert lagret.annonse == Tekstfelt(annonse)
    assert lagret.nokkelord == LISTE
    assert lagret.nokkelord_annonse == vask(ANNONSE)


def test_fr15_ekstra_mellomrom_gjenbruker_listen_i_testmodus(app, paa_resultat):
    """FR-15/FR-19 (story 7.3): i testmodus gir case 1 med tomme linjer i CV-en og ekstra
    mellomrom i annonsen samme resultatside som før, og bare gap kalles. Ingen kall telles."""
    kalt = []
    app.extensions["test_ki"] = TellendeKI(app.extensions["test_ki"], kalt=kalt)
    for_ = html_av(paa_resultat.get("/resultat"))
    assert treffteksten(CV) in for_
    assert paa_resultat.get("/innlegging").status_code == 200
    svar = sjekk_cv(paa_resultat, cv=f"\n\n{CV}\n\n", annonse=f"{ANNONSE}  \n")
    assert svar.location == "/resultat"
    assert kalt == ["gap"]
    assert treffteksten(CV) in html_av(paa_resultat.get("/resultat"))
    lagret = soknaden(app, paa_resultat)
    assert lagret.nokkelord == LISTE
    assert lagret.ki_kall == 0


# --- Annonsen er endret ---


def test_fr19_endret_annonse_henter_ny_liste(ekte_paa_resultat):
    """FR-19 (story 7.3): er annonsen endret, hentes en ny nøkkelordliste, og KI-en kalles for
    både nøkkelordene og gap-analysen (2 kall)."""
    app, client, ki = ekte_paa_resultat
    annonse = "Vi søker en ny utvikler med erfaring fra Rust."
    assert sjekk_cv(client, cv=NY_CV, annonse=annonse).location == "/resultat"
    assert ki.kalt == ["nokkelord", "gap"]
    lagret = soknaden(app, client)
    assert lagret.nokkelord_annonse == vask(annonse)
    assert lagret.ki_kall == 4


# --- KI-feil ---


def test_fr28_gap_feiler_ved_gjenbruk_og_prov_pa_nytt_kaller_bare_gap(ekte_paa_resultat):
    """FR-28/FR-15/NFR-11 (story 7.3): feiler gap-analysen når listen gjenbrukes, vises
    feilboksen som før med «Prøv på nytt». Listen står igjen, gap-analysen er ikke lagret, og
    1 kall er telt. «Prøv på nytt» kaller bare gap igjen."""
    app, client, ki = ekte_paa_resultat
    ki.feiler = {"gap"}
    svar = sjekk_cv(client, cv=NY_CV)
    assert svar.status_code == 200
    html = html_av(svar)
    assert tekster.KI_FEILTEKSTER[KIFeilType.ANNET] in html
    assert tekster.PROV_PA_NYTT_KNAPP in html
    assert ki.kalt == ["gap"]
    lagret = soknaden(app, client)
    assert lagret.nokkelord == LISTE
    assert lagret.arbeidsgiver == NOKKELORD_SVAR["arbeidsgiver"]
    assert lagret.gap is None
    assert lagret.cv == Tekstfelt(NY_CV)
    assert lagret.steg == Steg.INNLEGGING
    assert lagret.ki_kall == 3
    assert lagret.opptatt is False
    assert client.get("/resultat").location == "/innlegging"
    ki.feiler.clear()
    assert sjekk_cv(client, cv=NY_CV).location == "/resultat"
    assert ki.kalt == ["gap", "gap"]
    assert soknaden(app, client).ki_kall == 4


# --- Telleren for KI-kall ---


@pytest.mark.parametrize("brukt", [0, MAKS_KI_KALL - 1])
def test_nfr11_gjenbruk_teller_ett_kall(ekte_ki, brukt):
    """NFR-11/FR-15 (story 7.3): med ekte KI og listen gjenbrukt trenger analysen ett kall.
    Med 9 kall brukt er det plass til det, og telleren blir 10."""
    app, client, ki = ekte_ki
    sett_soknad(app, client, med_liste(brukt))
    assert sjekk_cv(client, cv=NY_CV).location == "/resultat"
    assert ki.kalt == ["gap"]
    assert soknaden(app, client).ki_kall == brukt + 1


def test_nfr11_alle_kallene_brukt_ved_gjenbruk_gir_meldingen(ekte_ki):
    """NFR-11 (story 7.3): med 10 kall brukt er det ikke plass til gap-kallet heller.
    Innleggingen viser meldingen uten «Prøv på nytt», og KI-en kalles ikke."""
    app, client, ki = ekte_ki
    sett_soknad(app, client, med_liste(MAKS_KI_KALL))
    svar = sjekk_cv(client, cv=NY_CV)
    assert svar.status_code == 200
    html = html_av(svar)
    assert tekster.KI_KALL_BRUKT in html
    assert tekster.PROV_PA_NYTT_KNAPP not in html
    assert ki.kalt == []
    lagret = soknaden(app, client)
    assert lagret.ki_kall == MAKS_KI_KALL
    assert lagret.nokkelord == LISTE
