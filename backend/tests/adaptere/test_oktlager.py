"""Tester for øktlageret i minnet (FR-3, FR-5, FR-6, FR-7)."""

from soknad import create_app
from soknad.adaptere.oktlager import Oktlager
from soknad.kjerne.okt import Innlogging, Soknad
from soknad.kjerne.steg import Steg


def test_fr5_soknaden_lagres_ved_siden_av_innloggingen():
    """FR-5/AD-7: søknaden lagres under økt-id-en og kan hentes igjen. Innloggingen er uendret."""
    lager = Oktlager()
    okt_id = lager.ny(Innlogging(1, testmodus=True))
    assert lager.hent_soknad(okt_id) is None
    soknad = Soknad(steg=Steg.MODUS)
    lager.lagre_soknad(okt_id, soknad)
    assert lager.hent_soknad(okt_id) == soknad
    assert lager.hent(okt_id) == Innlogging(1, testmodus=True)
    assert lager.hent_soknad(None) is None
    assert lager.hent_soknad("finnes-ikke") is None


def test_fr5_hver_okt_har_sin_egen_soknad():
    """FR-5/AD-7: to økter har hver sin søknad."""
    lager = Oktlager()
    en = lager.ny(Innlogging(1, testmodus=True))
    to = lager.ny(Innlogging(2, testmodus=True))
    lager.lagre_soknad(en, Soknad(steg=Steg.MODUS))
    assert lager.hent_soknad(to) is None


def test_fr6_soknad_lagres_ikke_uten_okt():
    """FR-6/AD-7: uten innlogging lagres ingen søknad, så ingenting blir liggende i minnet."""
    lager = Oktlager()
    lager.lagre_soknad("finnes-ikke", Soknad())
    lager.lagre_soknad(None, Soknad())
    assert lager.hent_soknad("finnes-ikke") is None
    assert lager._soknader == {}


def test_fr6_slett_sletter_ogsaa_soknaden():
    """FR-6/AD-7: utlogging (slett) fjerner både innloggingen og søknaden."""
    lager = Oktlager()
    okt_id = lager.ny(Innlogging(1, testmodus=True))
    lager.lagre_soknad(okt_id, Soknad())
    lager.slett(okt_id)
    assert lager.hent(okt_id) is None
    assert lager.hent_soknad(okt_id) is None
    lager.lagre_soknad(okt_id, Soknad())
    assert lager.hent_soknad(okt_id) is None


def test_ad8_erstatt_soknad_bare_naar_den_er_den_forventede():
    """AD-8: erstatt_soknad lagrer bare når søknaden i lageret er samme objekt som forventet.
    En lik, men ny søknad (startsiden i en annen fane) blir stående."""
    lager = Oktlager()
    okt_id = lager.ny(Innlogging(1, testmodus=True))
    opptatt = Soknad(steg=Steg.INNLEGGING, opptatt=True)
    lager.lagre_soknad(okt_id, opptatt)
    ferdig = Soknad(steg=Steg.RESULTAT)
    assert lager.erstatt_soknad(okt_id, opptatt, ferdig) is True
    assert lager.hent_soknad(okt_id) is ferdig
    # Byttet ut med en ny søknad: lik verdi er ikke nok, det må være samme objekt.
    ny = Soknad()
    lager.lagre_soknad(okt_id, ny)
    assert lager.erstatt_soknad(okt_id, Soknad(), ferdig) is False
    assert lager.erstatt_soknad(okt_id, opptatt, ferdig) is False
    assert lager.hent_soknad(okt_id) is ny


def test_ad8_erstatt_soknad_lagrer_ikke_uten_okt():
    """AD-8/FR-6: uten økt lagres ingenting, heller ikke etter at økten er slettet."""
    lager = Oktlager()
    assert lager.erstatt_soknad("finnes-ikke", Soknad(), Soknad()) is False
    assert lager.erstatt_soknad(None, Soknad(), Soknad()) is False
    assert lager.hent_soknad("finnes-ikke") is None
    okt_id = lager.ny(Innlogging(1, testmodus=True))
    soknad = Soknad()
    lager.lagre_soknad(okt_id, soknad)
    lager.slett(okt_id)
    assert lager.erstatt_soknad(okt_id, soknad, Soknad()) is False
    assert lager.hent_soknad(okt_id) is None


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


def test_fr32_bytt_innlogging_beholder_okt_id_og_soknad():
    """FR-32: bytt_innlogging bytter innloggingen på samme økt-id, og søknaden beholdes."""
    lager = Oktlager()
    okt_id = lager.ny(Innlogging(1, testmodus=False))
    soknad = Soknad(steg=Steg.START)
    lager.lagre_soknad(okt_id, soknad)
    assert lager.bytt_innlogging(okt_id, Innlogging(1, testmodus=True)) is True
    assert lager.hent(okt_id) == Innlogging(1, testmodus=True)
    assert lager.hent_soknad(okt_id) is soknad


def test_fr32_bytt_innlogging_uten_okt_lager_ingen_ny():
    """FR-32/FR-6: finnes ikke økten (utlogget), lages ingen ny innlogging."""
    lager = Oktlager()
    assert lager.bytt_innlogging("finnes-ikke", Innlogging(1, testmodus=False)) is False
    assert lager.bytt_innlogging(None, Innlogging(1, testmodus=False)) is False
    assert lager.hent("finnes-ikke") is None
    assert lager._innlogginger == {}
