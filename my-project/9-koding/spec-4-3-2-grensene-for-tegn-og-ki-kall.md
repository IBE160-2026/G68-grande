---
title: 'Story 4.3.2: Grensene for tegn og KI-kall'
type: 'feature'
created: '2026-11-14'
status: 'done'
baseline_commit: 'ad813079e1b24c4b7d11bf60a0e9b0f077cec6fc'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Med ekte KI kan en svært lang tekst eller mange trykk på «Sjekk CV-en min», «Lag søknadsbrevet mitt» og «Prøv på nytt» koste mye. NFR-11 (endret 12. november) sier at hvert innleggingsfelt godtar høyst 15 000 tegn, og at hver søknad kan bruke høyst 10 KI-kall.

**Approach:** `sjekk_innlegging` gir en ny feil `for_lang` når et felt har mer enn 15 000 tegn, med egen feiltekst ved feltet og i feilboksen. Søknaden teller KI-kallene sine (nøkkelord, gap og brev er ett kall hver). Når det ikke er plass til kallene en handling trenger, kalles ikke KI-en, og brukeren får en melding i feilboksen. Grensene ligger i `innstillinger.py`.

## Boundaries & Constraints

**Always:** Begge grensene i `innstillinger.py` (`MAKS_TEGN = 15_000`, `MAKS_KI_KALL = 10`). Tegnene telles med `\r\n` som ett tegn (slik brukeren ser teksten). Rekkefølgen per felt er tom, så for lang, så ikke testdata, og høyst én feil per felt. Hvert kall telles når det startes, også når det feiler, så telleren er riktig selv ved KI-feil. En handling startes bare når alle kallene den trenger får plass (analysen trenger 2, brevet 1), så grensen aldri passeres. Telleren følger søknaden: en ny søknad fra startsiden begynner på 0. Det som er lagt inn, er fortsatt der. Alle brukertekster i `web/tekster.py`. Testene kaller aldri det ekte API-et.

**Never:** Ikke `maxlength` på tekstboksene (da kuttes en lang tekst uten melding). Ingen endring i `adaptere/ki.py`, promptene eller `kjerne/ki_svar.py`. Ikke «Nytt forslag» (Epic 7, som må telle kallet sitt med den samme funksjonen). Ikke `scripts/lag_testsvar.py` (4.4).

**Beslutning (Kristine, 2026-11-14):** feilteksten er «CV: Teksten er for lang. Den kan være på høyst 15 000 tegn.» og «Stillingsannonse: Teksten er for lang. Den kan være på høyst 15 000 tegn.»
**Beslutning (Kristine, 2026-11-14):** meldingen er «Du har brukt alle KI-kallene for denne søknaden. Begynn på en ny søknad fra startsiden.» Den står i feilboksen øverst, uten «Prøv på nytt», og på innleggingen med «Det du har lagt inn, er ikke borte.» under (på resultatsiden «Resultatet og det du har lagt inn, er ikke borte.»).
**Beslutning (Kristine, 2026-11-14):** grensen på 10 KI-kall gjelder bare med ekte KI (testmodus av). I testmodus telles ingen kall, og ingenting stoppes. Tegngrensen gjelder i begge modusene.
**Beslutning (Kristine, 2026-11-14):** spec-en beholdes samlet (ca. 1800 tokens).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Akkurat 15 000 | CV på 15 000 tegn | godtas | – |
| For lang | CV på 15 001 tegn, annonse tom | feilboks med begge feilene, for lang ved CV, ingen KI-kall | teksten står igjen |
| Linjeskift | 15 000 tegn der linjeskift sendes som `\r\n` | godtas | – |
| Første analyse | 0 kall brukt | analysen kjøres, telleren blir 2 | – |
| KI-feil | nøkkelord feiler | telleren øker med 1 (gap ble ikke kalt) | KI-feilboksen som før |
| Ikke plass til analysen | 9 kall brukt, «Sjekk CV-en min» | ingen KI-kall, innleggingen med meldingen i feilboksen | telleren uendret |
| Ikke plass til brevet | 10 kall brukt, «Lag søknadsbrevet mitt» eller «Prøv på nytt» | ingen KI-kall, resultatsiden med meldingen | resultatet er ikke borte |
| Ny søknad | grensen nådd, så startsiden | telleren er 0 igjen | – |
| Testmodus | testmodus på, `ki_kall` = 10 | analysen og brevet kjøres som før, telleren uendret | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/innstillinger.py` -- grensene legges her, ved `MAKS_NOKKELORD`.
- `backend/soknad/kjerne/feil.py` -- `FeilType` (lukket liste) får `FOR_LANG = "for_lang"`. Testen `test_fr3_feiltypene_er_lukket_liste` i `tests/kjerne/test_inndata.py` må få den nye typen.
- `backend/soknad/kjerne/inndata.py` -- `sjekk_innlegging(cv, annonse, caser)`: legg for lang inn etter tom og før testdata. Ett felt med for lang skal ikke også få `ikke_testdata`.
- `backend/soknad/kjerne/okt.py` -- `Soknad` får `ki_kall: int = 0`. Ny funksjon (for eksempel `tell_ki_kall(soknad, antall)`) og en sjekk (for eksempel `har_plass_til(soknad, antall)`). `sett_inndata`, `velg_modus` og `begynn` bruker `replace`, så telleren beholdes.
- `backend/soknad/web/ruter.py` -- `innlegging()` POST: sjekken av plass kommer etter feltsjekken og `til_start_uten_samtykke`, før `sett_opptatt`. Kallene telles i `try`, og `finally` lagrer `ferdig` med telleren lagt til (også ved KI-feil). `resultat()` POST likeså, etter `til_start_uten_samtykke`. `erstatt_soknad` beholder en ny søknad fra en annen fane som før.
- `backend/soknad/web/templates/innlegging.html`, `resultat.html` -- feilboksen med `ki_feil`. Meldingen om brukte kall får sin egen gren (eller en parameter), uten «Prøv på nytt»-knappen, med samme fokus (`autofocus` på boksen).
- `backend/soknad/web/tekster.py` -- `FEILTEKSTER` får `("cv", FeilType.FOR_LANG)` og `("annonse", FeilType.FOR_LANG)` med tallet fra `MAKS_TEGN`, og meldingen om kallene.
- `backend/tests/web/hjelpere.py` -- `TellendeKI` (teller kall), `FeilendeKI`, `sett_soknad`, `sett_testmodus`, `app_med_nokkel`. Gjenbruk dem.
- `backend/soknad/web/flyt.py` -- `ki()` og `til_start_uten_samtykke` endres ikke.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/innstillinger.py`, `kjerne/feil.py`, `kjerne/inndata.py` -- grensene, `FOR_LANG` og sjekken i `sjekk_innlegging` -- NFR-11.
- [x] `backend/soknad/kjerne/okt.py` -- `ki_kall`, tellingen og sjekken av plass -- NFR-11, AD-7.
- [x] `backend/soknad/web/ruter.py`, `web/tekster.py`, `templates/innlegging.html`, `templates/resultat.html` -- sjekken før KI-kallene, tellingen, meldingen og feiltekstene -- NFR-11, FR-28.
- [x] `backend/tests/` -- tester for alle radene i matrisen (med `TellendeKI` og `FeilendeKI`), grensene i `innstillinger.py`, at feltet med for lang tekst har `aria-invalid` og feilteksten, og at meldingen ikke har «Prøv på nytt». Oppdater listen over feiltyper. NFR-11 i hver fil og funksjon.
- [x] `README.md` -- de to grensene, kort -- NFR-8.

**Acceptance Criteria:**
- Gitt hele testsuiten uten `ANTHROPIC_API_KEY`, når `uv run pytest` kjøres, så går alt gjennom uten nettverk.
- Gitt testdataene i testmodus, når hele flyten kjøres, så virker den som før (ingen av testfilene er over 15 000 tegn).

## Design Notes

Tellingen skjer i weblaget, rett før hvert kall (`kall += 1` før `nokkelord`, så før `gap`), og `finally` lagrer `tell_ki_kall(ferdig, kall)`. Da blir telleren riktig både når alt lykkes og ved KI-feil. Grensen er en myk sperre mot mange trykk. En ny søknad fra startsiden begynner på 0, og taket på 250 kr i Claude Console er den siste sperren (PRD, NFR-11).

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

**Manual checks (if no CLI):**
- Kristine, i nettleseren: lim inn en tekst på over 15 000 tegn (feilen ved feltet og i feilboksen), og med nøkkel og testmodus av: trykk «Sjekk CV-en min» til meldingen kommer (fem ganger gir 10 kall, den sjette gir meldingen). Det koster omtrent 5–8 kr, så det kan også bare sjekkes i testene.

## Implementation Notes

- Om et kall telles, avgjøres av KI-en som faktisk brukes: `_bruker_ekte_ki(valgt_ki)` i `ruter.py` er sann når `valgt_ki` ikke er `app.extensions["test_ki"]`. Da følger tellingen det som faktisk sendes til Claude, også hvis testmodus endres i en annen fane. `ki()` i `flyt.py` er uendret.
- `ANALYSE_KALL = 2` og `BREV_KALL = 1` står øverst i `ruter.py`. Grensene (`MAKS_TEGN`, `MAKS_KI_KALL`) står i `innstillinger.py`.
- `antall_tegn` i `kjerne/inndata.py` teller `\r\n` som ett tegn. `MAKS_TEGN_TEKST` i `tekster.py` gir «15 000» (vanlig mellomrom).
- Malene får `prov_pa_nytt` (standard sann). Meldingen om brukte kall vises med `prov_pa_nytt=False`, status 200.
- Eksisterende tester som er endret: listen over feiltyper, feltlisten i `Soknad` (`ki_kall` sist), og `test_fr28_ki_feil_fra_ekte_ki_vises_paa_innleggingen` (forventer nå `ki_kall=1`). Nye tester: `tests/web/test_grenser.py` og slutten av `tests/kjerne/test_inndata.py` og `test_okt.py`.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | kant | To «Sjekk CV-en min» eller to brev-POST-er samtidig kan begge passere `har_plass_til` før `opptatt` lagres, og kallene til den som taper i `erstatt_soknad`, telles ikke | low | Sant, men samme vindu som opptatt-sjekken har hatt siden 2.7.1. Det krever to POST-er innen millisekunder, knappen låses i JavaScript, og taket på 250 kr er den siste sperren. Rettingen krever en ny metode med lås i `Oktlager`. Avvist. |
| 2 | kant | Samme som #1, som påstand mot «høyst 10 KI-kall» | low | Samme årsak som #1. Avvist med den. |
| 3 | kant, blind | `antall_tegn` sier «slik brukeren ser teksten», men emoji og aksenttegn kan telle som flere tegn | low | Sant for docstringen. Telleregelen (kodepunkter) er grei. Direkte retting. Patch: docstringen. |
| 4 | kant, blind, verifisering | Ett telt kall kan bli to API-forespørsler med `max_retries=1` | low | Sant (`adaptere/ki.py:162`). Nye forsøk skjer bare ved feil. Direkte retting. Patch: en setning i kommentaren i `innstillinger.py` og i README. |
| 5 | kant | Hjelperne i `test_grenser.py` nevner ikke NFR-11 | false | Regelen gjelder testfiler og testfunksjoner. Fila og alle testfunksjonene nevner NFR-11. |
| 6 | blind | «Prøv på nytt» vises etter en KI-feil også når det ikke er plass til et nytt kall | low | Sant (8 brukt, nøkkelord feiler, 9). Trykket gir da meldingen om brukte kall, så brukeren får vite det. Rettingen krever en ny gren, og det skjer sjelden. Avvist. |
| 7 | blind | Kommentaren sier «søknaden er uendret» når det ikke er plass, men `sett_inndata` har alt lagret feltene | low | Sant for kommentaren. At resultatene nullstilles når teksten er endret, er AD-8 og gjaldt før. Patch: kommentaren. |
| 8 | blind | Ingen test av at et uventet unntak også teller kallene og slipper `opptatt` | low | Sant, `finally` har nå `tell_ki_kall`. Billig test. Patch. |
| 9 | blind | README kaller det en grense mot høy kostnad, men grensen gjelder per søknad og starter på 0 igjen | low | Sant, Design Notes sier det, men ikke README. Patch: README og kommentaren (samme som #4). |
| 10 | blind | Teksten lagres med `sett_inndata` før tegnsjekken, så en tekst opptil 16 MB blir liggende i øktlageret, og over 16 MB gir rå 413-side | low | Fantes før 4.3.2 (`sett_inndata` før sjekken, `MAKS_FORESPORSEL`). Defer. |
| 11 | blind | Ingen hjelpetekst «Høyst 15 000 tegn» eller teller under tekstboksene | false | Ikke en feil: intent og EXPERIENCE ber bare om egen feilmelding. Kan tas opp med Kristine som et ønske. |
| 12 | blind | Meldingen har ingen lenke til startsiden, og ingen varsel før grensen | low | Startsiden nås med «Tilbake» to ganger. Grensen nås sjelden, og en lenke er ny UI som Kristine må bestemme. Avvist, nevnes for Kristine. |
| 13 | blind | `tell_ki_kall` nevner ikke at `har_plass_til` må kalles først, eller Korrektur (Epic 5) | low | Sant. Direkte retting. Patch: docstringen. Føres også som åpent punkt i loggen. |
| 14 | blind | «15 000» har vanlig mellomrom og kan brytes på smal skjerm | low | De andre tekstene bruker vanlig mellomrom (for eksempel «64 %»). Bruddet krever akkurat den bredden. Avvist. |
| 15 | blind | Testhull: annonsen på akkurat 15 000 på websiden, «Tilbake» med for lang tekst, feltfeil sammen med «ingen plass» | low | Annonsen er dekket i `test_inndata.py`. «Tilbake» sjekker ingenting med vilje (som før). Rekkefølgen mellom feltfeil og meldingen er ikke testet. Patch: én test for rekkefølgen. |
| 16 | verifisering | Ingen testhull funnet | – | – |
