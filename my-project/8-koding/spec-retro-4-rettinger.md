---
title: 'Rettinger fra retrospektiven for epic 4: KI-kallet på ett sted'
type: 'bugfix'
created: '2026-11-14'
status: 'done'
baseline_commit: 'a360947bc4c0929f3870519b1220915f5511ad96'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-retro-2026-11-14.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Retrospektiven for epic 4 (action item 1, godtatt av Kristine 2026-11-14) fant tre ting:
- Samtykkesjekken og valget av KI leser innloggingen hver for seg. En annen fane kan slå av testmodus mellom dem, og da sendes teksten til Claude uten samtykke (A1).
- KI-kallet er bygd to ganger i `ruter.py`, og Korrektur og «Nytt forslag» skal lage to ruter til (B1).
- En utlogget bruker på resultatsiden får «Noe gikk galt hos KI-tjenesten» i stedet for innloggingen (B2).

**Approach:** Én hjelper for KI-kallet, brukt av `innlegging()` og `resultat()`. Ruten leser innloggingen én gang og gir den til hjelperen. Hjelperen bruker den samme innloggingen til samtykket og valget av KI, og sender en utlogget bruker til innloggingen.

**Decision (Kristine, 2026-11-14):** Rettingene etter retro 4 er delt opp. Denne spec-en tar bare action item 1. Punkt 2–4 står i `deferred-work.md`.

## Boundaries & Constraints

**Always:**
- Ingen endring i hva brukeren ser, bortsett fra B2.
- Rekkefølgen er som før: feltfeil først, så samtykke, så plass.
- Telleren for KI-kall, opptatt og `erstatt_soknad` virker som før. Hvert kall telles når det startes, også når det feiler, og bare med ekte KI.
- Alle eksisterende tester går gjennom uendret. Unntaket er tester som kaller `ki()` eller `til_start_uten_samtykke()` direkte. De følger den nye signaturen og sjekker det samme.
- Hver testfil og testfunksjon nevner FR- eller NFR-nummeret. Ingen testfil henter noe fra en annen testfil.

**Never:**
- Ikke endre tekstene i `tekster.py`, grensene, promptene eller `kontroller`.
- Ikke ta med punkt 2–4 fra retrospektiven: SDK-testen, nettverkssperren, `med_nokkel`, kommentarene, surrogatene, README og målingen.
- Ikke endre `prompt-logg.md`, `todo.md` eller andre filer i `my-project/` før etter PR-en.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Testmodus slås av mellom sjekken og valget | testmodus på, intet samtykke, en annen fane slår av testmodus etter at samtykket er sjekket | samme KI som sjekken gjaldt for (TestKI), EkteKI kalles ikke | – |
| Utlogget på resultatsiden | `POST /resultat` med `handling=brev`, logget ut i en annen fane etter `login_required` | redirect til innloggingen, ingen KI-kall, søknaden uendret | – |
| Analyse og brev som før | testmodus av med samtykke, eller testmodus på | samme svar, redirect, teller og opptatt som i dag | KI-feil, ingen plass og uventet unntak gir det samme som i dag |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/ruter.py`:
  - `innlegging()` linje 171–206: `innlogging` (171) brukes til `caser` (176). Så kommer `til_start_uten_samtykke` (180), `ki()` (185), `per_kall`/`har_plass_til` (187–191) og blokken med opptatt, `try`, `except KIFeil` og `finally` (198–206).
  - `resultat()` linje 239–263 har samme blokk, men leser ikke innloggingen.
  - `ANALYSE_KALL`/`BREV_KALL` (51–52) og `_bruker_ekte_ki` (380–383) kan flyttes inn i eller ved siden av hjelperen.
  - `_vis_innlegging`/`_vis_resultat` (386, 403) viser feilen. `til_innloggingen` er importert alt.
- `backend/soknad/web/flyt.py:29–47` -- `ki()` og `til_start_uten_samtykke()` leser `gjeldende_innlogging()` selv. De tar nå innloggingen som parameter. Selve regelen er uendret: utlogget gir TestKI, og uten nøkkel gir det TestKI.
- `backend/tests/web/test_samtykke.py`:
  - Linje 300–321 kaller `ki()` direkte og følger den nye signaturen.
  - `ByttendeKI` og `test_fr32_testmodus_av_midt_i_analysen_gir_ikke_ekte_ki` (rundt 240–279) er mønsteret for testen av vinduet. Den nye testen slår av testmodus etter samtykkesjekken og før valget, med monkeypatch på samtykkefunksjonen.
- `backend/tests/web/hjelpere.py` -- `TellendeKI`, `FeilendeKI`, `app_med_nokkel` og `sett_soknad` brukes som før.
- `backend/tests/web/test_grenser.py` -- tester telleren, ingen plass og uventet unntak for begge rutene. Skal gå gjennom uendret.
- Testen for utlogging midt i «Sjekk CV-en min» (retro-punkt 10 fra epic 2) finnes for innleggingen. Den nye testen for resultatsiden legges ved siden av, med samme mønster.
- `backend/soknad/kjerne/okt.py:135–139` -- docstringen til `tell_ki_kall` sier at Korrektur og «Nytt forslag» må bruke `har_plass_til` og `tell_ki_kall`. Den skal nå si at de bruker hjelperen.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/web/flyt.py` -- `ki(innlogging)` og `til_start_uten_samtykke(soknad, innlogging)`.
- [x] `backend/soknad/web/ruter.py` -- én hjelper for KI-kallet. `innlegging()` leser innloggingen én gang og bruker den til både `caser` og hjelperen. `resultat()` leser innloggingen og sender en utlogget bruker til innloggingen.
- [x] `backend/soknad/kjerne/okt.py` -- docstringen til `tell_ki_kall`.
- [x] `backend/tests/web/test_samtykke.py` -- direkte kall følger signaturen. Ny test: testmodus slås av mellom samtykkesjekken og valget, og EkteKI kalles ikke.
- [x] Testfila for utlogging eller resultatsiden -- ny test: utlogget på `POST /resultat` gir redirect til innloggingen, ingen KI-kall og søknaden uendret.

**Acceptance Criteria:**
- Given koden etter rettingen, when man søker etter `til_start_uten_samtykke(`, `ki(` og `har_plass_til(` i `ruter.py`, then står kallene bare i hjelperen.
- Given en midlertidig `ruter.py` der hjelperen ikke sjekker samtykket (kopi først, satt tilbake etterpå), when testene kjøres, then feiler minst én test for hver av de to rutene.
- Given alle testene, when de kjøres, then er de grønne, og antallet er 789 pluss de nye.

## Design Notes

Hjelperen gjør stegene i samme rekkefølge som i dag:
1. samtykket
2. valget av KI
3. plass
4. opptatt
5. kallene, der hvert telles når det startes
6. `finally` med `erstatt_soknad(opptatt, tell_ki_kall(ferdig, kall))`

Ruten gir den det som er ulikt:
- antall kall
- arbeidet, en funksjon `valgt_ki → ny søknad`
- hvordan en feil vises (`_vis_innlegging` eller `_vis_resultat`, med `prov_pa_nytt=False` når det ikke er plass)
- siden etterpå

En liten innpakning av KI-en som teller hvert kall når det startes, er én grei måte å telle på. Korrektur (Epic 5) og «Nytt forslag» (Epic 7) skal bruke samme hjelper.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

## Implementation Notes

- Hjelperen er `_med_ki(soknad, innlogging, kall, arbeid, vis_feil, neste)` i `ruter.py`. Tellingen skjer i `_TelteKall`, en innpakning av KI-en som teller hvert metodekall når det startes (1 med ekte KI, 0 med TestKI). `_bruker_ekte_ki` er lagt inn i hjelperen. `vis_feil` er `partial(_vis_innlegging, soknad, feil=[])` eller `partial(_vis_resultat, lagret)`.
- `innlegging()` beholder sin egen sjekk for utlogget før `caser`, så feltfeil ikke vises for en utlogget bruker (ingen endring i det brukeren ser). `resultat()` leser innloggingen etter sjekken av knappen og gir den til hjelperen, som sender en utlogget bruker til innloggingen.
- Nye tester (792 = 789 + 3): `test_fr36_testmodus_av_mellom_samtykket_og_valget_gir_ikke_ekte_ki_i_analysen` og `..._i_brevet` i `test_samtykke.py` (monkeypatch på `ruter.til_start_uten_samtykke`), og `test_fr7_utlogget_for_brevkallet_gir_innloggingen` i `test_brev.py` ved siden av `test_fr7_utlogget_midt_i_brevkallet_gir_innloggingen`. Ekte utlogging sletter også søknaden, så «søknaden uendret» er sjekket som at ingen søknad er lagret for den gamle økt-id-en.
- Mutasjoner (kopi av `ruter.py` først, satt tilbake etterpå, `cmp` likt): uten samtykkesjekken i hjelperen feiler 4 tester, to for hver rute (blant dem `test_fr36_ingen_ki_kall_fra_innleggingen_uten_samtykke` og `..._fra_resultatsiden_uten_samtykke`). Med `ki(gjeldende_innlogging())` i stedet for `ki(innlogging)` feiler de to nye vindustestene. Uten sjekken for utlogget feiler den nye testen for resultatsiden.
- Etter gjennomgangen (funn 2, 6, 8, 14 og 15):
  - `_TelteKall` gir attributter som ikke kan kalles, uendret.
  - Docstringene i `flyt.py` og `resultat()` er rettet.
  - De to testene for vinduet sjekker også telleren, og brevtesten sjekker samtykket.
  - Ny test: `test_fr36_testmodus_av_etter_feltsjekken_gir_ikke_ekte_ki_i_analysen`. Den feiler når `innlegging()` gir `_med_ki` en ny `gjeldende_innlogging()` (prøvd med kopi, satt tilbake og sjekket med `cmp`).
  - 793 tester (789 + 4), og `ruff` er grønn.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-14), tre lag: blind, kanttilfeller og testhull.

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | blind | `arbeid` kan gjøre flere kall enn `kall` sier, så telleren kan gå over `MAKS_KI_KALL` | low | Sant for en framtidig rute, men analysen gjør 2 og brevet 1, som oppgitt. Rettingen er en ny vakt. Avvist. Korrektur og «Nytt forslag» får riktig antall når de lages. |
| 2 | blind, kant | `_TelteKall.__getattr__` pakker inn alle attributter, så `telte.caser` gir en funksjon og et kall teller som et KI-kall | low | Sant (`ruter.py`, `__getattr__`). Ingen `arbeid` leser attributter i dag, men docstringen lover bare metodene. Direkte retting. Patch: attributter som ikke kan kalles, gis uendret. |
| 3 | blind | `arbeid` får ikke søknaden som argument, og `_med_ki` har ingen typehint | low | Ingen feil i dag: begge lukningene bruker søknaden de ga til `_med_ki`. Rettingen er ny form på hjelperen. Avvist. |
| 4 | blind | Ingen test sikrer at nye ruter bruker `_med_ki` | low | Akseptkriteriet sjekker det med søk, og påminnelsen til Epic 5 og 7 står i `issues.md`. En kildetest er ny kompleksitet. Avvist. |
| 5 | blind | `til_start_uten_samtykke(soknad, None)` slipper gjennom | low | Samme regel som før (utlogget slapp gjennom også da), og `_med_ki` sender utlogget til innloggingen før sjekken. Avvist. |
| 6 | blind | Docstringene i `flyt.py` sier «Ruten gir», men det er `_med_ki` som kaller begge | low | Sant. Direkte retting. Patch. |
| 7 | blind | Innloggingen sjekkes på to måter (`innlegging()` selv, `resultat()` via `_med_ki`) | low | Bevisst: `innlegging()` trenger innloggingen til `caser` før feltfeilene, og steg 1 i `_med_ki` er sikringen for resten. Avvist. |
| 8 | blind | De nye testene for vinduet sjekker ikke telleren, og brevtesten sjekker ikke samtykket | low | Sant. Direkte retting. Patch: `ki_kall == 0` i begge, `samtykke is False` i brevtesten. |
| 9 | blind | `issues.md:115–116`, kopien av spec-en i `my-project/` og `action_items` er ikke oppdatert | low | Ikke en del av diffen med vilje (Never: `my-project/` etter PR-en). Gjøres når PR-en er laget og flettet. Avvist her. |
| 10 | blind | Docstringen til `tell_ki_kall` i `kjerne/` peker på weblaget | low | Spec-en ba om at docstringen viser til hjelperen (Tasks). Avvist. |
| 11 | kant | `arbeid` som gir `None`, får `finally` til å feile og søknaden blir opptatt | false | Begge `arbeid` gir alltid en `Soknad` (`sett_analyse`, `sett_brev`). En framtidig feil der ville feile høyt i testene. |
| 12 | kant | Utlogging i en annen fane etter at innloggingen er lest, men før kallet: teksten sendes likevel | low | Ekte KI krever at samtykket er gitt. Vinduet er det samme som før mellom valget og kallet, og bare noen få linjer. Rettingen er en ny sjekk. Avvist. |
| 13 | kant | To POST-er samtidig kan begge passere opptatt-sjekken, og kallene telles ikke | low | carried: samme som 4.3.2 funn 1, avvist der. Fantes før denne endringen. |
| 14 | kant | Docstringen til `resultat()` sier «etter login_required», men utlogging før stegsjekken gir siden for steget | low | Sant for ordlyden. Direkte retting. Patch: «etter stegsjekken». |
| 15 | testhull | Ingen test sikrer at `innlegging()` gir `_med_ki` den samme innloggingen som ble brukt til `caser` | low | Fra testhull-laget, med bevis. Patch: test som slår av testmodus rett etter `sjekk_innlegging`. |
