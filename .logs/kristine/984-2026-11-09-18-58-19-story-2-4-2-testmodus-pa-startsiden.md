# Story 2.4.2: Testmodus på startsiden og merkelappen

## 2026-11-09 kl. 18:58 — Kristine

### Oppgave
Lage story 2.4.2 med `bmad-build`: andre halvdel av story 2.4, det som viser at nettsiden er i testmodus. Sensor skal se at ingenting sendes til ekstern KI, og få vite at API-nøkkelen mangler.

### Plan
- Spec: [spec-2-4-2-testmodus-pa-startsiden-og-merkelappen.md](../../_bmad-output/implementation-artifacts/spec-2-4-2-testmodus-pa-startsiden-og-merkelappen.md) (godkjent av Kristine uten endringer, ca. 1900 tokens, ikke delt).
- Startsiden: bryteren «Testmodus» oppe til høyre (på og låst fram til Epic 4), «Mangler API-nøkkel, se README» når nøkkelen mangler, og teksten om testmodus i et statusområde over den store knappen.
- De andre sidene etter innlogging: merkelappen «Testmodus» oppe til høyre fra `base.html`.
- Hovedøkta skrev koden selv. Gjennomgang med tre hjelpere (blind, grensetilfeller, testhull).

### Resultat
- Branch `story/2-4-2-testmodus-pa-startsiden-og-merkelappen`, commit `f1bf5a4` (bare lokalt, ikke pushet).
- Endret: `web/tekster.py`, `web/ruter.py`, `templates/base.html`, `templates/start.html`, `static/css/stil.css`, `tests/web/hjelpere.py`, `tests/web/test_modusvalg.py`. Ny: `tests/web/test_testmodus.py`.
- Sporet og knotten bruker `aspect-ratio` i stedet for `height`, fordi en test fra før ikke tillater faste høyder.
- Gjennomgangen: 14 funn. 8 små rettinger (blant annet at bryteren synes i Windows' høykontrastmodus, en ny testhjelper `sett_testmodus` og flere CSS-sjekker), 6 avvist med begrunnelse. Ingenting utsatt til `deferred-work.md`. Detaljene står i spec-en.
- Funnet om at en test skriver rett i øktlageret kom også i 2.4.1. Denne gangen ble det rettet i stedet for avvist (prosesspunktet fra retrospektiven).
- Tester: 16 nye, 288 i alt, alle grønne. `ruff check` og `ruff format --check` grønne.
- Story 2.4 står som `review` i `sprint-status.yaml`. Spec-en er `done`.
- Ikke sjekket ennå: hvordan sidene ser ut i nettleseren.

### Åpne punkter
- Story 2.4.2: prøve i nettleseren (bryteren og teksten på startsiden, Tab til bryteren og trykk uten at noe skjer, merkelappen på modusvalget og innleggingen, ingen rulling sidelengs ved 320 og 375 px). Deretter spec-kopi, push, PR med merknad om KI-feil, grønn CI og flette.
- Epic 4: når testmodus kan slås av, er raden oppe til høyre tom på de andre sidene, men tar fortsatt litt plass over logoen.