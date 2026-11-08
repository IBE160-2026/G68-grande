"""Alle tekster brukeren ser, samlet på ett sted."""

from soknad.innstillinger import MIN_PASSORD_LENGDE
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

# Lenken under innloggingsskjemaet: «Ny her? Registrer deg her».
TIL_REGISTRERING_TEKST = "Ny her?"
TIL_REGISTRERING_LENKE = "Registrer deg her"

REGISTRER_TITTEL = "Registrer deg"
REGISTRER_OVERSKRIFT = "Registrer deg"
REGISTRER_KNAPP = "Registrer deg"
FELT_GJENTA = "Gjenta passord"
PASSORD_HJELP = f"Minst {MIN_PASSORD_LENGDE} tegn"

# Lenken under registreringsskjemaet: «Har du allerede en bruker? Logg inn».
TIL_INNLOGGING_TEKST = "Har du allerede en bruker?"
TIL_INNLOGGING_LENKE = "Logg inn"

# Hjørneraden nederst på alle sider etter innlogging.
LOGG_UT_KNAPP = "Logg ut"

# Skjemafeil-boksen på innloggingen når man prøver en side uten å være logget inn.
MA_LOGGE_INN = "Du må logge inn først"

# Feiltekstene slås opp med (felt, type). felt=None betyr hele skjemaet.
FEILTEKSTER = {
    ("epost", FeilType.TOM): "Fyll inn e-post",
    ("epost", FeilType.EPOST_UGYLDIG): "E-posten er ikke gyldig",
    ("epost", FeilType.EPOST_FINNES): "Denne e-posten er allerede registrert",
    ("passord", FeilType.TOM): "Fyll inn passord",
    ("passord", FeilType.PASSORD_KORT): f"Passordet må ha minst {MIN_PASSORD_LENGDE} tegn",
    ("gjenta", FeilType.TOM): "Gjenta passordet",
    ("gjenta", FeilType.PASSORD_ULIKE): "Passordene er ikke like",
    (None, FeilType.FEIL_INNLOGGING): "Feil e-post eller passord",
}


def feiltekst(feil: InndataFeil) -> str:
    return FEILTEKSTER[(feil.felt, feil.type)]
