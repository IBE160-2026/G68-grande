"""Tester for kontrollen av KI-svar (FR-28, AD-4). Hvert tilfelle av ubrukelig svar gir
KIFeil(ubrukelig_svar)."""

import copy
import json
import pickle

import pytest

from soknad.innstillinger import MAKS_NOKKELORD
from soknad.kjerne.feil import KIFeil, KIFeilType
from soknad.kjerne.ki_svar import HILSEN, hele_brevet, kontroller


def test_fr28_gyldig_nokkelordsvar_gis_tilbake():
    """FR-28: et gyldig svar gis tilbake i formen fra AD-4."""
    tekst = '{"nokkelord": ["Python", "SQL"], "arbeidsgiver": "Testvik AS"}'
    assert kontroller("nokkelord", tekst) == {
        "nokkelord": ["Python", "SQL"],
        "arbeidsgiver": "Testvik AS",
    }


def test_fr28_arbeidsgiver_kan_vaere_null():
    """FR-28: mangler arbeidsgiveren, sender KI-en null (AD-4)."""
    svar = kontroller("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": null}')
    assert svar["arbeidsgiver"] is None


def test_fr28_gyldig_gapsvar_med_en_tom_liste():
    """FR-28: én tom liste er lov, så lenge ikke begge er tomme."""
    assert kontroller("gap", '{"dekker": [], "mangler": ["SQL"]}') == {
        "dekker": [],
        "mangler": ["SQL"],
    }


@pytest.mark.parametrize(
    ("oppgave", "tekst"),
    [
        # Ugyldig JSON
        ("nokkelord", ""),
        ("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": null'),
        ("gap", "ikke json"),
        # Tom nøkkelordliste
        ("nokkelord", '{"nokkelord": [], "arbeidsgiver": "Testvik AS"}'),
        # Både dekker og mangler tomme
        ("gap", '{"dekker": [], "mangler": []}'),
        # Bare tomme tekster regnes som tomt
        ("nokkelord", '{"nokkelord": ["", "  "], "arbeidsgiver": null}'),
        ("gap", '{"dekker": [""], "mangler": [" \\n"]}'),
        # JSON som er nøstet så dypt at Python gir opp
        ("gap", "[" * 100_000 + "]" * 100_000),
        # Feil form: ikke et objekt, felt som mangler eller er i tillegg, feil type
        ("nokkelord", '["Python"]'),
        ("nokkelord", '{"nokkelord": ["Python"]}'),
        ("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": null, "ekstra": 1}'),
        ("nokkelord", '{"nokkelord": "Python", "arbeidsgiver": null}'),
        ("nokkelord", '{"nokkelord": ["Python", 3], "arbeidsgiver": null}'),
        ("nokkelord", '{"nokkelord": ["Python"], "arbeidsgiver": 3}'),
        ("gap", '{"dekker": ["Python"]}'),
        ("gap", '{"dekker": "Python", "mangler": []}'),
        ("gap", '{"dekker": ["Python"], "mangler": [null]}'),
        ("gap", "null"),
        # Brev uten tekst (story 3.1)
        ("brev", '{"avsnitt": [], "navn": "Sara"}'),
        ("brev", '{"avsnitt": ["  "], "navn": "Sara"}'),
        ("brev", '{"avsnitt": ["", " \\n"], "navn": null}'),
        # Brev med bare kontrolltegn, som blir tomt etter rensingen (story 4.2)
        ("brev", '{"avsnitt": ["\\u000b", "\\u0000\\n\\u0001", "\\ud800\\uffff"], "navn": null}'),
        # Brev med bare hilsen og navn, som blir tomt når hilsenen er fjernet
        ("brev", '{"avsnitt": ["Med vennlig hilsen", "Sara"], "navn": "Sara"}'),
        ("brev", '{"avsnitt": ["Med vennlig hilsen,"], "navn": null}'),
        ("brev", '{"avsnitt": ["Med vennlig hilsen Sara Eksempel"], "navn": "Sara"}'),
        # Brev med feil form
        ("brev", '{"avsnitt": "Hei", "navn": null}'),
        ("brev", '{"avsnitt": ["Hei", 3], "navn": null}'),
        ("brev", '{"avsnitt": ["Hei"], "navn": null, "forslag": 1}'),
        ("brev", '{"tekst": "Hei"}'),
        ("brev", '["Hei"]'),
        # navn mangler, er et tall eller en liste
        ("brev", '{"avsnitt": ["Hei"]}'),
        ("brev", '{"avsnitt": ["Hei"], "navn": 3}'),
        ("brev", '{"avsnitt": ["Hei"], "navn": ["Sara"]}'),
        ("brev", '{"avsnitt": ["Hei"], "navn": true}'),
    ],
)
def test_fr28_ubrukelig_svar_gir_kifeil(oppgave, tekst):
    """FR-28: ugyldig JSON, tom nøkkelordliste, tomme dekker og mangler og feil form gir
    KIFeil(ubrukelig_svar)."""
    with pytest.raises(KIFeil) as feil:
        kontroller(oppgave, tekst)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def test_fr28_kifeil_beholder_typen_ved_kopi():
    """FR-28: en kopi av KIFeil (copy eller pickle) har samme type som originalen."""
    original = KIFeil(KIFeilType.UBRUKELIG_SVAR)
    for kopi in (copy.copy(original), pickle.loads(pickle.dumps(original))):
        assert kopi.type == KIFeilType.UBRUKELIG_SVAR


def test_fr28_ukjent_oppgave_er_en_programfeil():
    """FR-28: korrektur kommer i Epic 5. En ukjent oppgave er en feil i koden."""
    with pytest.raises(ValueError):
        kontroller("korrektur", '{"avsnitt": ["Hei"], "navn": null}')


def test_fr22_gyldig_brev_gis_tilbake():
    """FR-22/FR-28: et brev med minst ett avsnitt med tekst gis tilbake i formen fra AD-4,
    {avsnitt, navn}."""
    tekst = '{"avsnitt": ["Søknad på stillingen", "Jeg søker stillingen."], "navn": "Sara"}'
    assert kontroller("brev", tekst) == {
        "avsnitt": ["Søknad på stillingen", "Jeg søker stillingen."],
        "navn": "Sara",
    }


def test_fr22_tomme_avsnitt_i_brevet_fjernes():
    """FR-22/FR-28: avsnitt som er tomme eller bare har mellomrom, fjernes fra brevet."""
    svar = kontroller("brev", '{"avsnitt": ["Hei", "", "  "], "navn": null}')
    assert svar == {"avsnitt": ["Hei"], "navn": None}


def _brev(*avsnitt: str, navn: str | None = "Sara") -> list[str]:
    """Avsnittene etter kontroller() for et brev med disse avsnittene."""
    return kontroller("brev", json.dumps({"avsnitt": list(avsnitt), "navn": navn}))["avsnitt"]


def test_fr28_linjeskift_og_tab_i_brevet_blir_ett_mellomrom():
    """FR-28/FR-30: \\n, \\r og \\t blir mellomrom, og flere mellomrom på rad blir ett, også
    først og sist i avsnittet."""
    assert _brev("Jeg søker\nstillingen\r\nsom\tutvikler.   Hei", "  Jeg kan\n\nbegynne ") == [
        "Jeg søker stillingen som utvikler. Hei",
        "Jeg kan begynne",
    ]


@pytest.mark.parametrize("navn", [None, "", "  ", "\\n\\t", "\\u000b"])
def test_fr22_tomt_navn_blir_none(navn):
    """FR-22/FR-28: et navn som er null, tomt, bare mellomrom eller bare kontrolltegn, blir
    None, slik arbeidsgiver gjør."""
    verdi = "null" if navn is None else f'"{navn}"'
    svar = kontroller("brev", f'{{"avsnitt": ["Hei"], "navn": {verdi}}}')
    assert svar == {"avsnitt": ["Hei"], "navn": None}


def test_fr28_navnet_renses_som_avsnittene():
    """FR-28/FR-30: i navnet fjernes kontrolltegn, og linjeskift, tab og mellomrom først og
    sist blir som i avsnittene, så Word-fila blir lik siden."""
    svar = kontroller("brev", '{"avsnitt": ["Hei"], "navn": "  Sara\\n\\tEks\\u000bempel "}')
    assert svar["navn"] == "Sara Eksempel"


@pytest.mark.parametrize(
    "slutt",
    [
        ["Med vennlig hilsen", "Sara Eksempel"],
        ["Med vennlig hilsen,", "Sara Eksempel"],
        ["med vennlig hilsen", "Sara Eksempel"],
        ["MED VENNLIG HILSEN", "Sara Eksempel"],
        ["Med vennlig hilsen"],
        ["Med vennlig hilsen,"],
        ["Med vennlig hilsen."],
        ["Med vennlig hilsen Sara Eksempel"],
        ["Med vennlig hilsen, Sara Eksempel"],
        ["Med vennlig\nhilsen", "Sara\nEksempel"],
        ["Med vennlig hilsen", "  ", "Sara Eksempel", ""],
        # Andre hilsener: uten «Med», «Mvh» og nynorsk.
        ["Vennlig hilsen", "Sara Eksempel"],
        ["vennlig hilsen, Sara Eksempel"],
        ["Mvh", "Sara Eksempel"],
        ["Mvh."],
        ["MVH Sara Eksempel"],
        ["Med venleg helsing", "Sara Eksempel"],
        ["Venleg helsing,"],
        ["venleg helsing Sara Eksempel"],
    ],
)
def test_fr22_hilsenen_ki_en_skrev_selv_fjernes(slutt):
    """FR-22/FR-28: har KI-en likevel skrevet hilsenen og eventuelt navnet til slutt (også med
    komma, annen stor eller liten bokstav, navnet i samme avsnitt, «Vennlig hilsen», «Mvh» eller
    nynorsk «Med venleg helsing»), fjernes de, så hilsenen ikke kommer to ganger når
    hele_brevet() setter den inn."""
    assert _brev("Søknad på stillingen", "Jeg søker.", *slutt) == [
        "Søknad på stillingen",
        "Jeg søker.",
    ]


@pytest.mark.parametrize(
    "avsnitt",
    [
        # Hilsenen står ikke til slutt.
        ["Med vennlig hilsen", "Jeg søker.", "Jeg kan begynne i august."],
        # Hilsenen med noe etter i samme avsnitt er ikke nest siste avsnitt bare med hilsen.
        ["Jeg søker.", "Med vennlig hilsen Sara", "Jeg kan begynne i august."],
        # Ordet er ikke hilsenen.
        ["Jeg søker.", "Med vennlig hilsenen fra Sara"],
        ["Jeg søker.", "Jeg sender med vennlig hilsen"],
        # Bare «Hilsen» regnes ikke som hilsenen.
        ["Jeg søker.", "Hilsen Sara"],
    ],
)
def test_fr22_avsnitt_som_ikke_er_hilsenen_til_slutt_beholdes(avsnitt):
    """FR-22: bare hilsenen (og navnet) til slutt fjernes. Andre avsnitt står igjen."""
    assert _brev(*avsnitt) == avsnitt


@pytest.mark.parametrize("slutt", ["Sara Eksempel", "sara eksempel", "Sara\nEksempel "])
def test_fr22_navnet_alene_til_slutt_fjernes(slutt):
    """FR-22: slutter avsnittene med bare navnet (uten hilsen), fjernes det, så navnet ikke
    kommer to ganger når hele_brevet() setter det inn."""
    assert _brev("Jeg søker.", slutt, navn="Sara Eksempel") == ["Jeg søker."]


@pytest.mark.parametrize("navn", ["Sara Eksempel", None])
def test_fr22_siste_avsnitt_som_ikke_er_navnet_beholdes(navn):
    """FR-22: et siste avsnitt som ikke er lik navnet, står igjen. Uten navn fjernes ingenting."""
    avsnitt = ["Jeg søker.", "Sara"] if navn is None else ["Jeg søker.", "Jeg kan begynne."]
    assert _brev(*avsnitt, navn=navn) == avsnitt


def test_fr22_hele_brevet_har_hilsen_og_navn_til_slutt():
    """FR-22/FR-30: hele_brevet() gir avsnittene, så «Med vennlig hilsen» og navnet som to egne
    avsnitt. Det er dette som vises og lastes ned."""
    brev = {"avsnitt": ["Søknad på stillingen", "Jeg søker."], "navn": "Sara Eksempel"}
    assert hele_brevet(brev) == [
        "Søknad på stillingen",
        "Jeg søker.",
        "Med vennlig hilsen",
        "Sara Eksempel",
    ]
    assert HILSEN == "Med vennlig hilsen"


@pytest.mark.parametrize("navn", ["null", '""', '"  "'])
def test_fr22_hele_brevet_uten_navn_slutter_med_hilsenen(navn):
    """FR-22: uten navn (null, tomt eller bare mellomrom) slutter brevet med «Med vennlig
    hilsen»."""
    brev = kontroller("brev", f'{{"avsnitt": ["Jeg søker."], "navn": {navn}}}')
    assert hele_brevet(brev) == ["Jeg søker.", "Med vennlig hilsen"]


def test_fr22_hilsenen_kommer_ikke_to_ganger():
    """FR-22: skrev KI-en hilsenen og navnet selv, har hele brevet dem likevel bare én gang."""
    tekst = json.dumps(
        {"avsnitt": ["Jeg søker.", "Med vennlig hilsen,", "Sara Eksempel"], "navn": "Sara Eksempel"}
    )
    assert hele_brevet(kontroller("brev", tekst)) == [
        "Jeg søker.",
        "Med vennlig hilsen",
        "Sara Eksempel",
    ]


@pytest.mark.parametrize(
    "tegn",
    ["\x00", "\x01", "\x0b", "\x0c", "\x1f", "\x7f", "\x85", "\x9f", "\ud800", "\udfff"]
    + ["\ufffe", "\uffff"],
)
def test_fr28_kontrolltegn_i_brevet_fjernes(tegn):
    """FR-28/FR-30: kontrolltegn (Cc), enslige surrogater (Cs) og U+FFFE/U+FFFF fjernes fra
    avsnittet, og teksten rundt står igjen uten mellomrom der tegnet var."""
    assert _brev(f"kontroll{tegn}tegn", "Jeg søker.") == ["kontrolltegn", "Jeg søker."]


def test_fr28_vanlige_tegn_i_brevet_beholdes():
    """FR-28: æøå, sitattegn, tankestrek, emoji og tegn utenfor BMP beholdes."""
    tekst = "Æ, ø og å, «sitat» – tankestrek, 😀 og 𝄞."
    assert _brev(tekst) == [tekst]


def test_fr28_kontrolltegn_fjernes_ogsa_fra_json_escape():
    """FR-28: et kontrolltegn skrevet som \\u000b i JSON-en fjernes på samme måte."""
    svar = kontroller("brev", '{"avsnitt": ["a\\u000bb\\u0000c"], "navn": null}')
    assert svar == {"avsnitt": ["abc"], "navn": None}


@pytest.mark.parametrize(
    ("tekst", "forventet"),
    [
        (
            '{"nokkelord": ["Python", "  ", "", "SQL"], "arbeidsgiver": "Testvik AS"}',
            {"nokkelord": ["Python", "SQL"], "arbeidsgiver": "Testvik AS"},
        ),
        (
            '{"dekker": ["Python", " \\n"], "mangler": ["", "SQL", "\\t"]}',
            {"dekker": ["Python"], "mangler": ["SQL"]},
        ),
        ('{"dekker": ["  "], "mangler": ["SQL"]}', {"dekker": [], "mangler": ["SQL"]}),
    ],
)
def test_fr28_tomme_punkter_fjernes(tekst, forventet):
    """FR-28: punkter som er tomme eller bare har mellomrom, fjernes i nokkelord, dekker og
    mangler, så resultatsiden ikke viser tomme punkter."""
    oppgave = "nokkelord" if "nokkelord" in tekst else "gap"
    assert kontroller(oppgave, tekst) == forventet


@pytest.mark.parametrize(
    ("oppgave", "tekst", "forventet"),
    [
        (
            "nokkelord",
            '{"nokkelord": ["Py\\ud800thon", "\\ud800", "SQL"], "arbeidsgiver": null}',
            {"nokkelord": ["Python", "SQL"], "arbeidsgiver": None},
        ),
        (
            "gap",
            '{"dekker": ["SQL\\udfff"], "mangler": ["\\ud800", "G\\ud800it"]}',
            {"dekker": ["SQL"], "mangler": ["Git"]},
        ),
    ],
)
def test_fr28_enslige_surrogater_fjernes_fra_listene(oppgave, tekst, forventet):
    """FR-28: enslige surrogater (for eksempel \\ud800 i JSON-en) fjernes fra punktene i
    nokkelord, dekker og mangler, så resultatsiden ikke gir en feilside. Et punkt med bare en
    surrogat blir borte."""
    assert kontroller(oppgave, tekst) == forventet


def test_fr28_bare_surrogater_i_nokkelordene_gir_ubrukelig_svar():
    """FR-28: blir nøkkelordlisten tom når surrogatene er fjernet, er svaret ubrukelig."""
    with pytest.raises(KIFeil) as feil:
        kontroller("nokkelord", '{"nokkelord": ["\\ud800", "\\udfff"], "arbeidsgiver": null}')
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


@pytest.mark.parametrize("arbeidsgiver", ["", "   ", "\\n\\t"])
def test_fr28_tom_arbeidsgiver_blir_none(arbeidsgiver):
    """FR-28: en arbeidsgiver som er tom eller bare har mellomrom, blir None."""
    svar = kontroller("nokkelord", f'{{"nokkelord": ["Python"], "arbeidsgiver": "{arbeidsgiver}"}}')
    assert svar == {"nokkelord": ["Python"], "arbeidsgiver": None}


def test_fr15_fr28_tomme_punkter_regnes_ikke_med_i_grensen():
    """FR-15/FR-28: tomme punkter fjernes før grensen MAKS_NOKKELORD sjekkes."""
    nokkelord = [f"ord{n}" for n in range(MAKS_NOKKELORD)] + ["", "  "]
    svar = kontroller("nokkelord", json.dumps({"nokkelord": nokkelord, "arbeidsgiver": None}))
    assert len(svar["nokkelord"]) == MAKS_NOKKELORD


@pytest.mark.parametrize("stop_reason", ["max_tokens", "refusal", "pause_turn", None])
def test_fr28_stop_reason_som_ikke_er_end_turn_gir_ubrukelig_svar(stop_reason):
    """FR-28/AD-4: et avkuttet eller avvist svar gir KIFeil(ubrukelig_svar) før JSON-en leses,
    også når JSON-en er gyldig. Uten stop_reason gjelder end_turn (TestKI)."""
    tekst = '{"dekker": ["Python"], "mangler": []}'
    assert kontroller("gap", tekst) == kontroller("gap", tekst, "end_turn")
    with pytest.raises(KIFeil) as feil:
        kontroller("gap", tekst, stop_reason)
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR


def _nokkelord(antall: int) -> str:
    return json.dumps({"nokkelord": [f"ord{n}" for n in range(antall)], "arbeidsgiver": None})


def test_fr15_grensen_er_maks_nokkelord():
    """FR-15: grensen for antall nøkkelord er MAKS_NOKKELORD, som er 30."""
    assert MAKS_NOKKELORD == 30


def test_fr15_fr28_akkurat_30_nokkelord_godtas():
    """FR-15/FR-28: et svar med akkurat MAKS_NOKKELORD nøkkelord godtas."""
    svar = kontroller("nokkelord", _nokkelord(MAKS_NOKKELORD))
    assert len(svar["nokkelord"]) == MAKS_NOKKELORD


@pytest.mark.parametrize("antall", [MAKS_NOKKELORD + 1, 100])
def test_fr15_fr28_flere_enn_30_nokkelord_gir_ubrukelig_svar(antall):
    """FR-15/FR-28: flere enn MAKS_NOKKELORD nøkkelord gir KIFeil(ubrukelig_svar)."""
    with pytest.raises(KIFeil) as feil:
        kontroller("nokkelord", _nokkelord(antall))
    assert feil.value.type == KIFeilType.UBRUKELIG_SVAR
