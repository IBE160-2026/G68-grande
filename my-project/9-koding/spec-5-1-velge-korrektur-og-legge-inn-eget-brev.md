---
title: 'Story 5.1: Velge Korrektur og legge inn eget brev'
type: 'feature'
created: '2026-11-15'
baseline_commit: 'd4c7fb04351fc23473f9a1827e8494245b428519'
status: 'done'
route: 'dispatch'
review_loop_iteration: 1
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-5-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nettsiden har bare Full generering. En student som har skrevet et brev selv, kan ikke velge Korrektur eller legge inn brevet sitt (FR-20, FR-8, FR-9). Det finnes heller ikke noe testbrev, så Korrektur kan ikke prøves i testmodus (FR-34, NFR-3).

**Approach:** Modusvalget får kortet Korrektur. I Korrektur har innleggingen et tredje felt, «✉️ Ditt søknadsbrev», mellom CV og annonse, med de samme tilstandene, tekstene og feilene som de to andre. Testmodus kjenner igjen et nytt fiktivt `eget-brev.txt` i case 1. Resultatsiden i Korrektur viser gap-analysen og nøkkelordtreffet som før, men uten knappen videre til brevet (den kommer i 5.2).

## Boundaries & Constraints

**Always:** Kortet: ✏️ «Korrektur» · «Forbedre mitt brev» · «Du har skrevet et brev selv. Vi forbedrer språket og beholder innholdet ditt.», ved siden av Full generering, under hverandre under 700 px, hele kortet er én knapp. Overskriften i Korrektur: «Legg inn CV-en din, brevet ditt og stillingsannonsen». Rekkefølgen er CV, brev, annonse, også i feilboksen. Brevfeltet må fylles ut og har grensen på 15 000 tegn. Feiltekstene begynner med «Ditt søknadsbrev:». Tre felt side om side fra 1000 px, under hverandre under. «Tilbake» til modusvalget beholder CV og annonse (og brevet). Testbrevet er fiktivt og skrevet til annonsen i case 1, med ting som bør forbedres og minst én av de 17 KI-frasene. Testene kaller aldri det ekte API-et, og hver test nevner FR-nummeret.

**Never:** Ikke `korrektur()` i KI-en, `prompts/korrektur.md`, knappen «Oppdater søknadsbrevet mitt» eller feltet `korrektur` i `Soknad` (5.2). Ikke markeringer (5.3). Ikke PDF (Epic 6). Ingen ekte KI-kjøring. Ingen endring i Full generering, utenom at koden blir felles.

**Beslutning (Kristine, 2026-11-15):** CV og annonse fra case 2 i Korrektur gir den vanlige teksten på brevfeltet, «Ditt søknadsbrev: I testmodus fungerer bare testdataene fra mappen backend/testdata/.». Ingen ny feiltype og ikke noe testbrev for case 2.
**Beslutning (Kristine, 2026-11-15):** spec-en beholdes samlet (ca. 2600 tokens).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Korrektur, riktig | CV, eget brev og annonse fra case 1 i testmodus | resultatsiden med gap og treff, uten brevknapp | – |
| Brevet tomt | CV og annonse fylt ut, brevet tomt | «Ditt søknadsbrev: Fyll inn feltet. Last opp en PDF eller lim inn tekst.» | ingen KI-kall |
| Brevet for langt | over 15 000 tegn | «Ditt søknadsbrev: Teksten er for lang. Den kan være på høyst 15 000 tegn.» | ingen KI-kall |
| Ukjent brev | testmodus, CV fra case 1, egen brevtekst | «Ditt søknadsbrev: I testmodus fungerer bare testdataene fra mappen backend/testdata/.» | `ikke_testdata` på brevfeltet |
| Case 2 | testmodus, CV og annonse fra case 2, brevet fra case 1 | samme tekst som «Ukjent brev» | `ikke_testdata` på brevfeltet |
| Uten testmodus | Korrektur med ekte KI, alle felt fylt ut | analysen kjøres som i Full generering | – |
| Full generering | modus Full generering | ingen brevfelt, og et `eget_brev` i skjemaet ignoreres | – |
| Tilbake | Korrektur → «Tilbake» → Full generering → Korrektur | CV, annonse og brev står der fortsatt | – |
| Brevknapp i Korrektur | POST `handling=brev` på resultatsiden i Korrektur | blir avvist | 400 |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/okt.py:21-24` -- `Modus` får `KORREKTUR = "korrektur"`. `Soknad.eget_brev: Tekstfelt` finnes allerede (L46), men brukes ikke. `sett_inndata` (L76-95) får `eget_brev` (None i Full generering = brevet i søknaden er uendret). Er alle tre feltene like som før, er søknaden uendret. Er ett av dem endret, også bare brevet, nullstilles resultatene og steget blir høyst innlegging, akkurat som før. Ingen unntak for bare brevet: ruten kjører analysen på nytt uansett, og resultatsiden skal ikke kunne åpnes med et brev som ikke har bestått sjekken (AD-8). `velg_modus` (L69-73) beholder `eget_brev`.
- `backend/soknad/kjerne/inndata.py:52-77` -- `INNLEGGINGSFELT = ("cv", "annonse")` og `sjekk_innlegging`. Felt per modus (Korrektur: `cv`, `eget_brev`, `annonse`). Samme sjekk av TOM og FOR_LANG, og testdata-sjekken bare for felt uten feil.
- `backend/soknad/kjerne/testdata_match.py:17-62` -- `Testcase` får `eget_brev: str | None` (vasket). `finn_case` får `eget_brev=None`. Når det er satt, gir et brev som ikke er brevet i caset til CV-en, `IKKE_TESTDATA`. Er CV-en ukjent, får brevet feilen bare hvis det ikke er brevet i noe case (som annonsen). Tomt felt gir aldri testdatafeil.
- `backend/soknad/adaptere/ki.py:85-119` -- `les_testcaser` leser `eget-brev.txt` hvis den finnes (valgfri, case 2 har ingen). `_sjekk_unike` tar med brevene som finnes.
- `backend/soknad/web/tekster.py:78-111,258-288` -- `MODUS_KORT` får Korrektur. Ny `INNLEGGING_OVERSKRIFT_KORREKTUR`, og en tittel for fanen («Legg inn CV, brev og annonse»). `INNLEGGINGSFELT` får `"eget_brev": ("✉️", "Ditt søknadsbrev", "brevfeltet")`. `FEILTEKSTER` får `("eget_brev", TOM/FOR_LANG/IKKE_TESTDATA)`.
- `backend/soknad/web/ruter.py:141-200,203-242,424-456` -- `innlegging` leser `eget_brev` bare i Korrektur og sender det til `sett_inndata` og `sjekk_innlegging`. `_vis_innlegging` sender feltene for modusen, overskriften og `tekst["eget_brev"]`. `resultat` avviser `handling=brev` i Korrektur med 400, og `_vis_resultat` sender et flagg for modusen.
- `backend/soknad/web/templates/innlegging.html:11,29-37,44-74` -- løkken går over feltene for modusen, ikke hele `tekster.INNLEGGINGSFELT`. `modus.html` trenger ingen endring.
- `backend/soknad/web/templates/resultat.html:111-117` -- knappen «Lag søknadsbrevet mitt» bare i Full generering. «Tilbake» står i begge.
- `backend/soknad/web/static/css/stil.css:842-850` -- `.felt-rad` får tre kolonner fra 1000 px når det er tre felt (for eksempel en egen klasse). `.modus-kort` (L465-490) har allerede to side om side fra 700 px. `innlegging.js` virker uendret for et tredje felt.
- `backend/testdata/case-1-utvikler/eget-brev.txt` (ny) og `fasit.md` -- nytt avsnitt `## Sjekkliste for Korrektur` (innhold, eksempler og rekkefølge beholdt, KI-frasen skrevet om). Brevet bruker navnet fra `cv.txt`.
- `README.md:74` -- nevn `eget-brev.txt` i case 1. L102 og treet ved L118 ved behov.
- Tester som må endres: `tests/kjerne/test_okt.py:73` (`list(Modus)`), `tests/web/test_modusvalg.py:141` (bare ett kort), `tests/web/test_innlegging.py:342,380,517,529`, `tests/web/test_tekster.py:10`. Gjenbruk `tests/web/hjelpere.py` og fixturene `paa_innlegging`/`paa_resultat` (kopier ikke). `KI_FRASER` står i `tests/test_testdata.py:218-236`.
- Gamle kommentarer som sier «Epic 5» om Korrektur, skal si story 5.2: `adaptere/ki.py:68`, `kjerne/okt.py:151`, `web/ruter.py:404`.
- `adaptere/ki.py` `_sjekk_unike`: feilteksten må ikke si at brevet er påkrevd, for eksempel «Hvert testcase må ha sin egen CV og annonse, og sitt eget brev hvis det har et.»
- `fasit.md`, «Sjekkliste for Korrektur»: «så jeg kan begynne i august» står i innholdet som skal beholdes, og blandingen av «dere» og «du» og «Hei!» står blant tingene som bør forbedres. Hilsen og navn på slutten bestemmes i 5.2, ikke her. En test sjekker at de to KI-frasene som fasiten nevner, står i `eget-brev.txt`.
- Ikke endre: `tests/kjerne/test_ki_svar.py:104-106` (Korrektur i `kontroller` kommer i 5.2), `innlegging.js`, `_med_ki`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/okt.py`, `inndata.py`, `testdata_match.py`, `adaptere/ki.py` -- Korrektur i `Modus`, `eget_brev` i inndata, sjekken og testdataene -- kjernen først, så webdelen kan bygge på den
- [x] `backend/soknad/web/tekster.py`, `ruter.py`, `templates/innlegging.html`, `templates/resultat.html`, `static/css/stil.css` -- kortet, brevfeltet, overskriften, ingen brevknapp i Korrektur, tre kolonner
- [x] `backend/testdata/case-1-utvikler/eget-brev.txt`, `fasit.md`, `README.md` -- det fiktive testbrevet, sjekklisten for Korrektur og hvor brevet ligger
- [x] `backend/tests/kjerne/*`, `tests/adaptere/test_ki.py`, `tests/web/test_modusvalg.py`, `test_innlegging.py`, `test_resultat.py`, `test_tekster.py`, `tests/test_testdata.py` -- oppdater de gamle testene, og nye tester for hver rad i matrisen, kortet og testbrevet (fiktivt, minst én KI-frase, sjekklisten finnes)

**Acceptance Criteria:**
- Given modusvalget, when siden vises, then står kortene Full generering og Korrektur i den rekkefølgen, og hvert kort er én knapp
- Given innleggingen i Korrektur, when siden vises, then er overskriften og de tre feltene i rekkefølgen CV, brev, annonse, og feltet for brevet har samme tom tilstand, lim inn, søppelbøtte og feilmarkering som de andre
- Given innleggingen i Full generering, when siden vises, then er det to felt og den gamle overskriften, akkurat som før
- Given testmappen, when testene kjører, then finnes `eget-brev.txt` i case 1 med minst én av de 17 KI-frasene og bare fiktive opplysninger, og `fasit.md` har `## Sjekkliste for Korrektur`

## Implementation Notes

## Spec Change Log

- **Runde 1 → 2 (2026-11-15).** Funn: når bare brevet endres, beholdt `sett_inndata` analysen og steget RESULTAT, også når det nye brevet var tomt, for langt eller ikke testdata. Da kunne resultatsiden åpnes med et brev som ikke hadde bestått sjekken, og i 5.2 ville knappen videre bruke det. Unntaket sparte heller ingen KI-kall, fordi «Sjekk CV-en min» alltid kjører analysen på nytt. Endret: Code Map for `okt.py` (ingen unntak for bare brevet), og tre små rettinger fra gjennomgangen (gamle kommentarer, feilteksten i `_sjekk_unike`, fasiten og en test for den). Unngår: resultatsiden med et brev som ikke er sjekket (AD-8). **KEEP:** alt annet fra runde 1 virket og skal beholdes som det var. Koden fra runde 1 ligger i `_bmad-output/implementation-artifacts/keep/spec-5-1-runde-1.patch`. Bruk den som grunnlag (`git apply`), og endre bare det som står over: særlig `felt_for_modus` som eneste sted for feltene, `finn_case` og `les_testcaser` med valgfritt brev, rutene, malene, CSS-en med `tre-felt`, `eget-brev.txt` (teksten uendret), README, og testene. Testen `test_fr8_sett_inndata_med_bare_nytt_eget_brev_beholder_analysen` blir en test for at bare nytt brev nullstiller resultatene og steget.

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap (annet), edge-case, blind | Bare nytt brev beholder analysen og steget RESULTAT, også med et brev som feiler sjekken | medium | Stemmer: ruten lagrer søknaden før `sjekk_innlegging` (`ruter.py:181-200`), og `sett_inndata` returnerer med steg RESULTAT, så GET `/resultat` åpnes. Ufarlig i 5.1, men 5.2 ville bruke brevet. Planen ba om dette → bad_spec |
| 2 | blind | Å beholde analysen sparer ingenting, for analysen kjøres på nytt ved «Sjekk» | medium | Stemmer: `innlegging()` kaller alltid `_med_ki(... ANALYSE_KALL ...)` når sjekken består. Samme rot som 1 |
| 3 | edge-case | POST uten `eget_brev` i Korrektur (gammel fane fra Full generering) tømmer brevet | low | Stemmer, men krever to faner og modusbytte i den andre. Gjelder likevel bare innhold brukeren ser på siden etterpå. Retting = ny vakt. Avvist (lite sannsynlig, legger til vakt) |
| 4 | edge-case | Tom `eget-brev.txt` (bare tegnsetting) gjør at et brev med bare tegn godtas | low | Testbrevet er ikke tomt. Gjelder bare om noen lager en tom testfil. Samme for CV i dag. Avvist (hypotetisk, ny vakt) |
| 5 | edge-case | `eget-brev.txt` som er en mappe, blir oversett | low | Hypotetisk, ingen vil lage det. Avvist |
| 6 | blind | `sjekk_innlegging` gjetter modus ut fra `eget_brev is None` | low | Eneste kaller er ruten, som sender brevet ut fra `felt_for_modus(lagret.modus)`. Ingen kaller i dag går feil. Retting endrer signaturen. Avvist |
| 7 | blind | Korrektur er en blindvei til 5.2 (ingen knapp videre) | false | Intensjonen sier uttrykkelig at knappen kommer i 5.2. 5.2 lages samme dag. Avvist |
| 8 | blind | Feilteksten for case 2 er misvisende, og testhjelpen nevner ikke brevet | false | Kristine bestemte teksten (frosset beslutning). Avvist |
| 9 | blind | Feilteksten i `_sjekk_unike` sier at brevet er påkrevd | low | Stemmer, direkte tekstretting. Tatt med i runde 2 |
| 10 | blind | Gamle kommentarer «Epic 5» i `ki.py:68`, `okt.py:151`, `ruter.py:404` | low | Stemmer (sjekket med grep). Direkte retting. Tatt med i runde 2 |
| 11 | blind | Sjekklisten for Korrektur mangler «begynne i august», «dere/du» og «Hei!» | low | Stemmer for august og dere/du. Hilsen og navn hører til 5.2. Direkte tekstretting. Tatt med i runde 2 |
| 12 | blind | Ingen test holder fasiten og brevet i takt | low | Stemmer. En liten test. Tatt med i runde 2 |
| 13 | blind | Malen bruker `felter \| length == 3` som magisk tall | low | Det finnes bare to moduser. Ingen navngitt skade. Avvist |
| 14 | blind | Løkken i `test_fr9_feltene_star_i_samme_rekkefolge_som_feilene` kan ikke feile | low | Rekkefølgen på siden og i feilboksen er testet i `test_fr8_korrektur_har_overskriften_og_tre_felt_i_rekkefolge` og `test_fr9_alle_tomme_i_korrektur_gir_feilene_i_rekkefolgen_cv_brev_annonse`. Avvist |
| 15 | runde 2: blind, edge-case | POST uten `eget_brev` i Korrektur (gammel fane) tømmer brevet | low | carried fra rad 3: samme sted og samme påstand, koden er uendret. Avvist |
| 16 | runde 2: edge-case | Tom `eget-brev.txt` gjør at et brev med bare tegn godtas | low | carried fra rad 4. Avvist |
| 17 | runde 2: blind | `sjekk_innlegging` gjetter modus | low | carried fra rad 6. Avvist |
| 18 | runde 2: blind | Magisk tall `felter \| length == 3` | low | carried fra rad 13. Avvist |
| 19 | runde 2: blind | Testhjelpen i Korrektur nevner ikke testbrevet | false | carried fra rad 8 (Kristines beslutning). Avvist |
| 20 | runde 2: edge-case | Gammel Korrektur-fane sendt etter bytte til Full generering: brevet ignoreres og analysen kjøres som Full generering | low | Stemmer, men krever to faner og modusbytte, og brevet i økten er uendret (ingen tap). Retting = ny vakt. Avvist |
| 21 | runde 2: blind | `test_fr8_full_generering_ignorerer_eget_brev_i_skjemaet` tester ikke det den sier | low | Delvis: en rute som lagret brevet fra skjemaet, ville feilet testen. En rute som tømte brevet, ville bestått. Direkte retting i testen → patch |
| 22 | runde 2: blind | Ingen test for KI-feil og KI-grensen i Korrektur | false | Samme `_vis_innlegging` med `soknad.eget_brev` brukes for feilene, og «Prøv på nytt» sender hele `innlegging-skjema`. Ingen feil vist. Avvist |
| 23 | runde 2: blind | Statuslinjen i README sier at Korrektur «kommer» | false | Stemmer fortsatt: Korrektur virker ikke helt før story 5.2. Avvist |
| 24 | runde 2: blind | README nevner ikke at like egne brev stopper oppstarten, og at `eget-brev.txt` er valgfri | low | Stemmer. Direkte tekstretting → patch |
| 25 | runde 2: blind | Et testbrev som mangler eller er tomt, stopper ikke oppstarten | low | `test_fr34_bare_case_1_har_et_eget_brev` passer på fila i repoet. Retting = ny vakt. Avvist |
| 26 | runde 2: blind | Sjekklisten for Korrektur nevner ikke arbeidsgiveren, rollen hennes i gruppa og hva KI-frasen betyr | low | Stemmer. Direkte tekstretting → patch. Tittellinje og hilsen hører til 5.2 |
| 27 | runde 2: blind | «Er dette Korrektur?» står to steder for resultatsiden | low | Begge byttes ut når knappen kommer i 5.2. Ingen skade nå. Avvist |
| 28 | runde 2: blind | Plandokumentene er ikke oppdatert (kopi i `my-project/9-koding/`, sprint-status, todo) | false | Gjøres etter gjennomgangen, som i hver story. Ikke en feil i koden. Avvist |

## Design Notes

Feltene for modusen bestemmes ett sted (i `inndata`) og brukes både av sjekken, ruten og malen, så rekkefølgen i feilboksen og på siden alltid er lik. `eget_brev` beholdes i økten også i Full generering, men brukes ikke der. Da mister ikke brukeren brevet om hen bytter modus frem og tilbake.

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil (samme som CI)

**Manual checks (if no CLI):**
- Kristine prøver i nettleseren: modusvalget ved 375 og 1280 px, Korrektur med testdataene fra case 1, tomt brev, CV fra case 2 i Korrektur, «Tilbake» og at Full generering ser ut som før.
