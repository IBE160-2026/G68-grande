# Epic 6 Context: Laste opp CV og annonse som PDF

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Brukeren kan laste opp en PDF i stedet for å lime inn tekst i alle feltene på innleggingen (CV, annonse og, i Korrektur, eget brev). Brukeren får en tydelig melding ved feil filtype, for stor fil og PDF som ikke kan leses (for eksempel skannet), og ser PDF-tipset over feltene. Epicen er viktig fordi de fleste har CV-en som PDF, og fordi suksesskriterium 5 (PDF og innlimt tekst gir samme treff for CV, annonse og eget brev) og 10 (riktig feilmelding for feil filtype og uleselig PDF) vises her. PDF-opplasting er punkt 5 på nødlisten: kuttes den, virker nettsiden bare med innlimt tekst, og kriterium 5 må endres.

## Stories

- Story 6.1: Laste opp PDF
- Story 6.2: Feilmeldinger for filer

## Requirements & Constraints

- **Innleggingsfeltene:** i hvert felt kan brukeren enten laste opp en PDF eller lime inn tekst, i begge modusene. Fila sjekkes ikke når den velges, bare når brukeren trykker «Sjekk CV-en min». Søppelbøtta fjerner fila uten bekreftelse, og feltet går tilbake til tom tilstand (angre).
- **Lagring:** teksten fra PDF-en og filnavnet lagres bare i økten i minnet, aldri på disk. Ingenting lagres mellom øktene.
- **Feilene:** feil filtype, fil over 5 MB, PDF med under 50 bokstaver (uleselig) og hele forespørselen over 16 MB. Alle feilene vises samtidig, i rekkefølgen tom → feil filtype → for stor → uleselig → ikke testdata per felt, og felt uten feil beholdes. Feilene virker også i testmodus. Grensene 5 MB, 16 MB og 50 bokstaver ligger i `innstillinger.py`.
- **Testmodus:** PDF og `.txt` fra samme testcase skal gjenkjennes som samme case, og `cv.pdf` og `cv.txt` skal gi samme nøkkelordtreff (kriterium 5). Hvert testcase får `cv.pdf` og `annonse.pdf`, og case 1 også `eget-brev.pdf`, med samme tekst som `.txt`-filene, lagret fra Word. `testdata/feil/` får `skannet.pdf` (bilde uten tekst) og `feil-type.docx`.
- **Grensen på 50 bokstaver** prøves med `skannet.pdf` og PDF-ene i testdataene, og justeres i `innstillinger.py` hvis den ikke skiller dem.
- **Tabellprøven:** en fiktiv CV med en tabell (for eksempel ferdighetene), laget i Word og lagret som PDF, leses med pypdf. Resultatet står i PR-en og i testplanen. Kommer teksten i feil rekkefølge, blir det en kjent begrensning i README, og tabeller settes på kuttlisten i PRD-en, med dato og grunn i beslutningsloggen. Kolonner er alt prøvd (7. november): CV fra Word med to kolonner leses riktig, og fra Canva kommer all teksten, men overskriftene havner på feil sted. Reserven er innlimt tekst, og README skal si det under kjente begrensninger.
- **README** oppdateres når noe endres i hvordan nettsiden testes eller hvor testdataene ligger (PDF-filene og `testdata/feil/`).

## Technical Decisions

- **PDF inn bare i `adaptere/pdf_inn.py`**, med pypdf og vanlig `extract_text()`. `kjerne/` importerer aldri pypdf og leser aldri filer.
- **Feiltypene** `feil_filtype`, `for_stor` og `uleselig` hører til den lukkede listen i `kjerne/feil.py` og returneres som `InndataFeil(felt, type)` i en liste, ikke som unntak. Tekstene ligger bare i `web/tekster.py`. En egen 413-håndterer viser feilboksen med `for_stor` når hele forespørselen er over `MAX_CONTENT_LENGTH`. Etter en feil vises samme side på nytt uten redirect, med det som allerede er lagret.
- **Rekkefølgen med tegngrensen:** feltene godtar høyst 15 000 tegn (brevfeltet i Korrektur 5 000) med feilen `for_lang`, og i dag er rekkefølgen tom → for lang → ikke testdata. Hvor `for_lang` står i forhold til de nye filfeilene, er ikke bestemt i planene.
- **Utsatt hit fra tidligere epics:**
  - Filnavnet gjør feltet «endret» (retro 2): `sett_inndata` sammenligner hele feltet, så et filnavn kan få «Tilbake» til å nullstille analysen selv om ingenting er endret. Rettes i 6.1.
  - Tekst fra PDF kan ha æøå som to tegn (NFD), myke bindestreker, usynlige mellomrom eller orddeling ved linjeslutt, og da gir telleregelen ikke treff (testdata-vasken bruker NFKC, telleregelen ingenting). Avgjøres i 6.1 ved å sjekke `unicodedata.is_normalized("NFC", tekst)` og se etter U+00AD og U+200B i tekst fra CV-er fra Word, Canva og Mac. Løses i `pdf_inn.py` eller i vasken i `telleregel.py`.
  - Teksten lagres med `sett_inndata` før tegnsjekken, og over 16 MB gir i dag Flasks rå 413-side. Kan tas sammen med 413-håndtereren i 6.2.
- **Korrektur og PDF:** kontrollen av Korrektur-svaret ser bort fra mellomrom, linjeskift og usynlige formattegn, og i testmodus sjekkes svaret mot casets egen `eget-brev.txt`, ikke mot den opplastede teksten. Begge deler ble gjort i retro 5 med tanke på tekst fra PDF.
- **`.gitignore`:** regelen `*.docx` skjuler `feil-type.docx`, så den trenger unntaket `!backend/testdata/feil/feil-type.docx`, og en test sjekker at fila finnes, så CI feiler hvis den mangler på GitHub.
- **Personvern og logg:** loggen viser aldri CV, annonse eller brev, heller ikke filinnhold.
- **Tester:** dekker feil filtype, for stor fil, uleselig PDF og 413. Hver testfil og testfunksjon nevner FR-nummeret (FR-8, FR-10, FR-11, FR-12, FR-13, FR-34). Felles hjelpere i `tests/web/hjelpere.py` brukes og kopieres ikke. Aldri det ekte API-et.

## UX & Interaction Patterns

- **Tom tilstand:** «Last opp PDF» (hovedknapp) ved siden av «Lim inn tekst» (sekundær). Filvelgeren har `accept=".pdf"` og skal virke godt på mobil. Skjermlesere hører feltnavnet med, for eksempel «Last opp PDF, CV», mens den synlige teksten er bare «Last opp PDF».
- **Fil valgt:** filnavnet vises med en gang som `file-chip` (grønn stripe med ✓, langt navn kuttes med «…», søppelbøtta 🗑️ til høyre). Fokus går til søppelbøtta, og skjermlesere hører «CV lastet opp: <filnavn>». ✓ er pynt og skjules for skjermlesere.
- **Søppelbøtta:** uten ramme og bakgrunn, trykkflate minst 24 × 24 px, med fokusring og skjermlesertekst «Tøm CV-feltet», «Tøm brevfeltet» eller «Tøm annonsefeltet». Etter tømming går fokus til «Last opp PDF» i samme felt, og skjermlesere hører for eksempel «CV-feltet er tømt».
- **PDF-tipset** står over feltene i begge modusene: «Tips: PDF lagret fra Word leses best. Er CV-en laget i Canva eller et lignende program, kan teksten komme i feil rekkefølge. Lim den da heller inn.»
- **Feiltekstene** (feltnavnet byttes ut med «CV», «Ditt søknadsbrev» eller «Stillingsannonse»): «CV: Feil filtype, prøv PDF.», «CV: Filen er for stor. Den kan være på høyst 5 MB.» og «CV: Vi klarer ikke å lese teksten i PDF-en. Den kan være skannet. Lim inn teksten i stedet.» De står i feilboksen øverst («Noe må fikses før du kan gå videre:», én lenke per feil, fokus dit) og med rødt under feltnavnet, koblet med `aria-describedby`, og feltet får rød ramme.
- **Åpent punkt:** hjelpeteksten om tegngrensen ved tekstboksene (15 000 for CV og annonse, 5 000 for brevet) er anbefalt tatt med i 6.1, men Kristine har ikke bestemt det.
- **Kjente fallgruver i CSS** (testene tegner ikke siden, så bare nettleseren finner dem): alt som får fokus fra et skript (her søppelbøtta etter filvalg og «Last opp PDF» etter tømming), trenger også en `:focus`-regel, siden `:focus-visible` ikke vises etter museklikk. Overskrifter med `tabindex="-1"` skal ikke vise ring. I høykontrastmodus (`forced-colors: active`) forsvinner bakgrunner, så den grønne `file-chip` trenger ramme i `CanvasText`, med sjekk i CSS-testen. Hver ny SVG trenger høyde i CSS. Ingen `style=`, ingen faste høyder og ingen `nowrap` (også det lange filnavnet må kuttes uten å gi rulling sidelengs ved 320 og 375 px).

## Cross-Story Dependencies

- Epic 2 (innleggingssiden og feilboksen) og Epic 5 (brevfeltet) er ferdige. Epic 6 legger fil til i alle tre feltene.
- 6.1 lager opplastingen, tipset, lesingen i `pdf_inn.py`, PDF-ene i testdataene, testen av kriterium 5 og tabellprøven, og retter de to utsatte punktene (filnavnet gjør feltet «endret», og Unicode i tekst fra PDF).
- 6.2 trenger 6.1. Den legger til feilene for filer, 413-håndtereren, `testdata/feil/` med unntaket i `.gitignore` og prøven av grensen på 50 bokstaver.
- Kristine prøver i nettleseren og kommenterer PR-en.
- Mot senere epics: story 8.1 (README for sensor) tar med de kjente begrensningene for PDF (Canva og eventuelt tabeller).
