---
title: 'Story 7.1: Nytt forslag'
type: 'feature'
created: '2026-11-17'
baseline_commit: '6d9899cb0c78c85b0eb96b5638e0599230315cf6'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-7-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Brukeren kan ikke be om et annet brev hvis hen ikke liker det første (FR-25). Går man tilbake til resultatsiden og trykker «Lag søknadsbrevet mitt», byttes brevet ut uten å spørre (retro 3, B3).

**Approach:** «Nytt forslag» under nedlastingsknappene åpner vinduet «Vil du ha et nytt forslag?». «Ja, lag nytt forslag» sender en POST som øker `forslag` med `nytt_forslag` i kjernen og lager et nytt brev gjennom `_med_ki`. Samme vindu spør på resultatsiden når et brev finnes (bestemt av Kristine 12. november 2026, retro 3).

## Boundaries & Constraints

**Always:** Tekstene ordrett fra EXPERIENCE i `web/tekster.py`: «Nytt forslag», «Vil du ha et nytt forslag?», «Brevet du ser nå, blir slettet. Har du ikke lastet det ned, er det borte.», «Ja, lag nytt forslag», «Avbryt», «Brevet du hadde, er beholdt.». Ventetegnet bruker `VENTE_BREV`. Vinduet: fokus til «Avbryt», Esc og «Avbryt» lukker, fokus tilbake til knappen som åpnet. I Korrektur får KI-en alltid det opprinnelige `eget_brev`. Søknaden endres bare i kjernen (AD-8). KI-kallet går gjennom `_med_ki` (samtykke, plass, opptatt, telling). Testene kaller aldri det ekte API-et.

**Never:** Ikke PDF (7.2), fyrverkeri (7.4) eller vinduet «Logg ut før nedlasting» (7.5). Ingen endring i `TestKI`, promptene eller `EkteKI`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Nytt forslag | brevsiden, testmodus, forslag 1, lastet ned | `forslag` blir 2, `brev-2` vises, knappen og filnavn-linjen nullstilt | – |
| Korrektur | som over i Korrektur | `korrektur-2`, laget fra det opprinnelige `eget_brev` | – |
| KI-feil | `KIFeil` ved nytt forslag | brevsiden med det gamle brevet, `forslag` og `lastet_ned` uendret, feilboks med feilteksten, «Brevet du hadde, er beholdt.» og «Prøv på nytt» | vis_feil |
| Alle kall brukt | ekte KI, 10 kall brukt | samme feilboks med `KI_KALL_BRUKT`, uten «Prøv på nytt» | – |
| Resultatsiden med brev | tilbakeknappen fra brevsiden, «Lag søknadsbrevet mitt» | vinduet spør først, «Ja» gir neste forslag | – |
| Opptatt / ukjent knapp / uten brev | POST `/brev` | siden for steget / brevsiden med 400 / til resultatsiden | – |

**Beslutning (Kristine, 2026-11-17):** ca. 3,82 kr per søknad med ett «Nytt forslag» (lange tekster, retro 4) er godtatt. Ingen egen grense for nye forslag: grensen på 10 KI-kall per søknad og taket på 250 kr gjelder.
**Beslutning (Kristine, 2026-11-17):** spec-en er på ca. 2 200 tokens og beholdes hel, med resultatsiden i samme story og PR.

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/okt.py` -- `Soknad` får `forslag: int = 1`. Ny `nytt_forslag(soknad)`: `forslag + 1`, `brev`, `korrektur` og `lastet_ned` nullstilt. `velg_modus` og `sett_inndata` (endret tekst) setter `forslag` tilbake til 1. Fjern «forslag legges til i Epic 7» og Epic 7-merknaden i `tell_ki_kall`.
- `backend/soknad/web/ruter.py:259` `resultat` -- `brevet()` flyttes ut som `_lag_brev(soknad, valgt_ki)` (bruker `soknad.forslag`, `eget_brev` fra søknaden). Finnes et brev (`ferdig_brev`), lages det fra `nytt_forslag(lagret)`. `_vis_resultat` får `har_brev`.
- `backend/soknad/web/ruter.py:310` `brev` -- tar også POST med `handling=nytt_forslag`: uten brev til resultatsiden, opptatt til steget, ukjent knapp 400, ellers `_med_ki(kall=BREV_KALL, arbeid=lambda k: _lag_brev(nytt_forslag(lagret), k), vis_feil=partial(_vis_brev, lagret, avsnitt), neste="web.brev")`. `_vis_brev` får `ki_feil` og `prov_pa_nytt`.
- `backend/soknad/web/templates/brev.html` -- skjema `nytt-forslag-skjema` (POST `/brev`) med lenkeknappen «Nytt forslag» (`type=submit`, `handling=nytt_forslag`, `data-vente`, `data-bekreft="vindu-nytt-forslag"`) under `.nedlasting`. KI-feilboks som på resultatsiden, «Prøv på nytt» med `form=`. `ventetegn`-blokken og `vente.js`.
- `backend/soknad/web/templates/vindu_nytt_forslag.html` (ny) -- `<dialog class="vindu">` med `aria-labelledby`/`aria-describedby`, «Ja, lag nytt forslag» (hovedknapp, `type=button`, `data-bekreft-ja`) og «Avbryt» (sekundærknapp i `form method="dialog"`, `autofocus`). Inkluderes i `brev.html` og, når `har_brev`, i `resultat.html`.
- `backend/soknad/web/templates/resultat.html` -- «Lag søknadsbrevet mitt» får `data-bekreft` når `har_brev`. «Prøv på nytt» spør ikke.
- `backend/soknad/web/static/js/bekreft.js` (ny) -- klikk på knapp med `data-bekreft`: `preventDefault`, `showModal()`. «Ja»: lukk og `form.requestSubmit(knappen)`, så `vente.js` viser ventetegnet. `close`: fokus tilbake til knappen. Endrer aldri søknadsdata (AD-1).
- `backend/soknad/web/static/css/stil.css:1471` -- «Nytt forslag» under knappene, `:focus`-regel for «Avbryt» (som `#bli-her`), sjekk at `.vindu` i `forced-colors` dekker det nye vinduet.
- `backend/soknad/web/tekster.py` -- de nye tekstene.
- `backend/tests/web/hjelpere.py` -- `korrektur_svar(forslag)`, `korrektur_testki`, `sett_soknad` gjenbrukes.

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/kjerne/test_okt.py` -- `nytt_forslag` øker og nullstiller, `velg_modus`/`sett_inndata` setter `forslag` til 1 -- AD-8
- [x] `backend/soknad/kjerne/okt.py` -- `forslag` og `nytt_forslag` -- kjernen eier endringen
- [x] `backend/soknad/web/tekster.py`, `ruter.py`, malene, `bekreft.js`, `stil.css` -- som i Code Map
- [x] `backend/tests/web/test_nytt_forslag.py` (ny, så `test_brev.py` ikke vokser, retro 5 A6) -- hver rad i matrisen, også `forslag=1` og `forslag=2` gir ulike testbrev (FR-25), Korrektur får originalbrevet, tellingen med ekte KI, resultatsiden med og uten brev, tekstene, vinduet (aria, autofocus på «Avbryt»), skriptet og CSS-en
- [x] `backend/tests/web/test_brev.py`/`test_resultat.py` -- rett tester som antar at et nytt «Lag søknadsbrevet mitt» gir forslag 1

**Acceptance Criteria:**
- Given brevsiden, when den vises, then står «Nytt forslag» under nedlastingsknappene, og vinduet er lukket
- Given et nytt brev etter «Nytt forslag», when brevsiden vises, then er nedlastingsknappen blå og filnavn-linjen skjult
- Given `uv run pytest -q`, `ruff check` og `ruff format --check`, when de kjøres, then består alle

## Implementation Notes

- Kodet av en subagent etter spec-en. 1 244 tester besto, og `ruff check` og `ruff format --check` var rene (kjørt på nytt i hovedøkten).
- `_lag_brev(soknad, valgt_ki)` i `ruter.py` lager brevet for både resultatsiden og «Nytt forslag». I Korrektur sender den alltid `soknad.eget_brev.tekst`, altså originalbrevet.
- To tester i `test_brev.py` forventer nå forslag 2 når «Lag søknadsbrevet mitt» trykkes igjen med et brev (`brev-2.json` / `korrektur_brev(2)`). FR-26-testen godtar skjemaet og knappen «Nytt forslag» i `<main>`, og brevsiden har nå ventetegnet.
- `.nedlasting` har fått `margin-bottom` `space-4` (var `space-7`), og den nye `.nytt-forslag` har `space-7` under seg. `[data-bekreft]:focus` gir ring også etter museklikk, fordi fokus går tilbake til knappen fra skriptet.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap, blind | `bekreft.js` testes bare som kildetekst, ikke i en nettleser | medium | Stemmer. Repoet har ingen nettlesertester, som for `vente.js` og `nedlasting.js` (issue #16, story 8.2). Prøves for hånd i PR-en → defer |
| 2 | verification-gap, edge-case | `nedlasting.js` skjuler `#feilboks` ved hver nedlasting, også KI-feilboksen fra «Nytt forslag» med «Prøv på nytt» og meldingen om KI-kallene | low | Stemmer: samme id, og skriptet skjuler boksen uten å se hvilken det er. Direkte retting: skjul bare boksen fra FilFeil → patch |
| 3 | edge-case | `requestSubmit` mangler i Safari før 16, og da sendes ingenting | low | Stemmer for nettlesere fra før 2022. Svært lite sannsynlig, og rettingen er en ny vakt → avvist |
| 4 | blind | Docstringen sier at KI-en får `forslag`, men ekte KI sender det ikke | low | Stemmer: `EkteKI.brev` sender det ikke (ki.py:277). Teksten rettes → patch. At ekte KI kan gi et likt brev, er bestemt i arkitekturen (forslag sendes ikke) og hører ikke til denne storyen |
| 5 | blind | Gamle «Epic 7»-merknader i `ki.py:181–189` og `ki_svar.py:118` | low | Stemmer, de er ikke sanne lenger → patch |
| 6 | blind | Testene ble svekket til `med_autofocus(main(html))`, så en autofocus utenfor `<main>` blir ikke funnet | low | Stemmer. Hele siden sjekkes igjen, med «Avbryt» som eneste tillatte unntak → patch (bare tester) |
| 7 | blind | «Brevet du ser nå» passer dårlig på resultatsiden, der brevet ikke vises | low | Stemmer, men den frosne intensjonen sier samme vindu og tekstene ordrett fra EXPERIENCE → avvist. Lagt fram for Kristine som et valg om ordlyden |
| 8 | blind | KI-feil etter «Ja» på resultatsiden sier ikke at brevet er beholdt | low | Stemmer. Skjer bare med tilbakeknappen pluss KI-feil, og rettingen er en ny gren med ny tekst → avvist |
| 9 | blind | To faner, eller en gammel resultatside uten vinduet, kan lage nytt forslag uten å spørre | low | Stemmer i teorien. Sjelden, og rettingen er et nytt skjult felt med ny sjekk → avvist |
| 10 | blind | Laster man feilsiden på nytt, sendes POST-en igjen uten vinduet | low | Nettleseren spør selv før et skjema sendes på nytt. Å vise samme side uten redirect ved feil er bestemt i arkitekturen (AD-8) → avvist |
| 11 | blind | «Nytt forslag» vises og spør også når alle KI-kallene er brukt | low | Stemmer, men brevet slettes ikke (søknaden er uendret, testet). Sjelden, og rettingen er en ny gren → avvist |
| 12 | blind | Fokusringen `[data-bekreft]:focus` gjelder bare når knappen har vinduet | low | Bare utseende, og det er nettopp da fokus kommer fra skriptet. Rettingen er en ny klasse i skriptet → avvist |
| 13 | blind | Docstringen i `test_fr25_ny_modus_gir_forslag_1_igjen` lover mer enn testen sjekker | low | Stemmer. Direkte retting → patch |
| 14 | blind | `test_ad1_ventetegnet_bare_pa_sider_med_ki_kall` har ingen positiv sjekk av brevsiden | low | Dekket av `test_fr25_brevsiden_har_ventetegnet_og_skriptene` → avvist |
| 15 | blind | Uten JavaScript slettes brevet uten vinduet | low | Bevisst valg i Design Notes: knappen virker, men uten vinduet. Gjelder nesten ingen brukere → avvist |

## Design Notes

- «Nytt forslag» er en ekte submit-knapp. `bekreft.js` stopper trykket og spør. Uten JavaScript sendes skjemaet uten vinduet, men knappen virker. «Ja» sender skjemaet med `requestSubmit(knappen)`, så ventetegnet kommer fra `vente.js` uten endring, og fokus blir på knappen under brevet.
- `nytt_forslag` brukes inni `arbeid`. Feiler KI-en, lagrer `_med_ki` søknaden fra før, så det gamle brevet, `forslag` og `lastet_ned` er uendret, og «Prøv på nytt» prøver samme forslag igjen uten å spørre (brukeren har alt sagt ja).
- `forslag` tilbake til 1 når brevet slettes av `velg_modus` eller endret tekst, så første brev etter det alltid er `-1` i testmodus.

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine, i testmodus ved 375 og 1280 px: «Nytt forslag» → vinduet med fokus på «Avbryt» → Esc lukker og fokus er på «Nytt forslag» → «Ja» gir ventetegnet og et annet brev, knappen er blå igjen. Samme i Korrektur. Tilbakeknappen fra brevsiden → «Lag søknadsbrevet mitt» spør. Høykontrast: vinduet har ramme.
