---
title: 'Story 7.5: Logg ut før nedlasting, og arbeidsgiver i filnavnet'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_commit: 'e95513d116f6b116e7ea1c50a18afa782f2e4eaf'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-7-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Trykker brukeren «Logg ut» på brevsiden før brevet er lastet ned, er brevet borte uten advarsel. Filnavnet er alltid `Soknad_<dato>`, så flere søknader er vanskelige å skille (UX-DR17, UX-DR22, AD-11, retro 4 punkt B9).

**Approach:** «Logg ut» på brevsiden åpner vinduet «Du har ikke lastet ned brevet.» når brevet ikke er lastet ned i noe format, med det samme skriptet som vinduet «Nytt forslag» (`bekreft.js`). Filnavnet får arbeidsgiveren fra nøkkelordsvaret, renset i `kjerne/filnavn.py`.

## Boundaries & Constraints

**Always:**
- Vinduet som i skissen Kristine godkjente (`mockups/letter-page-1.html:176-185`): overskrift «Du har ikke lastet ned brevet.», tekst «Vil du logge ut likevel? Brevet blir slettet.», knappene «Logg ut» (hovedknapp) og «Avbryt» (sekundærknapp). `<dialog>` med `aria-labelledby` og `aria-describedby`, fokus til «Avbryt», Esc lukker, fokus tilbake til «Logg ut» nede til høyre.
- Vinduet gjelder bare brevsiden, og bare når `lastet_ned` er tom. Er brevet lastet ned (også i samme visning, før siden lastes på nytt), logges brukeren ut med en gang (NFR-4).
- Filnavn: `Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>.<endelse>`. æ → ae, ø → o, å → a (store: Æ → Ae, Ø → O, Å → A), andre tegn til ASCII, alt mellomrom (også linjeskift og tab) til bindestrek, alt annet enn `[A-Za-z0-9-]` fjernes, høyst 30 tegn. Uten arbeidsgiver, eller når ingenting er igjen etter rensingen: `Soknad_<dato>.<endelse>`.
- Filnavnet i vinduet etter nedlasting, i filnavn-linjen og i filen er det samme, i begge modusene og begge formatene.
- Skript endrer aldri søknadsdata (AD-1). Tester nevner FR-/UX-DR-/AD-nummeret, bruker `tests/web/hjelpere.py`, og nye tester ligger i nye filer.

**Never:**
- Ingen endring i `logg_ut`-ruten eller i kjernen utenom `filnavn.py` (og en kommentar i `ki_svar.py`).
- Ingen nettlesertester (issue #16, story 8.2). Skriptene prøves for hånd i PR-en.
- Ingen `style=`, ingen nye fargekoder, ingen `nowrap`.

**Mine valg (kan endres av Kristine ved godkjenningen):**
- Flere bindestreker etter hverandre blir én, og bindestrek først eller sist i arbeidsgiveren fjernes (også etter kuttet til 30 tegn). «Bergen & Co» blir `Bergen-Co`, ikke `Bergen--Co`.
- Uten JavaScript logges brukeren ut med en gang, uten vinduet (som «Nytt forslag» uten JavaScript).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Ikke lastet ned | Brevsiden, `lastet_ned` tom, «Logg ut» | Vinduet åpnes, fokus på «Avbryt» | N/A |
| Logg ut likevel | Vinduet, «Logg ut» | POST `/logg-ut`, innloggingssiden | N/A |
| Lastet ned før | Brevsiden, `lastet_ned` ikke tom | Logget ut med en gang | N/A |
| Lastet ned nå | Trykk på «Last ned som …», så «Bli her» og «Logg ut» | Logget ut med en gang (skriptet tar bort vinduet fra knappen) | N/A |
| Nytt forslag | Etter nedlasting, nytt brev | `lastet_ned` tom igjen, vinduet kommer tilbake | N/A |
| Andre sider | Start, innlegging, resultat | «Logg ut» som før | N/A |
| Case 1 | «Testvik Utvikling AS» | `Soknad_Testvik-Utvikling-AS_<dato>.docx` | N/A |
| Case 2 | «Prøvdal Regnskap AS» | `Soknad_Provdal-Regnskap-AS_<dato>.pdf` | N/A |
| Spesialtegn | «Café/Bar: Ål\nAS» | `Soknad_CafeBar-Al-AS_<dato>` | N/A |
| Lang | 40 tegn | Arbeidsgiver kuttet til ≤ 30 tegn, ingen bindestrek til slutt | N/A |
| Mangler | `None`, `""` eller bare «/:» | `Soknad_<dato>` | N/A |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/filnavn.py` -- `lag_filnavn(dato, endelse, arbeidsgiver=None)` og en privat rensefunksjon (`unicodedata` NFKD + `encode("ascii", "ignore")` etter æøå-tabellen, `re` for mellomrom og tillatte tegn). Oppdater docstringen (Epic 7 er her nå).
- `backend/soknad/web/ruter.py:398` (`last_ned`) og `:674` (`_vis_brev`) -- send med `lagret.arbeidsgiver` / `soknad.arbeidsgiver`. `_vis_brev` sender også `advar_utlogging=not soknad.lastet_ned`.
- `backend/soknad/web/templates/base.html:38-40` -- «Logg ut»-knappen får `data-bekreft="vindu-logg-ut"` bare når `advar_utlogging` er sann (udefinert på andre sider). Utvid kommentaren.
- `backend/soknad/web/templates/vindu_logg_ut.html` (ny) -- som `vindu_nytt_forslag.html`: `id="vindu-logg-ut"`, «Logg ut» er `type="button"` med `data-bekreft-ja`, «Avbryt» i `<form method="dialog">` med `autofocus`. Tas med i `{% block vinduer %}` i `brev.html` bare når `advar_utlogging`.
- `backend/soknad/web/static/js/bekreft.js` -- virker alt for alle `data-bekreft`-knapper («Ja» → `requestSubmit` med knappen som åpnet). Bare kommentaren øverst nevner det nye vinduet.
- `backend/soknad/web/static/js/nedlasting.js` -- ved trykk på en nedlastingslenke: ta bort `data-bekreft` fra knappen med `[data-bekreft="vindu-logg-ut"]`. Oppdater kommentaren.
- `backend/soknad/web/tekster.py:260-280` -- `VINDU_LOGG_UT_OVERSKRIFT` og `VINDU_LOGG_UT_TEKST`. Gjenbruk `LOGG_UT_KNAPP` og `AVBRYT_KNAPP`.
- `backend/soknad/kjerne/ki_svar.py:206` -- kommentaren «renses ikke arbeidsgiver før story 7.5» → renses i `filnavn.py`.
- `backend/tests/web/hjelpere.py:179` `filnavn_i_dag` -- tar også arbeidsgiver, så testene for nedlasting (`test_nedlasting.py:53`, `test_nedlasting_pdf.py:89` og andre som bruker den) får filnavnet med arbeidsgiveren fra caset de bruker.
- Mønstre: `vindu_nytt_forslag.html`, `test_nytt_forslag.py` (malen og skripttestene som kildetekst), fiksturene `paa_brev` og `paa_brev_korrektur`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/kjerne/test_filnavn.py` -- nye enhetstester for radene i matrisen (æøå store og små, mellomrom og linjeskift, spesialtegn, 30 tegn uten bindestrek til slutt, `None`/tom/bare spesialtegn), og at filnavnet bare har `[A-Za-z0-9_.-]` -- FR-29, AD-11
- [x] `backend/soknad/kjerne/filnavn.py` -- som i Code Map
- [x] `backend/soknad/web/ruter.py` -- som i Code Map
- [x] `backend/tests/web/hjelpere.py` og eksisterende nedlastingstester -- som i Code Map
- [x] `backend/tests/web/test_filnavn_arbeidsgiver.py` (ny) -- Content-Disposition, filnavn-linjen og vinduet har samme filnavn med arbeidsgiver for Word og PDF, i begge modusene (case 1 og case 2) -- FR-29, AD-11
- [x] `backend/soknad/web/tekster.py`, `templates/vindu_logg_ut.html`, `templates/base.html`, `templates/brev.html` -- som i Code Map
- [x] `backend/soknad/web/static/js/nedlasting.js` og `bekreft.js` -- som i Code Map
- [x] `backend/tests/web/test_vindu_logg_ut.py` (ny) -- vinduet og `data-bekreft` på brevsiden før nedlasting (begge modusene), ikke etter nedlasting, ikke på andre sider, tekstene, `aria-*`, `autofocus` på «Avbryt», `type="button"` + `data-bekreft-ja` på «Logg ut»; `nedlasting.js` tar bort `data-bekreft` (kildetekst); POST `/logg-ut` virker som før -- FR-6, NFR-4, UX-DR17, UX-DR22
- [x] `backend/soknad/kjerne/ki_svar.py` -- bare kommentaren

**Acceptance Criteria:**
- Given `uv run pytest -q`, `ruff check` og `ruff format --check`, when de kjøres, then består alle, også de eksisterende testene for utlogging, brevsiden og nedlastingen

## Implementation Notes

- Kodet av en underagent etter spec-en. 1 383 tester besto, og `ruff check` og `ruff format --check` var rene (kjørt på nytt i hovedøkten).
- Utenfor Code Map: `#logg-ut-avbryt:focus` er lagt til i den felles `:focus`-regelen i `stil.css`, fordi «Avbryt» får fokus fra skriptet (kjent fallgruve i epic-konteksten). Ingen nye farger.
- «Avbryt» i det nye vinduet har `autofocus`, så `med_autofocus` i `test_brev.py`, `test_nedlasting.py`, `test_vindu_etter_nedlasting.py` og `test_nytt_forslag.py` har fått `logg-ut-avbryt` før nedlasting.
- `filnavn_i_dag()` i `hjelpere.py` bruker arbeidsgiveren fra case 1 som standard, og `arbeidsgiver=None` gir filnavnet uten arbeidsgiver.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap | Vinduet og at `data-bekreft` tas bort, testes bare som kildetekst, ingen test kjører skriptene | medium | Stemmer, men prosjektet har bevisst ingen nettlesertester ennå (issue #16, story 8.2) → defer. Prøves for hånd i PR-en (før nedlasting, «Logg ut» i vinduet, etter nedlasting) |
| 2 | blind, edge-case | ß, ł, đ, þ og œ har ingen NFKD-oppdeling og forsvinner («Straße» → `Strae`) | low | Stemmer, og strider mot «andre tegn til ASCII». Direkte retting (flere tegn i tabellen) → patch |
| 3 | blind | `test_ux_dr17_bekreft_js_virker_for_alle_vinduene` sjekker til slutt en tekst som bare står i en kommentar | low | Stemmer. Direkte sletting av linjen → patch |
| 4 | blind | Testen for samme filnavn regner ut arbeidsgiveren med `replace` i stedet for kjente navn | low | Stemmer, kopiert logikk i testen. Direkte retting → patch |
| 5 | blind | Docstringen til `filnavn_i_dag` er misvisende om case 1 og `None` | low | Stemmer. Direkte retting → patch |
| 6 | blind | For lang kommentarlinje i `nedlasting.js` og en enslig «I» i docstringen til `_rens` | low | Stemmer, rest fra omskrivingen. Direkte retting → patch |
| 7 | blind | «BÆRUM» blir `BAeRUM` (Æ → Ae også i store bokstaver) | low | Stemmer, men spec-en sier Æ → Ae, og KI-en skriver navn med vanlig stor forbokstav. Retting krever ny regel → avvist |
| 8 | blind | Tankestrek, `_`, `.` og `+` fjernes, så ord limes sammen («Bergen–Oslo» → `BergenOslo`) | low | Stemmer, men følger AD-11 og spec-en («alt annet enn `[A-Za-z0-9-]` fjernes», «Café/Bar» → `CafeBar`). Retting krever endret spec → avvist |
| 9 | blind | Kuttet ved 30 tegn kan dele et ord | low | Følger «høyst 30 tegn» i spec-en og AD-11. Kutt ved ordgrense er ny logikk → avvist |
| 10 | blind, edge-case | `nedlasting.js` tar bort advarselen ved trykket, før nedlastingen er bekreftet. Feiler den på nettet, logges brukeren ut uten advarsel | low | Stemmer, men sjelden med en lokal nettside, og en serverfeil gir ny side med advarselen. Den grønne knappen virker på samme måte fra 3.2. Retting krever et nytt bekreftelsesopplegg → avvist |
| 11 | blind, edge-case | «Logg ut» på resultatsiden med et brev som ikke er lastet ned, advarer ikke | low | Planen (EXPERIENCE.md, UX-DR17) sier at vinduet bare gjelder brevsiden, og spec-en sier det samme → avvist som utenfor planen |
| 12 | edge-case | Nedlasting med midtklikk eller «Lagre lenke som» gir advarsel som ikke trengs før siden lastes på nytt | low | Stemmer, men advarer bare for mye (trygg retning) → avvist |
| 13 | edge-case | «Nytt forslag» i en annen fane nullstiller `lastet_ned`, men denne fanen advarer ikke | low | Krever to faner med samme søknad. Retting krever sjekk på serveren ved utlogging → avvist |
| 14 | blind, edge-case | Rundt midnatt kan datoen på siden og i filen bli ulik | low | Fantes før denne storyen (3.2, 7.2) og skjer bare rundt midnatt. Retting krever å sende datoen mellom sidene → avvist |
| 15 | edge-case | Korrektur testes bare med case 1, ikke case 2 (ø) | low | Rensingen er lik i begge modusene og testet i enhetstestene og i Full generering med case 2 → avvist |
| 16 | blind | Docstringen til `_vis_brev` beskriver `advar_utlogging` som om den var en parameter | low | Teksten sier hva verdien betyr for malen, og er riktig. Ingen skade → avvist |

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine: brevsiden i begge modusene. «Logg ut» før nedlasting → vinduet, fokus på «Avbryt», Esc og «Avbryt» lukker med fokus tilbake, «Logg ut» logger ut. Last ned, «Bli her», «Logg ut» → ut med en gang. Etter «Nytt forslag» kommer vinduet igjen. Filnavnet `Soknad_Testvik-Utvikling-AS_<dato>` i vinduet, linjen og filen. Ved 375 og 1280 px og i høykontrast.
