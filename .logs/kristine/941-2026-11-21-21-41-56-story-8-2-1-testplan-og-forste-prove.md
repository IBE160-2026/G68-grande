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
