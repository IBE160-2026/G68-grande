"""Tester for scripts/lag_testsvar.py (FR-38, AD-4). Testene bruker en falsk KI og kaller
aldri det ekte API-et. De skriver bare i tmp_path, aldri i den ekte testdata/."""

import json

import pytest

import soknad
from scripts import lag_testsvar
from soknad.innstillinger import STANDARD_MODELL
from soknad.kjerne.feil import KIFeil, KIFeilType

NOKKELORD = {"nokkelord": ["Python", "førerkort"], "arbeidsgiver": "Testvik Utvikling AS"}
GAP = {"dekker": ["Kan Python"], "mangler": ["Har førerkort klasse B"]}


def _brev(forslag):
    return {"avsnitt": ["Søknad på stillingen som utvikler", f"Forslag {forslag}", "Sara"]}


class FalskKI:
    """Gir faste svar og husker hvert kall. feiler_paa er en oppgave som gir KIFeil."""

    def __init__(self, feiler_paa=None):
        self.kall = []
        self.feiler_paa = feiler_paa

    def _kall(self, oppgave, *args):
        self.kall.append((oppgave, *args))
        if oppgave == self.feiler_paa:
            raise KIFeil(KIFeilType.NETTVERK)

    def nokkelord(self, annonse):
        self._kall("nokkelord", annonse)
        return NOKKELORD

    def gap(self, cv, annonse):
        self._kall("gap", cv, annonse)
        return GAP

    def brev(self, cv, annonse, forslag):
        self._kall("brev", cv, annonse, forslag)
        return _brev(forslag)


@pytest.fixture
def testdata(tmp_path):
    """To testcaser med CV og annonse, og gamle svar i ki-svar/ for case 1."""
    mappe = tmp_path / "testdata"
    for navn in ("case-1-utvikler", "case-2-annet"):
        (mappe / navn / "ki-svar").mkdir(parents=True)
        (mappe / navn / "cv.txt").write_text(f"CV for {navn}", encoding="utf-8")
        (mappe / navn / "annonse.txt").write_text(f"Annonse for {navn}", encoding="utf-8")
    (mappe / "case-1-utvikler" / "ki-svar" / "gap.json").write_text("gammelt", encoding="utf-8")
    return mappe


def _les(fil):
    return fil.read_text(encoding="utf-8")


def test_fr38_skriver_fire_filer_med_bare_objektet(testdata):
    """FR-38/AD-4: hvert testcase får nokkelord.json, gap.json, brev-1.json og brev-2.json med
    bare objektet, innrykk 2 og linjeskift til slutt. CV og annonse sendes urørt."""
    ki = FalskKI()
    assert lag_testsvar.lag_testsvar(ki, testdata) is True

    svar = testdata / "case-1-utvikler" / "ki-svar"
    assert sorted(fil.name for fil in svar.iterdir()) == [
        "brev-1.json",
        "brev-2.json",
        "gap.json",
        "nokkelord.json",
    ]
    assert json.loads(_les(svar / "nokkelord.json")) == NOKKELORD
    assert json.loads(_les(svar / "gap.json")) == GAP
    assert json.loads(_les(svar / "brev-1.json")) == _brev(1)
    assert json.loads(_les(svar / "brev-2.json")) == _brev(2)
    assert _les(svar / "gap.json") == json.dumps(GAP, ensure_ascii=False, indent=2) + "\n"
    assert (testdata / "case-2-annet" / "ki-svar" / "brev-2.json").exists()

    cv, annonse = "CV for case-1-utvikler", "Annonse for case-1-utvikler"
    assert ki.kall[:4] == [
        ("nokkelord", annonse),
        ("gap", cv, annonse),
        ("brev", cv, annonse, 1),
        ("brev", cv, annonse, 2),
    ]
    assert len(ki.kall) == 8


def test_fr38_aeoa_staar_som_vanlige_tegn(testdata):
    """FR-38: «førerkort» står med ø i fila, ikke som \\u00f8."""
    lag_testsvar.lag_testsvar(FalskKI(), testdata)
    tekst = (testdata / "case-1-utvikler" / "ki-svar" / "nokkelord.json").read_bytes()
    assert "førerkort".encode() in tekst
    assert b"\\u00f8" not in tekst


def test_fr38_ut_skriver_i_egen_mappe_og_ki_svar_er_uendret(testdata, tmp_path):
    """FR-38: med ut skrives svarene i ut/<case>/, og ki-svar/ er som før."""
    ut = tmp_path / "kjoring-2"
    assert lag_testsvar.lag_testsvar(FalskKI(), testdata, ut) is True
    assert json.loads(_les(ut / "case-1-utvikler" / "brev-2.json")) == _brev(2)
    assert (ut / "case-2-annet" / "nokkelord.json").exists()
    assert _les(testdata / "case-1-utvikler" / "ki-svar" / "gap.json") == "gammelt"
    assert not (testdata / "case-1-utvikler" / "ki-svar" / "nokkelord.json").exists()


@pytest.mark.parametrize("oppgave", ["nokkelord", "gap", "brev"])
def test_fr38_ki_feil_skriver_ingenting_for_caset(testdata, capsys, oppgave):
    """FR-38/FR-28: feiler et KI-kall, skrives ingenting for caset (de gamle svarene står
    igjen), feiltypen vises, og funksjonen gir False."""
    assert lag_testsvar.lag_testsvar(FalskKI(feiler_paa=oppgave), testdata) is False
    svar = testdata / "case-1-utvikler" / "ki-svar"
    assert [fil.name for fil in svar.iterdir()] == ["gap.json"]
    assert _les(svar / "gap.json") == "gammelt"
    assert "case-1-utvikler: et KI-kall feilet (nettverk)" in capsys.readouterr().out


def test_fr38_et_case_som_feiler_stopper_ikke_de_andre(testdata):
    """FR-38: feiler bare case 1, skrives case 2 likevel."""

    class FeilerForCase1(FalskKI):
        def nokkelord(self, annonse):
            if "case-1" in annonse:
                raise KIFeil(KIFeilType.ANNET)
            return super().nokkelord(annonse)

    assert lag_testsvar.lag_testsvar(FeilerForCase1(), testdata) is False
    assert not (testdata / "case-1-utvikler" / "ki-svar" / "nokkelord.json").exists()
    assert (testdata / "case-2-annet" / "ki-svar" / "nokkelord.json").exists()


def _ingen_ekte_ki(monkeypatch):
    """EkteKI erstattes, så et feilsteg i testen aldri kan kalle det ekte API-et."""

    def feil(*args, **kwargs):
        raise AssertionError("EkteKI skal ikke lages")

    monkeypatch.setattr(lag_testsvar, "EkteKI", feil)


def test_fr38_uten_nokkel_gir_melding_og_ingen_ki(testdata, monkeypatch, capsys):
    """FR-38/FR-32: uten API-nøkkel (heller ikke bare mellomrom) lages ingen KI, meldingen
    viser til README, og main gir feilkode 2."""
    _ingen_ekte_ki(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "  ")
    assert lag_testsvar.main([], testdata) == lag_testsvar.MANGLER_NOKKEL == 2
    utskrift = capsys.readouterr().out
    assert "Mangler API-nøkkel" in utskrift
    assert "README" in utskrift
    assert not (testdata / "case-1-utvikler" / "ki-svar" / "nokkelord.json").exists()


def _env_fil(monkeypatch, tmp_path, innhold):
    """En egen .env for testen. load_dotenv setter verdiene rett i os.environ, så
    variablene registreres i monkeypatch først og fjernes igjen etter testen."""
    env = tmp_path / ".env"
    env.write_text(innhold, encoding="utf-8")
    monkeypatch.setattr(soknad, "ENV_FIL", env)
    for navn in ("ANTHROPIC_API_KEY", "ANTHROPIC_MODEL"):
        monkeypatch.setenv(navn, "")
        monkeypatch.delenv(navn)


def _tell_ekte_ki(monkeypatch):
    """Erstatter EkteKI med en falsk KI og gir listen over (nøkkel, modell) den ble laget med."""
    laget = []

    def falsk_ekte_ki(nokkel, modell):
        laget.append((nokkel, modell))
        return FalskKI()

    monkeypatch.setattr(lag_testsvar, "EkteKI", falsk_ekte_ki)
    return laget


def test_fr38_main_bruker_standardmodellen_naar_modellen_er_tom(testdata, monkeypatch, tmp_path):
    """FR-38: med ANTHROPIC_MODEL= tom, som i .env.example, brukes STANDARD_MODELL."""
    _env_fil(monkeypatch, tmp_path, "ANTHROPIC_API_KEY=sk-fra-env\nANTHROPIC_MODEL=\n")
    laget = _tell_ekte_ki(monkeypatch)
    assert lag_testsvar.main(["--ut", str(tmp_path / "ut")], testdata) == 0
    assert laget == [("sk-fra-env", STANDARD_MODELL)]


def test_fr38_main_bruker_nokkel_og_modell_fra_miljoet(testdata, monkeypatch, tmp_path):
    """FR-38: main lager EkteKI med nøkkelen og modellen fra miljøet, leser .env-fila til
    nettsiden, og gir 0 når alt er skrevet og 1 når et case feiler."""
    _env_fil(monkeypatch, tmp_path, "ANTHROPIC_API_KEY=sk-fra-env\n")
    monkeypatch.setenv("ANTHROPIC_MODEL", "claude-test")
    laget = _tell_ekte_ki(monkeypatch)
    ut = tmp_path / "ut"
    assert lag_testsvar.main(["--ut", str(ut)], testdata) == 0
    assert laget == [("sk-fra-env", "claude-test")]
    assert (ut / "case-1-utvikler" / "brev-1.json").exists()

    monkeypatch.setattr(lag_testsvar, "EkteKI", lambda nokkel, modell: FalskKI("gap"))
    assert lag_testsvar.main([], testdata) == lag_testsvar.KI_FEILET == 1
