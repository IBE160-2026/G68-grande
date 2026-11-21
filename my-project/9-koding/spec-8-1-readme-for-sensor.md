---
title: 'Story 8.1: README for sensor'
type: 'chore'
created: '2026-11-21'
status: 'done'
baseline_commit: '606534aac2b6e865f31eda245fd8115ee0a7f8a8'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-8-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** README er oppdatert i hver story, men er ikke ferdig for sensor. «Skjermbilder» står som «Kommer», statuslinja sier at kodingen pågår, og tre kjente begrensninger mangler: at nettsiden ikke har CSRF-vern, at korte nøkkelord ikke gir treff inne i lengre ord, og hva som skjer med SameSite-cookien. I tillegg mangler noen mapper i mappestrukturen og lenkene til retro 5–7. Sensor vurderer README og kjørbarhet for seg (10 %), og skjermbilder nevnes i sensorveiledningen.

**Approach:** README fullføres mot alle punktene i NFR-8 (story 8.1 i `epics.md`). Kristine tar to–tre skjermbilder med ekte KI og fiktive testdata, og README viser dem. Etterpå krysses de åpne punktene for 8.1 av i `deferred-work.md`, `issues.md` og `todo.md`.

## Boundaries & Constraints

**Always:** Bare fiktive testdata i skjermbildene, med testmodus av («Teksten behandles av ekstern KI» synlig). Kristines egne formuleringer i README beholdes. Det som står fra før, endres bare der det er feil eller utdatert. Hver påstand i README skal stemme med koden (kommandoer, filnavn, innstillinger, grenser). Lærerens CI-sjekk (`test -f README.md` og `test -f my-project/1-product-brief/product-brief.md` i `.github/workflows/ci.yml`) må fortsatt gå gjennom.

**Never:** Ikke testplanen eller prøven fra en ny kopi (story 8.2, issue #16). Ikke CSRF-tokens eller andre nye sikkerhetsfunksjoner i koden. Ingen API-nøkkel, ekte CV eller `.env` i repoet eller på skjermbildene.

**Kristines beslutninger (2026-11-21):**
1. **CSRF:** README sier under «Kjente begrensninger» at nettsiden ikke har CSRF-beskyttelse, og at den må legges til før nettsiden legges på nett. I tillegg settes `SESSION_COOKIE_SAMESITE="Lax"` i `create_app`, med en test.
2. **«SQL» i «MySQL»:** punktet om telleregelen får en setning om at korte nøkkelord (1–3 tegn) ikke gir treff inne i lengre ord, for eksempel «SQL» i «MySQL» og «PostgreSQL».
3. **Skjermbilder:** tre PNG-er med case 1 og testmodus av, tatt av Kristine: `my-project/skjermbilder/resultatside.png` (gap-analyse og nøkkelordtreff), `brevside.png` (Full generering) og `korrektur.png` (markerte endringer). Seksjonen «Skjermbilder» flyttes opp rett under «Hvem den er for».

</frozen-after-approval>

## Code Map

- `README.md` -- hele leveransen. Linje 13: statuslinja (fjerne «Kodingen er i gang» og setningen om «kommer»). Linje 105–107: «Skjermbilder» / «*Kommer.*». Linje 111: innledningen «Flere kan komme til når nettsiden er laget». Linje 115: punktet om telleregelen (spørsmål 2). Linje 129–146: mappestrukturen mangler `backend/prompts/` (promptene til Claude), `backend/instance/` (databasen, lages ved oppstart), `my-project/testplan.md` og `my-project/testkjoringer/`. Linje 171: retro-lenkene stopper ved epic 4 (5, 6 og 7 finnes i `my-project/9-koding/`).
- `backend/soknad/__init__.py:64-70` -- `app.config.from_mapping(...)`, der `SESSION_COOKIE_SAMESITE="Lax"` settes (beslutning 1). `test_config` kan fortsatt overstyre.
- `backend/tests/test_app.py` -- testene for innstillingene (`test_nfr8_*`). Den nye testen for SameSite hører hjemme her, og helst sjekker den også `Set-Cookie` etter innlogging.
- `backend/.env.example` -- stemmer med tabellen i README (tre innstillinger). Endres ikke.
- `my-project/testplan.md:407-425` -- tabellprøven fra 6.1 (bestått). README linje 118 viser allerede til den.
- `_bmad-output/implementation-artifacts/deferred-work.md:1-3, 11-13, 17-19` -- de tre punktene for 8.1 (CSRF, «SQL» i «MySQL», SameSite) får `resolved:`.
- `.logs/kristine/issues.md:13, 42, 50, 57` -- de åpne punktene for README og 8.1 krysses av med dato.
- `my-project/todo.md:195` -- punktet om README-seksjonene merket «kommer».

## Tasks & Acceptance

**Execution:**
- [x] `README.md` -- statuslinja, innledningen til kjente begrensninger, CSRF-punktet og «SQL» i «MySQL», mappestrukturen (også `my-project/skjermbilder/`), retro-lenkene 5–7 og lenken til testplanen -- NFR-8 og de åpne punktene for 8.1
- [x] `backend/soknad/__init__.py` og `backend/tests/test_app.py` -- `SESSION_COOKIE_SAMESITE="Lax"` og en test som sjekker verdien -- beslutning 1
- [x] `README.md` -- seksjonen «Skjermbilder» flyttes opp under «Hvem den er for», med de tre bildene og alternativtekst for hvert -- FR-38, NFR-6, beslutning 3
- [ ] Kristine (for hånd) -- tar de tre skjermbildene og lagrer dem med navnene i beslutning 3 -- FR-38 krever ekte KI, nettleser og API-nøkkel
- [x] `deferred-work.md`, `.logs/kristine/issues.md`, `my-project/todo.md` -- krysse av punktene for 8.1 -- regelen om utsatte punkter

**Acceptance Criteria:**
- Given README etter story 8.1, when den leses fra toppen, then står ingen seksjon som «kommer», og statuslinja sier at nettsiden er ferdig
- Given punktlisten i NFR-8 (story 8.1 i `epics.md`), when hvert punkt sjekkes mot README, then finnes alle, også CSRF under kjente begrensninger
- Given hver kommando, filsti og innstilling i README, when de sjekkes mot repoet, then finnes de og stemmer
- Given bildene i «Skjermbilder», when README vises på GitHub, then vises to–tre bilder med alternativtekst, med testmodus av og bare fiktive data
- Given `.github/workflows/ci.yml`, when CI kjører på PR-en, then går sjekken av README og product brief gjennom, sammen med pytest og ruff

## Implementation Notes

- 2026-11-21: README, SameSite og avkrysningene er gjort. 1393 tester består, og ruff gir ingen feil. Alternativtekstene bruker overskriftene og forklaringen fra `web/tekster.py`, uten prosent, fordi ekte KI kan gi et annet tall. To punkter i `issues.md` (linje 50 og 57) var markert som løst, men sto fortsatt som åpne. De er nå krysset av. Punktet om «kommer» i `issues.md` og `todo.md` står åpent til skjermbildene er tatt. Kristine tar skjermbildene før PR-en, og fram til da viser README tre bilder som mangler.

## Spec Change Log

## Review Triage Log

| # | Funn (lag) | Dom | Begrunnelse | Rute |
| --- | --- | --- | --- | --- |
| 1 | Bildene i «Skjermbilder» finnes ikke ennå (blind, edge ×2, verification) | medium | `my-project/skjermbilder/` finnes ikke. Det er den åpne oppgaven til Kristine i Tasks | Blokkerer PR-en til bildene er lagt til |
| 2 | Alternativtekstene beskriver bilder som ikke er tatt (blind) | low | Overskriftene stemmer med `tekster.py`, men detaljene må sjekkes mot bildene | Sjekkes når bildene er tatt (samme oppgave) |
| 3 | «Nettsiden er ferdig» er for tidlig, fordi 8.2 står igjen (blind, edge) | false | 8.2 er testplanen og prøven fra en ny kopi, ikke nye funksjoner, og README leses etter 8.2 | Avvist |
| 4 | CSRF-punktet sier mer enn Lax gir: andre porter på localhost er samme nettsted, og en lenke (GET) til `/last-ned/<format>` setter `lastet_ned` (blind, edge ×2) | medium | Bekreftet: `ruter.py:369` er en GET-rute som kaller `sett_lastet_ned` (linje 394) | patch (README-teksten) + defer (ruten) |
| 5 | Testen heter `nfr8`, men NFR-8 handler om README (blind) | low | Sporingen fra krav til test blir feil. Innloggingen er FR-3 | patch (nytt navn) |
| 6 | Testen sjekker bare `/logg-inn`, ikke `/registrer` (blind) | false | `SESSION_COOKIE_SAMESITE` gjelder for hele appen. Flask setter det samme flagget på alle øktcookies | Avvist |
| 7 | Det som gjenstår, er gjemt i et gammelt punkt i `issues.md`/`todo.md` (blind) | low | Sesjonsloggen legger skjermbildene inn som eget nytt punkt nederst | Avvist (tas i sesjonsloggen) |
| 8 | `testkjoringer/` har også `brev-hilsen/`, og treet mangler `pyproject.toml`/`uv.lock` (blind) | low | Bekreftet med `ls` | patch |
| 9 | Spec-kopi, sprint-status `done`, notater og prompt-logg mangler (blind) | false | Det gjøres etter gjennomgangen og nettleserprøven, slik som i hver story | Avvist |
| 10 | AC om lærerens CI-sjekk er ikke vist (blind) | false | Begge filene finnes (sjekket), og CI kjører på PR-en | Avvist |
| 11 | «Skjermbilder» står foran «Installasjon» (blind) | false | Kristines beslutning 3 | Avvist |

## Verification

**Commands:**
- `cd backend && uv run pytest` -- expected: alle tester grønne
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Alle relative lenker i README peker på filer som finnes (sjekkes med et lite skript over `](...)`-lenkene)
- Bildene vises i README på GitHub i PR-en
