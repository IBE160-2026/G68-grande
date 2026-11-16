---
title: 'Story 6.1: Laste opp PDF'
type: 'feature'
created: '2026-11-16'
status: 'done'
baseline_commit: '57c5e3a77eb88e48a9762a6882a03aef8155ff10'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-6-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** På innleggingen kan studenten bare lime inn tekst. De fleste har CV-en som PDF og må kopiere teksten selv (FR-8, kriterium 5).

**Approach:** Hvert felt (CV, eget brev i Korrektur, annonse) får «Last opp PDF» ved siden av «Lim inn tekst». Valgt fil vises som filnavn med ✓ og søppelbøtte, og leses først når skjemaet sendes, bare i `adaptere/pdf_inn.py` med pypdf. Teksten og filnavnet lagres i økten som `Tekstfelt`. Testdataene får PDF-er lagret fra Word, og en tabellprøve viser om pypdf klarer tabeller.

## Boundaries & Constraints

**Always:** Bare `pdf_inn.py` importerer pypdf (`pypdf==6.21.4`). `kjerne/` leser aldri filer. PDF-teksten normaliseres i `pdf_inn.py` med NFKC, og U+00AD og usynlige tegn (U+200B–U+200D, U+2060, U+FEFF) fjernes, så telleregelen gir samme treff som for `.txt` (utsatt fra 2.1). Fil og tekst lagres bare i økten, aldri på disk, og logges aldri. Feltets kilde avgjøres av et skjult felt `<navn>_kilde` (`fil`/`tekst`): `fil` med ny fil leser fila, `fil` uten ny fil beholder `Tekstfelt` fra økten, `tekst` bruker tekstboksen. Det gjelder både «Sjekk CV-en min» og «Tilbake». `sett_inndata` sammenligner bare `.tekst`: samme tekst med nytt filnavn lagrer navnet uten å nullstille analysen (retro 2, A9). Alle tekster i `tekster.py`. Skriptet endrer bare skjemaet (AD-1). Ingen `style=`, ingen faste høyder, ingen `nowrap` i hele `stil.css` (finnes test): det lange navnet kuttes med `-webkit-line-clamp: 1` og `overflow-wrap: anywhere`. Hver test nevner FR-nummeret. Aldri det ekte API-et.

**Midlertidig til 6.2:** en fil pypdf ikke kan lese (eller som ikke er PDF) gir tom tekst, og feltet får feilen «tom». Ingen 5 MB-grense ennå.

**Never:** Ikke feilene for filtype, størrelse og uleselig PDF, 413-håndtereren eller `testdata/feil/` (6.2). Ikke OCR eller annen PDF-leser. Ikke endre telleregelen, `vask`, promptene eller KI-svarene i `testdata/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Velge fil | tomt CV-felt, velger `cv.pdf` | filnavnet med ✓ vises med en gang, fokus til søppelbøtta, status «CV lastet opp: cv.pdf». Ingen sjekk | – |
| Sjekk med PDF | testmodus, `cv.pdf` + `annonse.pdf` fra case 1 | samme case og samme treff som `.txt`, resultatsiden | – |
| Søppelbøtta på filnavnet | fil valgt eller lagret | feltet tomt, fokus til «Last opp PDF», status «CV-feltet er tømt», kilde `tekst` | – |
| Tilbake og inn igjen | PDF lagret | filnavnet vises fra økten. «Sjekk» uten ny fil bruker lagret tekst | – |
| Feil i et annet felt | PDF i CV, annonse tom | siden på nytt med filnavnet i CV og feilen på annonsen | som før |
| Ulesbar fil | `.docx` eller ødelagt PDF | tom tekst, feilen «tom» | ingen krasj (til 6.2) |
| Samme tekst, nytt navn | lagret `cv.txt`-tekst, laster opp `cv.pdf` med samme tekst | analysen beholdes, filnavnet lagres | – |
| Langt filnavn | 120 tegn uten mellomrom | kuttes med «…» på én linje, ingen rulling sidelengs ved 320 px, hele navnet i `title` | – |

**Beslutninger (Kristine, 2026-11-16):**
- Tekstboksene får en hjelpetekst under seg: «Høyst 15 000 tegn.» for CV og annonse, «Høyst 5 000 tegn.» for brevfeltet (tallene fra `MAKS_TEGN_TEKST`/`MAKS_TEGN_EGET_BREV_TEKST`). Den er koblet til tekstboksen med `aria-describedby` (sammen med feilteksten når den finnes), med `class="hjelpetekst"` som i skjemaene.
- Begge søppelbøttene (i tekstboksen og ved filnavnet) gir fokus til «Last opp PDF» i samme felt, som i UX.
- Én spec og én PR, selv om spec-en er over 1 600 tokens.

</frozen-after-approval>

## Code Map

- `backend/soknad/adaptere/pdf_inn.py` (ny) -- `les_pdf(innhold: bytes) -> str`: `PdfReader(BytesIO)`, `extract_text()` per side med `"\n"` mellom, normalisering som i Always. Alle unntak fra pypdf gir `""` (kommentar: feilene kommer i 6.2).
- `backend/pyproject.toml`, `uv.lock` -- `pypdf==6.21.4` (`uv add`).
- `backend/soknad/web/ruter.py:179-191` -- ny hjelper `_les_felt(navn, lagret_felt) -> Tekstfelt` etter regelen i Always. Filnavnet: bare delen etter siste `/` eller `\`. `request.files[f"{navn}_fil"]`. `sjekk_innlegging` får `.tekst`. `_vis_innlegging:456` sender `filnavn` per felt, og `tekst` er `""` for felt med filnavn.
- `backend/soknad/kjerne/okt.py:96` -- `sett_inndata`: sammenlign `.tekst`; er alle like, `replace` bare feltene (nye filnavn) uten nullstilling. Rett docstringen.
- `backend/soknad/web/tekster.py:100-138` -- `LAST_OPP_KNAPP = "Last opp PDF"`, `last_opp_skjermleser(felt)` («Last opp PDF, CV»), `lastet_opp_skjermleser(felt, filnavn)` («CV lastet opp: <filnavn>»), `PDF_TIPS`, `maks_tegn_hjelp(felt)` («Høyst 15 000 tegn.» / «Høyst 5 000 tegn.» for `eget_brev`, bruk `inndata.maks_tegn`).
- `backend/soknad/web/templates/innlegging.html:54-80` -- `enctype="multipart/form-data"`. `PDF_TIPS` over skjemaet (begge modusene). Tom tilstand: «Last opp PDF» (`hovedknapp last-opp`, `id="<navn>-last-opp"`, `aria-label`, `aria-describedby` ved feil) før «Lim inn tekst». Skjult `<input type="file" name="<navn>_fil" accept=".pdf" hidden>`, `<input type="hidden" name="<navn>_kilde">`. Ny `.filboks` (`file-chip`): `<span aria-hidden="true">✓</span>`, `.filnavn` med `title`, søppelbøtte med samme `aria-label`/`data-tomt` som i dag. Tre tilstander fra serveren: tom, tekst, fil. Under tekstboksen `<p class="hjelpetekst" id="<navn>-hjelp">` med `tekster.maks_tegn_hjelp(navn)`, og tekstboksen har `aria-describedby="<navn>-hjelp"` (pluss `<navn>-feil` ved feil).
- `backend/soknad/web/static/js/innlegging.js` -- «Last opp PDF» kaller `fil.click()`. `change` med fil: navnet inn, filboks vises, kilde `fil`, fokus til søppelbøtta, status via samme `ventende`-mønster. Søppelbøtta på filnavnet: `fil.value = ""`, kilde `tekst`. Begge søppelbøttene gir fokus til «Last opp PDF» (i dag «Lim inn tekst», testen ved `test_innlegging.py` endres). «Lim inn tekst» setter kilde `tekst`. `fokusIFeltet`: filboks → søppelbøtta, tekstboks → tekstboksen, ellers «Last opp PDF».
- `backend/soknad/web/static/css/stil.css:859-950` -- `.tom-tilstand` som rad med luft (`flex-wrap`), `.last-opp` overstyrer bredden til `.hovedknapp`, `.pdf-tips`, `.filboks` (`var(--success-tint)`, `var(--success)`, `var(--rounded-sm)`, søppelbøtta til høyre), `.filnavn` med line-clamp, `.last-opp:focus` som `.lim-inn:focus` (L940), og `.soppelbotte:focus`. I `forced-colors` (L1472): ramme i `CanvasText` på `.filboks`.
- `backend/testdata/case-1-utvikler/{cv,annonse,eget-brev}.pdf`, `case-2-okonomi/{cv,annonse}.pdf` (nye) -- lages av `backend/scripts/lag_testpdf.ps1` (ny): Word (COM) åpner hver `.txt` som UTF-8 og lagrer som PDF (format 17).
- Tester: `tests/adaptere/test_pdf_inn.py` (ny), `tests/test_testdata.py` (kriterium 5: per case gir `les_pdf(x.pdf)` samme `vask` og samme `tell_treff` med `nokkelord.json` som `x.txt`, og `finn_case` samme case), `tests/kjerne/test_okt.py` (A9), `tests/web/test_innlegging.py` (opplasting i begge modusene, beholdt fil, tilbake, `multipart`, tekstene, CSS, JS-strenger). Gjenbruk `tests/web/hjelpere.py` og eksisterende fixtures. Eksisterende tester for «Lim inn tekst» og søppelbøtta justeres bare der markupen endres.
- Ikke endre: `kjerne/telleregel.py`, `kjerne/testdata_match.py`, `adaptere/ki.py` (leser fortsatt `.txt`), `kjerne/inndata.py`, `prompts/`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/pyproject.toml`, `soknad/adaptere/pdf_inn.py`, `tests/adaptere/test_pdf_inn.py` -- pypdf, `les_pdf`, normalisering og tom tekst ved feil, testet med PDF-ene fra Word
- [x] `backend/scripts/lag_testpdf.ps1`, `backend/testdata/case-*/*.pdf`, `tests/test_testdata.py` -- PDF-ene og kriterium 5. Før normaliseringen: mål om Word-PDF-ene har NFD, U+00AD eller U+200B, og skriv det i Implementation Notes
- [x] `backend/soknad/kjerne/okt.py`, `tests/kjerne/test_okt.py` -- A9
- [x] `backend/soknad/web/ruter.py`, `tekster.py`, `templates/innlegging.html`, `static/js/innlegging.js`, `static/css/stil.css`, `tests/web/test_innlegging.py` -- opplastingen, filnavnet, tipset
- [x] Tabellprøven -- fiktiv CV med ferdighetene i en tabell (python-docx), lagret som PDF i Word, lest med `les_pdf`. PDF-en i `my-project/testkjoringer/6-1/`, resultatet i `my-project/testplan.md`. Feil rekkefølge → kjent begrensning i README, tabeller på kuttlisten i PRD-en og i beslutningsloggen med dato og grunn
- [x] `README.md` -- PDF-ene i testdataene og `lag_testpdf.ps1`

**Acceptance Criteria:**
- Given et tomt felt, when siden vises, then står «Last opp PDF» (aria-label «Last opp PDF, CV») før «Lim inn tekst», filvelgeren har `accept=".pdf"`, og PDF-tipset står over feltene i begge modusene
- Given et skjema med fil, when det sendes, then er `enctype` `multipart/form-data`, og teksten fra `pdf_inn.py` og filnavnet ligger i økten, ikke på disk
- Given hvert testcase, when `.pdf` og `.txt` sammenlignes, then gir de samme case og samme nøkkelordtreff
- Given en tekstboks, when den vises, then står «Høyst 15 000 tegn.» (brevfeltet «Høyst 5 000 tegn.») under den, koblet med `aria-describedby`, og søppelbøtta i tekstboksen gir fokus til «Last opp PDF»

## Implementation Notes

- **Unicode-målingen (før normaliseringen):** teksten pypdf leser fra alle fem Word-PDF-ene (case 1: cv, annonse, eget-brev; case 2: cv, annonse) er NFC og NFKC, og har ingen U+00AD, U+200B eller andre tegn i kategori Cf/Mn/Zs (utenom vanlig mellomrom). `vask(pdf) == vask(txt)` for alle fem. Normaliseringen i `pdf_inn.py` er altså ikke nødvendig for Word, men er der for Canva/Mac (ikke målt). Merk: bare å/é o.l. har NFD-oppdeling; æ og ø har ingen, så testen av NFD bruker å og é.
- **Tabellprøven:** riktig rekkefølge (rad for rad, celler fra venstre). Ingen kjent begrensning for tabeller, ingenting på kuttlisten i PRD-en eller i beslutningsloggen. Resultatet står i `my-project/testplan.md` (ny seksjon «Story 6.1»). `tabell-cv.docx` er ignorert av `*.docx` i `.gitignore`; PDF-en, skriptet og den leste teksten ligger i `my-project/testkjoringer/6-1/`.
- **Filnavn med `\`:** Werkzeug fjerner selv en `\` som ikke er escapet i `Content-Disposition` (`C:\Users\x\cv.pdf` blir `C:Usersxcv.pdf` før ruten ser den). Moderne nettlesere sender bare navnet, så det gjør ingenting i praksis. Splittingen er lagt i `ruter._uten_mappe` og testet direkte; `/` testes gjennom skjemaet.
- **`sett_inndata`:** returnerer fortsatt samme objekt (`is soknad`) når feltene er helt like (eksisterende tester), og `replace` med bare feltene når bare filnavnet er endret.
- **Markup:** begge søppelbøttene har klassen `soppelbotte` (skilt på foreldre-elementet `.filboks`/`.limeboks-topp`). Søppelbøtta ved filnavnet får `aria-describedby="<navn>-feil"` ved feil, siden lenken i feilboksen gir den fokus. Tekstboksens `aria-describedby` er `"<navn>-feil <navn>-hjelp"` ved feil (feilen først), ellers `"<navn>-hjelp"`. Det skjulte `<navn>_kilde` har `autocomplete="off"` så Firefox ikke henter fram en gammel kilde ved ny lasting.
- **Etter agenten (kontrollen i steg 3):** de usynlige tegnene og de kombinerende aksentene sto som rå tegn i `pdf_inn.py` og `test_pdf_inn.py`. De er byttet ut med `­`, `​` osv., så koden kan leses. 1 100 tester består, ruff uten feil.
- **README:** i tillegg til PDF-ene og skriptet fikk «Kjente begrensninger» et punkt om Canva-PDF og skannet PDF (fra epic-konteksten: «README skal si det under kjente begrensninger»).

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse | Rute |
|---|-------|------|---------|-------------|------|
| 1 | verification-gap | Ingen test låser `class="kilde"` og `class="filvelger"`, som skriptet leter etter. Et nytt klassenavn gjør at opplastingen stopper uten at en test feiler | medium | Sjekket: testene finner feltene på `name`, og JS-testene ser bare på teksten i skriptet | patch |
| 2 | edge-case, blind | Werkzeug legger opplastinger over 500 KB i en midlertidig fil på disk (`SpooledTemporaryFile`, `formparser.py:59`), i strid med NFR-4 og docstringen «skrives aldri til disk» | medium | Sjekket i `.venv/.../werkzeug/formparser.py`: `max_size = 500 KB`, og så `SpooledTemporaryFile`. Flask bruker `Request._get_file_stream` | patch |
| 3 | edge-case, blind | Over 16 MB gir Werkzeugs rå 413-side | medium | Ekte, men 413-håndtereren er utelatt fra 6.1 i den godkjente intensjonen (Never) og ligger i 6.2. Fantes også før (utsatt fra 4.3.2) | reject (6.2) |
| 4 | edge-case, blind | Ingen grense for antall sider eller tekstmengde fra pypdf, og teksten lagres i økten før tegnsjekken | medium | Ekte: en 16 MB PDF leses helt, og teksten lagres før `sjekk_innlegging`. Lagringen før sjekken fantes for tekst før (4.3.2). Grensene for filer er 6.2 | defer |
| 5 | edge-case | «For lang» på et felt med fil ber brukeren korte ned tekst hen ikke ser | low | Ekte, men sjelden (over 15 000 tegn i en PDF), og en egen tekst er Kristines valg. Tas opp i 6.2 | reject |
| 6 | edge-case | En gammel fane med `kilde=fil` sender teksten en annen fane har lagret | low | Sjelden, og løsningen trenger et nytt skjult felt og en sammenligning | reject |
| 7 | edge-case | `lag_testpdf.ps1` stopper midt i hvis en PDF er låst | low | Skript for utviklere. Kjøres på nytt | reject |
| 8 | blind | Den midlertidige feilen «tom» for en fil som ikke kan leses, står ikke i README, og det finnes ingen test for kryptert PDF | low | Varer bare til 6.2, står i spec-en. Ødelagte filer er testet | reject |
| 9 | blind | Brukeren kan ikke se eller rette teksten fra PDF-en | low | UX bestemmer at et felt med fil bare viser filnavnet | reject |
| 10 | blind | Hjelpeteksten om tegngrensen er skjult når feltet har en fil | false | Kristines beslutning: hjelpeteksten står under tekstboksen | reject |
| 11 | blind | Skjermlesere får ikke filnavnet når siden lastes på nytt | low | Filnavnet står som vanlig tekst i feltet og leses i lesemodus. Statusmeldingen gjelder bare når fila velges, som i UX | reject |
| 12 | blind | `accept` mangler `application/pdf` | low | Spec og UX sier `accept=".pdf"`, og det virker i moderne nettlesere | reject |
| 13 | blind | Normaliseringen gjelder bare PDF, ikke innlimt tekst. NFKC endrer noen tegn | low | Spec-en valgte `pdf_inn.py` (det utsatte punktet tillot det). Innlimt tekst er uendret fra før | reject |
| 14 | blind | README og testplanen sier hverandre imot om Canva | false | README bygger på prøven 7. november (kolonner fra Canva). Testplanen sier bare at Unicode i Canva ikke er målt | reject |
| 15 | blind | Docstringen i `test_fr8_pdf_og_txt_gir_samme_nokkelordtreff` lover mer enn testen sjekker | low | Ekte. Rettes ved å endre docstringen | patch |
| 16 | blind | `test_fr8_avkuttet_pdf_gir_tom_tekst_eller_teksten` sjekker bare at den ikke krasjer | low | Ekte. Rettes ved å gi testen et navn som sier at den ikke krasjer | patch |
| 17 | blind | Ingen test av en PDF med tekst over tegngrensen | medium | Ekte hull: PDF over 15 000 eller 5 000 tegn bør gi «for lang» med filnavnet igjen | patch |
| 18 | blind | Skriptet har en fast liste med navn, testen krever en PDF for hver `.txt`, og Word-PDF-er blir ikke like fra kjøring til kjøring | low | Bare for utviklere. README sier at skriptet kjøres på nytt når en `.txt` endres | reject |
| 19 | blind | Filnavnet blir ikke ryddet, og `_uten_mappe("mappe/")` gir `"mappe/"` | low | Filnavnet escapes ved visning og bare vises. Det skader ikke | reject |
| 20 | blind | PDF-tipset nevner bare CV-en | low | Teksten er ordrett fra epics og UX (Kristines ordlyd) | reject |
| 21 | blind | Notat til refleksjonsrapporten og avkrysning i todo mangler | low | Prosess, ikke kode. Gjøres ved slutten av økten | reject |

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check . && uv run ruff format --check .` -- expected: ingen feil

**Manual checks (Kristine i nettleseren):**
- Last opp `cv.pdf` og `annonse.pdf` fra case 1 i testmodus: filnavnet med ✓ med en gang, fokus på søppelbøtta, resultatsiden som med innlimt tekst. Prøv også i Korrektur med `eget-brev.pdf`.
- Søppelbøtta på filnavnet: tomt felt, fokusring på «Last opp PDF» (også etter museklikk).
- «Tilbake» og inn igjen: filnavnet står der fortsatt.
- Et langt filnavn ved 320 px: kuttes med «…», ingen rulling sidelengs. Høykontrast (Windows): stripa har ramme.
- Din egen Canva-CV med testmodus av er ikke nødvendig. Vil du, kan du laste den opp med testmodus på og se at du får feilen om testdata (ikke krasj).
