---
title: 'Rettinger fra retrospektiven for epic 2'
type: 'bugfix'
created: '2026-11-10'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'ca1df8575e20e17d1b82efe90362cce76691706e'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-retro-2026-11-10.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Retrospektiven for epic 2 fant fire ting som bør ordnes før epic 3 (action item 1–4). Et KI-kall som pågår, kan skrive den gamle søknaden over en ny søknad fra startsiden i en annen fane (A1). Ingen test sjekker at KI-en kalles på nytt etter «Tilbake» fra resultatsiden (A2). Utlogging i en annen fane midt i «Sjekk CV-en min» kan gi en 500-side (A3). Hjelpeteksten sier `testdata/`, men mappen er `backend/testdata/` (A12).

**Approach:** Én liten PR. Kristine har bestemt (2026-11-10): den nye søknaden fra startsiden vinner over KI-svaret, utlogging midt i kallet gir innloggingen, og hjelpeteksten og README sier `backend/testdata/`.

## Boundaries & Constraints

**Always:**
- Når KI-kallet er ferdig (lyktes, `KIFeil` eller annet unntak), lagres resultatet bare hvis søknaden i øktlageret fortsatt er den som ble satt opptatt. Er den byttet ut (ny søknad fra startsiden), blir den nye stående uendret.
- Følger AD-8: en ny POST mens `opptatt` er sann, sendes til siden for steget uten å endre søknaden. Det gjelder nå også «Begynn å lage søknad» (`POST /`) og modus-kortet (`POST /modus`), ikke bare innleggingen. `GET /` lager alltid en ny søknad, også mens en annen er opptatt (UX: startsiden starter alltid en ny søknad).
- Finnes ikke innloggingen lenger når innleggingen skal sjekke testmodus, tømmes cookien, og brukeren sendes til `/logg-inn?ikke_innlogget=1` («Du må logge inn først»), som `login_required` gjør.
- Hjelpeteksten blir ordrett «Testmodus: bruk filene i mappen backend/testdata/ i prosjektet.» I DESIGN.md og skissen beholdes formateringen (`backend/testdata/` i kode). README, «Kjente begrensninger»: «**I testmodus virker bare de fiktive testdataene i `backend/testdata/`.**»
- Hver test nevner FR-, NFR- eller AD-nummeret, som før.

**Never:**
- Feilteksten «… fra mappen testdata/.» endres ikke (Kristine ser på den i PR-en). Ingen andre tekster endres.
- Ingen endring i `vente.js`, malene eller utseendet. Ingen nye avhengigheter.
- Historiske dokumenter endres ikke: ferdige spec-er, `epic-2-context.md`, `.memlog.md`/`ux-memlog.md`, sesjonslogger og prompt-loggen.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Ny søknad under kallet | `GET /` midt i KI-kallet, kallet lykkes | Søknaden etterpå er `Soknad()` (steg start). POST-en gir 302 til `/resultat`, som sender til `/` | N/A |
| Ny søknad, KI-feil | `GET /` midt i kallet, kallet gir `KIFeil` | Søknaden etterpå er `Soknad()` | Siden med KI-feilen vises for den første POST-en |
| Begynn eller kort under kallet | `POST /` eller `POST /modus` mens opptatt | 302 til siden for steget, søknaden uendret | N/A |
| Vanlig kall | Ingen annen fane | Som før: analysen lagres, ikke opptatt | N/A |
| Utlogget før testmodus-sjekken | Økten slettes etter `login_required`, før sjekken | 302 til `/logg-inn?ikke_innlogget=1`, ingen 500 | Cookien tømmes |
| «Tilbake» fra resultatsiden | Samme CV og annonse, «Sjekk CV-en min» | KI-en kalles: `["nokkelord", "gap"]`, 302 til `/resultat` | N/A |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/oktlager.py` -- `Oktlager`. Ny metode som erstatter søknaden bare når den lagrede er samme objekt som forventet (`is`), under `self._las` og bare når økten finnes.
- `backend/soknad/web/flyt.py` -- `lagre_soknad`, `gjeldende_soknad`, `SIDE_FOR_STEG`. Naturlig sted for en hjelper som erstatter søknaden og en som sender til steget når søknaden er opptatt.
- `backend/soknad/web/ruter.py` -- `start` POST (linje 48-50), `modus` POST (64-70), `innlegging` (86-117: `opptatt`-sjekken 87-88, `gjeldende_innlogging()` 99-100, `sett_opptatt` 107, `finally` 115-116).
- `backend/soknad/web/tekster.py:53` -- `TESTDATA_HJELP`.
- `backend/tests/web/test_ventetegn.py` -- `SpionKI` (kaller kode midt i kallet), `paa_innlegging`, `send`, `test_fr27_ny_post_mens_opptatt_sender_til_steget` (mønster for opptatt-testene).
- `backend/tests/web/hjelpere.py` -- `FeilendeKI(..., oppgave=None, kalt=kalt)`, `sett_soknad`, `soknaden`, `okt_id`.
- `backend/tests/web/test_resultat.py:460` -- `test_fr15_kriterium_8_samme_treff_etter_tilbake`, utvides med `kalt`.
- `backend/tests/web/test_innlegging.py:399-410` -- testen av hjelpeteksten.
- Dokumenter med hjelpeteksten: `_bmad-output/planning-artifacts/epics.md:502`, `ux-designs/ux-kode-prosjekt-2026-10-20/EXPERIENCE.md:133`, `DESIGN.md:431`, `mockups/input-page-1.html:154`, og kopiene i `my-project/6-epics-og-stories/epics.md`, `my-project/3-ux/EXPERIENCE.md`, `DESIGN.md` og `skisser/input-page-1.html`. `README.md:86`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/adaptere/oktlager.py` -- metoden som erstatter bare forventet søknad -- A1.
- [x] `backend/soknad/web/flyt.py` og `backend/soknad/web/ruter.py` -- `finally` bruker den nye metoden med søknaden som ble satt opptatt. `POST /` og `POST /modus` sender til steget når søknaden er opptatt. Innleggingen sender til innloggingen når innloggingen mangler -- A1, A3.
- [x] `backend/soknad/web/tekster.py` og `backend/tests/web/test_innlegging.py` -- ny hjelpetekst -- A12.
- [x] `backend/tests/` -- tester for matrisen: oktlager-metoden, `GET /` midt i kallet (lykkes og `KIFeil`), `POST /` og `POST /modus` mens opptatt, utlogget før testmodus-sjekken (økten slettes med `monkeypatch` før sjekken), og `kalt` i kriterium 8-testen -- A1, A2, A3.
- [x] Dokumentene i Code Map og `README.md` -- ny hjelpetekst -- A12.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` og `uv run ruff check` kjøres, then er alt grønt.
- Given at `finally` lagrer ubetinget som før, when testen for `GET /` midt i kallet kjøres, then feiler den.
- Given repoet, when man søker etter «mappen testdata/ i prosjektet» utenfor de historiske dokumentene, then er det ingen treff.

## Implementation Notes

- Branch: `retro-2-rettinger`. Koden ble skrevet av en hjelpeagent ut fra spec-en.
- `Oktlager.erstatt_soknad` sammenligner med `is`. `flyt.py` har `erstatt_soknad` og `til_steget_hvis_opptatt`, og `innlogging.py` har `til_innloggingen`, som `login_required` også bruker.
- Hjelperen satte `finally` tilbake til å lagre uten sjekk, og da feilet begge testene med startsiden midt i kallet (kriterium 2). Uten sjekken av manglende innlogging feilet A3-testen.
- Kopiene i `_bmad-output/planning-artifacts/` er endret lokalt, men den mappen er ikke i Git. Kopiene i `my-project/` er i Git.
- Tester: 12 nye (én etter gjennomgangen), 441 i alt, alle grønne. `ruff` uten feil.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-10), tre lag: blind, grensetilfeller, testhull. Testhull-laget fant ingen hull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Startsiden kan treffe mellom sjekken av `opptatt` og lagringen av opptatt-søknaden, og bli skrevet over | blind, grensetilfeller | low | Riktig, men vinduet er noen mikrosekunder uten KI-kall. Det lange vinduet (KI-kallet) er rettet. Rettingen ville være nye greiner | avvist |
| 2 | To POST-er på innleggingen samtidig kan begge starte KI-kallet | blind, grensetilfeller | false | Bestemt av Kristine 2026-11-09: låsen i `vente.js` løser det. Ikke en del av denne spec-en | avvist |
| 3 | Utlogging etter sjekken av innlogging, men før opptatt lagres, gir KI-kall for en utlogget økt | grensetilfeller | low | Riktig, men vinduet er mikrosekunder, og `finally` lagrer ingenting uten økt | avvist |
| 4 | Ved KI-feil etter at startsiden har laget ny søknad, vises KI-feilsiden med de gamle feltene, og «Prøv på nytt» går til startsiden | blind, grensetilfeller | false | Slik matrisen sier: «Siden med KI-feilen vises for den første POST-en». Godkjent av Kristine | avvist |
| 5 | Svaret fra `erstatt_soknad` brukes ikke, så brukeren sendes via `/resultat` til `/` uten melding | blind, grensetilfeller | false | Slik matrisen sier: «302 til `/resultat`, som sender til `/`» | avvist |
| 6 | Kommentaren om lagringen står over feil linje, og «finally lagrer én gang» stemmer ikke lenger | blind | low | Riktig. Kommentaren er skrevet om | patch |
| 7 | Testen gir `forventet=None` selv om typen er `Soknad`, og leser `_soknader` | blind, grensetilfeller | low | Riktig. Testen bruker nå `Soknad()` og `hent_soknad`, og docstringen sier at sjekken er på `is` | patch |
| 8 | `til_steget_hvis_opptatt` og `til_innloggingen` mangler returtype | blind | low | Riktig. Lagt til | patch |
| 9 | Hjelpeteksten sier `backend/testdata/`, men feilteksten sier fortsatt `testdata/` | blind, grensetilfeller | false | Spec-en sier at feilteksten ikke endres, fordi Kristine bestemmer det i PR-en | avvist |
| 10 | Ingen test av utlogging i en annen fane mens KI-kallet går | blind | low | Riktig, bare grensen før testmodus-sjekken var testet. Ny test | patch |
| 11 | Testen med KI-feil sjekker ikke at startsiden faktisk ble åpnet | blind | low | Riktig. Testen sjekker nå statuskoden | patch |
| 12 | Ingen test for et uventet unntak etter at søknaden er byttet ut | blind | low | Samme `finally`-linje som for KI-feil, og `erstatt_soknad` er testet for seg | avvist |
| 13 | `SIDE_FOR_STEG` mangler brevsteget, så `til_steget_hvis_opptatt` kan gi `KeyError` | grensetilfeller | low | Fantes før (A8 i retrospektiven). Ingen søknad kan få brevsteget før Epic 3 | utsatt |
| 14 | TO DO, sprint-status og prompt-loggen er ikke oppdatert i diffen | blind | false | Det gjøres etter fletting, som for de andre storiene | avvist |

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle grønne
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Innleggingen i testmodus: hjelpeteksten sier `backend/testdata/`.
- Case 1 til resultatsiden, «Tilbake», «Sjekk CV-en min»: ventetegnet og så «7 av 11 = 64 %».
