# Story 7.3: gjenbruke nøkkelordlisten

## 2026-11-19 kl. 22:06 — Kristine

### Oppgave
`/bmad-build 7.3`: lage story 7.3 «Gjenbruke nøkkelordlisten når bare CV-en er endret». Når brukeren går tilbake fra resultatsiden og bare endrer CV-en, skal prosenten regnes fra den samme nøkkelordlisten, så hun ser om endringen faktisk ga bedre treff (FR-15, FR-19, kriterium 8).

### Plan
- Oppdaterte `epic-7-context.md` (7.2 ferdig, skriften Noto Sans), fordi arkitekturen var endret etter at konteksten ble laget.
- Spec: [spec-7-3-gjenbruke-nokkelordlisten-nar-bare-cv-en-er-endret.md](../../_bmad-output/implementation-artifacts/spec-7-3-gjenbruke-nokkelordlisten-nar-bare-cv-en-er-endret.md) (kopi i `my-project/9-koding/`).
- Kristine valgte samme vask som testmodus («C++» → «C#» regnes som lik annonse, retro 2 A11) og å beholde hele spec-en (ca. 2 400 tokens).
- Branch `story-7-3-gjenbruke-nokkelordlisten`. En underagent kodet, og tre underagenter gikk gjennom koden (blind, edge case, verification gap).

### Resultat
- `kjerne/okt.py`: `sett_inndata` beholder `nokkelord`, `nokkelord_annonse` og `arbeidsgiver` sammen når den vaskede annonsen er lik (og ikke tom). `web/ruter.py`: ved gjenbruk kalles bare `gap`, og grensen sjekkes for 1 kall (`GAP_KALL`).
- Ny testfil `tests/web/test_gjenbruk_nokkelord.py` med en falsk KI og testmodus av, fordi en endret CV ikke er testdata. Gamle tester i `test_okt.py`, `test_innlegging.py`, `test_resultat.py` og `test_grenser.py` er rettet.
- Endret oppførsel: også med helt lik tekst kalles nå bare `gap` (før 2 kall).
- Gjennomgangen ga 13 funn: 4 små rettinger (sjekk av tom vasket annonse, kommentar, docstring, test for «C++»/«C#»), 1 utsatt i `deferred-work.md`, resten avvist. Se Review Triage Log i spec-en.
- 1 305 tester består, `ruff check` og `ruff format --check` rene.
- Commits på branchen: `b296d0f` (story 7.3), `05903e1` (prompt-logg 487). Ikke pushet.
- Sprint-status: 7.3 = `review`, retro-punkt 15 fra epic 2 = `done`. TO DO har nytt punkt for 7.3. Notat for refleksjonsrapporten skrevet i `notater.md` (mappen er git-ignorert).
- Lukket i `issues.md`: punktet om å skrive de utsatte punktene fra retrospektiven for epic 2 inn i storiene (7.3 var det siste).

### Åpne punkter
- Prøve story 7.3 i nettleseren: case 1 i testmodus til resultatsiden, «Tilbake», tomme linjer i CV-en, «Sjekk CV-en min» → samme resultatside. Valgfritt med ekte KI (under 1 kr): legg til et manglende nøkkelord → samme liste, høyere prosent. Så push, PR med kommentar, grønn CI og fletting.
- Utsatt (`deferred-work.md`): lykkes nøkkelordkallet, men gap feiler i en analyse uten gjenbruk, kastes listen, og «Prøv på nytt» bruker 2 kall igjen.
