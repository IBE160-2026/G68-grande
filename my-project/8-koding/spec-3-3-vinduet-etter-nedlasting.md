---
title: 'Story 3.3: Vinduet etter nedlasting'
type: 'feature'
created: '2026-11-12'
status: 'done'
baseline_commit: '90b541495fc67bbc78f283783e924e0991b7f630'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Etter at brevet er lastet ned, står brukeren igjen på brevsiden uten et tydelig neste steg. Det finnes ingen vei til en ny søknad fra brevsiden (FR-31).

**Approach:** Brevsiden får et `<dialog>`-vindu som `nedlasting.js` åpner med `showModal()` hver gang en nedlastingslenke trykkes. Vinduet har «Brevet er lastet ned!», «Filnavn: Soknad_<dato>.docx», «Vil du lage en ny søknad eller logge ut?» og knappene «Lag ny søknad» (lenke til startsiden, som alltid lager en ny tom søknad og beholder testmodus), «Logg ut» (POST til `/logg-ut` som i story 1.4) og «Bli her». Fokus går til «Bli her» når vinduet åpnes. «Bli her» og Esc lukker vinduet, og fokus går tilbake til «Last ned som Word». Serveren og søknadsdataene endres ikke.

## Boundaries & Constraints

**Always:** Alle tekster i `web/tekster.py`. JavaScript endrer bare hvordan siden ser ut, aldri søknadsdata. «Lag ny søknad» bruker startsiden slik den er (GET `/`), og «Logg ut» bruker utloggingen slik den er. Vinduet har `aria-labelledby` til overskriften og `aria-describedby` til filnavnet og spørsmålet, så filnavnet leses opp. Mens vinduet er åpent, kan bare vinduet nås (`showModal()`). Ingen rulling sidelengs ved 320 px og 200 % zoom, ingen faste høyder, ingen `nowrap`. Hver testfil og testfunksjon nevner FR-nummeret.

**Never:** Ikke vinduet «Logg ut før nedlasting», «Nytt forslag», PDF eller arbeidsgiver i filnavnet (Epic 7). Ingen nye ruter og ingen endring i `kjerne/` eller `adaptere/`. Vinduet åpnes ikke av seg selv når siden lastes på nytt.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Nedlasting | trykk «Last ned som Word» | fila lastes ned, knappen blir grønn, vinduet åpnes med fokus på «Bli her» | – |
| Hver gang | trykk på den grønne knappen igjen | fila lastes ned på nytt, og vinduet åpnes igjen | – |
| Lag ny søknad | trykk «Lag ny søknad» | startsiden, ny tom søknad, testmodus beholdt | – |
| Logg ut | trykk «Logg ut» i vinduet | utlogget, til innloggingen, søknaden slettet | – |
| Bli her / Esc | vinduet åpent | vinduet lukkes, fokus til «Last ned som Word» | – |
| Fra feilboksen | «Prøv på nytt» etter `FilFeil` | som Nedlasting. Fokus tilbake til knappen under brevet, siden feilboksen er skjult | – |
| Filen kan ikke lages igjen | `FilFeil` etter trykket | nettleseren viser brevsiden med feilboksen fra 3.2, og vinduet er borte | som i 3.2 |
| Siden lastes på nytt | `lastet_ned` sann | grønn knapp og filnavnlinje, vinduet er lukket | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/templates/base.html` -- ny tom blokk `{% block vinduer %}{% endblock %}` etter `ventetegn`-blokken, utenfor `<main>`. Da holder `test_brev.py::test_fr26_…` (bare én lenke i `<main>`) fortsatt, og Epic 7 kan legge flere vinduer der.
- `backend/soknad/web/templates/brev.html` -- fyller `vinduer`: `<dialog class="vindu" id="vindu-nedlastet" aria-labelledby="vindu-nedlastet-overskrift" aria-describedby="vindu-nedlastet-filnavn vindu-nedlastet-tekst">` med `h2`, `<p id="…-filnavn">{{ tekster.filnavn_linje(filnavn) }}</p>`, `<p id="…-tekst">`, og en `.vindu-knapper`-rad: `<a class="hovedknapp" href="{{ url_for('web.start') }}">`, `<form method="post" action="{{ url_for('web.logg_ut') }}">` med `<button class="sekundaerknapp" type="submit">`, og `<form method="dialog">` med `<button class="lenkeknapp" id="bli-her">`. Ingen `autofocus` i vinduet (sidens `autofocus` står på h1 eller feilboksen).
- `backend/soknad/web/static/js/nedlasting.js` -- i klikkhandleren, etter dagens kode: `vindu.showModal()` hvis vinduet finnes og ikke er åpent, så `bli-her`.focus(). Én lytter på `close` som flytter fokus til `#last-ned-<format>` fra siste trykk. Ingen `preventDefault`.
- `backend/soknad/web/tekster.py` -- under nedlastingstekstene: `VINDU_NEDLASTET_OVERSKRIFT = "Brevet er lastet ned!"`, `VINDU_NEDLASTET_TEKST = "Vil du lage en ny søknad eller logge ut?"`, `LAG_NY_SOKNAD_KNAPP = "Lag ny søknad"`, `BLI_HER_KNAPP = "Bli her"`. «Logg ut» bruker `LOGG_UT_KNAPP`, filnavnet `filnavn_linje`.
- `backend/soknad/web/static/css/stil.css` -- etter `.filnavn-linje`: `.vindu` (hvit `--surface`, ingen kant, `--rounded-lg`, `--shadow`, `max-width: 420px`, `width: calc(100% - 2 * var(--space-4))`, polstring, sentrert tekst, toner inn på 0,2 s), `.vindu::backdrop` (`rgba(58, 37, 48, 0.45)`, altså `--text` med 45 %), `.vindu h2`, `.vindu-knapper` (flex, `flex-wrap`, `gap`, sentrert), `.vindu-knapper form { margin: 0 }`, `.vindu .hovedknapp` (inline-block, `width: auto`, `margin-top: 0`) og ny `.lenkeknapp` (understreket `--primary`-tekst, ingen ramme eller bakgrunn, fokusring som andre knapper). Redusert bevegelse dekkes alt av blokken nederst.
- Gjenbruk: `paa_brev`, `html_av`, `element`, `filnavn_i_dag` i `tests/web/test_nedlasting.py`, og `tagger_i`, `main`, `soknaden`, `okt_id`, `STIL`, `css_blokk` i `tests/web/hjelpere.py`. `GET /` lager alt `Soknad()` og beholder `Innlogging` (`test_startside.py:11`).

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/web/tekster.py`, `templates/base.html`, `templates/brev.html` -- tekstene, blokken og vinduet.
- [x] `backend/soknad/web/static/js/nedlasting.js` -- åpne vinduet, fokus inn og ut.
- [x] `backend/soknad/web/static/css/stil.css` -- vinduet, sløret, knapperaden og lenkeknappen.
- [x] `backend/tests/web/test_vindu_etter_nedlasting.py` (ny) -- vinduet finnes utenfor `<main>` med riktige tekster og ARIA-koblinger, filnavnet i vinduet er dagens, «Lag ny søknad» peker på `/` og gir en tom `Soknad()` med samme økt og testmodus (både på og av), «Logg ut» er et POST-skjema til `/logg-ut` som logger ut, «Bli her» er `method="dialog"`, ingen `autofocus` og ingen `open` i vinduet (også med `lastet_ned` sann og ved `FilFeil`), skriptet bruker `showModal`, fokuserer `bli-her` og lytter på `close`, tekstene ligger i `tekster.py`, og CSS-en har `max-width: 420px`, `::backdrop` og `.lenkeknapp`.

**Acceptance Criteria:**
- Given brevsiden, when brukeren trykker «Last ned som Word», then åpnes vinduet hver gang med «Brevet er lastet ned!», filnavnet og «Vil du lage en ny søknad eller logge ut?», og fokus står på «Bli her» (FR-31, UX-DR16, UX-DR17).
- Given vinduet, when brukeren trykker «Lag ny søknad», then kommer startsiden, søknaden er tom, og testmodus er beholdt (FR-31, AD-7).
- Given vinduet, when brukeren trykker «Logg ut», then logges brukeren ut som i story 1.4 (FR-6).
- Given vinduet, when brukeren trykker «Bli her» eller Esc, then lukkes vinduet, og fokus går tilbake til «Last ned som Word» (UX-DR17).

## Implementation Notes

- Branch: `story/3-3-vinduet-etter-nedlasting`, fra `main` på `90b541495fc67bbc78f283783e924e0991b7f630`. Sprint-status: 3.3 står på «in-progress». Kodet av en hjelpeagent ut fra spec-en.
- Avvik: sløret bruker `var(--veil)` i stedet for fargekoden. `--veil` står alt i `:root` med samme farge (`rgba(58, 37, 48, 0.45)`), og `test_ruter.py::test_ux_dr1_ingen_fargekoder_utenfor_root` forbyr fargekoder utenfor `:root`. Nettlesere fra før 2024 lar ikke `::backdrop` bruke variablene fra `:root`. Der mangler sløret, men vinduet virker likevel.
- Tillegg: i høykontrastmodus (`forced-colors`) får `.vindu` en `CanvasText`-ramme, slik andre elementer i stilarket har.
- Den nye testfila henter fiksturene `paa_brev` og `filfeil` fra `test_nedlasting.py`.
- 560 tester (11 nye), `ruff check` og `ruff format --check` grønne. De manuelle sjekkene i nettleseren er ikke gjort ennå.
- Etter gjennomgangen: CSS-testen sjekker høykontrastrammen, og tekstene i de regulære uttrykkene i testene er escapet. 560 tester, `ruff` grønn.
- Etter prøving i nettleseren: første gang vinduet ble åpnet med musa, viste ikke «Bli her» fokusringen (`:focus-visible` gir ingen ring etter et museklikk). `#bli-her:focus` viser nå ringen, som `.lim-inn:focus`. 560 tester grønne.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-12), tre lag: blind, kanttilfeller, testhull.

| # | Funn | Vurdering | Begrunnelse | Rute |
|---|------|-----------|-------------|------|
| 1 | `nedlasting.js` testes bare ved å lese kildeteksten. At vinduet åpnes, og hvor fokus havner, blir ikke kjørt i en nettleser (testhull + blind) | medium | Riktig. Prosjektet har ingen nettlesertester, og å sette opp det er større enn denne storyen. Manuell sjekk i PR-kommentaren dekker det til da | defer |
| 2 | Vinduet sier «Brevet er lastet ned!» før svaret er kommet, også når svaret blir feilboksen | low | Valgt i intent og Design Notes (åpnes ved trykket, som den grønne knappen i 3.2). Ved FilFeil bytter nettleseren side, og vinduet forsvinner | avvist |
| 3 | «Lag ny søknad» eller «Logg ut» trykket før fila er kommet, avbryter nedlastingen og sletter brevet (blind + kanttilfeller) | low | Mulig i teorien, men fila lages i minnet på en lokal server på brøkdelen av et sekund, og fokus står på «Bli her». Rettingen (forsinkelse eller låste knapper) gir ny kode | avvist |
| 4 | Filnavnet i vinduet regnes ut når siden vises, så det kan vise gårsdagens dato etter midnatt (blind + kanttilfeller) | low | Samme som funn 4 i 3.2. Sjelden, og rettingen krever et nytt felt | avvist |
| 5 | Ctrl-, Shift- og Cmd-klikk åpner vinduet selv om nedlastingen skjer i en annen fane (blind + kanttilfeller) | false | Fila lastes ned likevel, så teksten i vinduet stemmer. Den grønne knappen fra 3.2 gjør det samme | avvist |
| 6 | CSS-testen sjekker ikke høykontrastrammen på `.vindu` | low | Riktig. Én ekstra linje i testen | patch |
| 7 | `.lenkeknapp` har ingen hover- eller trykkeffekt og ingen minstehøyde | low | Den ser ut som en lenke, som `.lenkerad a`, som heller ikke har det. Med polstring blir den omtrent 40 px høy, over kravet på 24 px | avvist |
| 8 | «Bli her» har ikke `type="submit"` | false | Standardtypen i et skjema er submit, og `method="dialog"` lukker vinduet. Ingen feil | avvist |
| 9 | Den nye testfila låner fiksturer fra `test_nedlasting.py` | low | Virker (pytest samler ikke testene dobbelt). Å samle testhjelperne er alt et åpent punkt fra retrospektiven for Epic 1 | avvist |
| 10 | Tekstene settes rett inn i regulære uttrykk i testene, uten `re.escape` | low | Riktig. Tekster med `(`, `?` eller `.` senere vil gi feil treff. Direkte retting | patch |
| 11 | Ingen test for at `<main>` ikke blir `inert` | false | `showModal()` setter ikke `inert` på noe, og koden gjør det heller ikke | avvist |
| 12 | Tilbake etter «Lag ny søknad» viser brevsiden fra nettleserens minne med vinduet åpent | false | `tilbake.js` laster siden på nytt ved `pageshow` med `persisted`, og alle sider har `no-store` | avvist |
| 13 | Nettlesere uten `showModal` gir TypeError | low | Alle nettlesere siden 2022 har det. Nedlastingen og den grønne knappen skjer før kallet | avvist |
| 14 | Vinduet viser alltid .docx-filnavnet, også ved andre formater | false | Bare docx finnes. PDF kommer i Epic 7 | avvist |
| 15 | `tilbakeTil` kan være null hvis `#last-ned-<format>` mangler | false | Knappen står alltid på brevsiden | avvist |

## Design Notes

- **Vinduet åpnes ved trykket**, samme øyeblikk som knappen blir grønn (valgt i 3.2). Svaret er et vedlegg, så siden kan ikke vite når fila er lagret uten å hente den med `fetch`. Feiler fila (`FilFeil`), bytter nettleseren til brevsiden med feilboksen, og vinduet forsvinner av seg selv.
- **Fokus tilbake gjøres i skriptet** på `close`, ikke av nettleseren. Nettleseren ville sendt fokus til «Prøv på nytt» i feilboksen, som da er skjult.
- **«Bli her» er `<form method="dialog">`**, så nettleseren lukker vinduet uten ekstra kode. Esc lukker `showModal()`-vinduer av seg selv.
- **Uten JavaScript** lastes fila ned som før, men vinduet kommer ikke. «Logg ut» står uansett i hjørneraden.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Logg inn, case 1 → brevsiden → «Last ned som Word»: fila lastes ned, knappen blir grønn, vinduet åpnes med mørkt slør og fokus på «Bli her». Tab blir i vinduet. Esc lukker, fokus på knappen. Trykk igjen: vinduet kommer igjen.
- Skjermleser (NVDA/Forteller): overskriften, filnavnet og spørsmålet leses opp når vinduet åpnes.
- «Lag ny søknad» → startsiden, merkelappen/bryteren «Testmodus» er fortsatt på. «Logg ut» i vinduet → innloggingen.
- 320 px og 200 % zoom: knappene brytes til flere linjer, ingen rulling sidelengs.
