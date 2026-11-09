"""Tester for stegene i en søknad (FR-20, AD-8)."""

from soknad.kjerne.steg import Steg, kan_vises


def test_fr20_stegene_har_fast_rekkefolge():
    """FR-20/AD-8: start < modus < innlegging < resultat < brev, og ingen andre steg."""
    assert list(Steg) == [Steg.START, Steg.MODUS, Steg.INNLEGGING, Steg.RESULTAT, Steg.BREV]
    assert Steg.START < Steg.MODUS < Steg.INNLEGGING < Steg.RESULTAT < Steg.BREV


def test_fr20_side_kan_vises_naar_steget_er_naadd():
    """FR-20/AD-8: en side kan vises når sidens steg ≤ søknadens steg, ellers ikke."""
    assert kan_vises(Steg.START, Steg.START)
    assert kan_vises(Steg.MODUS, Steg.MODUS)
    assert kan_vises(Steg.START, Steg.INNLEGGING)
    assert kan_vises(Steg.MODUS, Steg.BREV)
    assert not kan_vises(Steg.MODUS, Steg.START)
    assert not kan_vises(Steg.INNLEGGING, Steg.MODUS)
    assert not kan_vises(Steg.BREV, Steg.RESULTAT)
