"""Tester for de fiktive testdataene og fasitene i testdata/case-*/ (NFR-3, FR-17, FR-38).
Hver test kjøres for hvert testcase (story 4.5). Testene sjekker at filene henger sammen, også
når KI-svarene lages på nytt med scripts/lag_testsvar.py. Ordlyden i gap.json sjekkes derfor
ikke mot fasiten."""

import json
import re
from pathlib import Path

import pytest

from soknad.kjerne.ki_svar import kontroller
from soknad.kjerne.telleregel import tell_treff
from soknad.kjerne.testdata_match import vask

TESTDATA = Path(__file__).parent.parent / "testdata"
CASER = sorted(mappe for mappe in TESTDATA.glob("case-*") if mappe.is_dir())

# Hver test kjøres én gang per testcase, med navnet på caset i test-id-en.
per_case = pytest.mark.parametrize("case", CASER, ids=[case.name for case in CASER])

# «X av Y = Z %» i fasiten.
PROSENTLINJE = re.compile(r"^(\d+) av (\d+) = (\d+) %$", re.MULTILINE)

# Alle e-postadresser i en tekst.
EPOST = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def _les(case: Path, navn: str) -> str:
    return (case / navn).read_text(encoding="utf-8")


def _les_json(case: Path, navn: str):
    return json.loads(_les(case, navn))


def _tabell(tekst: str, overskrift: str) -> list[list[str]]:
    """Radene i tabellen rett under overskriften, uten overskriftsraden og skillelinjen."""
    linjer = tekst.splitlines()
    start = linjer.index(f"## {overskrift}") + 1
    rader = []
    for linje in linjer[start:]:
        if linje.startswith("|"):
            rader.append([celle.strip() for celle in linje.strip().strip("|").split("|")])
        elif linje.startswith("## "):
            break
        elif rader:
            break
    return rader[2:]


def _er_eget_ord(ord_: str, tekst: str) -> bool:
    """Ordet står i teksten uten bokstav, tall eller _ rett foran eller bak."""
    vasket = " ".join(tekst.split()).casefold()
    return re.search(rf"(?<!\w){re.escape(ord_.casefold())}(?!\w)", vasket) is not None


def test_nfr3_det_finnes_minst_to_testcaser():
    """NFR-3 (story 4.5): testdataene har minst to testcaser, så kriteriene ikke bare holder
    for ett eksempel."""
    assert [case.name for case in CASER][:2] == ["case-1-utvikler", "case-2-okonomi"]


def test_nfr3_cv_ene_og_annonsene_er_unike_paa_tvers_av_caser():
    """NFR-3/AD-10 (story 4.5): ingen to caser har samme CV eller samme annonse etter vasken.
    CV-en avgjør caset, og nøkkelordene finnes ut fra annonsen."""
    for navn in ("cv.txt", "annonse.txt"):
        vasket = [vask(_les(case, navn)) for case in CASER]
        assert len(set(vasket)) == len(vasket), navn


@per_case
def test_fr17_fasiten_gir_samme_treff_og_prosent_som_telleregelen(case):
    """FR-17 (suksesskriterium 2): telleregelen gir samme Ja/Nei per nøkkelord og samme
    «X av Y = Z %» som fasiten, og tabellen har nøkkelordene i samme rekkefølge som
    nokkelord.json. Gjelder hvert testcase."""
    fasit = _les(case, "fasit.md")
    nokkelord = _les_json(case, "ki-svar/nokkelord.json")["nokkelord"]
    resultat = tell_treff(nokkelord, _les(case, "cv.txt"))

    tabell = _tabell(fasit, "Nøkkelord")
    assert [rad[0] for rad in tabell] == nokkelord
    assert all(rad[1] in ("Ja", "Nei") for rad in tabell)
    assert tuple(rad[0] for rad in tabell if rad[1] == "Ja") == resultat.treff
    assert tuple(rad[0] for rad in tabell if rad[1] == "Nei") == resultat.ikke_treff

    linjer = PROSENTLINJE.findall(fasit)
    assert len(linjer) == 1
    assert tuple(int(tall) for tall in linjer[0]) == (
        resultat.antall_treff,
        resultat.antall,
        resultat.prosent,
    )
    assert 0 < resultat.prosent < 100


@per_case
def test_fr38_alle_nokkelordene_staar_i_annonsen(case):
    """FR-38: alle nøkkelordene i nokkelord.json gir treff i annonsen, og arbeidsgiveren er
    en tekst som ikke er tom, og som står i annonsen."""
    svar = _les_json(case, "ki-svar/nokkelord.json")
    annonse = _les(case, "annonse.txt")
    assert tell_treff(svar["nokkelord"], annonse).ikke_treff == ()
    arbeidsgiver = svar["arbeidsgiver"]
    assert isinstance(arbeidsgiver, str)
    assert arbeidsgiver.strip()
    assert arbeidsgiver in annonse


@per_case
def test_fr17_hvert_treff_staar_i_cv_en_som_eget_ord(case):
    """FR-17: hvert nøkkelord som er treff, står i CV-en som eget ord. For nøkkelord på 4
    tegn eller mer betyr det at treffet ikke bare kommer fra et lengre ord, som «Java» i
    «JavaScript»."""
    nokkelord = _les_json(case, "ki-svar/nokkelord.json")["nokkelord"]
    cv = _les(case, "cv.txt")
    treff = tell_treff(nokkelord, cv).treff
    assert treff
    assert [ord_ for ord_ in treff if not _er_eget_ord(ord_, cv)] == []


@per_case
def test_fr17_nokkelord_som_mangler_staar_ikke_i_cv_en_i_noen_form(case):
    """FR-17: et nøkkelord som ikke er treff, står ikke i CV-en i noen form, heller ikke inne
    i et lengre ord. Ellers kunne for eksempel «MySQL» i CV-en gitt «SQL = Nei» uten at noen
    merket det, fordi korte nøkkelord bare telles som eget ord."""
    nokkelord = _les_json(case, "ki-svar/nokkelord.json")["nokkelord"]
    cv = _les(case, "cv.txt")
    vasket = " ".join(cv.split()).casefold()
    ikke_treff = tell_treff(nokkelord, cv).ikke_treff
    assert ikke_treff
    assert [ord_ for ord_ in ikke_treff if ord_.casefold() in vasket] == []


@per_case
def test_nfr3_kravtabellen_i_fasiten_har_ja_og_nei(case):
    """NFR-3: tabellen «Krav» i fasiten har rader, hver rad er merket Ja eller Nei, og CV-en
    både dekker og mangler minst ett krav. Ordlyden sammenlignes ikke med gap.json."""
    dekket = [rad[1] for rad in _tabell(_les(case, "fasit.md"), "Krav")]
    assert dekket
    assert all(verdi in ("Ja", "Nei") for verdi in dekket)
    assert "Ja" in dekket
    assert "Nei" in dekket


# De viktige nøkkelordene i fasiten for hvert testcase (suksesskriterium 14). Case 1 er
# bestemt av Kristine 14. november 2026 (story 4.4). Case 2 er foreslått av Claude og
# godkjent av Kristine samme dag (story 4.5).
VIKTIGE_NOKKELORD = {
    "case-1-utvikler": ["Python", "HTML", "CSS", "SQL", "Git", "Linux", "Docker", "førerkort"],
    "case-2-okonomi": [
        "regnskap",
        "Excel",
        "Power BI",
        "regnskapsprogram",
        "lønnskjøring",
        "Python",
    ],
}


def test_fr15_hvert_case_har_viktige_nokkelord():
    """FR-15 (story 4.5): listen over viktige nøkkelord finnes for akkurat de casene som
    finnes i testdata/."""
    assert sorted(VIKTIGE_NOKKELORD) == [case.name for case in CASER]


@per_case
def test_fr15_fasiten_markerer_de_viktige_nokkelordene(case):
    """FR-15 (suksesskriterium 14): tabellen «Viktige nøkkelord» i fasiten har akkurat de
    som er bestemt for caset, og hvert av dem står i annonsen."""
    viktige = [rad[0] for rad in _tabell(_les(case, "fasit.md"), "Viktige nøkkelord")]
    assert viktige == VIKTIGE_NOKKELORD[case.name]
    annonse = _les(case, "annonse.txt")
    assert [ord_ for ord_ in viktige if not _er_eget_ord(ord_, annonse)] == []


@per_case
def test_fr15_nokkelordlisten_har_alle_de_viktige(case):
    """FR-15 (suksesskriterium 14): hvert viktige nøkkelord står som eget ord i minst ett av
    nøkkelordene i nokkelord.json, så «førerkort klasse B» har med «førerkort»."""
    nokkelord = _les_json(case, "ki-svar/nokkelord.json")["nokkelord"]
    viktige = [rad[0] for rad in _tabell(_les(case, "fasit.md"), "Viktige nøkkelord")]
    mangler = [v for v in viktige if not any(_er_eget_ord(v, ord_) for ord_ in nokkelord)]
    assert mangler == []


@per_case
def test_fr38_ki_svarene_har_riktig_form(case):
    """FR-38 (AD-4): KI-svarene er gyldig JSON med akkurat feltene fra AD-4,
    nøkkelordlisten er ikke tom, og dekker og mangler er ikke begge tomme."""
    nokkelord = _les_json(case, "ki-svar/nokkelord.json")
    assert set(nokkelord) == {"nokkelord", "arbeidsgiver"}
    assert isinstance(nokkelord["nokkelord"], list)
    assert nokkelord["nokkelord"]
    assert all(isinstance(ord_, str) and ord_.strip() for ord_ in nokkelord["nokkelord"])
    assert nokkelord["arbeidsgiver"] is None or isinstance(nokkelord["arbeidsgiver"], str)

    gap = _les_json(case, "ki-svar/gap.json")
    assert set(gap) == {"dekker", "mangler"}
    for felt in ("dekker", "mangler"):
        assert isinstance(gap[felt], list)
        assert all(isinstance(krav, str) and krav.strip() for krav in gap[felt])
    assert gap["dekker"] or gap["mangler"]


@per_case
def test_nfr3_alle_epostene_er_fiktive(case):
    """NFR-3: alle e-postadressene i CV-en og annonsen slutter på @example.com."""
    for navn in ("cv.txt", "annonse.txt"):
        adresser = EPOST.findall(_les(case, navn))
        assert adresser
        assert all(adresse.endswith("@example.com") for adresse in adresser)


# De typiske KI-frasene fra addendum til PRD-en (FR-24), skrevet med små bokstaver og uten
# «…». Brevet skal ikke bruke noen av dem.
KI_FRASER = (
    "i dagens raskt skiftende arbeidsmarked",
    "i en verden der",
    "det er med stor glede og entusiasme at jeg søker",
    "jeg skriver for å uttrykke min interesse for",
    "jeg er lidenskapelig opptatt av",
    "jeg er begeistret for muligheten til",
    "drevet av en genuin interesse for",
    "jeg er overbevist om at jeg vil være en verdifull ressurs",
    "med min solide bakgrunn innen",
    "en unik kombinasjon av ferdigheter",
    "landskap",
    "navigere",
    "sømløst",
    "i skjæringspunktet mellom",
    "en spennende reise",
    "jeg ser frem til muligheten til å bidra til deres videre suksess",
    "takk for at du tok deg tid til å lese søknaden min",
)


def test_fr24_ki_fraselisten_har_17_fraser():
    """FR-24: listen har alle de 17 frasene fra addendum, uten duplikater."""
    assert len(set(KI_FRASER)) == len(KI_FRASER) == 17


def test_fr22_fr24_alle_testbrev_bestaar_kontrollen_uten_ki_fraser():
    """FR-22/FR-24/FR-28: hver ki-svar/brev-*.json i hvert testcase består kontroller(), og
    ingen avsnitt bruker frasene fra addendum (uten hensyn til store og små bokstaver)."""
    filer = sorted(TESTDATA.glob("case-*/ki-svar/brev-*.json"))
    for case in CASER:
        assert case / "ki-svar" / "brev-1.json" in filer
        assert case / "ki-svar" / "brev-2.json" in filer
    for fil in filer:
        brev = kontroller("brev", fil.read_text(encoding="utf-8"))
        assert len(brev["avsnitt"]) >= 2, fil
        assert brev["avsnitt"][0].startswith("Søknad på stillingen som "), fil
        tekst = " ".join(" ".join(brev["avsnitt"]).split()).casefold()
        assert [frase for frase in KI_FRASER if frase in tekst] == [], fil


# Ord fra «Sjekkliste for brevet» i fasit.md for hvert testcase: det står ikke i CV-en, så
# brevet kan ikke påstå det.
SJEKKLISTE_ORD = {
    "case-1-utvikler": ("sql", "database", "docker", "scrum", "smidig", "førerkort"),
    "case-2-okonomi": ("power bi", "tripletex", "regnskapsprogram", "lønn", "python", "programmer"),
}


def test_fr37_hvert_case_har_ord_fra_sjekklisten():
    """FR-37 (story 4.5): ordene fra sjekklisten finnes for akkurat de casene som finnes."""
    assert sorted(SJEKKLISTE_ORD) == [case.name for case in CASER]


@per_case
def test_fr37_testbrevene_har_ingen_pastander_fra_sjekklisten(case):
    """FR-37: brev-1.json og brev-2.json har ingen av ordene fra sjekklisten i fasit.md. For
    case 1: SQL, databaser, Docker, Scrum, smidig utvikling, førerkort. For case 2: Power BI,
    Tripletex og andre regnskapsprogram, lønn, Python og programmering. Punktene om graden og
    tidligere jobb har ingen ord å søke etter, og sjekkes for hånd (testplanen).

    Testen søker etter deler av ord og er streng med vilje (story 4.4): «lønn» gir også treff
    i «lønnsom», og «regnskapsprogram» i «opplæring i regnskapsprogrammene». Feiler den etter en
    ny kjøring, vurderes brevet for hånd før det blir plan B."""
    for navn in ("ki-svar/brev-1.json", "ki-svar/brev-2.json"):
        brev = kontroller("brev", _les(case, navn))
        tekst = " ".join(brev["avsnitt"]).casefold()
        assert [ord_ for ord_ in SJEKKLISTE_ORD[case.name] if ord_ in tekst] == [], navn


# Inndataene for kriterium 3 (story 4.5): CV-en fra case 1 og annonsen fra case 2.
KRITERIUM_3 = TESTDATA.parents[1] / "my-project" / "testkjoringer" / "4-5" / "inndata"


def test_fr22_inndataene_for_kriterium_3_er_like_testdataene():
    """FR-22 (suksesskriterium 3, story 4.5): kopiene i my-project/testkjoringer/4-5/inndata/
    er nøyaktig CV-en fra case 1 og annonsen fra case 2. Endres testdataene, feiler testen,
    så kriterium 3 aldri kjøres med gamle tekster."""
    mappe = KRITERIUM_3 / "case-1-cv-med-annonse-2"
    assert _les(mappe, "cv.txt") == _les(TESTDATA / "case-1-utvikler", "cv.txt")
    assert _les(mappe, "annonse.txt") == _les(TESTDATA / "case-2-okonomi", "annonse.txt")
