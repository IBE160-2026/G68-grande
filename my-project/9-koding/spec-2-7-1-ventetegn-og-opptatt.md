---
title: 'Story 2.7.1: Ventetegn og «opptatt»'
type: 'feature'
created: '2026-11-10'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'f18e9f2e5ff0346b0a73722802d7cd885c1429a7'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Etter «Sjekk CV-en min» skjer det ingenting synlig før svaret kommer, så brukeren kan trykke flere ganger og starte flere KI-kall (FR-27).

**Approach:** Et ventetegn som dekker siden og sperrer resten mens serveren jobber, og `opptatt` på serveren rundt KI-kallene. Den ferdige KI-feilboksen med «Prøv på nytt» er story 2.7.2.

## Boundaries & Constraints

**Always:**
- Ventetegnet vises når «Sjekk CV-en min» trykkes: tre prikker (16 px, hopper 14 px, 1 s, 0,15 s forsinkelse, farger `--primary`, `--dot-middle`, `--accent`), «På vei mot ny jobb» i Baloo 2 og «Vi sjekker CV-en din – det tar noen sekunder.». Bakgrunnen er `--background` med 94 %. Prikkene står stille ved `prefers-reduced-motion`.
- Mens man venter: resten av siden er `inert`, også topplinjen og hjørneraden. Knappen som ble trykket, får `aria-disabled="true"` og beholder fokus. Et nytt trykk sender ingenting. Ventesetningen skrives i et `role="status"`-område som finnes på siden hele tiden.
- Etterpå: resultatsiden gir fokus til `h1`. KI-feil gir fokus til feilboksen (som i dag).
- Serveren: POST på innleggingen ser først etter `opptatt`. Er den sann, sendes brukeren til siden for steget uten at noe lagres eller KI-en kalles. Ellers settes `opptatt` før KI-kallene og tas bort etterpå, også når kallet feiler med `KIFeil` eller et annet unntak.
- Tekstene i `web/tekster.py`, ordrett fra EXPERIENCE.

**Never:**
- Ikke «Det du har lagt inn, er ikke borte.» eller «Prøv på nytt» (2.7.2), ikke avbryt-knapp (ingen i versjon 1), ikke ventetekst for brevet (Epic 3).
- Ikke `disabled` på knappen (da mister den fokus), ikke `style=` i malene og ikke faste `height:` i CSS.
- JavaScript endrer aldri søknadsdata. Skriptet for ventetegnet lastes bare på sider med KI-kall.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Vellykket | case 1, «Sjekk CV-en min» | redirect til `/resultat`, `opptatt` usann etterpå | – |
| Under kallet | KI-kallet pågår | `opptatt` er sann i øktlageret | – |
| Ny POST | `opptatt` sann, steg innlegging | 302 til `/innlegging`, ingen KI-kall, søknaden uendret | – |
| KI-feil | `KIFeil` fra KI-en | samme side (200) som i dag, `opptatt` usann | – |
| Uventet feil | KI-en kaster `RuntimeError` | `opptatt` er usann etterpå | unntaket går videre |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/okt.py` -- nytt `sett_opptatt(soknad, opptatt)` med `replace`, som de andre endringsfunksjonene. Feltet `opptatt` finnes alt.
- `backend/soknad/web/ruter.py` -- `innlegging()`: sjekk `opptatt` først i POST (før `sett_inndata`), redirect med `SIDE_FOR_STEG` fra `web/flyt.py`. `finally` rundt de to KI-kallene. Kommentaren om story 2.7 fjernes.
- `backend/soknad/web/tekster.py` -- `VENTE_OVERSKRIFT`, `VENTE_SJEKKER`.
- `backend/soknad/web/templates/base.html` -- ny `{% block ventetegn %}` etter `<footer>`, utenfor `main`.
- `backend/soknad/web/templates/ventetegn.html` -- nytt: statusområdet og ventetegnet (`hidden`) i én beholder, som ikke gjøres `inert`. Prikkene `aria-hidden`.
- `backend/soknad/web/templates/innlegging.html` -- «Sjekk CV-en min» får `data-vente` med ventesetningen. `vente.js` i `{% block skript %}`, `ventetegn.html` i den nye blokken.
- `backend/soknad/web/templates/resultat.html` -- `h1` får `tabindex="-1"` og `autofocus`.
- `backend/soknad/web/static/js/vente.js` -- nytt: lytter på `submit`, bare når `submitter` har `data-vente`. Gjør søsknene til hver forelder fra knappen opp til `body` `inert`, unntatt ventebeholderen. `tilbake.js` laster siden på nytt ved «Tilbake» i nettleseren, så ventetegnet blir ikke stående.
- `backend/soknad/web/static/css/stil.css` -- `.ventetegn` (`position: fixed`, over hjørneraden, som har `z-index: 1`), prikkene med `min-width`/`min-height`, `@keyframes`, og regler i `prefers-reduced-motion` og `forced-colors`. 94 % med `color-mix` (fargekoder bare i `:root`). `@font-face` for Baloo 2 og `--font-logo` finnes.
- `backend/tests/web/hjelpere.py` -- `FeilendeKI` kan få en spion som leser `opptatt` under kallet, og et vilkårlig unntak.
- `backend/tests/web/test_ruter.py` -- startsiden skal fortsatt bare ha `tilbake.js`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/okt.py` og `tests/kjerne/test_okt.py` -- `sett_opptatt` med test.
- [x] `backend/soknad/web/tekster.py` og `ruter.py` -- tekstene og `opptatt` i POST.
- [x] `backend/soknad/web/templates/` (base, ventetegn, innlegging, resultat) -- ventetegnet og fokus.
- [x] `backend/soknad/web/static/js/vente.js` og `css/stil.css` -- sperringen og utseendet.
- [x] `backend/tests/web/test_innlegging.py` og `hjelpere.py` -- én test per rad i matrisen, prikkene `aria-hidden`, statusområdet, `data-vente` bare på «Sjekk CV-en min», `vente.js` bare på innleggingen, `h1` med fokus på resultatsiden, kildetekst-sjekk av `vente.js` (`inert`, `aria-disabled`, ingen `disabled`, ingen `fetch`) og CSS for redusert bevegelse. FR-nummer i navn og docstring.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (389 før denne storyen), og `ruff check` og `ruff format --check` har ingen feil.
- Given case 1 i nettleseren, when «Sjekk CV-en min» trykkes, then vises ventetegnet som i skissen `input-page-1.html`, og Tab kommer ikke ut av knappen.

## Implementation Notes

- Branch: `story/2-7-1-ventetegn-og-opptatt`.
- Hovedøkta skrev koden selv (ingen hjelpeagent), som i story 2.3–2.6.
- Testene ligger i en ny fil, `tests/web/test_ventetegn.py`, i stedet for i `test_innlegging.py`, med en egen `SpionKI` som ser `opptatt` under kallet. `hjelpere.py` er ikke endret. I `test_innlegging.py` ble bare mønsteret for «Sjekk CV-en min» endret, fordi knappen nå har `data-vente`.
- Bakgrunnen bruker tokenet `--wait-cover`, som alt fantes i `:root` med 94 %, i stedet for `color-mix`.
- `ruter.py` henter søknaden én gang i POST (`lagret`) og bruker den både til `opptatt`-sjekken, 400-svaret og `sett_inndata`.
- Prikkene i høykontrastmodus: `forced-color-adjust: none` og `CanvasText`, med `:nth-child(n)` så regelen slår fargene for prikk 2 og 3.
- Tester: 32 nye, 421 i alt, `ruff` grønn. Nettleser-kriteriet sjekker Kristine for hånd (Manual checks).
- Etter gjennomgangen bestemte Kristine (2026-11-10) at overskriften på resultatsiden ikke skal ha fokusring: `.side-overskrift[tabindex="-1"]:focus { outline: none; }` og en ny test (422 i alt). Commit `aaa4549`.
## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-10), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Ingen test kjører `vente.js`, bare tekstsøk i fila (dobbelttrykk, at ventetegnet ikke blir inert, at bare knapper med `data-vente` viser det) | testhull, blind | medium | Riktig, samme hull som for `innlegging.js` og `info.js`. Prosjektet har ingen nettlesertester. Sjekkes for hånd i PR-en | utsatt |
| 2 | `opptatt` sjekkes og settes ikke i én låst operasjon, så to POST-er samtidig kan begge starte KI-kall | grensetilfeller, blind | low | Riktig, men krever to innsendinger fra to faner innen noen millisekunder, og skriptet stopper dobbelttrykk. Valgt i Design Notes | avvist |
| 3 | En annen fane som endrer søknaden under kallet, blir skrevet over av `finally` | grensetilfeller, blind | low | Riktig, men valgt i Design Notes. Krever at brukeren går til startsiden i en annen fane mens kallet pågår | avvist |
| 4 | `SIDE_FOR_STEG[Steg.BREV]` finnes ikke og gir 500 | grensetilfeller | false | Ingenting setter steget til brev før Epic 3, og `krever_steg` slår opp på samme måte | avvist |
| 5 | En POST som stoppes av `opptatt`, sender tilbake til innleggingen uten melding | grensetilfeller, blind | low | Riktig, men skjer bare uten JavaScript, med to faner eller F5 midt i kallet. En melding trenger ny tekst fra EXPERIENCE | avvist |
| 6 | Henger KI-kallet, blir søknaden stående opptatt | grensetilfeller, blind | false | `TestKI` leser lokale filer og kan ikke henge. Stopper serveren, forsvinner øktlageret i minnet. Ekte KI får tidsgrense i Epic 4 (AD-13) | avvist |
| 7 | Stoppes lastingen med Esc, blir ventetegnet og `inert` stående | grensetilfeller, blind | low | Riktig, men sjeldent, og F5 løser det. En tilbakestilling trenger tidsur eller nye lyttere | avvist |
| 8 | Testene ligger i `test_ventetegn.py`, ikke i `test_innlegging.py` som Tasks sier | grensetilfeller | low | Riktig, og står i Implementation Notes. Rettingen ville vært å endre spec-en | avvist |
| 9 | Ved vellykket kall lagres søknaden to ganger, og mellom dem er den verken opptatt eller ferdig | blind | low | Riktig. `finally` lagrer nå bare én gang, med analysen når kallene lyktes | patch |
| 10 | `vente.js` sjekker bare at `#vente` finnes, ikke de andre elementene | blind | false | Alle fire står i samme `ventetegn.html`, som tas med i én blokk | avvist |
| 11 | Sjekken på ordet `location` er for bred | blind | low | Riktig, samme funn som #12 i 2.6. Den nye testen ser nå bare etter bruk (`location.`, `location =`) | patch |
| 12 | Overskriften med `autofocus` kan få fokusringen hver gang resultatsiden åpnes | blind | maybe-false | Avhenger av nettleseren. Sjekkes i nettleseren. Feilboksen har samme mønster, og en ring på overskriften er bare kosmetisk | avvist |
| 13 | Skjermlesere kan høre ventesetningen to ganger og hører ikke «På vei mot ny jobb» | blind | low | Statusområdet får ventesetningen, som EXPERIENCE sier. To ganger bare når man blar i de få sekundene man venter | avvist |
| 14 | Docstringen til `SpionKI` sier «det første kallet», men unntaket kastes fra hvert kall | blind | low | Riktig. Docstringen rettet | patch |
| 15 | Ingen test for andre ruter (`/`, `/modus`) mens `opptatt` er sann | blind | low | De sjekker ikke `opptatt` med vilje (funn #3). Utfallet ved KI-feil er testet | avvist |

## Design Notes

- `inert` på hele `main` ville tatt fokuset fra knappen. Derfor sperres bare søsknene langs veien fra knappen til `body`.
- `opptatt` sjekkes og settes uten lås. Tiden mellom er svært kort, og skriptet stopper dobbelttrykk i nettleseren.
- Går brukeren til startsiden i en annen fane mens kallet pågår, skriver `finally` den gamle søknaden tilbake. Det godtas.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Case 1: ventetegnet dekker siden, også hjørneraden. Svaret fra testdataene kommer fort, så sett tregere nettverk i F12 (Network › «Slow 4G») for å rekke å se det. Tab og Shift+Tab blir på knappen, «Logg ut» kan ikke trykkes. Etterpå har overskriften på resultatsiden fokus.
- Redusert bevegelse slått på i Windows (Innstillinger › Tilgjengelighet › Visuelle effekter › Animasjonseffekter av): prikkene står stille.
- 320 px og 200 % zoom: ventetegnet får plass uten rulling sidelengs.
