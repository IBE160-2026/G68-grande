---
title: 'Rettinger fra retrospektiven for epic 1'
type: 'refactor'
created: '2026-11-08'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'eb8ab23439905f4f25fe6d85552a972e7386d847'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-retro-2026-11-08.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Retrospektiven for epic 1 fant fire småting som bør ordnes før epic 2 (action item 1–4). Økten ryddes to steder. En innlogget bruker kan åpne innloggingen og registreringen og bytte bruker uten beskjed. Testhjelperne er kopiert og hentes fra andre testfiler. To tester er for løse.

**Approach:** Én liten PR. Kristine har bestemt at en innlogget bruker sendes til startsiden fra innloggingen og registreringen. Det strider ikke mot PRD-en, UX eller arkitekturen, men fyller et hull. Resten er rydding uten synlig endring.

## Boundaries & Constraints

**Always:**
- `logg_inn_bruker` kaller `logg_ut_bruker()` for å slette en gammel økt, og lager så en ny. Slettingen av økten finnes bare i `logg_ut_bruker`.
- Er brukeren innlogget (`gjeldende_innlogging()` er ikke `None`), gir både GET og POST på `/logg-inn` og `/registrer` 302 til startsiden. Ingenting sjekkes eller lagres, og økten er uendret. Er brukeren ikke innlogget, er alt som før, også meldingen «Du må logge inn først».
- Testhjelperne som brukes i flere filer, ligger i én modul som ikke er en testfil, `backend/tests/web/hjelpere.py`. Ingen testfil importerer fra en annen testfil. `test_ruter.py`, `test_innlogging.py`, `test_registrering.py` og `test_utlogging.py` bruker den.
- Escaping testes likt på innloggingen og registreringen: verdien kommer tilbake uendret i `value` (lest med HTML-parseren), og `<script` finnes ikke på siden.
- Lagsjekken for `kjerne/` feiler også på `soknad.adaptere` og `soknad.web` (hele modulnavnet). Den slår faktisk til, og det vises med en test på en liten kildetekst.
- Testen av `tilbake.js` sjekker at koden laster på nytt bare når `hendelse.persisted` er sann (betingelsen `if (hendelse.persisted)`), ikke bare at ordene finnes.
- Hver test nevner FR- eller NFR-nummeret, som før.

**Never:**
- Ingen endring av utseende, tekster eller `tilbake.js` selv. Ingen nye avhengigheter.
- Ingen omskriving av testene utover det som trengs for flyttingen. Tester som sjekker det samme flere steder, får stå.
- Testene skriver aldri til den ekte `backend/instance/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Innlogget åpner innloggingen | innlogget, `GET /logg-inn` (også `?ikke_innlogget=1`) | 302 til `/` | N/A |
| Innlogget sender innlogging | innlogget, `POST /logg-inn` med en annen bruker | 302 til `/`, samme økt-id, samme bruker | Ingen databasesjekk |
| Innlogget åpner registreringen | innlogget, `GET /registrer` | 302 til `/` | N/A |
| Innlogget sender registrering | innlogget, `POST /registrer` med ny e-post | 302 til `/`, ingen ny rad, samme økt | N/A |
| Gammel cookie | økt-id uten økt i minnet, `GET /logg-inn` | 200, innloggingen vises uten hjørnerad | N/A |
| Innlogging fra gammel cookie | økt-id uten økt i minnet, riktig innlogging | 302 til `/`, ny økt-id | N/A |
| Ny innlogging rydder | `logg_inn_bruker` med en eksisterende økt | den gamle økten er slettet via `logg_ut_bruker` | N/A |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/innlogging.py` -- `logg_inn_bruker` (linje ca. 40) og `logg_ut_bruker` (ca. 49). `gjeldende_innlogging()` brukes til sjekken.
- `backend/soknad/web/ruter.py` -- `logg_inn` og `registrer`. Sjekken av innlogget kommer først i begge. I `logg_inn` GET blir `gjeldende_innlogging() is None` i meldingssjekken overflødig og kan fjernes.
- `backend/tests/web/test_innlogging.py` -- har `Tagger`, `tagger_i`, `felt`, `med_autofocus`, `logg_inn`, `er_innlogget`. `test_fr3_ny_innlogging_gir_ny_okt_id_og_sletter_den_gamle` logger inn to ganger og må endres (andre innlogging gir nå redirect uten ny økt). `test_fr3_eposten_som_vises_igjen_er_escapet` er den svake escaping-testen.
- `backend/tests/web/test_ruter.py` -- egen kopi av `Tagger`/`tagger_i` og `STIL`.
- `backend/tests/web/test_registrering.py` -- henter `felt`, `med_autofocus`, `tagger_i` fra `test_innlogging`. Har egen `er_innlogget` og `STIL`. `test_fr1_auto_innlogging_gir_ny_okt_id_med_den_nye_brukeren` logger inn og registrerer så, og må endres. `test_fr1_eposten_som_vises_igjen_er_escapet` er mønsteret for escaping.
- `backend/tests/web/test_utlogging.py` -- henter `er_innlogget`, `logg_inn`, `med_autofocus`, `tagger_i` fra `test_innlogging`. Har `okt_id`, `footer`, `css_blokk`, `STIL`. `test_fr7_ingen_melding_naar_man_alt_er_innlogget` blir en test av redirect. `test_fr6_skriptet_for_tilbakeknappen_bare_etter_innlogging` er testen av `tilbake.js`.
- `backend/tests/kjerne/test_inndata.py` -- `_importerte_moduler` tar bare første del av modulnavnet. `test_nfr5_kjernen_importerer_ikke_...` sjekker `flask`, `werkzeug`, `sqlite3`.
- `backend/pyproject.toml` -- `pythonpath = ["."]`, så `from tests.web.hjelpere import …` virker. Ingen `__init__.py` i `tests/`.
- `backend/tests/web/test_alle_sider.py` -- `/logg-inn` og `/registrer` er unntatt, så den påvirkes ikke.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/web/innlogging.py` -- `logg_inn_bruker` bruker `logg_ut_bruker()`.
- [x] `backend/soknad/web/ruter.py` -- innlogget gir redirect til startsiden først i `logg_inn` og `registrer`, og meldingssjekken forenkles.
- [x] `backend/tests/web/hjelpere.py` (ny) -- de felles hjelperne, med en kort docstring.
- [x] `backend/tests/web/test_ruter.py`, `test_innlogging.py`, `test_registrering.py`, `test_utlogging.py` -- bruk `hjelpere.py`, fjern kopiene, og rett testene som logger inn mens man er innlogget (se Code Map). Ny escaping-sjekk i `test_innlogging.py`. Nye tester for matrisen (innlogget på begge sidene med GET og POST, gammel cookie, opprydding via `logg_ut_bruker`).
- [x] `backend/tests/kjerne/test_inndata.py` -- full lagsjekk og en test som viser at den slår til.
- [x] `backend/tests/web/test_utlogging.py` -- testen av `tilbake.js` sjekker betingelsen.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjøres, then er alle grønne, og `grep -rn "from tests.web.test_" backend/tests` gir ingen treff.
- Given en innlogget bruker i nettleseren, when hun skriver `/logg-inn` eller `/registrer` i adressefeltet, then kommer hun til «Velkommen».

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alle tester grønne
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Kristine logger inn og skriver `127.0.0.1:5000/logg-inn` og så `127.0.0.1:5000/registrer` i adressefeltet. Begge gangene kommer hun til «Velkommen». Så logger hun ut og ser at innloggingen og registreringen vises som før.
- Samtidig prøver hun innloggingen, registreringen og startsiden med «Logg ut» ved 320 px, 768 px og 200 % zoom (action item 5): ingenting ruller sidelengs, og «Logg ut» dekker ikke noe.

## Implementation Notes

- Etter implementeringen: 149 tester (133 før), `ruff check` og `ruff format --check` grønne, og `grep -rn "from tests.web.test_" backend/tests` gir ingen treff.
- Hjelpeagenten satte tilbake de gamle `ruter.py` og `innlogging.py` og kjørte testene: sju av de nye eller endrede testene feilet. De fanger altså det som manglet.
- `okt_id` ble også flyttet til `hjelpere.py`, fordi de nye testene trenger den.
- Etter gjennomgangen (3 rettelser i testene): 152 tester, `ruff check` og `ruff format --check` grønne.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-08), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | `hent(gammel) is None` er alltid sann i to tester, fordi testen sletter økten selv | blind, testhull | low | Riktig. Linjen fjernes, og slettingen dekkes av enhetstesten av `logg_inn_bruker` | patch |
| 2 | Lagsjekken forbyr ikke `os`, `pathlib`, `anthropic` og andre I/O-biblioteker, selv om testen heter «ikke_io» | blind, grensetilfeller | medium | Riktig: arkitekturen sier at `kjerne/` aldri importerer I/O-biblioteker eller leser filer. Lista utvides | patch |
| 3 | Oppsettet (registrering av `ola@x.no`) i testen av innlogging mens man er innlogget sjekkes ikke | blind | low | Riktig. Én assert | patch |
| 4 | Tilbakeknappen rett etter innlogging kan vise innloggingen fra nettleserens minne, så den nye sjekken aldri kjører | blind, grensetilfeller | low | Var slik før denne PR-en. Ingen personvernfare: skjemaet er tomt, og sender man det, kommer man til startsiden. Rettingen (`tilbake.js` på alle sider) bryter den låste regelen om `<script` i escaping-testene | defer |
| 5 | Spion-testen sjekker hvordan koden virker, ikke bare hva den gjør | blind | false | Den låste delen sier at slettingen bare skal finnes i `logg_ut_bruker`. Det er nettopp det spionen sjekker, og testen sjekker også resultatet | avvist |
| 6 | Lagsjekken ser bare på filene øverst i `kjerne/`, og relative importer regnes fra `soknad.kjerne` | blind, grensetilfeller | low | `kjerne/` har ingen undermapper, og arkitekturen legger ikke opp til det. En import forbi toppakken feiler uansett når den kjøres | avvist |
| 7 | Dynamiske importer (`importlib`, `__import__`) og innpakkede pakker blir ikke funnet | grensetilfeller | low | Svært lite sannsynlig i en liten kjerne med rene regler. Rettingen krever ny kode for kall i syntakstreet | avvist |
| 8 | `"<script" not in html` i escaping-testene brekker hvis `tilbake.js` kommer på alle sider | blind | low | Bestemt i den låste delen. `tilbake.js` vises i dag bare etter innlogging, og testene er utlogget | avvist |
| 9 | Testen av `tilbake.js` krever nøyaktig formatering | blind | low | Med vilje: den skal fange en snudd betingelse. Fila endres sjelden, og en ny formatering gir en tydelig feil | avvist |
| 10 | Lokale variabler heter `okt_id` og skjuler hjelperen. `innlogget_client` gjentar innloggingen | blind | low | Virker riktig, bare utseende. Den låste delen sier ingen omskriving utover flyttingen | avvist |
| 11 | De to testene av «alt innlogget» er ikke helt like | blind | low | Begge sjekker 302, adressen og at økten er uendret. Bare utseende | avvist |
| 12 | Ingen beskjed når en innlogget sender skjemaet for en annen bruker | blind | false | Kristine bestemte at man sendes til startsiden, uten beskjed (den låste delen) | avvist |
| 13 | «Full lagsjekk» er et for stort ord, for bare statiske importer sjekkes | grensetilfeller | low | Riktig om ordet, men koden gjør det spec-en ber om (hele modulnavnet). Ingen feil å rette | avvist |
