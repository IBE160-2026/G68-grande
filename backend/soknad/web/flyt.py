"""Søknaden i økten og stegsjekken for sidene (AD-7, AD-8)."""

from functools import wraps

from flask import current_app, redirect, session, url_for
from werkzeug.wrappers import Response

from soknad.adaptere.ki import KI
from soknad.kjerne.okt import Innlogging, Soknad
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


def har_nokkel() -> bool:
    """Sann når ANTHROPIC_API_KEY finnes (ikke bare mellomrom), altså når create_app har laget
    EkteKI. Uten nøkkel er bryteren låst på, og testmodus kan ikke slås av (FR-32)."""
    return current_app.extensions.get("ekte_ki") is not None


def ki(innlogging: Innlogging | None) -> KI:
    """KI-en for innloggingen (AD-3): EkteKI når testmodus er av, ellers TestKI. Rutene vet
    ikke hvilken som brukes. Uten ekte KI (ingen nøkkel) brukes TestKI, som aldri sender noe
    ut. Det skjer ikke i vanlig bruk, for uten nøkkel er testmodus alltid på. Utlogget
    (None) gir også TestKI. _med_ki i ruter.py gir den samme innloggingen hit og til
    til_start_uten_samtykke, så KI-en velges for samme testmodus som samtykket ble sjekket for."""
    ekte_ki = current_app.extensions.get("ekte_ki")
    if innlogging is not None and not innlogging.testmodus and ekte_ki is not None:
        return ekte_ki
    return current_app.extensions["test_ki"]


def til_start_uten_samtykke(soknad: Soknad, innlogging: Innlogging | None) -> Response | None:
    """En sikring før hvert KI-kall (AD-12, FR-36): er testmodus av og samtykket mangler, gir
    den en redirect til startsiden, og ingen tekst sendes til KI-en. Ellers None. I vanlig bruk
    kommer ikke søknaden forbi startsiden uten samtykke når testmodus er av. _med_ki i ruter.py
    gir den samme innloggingen hit og til ki(), så sjekken og valget av KI gjelder samme
    testmodus."""
    if innlogging is not None and not innlogging.testmodus and not soknad.samtykke:
        return redirect(url_for("web.start"))
    return None


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
