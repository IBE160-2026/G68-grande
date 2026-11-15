"""Tester for feiltekstene til de nye feilene: ikke_testdata på CV-, brev- og annonsefeltet og
alle typene KI-feil har en tekst (FR-8, FR-20, FR-28, FR-34, AD-9)."""

import pytest

from soknad.kjerne.feil import FeilType, InndataFeil, KIFeil, KIFeilType
from soknad.kjerne.okt import Modus
from soknad.web import tekster


@pytest.mark.parametrize("felt", ["cv", "eget_brev", "annonse"])
def test_fr34_ikke_testdata_har_tekst_for_feltet(felt):
    """FR-34 (story 5.1): ikke_testdata har en tekst på CV-feltet, brevfeltet og
    annonsefeltet."""
    tekst = tekster.feiltekst(InndataFeil(felt, FeilType.IKKE_TESTDATA))
    assert tekst.endswith("I testmodus fungerer bare testdataene fra mappen backend/testdata/.")


def test_fr34_feltnavnet_star_forst_i_teksten():
    """FR-34: teksten begynner med feltnavnet, slik som i UX."""
    assert tekster.feiltekst(InndataFeil("cv", FeilType.IKKE_TESTDATA)).startswith("CV: ")
    assert tekster.feiltekst(InndataFeil("annonse", FeilType.IKKE_TESTDATA)).startswith(
        "Stillingsannonse: "
    )
    assert tekster.feiltekst(InndataFeil("eget_brev", FeilType.IKKE_TESTDATA)).startswith(
        "Ditt søknadsbrev: "
    )


def test_fr8_fr20_tekstene_for_korrektur():
    """FR-8/FR-9/FR-20 (story 5.1): kortet, overskriften, tittelen, feltet og feiltekstene i
    Korrektur, slik som i spec-en."""
    assert tekster.MODUS_KORT[Modus.KORREKTUR] == (
        "✏️",
        "Korrektur",
        "Forbedre mitt brev",
        "Du har skrevet et brev selv. Vi forbedrer språket og beholder innholdet ditt.",
    )
    assert list(tekster.MODUS_KORT) == [Modus.FULL_GENERERING, Modus.KORREKTUR]
    assert tekster.INNLEGGING_OVERSKRIFT_KORREKTUR == (
        "Legg inn CV-en din, brevet ditt og stillingsannonsen"
    )
    assert tekster.INNLEGGING_TITTEL_KORREKTUR == "Legg inn CV, brev og annonse"
    assert tekster.INNLEGGINGSFELT["eget_brev"] == ("✉️", "Ditt søknadsbrev", "brevfeltet")
    assert tekster.feiltekst(InndataFeil("eget_brev", FeilType.TOM)) == (
        "Ditt søknadsbrev: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
    )
    assert tekster.feiltekst(InndataFeil("eget_brev", FeilType.FOR_LANG)) == (
        "Ditt søknadsbrev: Teksten er for lang. Den kan være på høyst 15 000 tegn."
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
