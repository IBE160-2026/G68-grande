"""Alle tekster brukeren ser, samlet på ett sted."""

from typing import NamedTuple

from soknad.innstillinger import (
    MAKS_FILSTORRELSE,
    MAKS_TEGN,
    MAKS_TEGN_EGET_BREV,
    MIN_PASSORD_LENGDE,
)
from soknad.kjerne.feil import FeilType, InndataFeil, KIFeil, KIFeilType
from soknad.kjerne.inndata import maks_tegn
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


class InfoPunkt(NamedTuple):
    """Et punkt i en «i»-boks: overskriften i fet skrift og teksten etter."""

    overskrift: str
    tekst: str


# Samtykket på startsiden, bare når testmodus er av (FR-36, UX-DR11).
SAMTYKKE_LINJE = "Teksten din sendes til ekstern KI."
SAMTYKKE_ETIKETT = "Jeg samtykker til bruk av KI"
SAMTYKKE_INFO_SKJERMLESER = "Hva betyr samtykket?"
SAMTYKKE_INFO = (
    InfoPunkt(
        "Hva samtykker jeg til?",
        "Teksten du legger inn, altså CV, brev og stillingsannonse, sendes til KI-tjenesten "
        "Claude fra selskapet Anthropic.",
    ),
    InfoPunkt(
        "Hvorfor sendes teksten?",
        "KI-tjenesten trenger teksten for å finne kravene i annonsen og skrive brevet.",
    ),
    InfoPunkt(
        "Lagres noe?", "Nei. Nettsiden lagrer ingenting du legger inn etter at du logger ut."
    ),
    InfoPunkt(
        "Personopplysninger:",
        "Vi anbefaler at du fjerner adresse, telefonnummer og fødselsdato fra CV-en først. "
        "Det er ditt valg.",
    ),
)
SAMTYKKE_FEIL = "Du må samtykke før du kan begynne"

# KI-merknaden nede til venstre i hjørneraden når testmodus er av (FR-35). Ikonet er bare
# pynt og skjules for skjermlesere.
KI_MERKNAD_IKON = "ⓘ"
KI_MERKNAD = "Teksten behandles av ekstern KI"

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


# Kortene i rekkefølge.
MODUS_KORT = {
    Modus.FULL_GENERERING: ModusKort(
        "✨",
        "Full generering",
        "Skriv nytt brev",
        "Du legger inn CV-en og annonsen, så skriver vi et brev til deg.",
    ),
    Modus.KORREKTUR: ModusKort(
        "✏️",
        "Korrektur",
        "Forbedre mitt brev",
        "Du har skrevet et brev selv. Vi forbedrer språket og beholder innholdet ditt.",
    ),
}

INNLEGGING_TITTEL = "Legg inn CV og annonse"
INNLEGGING_OVERSKRIFT = "Legg inn CV-en din og stillingsannonsen"
# Tittelen og overskriften i Korrektur, med brevfeltet (FR-8).
INNLEGGING_TITTEL_KORREKTUR = "Legg inn CV, brev og annonse"
INNLEGGING_OVERSKRIFT_KORREKTUR = "Legg inn CV-en din, brevet ditt og stillingsannonsen"
# Over feltene, bare i testmodus (FR-34).
TESTDATA_HJELP = "Testmodus: bruk filene i mappen backend/testdata/ i prosjektet."
# Over feltene i begge modusene (FR-8, story 6.1).
PDF_TIPS = (
    "Tips: PDF lagret fra Word leses best. Er CV-en laget i Canva eller et lignende program, "
    "kan teksten komme i feil rekkefølge. Lim den da heller inn."
)
# Hovedknappen i et tomt felt, foran «Lim inn tekst» (FR-8, story 6.1).
LAST_OPP_KNAPP = "Last opp PDF"
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


# Alle feltene i rekkefølge. Ditt søknadsbrev står bare på siden i Korrektur
# (inndata.felt_for_modus).
INNLEGGINGSFELT = {
    "cv": Innleggingsfelt("📄", "CV", "CV-feltet"),
    "eget_brev": Innleggingsfelt("✉️", "Ditt søknadsbrev", "brevfeltet"),
    "annonse": Innleggingsfelt("📢", "Stillingsannonse", "annonsefeltet"),
}


def lim_inn_skjermleser(felt: str) -> str:
    """«Lim inn tekst, CV»"""
    return f"{LIM_INN_KNAPP}, {INNLEGGINGSFELT[felt].navn}"


def last_opp_skjermleser(felt: str) -> str:
    """«Last opp PDF, CV»"""
    return f"{LAST_OPP_KNAPP}, {INNLEGGINGSFELT[felt].navn}"


def lastet_opp_skjermleser(felt: str, filnavn: str) -> str:
    """Etter at en fil er valgt: «CV lastet opp: cv.pdf». Med filnavn="" er det starten på
    teksten, som innlegging.js setter filnavnet etter."""
    return f"{INNLEGGINGSFELT[felt].navn} lastet opp: {filnavn}"


def maks_tegn_hjelp(felt: str) -> str:
    """Hjelpeteksten under tekstboksen: «Høyst 15 000 tegn.», og «Høyst 5 000 tegn.» for
    brevfeltet i Korrektur (NFR-11, story 6.1)."""
    return f"Høyst {_med_mellomrom(maks_tegn(felt))} tegn."


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


# Hovedknappen nederst på resultatsiden, til høyre for «Tilbake» (FR-21). I Korrektur heter
# den «Oppdater søknadsbrevet mitt» (FR-23), med samme ventetekst.
LAG_BREV_KNAPP = "Lag søknadsbrevet mitt"
OPPDATER_BREV_KNAPP = "Oppdater søknadsbrevet mitt"
VENTE_BREV = "Vi lager brevet ditt – det kan ta en liten stund."

BREV_TITTEL = "Søknadsbrev"
BREV_OVERSKRIFT = "Din ferdigstilte søknad!"
BREV_OVERSKRIFT_KORREKTUR = "Din oppdaterte søknad er ferdig!"

# Markeringene på brevsiden i Korrektur (FR-23, UX-DR15). Forklaringen står i en liten hvit
# boks over brevet, med en skjult tilleggstekst for skjermlesere. Hver endret setning er en
# knapp med den skjulte teksten «Endret setning» først, og trykk viser «Du skrev» med den
# gamle setningen, eller «(Ny setning)». Er ingenting endret eller fjernet, står
# INGENTING_ENDRET i stedet for forklaringen. Antallet fjernede står under brevet (fjernet).
KORREKTUR_FORKLARING = "Grønn og understreket = endret. Trykk på setningen for å se det du skrev."
KORREKTUR_FORKLARING_SKJERMLESER = "Endrede setninger er knapper."
ENDRET_SETNING_SKJERMLESER = "Endret setning"
DU_SKREV = "Du skrev"
NY_SETNING = "(Ny setning)"
INGENTING_ENDRET = "Vi fant ingenting å endre. Brevet ditt er bra som det er."

# Nedlastingen under brevet (FR-29, UX-DR16). Etter nedlasting blir knappen grønn med ✓ foran
# «Lastet ned som Word» eller «Lastet ned som PDF», hver knapp for seg. ✓ er bare pynt og
# skjules for skjermlesere.
LAST_NED_WORD = "Last ned som Word"
LASTET_NED_WORD = "Lastet ned som Word"
LAST_NED_PDF = "Last ned som PDF"
LASTET_NED_PDF = "Lastet ned som PDF"
FERDIG_IKON = "✓"
# Feilboksen øverst på brevsiden når filen ikke kan lages (FilFeil).
FIL_FEIL = "Vi klarte ikke å lage filen. Prøv på nytt."

# Vinduet etter nedlasting (FR-31, UX-DR17). Filnavnet står mellom overskriften og spørsmålet
# (filnavn_linje under). «Logg ut» bruker LOGG_UT_KNAPP.
VINDU_NEDLASTET_OVERSKRIFT = "Brevet er lastet ned!"
VINDU_NEDLASTET_TEKST = "Vil du lage en ny søknad eller logge ut?"
LAG_NY_SOKNAD_KNAPP = "Lag ny søknad"
BLI_HER_KNAPP = "Bli her"

# «Nytt forslag» under nedlastingen på brevsiden og vinduet som spør først (FR-25). Samme vindu
# spør på resultatsiden når et brev finnes (retro 3). Etter «Ja» står VENTE_BREV i ventetegnet.
NYTT_FORSLAG_KNAPP = "Nytt forslag"
VINDU_NYTT_FORSLAG_OVERSKRIFT = "Vil du ha et nytt forslag?"
VINDU_NYTT_FORSLAG_TEKST = (
    "Brevet du ser nå, blir slettet. Har du ikke lastet det ned, er det borte."
)
# Teksten i vinduet på resultatsiden, der brevet ikke vises (bestemt av Kristine 19. november
# 2026).
VINDU_NYTT_FORSLAG_TEKST_RESULTAT = (
    "Du har alt et brev. Det blir slettet hvis du trykker på «Ja, lag nytt forslag»."
)
JA_NYTT_FORSLAG_KNAPP = "Ja, lag nytt forslag"
AVBRYT_KNAPP = "Avbryt"

# Vinduet som spør før utlogging på brevsiden når brevet ikke er lastet ned i noe format
# (UX-DR17, UX-DR22, story 7.5). Knappene bruker LOGG_UT_KNAPP og AVBRYT_KNAPP.
VINDU_LOGG_UT_OVERSKRIFT = "Du har ikke lastet ned brevet."
VINDU_LOGG_UT_TEKST = "Vil du logge ut likevel? Brevet blir slettet."


def filnavn_linje(filnavn: str) -> str:
    """Under knappen etter nedlasting: «Filnavn: Soknad_2026-11-11.docx»."""
    return f"Filnavn: {filnavn}"


def fjernet(antall: int) -> str:
    """Under brevet i Korrektur: «1 setning er fjernet.» eller «2 setninger er fjernet.»."""
    return f"{antall} setning er fjernet." if antall == 1 else f"{antall} setninger er fjernet."


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


def _med_mellomrom(tall: int) -> str:
    """Tallet med mellomrom mellom tusenene: «15 000»."""
    return f"{tall:,}".replace(",", " ")


# Tegngrensene med mellomrom mellom tusenene: «15 000» og «5 000» for brevfeltet (NFR-11).
MAKS_TEGN_TEKST = _med_mellomrom(MAKS_TEGN)
MAKS_TEGN_EGET_BREV_TEKST = _med_mellomrom(MAKS_TEGN_EGET_BREV)
# Største fil i hvert felt: «5 MB» (story 6.2).
MAKS_FILSTORRELSE_TEKST = f"{MAKS_FILSTORRELSE // (1024 * 1024)} MB"

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
        "CV: I testmodus fungerer bare testdataene fra mappen backend/testdata/."
    ),
    ("annonse", FeilType.IKKE_TESTDATA): (
        "Stillingsannonse: I testmodus fungerer bare testdataene fra mappen backend/testdata/."
    ),
    # CV og annonse fra ulike testcaser. Teksten er bestemt av Kristine 14. november 2026.
    ("annonse", FeilType.ANNEN_CASE): (
        "Stillingsannonse: I testmodus må CV-en og annonsen være fra samme mappe i "
        "backend/testdata/."
    ),
    ("cv", FeilType.FOR_LANG): (
        f"CV: Teksten er for lang. Den kan være på høyst {MAKS_TEGN_TEKST} tegn."
    ),
    ("annonse", FeilType.FOR_LANG): (
        f"Stillingsannonse: Teksten er for lang. Den kan være på høyst {MAKS_TEGN_TEKST} tegn."
    ),
    # Brevfeltet i Korrektur (FR-8, FR-9, FR-34). Samme tekster som de andre feltene, men
    # grensen for lengden er lavere (retro 5, runde B).
    ("eget_brev", FeilType.TOM): (
        "Ditt søknadsbrev: Fyll inn feltet. Last opp en PDF eller lim inn tekst."
    ),
    ("eget_brev", FeilType.FOR_LANG): (
        "Ditt søknadsbrev: Teksten er for lang. Den kan være på høyst "
        f"{MAKS_TEGN_EGET_BREV_TEKST} tegn."
    ),
    ("eget_brev", FeilType.IKKE_TESTDATA): (
        "Ditt søknadsbrev: I testmodus fungerer bare testdataene fra mappen backend/testdata/."
    ),
    # Hele forespørselen er over MAKS_FORESPORSEL (story 6.2). Står i feilboksen uten feltnavn
    # og uten lenke (bestemt av Kristine 16. november 2026).
    (None, FeilType.FOR_STOR): (
        f"Filene er for store. Hver fil kan være på høyst {MAKS_FILSTORRELSE_TEKST}."
    ),
}

# Feilene for en opplastet fil, i alle tre feltene (FR-10, FR-11, FR-12, story 6.2). Feltnavnet
# står først, som i de andre feiltekstene.
for _navn, _felt in INNLEGGINGSFELT.items():
    FEILTEKSTER[(_navn, FeilType.FEIL_FILTYPE)] = f"{_felt.navn}: Feil filtype, prøv PDF."
    FEILTEKSTER[(_navn, FeilType.FOR_STOR)] = (
        f"{_felt.navn}: Filen er for stor. Den kan være på høyst {MAKS_FILSTORRELSE_TEKST}."
    )
    FEILTEKSTER[(_navn, FeilType.ULESELIG)] = (
        f"{_felt.navn}: Vi klarer ikke å lese teksten i PDF-en. Den kan være skannet. "
        "Lim inn teksten i stedet."
    )
del _navn, _felt

# Feil fra KI-en (FR-28). Et ubrukelig svar får samme tekst som andre feil.
KI_FEILTEKSTER = {
    KIFeilType.NETTVERK: "Nettverksfeil, sjekk nettverkstilgangen.",
    KIFeilType.ANNET: "Noe gikk galt hos KI-tjenesten. Prøv på nytt.",
    KIFeilType.UBRUKELIG_SVAR: "Noe gikk galt hos KI-tjenesten. Prøv på nytt.",
}
# Under feilteksten i feilboksen, per side (FR-28, UX-DR7).
KI_FEIL_BEHOLDT_INNLEGGING = "Det du har lagt inn, er ikke borte."
KI_FEIL_BEHOLDT_RESULTAT = "Resultatet og det du har lagt inn, er ikke borte."
# På brevsiden når «Nytt forslag» feiler (FR-25).
KI_FEIL_BEHOLDT_BREV = "Brevet du hadde, er beholdt."
# Knappen i feilboksen som prøver KI-kallet på nytt.
PROV_PA_NYTT_KNAPP = "Prøv på nytt"
# I feilboksen når søknaden har brukt alle KI-kallene (NFR-11), uten «Prøv på nytt».
KI_KALL_BRUKT = (
    "Du har brukt alle KI-kallene for denne søknaden. Begynn på en ny søknad fra startsiden."
)
# Samme melding når søknaden har et brev: på brevsiden, og på innleggingen og resultatsiden
# med GA_TIL_BREVET_KNAPP i stedet for «Lag ny søknad», så brevet ikke slettes (retro 8, A1,
# A6, bestemt av Kristine 22. november 2026).
KI_KALL_BRUKT_BREV = (
    "Du har brukt alle KI-kallene for denne søknaden. Last ned brevet, så kan du lage en ny "
    "søknad i vinduet etter nedlastingen."
)
GA_TIL_BREVET_KNAPP = "Gå til brevet"


def feiltekst(feil: InndataFeil) -> str:
    return FEILTEKSTER[(feil.felt, feil.type)]


def ki_feiltekst(feil: KIFeil) -> str:
    return KI_FEILTEKSTER[feil.type]
