"""Lager de ferdige svarene i testmodus med ekte KI (FR-38, AD-4).

Skriptet kjører EkteKI på hvert testcase i testdata/ og skriver nokkelord.json, gap.json,
brev-1.json og brev-2.json i testdata/<case>/ki-svar/. Har caset et eget-brev.txt (Korrektur,
bare case 1), skrives også korrektur-1.json og korrektur-2.json. Filene har bare objektet fra
AD-4, slik kontroller() i kjerne/ki_svar gir det. Feiler et KI-kall i et testcase, skrives
ingenting for det caset, og skriptet ender med feilkode. Tokens og anslått pris for hvert kall
står i terminalen (fra loggen i adaptere/ki.py).

Kjøres fra backend/ (API-nøkkelen leses fra backend/.env):

    uv run python -m scripts.lag_testsvar
    uv run python -m scripts.lag_testsvar --ut ../my-project/testkjoringer/4-4/kjoring-2
    uv run python -m scripts.lag_testsvar --case case-2-okonomi
    uv run python -m scripts.lag_testsvar --testdata ../my-project/testkjoringer/4-5/inndata
    uv run python -m scripts.lag_testsvar --case case-1-utvikler --bare-korrektur

--case kjører bare ett testcase. --testdata leser testcasene fra en annen mappe, for eksempel
CV-en fra ett case sammen med annonsen fra et annet (kriterium 3). Uten --ut skrives svarene
da i <mappe>/<case>/ki-svar/. --bare-korrektur lager bare korrektur-1.json og
korrektur-2.json (2 kall per case med eget-brev.txt), så de sjekkede brev-, gap- og
nøkkelordsvarene ikke lages på nytt. Caser uten eget-brev.txt hoppes da over.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

import soknad
from soknad.adaptere.ki import KI, TESTDATA_MAPPE, EkteKI
from soknad.innstillinger import STANDARD_MODELL
from soknad.kjerne.feil import KIFeil

# Feilkoder: 1 når et testcase ikke ble skrevet, 2 når API-nøkkelen mangler, 3 når testcaset
# i --case ikke finnes, når mappen ikke har noen testcaser, eller når ingen av testcasene har
# eget-brev.txt med --bare-korrektur.
KI_FEILET = 1
MANGLER_NOKKEL = 2
UKJENT_CASE = 3


def lag_svar(
    ki: KI, cv: str, annonse: str, eget_brev: str | None = None, bare_korrektur: bool = False
) -> dict[str, dict]:
    """Alle svarene for ett testcase, med filnavnet (uten .json) som nøkkel. brev-2 og
    korrektur-2 er det andre forslaget («Nytt forslag» i Epic 7). korrektur-1 og korrektur-2
    lages bare når caset har et eget brev. bare_korrektur gir bare dem."""
    svar = {}
    if not bare_korrektur:
        svar["nokkelord"] = ki.nokkelord(annonse)
        svar["gap"] = ki.gap(cv, annonse)
        svar["brev-1"] = ki.brev(cv, annonse, forslag=1)
        svar["brev-2"] = ki.brev(cv, annonse, forslag=2)
    if eget_brev is not None:
        svar["korrektur-1"] = ki.korrektur(cv, annonse, eget_brev, forslag=1)
        svar["korrektur-2"] = ki.korrektur(cv, annonse, eget_brev, forslag=2)
    return svar


def skriv_svar(mappe: Path, svar: dict[str, dict]) -> None:
    """Skriver hvert svar som <navn>.json, med æøå som vanlige tegn og linjeskift til slutt."""
    mappe.mkdir(parents=True, exist_ok=True)
    for navn, objekt in svar.items():
        tekst = json.dumps(objekt, ensure_ascii=False, indent=2) + "\n"
        (mappe / f"{navn}.json").write_text(tekst, encoding="utf-8")


def finn_caser(testdata: Path, navn: str | None = None) -> list[Path]:
    """Case-mappene i testdata, sortert på navn. Med navn bare den mappen (tom liste når den
    ikke finnes)."""
    caser = sorted(mappe for mappe in testdata.glob("case-*") if mappe.is_dir())
    return [case for case in caser if navn is None or case.name == navn]


def _eget_brev(case: Path) -> str | None:
    """Teksten i eget-brev.txt, eller None når caset ikke har noe eget brev."""
    fil = case / "eget-brev.txt"
    return fil.read_text(encoding="utf-8") if fil.is_file() else None


def lag_testsvar(
    ki: KI,
    testdata: Path = TESTDATA_MAPPE,
    ut: Path | None = None,
    case_navn: str | None = None,
    bare_korrektur: bool = False,
) -> bool:
    """Kjører KI-en på hvert testcase (eller bare case_navn) og skriver svarene i
    <case>/ki-svar/, eller i <ut>/<case>/ når ut er gitt. Med bare_korrektur lages bare
    korrektur-1 og korrektur-2, og caser uten eget-brev.txt hoppes over. Gir False når minst
    ett testcase ikke ble skrevet."""
    alle_skrevet = True
    for case in finn_caser(testdata, case_navn):
        cv = (case / "cv.txt").read_text(encoding="utf-8")
        annonse = (case / "annonse.txt").read_text(encoding="utf-8")
        eget_brev = _eget_brev(case)
        if bare_korrektur and eget_brev is None:
            print(f"{case.name}: har ikke eget-brev.txt, så det er hoppet over.")
            continue
        # Alle svarene hentes før noe skrives, så en KI-feil aldri gir en blanding av nye og
        # gamle svar. (En feil ved skrivingen, for eksempel full disk, kan gjøre det.)
        try:
            svar = lag_svar(ki, cv, annonse, eget_brev, bare_korrektur=bare_korrektur)
        except KIFeil as feil:
            print(f"{case.name}: et KI-kall feilet ({feil.type.value}). Ingenting er skrevet.")
            alle_skrevet = False
            continue
        mappe = ut / case.name if ut else case / "ki-svar"
        skriv_svar(mappe, svar)
        print(f"{case.name}: svarene er skrevet i {mappe}")
    return alle_skrevet


def main(argv: list[str] | None = None, testdata: Path = TESTDATA_MAPPE) -> int:
    parser = argparse.ArgumentParser(
        description="Lager de ferdige svarene i testmodus med ekte KI (Claude)."
    )
    parser.add_argument(
        "--ut",
        type=Path,
        help="skriv svarene i UT/<case>/ i stedet for i testdata/<case>/ki-svar/",
    )
    parser.add_argument("--case", help="kjør bare testcaset med dette navnet")
    parser.add_argument(
        "--testdata",
        type=Path,
        help="les testcasene fra denne mappen i stedet for fra testdata/",
    )
    parser.add_argument(
        "--bare-korrektur",
        action="store_true",
        help="lag bare korrektur-1.json og korrektur-2.json, for caser med eget-brev.txt",
    )
    argumenter = parser.parse_args(argv)
    testdata = argumenter.testdata or testdata

    # Sjekkes før nøkkelen, så et feilskrevet navn eller en feil mappe aldri gir et KI-kall
    # og aldri ender med 0 uten at noe er gjort.
    if not finn_caser(testdata, argumenter.case):
        if argumenter.case is None:
            print(f"Fant ingen testcaser (mapper som heter case-…) i {testdata}.")
        else:
            print(f"Fant ikke testcaset {argumenter.case} i {testdata}.")
        return UKJENT_CASE
    if argumenter.bare_korrektur and not any(
        _eget_brev(case) is not None for case in finn_caser(testdata, argumenter.case)
    ):
        print(f"Ingen av testcasene har eget-brev.txt (i {testdata}).")
        return UKJENT_CASE

    # Samme .env som nettsiden. Verdier som alt står i miljøet, beholdes.
    load_dotenv(soknad.ENV_FIL, override=False, encoding="utf-8")
    nokkel = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not nokkel:
        print("Mangler API-nøkkel. Legg ANTHROPIC_API_KEY i backend/.env, se README.")
        return MANGLER_NOKKEL

    soknad.sett_opp_logg()
    ki = EkteKI(nokkel, os.environ.get("ANTHROPIC_MODEL") or STANDARD_MODELL)
    skrevet = lag_testsvar(
        ki, testdata, argumenter.ut, argumenter.case, bare_korrektur=argumenter.bare_korrektur
    )
    return 0 if skrevet else KI_FEILET


if __name__ == "__main__":
    sys.exit(main())
