"""Felles hjelpere for webtestene. Dette er ikke en testfil, så pytest samler den ikke inn,
og testfilene henter hjelperne herfra i stedet for fra hverandre."""

import re
from html.parser import HTMLParser
from pathlib import Path

from soknad.innstillinger import TESTBRUKER_EPOST, TESTBRUKER_PASSORD
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.okt import Innlogging
from soknad.web.innlogging import OKT_ID

WEB = Path(__file__).resolve().parents[2] / "soknad" / "web"
STIL = WEB / "static" / "css" / "stil.css"


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


def header(html):
    """Det som står i <header>."""
    return re.search(r"<header[^>]*>(.*?)</header>", html, re.S).group(1)


def main(html):
    """Det som står i <main>."""
    return re.search(r"<main[^>]*>(.*?)</main>", html, re.S).group(1)


def css_blokk(css, velger):
    """Innholdet i CSS-blokken som begynner med velger på starten av en linje."""
    return re.search(rf"^{re.escape(velger)}\s*\{{(.*?)\}}", css, re.S | re.M).group(1)


def felt(html, felt_id):
    """Attributtene til input-feltet med denne id-en."""
    return next(a for t, a in tagger_i(html) if t == "input" and a.get("id") == felt_id)


def med_autofocus(html):
    return [a.get("id") for _, a in tagger_i(html) if "autofocus" in a]


def logg_inn(client, epost=TESTBRUKER_EPOST, passord=TESTBRUKER_PASSORD):
    return client.post("/logg-inn", data={"epost": epost, "passord": passord})


def er_innlogget(client):
    return client.get("/").status_code == 200


def okt_id(client):
    """Økt-id-en i cookien, eller None."""
    with client.session_transaction() as okt:
        return okt.get(OKT_ID)


def soknaden(app, client):
    """Søknaden i øktlageret for denne klienten, eller None."""
    return app.extensions["oktlager"].hent_soknad(okt_id(client))


def sett_soknad(app, client, soknad):
    """Legger en søknad rett i øktlageret, for å teste et bestemt steg."""
    app.extensions["oktlager"].lagre_soknad(okt_id(client), soknad)


class FeilendeKI:
    """Samme testcaser og svar som TestKI, men oppgaven (nokkelord eller gap) gir
    KIFeil(feiltype). oppgave=None gir ingen feil. Hver oppgave som kalles, skrives i kalt.
    Settes inn med app.extensions["test_ki"]."""

    def __init__(self, test_ki, oppgave="nokkelord", feiltype=KIFeilType.ANNET, kalt=None):
        self.test_ki = test_ki
        self.caser = test_ki.caser
        self.oppgave = oppgave
        self.feiltype = feiltype
        self.kalt = [] if kalt is None else kalt

    def _kall(self, oppgave, *args):
        self.kalt.append(oppgave)
        if oppgave == self.oppgave:
            raise KIFeil(self.feiltype)
        return getattr(self.test_ki, oppgave)(*args)

    def nokkelord(self, annonse):
        return self._kall("nokkelord", annonse)

    def gap(self, cv, annonse):
        return self._kall("gap", cv, annonse)


def sett_testmodus(app, client, testmodus):
    """Bytter innloggingen til en med testmodus satt til testmodus, med øktlagerets egne
    metoder (slett og ny), og peker cookien på den nye økt-id-en. Testmodus kan ikke slås av
    på nettsiden før Epic 4."""
    lager = app.extensions["oktlager"]
    gammel = lager.hent(okt_id(client))
    lager.slett(okt_id(client))
    ny_id = lager.ny(Innlogging(gammel.bruker_id, testmodus=testmodus))
    with client.session_transaction() as okt:
        okt[OKT_ID] = ny_id
