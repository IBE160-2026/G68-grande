"""Tester for pynten fra UX-kuttlisten (story 7.4): fyrverkeriet rundt brevoverskriften
(UX-DR18), prosentlinjen som fylles (UX-DR13) og ikonet som vipper på modusvalget (UX-DR12),
alt av ved redusert bevegelse, og canvas og ikonene skjult for skjermlesere (UX-DR21).
Skriptet testes bare som kildetekst (ingen nettlesertester, issue #16), så her testes at
canvas, skriptet og CSS-en er på plass. Testene er i en egen fil, så test_brev.py og
test_resultat.py ikke vokser."""

import re

import pytest

from soknad.web import tekster
from tests.web.hjelpere import (
    NEDLASTING,
    STIL,
    WEB,
    FeilendeKI,
    css_blokk,
    html_av,
    main,
    tagger_i,
)

SKRIPT = WEB / "static" / "js" / "fyrverkeri.js"
SKRIPT_TAG = '<script src="/static/js/fyrverkeri.js" defer></script>'
NYTT_FORSLAG = {"handling": "nytt_forslag"}


def _canvas(html):
    return [a for t, a in tagger_i(html) if t == "canvas"]


def _uten_kommentarer(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _media(css, sporring):
    """Innholdet i @media-blokken for sporring (til den første } på starten av en linje)."""
    return re.search(rf"@media {re.escape(sporring)} \{{(.*?)\n\}}", css, re.S).group(1)


# --- Brevsiden ---


@pytest.mark.parametrize("fikstur", ["paa_brev", "paa_brev_korrektur"])
def test_ux_dr18_brevsiden_har_fyrverkeri_bak_overskriften(request, fikstur):
    """UX-DR18/UX-DR21: brevsiden har én canvas for fyrverkeriet i begge modusene, skjult for
    skjermlesere, først i rammen rundt overskriften (bak teksten). fyrverkeri.js lastes med
    defer. Overskriften har fortsatt tabindex og autofocus, og canvas har ingen style=."""
    klient = request.getfixturevalue(fikstur)
    html = html_av(klient.get("/brev"))
    assert _canvas(html) == [{"class": "fyrverkeri", "aria-hidden": "true"}]
    assert SKRIPT_TAG in html
    ramme = re.search(r'<div class="fyrverkeri-ramme">(.*?)</div>', main(html), re.S).group(1)
    assert [t for t, _ in tagger_i(ramme)] == ["canvas", "h1"]
    h1 = [a for t, a in tagger_i(html) if t == "h1"]
    assert h1 == [{"class": "brev-overskrift", "tabindex": "-1", "autofocus": None}]
    # Canvas står over brevarket, aldri inni det.
    assert main(html).index("<canvas") < main(html).index('<article class="brevark">')
    assert "style=" not in main(html)


def test_ux_dr18_nytt_forslag_gir_nytt_fyrverkeri(paa_brev):
    """UX-DR18/FR-25: etter et nytt forslag sendes brukeren til GET /brev, og siden har
    fyrverkeriet igjen."""
    svar = paa_brev.post("/brev", data=NYTT_FORSLAG)
    assert svar.location == "/brev"
    html = html_av(paa_brev.get("/brev"))
    assert len(_canvas(html)) == 1
    assert SKRIPT_TAG in html


def test_ux_dr18_ingen_fyrverkeri_ved_ki_feil(app, paa_brev):
    """UX-DR18/FR-28: feiler KI-en ved «Nytt forslag», er det ikke noe å feire. Brevsiden med
    feilboksen har ingen canvas og ikke fyrverkeri.js, og overskriften står uten autofocus."""
    app.extensions["test_ki"] = FeilendeKI(app.extensions["test_ki"], oppgave="brev")
    svar = paa_brev.post("/brev", data=NYTT_FORSLAG)
    assert svar.status_code == 200
    html = html_av(svar)
    assert 'class="feilboks"' in html
    assert _canvas(html) == []
    assert "fyrverkeri" not in html
    h1 = [a for t, a in tagger_i(html) if t == "h1"]
    assert h1 == [{"class": "brev-overskrift", "tabindex": "-1"}]


def test_ux_dr18_ingen_fyrverkeri_ved_filfeil(paa_brev, filfeil):
    """UX-DR18/AD-9: kan filen ikke lages, har brevsiden med feilboksen ingen canvas og ikke
    fyrverkeri.js."""
    svar = paa_brev.get(NEDLASTING)
    assert svar.status_code == 500
    html = html_av(svar)
    assert tekster.FIL_FEIL in html
    assert _canvas(html) == []
    assert "fyrverkeri" not in html


# --- Skriptet ---


def test_ux_dr18_skriptet_tegner_fyrverkeriet_bare_som_pynt():
    """UX-DR18/AD-1: fyrverkeri.js tegner ingenting ved redusert bevegelse, tegner med
    requestAnimationFrame i canvas-ens devicePixelRatio, har nye utbrudd i 2200 ms, er ferdig
    etter 3200 ms og har minst 350 ms mellom utbruddene (høyst 3 i sekundet). Utbruddene står
    på venstre og høyre side. Fargene leses fra de fem CSS-variablene, uten fargekoder.
    Skriptet henter, sender og lagrer ingenting."""
    skript = SKRIPT.read_text(encoding="utf-8")
    assert 'matchMedia("(prefers-reduced-motion: reduce)")' in skript
    assert "requestAnimationFrame" in skript
    assert "devicePixelRatio" in skript
    assert 'querySelector("canvas.fyrverkeri")' in skript
    for konstant in ("= 2200;", "= 3200;", "= 350;", "= 26;"):
        assert konstant in skript, konstant
    assert "0.1 + Math.random() * 0.2" in skript
    assert "0.7 + Math.random() * 0.2" in skript
    assert "getComputedStyle(document.documentElement)" in skript
    for variabel in ("--fireworks-gold", "--primary", "--accent", "--dot-middle", "--success"):
        assert f'"{variabel}"' in skript, variabel
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", skript)
    assert not re.search(r"\b(rgb|rgba|hsl|hsla)\(", skript)
    for forbudt in ("fetch", "XMLHttpRequest", "localStorage", "sessionStorage", ".submit()"):
        assert forbudt not in skript, forbudt


def test_ux_dr18_fargene_finnes_i_root():
    """UX-DR18: de fem fargene skriptet leser, er definert i :root."""
    root = css_blokk(STIL.read_text(encoding="utf-8"), ":root")
    for variabel in ("--fireworks-gold", "--primary", "--accent", "--dot-middle", "--success"):
        assert re.search(rf"^\s*{re.escape(variabel)}:", root, re.M), variabel


# --- CSS ---


def test_ux_dr18_css_for_rammen_og_canvas():
    """UX-DR18/NFR-7: rammen er position: relative med luft fra --space-*, canvas fyller den
    (inset: 0, inline-size og block-size 100 %) og tar ikke trykk, og overskriften ligger over
    (z-index). Ingen fast høyde på overskriften og ingen nowrap."""
    css = STIL.read_text(encoding="utf-8")
    ramme = css_blokk(css, ".fyrverkeri-ramme")
    assert "position: relative;" in ramme
    assert re.search(r"padding: var\(--space-\d\)", ramme)
    canvas = css_blokk(css, ".fyrverkeri")
    for regel in (
        "position: absolute;",
        "inset: 0;",
        "inline-size: 100%;",
        "block-size: 100%;",
        "pointer-events: none;",
    ):
        assert regel in canvas, regel
    overskrift = _uten_kommentarer(css_blokk(css, ".brev-overskrift"))
    assert "position: relative;" in overskrift
    assert "z-index: 1;" in overskrift
    for blokk in (ramme, overskrift):
        assert not re.search(r"^\s*(min-|max-)?height:", blokk, re.M)
        assert "nowrap" not in blokk


def test_ux_dr13_prosentlinjen_fylles_paa_ett_sekund():
    """UX-DR13: fyllet i prosentlinjen vokser fra 0 (scaleX(0)) fra venstre kant på 1 s."""
    css = STIL.read_text(encoding="utf-8")
    fyll = css_blokk(css, ".prosentlinje .fyll")
    assert "transform-origin: 0 0;" in fyll
    assert "animation: fyll 1s ease-out;" in fyll
    keyframes = re.search(r"@keyframes fyll \{(.*?)\n\}", css, re.S).group(1)
    assert re.search(r"from\s*\{\s*transform: scaleX\(0\);\s*\}", keyframes)


def test_ux_dr13_tallet_staar_fortsatt_som_tekst(paa_resultat):
    """UX-DR13/FR-17: prosentlinjen er bare pynt. Tallet står som tekst, og bredden står i
    SVG-en, så linjen er riktig også uten animasjonen."""
    html = main(html_av(paa_resultat.get("/resultat")))
    assert re.search(r'<strong id="nokkelordtreff">[^<]*\d[^<]*</strong>', html)
    fyll = next(a for t, a in tagger_i(html) if t == "rect" and a.get("class") == "fyll")
    assert fyll["width"].isdigit()


def test_ux_dr12_ikonet_vipper_ved_hover():
    """UX-DR12: kortet løftes 4 px og får rammen i primary ved hover (fra før), og ikonet
    vipper −8° og blir 10 % større på 0,3 s."""
    css = STIL.read_text(encoding="utf-8")
    kort = css_blokk(css, ".modus-kort:hover")
    assert "transform: translateY(-4px);" in kort
    assert "border-color: var(--primary);" in kort
    assert "transition: transform 0.3s ease;" in css_blokk(css, ".modus-kort .ikon")
    hover = css_blokk(css, ".modus-kort:hover .ikon")
    assert "transform: rotate(-8deg) scale(1.1);" in hover


def test_ux_dr21_ikonene_er_skjult_for_skjermlesere(innlogget_client):
    """UX-DR21: ikonene på modus-kortene er bare pynt og skjult for skjermlesere."""
    innlogget_client.get("/")
    innlogget_client.post("/")
    html = html_av(innlogget_client.get("/modus"))
    ikoner = [a for t, a in tagger_i(main(html)) if a.get("class") == "ikon"]
    assert len(ikoner) == 2
    assert all(a.get("aria-hidden") == "true" for a in ikoner)


def test_ux_dr18_fyrverkeriet_skjules_i_hoykontrast():
    """UX-DR18/NFR-7: i høykontrastmodus følger ikke fargene på canvas systemfargene, så
    fyrverkeriet skjules."""
    hoykontrast = _media(STIL.read_text(encoding="utf-8"), "(forced-colors: active)")
    blokk = re.search(r"^\s*\.fyrverkeri\s*\{(.*?)\}", hoykontrast, re.M | re.S).group(1)
    assert "display: none;" in blokk


def test_ux_dr18_redusert_bevegelse_slaar_av_pynten():
    """UX-DR18/UX-DR12/UX-DR13: ved redusert bevegelse slår den felles regelen av alle
    animasjoner (prosentlinjen står ferdig fylt) og overganger, og ikonet vipper ikke ved
    hover. Skriptet tegner ingenting (testet over)."""
    redusert = _media(STIL.read_text(encoding="utf-8"), "(prefers-reduced-motion: reduce)")
    assert re.search(r"\*,\s*\*::before,\s*\*::after\s*\{\s*animation: none !important;", redusert)
    assert "transition: none !important;" in redusert
    velgere = re.search(r"([^{}]*)\{\s*transform: none;\s*\}", redusert).group(1)
    assert ".modus-kort:hover .ikon" in velgere
