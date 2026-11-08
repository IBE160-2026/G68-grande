"""Rutene på nettsiden."""

from flask import render_template

from soknad.web import tekster, web


@web.app_context_processor
def felles_tekster():
    """Gjør tekstene tilgjengelige i alle maler (logoen står i base.html)."""
    return {"tekster": tekster}


@web.route("/")
def start():
    return render_template("start.html")
