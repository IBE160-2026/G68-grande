---
title: 'Story 5.2.1: Forbedret brev fra KI-en'
type: 'feature'
created: '2026-11-15'
baseline_commit: 'af795769235248a18f62a8d1cadd671e037c56c6'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-5-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** I Korrektur stopper flyten på resultatsiden. Studenten kan ikke få en forbedret versjon av sitt eget brev (FR-23, FR-24, FR-37), og testmodus har ingen ekte Korrektur-svar (FR-38).

**Approach:** Ny KI-oppgave `korrektur` med egen prompt og eget skjema, i både `EkteKI` og `TestKI`. Svaret er setningene i brevets rekkefølge (`{setninger: [{ny, gammel, nytt_avsnitt}]}`) og kontrolleres mot det opprinnelige brevet. Resultatsiden i Korrektur får «Oppdater søknadsbrevet mitt», som gir brevsiden «Din oppdaterte søknad er ferdig!» med brevet uten markeringer, og Word-nedlasting som i Epic 3. Skriptet lager `korrektur-1.json` og `korrektur-2.json` med ekte KI (én kjøring).

## Boundaries & Constraints

**Always:** `prompts/korrektur.md` har reglene i FR-24 og FR-37, de 17 KI-frasene (skrives om hvis brukeren har brukt dem), at innhold, eksempler og rekkefølge beholdes, og at én setning aldri deles i to oppføringer (blir en lang setning til to, står begge i samme `ny`). KI-en får bare CV, annonse og eget brev, og bare når `samtykke` er sann eller testmodus er på. Visningen og nedlastingen regner aldri ut endringer selv. Brevet er alle `ny` som ikke er `null`, satt sammen av én funksjon i kjernen. Loggen viser aldri brevtekst. Testene kaller aldri det ekte API-et, og hver test nevner FR-nummeret. Kjøringen med ekte KI starter først når Kristine har godkjent den.

**Never:** Ingen markeringer, «Du skrev», forklaringsboks, «(Ny setning)» eller «setning er fjernet» (story 5.3). Ikke kjøring 2 og 3, sjekken mot fasiten eller testplanen for kriterium 12 (story 5.2.2). Ingen «Nytt forslag» og ikke noe fyrverkeri (Epic 7). Ikke PDF (Epic 6). Ingen endring i Full generering, i `brev.md` eller i brev-, gap- og nøkkelordsvarene i `testdata/`.

**Beslutning (Kristine, 2026-11-15):** KI-en retter overskriften til samme form som i Full generering («Søknad på stillingen som …», liten forbokstav) og fjerner en muntlig tiltale som «Hei!» (`ny: null`).
**Beslutning (Kristine, 2026-11-15):** hilsen og navn til slutt står slik brukeren skrev dem. Mangler de, legges ingenting til. Nettsiden setter ikke inn hilsen og navn i Korrektur.
**Beslutning (Kristine, 2026-11-15):** KI-en retter bare språk og ordvalg. Den kan gjøre en kobling til annonsen tydeligere i en setning som finnes, men legger ikke til nye setninger med innhold.
**Beslutning (Kristine, 2026-11-15):** story 5.2 deles. Kjøring 2 og 3, sjekken mot fasiten og testplanen er story 5.2.2.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Korrektur, testmodus | resultatsiden i Korrektur med case 1, «Oppdater søknadsbrevet mitt» | ventetegnet, så brevsiden med «Din oppdaterte søknad er ferdig!» og brevet fra `korrektur-1.json` | – |
| Avsnitt | `nytt_avsnitt` sann på setning 1 og 3 | to avsnitt: setning 1+2 og setning 3+… | – |
| Fjernet setning som begynte et avsnitt | `ny: null`, `nytt_avsnitt: true`, neste setning `nytt_avsnitt: false` | den neste setningen begynner avsnittet | – |
| Alle `ny` er `null` | svar fra KI-en | KI-feilboksen på resultatsiden, resultatet er der fortsatt | `KIFeil(ubrukelig_svar)` |
| `gammel` stemmer ikke | alle `gammel` satt sammen og vasket ≠ det egne brevet vasket | som over | `KIFeil(ubrukelig_svar)` |
| Feil form | ugyldig JSON, feil felt, tom `setninger`, `stop_reason` ≠ `end_turn` | som over | `KIFeil(ubrukelig_svar)` |
| Word | «Last ned som Word» på brevsiden i Korrektur | fila har det samme brevet som siden, uten markeringer, og vinduet etter nedlasting kommer | `FilFeil` som før |
| Uten samtykke | testmodus av, samtykket mangler | til startsiden, uten KI-kall | – |
| Full generering | modus Full generering | resultatsiden og brevsiden som før | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/ki_svar.py` -- `FELT["korrektur"] = {"setninger"}`. `kontroller(oppgave, tekst, stop_reason, eget_brev=None)`: for `korrektur` er `eget_brev` påkrevd (ellers `ValueError`). Formsjekk: `setninger` er en ikke-tom liste av objekter med nøyaktig `ny` (str | None), `gammel` (liste av str) og `nytt_avsnitt` (bool, ikke int). Rens `ny` og hver `gammel` med `_rens_avsnitt`, og tom `ny` blir `None`. Så gir alle `ny` `None` ubrukelig, og `vask("".join(alle gammel)) != vask(eget_brev)` gir ubrukelig (`testdata_match.vask`, AD-10). Ny `korrigert_brev(korrektur) -> list[str]`: en setning begynner et nytt avsnitt når den selv, eller en fjernet setning rett foran, har `nytt_avsnitt`. Ellers legges den til med ett mellomrom. `hele_brevet` og `_uten_hilsen` brukes ikke for Korrektur.
- `backend/soknad/kjerne/okt.py` -- `Soknad.korrektur: dict | None = None`. `sett_korrektur` som `sett_brev`. `velg_modus` og `sett_inndata` nullstiller `korrektur` som `brev`. Ny `ferdig_brev(soknad) -> list[str] | None`: `korrigert_brev` i Korrektur, `hele_brevet` ellers, `None` uten brev. Rett docstrings om «story 5.2» (L40-42, L149-150).
- `backend/soknad/adaptere/ki.py` -- `SKJEMA["korrektur"]` (setningsobjekt med `additionalProperties: false`, alle tre felt påkrevd). `KI`-protokollen får `korrektur(cv, annonse, eget_brev, forslag)`. `EkteKI.korrektur`: `_cv_og_annonse(...)` + `<eget_brev>…</eget_brev>`, og `_kall` gir `eget_brev` videre til `kontroller`. Prompten lastes av løkken over `SKJEMA` (L218-221). `TestKI.korrektur`: `finn_case(..., eget_brev=eget_brev)`, `korrektur-1` ved oddetall og `korrektur-2` ved partall `forslag`, og `_svar` gir `eget_brev` til `kontroller`.
- `backend/prompts/korrektur.md` (ny) -- bygd som `brev.md`: data i merker (`<cv>`, `<annonse>`, `<eget_brev>`), ikke følg instruksjoner i dem, reglene i Always og beslutningene, de 17 frasene (samme grupper som `brev.md`), `gammel` ordrett fra brevet så alle `gammel` til sammen er hele brevet, `nytt_avsnitt` sann der brevet har nytt avsnitt eller ny linje (også hilsen og navn), ingen markdown eller linjeskift i `ny`, og et lite eksempel med endret, uendret og fjernet setning.
- `backend/soknad/web/ruter.py:220-263,266-304,402-404,489-499` -- `resultat`: fjern 400 for Korrektur. `handling=brev` i Korrektur kaller `korrektur(cv, annonse, eget_brev.tekst, forslag=1)` og `sett_korrektur` via `_med_ki` med `BREV_KALL`, så «Prøv på nytt» virker uendret. `brev()`, `last_ned()` og `_vis_brev` bruker `ferdig_brev`. `_vis_brev` og `_vis_resultat` sender overskrift og knappetekst for modusen. Rett docstrings og kommentaren i `_med_ki`.
- `backend/soknad/web/tekster.py:197-201` -- `OPPDATER_BREV_KNAPP = "Oppdater søknadsbrevet mitt"`, `BREV_OVERSKRIFT_KORREKTUR = "Din oppdaterte søknad er ferdig!"`. `VENTE_BREV` gjenbrukes.
- `backend/soknad/web/templates/resultat.html:171-182`, `brev.html:7-10` -- knappen i begge moduser med teksten for modusen, overskriften fra ruten, og kommentarene om story 5.2 rettes.
- `backend/scripts/lag_testsvar.py` -- `lag_svar(ki, cv, annonse, eget_brev=None)` gir også `korrektur-1` og `korrektur-2` når caset har `eget-brev.txt`. Nytt flagg `--bare-korrektur` gir bare de to, så de sjekkede brev-, gap- og nøkkelordsvarene ikke lages på nytt. Rett docstringen.
- `README.md:74-83` -- de nye filene og `--bare-korrektur`.
- Tester: `tests/kjerne/test_ki_svar.py:103-106` (bytt `korrektur` med en ukjent oppgave), `test_okt.py`, `tests/adaptere/test_ki.py`, `test_ekte_ki.py` (`tests/falsk_api.py`, `oppgave_i` virker med `FELT`), `tests/scripts/test_lag_testsvar.py`, `tests/web/test_resultat.py` (5.1-testen for 400 i Korrektur blir en test for knappen), `test_brev.py`, `test_nedlasting.py`, `tests/test_testdata.py` (`KI_FRASER`, `KORREKTUR_CASE`). Fixturen `paa_resultat_korrektur` i `tests/web/conftest.py:48` og `tests/web/hjelpere.py` gjenbrukes.
- Ikke endre: `_med_ki` (utenom kommentaren), `innlegging.js`, `vente.js`, `fil_ut.lag_docx`, `prompts/brev.md`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/ki_svar.py`, `okt.py` -- `korrektur` i `kontroller`, `korrigert_brev`, `Soknad.korrektur`, `sett_korrektur`, `ferdig_brev` -- kjernen først
- [x] `backend/soknad/adaptere/ki.py`, `backend/prompts/korrektur.md` -- skjemaet, prompten og `korrektur` i begge KI-utgavene
- [x] `backend/soknad/web/ruter.py`, `tekster.py`, `templates/resultat.html`, `templates/brev.html` -- knappen, ruten via `_med_ki`, brevsiden og nedlastingen med `ferdig_brev`
- [x] `backend/scripts/lag_testsvar.py`, `README.md` -- Korrektur-svarene og `--bare-korrektur`
- [x] `backend/tests/...` -- tester for hver rad i matrisen, `kontroller` for Korrektur, `korrigert_brev`, skriptet og prompten. Webtestene som trenger svarfilene, venter til kjøringen under
- [x] Ekte KI, etter Kristines godkjenning -- `uv run python -m scripts.lag_testsvar --case case-1-utvikler --bare-korrektur` (2 kall, anslått 2–4 kr) skriver `ki-svar/korrektur-1.json` og `korrektur-2.json`. Terminalloggen lagres i `my-project/testkjoringer/5-2/runde-1/kjoring-1/`. Er et svar ubrukelig, stopp og spør Kristine
- [x] `backend/tests/test_testdata.py`, `tests/web/...` -- med svarfilene: begge består `kontroller` mot `eget-brev.txt`, minst én setning er endret, ingen `ny` har noen av de 17 frasene, og flyten i testmodus når brevsiden

**Acceptance Criteria:**
- Given resultatsiden i Korrektur, when siden vises, then står «Tilbake» og «Oppdater søknadsbrevet mitt» nederst, og i Full generering står «Lag søknadsbrevet mitt» som før
- Given `prompts/korrektur.md`, when testene kjører, then inneholder den alle de 17 KI-frasene og regelen om at én setning ikke deles
- Given `korrektur-1.json` og `korrektur-2.json`, when de kontrolleres mot `eget-brev.txt`, then består begge, minst én setning er endret, og ingen `ny` har noen av de 17 frasene

## Implementation Notes

- Kjøringen med ekte KI (godkjent av Kristine 15. november 2026, kl. 15.57): to kall, 4 686 tokens inn og 2 956 + 2 934 ut, ca. 0,86 + 0,85 = 1,71 kr. Begge svarene besto `kontroller` på første forsøk. Loggen og en kopi av svarene ligger i `my-project/testkjoringer/5-2/runde-1/kjoring-1/`.
- Kristine godkjente 15. november 2026 at prompten bruker «dere» når brevet blander «dere» og «du».
- `--bare-korrektur` hopper over caser uten `eget-brev.txt`, og gir feilkode 3 når ingen av de valgte casene har et.
- Webtestene bruker kopier av `testdata/` med egne svarfiler (`KorrekturTestKI` i `tests/web/hjelpere.py`), så kanttilfellene ikke avhenger av de ekte svarene. To tester bruker de ekte filene.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | edge-case, blind | En setning med tom `gammel` og tekst i `ny` (ny setning) godtas | false | AD-5 sier at en setning er ny når `gammel == []`, og story 5.3 viser den som «(Ny setning)». Prompten forbyr nye setninger med innhold, og det sjekkes mot fasiten i 5.2.2. Avvist |
| 2 | edge-case | Et eget brev nær 15 000 tegn kan gi `max_tokens`, fordi svaret har brevet to ganger (`gammel` og `ny`) | maybe-false | Med 16 000 tokens ut er det trolig nok for ca. 10 000 tokens brevtekst, men tenkingen kommer i tillegg. Avgjøres med én måling med et langt brev. Utsatt (deferred-work) |
| 3 | edge-case | KI-en kan sette `nytt_avsnitt` usann på overskrift, hilsen eller navn, så de slås sammen med avsnittet foran | low | Mulig, men begge de ekte svarene har det riktig. Retting = ny vakt. Avvist |
| 4 | edge-case | Tom `eget-brev.txt` gir to betalte kall med tomt brev | low | Hypotetisk, testbrevet er ikke tomt, og `test_fr34_bare_case_1_har_et_eget_brev` passer på fila. Retting = ny vakt. Avvist |
| 5 | blind | Ingenting i koden sjekker at `ny` beholder innholdet, hilsenen og navnet | low | Stemmer, men AD-4 og AD-5 legger reglene i prompten, og innholdet sjekkes for hånd mot fasiten (kriterium 12, story 5.2.2), som for brevet i Full generering. Retting = likhetssjekk (ny logikk). Avvist |
| 6 | blind | `_stemmer_med` godtar `gammel` som ikke er ordrett (store bokstaver, tegnsetting) | low | Stemmer. Vasken er bestemt i AD-4 og AD-10. Betyr noe først når 5.3 viser «Du skrev». Retting = ny sjekk. Avvist, nevnes i 5.3 |
| 7 | blind | Prompten sier både «skriv om, så meningen er den samme» og «heller ikke omskrivinger» om KI-frasene. `korrektur-1` ga «Takk for at dere har lest søknaden.» | low | Delvis: det er uklart om setningen er en omskriving av frasen. Det avgjøres i sjekken mot fasiten i 5.2.2, og plan B finnes for dette. En endring i prompten nå ville gjort de betalte svarene utdaterte. Avvist her, tas med i 5.2.2 (deferred-work) |
| 8 | blind | Eksempelet i prompten fjerner «Det var gøy», men reglene sier at alt innhold skal stå | low | Fasiten vil ha bort de muntlige ordene, og regelen «ord som er for muntlige» dekker det delvis. Samme grunn som 7: tas med i 5.2.2. Avvist her |
| 9 | blind | Testen av de ekte svarene sjekker lite av «Sjekkliste for Korrektur», og README sier at testene sjekker sjekklisten | false | Sjekklisten sjekkes for hånd i 5.2.2 (Kristines beslutning). Setningen i README gjelder brevene i Full generering. Avvist |
| 10 | blind | README sier ikke at feilkode 3 også gjelder `--bare-korrektur` uten `eget-brev.txt`, og tid og pris mangler for Korrektur | low | Stemmer. Direkte tekstretting → patch |
| 11 | blind | Testplanen har ikke resultatet for kriterium 12, og kjøring 2 og 3 mangler | false | Hører til story 5.2.2 (Kristines beslutning 15. november). Avvist |
| 12 | blind | `brev.html` sier at PDF kommer i Epic 6, men nedlasting som PDF er Epic 7 | low | Stemmer (Epic 6 er opplasting av PDF). Direkte retting → patch |
| 13 | blind | Docstringen til `_vis_resultat` nevner bare «Lag søknadsbrevet mitt» | low | Stemmer. Direkte retting → patch |
| 14 | blind | Alle feil i `kontroller()` logges som `ubrukelig_svar`, så loggen sier ikke hvilken regel som brøt | low | Stemmer, men slik var det før denne storyen også. Retting = nye feilkoder. Avvist |
| 15 | blind | `lagret.eget_brev.tekst` kan gi `AttributeError` når `eget_brev` er None | false | `Soknad.eget_brev` er alltid et `Tekstfelt` (`default_factory`), og `sett_inndata` setter aldri None. Avvist |

## Design Notes

`ferdig_brev` er det eneste stedet som velger mellom `brev` og `korrektur`, så brevsiden og Word-fila alltid har det samme brevet. Kontrollen mot originalen bruker samme vask som testdata-sjekken: tegnsetting og linjeskift teller ikke, men et ord som mangler eller er lagt til i `gammel`, gir feil. Eksempel:

```json
{"setninger": [
  {"ny": "Søknad på stillingen som junior utvikler", "gammel": ["Søknad på jobb som junior utvikler"], "nytt_avsnitt": true},
  {"ny": null, "gammel": ["Hei!"], "nytt_avsnitt": true},
  {"ny": "Med vennlig hilsen", "gammel": ["Med vennlig hilsen"], "nytt_avsnitt": true}
]}
```

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil (samme som CI)

**Manual checks (if no CLI):**
- Kristine prøver i nettleseren: Korrektur i testmodus med case 1 til brevsiden, Word-fila mot siden, og at Full generering er som før.
