"""Logger inn med testbrukeren og lager en søknad i testmodus med case 1 over HTTP.

Brukt i prøven fra en ny kopi (story 8.2.1, ny-kopi-1.txt). Kjøres mens nettsiden kjører, med
adressen og mappen til testcaset:

    uv run python my-project/testkjoringer/8-2/http_prove.py http://127.0.0.1:5000 \\
        backend/testdata/case-1-utvikler

Sjekker at testmodus er på («Mangler API-nøkkel, se README»), at resultatsiden viser prosenten
i fasit.md, at brevet har «Med vennlig hilsen», og at nedlastingene er en Word-fil (begynner med
PK) og en PDF (begynner med %PDF). Ender med feilkode 1 hvis en sjekk feiler.
"""

import http.cookiejar
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PROSENT = re.compile(r"\d+ av \d+ = \d+ %")


def tittel(html):
    m = re.search(rb"<title>(.*?)</title>", html, re.S)
    return m.group(1).decode().strip() if m else "?"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        print("Bruk: http_prove.py <adresse, f.eks. http://127.0.0.1:5000> <mappen til testcaset>")
        return 2
    base = sys.argv[1].rstrip("/")
    case = Path(sys.argv[2])
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    feil = []

    def kall(sti, data=None):
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        with op.open(base + sti, body) as svar:
            return svar.status, svar.geturl().replace(base, ""), svar.read(), svar.headers

    def sjekk(navn, ok):
        print(f"  {navn}: {'ja' if ok else 'NEI'}")
        if not ok:
            feil.append(navn)

    s, url, html, _ = kall("/")
    print(f"GET / -> {s} {url} «{tittel(html)}»")
    s, url, html, _ = kall("/logg-inn", {"epost": "test@example.com", "passord": "testpassord1"})
    print(f"POST /logg-inn (testbrukeren) -> {s} {url} «{tittel(html)}»")
    sjekk("Innlogget (startsiden)", url == "/")
    sjekk(
        "Testmodus låst på («Mangler API-nøkkel, se README»)",
        "Mangler API-nøkkel, se README" in html.decode(),
    )
    s, url, html, _ = kall("/", {})
    print(f"POST / (Begynn å lage søknad) -> {s} {url} «{tittel(html)}»")
    s, url, html, _ = kall("/modus", {"modus": "full_generering"})
    print(f"POST /modus (Full generering) -> {s} {url} «{tittel(html)}»")
    cv = (case / "cv.txt").read_text(encoding="utf-8")
    annonse = (case / "annonse.txt").read_text(encoding="utf-8")
    data = {"handling": "sjekk", "cv_kilde": "tekst", "cv": cv}
    data.update(annonse_kilde="tekst", annonse=annonse)
    s, url, html, _ = kall("/innlegging", data)
    print(f"POST /innlegging (CV og annonse fra case 1) -> {s} {url} «{tittel(html)}»")
    paa_siden = PROSENT.search(html.decode())
    i_fasit = PROSENT.search((case / "fasit.md").read_text(encoding="utf-8"))
    print(f"  Nøkkelordtreff på siden: {paa_siden.group(0) if paa_siden else 'fant ikke'}")
    print(f"  Nøkkelordtreff i fasit.md: {i_fasit.group(0) if i_fasit else 'fant ikke'}")
    sjekk("Resultatsiden", url == "/resultat")
    sjekk("Samme prosent som fasit.md", bool(paa_siden and i_fasit) and paa_siden[0] == i_fasit[0])
    s, url, html, _ = kall("/resultat", {"handling": "brev"})
    print(f"POST /resultat (Lag søknadsbrevet mitt) -> {s} {url} «{tittel(html)}»")
    sjekk("Brevsiden", url == "/brev")
    sjekk("«Med vennlig hilsen» i brevet", "Med vennlig hilsen" in html.decode())
    for fmt, start in (("docx", b"PK"), ("pdf", b"%PDF")):
        s, url, innhold, h = kall(f"/last-ned/{fmt}")
        navn = re.search(r'filename="?([^";]+)', h.get("Content-Disposition", ""))
        print(
            f"GET /last-ned/{fmt} -> {s}, {len(innhold)} byte, {h.get_content_type()}, "
            f"filnavn {navn.group(1) if navn else '?'}, starter med {innhold[:4]!r}"
        )
        sjekk(f"Fila begynner med {start.decode()}", innhold.startswith(start))
    s, url, html, _ = kall("/logg-ut", {})
    print(f"POST /logg-ut -> {s} {url} «{tittel(html)}»")
    print()
    print("Bestått." if not feil else f"Ikke bestått: {', '.join(feil)}.")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
