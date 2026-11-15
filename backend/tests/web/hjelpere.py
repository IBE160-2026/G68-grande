"""Felles hjelpere for webtestene. Dette er ikke en testfil, så pytest samler den ikke inn,
og testfilene henter hjelperne herfra i stedet for fra hverandre. Felles fiksturer står i
conftest.py ved siden av."""

import json
import re
import shutil
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

from soknad import create_app
from soknad.adaptere.ki import TESTDATA_MAPPE, TestKI
from soknad.innstillinger import TESTBRUKER_EPOST, TESTBRUKER_PASSORD
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.filnavn import lag_filnavn
from soknad.kjerne.okt import Innlogging
from soknad.web.innlogging import OKT_ID

WEB = Path(__file__).resolve().parents[2] / "soknad" / "web"
STIL = WEB / "static" / "css" / "stil.css"

# Testdataene fra case 1, som de fleste testene av flyten bruker.
CASE = TESTDATA_MAPPE / "case-1-utvikler"
CV = (CASE / "cv.txt").read_text(encoding="utf-8")
ANNONSE = (CASE / "annonse.txt").read_text(encoding="utf-8")
# Det fiktive brevet til Korrektur, bare i case 1 (story 5.1).
EGET_BREV = (CASE / "eget-brev.txt").read_text(encoding="utf-8")
NOKKELORD_SVAR = json.loads((CASE / "ki-svar" / "nokkelord.json").read_text(encoding="utf-8"))
GAP_SVAR = json.loads((CASE / "ki-svar" / "gap.json").read_text(encoding="utf-8"))

# Adressen til nedlastingen av brevet som Word.
NEDLASTING = "/last-ned/docx"

# Linjene med tekst i det egne brevet. Hver linje er ett avsnitt (eller hilsen og navn).
_LINJER = [linje for linje in EGET_BREV.splitlines() if linje.strip()]
KORREKTUR_OVERSKRIFT = "Søknad på stillingen som junior utvikler"


def korrektur_svar(forslag=1):
    """Et gyldig svar fra Korrektur for det egne brevet i case 1, til testene av flyten (story
    5.2.1): overskriften er rettet, «Hei!» er fjernet, og resten er uendret, én linje per
    oppføring. I forslag 2 er også den første setningen etter tiltalen endret. De ekte
    svarene (korrektur-1.json og korrektur-2.json) lages med skriptet."""
    assert _LINJER[:2] == ["Søknad på jobb som junior utvikler", "Hei!"]
    setninger = [
        {"ny": KORREKTUR_OVERSKRIFT, "gammel": [_LINJER[0]], "nytt_avsnitt": True},
        {"ny": None, "gammel": [_LINJER[1]], "nytt_avsnitt": True},
        *({"ny": linje, "gammel": [linje], "nytt_avsnitt": True} for linje in _LINJER[2:]),
    ]
    if forslag % 2 == 0:
        setninger[2] = {**setninger[2], "ny": "Forslag to."}
    return {"setninger": setninger}


def korrektur_brev(forslag=1):
    """Brevet som skal vises og lastes ned for korrektur_svar(forslag): overskriften, så resten
    av linjene uten «Hei!». Hilsenen og navnet er de brukeren skrev, og ingenting er lagt til."""
    resten = _LINJER[2:] if forslag % 2 else ["Forslag to.", *_LINJER[3:]]
    return [KORREKTUR_OVERSKRIFT, *resten]


def korrektur_testki(mappe, svar1=None):
    """En TestKI med en kopi av testdata/ i mappe, der case 1 har korrektur-1.json (svar1,
    eller korrektur_svar(1)) og korrektur-2.json (korrektur_svar(2)). svar1 kan også være
    tekst, for et ødelagt svar."""
    kopi = mappe / "testdata"
    shutil.copytree(TESTDATA_MAPPE, kopi)
    svar = kopi / CASE.name / "ki-svar"
    forste = korrektur_svar(1) if svar1 is None else svar1
    for navn, innhold in (("korrektur-1", forste), ("korrektur-2", korrektur_svar(2))):
        tekst = innhold if isinstance(innhold, str) else json.dumps(innhold, ensure_ascii=False)
        (svar / f"{navn}.json").write_text(tekst, encoding="utf-8")
    return TestKI(kopi)


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


class Brevtekst(HTMLParser):
    """Samler teksten i hvert <p> i brevarket slik den står på skjermen, uten de skjulte
    tekstene (.skjult) og uten «Du skrev» (.du-skrev) i Korrektur (story 5.3). Teksten er
    unescapet."""

    _HOPP_OVER = {"skjult", "du-skrev"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.avsnitt = []
        self._i_ark = False
        self._i_p = False
        # Antall åpne <span> inne i en span som hoppes over (0 = teksten tas med).
        self._hopp = 0

    def handle_starttag(self, tag, attrs):
        klasser = set((dict(attrs).get("class") or "").split())
        if tag == "article" and "brevark" in klasser:
            self._i_ark = True
        elif self._i_ark and tag == "p":
            self._i_p = True
            self.avsnitt.append("")
        elif self._i_p and tag == "span" and (self._hopp or klasser & self._HOPP_OVER):
            self._hopp += 1

    def handle_endtag(self, tag):
        if tag == "article":
            self._i_ark = False
        elif tag == "p":
            self._i_p = False
        elif tag == "span" and self._hopp:
            self._hopp -= 1

    def handle_data(self, data):
        if self._i_p and not self._hopp:
            self.avsnitt[-1] += data


def brevtekst(html):
    """Teksten i hvert avsnitt i brevarket, uten de skjulte tekstene og «Du skrev»."""
    leser = Brevtekst()
    leser.feed(html)
    return leser.avsnitt


def html_av(svar):
    """Svaret som tekst."""
    return svar.get_data(as_text=True)


def element(html, id_):
    """Attributtene til elementet med denne id-en."""
    return next(a for _, a in tagger_i(html) if a.get("id") == id_)


def header(html):
    """Det som står i <header>."""
    return re.search(r"<header[^>]*>(.*?)</header>", html, re.S).group(1)


def main(html):
    """Det som står i <main>."""
    return re.search(r"<main[^>]*>(.*?)</main>", html, re.S).group(1)


def footer(html):
    """Det som står i <footer> (hjørneraden)."""
    return re.search(r"<footer[^>]*>(.*?)</footer>", html, re.S).group(1)


def css_blokk(css, velger):
    """Innholdet i CSS-blokken som begynner med velger på starten av en linje."""
    return re.search(rf"^{re.escape(velger)}\s*\{{(.*?)\}}", css, re.S | re.M).group(1)


def felt(html, felt_id):
    """Attributtene til input-feltet med denne id-en."""
    return next(a for t, a in tagger_i(html) if t == "input" and a.get("id") == felt_id)


def med_autofocus(html):
    return [a.get("id") for _, a in tagger_i(html) if "autofocus" in a]


def filnavn_i_dag():
    """Filnavnet Word-filen får i dag."""
    return lag_filnavn(date.today(), "docx")


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
    """Samme testcaser og svar som TestKI, men oppgaven (nokkelord, gap, brev eller korrektur) gir
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

    def brev(self, cv, annonse, forslag):
        return self._kall("brev", cv, annonse, forslag)

    def korrektur(self, cv, annonse, eget_brev, forslag):
        return self._kall("korrektur", cv, annonse, eget_brev, forslag)


def sett_testmodus(app, client, testmodus):
    """Bytter innloggingen til en med testmodus satt til testmodus, på samme økt-id og med
    søknaden beholdt (Oktlager.bytt_innlogging). Brukes i apper uten API-nøkkel, der bryteren
    på nettsiden er låst på."""
    lager = app.extensions["oktlager"]
    gammel = lager.hent(okt_id(client))
    assert lager.bytt_innlogging(okt_id(client), Innlogging(gammel.bruker_id, testmodus))


def app_med_nokkel(nokkel="sk-test"):
    """En app der ANTHROPIC_API_KEY er satt til nokkel. EkteKI kobler ikke til nettet før det
    første kallet, og testene bytter den ut med TellendeKI før noe kalles."""
    return create_app({"TESTING": True, "SECRET_KEY": "test-nokkel", "ANTHROPIC_API_KEY": nokkel})


class TellendeKI:
    """En falsk KI som skriver hver oppgave i kalt og svarer med de ferdige svarene fra TestKI.
    Settes inn med app.extensions["ekte_ki"] (eller "test_ki"), så testene ser hvilken KI som
    ble kalt, uten nettverk."""

    def __init__(self, test_ki, kalt=None):
        self.test_ki = test_ki
        self.caser = test_ki.caser
        self.kalt = [] if kalt is None else kalt

    def nokkelord(self, annonse):
        self.kalt.append("nokkelord")
        return self.test_ki.nokkelord(annonse)

    def gap(self, cv, annonse):
        self.kalt.append("gap")
        return self.test_ki.gap(cv, annonse)

    def brev(self, cv, annonse, forslag):
        self.kalt.append("brev")
        return self.test_ki.brev(cv, annonse, forslag)

    def korrektur(self, cv, annonse, eget_brev, forslag):
        self.kalt.append("korrektur")
        return self.test_ki.korrektur(cv, annonse, eget_brev, forslag)
