---
title: 'Story 2.2: Fiktive testdata og fasit for første testcase'
type: 'feature'
created: '2026-11-08'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '3f0c1783154430bb8a0b2f1795b906059f43ff95'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Det finnes ingen testdata ennå. Uten en fiktiv CV, en annonse og en fasit kan ikke sensor prøve nettsiden i testmodus, og ingen kan sjekke at nøkkelordtreffet gir riktig prosent (NFR-3, suksesskriterium 2).

**Approach:** En ny mappe `backend/testdata/case-1-utvikler/` med en fiktiv CV og en fiktiv stillingsannonse som tekst, en fasit og to håndlagde KI-svar. En test sjekker at filene henger sammen: at svarene har riktig form, og at telleregelen gir nøyaktig prosenten i fasiten. Claude lager utkastet, og Kristine godkjenner innholdet før PR-en flettes.

## Boundaries & Constraints

**Always:**
- Filer: `cv.txt`, `annonse.txt`, `fasit.md`, `ki-svar/nokkelord.json` og `ki-svar/gap.json`, alle i utf-8.
- Casen: en student som søker en stilling som junior utvikler hos en fiktiv arbeidsgiver. Alle navn, e-poster (`@example.com`), telefonnumre, skoler og firmaer er oppdiktet eller generelle (NFR-3).
- CV-en har tydelige hull mot annonsen, blant annet «førerkort» og «SQL». Et nøkkelord som mangler, står ikke i CV-en i noen form (ikke som del av et ord, ikke bøyd). Et nøkkelord som er treff, står i CV-en som eget ord. Ingen nøkkelord som rammes av de kjente begrensningene i README («Java»/«JavaScript», «C»).
- 8–12 nøkkelord. Prosenten er verken 0 eller 100.
- `nokkelord.json` = `{"nokkelord": [...], "arbeidsgiver": "<navnet i annonsen>"}`, `gap.json` = `{"dekker": [...], "mangler": [...]}`, bare objektet (AD-4). Alle nøkkelordene står i annonsen.
- `fasit.md` har: kort innledning (fiktivt, hva casen tester, at KI-svarene er håndlagde og byttes ut med ekte KI-svar i Epic 4, FR-38). Tabellen «Krav» med alle kravene i annonsen, kolonnene `Krav | Dekket | Begrunnelse`, `Ja`/`Nei`. Tabellen «Nøkkelord» med kolonnene `Nøkkelord | Står i CV-en`, `Ja`/`Nei`, i samme rekkefølge som `nokkelord.json`. Én linje med «X av Y = Z %». En kort sjekkliste for brevet (kriterium 11): hva brevet ikke kan påstå, fordi det ikke står i CV-en.
- `gap.json` stemmer med tabellen «Krav»: `dekker` = kravene med `Ja`, `mangler` = kravene med `Nei`.
- README, «Testdata og tester»: linjen «*Kommer:* hvor de fiktive testdataene og fasiten ligger.» byttes med en kort tekst om `backend/testdata/`, én mappe per testcase, og at fasiten er `fasit.md` i samme mappe (NFR-8).

**Never:**
- Ingen ekte personer, CV-er eller firmaer.
- Ingen `.pdf`-filer (story 6.1), ingen `brev-1.json` (story 3.1), ingen `eget-brev` (story 5.1).
- Ingen ny kode i `soknad/`. Ingen gjenkjenning av testdata eller `TestKI` (story 2.3).
- Testen sjekker ikke ordlyden i `gap.json` mot fasiten, fordi ekte KI-svar i Epic 4 bruker andre ord og testene skal gå gjennom da også.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Fasit og telleregel | `nokkelord.json` og `cv.txt` | `tell_treff` gir samme «X av Y = Z %» som fasiten, og samme Ja/Nei per nøkkelord | Testen feiler |
| Nøkkelord fra annonsen | `nokkelord.json` og `annonse.txt` | alle nøkkelordene gir treff i annonsen | Testen feiler |
| Treff er eget ord | hvert treff | står i CV-en som eget ord, ikke bare inne i et lengre ord | Testen feiler |
| Svarformer | begge JSON-filene | gyldig JSON, akkurat feltene fra AD-4, ikke tom nøkkelordliste, ikke både `dekker` og `mangler` tomme | Testen feiler |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/telleregel.py` -- `tell_treff(nokkelord, cv)` gir `Nokkelordtreff` (`treff`, `ikke_treff`, `antall_treff`, `antall`, `prosent`). Brukes av testen. Ikke endre.
- `backend/tests/kjerne/test_telleregel.py` -- stilen for tester: modul-docstring med FR-nummer, `test_fr17_...`, docstring per test.
- `backend/tests/test_app.py` -- eksempel på en testfil rett i `tests/`. Den nye testen legges der, fordi den ikke hører til `kjerne/`, `web/` eller `adaptere/`.
- `backend/pyproject.toml` -- ruff krever `encoding` når filer åpnes (PLW1514), linjelengde 100.
- `README.md` linje 72 -- linjen som byttes.
- `_bmad-output/planning-artifacts/architecture/.../ARCHITECTURE-SPINE.md` AD-4 og mappeoppsettet (linje 293–295) -- formene og filnavnene.

## Tasks & Acceptance

**Execution:**
- [x] `backend/testdata/case-1-utvikler/annonse.txt` (ny) -- fiktiv annonse for junior utvikler, med 7–10 tydelige krav (blant annet SQL og førerkort klasse B).
- [x] `backend/testdata/case-1-utvikler/cv.txt` (ny) -- fiktiv student-CV som dekker de fleste kravene, med tydelige hull.
- [x] `backend/testdata/case-1-utvikler/ki-svar/nokkelord.json` og `gap.json` (nye) -- håndlagde svar etter reglene over.
- [x] `backend/testdata/case-1-utvikler/fasit.md` (ny) -- etter reglene over.
- [x] `backend/tests/test_testdata.py` (ny) -- én test per rad i matrisen, `test_nfr3_...`/`test_fr17_...`/`test_fr38_...` med docstring. Leser fasittabellene fra `fasit.md` (linjene under overskriftene).
- [x] `README.md` -- linjen om testdata.

**Acceptance Criteria:**
- Given den nye testfila, when en feil legges inn med vilje (prosenten i fasiten endres, eller ett Ja blir Nei), then feiler testen.
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (175 før denne storyen).

## Implementation Notes

- En hjelpeagent laget testdataene, fasiten, testen og README-teksten. Casen: Sara Eksempel (student, bachelor i IT) søker junior utvikler hos Testvik Utvikling AS. Annonsen har 10 krav, og CV-en mangler SQL, Docker, Scrum og førerkort. 11 nøkkelord gir 7 av 11 = 64 % (63,6 rundes opp).
- Hjelpeagenten la til en ekstra test, `test_nfr3_alle_epostene_er_fiktive`, fordi ingen rad i matrisen gjaldt NFR-3.
- Hovedøkta prøvde en feil med vilje: «Docker» fra Nei til Ja i fasiten fikk testen til å feile. Fasiten ble lagt tilbake fra en kopi og er lik originalen (samme kontrollsum).
- Etter gjennomgangen (6 rettelser): 7 tester i `test_testdata.py`, 182 i alt, `ruff check` og `ruff format --check` grønne. De to nye testene feiler når feilen de skal fange, legges inn («MySQL» i CV-en, «Nie» i tabellen «Krav»).

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-08), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Ingen test sjekker at nøkkelord som mangler, ikke står i CV-en i noen form. «MySQL» i CV-en ville latt «SQL = Nei» stå uten at noe feilet | testhull, blind, grensetilfeller | medium | Påvist av testhull-laget. Regelen står i Always, og testen dekket bare treffene. Ny test: ingen av nøkkelordene som mangler, står inne i CV-teksten | patch |
| 2 | Tabellen «Krav» leses aldri, så en skrivefeil i kolonnen «Dekket» feiler ingenting. Akseptansekriteriet «ett Ja blir Nei» gjelder bare tabellen «Nøkkelord» | blind, grensetilfeller (2 funn) | low | Riktig. En liten test av formen (bare Ja/Nei, minst én av hver) holder også med ekte KI-svar. Ordlyden sjekkes ikke, slik spec-en sier | patch |
| 3 | `arbeidsgiver` sjekkes ikke når den er `null`, og en tom tekst består «står i annonsen» | blind, grensetilfeller (2 funn) | low | Riktig. Annonsen har navnet, så også ekte KI skal gi det. Kravet om at den ikke er tom, er en direkte retting | patch |
| 4 | Docstringen sier at casen ikke har grensetilfeller, men for korte nøkkelord er sjekken den samme som i telleregelen, så «C» i «C#» fanges ikke | testhull | low | Riktig. Casen har ikke noe slikt nøkkelord. Docstringen sier nå bare det testen faktisk sjekker | patch |
| 5 | README sier at filene «kan limes inn i testmodus», men ingen side tar imot dem ennå, og `ki-svar/` er ikke nevnt | blind (2 funn) | low | Riktig. Innleggingen kommer i story 2.5. Én setning om de håndlagde svarene er nyttig for sensor | patch |
| 6 | Fasiten sier ikke hva som skjer med tabellen «Krav» og sjekklisten i Epic 4 | blind | low | Riktig. De endres ikke, og de ekte svarene sjekkes mot dem (kriterium 1). Én setning | patch |
| 7 | Testen gjelder bare `case-1-utvikler`, så en ny case får ingen sjekk | blind | low | Case 2 kommer i story 4.5, som kan legge den til. Å kjøre testene for alle mappene er mer enn en direkte retting | avvist |
| 8 | NFR-3-testen sjekker bare e-postene, ikke telefonnumrene og adressen | blind | low | Navnene er tydelig oppdiktet, og numrene (123…, 876…) er ikke vanlige private numre. Kristine sjekker innholdet for hånd. En sjekk av telefonformat er ny logikk | avvist |
| 9 | Kravet om førerkort er kortet ned i fasiten og `gap.json` («fordi du av og til skal besøke kunder» er tatt bort) | blind | low | Grunnen er ikke en del av kravet, og kravet er lett å kjenne igjen | avvist |
| 10 | `_tabell` gir en uklar feil når overskriften mangler, og sjekker ikke skillelinjen | blind | low | Testen feiler tydelig uansett, og feilen viser hvilken overskrift som mangler | avvist |
| 11 | Like nøkkelord eller nøkkelord med mellomrom i `nokkelord.json` gjør at tabellen og telleregelen ikke stemmer | grensetilfeller | low | Testdataene har ingen slike. Skjer det med ekte KI-svar, feiler testen tydelig, og det er riktig | avvist |
| 12 | Avrunding kan gi 100 % selv om noe mangler (199 av 200) | grensetilfeller | false | Casen har 8–12 nøkkelord, og da kan ikke avrundingen gi 0 eller 100 når noe er treff og noe mangler | avvist |
| 13 | `_er_eget_ord` rydder ikke mellomrom i nøkkelordet slik telleregelen gjør | grensetilfeller | low | Ingen nøkkelord har mellomrom foran eller bak. Det ville gitt en tydelig feil, ikke et skjult avvik | avvist |
| 14 | Samme krav kan stå både i `dekker` og `mangler` | grensetilfeller | low | Ikke en regel i arkitekturen (AD-4), og en ny regel hører til kontrollen av KI-svar (story 2.3), ikke her | avvist |

## Design Notes

Fasiten er det eneste sensor sammenligner med. Derfor sjekker testen bare det som skal gjelde også når de ekte KI-svarene kommer i Epic 4: nøkkelordtabellen og prosenten (fasiten oppdateres sammen med `nokkelord.json`), og formene. Om gap-analysen dekker de riktige kravene, sjekkes for hånd mot fasiten (kriterium 1).

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Ingen i nettleseren: ingen side bruker testdataene ennå (story 2.3 og 2.5).
- Kristine leser `cv.txt`, `annonse.txt` og `fasit.md` og sjekker at alt er fiktivt, at hullene er tydelige, og at begrunnelsene stemmer.
