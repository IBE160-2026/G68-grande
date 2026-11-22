---
title: 'Story 4.5: Et testcase til, og kriterium 3'
type: 'feature'
created: '2026-11-14'
baseline_commit: 'bdc1c3274240bc37764b0fefb635fce83fb549d4'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nettsiden er bare prøvd på én CV og én annonse (case 1), så suksesskriteriene kan holde for ett eksempel og ikke andre (NFR-3). Kriterium 3 (samme CV mot to annonser) er ikke testet, og testmodus tåler ikke flere caser: svarene kan blandes, testene gjelder bare case 1, manglende testdata gir uklare feil, og CV og annonse fra ulike caser gir en misvisende tekst (retro Epic 2, A4).

**Approach:** Claude lager utkastet til `testdata/case-2-okonomi/` (CV, annonse, fasit), Kristine godkjenner, og skriptet lager `ki-svar/` med ekte KI. Testmodus sjekker at casene er unike og at filene finnes, og gir en egen tekst for CV og annonse fra ulike caser. Kriterium 1, 11 og 14 kjøres tre ganger på case 2, og kriterium 3 tre ganger med CV-en fra case 1 mot annonsen fra case 2. Alt står i testplanen.

## Boundaries & Constraints

**Always:** Alt i case 2 er fiktivt (navn, firma, skoler, `@example.com`). CV-en og annonsen i case 2 er ulike case 1 (vasket, AD-10). Ingen ekte KI-kjøring før Kristine har godkjent utkastet til testdataene. Kriteriene kjøres tre ganger, alle tre må bestå, og plan B er som i 4.4 (prompten forbedres én gang, alle tre kjøres på nytt). Endres en prompt, kjøres også case 1 tre ganger på nytt, så alle svarene i testmodus er fra samme prompter. Resultatet står i testplanen også når noe feiler. Testene kaller aldri det ekte API-et. Hver test nevner FR-nummeret.

**Never:** Ikke Korrektur eller `eget-brev.txt` (Epic 5). Ikke håndredigering av `ki-svar/`. Ingen endring i promptene uten plan B. Ingen ny case 3.

**Beslutning (Kristine, 2026-11-14):** case 2 er økonomi med litt overlapp mot CV-en i case 1: en økonomistudent som søker en stilling som junior økonomimedarbeider i et regnskapsbyrå (for eksempel regnskap, Excel og Power BI, men også kundekontakt og norsk og engelsk). Mappen heter `case-2-okonomi`.
**Beslutning (Kristine, 2026-11-14):** teksten når CV og annonse er fra ulike caser er «Stillingsannonse: I testmodus må CV-en og annonsen være fra samme mappe i backend/testdata/.» (på annonsefeltet).
**Beslutning (Kristine, 2026-11-14):** Claude kjører skriptet (ca. 8–9 kr, og ca. 8 kr til ved plan B). Brevene med CV og annonse fra case 1 gjenbrukes fra runde 2 i story 4.4 når promptene er uendret.
**Beslutning (Kristine, 2026-11-14):** spec-en beholdes samlet (ca. 2500 tokens).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Riktig par | CV og annonse fra case 2 i testmodus | resultatsiden med prosenten fra fasiten i case 2 | – |
| Ulike caser | CV fra case 1, annonse fra case 2 | «Stillingsannonse: I testmodus må CV-en og annonsen være fra samme mappe i backend/testdata/.» | ingen KI-kall |
| Egen tekst | ukjent CV eller annonse | som før: `ikke_testdata` | – |
| Mangler fil | en case-mappe uten `cv.txt` eller `annonse.txt` | appen starter ikke, og feilen nevner mappen og fila | `TestdataFeil` |
| Mangler mappe | `testdata/` finnes ikke eller har ingen `case-*` | appen starter ikke, og feilen nevner mappen | `TestdataFeil` |
| Like caser | to caser med samme vaskede CV eller annonse | appen starter ikke, og feilen nevner begge casene | `TestdataFeil` |
| Skriptet, ett case | `--case case-2-okonomi` | bare det caset kjøres | ukjent navn: melding og feilkode |
| Skriptet, annen mappe | `--testdata MAPPE` | casene i MAPPE kjøres | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/ki.py:68-79,82-93` -- `les_testcaser` og `TestKI`. `les_testcaser` gir `TestdataFeil` (ny, i samme fil) for mappe som mangler, ingen `case-*`, fil som mangler og like vaskede CV-er eller annonser. `nokkelord` velger fortsatt case ut fra annonsen: med unike annonser er det samme case som `gap` (docstring). Docstringen øverst sier fortsatt «håndlagde svarene» (utsatt fra 4.4).
- `backend/soknad/kjerne/testdata_match.py:37-57` -- `finn_case`. Er CV-en kjent og annonsen annonsen i et annet case, gir den den nye feiltypen i stedet for `ikke_testdata`. Resten er uendret.
- `backend/soknad/kjerne/feil.py:7-17` -- ny `FeilType.ANNEN_CASE = "annen_case"`.
- `backend/soknad/web/tekster.py:271-276` -- ny tekst for `("annonse", FeilType.ANNEN_CASE)`. `tests/web/test_tekster.py` sjekker tekstene.
- `backend/soknad/__init__.py:65` -- `TestKI()` ved oppstart. Her stopper `TestdataFeil` appen, ingen endring.
- `backend/scripts/lag_testsvar.py:53-95` -- nye valg `--case NAVN` og `--testdata MAPPE`. `main(argv, testdata)` og alt-eller-ingenting per case beholdes.
- `backend/tests/test_testdata.py` -- `CASE` blir en parametrisering over alle `case-*` (minst to). `VIKTIGE_NOKKELORD` og `SJEKKLISTE_ORD` blir per case. Ny test for unike CV-er og annonser.
- `backend/tests/adaptere/test_ki.py`, `tests/kjerne/test_testdata_match.py`, `tests/scripts/test_lag_testsvar.py` -- nye tester for feilene og valgene. Lages i kopier i `tmp_path`, aldri i `testdata/`.
- `backend/testdata/case-1-utvikler/fasit.md` -- mal for fasiten i case 2 (Krav, Viktige nøkkelord, Nøkkelord, «X av Y = Z %», Sjekkliste for brevet).
- `_bmad-output/planning-artifacts/architecture/architecture-kode-prosjekt-2026-11-04/ARCHITECTURE-SPINE.md:188` (AD-10) og `ux-designs/*/EXPERIENCE.md:142` -- den nye feiltypen og teksten.
- `README.md:74,98` og `my-project/testplan.md` -- case 2, at Korrektur testes med case 1, og resultatene.

## Tasks & Acceptance

**Execution:**
- [x] `backend/testdata/case-2-okonomi/cv.txt`, `annonse.txt`, `fasit.md` -- utkast fra Claude med tydelige hull, viktige nøkkelord og sjekkliste. **Stopp og vis Kristine før KI-kjøringen** -- NFR-3, AD-10.
- [x] `backend/soknad/kjerne/feil.py`, `kjerne/testdata_match.py`, `web/tekster.py` -- `ANNEN_CASE` og teksten -- FR-34.
- [x] `backend/soknad/adaptere/ki.py` -- `TestdataFeil` i `les_testcaser`, docstringene -- FR-34, FR-38.
- [x] `backend/scripts/lag_testsvar.py` -- `--case` og `--testdata` -- FR-38.
- [x] Tester for alle radene i matrisen, og `tests/test_testdata.py` for alle caser, også kriterium 2 -- FR-17, FR-34, FR-38.
- [x] Kjør skriptet (Claude): kjøring 1 `--case case-2-okonomi` skriver `ki-svar/`, kjøring 2 og 3 med `--ut ../my-project/testkjoringer/4-5/case-2/kjoring-<n>`. Kriterium 3: `--testdata` mot en mappe i `my-project/testkjoringer/4-5/kriterium-3/` med CV-en fra case 1 og annonsen fra case 2, tre ganger. `logg.txt` i hver kjøringsmappe.
- [x] `fasit.md` i case 2 -- tabellen «Nøkkelord» og prosenten etter kjøring 1 -- FR-17.
- [x] `my-project/testplan.md` -- case 2 (kriterium 1, 11, 14, prosent, kostnad) og kriterium 3 (brevene mot hver annonse, med de annonsespesifikke kravene) -- NFR-12, FR-22.
- [x] `README.md`, AD-10, `EXPERIENCE.md` -- case 2, Korrektur bare med case 1, den nye teksten -- NFR-8.

**Acceptance Criteria:**
- Gitt hele testsuiten uten `ANTHROPIC_API_KEY`, når `uv run pytest` kjøres, så går alt gjennom uten nettverk.
- Gitt case 2 i testmodus i nettleseren, når CV og annonse fra case 2 limes inn, så vises resultatsiden og brevet fra `ki-svar/` i case 2.

## Design Notes

Unike annonser gjør at `nokkelord(annonse)` alltid treffer samme case som `gap(cv, annonse)` når `finn_case` har godtatt paret, så signaturen i AD-3 kan stå. Sjekken skjer ved oppstart, så en feil i testdataene merkes med en gang i stedet for som en KI-feil midt i flyten. Kriterium 3 bestås når hvert brev nevner minst ett krav som bare står i sin egen annonse, og ingen brev påstår noe som ikke står i CV-en.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

**Manual checks (if no CLI):**
- Kristine: case 2 i testmodus i nettleseren, og CV fra case 1 med annonse fra case 2 gir den nye teksten på annonsefeltet.

## Implementation Notes

- Implementert direkte i hovedøkta (ingen underagent), som i 4.4, fordi Kristine skulle godkjenne testdataene midt i arbeidet og de ekte KI-kjøringene måtte gjøres her.
- Testdataene: Kristine åpnet filene i Notisblokk og godkjente utkastet uendret (14. november 2026).
- `TestdataFeil` ligger i `adaptere/ki.py` og gis av `les_testcaser`. Mappe som ikke finnes og mappe uten `case-*` gir samme melding («Fant ingen testcaser … i <mappe>»). En `ki-svar/`-fil som mangler, gir fortsatt `KIFeil(annet)` når den trengs (uendret).
- `finn_case` gir `annen_case` bare når CV-en er kjent og annonsen er annonsen i et annet case. Er CV-en ukjent, gjelder `ikke_testdata` på CV-en som før.
- Skriptet: ny feilkode 3 (`UKJENT_CASE`). `--case` sjekkes før nøkkelen leses.
- `tests/test_testdata.py` er parametrisert over alle `case-*` med `per_case`. `_tabell` stopper nå også ved neste `## `-overskrift. Ny webtest for case 2 i `tests/web/test_resultat.py` (resultatsiden og brevet).
- Uventet: Python skrev loggen med Windows-tegnkoding når utskriften gikk gjennom `tee`. Loggen fra den første kjøringen ble gjort om til UTF-8 med `iconv`, og resten ble kjørt med `PYTHONIOENCODING=utf-8`.
- Runde 1 (kl. 17.24–17.32): case 2 besto kriterium 1, 11 og 14 alle tre gangene. Kriterium 3 besto på de annonsespesifikke kravene, men Kristine bestemte at «Python er språket jeg har jobbet mest med» og «min første faste jobb» er brudd på kriterium 11. Plan B: ny regel i `prompts/brev.md`, med test i `tests/adaptere/test_ekte_ki.py`.
- Runde 2 (kl. 17.33–17.44): fordi prompten ble endret, ble case 1, case 2 og kriterium 3 kjørt tre ganger hver på nytt (Always-regelen). Alt besto. `ki-svar/` for begge casene er fra runde 2, kjøring 1, og nøkkelordtabellene er oppdatert (case 1: 10 av 20 = 50 %, case 2: 7 av 16 = 44 %). Mappene er `my-project/testkjoringer/4-5/runde-1/` og `runde-2/`, og inndataene for kriterium 3 ligger i `4-5/inndata/`.
- Kostnad: ca. 24 kr for femten kjøringer, mer enn anslaget (8–9 kr pluss ca. 8 kr for plan B), fordi kriterium 3 også måtte kjøres på nytt. Står i testplanen.
- AD-10 og feiltekst-tabellen i EXPERIENCE er oppdatert både i `_bmad-output/planning-artifacts/` (ikke i Git) og i kopiene i `my-project/5-arkitektur/` og `my-project/3-ux/`.
- 786 tester grønne.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | verifisering | Ingen hull i testene | – | Ingen funn. 364 tester i de berørte filene gikk gjennom. |
| 2 | kant | `cv.txt` eller `annonse.txt` som ikke er UTF-8, gir `UnicodeDecodeError` ved oppstart, ikke `TestdataFeil` | low | Sant, men testdataene er UTF-8 og sjekkes av ruff og testene. Rettingen er en ny gren. Avvist. |
| 3 | kant | En tom `cv.txt` gir tom vasket tekst, og da kan innlimt tegnsetting matche caset | low | Sant i teorien, men ingen testfil er tom, og `test_testdata.py` krever innhold. Ny vakt avvises. |
| 4 | kant | Med API-nøkkel starter ikke nettsiden når testdataene er ødelagt | low | Bevisst: Design Notes sier at sjekken skjer ved oppstart, og `testdata/` ligger alltid i repoet. Avvist. |
| 5 | kant, blind | `--testdata` til en tom mappe, eller `--case ""`, gir kode 0 uten melding | low | Sant, og `--testdata` er nytt i denne storyen. Direkte retting: samme sjekk som for `--case` gjelder nå alltid. Patch: melding og kode 3, med ny test. |
| 6 | kant | En case-mappe under `--testdata` uten `cv.txt` stopper hele kjøringen med traceback | low | Fantes før (4.4, funn 10, avvist). Feilen er tydelig. Avvist igjen (første gang i en ny story, ikke samme funn i to stories). |
| 7 | kant | `ANNEN_CASE` på et annet felt enn annonsen gir `KeyError` | false | `finn_case` gir `ANNEN_CASE` bare for `felt="annonse"`, og det er den eneste veien. |
| 8 | kant | Testen for svarene fra hvert case leser også en fil som heter `case-*` | low | Direkte retting. Patch: `is_dir()` som i resten av koden. |
| 9 | kant, blind | README sier at nettsiden ikke starter når «en fil» mangler, men `ki-svar/` sjekkes ikke ved oppstart | low | Sant. Patch: README sier hvilke filer som sjekkes, og hva som skjer når en fil i `ki-svar/` mangler. |
| 10 | kant | Spec-en nevner `4-5/kriterium-3/` og `case-2/kjoring-<n>`, men mappene ble `inndata/`, `runde-1/` og `runde-2/` | low | Rettingen er en endring i spec-en. Avvist. Mappene står i testplanen og i Implementation Notes. |
| 11 | blind | Kjøringene i `runde-1/` og `runde-2/` står ikke i diffen | false | De ble tatt ut av diffen til gjennomgangen med vilje (rå KI-svar), men de er ikke ignorert og blir committet. |
| 12 | blind | README sier 1,2–1,7 kr per testcase, men en kjøring kostet opptil 1,81 kr | low | Sant. Patch: 1,2–1,8 kr. |
| 13 | blind | Sjekklisteordene for case 2 dekker ikke punktene om graden og tidligere jobb, men docstringen sier «ingenting fra sjekklisten» | low | Sant (gjelder også case 1). Patch: docstringen sier hvilke ord som søkes, og at de to punktene sjekkes for hånd. |
| 14 | blind | Søket på deler av ord kan feile på riktige brev («lønnsom», «opplæring i regnskapsprogrammene») | low | Sant. Testen er streng med vilje (Design Notes i 4.4). Patch: docstringen forklarer det, og at brevet vurderes for hånd før plan B. |
| 15 | blind | Ingen fasit for CV-en fra case 1 mot annonsen fra case 2, og gap-analysen sier at kundekontakt mangler | low | Sant, men kriterium 3 krever ingen fasit, og motsigelsen står i testplanen. Avvist. |
| 16 | blind | Kopiene i `4-5/inndata/` har ingen test som sikrer at de er like testdataene | low | Sant. Patch: `test_fr22_inndataene_for_kriterium_3_er_like_testdataene`. |
| 17 | blind | Testplanen blander kriterium 3 og 11, og sier at «case 1» besto igjen etter plan B | low | Sant. Patch: raden for kriterium 3 sier at de annonsespesifikke kravene besto i begge rundene, og raden for kriterium 11 skiller case 1, case 2 og kombinasjonen. |
| 18 | blind | Eksemplene i plan B-regelen er tatt fra brevene som feilet, og runde 2 brukte samme CV | medium | Sant. Prompten endres ikke uten Kristine. Patch: svakheten står i testplanen, med forslag om å prøve med Canva-CV-en. |
| 19 | blind | Noen slutninger i de nye svarene i testmodus («over et helt år», «har laget», «webtjeneste») står som bestått uten kommentar | low | Sant. Patch: listet i testplanen som «venter på Kristines vurdering». |
| 20 | blind | `test_fr32_testki_gir_de_handlagde_svarene` heter fortsatt «håndlagde» | low | Direkte retting. Patch: testen heter `…_ferdige_svarene`. |
| 21 | blind | Testen for hvert case sjekker ikke `brev-2`, og webtesten for case 2 sjekker ikke gap-analysen | low | Direkte retting. Patch: begge sjekkes. |
| 22 | blind | Korrektur med CV og annonse fra case 2 er verken bestemt eller testet | low | Utenfor intensjonen («Ikke Korrektur», Epic 5). Defer til story 5.1 i `deferred-work.md`. |
