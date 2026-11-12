"""Tester for «Last ned som Word» på brevsiden (FR-29, FR-30, NFR-4, NFR-7, NFR-9, AD-8, AD-9,
AD-11, UX-DR16). Story 3.2."""

import re
from io import BytesIO

import pytest
from docx import Document

from soknad.adaptere import fil_ut
from soknad.kjerne.okt import Soknad, Tekstfelt, sett_lastet_ned
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from tests.web.hjelpere import (
    ANNONSE,
    CV,
    NEDLASTING,
    STIL,
    css_blokk,
    element,
    filnavn_i_dag,
    html_av,
    main,
    med_autofocus,
    sett_soknad,
    soknaden,
    tagger_i,
)

# Fiksturene paa_brev og filfeil står i conftest.py.


def knapp_html(html):
    return re.search(r'<a [^>]*id="last-ned-docx".*?</a>', html, re.S).group(0)


# --- Matrisen ---


def test_fr29_nedlastingen_sender_word_filen(app, paa_brev):
    """FR-29/AD-8/AD-11: GET /last-ned/docx gir 200 med Word-filen som vedlegg, filnavnet
    Soknad_<i dag>.docx og lastet_ned sann. Steget og brevet er uendret."""
    for_ = soknaden(app, paa_brev)
    assert for_.lastet_ned is False
    svar = paa_brev.get(NEDLASTING)
    assert svar.status_code == 200
    assert svar.mimetype == fil_ut.DOCX_MEDIETYPE
    assert svar.headers["Content-Disposition"] == f"attachment; filename={filnavn_i_dag()}"
    # NFR-4: nettleseren lagrer ikke brevet i hurtigbufferen.
    assert svar.headers["Cache-Control"] == "no-store"
    assert re.fullmatch(r"Soknad_\d{4}-\d{2}-\d{2}\.docx", filnavn_i_dag())
    etter = soknaden(app, paa_brev)
    assert etter == sett_lastet_ned(for_)


def test_fr30_nedlastet_fil_er_lik_brevet_uten_topp_og_bunntekst(app, paa_brev):
    """FR-30/NFR-9: den nedlastede filen åpnes med python-docx. Avsnittene er like brevet, og
    det er ingen topp- eller bunntekst."""
    brev = soknaden(app, paa_brev).brev
    dokument = Document(BytesIO(paa_brev.get(NEDLASTING).data))
    assert [p.text for p in dokument.paragraphs] == brev["avsnitt"]
    for seksjon in dokument.sections:
        assert seksjon.header.is_linked_to_previous
        assert seksjon.footer.is_linked_to_previous
        assert all(not p.text for p in seksjon.header.paragraphs + seksjon.footer.paragraphs)


def test_ad9_filfeil_gir_brevsiden_med_feilboksen(app, paa_brev, filfeil):
    """FR-29/AD-9: kan filen ikke lages, vises brevsiden (500) med feilboksen øverst og brevet
    under. lastet_ned er uendret, og det er ingen redirect."""
    for_ = soknaden(app, paa_brev)
    svar = paa_brev.get(NEDLASTING)
    assert svar.status_code == 500
    assert svar.location is None
    assert "Content-Disposition" not in svar.headers
    html = main(html_av(svar))
    assert tekster.FIL_FEIL in html
    assert "ikke borte" not in html
    # Feilboksen står etter overskriften og før brevet.
    assert html.index(tekster.BREV_OVERSKRIFT) < html.index("feilboks") < html.index("brevark")
    for avsnitt in for_.brev["avsnitt"][:2]:
        assert avsnitt in html_av(svar)
    assert soknaden(app, paa_brev) is for_


def test_ux_dr7_filfeil_gir_fokus_til_feilboksen_og_prov_paa_nytt_laster_ned(paa_brev, filfeil):
    """AD-9/UX-DR7: feilboksen har fokus (ikke overskriften), og «Prøv på nytt» er en lenke som
    laster ned på nytt."""
    html = html_av(paa_brev.get(NEDLASTING))
    assert med_autofocus(html) == ["feilboks"]
    boks = re.search(r'<div class="feilboks".*?</div>', html, re.S).group(0)
    prov = re.search(r"<a [^>]*>(.*?)</a>", boks, re.S)
    assert prov.group(1) == tekster.PROV_PA_NYTT_KNAPP
    lenke = next(a for t, a in tagger_i(boks) if t == "a")
    assert lenke["href"] == NEDLASTING
    assert lenke["data-nedlasting"] == "docx"
    assert "hovedknapp" in lenke["class"]


def test_ad9_ekte_filfeil_fra_tegn_word_ikke_taler(app, paa_brev):
    """AD-9/FR-29: et brev med et tegn Word ikke tåler, gir feilboksen, ikke en feilside."""
    soknad = soknaden(app, paa_brev)
    sett_soknad(app, paa_brev, Soknad(**{**soknad.__dict__, "brev": {"avsnitt": ["a\x00b"]}}))
    svar = paa_brev.get(NEDLASTING)
    assert svar.status_code == 500
    assert tekster.FIL_FEIL in html_av(svar)


@pytest.mark.parametrize(
    ("steg", "side"),
    [
        (Steg.START, "/"),
        (Steg.MODUS, "/modus"),
        (Steg.INNLEGGING, "/innlegging"),
        (Steg.RESULTAT, "/resultat"),
    ],
)
def test_ad8_nedlasting_for_tidlig_sender_til_steget(app, innlogget_client, steg, side):
    """AD-8/FR-29: før brevet er laget, sendes /last-ned/docx til siden for steget, og
    søknaden er uendret."""
    soknad = Soknad(steg=steg)
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.get(NEDLASTING)
    assert svar.status_code == 302
    assert svar.location == side
    assert soknaden(app, innlogget_client) is soknad


def test_fr29_nedlasting_uten_brev_sender_til_resultatsiden(app, innlogget_client):
    """FR-29/AD-8: står søknaden på steg brev uten brev, sendes nedlastingen til /resultat."""
    soknad = Soknad(steg=Steg.BREV, cv=Tekstfelt("cv"), nokkelord=("cv",), gap={})
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.get(NEDLASTING)
    assert svar.location == "/resultat"
    assert soknaden(app, innlogget_client) is soknad


def test_fr27_nedlasting_mens_opptatt_sender_til_steget(app, paa_brev):
    """FR-27/AD-8: mens søknaden er opptatt, sendes nedlastingen til siden for steget uten fil,
    og søknaden er uendret."""
    soknad = Soknad(**{**soknaden(app, paa_brev).__dict__, "opptatt": True})
    sett_soknad(app, paa_brev, soknad)
    svar = paa_brev.get(NEDLASTING)
    assert svar.status_code == 302
    assert svar.location == "/brev"
    assert soknaden(app, paa_brev) is soknad


def test_ad8_endret_soknad_under_nedlastingen_skrives_ikke_over(app, paa_brev, monkeypatch):
    """AD-8: åpnes startsiden i en annen fane mens filen lages, blir den nye søknaden stående.
    lastet_ned lagres bare på søknaden filen ble laget fra."""
    ekte = fil_ut.lag_docx

    def startsiden_imens(avsnitt):
        assert paa_brev.get("/").status_code == 200
        return ekte(avsnitt)

    monkeypatch.setattr(fil_ut, "lag_docx", startsiden_imens)
    assert paa_brev.get(NEDLASTING).status_code == 200
    assert soknaden(app, paa_brev) == Soknad()


def test_ux_dr16_allerede_lastet_ned_gir_gronn_knapp_og_filnavn(paa_brev):
    """UX-DR16: etter nedlasting viser brevsiden knappen grønn med «✓ Lastet ned som Word» og
    filnavnlinjen, også når siden lastes på nytt."""
    paa_brev.get(NEDLASTING)
    html = html_av(paa_brev.get("/brev"))
    knapp = element(html, "last-ned-docx")
    assert "ferdig" in knapp["class"].split()
    assert "hidden" not in element(html, "filnavn-docx")
    assert f">{tekster.filnavn_linje(filnavn_i_dag())}</p>" in html
    spans = {a["class"]: a for t, a in tagger_i(knapp_html(html)) if t == "span" and "class" in a}
    assert "hidden" in spans["ikke-lastet-ned"]
    assert "hidden" not in spans["lastet-ned"]


@pytest.mark.parametrize(
    "endre",
    [
        lambda c: c.post("/resultat", data={"handling": "brev"}),
        lambda c: c.post("/modus", data={"modus": "full_generering"}),
        lambda c: c.post(
            "/innlegging", data={"cv": CV + " Ny linje.", "annonse": ANNONSE, "handling": "tilbake"}
        ),
    ],
    ids=["nytt-brev", "modus-paa-nytt", "endret-cv"],
)
def test_fr29_nytt_brev_eller_endret_inndata_nullstiller_lastet_ned(app, paa_brev, endre):
    """FR-29/AD-8: et nytt brev, modus på nytt eller endret CV gjør lastet_ned usann."""
    paa_brev.get(NEDLASTING)
    assert soknaden(app, paa_brev).lastet_ned is True
    paa_brev.get("/resultat")
    endre(paa_brev)
    assert soknaden(app, paa_brev).lastet_ned is False


# --- Brevsiden før nedlasting ---


def test_fr29_knappen_last_ned_som_word_under_brevet(paa_brev):
    """FR-29: under brevet står «Last ned som Word», en hovedknapp-lenke til /last-ned/docx.
    Den grønne teksten og filnavnet er skjult, og overskriften har fokus."""
    html = html_av(paa_brev.get("/brev"))
    knapp = element(html, "last-ned-docx")
    assert knapp["href"] == NEDLASTING
    assert knapp["data-nedlasting"] == "docx"
    assert knapp["class"].split() == ["hovedknapp"]
    assert main(html).index("brevark") < main(html).index("last-ned-docx")
    tekst = knapp_html(html)
    assert f">{tekster.LAST_NED_WORD}</span>" in tekst
    assert f'<span aria-hidden="true">{tekster.FERDIG_IKON}</span> {tekster.LASTET_NED_WORD}' in (
        tekst
    )
    spans = {a["class"]: a for t, a in tagger_i(tekst) if t == "span" and "class" in a}
    assert "hidden" not in spans["ikke-lastet-ned"]
    assert "hidden" in spans["lastet-ned"]
    filnavn = element(html, "filnavn-docx")
    assert "hidden" in filnavn
    assert "aria-live" not in filnavn
    assert f">{tekster.filnavn_linje(filnavn_i_dag())}</p>" in html
    assert med_autofocus(html) == [None]
    assert "feilboks" not in main(html)


def test_fr29_brevsiden_laster_nedlastingsskriptet(paa_brev):
    """FR-29/UX-DR16: brevsiden laster nedlasting.js. Skriptet gjør knappen grønn, viser
    filnavnet og skjuler feilboksen, men stopper ikke nedlastingen (AD-1)."""
    html = html_av(paa_brev.get("/brev"))
    assert '<script src="/static/js/nedlasting.js" defer></script>' in html
    skript = (STIL.parents[1] / "js" / "nedlasting.js").read_text(encoding="utf-8")
    for del_ in ('classList.add("ferdig")', "filnavn.hidden = false", "feilboks.hidden = true"):
        assert del_ in skript
    assert "preventDefault" not in skript
    assert "fetch" not in skript


def test_nfr4_filen_ligger_ikke_paa_disk(paa_brev, tmp_path, monkeypatch):
    """NFR-4: nedlastingen skriver ingen fil i arbeidsmappen."""
    arbeidsmappe = tmp_path / "arbeidsmappe"
    arbeidsmappe.mkdir()
    monkeypatch.chdir(arbeidsmappe)
    assert paa_brev.get(NEDLASTING).status_code == 200
    assert list(arbeidsmappe.iterdir()) == []


def test_fr29_tekstene_ligger_i_tekster_py():
    """FR-29/UX-DR16: tekstene står i web/tekster.py, ordrett fra EXPERIENCE, og ikke i malen."""
    assert tekster.LAST_NED_WORD == "Last ned som Word"
    assert tekster.LASTET_NED_WORD == "Lastet ned som Word"
    assert tekster.FERDIG_IKON == "✓"
    assert tekster.filnavn_linje("Soknad_2026-11-11.docx") == "Filnavn: Soknad_2026-11-11.docx"
    assert tekster.FIL_FEIL == "Vi klarte ikke å lage filen. Prøv på nytt."
    mal = STIL.parents[2] / "templates" / "brev.html"
    innhold = re.sub(r"\{#.*?#\}", "", mal.read_text(encoding="utf-8"), flags=re.S)
    for tekst in ("Last ned", "Lastet ned", "✓", "Filnavn", "klarte ikke"):
        assert tekst not in innhold, tekst


def test_nfr7_nedlastingsknappen_og_filnavnet_i_css():
    """NFR-7/UX-DR16: knappen er i midten uten fast bredde, den grønne knappen har success-
    fargene, og filnavnet bryter lange ord. Ingen fast høyde og ingen nowrap."""
    css = STIL.read_text(encoding="utf-8")
    nedlasting = css_blokk(css, ".nedlasting")
    assert "align-items: center;" in nedlasting
    knapp = css_blokk(css, ".nedlasting .hovedknapp")
    assert "width: auto;" in knapp
    assert "max-width: 100%;" in knapp
    ferdig = css_blokk(css, ".hovedknapp.ferdig")
    for linje in (
        "color: var(--success);",
        "background: var(--success-tint);",
        "border-color: var(--success);",
    ):
        assert linje in ferdig
    assert "overflow-wrap: anywhere;" in css_blokk(css, ".filnavn-linje")
    assert "text-decoration: none;" in css_blokk(css, "a.hovedknapp")
    for blokk in (nedlasting, knapp, ferdig, css_blokk(css, ".filnavn-linje")):
        assert "height" not in blokk
        assert "nowrap" not in blokk
