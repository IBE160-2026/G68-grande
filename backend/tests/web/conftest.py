"""Felles fiksturer for webtestene (FR-8, FR-20, FR-21, FR-29). Testfilene henter fiksturene
herfra og hjelperne fra hjelpere.py, aldri fra hverandre."""

import pytest

from soknad.adaptere import fil_ut
from soknad.kjerne.feil import FilFeil
from soknad.kjerne.okt import Modus, Soknad
from soknad.kjerne.steg import Steg
from tests.web.hjelpere import (
    ANNONSE,
    CV,
    EGET_BREV,
    TellendeKI,
    app_med_nokkel,
    korrektur_testki,
    logg_inn,
    sett_soknad,
)


@pytest.fixture
def med_nokkel():
    """(app, klient, kalt): innlogget i en app med API-nøkkel, så testmodus er av (FR-32). EkteKI
    er byttet ut med TellendeKI, og kalt viser hvilke oppgaver den har fått."""
    app = app_med_nokkel()
    kalt = []
    app.extensions["ekte_ki"] = TellendeKI(app.extensions["test_ki"], kalt=kalt)
    client = app.test_client()
    assert logg_inn(client).status_code == 302
    return app, client, kalt


@pytest.fixture
def paa_innlegging(app, innlogget_client):
    """En innlogget klient på innleggingen for Full generering."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))
    return innlogget_client


@pytest.fixture
def paa_korrektur(app, innlogget_client):
    """En innlogget klient på innleggingen for Korrektur, i testmodus (story 5.1)."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=Modus.KORREKTUR))
    return innlogget_client


@pytest.fixture
def paa_resultat_korrektur(paa_korrektur):
    """En innlogget klient i Korrektur som har lagt inn CV, eget brev og annonse fra case 1 og
    fått analysen (story 5.1)."""
    data = {"cv": CV, "eget_brev": EGET_BREV, "annonse": ANNONSE, "handling": "sjekk"}
    assert paa_korrektur.post("/innlegging", data=data).location == "/resultat"
    return paa_korrektur


@pytest.fixture
def korrektur_ki(app, tmp_path):
    """TestKI byttes ut med en som har korrektur-1.json og korrektur-2.json i case 1
    (korrektur_testki), så flyten i Korrektur kan testes uten de ekte svarfilene."""
    app.extensions["test_ki"] = korrektur_testki(tmp_path)
    return app.extensions["test_ki"]


@pytest.fixture
def paa_brev_korrektur(korrektur_ki, paa_resultat_korrektur):
    """En innlogget klient i Korrektur som har trykket «Oppdater søknadsbrevet mitt» og fått
    det forbedrede brevet (story 5.2.1)."""
    svar = paa_resultat_korrektur.post("/resultat", data={"handling": "brev"})
    assert svar.location == "/brev"
    return paa_resultat_korrektur


@pytest.fixture
def paa_resultat(paa_innlegging):
    """En innlogget klient som har lagt inn testdataene fra case 1 og fått analysen."""
    svar = paa_innlegging.post(
        "/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"}
    )
    assert svar.location == "/resultat"
    return paa_innlegging


@pytest.fixture
def paa_brev(paa_resultat):
    """En innlogget klient som har trykket «Lag søknadsbrevet mitt» og fått brevet."""
    assert paa_resultat.post("/resultat", data={"handling": "brev"}).location == "/brev"
    return paa_resultat


@pytest.fixture
def filfeil(monkeypatch):
    """Word-filen kan ikke lages."""

    def feiler(avsnitt):
        raise FilFeil()

    monkeypatch.setattr(fil_ut, "lag_docx", feiler)


@pytest.fixture
def filfeil_pdf(monkeypatch):
    """PDF-filen kan ikke lages (story 7.2). Word-filen lages som vanlig."""

    def feiler(avsnitt):
        raise FilFeil()

    monkeypatch.setattr(fil_ut, "lag_pdf", feiler)
