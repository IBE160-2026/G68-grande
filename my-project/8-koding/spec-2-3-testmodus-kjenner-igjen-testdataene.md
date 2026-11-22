---
title: 'Story 2.3: Testmodus kjenner igjen testdataene'
type: 'feature'
created: '2026-11-09'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '123c5fee882216f3592f90e66fb134003fc9c5ff'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Testdataene fra story 2.2 ligger i `backend/testdata/`, men ingen kode kjenner dem igjen eller gir de ferdige KI-svarene. Uten det kan ikke nettsiden kjøres uten API-nøkkel (FR-32–FR-34), og et ubrukelig KI-svar ville ikke blitt stoppet (FR-28).

**Approach:** Tre små deler, slik arkitekturen sier (AD-3, AD-4, AD-10): `kjerne/testdata_match.py` vasker tekst og finner testcaset, `kjerne/ki_svar.py` kontrollerer et KI-svar, og `adaptere/ki.py` får grensesnittet `KI` og utgaven `TestKI`, som leser svarfilene. Ingen side bruker dette ennå. Det kobles på i story 2.5.

## Boundaries & Constraints

**Always:**
- `vask(tekst)`: Unicode NFKC, så `casefold()`, så bare bokstaver og tall (`str.isalnum()`). To tekster er samme testfil når de vaskede tekstene er helt like.
- CV-en avgjør testcaset. Passer CV-en med et case og annonsen med det samme caset, er alt i orden. Passer annonsen ikke med det caset, får den `InndataFeil("annonse", ikke_testdata)`. Er CV-en ikke testdata, får den `InndataFeil("cv", ikke_testdata)`, og annonsen får feilen bare hvis den ikke er annonsen i noe case. Alle feilene kommer samtidig, cv først.
- Et felt som er tomt (bare mellomrom), får ingen `ikke_testdata`. `tom` sjekkes i story 2.5 og kommer før `ikke_testdata` (AD-9).
- Kjernen leser ingen filer. `testdata_match` får de kjente casene som data (navn + vasket CV + vasket annonse). Adapteren leser `testdata/case-*/cv.txt` og `annonse.txt` og lager dem.
- `kontroller(oppgave, tekst)` tar svaret som JSON-tekst og gir formen fra AD-4 tilbake, eller kaster `KIFeil(ubrukelig_svar)` ved: ugyldig JSON, feil form (ikke et objekt, felt som mangler eller er i tillegg, feil type), tom `nokkelord`-liste, eller både `dekker` og `mangler` tomme. `arbeidsgiver` kan være `null`. Oppgavene er bare `nokkelord` og `gap` i denne storyen.
- `KIFeil(type)` er et unntak med typene `nettverk`, `annet` og `ubrukelig_svar`. `FeilType` får `ikke_testdata`.
- `TestKI.nokkelord(annonse)` finner caset ut fra annonsen, `TestKI.gap(cv, annonse)` ut fra CV-en (og annonsen må høre til samme case). Svaret leses fra `testdata/<case>/ki-svar/<oppgave>.json` og sendes gjennom `kontroller()`. Er teksten ikke testdata, eller mangler svarfila, kastes `KIFeil(annet)`.
- `web/tekster.py` får tekst til alle nye feil: «CV: I testmodus fungerer bare testdataene fra mappen testdata/.», «Stillingsannonse: I testmodus fungerer bare testdataene fra mappen testdata/.», «Nettverksfeil, sjekk nettverkstilgangen.» (nettverk) og «Noe gikk galt hos KI-tjenesten. Prøv på nytt.» (annet og ubrukelig_svar).

**Never:**
- Ingen endringer i ruter, maler eller økten. `Soknad`, steg og valg av KI-utgave i web kommer i story 2.4 og 2.5.
- Ingen `EkteKI`, `anthropic`, `stop_reason`, `brev` eller `korrektur` (Epic 3–5).
- Ingen PDF-gjenkjenning (story 6.1). Ingen endring i testdataene fra story 2.2.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Samme tekst, annen form | CV og annonse fra case-1 med ekstra mellomrom, linjeskift og STORE bokstaver | caset `case-1-utvikler`, ingen feil | – |
| CV er ikke testdata | egen CV + annonsen fra case-1 | ingen case | `[InndataFeil("cv", ikke_testdata)]` |
| Annonse fra feil sted | CV fra case-1 + egen annonse | ingen case | `[InndataFeil("annonse", ikke_testdata)]` |
| Begge er feil | egen CV + egen annonse | ingen case | feil på cv og annonse |
| Tomt felt | CV fra case-1 + tom annonse | ingen `ikke_testdata` på annonsen | – |
| TestKI med testdata | case-1 | samme objekt som i `ki-svar/*.json` | – |
| Ubrukelig svar | ugyldig JSON / tom `nokkelord` / tomme `dekker` og `mangler` / feil form | – | `KIFeil(ubrukelig_svar)` |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/feil.py` -- `FeilType` og `InndataFeil`. Legg til `IKKE_TESTDATA`, `KIFeilType` og `KIFeil`.
- `backend/soknad/web/tekster.py` -- `FEILTEKSTER` slås opp med `(felt, type)`. Legg til tekstene over og en `KI_FEILTEKSTER` per `KIFeilType`.
- `backend/soknad/kjerne/telleregel.py` -- stilen for kjernemoduler (docstrings, `@dataclass(frozen=True)`). Ikke endre.
- `backend/testdata/case-1-utvikler/` -- de ekte testdataene. Ikke endre.
- `backend/tests/kjerne/test_inndata.py` -- `test_fr3_feiltypene_er_lukket_liste` lister alle `FeilType` og må få `ikke_testdata`. `test_nfr5_kjernen_importerer_ikke_io_adaptere_eller_web` sjekker de nye kjernefilene av seg selv (ingen `os`/`pathlib` i kjernen).
- `backend/tests/test_testdata.py` -- viser hvordan case-mappen finnes fra testene (`Path(__file__).parent.parent / "testdata"`).
- `backend/pyproject.toml` -- ruff: `encoding="utf-8"` når filer åpnes, linjelengde 100.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/feil.py` -- `IKKE_TESTDATA`, `KIFeilType` (StrEnum) og `KIFeil(Exception)` med `.type`.
- [x] `backend/soknad/kjerne/testdata_match.py` (ny) -- `vask`, `Testcase` (frossen: `navn`, `cv`, `annonse`, vasket), `lag_testcase(navn, cv, annonse)`, `case_for_annonse(annonse, caser) -> str | None` og `finn_case(cv, annonse, caser) -> tuple[str | None, list[InndataFeil]]`.
- [x] `backend/soknad/kjerne/ki_svar.py` (ny) -- `kontroller(oppgave, tekst) -> dict`.
- [x] `backend/soknad/adaptere/ki.py` (ny) -- `KI` (Protocol med `nokkelord` og `gap`), `TESTDATA_MAPPE`, `les_testcaser(mappe)` (sortert på navn) og `TestKI(mappe=TESTDATA_MAPPE)` med `.caser`. Sett `__test__ = False` på `TestKI`, så pytest ikke prøver å samle den som en testklasse.
- [x] `backend/soknad/web/tekster.py` -- tekstene og `ki_feiltekst(feil: KIFeil) -> str`.
- [x] `backend/tests/kjerne/test_testdata_match.py`, `test_ki_svar.py` og `backend/tests/adaptere/test_ki.py` (nye) -- én test per rad i matrisen, `test_fr34_...`/`test_fr28_...` med docstring. Ubrukelige svar testes i kjernen med tekst og i `TestKI` med en kopi av case-1 i `tmp_path` der en svarfil er ødelagt.
- [x] `backend/tests/kjerne/test_inndata.py` og en test i `tests/web/` -- feiltypelisten, og at hver `KIFeilType` og hver `(felt, ikke_testdata)` for cv og annonse har tekst.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (182 før denne storyen) og uten advarsler om `TestKI`.
- Given `ruff check` og `ruff format --check`, when de kjører, then er det ingen feil.

## Implementation Notes

- Hovedøkta skrev koden selv (ingen hjelpeagent), fordi endringen er liten og kodebasen kjent.
- Branch: `story/2-3-testmodus-kjenner-igjen-testdataene`.
- `TestKI` leser casene én gang når den lages (`.caser`). En svarfil som ikke er utf-8, gir `KIFeil(ubrukelig_svar)`, og en som mangler, gir `KIFeil(annet)`.
- `kontroller` kaster `ValueError` for en ukjent oppgave (for eksempel `brev`), fordi det er en feil i koden og ikke et svar fra KI-en.
- Nye tester: 45 (`test_testdata_match.py`, `test_ki_svar.py`, `adaptere/test_ki.py`, `web/test_tekster.py`), 227 i alt. Testene ble kjørt med `-W error::pytest.PytestCollectionWarning`, så `TestKI` gir ingen advarsel. `ruff check` og `ruff format --check` er grønne.
- Etter gjennomgangen (6 rettelser): 231 tester i alt, `ruff` grønn. `pyproject.toml` gjør nå `PytestCollectionWarning` til en feil.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-09), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | `kontroller` godtar lister med bare tomme tekster (`[""]`, `["  "]`, `dekker: [""]`). `tell_treff` gir da en vanlig `ValueError` i stedet for `KIFeil(ubrukelig_svar)` | grensetilfeller, blind, testhull | medium | Påvist: `tell_treff` hopper over tomme ord og kaster `ValueError` når ingen er igjen. `test_testdata.py` krever ikke-tomme ord, så de to reglene var ulike. En liste med bare tomme tekster er tom i praksis | patch |
| 2 | JSON som er nøstet veldig dypt, gir `RecursionError` og ikke `KIFeil` | grensetilfeller | low | Riktig, og rettingen er bare én unntakstype til i samme `except` | patch |
| 3 | `KIFeil` blir ødelagt ved `copy`/`pickle`, fordi `args` får `type.value` (en vanlig tekst) | grensetilfeller, blind | low | Påvist: `KIFeil("annet")` gir `AttributeError`. Rettingen er å sende `type` videre. Test lagt til | patch |
| 4 | Testen for rotete tekst sjekker bare `arbeidsgiver` i nøkkelordsvaret | blind | low | Riktig. Sammenligner nå med hele `nokkelord.json` | patch |
| 5 | Docstringen i `test_tekster.py` lover at alle feil har tekst, men testen sjekker bare de nye | blind | low | Riktig. Docstringen sier nå bare det testen sjekker | patch |
| 6 | Ingenting stopper testene hvis pytest igjen prøver å samle `TestKI` (akseptansekriteriet) | testhull | low | Påvist av laget. `filterwarnings` i `pyproject.toml` gjør advarselen til en feil. Prøvd med vilje: uten `__test__ = False` stopper testene | patch |
| 7 | Samme CV i to case gir `ikke_testdata` på en riktig annonse fra case 2 | grensetilfeller, blind | low | Ingen slike testdata. AD-10 sier at CV-en avgjør caset, og case 2 (story 4.5) får egen CV. CV 1 mot annonse 2 kjøres med ekte KI, ikke i testmodus | avvist |
| 8 | Samme annonse i to case gir svar fra ulike case i `nokkelord` og `gap` | grensetilfeller | low | Samme grunn som 7. Ingen slike testdata | avvist |
| 9 | En case-mappe uten `cv.txt`/`annonse.txt` gir `FileNotFoundError` når `TestKI` lages. En tom `testdata/` gir ingen advarsel | grensetilfeller, blind | low | Feiler tydelig og bare når noen lager en ødelagt case-mappe. En egen sjekk er mer enn en direkte retting | avvist |
| 10 | Tekst med bare tegn som «---» får `ikke_testdata` og ikke `tom` | grensetilfeller | low | `tom` defineres i story 2.5. Teksten «I testmodus fungerer bare testdataene …» er riktig for slik tekst | avvist |
| 11 | `arbeidsgiver: ""` godtas | grensetilfeller, blind | low | Ingen skade nå. Filnavnet (Epic 3) behandler manglende arbeidsgiver som tom. En ny regel er mer enn en retting | avvist |
| 12 | Docstringen til `vask` sier ikke at tegnsetting fjernes | blind | false | Den sier «bare bokstaver og tall beholdes» | avvist |
| 13 | Ingen sjekk av at `TestKI` følger `KI`-protokollen, og svarene er `dict` uten `TypedDict` | blind | low | Prosjektet har ingen typesjekker. Formen sjekkes av `kontroller` | avvist |
| 14 | Ingenting velger mellom `TestKI` og `EkteKI` i web | blind | false | Spec-en sier at dette kobles på i story 2.5 | avvist |
| 15 | `KIFeil(annet)` for tekst som ikke er testdata, gir en misvisende tekst | blind | low | Bestemt i spec-en (Always) og forklart i Design Notes. Inndataene sjekkes før KI-en kalles | avvist |

## Design Notes

`nokkelord(annonse)` har bare annonsen (signaturen er fast i AD-3), så den finner caset med `case_for_annonse`. `gap` bruker `finn_case`, der CV-en avgjør. At `TestKI` kaster `KIFeil(annet)` når teksten ikke er testdata, er bare en sikring: i story 2.5 sjekkes inndataene før KI-en kalles.

`kontroller` får JSON-tekst, ikke et ferdig objekt, fordi både svarfila og Claude gir tekst. Da sjekkes «ugyldig JSON» på samme sted for begge utgavene.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Ingen i nettleseren: ingen side bruker dette ennå (story 2.5).
