---
title: 'Story 3.2: Laste ned brevet som Word'
type: 'feature'
created: '2026-11-11'
status: 'done'
baseline_commit: 'fb66299e1b584baee5a23d7c57a4c1fe4ff1ed75'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Brevsiden viser brevet, men brukeren kan ikke ta det med seg. Det finnes ingen nedlasting (FR-29, FR-30).

**Approach:** Under brevarket står hovedknappen «Last ned som Word», en lenke til `GET /last-ned/docx`. Ruten lager filen i minnet med python-docx (`adaptere/fil_ut.py`, ett avsnitt per element i `brev["avsnitt"]`, uten topp- og bunntekst), setter `lastet_ned` og sender filen med filnavnet `Soknad_<ÅÅÅÅ-MM-DD>.docx` fra `kjerne/filnavn.py`. Et lite skript gjør knappen grønn med «✓ Lastet ned som Word» og viser «Filnavn: Soknad_<dato>.docx» under. Når siden lastes på nytt, viser serveren samme grønne tilstand ut fra `lastet_ned`. Kan filen ikke lages (`FilFeil`), vises brevsiden med feilboksen øverst: «Vi klarte ikke å lage filen. Prøv på nytt.» og knappen «Prøv på nytt». Brevet står der fortsatt. Kristine har bestemt at boksen ikke skal ha teksten «Brevet er ikke borte.».

## Boundaries & Constraints

**Always:** Word lages bare i `adaptere/fil_ut.py`, filnavnet bare i `kjerne/filnavn.py` (AD-11). `kjerne/` importerer aldri `docx`. Filen lages ved forespørselen og ligger aldri på disk (NFR-4). `lastet_ned` settes bare når filen er laget, og med `erstatt_soknad`, så en søknad som er endret i mellomtiden ikke skrives over. `sett_inndata`, `velg_modus` og `sett_brev` nullstiller `lastet_ned`. Alle tekster i `web/tekster.py`. JavaScript endrer bare hvordan siden ser ut, aldri søknadsdata. Hver testfil og testfunksjon nevner FR-nummeret.

**Never:** Ikke vinduet etter nedlasting (story 3.3), ikke PDF, arbeidsgiver i filnavnet, fyrverkeri eller «Nytt forslag» (Epic 7). Filnavnet leses ikke opp med `aria-live` (det leses opp i vinduet i 3.3).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Nedlasting | steg brev, brev finnes, GET `/last-ned/docx` | 200, Word-fil som vedlegg med `Soknad_<i dag>.docx`, `lastet_ned` sann | – |
| Filen kan ikke lages | `fil_ut` gir `FilFeil` (f.eks. kontrolltegn i et avsnitt) | Brevsiden (500) med feilboksen øverst, brevet vises, `lastet_ned` uendret | ingen redirect |
| For tidlig | steg < brev | redirect til siden for steget | – |
| Brevet mangler | steg brev, `brev` er None | redirect `/resultat` | – |
| Opptatt | `opptatt` sann | redirect til siden for steget, ingen fil | – |
| Allerede lastet ned | `lastet_ned` sann, GET `/brev` | knappen grønn med «✓ Lastet ned som Word», filnavnlinjen synlig | – |
| Nytt brev / endret inndata | `sett_brev`, `sett_inndata` (endret), `velg_modus` | `lastet_ned` usann | – |

</frozen-after-approval>

## Code Map

- `backend/pyproject.toml` + `uv.lock` -- `uv add python-docx==1.2.0` (versjonen fra arkitekturen).
- `soknad/kjerne/feil.py` -- ny `class FilFeil(Exception)` uten type.
- `soknad/kjerne/filnavn.py` -- ny `lag_filnavn(dato: date, endelse: str) -> str` → `Soknad_2026-11-11.docx`. Datoen sendes inn.
- `soknad/kjerne/okt.py` -- `Soknad.lastet_ned: bool = False` rett før `opptatt` (oppdater docstringen på linje 38). Ny `sett_lastet_ned(soknad)`. Nullstill i `velg_modus`, `sett_inndata` (bare når noe er endret) og `sett_brev`.
- `soknad/adaptere/fil_ut.py` -- ny `lag_docx(avsnitt: list[str]) -> bytes`: `Document()`, `add_paragraph` per avsnitt, tøm `core_properties` (author, last_modified_by, title), lagre til `BytesIO`. Alle unntak → `FilFeil`.
- `soknad/web/ruter.py` -- ny `last_ned(format)` på `/last-ned/<any(docx):format>` med `login_required` og `krever_steg(Steg.BREV)`. Rekkefølge: brev None → `/resultat`, `til_steget_hvis_opptatt`, `fil_ut.lag_docx` (kall via modulen, så testene kan bytte den ut), `erstatt_soknad(lagret, sett_lastet_ned(lagret))`, `send_file(BytesIO, as_attachment=True, download_name=..., mimetype=DOCX)`. `FilFeil` → `_vis_brev(soknad, fil_feil=True), 500`. `brev()` bruker også `_vis_brev`, som sender `avsnitt`, `lastet_ned` og `filnavn=lag_filnavn(date.today(), "docx")`.
- `soknad/web/tekster.py` -- `LAST_NED_WORD`, `LASTET_NED_WORD = "Lastet ned som Word"`, `FERDIG_IKON = "✓"`, `filnavn_linje(navn)` → «Filnavn: …» og `FIL_FEIL`.
- `soknad/web/templates/brev.html` -- h1 `autofocus` bare uten feil. Feilboksen etter h1 som i `resultat.html`, med `autofocus`, men «Prøv på nytt» er en lenke `<a class="hovedknapp">` til `/last-ned/docx`. Under brevarket: `<div class="nedlasting">` med lenken `id="last-ned-docx"` (klassen `ferdig` når `lastet_ned`), to `<span>` (vanlig tekst / ✓ med `aria-hidden` + «Lastet ned som Word») der den ene er `hidden`, og `<p class="filnavn-linje" id="filnavn-docx">` med `hidden` til den er lastet ned. `nedlasting.js` i `skript`-blokken.
- `soknad/web/static/js/nedlasting.js` -- ny. Ved klikk på `[data-nedlasting]`: legg til `ferdig`, bytt hvilken span som er `hidden`, vis filnavnlinjen, skjul `#feilboks`. Ingen `preventDefault`.
- `soknad/web/static/css/stil.css` -- under brevsiden: `.nedlasting` (sentrert, `gap`, `flex-wrap`), `a.hovedknapp` (`text-decoration: none`, `text-align: center`), `.nedlasting .hovedknapp` (inline-block, `width: auto`), `.hovedknapp.ferdig` (`--success-tint`, `--success`, kant `--success`, uten løft), `.filnavn-linje` (sentrert, `overflow-wrap: anywhere`).
- Gjenbruk: `.feilboks*`, `erstatt_soknad`, `til_steget_hvis_opptatt`, `krever_steg`, testhjelperne og `paa_brev`-fiksturen fra `tests/web/test_brev.py`. `test_alle_sider.py` klarer `AnyConverter` alt. `Cache-Control: no-store` settes alt for alle svar.

## Tasks & Acceptance

**Execution:**
- [x] `pyproject.toml`, `kjerne/feil.py`, `kjerne/filnavn.py`, `kjerne/okt.py` -- avhengigheten, feilen, filnavnet og feltet, med tester i `tests/kjerne/test_filnavn.py` (ny) og `tests/kjerne/test_okt.py` (feltlisten og nullstillingen).
- [x] `adaptere/fil_ut.py` + `tests/adaptere/test_fil_ut.py` (ny) -- fila åpnes med python-docx, avsnittene er like, ingen topp- og bunntekst, æøå beholdes, kontrolltegn gir `FilFeil`.
- [x] `web/ruter.py`, `web/tekster.py`, `brev.html`, `nedlasting.js`, CSS -- ruten og brevsiden.
- [x] `tests/web/test_nedlasting.py` (ny) -- hver rad i matrisen, `Content-Disposition` og mimetype, den nedlastede fila lik brevet, knappen og tekstene fra `tekster.py`, feilboksen med lenken og fokus, `test_alle_sider.py` nevner `web.last_ned`.

**Acceptance Criteria:**
- Given brevsiden, when den vises, then står «Last ned som Word» under brevet (FR-29).
- Given at brukeren trykker «Last ned som Word», when fila er lastet ned, then er knappen grønn med «✓ Lastet ned som Word», og «Filnavn: Soknad_<dato>.docx» står under (UX-DR16).
- Given den nedlastede fila, when den åpnes i Word, then har den bare brevteksten, ett avsnitt per avsnitt, uten topp- og bunntekst (FR-30).

## Implementation Notes

- Branch: `story/3-2-laste-ned-brevet-som-word`, fra `main` på `fb66299e1b584baee5a23d7c57a4c1fe4ff1ed75`. Sprint-status: 3.2 står på «in-progress». Implementert direkte i hovedøkten (ingen underagent).
- `uv add python-docx==1.2.0` tok også med `lxml` 6.1.3 og `typing-extensions` 4.16.0.
- Et kontrolltegn (for eksempel `\x00`) i et avsnitt gir `ValueError` i python-docx. Det blir `FilFeil` og brukes som ekte feiltest i tillegg til den utbyttede `lag_docx`.
- `nedlasting.js` flytter fokus til knappen under brevet når «Prøv på nytt» i feilboksen trykkes, så fokus ikke forsvinner når boksen skjules.
- Endret eldre test: `test_brev.py::test_fr26_…` tillater nå én lenke i `<main>`, og den lenken er nedlastingen.
- 548 tester, `ruff check` og `ruff format --check` grønne.
- Etter gjennomgangen: Word-fila får A4 og norsk bokmål (`nb-NO`), og nedlastingstesten sjekker `Cache-Control: no-store`. 549 tester, `ruff` grønn.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-11), tre lag: blind, kanttilfeller, testhull.

| # | Funn | Vurdering | Begrunnelse | Rute |
|---|------|-----------|-------------|------|
| 1 | Word-fila har amerikansk Letter-papir (malen i python-docx) | medium | Sjekket: 215,9 × 279,4 mm. Norske brukere skriver ut på A4 | patch |
| 2 | Språket i fila er en-US, så Word markerer det norske brevet som stavefeil | medium | Sjekket: `w:lang w:val="en-US"` i stilene. Brukeren skal jobbe videre i Word | patch |
| 3 | Nedlastingen sender ikke `Cache-Control: no-store` (send_file gir no-cache) | false | `login_required` setter `no-store` på alle svar (`innlogging.py:41`). Testen sjekker det nå | avvist |
| 4 | Filnavnlinjen regnes ut når siden vises, så den kan vise en annen dato enn fila etter midnatt (tre lag) | low | Riktig, men sjelden. Rettingen krever et nytt felt i `Soknad` | avvist |
| 5 | `date.today()` bruker serverens tidssone | false | Nettsiden kjører lokalt på brukerens PC, så tidssonen er brukerens | avvist |
| 6 | Skriptet viser «✓ Lastet ned» ved trykket, før det er kjent om fila kom fram | low | Valgt i Design Notes. Alternativet (fetch + blob) er mer JavaScript enn gevinsten | avvist |
| 7 | HEAD-forespørsel eller forhåndslasting av lenken setter `lastet_ned` | low | Nettlesere sender ikke HEAD eller forhåndslaster slike lenker av seg selv | avvist |
| 8 | FilFeil etter en vellykket nedlasting viser feilboksen og grønn knapp samtidig | false | FilFeil kommer av innholdet. Samme brev som lyktes før, lykkes igjen. Nytt brev nullstiller `lastet_ned` | avvist |
| 9 | Etter FilFeil står adressen på `/last-ned/docx`, så F5 laster ned på nytt | low | Med vilje (Design Notes): F5 er da det samme som «Prøv på nytt» | avvist |
| 10 | «Prøv på nytt» hjelper ikke når feilen kommer av et kontrolltegn i brevet | low | Kan ikke skje med testbrevet. Med ekte KI i Epic 4 hører en vask hjemme i `ki_svar.kontroller` | avvist |
| 11 | FilFeil logges ikke | low | Nettsiden logger ingenting ennå, og brevet skal aldri i loggen (NFR-4) | avvist |
| 12 | Metadata fra malen (laget 2013, «Microsoft Macintosh Word») er igjen | low | Kosmetisk, viser ikke noe om brukeren | avvist |
| 13 | `nedlasting.js` testes bare ved å lese kildeteksten | low | Riktig, som alle skriptene i prosjektet. Manuell sjekk i nettleseren dekker det | defer |
| 14 | Testen kan feile hvis den kjøres over midnatt | low | Ubetydelig | avvist |
| 15 | Svake tester: disk-testen ser bare på arbeidsmappen, ASCII-testen er triviell, `Content-Disposition` sjekkes ordrett | low | Riktig, men små. Arbeidsgiver i filnavnet testes i Epic 7 | avvist |
| 16 | `uv.lock` mangler i diffen | false | Tatt ut av diffen med vilje (bare pakkeliste). Den committes | avvist |
| 17 | Parameteren `format` skygger for den innebygde `format`, og PDF trenger en tabell | low | Gjør ingen skade. Tabellen hører til Epic 7 | avvist |

## Design Notes

- **Lenke, ikke skjema:** nedlastingen er en GET (AD-8), så knappen er en lenke som ser ut som en hovedknapp. Svaret er et vedlegg, så siden blir stående, og skriptet viser den grønne tilstanden. Feiler det, er svaret en HTML-side, og nettleseren viser brevsiden med feilboksen på adressen `/last-ned/docx`. «Prøv på nytt» og å laste siden på nytt prøver da nedlastingen igjen.
- **Feilboksen** har bare feilteksten og «Prøv på nytt», uten «Brevet er ikke borte.» fra skissen. Det har Kristine bestemt.
- **`lastet_ned` er sann/usann**, som i arkitekturen. Grønn tilstand per format (Word og PDF hver for seg) må vurderes i Epic 7.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Logg inn, case 1 → resultatsiden → «Lag søknadsbrevet mitt» → brevsiden: «Last ned som Word» under brevet. Trykk: fila `Soknad_<i dag>.docx` lastes ned, knappen blir grønn med ✓, filnavnlinjen står under. Last siden på nytt: fortsatt grønn.
- Åpne fila i Word: bare brevet, samme avsnitt som på siden, ingen topp- eller bunntekst, æøå riktig.
- 320 px og 200 % zoom: knappen og filnavnet uten rulling sidelengs.
