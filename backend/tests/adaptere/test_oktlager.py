"""Tester for øktlageret i minnet (FR-3, FR-7)."""

from soknad import create_app
from soknad.adaptere.oktlager import Oktlager
from soknad.kjerne.okt import Innlogging


def test_fr3_ny_okt_kan_hentes_med_okt_id():
    """FR-3: en ny økt lagres under en tilfeldig økt-id og kan hentes igjen."""
    lager = Oktlager()
    okt_id = lager.ny(Innlogging(1, testmodus=True))
    assert isinstance(okt_id, str)
    assert len(okt_id) >= 32
    assert lager.hent(okt_id) == Innlogging(1, testmodus=True)


def test_fr3_hver_okt_faar_ny_okt_id():
    """FR-3: to innlogginger gir to ulike økt-id-er."""
    lager = Oktlager()
    assert lager.ny(Innlogging(1, testmodus=True)) != lager.ny(Innlogging(1, testmodus=True))


def test_fr7_slettet_eller_ukjent_okt_gir_none():
    """FR-7: en slettet, ukjent eller manglende økt-id gir ingen innlogging."""
    lager = Oktlager()
    okt_id = lager.ny(Innlogging(1, testmodus=True))
    lager.slett(okt_id)
    assert lager.hent(okt_id) is None
    assert lager.hent("finnes-ikke") is None
    assert lager.hent(None) is None
    lager.slett("finnes-ikke")
    lager.slett(None)


def test_fr7_hver_app_har_sitt_eget_oktlager(app):
    """FR-7: øktlageret ligger i app.extensions, så en ny app (omstart) har ingen økter."""
    annen = create_app({"TESTING": True})
    assert isinstance(app.extensions["oktlager"], Oktlager)
    assert app.extensions["oktlager"] is not annen.extensions["oktlager"]
