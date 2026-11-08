"""Weblaget: ruter, maler, tekster og statiske filer."""

from flask import Blueprint

web = Blueprint("web", __name__)

from soknad.web import ruter  # noqa: E402, F401  (rutene registreres på blueprinten)
