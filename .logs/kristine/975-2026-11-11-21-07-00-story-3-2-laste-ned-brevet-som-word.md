# Story 3.2: Laste ned brevet som Word

## 2026-11-11 kl. 21:06 — Kristine

### Oppgave
`/bmad-build 3.2`: lage nedlastingen av søknadsbrevet som Word-fil fra brevsiden, slik story 3.2 i epics beskriver.

### Plan
- Planen ligger i [`my-project/9-koding/spec-3-2-laste-ned-brevet-som-word.md`](../../my-project/9-koding/spec-3-2-laste-ned-brevet-som-word.md) (kopi av `_bmad-output/implementation-artifacts/`).
- Kristine godkjente planen med én endring: feilboksen skal ikke ha «Brevet er ikke borte.».
- Branch `story/3-2-laste-ned-brevet-som-word` fra `main` (`fb66299`). Koden er skrevet i hovedøkten, og tre hjelpeagenter gikk gjennom den (blind, kanttilfeller, testhull).

### Resultat
- `fdcefb8` (kode): «Last ned som Word» under brevet, `GET /last-ned/docx`, `adaptere/fil_ut.py` (python-docx 1.2.0, A4, norsk bokmål, ett avsnitt per avsnitt, uten topp- og bunntekst), `kjerne/filnavn.py` (`Soknad_<ÅÅÅÅ-MM-DD>.docx`), `Soknad.lastet_ned`, `FilFeil` med feilboks, grønn knapp og filnavnlinje (`nedlasting.js`).
- Gjennomgangen ga 17 funn: 2 rettet (A4 og norsk språk i Word-fila, som ble KI-feilen i prompt-loggen), 1 utsatt (skriptet testes bare ved å lese teksten, lagt til issue #16 i TO DO og i `deferred-work.md`) og 14 avvist med begrunnelse.
- 549 tester grønne, `ruff check` og `ruff format --check` grønne.
- `53bf578` (dokumentasjon): spec-kopi, oversikten i `my-project/README.md`, TO DO, prompt-logg 329–330 og sprint-statusen (3.2 er «review»).
- Notat om KI-feilen er lagt i `my-project/8-refleksjonsrapport/notater.md`. Mappa er med i `.gitignore`, så notatet ligger bare lokalt.
- Branchen er ikke pushet.

### Åpne punkter
- Prøve story 3.2 i nettleseren: laste ned, åpne fila i Word (A4, norsk, ingen topp- eller bunntekst), se at knappen blir grønn med filnavnet, og sjekke 320 px og 200 % zoom.
- Story 3.2: push, PR med merknad om KI-feil og kommentar om prøvingen i nettleseren, grønn CI og flette.

## 2026-11-11 kl. 21:25 — Kristine

### Oppgave
Prøve story 3.2 i nettleseren: åpne nettsiden og annonsen fra case 1.

### Plan
- Starte nettsiden, åpne annonsen og la Kristine gå gjennom de manuelle sjekkene i spec-en.

### Resultat
- Kristine prøvde alt: nedlastingen, fila i Word og den grønne knappen. «Alt er testet og ser bra ut.»
- Notisblokk viste først CV-en fra et vindu som var åpent fra før. Annonseteksten ble kopiert til utklippstavlen og åpnet på nytt.
- Nettsiden er stoppet. TO DO og prompt-logg 331–332 er oppdatert. Punktet om å prøve i nettleseren er lukket i `issues.md`.

### Åpne punkter
- Story 3.2: push, PR med merknad om KI-feil og kommentar om prøvingen, grønn CI og flette (står fra før i `issues.md`).

## 2026-11-11 kl. 21:17 — Kristine

### Oppgave
«push»: pushe branchen for story 3.2 og lage PR-en.

### Plan
- Pushe branchen, lage PR med merknad om KI-feil, kommentere prøvingen i nettleseren og føre PR-en inn i TO DO og prompt-loggen.

### Resultat
- Branchen `story/3-2-laste-ned-brevet-som-word` er pushet, og [PR #20](https://github.com/IBE160-2026/G68-grande/pull/20) er laget med merknad om KI-feilen (Letter-papir og engelsk språk i Word-fila) og en kommentar om prøvingen i nettleseren.
- `314892f`: PR #20 i TO DO og prompt-logg 333.

### Åpne punkter
- Story 3.2: grønn CI og flette PR #20. Deretter sette 3.2 til ferdig i sprint-statusen, kopien, oversikten og TO DO.

## 2026-11-11 kl. 22:06 — Kristine

### Oppgave
PR #20 er flettet og branchen slettet på GitHub. Avslutte story 3.2.

### Plan
- Hente `main`, slette branchen lokalt, sette 3.2 til ferdig og pushe oppdateringene.

### Resultat
- `main` hentet (`9ef7002`), og branchen er slettet lokalt. `7edce26`: story 3.2 ferdig i sprint-statusen (begge kopiene), TO DO, oversikten med PR-lenken og prompt-logg 334. Pushet til `main`.
- PR-en ble flettet før CI hadde kjørt. Alle CI-kjøringene (to for PR-en, to for `main`) sto i kø uten jobber. Årsaken var en feil hos GitHub: «Actions is experiencing degraded availability» (githubstatus.com, fra kl. 21:48). Avbryting gikk ikke, fordi kjøringene aldri startet.
- Lærdom: vent med å flette til PR-en har grønn hake for både Linux og Windows.

### Åpne punkter
- Sjekke at CI på `main` (`7edce26`) blir grønn når GitHub Actions virker igjen. Står kjøringene fortsatt i kø etter at feilen er rettet: «Re-run». Blir den rød: rett i en liten ny PR.

## 2026-11-12 kl. 19:06 — Kristine

### Oppgave
Sjekke om GitHub Actions virker igjen, og om CI er grønn etter story 3.2.

### Plan
- Hente fra GitHub, se på CI-kjøringene og statussiden til GitHub.

### Resultat
- GitHub virker igjen («All Systems Operational»).
- Bård Pettersen har pushet to dokumenter til `main`: `my-project/2-prd/tilbakemelding-prd.md` og `my-project/5-arkitektur/technology.md`. Hentet med `git pull --rebase`.
- CI for den nyeste `main` (`60c53f0`) er grønn. Den inneholder koden fra story 3.2 (`7edce26`), så koden er sjekket på Linux og Windows. Den første CI-kjøringen for PR #20 ble også grønn.
- De gamle kjøringene fra 11. november står fortsatt som «queued» hos GitHub. De kan ikke avbrytes og har ingen betydning.

### Åpne punkter
- Lese tilbakemeldingen på PRD-en fra læreren (`my-project/2-prd/tilbakemelding-prd.md`).
