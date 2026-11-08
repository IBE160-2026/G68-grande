"""Alle tekster brukeren ser, samlet på ett sted."""

from soknad.kjerne.feil import FeilType, InndataFeil

LOGO = "Søknadsassistenten"

START_TITTEL = "Startside"
START_OVERSKRIFT = "Velkommen! 👋"
START_INGRESS = "Her lager du et søknadsbrev som passer til stillingen du vil søke på."

LOGG_INN_TITTEL = "Logg inn"
LOGG_INN_OVERSKRIFT = "Logg inn"
LOGG_INN_KNAPP = "Logg inn"
FELT_EPOST = "E-post"
FELT_PASSORD = "Passord"

# Feiltekstene slås opp med (felt, type). felt=None betyr hele skjemaet.
FEILTEKSTER = {
    ("epost", FeilType.TOM): "Fyll inn e-post",
    ("passord", FeilType.TOM): "Fyll inn passord",
    (None, FeilType.FEIL_INNLOGGING): "Feil e-post eller passord",
}


def feiltekst(feil: InndataFeil) -> str:
    return FEILTEKSTER[(feil.felt, feil.type)]
