# Story 5.3: se hva som er endret i Korrektur

## 2026-11-15 kl. 17:48 — Kristine

### Oppgave
`/bmad-build 5.3`: vise på brevsiden i Korrektur hvilke setninger KI-en har endret, og hva brukeren skrev før, så studenten kan vurdere endringene (FR-23, kriterium 4).

### Plan
- Planen: [spec-5-3-se-hva-som-er-endret-i-korrektur.md](../../my-project/9-koding/spec-5-3-se-hva-som-er-endret-i-korrektur.md) (kopi av `_bmad-output/implementation-artifacts/`).
- Kristine bestemte: er setninger bare fjernet (ingen grønne), skjules forklaringen over brevet. Planen (ca. 2 700 tokens) beholdes hel.
- Branch `story-5-3-se-hva-som-er-endret`. En hjelpeagent kodet ut fra planen, tre gjennomgangsagenter (blind, edge-case, verification-gap) så på koden.

### Resultat
- Kjernen: `korrektur_visning()` i `ki_svar.py` avgjør alene hva som er endret (`gammel != [ny]`) og bruker samme gruppering i avsnitt som `korrigert_brev`, så siden og Word-fila har samme tekst. Fjernede telles som setninger i `gammel`.
- Brevsiden: grønne, understrekede knapper med skjult «Endret setning», «Du skrev» med den gamle setningen (eller «(Ny setning)»), forklaringen eller «Vi fant ingenting å endre …» over brevet, «1 setning er fjernet.» under. Nytt skript `endringer.js`, CSS med høykontrast. Word-fila er uten markeringer.
- Gjennomgangen: 15 funn. Rettet: den skjulte teksten ble med ved kopiering (`user-select: none`), tellingen av fjernede, navnet `antall_endret` og en docstring. Utsatt: ingen test kjører skriptet (`deferred-work.md`, TO DO for story 8.2). Resten avvist med begrunnelse i spec-en.
- 1029 tester består, ruff uten feil. Commit `5c5e2cd` (lokalt, ikke pushet). Sprint-status: 5.3 = review.
- Lukket punktet fra 5.2.1 om at «Du skrev» viser `gammel` etter vasken: godtatt i Design Notes i spec-en for 5.3.

### Åpne punkter
- Prøve brevsiden i Korrektur i nettleseren: 375 og 1280 px, åpne og lukke «Du skrev» (også flere samtidig), tastatur (Tab, Enter, mellomrom), høykontrast, Word-fila og Full generering. Se særlig om lange grønne setninger som begynner på ny linje, ser greie ut.
- Lage PR for story 5.3 med merknad om KI-feil, og kommentar etter nettlesertesten. Etter fletting: 5.3 og epic 5 til ferdig, og retrospektiv for epic 5.
