"""Etikettene og alternativtekstene i HTML-en fra den kjørende nettsiden (NFR-6, story 8.2.1).

Logger inn med testbrukeren og går gjennom hele flyten i testmodus med case 1, både i Full
generering og i Korrektur. For hver side sjekkes det at:
- hvert felt (input som ikke er type="hidden" eller en knapp, textarea, select) har en synlig
  <label for="..."> eller ligger inni en <label>, eller har aria-label eller aria-labelledby.
  Felt med attributtet hidden (filvelgerne, som åpnes med knappen «Last opp PDF») er skjult
  for alle og telles for seg
- hver knapp har tekst eller aria-label
- hvert <img> har alt, og hvert <svg> og <canvas> er skjult for skjermlesere (aria-hidden) eller
  har role="img" med aria-label
- hver aria-labelledby og aria-describedby peker på id-er som finnes på siden

Kjøres mens nettsiden kjører (uv run flask --app soknad run fra backend/):

    uv run python my-project/testkjoringer/8-2/etiketter.py http://127.0.0.1:5000

Ender med feilkode 1 hvis noe mangler.
"""

import http.cookiejar
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

CASE = Path(__file__).resolve().parents[3] / "backend" / "testdata" / "case-1-utvikler"
TOMME = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source"}


class Side(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.id = set()
        self.label_for = set()
        self.felt = []  # (tag, attrs, inni_label)
        self.skjulte = 0  # felt med attributtet hidden
        self.knapper = []  # [attrs, tekst]
        self.bilder = []  # (tag, attrs)
        self.referanser = []  # (attributt, id)
        self.stakk = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.id.add(a["id"])
        for navn in ("aria-labelledby", "aria-describedby"):
            for ref in (a.get(navn) or "").split():
                self.referanser.append((navn, ref))
        inni_label = "label" in self.stakk
        er_felt = tag in ("textarea", "select") or (
            tag == "input" and a.get("type") not in ("hidden", "submit", "button")
        )
        if tag == "label" and a.get("for"):
            self.label_for.add(a["for"])
        if er_felt and "hidden" in a:
            self.skjulte += 1
        elif er_felt:
            self.felt.append((tag, a, inni_label))
        elif tag == "button":
            self.knapper.append([a, ""])
        elif tag in ("img", "svg", "canvas"):
            self.bilder.append((tag, a))
        if tag not in TOMME:
            self.stakk.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stakk:
            while self.stakk.pop() != tag:
                pass

    def handle_data(self, data):
        if "button" in self.stakk and self.knapper:
            self.knapper[-1][1] += data.strip()


def sjekk(navn, html):
    side = Side()
    side.feed(html)
    feil = []
    for tag, a, inni in side.felt:
        if not (
            inni or a.get("id") in side.label_for or a.get("aria-label") or a.get("aria-labelledby")
        ):
            feil.append(f"{tag} name={a.get('name')} id={a.get('id')} har ingen etikett")
    for a, tekst in side.knapper:
        if not (tekst or a.get("aria-label") or a.get("aria-labelledby")):
            feil.append(f"knapp {a.get('class')} har ingen tekst")
    for tag, a in side.bilder:
        if tag == "img" and "alt" not in a:
            feil.append(f"img {a.get('src')} mangler alt")
        if tag in ("svg", "canvas"):
            skjult = a.get("aria-hidden") == "true"
            har_navn = a.get("role") == "img" and (a.get("aria-label") or a.get("aria-labelledby"))
            if not (skjult or har_navn):
                feil.append(f"{tag} {a.get('class')} er verken skjult eller har navn")
    for attributt, ref in side.referanser:
        if ref not in side.id:
            feil.append(f"{attributt}={ref} finnes ikke på siden")
    resultat = "Bestått" if not feil else "Ikke bestått: " + "; ".join(feil)
    tall = [len(side.felt), side.skjulte, len(side.knapper), len(side.bilder)]
    print(f"| {navn} | {' | '.join(map(str, tall))} | {len(side.referanser)} | {resultat} |")
    return len(feil)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:5000"
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def side(sti, data=None):
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        with op.open(base + sti, body) as svar:
            return svar.read().decode("utf-8")

    cv = (CASE / "cv.txt").read_text(encoding="utf-8")
    annonse = (CASE / "annonse.txt").read_text(encoding="utf-8")
    eget_brev = (CASE / "eget-brev.txt").read_text(encoding="utf-8")
    felt = {"cv_kilde": "tekst", "cv": cv, "annonse_kilde": "tekst", "annonse": annonse}

    print(
        "| Side | Felt | Skjulte felt | Knapper | Bilder, svg og canvas | aria-referanser "
        "| Resultat |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- |")
    feil = 0
    feil += sjekk("Registrering", side("/registrer"))
    feil += sjekk("Innlogging", side("/logg-inn"))
    side("/logg-inn", {"epost": "test@example.com", "passord": "testpassord1"})
    for modus, navn in (("full_generering", "Full generering"), ("korrektur", "Korrektur")):
        feil += sjekk(f"Startside ({navn})", side("/"))
        feil += sjekk(f"Modusvalg ({navn})", side("/", {}))
        feil += sjekk(f"Innlegging ({navn})", side("/modus", {"modus": modus}))
        data = dict(felt, handling="sjekk")
        if modus == "korrektur":
            data.update(eget_brev_kilde="tekst", eget_brev=eget_brev)
        feil += sjekk(f"Innlegging med feil ({navn})", side("/innlegging", {"handling": "sjekk"}))
        feil += sjekk(f"Resultat ({navn})", side("/innlegging", data))
        feil += sjekk(f"Brev ({navn})", side("/resultat", {"handling": "brev"}))
    side("/logg-ut", {})
    print()
    print(f"{feil} feil.")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
