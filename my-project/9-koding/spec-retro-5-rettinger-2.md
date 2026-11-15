---
title: 'Rettinger etter retro 5, runde B: langt eget brev og bedre flyt i Korrektur'
type: 'feature'
created: '2026-11-15'
status: 'in-progress'
baseline_commit: '55b737e60dccac2fcad09b2cb5397ac77ae0ee39'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-5-retro-2026-11-15.md'
  - '{project-root}/_bmad-output/implementation-artifacts/epic-5-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Brevet fra Korrektur leses som setninger på rad, fordi prompten retter hver setning for seg (retro 5, punkt 4). Et eget brev nær grensen på 15 000 tegn får trolig ikke plass i svaret (`KI_MAKS_TOKENS` = 16 000) og rekker kanskje ikke tidsgrensen på 90 s, så brukeren får «Noe gikk galt» hver gang (punkt 3). Prompten sier også at `gammel` er «ord for ord», som passet den gamle vasken, ikke den strenge sjekken fra runde A.

**Approach:** Prompten får lov å bruke bindeord og slå sammen korte setninger i samme avsnitt, og sier at `gammel` kopieres nøyaktig. Deretter én måling med ekte KI og et langt fiktivt eget brev, så bestemmer Kristine grensen, og til slutt tre kjøringer og ny sjekk av kriterium 12 og 4.

**Beslutning (Kristine, 2026-11-15):** runde B gjøres alene, med egen branch og PR. Runde C kommer etterpå. «Bedre flyt» betyr at brevet skal kunne leses mer naturlig: setningene og avsnittene henger bedre sammen.

## Boundaries & Constraints

**Always:**
- Innholdet, eksemplene og rekkefølgen beholdes (kriterium 12). Setninger slås bare sammen innenfor samme avsnitt, og da står begge de gamle i `gammel`.
- Hver betalt kjøring får Kristines ja først, med omtrentlig kostnad.
- Kristine vurderer flyten og omformuleringene mot sjekklisten. KI-en foreslår, men bestemmer ikke (retro 5, C).
- Resultatet står i `my-project/testplan.md`, også når noe feiler.

**Never:**
- Ingen nye setninger med innhold, og ingen setning flyttes til et annet avsnitt.
- Ingen endring i kontrollen fra runde A, i visningen eller i Full generering.
- Målingens midlertidige verdier (høyere `max_tokens` og tidsgrense) committes ikke i koden.
- Runde C (avstemming av planene, sletting av brancher) gjøres ikke her.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| To korte setninger slås sammen | «Vi bruker Git. Det har gått greit.» i samme avsnitt | Én oppføring, `gammel` har begge, «Du skrev» viser begge | N/A |
| Store bokstaver eller tegnsetting endret i `gammel` | KI-en retter et komma i `gammel` | Ubrukelig svar | KI-feilboksen (som i runde A) |
| Brev over grensen (hvis A velges) | Brevfeltet over den nye grensen | Feilen «Ditt søknadsbrev: Teksten er for lang …» med det nye tallet | Feltet beholder teksten |

</frozen-after-approval>

## Code Map

- `backend/prompts/korrektur.md` -- reglene for innholdet (linje «Rett bare språk og ordvalg»), reglene for formen («ord for ord») og eksempelet. Eksempelet må fortsatt ha én fjernet, én uendret og én endret setning.
- `backend/tests/adaptere/test_ekte_ki.py:686-735` -- sjekker tekstbiter fra prompten og at eksempelet består `kontroller`.
- `backend/soknad/innstillinger.py` -- `MAKS_TEGN`, `KI_MAKS_TOKENS`, `KI_TIDSGRENSE` og kommentaren med målingene.
- `backend/soknad/kjerne/inndata.py:73-95` `sjekk_innlegging` -- én grense for alle felt i dag.
- `backend/soknad/web/tekster.py:286,325` -- `MAKS_TEGN_TEKST` og feilteksten for `eget_brev`.
- `backend/soknad/adaptere/ki.py:288` `EkteKI._kall` -- `max_tokens=KI_MAKS_TOKENS` for alle oppgaver, ikke strømmet. SDK-en (2.4.0) sjekker ikke 10-minuttersgrensen når klienten har egen `timeout`.
- `backend/scripts/lag_testsvar.py` -- `--bare-korrektur`, `--case`, `--testdata`, `--ut`. Gjenbrukes til de tre kjøringene.
- `my-project/testkjoringer/retro-4/inndata/case-lang/` -- Ingrids CV og annonse (ca. 14 600 tegn hver). Gjenbrukes til målingen.
- `backend/testdata/case-1-utvikler/ki-svar/korrektur-{1,2}.json` -- svarene i testmodus, lages på nytt i kjøring 1.
- `backend/tests/test_testdata.py` -- sjekker de ekte Korrektur-svarene (sjekklisten, frasene, `antall_endret`).

## Tasks & Acceptance

**Execution:**
- [ ] `backend/prompts/korrektur.md` -- la KI-en bruke bindeord og slå sammen korte setninger i samme avsnitt, så brevet leses naturlig. Si at `gammel` kopieres nøyaktig, med store og små bokstaver og tegnsetting. Eksempelet viser én sammenslåing -- retro 5, punkt 4 og runde A, funn 6
- [ ] `backend/tests/adaptere/test_ekte_ki.py` -- tekstbitene for de nye reglene, og at eksempelet har en sammenslåing (`len(gammel) == 2`)
- [ ] `my-project/testkjoringer/retro-5/inndata/case-lang/` -- Ingrids CV og annonse fra retro 4, og et fiktivt `eget-brev.txt` på 14 500–15 000 tegn (telt med `antall_tegn`) med vanlige feil. Ingen ekte personer
- [ ] **Måling (Kristine sier ja først, ca. 3–8 kr):** ett `korrektur`-kall med `max_tokens` 48 000 og tidsgrense 600 s satt bare i kommandoen. Tid, tokens inn og ut, `stop_reason` og om svaret består `kontroller` skrives i `testplan.md`, og svaret i `retro-5/maling/`
- [ ] **HALT: Kristine bestemmer** ut fra målingen: A) egen, lavere grense for brevfeltet (`MAKS_TEGN_EGET_BREV`, brukt i `sjekk_innlegging` og feilteksten), eller B) egen `max_tokens` og tidsgrense for Korrektur i `innstillinger.py` og `EkteKI._kall`. Med tester og oppdatert kommentar i `innstillinger.py`
- [ ] **Tre kjøringer (Kristine sier ja først, ca. 5–6 kr):** kjøring 1 i `testdata/` (svarene i testmodus), kjøring 2 og 3 i `my-project/testkjoringer/retro-5/kjoring-<n>/`. Sjekk mot «Sjekkliste for Korrektur». Plan B ved feil: prompten rettes én gang, og alle tre kjøres på nytt
- [ ] `my-project/testplan.md` -- ny seksjon «Retro 5: langt eget brev og flyt»: målingen, beslutningen, tabellen for kriterium 12 og 4, og kostnaden

**Acceptance Criteria:**
- Given den nye prompten, when tre kjøringer sjekkes, then alle seks brevene består kriterium 12 og 4 og `kontroller`, og Kristine har godkjent flyten.
- Given målingen, when Kristine har valgt A eller B, then et brev på den største tillatte lengden kan ikke gi feil av `max_tokens` eller tidsgrensen ut fra målingen.
- Given hele rettingen, when testene og ruff kjøres, then alt består.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

Regnestykket bak målingen: i 5.2.2 ga testbrevet (1 276 tegn) ca. 3 000 tokens ut på ca. 22 s, altså ca. 140 tokens/s. Kallet strømmes ikke, så serveren sender ingenting før svaret er ferdig, og tidsgrensen på 90 s gjelder i praksis hele svaret. Med samme fart rekker et svar på 16 000 tokens ikke 90 s (ca. 115 s). Derfor kan tidsgrensen slå til før `max_tokens`, og målingen trenger midlertidig høyere verdier for å vise hvor stort og tregt svaret faktisk blir.

Målingen kjøres uten å endre koden, for eksempel med `uv run python -c` som setter `soknad.adaptere.ki.KI_MAKS_TOKENS` og sender inn `Anthropic(timeout=600, max_retries=0)` som `klient`.

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check . && uv run ruff format --check .` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine leser brevene fra kjøring 1 i nettleseren (testmodus, Korrektur) og ser om de leses mer naturlig.
