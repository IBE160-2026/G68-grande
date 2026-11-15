---
title: 'Brevet: hilsen og navn fra nettsiden, og to nye regler i brev-prompten'
type: 'feature'
created: '2026-11-15'
status: 'done'
baseline_commit: '6caf52db90ed42db7e53bb82de5ebcd47c520f15'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** I to av tolv brev fra ekte KI (story 4.4 og 4.5) manglet «Med vennlig hilsen» og navnet, og ingen sjekk fanget det. I målingen med lange tekster kalte brevet noe som er «en fordel» i annonsen for et krav, og skrev om en ferdig jobb i nåtid (merknad 4 og 5 i `my-project/testplan.md`).

**Approach:** KI-en sender navnet fra CV-en i et eget felt `navn`. Nettsiden setter alltid inn «Med vennlig hilsen» og navnet til slutt, uten et nytt KI-kall. Brev-prompten får to nye regler. Etterpå kjøres brevkriteriene på nytt med ekte KI, og plan B-regelen prøves på en annen CV. Dette er bestemt av Kristine 15. november, se «Bestemt 15. november» i testplanen.

## Boundaries & Constraints

**Always:**
- Brevet på siden og i Word-fila er det samme som i dag: avsnittene, så «Med vennlig hilsen» og navnet som to egne avsnitt. Uten navn kommer bare «Med vennlig hilsen».
- Hilsen og navn settes sammen ett sted i kjernen. Ruter og `fil_ut` bruker den funksjonen og setter aldri sammen selv. Story 7.x (PDF og «Nytt forslag») skal bruke den samme.
- `navn` renses som avsnittene (`_rens_avsnitt`). Er det tomt eller bare mellomrom, blir det `None`, slik `arbeidsgiver` gjør.
- Lagret form er det samme som KI-svaret etter `kontroller`: `{avsnitt, navn}`. `lag_testsvar.py` skriver altså testsvarene i formen som `TestKI` leser.
- Ekte KI kjøres med samme rutine som i story 4.5: tre kjøringer per testcase, og kjøring 1 blir de ferdige svarene i testmodus.

**Never:**
- Prompten for gap-analysen og nøkkelordene skal ikke endres (merknad 1–3 er godtatt).
- Ikke noe nytt KI-kall for å reparere et brev.
- Ikke noe om Korrektur. Epic 5 får sin egen form.
- Ingen nye avhengigheter.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Vanlig | `{avsnitt: [overskrift, 4 avsnitt], navn: "Sara Eksempel"}` | Brevet vises med avsnittene + «Med vennlig hilsen» + «Sara Eksempel» | N/A |
| Uten navn | `navn: null`, `""` eller `"  "` | Brevet slutter med «Med vennlig hilsen» | N/A |
| KI-en skriver hilsenen likevel | De siste avsnittene er «Med vennlig hilsen» (også med komma eller annen stor/liten bokstav) og eventuelt navnet, eller «Med vennlig hilsen Sara Eksempel» i ett avsnitt | `kontroller` fjerner dem, så hilsenen ikke kommer to ganger | N/A |
| Bare hilsen | Avsnittene er bare hilsen og navn | Tomt brev | KIFeil(ubrukelig_svar) |
| Feil form | `navn` mangler, er et tall, eller det finnes ekstra felt | — | KIFeil(ubrukelig_svar) |

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/ki.py:54-58` -- `SKJEMA["brev"]`: legg til `navn` (`anyOf [string, null]`, som `arbeidsgiver` på l. 43), required begge.
- `backend/soknad/kjerne/ki_svar.py` -- `FELT["brev"]` (l. 14), `_riktig_form` (l. 30), `_rens` (l. 74), docstring for `kontroller`. Fjerning av hilsenen KI-en skrev selv skjer i `_rens`, før tom-sjekken.
- `backend/soknad/kjerne/` -- ny funksjon, for eksempel `hele_brevet(brev) -> list[str]`, i `ki_svar.py` eller en ny `kjerne/brev.py`.
- `backend/soknad/web/ruter.py:273` (`lag_docx`) og `:458-463` (`_vis_brev`) -- bruker den nye funksjonen.
- `backend/soknad/kjerne/okt.py:52` -- kommentaren om formen.
- `backend/prompts/brev.md:45-49` -- reglene for formen og JSON-linjen.
- `backend/testdata/case-1-utvikler/ki-svar/brev-{1,2}.json`, `case-2-okonomi/ki-svar/brev-{1,2}.json` -- skrives på nytt av kjøring 1.
- `backend/scripts/lag_testsvar.py` -- trenger ingen endring (`skriv_svar` skriver objektet som det er). `--testdata`, `--ut` og `--case`.
- Tester som må følge med: `tests/adaptere/test_ekte_ki.py` (`BREV_SVAR`, `test_fr22_brevskjemaet_er_avsnitt`, test for prompt-reglene), `test_ki_gjennom_sdk.py:21,26`, `tests/kjerne/test_ki_svar.py`, `tests/web/test_brev.py:436` (`<p>` = avsnitt), `tests/web/test_nedlasting.py:61`, `tests/web/test_ekte_ki_i_flyten.py:28,76`, `tests/test_testdata.py:244`, `tests/kjerne/test_okt.py:245`, `tests/adaptere/test_fil_ut.py`.
- `my-project/5-arkitektur/arkitektur.md` AD-4 (ca. l. 90) -- tabellraden for `brev`.
- Inndata til de nye kjøringene: `my-project/testkjoringer/4-5/inndata/` (kriterium 3) og `my-project/testkjoringer/retro-4/inndata/case-lang/` (den andre CV-en).

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/adaptere/ki.py` -- `navn` i skjemaet.
- [x] `backend/soknad/kjerne/ki_svar.py` -- form, rensing av `navn`, fjerning av hilsenen KI-en skrev selv, og funksjonen som setter sammen brevet med hilsen. Oppdater docstringen.
- [x] `backend/soknad/web/ruter.py`, `okt.py` -- bruk funksjonen på siden og i Word.
- [x] `backend/prompts/brev.md` -- (a) skriv ikke hilsen eller navn i `avsnitt`, men gi navnet fra CV-en i `navn`, eller null; (b) kall ikke noe et krav når annonsen sier at det er en fordel; (c) skriv om jobber og verv i nåtid bare når CV-en sier at de pågår, ellers i fortid. Hold linjen om antall ord og avsnitt i samsvar.
- [x] `backend/tests/` -- oppdater testene i Code Map, og legg til tester for hver rad i matrisen og for de to nye reglene i prompten.
- [x] `my-project/5-arkitektur/arkitektur.md` -- AD-4: `brev` er `{avsnitt: [str], navn: str | null}`, og hilsenen settes inn av kjernen.
- [x] Ekte KI (gjøres av hovedøkten etter kodegjennomgangen, ikke av implementasjonsagenten, så en endring i prompten under gjennomgangen ikke krever en ny betalt kjøring): runde 1 for case 1, case 2 og kriterium 3, tre kjøringer hver, til `my-project/testkjoringer/brev-hilsen/runde-1/`. Kjøring 1 for case 1 og 2 blir testsvarene. I tillegg én kjøring med `case-lang`. Ved brudd: plan B én gang (prompten forbedres, og alt kjøres på nytt i runde 2).
- [x] `my-project/testplan.md` (hovedøkten, etter kjøringen) -- ny seksjon med resultatene (kriterium 1, 3, 11 og 14, hilsen og navn, plan B på `case-lang`, merknad 4 og 5), kostnad og tid, og oppdatert statustabell.

**Acceptance Criteria:**
- Gitt testmodus, når brevet vises eller lastes ned, så er teksten lik det før endringen for begge casene (hilsen og navn til slutt).
- Gitt kjøringene med ekte KI, så har alle brevene «Med vennlig hilsen» og riktig navn, og kriterium 11 og 3 er bestått eller står som ikke bestått med grunn.
- Gitt `case-lang`, så rangerer ikke brevet ferdighetene, kaller ikke det som er en fordel for et krav, og skriver om den ferdige jobben i fortid. Ellers står det som merknad i testplanen.

## Implementation Notes

- De fire `testdata/case-*/ki-svar/brev-{1,2}.json` er gjort om til den nye formen for hånd (hilsen og navn tatt ut, `navn` lagt til), så testmodus virker til kjøring 1 med ekte KI lager dem på nytt.
- `_bmad-output/planning-artifacts/architecture/architecture-kode-prosjekt-2026-11-04/ARCHITECTURE-SPINE.md` fikk den nye versjonen av `my-project/5-arkitektur/arkitektur.md`, så de to kopiene fortsatt er like.
- `test_testdata.py` krever at `navn` er første linje i CV-en og at det ikke står noen hilsen i `avsnitt` i JSON-fila. Skriver KI-en hilsenen i kjøring 1, blir testen rød selv om siden er riktig. Det er med vilje, så et brudd på regelen synes.

- Ekte KI: runde 1 hadde ett brudd på kriterium 11 (kriterium 3, «Python er en sentral del av utdanningen min»), så regelen mot rangering i `brev.md` ble utvidet (plan B), med en test. Runde 2 besto. Ingrid-kjøringen i runde 1 stoppet fordi kreditten var brukt opp, og ble kjørt i runde 2. Case 2 fikk «lønn» som 17. nøkkelord, så `fasit.md` ble oppdatert (7 av 17 = 41 %). Resultatene står i `my-project/testplan.md`.

## Spec Change Log

## Review Triage Log

Gjennomgang 1 (blind, spesialtilfeller, testhull):

| # | Funn | Vurdering | Begrunnelse | Rute |
|---|------|-----------|-------------|------|
| 1 | Navnet alene til slutt i `avsnitt` (uten hilsen) fjernes ikke, så navnet kommer to ganger (alle tre) | medium | Det samme svaret fra KI-en som det `_uten_hilsen` skal fange. Sjekket i `_uten_hilsen`: bare treff på hilsenen gir fjerning | patch |
| 2 | Varianter som «Vennlig hilsen», «Mvh» og nynorsk «Med venleg helsing» fanges ikke (spesialtilfeller, blind) | low | Det skjer når prompten forbyr akkurat «Med vennlig hilsen». Retting er bare regex-en | patch |
| 3 | «Skriv ikke … studentens navn i `avsnitt`» kan leses som at navnet ikke får stå noe sted, også i e-posten (blind) | low | Case 2 `brev-2` har `jonas.eksempelsen@example.com`. Retting er ett ord i prompten («til slutt») | patch |
| 4 | `test_testdata.py` sjekker ikke at navnet mangler til slutt i `avsnitt` (blind) | low | Riktig, sjekker bare hilsenen (l. 259). Én linje | patch |
| 5 | Hilsen + navn + et avsnitt til (tlf., P.S.) fjernes ikke (testhull, spesialtilfeller) | low | Lite sannsynlig. Retting krever søk bakover og risikerer å slette innhold | avvist |
| 6 | Nest siste er bare hilsenen, og da fjernes det siste avsnittet uansett hva det er (alle tre) | low | Teksten etter en hilsen er avslutningen. Krav om at den er lik `navn` gir dobbel hilsen når navnet er skrevet litt annerledes | avvist |
| 7 | Hilsen limt inn til slutt i det siste avsnittet («… intervju. Med vennlig hilsen Sara») (spesialtilfeller, blind) | low | Ikke sett i noen av de 40+ brevene fra ekte KI. Søk midt i avsnitt kan slette innhold | avvist |
| 8 | `navn` som selv har hilsenen, eller «Navn: …» (spesialtilfeller, blind) | low | Lite sannsynlig med skjema og prompt. Krever en ny gren | avvist |
| 9 | Bare overskriften igjen etter fjerningen godtas (spesialtilfeller) | low | Gjaldt før endringen også (et brev med bare overskrift ble godtatt). Ikke sett fra ekte KI | avvist |
| 10 | Fjerningen logges ikke, så kjøringen med ekte KI viser ikke om KI-en følger regelen (blind) | low | Kjernen logger ingenting (AD-12). For brukeren er hilsen og navn nå alltid riktige, og det er det kriteriet sjekker | avvist |
| 11 | Regelen om nåtid trenger dagens dato, og «2024–2027» blir fortid (blind) | low | Regelen er slik Kristine bestemte den («nåtid bare når CV-en sier at de pågår»). Kjøringen med `case-lang` prøver den | avvist |
| 12 | Regelen om «fordel» nevner ikke «ønskelig», «et pluss»; bare testet som tekst i prompten (blind) | low | KI-en generaliserer ut fra eksemplet. Atferden sjekkes med ekte KI i denne PR-en | avvist |
| 13 | Testsvarene er endret for hånd, ikke laget av `lag_testsvar.py` (blind) | false | Kjøring 1 med ekte KI i denne PR-en lager dem på nytt (oppgavelista) | avvist |
| 14 | Korrektur (epic 5) er ikke tatt med: `navn`, hilsen i eget brev, AD-10 (blind) | false | Utenfor med vilje: «Ikke noe om Korrektur» i Boundaries. Tas opp i story 5.2 | avvist |
| 15 | Eldre spec-kopier og testplanen l. 54 beskriver den gamle måten; ingen spec-kopi eller todo (blind) | false | Spec-kopiene er historikk og endres ikke. Testplanen og kopien av spec-en gjøres i denne PR-en | avvist |

## Design Notes

Hilsen og navn ligger utenfor `avsnitt`, så testsvarene, sesjonen og `kontroller` har én form. Bare visningen legger dem til. Korrektur (epic 5) har sin egen form og påvirkes ikke.

## Verification

**Commands:**
- `cd backend; uv run ruff check; uv run ruff format --check; uv run pytest` -- expected: alt grønt.

**Manual checks (if no CLI):**
- Brevsiden i testmodus ved 375 og 1280 px, og Word-fila: hilsen og navn til slutt, ingen dobbel hilsen.
