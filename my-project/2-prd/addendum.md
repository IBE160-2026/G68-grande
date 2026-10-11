# Addendum: Søknadsassistenten

Detaljer som hører hjemme i UX-, arkitektur- eller andre dokumenter, men som kom fram under arbeidet med PRD-en.

## Til UX

- **Skisser (fra faglærer):** Skisser modusvalget (FR-20) og resultatsiden, med gap-analysen, nøkkelordlisten og forklaringen av begrepene (FR-14, FR-16, FR-18). På modusvalget viser knappene både modusnavnet og hva modusen gjør (FR-20).
- **Logg ut-knapp (FR-6):** Kristine ser for seg en liten logg ut-knapp nederst på skjermen.
- **Tomme felt (FR-4) og manglende innlogging (FR-7):** Feltene får rød ramme.
- **Innleggingssiden (FR-8, FR-13):** Kristine kaller feltene «opplastingsfelt», ett for CV og ett for stillingsannonsen, og i Korrektur også ett for brukerens eget søknadsbrev. Det skal være en angre-knapp.
- **Ventetegn (FR-27):** Kristine ser for seg et «laster»-tegn som går rundt i en sirkel, med en tekst inni, for eksempel «På vei mot ny jobb» (frasen er ikke bestemt).
- **Testmodus-bryter (FR-32):** ligger i et hjørne av startsiden.
- **Markeringer i Korrektur (FR-23):** Brukeren skal ikke måtte lese brevet to ganger. Kristines utgangspunkt: brevet vises én gang i den nye versjonen, endrede setninger er markert (for eksempel grønne og understreket), og et klikk på en markert setning viser den gamle. Alternativ som kan prøves på skisse: markering per ord, der bare ordene som er endret, vises i rødt og grønt. Avvist: per setning med gammel og ny setning under hverandre, fordi hele brevet da kan bli vist dobbelt.
- **Filnavn (FR-29):** Bestem navnet på den nedlastede filen, for eksempel «Soknad_2026-10-09.docx». Vurder om arbeidsgiveren skal stå i navnet, og unngå æ, ø og å.

## Til arkitektur

- **Filstørrelse (FR-12):** Kristine vet ikke hvilken grense som passer. Arkitekturen bestemmer tallet.
- **Lese tekst fra PDF (FR-11, fra product brief):** Hvordan nettsiden henter teksten ut av PDF-filer, avklares i arkitekturen.
- **Biblioteker (fra faglærer):** Velg få og godt dokumenterte biblioteker for å lese PDF og lage .docx og PDF, og begrunn valgene.
- **CV-er med kolonner og tabeller (FR-11, fra faglærer):** Bestem om testdataene skal ha en CV med to kolonner, eller om CV-er med én kolonne skal skrives ned som en kjent begrensning. Tekst fra CV-er med flere kolonner kan komme ut i feil rekkefølge, og da kan suksesskriterium 5 feile.
- **KI-tjeneste (NFR-11, fra product brief):** Claude (Anthropic) via API. Modell, kostnad og håndtering av nøkkelen avklares i arkitekturen. API-nøkkelen ligger bare lokalt og legges aldri i Git.
- **Ventetid på KI-en (FR-28):** Arkitekturen bestemmer hvor lenge nettsiden venter på svar fra KI-en før det regnes som at KI-en ikke svarer. Et langt søknadsbrev kan ta 20–30 sekunder.
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
- **Gjenkjenning av testdata (FR-34):** Arkitekturen bestemmer hvordan testmodus kjenner igjen testdataene, og hvor tolerant det skal være. Limer sensor inn teksten fra en test-PDF med et ekstra linjeskift eller mellomrom, bør det fortsatt regnes som testdata.
- **Språk:** Vurder om hele nettsiden kan lages i ett språk, slik at installasjonen for sensor blir enklere (NFR-8).

## Til prompten for brevet

- **Typiske KI-fraser (FR-24):** Brevet skal ikke bruke fraser fra denne listen. Listen er et utkast og er ikke bestemt ennå (åpent punkt, eier: Kristine). Eksempler så langt:
  - «Jeg er lidenskapelig opptatt av …»
  - «I dagens raskt skiftende arbeidsmarked …»
  - «Jeg er overbevist om at jeg vil være en verdifull ressurs …»
  - «Med min solide bakgrunn innen …»

## Arbeidsmåte

- **README (NFR-8):** README oppdateres fortløpende gjennom hele prosjektet, hver gang noe endres som påvirker hvordan nettsiden installeres, startes eller testes.
- **Kodestil:** Bruk en linter og en formaterer, og la CI sjekke dem.
- **Branches og pull requests (under kodingen):** Planleggingsdokumentene committes rett til `main`. Fra første story gjelder dette:
  1. Hver story får en egen branch og en pull request (PR) til `main`. Tittelen på PR-en viser til story og FR-nummer.
  2. I hver PR skrives én eller to setninger om hva som ble sjekket, og om KI-en gjorde noe feil eller noe jeg ikke ba om, og hvordan det ble rettet.
  3. De automatiske testene (CI) må være grønne før PR-en flettes inn.
  4. Prompt-loggen fortsetter under kodingen.
- **PRD under kodingen:** Når kodingen avviker fra PRD-en (et krav kuttes, endres eller legges til), oppdateres PRD-en og kopien i `my-project/2-prd/`, og avviket skrives i beslutningsloggen med dato og grunn.
