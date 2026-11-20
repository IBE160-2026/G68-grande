"""Kontroll av KI-svar (AD-4, FR-28). Både TestKI og EkteKI sender svaret hit, så et
ubrukelig svar stoppes på samme sted uansett utgave."""

import json
import re
import unicodedata

from soknad.innstillinger import MAKS_NOKKELORD
from soknad.kjerne.feil import KIFeil, KIFeilType

# Feltene hver oppgave skal ha, og nøyaktig disse (AD-4).
FELT = {
    "nokkelord": {"nokkelord", "arbeidsgiver"},
    "gap": {"dekker", "mangler"},
    "brev": {"avsnitt", "navn"},
    "korrektur": {"setninger"},
}

# Feltene i hver setning i Korrektur, og nøyaktig disse (story 5.2.1).
SETNING_FELT = {"ny", "gammel", "nytt_avsnitt"}

# Hilsenen til slutt i brevet. KI-en skriver den ikke selv, men hele_brevet() setter den inn
# før navnet, både på siden og i Word-fila.
HILSEN = "Med vennlig hilsen"


def _er_tekstliste(verdi) -> bool:
    return isinstance(verdi, list) and all(isinstance(element, str) for element in verdi)


def _riktig_setning(setning) -> bool:
    """Én setning i Korrektur: ny er tekst eller null, gammel er en liste med tekster, og
    nytt_avsnitt er true eller false (ikke et tall)."""
    if not isinstance(setning, dict) or set(setning) != SETNING_FELT:
        return False
    ny = setning["ny"]
    return (
        (ny is None or isinstance(ny, str))
        and _er_tekstliste(setning["gammel"])
        and isinstance(setning["nytt_avsnitt"], bool)
    )


def _riktig_form(oppgave: str, svar) -> bool:
    if not isinstance(svar, dict) or set(svar) != FELT[oppgave]:
        return False
    if oppgave == "korrektur":
        setninger = svar["setninger"]
        return (
            isinstance(setninger, list)
            and len(setninger) > 0
            and all(_riktig_setning(setning) for setning in setninger)
        )
    if oppgave == "nokkelord":
        arbeidsgiver = svar["arbeidsgiver"]
        return _er_tekstliste(svar["nokkelord"]) and (
            arbeidsgiver is None or isinstance(arbeidsgiver, str)
        )
    if oppgave == "brev":
        navn = svar["navn"]
        return _er_tekstliste(svar["avsnitt"]) and (navn is None or isinstance(navn, str))
    return _er_tekstliste(svar["dekker"]) and _er_tekstliste(svar["mangler"])


# Tegnene Word (XML) ikke tåler, fjernes fra brevet: kontrolltegn (kategori Cc), enslige
# surrogater (Cs, kan komme fra for eksempel \ud800 i JSON) og U+FFFE og U+FFFF. Tab,
# linjeskift og vognretur er også kontrolltegn, men de blir mellomrom i stedet.
_MELLOMROM_KONTROLLTEGN = "\t\n\r"
_IKKE_TEGN = "\ufffe\uffff"


def _word_taler(tegn: str) -> bool:
    if tegn in _MELLOMROM_KONTROLLTEGN:
        return True
    return unicodedata.category(tegn) not in ("Cc", "Cs") and tegn not in _IKKE_TEGN


def _rens_avsnitt(avsnitt: str) -> str:
    """Fjerner tegnene Word ikke tåler, og gjør alt mellomrom (også linjeskift og tab) om til
    ett mellomrom. Nettleseren viser flere mellomrom som ett, så da blir Word-fila lik siden.
    Teksten får Unicode NFC, så «å» skrevet som a + ring blir samme tegn som «å» (retro 5)."""
    tekst = unicodedata.normalize("NFC", avsnitt)
    return " ".join("".join(tegn for tegn in tekst if _word_taler(tegn)).split())


# En hilsen først i et avsnitt: «(Med) vennlig hilsen», «Mvh» eller nynorsk «(Med) venleg
# helsing», uten hensyn til store og små bokstaver, med eventuelt komma eller punktum etter.
# Bare «Hilsen» regnes ikke med. Gruppen er resten av avsnittet, for eksempel navnet.
_HILSEN_MONSTER = re.compile(
    r"(?:(?:med\s+)?vennlig\s+hilsen|mvh|(?:med\s+)?venleg\s+helsing)\b[\s,.!:;]*(.*)",
    re.IGNORECASE,
)


def _uten_hilsen(avsnitt: list[str], navn: str | None) -> list[str]:
    """Avsnittene uten hilsenen og navnet, hvis KI-en likevel skrev dem til slutt. Da kommer ikke
    hilsenen eller navnet to ganger når hele_brevet() setter dem inn. Det fjernes:
    - det siste avsnittet, når det er hilsenen, også med navnet etter («Med vennlig hilsen Sara
      Eksempel»)
    - de to siste avsnittene, når det nest siste er bare hilsenen. Da er det siste navnet.
    - ellers det siste avsnittet, når det er lik navnet (renset, uten hensyn til store og små
      bokstaver)
    Avsnittene og navnet er alt renset, så det er ingen tomme avsnitt og ingen linjeskift."""
    for fra in (len(avsnitt) - 1, len(avsnitt) - 2):
        if fra < 0:
            continue
        treff = _HILSEN_MONSTER.fullmatch(avsnitt[fra])
        if treff and (fra == len(avsnitt) - 1 or not treff.group(1)):
            return avsnitt[:fra]
    if navn is not None and avsnitt and avsnitt[-1].casefold() == navn.casefold():
        return avsnitt[:-1]
    return avsnitt


def hele_brevet(brev: dict) -> list[str]:
    """Brevet som vises og lastes ned: avsnittene, så «Med vennlig hilsen» og navnet som to egne
    avsnitt. Uten navn kommer bare hilsenen. Ruter og fil_ut setter aldri sammen brevet selv.
    «Nytt forslag» (story 7.1) bruker den, og PDF (story 7.2) skal også bruke den. brev er i
    formen fra kontroller()."""
    navn = brev["navn"]
    return [*brev["avsnitt"], HILSEN, *([navn] if navn else [])]


def _korrektur_avsnitt(korrektur: dict) -> list[list[dict]]:
    """Setningene i Korrektur som har ny (ikke None), i rekkefølge, gruppert i avsnitt. En
    setning begynner et nytt avsnitt når den selv, eller en fjernet setning rett foran den, har
    nytt_avsnitt. Den første setningen begynner alltid et avsnitt. Både korrigert_brev og
    korrektur_visning bruker denne, så siden og Word-fila har de samme avsnittene."""
    avsnitt: list[list[dict]] = []
    nytt = False
    for setning in korrektur["setninger"]:
        nytt = nytt or setning["nytt_avsnitt"]
        if setning["ny"] is None:
            continue
        if nytt or not avsnitt:
            avsnitt.append([setning])
        else:
            avsnitt[-1].append(setning)
        nytt = False
    return avsnitt


def korrigert_brev(korrektur: dict) -> list[str]:
    """Brevet i Korrektur som vises og lastes ned: alle ny som ikke er None, i rekkefølge, satt
    sammen til avsnitt (se _korrektur_avsnitt), med ett mellomrom mellom setningene i hvert
    avsnitt. Hilsen og navn står slik brukeren skrev dem, og ingenting legges til. Ruter og
    fil_ut setter aldri sammen brevet selv. korrektur er i formen fra kontroller()."""
    return [
        " ".join(setning["ny"] for setning in avsnitt) for avsnitt in _korrektur_avsnitt(korrektur)
    ]


def korrektur_visning(korrektur: dict) -> dict:
    """Markeringene på brevsiden i Korrektur (FR-23, AD-5). Dette er det eneste stedet som
    avgjør hva som er endret. Malen og skriptet regner aldri ut det selv. Gir:
    - avsnitt: de samme avsnittene som korrigert_brev, som lister av {ny, gammel, endret}. Bare
      setninger med ny er med. endret er sann når gammel != [ny], også for en ny setning
      (gammel == []).
    - fjernet: antall gamle setninger som er fjernet, altså alle gammel i oppføringene der ny
      er None. To gamle setninger i én slik oppføring er to fjernede, og en oppføring med
      tom gammel er ingen. De vises ikke.
    - antall_endret: antall setninger som er markert som endret (endret over).
    korrektur er i formen fra kontroller()."""
    avsnitt = [
        [
            {
                "ny": setning["ny"],
                "gammel": list(setning["gammel"]),
                "endret": setning["gammel"] != [setning["ny"]],
            }
            for setning in gruppe
        ]
        for gruppe in _korrektur_avsnitt(korrektur)
    ]
    return {
        "avsnitt": avsnitt,
        "fjernet": sum(
            len(setning["gammel"]) for setning in korrektur["setninger"] if setning["ny"] is None
        ),
        "antall_endret": sum(1 for gruppe in avsnitt for setning in gruppe if setning["endret"]),
    }


def _uten_tomme(liste: list[str]) -> list[str]:
    """Listen uten punkter som er tomme eller bare har mellomrom."""
    return [element for element in liste if element.strip()]


def _uten_surrogater(liste: list[str]) -> list[str]:
    """Listen der enslige surrogater (Cs) er fjernet fra hvert punkt. Ellers gir siden en
    feilside når punktet skal vises. Et punkt med bare surrogater blir tomt."""
    return ["".join(t for t in element if unicodedata.category(t) != "Cs") for element in liste]


def _rens_setning(setning: dict) -> dict:
    ny = setning["ny"]
    return {
        "ny": None if ny is None else (_rens_avsnitt(ny) or None),
        "gammel": [_rens_avsnitt(gammel) for gammel in setning["gammel"]],
        "nytt_avsnitt": setning["nytt_avsnitt"],
    }


def _rens(oppgave: str, svar: dict) -> dict:
    """Svaret uten tomme punkter og uten enslige surrogater i listene. Tom arbeidsgiver blir
    None, og brevteksten renses. Ellers renses ikke arbeidsgiver her, men i kjerne/filnavn.py
    når filnavnet lages (story 7.5). I brevet renses navnet som avsnittene, tomt navn blir None,
    og hilsenen KI-en skrev selv, fjernes. I Korrektur renses ny og hver gammel som avsnittene,
    og tom ny blir None."""
    if oppgave == "korrektur":
        return {"setninger": [_rens_setning(setning) for setning in svar["setninger"]]}
    if oppgave == "nokkelord":
        arbeidsgiver = svar["arbeidsgiver"]
        if arbeidsgiver is not None and not arbeidsgiver.strip():
            arbeidsgiver = None
        nokkelord = _uten_tomme(_uten_surrogater(svar["nokkelord"]))
        return {"nokkelord": nokkelord, "arbeidsgiver": arbeidsgiver}
    if oppgave == "brev":
        avsnitt = _uten_tomme([_rens_avsnitt(avsnitt) for avsnitt in svar["avsnitt"]])
        navn = svar["navn"]
        if navn is not None:
            navn = _rens_avsnitt(navn) or None
        return {"avsnitt": _uten_hilsen(avsnitt, navn), "navn": navn}
    return {
        "dekker": _uten_tomme(_uten_surrogater(svar["dekker"])),
        "mangler": _uten_tomme(_uten_surrogater(svar["mangler"])),
    }


def _bare_tomme(liste: list[str]) -> bool:
    """Sann når listen er tom eller bare har tomme tekster (også bare mellomrom)."""
    return not any(element.strip() for element in liste)


def _tomt(oppgave: str, svar: dict) -> bool:
    if oppgave == "korrektur":
        return all(setning["ny"] is None for setning in svar["setninger"])
    if oppgave == "nokkelord":
        return _bare_tomme(svar["nokkelord"])
    if oppgave == "brev":
        return _bare_tomme(svar["avsnitt"])
    return _bare_tomme(svar["dekker"] + svar["mangler"])


def _uten_mellomrom(tekst: str) -> str:
    """Teksten renset (_rens_avsnitt, med NFC) og uten mellomrom og usynlige formattegn
    (kategori Cf, for eksempel myk bindestrek, nullbreddemellomrom og BOM fra Word eller PDF).
    Alt annet beholdes, også store bokstaver og tegnsetting."""
    return "".join(
        tegn
        for tegn in _rens_avsnitt(tekst)
        if not tegn.isspace() and unicodedata.category(tegn) != "Cf"
    )


def _stemmer_med(korrektur: dict, eget_brev: str) -> bool:
    """Sann når alle gammel satt sammen er det egne brevet ordrett (AD-4, retro 5). Store
    bokstaver og tegnsetting teller, så «Du skrev» viser teksten slik den sto i brevet KI-en
    fikk, og en endring bare i tegnsetting blir markert. Mellomrom (også mellom setninger, så
    «butikk.Det» i brevet stemmer med «butikk.» og «Det»), linjeskift, usynlige formattegn og
    tegn Word ikke tåler teller ikke (_uten_mellomrom). En tom gammel stemmer aldri, fordi den
    ville gitt en tom linje i «Du skrev»."""
    gammel = [tekst for setning in korrektur["setninger"] for tekst in setning["gammel"]]
    if any(not tekst for tekst in gammel):
        return False
    return _uten_mellomrom("".join(gammel)) == _uten_mellomrom(eget_brev)


def kontroller(
    oppgave: str,
    tekst: str,
    stop_reason: str | None = "end_turn",
    eget_brev: str | None = None,
) -> dict:
    """Gir svaret i formen fra AD-4. Ugyldig JSON, feil form, tom nøkkelordliste, både
    dekker og mangler tomme eller et brev uten tekst gir KIFeil(ubrukelig_svar). Oppgavene er
    nokkelord, gap, brev og korrektur.

    Korrektur (FR-23, FR-24) har formen {setninger: [{ny, gammel, nytt_avsnitt}]}, og
    eget_brev er påkrevd (ellers ValueError, en feil i koden). Tom setninger, en setning med
    feil felt eller feil type (nytt_avsnitt må være true eller false), alle ny null, eller
    alle gammel satt sammen ulik det egne brevet ordrett, eller en tom gammel (se _stemmer_med),
    gir KIFeil(ubrukelig_svar). ny og hver gammel renses som avsnittene i brevet før sjekken, og
    tom ny blir None. eget_brev brukes ikke for de andre oppgavene. hele_brevet og _uten_hilsen
    brukes ikke for Korrektur.

    Før tom-sjekken renses svaret (FR-28, FR-30), både for TestKI og EkteKI:
    - Punkter som er tomme eller bare har mellomrom, fjernes i nokkelord, dekker, mangler og
      avsnitt, så siden ikke viser tomme punkter. En liste med bare slike punkter er tom.
    - Enslige surrogater fjernes fra punktene i nokkelord, dekker og mangler, før de tomme
      punktene fjernes. Et punkt med bare surrogater blir altså borte.
    - Tom arbeidsgiver (eller bare mellomrom) blir None.
    - I hvert avsnitt i brevet og i navnet fjernes kontrolltegn og andre tegn Word ikke tåler,
      og alt mellomrom (også linjeskift og tab) blir ett mellomrom, så Word-fila blir lik
      siden. Tomt navn (eller bare mellomrom) blir None.
    - Har KI-en likevel skrevet «Med vennlig hilsen» (eller for eksempel «Mvh») og eventuelt
      navnet, eller bare navnet, til slutt i brevet, fjernes de (se _uten_hilsen), fordi
      hele_brevet() setter dem inn. Et brev som blir tomt av dette eller av rensingen, gir
      KIFeil(ubrukelig_svar).

    En nøkkelordliste med flere enn MAKS_NOKKELORD (30) nøkkelord (tomme punkter ikke
    medregnet) gir også KIFeil(ubrukelig_svar) (FR-15).

    stop_reason kommer fra Claude. Alt annet enn end_turn (for eksempel max_tokens eller
    refusal) betyr at svaret er avkuttet eller avvist, og gir KIFeil(ubrukelig_svar) før
    JSON-en leses. TestKI sender den ikke, og da gjelder standarden end_turn."""
    if oppgave not in FELT:
        raise ValueError(f"Ukjent KI-oppgave: {oppgave}")
    if oppgave == "korrektur" and eget_brev is None:
        raise ValueError("Korrektur trenger det egne brevet for å kontrollere svaret.")
    if stop_reason != "end_turn":
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    try:
        svar = json.loads(tekst)
    except (json.JSONDecodeError, RecursionError) as feil:
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR) from feil
    if not _riktig_form(oppgave, svar):
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    svar = _rens(oppgave, svar)
    if _tomt(oppgave, svar):
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    if oppgave == "nokkelord" and len(svar["nokkelord"]) > MAKS_NOKKELORD:
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    if oppgave == "korrektur" and not _stemmer_med(svar, eget_brev):
        raise KIFeil(KIFeilType.UBRUKELIG_SVAR)
    return svar
