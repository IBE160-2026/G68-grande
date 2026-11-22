# Story 8.2.1: Testplanen og første prøve fra en ny kopi

## 2026-11-21 kl. 21:41 — Kristine

### Oppgave
Kristine startet story 8.2 «Testplan og prøve fra en ny kopi» med `bmad-build`. Testplanen skal vise resultatet for alle suksesskriteriene (NFR-12), README skal prøves fra en ny kopi, og issue #16 skal lukkes.

### Plan
- Planen: `_bmad-output/implementation-artifacts/spec-8-2-1-testplan-og-forste-prove.md` (godkjent av Kristine).
- Kristines beslutninger: ingen nettlesertester for skriptene (issue #16 lukkes med en tabell i testplanen og en kjent begrensning i README), og story 8.2 deles. 8.2.1 gjøres nå. 8.2.2 (kriterium 13 og andre prøve rett før levering) gjøres senere med egen branch og PR.
- Første prøve bruker README slik den er nå, ikke slik den var etter Epic 1–6, fordi 8.1 alt er ferdig. Det står i testplanen.
- En agent laget arbeidet. Tre gjennomgangsagenter fant 23 punkter: 15 ble rettet, 2 utsatt og 6 avvist (se Review Triage Log i spec-en).

### Resultat
- Branch `story-8-2-1-testplan-og-forste-prove`, commit `cc0f7b3` (arbeidet) og `c182413` (rettingene etter gjennomgangen). Ikke pushet.
- `my-project/testplan.md`: oversikt over alle 14 kriteriene (automatisk med testfil og testnavn, eller for hånd med dato), og nye deler: «Kostnad per søknad», «Prøven fra en ny kopi», «Hele flyten for hånd», «Tilgjengelighet og skjermbredder», «Skriptene som prøves for hånd» og «Kriterium 13» (kommer i 8.2.2).
- Første prøve fra en ny kopi: klonet fra GitHub til en tom mappe uten `.env`. `uv sync`, alle tester, innlogging med testbrukeren og en søknad i testmodus med case 1 (50 %, som i fasiten) virket. Ingen feil i README.
- `my-project/testkjoringer/8-2/`: `kontrast.py` (25 fargepar, alle med krav består, lavest 4,53:1), `etiketter.py` (14 sider, ingen feil), `http_prove.py` (sjekker søknaden over HTTP) og loggen `ny-kopi-1.txt`.
- Ny test `backend/tests/web/test_kontrast.py`, så kontrasten sjekkes i CI. 1 416 tester består, og ruff gir ingen feil.
- README: ny kjent begrensning om at JavaScript-filene ikke har nettlesertester.
- `issues.md` og `todo.md`: punktene for issue #16 er krysset av, og de to sjekkpunktene for 22. og 29. november er krysset av (nådd 12. november). `deferred-work.md` har to nye utsatte punkter (etikettsjekken i CI, og vilkårene for prøve 2).

### Åpne punkter
- Kristine prøver i nettleseren før PR-en: hele flyten i begge modusene, ekte KI én gang, åpne .docx og PDF, tastatur, synlige etiketter, fire bredder, 200 % zoom og de 8 skriptene. Resultatene skrives inn i testplanen.
- Kristine bestemmer om README skal si hvordan repoet hentes (`git clone` eller ZIP) og at man må `cd G68-grande` etterpå.
- Story 8.2.2: kriterium 13 og andre prøve fra en ny kopi, uten uv fra før, med tomt mellomlager og i PowerShell.
- PR-en for 8.2.1 skal ha «Closes #16» (punktet fra 10. november).

## 2026-11-22 kl. 11:52 — Kristine

### Oppgave
Kristine spurte hva hun skulle gjøre videre (`bmad-help`). Så ba hun om at nettsiden ble åpnet, og om en liste steg for steg for prøvene i nettleseren før PR-en for 8.2.1. Hun rapporterte resultatene og ba om push.

### Plan
- Starte nettsiden i bakgrunnen (`uv run flask --app soknad run`) og åpne den i nettleseren.
- En liste i fem runder: Full generering i testmodus med mus, Korrektur i testmodus, bare tastatur, bredder, zoom og etiketter, og ekte KI.
- Føre resultatene inn i testplanen etter hver runde, og lese tokens og kroner for søknaden med ekte KI fra terminalen.
- Kristines beslutning om README: det skal være så enkelt som mulig for sensor. Claude anbefalte å vise både `git clone` og ZIP, og hun godkjente teksten.

### Resultat
- Alt besto i nettleseren 22. november: hele flyten i begge modusene, ekte KI (7 635 tokens inn, 2 377 ut, ca. 0,86 kr), .docx og PDF åpnet, bare tastatur, synlige etiketter, 320, 375, 768 og 1280 px, 200 % zoom og de 8 skriptene. Ført inn i `my-project/testplan.md`, og ingen rader står lenger som «Ikke prøvd ennå».
- Med bare tastatur går Tab også gjennom knappene i nettleseren før nettsiden. Kristine og Claude ble enige om at det er vanlig i nettlesere, og det står som en merknad i testplanen.
- Fyrverkeriet med animasjonene av ble prøvd i story 7.4, og `fyrverkeri.js` er ikke endret siden (sjekket i git). «Prøv på nytt» i KI-feilboksen ble ikke prøvd, fordi ingen KI-feil kom.
- README: nytt steg «1. Hent koden» (`git clone` og `cd G68-grande`, eller «Download ZIP» og mappen `G68-grande-main`). Stegene etter heter nå 2 og 3. Testene som leser README, består (66 tester).
- Spec-en er kopiert til `my-project/9-koding/` med en rad i `my-project/README.md`. Notatet til refleksjonsrapporten er skrevet i `my-project/8-refleksjonsrapport/notater.md` (mappen er git-ignorert, så det ligger bare lokalt).
- Commits `b570c26`, `567fa6b` og `1e2bca1`. Branchen er pushet, og [PR #53](https://github.com/IBE160-2026/G68-grande/pull/53) er laget med «Closes #16» og en merknad om KI-feilene. CI kjørte da loggen ble skrevet.
- I `issues.md` er disse punktene lukket: nettleserprøven, README-beslutningen og «Closes #16». Punktet for 8.2.2 har fått med det nye README-steget.
- Nettsiden kjører fortsatt i bakgrunnen.

### Åpne punkter
- Flette PR #53 når CI er grønn, så issue #16 lukkes. Story 8.2 blir stående som «in-progress» til 8.2.2 er ferdig.
- Story 8.2.2: kriterium 13 og andre prøve fra en ny kopi, også det nye steget «1. Hent koden» (punktet står alt i `issues.md`).