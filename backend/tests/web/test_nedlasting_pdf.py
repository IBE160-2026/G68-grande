"""Tester for «Last ned som PDF» på brevsiden (FR-29, FR-30, FR-31, NFR-4, NFR-7, AD-8, AD-9,
AD-11, UX-DR16, UX-DR17). Story 7.2. Testene er i en egen fil, så test_nedlasting.py ikke
vokser. PDF-en leses med pypdf. Skriptet testes bare som kildetekst, så åpningen av vinduet
prøves for hånd i nettleseren."""

import re
from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfReader

from soknad.adaptere import fil_ut
from soknad.kjerne.okt import Soknad, Tekstfelt
from soknad.kjerne.steg import Steg
from soknad.web import tekster
from tests.web.hjelpere import (
    ANNONSE,
    CV,
    NEDLASTING,
    NEDLASTING_PDF,
    STIL,
    brevtekst,
    css_blokk,
    element,
    filnavn_i_dag,
    html_av,
    korrektur_brev,
    main,
    med_autofocus,
    sett_soknad,
    soknaden,
    tagger_i,
)

# Fiksturene paa_brev, paa_brev_korrektur, filfeil (Word) og filfeil_pdf står i conftest.py.

SKRIPT = STIL.parents[1] / "js" / "nedlasting.js"
MAL = STIL.parents[2] / "templates" / "brev.html"
KJERNE = Path(fil_ut.__file__).resolve().parents[1] / "kjerne"


def pdf_tekst(innhold):
    """Teksten i PDF-en med mellomrom og linjeskift slått sammen til ett mellomrom."""
    leser = PdfReader(BytesIO(innhold))
    return " ".join(" ".join(side.extract_text() for side in leser.pages).split())


def slaa_sammen(avsnitt):
    return " ".join(" ".join(avsnitt).split())


def knapp_html(html, format_):
    return re.search(rf'<a [^>]*id="last-ned-{format_}".*?</a>', html, re.S).group(0)


def spans(html, format_):
    return {
        a["class"]: a
        for t, a in tagger_i(knapp_html(html, format_))
        if t == "span" and "class" in a
    }


def er_gronn(html, format_):
    """Sann når knappen for formatet er grønn med «Lastet ned som …» og filnavnet synlig, usann
    når den er blå med filnavnet skjult. Noe midt imellom gir en feil i testen."""
    ferdig = "ferdig" in element(html, f"last-ned-{format_}")["class"].split()
    deler = spans(html, format_)
    assert ("hidden" in deler["ikke-lastet-ned"]) is ferdig
    assert ("hidden" not in deler["lastet-ned"]) is ferdig
    assert ("hidden" not in element(html, f"filnavn-{format_}")) is ferdig
    return ferdig


# --- Matrisen ---


def test_fr29_pdf_nedlastingen_sender_pdf_filen(app, paa_brev):
    """FR-29/FR-30/AD-8/AD-11: GET /last-ned/pdf gir 200 med PDF-en som vedlegg, filnavnet
    Soknad_<i dag>.pdf og application/pdf. Teksten (pypdf) er lik brevet på siden, med «Med
    vennlig hilsen» og navnet til slutt. lastet_ned er {pdf}, og resten er uendret."""
    for_ = soknaden(app, paa_brev)
    html = html_av(paa_brev.get("/brev"))
    svar = paa_brev.get(NEDLASTING_PDF)
    assert svar.status_code == 200
    assert svar.mimetype == "application/pdf"
    assert svar.mimetype == fil_ut.PDF_MEDIETYPE
    assert re.fullmatch(r"Soknad_Testvik-Utvikling-AS_\d{4}-\d{2}-\d{2}\.pdf", filnavn_i_dag("pdf"))
    assert svar.headers["Content-Disposition"] == f"attachment; filename={filnavn_i_dag('pdf')}"
    # NFR-4: nettleseren lagrer ikke brevet i hurtigbufferen.
    assert svar.headers["Cache-Control"] == "no-store"
    brev = for_.brev
    forventet = [*brev["avsnitt"], "Med vennlig hilsen", brev["navn"]]
    assert brevtekst(html) == forventet
    assert pdf_tekst(svar.data) == slaa_sammen(forventet)
    etter = soknaden(app, paa_brev)
    assert etter.lastet_ned == {"pdf"}
    assert etter == Soknad(**{**for_.__dict__, "lastet_ned": frozenset({"pdf"})})


def test_fr30_pdf_i_korrektur_er_lik_avsnittene_uten_markeringer(app, paa_brev_korrektur):
    """FR-23/FR-30: i Korrektur er PDF-teksten lik avsnittene på brevsiden, uten «Endret
    setning», «Du skrev», «(Ny setning)» eller forklaringen."""
    html = html_av(paa_brev_korrektur.get("/brev"))
    assert tekster.KORREKTUR_FORKLARING in html
    svar = paa_brev_korrektur.get(NEDLASTING_PDF)
    assert svar.status_code == 200
    tekst = pdf_tekst(svar.data)
    assert brevtekst(html) == korrektur_brev(1)
    assert tekst == slaa_sammen(korrektur_brev(1))
    for markering in (
        tekster.ENDRET_SETNING_SKJERMLESER,
        tekster.DU_SKREV,
        tekster.NY_SETNING,
        tekster.KORREKTUR_FORKLARING,
        "Hei!",
    ):
        assert markering not in tekst
    assert soknaden(app, paa_brev_korrektur).lastet_ned == {"pdf"}


def test_fr29_word_og_saa_pdf_gir_begge_gronne(app, paa_brev):
    """FR-29/UX-DR16: Word og så PDF gir lastet_ned {docx, pdf}. Begge knappene er grønne med
    hver sin tekst og hver sin filnavn-linje, også når siden lastes på nytt."""
    assert paa_brev.get(NEDLASTING).status_code == 200
    assert paa_brev.get(NEDLASTING_PDF).status_code == 200
    assert soknaden(app, paa_brev).lastet_ned == {"docx", "pdf"}
    html = html_av(paa_brev.get("/brev"))
    assert er_gronn(html, "docx")
    assert er_gronn(html, "pdf")
    assert tekster.LASTET_NED_WORD in knapp_html(html, "docx")
    assert tekster.LASTET_NED_PDF in knapp_html(html, "pdf")
    assert f">{tekster.filnavn_linje(filnavn_i_dag('docx'))}</p>" in html
    assert f">{tekster.filnavn_linje(filnavn_i_dag('pdf'))}</p>" in html


def test_fr29_bare_word_gir_word_gronn_og_pdf_blaa(paa_brev):
    """FR-29/UX-DR16: etter Word og ny lasting av siden er Word grønn og PDF blå, og bare
    filnavn-docx er synlig."""
    paa_brev.get(NEDLASTING)
    html = html_av(paa_brev.get("/brev"))
    assert er_gronn(html, "docx")
    assert not er_gronn(html, "pdf")
    assert element(html, "last-ned-pdf")["class"].split() == ["hovedknapp"]


def test_fr29_bare_pdf_gir_pdf_gronn_og_word_blaa(paa_brev):
    """FR-29/UX-DR16: hver knapp blir grønn for seg: etter bare PDF er Word fortsatt blå."""
    paa_brev.get(NEDLASTING_PDF)
    html = html_av(paa_brev.get("/brev"))
    assert er_gronn(html, "pdf")
    assert not er_gronn(html, "docx")


@pytest.mark.parametrize(
    "endre",
    [
        lambda c: c.post("/brev", data={"handling": "nytt_forslag"}),
        lambda c: c.post("/modus", data={"modus": "full_generering"}),
        lambda c: c.post(
            "/innlegging", data={"cv": CV + " Ny linje.", "annonse": ANNONSE, "handling": "tilbake"}
        ),
    ],
    ids=["nytt-forslag", "ny-modus", "endret-cv"],
)
def test_fr29_nullstilling_gir_begge_blaa(app, paa_brev, endre):
    """FR-25/FR-29/AD-8: nytt forslag, ny modus eller endret CV etter begge nedlastingene gir
    tom lastet_ned, og begge knappene er blå når brevsiden vises igjen."""
    paa_brev.get(NEDLASTING)
    paa_brev.get(NEDLASTING_PDF)
    assert soknaden(app, paa_brev).lastet_ned == {"docx", "pdf"}
    endre(paa_brev)
    assert soknaden(app, paa_brev).lastet_ned == frozenset()
    # Lag brevet igjen der det trengs, så brevsiden kan vises.
    if soknaden(app, paa_brev).brev is None:
        paa_brev.post("/innlegging", data={"cv": CV, "annonse": ANNONSE, "handling": "sjekk"})
        paa_brev.post("/resultat", data={"handling": "brev"})
    html = html_av(paa_brev.get("/brev"))
    assert not er_gronn(html, "docx")
    assert not er_gronn(html, "pdf")


def test_ad9_filfeil_pdf_gir_brevsiden_og_prov_paa_nytt_til_pdf(app, paa_brev, filfeil_pdf):
    """FR-29/AD-9: kan PDF-en ikke lages, vises brevsiden (500) med feilboksen øverst, som har
    fokus, og brevet under. «Prøv på nytt» laster ned PDF på nytt. lastet_ned er uendret, også
    når Word alt er lastet ned."""
    paa_brev.get(NEDLASTING)
    for_ = soknaden(app, paa_brev)
    svar = paa_brev.get(NEDLASTING_PDF)
    assert svar.status_code == 500
    assert svar.location is None
    assert "Content-Disposition" not in svar.headers
    html = html_av(svar)
    assert tekster.FIL_FEIL in main(html)
    assert med_autofocus(html) == ["feilboks", "nytt-forslag-avbryt"]
    boks = re.search(r'<div class="feilboks".*?</div>', html, re.S).group(0)
    lenke = next(a for t, a in tagger_i(boks) if t == "a")
    assert lenke["href"] == NEDLASTING_PDF
    assert lenke["data-nedlasting"] == "pdf"
    assert tekster.PROV_PA_NYTT_KNAPP in boks
    assert brevtekst(html) == brevtekst(html_av(paa_brev.get("/brev")))
    assert soknaden(app, paa_brev) is for_
    assert for_.lastet_ned == {"docx"}
    # Word er fortsatt grønn i feilsiden, PDF blå.
    assert er_gronn(html, "docx")
    assert not er_gronn(html, "pdf")


def test_ad9_filfeil_word_gir_prov_paa_nytt_til_word(paa_brev, filfeil):
    """FR-29/AD-9: kan Word-fila ikke lages, går «Prøv på nytt» fortsatt til Word."""
    html = html_av(paa_brev.get(NEDLASTING))
    boks = re.search(r'<div class="feilboks".*?</div>', html, re.S).group(0)
    lenke = next(a for t, a in tagger_i(boks) if t == "a")
    assert lenke["href"] == NEDLASTING
    assert lenke["data-nedlasting"] == "docx"


def test_ad9_ekte_filfeil_pdf_uten_skrift(app, paa_brev, monkeypatch, tmp_path):
    """FR-29/AD-9: mangler skriften, gir PDF-nedlastingen feilboksen, ikke en feilside."""
    monkeypatch.setattr(fil_ut, "SKRIFT", tmp_path / "finnes-ikke.ttf")
    svar = paa_brev.get(NEDLASTING_PDF)
    assert svar.status_code == 500
    assert tekster.FIL_FEIL in html_av(svar)
    assert soknaden(app, paa_brev).lastet_ned == frozenset()


def test_ad8_ukjent_format_gir_404(app, paa_brev):
    """AD-8: et annet format enn docx og pdf finnes ikke (404), og søknaden er uendret."""
    for_ = soknaden(app, paa_brev)
    for adresse in ("/last-ned/txt", "/last-ned/PDF", "/last-ned/"):
        assert paa_brev.get(adresse).status_code == 404
    assert soknaden(app, paa_brev) is for_


def test_fr29_pdf_uten_brev_sender_til_resultatsiden(app, innlogget_client):
    """FR-29/AD-8: står søknaden på steg brev uten brev, sendes PDF-nedlastingen til
    /resultat, som Word."""
    soknad = Soknad(steg=Steg.BREV, cv=Tekstfelt("cv"), nokkelord=("cv",), gap={})
    sett_soknad(app, innlogget_client, soknad)
    assert innlogget_client.get(NEDLASTING_PDF).location == "/resultat"
    assert soknaden(app, innlogget_client) is soknad


@pytest.mark.parametrize(("steg", "side"), [(Steg.MODUS, "/modus"), (Steg.RESULTAT, "/resultat")])
def test_ad8_pdf_for_tidlig_sender_til_steget(app, innlogget_client, steg, side):
    """AD-8/FR-29: før brevet er laget, sendes /last-ned/pdf til siden for steget, som Word."""
    soknad = Soknad(steg=steg)
    sett_soknad(app, innlogget_client, soknad)
    svar = innlogget_client.get(NEDLASTING_PDF)
    assert svar.status_code == 302
    assert svar.location == side
    assert soknaden(app, innlogget_client) is soknad


def test_fr27_pdf_mens_opptatt_sender_til_steget(app, paa_brev):
    """FR-27/AD-8: mens søknaden er opptatt, gir PDF-nedlastingen ingen fil, som Word."""
    soknad = Soknad(**{**soknaden(app, paa_brev).__dict__, "opptatt": True})
    sett_soknad(app, paa_brev, soknad)
    svar = paa_brev.get(NEDLASTING_PDF)
    assert svar.status_code == 302
    assert svar.location == "/brev"
    assert soknaden(app, paa_brev) is soknad


def test_nfr4_pdf_ligger_ikke_paa_disk(paa_brev, tmp_path, monkeypatch):
    """NFR-4: PDF-nedlastingen skriver ingen fil i arbeidsmappen."""
    arbeidsmappe = tmp_path / "arbeidsmappe"
    arbeidsmappe.mkdir()
    monkeypatch.chdir(arbeidsmappe)
    assert paa_brev.get(NEDLASTING_PDF).status_code == 200
    assert list(arbeidsmappe.iterdir()) == []


def test_ad11_kjernen_importerer_aldri_fpdf():
    """AD-11: PDF lages bare i adaptere/fil_ut.py. Ingen fil i kjerne/ nevner fpdf."""
    filer = list(KJERNE.glob("*.py"))
    assert filer
    for fil in filer:
        assert "fpdf" not in fil.read_text(encoding="utf-8"), fil.name


# --- Knappene og tekstene ---


def test_fr29_knappene_staar_ved_siden_av_hverandre_over_nytt_forslag(paa_brev):
    """FR-29/UX-DR16: «Last ned som Word» og «Last ned som PDF» er blå hovedknapp-lenker i hver
    sin blokk i .nedlasting, Word først, under brevet og over «Nytt forslag». Hver blokk har
    knappen og filnavn-linjen for formatet."""
    html = html_av(paa_brev.get("/brev"))
    innhold = main(html)
    nedlasting = re.search(r'<div class="nedlasting">(.*?)\n</div>', innhold, re.S).group(1)
    blokker = re.findall(r'<div class="nedlasting-format">(.*?)</div>', nedlasting, re.S)
    assert len(blokker) == 2
    for blokk, format_, adresse in zip(
        blokker, ("docx", "pdf"), (NEDLASTING, NEDLASTING_PDF), strict=True
    ):
        assert f'id="last-ned-{format_}"' in blokk
        assert f'id="filnavn-{format_}"' in blokk
        knapp = element(html, f"last-ned-{format_}")
        assert knapp["href"] == adresse
        assert knapp["data-nedlasting"] == format_
        assert knapp["class"].split() == ["hovedknapp"]
    assert (
        innhold.index("brevark")
        < innhold.index('id="last-ned-docx"')
        < innhold.index('id="last-ned-pdf"')
        < innhold.index('id="nytt-forslag"')
    )
    tekst = knapp_html(html, "pdf")
    assert f">{tekster.LAST_NED_PDF}</span>" in tekst
    ikon = f'<span aria-hidden="true">{tekster.FERDIG_IKON}</span> {tekster.LASTET_NED_PDF}'
    assert ikon in tekst
    filnavn = element(html, "filnavn-pdf")
    assert "hidden" in filnavn
    assert "aria-live" not in filnavn
    assert f">{tekster.filnavn_linje(filnavn_i_dag('pdf'))}</p>" in html
    assert not er_gronn(html, "pdf")


def test_fr31_vinduet_viser_word_filnavnet_fra_serveren(paa_brev):
    """FR-31/UX-DR17: vinduet etter nedlasting har Word-filnavnet fra serveren. Skriptet bytter
    det til filnavnet for formatet som ble lastet ned."""
    html = html_av(paa_brev.get("/brev"))
    boks = re.search(r'<dialog [^>]*id="vindu-nedlastet".*?</dialog>', html, re.S).group(0)
    forventet = tekster.filnavn_linje(filnavn_i_dag("docx"))
    assert f'<p id="vindu-nedlastet-filnavn">{forventet}</p>' in boks


def test_fr29_pdf_tekstene_ligger_i_tekster_py():
    """FR-29/UX-DR16: tekstene står ordrett i web/tekster.py og ikke i malen."""
    assert tekster.LAST_NED_PDF == "Last ned som PDF"
    assert tekster.LASTET_NED_PDF == "Lastet ned som PDF"
    assert tekster.filnavn_linje("Soknad_2026-11-19.pdf") == "Filnavn: Soknad_2026-11-19.pdf"
    innhold = re.sub(r"\{#.*?#\}", "", MAL.read_text(encoding="utf-8"), flags=re.S)
    for tekst in ("Last ned", "Lastet ned", "Filnavn"):
        assert tekst not in innhold, tekst


# --- Skriptet og CSS-en ---


def test_fr31_skriptet_kopierer_filnavnet_inn_i_vinduet():
    """FR-31/UX-DR17: nedlasting.js kopierer teksten fra filnavn-<format> til
    vindu-nedlastet-filnavn før showModal(), så vinduet viser filnavnet for formatet som ble
    lastet ned. Det stopper ikke nedlastingen og henter ingenting (AD-1)."""
    skript = SKRIPT.read_text(encoding="utf-8")
    assert 'document.getElementById("filnavn-" + format)' in skript
    assert 'getElementById("vindu-nedlastet-filnavn")' in skript
    kopi = "vinduFilnavn.textContent = filnavn.textContent;"
    assert kopi in skript
    assert skript.index(kopi) < skript.index(".showModal()")
    assert "innerHTML" not in skript
    assert "preventDefault" not in skript
    assert "fetch" not in skript


def test_fr31_skriptet_skjuler_bare_feilboksen_for_samme_format():
    """FR-31/AD-9: nedlasting.js skjuler feilboksen bare når lenken i den er for formatet som
    lastes ned. Feilet PDF-en og brukeren laster ned Word, blir boksen med «Prøv på nytt» for
    PDF stående (retro 7, A3). Feilet Word og brukeren laster ned Word (eller trykker «Prøv på
    nytt»), skjules boksen, og fokus flyttes som før."""
    skript = SKRIPT.read_text(encoding="utf-8")
    vakt = "if (feilboks && feilboks.querySelector('a[data-nedlasting=\"' + format + '\"]'))"
    assert vakt in skript
    assert 'feilboks.querySelector("a[data-nedlasting]")' not in skript
    assert skript.index('var format = lenke.getAttribute("data-nedlasting");') < skript.index(vakt)
    etter = skript[skript.index(vakt) :]
    assert etter.index("feilboks.hidden = true;") < etter.index("knapp.focus();")


def test_nfr7_knappene_ved_siden_av_hverandre_og_brytes_i_css():
    """NFR-7/UX-DR16: blokkene står ved siden av hverandre i midten og brytes til under
    hverandre når det er trangt (flex-wrap), med toppen likt. Ingen fast høyde, ingen bredde i
    piksler og ingen nowrap, så det ikke blir rulling sidelengs ved 320 px."""
    css = STIL.read_text(encoding="utf-8")
    nedlasting = css_blokk(css, ".nedlasting")
    for linje in (
        "display: flex;",
        "flex-wrap: wrap;",
        "justify-content: center;",
        "align-items: flex-start;",
    ):
        assert linje in nedlasting
    assert "flex-direction: column;" not in nedlasting
    format_ = css_blokk(css, ".nedlasting-format")
    assert "flex-direction: column;" in format_
    assert "align-items: center;" in format_
    assert "max-width: 100%;" in format_
    assert "min-width: 0;" in format_
    for blokk in (nedlasting, format_, css_blokk(css, ".nedlasting .hovedknapp")):
        assert "height" not in blokk
        assert "nowrap" not in blokk
        assert not re.search(r"(?<!max-)width: \d+px", blokk)


def test_nfr7_gronn_knapp_har_ramme_i_hoykontrast():
    """NFR-7/UX-DR16: i høykontrastmodus forsvinner den grønne fargen, så «Lastet ned»-knappen
    (Word og PDF) har en ramme i CanvasText."""
    css = STIL.read_text(encoding="utf-8")
    hoykontrast = re.search(r"@media \(forced-colors: active\) \{(.*?)\n\}", css, re.S).group(1)
    ferdig = re.search(r"^\s*\.hovedknapp\.ferdig\s*\{(.*?)\}", hoykontrast, re.S | re.M)
    assert "border: 2px solid CanvasText;" in ferdig.group(1)
