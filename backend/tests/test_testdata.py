"""Tester for de fiktive testdataene og fasiten i testdata/case-1-utvikler/ (NFR-3, FR-17,
FR-38). Testene sjekker at filene henger sammen, også når de håndlagde KI-svarene byttes ut
med ekte KI-svar i Epic 4. Ordlyden i gap.json sjekkes derfor ikke mot fasiten."""

import json
import re
from pathlib import Path

from soknad.kjerne.ki_svar import kontroller
from soknad.kjerne.telleregel import tell_treff

CASE = Path(__file__).parent.parent / "testdata" / "case-1-utvikler"

# «X av Y = Z %» i fasiten.
PROSENTLINJE = re.compile(r"^(\d+) av (\d+) = (\d+) %$", re.MULTILINE)

# Alle e-postadresser i en tekst.
EPOST = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def _les(navn: str) -> str:
    return (CASE / navn).read_text(encoding="utf-8")


def _les_json(navn: str):
    return json.loads(_les(navn))


def _tabell(tekst: str, overskrift: str) -> list[list[str]]:
    """Radene i tabellen rett under overskriften, uten overskriftsraden og skillelinjen."""
    linjer = tekst.splitlines()
    start = linjer.index(f"## {overskrift}") + 1
    rader = []
    for linje in linjer[start:]:
        if linje.startswith("|"):
            rader.append([celle.strip() for celle in linje.strip().strip("|").split("|")])
        elif rader:
            break
    return rader[2:]


def _er_eget_ord(ord_: str, tekst: str) -> bool:
    """Ordet står i teksten uten bokstav, tall eller _ rett foran eller bak."""
    vasket = " ".join(tekst.split()).casefold()
    return re.search(rf"(?<!\w){re.escape(ord_.casefold())}(?!\w)", vasket) is not None


def test_fr17_fasiten_gir_samme_treff_og_prosent_som_telleregelen():
    """FR-17 (suksesskriterium 2): telleregelen gir samme Ja/Nei per nøkkelord og samme
    «X av Y = Z %» som fasiten, og tabellen har nøkkelordene i samme rekkefølge som
    nokkelord.json."""
    fasit = _les("fasit.md")
    nokkelord = _les_json("ki-svar/nokkelord.json")["nokkelord"]
    resultat = tell_treff(nokkelord, _les("cv.txt"))

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


def test_fr38_alle_nokkelordene_staar_i_annonsen():
    """FR-38: alle nøkkelordene i nokkelord.json gir treff i annonsen, og arbeidsgiveren er
    en tekst som ikke er tom, og som står i annonsen."""
    svar = _les_json("ki-svar/nokkelord.json")
    annonse = _les("annonse.txt")
    assert tell_treff(svar["nokkelord"], annonse).ikke_treff == ()
    arbeidsgiver = svar["arbeidsgiver"]
    assert isinstance(arbeidsgiver, str)
    assert arbeidsgiver.strip()
    assert arbeidsgiver in annonse


def test_fr17_hvert_treff_staar_i_cv_en_som_eget_ord():
    """FR-17: hvert nøkkelord som er treff, står i CV-en som eget ord. For nøkkelord på 4
    tegn eller mer betyr det at treffet ikke bare kommer fra et lengre ord, som «Java» i
    «JavaScript»."""
    nokkelord = _les_json("ki-svar/nokkelord.json")["nokkelord"]
    cv = _les("cv.txt")
    treff = tell_treff(nokkelord, cv).treff
    assert treff
    assert [ord_ for ord_ in treff if not _er_eget_ord(ord_, cv)] == []


def test_fr17_nokkelord_som_mangler_staar_ikke_i_cv_en_i_noen_form():
    """FR-17: et nøkkelord som ikke er treff, står ikke i CV-en i noen form, heller ikke inne
    i et lengre ord. Ellers kunne for eksempel «MySQL» i CV-en gitt «SQL = Nei» uten at noen
    merket det, fordi korte nøkkelord bare telles som eget ord."""
    nokkelord = _les_json("ki-svar/nokkelord.json")["nokkelord"]
    cv = _les("cv.txt")
    vasket = " ".join(cv.split()).casefold()
    ikke_treff = tell_treff(nokkelord, cv).ikke_treff
    assert ikke_treff
    assert [ord_ for ord_ in ikke_treff if ord_.casefold() in vasket] == []


def test_nfr3_kravtabellen_i_fasiten_har_ja_og_nei():
    """NFR-3: tabellen «Krav» i fasiten har rader, hver rad er merket Ja eller Nei, og CV-en
    både dekker og mangler minst ett krav. Ordlyden sammenlignes ikke med gap.json."""
    dekket = [rad[1] for rad in _tabell(_les("fasit.md"), "Krav")]
    assert dekket
    assert all(verdi in ("Ja", "Nei") for verdi in dekket)
    assert "Ja" in dekket
    assert "Nei" in dekket


def test_fr38_ki_svarene_har_riktig_form():
    """FR-38 (AD-4): de håndlagde KI-svarene er gyldig JSON med akkurat feltene fra AD-4,
    nøkkelordlisten er ikke tom, og dekker og mangler er ikke begge tomme."""
    nokkelord = _les_json("ki-svar/nokkelord.json")
    assert set(nokkelord) == {"nokkelord", "arbeidsgiver"}
    assert isinstance(nokkelord["nokkelord"], list)
    assert nokkelord["nokkelord"]
    assert all(isinstance(ord_, str) and ord_.strip() for ord_ in nokkelord["nokkelord"])
    assert nokkelord["arbeidsgiver"] is None or isinstance(nokkelord["arbeidsgiver"], str)

    gap = _les_json("ki-svar/gap.json")
    assert set(gap) == {"dekker", "mangler"}
    for felt in ("dekker", "mangler"):
        assert isinstance(gap[felt], list)
        assert all(isinstance(krav, str) and krav.strip() for krav in gap[felt])
    assert gap["dekker"] or gap["mangler"]


def test_nfr3_alle_epostene_er_fiktive():
    """NFR-3: alle e-postadressene i CV-en og annonsen slutter på @example.com."""
    for navn in ("cv.txt", "annonse.txt"):
        adresser = EPOST.findall(_les(navn))
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


def test_fr22_fr24_testbrevet_bestaar_kontrollen_uten_ki_fraser():
    """FR-22/FR-24/FR-28: brev-1.json består kontroller(), og ingen avsnitt bruker frasene
    fra addendum."""
    brev = kontroller("brev", _les("ki-svar/brev-1.json"))
    assert len(brev["avsnitt"]) >= 2
    tekst = " ".join(" ".join(brev["avsnitt"]).split()).casefold()
    assert [frase for frase in KI_FRASER if frase in tekst] == []


# Ord fra «Sjekkliste for brevet» i fasit.md: det står ikke i CV-en, så brevet kan ikke
# påstå det.
SJEKKLISTE_ORD = ("sql", "database", "docker", "scrum", "smidig", "førerkort")


def test_fr37_testbrevet_har_ingen_pastander_fra_sjekklisten():
    """FR-37: brev-1.json nevner ingenting fra sjekklisten i fasit.md (SQL, databaser, Docker,
    Scrum, smidig utvikling, førerkort)."""
    brev = kontroller("brev", _les("ki-svar/brev-1.json"))
    tekst = " ".join(brev["avsnitt"]).casefold()
    assert [ord_ for ord_ in SJEKKLISTE_ORD if ord_ in tekst] == []
