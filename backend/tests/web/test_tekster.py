"""Tester for feiltekstene til de nye feilene: ikke_testdata på CV- og annonsefeltet og alle
typene KI-feil har en tekst (FR-28, FR-34, AD-9)."""

import pytest

from soknad.kjerne.feil import FeilType, InndataFeil, KIFeil, KIFeilType
from soknad.web import tekster


@pytest.mark.parametrize("felt", ["cv", "annonse"])
def test_fr34_ikke_testdata_har_tekst_for_feltet(felt):
    """FR-34: ikke_testdata har en tekst på både CV- og annonsefeltet."""
    tekst = tekster.feiltekst(InndataFeil(felt, FeilType.IKKE_TESTDATA))
    assert tekst.endswith("I testmodus fungerer bare testdataene fra mappen backend/testdata/.")


def test_fr34_feltnavnet_star_forst_i_teksten():
    """FR-34: teksten begynner med feltnavnet, slik som i UX."""
    assert tekster.feiltekst(InndataFeil("cv", FeilType.IKKE_TESTDATA)).startswith("CV: ")
    assert tekster.feiltekst(InndataFeil("annonse", FeilType.IKKE_TESTDATA)).startswith(
        "Stillingsannonse: "
    )


def test_fr34_annen_case_har_teksten_kristine_bestemte():
    """FR-34 (story 4.5): CV og annonse fra ulike testcaser gir en egen tekst på
    annonsefeltet, bestemt av Kristine 14. november 2026."""
    assert tekster.feiltekst(InndataFeil("annonse", FeilType.ANNEN_CASE)) == (
        "Stillingsannonse: I testmodus må CV-en og annonsen være fra samme mappe i "
        "backend/testdata/."
    )


@pytest.mark.parametrize("type", list(KIFeilType))
def test_fr28_hver_ki_feil_har_tekst(type):
    """FR-28: hver type KI-feil har en tekst."""
    assert tekster.ki_feiltekst(KIFeil(type))


def test_fr28_ki_feiltekstene_fra_ux():
    """FR-28: nettverksfeil har egen tekst. Andre feil og ubrukelige svar har samme tekst."""
    assert tekster.ki_feiltekst(KIFeil(KIFeilType.NETTVERK)) == (
        "Nettverksfeil, sjekk nettverkstilgangen."
    )
    andre = "Noe gikk galt hos KI-tjenesten. Prøv på nytt."
    assert tekster.ki_feiltekst(KIFeil(KIFeilType.ANNET)) == andre
    assert tekster.ki_feiltekst(KIFeil(KIFeilType.UBRUKELIG_SVAR)) == andre


def test_fr28_tekstene_i_feilboksen_fra_ux():
    """FR-28/UX-DR7: setningen under feilteksten på innleggingen og knappen, ordrett fra
    EXPERIENCE."""
    assert tekster.KI_FEIL_BEHOLDT_INNLEGGING == "Det du har lagt inn, er ikke borte."
    assert tekster.PROV_PA_NYTT_KNAPP == "Prøv på nytt"
