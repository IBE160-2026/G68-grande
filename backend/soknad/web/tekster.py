"""Alle tekster brukeren ser, samlet på ett sted."""

from typing import NamedTuple

from soknad.innstillinger import MIN_PASSORD_LENGDE
from soknad.kjerne.feil import FeilType, InndataFeil, KIFeil, KIFeilType
from soknad.kjerne.okt import Modus

LOGO = "Søknadsassistenten"

START_TITTEL = "Startside"
START_OVERSKRIFT = "Velkommen! 👋"
START_INGRESS = "Her lager du et søknadsbrev som passer til stillingen du vil søke på."
START_KNAPP = "Begynn å lage søknad"

# Bryteren på startsiden og merkelappen oppe til høyre på de andre sidene (FR-32, FR-33).
TESTMODUS = "Testmodus"
TESTMODUS_STATUS = (
    "Du er i testmodus. Nettsiden bruker ferdige svar, og ingenting sendes til ekstern KI."
)
# Under bryteren når ANTHROPIC_API_KEY mangler.
MANGLER_NOKKEL = "Mangler API-nøkkel, se README"

# «Tilbake» på modusvalget (og senere på innleggingen og resultatsiden).
TILBAKE_KNAPP = "Tilbake"

MODUS_TITTEL = "Velg modus"
MODUS_OVERSKRIFT = "Hva vil du gjøre i dag?"


class ModusKort(NamedTuple):
    """Teksten på et modus-kort: ikon, modusnavn, handling og forklaring."""

    ikon: str
    navn: str
    handling: str
    forklaring: str


# Kortene i rekkefølge. Korrektur kommer i Epic 5.
MODUS_KORT = {
    Modus.FULL_GENERERING: ModusKort(
        "✨",
        "Full generering",
        "Skriv nytt brev",
        "Du legger inn CV-en og annonsen, så skriver vi et brev til deg.",
    ),
}

INNLEGGING_TITTEL = "Legg inn CV og annonse"
INNLEGGING_OVERSKRIFT = "Legg inn CV-en din og stillingsannonsen"
# Over feltene, bare i testmodus (FR-34).
TESTDATA_HJELP = "Testmodus: bruk filene i mappen backend/testdata/ i prosjektet."
LIM_INN_KNAPP = "Lim inn tekst"
LIM_INN_ETIKETT = "Lim inn teksten her"
SJEKK_KNAPP = "Sjekk CV-en min"
FEILBOKS_OVERSKRIFT = "Noe må fikses før du kan gå videre:"


class Innleggingsfelt(NamedTuple):
    """Et felt på innleggingen: ikon, feltnavn og navnet på feltet i skjermlesertekstene.
    Feltnavnet står også først i feiltekstene og i skjermlesertekstene til knappene."""

    ikon: str
    navn: str
    tomt: str


# Feltene i rekkefølge. Ditt søknadsbrev kommer i Epic 5.
INNLEGGINGSFELT = {
    "cv": Innleggingsfelt("📄", "CV", "CV-feltet"),
    "annonse": Innleggingsfelt("📢", "Stillingsannonse", "annonsefeltet"),
}


def lim_inn_skjermleser(felt: str) -> str:
    """«Lim inn tekst, CV»"""
    return f"{LIM_INN_KNAPP}, {INNLEGGINGSFELT[felt].navn}"


def tom_skjermleser(felt: str) -> str:
    """Søppelbøtta: «Tøm CV-feltet», «Tøm annonsefeltet»."""
    return f"Tøm {INNLEGGINGSFELT[felt].tomt}"


def er_tomt_skjermleser(felt: str) -> str:
    """Etter tømming: «CV-feltet er tømt», «Annonsefeltet er tømt»."""
    tomt = INNLEGGINGSFELT[felt].tomt
    return f"{tomt[0].upper()}{tomt[1:]} er tømt"


# Ventetegnet (FR-27). Overskriften er lik for alle handlinger, ventesetningen per handling.
VENTE_OVERSKRIFT = "På vei mot ny jobb"
VENTE_SJEKKER = "Vi sjekker CV-en din – det tar noen sekunder."

RESULTAT_TITTEL = "Resultat"
RESULTAT_OVERSKRIFT = "Slik passer CV-en din til stillingen"

# «i»-knappen: ikonet er bare pynt, og knappen har en egen tekst for skjermlesere (UX-DR11).
INFO_IKON = "i"

# Pynteikonene foran punktene i listene, skjult for skjermlesere (UX-DR21).
IKON_DEKKER = "✓"
IKON_MANGLER = "→"
IKON_TREFF = "✓"
IKON_IKKE_TREFF = "○"

GAP_OVERSKRIFT = "Gap-analyse"
GAP_INFO_SKJERMLESER = "Hva er en gap-analyse?"
GAP_INFO = (
    "En KI-vurdering av hvilke krav i annonsen CV-en dekker, og hvilke du kan jobbe videre med."
)
LAGET_AV_KI = "Laget av KI"
GAP_UNDERTEKST = "Kravene fra annonsen, sammenlignet med CV-en din."
GAP_DEKKER = "Dette dekker CV-en din"
GAP_MANGLER = "Dette kan du jobbe videre med"
# Tomme gap-lister (UX-DR13). 🎉 står for seg, så den kan skjules for skjermlesere.
GAP_DEKKER_TOM = "CV-en din dekker ingen av kravene ennå. Se hva du kan jobbe videre med."
GAP_MANGLER_TOM = "Bra jobbet! CV-en din dekker alle kravene i annonsen."
GAP_MANGLER_TOM_IKON = "🎉"

# Mellom gap-analysen og nøkkelordtreffet (FR-18).
KAN_SI_FORSKJELLIG = (
    "Gap-analysen og nøkkelordtreffet kan si litt forskjellig. Gap-analysen er en vurdering "
    "KI-en gjør, mens nøkkelordtreffet bare teller ord."
)

NOKKELORD_OVERSKRIFT = "Nøkkelordtreff"
NOKKELORD_INFO_SKJERMLESER = "Hva er nøkkelordtreff?"
NOKKELORD_INFO = (
    "En ordtelling av hvor mange av annonsens nøkkelord som står i CV-en. Det er bare en "
    "pekepinn på hvordan et ATS kan vurdere CV-en, ikke en garanti."
)
NOKKELORDTREFF_FORKLARING = "av nøkkelordene står i CV-en din"
NOKKELORD_TREFF_TOM = "Ingen av nøkkelordene står i CV-en ennå."
NOKKELORD_IKKE_TREFF_TOM = "Alle nøkkelordene står i CV-en din!"

ATS_OVERSKRIFT = "Hva er ATS og hva betyr det for deg?"
ATS_AVSNITT = (
    "Mange arbeidsgivere sender søknadene gjennom et ATS før et menneske leser dem. Et ATS er "
    "et dataprogram som blant annet ser etter ord fra annonsen.",
    "Står flere av nøkkelordene i CV-en din, er det større sjanse for at den blir lest. Men "
    "prosenten over er bare en pekepinn, ikke en garanti.",
)


def nokkelordtreff(antall_treff: int, antall: int, prosent: int) -> str:
    """«7 av 11 = 64 %», med vanlig mellomrom før %."""
    return f"{antall_treff} av {antall} = {prosent} %"


def nokkelord_treff_overskrift(antall: int) -> str:
    """«Står i CV-en (7)»"""
    return f"Står i CV-en ({antall})"


def nokkelord_ikke_treff_overskrift(antall: int) -> str:
    """«Står ikke i CV-en (4)»"""
    return f"Står ikke i CV-en ({antall})"


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
    ("cv", FeilType.TOM): "CV: Fyll inn feltet. Last opp en PDF eller lim inn tekst.",
    ("annonse", FeilType.TOM): (
        "Stillingsannonse: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
    ),
    ("cv", FeilType.IKKE_TESTDATA): (
        "CV: I testmodus fungerer bare testdataene fra mappen testdata/."
    ),
    ("annonse", FeilType.IKKE_TESTDATA): (
        "Stillingsannonse: I testmodus fungerer bare testdataene fra mappen testdata/."
    ),
}

# Feil fra KI-en (FR-28). Et ubrukelig svar får samme tekst som andre feil.
KI_FEILTEKSTER = {
    KIFeilType.NETTVERK: "Nettverksfeil, sjekk nettverkstilgangen.",
    KIFeilType.ANNET: "Noe gikk galt hos KI-tjenesten. Prøv på nytt.",
    KIFeilType.UBRUKELIG_SVAR: "Noe gikk galt hos KI-tjenesten. Prøv på nytt.",
}
# Under feilteksten i feilboksen, per side (FR-28, UX-DR7). Resultatsiden får sin i Epic 3.
KI_FEIL_BEHOLDT_INNLEGGING = "Det du har lagt inn, er ikke borte."
# Knappen i feilboksen som prøver KI-kallet på nytt.
PROV_PA_NYTT_KNAPP = "Prøv på nytt"


def feiltekst(feil: InndataFeil) -> str:
    return FEILTEKSTER[(feil.felt, feil.type)]


def ki_feiltekst(feil: KIFeil) -> str:
    return KI_FEILTEKSTER[feil.type]
