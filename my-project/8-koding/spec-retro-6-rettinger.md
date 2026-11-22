---
title: 'Rettinger etter retro 6: PDF-lesingen, testene for filfeltet og avstemming av papirene'
type: 'bugfix'
created: '2026-11-17'
status: 'done'
baseline_commit: '23f6dc773c822d67b9a2193278cc6f817517bacf'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-6-retro-2026-11-17.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Teksten fra en PDF har ingen øvre grense før den lagres i økten, har et mellomrom foran hvert linjeskift, blir helt tom hvis én side feiler, og pypdf kan logge linjer fra fila (retro 6, A1, A2, A5, A6). Ingen test sender filfeltet slik nettleseren gjør, eller vokter forholdet 16 MB / 5 MB (A4, A7). Spec-raden og testen for «samme tekst, nytt navn» lover mer enn regelen gjør (A3). Planene og papirene er ikke avstemt etter epic 6 (B).

**Approach:** Punkt 1–4 i retro 6 i én runde med én branch (`retro-6-rettinger`) og én PR. Punkt 5 (prosessen) føres inn i KI-ens minne.

**Beslutninger (Kristine, 2026-11-17):** én runde før epic 7. A3: regelen beholdes (bare samme PDF på nytt beholder analysen), bare spec-raden og docstringen rettes. Real-KI-kjøringer trengs ikke.

## Boundaries & Constraints

**Always:** `for_lang` kommer fortsatt for en PDF over grensen. pypdf brukes bare i `adaptere/pdf_inn.py`. Verken fila eller teksten logges (NFR-4). Endringer i en plan i `_bmad-output/` kopieres til samme fil i `my-project/`. Kristines egne formuleringer endres ikke utover det rettingen trenger.

**Never:** ingen ny regel for A3 (sammenligne vasket tekst). A8–A11 rettes ikke. Ingen endring i grensene (5 MB, 16 MB, 50 bokstaver, tegngrensene).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| PDF over grensen | CV-PDF med mer enn 15 000 tegn | teksten lagres med høyst 15 001 tegn, «CV: Teksten er for lang …» | – |
| Brevfelt | brev-PDF med mer enn 5 000 tegn | høyst 5 001 tegn lagres, `for_lang` | – |
| Mellomrom før linjeskift | `cv.pdf` fra case 1 | ingen `" \n"` i teksten, samme `vask` som `.txt` | – |
| Én side feiler | `extract_text()` kaster på side 2 | teksten fra de andre sidene | uleselig bare hvis for få bokstaver |
| Tomt filfelt | nettleseren sender `filename=""` med tekst eller lagret fil | feltet fra økten eller teksten brukes, ingen filfeil | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/pdf_inn.py` -- `normaliser`, `les_pdf`: kutt, mellomrom, unntak per side, logger.
- `backend/soknad/web/ruter.py:491-518` -- `_les_felt` kaller `les_pdf`. Bruk `maks_tegn(navn)` fra `kjerne/inndata.py:79`.
- `backend/soknad/kjerne/inndata.py:73` -- `antall_tegn` (len, `\r\n` = 1). Ikke endre.
- `backend/soknad/innstillinger.py:8-11` -- `MAKS_FORESPORSEL`, `MAKS_FILSTORRELSE`.
- `backend/tests/adaptere/test_pdf_inn.py`, `backend/tests/web/test_innlegging.py:811` (`send_felt`), `:1037` (A3-testen).
- Werkzeug: `(BytesIO(b""), "")` i testklienten gir en tom `FileStorage` med `filename=""`, som nettleseren (prøvd).
- Papirene: `_bmad-output/planning-artifacts/epics.md:946`, `architecture/…/ARCHITECTURE-SPINE.md:172`, `ux-designs/…/EXPERIENCE.md:130-145, 202-203`, `README.md:13`, `my-project/testplan.md:444`, `deferred-work.md:5-9, 88-90, 149-151`, `.logs/kristine/issues.md:20, 119`, `my-project/prompt-logg.md` (slutten), `my-project/README.md` (8-koding-tabellen), `sprint-status.yaml:375-413`, `spec-6-1-laste-opp-pdf.md:39` (begge kopiene).
- Kristines ordrette prompts for 6.1 og 6.2 finnes i transkriptene `a040d139…` og `7708b50a…` i `~/.claude/projects/C--BMAD-G68-grande/`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/adaptere/pdf_inn.py` -- `normaliser` fjerner `[ \t]+` foran `\n`. `les_pdf(innhold, maks=None)`: unntak fanges per side, lesingen stopper når den normaliserte teksten er over `maks`, og svaret kuttes til `maks + 1` tegn. `logging.getLogger("pypdf").setLevel(logging.ERROR)`.
- [x] `backend/soknad/web/ruter.py` -- `_les_felt` sender `maks=maks_tegn(navn)`.
- [x] `backend/tests/adaptere/test_pdf_inn.py` -- tester for kutt, mellomrom, én side som feiler (monkeypatch), loggernivået.
- [x] `backend/tests/web/test_innlegging.py` -- `send_felt` sender `<navn>_fil=(BytesIO(b""), "")` for `None` og tekst. Rett A3-docstringen. Test via ruten: lang PDF gir `for_lang` og lagret tekst ≤ grensen + 1.
- [x] `backend/tests/kjerne/test_inndata.py` (ved linje 457) -- `MAKS_FORESPORSEL >= 3 * MAKS_FILSTORRELSE + 1 MB` (plass til skjemaet).
- [x] `spec-6-1-laste-opp-pdf.md` (begge) -- raden «Samme tekst, nytt navn»: samme PDF lastet opp på nytt.
- [x] `epics.md` og AD-9 -- `for_lang` i rekkefølgen. `epics.md` (6.1, 6.2) og `EXPERIENCE.md`: hjelpeteksten om tegngrensen, begge søppelbøttene gir fokus til «Last opp PDF», et felt med avvist fil blir tomt, og raden for 16 MB.
- [x] `README.md`, `testplan.md` -- statuslinja (PDF-opplasting virker), «Prøvd i nettleseren av Kristine (PR #43)».
- [x] `deferred-work.md`, `issues.md` -- `resolved:` for Unicode (2.1), 413 (4.3.2) og 6.1-punktet. Lukk issues linje 20 og 119.
- [x] `prompt-logg.md`, `my-project/README.md` -- rader for 6.1 og 6.2 (merket «ført i ettertid»), denne runden, og oversiktsradene for epic 6 og denne spec-en.
- [x] `sprint-status.yaml`, `todo.md` -- punkt 41–44 `done`, 45 `in-progress` (minnet føres av hovedøkten).
- [x] Slett `story-6-1-laste-opp-pdf` og `story-6-2-feilmeldinger-for-filer` lokalt og på GitHub (gjort av hovedøkten 17. november, før commiten).

**Acceptance Criteria:**
- Given en PDF med teksten fra case 1, when den leses, then er `vask` lik `.txt` og kriterium 5 består.
- Given alle tester, when `pytest` og `ruff` kjøres, then består alt.

## Implementation Notes

- **Normaliseringen per side (avvik fra Design Notes):** `les_pdf` normaliserer hver side som `normaliser(side + "\n")[:-1]` og teller lengden side for side, i stedet for å normalisere hele teksten på nytt etter hver side (det ville gitt kvadratisk tid for en PDF med mange tomme sider). `"\n".join(sider)` er den samme teksten som `normaliser("\n".join(...))`, og mellomrom på slutten av en side fjernes som Design Notes sier. Eneste forskjell: mellomrom på slutten av den siste siden fjernes også.
- **`\r` foran linjeskift:** regexen er `[ \t\r]+\n`, ikke bare `[ \t]+\n`. Da har teksten fra en PDF aldri `\r\n`, så `len` og `antall_tegn` teller likt, og et kutt på `maks + 1` tegn gir alltid `for_lang`.
- **Unntak:** `extract_text()` fanges per side. `PdfReader(...)`, `len(leser.pages)` og `leser.pages[i]` står fortsatt i det ytre `try`, så en ødelagt fil gir tom tekst som før.
- **Testene som bytter ut `les_pdf`:** lambdaen i `test_nfr11_for_lang_tekst_fra_pdf_gir_for_lang`, fixturen `lest` og `ikke_kall` tar nå `maks` også.
- **Ny test via ruten:** `test_nfr11_lang_pdf_lagres_kuttet_rett_over_grensen` bytter `PdfReader` med en falsk leser (20 sider à 7 000 tegn) og sjekker `for_lang`, at økten har nøyaktig grensen + 1 tegn, og at ikke alle sidene leses.
- **Vokter av tom fildel:** prøvd ved å fjerne `not fil.filename` i `_les_felt`. Da feiler fire tester i `test_innlegging.py`.
- **Utenom listen:** `my-project/todo.md` linje 63 (README om Canva) er krysset av sammen med `issues.md` linje 20, og punktet for runden har fått en merknad om at PR-en og slettingen av branchene gjenstår.
- **Etter gjennomgangen** (se Review Triage Log): docstringen i `les_pdf` sier at grensen sjekkes mellom sidene. Ny test for skjema uten fildel (`fil is None`). Testen for lang PDF sjekker nøyaktig antall sider (3 og 1). A3-testen lagrer teksten med filnavn. AD-9 har `for_lang` og `annen_case` i typelista. `EXPERIENCE.md` og `epics.md` har raden for «for lang» og hva som skjer med en PDF over tegngrensen. `issues.md` og `deferred-work.md` sier 500 KB per tekstfelt (Flasks `MAX_FORM_MEMORY_SIZE`), ikke 16 MB. Ett punkt er utsatt i `deferred-work.md` (over 500 KB innlimt tekst gir meldingen om filer). Branchene for epic 6 er slettet lokalt og på GitHub. 1 206 tester består, og ruff er uten feil.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap, edge-case 1 | Kuttet skjer før `er_uleselig`, så en PDF med under 50 bokstaver i de første `maks + 1` tegnene og mye tekst senere får «uleselig» i stedet for `for_lang` | low | Stemmer, men en CV med 15 000 tegn nesten uten bokstaver først finnes ikke i praksis, og rettingen krever en ny gren. Avvist |
| 2 | edge-case 2, blind 9 | Én side med svært mye tekst pakkes ut og normaliseres helt før grensen sjekkes. Docstringen lover mer | low | Stemmer. Fila er høyst 5 MB, og det som lagres, er begrenset. Docstringen sier nå at grensen gjelder mellom sidene → patch |
| 3 | edge-case 3 | Ingen test dekker grenen `fil is None` i `_les_felt` lenger, fordi `send_felt` alltid sender fildelen | low | Stemmer. Én test som sender skjemaet uten fildel → patch |
| 4 | edge-case 4 | pypdf kan logge verdier fra fila (koding) på ERROR | low | Stemmer, men det er navn fra skriften i fila, ikke CV-teksten, og retro 6 bestemte «bare feil». Avvist |
| 5 | blind 1 | Punkt 44 i sprint-status er `done` før branchene er slettet | low | Stemmer. Branchene slettes i denne økten før commiten → patch (hovedøkten) |
| 6 | blind 2 | Typelista i AD-9 mangler `for_lang` og `annen_case` | low | Stemmer (`kjerne/feil.py:17, 19`). Lagt til → patch |
| 7 | blind 3 | `EXPERIENCE.md` har ingen rad for «for lang» | low | Stemmer. Raden lagt til med teksten fra `tekster.py` → patch |
| 8 | blind 4 | UX og epics sier ikke hva som skjer med en PDF over tegngrensen (filnavnet står, teksten kuttes) | low | Stemmer. Én setning i hver → patch |
| 9 | blind 5 | Oppsettet i A3-testen lagrer teksten uten filnavn, som er innlimt tekst, ikke den samme PDF-en | low | Stemmer. Oppsettet har nå et filnavn → patch |
| 10 | blind 6 | Ingen test for at innlimt tekst byttet med en PDF gir ny analyse | low | Kristine bestemte at bare spec-raden og docstringen rettes (A3). Avvist |
| 11 | blind 7 | 413-punktet er lukket, men innlimt tekst lagres fortsatt før tegnsjekken, og teksten sier «høyst 16 MB» | medium | Retroen ba om `resolved:`. Men «16 MB» er feil: Flask stopper hvert tekstfelt ved 500 KB (`MAX_FORM_MEMORY_SIZE`). Rettet i `issues.md` og `deferred-work.md` → patch. At over 500 KB innlimt tekst gir «Filene er for store», fantes før → defer |
| 12 | blind 8 | Punktet i `issues.md` om hjelpeteksten «Høyst 15 000 tegn» er halvt løst i 6.1 | low | Stemmer. Merknad lagt til, lenken står åpen → patch |
| 13 | blind 10 | `len(lest) < 20` sjekker ikke at lesingen stopper tidlig | low | Stemmer. Testen sjekker nå nøyaktig antall sider (3 og 1) → patch |
| 14 | blind 11 | NFR-4-testen sjekker bare nivået på loggeren, ikke at ingenting logges | low | En test med en PDF som gir advarsler, må lages for hånd. Nivået er det som er endret. Avvist |
| 15 | blind 12 | Oppgavelista og Design Notes sier noe annet enn koden (`\r`, side for side) | false | Implementation Notes forklarer begge avvikene, og funnet er en endring i denne spec-en. Avvist |
| 16 | blind 13 | Spec-status, PR-lenke og gjennomgangen mangler i papirene | false | De fylles inn når PR-en lages (steg 5). Avvist |

## Design Notes

Kuttet skjer i `les_pdf` (ikke i ruten), så pypdf slutter å lese sider når grensen er nådd. Normaliseringen gjøres på hele teksten etter `"\n".join`, så et mellomrom på slutten av en side også fjernes. Prompt-loggen får de etterførte radene nederst (467 og videre), ikke midt i, så numrene 465–466 i commitene stemmer.

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle består
- `cd backend && uv run ruff check . && uv run ruff format --check .` -- expected: ingen feil
