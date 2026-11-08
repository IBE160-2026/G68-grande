"""Rutene på nettsiden."""

from flask import current_app, redirect, render_template, request, url_for

from soknad.adaptere.db import finn_bruker
from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.inndata import sjekk_innlogging
from soknad.web import tekster, web
from soknad.web.innlogging import logg_inn_bruker, login_required


@web.app_context_processor
def felles_tekster():
    """Gjør tekstene tilgjengelige i alle maler (logoen står i base.html)."""
    return {"tekster": tekster}


@web.route("/")
@login_required
def start():
    return render_template("start.html")


@web.route("/logg-inn", methods=["GET", "POST"])
def logg_inn():
    if request.method == "GET":
        return _vis_logg_inn(epost="", feil=[])

    epost = request.form.get("epost", "")
    passord = request.form.get("passord", "")
    feil = sjekk_innlogging(epost, passord)
    if not feil:
        bruker_id = finn_bruker(current_app.config["DATABASE"], epost, passord)
        if bruker_id is not None:
            logg_inn_bruker(bruker_id)
            return redirect(url_for("web.start"))
        feil = [InndataFeil(None, FeilType.FEIL_INNLOGGING)]
    # Feil: samme side på nytt uten redirect. E-posten står igjen, passordet aldri.
    return _vis_logg_inn(epost=epost, feil=feil)


def _vis_logg_inn(epost, feil):
    feltfeil = {f.felt: tekster.feiltekst(f) for f in feil if f.felt is not None}
    skjemafeil = next((tekster.feiltekst(f) for f in feil if f.felt is None), None)
    # Fokus (autofocus, uten JavaScript): første felt med feil, ellers skjemafeil-boksen.
    fokus = next(iter(feltfeil), "skjemafeil" if skjemafeil else None)
    return render_template(
        "logg_inn.html", epost=epost, feltfeil=feltfeil, skjemafeil=skjemafeil, fokus=fokus
    )
