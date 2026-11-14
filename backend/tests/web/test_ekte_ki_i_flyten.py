"""Tester av hele flyten med EkteKI og kontroller sammen (FR-32, FR-36, NFR-11, FR-28, AD-3,
AD-13). EkteKI har en ekte Anthropic-klient med httpx2.MockTransport (tests/falsk_api.py),
så rutene, EkteKI, SDK-et og kontroller testes samlet. Ingen test går mot nettet, og ingen
bruker en ekte API-nøkkel."""

import re

from soknad.adaptere.ki import EkteKI
from tests.falsk_api import klient_med_svar, oppgave_i
from tests.web.hjelpere import (
    ANNONSE,
    CV,
    TellendeKI,
    app_med_nokkel,
    html_av,
    logg_inn,
    main,
)

# Svarene fra den falske transporten. De er ikke like svarene i testmodus, så siden viser at
# svarene kom gjennom EkteKI. Nøkkelordene står ikke i CV-en, annonsen eller gap-svaret, så de
# vises bare hvis nøkkelordsvaret vises. De tomme punktene og linjeskiftet viser at
# kontroller() er brukt: punktene fjernes, og linjeskiftet blir et mellomrom.
NOKKELORD = ["Zorbulator", "Kvasarmodul"]
SVAR = {
    "nokkelord": {"nokkelord": [*NOKKELORD, " "], "arbeidsgiver": "Testvik AS"},
    "gap": {"dekker": ["Dekket fra falsk API"], "mangler": ["Mangler fra falsk API", ""]},
    "brev": {"avsnitt": ["Første avsnitt\nfra falsk API.", "Med vennlig hilsen", "Sara"]},
}


def app_med_falsk_api(svar, sendt):
    """(app, klient): innlogget i en app med nøkkel, der EkteKI har den falske transporten med
    svar. Testmodus er av."""
    app = app_med_nokkel()
    app.extensions["ekte_ki"] = EkteKI(
        "sk-test", app.config["ANTHROPIC_MODEL"], klient=klient_med_svar(svar, sendt)
    )
    client = app.test_client()
    assert logg_inn(client).status_code == 302
    return app, client


def til_resultatsiden(client):
    """Samtykke, Full generering og «Sjekk CV-en min» med testdataene fra case 1."""
    client.get("/")
    assert client.post("/", data={"samtykke": "ja"}).location == "/modus"
    assert client.post("/modus", data={"modus": "full_generering"}).location == "/innlegging"
    svar = client.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
    assert svar.location == "/resultat"


def test_fr32_hele_flyten_med_ekte_ki_gjennom_sdk_et():
    """FR-32/FR-36/NFR-11/FR-28/AD-3: med nøkkel, testmodus av og samtykke går «Sjekk CV-en
    min» og «Lag søknadsbrevet mitt» gjennom EkteKI, SDK-et og kontroller. Resultatsiden viser
    nøkkelordene og gap-svaret, brevsiden viser avsnittene, og tre forespørsler er sendt
    (nokkelord, gap og brev). TestKI kalles ikke."""
    sendt = []
    app, client = app_med_falsk_api(SVAR, sendt)
    test_kalt = []
    app.extensions["test_ki"] = TellendeKI(app.extensions["test_ki"], kalt=test_kalt)
    til_resultatsiden(client)

    for ord_ in NOKKELORD:
        assert ord_ not in CV + ANNONSE + str(SVAR["gap"]), ord_
    resultat = main(html_av(client.get("/resultat")))
    for tekst in (*NOKKELORD, "Dekket fra falsk API", "Mangler fra falsk API"):
        assert tekst in resultat, tekst
    # Ingen tomme punkter i listene (punktikonet og så ingenting).
    assert re.search(r"</span>\s*</li>", resultat) is None

    assert client.post("/resultat", data={"handling": "brev"}).location == "/brev"
    brev = main(html_av(client.get("/brev")))
    for tekst in (
        "<p>Første avsnitt fra falsk API.</p>",
        "<p>Med vennlig hilsen</p>",
        "<p>Sara</p>",
    ):
        assert tekst in brev, tekst

    assert [oppgave_i(foresporsel["json"]) for foresporsel in sendt] == ["nokkelord", "gap", "brev"]
    assert {foresporsel["json"]["model"] for foresporsel in sendt} == {
        app.config["ANTHROPIC_MODEL"]
    }
    assert test_kalt == []


def test_fr28_enslig_surrogat_i_gap_svaret_gir_resultatsiden():
    """FR-28: et gap-svar fra KI-en med en enslig surrogat (\\ud800 i JSON-en) gir resultatsiden
    (200) uten surrogaten, ikke en feilside. Et punkt med bare surrogaten vises ikke."""
    svar = {
        **SVAR,
        "gap": {"dekker": ["Dekket\ud800 fra falsk API", "\ud800"], "mangler": ["Mangler"]},
    }
    _, client = app_med_falsk_api(svar, [])
    til_resultatsiden(client)

    side = client.get("/resultat")
    assert side.status_code == 200
    resultat = main(html_av(side))
    assert "Dekket fra falsk API" in resultat
    assert re.search(r"</span>\s*</li>", resultat) is None
