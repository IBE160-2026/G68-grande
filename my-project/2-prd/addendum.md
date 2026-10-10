# Addendum: Søknadsassistenten

Detaljer som hører hjemme i UX-, arkitektur- eller andre dokumenter, men som kom fram under arbeidet med PRD-en.

## Til UX

- **Logg ut-knapp (FR-6):** Kristine ser for seg en liten logg ut-knapp nederst på skjermen.
- **Tomme felt (FR-4) og manglende innlogging (FR-7):** feltene får rød ramme.
- **Innleggingssiden (FR-8, FR-13):** Kristine kaller feltene «opplastingsfelt», ett for CV og ett for stillingsannonsen, og i «Forbedre mitt brev» også ett for brukerens eget søknadsbrev. Det skal være en angre-knapp.

- **Ventetegn (FR-27):** Kristine ser for seg et «laster»-tegn som går rundt i en sirkel, med en tekst inni, for eksempel «På vei mot ny jobb» (frasen er ikke bestemt).

- **Testmodus-bryter (FR-32):** ligger i et hjørne av startsiden.

## Til arkitektur

- **Filstørrelse (FR-12):** Kristine vet ikke hvilken grense som passer. Arkitekturen bestemmer tallet.
- **KI-tjeneste (NFR-11):** Claude (Anthropic) via API. Modell, kostnad og håndtering av nøkkelen avklares i arkitekturen. API-nøkkelen ligger bare lokalt og legges aldri i Git. (Fra product brief.)
- **Lese tekst fra PDF (FR-11):** Hvordan nettsiden henter teksten ut av PDF-filer, avklares i arkitekturen. (Fra product brief.)

## Arbeidsmåte

- **README (NFR-8):** README oppdateres fortløpende gjennom hele prosjektet, hver gang noe endres som påvirker hvordan nettsiden installeres, startes eller testes.
