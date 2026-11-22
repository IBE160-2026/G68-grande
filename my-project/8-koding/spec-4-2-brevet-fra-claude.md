---
title: 'Story 4.2: Brevet fra Claude'
type: 'feature'
created: '2026-11-13'
status: 'done'
baseline_commit: '4d4d2f1a903b40b224f3e0151280ff5e0738fb6b'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `EkteKI` kan lage nøkkelord og gap-analyse, men ikke brevet. Det finnes ingen `prompts/brev.md` med reglene i FR-24 og FR-37, og `kontroller("brev")` godtar kontrolltegn, linjeskift og tab, som gjør at Word-fila feiler eller ikke er lik brevet på siden (retro-punkt 22, Epic 3). Tomme punkter og tom `arbeidsgiver` slipper også gjennom (retro-punkt 14, Epic 2).

**Approach:** `EkteKI.brev(cv, annonse, forslag)` sender bare CV og annonse med prompten `prompts/brev.md` og skjemaet `{avsnitt: [str]}`, gjennom den samme `_kall` og `kontroller` som i 4.1. `kontroller` renser brevteksten, fjerner tomme punkter i alle lister og gjør tom `arbeidsgiver` om til `None`. Nettsiden bruker fortsatt `TestKI` (4.3).

## Boundaries & Constraints

**Always:** Prompten er på norsk og inneholder FR-24 (norsk, formell og akademisk tone som gjør arbeidsgiveren oppmerksom og engasjert, ikke generisk KI-tekst, stillingen og arbeidsgiveren ved navn, minst to konkrete krav fra annonsen koblet til CV-en), alle 17 KI-frasene fra addendum med ordlyden derfra, og FR-37 (bare CV og annonse, ingen ny erfaring, utdanning eller ferdighet, omformulering og kobling til kravene er lov). CV og annonse er bare data, og instruksjoner i dem følges ikke (som i 4.1). Rensingen gjelder både `TestKI` og `EkteKI`. Testene bruker den falske klienten og kaller aldri API-et. Hver testfil og testfunksjon nevner FR-nummeret.

**Never:** Ingen endring i `web/` eller i `ki()` (4.3). Ikke `scripts/lag_testsvar.py` og ingen nye `ki-svar/*.json` (4.4). `forslag` sendes ikke til Claude (FR-37: bare CV og annonse). Ingen strømming, `temperature` eller `thinking`. Koden fra 4.1 (`_kall`, feilene, loggingen) skrives ikke om.

**Beslutning (Kristine, 2026-11-13, endret samme kveld):** brevet begynner med overskriften «Søknad på stillingen som …» som vanlig tekst i første avsnitt, og slutter med «Med vennlig hilsen» og navnet fra CV-en som egne avsnitt. `brev-1.json` får samme overskrift. Ingen dato, adresse eller tiltale.
**Beslutning (Kristine, 2026-11-13):** brevet er høyst én A4-side, omtrent 250–400 ord i 4–6 avsnitt (overskrift, hilsen og navn ikke medregnet).
**Beslutning (Kristine, 2026-11-13):** spec-en beholdes samlet (ca. 2400 tokens), fordi rensingen og brevet testes sammen med `kontroller` og `lag_docx`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Brev | CV, annonse, `forslag` 1 eller 2, gyldig svar | `{avsnitt: [...]}`, brukermeldingen har bare `<cv>` og `<annonse>` | – |
| Linjeskift og tab | avsnitt med `\n`, `\r` eller `\t` | blir ett mellomrom, flere mellomrom på rad blir ett | – |
| Kontrolltegn | avsnitt med for eksempel `\u000b` eller `\u0000` | tegnet fjernes, og `lag_docx` lager fila | – |
| Bare kontrolltegn | alle avsnitt blir tomme etter rensing | – | `KIFeil(ubrukelig_svar)` |
| Tomme punkter | `"  "` blant ekte punkter i `nokkelord`, `dekker`, `mangler` | punktet fjernes | – |
| Tom arbeidsgiver | `arbeidsgiver` er `""` eller bare mellomrom | `None` | – |
| Feil fra API-et | nettverk, tidsavbrudd, `refusal`, ugyldig JSON | – | som i 4.1 |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/ki.py` -- `SKJEMA` (legg til `brev`), `EkteKI.__init__` leser en prompt per nøkkel i `SKJEMA`, så `brev.md` leses automatisk. `_kall(oppgave, brukermelding)` brukes som den er. Brukermeldingen for brevet er den samme som i `gap`. `TestKI` endres ikke.
- `backend/prompts/nokkelord.md`, `gap.md` -- mønsteret for prompten: åpningen om merkene og at teksten bare er data, reglene i punkter og «Svar bare med JSON i formen fra skjemaet».
- `backend/soknad/kjerne/ki_svar.py` -- `kontroller` filtrerer alt tomme avsnitt for `brev`. Rensingen og fjerningen av tomme punkter legges her, før tom-sjekken og grensen `MAKS_NOKKELORD`.
- `backend/soknad/adaptere/fil_ut.py` -- `lag_docx(avsnitt)` gir `FilFeil` for tegn XML ikke tåler. Endres ikke.
- `backend/testdata/case-1-utvikler/ki-svar/brev-1.json` -- formen på et ferdig brev. `fasit.md` har sjekklisten for brevet (kriterium 11).
- `_bmad-output/planning-artifacts/prds/prd-kode-prosjekt-2026-10-09/prd.md` (FR-24, FR-37) og `addendum.md` («Til prompten for brevet») -- kravene og de 17 frasene.
- `backend/tests/adaptere/test_ekte_ki.py` -- `FalskKlient`, `_svar`, `_ki`, `_kall` (utvides med `brev`), og de parametriserte testene over `["nokkelord", "gap"]`.
- `backend/tests/kjerne/test_ki_svar.py`, `backend/tests/adaptere/test_fil_ut.py` -- her legges testene for rensingen og testen som kjører `kontroller` og `lag_docx` sammen.

## Tasks & Acceptance

**Execution:**
- [x] `backend/prompts/brev.md` -- norsk prompt med FR-24, FR-37, de 17 frasene og svarformen `avsnitt` (ett avsnitt per element, ren tekst uten markdown), begynnelsen og slutten og lengden fra beslutningene -- AD-14, NFR-10.
- [x] `backend/soknad/adaptere/ki.py` -- `SKJEMA["brev"]` = `{avsnitt: tekstliste}` med `additionalProperties: false`. `EkteKI.brev(cv, annonse, forslag)` kaller `_kall("brev", ...)` med bare `<cv>` og `<annonse>`. Docstringen sier at `forslag` ikke sendes, fordi hvert kall gir et nytt brev -- AD-3, AD-4, FR-37.
- [x] `backend/soknad/kjerne/ki_svar.py` -- i hvert avsnitt blir alt mellomrom (også `\n`, `\r`, `\t`) ett mellomrom, og kontrolltegn og andre tegn Word ikke tåler fjernes. Tomme punkter fjernes i `nokkelord`, `dekker` og `mangler`, og tom `arbeidsgiver` blir `None`. Docstringen oppdateres -- FR-28, FR-30.
- [x] `backend/tests/adaptere/test_ekte_ki.py` -- `brev` med i de parametriserte testene (kallet, feilene). Test at brukermeldingen bare har CV og annonse (ingen `forslag`), at skjemaet er `{avsnitt}`, at prompten nevner alle 17 frasene og at `TestKI` fortsatt er KI-en nettsiden bruker -- FR-37, FR-24, NFR-10.
- [x] `backend/tests/kjerne/test_ki_svar.py` -- tester for alle radene i matrisen som gjelder `kontroller` -- FR-28.
- [x] `backend/tests/adaptere/test_fil_ut.py` -- et brev med `\u000b`, `\n` og `\t` går gjennom `kontroller` og så `lag_docx` uten `FilFeil`, og avsnittene i fila er like avsnittene fra `kontroller` -- FR-30.
- [x] `backend/tests/test_testdata.py` -- ingen av de 17 frasene står i noen `ki-svar/brev-*.json` i noen case (uten hensyn til store og små bokstaver) -- FR-24.

**Acceptance Criteria:**
- Gitt `prompts/brev.md`, når den leses som utf-8, så inneholder den kravene i FR-24 og FR-37 og alle 17 frasene fra addendum.
- Gitt `EkteKI.brev(cv, annonse, 2)` og en falsk klient, så har kallet prompten fra `brev.md`, skjemaet `{avsnitt}` og en brukermelding med bare CV og annonse, og svaret har gått gjennom `kontroller`.
- Gitt hele testsuiten uten `ANTHROPIC_API_KEY`, når `uv run pytest` kjøres, så går alt gjennom uten nettverk.

## Design Notes

Kontrolltegn fjernes i stedet for å gi `ubrukelig_svar`, fordi et nytt kall kan gi samme tegn igjen, og tegnet ikke synes på siden uansett. Mellomrom slås sammen, fordi nettleseren viser flere mellomrom som ett, og da blir Word-fila lik siden. Tegn som må fjernes: kategori `Cc` (unntatt mellomrom-tegnene, som blir mellomrom), enslige surrogater (`Cs`, kan komme fra `\ud800` i JSON) og `￾`/`￿`.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne, også de gamle

## Implementation Notes

- En hjelpeagent kodet ut fra spec-en. Hovedøkta leste diffen, kjørte ruff og pytest (655 tester grønne) og la til en test for avkuttet eller avvist brev (`max_tokens`, `refusal`).
- `\u000b` fjernes, men `\t`, `\n` og `\r` blir mellomrom, som i matrisen. Annet mellomrom (for eksempel hardt mellomrom og U+2028) blir også et vanlig mellomrom.
- Tomme punkter fjernes før grensen på 30 nøkkelord sjekkes.
- Prompten sier at brevet slutter med bare «Med vennlig hilsen» når CV-en ikke har noe navn, så Claude ikke dikter opp et navn (FR-37).
- Listen med de 17 frasene står i både `test_ekte_ki.py` og `test_testdata.py`, fordi en testfil ikke kan hente noe fra en annen.
- Hjelperen `_cv_og_annonse` lager brukermeldingen for både `gap` og `brev`.

## Spec Change Log

- **2026-11-13 (Kristine, etter gjennomgangen):** Kristine spurte om søknaden burde ha en overskrift, og valgte overskriften «Søknad på stillingen som …» som vanlig tekst (ikke fet), fordi det er vanlig i norske søknadsbrev. Endret: beslutningen om begynnelsen og lengden (inne i den frosne delen, godkjent av Kristine), regelen i `prompts/brev.md`, `brev-1.json` og to tester (prompten nevner overskriften, og hvert `brev-*.json` begynner med den). **KEEP:** resten av koden og rettingene fra gjennomgangen.

## Review Triage Log

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | blind, kant | `\x0b`, `\x0c`, `\x85` og `\x1c`–`\x1f` fjernes, så ordene på hver side limes sammen («Pythonog») | low | Følger matrisen («tegnet fjernes»). Claude sender sjelden slike tegn mellom ord. Avvist. |
| 2 | blind | Et brev der Claude legger flere avsnitt i ett element med `\n\n`, blir ett langt avsnitt | maybe-false | Prompten og skjemaet krever ett avsnitt per element. Uvisst om Claude gjør det. Defer (middels hvis det skjer): sjekkes når brevet prøves med ekte KI i 4.3 og 4.4. |
| 3 | blind | `</cv>` eller `<annonse>` i teksten kan bryte ut av merkene | low | carried: som #8 i 4.1, avvist. |
| 4 | blind | Prompten krever arbeidsgiverens navn, men sier ikke hva som skjer når annonsen ikke har noe navn | medium | Claude kan dikte opp et navn (FR-37). Patch: én setning i prompten, med test. |
| 5 | blind | «Minst to krav» kolliderer med «ikke påstå krav CV-en ikke viser» når CV-en dekker færre enn to | medium | Uten regel kan Claude strekke CV-en (FR-37, kuttes aldri). Patch: FR-37 går foran, med test. |
| 6 | blind | Uklart om hilsen og navn regnes med i «4–6 avsnitt» | low | Beslutningen sier at de ikke regnes med. Patch: presisering i prompten. |
| 7 | blind, kant | Ingen sjekk av brevet etterpå (KI-fraser, lengde, markdown, antall avsnitt) | maybe-false | AD-14 legger reglene i prompten. En sjekk i koden ville gitt flere KI-kall og høyere kostnad. Defer: suksesskriteriene kjøres tre ganger med ekte KI i 4.4 og 4.5 og viser om brevene bryter reglene. |
| 8 | blind | Listen med de 17 frasene står i to testfiler | low | En testfil kan ikke hente fra en annen, og listen er bestemt (7. november). Avvist. |
| 9 | blind | Testen mot sjekklisten i `fasit.md` leser bare `brev-1.json` | low | Fantes før 4.2. `brev-2.json` kommer i 4.4. Defer til 4.4. |
| 10 | blind | Nøkkelord og gap-punkter renses ikke for kontrolltegn og linjeskift | low | Vises bare på siden, ikke i Word, og `telleregel` vasker nøkkelordene. Avvist. |
| 11 | blind | `forslag` gjør ingen forskjell i `EkteKI`, så forslag 2 er ikke et ekte nytt forslag | false | Uten `temperature` brukes standarden, og hvert kall gir et nytt brev. |
| 12 | blind | Ikke sjekket at `KI_MAKS_TOKENS` holder til brevet | low | Et brev på 400 ord er under 1000 tokens, og `stop_reason` står i loggen. Måles i 4.3. Avvist. |
| 13 | blind | `.strip()` i `_bare_tomme` er overflødig etter rensingen | low | Ufarlig. Avvist. |
| 14 | kant | Avsnitt med bare usynlige formattegn (U+200B, U+FEFF) regnes ikke som tomme | low | Lite sannsynlig fra Claude, og rettingen krever ny regel. Avvist. |
| 15 | verifisering | Docstringen i testen i `test_fil_ut.py` har ekte kontrolltegn (ikke rå streng) | low | Direkte retting. Patch. |
