"""Tester for create_app: oppstart uten .env og innstillinger (NFR-2, NFR-8)."""

from pathlib import Path

import pytest

import soknad
from soknad import create_app
from soknad.innstillinger import MAKS_FORESPORSEL, STANDARD_MODELL


@pytest.fixture
def uten_env(monkeypatch, tmp_path):
    """Som en ny kopi av repoet: ingen .env og ingen innstillinger i miljøet."""
    monkeypatch.setattr(soknad, "ENV_FIL", tmp_path / ".env")
    for navn in ("SECRET_KEY", "ANTHROPIC_MODEL", "ANTHROPIC_API_KEY"):
        # setenv først, så monkeypatch rydder opp også det load_dotenv skriver.
        monkeypatch.setenv(navn, "")
        monkeypatch.delenv(navn)


def test_nfr8_starter_uten_env_med_tilfeldig_secret_key(uten_env):
    """NFR-8: ny kopi uten .env starter, og SECRET_KEY er tilfeldig og minst 32 tegn."""
    app1 = create_app()
    app2 = create_app()
    assert len(app1.config["SECRET_KEY"]) >= 32
    assert app1.config["SECRET_KEY"] != app2.config["SECRET_KEY"]


def test_nfr8_standardverdier_uten_env(uten_env):
    """NFR-8: uten .env brukes standardmodellen, tom API-nøkkel og grensen på 16 MB."""
    app = create_app()
    assert app.config["ANTHROPIC_MODEL"] == STANDARD_MODELL == "claude-opus-5-5"
    assert app.config["ANTHROPIC_API_KEY"] == ""
    assert app.config["MAX_CONTENT_LENGTH"] == MAKS_FORESPORSEL == 16 * 1024 * 1024


def test_nfr2_innstillinger_fra_miljoet_brukes(uten_env, monkeypatch):
    """NFR-2: står SECRET_KEY og ANTHROPIC_MODEL i miljøet, brukes de verdiene."""
    monkeypatch.setenv("SECRET_KEY", "fra-miljoet")
    monkeypatch.setenv("ANTHROPIC_MODEL", "annen-modell")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "nokkel-fra-miljoet")
    app = create_app()
    assert app.config["SECRET_KEY"] == "fra-miljoet"
    assert app.config["ANTHROPIC_MODEL"] == "annen-modell"
    assert app.config["ANTHROPIC_API_KEY"] == "nokkel-fra-miljoet"


def test_nfr2_env_fil_leses_uten_aa_overstyre_miljoet(uten_env, monkeypatch, tmp_path):
    """NFR-2: backend/.env leses, men verdier som alt står i miljøet, vinner."""
    env_fil = tmp_path / ".env"
    env_fil.write_text(
        "SECRET_KEY=fra-fil\nANTHROPIC_MODEL=modell-fra-fil\nANTHROPIC_API_KEY=nokkel-fra-fil\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("ANTHROPIC_MODEL", "modell-fra-miljoet")
    app = create_app()
    assert app.config["SECRET_KEY"] == "fra-fil"
    assert app.config["ANTHROPIC_MODEL"] == "modell-fra-miljoet"
    assert app.config["ANTHROPIC_API_KEY"] == "nokkel-fra-fil"


def test_nfr2_nfr8_kopiert_tom_env_example_gir_standardverdier(uten_env, tmp_path):
    """NFR-2/NFR-8: en kopiert .env.example uten verdier gir de samme standardverdiene."""
    (tmp_path / ".env").write_text(
        "SECRET_KEY=\nANTHROPIC_MODEL=\nANTHROPIC_API_KEY=\n", encoding="utf-8"
    )
    app = create_app()
    assert len(app.config["SECRET_KEY"]) >= 32
    assert app.config["ANTHROPIC_MODEL"] == STANDARD_MODELL
    assert app.config["ANTHROPIC_API_KEY"] == ""


def test_nfr8_test_config_vinner_over_miljoet(uten_env, monkeypatch):
    """NFR-8: test_config vinner over miljøet."""
    monkeypatch.setenv("SECRET_KEY", "fra-miljoet")
    app = create_app({"TESTING": True, "SECRET_KEY": "x"})
    assert app.config["SECRET_KEY"] == "x"
    assert app.testing is True


def test_nfr2_env_example_har_ingen_verdier():
    """NFR-2: .env.example viser innstillingene, men uten verdier."""
    eksempel = Path(soknad.__file__).resolve().parent.parent / ".env.example"
    linjer = [
        linje.strip()
        for linje in eksempel.read_text(encoding="utf-8").splitlines()
        if linje.strip() and not linje.strip().startswith("#")
    ]
    assert linjer == ["ANTHROPIC_API_KEY=", "ANTHROPIC_MODEL=", "SECRET_KEY="]
