"""Innloggingssjekken: cookien har bare økt-id-en, og øktene ligger i øktlageret."""

from functools import wraps

from flask import current_app, redirect, session, url_for

from soknad.adaptere.oktlager import Oktlager
from soknad.kjerne.okt import Innlogging

# Det eneste som står i den signerte cookien.
OKT_ID = "okt_id"


def oktlager() -> Oktlager:
    return current_app.extensions["oktlager"]


def gjeldende_innlogging() -> Innlogging | None:
    """Innloggingen for denne økten. En cookie uten økt i minnet gir None (utlogget)."""
    return oktlager().hent(session.get(OKT_ID))


def login_required(visning):
    """Slipper bare inn innloggede. Andre sendes til innloggingen."""

    @wraps(visning)
    def innpakket(*args, **kwargs):
        if gjeldende_innlogging() is None:
            # Gammel eller ukjent økt-id: cookien tømmes, og brukeren er utlogget.
            session.clear()
            return redirect(url_for("web.logg_inn"))
        return visning(*args, **kwargs)

    return innpakket


def logg_inn_bruker(bruker_id: int) -> None:
    """Sletter den gamle økten og lager en ny med ny, tilfeldig økt-id."""
    oktlager().slett(session.get(OKT_ID))
    session.clear()
    # Testmodus er alltid på fram til Epic 4.
    session[OKT_ID] = oktlager().ny(Innlogging(bruker_id, testmodus=True))
