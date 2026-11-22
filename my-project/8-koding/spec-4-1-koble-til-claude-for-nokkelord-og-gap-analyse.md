---
title: 'Story 4.1: Koble til Claude for nøkkelord og gap-analyse'
type: 'feature'
created: '2026-11-12'
status: 'done'
baseline_commit: '11a6eaacbc48f3d29b85914a5ea3b6fd005a8a88'
route: 'dispatch'
review_loop_iteration: 1
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nettsiden har bare `TestKI`, som gir ferdige svar for testdataene. Det finnes ingen kode som sender studentens egen CV og annonse til Claude (AD-3, AD-13, NFR-11).

**Approach:** `EkteKI` i `adaptere/ki.py` får `nokkelord(annonse)` og `gap(cv, annonse)` med de samme signaturene og svarformene som `TestKI`. Hver oppgave har sin prompt i `backend/prompts/` og sitt JSON-skjema, sendt med `output_config.format`. Svaret går gjennom den samme `kontroller()`. API-feil blir `KIFeil`, og hvert kall logger oppgave, tokens og anslått pris. Nettsiden kobles ikke til `EkteKI` ennå (story 4.3).

## Boundaries & Constraints

**Always:** `anthropic==2.4.0` importeres bare i `adaptere/ki.py`, aldri i `kjerne/`. Klienten er `Anthropic(timeout=90, max_retries=1)` med begge verdiene satt uttrykkelig fra `innstillinger.py`. Modellen er `ANTHROPIC_MODEL` eller `claude-opus-5-5`. Skjemaene har `additionalProperties: false` og alle felt påkrevd (`arbeidsgiver` er tekst eller `null`). Prompt-filene åpnes med `encoding="utf-8"`. Loggen viser aldri CV, annonse, nøkkel eller selve KI-svaret. Testene bruker en falsk klient og kaller aldri det ekte API-et. Hver testfil og testfunksjon nevner FR-nummeret.

**Never:** Ingen endring i `web/` eller i hvilken KI nettsiden bruker (`ki()` i `web/flyt.py` er 4.3). Ikke `brev` i `EkteKI` (4.2), ikke rensing av brevtekst i `kontroller` (4.2), ikke `scripts/lag_testsvar.py` (4.4). Ingen strømming, ingen `temperature`, ingen `thinking`-parameter.

**Beslutning (Kristine, 2026-11-12):** ingen reservemodell («fallbacks») når Claude avviser et kall. `stop_reason: refusal` gir `KIFeil(ubrukelig_svar)` og «Prøv på nytt», som andre ubrukelige svar. Kallet går gjennom vanlige `client.messages.create`, uten betaflagg.
**Beslutning (Kristine, 2026-11-12):** spec-en beholdes samlet (ca. 2500 tokens), fordi klienten, promptene, feilene og loggingen testes med den samme falske klienten.
**Beslutning (Kristine, 2026-11-13):** FR-15 i PRD-en (endret 12. november) tas med i 4.1. Nøkkelordprompten ber om 8–20 nøkkelord på 1–3 ord hver, uten duplikater. Er listen tom eller lengre enn 30 nøkkelord, gir `kontroller("nokkelord")` `KIFeil(ubrukelig_svar)`. Det gjelder også `TestKI`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Nøkkelord | annonse, svar med gyldig JSON og `end_turn` | `{nokkelord: [...], arbeidsgiver: "..." eller None}` | – |
| Gap | CV og annonse, gyldig svar | `{dekker: [...], mangler: [...]}` | – |
| Nettverksfeil | klienten kaster `APIConnectionError` | – | `KIFeil(nettverk)` |
| Tidsavbrudd | klienten kaster `APITimeoutError` (også etter det ene nye forsøket) | – | `KIFeil(annet)`, ikke `nettverk` |
| Annen API-feil | `APIStatusError` (for eksempel 401, 429, 500) | – | `KIFeil(annet)` |
| Avkuttet eller avvist svar | `stop_reason` er `max_tokens`, `refusal` eller annet enn `end_turn` | – | `KIFeil(ubrukelig_svar)` |
| Ugyldig svar | ugyldig JSON, feil form, tom liste, ingen tekstblokk | – | `KIFeil(ubrukelig_svar)` |
| For mange nøkkelord (FR-15) | `nokkelord` med 31 eller flere nøkkelord | – | `KIFeil(ubrukelig_svar)` |
| Akkurat 30 nøkkelord (FR-15) | `nokkelord` med 30 nøkkelord | svaret godtas | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/ki.py` -- `KI`-protokollen, `TestKI` og `les_testcaser`. `EkteKI` legges til her. `TestKI` endres ikke.
- `backend/soknad/kjerne/ki_svar.py` -- `kontroller(oppgave, tekst)` med `FELT`. Den får en valgfri `stop_reason` (standard `"end_turn"`), så TestKI-kallene er uendret.
- `backend/soknad/kjerne/feil.py` -- `KIFeil` og `KIFeilType` (`NETTVERK`, `ANNET`, `UBRUKELIG_SVAR`). Brukes som de er.
- `backend/soknad/innstillinger.py` -- `STANDARD_MODELL` finnes. Nye konstanter for KI-kallet legges her.
- `backend/soknad/__init__.py` -- `create_app` leser `ANTHROPIC_API_KEY` og `ANTHROPIC_MODEL` til `app.config`. Her settes loggeren `soknad` til INFO med utskrift til terminalen.
- `backend/tests/adaptere/test_ki.py` -- mønsteret for KI-tester. Ingen testfil henter fra en annen testfil (retro-punkt 20).
- `backend/testdata/case-1-utvikler/fasit.md` og `ki-svar/*.json` -- viser hvilke nøkkelord og krav promptene skal gi: korte ord som står ordrett i annonsen (telleregelen FR-17 teller delstrenger), og kravene formulert som i annonsen.
- `backend/pyproject.toml`, `backend/uv.lock` -- `anthropic==2.4.0` legges til med `uv add`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/pyproject.toml`, `backend/uv.lock` -- `uv add anthropic==2.4.0` -- SDK-et fra stacken.
- [x] `backend/soknad/innstillinger.py` -- legg til `KI_TIDSGRENSE = 90`, `KI_NYE_FORSOK = 1`, `KI_MAKS_TOKENS = 16000`, `KI_INNSATS = "medium"`, pris per million tokens inn/ut i dollar (4 og 20 for `claude-opus-5-5`) og en omtrentlig kronekurs -- grensene på ett sted.
- [x] `backend/prompts/nokkelord.md`, `backend/prompts/gap.md` -- norske prompter. Nøkkelord: korte ord eller uttrykk fra annonsen (ferdigheter, verktøy, krav), skrevet slik de står i annonsen, og arbeidsgiverens navn eller `null`. Gap: hvert krav i annonsen i enten `dekker` eller `mangler`, bare ut fra det som står i CV-en -- NFR-10.
- [x] `backend/soknad/kjerne/ki_svar.py` -- `kontroller(oppgave, tekst, stop_reason="end_turn")`: annet enn `end_turn` gir `KIFeil(ubrukelig_svar)` før JSON leses -- AD-4.
- [x] `backend/soknad/adaptere/ki.py` -- `EkteKI(api_nokkel, modell, klient=None)`. `klient` gjør det mulig å bruke en falsk klient i testene. Ellers lages `Anthropic(api_key=..., timeout=KI_TIDSGRENSE, max_retries=KI_NYE_FORSOK)`. Én privat metode sender prompten som `system`, teksten i `<annonse>`/`<cv>`-merker som brukermelding, skjemaet i `output_config` sammen med `effort`, setter sammen tekstblokkene, logger og kaller `kontroller`. Feilene fanges i rekkefølgen `APITimeoutError` → `APIConnectionError` → `APIError` -- AD-3, AD-4, AD-13.
- [x] `backend/soknad/__init__.py` -- loggeren `soknad` får nivå INFO og én `StreamHandler` (ikke en ny for hver `create_app`) -- AD-12.
- [x] `backend/tests/adaptere/test_ekte_ki.py` -- tester med falsk klient for alle radene i matrisen, riktig skjema og modell i kallet, at CV og annonse er med i brukermeldingen, klientens `timeout` og `max_retries`, og loggen (oppgave og tokens med, CV-, annonse- og nøkkeltekst ikke med) -- NFR-9, FR-28.
- [x] `backend/soknad/innstillinger.py`, `backend/soknad/kjerne/ki_svar.py` -- `MAKS_NOKKELORD = 30` i innstillingene. `kontroller("nokkelord")` gir `KIFeil(ubrukelig_svar)` når listen har flere enn `MAKS_NOKKELORD` elementer, i tillegg til regelen for tom liste. Docstringen nevner regelen -- FR-15, FR-28.
- [x] `backend/prompts/nokkelord.md` -- regelen om nøkkelordene ber om 8–20 nøkkelord på 1–3 ord hver, uten duplikater (erstatter «helst ett eller to ord» og «bare én gang», resten beholdes) -- FR-15.
- [x] `backend/tests/kjerne/test_ki_svar.py` -- test at 30 nøkkelord godtas og 31 gir `ubrukelig_svar`, og at grensen er `MAKS_NOKKELORD` -- FR-15, NFR-9.
- [x] `backend/tests/adaptere/test_ekte_ki.py` -- test at et svar fra Claude med 31 nøkkelord gir `KIFeil(ubrukelig_svar)`, og at prompten nevner 8–20 nøkkelord -- FR-15.

**Acceptance Criteria:**
- Gitt `EkteKI` og en falsk klient, når `nokkelord` og `gap` kalles, så har kallet `model`, `system` fra prompt-fila, `max_tokens`, og `output_config` med `format: {type: "json_schema", schema: ...}` og `effort`.
- Gitt `EkteKI(api_nokkel="x", modell=...)` uten falsk klient, så er klientens `timeout` 90 og `max_retries` 1, og ingen nettverkskall gjøres.
- Gitt et vellykket kall, så logger `soknad.adaptere.ki` én INFO-linje med oppgaven, tokens inn og ut og anslått pris. Gitt en `KIFeil`, så logges oppgaven og feiltypen, uten feilmeldingen fra API-et.
- Gitt hele testsuiten, når `uv run pytest` kjøres uten `ANTHROPIC_API_KEY`, så går alt gjennom uten nettverk, og `TestKI` er fortsatt KI-en nettsiden bruker.

## Design Notes

Claude Opus 5.5 tenker alltid. `thinking: disabled` gir 400, så parameteren sendes ikke, og `effort` styrer hvor mye den tenker. Standarden er `medium`, men den settes uttrykkelig så den kan justeres etter målingen i 4.3. Svaret kan ha tomme `thinking`-blokker før tekstblokken, så bare blokker med `type == "text"` settes sammen. I anthropic 2.x (`httpx2`) er `APITimeoutError` en underklasse av `APIConnectionError`, så tidsavbrudd må fanges først. Feilene i testene lages med `httpx2.Request`/`httpx2.Response`.

```python
# Loggen, eksempel
"KI-kall nokkelord: 812 tokens inn, 143 ut, anslått 0,0061 dollar (ca. 0,07 kr)"
```

Sjekk mot claude-api-skillen (AD-15): parameteren heter `output_config.format` med `type: "json_schema"`, og `stop_reason` kan være `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn` og `refusal`. Det stemmer med AD-4, så arkitekturen trenger ingen endring.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne, også de gamle

## Implementation Notes

- En hjelpeagent kodet ut fra spec-en. Den stoppet på grunn av bruksgrensen rett før den skrev disse notatene, men koden og testene var ferdige. Hovedøkta sjekket endringene, kjørte ruff og pytest (607 tester grønne, 78 i `test_ekte_ki.py` og `test_ki_svar.py`) og skrev notatene.
- `kontroller` fikk `stop_reason: str | None = "end_turn"`. `None` gir også `ubrukelig_svar`.
- `EkteKI` leser promptene én gang når den lages. Et ubrukelig svar logger både tokens og pris (kallet har kostet penger) og feiltypen.
- Loggeren `soknad` får én felles `StreamHandler` (`TERMINAL_LOGG` i `soknad/__init__.py`), så linjene ikke dobles når `create_app` kalles flere ganger.
- Testene lager svarene med `anthropic.types.Message.model_validate` og feilene med `httpx2.Request`/`httpx2.Response`. Testen for klienten stopper `httpx2.Client.send`, så ingen nettverkskall kan skje.
- Arkitekturen trengte ingen endring (AD-15): `output_config.format` og verdiene for `stop_reason` stemmer med AD-4.

## Spec Change Log

- **2026-11-13, runde 1 (intent_gap):** Etter gjennomgangen, under oppdateringen av TO DO, ble det funnet at FR-15 i PRD-en ble endret 12. november (8–20 nøkkelord på 1–3 ord, tom liste eller over 30 er ubrukelig). Epics-fila og konteksten for epic 4 var ikke oppdatert, så spec-en manglet regelen. Kristine valgte å ta den med i 4.1. Endret: beslutning og to rader i matrisen (inne i den frosne delen, godkjent av Kristine), og fire nye oppgaver. Unngår: at en nøkkelordliste på over 30 slipper gjennom, og at prompten ber om noe annet enn PRD-en. **KEEP:** all koden i commit `b6d7974` (EkteKI, feilene, loggingen, promptene og testene) er gjennomgått og godkjent og skal ikke skrives om. Endringen legges oppå.

## Review Triage Log

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | blind, kant | Andre `AnthropicError` enn `APIError` (for eksempel `RetryableError`, `CredentialsError`) slipper ut av `_kall` uten å bli `KIFeil` | low | `_exceptions.py` i 2.4.0 har dem som søsken av `APIError`. Patch: siste `except` blir `AnthropicError`, med test. |
| 2 | blind, kant | Kommentarene lover at et kall aldri tar mer enn 90 s / 2 x 90 s | low | Tidsgrensen gjelder per fase, og SDK-et venter backoff (opptil 8 s) eller `retry-after` mellom forsøkene. Patch: kommentarene rettes. |
| 3 | blind | Nøkkelordprompten utelukker ikke arbeidsgiverens navn og stillingstittelen | low | Ville gitt treff som ikke er ferdigheter. Patch: én linje i prompten. |
| 4 | blind | Logglinjen sier ikke hvilken modell som kjørte, så prisen kan være feil uten at det synes | low | Prisen regnes alltid med Opus-prisene. Patch: modellen med i linjen. |
| 5 | verifisering, blind | Ingen test sender kallet gjennom det ekte SDK-et, så et feil parameternavn ville bare synes ved første ekte kall | medium | Riktig i dag (`OutputConfigParam` har `format` og `effort` i 2.4.0), men ikke vernet mot endringer. Defer til 4.3 (test med `httpx2.MockTransport`, eller ett ekte kall). |
| 6 | kant | En 429/529 med stor `retry-after` får SDK-et til å vente så lenge før det nye forsøket | maybe-false | `_calculate_retry_timeout` følger `retry-after` uten tak. Uvisst hvor store verdier API-et sender. Defer til 4.3, måles der. |
| 7 | blind | Nøkkelord som ikke står ordrett i annonsen, sjekkes ikke, og like nøkkelord fjernes ikke | maybe-false | Like nøkkelord er false: `telleregel` teller hvert vaskede nøkkelord én gang. Om Claude omformulerer nøkkelord, avgjøres når promptene kjøres mot fasiten i 4.4. Defer. |
| 8 | blind, kant | `</annonse>` eller `</cv>` i teksten kan bryte ut av merkene | low | Teksten er brukerens egen, så hun kan bare skade sin egen analyse. Retting krever ny vask. Avvist. |
| 9 | blind, kant | En manglende prompt-fil gir `FileNotFoundError` når `EkteKI` lages | false | Filene ligger i Git. En tydelig feil ved oppstart er riktig oppførsel. |
| 10 | blind, kant | `propagate` er på, så linjene dobles hvis rotloggeren får en handler (`ANTHROPIC_LOG`) | low | Skjer bare med `ANTHROPIC_LOG` satt. `propagate = False` ville stoppe `caplog` i testene. Avvist. |
| 11 | blind, kant | `StreamHandler` binder `sys.stderr` når modulen importeres | low | Under `flask run` byttes ikke stderr. 607 tester uten loggfeil. Retting krever egen klasse. Avvist. |
| 12 | blind, kant | Testene importerer `httpx2`, som bare kommer via `anthropic` | low | `uv.lock` låser versjonen, så et bytte er alltid med vilje. Avvist. |
| 13 | blind | Gap-svaret kan ha samme krav i begge listene | low | Prompten krever nøyaktig én liste. En sjekk ville gitt ny regel i `kontroller`. Avvist. |
| 14 | blind | Standardverdien `stop_reason="end_turn"` lar en ny kaller hoppe over sjekken | false | Alle kall i `EkteKI` går gjennom `_kall`, som alltid sender `stop_reason`. Bare `TestKI` bruker standarden. |
| 15 | blind | Mangler test for logging av `refusal`, for ren `APIError` og for manglende prompt | low | Samme kodevei som testene for ugyldig svar. Ren `AnthropicError` får test i patch 1. Avvist. |
| 16 | blind | `ingen_ekte_env` tømmer ikke `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` | false | Testen sjekker bare `timeout`, `max_retries` og `api_key`, som ikke påvirkes av disse. |

**Runde 2 (etter FR-15-tillegget):**

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 17 | blind | Loggen sier ikke hvorfor et svar var ubrukelig (`max_tokens` eller `refusal`) | low | `stop_reason` er ikke sensitiv og trengs når `KI_MAKS_TOKENS` og `effort` justeres i 4.3. Patch: `stopp <stop_reason>` i INFO-linjen. |
| 18 | blind, kant | `</annonse>`/`</cv>` i teksten bryter ut av merkene | low | carried: som #8, avvist. |
| 19 | kant | Manglende prompt-fil gir rå feil når `EkteKI` lages | false | carried: som #9. |
| 20 | blind, kant | `propagate` på gir doble linjer med en rot-handler | low | carried: som #10, avvist. |
| 21 | verifisering, kant | `httpx2` importeres i testene uten å stå i `pyproject.toml` | low | carried: som #12, avvist. |
| 22 | blind, kant | Samme krav i både `dekker` og `mangler`, og ingen øvre grense for gap-listene | low | carried: som #13, avvist. Grensen for gap-listene står ikke i PRD-en. |
| 23 | blind | `stop_reason` har standardverdi i `kontroller` | false | carried: som #14. |
| 24 | blind, kant | Nøkkelord og arbeidsgiver som ikke står i annonsen, sjekkes ikke | maybe-false | carried: som #7, utsatt til 4.4. |
| 25 | blind, kant | Like nøkkelord («Python», «python») gir høyere Y i «X av Y» | false | `telleregel._vask` gjør `strip().casefold()`, og hvert vaskede nøkkelord telles én gang. |
| 26 | blind, kant | Tomme punkter (`"  "`) blant ekte punkter slipper gjennom i `nokkelord`, `dekker` og `mangler` | low | Fantes før 4.1 (også `TestKI`), og står alt i konteksten for epic 4 som en del av 4.2. Defer. |
| 27 | kant | Tom `arbeidsgiver` (`""`) blir ikke `None` | low | Retro-punkt 14 legger dette i 4.2. Defer. |
| 28 | kant | `EkteKI` har ikke `brev`, så et bytte før 4.2 gir `AttributeError` | false | Nettsiden bruker ikke `EkteKI` før 4.3, som kommer etter 4.2. |
| 29 | kant | `api_nokkel=None` gir `TypeError` ved kallet | low | `ANTHROPIC_API_KEY` er `""` som standard, og 4.3 velger `EkteKI` bare når nøkkelen finnes. Avvist. |
| 30 | blind, kant | `sett_opp_logg` setter INFO hver gang og skjuler `app.logger.debug` | low | Ingen kode bruker `app.logger`. Avvist. |
| 31 | blind | Prisen er misvisende når en annen modell brukes | low | Modellen står nå i linjen (#4), og kommentaren i `innstillinger.py` sier det. Avvist. |
| 32 | blind | Loggtesten har faste tall | low | Tallene låser regnestykket med vilje (testhull-laget bekreftet det). Avvist. |
| 33 | blind | Grunnen til at tidsavbrudd gir `annet` står ikke i koden | low | Grunnen står i epics (story 4.1) og EXPERIENCE (State Patterns). Avvist. |
