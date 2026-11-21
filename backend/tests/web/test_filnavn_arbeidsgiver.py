"""Tester for arbeidsgiveren i filnavnet (FR-29, AD-11). Story 7.5. Filnavnet i vinduet etter
nedlasting, i filnavn-linjen under knappen og i Content-Disposition er det samme, med
arbeidsgiveren fra nøkkelordsvaret, for Word og PDF og i begge modusene. Testene er i en egen
fil, så test_nedlasting.py og test_nedlasting_pdf.py ikke vokser."""

import json
import re

import pytest

from soknad.adaptere.ki import TESTDATA_MAPPE
from soknad.kjerne.okt import Modus, Soknad
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from tests.web.hjelpere import (
    ARBEIDSGIVER,
    NEDLASTING,
    NEDLASTING_PDF,
    filnavn_i_dag,
    html_av,
    sett_soknad,
    soknaden,
)

# Fiksturene paa_innlegging, paa_brev og paa_brev_korrektur står i conftest.py.

CASE_2 = TESTDATA_MAPPE / "case-2-okonomi"
CV_2 = (CASE_2 / "cv.txt").read_text(encoding="utf-8")
ANNONSE_2 = (CASE_2 / "annonse.txt").read_text(encoding="utf-8")
NOKKELORD_SVAR_2 = json.loads((CASE_2 / "ki-svar" / "nokkelord.json").read_text(encoding="utf-8"))
ARBEIDSGIVER_2 = NOKKELORD_SVAR_2["arbeidsgiver"]
ADRESSE = {"docx": NEDLASTING, "pdf": NEDLASTING_PDF}


def paa_brev_case_2(client):
    """Klienten på innleggingen legger inn case 2 og får brevet i Full generering."""
    data = {"cv": CV_2, "annonse": ANNONSE_2, "handling": "sjekk"}
    assert client.post("/innlegging", data=data).location == "/resultat"
    assert client.post("/resultat", data={"handling": "brev"}).location == "/brev"
    return client


def filnavn_linje(html, format_):
    linje = re.search(rf'<p class="filnavn-linje" id="filnavn-{format_}"[^>]*>(.*?)</p>', html)
    return linje.group(1)


def vindu_filnavn(html):
    return re.search(r'<p id="vindu-nedlastet-filnavn">(.*?)</p>', html).group(1)


def test_fr29_casene_har_arbeidsgiveren_fra_matrisen():
    """FR-29/AD-11: arbeidsgiverne i testdataene er de i matrisen i story 7.5."""
    assert ARBEIDSGIVER == "Testvik Utvikling AS"
    assert ARBEIDSGIVER_2 == "Prøvdal Regnskap AS"
    assert filnavn_i_dag("docx").startswith("Soknad_Testvik-Utvikling-AS_")
    assert filnavn_i_dag("pdf", ARBEIDSGIVER_2).startswith("Soknad_Provdal-Regnskap-AS_")
    assert re.fullmatch(r"Soknad_Testvik-Utvikling-AS_\d{4}-\d{2}-\d{2}\.docx", filnavn_i_dag())


@pytest.mark.parametrize("format_", ["docx", "pdf"])
@pytest.mark.parametrize(
    ("oppsett", "arbeidsgiver", "navn"),
    [
        ("full_case_1", ARBEIDSGIVER, "Testvik-Utvikling-AS"),
        ("full_case_2", ARBEIDSGIVER_2, "Provdal-Regnskap-AS"),
        ("korrektur_case_1", ARBEIDSGIVER, "Testvik-Utvikling-AS"),
    ],
)
def test_fr29_filen_linjen_og_vinduet_har_samme_filnavn(
    request, oppsett, arbeidsgiver, navn, format_
):
    """FR-29/AD-11: i Full generering (case 1 og case 2) og i Korrektur (case 1) har
    Content-Disposition, filnavn-linjen for formatet og vinduet etter nedlasting samme filnavn,
    Soknad_<Arbeidsgiver>_<dato>, for Word og PDF. Vinduet har Word-filnavnet fra serveren, og
    nedlasting.js kopierer filnavn-linjen for formatet inn, så linjen og vinduet er like."""
    if oppsett == "korrektur_case_1":
        client = request.getfixturevalue("paa_brev_korrektur")
    elif oppsett == "full_case_2":
        client = paa_brev_case_2(request.getfixturevalue("paa_innlegging"))
    else:
        client = request.getfixturevalue("paa_brev")
    forventet = filnavn_i_dag(format_, arbeidsgiver)
    assert re.fullmatch(rf"Soknad_{navn}_\d{{4}}-\d{{2}}-\d{{2}}\.{format_}", forventet)
    # Før nedlasting: linjen står skjult med filnavnet, og vinduet har Word-filnavnet.
    html = html_av(client.get("/brev"))
    assert filnavn_linje(html, format_) == tekster.filnavn_linje(forventet)
    assert vindu_filnavn(html) == filnavn_linje(html, "docx")
    # Filen.
    svar = client.get(ADRESSE[format_])
    assert svar.status_code == 200
    assert svar.headers["Content-Disposition"] == f"attachment; filename={forventet}"
    # Etter nedlasting, også når siden lastes på nytt.
    html = html_av(client.get("/brev"))
    assert filnavn_linje(html, format_) == tekster.filnavn_linje(forventet)
    assert vindu_filnavn(html) == tekster.filnavn_linje(filnavn_i_dag("docx", arbeidsgiver))


@pytest.mark.parametrize("format_", ["docx", "pdf"])
@pytest.mark.parametrize("arbeidsgiver", [None, "", "/:"])
def test_fr29_uten_arbeidsgiver_er_filnavnet_bare_datoen(
    app, innlogget_client, arbeidsgiver, format_
):
    """FR-29/AD-11: uten arbeidsgiver i søknaden, eller når ingenting er igjen etter rensingen,
    har filen, linjen og vinduet filnavnet Soknad_<dato>."""
    brev = {"avsnitt": ["Hei."], "navn": "Kari"}
    soknad = Soknad(
        steg=Steg.BREV, modus=Modus.FULL_GENERERING, brev=brev, arbeidsgiver=arbeidsgiver
    )
    sett_soknad(app, innlogget_client, soknad)
    forventet = filnavn_i_dag(format_, None)
    assert re.fullmatch(rf"Soknad_\d{{4}}-\d{{2}}-\d{{2}}\.{format_}", forventet)
    svar = innlogget_client.get(ADRESSE[format_])
    assert svar.headers["Content-Disposition"] == f"attachment; filename={forventet}"
    html = html_av(innlogget_client.get("/brev"))
    assert filnavn_linje(html, format_) == tekster.filnavn_linje(forventet)
    assert vindu_filnavn(html) == tekster.filnavn_linje(filnavn_i_dag("docx", None))


def test_fr29_rare_tegn_i_arbeidsgiveren_renses_i_filnavnet(app, innlogget_client):
    """FR-29/AD-11: en arbeidsgiver med linjeskift, / og : gir et trygt filnavn i filen og på
    siden, og søknaden er uendret (bare filnavnet renses)."""
    brev = {"avsnitt": ["Hei."], "navn": "Kari"}
    soknad = Soknad(
        steg=Steg.BREV, modus=Modus.FULL_GENERERING, brev=brev, arbeidsgiver="Café/Bar: Ål\nAS"
    )
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.get(NEDLASTING)
    filnavn = svar.headers["Content-Disposition"].removeprefix("attachment; filename=")
    assert re.fullmatch(r"Soknad_CafeBar-Al-AS_\d{4}-\d{2}-\d{2}\.docx", filnavn)
    assert soknaden(app, innlogget_client).arbeidsgiver == "Café/Bar: Ål\nAS"
    html = html_av(innlogget_client.get("/brev"))
    assert filnavn_linje(html, "docx") == tekster.filnavn_linje(filnavn)
