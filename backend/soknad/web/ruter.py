"""Rutene på nettsiden."""

from flask import current_app, redirect, render_template, request, url_for

from soknad.adaptere.db import epost_finnes, finn_bruker, lag_bruker
from soknad.kjerne.feil import FeilType, InndataFeil, KIFeil
from soknad.kjerne.inndata import sjekk_innlegging, sjekk_innlogging, sjekk_registrering
from soknad.kjerne.okt import (
    Modus,
    Soknad,
    Tekstfelt,
    begynn,
    sett_analyse,
    sett_brev,
    sett_inndata,
    sett_opptatt,
    velg_modus,
)
from soknad.kjerne.steg import Steg
from soknad.kjerne.telleregel import tell_treff
from soknad.web import tekster, web
from soknad.web.flyt import (
    erstatt_soknad,
    gjeldende_soknad,
    ki,
    krever_steg,
    lagre_soknad,
    til_steget_hvis_opptatt,
)
from soknad.web.innlogging import (
    gjeldende_innlogging,
    logg_inn_bruker,
    logg_ut_bruker,
    login_required,
    til_innloggingen,
)


@web.app_context_processor
def felles_tekster():
    """Gjør tekstene tilgjengelige i alle maler (logoen står i base.html), og sier om
    brukeren er logget inn og om testmodus er på. Da får alle sider etter innlogging
    hjørneraden med «Logg ut», og merkelappen «Testmodus» når testmodus er på."""
    innlogging = gjeldende_innlogging()
    return {
        "tekster": tekster,
        "innlogget": innlogging is not None,
        "testmodus": innlogging is not None and innlogging.testmodus,
    }


@web.route("/", methods=["GET", "POST"])
@login_required
def start():
    """GET lager alltid en ny søknad (testmodus i Innlogging beholdes), også mens en annen er
    opptatt. POST er «Begynn å lage søknad» og sender til modusvalget. Mens søknaden er opptatt,
    sendes POST til siden for steget uten at noe lagres (AD-8)."""
    if request.method == "POST":
        lagret = gjeldende_soknad()
        opptatt = til_steget_hvis_opptatt(lagret)
        if opptatt is not None:
            return opptatt
        lagre_soknad(begynn(lagret))
        return redirect(url_for("web.modus"))
    lagre_soknad(Soknad())
    # Bryteren er låst på fram til Epic 4. Uten nøkkel står «Mangler API-nøkkel, se README».
    mangler_nokkel = not (current_app.config.get("ANTHROPIC_API_KEY") or "").strip()
    return render_template("start.html", mangler_nokkel=mangler_nokkel)


@web.route("/modus", methods=["GET", "POST"])
@login_required
@krever_steg(Steg.MODUS)
def modus():
    """Modusvalget. Et trykk på et kort lagrer modusen og sender til innleggingen. Mens
    søknaden er opptatt, sendes POST til siden for steget uten at noe lagres (AD-8)."""
    if request.method == "GET":
        return render_template("modus.html")
    lagret = gjeldende_soknad()
    opptatt = til_steget_hvis_opptatt(lagret)
    if opptatt is not None:
        return opptatt
    try:
        valgt = Modus(request.form.get("modus", ""))
    except ValueError:
        # Ukjent modus: samme side på nytt uten redirect, og søknaden er uendret.
        return render_template("modus.html"), 400
    lagre_soknad(velg_modus(lagret, valgt))
    return redirect(url_for("web.innlegging"))


@web.route("/innlegging", methods=["GET", "POST"])
@login_required
@krever_steg(Steg.INNLEGGING)
def innlegging():
    """Innleggingen. POST lagrer alltid feltene med sett_inndata. «Tilbake» sender til
    modusvalget uten å sjekke dem. «Sjekk CV-en min» sjekker alle feltene samtidig. Med feil
    vises siden på nytt, uten redirect. Uten feil hentes analysen fra KI-en, og brukeren
    sendes til resultatsiden. En KIFeil gir siden på nytt med feilteksten (FR-28).

    Mens KI-en jobber, er søknaden opptatt. En ny POST da sendes til siden for steget, uten at
    noe lagres eller KI-en kalles (AD-8, FR-27). Er søknaden byttet ut med en ny fra startsiden
    mens KI-en jobbet, blir den nye stående, og analysen kastes."""
    if request.method == "GET":
        return _vis_innlegging(gjeldende_soknad(), feil=[])
    lagret = gjeldende_soknad()
    opptatt = til_steget_hvis_opptatt(lagret)
    if opptatt is not None:
        return opptatt
    handling = request.form.get("handling")
    if handling not in ("tilbake", "sjekk"):
        # Ukjent knapp: samme side på nytt, og søknaden er uendret.
        return _vis_innlegging(lagret, feil=[]), 400
    cv = request.form.get("cv", "")
    annonse = request.form.get("annonse", "")
    soknad = sett_inndata(lagret, cv=Tekstfelt(cv), annonse=Tekstfelt(annonse))
    lagre_soknad(soknad)
    if handling == "tilbake":
        return redirect(url_for("web.modus"))
    innlogging = gjeldende_innlogging()
    if innlogging is None:
        # Logget ut i en annen fane etter login_required: til innloggingen, ingen feilside.
        return til_innloggingen()
    caser = ki().caser if innlogging.testmodus else None
    feil = sjekk_innlegging(cv, annonse, caser)
    if feil:
        return _vis_innlegging(soknad, feil=feil)
    # Feltene er alt lagret med sett_inndata. Nå lagres søknaden som opptatt. Etter KI-kallene
    # lagrer finally resultatet uten opptatt: analysen når kallene lyktes, ellers søknaden fra
    # før, også ved et uventet unntak. Det lagres bare når søknaden i øktlageret fortsatt er den
    # som ble satt opptatt, så en ny søknad fra startsiden i en annen fane blir stående.
    opptatt_soknad = sett_opptatt(soknad, True)
    lagre_soknad(opptatt_soknad)
    ferdig = soknad
    try:
        nokkelord = ki().nokkelord(annonse)
        gap = ki().gap(cv, annonse)
        ferdig = sett_analyse(soknad, nokkelord=nokkelord, gap=gap)
    except KIFeil as ki_feil:
        return _vis_innlegging(soknad, feil=[], ki_feil=tekster.ki_feiltekst(ki_feil))
    finally:
        erstatt_soknad(opptatt_soknad, ferdig)
    return redirect(url_for("web.resultat"))


@web.route("/resultat", methods=["GET", "POST"])
@login_required
@krever_steg(Steg.RESULTAT)
def resultat():
    """Resultatsiden. Mangler analysen, sendes brukeren til innleggingen, også ved POST.

    POST er «Lag søknadsbrevet mitt» (FR-21, FR-22). Brevet hentes fra KI-en, lagres, og
    brukeren sendes til brevsiden. En KIFeil gir resultatsiden på nytt med feilteksten, uten
    redirect, og søknaden er uendret (FR-28). Mens KI-en jobber, er søknaden opptatt, og en ny
    POST sendes til siden for steget uten at KI-en kalles (AD-8, FR-27). Er søknaden byttet ut
    med en ny fra startsiden mens KI-en jobbet, blir den nye stående, og brevet kastes."""
    lagret = gjeldende_soknad()
    if lagret.nokkelord is None or lagret.gap is None:
        return redirect(url_for("web.innlegging"))
    if request.method == "GET":
        return _vis_resultat(lagret)
    opptatt = til_steget_hvis_opptatt(lagret)
    if opptatt is not None:
        return opptatt
    if request.form.get("handling") != "brev":
        # Ukjent knapp: samme side på nytt, og søknaden er uendret.
        return _vis_resultat(lagret), 400
    # Som på innleggingen: finally lagrer brevet når kallet lyktes, ellers søknaden fra før,
    # men bare når søknaden i øktlageret fortsatt er den som ble satt opptatt.
    opptatt_soknad = sett_opptatt(lagret, True)
    lagre_soknad(opptatt_soknad)
    ferdig = lagret
    try:
        svar = ki().brev(lagret.cv.tekst, lagret.annonse.tekst, forslag=1)
        ferdig = sett_brev(lagret, svar)
    except KIFeil as ki_feil:
        return _vis_resultat(lagret, ki_feil=tekster.ki_feiltekst(ki_feil))
    finally:
        erstatt_soknad(opptatt_soknad, ferdig)
    return redirect(url_for("web.brev"))


@web.route("/brev")
@login_required
@krever_steg(Steg.BREV)
def brev():
    """Brevsiden (FR-22, FR-26). Brevet vises bare og kan ikke redigeres. Uten brev sendes
    brukeren til resultatsiden."""
    soknad = gjeldende_soknad()
    if soknad.brev is None:
        return redirect(url_for("web.resultat"))
    return render_template("brev.html", avsnitt=soknad.brev["avsnitt"])


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


def _vis_innlegging(soknad, feil, ki_feil=None):
    """Viser innleggingen med det som er lagret i søknaden. feil er i samme rekkefølge som
    feltene på siden, høyst én per felt. ki_feil er teksten til en KI-feil, som står øverst i
    feilboksen, uten lenker, over «Det du har lagt inn, er ikke borte.» og «Prøv på nytt»."""
    feltfeil = {f.felt: tekster.feiltekst(f) for f in feil}
    tekst = {"cv": soknad.cv.tekst, "annonse": soknad.annonse.tekst}
    return render_template("innlegging.html", tekst=tekst, feltfeil=feltfeil, ki_feil=ki_feil)


def _vis_resultat(soknad, ki_feil=None):
    """Viser resultatsiden. Prosenten regnes med telleregelen fra den lagrede nøkkelordlisten
    og CV-en hver gang siden vises, så samme søknad alltid gir samme prosent (FR-15, FR-17).
    ki_feil er teksten til en KI-feil fra «Lag søknadsbrevet mitt», som står øverst i
    feilboksen over «Resultatet og det du har lagt inn, er ikke borte.» og «Prøv på nytt»."""
    treff = tell_treff(list(soknad.nokkelord), soknad.cv.tekst)
    return render_template(
        "resultat.html",
        gap=soknad.gap,
        treff=treff,
        nokkelordtreff=tekster.nokkelordtreff(treff.antall_treff, treff.antall, treff.prosent),
        ki_feil=ki_feil,
    )


def _vis_skjema(mal, epost, feil, skjemafeil=None):
    """Viser innloggingen eller registreringen med feltfeil og skjemafeil.
    feil er i samme rekkefølge som feltene på siden. skjemafeil er en tekst til
    skjemafeil-boksen som ikke er en InndataFeil («Du må logge inn først»)."""
    feltfeil = {f.felt: tekster.feiltekst(f) for f in feil if f.felt is not None}
    skjemafeil = next((tekster.feiltekst(f) for f in feil if f.felt is None), skjemafeil)
    # Fokus (autofocus, uten JavaScript): første felt med feil, ellers skjemafeil-boksen.
    fokus = next(iter(feltfeil), "skjemafeil" if skjemafeil else None)
    return render_template(mal, epost=epost, feltfeil=feltfeil, skjemafeil=skjemafeil, fokus=fokus)
