---
title: 'Story 4.4: Ekte KI-svar i testmodus'
type: 'feature'
created: '2026-11-14'
baseline_commit: '21a158d75769878caf7df93c0d3b3b2911a77463'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** De ferdige svarene i testmodus (`testdata/case-1-utvikler/ki-svar/`) er håndlagde, så testmodus viser ikke hvordan nettsiden virker med ekte KI (FR-38). Kriterium 1, 11 og 14 er heller ikke prøvd med ekte KI, og det finnes ingen testplan.

**Approach:** Et nytt skript `backend/scripts/lag_testsvar.py` kjører `EkteKI` på hvert testcase og skriver `nokkelord.json`, `gap.json`, `brev-1.json` og `brev-2.json`. Fasiten får de viktige nøkkelordene og en ny nøkkelordtabell, og `my-project/testplan.md` får resultatet av tre kjøringer med tokens og kroner per søknad.

## Boundaries & Constraints

**Always:** Filene har bare objektet fra AD-4 (svaret fra `kontroller`), UTF-8 med `ensure_ascii=False`, innrykk 2 og linjeskift til slutt. Et testcase der et KI-kall feiler, skrives ikke (alt eller ingenting per case), og skriptet ender med feilkode. Uten nøkkel skriver skriptet en melding og kaller ingen KI. Loggen viser bare oppgave, tokens og pris (som i dag). Testene kaller aldri det ekte API-et. Alle testene som bruker testdataene, går gjennom med de nye svarene. Kriteriene kjøres tre ganger, og alle tre må bestå. Feiler én, forbedres prompten én gang og alle tre kjøres på nytt (plan B, PRD del 5). Resultatet står i testplanen også når noe feiler.

**Never:** Ingen endring i `adaptere/ki.py`, `kjerne/` eller weblaget. Ikke case 2 eller kriterium 3 i praksis (4.5). Ikke Korrektur (Epic 5). Ikke håndredigering av filene i `ki-svar/`.

**Beslutning (Kristine, 2026-11-14):** de viktige nøkkelordene i case 1 er Python, HTML, CSS, SQL, Git, Linux, Docker og førerkort. Flask og Scrum («gjerne») og norsk og engelsk er ikke viktige.
**Beslutning (Kristine, 2026-11-14):** Claude kjører skriptet tre ganger med nøkkelen i `backend/.env` (ca. 8 kr, mer ved plan B), sjekker svarene mot fasiten og skriver utkastet til testplanen. Kristine sjekker.
**Beslutning (Kristine, 2026-11-14):** testplanen har radene for kriterium 3 og 12, merket «testes i story 4.5» og «testes i Epic 5».
**Beslutning (Kristine, 2026-11-14):** spec-en beholdes samlet (ca. 1900 tokens).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Vanlig kjøring | nøkkel i `backend/.env` | fire filer i `ki-svar/` per case, tokens og pris i terminalen | – |
| `--ut MAPPE` | samme | filene i `MAPPE/<case>/`, `ki-svar/` er uendret | – |
| Uten nøkkel | `ANTHROPIC_API_KEY` mangler | melding som viser til README, feilkode | ingen KI-kall |
| KI-feil | ett kall i et case feiler | caset skrives ikke, feiltypen vises, de andre casene kjøres | feilkode til slutt |
| æøå | svar med «førerkort» | står som æøå i fila, ikke `ø` | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/ki.py` -- `EkteKI(api_nokkel, modell)`, `nokkelord`/`gap`/`brev(cv, annonse, forslag)`, logger tokens og pris på INFO i `soknad.adaptere.ki`. Brukes uendret.
- `backend/soknad/__init__.py:40,52-53` -- `load_dotenv(ENV_FIL, override=False, encoding="utf-8")`, `ANTHROPIC_MODEL` eller `STANDARD_MODELL`. Skriptet gjør det samme.
- `backend/pyproject.toml` -- prosjektet installeres ikke som pakke (`pythonpath = ["."]` bare for pytest), så skriptet kjøres med `uv run python -m scripts.lag_testsvar` fra `backend/`.
- `backend/testdata/case-1-utvikler/` -- `cv.txt` og `annonse.txt` sendes urørt. `fasit.md`: avsnittet om håndlagde svar, tabellen «Nøkkelord» (må ha nøkkelordene i samme rekkefølge som `nokkelord.json`, med Ja/Nei satt etter CV-en) og «X av Y = Z %». «Krav» og sjekklisten endres ikke.
- `backend/tests/test_testdata.py` -- leser svarene dynamisk. `test_fr17_fasiten_gir_samme_treff_og_prosent_som_telleregelen` krever ny tabell. `test_fr37_testbrevet_har_ingen_pastander_fra_sjekklisten` sjekker bare `brev-1.json`. `_tabell` kan gjenbrukes for en ny liste.
- `backend/tests/adaptere/test_ki.py:69-78` -- `test_fr28_brevfil_som_mangler_gir_kifeil_annet` regner med at `brev-2.json` mangler. Må slette den i kopien først.
- `backend/tests/web/hjelpere.py:23-27`, `tests/web/test_brev.py:37` -- leser svarene fra filene, tåler nye svar.
- `README.md:74,102` -- «håndlagde KI-svar».

## Tasks & Acceptance

**Execution:**
- [x] `backend/scripts/lag_testsvar.py` -- skriptet med `--ut`, alt eller ingenting per case, logging på INFO bare for `soknad` -- FR-38, AD-4.
- [x] `backend/tests/scripts/test_lag_testsvar.py` -- alle radene i matrisen med en falsk KI laget i fila -- FR-38.
- [x] Kjør skriptet (Claude): kjøring 1 skriver `ki-svar/`, kjøring 2 og 3 med `--ut ../my-project/testkjoringer/4-4/kjoring-<n>`.
- [x] `backend/testdata/case-1-utvikler/fasit.md` -- teksten om svarene, «Viktige nøkkelord», ny tabell «Nøkkelord» og prosent -- FR-15, FR-17.
- [x] `backend/tests/test_testdata.py`, `tests/adaptere/test_ki.py` -- de viktige nøkkelordene står i `nokkelord.json`, `brev-2.json` finnes, sjekklisten gjelder begge brevene, og rettingen i `test_fr28` -- FR-15, FR-24, FR-37, FR-38.
- [x] `my-project/testplan.md` -- ny fil: hvordan kriteriene testes, resultat per kjøring for kriterium 1, 11 og 14, tokens og kr per fullført søknad (nøkkelord + gap + brev, mål under 3 kr), plan B, og en rad for Canva-CV-en som Kristine fyller inn -- NFR-12, NFR-11.
- [x] `README.md` -- testsvarene er ekte KI-svar, og hvordan skriptet kjøres og hva det koster -- NFR-8, FR-38.

**Acceptance Criteria:**
- Gitt hele testsuiten uten `ANTHROPIC_API_KEY`, når `uv run pytest` kjøres, så går alt gjennom uten nettverk.
- Gitt de nye svarene i testmodus, når hele flyten kjøres i nettleseren, så vises resultatsiden og brevet som før, med prosenten fra fasiten.

## Design Notes

En fullført søknad er nøkkelord + gap + ett brev (`brev-2` er «Nytt forslag» i Epic 7 og regnes for seg). Tokens og kroner hentes fra linjene `KI-kall … anslått … kr` i terminalen. Kriterium 1 og 11 sjekkes for hånd mot «Krav» og sjekklisten. Kriterium 14 sjekkes mot «Viktige nøkkelord». Sjekklistetesten er streng med vilje: nevner et brev SQL, Docker, Scrum eller førerkort, også ærlig, er det plan B.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

**Manual checks (if no CLI):**
- Kristine: testmodus i nettleseren med case 1, og Canva-CV-en med ekte KI (noteres i testplanen).

## Implementation Notes

- Implementert direkte i hovedøkta (ingen underagent), fordi de ekte KI-kjøringene uansett måtte gjøres her.
- Skriptet bruker `soknad.ENV_FIL` og `soknad.sett_opp_logg()` fra appen. `ENV_FIL` leses når `main` kjøres (ikke ved import), så den autouse-fiksturen `ingen_ekte_env` i `tests/conftest.py` også beskytter skripttestene mot den ekte `.env`. `main(argv, testdata)` tar testdata-mappen som parameter, så testene aldri skriver i den ekte `testdata/`.
- Feilkoder: 1 når et case ikke ble skrevet, 2 når nøkkelen mangler.
- Tre ekte kjøringer 14. november kl. 13.42–13.50 (ca. 4 kr i alt). Kjøring 1 ble `ki-svar/`. `gap.json` ble lik den gamle, så den står ikke som endret i Git.
- Kriterium 14: et viktig nøkkelord regnes som med når det står som eget ord i et av nøkkelordene (KI-en skrev «førerkort klasse B»). Regelen står i `fasit.md` og i testen.
- Nye tabeller i fasiten: «Viktige nøkkelord» og «Nøkkelord» (19 ord, 9 av 19 = 47 %). Ja/Nei er sjekket mot CV-en og er lik telleregelen.
- Uventet: to tester i `tests/web/test_resultat.py` hadde 64 % og (7)/(4) skrevet inn. De leser nå tallene fra fasiten.
- Kriterium 11: ingen brev påstår noe fra sjekklisten. Små utbroderinger (Linux «fra studiet», «til daglig», «travle perioder») og en ærlig omtale av SQL i `brev-2` i kjøring 2 står som merknader i testplanen. Kristine avgjør om de er brudd (da plan B). Design Notes sier at en ærlig omtale gir plan B, men det gjelder sjekklistetesten på `ki-svar/`, og `brev-2` i kjøring 2 er ikke der.
- Akseptansekriteriet om nettleseren er dekket av webtestene med testdataene, men Kristine prøver det selv.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | blind | Testplanen sier at kriterium 11 er bestått før Kristine har vurdert merknadene | low | Sant. Patch: statusen sier nå «venter på Kristines vurdering». |
| 2 | blind | Merknadene under kriterium 11 er ufullstendige og ujevne (flere utledede egenskaper er ikke nevnt) | low | Sant, jeg hadde bare tatt med noen. Patch: merknadene er delt i fakta som ikke står i CV-en og egenskaper lest ut av en jobb, med alle tilfellene. «Samarbeid og prosjektarbeid» er lov etter prompten, og det står nå. |
| 3 | blind | Sjekklistetesten er strengere enn kriterium 11, og README sier at bare nøkkelordtabellen må oppdateres etter en ny kjøring | low | Sant (`brev-2` i kjøring 2 nevner SQL ærlig). Patch: README sier at brevtestene kan feile (plan B), og testplanen spør Kristine om en ærlig omtale er lov. Testen beholdes streng (Design Notes). |
| 4 | blind | Prosenten per kjøring står ikke i testplanen, og den varierer (kjøring 3 gir 50 %) | low | Sant. Patch: ny rad i resultattabellen. |
| 5 | blind | Fallet fra 64 % til 47 % («bachelorgrad», «informatikk») er ikke drøftet | low | Sant. Patch: et avsnitt i testplanen som viser til de kjente begrensningene i README. Ingen endring i prompten uten Kristine. |
| 6 | blind | Begrunnelsen for de viktige nøkkelordene mangler for graden og språkene, og kommentaren mangler år | low | Sant. Patch: `fasit.md` sier at Kristine valgte de åtte ferdighetene, verktøyene og sertifikatet, og at graden og språkene ikke er med. Året er lagt til i testen. |
| 7 | blind | Kjøring 1 ligger bare i `ki-svar/` og blir borte ved neste kjøring, og at `gap.json` er uendret er ikke forklart | low | Sant. Patch: kjøring 1 er kopiert til `my-project/testkjoringer/4-4/kjoring-1/`, og testplanen forklarer `gap.json`. |
| 8 | blind | Modell, tid, tokens og pris lagres ikke sammen med kjøringen, og README-eksemplet følger ikke mappeoppsettet | low | Sant. Patch: `logg.txt` med terminalutskriften i hver kjøringsmappe, og eksemplet i README er `testkjoringer/<story>/kjoring-<n>`. Ingen ny loggfil fra skriptet (AC sier «fra loggen»). |
| 9 | blind, kant | Ingen `case-*`-mapper gir ingen utskrift og feilkode 0 | low | Sant, men `testdata/` er alltid standard og har case 1. Rettingen er en ny gren. Avvist. |
| 10 | blind, kant | Mangler `cv.txt` eller `annonse.txt`, eller kommer et annet unntak enn `KIFeil`, stopper hele kjøringen med traceback | low | Sant, men feilen er tydelig og skjer ikke med testdataene. Rettingen er ny feilhåndtering. Avvist. |
| 11 | blind, kant | `skriv_svar` skriver filene én og én, så en skrivefeil kan gi en blanding, og kommentaren lover mer | low | Sant for kommentaren. Patch: kommentaren sier nå at det gjelder KI-feil, og at en skrivefeil kan gi en blanding. Midlertidige filer er ny kompleksitet og avvises. |
| 12 | blind, verifisering, kant | Docstringen i `test_fr16_nokkelordlistene_som_i_fasiten` sier (7) og (4), og `test_ki.py` sier «håndlagde» | low | Sant. Patch: begge docstringene. |
| 13 | kant | Docstringen i `adaptere/ki.py` sier «håndlagde svarene» | low | Sant, men spec-en sier «ingen endring i `adaptere/ki.py`». Defer til 4.5, som endrer `ki.py`. |
| 14 | blind, kant | `re.search(...).groups()` på modulnivå gir en uklar `AttributeError` hvis prosentlinjen mangler | low | Sant. Direkte retting. Patch: `assert` med melding. |
| 15 | blind | Avsnittet om Canva-CV-en sier ikke at personopplysninger ikke skal i repoet | medium | Sant, og det er Kristines ekte CV. Patch: en setning i testplanen. |
| 16 | blind | Overskriften har «Junior» med stor J i fem av seks brev | low | Sant, KI-en følger annonsen. Krever endring i prompten, som er Kristines valg. Patch: merknad i testplanen, med plan B. |
| 17 | verifisering | Ingen test av at skriptet bruker `STANDARD_MODELL` når `ANTHROPIC_MODEL` er tom (som i `.env.example`) | medium | Gap fra verifiseringslaget. Patch: ny test `test_fr38_main_bruker_standardmodellen_naar_modellen_er_tom`. |
| 18 | verifisering | `load_dotenv` i testen legger `ANTHROPIC_API_KEY` i miljøet uten at monkeypatch rydder opp | low | Sant. Direkte retting. Patch: hjelperen `_env_fil` registrerer variablene i monkeypatch først. |
| 19 | kant | `ANTHROPIC_MODEL` med bare mellomrom brukes som modellnavn | low | Sant, men usannsynlig, og nettsiden (`soknad/__init__.py`) gjør det samme. Avvist for å holde dem like. |
| 20 | kant | `scripts/` har ingen `__init__.py`, så en vanlig pakke med navnet `scripts` kan skygge for den | low | Ingen slik pakke i `.venv` (sjekket), og `tests/` bruker heller ingen `__init__.py`. Avvist. |
