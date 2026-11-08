"""Felles hjelpere for webtestene. Dette er ikke en testfil, så pytest samler den ikke inn,
og testfilene henter hjelperne herfra i stedet for fra hverandre."""

from html.parser import HTMLParser
from pathlib import Path

from soknad.innstillinger import TESTBRUKER_EPOST, TESTBRUKER_PASSORD
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
