---
title: 'Story 1.1: Nettsiden starter fra en ny kopi av repoet'
type: 'feature'
created: '2026-11-08'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'bb34317f4803671a35ad9d992adcea705da811f3'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-kode-prosjekt-2026-10-20/DESIGN.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Repoet har ingen kode ennå. Sensor må kunne starte nettsiden fra en ny kopi med tre kommandoer, uten å lage `.env` først, og alle senere stories trenger en felles grunnmur (app, `base.html`, farger, CI og første test).

**Approach:** Lage Flask-appen i `backend/` med `create_app(test_config)`, en startside som arver `base.html` (logo i lokal Baloo 2, alle design-tokens som CSS-variabler), utvide lærerens CI med ruff og Windows, og skrive installasjon og testing i README.

## Boundaries & Constraints

**Always:**
- Nettsiden starter uten `.env`: mangler `SECRET_KEY`, lages en tilfeldig ved oppstart. Mangler `ANTHROPIC_MODEL`, brukes `claude-opus-5-5`. Finnes `backend/.env`, leses den.
- Alle filer åpnes med `encoding="utf-8"`. Ruff-regelen `PLW1514` er på og er bevist å slå til.
- Alle farger, skrifter, hjørner, avstander og skyggen fra DESIGN.md står som CSS-variabler i `:root` i én fil. Ingen fargekoder andre steder.
- `base.html`: `lang="nb"`, sidetittel per side (`Startside – Søknadsassistenten`), landemerkene `header` (logoen, ikke en overskrift), `main` og `footer`. Hver side har én `h1`.
- Logoen «Søknadsassistenten» står sentrert øverst i Baloo 2 ExtraBold (800) fra en fil i prosjektet, `font-size: clamp(1.35rem, 5vw, 2.4rem)`, uten `nowrap` og uten faste høyder.
- Startsiden viser bare «Velkommen! 👋» (`h1`) og ingressen «Her lager du et søknadsbrev som passer til stillingen du vil søke på.» Brukertekster ligger i `web/tekster.py`.
- Lærerens `ci.yml` utvides i backend-jobben (matrise Linux og Windows, ruff check, ruff format --check, pytest). De andre jobbene er uendret.
- Tester nevner FR/NFR-nummer i navn eller docstring. Versjoner: Flask 3.1.3, python-dotenv 1.2.4, pytest 9.2.0, ruff 0.17.3, Python ≥ 3.12 (`.python-version` = 3.14).

**Never:**
- Ingen innlogging, database, `kjerne/` eller `adaptere/` (story 1.2–1.4). Ingen `instance/`-mappe lages ennå, bare `.gitignore`-linjen.
- Ingenting hentes fra Google Fonts eller andre nettadresser når siden kjører.
- Ingen hemmeligheter eller verdier i `.env.example`. Ingen JavaScript.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Ny kopi | Ingen `.env`, ingen `SECRET_KEY` i miljøet | Appen starter, `SECRET_KEY` er en tilfeldig streng på minst 32 tegn | N/A |
| Med `.env` | `SECRET_KEY` satt i miljøet | Den verdien brukes | N/A |
| Test-config | `create_app({"TESTING": True, "SECRET_KEY": "x"})` | test_config vinner over miljøet | N/A |
| Startsiden | GET `/` | 200, `lang="nb"`, én `h1`, `header`/`main`/`footer`, ingen `fonts.googleapis` | N/A |
| Ukjent side | GET `/finnes-ikke` | 404 | Flasks vanlige 404 |

</frozen-after-approval>

## Code Map

- `.github/workflows/ci.yml` -- lærerens CI. Backend-jobben hopper over seg selv uten `backend/pyproject.toml` og kjører i dag `uv run --with pytest pytest`. Behold `if: hashFiles(...)`-mønsteret, navnene og jobbene `prosjekt` og `frontend` uendret.
- `.gitignore` -- har `.env`, `.env.*`, `!.env.example`. Mangler `instance/`.
- `README.md` -- seksjonene «Installasjon og oppstart» og «Testdata og tester» står som *Kommer*. Behold resten av ordlyden.
- `backend/` -- finnes ikke ennå. Struktur fra arkitekturen: `soknad/{__init__.py, innstillinger.py, web/}`, `tests/`.
- Ingen skriftfil finnes i repoet. Baloo 2 er OFL-lisensiert i `google/fonts` på GitHub (`ofl/baloo2/`).

## Tasks & Acceptance

**Execution:**
- [x] `backend/pyproject.toml`, `backend/.python-version`, `backend/uv.lock` -- prosjekt `soknad`, `requires-python = ">=3.12"`, avhengigheter flask og python-dotenv, dev-gruppe pytest og ruff (eksakte versjoner), ruff-oppsett med `PLW1514` (med `preview`/`explicit-preview-rules` hvis regelen krever det). Lag `uv.lock` med `uv lock` -- grunnmur for alt.
- [x] `backend/soknad/innstillinger.py` -- `STANDARD_MODELL = "claude-opus-5-5"` og `MAKS_FORESPORSEL = 16 * 1024 * 1024` -- konstanter på ett sted.
- [x] `backend/soknad/__init__.py` -- `create_app(test_config=None)`: `load_dotenv(backend/.env)` uten å overstyre miljøet, `SECRET_KEY` fra miljøet eller `secrets.token_hex(32)`, `ANTHROPIC_MODEL` med standardverdi, `ANTHROPIC_API_KEY` (kan være tom), `MAX_CONTENT_LENGTH`, så `test_config`, og registrer web-blueprinten.
- [x] `backend/soknad/web/__init__.py`, `ruter.py`, `tekster.py` -- blueprint med `/` som viser `start.html` med tekstene fra `tekster.py`.
- [x] `backend/soknad/web/templates/base.html`, `start.html` -- `base.html` med `lang`, tittel-blokk, viewport, lenke til CSS, `header` med logoen, `main`, tom `footer`. `start.html` arver.
- [x] `backend/soknad/web/static/css/stil.css` -- alle tokens fra DESIGN.md i `:root`, `@font-face` for Baloo 2, grunnoppsett (sidemarg 20/16 px, `max-width` på innhold, ingen sidelengs rulling).
- [x] `backend/soknad/web/static/fonts/` -- Baloo 2 ExtraBold som `.woff2`, laget én gang fra den variable TTF-en i `google/fonts` (instans på vekt 800, delmengde Latin + Latin-1 med æøå) med `uvx fonttools`, og `OFL.txt` ved siden av.
- [x] `backend/.env.example` -- `ANTHROPIC_API_KEY=`, `ANTHROPIC_MODEL=`, `SECRET_KEY=` med korte norske kommentarer.
- [x] `.gitignore` -- legg til `instance/`.
- [x] `backend/tests/conftest.py`, `backend/tests/test_app.py`, `backend/tests/web/test_ruter.py` -- fikstur `app`/`client` med test_config. Tester for matrisen over (NFR-1, NFR-2, NFR-8), `lang="nb"` og én `h1` (NFR-6), og en test som leser `stil.css` og malene og feiler hvis det finnes `#rgb`/`rgba(` utenfor `:root` (UX-DR1).
- [x] `.github/workflows/ci.yml` -- backend-jobben: `strategy.matrix.os: [ubuntu-latest, windows-latest]`, `runs-on: ${{ matrix.os }}`, nye steg `uv run ruff check` og `uv run ruff format --check`, og pytest via dev-gruppen.
- [x] `README.md` -- fyll inn «Installasjon og oppstart» (uv på Windows og Mac, de tre kommandoene, `.env.example` er valgfri) og «Testdata og tester» (`uv run pytest`, `uv run ruff check`). Testbruker og testdata står fortsatt som «kommer».

**Acceptance Criteria:**
- Given en ny kopi uten `.env`, when `cd backend`, `uv sync` og `uv run flask --app soknad run` kjøres, then starter nettsiden på localhost uten feil.
- Given en fil med `open(p)` uten `encoding`, when `uv run ruff check` kjøres, then feiler den med `PLW1514` (prøves lokalt og fjernes igjen).
- Given startsiden ved 375, 768 og 1280 px, when den vises i nettleseren, then står logoen på én linje, sentrert, i Baloo 2, og ingen side ruller sidelengs.
- Given en PR, when CI kjører, then er backend-jobben grønn på både Linux og Windows.

## Implementation Notes

- `PLW1514` er en preview-regel i ruff 0.17.3. Uten `preview = true` sier ruff at regelen «has no effect». Løst med `preview = true` og `explicit-preview-rules = true`, så bare reglene vi velger selv er preview. Prøvd med en midlertidig fil med `open(p)`: ruff feiler.
- Baloo 2 er laget fra den variable TTF-en i `google/fonts` med `uvx fonttools` (vekt 800, Latin + Latin-1). Filen er 17 kB og har æøå/ÆØÅ.
- Egne valg utenfor spec-en: `--content-max: 1100px`, fokusring på 3 px og regel for redusert bevegelse, og slør-fargene fra DESIGN.md som tokens i `:root`.
- Prøvd i headless Edge ved 320, 375, 768 og 1280 px: logoen på én linje, ingen sidelengs rulling. Edge kan ikke lage vinduer smalere enn ca. 500 px, så 320 og 375 ble prøvd i en ramme.
- Etter gjennomgangen: 17 tester, `ruff check` og `ruff format --check` grønne.

## Spec Change Log

Ingen endringer (ingen tilbakeløp fra gjennomgangen).

## Review Triage Log

Runde 1 (2026-11-08), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Tomme verdier fra en kopiert `.env.example` er ikke testet | testhull, blind | medium | Ingen test skriver `SECRET_KEY=` i `.env`. Bytter man `or` mot `get(..., standard)`, er alle tester fortsatt grønne, men nøkkelen blir tom | patch |
| 2 | `ANTHROPIC_API_KEY` fra miljøet eller `.env` er ikke testet | testhull | low | Eneste test sjekker `""`. En feilstavet nøkkel ville ikke blitt oppdaget. Rettes med én assert | patch |
| 3 | Fiksturen `app` kan få ekte nøkler fra terminalen | blind, grensetilfeller | low | `ingen_ekte_env` bytter bare `ENV_FIL`, `os.environ` beholdes. Rettes med `delenv` i fiksturen | patch |
| 4 | Fargesjekken slår til på `&#8211;` og `href="#add"` i maler | blind | low | `#[0-9a-fA-F]{3,8}\b` treffer begge. Vil stoppe gyldige maler i senere stories | patch |
| 5 | Fargesjekken finner ikke fargenavn, `oklch()` og lignende | blind, grensetilfeller | low | Riktig, men lite sannsynlig og krever en lang liste med navn | avvist |
| 6 | Sjekken for ressurser utenfra finner ikke `@import` og `href = "…"` | grensetilfeller | low | Riktig. Rettes med en litt bredere regex | patch |
| 7 | CI bruker `uv sync` uten `--locked` | blind, grensetilfeller | low | En utdatert `uv.lock` blir løst på nytt i stedet for å feile | patch |
| 8 | `ci.yml` slutter uten linjeskift | blind | low | Var slik fra før, rettes i samme linje | patch |
| 9 | Port 5000 er opptatt av AirPlay på nyere Mac | blind, grensetilfeller | medium | Sensor på Mac kan få feil eller 403. README sier ingenting | patch |
| 10 | README nevner ikke Linux | blind | low | curl-kommandoen virker også på Linux | patch |
| 11 | README lover sjekk av `utf-8`, men `PLW1514` krever bare en `encoding` | grensetilfeller | low | Ordlyden lover mer enn ruff sjekker | patch |
| 12 | `.ingress` har `margin: 0 auto` uten `max-width` | blind | low | `auto` gjør ingenting. Rettes ved å fjerne den | patch |
| 13 | Ulik lesing av nøklene, mellomrom regnes som verdi | blind, grensetilfeller | low | Bare mulig når nøkkelen settes i operativsystemet med bare mellomrom. Lite sannsynlig | avvist |
| 14 | `load_dotenv` endrer `os.environ` | blind | false | Flask CLI gjør det samme. Ingen feil for brukeren | avvist |
| 15 | Følgene av tom `SECRET_KEY` er ikke beskrevet | blind | false | README sier «En tilfeldig nøkkel lages ved hver oppstart». Økten ligger i minnet og forsvinner ved omstart uansett. Bare én prosess | avvist |
| 16 | CI tester bare Python 3.14 | blind | low | uv bruker alltid `.python-version`, også hos sensor. Lite sannsynlig å treffe | avvist |
| 17 | uv-versjonen håndheves ikke | blind | low | Installasjonen gir nyeste uv | avvist |
| 18 | Tom sidetittel når en side ikke fyller blokken | blind, grensetilfeller | low | Ingen side mangler blokken. Hver side skal ha egen tittel | avvist |
| 19 | Tom `footer` | blind | false | Landemerket kreves av storyen. Hjørneraden kommer i story 1.4 | avvist |
| 20 | Logoen er ikke en lenke, ingen favicon | blind | false | Ingen av delene er krav. 404 for favicon er bare en linje i loggen | avvist |
| 21 | `instance/` i `.gitignore` er for bred | blind | false | Arkitekturen sier `instance/` | avvist |
| 22 | Ingen test for 413 ved 16 MB | blind | low | Grensen brukes først når filopplasting kommer | avvist |
| 23 | Testene sammenligner med fast tekst | blind | false | Med vilje: testen sjekker den eksakte ordlyden fra UX | avvist |
| 24 | `OFL.txt` har BOM | blind | low | Lisensfilen er kopiert uendret fra kilden | avvist |
| 25 | Flasks engelske 404- og 413-side | grensetilfeller | false | Matrisen i spec-en sier «Flasks vanlige 404» | avvist |

## Design Notes

Skriften lastes ned én gang mens storyen lages (fra GitHub, ikke Google Fonts-tjenesten) og ligger så i repoet. `.woff2` med bare vekt 800 og Latin-tegn er liten (ca. 20–40 kB). `font-display: swap` gir systemskrift til filen er lastet. Teksten «Søknadsassistenten» i logoen ligger i `tekster.py` som de andre tekstene.

## Verification

**Commands:**
- `cd backend; uv sync; uv run pytest` -- expected: alle tester grønne
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run flask --app soknad run` -- expected: starter, `/` gir 200

**Manual checks:**
- Kristine åpner `http://127.0.0.1:5000` og ser logo og velkomst, også smalt vindu (375 px).
</content>
</invoke>
