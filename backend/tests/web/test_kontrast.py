"""Kontrasten for fargeparene i stil.css (NFR-6, WCAG AA, story 8.2.1).

Leser fargevariablene i :root og regner ut kontrasten etter WCAG 2.2. Parene er de som brukes
sammen i stil.css. Tekst må ha minst 4,5:1. Rammer rundt felt, fokusringen og bryteren må ha
minst 3:1. Tabellen med alle tallene lages med my-project/testkjoringer/8-2/kontrast.py.
"""

import re

import pytest

from tests.web.hjelpere import STIL

TEKST = 4.5
IKKE_TEKST = 3.0

# (forgrunn, bakgrunn, krav). Prosentlinjen (primary mot border) er bare pynt og er ikke med.
PAR = [
    ("text", "background", TEKST),
    ("text", "surface", TEKST),
    ("text-muted", "background", TEKST),
    ("text-muted", "surface", TEKST),
    ("text-muted", "wait-cover", TEKST),
    ("primary", "background", TEKST),
    ("primary", "surface", TEKST),
    ("primary", "wait-cover", TEKST),
    ("primary-contrast", "primary", TEKST),
    ("primary-contrast", "text", TEKST),
    ("text", "accent", TEKST),
    ("error", "surface", TEKST),
    ("error", "error-tint", TEKST),
    ("success", "success-tint", TEKST),
    ("work-on", "work-on-tint", TEKST),
    ("text", "success-tint", TEKST),
    ("text", "work-on-tint", TEKST),
    ("text", "changed-active", TEKST),
    ("focus-ring", "background", IKKE_TEKST),
    ("focus-ring", "surface", IKKE_TEKST),
    ("text-muted", "background", IKKE_TEKST),
    ("surface", "primary", IKKE_TEKST),
]


def _farger():
    """Fargevariablene i :root som (r, g, b, alfa). Halvgjennomsiktige farger legges over
    --background, slik de vises på siden."""
    rot = re.search(r":root\s*\{(.*?)\}", STIL.read_text(encoding="utf-8"), flags=re.S)
    assert rot is not None
    farger = {}
    for navn, verdi in re.findall(r"--([\w-]+):\s*([^;]+);", rot.group(1)):
        verdi = verdi.strip()
        if m := re.fullmatch(r"#([0-9a-fA-F]{6})", verdi):
            h = m.group(1)
            farger[navn] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
        elif m := re.fullmatch(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", verdi):
            farger[navn] = (*map(int, m.groups()[:3]), float(m.group(4)))
    bunn = farger["background"]
    synlige = {}
    for navn, (r, g, b, a) in farger.items():
        synlige[navn] = tuple(a * x + (1 - a) * y for x, y in zip((r, g, b), bunn[:3], strict=True))
    return synlige


def _luminans(rgb):
    def kanal(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (kanal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _kontrast(a, b):
    lys, mork = sorted((_luminans(a), _luminans(b)), reverse=True)
    return (lys + 0.05) / (mork + 0.05)


def test_nfr6_kontrast_hvit_mot_svart_er_21():
    """NFR-6: utregningen gir 21:1 for hvit mot svart, som i WCAG."""
    assert _kontrast((255, 255, 255), (0, 0, 0)) == pytest.approx(21.0)


@pytest.mark.parametrize(("forgrunn", "bakgrunn", "krav"), PAR)
def test_nfr6_kontrast_fargeparene_i_stilen_holder_wcag_aa(forgrunn, bakgrunn, krav):
    """NFR-6: hvert fargepar som brukes sammen i stil.css, har minst kravet i WCAG AA."""
    farger = _farger()
    assert _kontrast(farger[forgrunn], farger[bakgrunn]) >= krav
