---
title: 'Story 1.2: Logge inn med testbrukeren'
type: 'feature'
created: '2026-11-08'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'bff3fbab89ae68df61e60454628679fe226b85c8'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Startsiden er åpen for alle, og det finnes verken database, testbruker eller innlogging. Sensor må kunne logge inn med testbrukeren fra README uten å registrere seg.

**Approach:** Ved oppstart lager `create_app` `instance/brukere.db` med testbrukeren (bare første gang). En vanlig innloggingsside (`/logg-inn`) sjekker e-post og passord, lager en ny økt i minnet og sender til startsiden. Startsiden krever innlogging.

## Boundaries & Constraints

**Always:**
- Passord lagres bare som hash fra `werkzeug.security`. Ingen ekstern tjeneste. Passord logges aldri.
- Testbrukeren `test@example.com` / `testpassord1` står i `innstillinger.py` og lages bare hvis e-posten ikke finnes i tabellen.
- E-post lagres og sammenlignes med `strip()` + `casefold()`. Passordet endres aldri (ingen `strip`).
- Innlogging: `session.clear()`, gammel økt slettes fra minnet, ny tilfeldig økt-id. Cookien har bare økt-id-en. `Innlogging(bruker_id, testmodus=True)`: testmodus er alltid på fram til Epic 4.
- Etter riktig innlogging: redirect til startsiden, alltid (ingen `next=`). Feil: samme side på nytt, uten redirect, status 200, e-posten står fortsatt i feltet, passordet aldri.
- Feiltyper i `kjerne/feil.py` (`StrEnum`: `tom`, `epost_finnes`, `epost_ugyldig`, `passord_kort`, `passord_ulike`, `feil_innlogging`) og `InndataFeil(felt, type)`. `felt=None` betyr hele skjemaet. Alle tekster i `web/tekster.py`.
- Skjema: `novalidate`, etikett over feltet, feiltekst under koblet med `aria-describedby`, `aria-invalid="true"`, rød ramme. Fokus uten JavaScript: `autofocus` på første felt med feil, eller på skjemafeil-boksen (`tabindex="-1"`, uten `role="alert"`). Liming og passordbehandler er lov.
- `kjerne/` importerer aldri flask, werkzeug eller sqlite3.

**Never:**
- Ingen registrering, lenke «Ny her? Registrer deg her», utlogging, hjørnerad eller «Du må logge inn først» (story 1.3 og 1.4).
- Ingen JavaScript, ingen CSRF (utsatt i arkitekturen), ingen nye avhengigheter.
- Testene skriver aldri til den ekte `backend/instance/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Første oppstart | Ingen `instance/` | Mappen, `brukere.db`, tabellen og testbrukeren lages | N/A |
| Ny oppstart | Testbrukeren finnes | Ingen ny rad, hashen er uendret | N/A |
| Riktig innlogging | `test@example.com` / `testpassord1` | 302 til `/`, ny økt i minnet, `/` gir 200 | N/A |
| Store bokstaver, mellomrom | ` Test@Example.com ` / riktig passord | Logget inn | N/A |
| Feil passord / ukjent e-post | gyldig e-post, feil passord | Skjemafeil «Feil e-post eller passord» med fokus, ingen rød ramme | Ikke logget inn |
| Tomme felt | begge tomme (eller e-post bare mellomrom) | «Fyll inn e-post» og «Fyll inn passord» samtidig, fokus på e-post | Ingen databasesjekk |
| Ikke logget inn | GET `/` uten økt | 302 til `/logg-inn` | N/A |
| Gammel cookie | Økt-id finnes ikke i minnet | Behandles som utlogget | N/A |

</frozen-after-approval>

## Code Map

- `backend/soknad/__init__.py` -- `create_app`. Legg til `INSTANCE_MAPPE` (modulnivå, som `ENV_FIL`) og `Flask(..., instance_path=...)`, `DATABASE` i config (test_config kan overstyre), lag databasen etter `test_config`, og legg øktlageret i `app.extensions`.
- `backend/soknad/innstillinger.py` -- legg til testbrukeren.
- `backend/soknad/web/ruter.py`, `tekster.py`, `templates/base.html`, `start.html` -- bygg videre på dem. `felles_tekster` gjør `tekster` tilgjengelig i alle maler.
- `backend/soknad/web/static/css/stil.css` -- bare `var(--…)` utenfor `:root`. Tokens som trengs finnes (`--error`, `--error-tint`, `--form-max`, `--rounded-sm/lg`, `--size-label`, `--size-small`, `--shadow`, `--shadow-hover`, `--size-heading-page`).
- `backend/tests/conftest.py` -- autouse-fiksturen `ingen_ekte_env` får også `INSTANCE_MAPPE` til `tmp_path`.
- `backend/tests/web/test_ruter.py` -- testene av `/` må logge inn først. `MALER`-sjekken (ingen `style`) dekker nye maler.
- `README.md` linje 57 -- «*Kommer:* e-post og passord til testbrukeren» erstattes.
- Skissen `_bmad-output/planning-artifacts/ux-designs/ux-kode-prosjekt-2026-10-20/mockups/login-register-1.html` viser oppsettet (ikke kopier `role="alert"` eller Google Fonts derfra).

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/innstillinger.py` -- `TESTBRUKER_EPOST`, `TESTBRUKER_PASSORD`.
- [x] `backend/soknad/kjerne/__init__.py`, `feil.py`, `okt.py`, `inndata.py` -- feiltypene, `Innlogging` (frosset dataklasse), `normaliser_epost()` og `sjekk_innlogging(epost, passord) -> list[InndataFeil]` (tomme felt).
- [x] `backend/soknad/adaptere/__init__.py`, `db.py`, `oktlager.py` -- `lag_database(sti)` (tabell `brukere(id, epost UNIQUE, passord_hash)` + testbruker), `finn_bruker(sti, epost, passord) -> int | None`; `Oktlager` med `ny(innlogging) -> okt_id`, `hent(okt_id)`, `slett(okt_id)`.
- [x] `backend/soknad/__init__.py` -- som i Code Map.
- [x] `backend/soknad/web/innlogging.py` -- `login_required` (sender til `web.logg_inn`) og `logg_inn_bruker(bruker_id)`.
- [x] `backend/soknad/web/ruter.py`, `tekster.py`, `templates/logg_inn.html` -- GET/POST `/logg-inn`, `login_required` på `/`, tekstene og feiltekstene.
- [x] `backend/soknad/web/static/css/stil.css` -- skjemakort, felt, feiltekst, skjemafeil, hovedknapp (hover løft 2 px og skygge, trykk 96 %, låst 55 %, 0,15 s).
- [x] `backend/tests/` -- `conftest.py` (instans i `tmp_path`, fiksturen `innlogget_client`), `kjerne/test_inndata.py`, `adaptere/test_db.py`, `adaptere/test_oktlager.py`, `web/test_innlogging.py`, og oppdater `web/test_ruter.py`. Dekker matrisen, hashing (ingen klartekst i databasefilen), én testbruker, og at `kjerne/` ikke importerer flask/werkzeug/sqlite3. Hver test nevner FR/NFR.
- [x] `README.md` -- testbrukerens e-post og passord.

**Acceptance Criteria:**
- Given innloggingssiden, then har den tittelen «Logg inn – Søknadsassistenten», én `h1` «Logg inn», feltene «E-post» (`autocomplete="email"`) og «Passord» (`autocomplete="current-password"`) og knappen «Logg inn».
- Given en ny kopi, when nettsiden startes og testbrukeren fra README logges inn, then vises «Velkommen! 👋».
- Given siden i nettleseren ved 375 og 1280 px, then ruller ingenting sidelengs, og alt kan brukes med tastatur med synlig fokusring.

## Implementation Notes

- Werkzeugs vanlige hash (scrypt) tar ca. 0,84 s her. Med den tok testene 66 s. Den autouse-fiksturen `rask_hash` i `conftest.py` bytter derfor til pbkdf2 bare i testene. `test_nfr1_ekte_oppstart_bruker_werkzeugs_vanlige_hash` sjekker at den ekte koden gir `scrypt:`.
- Skjemafeil-boksen og `h1` står inne i skjemakortet, som i skissen. Feltene har `padding: 10px var(--space-3)`: 10 px kommer fra `text-input` i DESIGN.md, og det finnes ingen token for det.
- GET `/logg-inn` når man er innlogget, viser bare skjemaet.
- `test_fr3_ingen_registrering_eller_utlogging_ennaa` må endres i story 1.3 og 1.4.
- Prøvd med en ekte server og i headless Edge (1280 og 500 px): ingen sidelengs rulling, og `autofocus` gir fokusringen på første felt med feil og på skjemafeil-boksen. Passordet står ikke i serverloggen. `backend/instance/` er slettet etterpå.
- Etter implementeringen: 58 tester, `ruff check` og `ruff format --check` grønne.
- Etter gjennomgangen (9 rettelser): 59 tester, `ruff check` og `ruff format --check` grønne. `Innlogging` har ikke lenger standardverdi for `testmodus`.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-08), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Ukjent e-post svarer raskere enn feil passord (tidsforskjell) | blind, grensetilfeller | low | Riktig: ukjent e-post hopper over scrypt. Nettsiden kjører bare lokalt, og rettingen krever en ekstra hash og en gren | avvist |
| 2 | Øktlageret vokser uten grense, gamle økter gjelder for alltid | blind, grensetilfeller | low | Riktig, men én bruker lokalt. Arkitekturen sier «ingen automatisk utlogging», så en tidsgrense ville brutt den | avvist |
| 3 | Knappen hopper fortsatt ved redusert bevegelse | blind, grensetilfeller | low | `transform` på hover/trykk gjelder fortsatt, bare uten overgang. Rettes med én linje | patch |
| 4 | `feiltekst()` gir 500 for (felt, type) uten tekst | blind, grensetilfeller | false | Koden lager i dag bare `epost`/`passord` + `tom` og `None` + `feil_innlogging`, og alle tre har tekst | avvist |
| 5 | `client` og `innlogget_client` er samme objekt i to tester | blind, grensetilfeller | low | Riktig: `/logg-inn` hentes som innlogget. Rettes med en egen anonym klient | patch |
| 6 | `test_nfr1_passordet_logges_aldri` kan aldri feile | blind | low | Riktig: testklienten og appen logger ingenting, så `caplog` er tom. Testen slettes. Serverloggen ble sjekket for hånd | patch |
| 7 | Testen av økten sjekker ikke `bruker_id` | blind, testhull | low | Riktig: docstringen lover mer enn testen sjekker. Én assert til | patch |
| 8 | Ingen test av at e-posten escapes i `value` | blind | low | Jinja escaper i dag. En kort test hindrer at det brytes senere | patch |
| 9 | «Testmodus på» står to steder | blind | low | Riktig: standardverdi i `okt.py` og argument i `innlogging.py`. Standardverdien fjernes | patch |
| 10 | Slettet database mens serveren kjører gir 500 | blind, grensetilfeller | low | Riktig, men README sier at serveren skal stoppes først. Rettingen krever en ekstra sjekk | avvist |
| 11 | Ny app-test sjekker ikke at lageret er tomt | blind | low | Testen viser at det er et nytt objekt. Å sjekke at det er tomt krever privat tilgang | avvist |
| 12 | `"<script" not in html` sjekkes to ganger | blind | low | Riktig, linjen slettes | patch |
| 13 | README sier ikke at omstart logger ut alle | blind | low | Sensor kan tro det er en feil. Én setning | patch |
| 14 | To prosesser som starter samtidig kan begge legge inn testbrukeren | grensetilfeller | low | Nettsiden kjører i én prosess (arkitekturen). `INSERT OR IGNORE` alene ville laget en scrypt-hash ved hver oppstart | avvist |
| 15 | Flere prosesser ville gitt hver sitt øktlager | grensetilfeller | false | Arkitekturen sier én prosess, og README starter med `flask run` | avvist |
| 16 | Feil passord som innlogget beholder den gamle økten | grensetilfeller | low | Ikke en tydelig feil, og rettingen legger til ny oppførsel | avvist |
| 17 | `casefold()` gjør «ß» til «ss» | grensetilfeller | low | Svært lite sannsynlig, og `casefold` er bestemt i spec-ens låste del | avvist |
| 18 | `DATABASE=":memory:"` virker ikke | grensetilfeller | false | Ingen kode eller test setter den verdien | avvist |
| 19 | Standardplasseringen `backend/instance/` testes aldri | testhull | low | Riktig: autouse-fiksturen bytter alltid `INSTANCE_MAPPE`. README sier at mappen kan slettes | patch |

## Design Notes

Øktlageret ligger i `app.extensions["oktlager"]`, så hver test-app får sitt eget. Cookien har bare `session["okt_id"]`, og navnet er en konstant i `web/innlogging.py`. Feiltekstene slås opp med `(felt, type)`, for eksempel `("epost", FeilType.TOM) → "Fyll inn e-post"`, `(None, FeilType.FEIL_INNLOGGING) → "Feil e-post eller passord"`.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alle tester grønne
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Kristine starter nettsiden, logger inn med testbrukeren og prøver tomme felt og feil passord.
