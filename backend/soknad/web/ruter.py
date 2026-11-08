"""Rutene på nettsiden."""

from flask import current_app, redirect, render_template, request, url_for

from soknad.adaptere.db import epost_finnes, finn_bruker, lag_bruker
from soknad.kjerne.feil import FeilType, InndataFeil
from soknad.kjerne.inndata import sjekk_innlogging, sjekk_registrering
from soknad.web import tekster, web
from soknad.web.innlogging import (
    gjeldende_innlogging,
    logg_inn_bruker,
    logg_ut_bruker,
    login_required,
)


@web.app_context_processor
def felles_tekster():
    """Gjør tekstene tilgjengelige i alle maler (logoen står i base.html), og sier om
    brukeren er logget inn. Da får alle sider etter innlogging hjørneraden med «Logg ut»."""
    return {"tekster": tekster, "innlogget": gjeldende_innlogging() is not None}


@web.route("/")
@login_required
def start():
    return render_template("start.html")


@web.route("/logg-ut", methods=["POST"])
@login_required
def logg_ut():
    """Bare POST: sletter økten og sender til innloggingen uten melding."""
    logg_ut_bruker()
    return redirect(url_for("web.logg_inn"))


@web.route("/logg-inn", methods=["GET", "POST"])
def logg_inn():
    if gjeldende_innlogging() is not None:
        # Alt logget inn: rett til startsiden. Ingenting sjekkes, og økten er uendret.
        return redirect(url_for("web.start"))
    if request.method == "GET":
        # Sendt hit fra en side som krever innlogging: «Du må logge inn først».
        vis = request.args.get("ikke_innlogget") == "1"
        melding = tekster.MA_LOGGE_INN if vis else None
        return _vis_skjema("logg_inn.html", epost="", feil=[], skjemafeil=melding)

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
    return _vis_skjema("logg_inn.html", epost=epost, feil=feil)


@web.route("/registrer", methods=["GET", "POST"])
def registrer():
    if gjeldende_innlogging() is not None:
        # Alt logget inn: rett til startsiden. Ingenting sjekkes eller lagres.
        return redirect(url_for("web.start"))
    if request.method == "GET":
        return _vis_skjema("registrer.html", epost="", feil=[])

    database = current_app.config["DATABASE"]
    epost = request.form.get("epost", "")
    passord = request.form.get("passord", "")
    gjenta = request.form.get("gjenta", "")
    feil = sjekk_registrering(epost, passord, gjenta)
    # Om e-posten finnes, sjekkes bare når den ellers er gyldig. Den står først i lista.
    epost_ok = not any(f.felt == "epost" for f in feil)
    if epost_ok and epost_finnes(database, epost):
        feil.insert(0, InndataFeil("epost", FeilType.EPOST_FINNES))
    if not feil:
        bruker_id = lag_bruker(database, epost, passord)
        if bruker_id is not None:
            logg_inn_bruker(bruker_id)
            return redirect(url_for("web.start"))
        # E-posten ble registrert i mellomtiden.
        feil = [InndataFeil("epost", FeilType.EPOST_FINNES)]
    # Feil: samme side på nytt uten redirect. E-posten står igjen, passordene aldri.
    return _vis_skjema("registrer.html", epost=epost, feil=feil)


def _vis_skjema(mal, epost, feil, skjemafeil=None):
    """Viser innloggingen eller registreringen med feltfeil og skjemafeil.
    feil er i samme rekkefølge som feltene på siden. skjemafeil er en tekst til
    skjemafeil-boksen som ikke er en InndataFeil («Du må logge inn først»)."""
    feltfeil = {f.felt: tekster.feiltekst(f) for f in feil if f.felt is not None}
    skjemafeil = next((tekster.feiltekst(f) for f in feil if f.felt is None), skjemafeil)
    # Fokus (autofocus, uten JavaScript): første felt med feil, ellers skjemafeil-boksen.
    fokus = next(iter(feltfeil), "skjemafeil" if skjemafeil else None)
    return render_template(mal, epost=epost, feltfeil=feltfeil, skjemafeil=skjemafeil, fokus=fokus)
