"""Rutene på nettsiden."""

from datetime import date
from io import BytesIO

from flask import current_app, redirect, render_template, request, send_file, url_for

from soknad.adaptere import fil_ut
from soknad.adaptere.db import epost_finnes, finn_bruker, lag_bruker
from soknad.kjerne.feil import FeilType, FilFeil, InndataFeil, KIFeil
from soknad.kjerne.filnavn import lag_filnavn
from soknad.kjerne.inndata import sjekk_innlegging, sjekk_innlogging, sjekk_registrering
from soknad.kjerne.okt import (
    Modus,
    Soknad,
    Tekstfelt,
    begynn,
    har_plass_til,
    sett_analyse,
    sett_brev,
    sett_inndata,
    sett_lastet_ned,
    sett_opptatt,
    tell_ki_kall,
    velg_modus,
)
from soknad.kjerne.steg import Steg
from soknad.kjerne.telleregel import tell_treff
from soknad.web import tekster, web
from soknad.web.flyt import (
    SIDE_FOR_STEG,
    erstatt_soknad,
    gjeldende_soknad,
    har_nokkel,
    ki,
    krever_steg,
    lagre_soknad,
    til_start_uten_samtykke,
    til_steget_hvis_opptatt,
)
from soknad.web.innlogging import (
    endre_testmodus,
    gjeldende_innlogging,
    logg_inn_bruker,
    logg_ut_bruker,
    login_required,
    til_innloggingen,
)

# KI-kallene hver handling trenger (NFR-11): analysen er nøkkelord og gap, brevet er ett kall.
ANALYSE_KALL = 2
BREV_KALL = 1


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
    opptatt. Da er avkrysningsboksen for samtykket alltid tom. ?bryter=1 (etter bryteren) gir
    bryteren fokus.

    POST er «Begynn å lage søknad» og sender til modusvalget. Når testmodus er av, må boksen
    være krysset av (FR-36). Ellers vises startsiden på nytt med feilen, og steget er fortsatt
    start. Mens søknaden er opptatt, sendes POST til siden for steget uten at noe lagres
    (AD-8)."""
    if request.method == "POST":
        lagret = gjeldende_soknad()
        opptatt = til_steget_hvis_opptatt(lagret)
        if opptatt is not None:
            return opptatt
        innlogging = gjeldende_innlogging()
        if innlogging is None:
            # Logget ut i en annen fane etter login_required: til innloggingen.
            return til_innloggingen()
        samtykke = request.form.get("samtykke") == "ja"
        # Et samtykke som alt er lagret (søknaden er lenger fram i en annen fane), gjelder.
        if not innlogging.testmodus and not samtykke and not lagret.samtykke:
            return _vis_start(samtykke_feil=True)
        # I testmodus vises ingen boks, så et samtykke derfra lagres ikke.
        lagre_soknad(begynn(lagret, samtykke=samtykke and not innlogging.testmodus))
        return redirect(url_for("web.modus"))
    lagre_soknad(Soknad())
    return _vis_start(bryter_fokus=request.args.get("bryter") == "1")


@web.route("/testmodus", methods=["POST"])
@login_required
def bryter():
    """Bryteren «Testmodus» (FR-32). Skjemaet sender testmodus=av eller testmodus=paa, og
    brukeren sendes til startsiden med fokus på bryteren. Bryteren endres bare når søknaden er
    på steg start og ikke opptatt. Ellers sendes brukeren til siden for steget, og ingenting
    endres (AD-8). Uten API-nøkkel er testmodus alltid på, og ingenting endres."""
    lagret = gjeldende_soknad()
    if lagret.steg != Steg.START or lagret.opptatt:
        return redirect(url_for(SIDE_FOR_STEG[lagret.steg]))
    innlogging = gjeldende_innlogging()
    if innlogging is None:
        return til_innloggingen()
    valg = request.form.get("testmodus")
    if har_nokkel() and valg in ("av", "paa"):
        endre_testmodus(innlogging, testmodus=valg == "paa")
    return redirect(url_for("web.start", bryter=1))


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
    mens KI-en jobbet, blir den nye stående, og analysen kastes.

    Er testmodus av og samtykket mangler, sendes brukeren til startsiden uten KI-kall (AD-12).
    Med ekte KI telles KI-kallene i søknaden. Er det ikke plass til begge kallene i analysen,
    vises innleggingen med meldingen om det, uten KI-kall (NFR-11)."""
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
    # Testcasene finnes bare i TestKI, så de hentes derfra, ikke fra ki() (AD-3).
    caser = current_app.extensions["test_ki"].caser if innlogging.testmodus else None
    feil = sjekk_innlegging(cv, annonse, caser)
    if feil:
        return _vis_innlegging(soknad, feil=feil)
    uten_samtykke = til_start_uten_samtykke(soknad)
    if uten_samtykke is not None:
        return uten_samtykke
    # Én KI for begge kallene: slås testmodus av i en annen fane mellom kallene, går gap
    # likevel til samme KI som sjekken over gjaldt for (AD-12).
    valgt_ki = ki()
    # Med ekte KI telles hvert kall som 1. I testmodus telles ingen kall (NFR-11).
    per_kall = 1 if _bruker_ekte_ki(valgt_ki) else 0
    # Analysen trenger to kall (nøkkelord og gap). Er det ikke plass til begge, kalles ikke
    # KI-en. Feltene er alt lagret med sett_inndata, og telleren er uendret (NFR-11).
    if per_kall and not har_plass_til(soknad, ANALYSE_KALL):
        return _vis_innlegging(soknad, feil=[], ki_feil=tekster.KI_KALL_BRUKT, prov_pa_nytt=False)
    # Feltene er alt lagret med sett_inndata. Nå lagres søknaden som opptatt. Etter KI-kallene
    # lagrer finally resultatet uten opptatt: analysen når kallene lyktes, ellers søknaden fra
    # før, også ved et uventet unntak. Det lagres bare når søknaden i øktlageret fortsatt er den
    # som ble satt opptatt, så en ny søknad fra startsiden i en annen fane blir stående.
    # Hvert kall telles når det startes, også når det feiler, så telleren i det som lagres,
    # er riktig både når alt lykkes og ved KI-feil (NFR-11).
    opptatt_soknad = sett_opptatt(soknad, True)
    lagre_soknad(opptatt_soknad)
    ferdig = soknad
    kall = 0
    try:
        kall += per_kall
        nokkelord = valgt_ki.nokkelord(annonse)
        kall += per_kall
        gap = valgt_ki.gap(cv, annonse)
        ferdig = sett_analyse(soknad, nokkelord=nokkelord, gap=gap)
    except KIFeil as ki_feil:
        return _vis_innlegging(soknad, feil=[], ki_feil=tekster.ki_feiltekst(ki_feil))
    finally:
        erstatt_soknad(opptatt_soknad, tell_ki_kall(ferdig, kall))
    return redirect(url_for("web.resultat"))


@web.route("/resultat", methods=["GET", "POST"])
@login_required
@krever_steg(Steg.RESULTAT)
def resultat():
    """Resultatsiden. Mangler analysen, sendes brukeren til innleggingen, også ved POST.

    POST er «Lag søknadsbrevet mitt» (FR-21, FR-22). Brevet hentes fra KI-en, lagres, og
    brukeren sendes til brevsiden. En KIFeil gir resultatsiden på nytt med feilteksten, uten
    redirect, og søknaden er uendret bortsett fra telleren for KI-kall (FR-28). Mens KI-en
    jobber, er søknaden opptatt, og en ny POST sendes til siden for steget uten at KI-en kalles
    (AD-8, FR-27). Er søknaden byttet ut med en ny fra startsiden mens KI-en jobbet, blir den
    nye stående, og brevet kastes. Er testmodus av og samtykket mangler, sendes brukeren til
    startsiden uten KI-kall (AD-12). Med ekte KI og alle KI-kallene brukt vises resultatsiden
    med meldingen om det, uten KI-kall (NFR-11)."""
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
    uten_samtykke = til_start_uten_samtykke(lagret)
    if uten_samtykke is not None:
        return uten_samtykke
    valgt_ki = ki()
    per_kall = 1 if _bruker_ekte_ki(valgt_ki) else 0
    # Brevet trenger ett kall. Er det ikke plass, kalles ikke KI-en, og søknaden er uendret.
    if per_kall and not har_plass_til(lagret, BREV_KALL):
        return _vis_resultat(lagret, ki_feil=tekster.KI_KALL_BRUKT, prov_pa_nytt=False)
    # Som på innleggingen: finally lagrer brevet når kallet lyktes, ellers søknaden fra før,
    # men bare når søknaden i øktlageret fortsatt er den som ble satt opptatt. Kallet telles
    # når det startes, også når det feiler (NFR-11).
    opptatt_soknad = sett_opptatt(lagret, True)
    lagre_soknad(opptatt_soknad)
    ferdig = lagret
    kall = 0
    try:
        kall += per_kall
        svar = valgt_ki.brev(lagret.cv.tekst, lagret.annonse.tekst, forslag=1)
        ferdig = sett_brev(lagret, svar)
    except KIFeil as ki_feil:
        return _vis_resultat(lagret, ki_feil=tekster.ki_feiltekst(ki_feil))
    finally:
        erstatt_soknad(opptatt_soknad, tell_ki_kall(ferdig, kall))
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
    return _vis_brev(soknad)


@web.route("/last-ned/<any(docx):format>")
@login_required
@krever_steg(Steg.BREV)
def last_ned(format):
    """«Last ned som Word» (FR-29, FR-30, AD-8). Filen lages i minnet, lastet_ned settes, og
    filen sendes som vedlegg, så brevsiden blir stående. PDF kommer i Epic 7.

    Uten brev sendes brukeren til resultatsiden. Mens søknaden er opptatt, sendes brukeren til
    siden for steget uten fil. Kan filen ikke lages (FilFeil), vises brevsiden med feilboksen,
    og brevet er ikke borte. lastet_ned lagres bare når søknaden ikke er endret i mellomtiden."""
    lagret = gjeldende_soknad()
    if lagret.brev is None:
        return redirect(url_for("web.resultat"))
    opptatt = til_steget_hvis_opptatt(lagret)
    if opptatt is not None:
        return opptatt
    try:
        innhold = fil_ut.lag_docx(lagret.brev["avsnitt"])
    except FilFeil:
        return _vis_brev(lagret, fil_feil=True), 500
    erstatt_soknad(lagret, sett_lastet_ned(lagret))
    return send_file(
        BytesIO(innhold),
        mimetype=fil_ut.DOCX_MEDIETYPE,
        as_attachment=True,
        download_name=lag_filnavn(date.today(), format),
    )


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
            logg_inn_bruker(bruker_id, testmodus=not har_nokkel())
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
            logg_inn_bruker(bruker_id, testmodus=not har_nokkel())
            return redirect(url_for("web.start"))
        # E-posten ble registrert i mellomtiden.
        feil = [InndataFeil("epost", FeilType.EPOST_FINNES)]
    # Feil: samme side på nytt uten redirect. E-posten står igjen, passordene aldri.
    return _vis_skjema("registrer.html", epost=epost, feil=feil)


def _vis_start(samtykke_feil=False, bryter_fokus=False):
    """Viser startsiden. Med nøkkel står bryteren i et eget skjema, uten nøkkel er den låst på
    med «Mangler API-nøkkel, se README» (FR-32). samtykke_feil: «Begynn å lage søknad» uten
    avkryssing gir rød ramme, feilteksten og fokus på boksen (FR-36). bryter_fokus gir bryteren
    fokus etter at den er trykket, så tastaturbrukere ikke mister plassen."""
    return render_template(
        "start.html",
        har_nokkel=har_nokkel(),
        samtykke_feil=samtykke_feil,
        bryter_fokus=bryter_fokus,
    )


def _bruker_ekte_ki(valgt_ki) -> bool:
    """Sann når valgt_ki er ekte KI og ikke TestKI. Bare da telles KI-kallene, og bare da
    gjelder grensen på MAKS_KI_KALL (NFR-11)."""
    return valgt_ki is not current_app.extensions["test_ki"]


def _vis_innlegging(soknad, feil, ki_feil=None, prov_pa_nytt=True):
    """Viser innleggingen med det som er lagret i søknaden. feil er i samme rekkefølge som
    feltene på siden, høyst én per felt. ki_feil er teksten til en KI-feil, som står øverst i
    feilboksen, uten lenker, over «Det du har lagt inn, er ikke borte.» og «Prøv på nytt».
    prov_pa_nytt=False tar bort «Prøv på nytt», for meldingen om at alle KI-kallene er brukt
    (NFR-11)."""
    feltfeil = {f.felt: tekster.feiltekst(f) for f in feil}
    tekst = {"cv": soknad.cv.tekst, "annonse": soknad.annonse.tekst}
    return render_template(
        "innlegging.html",
        tekst=tekst,
        feltfeil=feltfeil,
        ki_feil=ki_feil,
        prov_pa_nytt=prov_pa_nytt,
    )


def _vis_resultat(soknad, ki_feil=None, prov_pa_nytt=True):
    """Viser resultatsiden. Prosenten regnes med telleregelen fra den lagrede nøkkelordlisten
    og CV-en hver gang siden vises, så samme søknad alltid gir samme prosent (FR-15, FR-17).
    ki_feil er teksten til en KI-feil fra «Lag søknadsbrevet mitt», som står øverst i
    feilboksen over «Resultatet og det du har lagt inn, er ikke borte.» og «Prøv på nytt».
    prov_pa_nytt=False tar bort «Prøv på nytt», for meldingen om at alle KI-kallene er brukt
    (NFR-11)."""
    treff = tell_treff(list(soknad.nokkelord), soknad.cv.tekst)
    return render_template(
        "resultat.html",
        gap=soknad.gap,
        treff=treff,
        nokkelordtreff=tekster.nokkelordtreff(treff.antall_treff, treff.antall, treff.prosent),
        ki_feil=ki_feil,
        prov_pa_nytt=prov_pa_nytt,
    )


def _vis_brev(soknad, fil_feil=False):
    """Viser brevsiden. Er brevet lastet ned, er knappen grønn og filnavnet står under, også
    når siden lastes på nytt (UX-DR16). fil_feil gir feilboksen øverst (FilFeil)."""
    return render_template(
        "brev.html",
        avsnitt=soknad.brev["avsnitt"],
        lastet_ned=soknad.lastet_ned,
        filnavn=lag_filnavn(date.today(), "docx"),
        fil_feil=fil_feil,
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
