---
title: 'Story 2.6: Hele resultatsiden med forklaringer og «Tilbake»'
type: 'feature'
created: '2026-11-10'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '5fce6df6fb457b03b375a4918f3323f54ff1eb66'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Resultatsiden fra 2.5.2 viser bare listene og prosenten. Brukeren får ikke vite hva gap-analysen og nøkkelordtreffet betyr, ser ikke hvilke nøkkelord som mangler, og kan ikke gå tilbake og endre teksten (FR-14–FR-19).

**Approach:** Gjør ferdig resultatsiden etter EXPERIENCE og DESIGN: «i»-ikoner, «Laget av KI», undertekst, fargede gap-lister, FR-18-linjen, nøkkelordlistene med prosentlinje, ATS-forklaringen som foldes ut, tekster for tomme lister og «Tilbake» til innleggingen.

## Boundaries & Constraints

**Always:**
- Rekkefølge i `main`: `h1`, gap-analysen, FR-18-linjen, nøkkelordtreffet, ATS-forklaringen, knapperaden med «Tilbake».
- `h2` «Gap-analyse» med «i»-knapp og merket «Laget av KI» ved siden av (ikke inne i overskriften), undertekst «Kravene fra annonsen, sammenlignet med CV-en din.», `h3`-listene «Dette dekker CV-en din» (grønn, ✓) og «Dette kan du jobbe videre med» (`work-on-tint`, →, aldri rød).
- `h2` «Nøkkelordtreff» med «i»-knapp, «X av Y = Z %» stort med «av nøkkelordene står i CV-en din», prosentlinje (12 px, `aria-hidden`, uten animasjon) og `h3` «Står i CV-en (antall)» med ✓ og «Står ikke i CV-en (antall)» med ○. Listene kommer fra `tell_treff` (`treff`, `ikke_treff`), bare visning.
- ATS-forklaringen er `<details>`/`<summary>` «Hva er ATS og hva betyr det for deg?», lukket når siden åpnes.
- «i»-knappen: `aria-label` «Hva er en gap-analyse?» / «Hva er nøkkelordtreff?», `aria-expanded`, `aria-controls`, boksen rett etter knappen. Trykk, Enter og mellomrom åpner og lukker, Esc lukker, hover med mus åpner og holder åpen over ikon og boks. Fokus alene åpner ikke.
- Tomme lister viser tekstene fra EXPERIENCE i stedet for listen (🎉 skjult for skjermlesere).
- Ikoner som bare er pynt (✓ → ○ 🎉 og «i»-bokstaven), er skjult for skjermlesere.
- Gap-listene og nøkkelordlistene står side om side fra 700 px. Ingen rulling sidelengs ved 320–1280 px og 200 % zoom.
- «Tilbake» er en sekundærknapp nederst til venstre, en lenke til `/innlegging` (som på modusvalget). Feltene er fylt ut der.
- Alle tekster i `web/tekster.py`, tekstene ordrett fra EXPERIENCE.

**Never:**
- Ikke «Lag søknadsbrevet mitt» (story 3.1), ventetegn eller «Prøv på nytt» (2.7), animasjon i prosentlinjen (Epic 7) eller gjenbruk av nøkkelordlisten (story 7.3).
- Ikke endre `kjerne/` eller `adaptere/`. JavaScript endrer aldri søknadsdata.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Case 1 | analysen fra case 1 | listene fra `gap.json`, «Står i CV-en (7)» og «Står ikke i CV-en (4)» som i `fasit.md`, 64 % | – |
| Tom «dekker» | `gap.dekker == []` | «CV-en din dekker ingen av kravene ennå. Se hva du kan jobbe videre med.» | – |
| Tom «mangler» | `gap.mangler == []` | «Bra jobbet! CV-en din dekker alle kravene i annonsen. 🎉» | – |
| Ingen treff | ingen nøkkelord i CV-en | «Står i CV-en (0)» med «Ingen av nøkkelordene står i CV-en ennå.», 0 % | – |
| Alle treff | alle nøkkelord i CV-en | «Står ikke i CV-en (0)» med «Alle nøkkelordene står i CV-en din!», 100 % | – |
| Tilbake og videre | case 1, «Tilbake», «Sjekk CV-en min» med samme tekst | feltene fylt ut, samme nøkkelordtreff (kriterium 8) | – |
| Tilbake og endre | «Tilbake», endret CV, «Tilbake» til modusvalget | steg innlegging, `/resultat` sender til `/innlegging` | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/ruter.py` -- `resultat()`: send også `treff` (hele `Nokkelordtreff`) og prosenten til malen. Ellers uendret.
- `backend/soknad/web/tekster.py` -- nye tekster under `RESULTAT_*`/`GAP_*`: undertekst, «Laget av KI», «i»-tekstene og skjermlesertekstene, FR-18-linjen, «av nøkkelordene står i CV-en din», funksjoner for «Står i CV-en (n)» og «Står ikke i CV-en (n)», ATS-overskrift og to avsnitt, fire tekster for tomme lister. `TILBAKE_KNAPP` finnes.
- `backend/soknad/web/templates/resultat.html` -- bygges ut. Behold `id="gap-dekker"`, `id="gap-mangler"` og `id="nokkelordtreff"` (på elementet med «X av Y = Z %»). Nye id-er `nokkelord-treff`, `nokkelord-ikke-treff`.
- `backend/soknad/web/static/js/info.js` -- nytt, generelt for alle `.info`-knapper (startsiden gjenbruker det i Epic 4). Lastes i `{% block skript %}`.
- `backend/soknad/web/static/css/stil.css` -- klasser for `info-icon`, `info-tip`, `ai-tag`, `gap-covers`, `gap-work-on`, `score-meter`, nøkkelordlister og `details`. Bruk tokenene som finnes (`--success-tint`, `--work-on`, `--work-on-tint`, `--accent`, `--size-score`, `--rounded-*`). Følg mønstrene for `forced-colors` og `prefers-reduced-motion`. `.knapperad` og `.sekundaerknapp` finnes.
- `backend/tests/web/test_resultat.py` -- helperne `liste()` og `nokkelordtreff()` må tåle `<span aria-hidden>` i punktene. Tomme lister lages med `sett_soknad` og egen `gap`/`nokkelord` (som `test_fr17_prosenten_regnes_fra_den_lagrede_listen`), ikke i `testdata/`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/web/tekster.py` og `ruter.py` -- tekstene og `treff` til malen.
- [x] `backend/soknad/web/templates/resultat.html` -- hele siden som i Always.
- [x] `backend/soknad/web/static/js/info.js` og `css/stil.css` -- «i»-boksen og utseendet.
- [x] `backend/tests/web/test_resultat.py` -- én test per rad i matrisen, rekkefølgen, `aria-*` på «i»-knappene, `<details>` uten `open`, pynt med `aria-hidden`, at «Tilbake» lenker til `/innlegging`, at alle nye tekster ligger i `tekster.py`, og kildetekst-sjekk av `info.js` (Escape, `aria-expanded`, ingen `focus`-lytter som åpner). FR-nummer i navn og docstring.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (361 før denne storyen), og `ruff check` og `ruff format --check` har ingen feil.
- Given testdataene fra case 1 i nettleseren, when resultatsiden vises, then ser den ut som skissen `result-page-1.html` (Full generering), og «i»-boksene virker med mus, tastatur og trykk.

## Implementation Notes

- Branch: `story/2-6-hele-resultatsiden-med-forklaringer-og-tilbake`.
- Hovedøkta skrev koden selv (ingen hjelpeagent), som i story 2.3–2.5.2.
- Prosentlinjen ble en SVG i stedet for `<div>` med `style=`, fordi to prosjekttester stoppet `style=` i malene og `height:` i CSS. «i»-knappen bruker `min-width`/`min-height: 24px` av samme grunn.
- `info.js`: et trykk på en boks som er åpnet med hover, fester den (den lukkes ikke når musa går ut). Et nytt trykk eller Esc lukker. Uten dette ville et museklikk lukke boksen som hover nettopp åpnet. Musa har 200 ms til å gå fra knappen til boksen.
- «i»-boksen legges under raden med overskriften, fra venstre kant, med bredde `min(300px, 100%)`, så den aldri går utenfor siden på mobil.
- «Laget av KI» bruker klassen `merkelapp`, som merkelappen «Testmodus» (samme farger i DESIGN).
- Tomme lister er en `<p class="tom-liste">` med samme id som listen. Testhjelperen `liste()` gir `[]` for dem, og `tom_tekst()` gir teksten.
- Kristine fant i nettleseren at prosentlinjen var ca. 120 px høy: `svg { height: auto }` i den felles stilen overstyrte `height="12"`. `min-height`/`max-height: 12px` på `.prosentlinje` og en ny test.
- Tester: 28 nye, 389 i alt, `ruff` grønn.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-10), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Ingen test kjører `info.js`, bare tekstsøk i fila | testhull, blind | low | Riktig, samme hull som for `innlegging.js`. Prosjektet har ingen nettlesertester. Sjekkes for hånd i PR-en | utsatt |
| 2 | Testen sjekker ikke klassene `info` og `info-knapp`, som `info.js` leter etter | testhull | low | Riktig. Testen sjekker nå begge | patch |
| 3 | Punkter med bare mellomrom gir et tomt ✓-punkt i stedet for teksten for tom liste | grensetilfeller | low | Riktig, men samme funn som #4 i 2.5.2 (`ki_svar.kontroller`), og kan ikke skje med testdataene | utsatt |
| 4 | Uten JavaScript kan «i»-teksten ikke leses | grensetilfeller, blind | low | Riktig, men nettsiden krever vanlig nettleser, og å vise boksen fra serveren gir et blink før skriptet skjuler den | avvist |
| 5 | `info.js` krasjer hvis knappen eller boksen mangler | grensetilfeller | false | Makroen lager alltid knappen og boksen med samme id | avvist |
| 6 | Et langt ord uten bindestrek gjør siden bredere ved 320 px | grensetilfeller | medium | Riktig: `overflow-wrap: break-word` teller ikke i flex-punktet, og norske sammensatte ord kan bli lange. `overflow-wrap: anywhere` lagt til | patch |
| 7 | En boks åpnet med trykk blir liggende over listene til «i» trykkes igjen (ingen Esc på mobil) | grensetilfeller, blind | low | Riktig, og møtes hver gang på mobil. Et trykk utenfor lukker nå boksen | patch |
| 8 | ✓, → og ○ står i malen, ikke i `tekster.py` | grensetilfeller | low | Riktig. Flyttet til `tekster.py` | patch |
| 9 | Et klikk på en boks åpnet med hover lukker den ikke | blind | low | Valgt med vilje (Implementation Notes): ellers ville klikket på «i» lukke boksen hover nettopp åpnet | avvist |
| 10 | Boksen står under overskriften, så musa må krysse `h2` og rekker ikke fram på 200 ms | blind | false | Boksen går fra venstre kant og 300 px bort, så den ligger rett under «i»-knappen, og veien ned går ikke over `h2` | avvist |
| 11 | ATS-overskriften har nettleserens ▸ til venstre, ikke ▾ til høyre som i DESIGN | blind | low | Riktig. ▾ til høyre, snur seg når den er åpen, skjult for skjermlesere | patch |
| 12 | Forbudt-ord-sjekken på `"location"` er for bred | blind | low | Riktig, men slår bare til ved en kommentar med ordet, og samme sjekk brukes for `innlegging.js` | avvist |
| 13 | ATS-testen sammenligner koden med seg selv | blind | low | Riktig. Begge avsnittene sjekkes nå ordrett mot EXPERIENCE | patch |
| 14 | Antallet i listeoverskriftene og i «X av Y» kommer fra to kilder | blind | false | `tell_treff` setter `antall_treff = len(treff)` og `antall = len(treff) + len(ikke_treff)`, så de kan ikke bli ulike | avvist |
| 15 | Gap-boksene mister bakgrunnen og har ingen kant i høykontrastmodus | blind | low | Riktig. Ramme i `forced-colors` lagt til | patch |

## Design Notes

- Hover styres i `info.js` med `pointerenter`/`pointerleave` (bare `pointerType === "mouse"`), ikke med CSS `:hover`, så `aria-expanded` stemmer og Esc også lukker en boks åpnet med hover.
- Boksen har `hidden` i HTML-en. Uten JavaScript vises den ikke, men resten av siden virker.
- Prosentlinjen er en SVG (`viewBox="0 0 100 12"`, `height="12"`, `aria-hidden`) med to `rect`, der fyllet har `width="{{ prosent }}"`. Prosjektet forbyr `style=` i malene og faste høyder i CSS (testene i `test_ruter.py`), så bredden og høyden står som SVG-attributter.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Case 1 i nettleseren: rekkefølgen, fargene, «7 av 11 = 64 %» og nøkkelordlistene. «i» med mus (hover), trykk, Enter, mellomrom og Esc. ATS-forklaringen lukket, åpnes med Enter.
- «Tilbake»: feltene fylt ut. «Sjekk CV-en min» igjen: samme prosent.
- 320 px, 375 px og 200 % zoom: ingenting ruller sidelengs, listene under hverandre under 700 px.
