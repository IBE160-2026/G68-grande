---
title: 'Story 2.5.1: Innleggingssiden'
type: 'feature'
created: '2026-11-09'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'f389687a3fbc773feb48a3961d4f728e6d8a9f7c'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Innleggingen har bare overskriften. Brukeren kan ikke legge inn CV og annonse, og ingenting sjekker det som legges inn (FR-8, FR-9, FR-13, FR-34).

**Approach:** Innleggingen får feltene «📄 CV» og «📢 Stillingsannonse» med «Lim inn tekst», søppelbøtte, hjelpetekst om testdata, feilboks og knappene «Tilbake» og «Sjekk CV-en min». Dette er første halvdel av story 2.5. Analysen og resultatsiden kommer i 2.5.2. Til da vises innleggingen på nytt, uten feil, når alt er riktig.

## Boundaries & Constraints

**Always:**
- Ett skjema med to tekstbokser (`name="cv"`, `name="annonse"`) og to knapper: `handling=tilbake` («Tilbake», sekundær, til venstre) og `handling=sjekk` («Sjekk CV-en min», hoved).
- Et tomt felt viser bare «Lim inn tekst». Et felt med tekst viser tekstboksen med «Lim inn teksten her» og søppelbøtta over. JavaScript bytter mellom de to uten å spørre serveren.
- Skjermlesertekster: «Lim inn tekst, CV», tekstboksen «CV: Lim inn teksten her», søppelbøtta «Tøm CV-feltet», etter tømming «CV-feltet er tømt» i et `role="status"`-område (tilsvarende for Stillingsannonse). Søppelbøtta er minst 24 × 24 px og har fokusring. Ikonene er `aria-hidden`.
- I testmodus står «Testmodus: bruk filene i mappen testdata/ i prosjektet.» over feltene, i en boks med stiplet ramme.
- «Sjekk CV-en min» lagrer feltene med `sett_inndata` og sjekker så alle feltene samtidig: tomt (også bare mellomrom) først, så `ikke_testdata` i testmodus. Det brukeren skrev, står fortsatt i feltene, også ved feil.
- Feilboksen øverst: «Noe må fikses før du kan gå videre:», `tabindex="-1"` og `autofocus`, ikke `role="alert"`. Hver feil er en lenke til feltet. Feltet får rød ramme, tekstboksen `aria-invalid="true"`, og feilteksten står under feltnavnet, koblet med `aria-describedby` til knappen og tekstboksen.
- «Tilbake» lagrer feltene med `sett_inndata` uten å sjekke dem og sender til modusvalget.
- `sett_inndata` endrer ingenting når begge tekstene er like. Ellers lagres tekstene, `nokkelord`, `nokkelord_annonse`, `arbeidsgiver` og `gap` nullstilles, og steget blir høyst innlegging.
- Feltene står side om side fra 1000 px. Tekstboksen kan dras større, `min-height` ca. 160 px (200 px under 700 px). Ingen `nowrap` og ingen faste høyder.
- Alle nye tekster i `web/tekster.py`. CV og annonse ligger bare i øktlageret i minnet.

**Never:**
- Ingen KI-kall, ingen resultatside og ingen redirect ved riktig innlegging (2.5.2).
- Ingen «Last opp PDF» og ingen PDF-tips (Epic 6). Ingen Korrektur-felt (Epic 5). Ikke ventetegn (2.7).
- JavaScript sender aldri noe til serveren.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Begge tomme | `""` og `"  \n"`, `handling=sjekk` | samme side, to feil, CV først | – |
| Ikke testdata | egen CV, riktig annonse | «CV: I testmodus fungerer bare testdataene …», annonsen står igjen | – |
| Tom og feil | tom CV, egen annonse | `tom` på CV og `ikke_testdata` på annonsen | – |
| Riktig | `cv.txt` og `annonse.txt` fra case 1 | samme side uten feilboks, tekstene lagret i søknaden | – |
| Tilbake | egen tekst i begge, `handling=tilbake` | 302 til `/modus`, ingen feil, GET `/innlegging` viser tekstene | – |
| Uendret | samme tekster sendes på nytt | søknaden er den samme (også `nokkelord` og steget) | – |
| Endret | steg resultat med `gap` og `nokkelord`, ny CV | nullstilt, steget blir innlegging | – |
| Ukjent handling | `handling=noe` | 400, søknaden uendret | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/okt.py` -- `sett_inndata(soknad, *, cv: Tekstfelt, annonse: Tekstfelt)`. `velg_modus` og `begynn` endres ikke.
- `backend/soknad/kjerne/inndata.py` -- `sjekk_innlegging(cv, annonse, caser: list[Testcase] | None) -> list[InndataFeil]`. Tom først per felt, så `finn_case` (som alt hopper over tomme felt) når `caser` ikke er `None`. Sortert cv, annonse.
- `backend/soknad/__init__.py` -- `app.extensions["test_ki"] = TestKI()` (leser testdataene én gang). `adaptere/ki.py` endres ikke.
- `backend/soknad/web/flyt.py` -- `ki()` som gir `test_ki`. Ruten bruker `ki().caser` når `Innlogging.testmodus` er sann, ellers `None`.
- `backend/soknad/web/ruter.py` -- `innlegging()` får GET og POST. Feil gir samme side uten redirect, som `_vis_skjema`.
- `backend/soknad/web/tekster.py` -- feltnavn, knapper, skjermlesertekster, hjelpetekst, feilboksoverskrift og `("cv"|"annonse", FeilType.TOM)` i `FEILTEKSTER`.
- `backend/soknad/web/templates/innlegging.html` -- felt, feilboks, knapperad. `skjemafelt.html` er for `input` og brukes ikke her.
- `backend/soknad/web/static/js/innlegging.js` -- ny, `defer`, bare på innleggingen: «Lim inn tekst», søppelbøtta, statusområdet, og at en lenke i feilboksen gir fokus til feltet.
- `backend/soknad/web/static/css/stil.css` -- `.innleggingsfelt` (hvitt kort, `--error`-ramme ved feil), `.felt-rad` (grid, 2 kolonner fra 1000 px), tekstboksen (`resize: vertical`, `min-height`), `.soppelbotte`, `.feilboks` (`--error-tint`, `--rounded-md`), `.testhjelp` (stiplet ramme). Gjenbruk `.knapperad`, `.hovedknapp`, `.sekundaerknapp`, `.feiltekst`.
- Tester: `tests/kjerne/test_okt.py`, `tests/kjerne/test_inndata.py`, ny `tests/web/test_innlegging.py`. Gjenbruk `sett_soknad`, `soknaden`, `tagger_i`, `main`, `css_blokk` fra `hjelpere.py`.
- Ikke endre: `telleregel.py`, `testdata_match.py`, `ki_svar.py`, `testdata/`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/okt.py` og `inndata.py` -- `sett_inndata` og `sjekk_innlegging`, med tester.
- [x] `backend/soknad/__init__.py` og `web/flyt.py` -- `test_ki` og `ki()`.
- [x] `backend/soknad/web/tekster.py` og `ruter.py` -- tekstene og POST på innleggingen.
- [x] Mal, `innlegging.js` og `stil.css` -- som i Always.
- [x] Webtester -- én per rad i matrisen, og at cookien bare har `okt_id`, at alle feiltypene kjernen kan lage har tekst, at skjermlesertekstene og `aria-describedby` stemmer, og CSS-en (1000 px, `min-height`, 24 px, ingen `nowrap`). FR-nummer i navn og docstring.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (288 før denne storyen), og `ruff check` og `ruff format --check` har ingen feil.
- Given et tomt CV-felt i nettleseren, when jeg trykker «Lim inn tekst», then åpnes tekstboksen med markøren i, and when jeg trykker søppelbøtta, then er feltet tomt og fokus på «Lim inn tekst».
- Given feil i begge feltene, when siden kommer tilbake, then har feilboksen fokus, og en lenke i den flytter fokus til feltet.

## Implementation Notes

- Branch: `story/2-5-1-innleggingssiden`.
- Hovedøkta skrev koden selv (ingen hjelpeagent), som i story 2.3 og 2.4.
- Skjermlesernavnet på tekstboksen er en skjult `<span class="skjult">CV: </span>` i etiketten, ikke `aria-label`, så den synlige teksten og navnet henger sammen. `.skjult` bruker `max-height` og `clip-path`, fordi testene ikke tillater `height` eller `nowrap` i CSS-en.
- Feillenkene går til feltet (`#cv-felt`, `tabindex="-1"`). Uten JavaScript får feltet fokus. Med JavaScript rulles feltet fram, og fokus går til tekstboksen eller «Lim inn tekst», avhengig av hva som vises nå.
- `[hidden] { display: none !important; }` er lagt til, så `hidden` alltid skjuler.
- `base.html` har fått `{% block skript %}`, så bare innleggingen laster `innlegging.js`.
- Testen `test_fr20_innleggingen_har_bare_overskriften` i `test_modusvalg.py` er skrevet om, fordi innleggingen nå har et skjema.
- Tester: 45 nye, 333 i alt, `ruff` grønn.
- Prøvd i nettleseren av Kristine: «Lim inn tekst», søppelbøtta, feilboksen, «Tilbake» og bredder. Hun fant at en lenke i feilboksen så ut til å ikke gjøre noe. Fokus gikk til «Lim inn tekst», men nettleseren viser ikke ringen for `:focus-visible` etter et museklikk. `.lim-inn:focus` har nå fokusringen (commit `022b315`), med test.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-09), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Uten JavaScript (eller hvis skriptet ikke lastes) kan man ikke skrive i et tomt felt | blind, grensetilfeller | low | Riktig. Bestemt i spec-en (Design Notes). Alle vanlige nettlesere har JavaScript på, og en reserve gir mer kode | avvist |
| 2 | En POST uten `cv`/`annonse` lagrer tomme felt og nullstiller resultatene | blind, grensetilfeller | low | Riktig, men nettleseren sender alltid begge tekstboksene, også skjulte. Krever en laget forespørsel, og rettingen er en ny gren | avvist |
| 3 | Logges man ut i en annen fane midt i POST-en, gir `innlogging.testmodus` feil 500 | grensetilfeller | low | Riktig, men krever to forespørsler på nesten samme tid (samme som #2 i 2.4.2). Rettingen er ny kode | avvist |
| 4 | To POST-er samtidig: den siste vinner | grensetilfeller | low | Riktig, men gjelder hele øktlageret fra før, og krever to faner | avvist |
| 5 | Mangler `testdata/`, får all tekst `ikke_testdata` | grensetilfeller | low | Testdataene ligger i repoet. En slik feil vises med en gang i testene | avvist |
| 6 | En case-mappe uten `cv.txt` stopper oppstarten | grensetilfeller | false | At appen ikke starter med ødelagte testdata, er riktig oppførsel. Testdataene ligger i repoet | avvist |
| 7 | Tekst med bare usynlige tegn (U+200B) regnes som fylt utenfor testmodus | grensetilfeller | low | Riktig, men testmodus kan ikke slås av før Epic 4, og i testmodus gir teksten `ikke_testdata` | avvist |
| 8 | Søppelbøtta i to felt innen 100 ms gir to meldinger | grensetilfeller | low | Riktig. Bare den siste meldingen skrives nå (`clearTimeout`) | patch |
| 9 | Testen for tomme felt sjekker `hidden` på knappen, men `hidden` står på diven rundt, og limeboksene sjekkes ikke per felt | grensetilfeller, testhull, blind | low | Riktig. Testen sjekker nå `tom-tilstand` og `limeboks` i hvert felt | patch |
| 10 | `sett_inndata` nullstiller ikke `opptatt` | grensetilfeller | false | `opptatt` settes ikke før story 2.7 | avvist |
| 11 | Ingen test kjører `innlegging.js` | testhull | low | Riktig. Prosjektet har ingen nettlesertester. Sjekkes for hånd i gjennomgangen med Kristine | utsatt |
| 12 | Feilteksten nevner «Last opp en PDF», som ikke finnes før Epic 6 | blind | false | Teksten er fast i UX og i akseptansekriteriene til story 2.5 | avvist |
| 13 | `sett_inndata` sammenligner hele `Tekstfelt`, så `filnavn` teller med i Epic 6 | blind, testhull | low | Ingen feil i dag (`filnavn` er alltid `None`). Epic 6 endrer `sett_inndata` uansett | avvist |
| 14 | Rekkefølgen på feltene står både i `inndata.py` og `tekster.py` | blind | low | Riktig, kan skli fra hverandre i Epic 5. Ny test sjekker at de er like | patch |
| 15 | Ingen test for POST til `/innlegging` på et for tidlig steg | blind | low | Riktig. Testen er lagt til | patch |
| 16 | Riktig innlegging gir ingen tilbakemelding | blind | false | Bestemt i spec-en: siden vises på nytt til story 2.5.2 | avvist |
| 17 | Ukjent `handling` (400) viser den lagrede teksten, ikke den sendte | blind | low | Krever en laget forespørsel. Knappene sender alltid en kjent verdi | avvist |
| 18 | `.knapperad .hovedknapp` gjelder alle knapperader | blind | low | Riktig. Gjelder nå bare `.knapperad.mellomrom` | patch |
| 19 | Testene bruker `
`, men nettlesere sender `
` | blind | false | Nettleseren sender samme linjeskift hver gang, så like tekster er fortsatt like. Linjeskiftet etter `<textarea>` fjernes uansett type | avvist |
| 20 | Sorteringen krasjer hvis en feil har `felt=None` | blind | false | `finn_case` og tom-sjekken gir alltid `cv` eller `annonse`. Case A mot case B er testet i `test_testdata_match.py` | avvist |

## Design Notes

Tekstboksen står alltid i HTML-en, så teksten sendes med skjemaet. Når feltet er tomt, har den `hidden`, og «Lim inn tekst» vises. JavaScript fjerner `hidden` og setter fokus. Søppelbøtta tømmer, skjuler og setter fokus tilbake. Det er bare skjemaet i nettleseren som endres, så AD-1 holder: søknaden endres først når skjemaet sendes.

Feillenken går til tekstboksen når feltet har tekst, ellers til «Lim inn tekst». `sett_inndata` sammenligner rå tekst.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Logg inn, «Begynn å lage søknad», Full generering. Trykk «Sjekk CV-en min» med tomme felt: feilboksen med to lenker og røde rammer.
- Lim inn noe eget i CV-feltet: «CV: I testmodus fungerer bare testdataene fra mappen testdata/.» Lim inn `cv.txt` og `annonse.txt` fra `backend/testdata/case-1-utvikler/`: ingen feil.
- Skriv noe, trykk «Tilbake», så kortet igjen: teksten står der. Søppelbøtta tømmer, og fokus går til «Lim inn tekst».
- Gjør vinduet 375 px og 1280 px: feltene under hverandre og side om side, ingenting ruller sidelengs.
