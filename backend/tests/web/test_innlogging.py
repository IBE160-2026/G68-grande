"""Tester for innloggingssiden og login_required (FR-3, FR-4, FR-5, FR-6, FR-7, NFR-6)."""

import re
from html.parser import HTMLParser

import pytest

from soknad.adaptere.db import finn_bruker
from soknad.innstillinger import TESTBRUKER_EPOST, TESTBRUKER_PASSORD
from soknad.kjerne.feil import FeilType
from soknad.kjerne.okt import Innlogging
from soknad.web import ruter, tekster
from soknad.web.innlogging import OKT_ID


class Tagger(HTMLParser):
    """Samler alle starttagger med attributter."""

    def __init__(self):
        super().__init__()
        self.tagger = []

    def handle_starttag(self, tag, attrs):
        self.tagger.append((tag, dict(attrs)))


def tagger_i(html):
    leser = Tagger()
    leser.feed(html)
    return leser.tagger


def felt(html, felt_id):
    """Attributtene til input-feltet med denne id-en."""
    return next(a for t, a in tagger_i(html) if t == "input" and a.get("id") == felt_id)


def med_autofocus(html):
    return [a.get("id") for _, a in tagger_i(html) if "autofocus" in a]


def logg_inn(client, epost=TESTBRUKER_EPOST, passord=TESTBRUKER_PASSORD):
    return client.post("/logg-inn", data={"epost": epost, "passord": passord})


def er_innlogget(client):
    return client.get("/").status_code == 200


# --- Siden ---


def test_fr3_innloggingssiden_har_tittel_overskrift_felt_og_knapp(client):
    """FR-3: tittel, én h1 «Logg inn», feltene E-post og Passord og knappen «Logg inn»."""
    svar = client.get("/logg-inn")
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    tagger = tagger_i(html)
    navn = [tag for tag, _ in tagger]

    assert "<title>Logg inn – Søknadsassistenten</title>" in html
    assert navn.count("h1") == 1
    assert re.search(r"<h1[^>]*>\s*Logg inn\s*</h1>", html)
    assert re.search(r'<label for="epost">\s*E-post\s*</label>', html)
    assert re.search(r'<label for="passord">\s*Passord\s*</label>', html)
    assert felt(html, "epost")["autocomplete"] == "email"
    assert felt(html, "epost")["type"] == "email"
    assert felt(html, "passord")["autocomplete"] == "current-password"
    assert felt(html, "passord")["type"] == "password"
    assert re.search(r'<button[^>]*type="submit"[^>]*>\s*Logg inn\s*</button>', html)


def test_nfr6_skjemaet_har_novalidate_og_ingen_feil_eller_fokus_foer_innsending(client):
    """NFR-6: novalidate, landemerker, ingen feil, ingen autofocus, ingen role="alert"."""
    html = client.get("/logg-inn").get_data(as_text=True)
    tagger = tagger_i(html)
    skjema = next(a for t, a in tagger if t == "form")
    assert "novalidate" in skjema
    assert skjema["method"] == "post"
    assert ("html", {"lang": "nb"}) in tagger
    for landemerke in ("header", "main", "footer"):
        assert [t for t, _ in tagger].count(landemerke) == 1
    assert "aria-invalid" not in html
    assert "autofocus" not in html
    assert "role=" not in html
    assert "<script" not in html


def test_fr6_fr7_ingen_utlogging_ennaa(app, innlogget_client):
    """FR-6/FR-7: «Logg ut» og «Du må logge inn først» kommer i story 1.4."""
    html = app.test_client().get("/logg-inn").get_data(as_text=True)
    assert "Du må logge inn først" not in html
    assert "Logg ut" not in innlogget_client.get("/").get_data(as_text=True)


# --- Riktig innlogging ---


def test_fr3_fr5_riktig_innlogging_gir_startsiden(app, client):
    """FR-3/FR-5: testbrukeren fra README sendes til startsiden og ser «Velkommen! 👋»."""
    svar = logg_inn(client)
    assert svar.status_code == 302
    assert svar.location == "/"
    start = client.get("/")
    assert start.status_code == 200
    assert "Velkommen! 👋" in start.get_data(as_text=True)


def test_fr3_cookien_har_bare_okt_id_og_okten_ligger_i_minnet(app, client):
    """FR-3: cookien har bare økt-id-en, og Innlogging(bruker_id, testmodus=True) er i minnet."""
    with client.session_transaction() as okt:
        okt["noe_gammelt"] = "skal bort"
    logg_inn(client)
    with client.session_transaction() as okt:
        assert list(okt.keys()) == [OKT_ID]
        okt_id = okt[OKT_ID]
    innlogging = app.extensions["oktlager"].hent(okt_id)
    assert isinstance(innlogging, Innlogging)
    assert innlogging.bruker_id == finn_bruker(
        app.config["DATABASE"], TESTBRUKER_EPOST, TESTBRUKER_PASSORD
    )
    assert innlogging.testmodus is True


def test_fr3_ny_innlogging_gir_ny_okt_id_og_sletter_den_gamle(app, client):
    """FR-3: hver innlogging gir ny økt-id, og den gamle økten slettes fra minnet."""
    logg_inn(client)
    with client.session_transaction() as okt:
        gammel = okt[OKT_ID]
    logg_inn(client)
    with client.session_transaction() as okt:
        ny = okt[OKT_ID]
    assert ny != gammel
    assert app.extensions["oktlager"].hent(gammel) is None
    assert app.extensions["oktlager"].hent(ny) is not None


def test_fr3_epost_med_store_bokstaver_og_mellomrom_logger_inn(client):
    """FR-3: « Test@Example.com » med riktig passord logger inn."""
    svar = logg_inn(client, epost=" Test@Example.com ")
    assert svar.status_code == 302
    assert er_innlogget(client)


def test_fr3_alltid_til_startsiden_uten_next(client):
    """FR-3: etter innlogging alltid til startsiden; next= brukes ikke."""
    svar = client.post(
        "/logg-inn?next=/finnes-ikke",
        data={"epost": TESTBRUKER_EPOST, "passord": TESTBRUKER_PASSORD, "next": "/x"},
    )
    assert svar.location == "/"


# --- Feil innlogging ---


@pytest.mark.parametrize(
    ("epost", "passord"),
    [
        (TESTBRUKER_EPOST, "feilpassord"),
        ("ukjent@example.com", TESTBRUKER_PASSORD),
        (TESTBRUKER_EPOST, TESTBRUKER_PASSORD + " "),
    ],
)
def test_fr3_feil_passord_eller_ukjent_epost_gir_skjemafeil(client, epost, passord):
    """FR-3: «Feil e-post eller passord» i en boks med fokus, uten rød ramme, ikke innlogget."""
    svar = logg_inn(client, epost=epost, passord=passord)
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    boks = next(a for _, a in tagger_i(html) if a.get("id") == "skjemafeil")
    assert boks["tabindex"] == "-1"
    assert "autofocus" in boks
    assert "role" not in boks
    assert re.search(r'id="skjemafeil"[^>]*>\s*Feil e-post eller passord\s*<', html)
    assert med_autofocus(html) == ["skjemafeil"]
    assert "aria-invalid" not in html
    assert 'class="feiltekst"' not in html
    assert felt(html, "epost")["value"] == epost
    assert "value" not in felt(html, "passord")
    assert passord not in html
    assert not er_innlogget(client)


def test_fr3_eposten_som_vises_igjen_er_escapet(client):
    """FR-3: e-posten som skrives tilbake i value="…" etter feil innlogging, er escapet."""
    html = logg_inn(client, epost='"><script>x</script>', passord="feil").get_data(as_text=True)
    assert "<script>x</script>" not in html


# --- Tomme felt ---


def test_fr4_tomme_felt_gir_begge_feiltekstene_og_fokus_paa_epost(client, monkeypatch):
    """FR-4: begge tomme gir «Fyll inn e-post» og «Fyll inn passord», fokus på e-post,
    og databasen sjekkes ikke."""

    def ikke_kall(*args, **kwargs):
        raise AssertionError("databasen skal ikke sjekkes ved tomme felt")

    monkeypatch.setattr(ruter, "finn_bruker", ikke_kall)
    for epost in ("", "   "):
        svar = logg_inn(client, epost=epost, passord="")
        assert svar.status_code == 200
        html = svar.get_data(as_text=True)
        for navn, tekst in (("epost", "Fyll inn e-post"), ("passord", "Fyll inn passord")):
            attr = felt(html, navn)
            assert attr["aria-invalid"] == "true"
            assert attr["aria-describedby"] == f"{navn}-feil"
            assert re.search(rf'<p class="feiltekst" id="{navn}-feil">{tekst}</p>', html)
        assert med_autofocus(html) == ["epost"]
        assert "skjemafeil" not in html
        assert not er_innlogget(client)


def test_fr4_bare_tomt_passord_gir_fokus_paa_passord_og_beholder_eposten(client):
    """FR-4: bare passordet tomt: feil ved passord, fokus der, og e-posten står igjen."""
    html = logg_inn(client, epost="ola@example.com", passord="").get_data(as_text=True)
    assert "Fyll inn passord" in html
    assert "Fyll inn e-post" not in html
    assert "aria-invalid" not in felt(html, "epost")
    assert felt(html, "epost")["value"] == "ola@example.com"
    assert med_autofocus(html) == ["passord"]


def test_fr4_feiltekstene_ligger_i_tekster():
    """FR-3/FR-4: feiltekstene slås opp med (felt, type) i web/tekster.py."""
    assert tekster.FEILTEKSTER[("epost", FeilType.TOM)] == "Fyll inn e-post"
    assert tekster.FEILTEKSTER[("passord", FeilType.TOM)] == "Fyll inn passord"
    assert tekster.FEILTEKSTER[(None, FeilType.FEIL_INNLOGGING)] == "Feil e-post eller passord"


# --- Krever innlogging ---


def test_fr7_startsiden_uten_okt_sender_til_innloggingen(client):
    """FR-7: GET / uten økt gir 302 til /logg-inn."""
    svar = client.get("/")
    assert svar.status_code == 302
    assert svar.location == "/logg-inn"


def test_fr7_gammel_cookie_uten_okt_i_minnet_er_utlogget(app, client):
    """FR-7: en gyldig cookie med økt-id som ikke finnes i minnet (omstart) er utlogget."""
    logg_inn(client)
    with client.session_transaction() as okt:
        okt_id = okt[OKT_ID]
    app.extensions["oktlager"].slett(okt_id)
    svar = client.get("/")
    assert svar.status_code == 302
    assert svar.location == "/logg-inn"
    with client.session_transaction() as okt:
        assert OKT_ID not in okt
