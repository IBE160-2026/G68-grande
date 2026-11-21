"""Etikettene og alternativtekstene i HTML-en fra den kjørende nettsiden (NFR-6, story 8.2.1).

Logger inn med testbrukeren og går gjennom flyten i testmodus med case 1, både i Full
generering og i Korrektur. Hvert steg sjekker at nettsiden kom til siden steget skal gi (stien
i adressen etter alle videresendingene). Kommer den til en annen side, stopper skriptet med
feilkode 1, så en feilet innlogging ikke gir sjekker av innloggingssiden i stedet. For hver side
sjekkes det at:
- hvert felt (input som ikke er type="hidden" eller en knapp, textarea, select) har en etikett:
  en <label for="...">, en <label> rundt feltet, aria-label eller aria-labelledby. Om etiketten
  synes på skjermen, kan skriptet ikke se. Felt med attributtet hidden (filvelgerne, som åpnes
  med knappen «Last opp PDF») er skjult for alle og telles for seg
- hver knapp har tekst eller aria-label. Tekst inni et element med aria-hidden="true" (for
  eksempel et ikon) teller ikke, fordi skjermlesere ikke leser den
- hvert <img> har alt, og hvert <svg> og <canvas> er skjult for skjermlesere (aria-hidden) eller
  har role="img" med aria-label
- hver aria-labelledby, aria-describedby og aria-controls peker på id-er som finnes på siden
- ingen id står to ganger på samme side

Kjøres mens nettsiden kjører i testmodus (uv run flask --app soknad run fra backend/):

    uv run python my-project/testkjoringer/8-2/etiketter.py http://127.0.0.1:5000

Ender med feilkode 1 hvis noe mangler.
"""

import http.cookiejar
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

CASE = Path(__file__).resolve().parents[3] / "backend" / "testdata" / "case-1-utvikler"
TOMME = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source"}
REFERANSER = ("aria-labelledby", "aria-describedby", "aria-controls")


class Side(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.id = []
        self.label_for = set()
        self.felt = []  # (tag, attrs, inni_label)
        self.skjulte = 0  # felt med attributtet hidden
        self.knapper = []  # [attrs, tekst]
        self.bilder = []  # (tag, attrs)
        self.referanser = []  # (attributt, id)
        self.stakk = []  # (tag, aria_hidden)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.id.append(a["id"])
        for navn in REFERANSER:
            for ref in (a.get(navn) or "").split():
                self.referanser.append((navn, ref))
        inni_label = any(t == "label" for t, _ in self.stakk)
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
            self.stakk.append((tag, a.get("aria-hidden") == "true"))

    def handle_endtag(self, tag):
        if any(t == tag for t, _ in self.stakk):
            while self.stakk.pop()[0] != tag:
                pass

    def handle_data(self, data):
        i_knapp = any(t == "button" for t, _ in self.stakk)
        skjult = any(h for _, h in self.stakk)
        if i_knapp and not skjult and self.knapper:
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
    for id_, antall in Counter(side.id).items():
        if antall > 1:
            feil.append(f"id={id_} står {antall} ganger")
    resultat = "Bestått" if not feil else "Ikke bestått: " + "; ".join(feil)
    tall = [len(side.felt), side.skjulte, len(side.knapper), len(side.bilder)]
    print(f"| {navn} | {' | '.join(map(str, tall))} | {len(side.referanser)} | {resultat} |")
    return len(feil)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:5000"
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def side(sti, forventet, data=None):
        """Henter sti (POST med data) og gir HTML-en. Er stien etter videresendingene ikke
        forventet, stopper skriptet. En feilside (HTTPError) leses som en vanlig side."""
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        try:
            with op.open(base + sti, body) as svar:
                status, url, html = svar.status, svar.geturl(), svar.read()
        except urllib.error.HTTPError as feil:
            status, url, html = feil.code, feil.geturl(), feil.read()
        kom_til = urllib.parse.urlsplit(url).path
        if kom_til != forventet:
            print(f"\n{sti} ga {kom_til} (status {status}), ikke {forventet}. Stopper.")
            raise SystemExit(1)
        return html.decode("utf-8")

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
    feil += sjekk("Registrering", side("/registrer", "/registrer"))
    feil += sjekk("Innlogging", side("/logg-inn", "/logg-inn"))
    side("/logg-inn", "/", {"epost": "test@example.com", "passord": "testpassord1"})
    for modus, navn in (("full_generering", "Full generering"), ("korrektur", "Korrektur")):
        feil += sjekk(f"Startside ({navn})", side("/", "/"))
        feil += sjekk(f"Modusvalg ({navn})", side("/", "/modus", {}))
        feil += sjekk(f"Innlegging ({navn})", side("/modus", "/innlegging", {"modus": modus}))
        data = dict(felt, handling="sjekk")
        if modus == "korrektur":
            data.update(eget_brev_kilde="tekst", eget_brev=eget_brev)
        tomme = side("/innlegging", "/innlegging", {"handling": "sjekk"})
        feil += sjekk(f"Innlegging med feil ({navn})", tomme)
        feil += sjekk(f"Resultat ({navn})", side("/innlegging", "/resultat", data))
        feil += sjekk(f"Brev ({navn})", side("/resultat", "/brev", {"handling": "brev"}))
    side("/logg-ut", "/logg-inn", {})
    print()
    print(f"{feil} feil.")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
