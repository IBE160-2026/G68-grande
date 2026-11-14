---
title: 'Rettinger fra retrospektiven for epic 4, runde 2: tester mot Claude og sperre mot nettverk'
type: 'chore'
created: '2026-11-14'
status: 'done'
baseline_commit: 'ea9929a92e3a60f978a54a109dda04c3a9bcf0a6'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-retro-2026-11-14.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Retrospektiven for epic 4 (action item 2, godtatt av Kristine 2026-11-14) fant tre hull:
- Ingen test sender kallet gjennom det ekte Anthropic-SDK-et. `FalskKlient` godtar alle argumenter, så et feil parameternavn etter en ny versjon av SDK-et synes først ved et ekte kall (A2).
- Ingen felles sperre mot nettverk i testene. At ingen test går mot nettet, hviler på at hver fikstur bytter ut `EkteKI` (B4).
- Ingen webtest går gjennom `EkteKI` og `kontroller` sammen (B5).

**Approach:** Én felles hjelper for testene: en ekte `Anthropic`-klient med `httpx2.MockTransport`, som svarer ut fra skjemaet i forespørselen. Den brukes i en adaptertest og i en webtest. En autouse-sperre i `tests/conftest.py` stopper alle ekte HTTP-kall og får testen til å feile. De fire punktene fra 4.1 i `deferred-work.md` lukkes, og `retry-after` uten tak blir en kjent begrensning i README.

**Decision (Kristine, 2026-11-14):** Rettingene etter retro 4 tas i tre runder med én branch og PR hver. Dette er runde 2. Runde 3 (småtingene) og runde 4 (målingen) står i `deferred-work.md`.

## Boundaries & Constraints

**Always:**
- Ingen endring i koden under `backend/soknad/`. Bare tester, `README.md`, `deferred-work.md` og `issues.md`.
- Alle eksisterende tester går gjennom uendret.
- Hver testfil og testfunksjon nevner FR- eller NFR-nummeret. Ingen testfil henter noe fra en annen testfil (en hjelpefil som ikke er en testfil, er greit).
- Ingen test går mot nettet, og ingen test bruker en ekte API-nøkkel.

**Never:**
- Ikke ta med punktene fra runde 3 og 4: `med_nokkel`, kommentarene om «4.3», `test_nfr11_nettsiden_bruker_fortsatt_testki`, surrogatene, README-radene, øktlageret og målingen.
- Ikke rette `retry-after` i koden (ingen tak, ingen `max_retries=0`). Den blir bare en kjent begrensning.
- Ikke endre `prompt-logg.md`, `todo.md` eller andre filer i `my-project/` før koden er gjennomgått.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Kall gjennom SDK-et | `EkteKI` med ekte `Anthropic` og `MockTransport`, kall `nokkelord`, `gap` og `brev` | JSON-en som sendes, har `model`, `max_tokens`, `system`, `messages` og `output_config` med `format` og `effort`, og svaret er det kontrollerte svaret | – |
| Webflyten med ekte SDK | testmodus av, samtykke, «Sjekk CV-en min» og «Lag søknadsbrevet mitt» | resultatsiden og brevsiden viser svarene fra den falske transporten, gjennom `kontroller` | – |
| Test som når nettet | en test bruker `EkteKI` uten falsk klient | testen feiler med en melding om at den prøvde å nå nettet | sperren kaster, og pytest feiler ved avslutning selv om `EkteKI` gjør feilen om til `KIFeil` |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/ki.py:185–256` -- `EkteKI(api_nokkel, modell, klient=None)` og `_kall`. Uendret.
- `backend/soknad/kjerne/ki_svar.py:11` -- `FELT` gir oppgaven ut fra `schema["properties"]` i forespørselen.
- `backend/tests/conftest.py:12–19` -- `ingen_ekte_env` (`delenv`). Sperren blir en ny autouse-fikstur her.
- `backend/tests/adaptere/test_ekte_ki.py` -- `FalskKlient` og testene er uendret. Testen på linje 174 patcher `httpx2.Client.send` og skal virke som før.
- `backend/tests/web/hjelpere.py:155` -- `app_med_nokkel()`, og `test_samtykke.py:205` -- `gjennom_flyten` er mønsteret for webtesten.
- Prøvd i planleggingen (anthropic 2.4.0, httpx2 2.16.0): `Anthropic(api_key=…, max_retries=0, http_client=httpx2.Client(transport=httpx2.MockTransport(handler)))` virker med `EkteKI`. En patch av `httpx2.HTTPTransport.handle_request` stopper den ekte klienten, men `EkteKI` gjør feilen om til `KIFeil(nettverk)`. Derfor noterer sperren forsøket og feiler testen ved avslutning.
- `deferred-work.md:56–67` (de fire punktene fra 4.1), `issues.md:107`, `README.md:94–105`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/falsk_api.py` (ny hjelpefil, ikke testfil) -- `klient_med_svar(svar, sendt)`: ekte `Anthropic` med `MockTransport` og `max_retries=0`. Den svarer med `svar[oppgave]` som JSON-tekst (oppgaven ut fra skjemaet), `stop_reason` `end_turn`, og legger hver forespørsel (JSON og headere) i `sendt`.
- [x] `backend/tests/conftest.py` -- autouse-sperre: `httpx2.HTTPTransport.handle_request` noterer forsøket og kaster `httpx2.ConnectError`. Etter testen feiler `pytest.fail` hvis noe er notert. `ANTHROPIC_AUTH_TOKEN` og `ANTHROPIC_BASE_URL` i `delenv`.
- [x] `backend/tests/adaptere/test_ki_gjennom_sdk.py` (ny) -- for hver oppgave: kallet går gjennom SDK-et, og JSON-en og `x-api-key` er riktige, og svaret er kontrollert. Test av sperren: `EkteKI` uten falsk klient gir `KIFeil(nettverk)`, og forsøket er notert (testen tømmer lista).
- [x] `backend/tests/web/test_ekte_ki_i_flyten.py` (ny) -- hele flyten med nøkkel, testmodus av og samtykke, med `EkteKI` og den falske klienten: resultatsiden viser nøkkelordene og gap-svaret, brevsiden viser avsnittene, og tre forespørsler er sendt (nokkelord, gap, brev).
- [x] `README.md` -- nytt punkt i «Kjente begrensninger»: «**Et svar fra Claude om å vente kan gjøre at det tar lenge:** ber API-et om å vente før neste forsøk (`retry-after`), venter nettsiden så lenge før det ene nye forsøket. Da kan «Sjekk CV-en min» ta mye lengre tid enn vanlig.»
- [x] `deferred-work.md` og `issues.md` -- de fire punktene fra 4.1 får en linje `resolved:` (SDK-testen: denne runden; `retry-after`: README; ordrett: kjent begrensning, se `testplan.md`; tomme punkter: `_uten_tomme` i 4.2). `issues.md:107` krysses av med «(løst …)».

**Acceptance Criteria:**
- Given en midlertidig `ki.py` med `output_confg` i stedet for `output_config` (kopi først, satt tilbake og sjekket med `cmp`), when testene kjøres, then feiler minst én ny test, og testene med `FalskKlient` går gjennom.
- Given en midlertidig `test_testmodus.py`-test som kaller `EkteKI` uten falsk klient, when den kjøres, then feiler den med meldingen fra sperren.
- Given alle testene, when de kjøres, then er de grønne, og antallet er 793 pluss de nye.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

## Implementation Notes

- anthropic 2.4.0 sender nøkkelen i `authorization: Bearer …`, ikke i `x-api-key` (`_api_key_auth` i `anthropic/_client.py`). Testen godtar derfor nøkkelen i en av de to headerne. Målet er å se at nøkkelen sendes, og et nytt navn på headeren gjør ikke kallet feil.
- AC 1 (`output_confg`): alle de fem nye testene feilet, de fire SDK-testene med `TypeError: Messages.create() got an unexpected keyword argument` fra SDK-et. Men fem av testene med `FalskKlient` feilet også, fordi de leser `kall["output_config"]` direkte (`KeyError`). Testene med `FalskKlient` som bare ser på svaret (for eksempel `test_nfr11_gap_gir_svaret_fra_claude`), gikk gjennom. `ki.py` er satt tilbake og sjekket med `cmp`.
- AC 2: en midlertidig test i `test_testmodus.py` ga «Failed: Testen prøvde å nå nettet: POST https://api.anthropic.com/v1/messages, …» ved avslutning (to forsøk, fordi `max_retries=1`). Fila er satt tilbake og sjekket med `cmp`.
- AC 3: 798 tester grønne (793 + 5 nye). `ruff check` og `ruff format --check` uten feil.
- Den nye linja `resolved:` står også på punktet for runde 2 nederst i `deferred-work.md`.
- Ekstra mutasjon (hovedøkta): et parameter SDK-et ikke kjenner (`ekstra_valg=True` i `messages.create`) fikk alle de 5 nye testene til å feile, mens alle 63 testene i `test_ekte_ki.py` gikk gjennom. Det er dette AC 1 skulle vise. `ki.py` er satt tilbake og sjekket med `cmp`.
- Kommentaren om headeren i `falsk_api.py` er rettet (authorization, ikke x-api-key).

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-14), tre lag: blind, kanttilfeller og testhull.

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | blind | Punktet i `issues.md:107` lukkes uten at store `retry-after`-verdier er målt eller rettet | low | Intent sier at `retry-after` bare blir kjent begrensning, og Never forbyr retting i koden. Tidene ble målt i 4.3.1, 4.4 og 4.5. Avvist. |
| 2 | blind, kant | README-linja sier bare «Sjekk CV-en min» og «mye lengre tid», men ventetiden har ingen øvre grense (tidsgrensen gjelder ikke ventingen) og gjelder alle KI-kall | low | Sant (`_calculate_retry_timeout` i anthropic 2.4.0, bekreftet av testhull-laget). Direkte retting av teksten. Patch, og Kristine sjekker den nye ordlyden. |
| 3 | blind | Ingen feilvei (tidsavbrudd, 400/500, `max_tokens`) testes gjennom det ekte SDK-et | low | Feiltypene er testet med SDK-ets egne unntaksklasser i `test_ekte_ki.py`. Intent (A2) gjaldt parameternavn i kallet. Nye tester er mer enn en direkte retting. Avvist. |
| 4 | blind, kant | En feil i `falsk_api.py` (KeyError, StopIteration) vises som `KIFeil(nettverk)` | low | Feilen er lenket: SDK-et gjør `raise APIConnectionError(...) from err` (`_base_client.py:1453`) og `EkteKI` gjør `raise ... from feil`, så pytest viser den opprinnelige feilen i traceback. Bare for utvikleren. Avvist. |
| 5 | blind | SDK-testen sjekker ikke at `EkteKI` gir videre sin egen `api_nokkel` | false | Dekket av `test_ekte_ki.py:186` (`ki.klient.api_key == "x"`), som testhull-laget også fant. |
| 6 | blind, kant | Webtesten beviser ikke nøkkelordene («Python» står i CV-en, «Fiktivverktøy» inne i gap-tekstene) og sjekker ikke at tomme punkter fjernes | low | Sant. Direkte retting. Patch: egne nøkkelord som ikke står andre steder, og ingen tom `<li>`. |
| 7 | blind | Hjelperen som finner oppgaven, er skrevet to ganger med ulik logikk | low | Sant (`falsk_api._oppgave` og `test_ekte_ki_i_flyten._oppgaven`). Direkte retting. Patch: én hjelper i `falsk_api.py`. |
| 8 | blind, kant | Docstringen til `nettsperre` lover at ingen test når nettet, men bare synkron httpx2 er stoppet | low | Sant for ordlyden. Nettsiden bruker bare den synkrone klienten. Patch: docstringen sier nøyaktig hva som stoppes. |
| 9 | blind, kant | Testen av sperren venter ca. 0,5 s før det nye forsøket | low | Sant, men 0,5 s av ca. 70 s, og ventingen viser at det nye forsøket også stoppes. Avvist. |
| 10 | kant | `ANTHROPIC_CUSTOM_HEADERS` i miljøet fjernes ikke, så headerne kan bli ulike på ulike PC-er | low | Sant (`anthropic/_client.py:252` leser den). Direkte retting. Patch: med i `delenv`. |
| 11 | testhull | Steget i `nettsperre` som feiler testen etterpå, har ingen egen test | low | Sant, men å teste det krever `pytester`, som repoet ikke bruker. Det er prøvd for hånd (AC 2), og selve sperren stopper nettet uansett. Avvist. |
