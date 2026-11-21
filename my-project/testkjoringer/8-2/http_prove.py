"""Logger inn med testbrukeren og lager en søknad i testmodus med case 1 over HTTP.

Brukt i prøven fra en ny kopi (story 8.2.1, ny-kopi-1.txt). Kjøres fra backend/ i kopien
mens nettsiden kjører:

    uv run python <sti>/http_prove.py http://127.0.0.1:5000 testdata/case-1-utvikler
"""

import http.cookiejar
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BASE = sys.argv[1]
CASE = Path(sys.argv[2])
jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def kall(sti, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    with op.open(BASE + sti, body) as svar:
        return svar.status, svar.geturl().replace(BASE, ""), svar.read(), svar.headers


def tittel(html):
    m = re.search(rb"<title>(.*?)</title>", html, re.S)
    return m.group(1).decode().strip() if m else "?"


s, url, html, _ = kall("/")
print(f"GET / -> {s} {url} «{tittel(html)}»")
s, url, html, _ = kall("/logg-inn", {"epost": "test@example.com", "passord": "testpassord1"})
print(f"POST /logg-inn (testbrukeren) -> {s} {url} «{tittel(html)}»")
print("  Testmodus låst på:", "Mangler API-nøkkel, se README" in html.decode())
s, url, html, _ = kall("/", {})
print(f"POST / (Begynn å lage søknad) -> {s} {url} «{tittel(html)}»")
s, url, html, _ = kall("/modus", {"modus": "full_generering"})
print(f"POST /modus (Full generering) -> {s} {url} «{tittel(html)}»")
cv = (CASE / "cv.txt").read_text(encoding="utf-8")
annonse = (CASE / "annonse.txt").read_text(encoding="utf-8")
s, url, html, _ = kall(
    "/innlegging",
    {
        "handling": "sjekk",
        "cv_kilde": "tekst",
        "cv": cv,
        "annonse_kilde": "tekst",
        "annonse": annonse,
    },
)
tekst = html.decode()
print(f"POST /innlegging (CV og annonse fra case 1) -> {s} {url} «{tittel(html)}»")
m = re.search(r"(\d+) av (\d+) = (\d+) %", tekst)
print("  Nøkkelordtreff på siden:", m.group(0) if m else "fant ikke")
fasit = (CASE / "fasit.md").read_text(encoding="utf-8")
mf = re.search(r"(\d+) av (\d+) = (\d+) %", fasit)
print("  Nøkkelordtreff i fasit.md:", mf.group(0) if mf else "fant ikke")
s, url, html, _ = kall("/resultat", {"handling": "brev"})
tekst = html.decode()
print(f"POST /resultat (Lag søknadsbrevet mitt) -> {s} {url} «{tittel(html)}»")
print("  «Med vennlig hilsen» i brevet:", "Med vennlig hilsen" in tekst)
for fmt in ("docx", "pdf"):
    s, url, innhold, h = kall(f"/last-ned/{fmt}")
    navn = re.search(r'filename="?([^";]+)', h.get("Content-Disposition", ""))
    print(
        f"GET /last-ned/{fmt} -> {s}, {len(innhold)} byte, {h.get_content_type()}, "
        f"filnavn {navn.group(1) if navn else '?'}, starter med {innhold[:4]!r}"
    )
s, url, html, _ = kall("/logg-ut", {})
print(f"POST /logg-ut -> {s} {url} «{tittel(html)}»")
