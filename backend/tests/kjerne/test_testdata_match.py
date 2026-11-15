"""Tester for gjenkjenning av testdata i testmodus (FR-34, AD-10). Kjernetestene leser ingen
filer, så casene lages av tekst her."""

from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.testdata_match import case_for_annonse, finn_case, lag_testcase, vask

CV = "Sara Eksempel\nStudent, bachelor i IT\n\nKan Python og Flask."
ANNONSE = "Junior utvikler hos Testvik Utvikling AS.\nVi søker deg som kan SQL."
# Bare case 1 har et eget brev til Korrektur, som i testdata/ (story 5.1).
BREV = "Hei!\n\nJeg er lidenskapelig opptatt av nettsider.\n\nMed vennlig hilsen\nSara"
CV_2 = "En helt annen CV"
ANNONSE_2 = "En helt annen annonse"
CASER = [
    lag_testcase("case-1-utvikler", CV, ANNONSE, BREV),
    lag_testcase("case-2-annet", CV_2, ANNONSE_2),
]

IKKE_TESTDATA_CV = InndataFeil("cv", FeilType.IKKE_TESTDATA)
IKKE_TESTDATA_ANNONSE = InndataFeil("annonse", FeilType.IKKE_TESTDATA)
IKKE_TESTDATA_BREV = InndataFeil("eget_brev", FeilType.IKKE_TESTDATA)


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


def test_fr34_annonse_fra_et_annet_case_gir_annen_case_pa_annonsen():
    """FR-34 (story 4.5): annonsen må høre til samme case som CV-en. Er den annonsen i et
    annet case, får annonsefeltet annen_case, ikke ikke_testdata."""
    assert finn_case(CV, "En helt annen annonse", CASER) == (
        None,
        [InndataFeil("annonse", FeilType.ANNEN_CASE)],
    )
    # Med rotete tekst er det fortsatt annonsen i det andre caset.
    assert finn_case(CV, "  EN HELT\nANNEN annonse ", CASER) == (
        None,
        [InndataFeil("annonse", FeilType.ANNEN_CASE)],
    )


def test_fr34_ukjent_cv_og_annonse_fra_et_case_gir_bare_feil_pa_cv():
    """FR-34 (story 4.5): er CV-en ukjent, gjelder ikke annen_case. Annonsen er testdata og
    får ingen feil."""
    assert finn_case("Min egen CV", "En helt annen annonse", CASER) == (None, [IKKE_TESTDATA_CV])


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


# --- Eget brev i Korrektur (story 5.1) ---


def test_fr34_lag_testcase_vasker_brevet():
    """FR-34 (story 5.1): brevet lagres vasket, og et case uten brev har eget_brev None."""
    assert CASER[0].eget_brev == vask(BREV)
    assert CASER[1].eget_brev is None


def test_fr34_brevet_fra_caset_gir_caset():
    """FR-34 (story 5.1): CV, annonse og brev fra case 1 gir case 1, også med rotete tekst."""
    assert finn_case(CV, ANNONSE, CASER, eget_brev=BREV) == ("case-1-utvikler", [])
    rotete = "  " + BREV.upper().replace("\n", "\r\n\n") + "  "
    assert finn_case(CV, ANNONSE, CASER, eget_brev=rotete) == ("case-1-utvikler", [])


def test_fr34_ukjent_brev_gir_feil_pa_brevet():
    """FR-34 (story 5.1): et eget brev som ikke er testdata, gir ikke_testdata på
    brevfeltet."""
    assert finn_case(CV, ANNONSE, CASER, eget_brev="Mitt eget brev") == (
        None,
        [IKKE_TESTDATA_BREV],
    )


def test_fr34_case_uten_brev_gir_feil_pa_brevet():
    """FR-34 (story 5.1, bestemt av Kristine 15. november 2026): CV og annonse fra case 2,
    som ikke har noe brev, gir den vanlige ikke_testdata på brevfeltet, også med brevet fra
    case 1. Ingen ny feiltype."""
    assert finn_case(CV_2, ANNONSE_2, CASER, eget_brev=BREV) == (None, [IKKE_TESTDATA_BREV])
    assert finn_case(CV_2, ANNONSE_2, CASER, eget_brev="Mitt brev") == (
        None,
        [IKKE_TESTDATA_BREV],
    )


def test_fr34_ukjent_cv_gir_feil_pa_brevet_bare_naar_det_ikke_er_testdata():
    """FR-34 (story 5.1): er CV-en ukjent, får brevet feil bare hvis det ikke er brevet i noe
    case, som annonsen. Feilene kommer i rekkefølgen cv, eget_brev, annonse."""
    assert finn_case("Min egen CV", ANNONSE, CASER, eget_brev=BREV) == (None, [IKKE_TESTDATA_CV])
    assert finn_case("Min egen CV", "Min egen annonse", CASER, eget_brev="Mitt brev") == (
        None,
        [IKKE_TESTDATA_CV, IKKE_TESTDATA_BREV, IKKE_TESTDATA_ANNONSE],
    )


def test_fr34_tomt_brev_gir_ingen_ikke_testdata():
    """FR-34/AD-9 (story 5.1): et tomt brevfelt får ingen ikke_testdata, men gir heller ikke
    noe case."""
    assert finn_case(CV, ANNONSE, CASER, eget_brev="") == (None, [])
    assert finn_case(CV, ANNONSE, CASER, eget_brev=" \n\t") == (None, [])
    assert finn_case(CV_2, ANNONSE_2, CASER, eget_brev="") == (None, [])
    assert finn_case("Min egen CV", ANNONSE, CASER, eget_brev="") == (None, [IKKE_TESTDATA_CV])


def test_fr34_uten_brev_sjekkes_ikke_brevet():
    """FR-34 (story 5.1): i Full generering (eget_brev None) sjekkes ikke brevet, så case 2
    gir case 2 som før."""
    assert finn_case(CV_2, ANNONSE_2, CASER) == ("case-2-annet", [])


def test_fr34_case_for_annonse():
    """FR-34: nøkkelordene har bare annonsen, så caset kan finnes ut fra den alene."""
    assert case_for_annonse(ANNONSE.upper(), CASER) == "case-1-utvikler"
    assert case_for_annonse("Min egen annonse", CASER) is None
