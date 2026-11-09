"""Tester for gjenkjenning av testdata i testmodus (FR-34, AD-10). Kjernetestene leser ingen
filer, så casene lages av tekst her."""

from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.testdata_match import case_for_annonse, finn_case, lag_testcase, vask

CV = "Sara Eksempel\nStudent, bachelor i IT\n\nKan Python og Flask."
ANNONSE = "Junior utvikler hos Testvik Utvikling AS.\nVi søker deg som kan SQL."
CASER = [
    lag_testcase("case-1-utvikler", CV, ANNONSE),
    lag_testcase("case-2-annet", "En helt annen CV", "En helt annen annonse"),
]

IKKE_TESTDATA_CV = InndataFeil("cv", FeilType.IKKE_TESTDATA)
IKKE_TESTDATA_ANNONSE = InndataFeil("annonse", FeilType.IKKE_TESTDATA)


def test_fr34_vask_fjerner_alt_annet_enn_bokstaver_og_tall():
    """FR-34: vask gjør casefold() og beholder bare bokstaver og tall, også æøå."""
    assert vask("Hei, Ærlige Øyvind!\n\tÅ 12 3.") == "heiærligeøyvindå123"


def test_fr34_vask_gjor_nfkc():
    """FR-34: vask gjør Unicode NFKC, så for eksempel «ﬁ» og «①» blir «fi» og «1»."""
    assert vask("ﬁl ①") == "fil1"
    # «å» som a + ring over (to tegn) blir det samme som «å» (ett tegn).
    assert vask("å") == vask("å")


def test_fr34_samme_tekst_med_mellomrom_linjeskift_og_store_bokstaver():
    """FR-34: ekstra mellomrom, linjeskift og store bokstaver gir samme case."""
    cv = "  " + CV.upper().replace(" ", "   ").replace("\n", "\r\n\n") + "\n"
    annonse = ANNONSE.replace("\n", " ").upper() + "   "
    assert finn_case(cv, annonse, CASER) == ("case-1-utvikler", [])


def test_fr34_cv_som_ikke_er_testdata_gir_feil_pa_cv():
    """FR-34: en egen CV med annonsen fra et case gir ikke_testdata bare på CV-feltet."""
    assert finn_case("Min egen CV", ANNONSE, CASER) == (None, [IKKE_TESTDATA_CV])


def test_fr34_annonse_fra_feil_sted_gir_feil_pa_annonsen():
    """FR-34: CV-en avgjør caset. En egen annonse gir ikke_testdata på annonsefeltet."""
    assert finn_case(CV, "Min egen annonse", CASER) == (None, [IKKE_TESTDATA_ANNONSE])


def test_fr34_annonse_fra_et_annet_case_gir_feil_pa_annonsen():
    """FR-34: annonsen må høre til samme case som CV-en."""
    assert finn_case(CV, "En helt annen annonse", CASER) == (None, [IKKE_TESTDATA_ANNONSE])


def test_fr34_begge_feil_gir_feil_pa_begge_feltene():
    """FR-34: alle feilene kommer samtidig, cv først."""
    assert finn_case("Min egen CV", "Min egen annonse", CASER) == (
        None,
        [IKKE_TESTDATA_CV, IKKE_TESTDATA_ANNONSE],
    )


def test_fr34_tomt_felt_gir_ingen_ikke_testdata():
    """FR-34/AD-9: tom sjekkes først (story 2.5), så et tomt felt får ingen ikke_testdata."""
    assert finn_case(CV, "", CASER) == (None, [])
    assert finn_case(CV, "  \n\t ", CASER) == (None, [])
    assert finn_case("", ANNONSE, CASER) == (None, [])
    assert finn_case("", "Min egen annonse", CASER) == (None, [IKKE_TESTDATA_ANNONSE])
    assert finn_case("Min egen CV", " ", CASER) == (None, [IKKE_TESTDATA_CV])


def test_fr34_case_for_annonse():
    """FR-34: nøkkelordene har bare annonsen, så caset kan finnes ut fra den alene."""
    assert case_for_annonse(ANNONSE.upper(), CASER) == "case-1-utvikler"
    assert case_for_annonse("Min egen annonse", CASER) is None
