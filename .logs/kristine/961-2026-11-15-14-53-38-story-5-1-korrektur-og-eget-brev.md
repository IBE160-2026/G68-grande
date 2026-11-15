# Story 5.1: velge Korrektur og legge inn eget brev

## 2026-11-15 kl. 14:53 — Kristine

### Oppgave
Kristine startet story 5.1 med `/bmad-build 5.1`. Målet er at en student som har skrevet et brev selv, kan velge Korrektur og legge inn brevet sitt, og at Korrektur kan prøves i testmodus med et fiktivt testbrev.

### Plan
- Lage oversikten over epic 5 (`epic-5-context.md`) og undersøke koden for modusvalget, innleggingen, testmodus og testene.
- Skrive planen [spec-5-1-velge-korrektur-og-legge-inn-eget-brev.md](../../my-project/9-koding/spec-5-1-velge-korrektur-og-legge-inn-eget-brev.md). Kristine bestemte at CV og annonse fra case 2 i Korrektur gir den vanlige feilteksten på brevfeltet (ingen ny feiltype, ingen testbrev for case 2), og at planen beholdes samlet (ca. 2600 tokens).
- Branch `story-5-1-korrektur-og-eget-brev`. En hjelpeagent koder, og tre gjennomgangsagenter går gjennom koden.

### Resultat
- Kortet ✏️ «Korrektur» står ved siden av Full generering. I Korrektur har innleggingen overskriften «Legg inn CV-en din, brevet ditt og stillingsannonsen» og feltene CV, «✉️ Ditt søknadsbrev» og annonse, tre side om side fra 1000 px. Brevfeltet har de samme tilstandene og feilene som de andre (tomt, over 15 000 tegn, ikke testdata). Fanen heter «Legg inn CV, brev og annonse».
- `felt_for_modus` i `kjerne/inndata.py` er det eneste stedet som bestemmer feltene for modusen. `finn_case` og `les_testcaser` har et valgfritt eget brev. Resultatsiden i Korrektur har bare «Tilbake», og POST `handling=brev` gir 400.
- Nytt fiktivt `backend/testdata/case-1-utvikler/eget-brev.txt` (Sara til Testvik Utvikling AS, med muntlige ord og to KI-fraser), og «Sjekkliste for Korrektur» i `fasit.md`. README forteller hvor testbrevet ligger.
- Kodegjennomgang runde 1 fant at når bare brevet ble endret, kunne resultatsiden åpnes med et brev som hadde feilet sjekken. Regelen kom fra planen, så planen ble rettet og koden laget på nytt (runde 2). Runde 2 ga tre små rettinger (en test, README og sjekklisten). Alle 28 funn står med vurdering i planen.
- 914 tester består, og ruff check og format er grønne. Commit `8c1473e` på branchen (ikke pushet). Planen og epic-konteksten er kopiert til `my-project/9-koding/`, og sprint-status, TO DO, README og prompt-loggen er oppdatert.
- Lukket punktet om hva Korrektur gjør med case 2 i `issues.md`.

### Åpne punkter
- Kristine prøver Korrektur i nettleseren før PR-en flettes: modusvalget ved 375 og 1280 px, testdataene fra case 1, tomt brev, case 2 i Korrektur, «Tilbake», og at Full generering ser ut som før. Se særlig om tre felt på ca. 300 px hver ved 1000 px blir for trangt
- Kristine leser teksten i `eget-brev.txt` og «Sjekkliste for Korrektur» i `fasit.md` før PR-en flettes
- Story 5.2: testbrevet slutter med «Med vennlig hilsen» og «Sara Eksempel». Bestemme hvordan Korrektur behandler hilsen og navn (de må stå i `gammel`), og om tittellinjen og «Hei!» skal skrives om
