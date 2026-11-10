"""Øktene ligger bare i minnet på serveren, nøklet på en tilfeldig økt-id."""

import secrets
import threading

from soknad.kjerne.okt import Innlogging, Soknad


class Oktlager:
    """Innlogginger og søknader i minnet. Etter en omstart er lageret tomt, og alle er
    logget ut."""

    def __init__(self):
        self._innlogginger: dict[str, Innlogging] = {}
        self._soknader: dict[str, Soknad] = {}
        self._las = threading.Lock()

    def ny(self, innlogging: Innlogging) -> str:
        """Lagrer innloggingen under en ny, tilfeldig økt-id og gir id-en tilbake."""
        okt_id = secrets.token_urlsafe(32)
        with self._las:
            self._innlogginger[okt_id] = innlogging
        return okt_id

    def hent(self, okt_id: str | None) -> Innlogging | None:
        if okt_id is None:
            return None
        with self._las:
            return self._innlogginger.get(okt_id)

    def hent_soknad(self, okt_id: str | None) -> Soknad | None:
        if okt_id is None:
            return None
        with self._las:
            return self._soknader.get(okt_id)

    def lagre_soknad(self, okt_id: str | None, soknad: Soknad) -> None:
        """Lagrer søknaden, men bare når økten finnes. Ellers kunne en søknad bli liggende
        igjen i minnet etter utlogging."""
        with self._las:
            if okt_id in self._innlogginger:
                self._soknader[okt_id] = soknad

    def erstatt_soknad(self, okt_id: str | None, forventet: Soknad, soknad: Soknad) -> bool:
        """Lagrer søknaden bare når den lagrede fortsatt er samme objekt som forventet, og
        økten finnes. Ellers er den byttet ut i mellomtiden (en ny søknad fra startsiden i en
        annen fane), og den nye blir stående. Sjekken er på identitet (is), og det virker
        fordi lageret har det samme objektet i minnet. Gir True når søknaden ble lagret."""
        with self._las:
            if okt_id in self._innlogginger and self._soknader.get(okt_id) is forventet:
                self._soknader[okt_id] = soknad
                return True
            return False

    def slett(self, okt_id: str | None) -> None:
        """Sletter både innloggingen og søknaden."""
        with self._las:
            self._innlogginger.pop(okt_id, None)
            self._soknader.pop(okt_id, None)
