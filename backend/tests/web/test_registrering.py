"""Tester for registreringen og lenkene mellom innlogging og registrering
(FR-1, FR-2, FR-3, FR-4, FR-5, FR-7, NFR-1, NFR-6)."""

import re
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from soknad.adaptere.db import finn_bruker
from soknad.innstillinger import TESTBRUKER_EPOST
from soknad.kjerne.feil import FeilType
from soknad.kjerne.okt import Innlogging
from soknad.web import ruter, tekster
from soknad.web.innlogging import OKT_ID
from tests.web.hjelpere import STIL, er_innlogget, felt, logg_inn, med_autofocus, okt_id, tagger_i


def registrer(client, epost="ola@x.no", passord="passord12", gjenta="passord12"):
    return client.post("/registrer", data={"epost": epost, "passord": passord, "gjenta": gjenta})


def antall_brukere(app):
    with closing(sqlite3.connect(app.config["DATABASE"])) as db:
        return db.execute("SELECT COUNT(*) FROM brukere").fetchone()[0]


def feiltekst_ved(html, navn):
    """Feilteksten under feltet, eller None."""
    treff = re.search(rf'<p class="feiltekst" id="{navn}-feil">([^<]*)</p>', html)
    return treff.group(1) if treff else None


@pytest.fixture
def ingen_databasesjekk(monkeypatch):
    def ikke_kall(*args, **kwargs):
        raise AssertionError("databasen skal ikke sjekkes")

    monkeypatch.setattr(ruter, "epost_finnes", ikke_kall)
    monkeypatch.setattr(ruter, "lag_bruker", ikke_kall)


# --- Siden ---


def test_fr1_registreringen_har_tittel_overskrift_felt_og_knapp(client):
    """FR-1: tittel, én h1 «Registrer deg», tre felt med etiketter, autocomplete og knapp."""
    svar = client.get("/registrer")
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    navn = [tag for tag, _ in tagger_i(html)]

    assert "<title>Registrer deg – Søknadsassistenten</title>" in html
    assert navn.count("h1") == 1
    assert re.search(r"<h1[^>]*>\s*Registrer deg\s*</h1>", html)
    for felt_id, etikett in (
        ("epost", "E-post"),
        ("passord", "Passord"),
        ("gjenta", "Gjenta passord"),
    ):
        assert re.search(rf'<label for="{felt_id}">\s*{etikett}\s*</label>', html)
        assert felt(html, felt_id)["name"] == felt_id
    assert felt(html, "epost")["type"] == "email"
    assert felt(html, "epost")["autocomplete"] == "email"
    for felt_id in ("passord", "gjenta"):
        assert felt(html, felt_id)["type"] == "password"
        assert felt(html, felt_id)["autocomplete"] == "new-password"
    assert re.search(r'<button[^>]*type="submit"[^>]*>\s*Registrer deg\s*</button>', html)


def test_nfr6_registreringen_uten_feil_eller_fokus_foer_innsending(client):
    """NFR-6: novalidate, «Minst 8 tegn» koblet til passordet, ingen feil, fokus eller skript."""
    html = client.get("/registrer").get_data(as_text=True)
    skjema = next(a for t, a in tagger_i(html) if t == "form")
    assert "novalidate" in skjema
    assert skjema["method"] == "post"
    assert skjema["action"] == "/registrer"
    assert re.search(r'<p class="hjelpetekst" id="passord-hjelp">Minst 8 tegn</p>', html)
    assert felt(html, "passord")["aria-describedby"] == "passord-hjelp"
    assert "aria-describedby" not in felt(html, "epost")
    assert "aria-describedby" not in felt(html, "gjenta")
    assert "aria-invalid" not in html
    assert "autofocus" not in html
    assert 'class="feiltekst"' not in html
    assert "role=" not in html
    assert "<script" not in html


def test_fr7_registreringen_krever_ikke_innlogging(client):
    """FR-7: registreringen kan brukes uten å være logget inn."""
    assert client.get("/registrer").status_code == 200
    assert registrer(client).status_code == 302


def test_fr1_tekstene_ligger_i_tekster():
    """FR-1/FR-2/FR-4: tekstene for registreringen ligger i web/tekster.py."""
    assert tekster.REGISTRER_TITTEL == "Registrer deg"
    assert tekster.REGISTRER_OVERSKRIFT == "Registrer deg"
    assert tekster.REGISTRER_KNAPP == "Registrer deg"
    assert tekster.FELT_GJENTA == "Gjenta passord"
    assert tekster.PASSORD_HJELP == "Minst 8 tegn"
    f = tekster.FEILTEKSTER
    assert f[("epost", FeilType.TOM)] == "Fyll inn e-post"
    assert f[("epost", FeilType.EPOST_UGYLDIG)] == "E-posten er ikke gyldig"
    assert f[("epost", FeilType.EPOST_FINNES)] == "Denne e-posten er allerede registrert"
    assert f[("passord", FeilType.TOM)] == "Fyll inn passord"
    assert f[("passord", FeilType.PASSORD_KORT)] == "Passordet må ha minst 8 tegn"
    assert f[("gjenta", FeilType.TOM)] == "Gjenta passordet"
    assert f[("gjenta", FeilType.PASSORD_ULIKE)] == "Passordene er ikke like"


# --- Lenkene begge veier ---


def test_fr1_innloggingen_lenker_til_registreringen(client):
    """FR-1: «Ny her? Registrer deg her» under innloggingsskjemaet, lenke på «Registrer deg her»."""
    html = client.get("/logg-inn").get_data(as_text=True)
    assert re.search(
        r'<p class="lenkerad">Ny her\?\s*<a href="/registrer">Registrer deg her</a></p>', html
    )
    assert html.index("</button>") < html.index('class="lenkerad"') < html.index("</form>")


def test_fr3_registreringen_lenker_til_innloggingen(client):
    """FR-3: «Har du allerede en bruker? Logg inn» under registreringen, lenke på «Logg inn»."""
    html = client.get("/registrer").get_data(as_text=True)
    assert re.search(
        r'<p class="lenkerad">Har du allerede en bruker\?\s*<a href="/logg-inn">Logg inn</a></p>',
        html,
    )
    assert html.index("</button>") < html.index('class="lenkerad"') < html.index("</form>")


def test_nfr6_hjelpetekst_og_lenker_i_stilen():
    """NFR-6: hjelpeteksten er dempet og liten, og lenkene er understreket i primary."""
    css = STIL.read_text(encoding="utf-8")
    hjelp = re.search(r"\.hjelpetekst\s*\{(.*?)\}", css, re.S).group(1)
    assert "var(--text-muted)" in hjelp
    assert "var(--size-small)" in hjelp
    rad = re.search(r"\.lenkerad\s*\{(.*?)\}", css, re.S).group(1)
    assert "text-align: center" in rad
    lenke = re.search(r"\.lenkerad a\s*\{(.*?)\}", css, re.S).group(1)
    assert "color: var(--primary)" in lenke
    assert "text-decoration: underline" in lenke
    assert "font-weight: 600" in lenke


# --- Riktig registrering ---


def test_fr1_fr5_riktig_registrering_lagrer_og_gir_startsiden(app, client):
    """FR-1/FR-5: riktig utfylt gir 302 til /, en ny rad med hash, og brukeren er innlogget."""
    for_registrering = antall_brukere(app)
    svar = registrer(client)
    assert svar.status_code == 302
    assert svar.location == "/"
    assert antall_brukere(app) == for_registrering + 1
    start = client.get("/")
    assert start.status_code == 200
    assert "Velkommen! 👋" in start.get_data(as_text=True)


def test_nfr1_passordet_lagres_bare_som_hash(app, client):
    """NFR-1: passordet til den nye brukeren står aldri i klartekst i databasefilen."""
    registrer(client)
    assert b"passord12" not in Path(app.config["DATABASE"]).read_bytes()


def test_fr1_auto_innlogging_gir_ny_okt_id_med_den_nye_brukeren(app, client):
    """FR-1: registreringen logger inn den nye brukeren med ny økt-id og testmodus=True,
    også fra en gammel cookie (økten er ikke i minnet etter omstart)."""
    logg_inn(client)
    gammel = okt_id(client)
    app.extensions["oktlager"].slett(gammel)
    registrer(client)
    with client.session_transaction() as okt:
        assert list(okt.keys()) == [OKT_ID]
        ny = okt[OKT_ID]
    lager = app.extensions["oktlager"]
    assert ny != gammel
    ny_id = finn_bruker(app.config["DATABASE"], "ola@x.no", "passord12")
    assert ny_id is not None
    assert lager.hent(ny) == Innlogging(ny_id, testmodus=True)


def test_fr1_fr3_ny_bruker_kan_logge_inn_senere_med_andre_bokstaver(app):
    """FR-1/FR-3: den nye brukeren kan senere logge inn med e-post i andre bokstaver."""
    registrer(app.test_client(), epost=" Ola@X.no ")
    client = app.test_client()
    svar = client.post("/logg-inn", data={"epost": "OLA@x.NO", "passord": "passord12"})
    assert svar.status_code == 302
    assert er_innlogget(client)


# --- Feil ---


@pytest.mark.parametrize("epost", [" Ola@X.no ", "ola@x.no"])
def test_fr2_epost_som_finnes_gir_feil_og_ingen_ny_rad(app, client, epost):
    """FR-2: e-post som finnes (sammenlignet normalisert) gir feil ved e-post og ingen ny rad."""
    registrer(app.test_client())
    for_forsok = antall_brukere(app)
    svar = registrer(client, epost=epost, passord="annetpassord", gjenta="annetpassord")
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    assert feiltekst_ved(html, "epost") == "Denne e-posten er allerede registrert"
    assert felt(html, "epost")["aria-invalid"] == "true"
    assert felt(html, "epost")["value"] == epost
    assert med_autofocus(html) == ["epost"]
    assert antall_brukere(app) == for_forsok
    assert not er_innlogget(client)


def test_fr2_testbrukeren_finnes_fra_for(app, client):
    """FR-2: testbrukerens e-post gir samme feil og ingen ny rad."""
    for_forsok = antall_brukere(app)
    html = registrer(client, epost=TESTBRUKER_EPOST).get_data(as_text=True)
    assert feiltekst_ved(html, "epost") == "Denne e-posten er allerede registrert"
    assert antall_brukere(app) == for_forsok


def test_fr4_alt_tomt_gir_tre_feil_og_fokus_paa_epost(app, client, ingen_databasesjekk):
    """FR-4: tre tomme felt gir tre feiltekster samtidig, fokus på e-post, ingen databasesjekk."""
    svar = registrer(client, epost="", passord="", gjenta="")
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    assert feiltekst_ved(html, "epost") == "Fyll inn e-post"
    assert feiltekst_ved(html, "passord") == "Fyll inn passord"
    assert feiltekst_ved(html, "gjenta") == "Gjenta passordet"
    for navn in ("epost", "passord", "gjenta"):
        assert felt(html, navn)["aria-invalid"] == "true"
    assert felt(html, "epost")["aria-describedby"] == "epost-feil"
    assert felt(html, "passord")["aria-describedby"] == "passord-hjelp passord-feil"
    assert felt(html, "gjenta")["aria-describedby"] == "gjenta-feil"
    assert "Minst 8 tegn" in html
    assert med_autofocus(html) == ["epost"]
    assert not er_innlogget(client)


def test_fr1_ugyldig_epost_gir_feil_uten_databasesjekk(client, ingen_databasesjekk):
    """FR-1: «ola@» gir «E-posten er ikke gyldig», og databasen sjekkes ikke for e-posten."""
    html = registrer(client, epost="ola@").get_data(as_text=True)
    assert feiltekst_ved(html, "epost") == "E-posten er ikke gyldig"
    assert feiltekst_ved(html, "passord") is None
    assert feiltekst_ved(html, "gjenta") is None
    assert felt(html, "epost")["value"] == "ola@"
    assert med_autofocus(html) == ["epost"]


def test_fr1_for_kort_passord_gir_feil_og_fokus_paa_passord(app, client):
    """FR-1: 7 like tegn gir «Passordet må ha minst 8 tegn», fokus på passord, ikke lagret."""
    for_forsok = antall_brukere(app)
    html = registrer(client, passord="1234567", gjenta="1234567").get_data(as_text=True)
    assert feiltekst_ved(html, "passord") == "Passordet må ha minst 8 tegn"
    assert felt(html, "passord")["aria-describedby"] == "passord-hjelp passord-feil"
    assert feiltekst_ved(html, "gjenta") is None
    assert "aria-invalid" not in felt(html, "epost")
    assert felt(html, "epost")["value"] == "ola@x.no"
    assert med_autofocus(html) == ["passord"]
    assert antall_brukere(app) == for_forsok
    assert not er_innlogget(client)


def test_fr1_ulike_passord_gir_feil_ved_gjenta(app, client):
    """FR-1: «passord12» / «passord13» gir «Passordene er ikke like» ved gjenta, ikke lagret."""
    for_forsok = antall_brukere(app)
    html = registrer(client, passord="passord12", gjenta="passord13").get_data(as_text=True)
    assert feiltekst_ved(html, "gjenta") == "Passordene er ikke like"
    assert feiltekst_ved(html, "passord") is None
    assert felt(html, "gjenta")["aria-invalid"] == "true"
    assert med_autofocus(html) == ["gjenta"]
    assert antall_brukere(app) == for_forsok


def test_fr1_fr2_flere_feil_vises_samtidig(app, client):
    """FR-1/FR-2/FR-4: e-post som finnes, kort passord og ulike passord gir alle tre feilene."""
    for_forsok = antall_brukere(app)
    html = registrer(client, epost=TESTBRUKER_EPOST, passord="kort", gjenta="annet").get_data(
        as_text=True
    )
    assert feiltekst_ved(html, "epost") == "Denne e-posten er allerede registrert"
    assert feiltekst_ved(html, "passord") == "Passordet må ha minst 8 tegn"
    assert feiltekst_ved(html, "gjenta") == "Passordene er ikke like"
    assert med_autofocus(html) == ["epost"]
    assert antall_brukere(app) == for_forsok


def test_fr1_tomt_passord_og_fylt_gjenta_gir_bare_tom_ved_passord(app, client):
    """FR-1/FR-4: passord tomt og gjenta fylt gir bare «Fyll inn passord»."""
    html = registrer(client, passord="", gjenta="passord12").get_data(as_text=True)
    assert feiltekst_ved(html, "passord") == "Fyll inn passord"
    assert feiltekst_ved(html, "gjenta") is None
    assert feiltekst_ved(html, "epost") is None
    assert med_autofocus(html) == ["passord"]


def test_fr2_eposten_kom_inn_i_mellomtiden(app, client, monkeypatch):
    """FR-2: gir lag_bruker None (e-posten kom inn i mellomtiden), vises «finnes»-feilen."""
    monkeypatch.setattr(ruter, "epost_finnes", lambda *args: False)
    monkeypatch.setattr(ruter, "lag_bruker", lambda *args: None)
    svar = registrer(client)
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    assert feiltekst_ved(html, "epost") == "Denne e-posten er allerede registrert"
    assert med_autofocus(html) == ["epost"]
    assert not er_innlogget(client)


@pytest.mark.parametrize(
    "data",
    [
        {"epost": "", "passord": "hemmelig1", "gjenta": "hemmelig2"},
        {"epost": "ola@", "passord": "hemmelig1", "gjenta": "hemmelig1"},
        {"epost": TESTBRUKER_EPOST, "passord": "hemmelig1", "gjenta": "hemmelig1"},
    ],
)
def test_fr1_passordene_vises_aldri_igjen(client, data):
    """FR-1: ved feil står e-posten igjen, men passordene aldri."""
    html = client.post("/registrer", data=data).get_data(as_text=True)
    assert "hemmelig" not in html
    assert "value" not in felt(html, "passord")
    assert "value" not in felt(html, "gjenta")


def test_fr1_eposten_som_vises_igjen_er_escapet(client):
    """FR-1: e-posten som skrives tilbake i value="…" etter feil, er escapet."""
    html = registrer(client, epost='"><script>x</script>').get_data(as_text=True)
    assert felt(html, "epost")["value"] == '"><script>x</script>'
    assert "<script" not in html


# --- Alt innlogget ---


def test_fr1_innlogget_paa_registreringen_gir_startsiden(app, innlogget_client):
    """FR-1/FR-5: den som alt er logget inn og åpner registreringen, sendes til startsiden,
    og økten er uendret."""
    for_svar = okt_id(innlogget_client)
    svar = innlogget_client.get("/registrer")
    assert svar.status_code == 302
    assert svar.location == "/"
    assert okt_id(innlogget_client) == for_svar
    assert app.extensions["oktlager"].hent(for_svar) is not None


def test_fr1_innlogget_som_sender_registrering_lagrer_ingenting(
    app, innlogget_client, ingen_databasesjekk, monkeypatch
):
    """FR-1: sender den innloggede en registrering med ny e-post, sendes hun til startsiden
    uten at noe sjekkes eller lagres, og økten og brukeren er de samme."""

    def ikke_kall(*args, **kwargs):
        raise AssertionError("ingenting skal sjekkes når man alt er logget inn")

    monkeypatch.setattr(ruter, "sjekk_registrering", ikke_kall)
    lager = app.extensions["oktlager"]
    for_svar = okt_id(innlogget_client)
    bruker_for = lager.hent(for_svar)
    for_forsok = antall_brukere(app)
    svar = registrer(innlogget_client, epost="ny@x.no")
    assert svar.status_code == 302
    assert svar.location == "/"
    assert antall_brukere(app) == for_forsok
    assert okt_id(innlogget_client) == for_svar
    assert lager.hent(for_svar) == bruker_for
