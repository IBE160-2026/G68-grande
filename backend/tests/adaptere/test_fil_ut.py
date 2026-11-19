"""Tester for Word- og PDF-filen til nedlastingen (FR-29, FR-30, NFR-9, AD-11). Story 3.2
(Word) og 7.2 (PDF). Word-filen åpnes med python-docx og PDF-filen med pypdf, som filene
brukeren laster ned."""

import json
from io import BytesIO

import pytest
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader
from pypdf.generic import ContentStream

from soknad.adaptere import fil_ut
from soknad.adaptere.fil_ut import lag_docx, lag_pdf
from soknad.kjerne.feil import FilFeil
from soknad.kjerne.ki_svar import hele_brevet, kontroller

AVSNITT = [
    "Jeg søker stillingen som junior utvikler.",
    "Jeg har æ, ø og å, «sitattegn» og – tankestrek.",
    "Med vennlig hilsen",
    "Sara Eksempel",
]


def _apne(innhold: bytes):
    return Document(BytesIO(innhold))


def test_fr30_filen_har_bare_avsnittene_fra_brevet():
    """FR-30/NFR-9: ett avsnitt per element, i samme rekkefølge og med samme tekst (også æøå),
    og ingen tabeller eller andre avsnitt."""
    dokument = _apne(lag_docx(AVSNITT))
    assert [p.text for p in dokument.paragraphs] == AVSNITT
    assert dokument.tables == []


def test_fr30_filen_har_ingen_topp_eller_bunntekst():
    """FR-30/NFR-9: ingen seksjon har egen topp- eller bunntekst, og de er tomme."""
    dokument = _apne(lag_docx(AVSNITT))
    for seksjon in dokument.sections:
        for del_ in (
            seksjon.header,
            seksjon.footer,
            seksjon.first_page_header,
            seksjon.first_page_footer,
            seksjon.even_page_header,
            seksjon.even_page_footer,
        ):
            assert del_.is_linked_to_previous
            assert all(not p.text for p in del_.paragraphs)


def test_fr30_filen_har_ingen_markeringer():
    """FR-30: teksten er vanlig tekst, uten fet, kursiv, understreking eller farge."""
    dokument = _apne(lag_docx(AVSNITT))
    for avsnitt in dokument.paragraphs:
        for bit in avsnitt.runs:
            assert not bit.bold
            assert not bit.italic
            assert not bit.underline
            assert bit.font.color.rgb is None


def test_nfr4_filens_egenskaper_er_tomme():
    """NFR-4/FR-30: forfatter, tittel og kommentar i filens egenskaper er tomme."""
    egenskaper = _apne(lag_docx(AVSNITT)).core_properties
    assert egenskaper.author == ""
    assert egenskaper.last_modified_by == ""
    assert egenskaper.title == ""
    assert egenskaper.comments == ""


def test_fr29_filen_er_a4_og_norsk():
    """FR-29: siden er A4 (ikke amerikansk Letter), og språket er norsk bokmål, så Word ikke
    markerer brevet som stavefeil."""
    dokument = _apne(lag_docx(AVSNITT))
    for seksjon in dokument.sections:
        assert round(seksjon.page_width.mm) == 210
        assert round(seksjon.page_height.mm) == 297
    sprak = [e.get(qn("w:val")) for e in dokument.styles.element.iter(qn("w:lang"))]
    assert sprak
    assert set(sprak) == {"nb-NO"}


def test_fr29_filen_har_2_5_cm_marger():
    """FR-29: margen er 2,5 cm (25 mm) oppe, nede, til venstre og til høyre, ikke de
    amerikanske margene fra malen (25,4 mm og 31,75 mm). Kristine bestemte 2,5 cm 2026-11-12
    i retrospektiven for epic 3."""
    dokument = _apne(lag_docx(AVSNITT))
    assert dokument.sections
    for seksjon in dokument.sections:
        marger = (
            seksjon.top_margin,
            seksjon.bottom_margin,
            seksjon.left_margin,
            seksjon.right_margin,
        )
        assert [round(m.mm, 1) for m in marger] == [25.0, 25.0, 25.0, 25.0]


@pytest.mark.parametrize("tekst", ["null\x00tegn", "kontroll\x0btegn"])
def test_fr29_tegn_word_ikke_taler_gir_filfeil(tekst):
    """FR-29/AD-9: et tegn Word ikke tåler, gir FilFeil, ikke et annet unntak."""
    with pytest.raises(FilFeil):
        lag_docx(["Første avsnitt.", tekst])


def test_fr30_brev_med_kontrolltegn_gar_gjennom_kontroller_og_lag_docx():
    """FR-30/FR-28 (story 4.2): et brev med \\u000b, \\n og \\t går gjennom kontroller() og
    så lag_docx() uten FilFeil, og avsnittene i fila er like hele_brevet(), med hilsenen og det
    rensede navnet til slutt."""
    tekst = json.dumps(
        {
            "avsnitt": [
                "Jeg søker\nstillingen\tsom junior utvikler.",
                "Jeg kan Python\u000b og Flask.\r\n",
                "\u0000",
            ],
            "navn": "Sara\u000b Eksempel\n",
        }
    )
    avsnitt = hele_brevet(kontroller("brev", tekst))
    assert avsnitt == [
        "Jeg søker stillingen som junior utvikler.",
        "Jeg kan Python og Flask.",
        "Med vennlig hilsen",
        "Sara Eksempel",
    ]
    dokument = _apne(lag_docx(avsnitt))
    assert [p.text for p in dokument.paragraphs] == avsnitt


# --- PDF (story 7.2) ---

# Punkter per millimeter i PDF (72 punkter per tomme, 25,4 mm per tomme).
PT_PER_MM = 72 / 25.4


def _pdf(innhold: bytes) -> PdfReader:
    return PdfReader(BytesIO(innhold))


def _slaa_sammen(tekst: str) -> str:
    """Mellomrom og linjeskift slått sammen til ett mellomrom, så linjebrytingen i PDF-en ikke
    teller."""
    return " ".join(tekst.split())


def _pdf_tekst(innhold: bytes) -> str:
    return _slaa_sammen(" ".join(side.extract_text() for side in _pdf(innhold).pages))


def test_fr30_pdf_teksten_er_lik_avsnittene_med_aeoeaa():
    """FR-30/NFR-9: teksten i PDF-en (lest med pypdf) er avsnittene etter hverandre, i samme
    rekkefølge og med æ, ø, å, «sitattegn» og tankestrek, og ingenting annet (ingen topp- eller
    bunntekst)."""
    innhold = lag_pdf(AVSNITT)
    assert innhold.startswith(b"%PDF-")
    assert _pdf_tekst(innhold) == _slaa_sammen(" ".join(AVSNITT))
    assert "æ, ø og å" in _pdf_tekst(innhold)


def test_fr30_pdf_avsnittene_staar_paa_egne_linjer():
    """FR-30: hvert avsnitt begynner på en ny linje, så hilsenen og navnet står for seg."""
    linjer = _pdf(lag_pdf(AVSNITT)).pages[0].extract_text().splitlines()
    assert [linje.strip() for linje in linjer] == AVSNITT


def test_fr29_pdf_er_a4_med_2_5_cm_marg():
    """FR-29: siden er A4 (210 × 297 mm), og teksten begynner 25 mm fra venstre og fra toppen,
    som margen i Word-fila."""
    leser = _pdf(lag_pdf(AVSNITT))
    side = leser.pages[0]
    assert round(float(side.mediabox.width) / PT_PER_MM) == 210
    assert round(float(side.mediabox.height) / PT_PER_MM) == 297
    posisjoner = []

    def besok(tekst, cm, tm, font_dict, font_size):
        if tekst.strip():
            posisjoner.append((tm[4], tm[5]))

    side.extract_text(visitor_text=besok)
    venstre = min(x for x, _ in posisjoner) / PT_PER_MM
    hoyeste = max(y for _, y in posisjoner) / PT_PER_MM
    assert venstre == pytest.approx(25, abs=0.5)
    # Grunnlinjen i første linje står litt under toppmargen (25 mm).
    assert 25 < 297 - hoyeste < 32


def test_fr29_pdf_er_norsk_med_noto_sans_11_pt():
    """FR-29: språket i PDF-en er norsk bokmål, og skriften er Noto Sans i 11 pt (bestemt av
    Kristine 19. november 2026), lagt inn i filen."""
    leser = _pdf(lag_pdf(AVSNITT))
    assert leser.trailer["/Root"]["/Lang"] == "nb-NO"
    skrifter = leser.pages[0]["/Resources"]["/Font"]
    navn = [str(skrift.get_object()["/BaseFont"]) for skrift in skrifter.values()]
    assert navn
    assert all(n.endswith("NotoSans") for n in navn)
    operasjoner = ContentStream(leser.pages[0].get_contents(), leser).operations
    storrelser = {float(operander[1]) for operander, op in operasjoner if op == b"Tf"}
    assert storrelser == {11}


def test_fr29_skriften_ligger_lokalt_med_lisensen():
    """AD-11: skriften ligger i soknad/fonts/ med lisensfilen (OFL) ved siden av."""
    assert fil_ut.SKRIFT.is_file()
    assert fil_ut.SKRIFT.name == "NotoSans-Regular.ttf"
    lisens = (fil_ut.SKRIFT.parent / "OFL.txt").read_text(encoding="utf-8")
    assert "SIL Open Font License" in lisens


def test_fr30_lang_pdf_gir_flere_sider_uten_at_tekst_forsvinner():
    """FR-30: et langt brev fortsetter på neste side, og hele teksten er med."""
    avsnitt = [
        f"Avsnitt {nummer}: " + "Jeg har erfaring med Python og Flask. " * 8 for nummer in range(12)
    ]
    innhold = lag_pdf(avsnitt)
    assert len(_pdf(innhold).pages) > 1
    assert _pdf_tekst(innhold) == _slaa_sammen(" ".join(avsnitt))


def test_nfr4_pdf_metadata_er_tomme():
    """NFR-4/FR-30: forfatter, tittel, emne, laget av og produsent er tomme, så filen ikke
    sier «fpdf2» eller noe om brukeren."""
    metadata = _pdf(lag_pdf(AVSNITT)).metadata or {}
    for felt in ("/Author", "/Title", "/Subject", "/Creator", "/Producer", "/Keywords"):
        assert not metadata.get(felt), felt
    assert b"fpdf" not in lag_pdf(AVSNITT).lower()


def test_fr30_pdf_har_ingen_markeringer():
    """FR-30: bare tekst i én skrift og standardfargen (svart): ingen farger, streker
    (understreking), rammer eller lenker. Operasjonene på siden er bare tekst."""
    leser = _pdf(lag_pdf(AVSNITT))
    side = leser.pages[0]
    assert "/Annots" not in side
    operasjoner = {op for _, op in ContentStream(side.get_contents(), leser).operations}
    assert operasjoner <= {b"J", b"w", b"BT", b"Tf", b"ET", b"Td", b"Tj"}
    assert {b"BT", b"Tf", b"Td", b"Tj"} <= operasjoner


def test_fr30_pdf_med_tegn_skriften_ikke_har_gir_ingen_feil():
    """FR-30: et tegn som ikke finnes i skriften (for eksempel emoji), gir ingen feil, men vises
    ikke. Resten av teksten er med (står i README under «Kjente begrensninger»)."""
    innhold = lag_pdf(["Jeg gleder meg \U0001f600 til å høre fra dere."])
    assert _pdf_tekst(innhold) == "Jeg gleder meg til å høre fra dere."


def test_fr29_pdf_uten_skrift_gir_filfeil(monkeypatch, tmp_path):
    """FR-29/AD-9: kan PDF-en ikke lages (her fordi skriften mangler), gir den FilFeil, ikke et
    annet unntak."""
    monkeypatch.setattr(fil_ut, "SKRIFT", tmp_path / "finnes-ikke.ttf")
    with pytest.raises(FilFeil):
        lag_pdf(AVSNITT)


def test_fr29_pdf_med_feil_type_gir_filfeil():
    """FR-29/AD-9: noe annet enn tekst i avsnittene gir FilFeil."""
    with pytest.raises(FilFeil):
        lag_pdf([None])


def test_fr30_pdf_lik_word_for_brev_fra_kontroller():
    """FR-30: et brev som har gått gjennom kontroller() og hele_brevet(), gir samme tekst i PDF
    som i Word-fila."""
    avsnitt = hele_brevet(
        kontroller("brev", json.dumps({"avsnitt": ["Jeg søker\nstillingen."], "navn": "Sara"}))
    )
    word = [p.text for p in _apne(lag_docx(avsnitt)).paragraphs]
    assert word == avsnitt
    assert _pdf_tekst(lag_pdf(avsnitt)) == _slaa_sammen(" ".join(word))
