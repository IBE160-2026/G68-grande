"""Felles fiksturer for testene."""

import httpx2
import pytest
from werkzeug.security import generate_password_hash

import soknad
from soknad import create_app
from soknad.adaptere import db
from soknad.innstillinger import TESTBRUKER_EPOST, TESTBRUKER_PASSORD


@pytest.fixture(autouse=True)
def ingen_ekte_env(monkeypatch, tmp_path):
    """Testene leser aldri en ekte backend/.env eller innstillinger fra terminalen, og de
    skriver aldri til den ekte backend/instance/. Da gir de samme svar på alle PC-er."""
    monkeypatch.setattr(soknad, "ENV_FIL", tmp_path / "finnes-ikke.env")
    monkeypatch.setattr(soknad, "INSTANCE_MAPPE", tmp_path / "instance")
    for navn in (
        "SECRET_KEY",
        "ANTHROPIC_MODEL",
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_BASE_URL",
        "ANTHROPIC_CUSTOM_HEADERS",
    ):
        monkeypatch.delenv(navn, raising=False)


@pytest.fixture(autouse=True)
def nettsperre(monkeypatch):
    """Sperre mot ekte HTTP-kall med httpx2 uten async (NFR-11, AD-13). Det er det Anthropic
    og EkteKI bruker. Bare httpx2.HTTPTransport.handle_request stoppes, ikke async-transporten,
    socket eller urllib. Prøver en test et slikt kall (for eksempel EkteKI uten falsk klient),
    kastes httpx2.ConnectError, og forsøket noteres. EkteKI gjør feilen om til
    KIFeil(nettverk), så testen kan se grønn ut. Derfor feiler testen etterpå når noe er
    notert. Fiksturen gir lista med forsøkene, så testen av sperren kan tømme den."""
    forsok: list[str] = []

    def stopp(self, request):
        forsok.append(f"{request.method} {request.url}")
        raise httpx2.ConnectError("Testene skal ikke nå nettet.", request=request)

    monkeypatch.setattr(httpx2.HTTPTransport, "handle_request", stopp)
    yield forsok
    if forsok:
        pytest.fail(f"Testen prøvde å nå nettet: {', '.join(forsok)}")


@pytest.fixture(autouse=True)
def rask_hash(monkeypatch):
    """Werkzeugs vanlige hash (scrypt) tar nesten ett sekund på noen PC-er. Testene bruker
    derfor en raskere hash. test_db.py har en egen test av den ekte hashen."""

    def rask(passord):
        return generate_password_hash(passord, method="pbkdf2:sha256:1000")

    monkeypatch.setattr(db, "generate_password_hash", rask)


@pytest.fixture
def app():
    return create_app({"TESTING": True, "SECRET_KEY": "test-nokkel"})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def innlogget_client(client):
    """En klient som er logget inn med testbrukeren fra README."""
    svar = client.post("/logg-inn", data={"epost": TESTBRUKER_EPOST, "passord": TESTBRUKER_PASSORD})
    assert svar.status_code == 302
    return client
