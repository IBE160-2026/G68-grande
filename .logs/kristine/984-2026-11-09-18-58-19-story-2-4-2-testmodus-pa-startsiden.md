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
- Prøvd i nettleseren av Kristine (nettsiden startet og åpnet av KI-en): bryteren, teksten om testmodus, Tab til bryteren, merkelappen og smal skjerm. Alt så bra ut.
- Spec-kopi i `my-project/9-koding/`, rad i `my-project/README.md`, TO DO og prompt-logg 269–271 (commit `70ec72c`). Notat om høykontrastmodus i notatene til refleksjonsrapporten (ikke i Git).
- [PR #11](https://github.com/IBE160-2026/G68-grande/pull/11) laget med merknad om KI-feil. CI grønn på Linux og Windows, og Kristine flettet den.
- Etter flettingen: story 2.4 er satt til `done` i `sprint-status.yaml` (og kopien i `my-project/7-sprint-planning/`), TO DO og prompt-logg 272 (commit `3844b74` på main, ikke pushet).

### Åpne punkter
- Neste steg: story 2.5 «Lime inn CV og stillingsannonse» med egen branch og PR (`bmad-build`).
- Epic 4: når testmodus kan slås av, er raden oppe til høyre tom på de andre sidene, men tar fortsatt litt plass over logoen.