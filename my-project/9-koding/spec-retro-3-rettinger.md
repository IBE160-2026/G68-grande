---
title: 'Rettinger fra retrospektiven for epic 3'
type: 'bugfix'
created: '2026-11-12'
status: 'done'
baseline_commit: '3fc008a9eb981133672655def286d336f32233f5'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-retro-2026-11-12.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Retrospektiven for epic 3 fant tre ting (action item 1–3). Testen for «Logg ut» på brevsiden blir grønn selv om knappen i hjørneraden mangler, fordi vinduet fra 3.3 har samme skjema (B1). Testhjelperne er kopiert til flere filer igjen, og én testfil henter fiksturer fra en annen (B2). Word-fila har amerikanske marger, og README sier at brevet og nedlastingen «kommer» (B4, C).

**Approach:** (1) Testen ser bare på `<footer>`. (2) Felles fiksturer flyttes til en ny `tests/web/conftest.py` og felles hjelpere til `tests/web/hjelpere.py`, og ingen testfil importerer fra en annen testfil. (3) `lag_docx` setter 2,5 cm marger på alle fire sider (Kristine bestemte det 2026-11-12), med test. README oppdateres.

## Boundaries & Constraints

**Always:** Ingen endring i hva nettsiden gjør, bortsett fra margene i Word-fila. Testene sjekker det samme som før, og antallet tester er det samme pluss de nye. Hver testfil og testfunksjon nevner FR-nummeret. `kjerne/` importerer aldri `docx`.

**Never:** Ikke rense brevteksten (Epic 4), ikke endre filnavnet eller når vinduet åpnes (godtatt for godt). Ikke endre `prompt-logg.md`, `todo.md` eller andre filer i `my-project/` (det gjøres etter PR-en).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Hjørneraden mangler på brevsiden | `base.html` uten «Logg ut» i `<footer>` på `/brev` | testen for «Logg ut» på brevsiden feiler | – |
| Word-fila | `lag_docx(avsnitt)` | marger 25 mm oppe, nede, til venstre og til høyre, A4 og `nb-NO` som før | – |

</frozen-after-approval>

## Code Map

- `backend/tests/web/test_brev.py:462-467` -- `test_fr22_brevsiden_har_logg_ut_og_ingen_ventetegn` sjekker `'action="/logg-ut"' in html`. Skal sjekke skjemaene i `footer(html)`.
- `backend/tests/web/test_utlogging.py:9-15` -- egne `footer` og `css_blokk` (`css_blokk` er lik den i `hjelpere.py:44`). `footer` flyttes til `hjelpere.py`.
- Duplikater som skal samles (sjekk at utgavene er like før de slås sammen):
  - `CASE`, `CV`, `ANNONSE` for case 1 i `test_brev.py:29-31`, `test_innlegging.py:32-34`, `test_nedlasting.py:20-22`, `test_resultat.py:26-28`, `test_ventetegn.py:26-28` → `hjelpere.py`. `BREV_SVAR`, `GAP_SVAR`, `NOKKELORD_SVAR` og `FASIT` blir der de brukes.
  - `html_av` i fem filer og `element` i fire → `hjelpere.py`.
  - Fiksturene `paa_resultat` (`test_brev.py:36`, `test_resultat.py:35`), `paa_brev` (`test_brev.py:47` via `lag_brev`, `test_nedlasting.py:27`), `paa_innlegging` (`test_innlegging.py:59`, `test_ventetegn.py:65`) og `filfeil` (`test_nedlasting.py:39`) → ny `tests/web/conftest.py`.
  - `test_vindu_etter_nedlasting.py:11, 23-24` henter fra `test_nedlasting.py`. Fjernes. `NEDLASTING` og `filnavn_i_dag` legges i `hjelpere.py`.
- `backend/tests/web/hjelpere.py:1-2` -- docstringen sier alt at testfilene henter herfra og ikke fra hverandre.
- `backend/soknad/adaptere/fil_ut.py:27-31` -- løkken over `dokument.sections` setter A4. Margene legges i samme løkke (`Mm(25)` for `top_margin`, `bottom_margin`, `left_margin`, `right_margin`). Ny konstant ved siden av `A4_BREDDE`.
- `backend/tests/adaptere/test_fil_ut.py:69-79` -- `test_fr29_filen_er_a4_og_norsk`. Ny test for margene ved siden av.
- `README.md:13` (status), `README.md:97` (`adaptere/`) og `README.md:130` (lenke bare til retrospektiven for epic 1).

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/web/hjelpere.py`, `backend/tests/web/conftest.py` (ny) -- felles hjelpere og fiksturer.
- [x] `backend/tests/web/test_*.py` -- bruker de felles hjelperne og fiksturene. Kopiene og importen fra `test_nedlasting.py` er borte.
- [x] `backend/tests/web/test_brev.py` -- testen for «Logg ut» ser på hjørneraden: nøyaktig ett skjema der, `action="/logg-ut"`.
- [x] `backend/soknad/adaptere/fil_ut.py`, `backend/tests/adaptere/test_fil_ut.py` -- 2,5 cm marger, med test.
- [x] `README.md` -- status: i testmodus virker også søknadsbrevet, nedlastingen som Word og vinduet etter nedlasting. Korrektur, PDF-opplasting, PDF-nedlasting og ekte KI kommer. `adaptere/`: «database, øktlager, KI og Word-fila». Lenke til retrospektivene for epic 1, 2 og 3 i `my-project/9-koding/`.

**Acceptance Criteria:**
- Given koden etter rettingen, when `grep -rn "from tests.web.test_\|from tests.web import test_" backend/tests` kjøres, then er det ingen treff.
- Given en midlertidig `base.html` uten «Logg ut» i hjørneraden på `/brev`, when testene kjøres, then feiler testen for «Logg ut» på brevsiden (prøves med kopi og settes tilbake).
- Given alle testene, when de kjøres, then er de grønne, og antallet er 560 pluss de nye.

## Implementation Notes

- Branch: `retro-3-rettinger`, fra `main` på `3fc008a9eb981133672655def286d336f32233f5`. Kodet av en hjelpeagent ut fra spec-en.
- Ny `tests/web/conftest.py` med `paa_innlegging`, `paa_resultat` (bygger nå på `paa_innlegging`), `paa_brev` og `filfeil`. `CASE`, `CV`, `ANNONSE`, `NEDLASTING`, `html_av`, `element`, `footer` og `filnavn_i_dag` står i `hjelpere.py`. Utgavene var like før de ble slått sammen. `lag_brev` og `til_innlegging` står igjen der de brukes.
- `test_utlogging.py` hadde også sin egen `css_blokk` (samme uttrykk som i `hjelpere.py`). Den er fjernet.
- Prøvd: `base.html` uten «Logg ut» i hjørneraden på `/brev` (kopi tatt og satt tilbake) gir én feilende test, `test_fr22_brevsiden_har_logg_ut_og_ingen_ventetegn`.
- 561 tester (560 + testen for margene), `ruff check` og `ruff format --check` grønne. Ingen import fra en annen testfil.
- Etter gjennomgangen: ny test `test_nfr9_ingen_testfil_henter_fra_en_annen` i `tests/test_app.py` som stopper importer fra en annen testfil, `GAP_SVAR` og `NOKKELORD_SVAR` i `hjelpere.py`, testen for «Logg ut» sammenligner hele skjemaet og sjekker teksten, og én kommentar om margene med de gamle tallene og beslutningen. 562 tester, `ruff` grønn.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-12), tre lag: blind, kanttilfeller, testhull. Testhull-laget fant ingen hull (561 tester).

| # | Funn | Vurdering | Begrunnelse | Rute |
|---|------|-----------|-------------|------|
| 1 | Ingenting hindrer at en testfil igjen henter fra en annen testfil (blind) | low | Riktig, og det var nettopp det som skjedde etter Epic 1. En liten test som leter etter slike importer, er en direkte vakt | patch |
| 2 | `GAP_SVAR` og `NOKKELORD_SVAR` lastes likt i både `test_innlegging.py` og `test_resultat.py` (blind + kanttilfeller) | low | Riktig, samme slags kopi som retro-funn B2. To konstanter flyttes | patch |
| 3 | Testen for «Logg ut» sjekker ikke `method="post"` eller knappeteksten, og gir `KeyError` hvis `action` mangler (blind) | low | Riktig. Sammenlign hele attributtene, som testen for vinduet, og sjekk teksten | patch |
| 4 | Margen på 2,5 cm viser til FR-29, men er Kristines beslutning fra retrospektiven. To kommentarer sier nesten det samme uten de gamle tallene (blind) | low | Riktig. Én kommentar med de gamle tallene (25,4 og 31,75 mm) og henvisning til beslutningen | patch |
| 5 | `til_innlegging` gjør det samme som fiksturen `paa_innlegging` (blind + kanttilfeller) | low | Det er en vanlig funksjon som `uten_testmodus` bruker etter at økten er byttet. En fikstur kan ikke kalles der | avvist |
| 6 | Regexen for feilboksen står fire ganger, `lag_brev` sender samme POST som `paa_brev` (blind) | low | Mest innenfor én fil, og `lag_brev` brukes med andre knapper. Liten nytte | avvist |
| 7 | `CV` og `ANNONSE` leses når `hjelpere.py` importeres, så alle webtester feiler hvis fila mangler (kanttilfeller, blind) | low | Var slik i fem filer før. Testdataene ligger i repoet, og mangler de, feiler testene uansett | avvist |
| 8 | `filnavn_i_dag()` kan gi en annen dato enn ruten over midnatt (kanttilfeller) | low | Fantes før (3.2 funn 14), bare flyttet. Godtatt for godt i retrospektiven (A2) | avvist |
| 9 | Kopien av spec-en, sprint-statusen og TO DO er ikke i diffen (blind) | false | Gjøres etter PR-en, som spec-en sier under Never | avvist |
| 10 | Branchen `story/3-3-vinduet-etter-nedlasting` finnes fortsatt (blind) | false | Ikke kode. Kristine sletter branchene på GitHub selv | avvist |
| 11 | FR-numrene i docstringen i `conftest.py` passer ikke helt med fiksturene (blind) | low | Kosmetisk. Regelen er at hver testfil nevner et FR-nummer | avvist |

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Last ned brevet og åpne fila i Word: Oppsett → Marger viser 2,5 cm på alle sider.
