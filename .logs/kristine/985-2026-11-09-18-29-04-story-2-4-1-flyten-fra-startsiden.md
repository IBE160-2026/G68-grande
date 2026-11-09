# Story 2.4.1: Flyten fra startsiden til innleggingen

## 2026-11-09 kl. 18:29 — Kristine

### Oppgave
Kristine ba om story 2.4 med `/bmad-build`, og ville lese spec-en før koden ble laget. Målet er at man kan gå fra startsiden via modusvalget til innleggingen, og at nettsiden viser at den er i testmodus.

### Plan
- Spec-en for hele story 2.4 ble på ca. 2500 tokens (grensen er 1600). Kristine valgte å dele den i to:
  - **2.4.1** (denne): søknaden i økten, stegene, «Begynn å lage søknad», modusvalget og innleggingssiden med bare overskriften.
  - **2.4.2**: bryteren, teksten om testmodus og merkelappen «Testmodus». Står i `_bmad-output/implementation-artifacts/deferred-work.md`.
- Spec: [`spec-2-4-1-flyten-fra-startsiden-til-innleggingen.md`](../../my-project/9-koding/spec-2-4-1-flyten-fra-startsiden-til-innleggingen.md) (kopi av `_bmad-output/implementation-artifacts/`).
- Valg tatt av KI-en: innleggingssiden har bare overskriften til story 2.5, og «Tilbake» står til venstre slik epics-fila sier (i skissen står den i midten).
- Egen branch `story/2-4-1-flyten-fra-startsiden-til-innleggingen`. Hovedøkta skrev koden, og tre hjelpeagenter gikk gjennom den (blind, grensetilfeller, testhull).

### Resultat
- Ny kode: `kjerne/steg.py` (`Steg`, `kan_vises`), `Soknad`, `Modus`, `begynn` og `velg_modus` i `kjerne/okt.py`, søknaden i `adaptere/oktlager.py` (`slett` sletter begge), `web/flyt.py` (`krever_steg`), rutene `/` (GET og POST), `/modus` og `/innlegging`, malene `modus.html` og `innlegging.html`, og stilen for den store knappen og modus-kortene.
- Gjennomgangen: 13 funn. 3 er rettet (testbeskrivelser som lovet mer enn testen sjekket, to skjøre tekstsjekker og et testnavn), 9 er avvist med begrunnelse, og 1 er utsatt (CSRF/SameSite, som gjelder hele nettsiden, ført i `deferred-work.md`).
- 272 tester grønne (231 før), `ruff check` og `ruff format --check` grønne.
- Commits på branchen: `4e2bddc` (koden) og `7c150a7` (spec-kopi, rad i `my-project/README.md`, TO DO og prompt-logg 264–266). Notatene til refleksjonsrapporten er oppdatert (4.2), men mappen er utelatt fra Git med vilje.
- Sprint-status: story 2.4 står som `in-progress` og ikke `review`, fordi 2.4.2 gjenstår.
- Ikke pushet, og ingen PR ennå.
- `issues.md`: punktet «Neste steg: story 2.4» er lukket og erstattet av punktene under.
- Kristine prøvde nettsiden i nettleseren (startet med `uv run flask --app soknad run`): «det ser veldig bra ut». Nettsiden er stoppet igjen.

### Åpne punkter
- Story 2.4.1: push, PR med merknad om KI-feil, grønn CI og flette.
- Story 2.4.2 «Det som viser testmodus» (bryteren, teksten om testmodus og merkelappen «Testmodus») med egen branch og PR (`bmad-build`). Story 2.4 er ferdig når begge er flettet.
- Bestemme om `SESSION_COOKIE_SAMESITE="Lax"` skal settes, eller om CSRF bare nevnes i README (story 8.1, sammen med punktet om CSRF fra story 1.4).
