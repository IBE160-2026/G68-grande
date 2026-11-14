---
title: 'Rettinger fra retrospektiven for epic 4, runde 4: måling med lange tekster'
type: 'chore'
created: '2026-11-14'
status: 'done'
baseline_commit: '88a35a7950f2aa6b52f4647ec83376c2620d9923'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-retro-2026-11-14.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Grensen i 4.3.2 tillater CV og annonse på 15 000 tegn hver, men tiden for KI-kallene er bare målt med de korte testdataene (2–5 s for nøkkelord og gap, 16–47 s for et brev). Kallet strømmes ikke, så tidsgrensen på 90 s gjelder i praksis hele brevet (retro 4, funn B7, action item 4).

**Approach:** Én kjøring av `scripts/lag_testsvar.py` med ekte KI på en fiktiv CV og en fiktiv annonse på 14 500–15 000 tegn hver. Tiden for hvert kall leses fra tidsstemplene i loggen. Tid, tokens og pris skrives i `my-project/testplan.md` og i kommentaren ved `KI_TIDSGRENSE` i `innstillinger.py`.

**Decision (Kristine, 2026-11-14):** Runde 4 av tre runder etter retro 4, med egen branch og PR. Kristine godkjente kostnaden: ca. 3–4 kr for de 4 kallene i skriptet (nøkkelord, gap og to brev).

## Boundaries & Constraints

**Always:**
- Skriptet kjøres nøyaktig én gang. Feiler et kall (for eksempel tidsavbrudd), skrives feilen og tiden ned, og skriptet kjøres ikke på nytt. Hovedøkta spør Kristine.
- CV-en og annonsen er helt fiktive: ingen ekte personer, firmaer, adresser eller telefonnumre. De er på norsk og ligner en ekte CV og annonse for en junior utvikler.
- Hvert felt er 14 500–15 000 tegn, telt med `antall_tegn` i `soknad.kjerne.inndata` (samme telling som nettsiden).
- Ingen API-nøkkel eller tekst fra `.env` i filene som lagres.

**Never:**
- Ikke endre verdiene i `innstillinger.py` (`KI_TIDSGRENSE` og de andre), promptene eller koden i `backend/soknad/`, bare kommentaren ved `KI_TIDSGRENSE`. Viser målingen at grensen bør endres, er det en beslutning for Kristine.
- Ikke skrive til `backend/testdata/` (bruk `--testdata` og `--ut`).
- Ikke endre `prompt-logg.md` eller `todo.md`.

</frozen-after-approval>

## Code Map

- `backend/scripts/lag_testsvar.py` -- kjøres fra `backend/` med `uv run python -m scripts.lag_testsvar --testdata ../my-project/testkjoringer/retro-4/inndata --ut ../my-project/testkjoringer/retro-4/kjoring-1`. Leser `case-*/cv.txt` og `annonse.txt`, gjør 4 kall og logger tokens og pris med tidsstempel. Nøkkelen leses fra `backend/.env`.
- `my-project/testkjoringer/4-4/runde-1/kjoring-1/logg.txt` -- mønsteret for loggfila: to linjer om kjøringen og kommandoen, så utskriften fra terminalen.
- `backend/soknad/kjerne/inndata.py` -- `antall_tegn` til tellingen.
- `my-project/testplan.md:60–75` -- «Kostnad og tid» for 4.4 er mønsteret for tabellen og teksten. Ny seksjon nederst: «Retro 4: måling med lange tekster (14. november 2026)».
- `backend/soknad/innstillinger.py:29–34` -- kommentaren ved `KI_TIDSGRENSE` sier nå «Målingen med lange tekster kommer senere». Den byttes ut med resultatet.
- Tiden for hvert kall er tiden fra forrige logglinje (eller starten for det første kallet) til logglinjen for kallet. Starten noteres i loggfila (klokkeslett rett før kjøringen).

## Tasks & Acceptance

**Execution:**
- [x] `my-project/testkjoringer/retro-4/inndata/case-lang/cv.txt` og `annonse.txt` -- de fiktive tekstene, 14 500–15 000 tegn hver.
- [x] Kjøringen -- én gang, utskriften i `my-project/testkjoringer/retro-4/kjoring-1/logg.txt`, svarene i samme mappe.
- [x] `my-project/testplan.md` -- ny seksjon: antall tegn, tokens inn og ut, tid og pris for hvert kall, og hva det betyr for grensen på 90 s.
- [x] `backend/soknad/innstillinger.py` -- kommentaren ved `KI_TIDSGRENSE` med tiden for de lange tekstene.

**Acceptance Criteria:**
- Given loggen fra kjøringen, when tidene og prisene i testplanen sammenlignes med den, then stemmer de.
- Given de to tekstfilene, when `antall_tegn` kjøres på dem, then er begge 14 500–15 000.
- Given alle testene, when de kjøres, then er de grønne (801).

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

## Implementation Notes

- Tekstene: CV 14 622 tegn og annonse 14 584 tegn (`antall_tegn`). Ingrid Prøvesen (informatikkstudent) søker som junior utvikler i Prøvestad Data AS. Telefon `000 00 000`, e-post på example.com, steder som Eksempelby og Prøvegata.
- Kjøringen ble gjort én gang, kl. 22:00:09,966–22:01:23,339, med feilkode 0. Tid: nøkkelord ca. 12,0 s (med oppstarten), gap 13,9 s, brev 1 25,0 s og brev 2 21,3 s. Kostnad 3,82 kr i alt, og 2,60 kr per fullført søknad.
- Terminalen skrev «anslått» med feil tegnkoding (Windows-terminalen). I `logg.txt` står ordet med riktig tegn. Ellers er utskriften kopiert ordrett.
- Til Kristine: 2,60 kr per søknad er under 3 kr, men nær. Med «Nytt forslag» blir det 3,82 kr. Grensen på 90 s er ikke endret (lengste kall 25 s).

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-14), tre lag: blind, kanttilfeller og testhull. Testhull-laget fant ingen hull. Begge de andre lagene sjekket alle tallene mot `logg.txt`, og de stemmer.

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | blind | Slutningen om at tiden «avhenger mest av hvor langt svaret er», motsies av nøkkelordene (134 tokens ut, men 12 s mot 2–5 s) | low | Sant. Direkte retting av teksten. Patch: lengre tekst inn gjorde særlig de korte kallene tregere. |
| 2 | blind, kant | «12–14 s» i kommentaren og konklusjonen tar med oppstarten av skriptet uten å si det | low | Sant (bare tabellraden har forbeholdet). Patch begge steder. |
| 3 | blind | Kommentaren begrunner fortsatt 90 s bare med brevet på 47 s | low | Sant. Patch: 90 s er beholdt også etter denne målingen. |
| 4 | blind | Det står ikke rett ut at 3,82 kr er over målet på 3 kr, eller at 2,60 kr er over overslaget på ca. 2 kr i PRD-en | low | Sant. Målet gjelder en fullført søknad med ett brev, men marginen er liten. Patch: begge deler står rett ut. |
| 5 | blind | Bare én kjøring, mens testplanen ellers bruker tre | low | Intent (Kristine godkjente én kjøring og kostnaden for den). Avvist. |
| 6 | blind | Tydelige feil i gap-svaret og brevene (React og TypeScript, egne krav, nåtid om en ferdig jobb, «krav» om noe som er en fordel) er ikke nevnt | low | Delvis sjekket av hovedøkta (CV-en har React og TypeScript som «grunnleggende», men gap sier at de mangler). Patch: en kort liste med merknadene som holder, og Kristine vurderer dem, som i 4.4 og 4.5. |
| 7 | blind | Kjøringen kan ikke gjentas, fordi commiten for promptene ikke står | low | Sant. Direkte retting. Patch: commiten står i loggen og testplanen. |
| 8 | blind | Ingenting viser at action item 4 og funn B7 er lukket (TO DO, sprint-status, prompt-logg) | false | Bokføringen gjøres etter gjennomgangen, som i runde 2 og 3 (Never: `todo.md` og `prompt-logg.md`). |
