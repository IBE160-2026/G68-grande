"""Alle sider krever innlogging (FR-7, NFR-9).

Testen går gjennom alle registrerte ruter, så sider fra senere epics blir testet automatisk.
Bare innloggingen, registreringen og de statiske filene er åpne."""

import uuid

import pytest
from werkzeug.routing import (
    AnyConverter,
    BaseConverter,
    FloatConverter,
    IntegerConverter,
    Map,
    PathConverter,
    Rule,
    UnicodeConverter,
    UUIDConverter,
)

APNE_SIDER = {"web.logg_inn", "web.registrer", "static"}

# Eksempelverdier for argumentene i adressen, etter type. PathConverter arver fra
# UnicodeConverter, så den må stå først.
EKSEMPELVERDIER = [
    (PathConverter, "eksempel/sti"),
    (UnicodeConverter, "eksempel"),
    (IntegerConverter, 1),
    (FloatConverter, 1.5),
    (UUIDConverter, uuid.UUID(int=1)),
]


def eksempelverdi(regel, navn):
    # Werkzeug har ikke noe offentlig API for konverterene, så testen må rettes hvis navnet endres.
    konverterer = regel._converters[navn]
    if isinstance(konverterer, AnyConverter):
        return min(konverterer.items)
    for type_, verdi in EKSEMPELVERDIER:
        if isinstance(konverterer, type_):
            return verdi
    raise AssertionError(
        f"Testen kan ikke lage en eksempelverdi for <{navn}> i {regel.rule} "
        f"({type(konverterer).__name__}). Legg typen til i EKSEMPELVERDIER."
    )


def adresse(regel):
    verdier = {navn: eksempelverdi(regel, navn) for navn in regel.arguments}
    _, sti = regel.build(verdier, append_unknown=False)
    return sti


def test_nfr9_fr7_alle_sider_krever_innlogging(app):
    """FR-7/NFR-9: alle ruter unntatt innlogging, registrering og static sender den som ikke
    er logget inn, til /logg-inn?ikke_innlogget=1, med alle metoder (uten HEAD og OPTIONS)."""
    testet = set()
    for regel in app.url_map.iter_rules():
        if regel.endpoint in APNE_SIDER:
            continue
        sti = adresse(regel)
        for metode in sorted(regel.methods - {"HEAD", "OPTIONS"}):
            svar = app.test_client().open(sti, method=metode)
            assert svar.status_code == 302, f"{metode} {sti}"
            assert svar.location == "/logg-inn?ikke_innlogget=1", f"{metode} {sti}"
        testet.add(regel.endpoint)
    # Sjekker at testen faktisk fant sidene vi vet om.
    assert {"web.start", "web.logg_ut"} <= testet


def test_nfr9_eksempelverdi_feiler_for_ukjent_type():
    """NFR-9: testen feiler hvis den ikke kan lage en eksempelverdi for et argument."""

    class Ukjent(BaseConverter):
        pass

    kart = Map([Rule("/x/<ukjent:verdi>", endpoint="x")], converters={"ukjent": Ukjent})
    regel = next(kart.iter_rules())
    with pytest.raises(AssertionError, match="eksempelverdi"):
        eksempelverdi(regel, "verdi")


def test_nfr9_eksempelverdier_gir_gyldige_adresser():
    """NFR-9: eksempelverdiene for de vanlige typene gir adresser som kan bygges."""
    kart = Map(
        [
            Rule("/a/<navn>/<int:nr>/<float:tall>", endpoint="a"),
            Rule("/b/<path:sti>/<uuid:id>/<any(en, to):valg>", endpoint="b"),
        ]
    )
    adresser = [adresse(regel) for regel in kart.iter_rules()]
    assert adresser == [
        "/a/eksempel/1/1.5",
        "/b/eksempel/sti/00000000-0000-0000-0000-000000000001/en",
    ]
