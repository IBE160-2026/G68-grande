"""Søknaden i økten og stegsjekken for sidene (AD-7, AD-8)."""

from functools import wraps

from flask import redirect, session, url_for

from soknad.kjerne.okt import Soknad
from soknad.kjerne.steg import Steg, kan_vises
from soknad.web.innlogging import OKT_ID, oktlager

# Siden for hvert steg. Resultatsiden (story 2.6) og brevsiden (Epic 3) legges til her.
SIDE_FOR_STEG = {
    Steg.START: "web.start",
    Steg.MODUS: "web.modus",
    Steg.INNLEGGING: "web.innlegging",
}


def gjeldende_soknad() -> Soknad:
    """Søknaden i denne økten. Finnes det ingen, er det en ny søknad på steg start."""
    return oktlager().hent_soknad(session.get(OKT_ID)) or Soknad()


def lagre_soknad(soknad: Soknad) -> None:
    oktlager().lagre_soknad(session.get(OKT_ID), soknad)


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
