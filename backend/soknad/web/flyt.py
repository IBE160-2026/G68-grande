"""Søknaden i økten og stegsjekken for sidene (AD-7, AD-8)."""

from functools import wraps

from flask import current_app, redirect, session, url_for
from werkzeug.wrappers import Response

from soknad.adaptere.ki import TestKI
from soknad.kjerne.okt import Soknad
from soknad.kjerne.steg import Steg, kan_vises
from soknad.web.innlogging import OKT_ID, oktlager

# Siden for hvert steg.
SIDE_FOR_STEG = {
    Steg.START: "web.start",
    Steg.MODUS: "web.modus",
    Steg.INNLEGGING: "web.innlegging",
    Steg.RESULTAT: "web.resultat",
    Steg.BREV: "web.brev",
}


def ki() -> TestKI:
    """KI-en for denne økten. Fram til Epic 4 er det alltid TestKI. Da velges utgaven ut fra
    Innlogging.testmodus, og typen blir KI-grensesnittet."""
    return current_app.extensions["test_ki"]


def gjeldende_soknad() -> Soknad:
    """Søknaden i denne økten. Finnes det ingen, er det en ny søknad på steg start."""
    return oktlager().hent_soknad(session.get(OKT_ID)) or Soknad()


def lagre_soknad(soknad: Soknad) -> None:
    oktlager().lagre_soknad(session.get(OKT_ID), soknad)


def erstatt_soknad(forventet: Soknad, soknad: Soknad) -> None:
    """Lagrer søknaden bare når den lagrede fortsatt er forventet. Brukes etter KI-kallet: er
    søknaden byttet ut med en ny fra startsiden i mellomtiden, vinner den nye."""
    oktlager().erstatt_soknad(session.get(OKT_ID), forventet, soknad)


def til_steget_hvis_opptatt(soknad: Soknad) -> Response | None:
    """Er søknaden opptatt (et KI-kall pågår), gir den en redirect til siden for steget, og
    ingenting skal lagres (AD-8, FR-27). Ellers None."""
    if soknad.opptatt:
        return redirect(url_for(SIDE_FOR_STEG[soknad.steg]))
    return None


def krever_steg(side: Steg):
    """Slipper bare inn når sidens steg ≤ søknadens steg, både for GET og POST. Ellers sendes
    brukeren til siden for steget sitt, og søknaden er uendret. Brukes under login_required."""

    def dekorator(visning):
        @wraps(visning)
        def innpakket(*args, **kwargs):
            steg = gjeldende_soknad().steg
            if not kan_vises(side, steg):
                return redirect(url_for(SIDE_FOR_STEG[steg]))
            return visning(*args, **kwargs)

        return innpakket

    return dekorator
