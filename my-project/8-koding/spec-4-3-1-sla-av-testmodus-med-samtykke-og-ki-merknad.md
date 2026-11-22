---
title: 'Story 4.3.1: Slå av testmodus, med samtykke og KI-merknad'
type: 'feature'
created: '2026-11-13'
status: 'done'
baseline_commit: 'ce95faef622a39356836f4d2e159fc3c72c78ced'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Bryteren «Testmodus» er låst på også med API-nøkkel, `ki()` gir alltid `TestKI`, og nettsiden har verken samtykke eller KI-merknad. Ekte KI (4.1, 4.2) kan derfor ikke brukes fra nettsiden.

**Approach:** Med nøkkel kan bryteren slås av og på på startsiden (et skjema som sender POST, og siden lastes på nytt). Med testmodus av velger `ki()` `EkteKI`, startsiden krever samtykke før «Begynn å lage søknad», og KI-merknaden står i hjørneraden. Grensene (15 000 tegn, 10 KI-kall) er story 4.3.2.

## Boundaries & Constraints

**Always:** Bryteren endres bare når søknaden er på steg start og ikke opptatt. Ellers sendes brukeren til siden for steget, og ingenting endres (FR-32, AD-8). Uten nøkkel (eller bare mellomrom) er bryteren låst på som før, og en POST endrer ingenting. Ved innlogging og registrering er testmodus av med nøkkel og på uten. Tekst sendes til Claude bare når `Soknad.samtykke` er sann (AD-12). Alle brukertekster i `web/tekster.py`, ordrett fra EXPERIENCE. Skjemaene virker uten JavaScript. Testene kaller aldri det ekte API-et.

**Never:** Ingen endring i `adaptere/ki.py` utenom det `ki()` trenger, i promptene eller i `kjerne/ki_svar.py`. Ikke grensene fra NFR-11 (4.3.2). Ikke `scripts/lag_testsvar.py` (4.4). Ikke `style=` eller faste høyder i malene.

**Beslutning (Kristine, 2026-11-13):** story 4.3 deles. 4.3.1 er bryteren, samtykket og KI-merknaden. 4.3.2 er grensene.
**Beslutning (Kristine, 2026-11-13):** spec-en beholdes samlet (ca. 2500 tokens), fordi bryteren, samtykket og KI-merknaden henger tett sammen. Bryteren laster siden på nytt (ikke JavaScript som i skissen), og fokus blir på bryteren.
**Beslutning (Kristine, 2026-11-14, etter prøven med ekte KI, endret samme dag):** rett etter overskriften, før avsnittene om kravene og erfaringen, kommer ett avsnitt som presenterer studenten som person, så arbeidsgiveren først får vite hvem studenten er. Claude ser etter alder, «Om meg», hobbyer, interesser og frivillig arbeid i hele CV-en og bygger bare på det som står der. Uten noe slikt i CV-en begynner brevet rett på stillingen og kravene. Regelen står i `prompts/brev.md`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Slå av | nøkkel, steg start, POST bryteren | `Innlogging.testmodus` blir usann, startsiden vises med samtykket, fokus på bryteren | – |
| Slå på igjen | testmodus av, POST bryteren | testmodus på, samtykket skjult, avkrysningsboksen tom neste gang | – |
| Uten nøkkel | POST bryteren | testmodus fortsatt på | ingen endring |
| Etter startsiden | steg modus eller senere, eller opptatt | redirect til siden for steget | testmodus uendret |
| Begynn uten samtykke | testmodus av, boksen ikke krysset av | startsiden på nytt: rød ramme, «Du må samtykke før du kan begynne» koblet til boksen, fokus på boksen, steget fortsatt start | – |
| Begynn med samtykke | testmodus av, boksen krysset av | `samtykke=True`, til modusvalget | – |
| Begynn i testmodus | testmodus på, ingen boks | til modusvalget uten samtykke | – |
| KI-kall uten samtykke | testmodus av, `samtykke=False` på innlegging eller resultat, POST | ingen KI-kall, redirect til startsiden | – |
| Ny innlogging | nøkkel finnes | testmodus av | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/__init__.py` -- `create_app` lager `app.extensions["ekte_ki"] = EkteKI(nøkkel, modell)` når nøkkelen finnes (ikke bare mellomrom), ellers `None`. `EkteKI.__init__` kobler ikke til nettet.
- `backend/soknad/web/flyt.py` -- `ki()` får returtypen `KI` (Protocol fra `adaptere/ki.py`) og velger `test_ki` eller `ekte_ki` ut fra `gjeldende_innlogging().testmodus`. Her legges også `har_nokkel()` (flyttet fra `start()`) og en sjekk av samtykket.
- `backend/soknad/web/innlogging.py` -- `logg_inn_bruker` setter i dag `testmodus=True` fast.
- `backend/soknad/adaptere/oktlager.py` -- `Oktlager` har `ny`, `hent`, `slett` og søknadsmetodene, men ingen måte å endre innloggingen på samme økt-id.
- `backend/soknad/kjerne/okt.py` -- `begynn(soknad)` setter steget. `Soknad.samtykke` finnes alt.
- `backend/soknad/web/ruter.py` -- `start()` (GET lager ny søknad, POST «Begynn»), `innlegging()` bruker `ki().caser` (bare `TestKI` har det: hent fra `current_app.extensions["test_ki"]`), `resultat()` kaller `ki().brev`. `_vis_*`-hjelperne er mønsteret for en `_vis_start`.
- `backend/soknad/web/templates/start.html` -- bryteren er en `<button role="switch" aria-disabled="true">` utenfor skjema, og `.testinfo role="status"` finnes alltid.
- `backend/soknad/web/templates/base.html` -- hjørneraden (`footer.hjornerad`) har bare «Logg ut» (`.utlogging` har `margin-left: auto`).
- `backend/soknad/web/templates/resultat.html` -- makroen `info` (`.info`, `.info-knapp` med `aria-expanded`/`aria-controls`, `.info-boks hidden`). `static/js/info.js` virker på alle `.info`. Resultatsiden endres ikke.
- `backend/soknad/web/static/css/stil.css` -- `.bryter`, `.hjornerad`, `.info-boks`, `.testinfo`, `@media (forced-colors: active)`, `#bli-her:focus` (mønsteret for `:focus`).
- `backend/tests/web/test_testmodus.py`, `test_startside.py`, `test_innlogging.py`, `test_registrering.py` -- tester som sier at bryteren er låst med nøkkel, må endres. `tests/web/hjelpere.py` har `sett_testmodus`, `FeilendeKI`, `sett_soknad`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/adaptere/oktlager.py` -- metode som bytter `Innlogging` på samme økt-id (søknaden beholdes) -- FR-32.
- [x] `backend/soknad/kjerne/okt.py` -- `begynn(soknad, samtykke=False)` lagrer samtykket -- FR-36, AD-7.
- [x] `backend/soknad/__init__.py`, `web/flyt.py`, `web/innlogging.py` -- `ekte_ki`, `ki()` med typen `KI` og valget ut fra testmodus, `har_nokkel()`, testmodus ved innlogging -- AD-3, FR-32.
- [x] `backend/soknad/web/ruter.py` -- ny rute (POST) for bryteren etter matrisen, med redirect til startsiden og fokus på bryteren etterpå. `start()` POST krever samtykke når testmodus er av. `innlegging()` og `resultat()` sender til startsiden uten KI-kall når testmodus er av og samtykket mangler. `caser` fra `test_ki` -- FR-32, FR-36, AD-12.
- [x] `backend/soknad/web/tekster.py` -- «Teksten din sendes til ekstern KI.», «Jeg samtykker til bruk av KI», «Hva betyr samtykket?», de fire punktene (fet overskrift + tekst), «Du må samtykke før du kan begynne», «Teksten behandles av ekstern KI» -- FR-35, FR-36.
- [x] `backend/soknad/web/templates/start.html`, `base.html` -- bryteren i et eget skjema (med nøkkel uten `aria-disabled`). Med testmodus av: samtykket i «Begynn»-skjemaet (linjen over, boksen, «i»-knappen og «i»-boksen med `.info`-klassene og `info.js`), og ved feil `aria-invalid`, `aria-describedby` til feilteksten og `autofocus`. KI-merknaden nede til venstre i hjørneraden når testmodus er av, med «ⓘ» skjult for skjermlesere -- UX-DR3, UX-DR10, UX-DR11.
- [x] `backend/soknad/web/static/css/stil.css` -- avkrysningsboksen 22 px, rød ramme ved feil, `:focus`-regel for boksen (fokus etter museklikk), KI-merknaden til venstre, og `forced-colors` for bryteren av, den røde rammen, «i»-boksen og KI-merknaden -- UX-DR10.
- [x] `backend/tests/` -- tester for alle radene i matrisen (med en falsk KI i `ekte_ki` som teller kall), at `ki()` gir `EkteKI` og `TestKI` riktig, at boksen er tom etter av-på-av, at KI-merknaden står i hjørneraden bare når testmodus er av, at «i»-boksen har de fire punktene og ARIA, og CSS-sjekkene. Oppdater de gamle testene om låst bryter med nøkkel. FR-nummer i hver fil og funksjon -- FR-32, FR-35, FR-36.
- [x] `README.md` -- testmodus kan slås av med nøkkel, og samtykket -- NFR-8.

**Acceptance Criteria:**
- Gitt nøkkel og testmodus av, når «Sjekk CV-en min» og «Lag søknadsbrevet mitt» trykkes etter samtykke, så kalles `EkteKI` (falsk klient i testene), og med testmodus på kalles `TestKI`.
- Gitt hele testsuiten uten `ANTHROPIC_API_KEY`, når `uv run pytest` kjøres, så går alt gjennom uten nettverk.

## Design Notes

Bryteren er et skjema med POST, ikke JavaScript, fordi skriptene bare endrer visningen (AD-1), og siden lastes på nytt uansett når samtykket skal tømmes. Etter redirecten får bryteren `autofocus` (for eksempel med `?bryter=1`), så tastaturbrukere ikke mister plassen. Sjekken av samtykket i `innlegging()` og `resultat()` er en sikring: i vanlig bruk kan ikke steget komme forbi start uten samtykke når testmodus er av.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

**Manual checks (if no CLI):**
- Kristine, i nettleseren med nøkkel: slå av og på med mus og tastatur (fokus blir på bryteren), «Begynn» uten avkryssing etter museklikk (rød ramme, synlig fokusring på boksen), «i»-boksen med trykk, Enter, Esc og hover, KI-merknaden ved 320 px og i høykontrast.
- Kristine kjører hele flyten én gang med ekte KI på case 1: analysen, og brevet mot sjekklisten i `fasit.md` (kriterium 11 og 12). Hun noterer i PR-en hvor lang tid analysen og brevet tar (for `KI_TIDSGRENSE`), og om brevet hadde flere avsnitt i ett.

## Implementation Notes

- En hjelpeagent kodet ut fra spec-en. Hovedøkta leste diffen, kjørte ruff og pytest (702 tester grønne) og sjekket at hver rad i matrisen har en test som går gjennom.
- Bryteren sender den nye verdien (`testmodus=av` eller `paa`), ikke «bytt», så to trykk eller to faner ikke slår den om to ganger.
- `ki()` gir `TestKI` når testmodus er av, men det ikke finnes noen `EkteKI`. Det skjer bare i testene.
- På innleggingen sjekkes samtykket etter feltsjekken, så feil i feltene vises først.
- Fokusringen tar plassen til den røde ytre rammen mens boksen har fokus, men kanten på selve boksen er fortsatt rød. Det må sjekkes i nettleseren.

## Spec Change Log

- **2026-11-14 (Kristine, etter prøven med ekte KI på case 1):** Kristine savnet et avsnitt der studenten presenterer seg som person, fordi hele brevet handlet om erfaring. Hun valgte at avsnittet står mot slutten. Endret: beslutningen over (inne i den frosne delen, godkjent av Kristine), en ny regel i `prompts/brev.md` og en test i `test_ekte_ki.py`. **KEEP:** resten av koden og rettingene fra gjennomgangen.
- **2026-11-14 (Kristine, samme dag):** Kristine ville at avsnittet om studenten som person kommer først, rett etter overskriften, så arbeidsgiveren blir kjent med personen før ferdighetene, og at Claude ser etter alder, hobbyer og interesser i hele CV-en. Endret: beslutningen over (inne i den frosne delen, godkjent av Kristine), regelen i `prompts/brev.md` og testen i `test_ekte_ki.py`. **KEEP:** som i forrige punkt.
- **2026-11-14 (Kristine, samtykketeksten):** to av de fire punktene i «i»-boksen er endret i EXPERIENCE (Kristines ordlyd): punkt 1 sier «sendes til KI-tjenesten Claude fra selskapet Anthropic», og punkt 3 sier «Nei. Nettsiden lagrer ingenting du legger inn etter at du logger ut.». KI-en foreslo også å nevne at Anthropic kan lagre teksten i opptil 30 dager, men Kristine valgte å la være. Endret: `tekster.py` og testen i `test_samtykke.py`. **KEEP:** resten.

## Review Triage Log

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | kant | `ki()` kalles to ganger på innleggingen. Slås testmodus av i en annen fane mellom kallene, går `gap` til Claude uten samtykke. | medium | Sant: `GET /` i fane B gir steg start, så bryteren kan endres. Vinduet er kort, men det gjelder personvernet (AD-12). Patch: `ki()` kalles én gang, med test. |
| 2 | kant | Sjekken av samtykket og valget av KI leser innloggingen hver for seg | medium | Samme årsak som #1, og rettes med den. |
| 3 | kant | `assert` i `sett_testmodus` forsvinner med `python -O` | low | Testene kjøres aldri med `-O`. Avvist. |
| 4 | verifisering, blind | Ingen test av `innlogging is None` i `start()` POST og `bryter()` (logget ut i en annen fane) | low | Sant, det er nye grener. Patch: to tester, og en test av en annen verdi enn «ja». |
| 5 | verifisering | Docstringen til `uten_testmodus` i `test_innlegging.py` stemmer ikke lenger | low | Direkte retting. Patch. |
| 6 | blind | Samtykkesjekken må kalles i hver rute, og glemmes den i Korrektur, «Nytt forslag» eller «Prøv på nytt», kommer ingen feil | low | «Prøv på nytt» bruker de samme rutene. Korrektur og «Nytt forslag» er nye ruter i Epic 5 og 7, og må kalle `til_start_uten_samtykke`. Ingen feil nå. Avvist, med denne merknaden til Epic 5 og 7. |
| 7 | blind | `har_nokkel()` og `extensions["ekte_ki"]` avgjør hver for seg om nøkkelen finnes | low | To kilder for det samme. Direkte retting. Patch: `har_nokkel()` leser `ekte_ki`. |
| 8 | blind | Sikringen sender til startsiden, og der tømmes CV-en og annonsen uten forklaring | low | Kan ikke nås i vanlig bruk, heller ikke etter #1. Rettingen krever ny tekst og ny gren. Avvist. |
| 9 | blind | Den røde ytre rammen erstattes av fokusringen mens boksen har fokus | low | Kanten på boksen er fortsatt rød. Kristine ser på dette i nettleseren (Manual checks). Avvist foreløpig. |
| 10 | blind | Samtykketeksten nevner ikke Anthropic eller lagring hos KI-tjenesten | low | Teksten er Kristines egen (EXPERIENCE) og står ordrett. Ingen kodefeil. Tas opp med Kristine. |
| 11 | blind | Samtykket lagres også i testmodus når POST-en har `samtykke=ja` | low | Sant, men skjer bare med en laget POST. Direkte retting. Patch. |
| 12 | blind | Ingen CSRF-beskyttelse, og `SESSION_COOKIE_SAMESITE` er ikke satt | low | Fantes før 4.3.1 for alle skjemaene. Samtykket stopper fortsatt KI-kallet. Defer. |
| 13 | blind | Ingen test av en KI-feil med ekte KI | low | Samme rute som før, men en billig test. Patch. |
| 14 | blind | KI-merknaden testes bare på `/` og `/modus` | low | Den kommer fra `base.html` på alle sider. Avvist. |
| 15 | blind | README sier ikke at nøkkelen bare leses ved oppstart, eller hva en ugyldig nøkkel gir | low | Direkte retting. Patch. |
| 16 | blind | Svaret fra `bytt_innlogging` brukes ikke, og en test leser `_innlogginger` | low | `login_required` fanger en utlogget økt. Avvist. |
