---
title: 'Story 7.3: Gjenbruke nøkkelordlisten når bare CV-en er endret'
type: 'feature'
created: '2026-11-19'
status: 'done'
baseline_commit: 'ff5353ef734ef9254793160a6c36acd3c70989a6'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-7-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Når brukeren går tilbake fra resultatsiden, endrer CV-en og trykker «Sjekk CV-en min» igjen, henter KI-en en ny nøkkelordliste. Listen kan bli litt annerledes, så prosenten kan endre seg selv om CV-en ikke ble bedre. Brukeren kan da ikke se om endringen faktisk hjalp (FR-15, FR-19, suksesskriterium 8).

**Approach:** `sett_inndata` beholder nøkkelordlisten og arbeidsgiveren når den vaskede annonseteksten er lik den listen ble laget fra. Analysen i innleggingsruten bruker da den lagrede listen og kaller KI-en bare for gap-analysen. Endres annonsen, hentes en ny liste som i dag.

## Boundaries & Constraints

**Always:**
- Bare `sett_inndata` i `kjerne/okt.py` avgjør om listen beholdes (AD-8). Ruten ser bare på om `soknad.nokkelord` finnes.
- Listen beholdes når `vask(annonse.tekst) == soknad.nokkelord_annonse`. `nokkelord`, `nokkelord_annonse` og `arbeidsgiver` følger hverandre: beholdes eller nullstilles sammen.
- Gap-analysen kjøres alltid på nytt. Gap, brev, korrektur, `forslag`, `lastet_ned` og steget nullstilles som før når en tekst er endret.
- Er all teksten lik, er søknaden uendret som før (retro 6).
- Når listen gjenbrukes, trenger analysen ett KI-kall, så grensen sjekkes for 1 kall i stedet for 2 (NFR-11).
- Tester nevner FR-nummeret, bruker `tests/web/hjelpere.py`, og aldri det ekte API-et. Nye webtester i en egen fil.

**Never:**
- Ingen ny tekst eller merknad på resultatsiden (UX sier at FR-15 er logikk, ikke noe som vises).
- Ikke lagre gap-analysen eller nøkkelord fra et kall som feilet.
- Ingen endring i `vask` (testdata-gjenkjenningen bruker den).

**Beslutning (Kristine, 19. november 2026):** samme vask som i dag (AD-10). En annonse der bare tegnsetting er endret (for eksempel «C++» → «C#»), regnes som lik, og den gamle listen brukes. Arkitekturen endres ikke (retro 2, A11).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Bare CV endret | Resultat finnes, ny CV, samme annonse | Listen og arbeidsgiveren beholdes, gap nullstilles, steg innlegging. «Sjekk» kaller bare `gap` | N/A |
| Ekstra mellomrom | Samme annonse med ekstra mellomrom/linjeskift | Regnes som lik, listen beholdes | N/A |
| Annonse endret | Ny tekst i annonsen | Listen nullstilles, «Sjekk» kaller `nokkelord` og `gap` | N/A |
| Bare eget brev endret (Korrektur) | Samme CV og annonse, nytt brev | Listen beholdes, gap nullstilles | N/A |
| Ingen liste fra før | `nokkelord_annonse is None` | Listen hentes som i dag | N/A |
| Gap feiler ved gjenbruk | Listen gjenbrukt, `gap` gir KIFeil | Feilboksen som i dag, listen står igjen, 1 kall telt. «Prøv på nytt» kaller bare `gap` | FR-28 |
| 9 kall brukt, gjenbruk | `ki_kall == 9`, listen gjenbrukes | Gap kjøres, `ki_kall == 10` | NFR-11 |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/okt.py:100` `sett_inndata` -- når tekst er endret: behold `nokkelord`, `nokkelord_annonse`, `arbeidsgiver` hvis `vask(annonse.tekst) == soknad.nokkelord_annonse`, ellers `None`. Resten av nullstillingen uendret. Fjern «kommer i Epic 7» i docstringen. `vask` er alt importert.
- `backend/soknad/kjerne/okt.py:146` `sett_analyse` -- uendret i oppførsel. Docstringen: «så Epic 7 kan se» → «så sett_inndata kan se» (FR-19).
- `backend/soknad/web/ruter.py:223` `analyse` i `innlegging` -- hvis `soknad.nokkelord is not None`: bruk `{"nokkelord": list(soknad.nokkelord), "arbeidsgiver": soknad.arbeidsgiver}` og kall bare `valgt_ki.gap`. `kall=` i `_med_ki` blir `GAP_KALL` (ny konstant 1) ved gjenbruk, ellers `ANALYSE_KALL`. Docstringen i `innlegging` nevner gjenbruken.
- `backend/soknad/web/ruter.py:285` `resultat` -- uendret: `gap is None` sender alt til innleggingen.
- `backend/tests/kjerne/test_okt.py:128-290` -- `_med_resultater` har `nokkelord_annonse="annonsen"` (= `vask("annonsen")`). Testene som venter `nokkelord=None` når bare CV eller eget brev er endret (`test_fr19_sett_inndata_med_endret_tekst_nullstiller_resultatene` med `"ny cv"` og `"min cv "`, `test_fr8_..._bare_nytt_eget_brev_...`, `test_fr8_..._ny_cv_og_nytt_brev_...`, `:201`, `:233`) må rettes til at listen beholdes.
- `backend/tests/web/test_innlegging.py:306`, `test_resultat.py:507` -- venter at listen nullstilles ved ny CV. Rettes.
- `backend/tests/web/test_grenser.py:248` `test_nfr11_fem_analyser_...` -- med gjenbruk gir 5 analyser 2+1+1+1+1 = 6 kall. Rettes til 9 analyser = 10 kall, og den tiende gir meldingen. `legg_paa_innlegging`/`legg_paa_resultat` har ingen `nokkelord_annonse`, så andre grensetester er uendret.
- I testmodus må CV-en være lik testdataene (`ikke_testdata`), og `TestKI.gap` finner caset ut fra CV-en. Webtester med endret CV kjører derfor med testmodus av (`app_med_nokkel`, samtykke) og en liten falsk KI i den nye testfila som svarer `NOKKELORD_SVAR`/`GAP_SVAR` uansett CV og skriver kallene i `kalt`. Ekstra mellomrom i CV-en går også i testmodus.
- Gjenbruk: `TellendeKI`, `FeilendeKI`, `sett_soknad`, `soknaden`, `CV`, `ANNONSE`, `NOKKELORD_SVAR`, `GAP_SVAR` i `tests/web/hjelpere.py`. `sjekk`/`legg_paa_*` i `test_grenser.py` (lokale, ikke kopier: lag egne små hjelpere i den nye filen eller flytt dem til `hjelpere.py`).

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/kjerne/test_okt.py` -- nye tester for `sett_inndata`: bare CV endret, ekstra mellomrom i annonsen, annonse endret, bare eget brev endret, ingen liste fra før; rett de eksisterende -- FR-15, FR-19
- [x] `backend/soknad/kjerne/okt.py` -- som i Code Map
- [x] `backend/soknad/web/ruter.py` -- som i Code Map
- [x] `backend/tests/web/test_gjenbruk_nokkelord.py` (ny) -- flyten resultat → «Tilbake» → ny CV → «Sjekk» med `TellendeKI`: `kalt == ["gap"]`, samme liste, ny prosent; ekstra mellomrom; endret annonse gir `["nokkelord", "gap"]`; gap feiler og «Prøv på nytt»; 9 kall brukt med gjenbruk; ekte KI teller 1 kall -- FR-15, FR-19, NFR-11
- [x] `backend/tests/web/test_innlegging.py`, `test_resultat.py`, `test_grenser.py` -- rett testene i Code Map

**Acceptance Criteria:**
- Given testmodus av og en falsk KI, på resultatsiden, when brukeren går «Tilbake», legger til et manglende nøkkelord i CV-en og trykker «Sjekk CV-en min», then er nøkkelordlisten den samme, prosenten høyere, og bare `gap` er kalt
- Given `uv run pytest -q`, `ruff check` og `ruff format --check`, when de kjøres, then består alle

## Implementation Notes

- Kodet av en underagent etter spec-en. 1 302 tester besto, og `ruff check` og `ruff format --check` var rene (kjørt på nytt i hovedøkten).
- `sett_inndata` beholder `nokkelord`, `nokkelord_annonse` og `arbeidsgiver` sammen. Ruten har `GAP_KALL = 1` og `gjenbruk = soknad.nokkelord is not None`, og bygger AD-4-formen fra søknaden når listen gjenbrukes.
- Ny testfil `tests/web/test_gjenbruk_nokkelord.py` med en egen falsk KI (`FasteSvarKI`) som svarer likt uansett CV, siden en endret CV ikke er testdata.
- Endret oppførsel: også med helt lik tekst (for eksempel «Tilbake» og «Sjekk» uten endring) kalles nå bare `gap`, fordi listen finnes. Før var det 2 kall. `test_fr15_kriterium_8_samme_treff_etter_tilbake` og NFR-11-testen med mange analyser er rettet etter det (9 analyser = 10 kall).

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | edge-case, verification-gap | «C++» → «C#» i annonsen regnes som lik, og den gamle listen brukes | false | Dette er Kristines beslutning 19. november (i den frosne delen). Låses med en test → se #9 |
| 2 | edge-case, blind | En lagret annonse som vasker til `""` (bare tegn eller emoji) passer til en annen slik annonse eller en tom annonse, så en gammel liste beholdes | low | Stemmer: `is not None` slipper `""` gjennom. Rettingen er en direkte endring til en sannhetssjekk, med test → patch |
| 3 | edge-case | En tom annonse underveis (eller en filfeil) sletter listen, så samme annonse etterpå henter en ny | low | Stemmer, men følger matrisen («annonse endret → ny liste»). Sjelden, og rettingen er en ny gren → avvist |
| 4 | edge-case, blind | Ruten sjekker `nokkelord`, kjernen sjekker `nokkelord_annonse`, så de kan være uenige | false | Bare `sett_analyse` setter `nokkelord`, og den setter `nokkelord_annonse` samtidig. `sett_inndata` beholder eller nullstiller alle tre sammen. Tilstanden finnes bare i testfiksturer |
| 5 | edge-case | Intent sier «endres annonsen, hentes en ny liste», men tegnsetting teller ikke | false | Beslutningen står i den frosne delen rett under. Rettingen ville endre spec-en → avvist |
| 6 | blind | Kommentaren i `analyse` sier «begge kallene» også ved gjenbruk | low | Stemmer. Direkte retting av kommentaren → patch |
| 7 | blind | Docstringen til `sett_analyse` sier «bare gap», men funksjonen skriver alltid listen | low | Stemmer: ruten gir den lagrede listen tilbake. Direkte retting av docstringen → patch |
| 8 | blind | Webtestene viser ikke at en ny liste er annerledes, fordi den falske KI-en alltid gir samme liste | low | `kalt == ["gap"]` og `kalt == ["nokkelord", "gap"]` viser om listen ble hentet, og `nokkelord_annonse` viser at ny analyse ble lagret → avvist |
| 9 | blind | Beslutningen om tegnsetting er ikke låst med en test | low | Stemmer, bare «Annonsen!» er testet. En ny testverdi med «C++»/«C#» → patch |
| 10 | blind | Ingen webtest for Korrektur med nytt gyldig brev ved gjenbruk | low | Ruten har ingen gren for modus i gjenbruken, og kjernen er testet for brevet (`test_okt.py`) → avvist |
| 11 | blind | Ingen test for gjenbruk etter modusbytte | false | `velg_modus` beholder listen (testet i `test_okt.py:107`), og gjenbruk med lik tekst er testet i `test_resultat.py` |
| 12 | blind | Lykkes nøkkelordene og gap feiler i vanlig analyse, kastes listen | medium | Stemmer, men slik var det før 7.3 også → defer (`deferred-work.md`) |
| 13 | blind | Spec-seksjoner, sprint-status og retro-punkt 15 er ikke oppdatert | false | Gjøres i slutten av arbeidsflyten. Retro-punkt 15 settes til `done` når storyen er ferdig |

## Design Notes

- Valget ligger i kjernen, ikke i ruten: ruten spør bare «finnes listen?». Da gjelder samme regel for «Tilbake» til modusvalget og for «Sjekk».
- `kall` er 1 ved gjenbruk, fordi grensen skal hindre kall som faktisk gjøres. Med 2 ville brukeren fått meldingen selv om det var plass.

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine, i testmodus: case 1 til resultatsiden, «Tilbake», legg til tomme linjer i CV-en, «Sjekk CV-en min» → samme resultatside som før. Endre annonsen → feilen for testdata som før.
- Valgfritt med ekte KI (ett gap-kall, under 1 kr): legg til et manglende nøkkelord i CV-en → samme liste, høyere prosent.
