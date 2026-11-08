# Story 2.2: Fiktive testdata og fasit for første testcase

## 2026-11-08 kl. 18:46 — Kristine

### Oppgave
Kristine startet `/bmad-build` med «2.2». Nettsiden skal ha fiktive testdata med en fasit, slik at sensor kan prøve nettsiden i testmodus og se at nøkkelordtreffet gir nøyaktig prosenten i fasiten (suksesskriterium 2). Claude lager utkastet, og Kristine godkjenner innholdet før PR-en flettes.

### Plan
- Egen branch `story/2-2-fiktive-testdata-og-fasit-for-forste-testcase`. Kristine sa ja til hjelpeagenter i hele økta.
- Epic 2-konteksten fra story 2.1 var fortsatt gyldig og ble brukt på nytt.
- Spec skrevet: [spec-2-2-fiktive-testdata-og-fasit-for-forste-testcase.md](../../my-project/9-koding/spec-2-2-fiktive-testdata-og-fasit-for-forste-testcase.md) (originalen ligger i `_bmad-output/implementation-artifacts/`).
  - Den er på ca. 1800 tokens, og Kristine valgte «Godkjenn og fortsett».
  - KI-en tok selv disse valgene: casen er en junior utvikler (som i eksempelet i PRD-addendumet), mappen heter `case-1-utvikler`, og testen sjekker ikke ordlyden i gap-analysen, fordi ekte KI-svar i Epic 4 bruker andre ord.
  - KI-en la også til en kort sjekkliste for brevet i fasiten (kriterium 11), fordi arkitekturen sier at fasiten skal ha den, og ingen annen story lager den.
- En hjelpeagent laget utkastet ut fra spec-en. Tre hjelpeagenter gikk gjennom det (blind, grensetilfeller, testhull), og så ble funnene vurdert og rettet.

### Resultat
- **Ny mappe `backend/testdata/case-1-utvikler/`:**
  - `cv.txt`: Sara Eksempel, student på bachelor i IT, ferdig våren 2027.
  - `annonse.txt`: junior utvikler hos Testvik Utvikling AS i Eksempelby, med 10 krav.
  - `fasit.md`: tabellen «Krav» (Ja/Nei med begrunnelse), tabellen «Nøkkelord», «7 av 11 = 64 %» og sjekklisten for brevet.
  - `ki-svar/nokkelord.json` og `ki-svar/gap.json`: håndlagde svar.
  - Hullene er SQL, Docker, Scrum og førerkort. Alle navn er oppdiktet, og e-postene slutter på `@example.com`.
- **Ny fil `backend/tests/test_testdata.py`:** 7 tester. De sjekker:
  - at fasiten og telleregelen gir samme prosent og samme Ja/Nei per nøkkelord
  - at alle nøkkelordene står i annonsen
  - at treffene står som egne ord, og at nøkkelordene som mangler, ikke står i CV-en i noen form
  - formen på KI-svarene og tabellen «Krav»
  - at e-postene er fiktive
- **README:** «Testdata og tester» sier nå hvor testdataene, fasiten og de håndlagde KI-svarene ligger.
- **Gjennomgangen:** 14 funn. 6 ble rettet og 8 avvist med begrunnelse, og ingenting er utsatt (Review Triage Log i spec-en). Det viktigste funnet: testen sjekket bare treffene, så «MySQL» i CV-en kunne gitt «SQL = Nei» uten at noe feilet.
- Ingen av funnene som ble avvist, var avvist i en tidligere story, så punkt 7 fra retrospektiven ga ingen beslutning til Kristine denne gangen.
- **KI-feil i hovedøkta:** KI-en prøvde om testen virket ved å endre fasiten med vilje. Etterpå prøvde den å legge fila tilbake med Git, men fila var ikke lagret i Git ennå, og ble tømt. Den ble lagt tilbake fra en kopi KI-en hadde tatt først, og den er helt lik originalen (samme kontrollsum, `20a262a`).
- 182 tester grønne (175 før), `ruff check` og `ruff format --check` grønne.
- Commits: `0881b4a` (testdataene, testene og README), `51a0d3c` (spec i `my-project/9-koding/`, prompt-logg 256–257 og TO DO).
- `sprint-status.yaml`: story 2.2 er `review`. Kopien i `my-project/7-sprint-planning/` oppdateres når PR-en er flettet.
- Notater til refleksjonsrapporten lagt inn i `my-project/8-refleksjonsrapport/notater.md` (3.3 og 5.5).
- Ingenting å prøve i nettleseren, fordi ingen side bruker testdataene ennå (story 2.3 og 2.5).

### Åpne punkter
- Story 2.2: Kristine leser `cv.txt`, `annonse.txt` og `fasit.md` og sjekker at alt er fiktivt, at hullene er tydelige og at begrunnelsene stemmer. Så push, PR med merknad om KI-feil, grønn CI på Linux og Windows, og flette. Deretter story 2.2 til `done`, og oppdatere kopien av `sprint-status.yaml` og `todo.md`.
- Neste steg: story 2.3 «Testmodus kjenner igjen testdataene» med egen branch og PR.
