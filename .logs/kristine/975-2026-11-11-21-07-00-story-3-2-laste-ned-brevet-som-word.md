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
