---
title: 'Story 3.1: Se søknadsbrevet'
type: 'feature'
created: '2026-11-11'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'd1b95402ab47fb90412b7f9eb410b3e0e84f4df6'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Resultatsiden ender i dag i en blindvei. Brukeren kan ikke få et søknadsbrev, og det finnes ingen brevside (FR-21, FR-22, FR-26, FR-28).

**Approach:** Resultatsiden får hovedknappen «Lag søknadsbrevet mitt» til høyre for «Tilbake». Trykket sender en POST til `/resultat`, som viser ventetegnet («Vi lager brevet ditt – det kan ta en liten stund.»), kaller `ki().brev(cv, annonse, forslag=1)` med `opptatt` rundt, lagrer brevet og sender til `/brev`. Brevsiden viser «Din ferdigstilte søknad!» og brevet som et hvitt ark (høyst 720 px), ett `<p>` per avsnitt, uten «Tilbake» og uten redigering. `TestKI` leser et håndlaget `testdata/case-1-utvikler/ki-svar/brev-1.json`. En `KIFeil` viser resultatsiden på nytt med feilboksen, «Resultatet og det du har lagt inn, er ikke borte.» og «Prøv på nytt». Retro-punktet tas med: brevsteget i `SIDE_FOR_STEG`, og resultatsiden sender til innleggingen når analysen mangler.

## Boundaries & Constraints

**Always:** Steget flyttes bare etter en POST som lyktes (AD-8). KI-kallet bare fra POST, med samme mønster som `innlegging()`: `til_steget_hvis_opptatt`, `sett_opptatt`, `erstatt_soknad` i `finally`, så en ny søknad fra startsiden vinner. `brev` går gjennom `kontroller()`. `velg_modus` og `sett_inndata` nullstiller `brev`. Alle tekster i `web/tekster.py`, ordrett fra EXPERIENCE. Brevet bare i minnet. Hver testfil og testfunksjon nevner FR-nummeret.

**Never:** Ingen nedlasting, `lastet_ned`, `forslag`-felt, fyrverkeri eller «Nytt forslag» (story 3.2 og Epic 7). Ikke `contenteditable` eller tekstfelt for brevet. JavaScript endrer aldri søknadsdata. `kjerne/` leser ingen filer.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Brevet lages | steg resultat, case 1, POST `handling=brev` | `Soknad.brev` lagret, steg brev, redirect `/brev` | – |
| KI-feil | `brev` gir `KIFeil(type)` | Resultatsiden (200) med feiltekst for typen, «Resultatet …» og «Prøv på nytt». Steg og søknad uendret, `opptatt` usann | ingen redirect |
| Tomt brev | `avsnitt: []` eller bare `"  "` | `KIFeil(ubrukelig_svar)` → som KI-feil | – |
| Opptatt | `opptatt` sann, POST | redirect til siden for steget, `brev` kalles ikke | – |
| Brevsiden for tidlig | steg < brev, GET `/brev` | redirect til siden for steget | – |
| Analysen mangler | steg ≥ resultat, `gap` eller `nokkelord` er None | GET og POST `/resultat` → `/innlegging` | – |
| Ukjent handling | POST uten `handling=brev` | resultatsiden, 400, søknaden uendret | – |

</frozen-after-approval>

## Code Map

- `soknad/kjerne/okt.py` -- `Soknad` (legg til `brev: dict | None = None`), `velg_modus`, `sett_inndata` (nullstill `brev`), ny `sett_brev(soknad, brev)` med steg `max(steg, BREV)`.
- `soknad/kjerne/ki_svar.py` -- `FELT` + `_riktig_form`/`_tomt`: `brev` = `{avsnitt: [str]}`, tom når `_bare_tomme(avsnitt)`.
- `soknad/adaptere/ki.py` -- `KI`-protokollen og `TestKI.brev(cv, annonse, forslag)`: caset som i `gap` (`finn_case`), fila `brev-1` ved oddetall, `brev-2` ved partall. `_svar` må kunne lese et filnavn som ikke er lik oppgaven.
- `soknad/web/flyt.py` -- `SIDE_FOR_STEG[Steg.BREV] = "web.brev"`, fjern kommentaren om Epic 3.
- `soknad/web/ruter.py` -- `resultat()` blir GET+POST, ny `brev()` med `@krever_steg(Steg.BREV)`, ny `_vis_resultat(soknad, ki_feil=None)`. `brev is None` på `/brev` → `/resultat`.
- `soknad/web/tekster.py` -- `LAG_BREV_KNAPP`, `VENTE_BREV`, `KI_FEIL_BEHOLDT_RESULTAT`, `BREV_TITTEL = "Søknadsbrev"`, `BREV_OVERSKRIFT`. Fjern «Resultatsiden får sin i Epic 3».
- `soknad/web/templates/resultat.html` -- skjema `id="resultat-skjema"` rundt knapperaden (`knapperad mellomrom`), `ventetegn`-blokken og `vente.js`. Feilboksen som i `innlegging.html` (form=, `data-vente`). h1 har `autofocus` bare uten feil.
- `soknad/web/templates/brev.html` -- ny. h1 `brev-overskrift` med `tabindex="-1" autofocus`, `<article class="brevark">`.
- `soknad/web/static/css/stil.css` -- `.brev-overskrift` (sentrert, `--size-heading-letter`, mobil `--size-heading-letter-mobile` under 700 px) og `.brevark` (`--surface`, kant, `--rounded-md`, `--shadow`, `max-width: 720px`, `margin: 0 auto`, luft `--space-6`×`--space-7`, mobil `--space-4`, `overflow-wrap: anywhere`).
- `testdata/case-1-utvikler/ki-svar/brev-1.json` -- ny, teksten i Design Notes.
- `tests/web/hjelpere.py` -- `FeilendeKI.brev`.
- `tests/web/test_modusvalg.py:117` -- tabelltesten tar med `Steg.BREV`.
- Gjenbruk: `ki_feiltekst`, `PROV_PA_NYTT_KNAPP`, `.feilboks*`, `ventetegn.html`, `vente.js` (uendret). `Cache-Control: no-store` settes alt for alle sider i `innlogging.py:41`.

## Tasks & Acceptance

**Execution:**
- [x] `kjerne/okt.py`, `kjerne/ki_svar.py`, `adaptere/ki.py` -- feltet, kontrollen og `TestKI.brev`, med tester i `tests/kjerne/` og `tests/adaptere/test_ki.py` (også `forslag=2` → `brev-2`, mangler fila → `KIFeil(annet)`).
- [x] `testdata/.../brev-1.json` -- testbrevet, og en test i `tests/test_testdata.py` om at det består `kontroller` og ikke har frasene fra addendum.
- [x] `web/flyt.py`, `web/ruter.py`, `web/tekster.py`, malene, CSS -- rutene og sidene.
- [x] `tests/web/test_brev.py` -- ny: hver rad i matrisen, knappen med `data-vente`, h1 og sidetittel, ett `<p>` per avsnitt med escaping, ingen «Tilbake»/`textarea`/`contenteditable`, ingen redirect ved KI-feil, «Prøv på nytt» sender `handling=brev`, tekstene i `tekster.py`, CSS-bredden 720 px.

**Acceptance Criteria:**
- Given resultatsiden, when den vises, then står «Tilbake» til venstre og «Lag søknadsbrevet mitt» til høyre nederst, og brevet er ikke laget ennå (FR-21).
- Given brevsiden, when den åpnes, then har den fokus på «Din ferdigstilte søknad!», sidetittelen «Søknadsbrev – Søknadsassistenten» og ingen rulling sidelengs ved 320 px og 200 % zoom.
- Given at brukeren endrer CV-en eller velger modus på nytt, when steget går tilbake, then er det gamle brevet borte.

## Implementation Notes

- Branch: `story/3-1-se-soknadsbrevet`, fra `main` på `d1b95402ab47fb90412b7f9eb410b3e0e84f4df6`. Sprint-status: epic 3 og 3.1 står på «in-progress».
- `.brevark` har `margin: 0 auto var(--space-7)`, så arket ikke ligger inntil hjørneraden. 720 px kommer fra den eksisterende `--letter-max`.
- `resultat()` sjekker analysen før opptatt-sjekken. Ukjent `handling` gir 400. «Lag søknadsbrevet mitt» på steg brev lager brevet på nytt (som i manuell sjekk). Er CV og annonse uendret, beholdes brevet etter «Sjekk CV-en min».
- Endrede eldre tester: `test_modusvalg.py` (tabellen), `test_resultat.py` (`knapperad mellomrom`), `test_ki_svar.py` (ukjent oppgave er nå `korrektur`), `test_ventetegn.py` (siden uten ventetegn er nå `/brev`).
- 509 tester før gjennomgangen, `ruff` grønn.
- Etter gjennomgangen: `kontroller` fjerner tomme avsnitt i et brev, nye tester for utlogging midt i brevkallet og for sjekklisten i `fasit.md`, og `test_alle_sider.py` nevner resultatsiden og brevsiden. 512 tester, `ruff` grønn.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-11), tre lag: blind, kanttilfeller, testhull (ingen funn).

| # | Funn | Vurdering | Begrunnelse | Rute |
|---|------|-----------|-------------|------|
| 1 | To POST-er samtidig kan begge lese søknaden før den blir opptatt | low | Samme mønster som innleggingen. `vente.js` stopper dobbelttrykk. En atomisk sjekk i øktlageret er mer kode enn skaden er verdt | avvist |
| 2 | KI-feil etter at søknaden er byttet ut i en annen fane viser den gamle resultatsiden | low | Riktig, men «Prøv på nytt» sender da til startsiden. Samme som på innleggingen | avvist |
| 3 | Lykkes kallet, men lagringen ikke, sendes brukeren til `/brev` og videre | false | Med vilje: den nye søknaden fra startsiden vinner, og `/brev` sender til steget | avvist |
| 4 | `forslag` 0 eller negativ gir `brev-2` uten feil (to lag) | low | Kalles bare med 1 i denne epicen. Vakt hører hjemme i Epic 7 med telleren | avvist |
| 5 | Brev med noen tomme avsnitt slipper gjennom og gir tomme `<p>` | low | Riktig, kan skje med ekte KI i Epic 4. `kontroller` fjerner tomme avsnitt | patch |
| 6 | Linjeskift i et avsnitt forsvinner, og «Med vennlig hilsen» står et helt avsnitt fra navnet | low | Ser kosmetisk ut. Kristine ser på brevet i nettleseren og bestemmer | avvist |
| 7 | Ingen test for utlogging i en annen fane mens brevet lages | low | Riktig testhull (retro-punkt 10 gjaldt innleggingen) | patch |
| 8 | «Lag søknadsbrevet mitt» igjen kaller KI-en på nytt og bytter brevet | false | Slik spec-en sier (manuell sjekk). Fiksen ville vært å endre spec-en | avvist |
| 9 | Ingen test for sjekklisten i `fasit.md` mot testbrevet | low | Riktig, lett å teste med nøkkelord | patch |
| 10 | Frasesjekken matcher deler av ord og bør ligge i en felles modul | low | Gir bare falske treff, ikke falske godkjenninger. Felles liste hører til Epic 4-prompten | avvist |
| 11 | Noen nye tester nevner bare NFR/UX-DR, og én docstring har «UX-DR:» uten nummer | low | NFR og UX-DR brukes i eldre tester også. Nummeret som manglet, er rettet | patch |
| 12 | `test_alle_sider.py:68` nevner ikke resultatsiden og brevsiden | low | Riktig | patch |
| 13 | Ventetegnet kan bli stående etter tilbakeknappen (bfcache) | false | `tilbake.js` laster siden på nytt ved `pageshow` med `persisted` | avvist |
| 14 | Små testhull: fast tekst i regex, `vente.js` på feilsiden, positiv sjekk i ventetegn-testen | low | Tekstene er testet i `test_tekster`-testene, og `vente.js` står i malen uten vilkår | avvist |
| 15 | Brevsiden er en blindvei uten knapper | false | Med vilje: nedlasting og vinduet kommer i 3.2 og 3.3 | avvist |

## Design Notes

Testbrevet (`brev-1.json`), utkast fra Claude som Kristine godkjenner. Ingen påstander fra sjekklisten i `fasit.md`, ingen fraser fra addendum:

1. «Jeg søker stillingen som junior utvikler i Testvik Utvikling AS. Jeg går tredje år på bachelor i IT ved Eksempelby høgskole og fullfører graden våren 2027, slik at jeg kan begynne i august 2027.»
2. «I annonsen ber dere om erfaring med Python, gjerne med Flask, og om kunnskap i HTML og CSS. I bachelorprosjektet lager vi en nettside der studenter kan booke grupperom, laget i Python med Flask, HTML og CSS. Jeg har også laget et program i Python som henter værdata og viser dem som grafer.»
3. «Dere ser også etter en som bruker Git og har jobbet med Linux. I bachelorprosjektet er vi tre på gruppa, og vi bruker Git til versjonskontroll. Sommeren 2025 var jeg IT-assistent på høgskolen. Der hjalp jeg studenter med pålogging og satte opp PC-er med Linux.»
4. «Stillingen har også møter med kunder. Siden 2022 har jeg jobbet deltid som butikkmedarbeider med kundeservice. Jeg har norsk som morsmål og snakker og skriver engelsk flytende.»
5. «Jeg lærer nye verktøy raskt og ser etter min første jobb som utvikler. En stilling med fast fadder og tett samarbeid med erfarne kolleger passer derfor godt for meg. Jeg stiller gjerne til intervju.»
6. «Med vennlig hilsen» 7. «Sara Eksempel»

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Logg inn, case 1 fra `backend/testdata/` → resultatsiden: «Tilbake» til venstre, «Lag søknadsbrevet mitt» til høyre. Trykk (gjerne «Slow 4G» i F12): ventetegnet med «Vi lager brevet ditt – det kan ta en liten stund.», så brevsiden med fokus på overskriften.
- Brevet som hvitt ark, ett avsnitt per avsnitt, ingen «Tilbake», kan ikke skrives i. 320 px, 768 px, 1280 px og 200 % zoom: ingen rulling sidelengs.
- KI-feil: gi `brev-1.json` `{"avsnitt": []}` midlertidig (ta kopi først): resultatsiden med feilboksen, «Resultatet og det du har lagt inn, er ikke borte.» og «Prøv på nytt», som har fokus. Sett fila tilbake fra kopien og trykk «Prøv på nytt»: brevsiden.
- Nettleserens tilbakeknapp fra brevsiden til resultatsiden og så «Lag søknadsbrevet mitt» igjen: brevsiden kommer på nytt.
