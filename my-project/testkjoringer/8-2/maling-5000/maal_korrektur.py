"""Måler ett Korrektur-kall med ekte KI og et eget brev på nesten 5 000 tegn (MAKS_TEGN_EGET_BREV).

Brevet lages av det lange testbrevet fra retro 5 (Ingrid Prøvesen, 14 637 tegn): overskriften,
«Hei!», de første avsnittene og avslutningen med hilsenen. Er det plass, tas hele setninger fra
neste avsnitt med, til brevet er så nær 5 000 tegn som mulig. CV-en og annonsen er de nær
15 000 tegn fra retro 4, altså det verste tilfellet.

Kallet går gjennom EkteKI med de samme grensene som nettsiden (KI_TIDSGRENSE og KI_MAKS_TOKENS),
men uten nytt forsøk (max_retries=0), så et tidsavbrudd ikke skjules av et nytt forsøk.

Kjøres fra backend/ (trenger ANTHROPIC_API_KEY i backend/.env, koster ca. 3 kr):

    uv run python ../my-project/testkjoringer/8-2/maling-5000/maal_korrektur.py
"""

import json
import re
import sys
import time
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from soknad.adaptere.ki import EkteKI
from soknad.innstillinger import (
    KI_MAKS_TOKENS,
    KI_TIDSGRENSE,
    MAKS_TEGN_EGET_BREV,
    STANDARD_MODELL,
)
from soknad.kjerne.feil import KIFeil
from soknad.kjerne.inndata import antall_tegn

HER = Path(__file__).resolve().parent
INNDATA = HER.parent.parent / "retro-5" / "inndata" / "case-lang"


def lag_brev(langt: str, grense: int) -> str:
    """Overskriften, «Hei!», så mange hele avsnitt som får plass, hele setninger fra neste
    avsnitt, og avslutningen (de tre siste avsnittene)."""
    avsnitt = re.split(r"\n\s*\n", langt.replace("\r\n", "\n").strip())
    start, midten, slutt = avsnitt[:2], avsnitt[2:-3], avsnitt[-3:]

    def lengde(deler):
        return antall_tegn("\n\n".join(deler))

    valgt = []
    for a in midten:
        if lengde(start + valgt + [a] + slutt) <= grense:
            valgt.append(a)
            continue
        # Hele setninger fra dette avsnittet, så lenge det er plass.
        setninger = re.split(r"(?<=[.!?])\s+", a)
        biter = []
        for s in setninger:
            if lengde(start + valgt + [" ".join(biter + [s])] + slutt) > grense:
                break
            biter.append(s)
        if biter:
            valgt.append(" ".join(biter))
        break
    return "\n\n".join(start + valgt + slutt) + "\n"


def main() -> int:
    load_dotenv(Path.cwd() / ".env")
    import os

    nokkel = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not nokkel:
        print("Mangler ANTHROPIC_API_KEY i backend/.env")
        return 1
    modell = os.environ.get("ANTHROPIC_MODEL", "").strip() or STANDARD_MODELL

    cv = (INNDATA / "cv.txt").read_text(encoding="utf-8")
    annonse = (INNDATA / "annonse.txt").read_text(encoding="utf-8")
    brev = lag_brev((INNDATA / "eget-brev.txt").read_text(encoding="utf-8"), MAKS_TEGN_EGET_BREV)
    (HER / "eget-brev-5000.txt").write_text(brev, encoding="utf-8")
    print(f"Eget brev: {antall_tegn(brev)} tegn (grense {MAKS_TEGN_EGET_BREV})")
    print(f"CV: {antall_tegn(cv)} tegn, annonse: {antall_tegn(annonse)} tegn")

    klient = Anthropic(api_key=nokkel, timeout=KI_TIDSGRENSE, max_retries=0)
    ki = EkteKI(nokkel, modell, klient=klient)

    # Henter tokens og stop_reason fra selve svaret, ved å pakke inn messages.create.
    fanget = {}
    opprinnelig = klient.messages.create

    def create(**kwargs):
        svar = opprinnelig(**kwargs)
        fanget["tokens_inn"] = svar.usage.input_tokens
        fanget["tokens_ut"] = svar.usage.output_tokens
        fanget["stop_reason"] = svar.stop_reason
        return svar

    klient.messages.create = create

    resultat = {
        "modell": modell,
        "tegn_eget_brev": antall_tegn(brev),
        "tidsgrense_s": KI_TIDSGRENSE,
        "maks_tokens": KI_MAKS_TOKENS,
    }
    start = time.monotonic()
    try:
        svar = ki.korrektur(cv, annonse, brev, forslag=1)
        resultat["kontroller"] = "bestått"
        (HER / "korrektur.json").write_text(
            json.dumps(svar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except KIFeil as feil:
        resultat["kontroller"] = f"KI-feil: {feil.type.name}"
    resultat["sekunder"] = round(time.monotonic() - start, 1)
    resultat.update(fanget)
    (HER / "resultat.json").write_text(
        json.dumps(resultat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(resultat, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
