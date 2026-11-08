"""Felles fiksturer for testene."""

import pytest

import soknad
from soknad import create_app


@pytest.fixture(autouse=True)
def ingen_ekte_env(monkeypatch, tmp_path):
    """Testene leser aldri en ekte backend/.env eller innstillinger fra terminalen,
    så de gir samme svar på alle PC-er."""
    monkeypatch.setattr(soknad, "ENV_FIL", tmp_path / "finnes-ikke.env")
    for navn in ("SECRET_KEY", "ANTHROPIC_MODEL", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(navn, raising=False)


@pytest.fixture
def app():
    return create_app({"TESTING": True, "SECRET_KEY": "test-nokkel"})


@pytest.fixture
def client(app):
    return app.test_client()
