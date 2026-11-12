"""Felles fiksturer for webtestene (FR-8, FR-21, FR-29). Testfilene henter fiksturene herfra
og hjelperne fra hjelpere.py, aldri fra hverandre."""

import pytest

from soknad.adaptere import fil_ut
from soknad.kjerne.feil import FilFeil
from soknad.kjerne.okt import Modus, Soknad
from soknad.kjerne.steg import Steg
from tests.web.hjelpere import ANNONSE, CV, sett_soknad


@pytest.fixture
def paa_innlegging(app, innlogget_client):
    """En innlogget klient på innleggingen for Full generering."""
    sett_soknad(app, innlogget_client, Soknad(steg=Steg.INNLEGGING, modus=Modus.FULL_GENERERING))
    return innlogget_client


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
