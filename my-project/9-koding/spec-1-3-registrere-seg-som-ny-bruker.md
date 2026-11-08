---
title: 'Story 1.3: Registrere seg som ny bruker'
type: 'feature'
created: '2026-11-08'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '29c7d19f92d551c7e76e12a19054a3799542ef65'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Bare testbrukeren kan logge inn. En student kan ikke lage sin egen bruker (FR-1, FR-2).

**Approach:** En vanlig registreringsside (`/registrer`) med «E-post», «Passord» og «Gjenta passord». Riktig utfylt lagrer brukeren med hashet passord, logger inn med ny økt og sender til startsiden. Innloggingen og registreringen lenker til hverandre.

## Boundaries & Constraints

**Always:**
- Samme oppsett og regler som innloggingen fra story 1.2: `novalidate`, etikett over, feiltekst under koblet med `aria-describedby`, `aria-invalid="true"`, rød ramme, `autofocus` på første felt med feil (rekkefølge: e-post, passord, gjenta). Ingen JavaScript.
- Tekster (alle i `web/tekster.py`): tittel og `h1` «Registrer deg», knapp «Registrer deg», hjelpetekst «Minst 8 tegn» under passordfeltet hele tiden (koblet med `aria-describedby`, sammen med feilteksten når den finnes). Feil: «Fyll inn e-post», «Fyll inn passord», «Gjenta passordet», «Passordet må ha minst 8 tegn», «E-posten er ikke gyldig», «Passordene er ikke like» (ved «Gjenta passord»), «Denne e-posten er allerede registrert».
- `autocomplete`: `email`, og `new-password` på begge passordfeltene.
- Alle feilene vises samtidig, høyst én per felt. E-post: tom → ugyldig → finnes. Passord: tom → kort. Gjenta: tom → ulike.
- Gyldig e-post: `^[^@\s]+@[^@\s]+\.[^@\s]+$` etter `normaliser_epost` (som i skissen). E-posten lagres normalisert.
- Passordet endres aldri (ingen `strip`). Minst 8 tegn = `len(passord) >= MIN_PASSORD_LENGDE` (8, i `innstillinger.py`).
- Lykkes det: `logg_inn_bruker(ny_id)` (ny økt-id, `testmodus=True`), redirect til startsiden. Feiler det: samme side, status 200, e-posten står igjen, passordene aldri.
- Under innloggingsskjemaet: «Ny her? Registrer deg her» (lenke på «Registrer deg her»). Under registreringsskjemaet: «Har du allerede en bruker? Logg inn» (lenke på «Logg inn»). Lenkene er understreket og i `primary`.

**Never:**
- Ingen utlogging, «Logg ut», hjørnerad eller «Du må logge inn først» (story 1.4).
- Ingen nye avhengigheter, ingen CSRF, ingen endring av tabellen `brukere`.
- Testene skriver aldri til den ekte `backend/instance/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Riktig registrering | `ola@x.no`, `passord12` to ganger | 302 til `/`, ny rad med hash, innlogget | N/A |
| Allerede registrert | ` Ola@X.no ` når `ola@x.no` finnes | «Denne e-posten er allerede registrert» ved e-post | Ingen ny rad |
| Testbrukeren | `test@example.com` | Samme feil som over | Ingen ny rad |
| Alt tomt | tre tomme felt | Tre feiltekster samtidig, fokus på e-post | Ingen databasesjekk |
| Ugyldig e-post | `ola@` | «E-posten er ikke gyldig» | Ingen databasesjekk for e-posten |
| For kort passord | 7 tegn, like | «Passordet må ha minst 8 tegn», fokus på passord | Ikke lagret |
| Ulike passord | `passord12` / `passord13` | «Passordene er ikke like» ved gjenta | Ikke lagret |
| Flere feil | finnes + kort + ulike | Alle tre feilene samtidig | Ikke lagret |
| Passord tomt, gjenta fylt | `""` / `passord12` | Bare «Fyll inn passord» (ulike sjekkes bare når begge er fylt) | Ikke lagret |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/inndata.py` -- `normaliser_epost`, `sjekk_innlogging`. Legg til `sjekk_registrering`. Kjernen importerer aldri flask/werkzeug/sqlite3.
- `backend/soknad/kjerne/feil.py` -- alle feiltypene finnes alt. Ikke endre.
- `backend/soknad/adaptere/db.py` -- `_koble_til`, `lag_database`, `finn_bruker`. `generate_password_hash` brukes via modulnavnet (testene bytter den ut med `rask_hash`).
- `backend/soknad/web/ruter.py` -- `logg_inn` og `_vis_logg_inn` er mønsteret (feltfeil, skjemafeil, fokus).
- `backend/soknad/web/innlogging.py` -- `logg_inn_bruker` gjenbrukes uendret.
- `backend/soknad/web/templates/logg_inn.html` -- makroen `felt` flyttes til en felles makrofil og får valgfri hjelpetekst.
- `backend/soknad/web/static/css/stil.css` -- bare `var(--…)` utenfor `:root`. `--text-muted`, `--size-small`, `--primary` finnes. Fokusringen er global (`:focus-visible`).
- `backend/tests/web/test_innlogging.py` -- `Tagger`, `felt`, `med_autofocus` kan gjenbrukes. `test_fr3_ingen_registrering_eller_utlogging_ennaa` endres.
- Skissen `_bmad-output/planning-artifacts/ux-designs/ux-kode-prosjekt-2026-10-20/mockups/login-register-1.html` (seksjonen `#reg`) viser oppsettet. Ikke kopier `role="alert"`, Google Fonts eller JavaScript derfra.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/innstillinger.py` -- `MIN_PASSORD_LENGDE = 8`.
- [x] `backend/soknad/kjerne/inndata.py` -- `sjekk_registrering(epost, passord, gjenta) -> list[InndataFeil]` med reglene over (ikke «finnes»).
- [x] `backend/soknad/adaptere/db.py` -- `epost_finnes(sti, epost) -> bool` og `lag_bruker(sti, epost, passord) -> int | None` (None ved `IntegrityError`, altså e-posten kom inn i mellomtiden).
- [x] `backend/soknad/web/ruter.py`, `tekster.py` -- GET/POST `/registrer` (endepunkt `web.registrer`, uten `login_required`). «Finnes» sjekkes bare når e-posten ellers er gyldig. `lag_bruker` kalles bare uten feil; gir den None, vises «finnes»-feilen.
- [x] `backend/soknad/web/templates/skjemafelt.html` (ny), `logg_inn.html`, `registrer.html` (ny) -- felles makro, lenkene under skjemaene.
- [x] `backend/soknad/web/static/css/stil.css` -- `.hjelpetekst` (`--text-muted`, `--size-small`) og lenkeraden under skjemaet (sentrert, understreket lenke i `--primary`, `font-weight: 600`).
- [x] `backend/tests/` -- `kjerne/test_inndata.py` (alle regler og rekkefølgen), `adaptere/test_db.py` (`lag_bruker` lagrer normalisert e-post og bare hash, None ved finnes, `epost_finnes`), ny `web/test_registrering.py` (siden, matrisen, auto-innlogging med ny økt-id, lenkene begge veier, escaping), og endre testen for story 1.4 i `web/test_innlogging.py` til bare å sjekke «Logg ut» og «Du må logge inn først». Hver test nevner FR/NFR.

**Acceptance Criteria:**
- Given registreringen, then har den tittelen «Registrer deg – Søknadsassistenten», én `h1`, de tre feltene med etiketter, `autocomplete` som over, «Minst 8 tegn» koblet til passordfeltet før noe er sendt, og ingen `aria-invalid` eller `autofocus`.
- Given en ny bruker registrert, when brukeren senere logger inn med samme e-post (andre bokstaver) og passord, then kommer brukeren inn.
- Given siden i nettleseren ved 375 og 1280 px, then ruller ingenting sidelengs, og alt (også lenkene) kan brukes med tastatur med synlig fokusring.

## Implementation Notes

- Etter implementeringen: 110 tester (59 før), `ruff check` og `ruff format --check` grønne.
- Lenkeraden står inne i skjemakortet, under knappen, som i skissen.
- `test_registrering.py` henter hjelperne `felt`, `med_autofocus` og `tagger_i` fra `tests.web.test_innlogging` (virker med `pythonpath = ["."]`).
- Etter gjennomgangen (3 rettelser i testene): fortsatt 110 tester, `ruff check` og `ruff format --check` grønne.
- Prøvd med en ekte server og midlertidig database i headless Edge: 1280 px direkte, og 375 px i en ramme som er 375 px bred (Edge uten vindu blir ikke smalere enn ca. 500 px). Ingen sidelengs rulling, `autofocus` gir fokusringen på e-postfeltet ved feil, og lenkene vises på begge sidene. Den ekte `backend/instance/brukere.db` ble ikke rørt.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-08), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Testen «ingenting hentes utenfra» sjekker ikke `/registrer` | testhull | low | Riktig: testen henter bare `/logg-inn` og `/`. Én linje til | patch |
| 2 | Testen av escaping ville også bestått hvis e-posten ble borte | blind | low | Riktig: den sjekket bare at `<script` mangler. Sjekker nå at verdien kommer tilbake | patch |
| 3 | `aria-describedby` med hjelpetekst og feil testes ikke ved for kort passord | blind | low | Riktig: bare sjekket når alt er tomt. Én assert til | patch |
| 4 | Ingen øvre grense for e-post og passord | blind, grensetilfeller | low | Nettsiden kjører lokalt med én bruker, og forespørselen er alt begrenset til 16 MB. Rettingen krever en ny regel og en ny feiltekst | avvist |
| 5 | `lag_bruker` tolker alle `IntegrityError` som «finnes» | blind | false | Den eneste andre regelen er `NOT NULL`, og verken normalisert e-post eller hash kan være `None` | avvist |
| 6 | README nevner ikke registreringen | blind | low | Installasjon, oppstart og testing er uendret, og lenken står på innloggingssiden. Sensor bruker testbrukeren | avvist |
| 7 | Testene henter hjelpere fra en annen testfil | blind | low | Virker på Linux og Windows med `pythonpath = ["."]`. Å flytte dem er en omskriving uten feil å rette | avvist |
| 8 | Passord med bare mellomrom godtas | blind | low | Bestemt i spec-ens låste del: passordet endres aldri, og lengden er `len(passord)`. Innloggingen gjør det samme | avvist |
| 9 | Innlogget bruker kan registrere seg og får ny økt | blind, grensetilfeller | low | Samme som innloggingen fra story 1.2, og registrering skal logge inn den nye brukeren. Rettingen legger til ny oppførsel | avvist |
| 10 | Fokus avhenger av rekkefølgen i feillista | blind | low | Står i docstringen, og testene sjekker fokus i alle tilfellene. Ingen feil i dag | avvist |
| 11 | Regex godtar `ola@x..no` og `ola@x.no.` | blind, grensetilfeller | low | Regelen er valgt i spec-ens låste del (som i skissen). En enkel sjekk av formen, ikke full e-postkontroll | avvist |
| 12 | Tester som bare gjentar konstanter og CSS-tekst | blind | low | Samme mønster som i story 1.2. De fanger at tekstene endres ved et uhell | avvist |
| 13 | «Database is locked» gir 500 | grensetilfeller | low | Én prosess lokalt, og SQLite venter 5 s. Svært lite sannsynlig | avvist |
| 14 | `casefold()` gjør «ß» til «ss» | grensetilfeller | low | Bestemt i story 1.2 (funn 17), svært lite sannsynlig | avvist |
| 15 | Ingen CSRF-beskyttelse | grensetilfeller | low | Utsatt i arkitekturen og står under «Never» i spec-en | avvist |
| 16 | `registrer.html` mangler skjemafeil-boksen | grensetilfeller | false | Registreringen lager aldri feil med `felt=None`, så boksen trengs ikke | avvist |

## Design Notes

Makrofilen importeres med `{% from "skjemafelt.html" import felt %}`. `felt` får `hjelp=None`: når den finnes, lages `<p class="hjelpetekst" id="{navn}-hjelp">`, og `aria-describedby` blir `"{navn}-hjelp {navn}-feil"` (eller bare den som finnes). Fokus regnes ut som i `_vis_logg_inn`, så en felles hjelper i `ruter.py` kan brukes av begge sidene.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alle tester grønne
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Kristine registrerer en ny bruker, prøver feilene (tomt, `ola@`, kort passord, ulike passord, `test@example.com`) og logger inn med den nye brukeren.
