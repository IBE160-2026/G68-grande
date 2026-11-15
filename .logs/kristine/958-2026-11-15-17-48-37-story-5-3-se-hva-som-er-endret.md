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
- Etter 5.3: bedre flyt i brevet fra Korrektur (bindeord, sammenslåtte korte setninger). Endring i prompten med egen branch og PR, tre kjøringer med ekte KI (ca. 5 kr) og ny sjekk av kriterium 12.

## 2026-11-15 kl. 18:15 — Kristine

### Oppgave
Kristine prøvde brevsiden i nettleseren («det ser bra ut») og sa at brevet ikke har god flyt. Hun mente selve teksten fra KI-en.

### Plan
- KI-en misforsto først og trodde det var de grønne knappene som ikke fløt i avsnittet. Den gjorde dem om til `<span role="button">`, med Enter og mellomrom i `endringer.js`. Endringen ble ikke committet.
- Etter Kristines forklaring: se på teksten i `korrektur-1.json` og spørre hva som skal gjøres.

### Resultat
- Årsaken: prompten for Korrektur retter hver setning for seg, fordi den bare skal rette språk og ordvalg og beholde rekkefølgen (beslutningen i 5.2.1). Overgangene mellom setningene blir derfor ikke bedre.
- Kristine bestemte: flyten rettes i en egen oppgave etter 5.3 (prompt, tre kjøringer med ekte KI, ny sjekk av kriterium 12). Står i `my-project/todo.md` og `deferred-work.md`.
- Kristine bestemte: endringen av knappene angres. Den ble angret med `git restore`, og koden er som i `5c5e2cd`.

### Åpne punkter
- Etter 5.3: bedre flyt i brevet fra Korrektur, med egen branch og PR. Tre kjøringer med ekte KI (ca. 5 kr, Kristine godkjenner først).
- Flette [PR #37](https://github.com/IBE160-2026/G68-grande/pull/37). Etter flettingen: 5.3 og epic 5 til ferdig i sprint-status og TO DO, og retrospektiv for epic 5.

## 2026-11-15 kl. 18:25 — Kristine

### Oppgave
«push»: pushe branchen og lage PR for story 5.3.

### Plan
- Pushe `story-5-3-se-hva-som-er-endret`, lage PR med merknad om KI-feil, og kommentere nettlesertesten på PR-en.

### Resultat
- [PR #37](https://github.com/IBE160-2026/G68-grande/pull/37) er laget. KI-feilene står i PR-teksten: misforstått tilbakemelding om flyt (angret), spec uten alle seksjoner fra malen, og flyten i brevet som egen oppgave.
- Kommentar på PR-en om Kristines nettlesertest («det ser bra ut»).
- CI er grønn: backend på Linux og Windows, frontend og prosjektsjekken.

### Åpne punkter
- Flette PR #37. Etter flettingen: 5.3 og epic 5 til ferdig, og retrospektiv for epic 5.
- Etter 5.3: bedre flyt i brevet fra Korrektur (står allerede i `issues.md`).

## 2026-11-15 kl. 20:02 — Kristine

### Oppgave
«merget»: PR #37 er flettet. Oppdatere sprint-status, TO DO og logg.

### Plan
- Hente `main`, ta med loggcommiten som kom etter flettingen, og sette 5.3 og epic 5 til ferdig.

### Resultat
- `main` hentet (fletting `73e7873`). Den siste loggcommiten på branchen (`02f8aa1`) ble pushet etter flettingen, så den ble tatt med i `main` med cherry-pick.
- Sprint-status: 5.3 og epic 5 er ferdige (også kopien i `my-project/7-sprint-planning/`). TO DO: story 5.3 og risikopunktet om markerte endringer er krysset av. README har lenke til PR #37, og prompt-loggen har to nye rader.
- Ikke pushet: push til `main` ble stoppet av tillatelsene i Claude Code.

### Åpne punkter
- Retrospektiv for epic 5 (`bmad-retrospective`).
- Etter 5.3: bedre flyt i brevet fra Korrektur (står allerede i `issues.md`).
