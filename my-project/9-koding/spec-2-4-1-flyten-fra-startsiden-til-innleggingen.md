---
title: 'Story 2.4.1: Flyten fra startsiden til innleggingen'
type: 'feature'
created: '2026-11-09'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '6dba0f812305797e8c0414e0447f0fbb1c1742c6'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Startsiden har bare velkomsten. Det finnes ingen søknad i økten, ingen steg og ingen vei videre, så man kan ikke begynne på en søknad (FR-5, FR-20).

**Approach:** Kjernen får `Soknad` og stegmodellen (AD-7, AD-8), og øktlageret lagrer søknaden. Web får «Begynn å lage søknad» på startsiden, modusvalget med kortet Full generering og en innleggingsside med bare overskriften (feltene kommer i story 2.5). Story 2.4 er delt i to: bryteren, statusteksten om testmodus og merkelappen «Testmodus» kommer i 2.4.2.

## Boundaries & Constraints

**Always:**
- Steg: start < modus < innlegging < resultat < brev. En side vises bare når sidens steg ≤ `Soknad.steg`, ellers redirect til siden for steget. Gjelder også POST.
- GET `/` lager alltid en ny `Soknad` (steg start). `Innlogging` (og testmodus) røres ikke. Mangler søknad i økten, regnes det som en ny søknad på steg start.
- Steget flyttes bare etter en POST som har lyktes, og da kommer redirect. «Begynn å lage søknad» gir steg modus (aldri lavere enn før). Et trykk på kortet kaller `velg_modus`, som setter modus, setter steget til innlegging og nullstiller `gap`. CV, annonse og nøkkelordlisten beholdes.
- Ukjent modus i POST: samme side på nytt uten redirect (status 400), og søknaden er uendret.
- «Begynn å lage søknad» er den største knappen (1,5rem, padding 24px 64px; under 700 px 1,25rem og hele bredden).
- Modusvalget: `h1` «Hva vil du gjøre i dag?», kortet ✨ «Full generering» · «Skriv nytt brev» · «Du legger inn CV-en og annonsen, så skriver vi et brev til deg.» som én knapp (ikonet skjult for skjermlesere). «Tilbake» (sekundærknapp, til venstre) er en lenke til `/`.
- Innleggingssiden: `h1` «Legg inn CV-en din og stillingsannonsen».
- Utlogging sletter også søknaden. Alle nye tekster ligger i `web/tekster.py`.

**Never:**
- Ingen bryter, statustekst om testmodus eller merkelapp «Testmodus» (story 2.4.2).
- Ingen samtykke eller KI-merknad (Epic 4), ikke kortet Korrektur (Epic 5), ikke ikonet som vipper (Epic 7).
- Ingen felt eller knapper på innleggingssiden (story 2.5). Ingen JavaScript som endrer søknadsdata.
- Kjernen importerer ikke flask og leser ingen filer.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Ny søknad | søknad på steg innlegging, GET `/` | ny `Soknad` på steg start, samme `Innlogging` | – |
| Begynn | POST `/` | steg modus, redirect til `/modus` | – |
| Velg modus | steg modus, POST `/modus` med `full_generering` | modus satt, steg innlegging, redirect til `/innlegging` | – |
| Hoppe over steg | steg start, GET `/modus` eller `/innlegging` | redirect til `/` | – |
| POST for tidlig | steg start, POST `/modus` | redirect til `/`, søknaden uendret | – |
| Ukjent modus | POST `/modus` med `tull` | modusvalget på nytt, status 400 | søknaden uendret |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/okt.py` -- `Innlogging` (frossen). `Modus`, `Tekstfelt`, `Soknad`, `begynn` og `velg_modus` legges her.
- `backend/soknad/adaptere/oktlager.py` -- lagrer `Innlogging` per økt-id med lås. Søknaden lagres ved siden av, og `slett` sletter begge.
- `backend/soknad/web/innlogging.py` -- `login_required` (setter `no-store`), `logg_ut_bruker` (kommentaren om Epic 2 fjernes).
- `backend/soknad/web/ruter.py` -- `start` og `felles_tekster`. Nye ruter her.
- `backend/soknad/web/static/css/stil.css` -- alle tokens finnes alt. Bruk `var(--…)`, ingen fargekoder.
- `backend/tests/web/test_alle_sider.py` -- finner nye ruter av seg selv. Legg `web.modus` og `web.innlegging` til i settet som sjekkes.
- `backend/tests/web/hjelpere.py` -- `tagger_i`, `logg_inn`, `okt_id`. Gjenbruk.
- Skisse: `_bmad-output/planning-artifacts/ux-designs/ux-kode-prosjekt-2026-10-20/mockups/mode-select-1.html`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/steg.py` (ny) -- `Steg(IntEnum)` og `kan_vises(side, steg) -> bool`. Importerer ikke `okt`.
- [x] `backend/soknad/kjerne/okt.py` -- `Modus(StrEnum)` med `FULL_GENERERING = "full_generering"`, frossen `Tekstfelt(tekst="", filnavn=None)`, frossen `Soknad` med standardverdier (`steg`, `modus`, `samtykke`, `cv`, `annonse`, `eget_brev`, `nokkelord`, `nokkelord_annonse`, `arbeidsgiver`, `gap`, `opptatt`), `begynn(soknad)` og `velg_modus(soknad, modus)` med `dataclasses.replace`.
- [x] `backend/soknad/adaptere/oktlager.py` -- `hent_soknad(okt_id)` og `lagre_soknad(okt_id, soknad)` (lagrer bare når økten finnes). `slett` sletter begge.
- [x] `backend/soknad/web/flyt.py` (ny) -- `gjeldende_soknad()`, `lagre_soknad(soknad)`, `SIDE_FOR_STEG` (start, modus, innlegging) og dekoratoren `krever_steg(steg)`.
- [x] `backend/soknad/web/ruter.py` og `web/tekster.py` -- GET/POST `/`, GET/POST `/modus`, GET `/innlegging`.
- [x] `backend/soknad/web/templates/` -- `start.html` (skjema med stor knapp), `modus.html` og `innlegging.html` (nye).
- [x] `backend/soknad/web/static/css/stil.css` -- stor knapp, modus-kort (hover løfter 4 px, ramme i primary, sterkere skygge; trykk 97 %), kortrutenett (to kolonner fra 700 px), knapperad. Ingen `nowrap`, ingen faste høyder.
- [x] Tester -- `tests/kjerne/test_steg.py`, `test_okt.py`, `tests/adaptere/test_oktlager.py`, `tests/web/test_startside.py`, `test_modusvalg.py` og `test_utlogging.py`: én test per rad i matrisen, og at utlogging sletter søknaden. FR-nummer i navn og docstring.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (231 før denne storyen).
- Given `ruff check` og `ruff format --check`, when de kjører, then er det ingen feil.
- Given nettsiden i nettleseren, when jeg logger inn, trykker «Begynn å lage søknad» og så kortet, then kommer jeg til innleggingen, og ingen side ruller sidelengs ved 320 og 375 px.

## Implementation Notes

- Story 2.4 ble delt i 2.4.1 (denne) og 2.4.2 (det som viser testmodus, står i `deferred-work.md`), fordi den samlede spec-en var på ca. 2500 tokens. Kristine valgte å dele.
- Hovedøkta skrev koden selv (ingen hjelpeagent), som i story 2.3.
- Branch: `story/2-4-1-flyten-fra-startsiden-til-innleggingen`.
- Teksten på modus-kortene ligger i `tekster.MODUS_KORT` (ordbok fra `Modus` til `ModusKort`), så kortet Korrektur i Epic 5 bare er én ny linje. En test sjekker at hver `Modus` har et kort.
- Kortene står i en flex-rad som brytes, ikke i et rutenett med to kolonner. Da står ett kort alene i midten fram til Epic 5. Fra 700 px er hvert kort halve bredden.
- «Tilbake» er en lenke med klassen `sekundaerknapp`. Den klassen har nå `display: inline-block` og `text-decoration: none`.
- `Oktlager.lagre_soknad` lagrer bare når innloggingen finnes, så en søknad aldri blir liggende igjen etter utlogging.
- Tester: 41 nye, 272 i alt, `ruff` grønn. Bredder i nettleseren (320/375 px) er ikke sjekket av hovedøkta. Det gjøres i gjennomgangen sammen med Kristine.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-09), tre lag: blind, grensetilfeller, testhull. Testhull-laget fant ingen hull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | GET `/` sletter søknaden, også via «Tilbake», nettleserens tilbakeknapp og oppfriskning | blind, testhull | false | Bestemt i EXPERIENCE (State Patterns: «Det starter alltid en ny søknad med tomme felt … også via Tilbake») og AD-7. Test for det finnes (`test_fr5_startsiden_lager_ny_soknad_…`) | avvist |
| 2 | Lese, endre og lagre søknaden skjer ikke under én lås, så to faner kan overskrive hverandre | blind, grensetilfeller | low | Riktig, men krever to forespørsler på nesten samme tid i samme økt. Rettingen er en ny metode i øktlageret, ikke en direkte retting. `opptatt` rundt KI-kall kommer i story 2.5/2.7 | avvist |
| 3 | `gap: dict` kan endres på stedet, og `hash(soknad)` feiler når `gap` er satt | blind | low | Ingen kode hasher `Soknad` eller endrer `gap` på stedet. Formen på `gap` bestemmes i story 2.5, når den settes første gang | avvist |
| 4 | `SIDE_FOR_STEG[steg]` gir KeyError for resultat og brev | blind | false | Ingen kode kan sette steget til resultat eller brev ennå. Sidene legges i tabellen i story 2.6 og Epic 3 | avvist |
| 5 | Ukjent modus gir 400 uten melding | blind | false | Skjer bare ved en POST som er laget for hånd. Bestemt i spec-en (samme side, status 400) | avvist |
| 6 | Docstringer lover mer enn testene sjekker (største knapp, «Tilbake» til venstre, én h1 på innleggingen) | blind | low | Riktig. Docstringene er rettet, og testen for innleggingen sjekker nå at det er én h1 | patch |
| 7 | `"Velg" not in html` og `"Korrektur" not in html` feiler på framtidig tekst | blind | low | Riktig. Fjernet. Sjekken av knappelisten dekker kravet | patch |
| 8 | Modusvalget viser ikke hvilken modus som er valgt | blind | low | Ikke et krav i UX, og med én modus er det ingenting å velge mellom | avvist |
| 9 | POST `/` og `/modus` uten CSRF-token eller `SESSION_COOKIE_SAMESITE` | blind, grensetilfeller | low | Gjelder hele nettsiden fra før (Epic 1). Arkitekturen godtar det når README sier det | defer |
| 10 | `test_fr20_sidene_lagres_ikke_i_nettleseren` sier FR-6 i docstringen | blind | low | Riktig. Omdøpt til `test_fr6_…` | patch |
| 11 | Testen for utlogging bruker øktlageret direkte, og en test leser `_soknader` | blind | false | Testen må bruke den gamle økt-id-en etter utlogging, og hjelperen bruker cookien. `_soknader` er den eneste måten å se at ingenting er lagret | avvist |
| 12 | `lagre_soknad` gjør stille ingenting uten økt | blind | false | Med vilje, så ingen søknad blir liggende etter utlogging. Test finnes | avvist |
| 13 | Docstringen «Varer én søknad.» er uklar, og feltnavnene for Epic 3/5 låses i en kommentar | blind | false | Samme ordlyd som AD-7 og `Innlogging`. Feltnavnene står i AD-7 | avvist |

## Design Notes

`Steg` ligger i `steg.py` uten import av `okt`, så `okt.py` kan importere `Steg` uten at filene importerer hverandre. `velg_modus` setter alltid steget til innlegging, fordi analysen skal kjøres på nytt før resultatsiden vises igjen.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- I nettleseren: startsiden med den store knappen, modusvalget, innleggingen og «Tilbake» til startsiden. Sjekk 375 px og 1280 px.
