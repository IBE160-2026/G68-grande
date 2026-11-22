---
title: 'Rettinger etter retro 7: advarselen og feilboksene, prosentlinjen ved feil og avstemming av papirene'
type: 'bugfix'
created: '2026-11-21'
status: 'done'
baseline_commit: '85e147a3bca20414ee25a06e5b67164975e8d99c'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-7-retro-2026-11-21.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Ingen test vokter at «Logg ut» advarer på brevsiden med KI-feilboksen fra «Nytt forslag» (retro 7, A2). En Word-nedlasting skjuler feilboksen fra en PDF som feilet (A3). Prosentlinjen fylles på nytt når resultatsiden viser en feilmelding (A7). To tekster i koden stemmer ikke lenger (A9). Kristines beslutninger fra 7.2–7.5 står bare i spec-ene, og README, oversikten, epic-konteksten og `issues.md` er ikke avstemt etter epic 7 (B).

**Approach:** Punkt 1–3 i retro 7 i én runde med én branch (`retro-7-rettinger`) og én PR. Punkt 4 (prosessen) føres inn i KI-ens minne.

**Beslutninger (Kristine, 2026-11-21):** én runde før epic 8, og spec-en beholdes hel (ca. 2 300 tokens). A1 godtas: brevet kan slettes uten vinduet når CV-en endres etter «Tilbake» eller et modus-kort velges, og det skrives i README. A7: prosentlinjen står stille når resultatsiden har en feilboks, samme regel som fyrverkeriet. A4 og A5 skrives som kjente begrensninger. Ekte KI trengs ikke.

## Boundaries & Constraints

**Always:** Skript endrer aldri søknadsdata (AD-1). Tester nevner FR-/UX-DR-/AD-nummeret og bruker `tests/web/hjelpere.py`. Endringer i en plan i `_bmad-output/` kopieres til samme fil i `my-project/` (kopiene er like i dag). Kristines egne formuleringer endres ikke utover det rettingen trenger. Ingen `style=`, ingen nye fargekoder.

**Never:** Ingen vindu på innleggingen eller modusvalget (A1). A4, A5, A6, A10 rettes ikke i koden. A8 (ð, ı, ħ) tas ikke med. Ingen endring i kjernen utenom navnet på tabellen i `filnavn.py` og docstringen i `ki_svar.py`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| KI-feil uten nedlasting | brevsiden, `lastet_ned` tom, «Nytt forslag» gir `KIFeil` | «Logg ut» har `data-bekreft="vindu-logg-ut"`, vinduet finnes | – |
| Alle kall brukt uten nedlasting | ekte KI, 10 kall brukt, «Nytt forslag» | samme som over | – |
| PDF feilet, så Word | feilboks med lenke `data-nedlasting="pdf"`, trykk på Word | feilboksen blir stående | – |
| Word feilet, så Word | feilboks med lenke for `docx`, trykk på Word eller «Prøv på nytt» | feilboksen skjules, fokus som før | – |
| Resultatsiden med KI-feil | `ki_feil` satt (også `KI_KALL_BRUKT`) | prosentlinjen har klassen `uten-animasjon` og fylles ikke | – |
| Resultatsiden uten feil | vanlig visning | prosentlinjen fylles på 1 s som før | – |

</frozen-after-approval>

## Code Map

- `backend/tests/web/test_vindu_logg_ut.py:146-162` -- ved siden av `test_ux_dr17_ki_feil_fra_nytt_forslag_beholder_nedlastingen` (samme mønster, men uten `paa_brev.get(NEDLASTING)`). `FeilendeKI(..., oppgave="brev")` og `logg_ut_knapp`. For `KI_KALL_BRUKT`: se `test_nfr11_alle_kall_brukt_gir_feilboksen_uten_prov_paa_nytt` i `test_nytt_forslag.py:378-393` (`paa_brev_med_ekte_ki`).
- `backend/soknad/web/static/js/nedlasting.js:38-48` -- `feilboks.querySelector("a[data-nedlasting]")` blir `'a[data-nedlasting="' + format + '"]'`. Oppdater kommentaren. Kildetekst-test i `test_nedlasting_pdf.py` eller `test_nedlasting.py` (mønster: andre skripttester der).
- `backend/soknad/web/templates/resultat.html:88-93` -- `<svg class="prosentlinje{% if ki_feil %} uten-animasjon{% endif %}" …>`. Rett kommentaren over.
- `backend/soknad/web/static/css/stil.css:1212-1222` -- ny regel `.prosentlinje.uten-animasjon .fyll { animation: none; }` med kommentar. CSS-test i `backend/tests/web/test_pynt.py` (ved `test_ux_dr13_prosentlinjen_fylles_paa_ett_sekund`, bruk `css_blokk`/`STIL`), og webtest: KI-feil på resultatsiden (mønster `test_resultat.py:659-672`, `FeilendeKI(oppgave="brev")` i Full generering) gir klassen, vanlig visning gir den ikke.
- `backend/soknad/kjerne/ki_svar.py:116-119` -- docstringen: siden, Word-fila, PDF-fila (7.2) og «Nytt forslag» (7.1) bruker den.
- `backend/soknad/kjerne/filnavn.py:17, 45` -- `_AEOEAA` → `_TIL_ASCII`, kommentaren sier at den gjelder bokstaver NFKD ikke deler opp. Sjekk med `grep` at testene ikke bruker navnet.
- Papirene (hver endring i begge kopiene der det står to):
  - `_bmad-output/planning-artifacts/epics.md` = `my-project/6-epics-og-stories/epics.md`: `:982` «`lastet_ned` settes til usann» → tømmes. `:1002` skriften: Noto Sans 11 pt (OFL), bestemt av Kristine 19. november 2026. Story 7.3: tegnsetting i annonsen regnes som lik (beslutning 19. november). Story 7.4: ikke fyrverkeri ved feilboks eller i høykontrast, og prosentlinjen står stille ved feilboks (21. november). Story 7.5: flere bindestreker blir én, bindestrek først/sist fjernes, uten JavaScript logges man ut uten vinduet.
  - `…/ux-designs/ux-kode-prosjekt-2026-10-20/EXPERIENCE.md` = `my-project/3-ux/EXPERIENCE.md`: `:249` (filnavn: bindestrekene), tabellen ved `:278-286` («Brevet vises»: ikke ved feilboks eller høykontrast; «Resultat»/KI-feil: prosentlinjen står stille), `:227` eller `:286` (uten JavaScript).
  - `…/architecture/architecture-kode-prosjekt-2026-11-04/ARCHITECTURE-SPINE.md:198-202` = `my-project/5-arkitektur/arkitektur.md` (AD-11): bindestrekene, og at ß, ł, đ, þ, œ står i tabellen.
  - `README.md:13` statuslinja: legg til «Nytt forslag», gjenbruken av nøkkelordlisten, pynten, vinduet før utlogging og arbeidsgiveren i filnavnet. `README.md:109-121` «Kjente begrensninger»: tre nye punkter (A1, A4, A5).
  - `my-project/README.md:94` -- rader for `spec-7-2-…`, `spec-7-3-…`, `spec-7-4-…`, `spec-7-5-…` og `spec-retro-7-rettinger.md` (som radene for 6.1/6.2).
  - `_bmad-output/implementation-artifacts/epic-7-context.md:7` = `my-project/8-koding/epic-7-context.md` -- «Story 7.1 og 7.2 er ferdige (flettet). Neste er 7.3.» → alle fem er ferdige.
  - `.logs/kristine/issues.md:27` -- `[ ]` → `[x]` (teksten sier alt løst 2026-11-19).

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/web/test_vindu_logg_ut.py` -- to tester for matrisens to første rader -- FR-6, NFR-4, UX-DR17
- [x] `backend/soknad/web/static/js/nedlasting.js` + kildetekst-test -- feilboksen bare for samme format -- FR-31
- [x] `backend/soknad/web/templates/resultat.html`, `stil.css`, `test_pynt.py`, `test_resultat.py` -- prosentlinjen ved feilboks -- UX-DR13
- [x] `backend/soknad/kjerne/ki_svar.py`, `filnavn.py` -- docstring og navn
- [x] Papirene i Code Map
- [x] `my-project/todo.md` -- merknad på punktet for runden (PR-en gjenstår)

**Acceptance Criteria:**
- Given redusert bevegelse, when resultatsiden vises, then står prosentlinjen ferdig fylt som før.
- Given `uv run pytest -q`, `ruff check` og `ruff format --check`, when de kjøres, then består alle.

## Implementation Notes

- Testen for «alle kall brukt» (`test_vindu_logg_ut.py`) bygger søknaden selv med konstantene fra `hjelpere.py`, fordi `paa_brev_med_ekte_ki` står i `test_nytt_forslag.py` og testfilene ikke henter hjelpere fra hverandre (`conftest.py`).
- Resultatsiden har tre nye tester i `test_resultat.py`: vanlig visning uten klassen, KI-feil fra «Lag søknadsbrevet mitt» med klassen (og samme bredde), og alle KI-kall brukt med klassen. CSS-testen står i `test_pynt.py`. Redusert bevegelse er uendret (den felles regelen slår av alle animasjoner, `test_ux_dr18_redusert_bevegelse_slaar_av_pynten`).
- Kildetekst-testen for feilboksen står i `test_nedlasting_pdf.py`, og den gamle sjekken i `test_nedlasting.py` er endret til den nye vakta.
- Beslutningene fra 7.4 og 7.5 («Mine valg») er ført inn med datoen storiene ble godkjent og flettet (20. november 2026, `git log` for `my-project/8-koding/`).
- `_bmad-output/` er git-ignorert, så endringene i planene vises i Git bare gjennom kopiene i `my-project/`. Kopiene er skrevet på nytt fra `_bmad-output/` (med CRLF, som før), og er like bortsett fra linjeskiftene.

- Etter gjennomgangen (16 funn): 8 små rettinger av tekster i README, AD-11, EXPERIENCE, epics og kommentarene i koden, og én ekstra sjekk i A2-testen. 1 utsatt (nettlesertest av `nedlasting.js`, issue #16), resten avvist. 1 392 tester består, og ruff er rent.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap, blind | At feilboksen bare skjules for samme format, testes bare som kildetekst i `nedlasting.js`, ingen test kjører skriptet | medium | Stemmer. Repoet har ingen nettlesertester (issue #16, story 8.2), som for de andre skriptene → defer (`deferred-work.md`) |
| 2 | edge-case | README (A1) sier bare «endrer CV-en», men brevet slettes også når annonsen endres | low | Stemmer: `sett_inndata` nullstiller brevet når et felt er endret. Direkte retting av teksten → patch |
| 3 | blind | «Samme regel som fyrverkeriet» er bare halvt sant, fordi fyrverkeriet også skjules i høykontrast | low | Stemmer for ordlyden. Direkte retting i kommentarene, EXPERIENCE og epics → patch |
| 4 | blind | Regelen om feilboksen per format står ikke i planene | low | Stemmer. Én setning i EXPERIENCE («Filen kan ikke lages») og epics (7.2) → patch |
| 5 | blind | Feilboksen som blir stående, sier ikke hvilket format som feilet | low | Teksten er fra UX-en og fantes før. Før rettingen forsvant boksen, som var verre. Ny tekst krever Kristines ordlyd → avvist |
| 6 | blind | Kildetekst-testene er sårbare for omskriving av skriptet | low | Samme rot som #1 → tas med i defer for #1 |
| 7 | blind | Manual checks i spec-en nevner ikke A2 og A3 | low | Rettingen er å endre denne spec-en → avvist. PR-en sier hvordan A2 og A3 er dekket |
| 8 | blind | Akseptansekriteriene er tynne, og statusen var `in-progress` | false | Matrisen i den frosne delen dekker A2, A3 og A7. Statusen settes av arbeidsflyten (`in-review` nå). Rettingen er å endre spec-en |
| 9 | blind | Resultatsiden testes bare i Full generering, og testen for alle kall sjekker ikke bredden | low | Klassen kommer bare fra `ki_feil` i malen, uten gren for modus. Ny test gir ingen ny dekning → avvist |
| 10 | blind | Søknaden med `ki_kall=MAKS_KI_KALL` bygges for hånd i to testfiler | low | Bare testkode, to steder. En ny hjelper i `hjelpere.py` er mer enn en direkte retting → avvist |
| 11 | blind | A2-testen sjekker bare `class="feilboks"`, ikke at det er KI-feilboksen | low | Stemmer. Én linje med `KI_FEIL_BEHOLDT_BREV` → patch |
| 12 | blind | EXPERIENCE linje 227 mangler unntaket uten JavaScript, som linje 286 har | low | Stemmer, dokumentet sier to ting. Direkte retting → patch |
| 13 | blind | I AD-11 står den nye bindestrek-regelen før punktet om 30 tegn | low | Stemmer (`arkitektur.md:201-202`). Direkte flytting → patch |
| 14 | blind | Kommentaren i `filnavn.py` forteller om navnebyttet og nevner bare små bokstaver | low | Stemmer, tabellen har også Ł, Đ, Œ og Þ. Direkte retting → patch |
| 15 | blind | README og epics (7.3) beskriver «lik annonse» ulikt | false | Begge stemmer: epics har Kristines beslutning om tegnsetting, README forklarer vasken for brukeren. Ingen motsigelse |
| 16 | edge-case | Kopien av spec-en i `my-project` har gammel status | low | Stemmer. Kopieres på nytt når runden avsluttes → patch (hovedøkten) |

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine, i testmodus: resultatsiden fylles som før. KI-feil på resultatsiden lages ikke lett i testmodus, så den sjekkes i testene. Les gjennom de nye tekstene i `epics.md`, `EXPERIENCE.md`, AD-11 og README.
