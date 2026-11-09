# Story 2.5.1: Innleggingssiden

## 2026-11-09 kl. 19:47 — Kristine

### Oppgave
Kristine ba om story 2.5 «Lime inn CV og stillingsannonse» med `/bmad-build`, og ville lese spec-en før koden ble skrevet. Spec-en ble for lang (ca. 2800 tokens), og hun valgte å dele storyen i 2.5.1 (innleggingssiden) og 2.5.2 (analysen og første resultatside), som med story 2.4.

### Plan
- Spec: [`spec-2-5-1-innleggingssiden.md`](../../_bmad-output/implementation-artifacts/spec-2-5-1-innleggingssiden.md), åpnet i Notisblokk. Godkjent av Kristine («Godkjenn og fortsett»).
- 2.5.2 er skrevet inn i `_bmad-output/implementation-artifacts/deferred-work.md`.
- Branch `story/2-5-1-innleggingssiden` fra `main`. Hovedøkta skrev koden selv, og så gikk tre hjelpere gjennom endringen (blind, grensetilfeller, testhull).

### Resultat
- Commit `d5986c4` på branchen (ikke pushet):
  - Feltene «📄 CV» og «📢 Stillingsannonse» med «Lim inn tekst», tekstboks og søppelbøtte (nytt skript `innlegging.js`). Hjelpeteksten om `testdata/` vises i testmodus, og feltene står side om side fra 1000 px.
  - «Sjekk CV-en min» lagrer feltene (`sett_inndata` i `kjerne/okt.py`) og sjekker alle samtidig (`sjekk_innlegging` i `kjerne/inndata.py`). Feilboks med lenker til feltene.
  - «Tilbake» lagrer feltene uten å sjekke dem og sender til modusvalget.
  - `TestKI` lages én gang i `create_app`, og `ki()` i `web/flyt.py` gir den.
- Tester: 44 nye, 332 i alt, alle grønne. `ruff check` og `ruff format --check` er uten feil.
- Gjennomgangen ga 20 funn: 5 rettet, 14 avvist med begrunnelse og 1 utsatt (ingen nettlesertester av `innlegging.js`, ført i `deferred-work.md`). Alt står i tabellen i spec-en.
- Spec-en har status `done`. Story 2.5 står som `in-progress` i `sprint-status.yaml` til 2.5.2 også er ferdig.
- Prøvd i nettleseren av Kristine: alt virket, bortsett fra at en lenke i feilboksen så ut til å ikke gjøre noe (fokusringen vises ikke etter et museklikk). Rettet med `.lim-inn:focus` og en test i commit `022b315`. 333 tester.
- Spec-kopi, oversikten, TO DO og prompt-logg 273–276 i commit `810f3c1`.
- Kristine så at CI på `main` var rød etter PR #11. PR-en selv var grønn, men to kjøringer på `main` manglet jobber (midlertidig feil hos GitHub, alle jobbene som kjørte, var grønne). CI ble kjørt på nytt og ble grønn.
- Branchen ble pushet, og [PR #12](https://github.com/IBE160-2026/G68-grande/pull/12) ble laget med merknad om KI-feil. CI var grønn på Linux og Windows, og Kristine flettet PR-en (`34d7b39`). TO DO, kopien av sprint-statusen og prompt-logg 277 er oppdatert på `main`.

### Åpne punkter
- Story 2.5.2 «Analysen og første resultatside» med egen branch og PR (`bmad-build`), etter at 2.5.1 er flettet.
- Ingen automatisk test kjører `innlegging.js`. Kan vurderes i story 8.2 (testplanen).
