# Story 6.2: Feilmeldinger for filer

## 2026-11-17 kl. 07:16 — Kristine

### Oppgave
Bygge story 6.2 med `bmad-build`: tydelige feilmeldinger når en fil ikke kan brukes (feil filtype, for stor fil, skannet PDF), og en egen side i stedet for den rå 413-siden når alt til sammen er over 16 MB (FR-10, FR-11, FR-12, kriterium 10).

### Plan
- Spec: [spec-6-2-feilmeldinger-for-filer.md](../../my-project/9-koding/spec-6-2-feilmeldinger-for-filer.md) (kopi av `_bmad-output/implementation-artifacts/spec-6-2-feilmeldinger-for-filer.md`).
- Kristines beslutninger: et felt med en avvist fil blir tomt med feilteksten. Over 16 MB: «Filene er for store. Hver fil kan være på høyst 5 MB.». «For lang» for en PDF beholder dagens tekst. Én spec og én PR, selv om spec-en er ca. 2 800 tokens.
- Egen gren `story-6-2-feilmeldinger-for-filer`. En agent skrev koden, tre agenter gikk gjennom den (blind, edge-case, verification-gap), og agenten rettet fire funn.

### Resultat
- Commit `af6402c` på grenen `story-6-2-feilmeldinger-for-filer`. Ikke pushet, ingen PR ennå.
- `kjerne/inndata.py`: `sjekk_fil` (filtype: navnet slutter på `.pdf` og `%PDF-` i de første 1 024 bytene, så 5 MB) og `er_uleselig` (under 50 bokstaver). Filfeilene går inn i `sjekk_innlegging`, og rekkefølgen er tom → feil_filtype → for_stor → uleselig → for_lang → ikke_testdata. Grensene `MAKS_FILSTORRELSE` og `MIN_BOKSTAVER_PDF` ligger i `innstillinger.py`.
- `web/ruter.py`: `_les_felt` sjekker hver ny fil, og en 413-håndterer viser innleggingen med feilboksen (bare på innleggingen). `tekster.py` har de ni tekstene med feltnavnet og teksten for 16 MB.
- `testdata/feil/` med `skannet.pdf` og `feil-type.docx`, laget med `backend/scripts/lag_feilfiler.ps1`. `.gitignore` har unntak for docx-fila.
- Grensen på 50 bokstaver er prøvd: `skannet.pdf` 0, PDF-ene i testdataene 896–1 038 (`my-project/testplan.md`, «Story 6.2»). 413 er prøvd med den ekte utviklingsserveren og `urllib`: siden kom, og forbindelsen ble ikke brutt.
- 1 184 tester består, og ruff er uten feil. Gjennomgangen: 17 funn, 4 rettet (en død testkonstant, to tester som sjekket for lite eller for strengt, en docstring), resten avvist (se Review Triage Log i spec-en). Ingenting utsatt.
- Sprint-status: 6.2 er `review`. Notat lagt til i `my-project/8-refleksjonsrapport/notater.md`.
- Lukket i `issues.md`: de to punktene fra 6.1 om 6.2.

### Åpne punkter
- Prøve story 6.2 i nettleseren: `feil-type.docx`, `skannet.pdf` og en PDF over 5 MB i hvert sitt felt (tre feil samtidig, lenkene gir fokus), det samme i testmodus, og en fil over 16 MB (siden med feilboksen, ikke en hvit feilside). Kommentere PR-en etterpå.
