---
title: 'Rettinger fra retrospektiven for epic 4, runde 3: småtingene'
type: 'chore'
created: '2026-11-14'
status: 'done'
baseline_commit: 'ff3fca22c8fb199069ecd2abf13fdca312c63cdc'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-retro-2026-11-14.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Retrospektiven for epic 4 (action item 3, godtatt av Kristine 2026-11-14) fant flere småting:
- `med_nokkel` er kopiert i tre testfiler (B3).
- Kommentarer og en test sier at tiden «måles i 4.3», og testen sier at nettsiden bruker TestKI fram til 4.3 (B6).
- Enslige surrogater renses bare i brevet, ikke i listene `nokkelord`, `dekker` og `mangler`, og da gir resultatsiden en feilside (B8).
- `my-project/README.md` mangler radene for 4.3.2, 4.4 og 4.5, og `README.md` lenker ikke til retrospektiven for epic 4 (C).
- README nevner ikke at det man har lagt inn, ligger i minnet til man logger ut eller nettsiden stoppes (B11).

**Approach:** Én fikstur `med_nokkel` i `tests/web/conftest.py`, rettede kommentarer, den gamle testen slettes, surrogatene fjernes også fra listepunktene i `kontroller`, og radene og lenkene i README-ene.

**Decision (Kristine, 2026-11-14):** Runde 3 av tre, med egen branch og PR. Branchene for epic 4 er alt slettet, på GitHub av Kristine og lokalt av KI-en. Branchen bygger på runde 2 (`retro-4-rettinger-2`, PR #30).

## Boundaries & Constraints

**Always:**
- Ingen endring i det brukeren ser, bortsett fra at et listepunkt med en enslig surrogat vises uten den i stedet for en feilside.
- Alle eksisterende tester går gjennom. Unntaket er de som brukte en lokal `med_nokkel`: de bruker den felles og sjekker det samme.
- Hver testfil og testfunksjon nevner FR- eller NFR-nummeret. Ingen testfil henter noe fra en annen testfil.

**Never:**
- Ikke rense `arbeidsgiver` (story 7.5, action item 5).
- Ikke endre tidsgrensen eller andre verdier i `innstillinger.py`, bare kommentarene. Målingen med lange tekster er runde 4.
- Ikke endre `prompt-logg.md` eller `todo.md` før koden er gjennomgått.

</frozen-after-approval>

## Code Map

- `backend/tests/web/test_samtykke.py:40` og `test_grenser.py:53` -- `med_nokkel` gir `(app, klient, kalt)` med `TellendeKI` som `ekte_ki`. `test_testmodus.py:232` gir `(app, klient)` og bytter ikke ut `EkteKI`.
- `backend/tests/web/conftest.py` -- felles fiksturer for webtestene. Her kommer `med_nokkel` i formen fra `test_samtykke.py`. `test_testmodus.py` pakker ut tre verdier (17 bruk).
- `backend/soknad/innstillinger.py:29–32` og `backend/soknad/adaptere/ki.py:191–194` -- kommentarene om «måles i 4.3». Målt i 4.3.1, 4.4 og 4.5: nøkkelord og gap 2–5 s hver, et brev 16–47 s (`my-project/testplan.md:75`).
- `backend/tests/adaptere/test_ekte_ki.py:357–360` -- `test_nfr11_nettsiden_bruker_fortsatt_testki` slettes. `testplan.md:181` nevner den ikke (sjekk med søk og rett hvis den står der).
- `backend/soknad/kjerne/ki_svar.py:36–68` -- `_word_taler`, `_rens_avsnitt`, `_uten_tomme` og `_rens`. Listepunktene i `nokkelord`, `dekker` og `mangler` får enslige surrogater (kategori `Cs`) fjernet før `_uten_tomme`. Ikke `arbeidsgiver`.
- `my-project/README.md:69–72` -- radene for spec-ene. Nye rader for `spec-4-3-2-…`, `spec-4-4-…` og `spec-4-5-…` (kopiene finnes i `my-project/8-koding/`), i samme stil og med PR #26, #27 og #28.
- `README.md:105` -- «Ingenting lagres mellom øktene.» `README.md:149` -- lenkene til retrospektivene for epic 1–3.

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/web/conftest.py` -- fiksturen `med_nokkel`, og de tre lokale fjernes fra `test_samtykke.py`, `test_grenser.py` og `test_testmodus.py`.
- [x] `backend/soknad/innstillinger.py` og `backend/soknad/adaptere/ki.py` -- kommentarene sier hva som ble målt (2–5 s og 16–47 s), og at et kall kan ta lenger enn 2 × 90 s med ett nytt forsøk og `retry-after`.
- [x] `backend/tests/adaptere/test_ekte_ki.py` -- slett `test_nfr11_nettsiden_bruker_fortsatt_testki`.
- [x] `backend/soknad/kjerne/ki_svar.py` -- enslige surrogater fjernes fra listepunktene. Tester i testfila for `ki_svar`: `\ud800` i et nøkkelord og i et gap-punkt fjernes, og et punkt med bare en surrogat blir borte.
- [x] Webtest -- et gap-svar med `\ud800` fra KI-en gir resultatsiden (200), ikke en feilside.
- [x] `my-project/README.md` -- radene for 4.3.2, 4.4 og 4.5.
- [x] `README.md` -- lenke til retrospektiven for epic 4 (`my-project/8-koding/epic-4-retro-2026-11-14.md`) på linje 149, og nytt punkt rett etter «Ingenting lagres mellom øktene»: «**Det du har lagt inn, ligger i minnet til du logger ut.** Lukker du nettleseren uten å logge ut, blir CV-en, annonsen og brevet liggende i minnet på serveren til nettsiden stoppes.»

**Acceptance Criteria:**
- Given koden etter rettingen, when man søker etter `def med_nokkel` og «måles i» i `backend/`, then står `med_nokkel` bare i `tests/web/conftest.py`, og «måles i 4.3» står ingen steder.
- Given en midlertidig `ki_svar.py` uten den nye rensingen (kopi først, satt tilbake og sjekket med `cmp`), when testene kjøres, then feiler de nye testene.
- Given alle testene, when de kjøres, then er de grønne (798 − 1 + de nye).

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil
- `cd backend; uv run pytest` -- expected: alle tester grønne

## Implementation Notes

- `med_nokkel` står i `tests/web/conftest.py` i formen fra `test_samtykke.py`. `test_testmodus.py` hadde 6 bruk (ikke 17), som nå pakker ut `app, client, _`. Ubrukte importer (`app_med_nokkel`, `logg_inn`) er fjernet fra `test_grenser.py` og `test_samtykke.py`.
- Rensingen er en ny hjelper `_uten_surrogater` i `ki_svar.py`, brukt før `_uten_tomme` for `nokkelord`, `dekker` og `mangler`. `arbeidsgiver` er urørt. Docstringen til `kontroller` og `_rens` nevner det.
- Nye tester: `test_fr28_enslige_surrogater_fjernes_fra_listene` (2 tilfeller) og `test_fr28_bare_surrogater_i_nokkelordene_gir_ubrukelig_svar` i `tests/kjerne/test_ki_svar.py`, og `test_fr28_enslig_surrogat_i_gap_svaret_gir_resultatsiden` i `tests/web/test_ekte_ki_i_flyten.py`. Webtesten går gjennom `EkteKI`, SDK-et og `kontroller` med den falske transporten. Oppsettet i fila er flyttet til to lokale hjelpere (`app_med_falsk_api`, `til_resultatsiden`), som også den gamle testen bruker.
- Mutasjon: med `_uten_surrogater` satt til `return liste` (kopi først, satt tilbake og sjekket med `cmp`) feilet de 4 nye testene, og 797 gikk gjennom.
- `testplan.md` nevnte ikke den slettede testen, så den er ikke endret.
- Resultat: 801 tester grønne (798 − 1 + 4). `ruff check` og `ruff format --check` uten feil.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-14), tre lag: blind, kanttilfeller og testhull. Testhull-laget fant ingen hull.

| # | Kilde | Funn | Dom | Begrunnelse / rute |
| --- | --- | --- | --- | --- |
| 1 | kant | Kommentaren i `innstillinger.py` sier at tidene fra 4.3.1, 4.4 og 4.5 står i `testplan.md`, men 4.3.1 står bare i sesjonsloggen | low | Sant (`testplan.md:75` og `:181`, `.logs/kristine/968`). Direkte retting. Patch. |
| 2 | blind | Kommentaren sier ikke lenger at 90 s er beholdt med vilje | low | Sant: «startverdi som justeres» ble fjernet uten at beslutningen ble skrevet. Én setning. Patch, sammen med 1. |
| 3 | blind | Kommentaren i `ki.py` gjentar tallene uten «med testdataene», så de to kopiene kan gli fra hverandre | low | Sant. Direkte retting. Patch: `ki.py` viser til kommentaren i `innstillinger.py`. |
| 4 | blind | Docstringen til `_rens` sier både at tom arbeidsgiver blir None og at den ikke renses, og `kontroller` sier «bare en surrogat» | low | Sant for ordlyden. Direkte retting. Patch. |
| 5 | blind | Raden for runde 2 i `my-project/README.md` mangler lenke til PR #30 | low | Sant. PR #30 ble flettet 2026-11-14. Patch. |
| 6 | blind | «alle 16 funn» (4.3.2) og «alle 22 funn» (4.5) teller med en rad uten funn | low | Sant (rad 16 i 4.3.2 og rad 1 i 4.5). Patch: 15 og 21. |
| 7 | blind | Ingen rad og spec-kopi for runde 3 i `my-project/` | false | Gjøres etter gjennomgangen, som i runde 2 (Never: `todo.md` og `prompt-logg.md` før gjennomgangen). |
| 8 | blind | Det nye README-punktet overlapper punktet over, og overskriften sier bare «til du logger ut» | low | Kristine godkjente ordlyden ved sjekkpunktet. Avvist. Hun kan endre den i PR-en. |
| 9 | blind | Ingen test av at et gap-svar med bare surrogater gir `ubrukelig_svar` | low | Samme `_bare_tomme`-sjekk som for nøkkelordene, som er testet, og mutasjonen viser at rensingen er dekket. En ny test er mer enn en direkte retting. Avvist. |
| 10 | blind | Webtesten har surrogat bare i gap-svaret, og sjekken `</span>\s*</li>` avhenger av malen | low | Nøkkelordene er dekket i `test_ki_svar.py`, og samme sjekk av malen brukes i runde 2. Avvist. |
| 11 | blind | `med_nokkel` havnet i `conftest.py`, ikke `hjelpere.py`, og `test_testmodus.py` bruker nå `TellendeKI` | false | Spec-en (og `deferred-work.md`) sier `tests/web/conftest.py`, og en fikstur hører hjemme der. Endringen i `test_testmodus.py` står i Implementation Notes, og testene sjekker det samme. |
| 12 | blind | `issues.md:124` og punktet om runde 3 og 4 i `issues.md` er ikke oppdatert, og slettingen av branchene står ikke som gjort | low | Bokføringen gjøres etter gjennomgangen. Slettingen står i Decision. Avvist her, `issues.md` oppdateres i loggen. |
