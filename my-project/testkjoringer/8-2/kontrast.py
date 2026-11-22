"""Kontrasten for fargeparene i stil.css (NFR-6, story 8.2.1).

Leser fargevariablene i :root i backend/soknad/web/static/css/stil.css og regner ut
kontrasten etter WCAG 2.2 (relativ luminans). Parene er de som brukes sammen i stil.css:
tekst mot bakgrunnen den står på, og rammer, fokusring og bryter mot flaten rundt.
Tekst må ha minst 4,5:1 (WCAG AA). Rammer rundt felt, fokusringen og bryteren må ha minst
3:1 (WCAG 1.4.11). Halvgjennomsiktige farger (--wait-cover) legges over --background.

Kjøres fra roten av repoet:

    uv run python my-project/testkjoringer/8-2/kontrast.py

Skriver en tabell i markdown og ender med feilkode 1 hvis et par er under kravet.
"""

import re
import sys
from pathlib import Path

STIL = (
    Path(__file__).resolve().parents[3]
    / "backend"
    / "soknad"
    / "web"
    / "static"
    / "css"
    / "stil.css"
)

TEKST = 4.5
IKKE_TEKST = 3.0

# (forgrunn, bakgrunn, krav, hvor paret brukes). krav None = bare pynt, sjekkes ikke.
PAR = [
    ("text", "background", TEKST, "vanlig tekst på siden"),
    ("text", "surface", TEKST, "tekst i skjema, kort, bokser og brevet"),
    ("text-muted", "background", TEKST, "ingressen, «Du skrev», hjørneraden"),
    ("text-muted", "surface", TEKST, "hjelpetekst, forklaringer i kortene, testinfo"),
    ("text-muted", "wait-cover", TEKST, "teksten i ventetegnet"),
    ("primary", "background", TEKST, "logoen og lenker på siden"),
    ("primary", "surface", TEKST, "lenker, sekundærknappen, «i»-knappen, «Om ATS»"),
    ("primary", "wait-cover", TEKST, "overskriften i ventetegnet"),
    ("primary-contrast", "primary", TEKST, "hvit tekst på hovedknappene"),
    ("primary-contrast", "text", TEKST, "hvit tekst i «i»-boksen"),
    ("text", "accent", TEKST, "merkelappen på modus-kortet"),
    ("error", "surface", TEKST, "feilteksten ved feltene"),
    ("error", "error-tint", TEKST, "feilboksen og skjemafeilen"),
    ("success", "success-tint", TEKST, "filboksen, «Dekker», «Lastet ned»"),
    ("work-on", "work-on-tint", TEKST, "«Kan jobbes videre med»"),
    ("text", "success-tint", TEKST, "endret setning i Korrektur"),
    ("text", "work-on-tint", TEKST, "tekst i boksen «Kan jobbes videre med»"),
    ("text", "changed-active", TEKST, "endret setning med pekeren over eller åpen"),
    ("primary", "surface", IKKE_TEKST, "rammen rundt tekstfelt og avkrysningsboks"),
    ("error", "surface", IKKE_TEKST, "rammen rundt et felt med feil"),
    ("focus-ring", "background", IKKE_TEKST, "fokusringen på siden"),
    ("focus-ring", "surface", IKKE_TEKST, "fokusringen i skjema og bokser"),
    ("text-muted", "background", IKKE_TEKST, "bryteren når den er av"),
    ("surface", "primary", IKKE_TEKST, "knotten på bryteren når den er på"),
    ("primary", "border", None, "prosentlinjen (bare pynt, tallet står som tekst)"),
]


def les_farger(css: str) -> dict[str, tuple[float, float, float, float]]:
    """Fargevariablene i PAR fra :root som (r, g, b, alfa), med r, g, b fra 0 til 255. Mangler
    en av dem, eller har den et format skriptet ikke kjenner (bare #rrggbb og rgba(...)),
    stopper skriptet med navnet og verdien."""
    rot = re.search(r":root\s*\{(.*?)\}", css, flags=re.S)
    if rot is None:
        raise SystemExit("Fant ikke :root i stil.css")
    verdier = dict(re.findall(r"--([\w-]+):\s*([^;]+);", rot.group(1)))
    farger = {}
    for navn in {n for par in PAR for n in par[:2]} | {"background"}:
        if navn not in verdier:
            raise SystemExit(f"--{navn} finnes ikke i :root i stil.css")
        verdi = verdier[navn].strip()
        if m := re.fullmatch(r"#([0-9a-fA-F]{6})", verdi):
            h = m.group(1)
            farger[navn] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
        elif m := re.fullmatch(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", verdi):
            r, g, b, a = m.groups()
            farger[navn] = (int(r), int(g), int(b), float(a))
        else:
            raise SystemExit(f"--{navn} har et fargeformat skriptet ikke kjenner: {verdi!r}")
    return farger


def over(farge, bunn):
    """Legger en halvgjennomsiktig farge over en hel farge."""
    r, g, b, a = farge
    return tuple(a * x + (1 - a) * y for x, y in zip((r, g, b), bunn[:3], strict=True)) + (1.0,)


def luminans(farge) -> float:
    def kanal(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (kanal(c) for c in farge[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a, b) -> float:
    lys, mork = sorted((luminans(a), luminans(b)), reverse=True)
    return (lys + 0.05) / (mork + 0.05)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    farger = les_farger(STIL.read_text(encoding="utf-8"))

    def hent(navn):
        farge = farger[navn]
        return over(farge, farger["background"]) if farge[3] < 1 else farge

    print("| Forgrunn | Bakgrunn | Brukes til | Kontrast | Krav | Resultat |")
    print("| --- | --- | --- | --- | --- | --- |")
    feil = 0
    for forgrunn, bakgrunn, krav, hvor in PAR:
        k = kontrast(hent(forgrunn), hent(bakgrunn))
        if krav is None:
            kravtekst, resultat = "ingen", "Pynt"
        else:
            kravtekst = f"{krav:.1f}:1".replace(".", ",")
            resultat = "Bestått" if k >= krav else "Ikke bestått"
            feil += k < krav
        tall = f"{k:.2f}:1".replace(".", ",")
        print(f"| `{forgrunn}` | `{bakgrunn}` | {hvor} | {tall} | {kravtekst} | {resultat} |")
    print()
    print(f"{len(PAR)} par, {feil} under kravet.")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
