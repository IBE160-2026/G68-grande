"""Øktene ligger bare i minnet på serveren, nøklet på en tilfeldig økt-id."""

import secrets
import threading

from soknad.kjerne.okt import Innlogging


class Oktlager:
    """Innlogginger i minnet. Etter en omstart er lageret tomt, og alle er logget ut."""

    def __init__(self):
        self._innlogginger: dict[str, Innlogging] = {}
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

    def slett(self, okt_id: str | None) -> None:
        with self._las:
            self._innlogginger.pop(okt_id, None)
