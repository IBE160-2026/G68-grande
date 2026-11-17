---
title: 'Story 6.2: Feilmeldinger for filer'
type: 'feature'
created: '2026-11-16'
status: 'done'
baseline_commit: '9ae7a6af6a02b2150bf9b6305c33b83dbf22fd54'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-6-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** En fil som ikke er PDF, en skannet PDF eller en ødelagt fil gir i dag bare «Fyll inn feltet» (midlertidig fra 6.1), og en forespørsel over 16 MB gir Werkzeugs rå 413-side. Brukeren vet ikke hva som er galt (FR-10, FR-11, FR-12, kriterium 10).

**Approach:** Ved «Sjekk CV-en min» sjekkes hver ny fil: feil filtype, over 5 MB, og under 50 bokstaver fra pypdf (uleselig). Feilene blir `InndataFeil` i samme liste som de andre, med tekstene fra UX, og vises samtidig. En egen 413-håndterer viser innleggingen med feilboksen. `testdata/feil/` får `skannet.pdf` og `feil-type.docx`.

## Boundaries & Constraints

**Always:** Rekkefølge per felt: tom → feil_filtype → for_stor → uleselig → for_lang → ikke_testdata, høyst én feil per felt. `for_lang` står etter filfeilene, siden den trenger lesbar tekst. Grensene `MAKS_FILSTORRELSE` (5 MB), `MAKS_FORESPORSEL` (16 MB, finnes) og `MIN_BOKSTAVER_PDF` (50) i `innstillinger.py`. Reglene i `kjerne/inndata.py`, som bare får filnavn, bytes og tekst og aldri leser filer selv. pypdf bare i `pdf_inn.py`. Feil filtype: navnet slutter ikke på `.pdf` (uansett store/små bokstaver), eller `%PDF-` står ikke i de første 1 024 bytene. Filer med feil type eller over 5 MB leses ikke med pypdf. Alt som pypdf ikke klarer, gir under 50 bokstaver og dermed `uleselig`. Bare en ny fil sjekkes. En fil som er lagret i økten fra før, har alt passert. Feilene virker også i testmodus. Etter en feil vises siden på nytt uten redirect, og felt uten feil beholdes. Fil og tekst aldri på disk og aldri i loggen. Alle tekster i `tekster.py`. Hver test nevner FR-nummeret. Aldri det ekte API-et.

**Never:** Ingen sjekk i nettleseren når fila velges (UX: bare ved «Sjekk»). Ikke OCR. Ikke endre telleregelen, `vask`, promptene eller KI-svarene. Ikke grense for antall sider.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Feil filtype | `feil-type.docx` i CV | «CV: Feil filtype, prøv PDF.» | feltet blir tomt |
| Omdøpt fil | `.docx` omdøpt til `cv.pdf` | `feil_filtype` (ikke `%PDF-`) | – |
| For stor fil | PDF på 5 MB + 1 byte | «CV: Filen er for stor. Den kan være på høyst 5 MB.», fila leses ikke | – |
| Skannet PDF | `skannet.pdf` | «CV: Vi klarer ikke å lese teksten i PDF-en. Den kan være skannet. Lim inn teksten i stedet.» | – |
| Ødelagt PDF | `%PDF-` + søppel | `uleselig`, ingen krasj | – |
| Flere feil | `.docx` i CV, tom annonse | begge i feilboksen, i feltrekkefølgen | – |
| Testmodus | skannet PDF i CV, testannonse | `uleselig` på CV, ingen `ikke_testdata` på CV | – |
| Over 16 MB | hele forespørselen > `MAX_CONTENT_LENGTH` | innleggingen med «Filene er for store. Hver fil kan være på høyst 5 MB.», status 413, det som var lagret fra før står | ingen rå 413-side |
| 413 på andre sider | over 16 MB til f.eks. `/logg-inn` | Werkzeugs vanlige 413 | uendret |

**Beslutninger (Kristine, 2026-11-16):**
- Etter en filfeil er feltet tomt («Last opp PDF» og «Lim inn tekst») med den røde feilteksten. Den avviste fila lagres ikke i økten (feltet lagres som tomt `Tekstfelt`).
- Over 16 MB: «Filene er for store. Hver fil kan være på høyst 5 MB.» i feilboksen, uten feltnavn og uten lenke.
- «For lang» for en PDF beholder dagens tekst. Ingen ny feiltype.
- Én spec og én PR, selv om spec-en er over 1 600 tokens.

</frozen-after-approval>

## Code Map

- `backend/soknad/innstillinger.py` -- `MAKS_FILSTORRELSE = 5 * 1024 * 1024`, `MIN_BOKSTAVER_PDF = 50`, ved `MAKS_FORESPORSEL`.
- `backend/soknad/kjerne/feil.py` -- `FEIL_FILTYPE = "feil_filtype"`, `FOR_STOR = "for_stor"`, `ULESELIG = "uleselig"` i `FeilType`.
- `backend/soknad/kjerne/inndata.py` -- ny `sjekk_fil(filnavn: str, innhold: bytes) -> FeilType | None` (filtype, så størrelse) og `er_uleselig(tekst: str) -> bool` (`sum(t.isalpha() for t in tekst) < MIN_BOKSTAVER_PDF`). `sjekk_innlegging` får `filfeil: list[InndataFeil] = ()`: et felt med filfeil får den feilen og hoppes over i tom/for_lang og i testdatasjekken. Rett docstringen (rekkefølgen).
- `backend/soknad/adaptere/pdf_inn.py` -- `les_pdf` gir fortsatt `""` ved unntak. Fjern «midlertidig/6.2»-kommentarene, si at `""` blir `uleselig`.
- `backend/soknad/web/ruter.py:460-475` -- `_les_felt` returnerer `(Tekstfelt, InndataFeil | None)`: ny fil → `sjekk_fil`, ellers `les_pdf` og `er_uleselig`. Ved feil et tomt `Tekstfelt()`. `innlegging()` (L185-205) samler filfeilene og sender dem til `sjekk_innlegging`. Ny `@web.app_errorhandler(413)`: bare for `request.endpoint == "web.innlegging"` vises `_vis_innlegging(gjeldende_soknad(), feil=[InndataFeil(None, FeilType.FOR_STOR)])` med status 413, ellers returneres feilen. `_vis_innlegging` (L483) skiller ut feil med `felt=None` som `skjemafeil`.
- `backend/soknad/web/tekster.py:321-363` -- de ni tekstene (`cv`, `eget_brev`, `annonse` × tre typer) med feltnavnet først, `5 MB` fra `MAKS_FILSTORRELSE`, og `(None, FOR_STOR)`.
- `backend/soknad/web/templates/innlegging.html:29-36` -- `skjemafeil` som `<li>` uten lenke i samme feilboks, før feltfeilene.
- `backend/scripts/lag_feilfiler.ps1` (ny) -- som `lag_testpdf.ps1`: System.Drawing tegner CV-teksten fra case 1 som bilde (PNG i temp), Word setter bildet inn og lagrer `testdata/feil/skannet.pdf` (format 17). Word åpner `case-1-utvikler/cv.txt` og lagrer `testdata/feil/feil-type.docx` (format 16). Temp-fila slettes.
- `.gitignore:84` -- `!backend/testdata/feil/feil-type.docx` etter `*.docx`.
- `README.md:76-80, 128` -- `testdata/feil/` og `lag_feilfiler.ps1`. Fjern «midlertidig» om skannet PDF i «Kjente begrensninger» hvis det står.
- Tester: `tests/kjerne/test_inndata.py` (`sjekk_fil`, `er_uleselig`, rekkefølgen med `filfeil`), `tests/adaptere/test_pdf_inn.py` (`skannet.pdf` < 50 bokstaver, alle testdata-PDF-ene ≥ 50), `tests/test_testdata.py` (filene i `feil/` finnes, `feil/` er ikke et case), `tests/web/test_innlegging.py` (hver feil i begge modusene og i testmodus, flere feil, felt uten feil beholdes, 413 med liten `MAX_CONTENT_LENGTH` i `test_config`, 413 på en annen side). Bytt testene for den midlertidige «tom»-feilen fra 6.1. Gjenbruk `tests/web/hjelpere.py`.
- Ikke endre: `kjerne/telleregel.py`, `kjerne/testdata_match.py`, `adaptere/ki.py` (leser bare `case-*`), `innlegging.js`, `stil.css` (feilmarkeringen finnes).

## Tasks & Acceptance

**Execution:**
- [x] `innstillinger.py`, `kjerne/feil.py`, `kjerne/inndata.py`, `tests/kjerne/test_inndata.py` -- grensene, typene, `sjekk_fil`, `er_uleselig`, `filfeil` i `sjekk_innlegging`
- [x] `scripts/lag_feilfiler.ps1`, `testdata/feil/*`, `.gitignore`, `tests/test_testdata.py`, `tests/adaptere/test_pdf_inn.py` -- feilfilene og prøven av 50 bokstaver. Mål bokstavene i hver PDF og skriv tallene i Implementation Notes. Skiller ikke 50 dem, juster i `innstillinger.py`
- [x] `adaptere/pdf_inn.py`, `web/ruter.py`, `web/tekster.py`, `templates/innlegging.html`, `tests/web/test_innlegging.py` -- feilene på siden og 413-håndtereren
- [x] 413 med den ekte utviklingsserveren -- start `flask run`, send over 16 MB (Python `urllib`) til `/innlegging` innlogget, og se at svaret er siden med feilboksen, ikke at forbindelsen brytes. Brytes den, les og kast resten av `wsgi.input` i håndtereren (uten å lagre). Skriv resultatet i Implementation Notes
- [x] `README.md` -- `testdata/feil/` og skriptet

**Acceptance Criteria:**
- Given hvert felt i begge modusene, when en fil med feil type, over 5 MB eller uleselig sendes, then står UX-teksten med feltnavnet i feilboksen (med lenke) og under feltet, koblet med `aria-describedby`
- Given `testdata/feil/feil-type.docx`, when testene kjøres på GitHub, then finnes fila (unntaket i `.gitignore` virker)
- Given `skannet.pdf` og alle PDF-ene i `testdata/case-*`, when bokstavene telles, then er bare `skannet.pdf` under `MIN_BOKSTAVER_PDF`

## Implementation Notes

- **Bokstaver per PDF (målt 16. november 2026 med `les_pdf` og `isalpha`):** `feil/skannet.pdf` 0, `case-1-utvikler/annonse.pdf` 896, `case-1-utvikler/cv.pdf` 993, `case-1-utvikler/eget-brev.pdf` 952, `case-2-okonomi/annonse.pdf` 952, `case-2-okonomi/cv.pdf` 1 038. 50 skiller dem godt, så `MIN_BOKSTAVER_PDF` er beholdt. `skannet.pdf` har én side med ett bilde (1240 × 1754) og ingen tekst.
- **413 med den ekte utviklingsserveren:** `flask --app soknad run --port 5077`, innlogget med testbrukeren, Full generering, så `POST /innlegging` med `cv_fil` på 17 MB fra Python `urllib`. Svaret var status 413 med innleggingen og feilboksen («Filene er for store. Hver fil kan være på høyst 5 MB.»), og forbindelsen ble ikke brutt. Derfor leses ikke `wsgi.input` i håndtereren. Prøvd bare med `urllib` på Windows, ikke i en nettleser (det er Kristines manuelle sjekk).
- **`lag_feilfiler.ps1`:** Word hang i `SaveAs2` når stien kom rett fra `Join-Path` (en PowerShell-streng), men ikke med en vanlig .NET-streng. Stiene er derfor `[string]`, med en kommentar i skriptet.
- **Filfeil ved «Tilbake»:** `_les_felt` sjekker fila også ved «Tilbake» (som i 6.1, der fila ble lest begge gangene). En avvist fil gir da et tomt felt i økten, men ingen feilmelding, siden «Tilbake» ikke sjekker feltene.
- **413-håndtereren** setter `Cache-Control: no-store` selv, fordi feilen kastes inne i `login_required` og svaret derfor ikke går gjennom den. Er brukeren ikke logget inn, gis Werkzeugs vanlige 413.
- **Feiltekstene for filer** lages i en løkke over `tekster.INNLEGGINGSFELT`, så de ni tekstene har samme feltnavn som resten av siden.
- `tests/web/test_samtykke.py`: den falske `sjekk_innlegging` tar nå også `filfeil`.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse | Rute |
|---|-------|------|---------|-------------|------|
| 1 | edge-case | Innlimt tekst over Flasks `MAX_FORM_MEMORY_SIZE` (500 KB) gir 413 uten fil, og da står «Filene er for store» | low | Sjekket: `MAX_FORM_MEMORY_SIZE` er 500 000. Før 6.2 ga det Werkzeugs rå 413-side. 500 KB er over 30 ganger tegngrensen, og en egen tekst trenger ny gren og ny ordlyd | reject |
| 2 | edge-case | En ekte PDF uten `.pdf` i navnet eller med mellomrom bak navnet avvises | false | Spec-en bestemmer at navnet må slutte på `.pdf`. Nettlesere sender ikke mellomrom bak filnavnet | reject |
| 3 | edge-case | En kryptert PDF får teksten «Den kan være skannet» | low | Ekte, men sjelden, og rådet («lim inn teksten») virker likevel. Egen feiltype er ny ordlyd | reject |
| 4 | edge-case, verification-gap | Konstanten `DOCX` i `test_innlegging.py:810` brukes ikke lenger | low | Sjekket med grep: bare definisjonen er igjen | patch |
| 5 | blind | Docstringen i `sjekk_innlegging` sier tom → feil_filtype, men koden tar filfeil først | low | Et felt med filfeil har alltid tom tekst, så rekkefølgen er riktig, men docstringen kan leses som en motsigelse | patch |
| 6 | blind | «Tilbake» med en avvist fil lagrer feltet tomt uten melding | low | Følger Kristines beslutning (avvist fil lagres ikke), og «Tilbake» sjekker aldri feltene. Brukeren ser det tomme feltet når hen kommer tilbake | reject |
| 7 | blind | 413-håndtereren ser bort fra «Tilbake» og fra sjekken av opptatt | low | Skjemaet kan ikke leses ved 413, så knappen er ukjent. Opptatt krever to faner og en fil over 16 MB samtidig | reject |
| 8 | blind | Ingen test av grenen uten innlogging, 413 i Korrektur eller 16 MB på appen | low | `login_required` stopper før skjemaet leses, så grenen er et vern. 16 MB er testet i `test_app.py:43` | reject |
| 9 | blind | `test_fr10_feil_er_ikke_et_testcase` beviser ingenting, siden `CASER` selv er laget med `glob("case-*")` | low | Sjekket i `test_testdata.py:473-478`: påstandene er alltid sanne | patch |
| 10 | blind | `test_fr10_fr11_feilfilene_finnes` krever nøyaktig to filer, så en låsefil fra Word feiler lokalt | low | Sjekket i `test_testdata.py:467` | patch |
| 11 | blind | `lag_feilfiler.ps1` gjør om bare to av stiene til `[string]` | low | Skriptet er kjørt og virket. Bare for utviklere | reject |
| 12 | blind | `er_uleselig` teller bokstaver, så en PDF med ødelagt skrift kan gi tull som passerer | low | Ekte grense i regelen fra arkitekturen (AD-11). Ingen annen PDF-leser eller OCR (Never) | reject |
| 13 | blind | Prosessfilene (kopi i `my-project/`, sprint-status, notater) mangler | low | Prosess, gjøres ved slutten av økten | reject |
| 14 | blind | Navnet på den avviste fila vises ikke | false | Kristines beslutning: feltet blir tomt | reject |
| 15 | blind | De to feilene for «for stor» ser ulike ut, og ingen sjekk av størrelsen i nettleseren | false | Kristine valgte teksten for 16 MB. UX: ingen sjekk når fila velges | reject |
| 16 | blind | Testmodulen leser store filer ved import | low | Mangler filene, feiler testene likevel tydelig i CI | reject |
| 17 | blind | `MAKS_FILSTORRELSE_TEKST` runder ned | low | Grensen er hele 5 MB | reject |

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check . && uv run ruff format --check .` -- expected: ingen feil

**Manual checks (Kristine i nettleseren):**
- Last opp `testdata/feil/feil-type.docx` (velg «Alle filer» i filvelgeren), `skannet.pdf` og en PDF over 5 MB i hvert sitt felt, og trykk «Sjekk CV-en min»: tre feil samtidig, lenkene gir fokus til feltet.
- Gjør det i testmodus også.
- En fil over 16 MB: siden med feilboksen, ikke en hvit feilside.
