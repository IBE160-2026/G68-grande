# Addendum: Søknadsassistenten

Detaljer som hører hjemme i UX-, arkitektur- eller andre dokumenter, men som kom fram under arbeidet med PRD-en.

## Til UX

- **Logg ut-knapp (FR-6):** Kristine ser for seg en liten logg ut-knapp nederst på skjermen.
- **Tomme felt (FR-4) og manglende innlogging (FR-7):** feltene får rød ramme.
- **Innleggingssiden (FR-8, FR-13):** Kristine kaller feltene «opplastingsfelt», ett for CV og ett for stillingsannonsen, og i «Forbedre mitt brev» også ett for brukerens eget søknadsbrev. Det skal være en angre-knapp.

- **Ventetegn (FR-27):** Kristine ser for seg et «laster»-tegn som går rundt i en sirkel, med en tekst inni, for eksempel «På vei mot ny jobb» (frasen er ikke bestemt).

- **Testmodus-bryter (FR-32):** ligger i et hjørne av startsiden.

- **Skisser (fra faglærer):** Skisser modusvalget (FR-20) og resultatsiden, med gap-analysen, nøkkelordlisten og forklaringen av begrepene (FR-14, FR-16, FR-18).

## Til arkitektur

- **Filstørrelse (FR-12):** Kristine vet ikke hvilken grense som passer. Arkitekturen bestemmer tallet.
- **KI-tjeneste (NFR-11):** Claude (Anthropic) via API. Modell, kostnad og håndtering av nøkkelen avklares i arkitekturen. API-nøkkelen ligger bare lokalt og legges aldri i Git. (Fra product brief.)
- **Lese tekst fra PDF (FR-11):** Hvordan nettsiden henter teksten ut av PDF-filer, avklares i arkitekturen. (Fra product brief.)
- **Biblioteker (fra faglærer):** Velg få og godt dokumenterte biblioteker for å lese PDF og lage .docx og PDF, og begrunn valgene.
- **CV-er med kolonner og tabeller (FR-11, fra faglærer):** Bestem om testdataene skal ha en CV med to kolonner, eller om CV-er med én kolonne skal skrives ned som en kjent begrensning. Tekst fra CV-er med flere kolonner kan komme ut i feil rekkefølge, og da kan suksesskriterium 5 feile.
- **Testdata og fasit (NFR-3):** Eksempel på mappestruktur, med én undermappe per testcase og fasiten ved siden av testdataene. Endelig struktur avklares i arkitekturen.

  ```
  testdata/
    case-1-utvikler/
      cv.pdf
      annonse.txt
      eget-brev.pdf
      fasit.md        ← hvilke krav som mangler, riktig prosent osv.
    case-2-okonomi/
      ...
  ```

## Arbeidsmåte

- **README (NFR-8):** README oppdateres fortløpende gjennom hele prosjektet, hver gang noe endres som påvirker hvordan nettsiden installeres, startes eller testes.
