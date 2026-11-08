"""Tester for startsiden, base.html og stilen (NFR-6, NFR-7, NFR-8, UX-DR1).
Startsiden krever innlogging, så testene logger inn med testbrukeren først."""

import re
from html.parser import HTMLParser
from pathlib import Path

from soknad.web import tekster

WEB = Path(__file__).resolve().parents[2] / "soknad" / "web"
STIL = WEB / "static" / "css" / "stil.css"
MALER = sorted((WEB / "templates").glob("*.html"))


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


def test_nfr8_startsiden_svarer_200(innlogget_client):
    """NFR-8: startsiden virker på en ny kopi (etter innlogging med testbrukeren)."""
    svar = innlogget_client.get("/")
    assert svar.status_code == 200
    assert svar.mimetype == "text/html"


def test_nfr6_startsiden_har_lang_tittel_og_landemerker(innlogget_client):
    """NFR-6: lang="nb", egen sidetittel, header/main/footer og nøyaktig én h1."""
    html = innlogget_client.get("/").get_data(as_text=True)
    tagger = tagger_i(html)
    navn = [tag for tag, _ in tagger]

    assert ("html", {"lang": "nb"}) in tagger
    assert "<title>Startside – Søknadsassistenten</title>" in html
    for landemerke in ("header", "main", "footer"):
        assert navn.count(landemerke) == 1, landemerke
    assert navn.count("h1") == 1


def test_nfr6_logoen_er_ikke_en_overskrift(innlogget_client):
    """NFR-6: logoen står i header, men er ikke en overskrift."""
    html = innlogget_client.get("/").get_data(as_text=True)
    header = re.search(r"<header[^>]*>(.*?)</header>", html, re.S).group(1)
    assert tekster.LOGO == "Søknadsassistenten"
    assert tekster.LOGO in header
    assert not re.search(r"<h[1-6]", header)


def test_nfr8_startsiden_viser_velkomst_og_ingress(innlogget_client):
    """NFR-8: startsiden viser «Velkommen! 👋» som h1 og ingressen fra tekster.py."""
    html = innlogget_client.get("/").get_data(as_text=True)
    assert re.search(r"<h1[^>]*>\s*Velkommen! 👋\s*</h1>", html)
    assert tekster.START_INGRESS == (
        "Her lager du et søknadsbrev som passer til stillingen du vil søke på."
    )
    assert tekster.START_INGRESS in html


def test_nfr8_ukjent_side_gir_404(client):
    """NFR-8: en side som ikke finnes, gir Flasks vanlige 404."""
    assert client.get("/finnes-ikke").status_code == 404


def test_nfr6_ingenting_hentes_utenfra(app, innlogget_client):
    """NFR-6: ingen Google Fonts eller andre nettadresser på sidene eller i stilen."""
    innlogging = app.test_client().get("/logg-inn").get_data(as_text=True)
    html = innlogget_client.get("/").get_data(as_text=True)
    css = STIL.read_text(encoding="utf-8")
    for side in (innlogging, html):
        assert "<script" not in side
    for innhold in (innlogging, html, css):
        assert "fonts.googleapis" not in innhold
        assert "fonts.gstatic" not in innhold
        assert not re.search(r"(?:src|href|srcset)\s*=\s*[\"']?(?:https?:)?//", innhold)
        assert not re.search(r"url\(\s*[\"']?(?:https?:)?//", innhold)
        assert not re.search(r"@import\s+(?:url\(\s*)?[\"']?(?:https?:)?//", innhold)


def test_nfr8_stil_og_skrift_lastes_lokalt(innlogget_client):
    """NFR-8: stilen og Baloo 2-filen ligger i prosjektet og kan lastes."""
    html = innlogget_client.get("/").get_data(as_text=True)
    assert "/static/css/stil.css" in html
    assert innlogget_client.get("/static/css/stil.css").status_code == 200
    skrift = innlogget_client.get("/static/fonts/Baloo2-ExtraBold.woff2")
    assert skrift.status_code == 200
    assert skrift.data[:4] == b"wOF2"
    assert (WEB / "static" / "fonts" / "OFL.txt").is_file()


def test_nfr7_logoen_bruker_baloo2_med_clamp_uten_nowrap():
    """NFR-7: logoen i Baloo 2 (800) med clamp, uten nowrap og uten faste høyder."""
    css = STIL.read_text(encoding="utf-8")
    assert "--size-logo: clamp(1.35rem, 5vw, 2.4rem);" in css
    logo = re.search(r"\.logo\s*\{(.*?)\}", css, re.S).group(1)
    assert "var(--font-logo)" in logo
    assert "font-weight: 800" in logo
    assert "var(--size-logo)" in logo
    assert "text-align: center" in logo
    assert "nowrap" not in css
    assert not re.search(r"(?<![-\w])height\s*:\s*\d", css)


FARGEKODE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(")


def _uten_root(css):
    """Fjerner :root-blokken, så bare resten av stilen sjekkes."""
    return re.sub(r":root\s*\{.*?\}", "", css, count=1, flags=re.S)


def test_ux_dr1_ingen_fargekoder_utenfor_root():
    """UX-DR1: alle farger står som variabler i :root, ingen fargekoder andre steder."""
    css = STIL.read_text(encoding="utf-8")
    assert len(re.findall(r":root\s*\{", css)) == 1
    assert FARGEKODE.search(_uten_root(css)) is None
    assert MALER
    for mal in MALER:
        # All stil ligger i stil.css: ingen style-attributt og ingen <style> i malene.
        innhold = mal.read_text(encoding="utf-8")
        assert not re.search(r"\sstyle\s*=", innhold, re.I), mal.name
        assert not re.search(r"<style", innhold, re.I), mal.name


def test_ux_dr1_sjekken_finner_fargekoder():
    """UX-DR1: sjekken over slår faktisk til på fargekoder utenfor :root."""
    assert FARGEKODE.search(_uten_root(":root { --a: #fff; } p { color: #A23E6C; }"))
    assert FARGEKODE.search(_uten_root(":root { --a: #fff; } p { color: rgba(0, 0, 0, 0.5); }"))
    assert FARGEKODE.search(_uten_root(":root { --a: #fff; } p { color: var(--a); }")) is None
