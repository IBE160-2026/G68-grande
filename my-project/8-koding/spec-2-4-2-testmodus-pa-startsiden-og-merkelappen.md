---
title: 'Story 2.4.2: Testmodus på startsiden og merkelappen'
type: 'feature'
created: '2026-11-09'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'beef26a808af213e42f0cc47c3c52c8c7766a963'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nettsiden er alltid i testmodus, men det står ingen steder. Sensor ser ikke at ingenting sendes til ekstern KI, og får ikke vite at API-nøkkelen mangler (FR-32, FR-33).

**Approach:** Startsiden får bryteren «Testmodus» oppe til høyre, «Mangler API-nøkkel, se README» når nøkkelen mangler, og teksten om testmodus i et statusområde. Alle andre sider etter innlogging får merkelappen «Testmodus» oppe til høyre fra `base.html`. Dette er andre halvdel av story 2.4.

## Boundaries & Constraints

**Always:**
- Bryteren: `<button type="button" role="switch" aria-checked="true" aria-disabled="true">` med synlig etikett «Testmodus» inne i knappen, i `header` oppe til høyre. Den står ikke i noe skjema og gjør ingenting når den trykkes. Den kan nås med Tab.
- Bryteren er slått på og låst fram til Epic 4, også når API-nøkkelen finnes. `aria-checked` kommer fra `Innlogging.testmodus`.
- «Mangler API-nøkkel, se README» står under bryteren og er koblet med `aria-describedby`, bare når `ANTHROPIC_API_KEY` er tom eller bare mellomrom. Med nøkkel finnes verken teksten eller `aria-describedby`.
- «Du er i testmodus. Nettsiden bruker ferdige svar, og ingenting sendes til ekstern KI.» står i et `role="status"`-område på startsiden, mellom ingressen og «Begynn å lage søknad». Området finnes alltid, men har teksten bare når testmodus er på.
- Merkelappen «Testmodus» (`accent`-bakgrunn, `text`-farge, `rounded-sm`, `size-tag`, vekt 600) står oppe til høyre på alle innloggede sider unntatt startsiden, når `Innlogging.testmodus` er sann. Den er bare tekst, ikke en knapp eller lenke.
- Låst bryter: sporet er 60 % synlig (som skissen), etiketten har full farge. Sporet 44 × 24 px, i `primary` når på.
- Ingen `nowrap` og ingen faste høyder på tekst. Alle nye tekster i `web/tekster.py`.

**Never:**
- Bryteren kan ikke slås av, og det er ingen rute eller JavaScript som endrer testmodus (Epic 4).
- Ingen samtykke og ingen KI-merknad (Epic 4).
- Innloggingen og registreringen får verken bryter eller merkelapp.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Uten nøkkel | `ANTHROPIC_API_KEY=""`, GET `/` | bryter på og låst, «Mangler API-nøkkel, se README» med `aria-describedby`, statusteksten | – |
| Med nøkkel | `ANTHROPIC_API_KEY="sk-test"`, GET `/` | bryter på og låst, ingen nøkkeltekst, ingen `aria-describedby`, statusteksten | – |
| Bare mellomrom | `ANTHROPIC_API_KEY="  "`, GET `/` | som uten nøkkel | – |
| Andre sider | GET `/modus` og `/innlegging` | merkelappen «Testmodus» i `header`, ingen bryter | – |
| Startsiden | GET `/` | ingen merkelapp | – |
| Utlogget | GET `/logg-inn` og `/registrer` | verken bryter, merkelapp eller statustekst | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/templates/base.html` -- `header.topp` har bare logoen. Legg en rad oppe til høyre før logoen, bare når `innlogget`, med en `{% block topplinje %}` som viser merkelappen.
- `backend/soknad/web/templates/start.html` -- overstyrer `topplinje` med bryteren. Statusområdet før skjemaet `begynn`.
- `backend/soknad/web/ruter.py` -- `felles_tekster()` gir `innlogget`; legg til `testmodus`. `start()` (GET) sender `mangler_nokkel` fra `current_app.config["ANTHROPIC_API_KEY"]`.
- `backend/soknad/__init__.py` -- `ANTHROPIC_API_KEY` er alt i config (tom streng uten nøkkel). Ikke endre.
- `backend/soknad/web/tekster.py` -- `TESTMODUS`, `TESTMODUS_STATUS`, `MANGLER_NOKKEL`.
- `backend/soknad/web/static/css/stil.css` -- tokens finnes alt (`--accent`, `--size-tag`, `--rounded-sm`). Bryterens CSS fra skissen `mockups/start-page-1.html` (`.toggle`, `.track`, `.nokey`), skrevet om til en knapp.
- `backend/tests/web/test_startside.py`, `test_modusvalg.py`, `test_ruter.py` -- legg til tester. Gjenbruk `tagger_i` og `STIL` fra `hjelpere.py`. `conftest.py` tømmer `ANTHROPIC_API_KEY`; testen med nøkkel lager sin egen app med `create_app({... "ANTHROPIC_API_KEY": "sk-test"})`.
- Ikke endre: `innlogging.py` (testmodus settes alt til `True` ved innlogging), `okt.py`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/web/tekster.py` -- tre nye tekster.
- [x] `backend/soknad/web/ruter.py` -- `testmodus` i `felles_tekster`, `mangler_nokkel` i `start()`.
- [x] `backend/soknad/web/templates/base.html` og `start.html` -- rad oppe til høyre, merkelapp, bryter, nøkkeltekst og statusområde.
- [x] `backend/soknad/web/static/css/stil.css` -- `.topplinje` (flex, høyre, brytes), `.bryter` med spor og knott, låst spor 60 %, `.nokkeltekst` (`size-caption`, `text-muted`, hele bredden, høyrestilt), `.merkelapp`, `.testinfo`. Knotten flyttes uten overgang ved `prefers-reduced-motion` (dekkes av regelen som finnes).
- [x] Tester -- én test per rad i matrisen, og at bryteren ikke står i et skjema, at statusområdet har `role="status"`, og CSS-en (60 %, `var(--accent)`, ingen `nowrap`). FR-nummer i navn og docstring.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (272 før denne storyen).
- Given `ruff check` og `ruff format --check`, when de kjører, then er det ingen feil.
- Given startsiden uten API-nøkkel, when jeg trykker Tab, then får bryteren fokusring, og et trykk på den endrer ingenting.

## Implementation Notes

- Branch: `story/2-4-2-testmodus-pa-startsiden-og-merkelappen`.
- Hovedøkta skrev koden selv (ingen hjelpeagent), som i story 2.3 og 2.4.1.
- Testene står i én ny fil, `tests/web/test_testmodus.py`, i stedet for spredt på tre filer. Da ligger alt om testmodus på ett sted.
- Sporet og knotten bruker `aspect-ratio` i stedet for `height`, fordi en test fra før (`test_nfr7_…`) ikke tillater faste høyder i CSS-en. Størrelsen er den samme (44 × 24 og 18 × 18 px).
- Skyggen på knotten er et nytt token, `--shadow-knob`, fordi fargekoder bare får stå i `:root`.
- Teksten om testmodus står i et hvitt kort, som i skissen. Er området tomt, har det verken ramme eller skygge.
- Testen for testmodus av bytter innloggingen direkte i `_innlogginger`, fordi testmodus ikke kan slås av før Epic 4.
- Tester: 16 nye, 288 i alt (etter gjennomgangen), `ruff` grønn. Bredder i nettleseren er ikke sjekket av hovedøkta. Det gjøres i gjennomgangen sammen med Kristine.
## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-09), tre lag: blind, grensetilfeller, testhull. Testhull-laget fant ingen hull i det som er testet.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | `.strip()` feiler hvis `ANTHROPIC_API_KEY` er et tall eller `True` | grensetilfeller | false | Verdien kommer bare fra miljøet eller `.env` (alltid tekst), eller er tom. Ingen kode setter noe annet | avvist |
| 2 | Logges man ut i en annen fane midt i en forespørsel, vises siden uten bryter, merkelapp og «Logg ut» | grensetilfeller | low | Riktig, men krever to forespørsler på nesten samme tid. `innlogget` har virket slik siden Epic 1, og rettingen er ny kode i `login_required` | avvist |
| 3 | Med testmodus av (Epic 4) blir raden oppe til høyre tom, men tar fortsatt litt plass | grensetilfeller, blind | low | Riktig, men testmodus kan ikke slås av før Epic 4. Epic 4 må se på det når bryteren kan slås av | avvist |
| 4 | Testen for testmodus av sjekker ikke at `/modus` svarer 200 | testhull | low | Riktig. Sjekker nå status 200 og at raden finnes | patch |
| 5 | Sporet og knotten forsvinner i Windows' høykontrastmodus | blind | low | Riktig, bakgrunn og skygge fjernes der. Sporet har nå ramme og knotten `CanvasText` i `@media (forced-colors: active)`, med test | patch |
| 6 | Logoen flytter seg litt mellom innloggingen, startsiden og de andre sidene | blind | low | Riktig, raden er ulikt høy. Sidene har ulikt innhold, og forskjellen er noen få piksler | avvist |
| 7 | Kommentaren om statusområdet lover at teksten leses opp når den kommer | blind | low | Riktig, teksten kommer med siden. Kommentaren er skrevet om | patch |
| 8 | Testen skriver rett i `_innlogginger` uten lås | blind | low | Riktig. Ny hjelper `sett_testmodus` i `hjelpere.py` bruker øktlagerets egne metoder. (Samme type funn som #11 i 2.4.1, nå rettet i stedet for avvist) | patch |
| 9 | Testen for at etiketten ikke blekes, ser bare i `.bryter` | blind | low | Riktig. Sjekker nå også `.bryter[aria-disabled="true"]`, og at etiketten har `text`-farge | patch |
| 10 | Vekt 600 på merkelappen og etiketten er ikke testet | blind | low | Riktig. Lagt til | patch |
| 11 | `justify-content`, `.nokkeltekst` og at raden står før logoen er ikke testet | blind | low | Riktig. To tester lagt til | patch |
| 12 | Med API-nøkkel står det ingenting om hvorfor bryteren er låst | blind | low | Bestemt i spec-en: låst uten tekst fram til Epic 4. Sensor har ingen nøkkel og ser «Mangler API-nøkkel, se README» | avvist |
| 13 | Merkelappen forklarer ikke testmodus for skjermlesere på de andre sidene | blind | false | UX sier at merkelappen bare er visning med teksten «Testmodus». Forklaringen står på startsiden, der testmodus velges | avvist |
| 14 | `header()` og `main()` er skrevet på nytt i testfila i stedet for i `hjelpere.py` | blind | low | Riktig. `header`, `main` og `css_blokk` ligger nå i `hjelpere.py`, og `test_modusvalg.py` bruker `main` derfra | patch |

## Design Notes

En blokk i `base.html` gjør at bare startsiden trenger å vite om bryteren. Andre sider får merkelappen uten å gjøre noe:

```jinja
{%- if innlogget %}
<div class="topplinje">
  {%- block topplinje %}{% if testmodus %}<span class="merkelapp">{{ tekster.TESTMODUS }}</span>{% endif %}{% endblock %}
</div>
{%- endif %}
```

Bryteren er en `button` og ikke en avkrysningsboks som i skissen, fordi den ikke skal sende noe før Epic 4, og `aria-disabled` lar den fortsatt nås med Tab.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Uten nøkkel i `backend/.env`: logg inn. Startsiden har bryteren oppe til høyre (på, blek), «Mangler API-nøkkel, se README» under og teksten om testmodus over den store knappen. Tab til bryteren: fokusring. Trykk på den: ingenting skjer.
- Trykk «Begynn å lage søknad»: modusvalget har merkelappen «Testmodus» oppe til høyre og ingen bryter. Det samme på innleggingen.
- Gjør vinduet 320 px og 375 px smalt: ingenting ruller sidelengs, og nøkkelteksten brytes under bryteren.
