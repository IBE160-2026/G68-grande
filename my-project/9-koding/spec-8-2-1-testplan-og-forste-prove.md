---
title: 'Story 8.2.1: Testplanen og første prøve fra en ny kopi'
type: 'chore'
created: '2026-11-21'
status: 'done'
baseline_commit: '8e13bf18a59c3cd956a581c96c0133142c31dcd5'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-8-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `my-project/testplan.md` har resultatene med ekte KI, men mangler resten av NFR-12: en oversikt over alle 14 suksesskriteriene, hele flyten for hånd i begge modusene, sjekkene av tilgjengelighet og skjermbredder, og prøven av README fra en ny kopi. Issue #16 (skriptene uten nettlesertester) står åpen.

**Approach:** Testplanen får en oversikt over kriteriene og nye seksjoner for det som prøves for hånd. KI-en måler det den kan selv: første prøve fra en ny kopi i terminalen, kontrasten i `stil.css`, og etikettene og alternativtekstene i HTML-en. Kristine prøver i nettleseren det som krever øyne og tastatur, og resultatene skrives inn med dato.

## Boundaries & Constraints

**Always:** Bare fiktive testdata. Hver rad har dato, hva som ble gjort, og bestått eller ikke bestått, og det som ikke består, skrives ærlig. Kristines formuleringer beholdes. Finner prøven en feil i README, rettes README i samme PR. Lærerens CI-sjekk må gå gjennom.

**Never:** Ingen nye funksjoner. Ingen API-nøkkel eller `.env` i repoet. Kriterium 1, 3, 11, 12 og 14 kjøres ikke på nytt (bestått, og promptene er ikke endret siden).

**Kristines beslutninger (2026-11-21):**
1. **Issue #16:** ingen nettlesertester. Testplanen får en tabell over hvert skript (hva det gjør, PR-ene det er prøvd i, og en siste prøve for hånd i 8.2.1). README nevner det under «Kjente begrensninger», og PR-en har «Closes #16».
2. **Deling:** 8.2.1 nå. Story 8.2.2 senere, med egen branch og PR: kriterium 13 og andre prøve fra en ny kopi rett før levering (ført i `deferred-work.md`). Testplanen viser begge som «kommer i 8.2.2».

</frozen-after-approval>

## Code Map

- `my-project/testplan.md` -- leveransen. Linje 3: innledningen. Linje 9–17: tabellen for kriteriene med ekte KI (beholdes). «Kostnad og tid» i hver runde (linje 60, 159, 189, 278, 329, 390) er grunnlaget for oppsummeringen av tokens og kroner per søknad. Linje 413–415: kriterium 5 mangler at .docx og PDF kan åpnes.
- Automatiske kriterier: 2, 4, 5 (treff), 8 og 14 nevnes med nummer i `backend/tests/test_testdata.py`, `web/test_resultat.py`, `kjerne/test_ki_svar.py`. 6, 9 og 10 testes med FR-numrene (FR-1, FR-3, FR-36, FR-4, FR-9–11) i `web/test_*.py`. Riktig testfil slås opp med `grep`. For hånd: 1, 3, 11, 12, 14 (ferdig), 5 (åpne filene), 7 (ny kopi), 13 (8.2.2).
- `backend/soknad/web/static/js/` -- de åtte skriptene: `innlegging.js`, `info.js`, `vente.js`, `nedlasting.js`, `endringer.js`, `bekreft.js`, `fyrverkeri.js`, `tilbake.js`. PR-ene der de er prøvd: `my-project/todo.md:177` og `deferred-work.md:28-49, 166-185`.
- `backend/soknad/web/static/css/stil.css` -- fargevariablene (WCAG AA: 4,5:1 for tekst, 3:1 for store tekster og rammer).
- `README.md:35-76` -- «Installasjon og oppstart», som følges i prøven. `README.md:121` -- «Kjente begrensninger».
- `deferred-work.md` (punktene som viser til 8.2 og #16), `.logs/kristine/issues.md:9-10, 63, 69, 73, 78, 80, 171, 176, 183, 186, 190`, `my-project/todo.md:177` -- krysses av.

## Tasks & Acceptance

**Execution:**
- [x] `my-project/testkjoringer/8-2/kontrast.py` -- regner ut kontrasten for fargeparene i `stil.css` og skriver en tabell -- NFR-6
- [x] KI-en (terminal) -- `git clone` til en tom mappe og README uten `.env`: `uv sync`, `uv run pytest`, `uv run flask --app soknad run`, innlogging med testbrukeren og en søknad i testmodus med case 1 over HTTP. Loggen i `my-project/testkjoringer/8-2/ny-kopi-1.txt` -- NFR-8, kriterium 7
- [x] `my-project/testplan.md` -- ny innledning, oversikt over alle 14 kriteriene (automatisk med testfil, eller for hånd med lenke), og seksjonene «Prøven fra en ny kopi», «Hele flyten for hånd», «Tilgjengelighet og skjermbredder», «Skriptene som prøves for hånd», «Kostnad per søknad» og «Kriterium 13» -- NFR-12
- [x] `README.md` -- kjent begrensning om at skriptene ikke har nettlesertester -- beslutning 1
- [x] Kristine (nettleser) -- hele flyten i testmodus (Full generering og Korrektur, case 1) og én gang med ekte KI (ca. 1 kr), åpne .docx og PDF, tastatur, synlige etiketter, 320/375/768/1280 px og 200 % zoom, og hvert skript i tabellen. KI-en skriver resultatene inn -- NFR-6, NFR-7, kriterium 5
- [x] `deferred-work.md`, `.logs/kristine/issues.md`, `my-project/todo.md` -- krysse av punktene for #16 og 8.2.1 -- regelen om utsatte punkter

**Acceptance Criteria:**
- Given `testplan.md`, when hvert av de 14 kriteriene slås opp i oversikten, then står det automatisk (med testfil) eller for hånd (med dato og resultat, eller «kommer i 8.2.2»)
- Given en tom mappe uten `.env`, when README følges, then starter nettsiden i testmodus, testbrukeren logger inn, og alle tester består, med dato og resultat i testplanen
- Given seksjonen om tilgjengelighet, when den leses, then har hver sjekk (tastatur, kontrast, etiketter, alternativtekst, fire bredder, 200 % zoom) dato og resultat
- Given PR-en, when den flettes, then lukkes issue #16, og CI er grønn

## Implementation Notes

- 2026-11-21: Alt KI-en kan gjøre selv, er gjort i commit `cc0f7b3`. Første prøve fra en ny kopi besto (1 393 tester, testbrukeren logger inn, case 1 gir 50 % som i fasiten), uten feil i README. Kontrasten: alle 24 parene med krav består (lavest 4,53:1). Etikettene: 14 sider uten feil. Testplanen har oversikten over alle 14 kriteriene, og testnavnene der er sjekket mot `backend/tests/`. Raden for Kristines nettleserprøve står igjen, og radene merket «Ikke prøvd ennå» fylles inn etter den. `deferred-work.md` er git-ignorert, så avkrysningen der finnes bare på PC-en. Merknad til Kristine: README sier ikke hvordan repoet hentes (`git clone` eller ZIP) eller at man må `cd G68-grande` etterpå.

## Spec Change Log

## Review Triage Log

| # | Funn (lag) | Dom | Begrunnelse | Rute |
| --- | --- | --- | --- | --- |
| 1 | Kontrasten sjekkes bare når skriptet kjøres for hånd, ikke i CI (verification) | medium | Bekreftet: `testpaths = ["tests"]`, og ingen test i `backend/tests` regner ut kontrast. En lysere `--success` ville gått gjennom CI | patch (pytest-test for kontrasten) |
| 2 | Etikettsjekken kjøres heller ikke i CI (verification) | medium | Bekreftet, men å flytte den til testklienten er mer enn en liten retting | defer |
| 3 | `#16`-punktene er krysset av før nettleserprøven, og ingen åpne punkter sporer Kristines rader (verification, blind, edge) | medium | Bekreftet: alle åtte skriptene og ca. 20 rader står som «Ikke prøvd ennå», uten eget punkt i `issues.md` eller `todo.md` | patch (åpne punkter for nettleserprøven) |
| 4 | `etiketter.py` sjekker ikke at den kom til riktig side (blind, edge ×2) | medium | Bekreftet: `side()` ser ikke på URL eller tittel. Feiler innloggingen, sjekkes innloggingssiden 12 ganger, og alt «består» | patch |
| 5 | Knapper med bare et skjult ikon (`aria-hidden`) regnes som knapper med tekst (blind, edge) | medium | Bekreftet: `handle_data` legger til all tekst inni `<button>` | patch |
| 6 | `aria-controls` og like `id`-er sjekkes ikke (blind, edge) | low | Bekreftet. Liten utvidelse av samme løkke | patch |
| 7 | `input type=submit/image` uten navn sjekkes ikke (blind, edge) | low | Malene bruker `<button>`, ikke slike `input` | Avvist |
| 8 | Tom `<label for>` går gjennom, og docstringen lover «synlig» (blind, edge) | low | Synligheten prøves for hånd (egen rad). Docstringen rettes | patch (bare docstringen) |
| 9 | Feiltilstandene (feil passord, KI-feilboksen, grensen på KI-kall) er ikke med, men testplanen sier «alle sidene» (blind, edge) | low | Bekreftet: 14 sider, bare én feiltilstand per modus | patch (ordlyden i testplanen) |
| 10 | Raden «Alternativtekst» sier at ikonene er sjekket med skriptet, men skriptet ser bare på `img`, `svg` og `canvas` (blind, edge) | medium | Bekreftet: ikonene er `<span>` med emoji | patch (ordlyden, eller skriptet sjekker spanene) |
| 11 | «Ca. 4 minutter» er for lavt, fordi pytest kjørte samtidig med nettsiden (blind) | low | Bekreftet i `ny-kopi-1.txt` | patch (ordlyden og loggen) |
| 12 | Den andre kjøringen av `etiketter.py` er ikke forklart, og stiene til skriptene i loggen stemmer ikke med kopien (blind) | low | Bekreftet: skriptene finnes ikke i kopien på `8e13bf1` | patch (loggen) |
| 13 | `http_prove.py` sjekker ingenting selv, og krasjer uten argumenter (blind, edge) | medium | Bekreftet: ingen `main()`, ingen `assert`. «Bestått» ble avgjort ved å lese utskriften | patch |
| 14 | `filename*=` og skråstrek på slutten i `http_prove.py` (edge) | low | Case 1 gir et filnavn uten særtegn, og skråstreken fjernes i rettingen av punkt 13 | Avvist |
| 15 | `kontrast.py` krasjer med `KeyError` ved et ukjent fargeformat (blind, edge) | low | Bekreftet. Rettingen er én linje | patch |
| 16 | Halvgjennomsiktige farger legges over `background`, ikke over bakgrunnen i paret (edge) | low | Ingen av de 25 parene bruker `rgba` | Avvist |
| 17 | Fargeparene er skrevet inn for hånd, og hover og deaktivert er ikke med (blind) | low | Valgt slik. Kravet gjelder fargene som brukes sammen | Avvist |
| 18 | Prøve 2 bør gjøres uten uv, med tomt mellomlager og i PowerShell (blind) | medium | Bekreftet: prøve 1 hadde uv og mellomlageret fra før | defer (story 8.2.2) |
| 19 | README-merknaden (`git clone`, `cd G68-grande`) spores ikke (blind) | low | Bekreftet: står bare i testplanen | patch (åpent punkt) |
| 20 | `issues.md` og `todo.md` er ikke enige om «Closes #16», og 8.2.2 mangler i `issues.md` (blind) | low | Bekreftet | patch |
| 21 | De to sjekkpunktene mangler «løst 2026-11-21:» (blind) | low | Bekreftet | patch |
| 22 | Kriterium 1, 3, 11, 12 og 14 har ingen dato i oversikten (edge) | low | Bekreftet: datoene står bare i seksjonene under | patch |
| 23 | `issues.md:12` sier at hele flyten i testmodus virket i kopien, men bare Full generering ble kjørt (edge) | low | Bekreftet: Korrektur ble bare hentet av `etiketter.py`, uten nedlasting | patch |

## Design Notes

Planen sa at første prøve skulle bruke README slik den var etter Epic 1–6, før 8.1. 8.1 er ferdig, så første prøve bruker README slik den er nå (21. november), før kodestopp. Det står i testplanen. Hensikten, å finne feil i README tidlig, er den samme.

## Verification

**Commands:**
- `cd backend && uv run pytest` -- expected: alle tester grønne
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil
- `uv run python my-project/testkjoringer/8-2/kontrast.py` -- expected: alle tekstpar minst 4,5:1

**Manual checks (if no CLI):**
- Alle relative lenker i `testplan.md` peker på filer som finnes
