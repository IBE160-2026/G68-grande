---
title: 'Story 7.2: Laste ned brevet som PDF'
type: 'feature'
created: '2026-11-19'
baseline_commit: 'f342163530b5814110bde190638c5ba0f73a1969'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-7-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Brevet kan bare lastes ned som Word. Suksesskriterium 5 krever at både .docx og PDF kan åpnes (FR-29).

**Approach:** «Last ned som PDF» ved siden av «Last ned som Word». `GET /last-ned/pdf` lager PDF-en med fpdf2 og en fri TTF-skrift i `adaptere/fil_ut.py`. Søknaden husker hvilke formater som er lastet ned, så hver knapp blir grønn for seg (EXPERIENCE, reise 1 trinn 9).

## Boundaries & Constraints

**Always:** PDF-en har bare brevteksten fra `ferdig_brev` med avsnittene, uten markeringer, topp- eller bunntekst. A4, 25 mm marg, norsk språk, tomme forfatter- og tittelfelt, som Word-fila. Æøå riktig. Skriften ligger lokalt med lisensfila ved siden av. `kjerne/` importerer aldri fpdf. Søknaden endres bare i kjernen. Tekstene ordrett: «Last ned som PDF», «Lastet ned som PDF». Vinduet etter nedlasting åpnes hver gang og viser filnavnet for formatet som ble lastet ned. Samme `FilFeil` som for Word.

**Skrift (bestemt av Kristine 19. november 2026):** Noto Sans, 11 pt (fri lisens OFL). Word-fila beholder sin skrift.

**Never:** Ikke arbeidsgiver i filnavnet eller «Logg ut før nedlasting» (7.5), ikke fyrverkeri (7.4). Ingen endring i KI-delen eller i hvordan Word-fila lages.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| PDF | brevsiden, Full generering | `Soknad_<dato>.pdf`, `application/pdf`, teksten (pypdf) lik brevet med hilsen og navn, `lastet_ned` = {pdf} | – |
| Korrektur | brev med markeringer | PDF-teksten lik avsnittene på siden, uten «Endret setning» / «Du skrev» | – |
| Begge formater | Word så PDF | `lastet_ned` = {docx, pdf}, begge knappene grønne med hver sin filnavn-linje | – |
| Bare Word | etter Word, siden lastes på nytt | Word grønn, PDF blå, bare `filnavn-docx` synlig | – |
| Nullstilling | nytt forslag, ny modus, endret CV | `lastet_ned` tom, begge blå | – |
| Filfeil | `lag_pdf` feiler | brevsiden 500 med feilboksen, «Prøv på nytt» → `/last-ned/pdf` | `lastet_ned` uendret |
| Ukjent format | `/last-ned/txt` | 404 | – |
| Uten brev / opptatt | som Word | resultatsiden / siden for steget | – |

</frozen-after-approval>

## Code Map

- `backend/pyproject.toml` -- legg til `fpdf2==2.9.0` (AD-11, versjonen i arkitekturen). `uv lock`.
- `backend/soknad/fonts/` (ny) -- `NotoSans-Regular.ttf` (github.com/notofonts) og `OFL.txt`.
- `backend/soknad/adaptere/fil_ut.py` -- ny `lag_pdf(avsnitt) -> bytes` ved siden av `lag_docx`: A4, `MARG` 25 mm, skriften med `add_font`, 11 pt, avsnitt med `multi_cell` og luft mellom, `set_lang("nb-NO")`, tom forfatter/tittel/produsent. All feil → `FilFeil`. `PDF_MEDIETYPE`. Fjern «PDF kommer i Epic 7».
- `backend/soknad/kjerne/okt.py:69` -- `lastet_ned: frozenset[str] = frozenset()` (formatene som er lastet ned). `sett_lastet_ned(soknad, format)` legger til formatet. `velg_modus`, `sett_inndata`, `sett_brev`, `sett_korrektur`, `nytt_forslag` setter `frozenset()`. Tom mengde er usann, så 7.5 kan spørre «lastet ned i noe format».
- `backend/soknad/web/ruter.py:351` `last_ned` -- `<any(docx, pdf):format>`, velger `lag_docx`/`lag_pdf` og medietype etter format, `sett_lastet_ned(lagret, format)`, `_vis_brev(..., fil_feil=format)`.
- `backend/soknad/web/ruter.py:633` `_vis_brev` -- `fil_feil` er formatet eller None. Sender `lastet_ned` (mengden) og `filnavn` som `{"docx": ..., "pdf": ...}`.
- `backend/soknad/web/templates/brev.html:106` -- `.nedlasting` får én blokk per format (knapp `last-ned-<format>` + `filnavn-<format>`), Word først. Feilboksens «Prøv på nytt» går til `fil_feil`-formatet. Vinduet viser Word-filnavnet fra serveren.
- `backend/soknad/web/static/js/nedlasting.js` -- er alt laget per format. Nytt: kopier teksten fra `filnavn-<format>` til `vindu-nedlastet-filnavn` før `showModal()`.
- `backend/soknad/web/static/css/stil.css:1377` -- blokkene ved siden av hverandre, brytes til under hverandre når det er trangt (`flex-wrap`, ingen `nowrap`, ingen rulling sidelengs ved 320 px).
- `backend/soknad/web/tekster.py:250` -- `LAST_NED_PDF`, `LASTET_NED_PDF`.
- `README.md:13` og `:132` -- PDF-nedlasting virker, `adaptere/` lager Word- og PDF-fila, skriften og lisensen nevnt.
- Gjenbruk: `tests/web/hjelpere.py` (`paa_brev`, `paa_brev_korrektur`, `soknaden`, `html_av`, `element`), `filfeil`-fikstur i `test_nedlasting.py`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/pyproject.toml`, `backend/uv.lock`, `backend/soknad/fonts/` -- fpdf2 og skriften -- AD-11
- [x] `backend/tests/kjerne/test_okt.py` -- `lastet_ned` som mengde: legge til, to formater, nullstilling i alle fem funksjonene -- AD-8
- [x] `backend/soknad/kjerne/okt.py` -- som i Code Map
- [x] `backend/tests/adaptere/test_fil_ut.py` -- `lag_pdf`: pypdf-teksten lik avsnittene (mellomrom og linjeskift slått sammen), æøå, A4, lang tekst gir flere sider, tomme metadata, feil → `FilFeil` -- FR-30
- [x] `backend/soknad/adaptere/fil_ut.py`, `ruter.py`, `brev.html`, `nedlasting.js`, `stil.css`, `tekster.py` -- som i Code Map
- [x] `backend/tests/web/test_nedlasting_pdf.py` (ny) -- hver rad i matrisen, knappene og tekstene, skriptet kopierer filnavnet, CSS-en -- FR-29, FR-30, FR-31
- [x] `backend/tests/web/test_nedlasting.py`, `test_nytt_forslag.py`, `test_vindu_etter_nedlasting.py` -- `lastet_ned is True/False` → mengden
- [x] `README.md` -- som i Code Map

**Acceptance Criteria:**
- Given brevsiden, when den vises, then står «Last ned som Word» og «Last ned som PDF» som blå hovedknapper ved siden av hverandre, over «Nytt forslag»
- Given en PDF-nedlasting, when vinduet åpnes, then står `Filnavn: Soknad_<dato>.pdf` i det
- Given `uv run pytest -q`, `ruff check` og `ruff format --check`, when de kjøres, then består alle

## Implementation Notes

- Kodet av en subagent etter spec-en. 1 288 tester besto, og `ruff check` og `ruff format --check` var rene (kjørt på nytt i hovedøkten).
- fpdf2 2.9.0 tar med seg fonttools og pillow. Skriften (`NotoSans-Regular.ttf`, ca. 620 KB) og `OFL.txt` er hentet fra github.com/notofonts. PDF-en har bare tegnene som brukes, så filen er liten.
- `lag_pdf`: A4, 25 mm marg, `c_margin = 0` så teksten begynner ved margen, linjehøyde 5,5 mm og 4 mm luft mellom avsnittene. Forfatter, tittel, laget av og produsent er tomme.
- `.nedlasting` er nå en rad som brytes (`flex-wrap`), med én `.nedlasting-format`-blokk per format. En CSS-test i `test_nedlasting.py` sjekker nå `justify-content: center` i stedet for `align-items: center`. Den grønne knappen har ramme i `CanvasText` i høykontrast.
- Tabulator og andre kontrolltegn fjernes alt av `kontroller()`, så de når aldri PDF-en (sjekket i gjennomgangen).

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap, blind | At vinduet viser `.pdf`-filnavnet etter PDF-nedlasting, testes bare som kildetekst i `nedlasting.js` | medium | Stemmer. Repoet har ingen nettlesertester (issue #16, story 8.2), som for `bekreft.js` og `vente.js`. Prøves for hånd i PR-en → defer |
| 2 | edge-case | Word og PDF lastet ned samtidig: den andre forespørselen får ikke lagret formatet (`erstatt_soknad` feiler stille), så knappen er blå etter ny lasting | low | Stemmer bare hvis to nedlastinger går samtidig. Brukeren lukker vinduet før neste trykk, og rettingen er en ny gren → avvist |
| 3 | blind | Et ukjent format får Word-fil i ruten | false | Ruten slipper bare `docx` og `pdf` gjennom (`any(docx, pdf)`), og andre gir 404 (testet) |
| 4 | blind | Kommentaren over `MEDIETYPER` sier at den har rekkefølgen til knappene, men malen har egen liste | low | Stemmer. Direkte retting av kommentaren → patch |
| 5 | blind | `sett_lastet_ned` godtar hvilken som helst tekst | false | Bare ruten kaller den, med `format` fra `any(docx, pdf)`. Ingen vei gir en annen verdi |
| 6 | blind | Docstringen i `_vis_brev` omtaler `filnavn` som om den var en parameter | low | Stemmer. Direkte retting → patch |
| 7 | blind | «Med vennlig hilsen» og navnet kan havne på hver sin side i et langt brev | low | Stemmer i teorien, og Word-fila gjør det samme. Brevet er vanligvis én side, og rettingen er ny logikk → avvist |
| 8 | blind | Ingen PDF-test med kontrolltegn (tabulator, myke bindestreker) | false | `kontroller()` gjør tabulator og linjeskift om til mellomrom før brevet når `lag_pdf` (prøvd), og edge-case-laget kjørte myke bindestreker og usynlige tegn uten feil |
| 9 | blind | Ingen test med et langt ord uten mellomrom (URL, e-post) | false | Edge-case-laget kjørte en URL på 300 tegn: den ble brutt over linjer uten feil |
| 10 | blind | `test_fr30_pdf_har_ingen_markeringer` avhenger av hvordan fpdf2 skriver siden | low | fpdf2 er låst til 2.9.0, og en endring der vises i testen → avvist |
| 11 | blind | `/CreationDate` og dokument-ID er ikke fjernet | false | De sier ingenting om brukeren. Word-fila har også datoer |
| 12 | blind | Tom tittel gjør PDF-en dårligere for skjermlesere | low | Spec-en bestemmer tomme felt som i Word-fila. Rettingen ville endre spec-en → avvist |
| 13 | blind | Skriften leses på nytt ved hver nedlasting | low | Koster litt tid per nedlasting, uten feil. Rettingen er mellomlagring → avvist |
| 14 | blind | Arkitekturen sier fortsatt at skriften ikke er valgt | low | Stemmer (`arkitektur.md:342` og kopien i planene). Direkte retting → patch |
| 15 | blind | pillow og fonttools kommer med uten å være nevnt | low | Står i `uv.lock`. Ingen skade → avvist |
| 16 | blind | Rammen på 2 px i høykontrast gjør den grønne knappen større | false | `.hovedknapp` har alt `border: 2px` (`stil.css:630`), så størrelsen er lik |
| 17 | blind | Toppkommentaren i `nedlasting.js` er utdatert, og siste linje er for lang | low | Stemmer. Direkte retting → patch |
| 18 | blind | Linjeavstand og luft er ikke sammenlignet med Word-fila | low | Bare utseende. Kristine åpner PDF-en i PR-prøven → avvist |
| 19 | blind | Sprint-status, TO DO og notater er ikke med i diffen | false | Sprint-statusen ligger i `_bmad-output/` (ikke i git) og er oppdatert. Resten gjøres når storyen avsluttes |

## Design Notes

- `lastet_ned` som `frozenset` i stedet for to bool-felt: ett felt å nullstille, og nye formater trenger ingen ny kode i kjernen.
- Tegn som ikke finnes i skriften (for eksempel emoji), gir ingen feil i fpdf2, men vises ikke. KI-en skriver vanlig norsk tekst, så det godtas og nevnes i README under «Kjente begrensninger».

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine, i testmodus ved 375 og 1280 px: last ned Word, «Bli her», last ned PDF → begge grønne, vinduet viser `.pdf`. Åpne PDF-en: æøå, avsnitt, hilsen og navn. Samme i Korrektur. Høykontrast: grønne knapper har ramme.
