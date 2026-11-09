"""Søknadsassistenten: Flask-appen lages i create_app()."""

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from soknad.adaptere.db import lag_database
from soknad.adaptere.ki import TestKI
from soknad.adaptere.oktlager import Oktlager
from soknad.innstillinger import MAKS_FORESPORSEL, STANDARD_MODELL

# backend/.env (valgfri). Den ligger én mappe over soknad/.
ENV_FIL = Path(__file__).resolve().parent.parent / ".env"

# backend/instance/ med databasen brukere.db. Mappen står i .gitignore.
INSTANCE_MAPPE = Path(__file__).resolve().parent.parent / "instance"


def create_app(test_config=None):
    """Lager Flask-appen. test_config vinner over miljøet og .env."""
    # override=False: verdier som alt står i miljøet, beholdes.
    load_dotenv(ENV_FIL, override=False, encoding="utf-8")

    # Maler og statiske filer hører til weblaget.
    app = Flask(
        __name__,
        instance_path=str(INSTANCE_MAPPE),
        template_folder="web/templates",
        static_folder="web/static",
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        ANTHROPIC_MODEL=os.environ.get("ANTHROPIC_MODEL") or STANDARD_MODELL,
        ANTHROPIC_API_KEY=os.environ.get("ANTHROPIC_API_KEY", ""),
        MAX_CONTENT_LENGTH=MAKS_FORESPORSEL,
        DATABASE=str(Path(app.instance_path) / "brukere.db"),
    )
    if test_config is not None:
        app.config.from_mapping(test_config)

    # Databasen og testbrukeren lages ved første oppstart, og bare én gang.
    lag_database(app.config["DATABASE"])
    # Hver app får sitt eget øktlager i minnet.
    app.extensions["oktlager"] = Oktlager()
    # Testmodus: de ferdige KI-svarene og testcasene, lest fra testdata/ én gang.
    app.extensions["test_ki"] = TestKI()

    from soknad.web import web

    app.register_blueprint(web)
    return app
