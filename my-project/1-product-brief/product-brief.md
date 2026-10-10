---
title: "Søknadsassistenten"
status: final
created: 2026-09-16
updated: 2026-10-10
---

# Produktbrief: Søknadsassistenten

## Sammendrag

Søknadsassistenten er et nettbasert verktøy som hjelper studenter med å skrive et søknadsbrev som er skreddersydd til én konkret stilling. Brukeren legger inn CV-en sin og en stillingsannonse, og velger mellom to moduser: **Full generering**, der KI-en skriver brevet fra bunnen, eller **Korrektur**, der KI-en forbedrer et brev brukeren har skrevet selv og viser hva som er endret.

Før brevet skrives, får brukeren en **gap-analyse**, som viser hvilke krav i annonsen CV-en ikke dekker, og et **nøkkelordtreff**, som viser hvor stor andel av annonsens nøkkelord som står i CV-en. Mange arbeidsgivere bruker et ATS (Applicant Tracking System), altså programvare som sorterer søknader automatisk før et menneske leser dem. Nøkkelordtreffet gir studenten en enkel og forståelig pekepinn på hvordan CV-en kan bli vurdert.

Versjon 1 er bevisst avgrenset med kun søknadsbrev, kun norsk, og én tydelig flyt fra opplasting til nedlastet brev.

## Problemet

Det tar tid å skrive en god søknad som er tilpasset hver enkelt stilling. Studenter uten mye arbeidserfaring vet ofte ikke hva som skiller en søknad som blir lest, fra en som blir silt ut. I dag ender mange opp med å:

- gjenbruke det samme søknadsbrevet med små justeringer, som gir generiske søknader som treffer dårlig
- be en generell KI-chatbot om å «skrive en søknad», uten at den kjenner CV-en deres eller sier hva som mangler
- ikke vite at mange arbeidsgivere bruker ATS-systemer som filtrerer søknader på nøkkelord før et menneske ser dem

Resultatet er søknader som aldri blir lest av et menneske, og studenter som ikke forstår *hvorfor* de blir silt ut.

## Løsningen

Brukeren går gjennom én flyt:

1. **Logg inn** med e-post og passord.
2. **Legg inn CV og stillingsannonse**, enten som PDF-fil eller som innlimt tekst. Hvis nettsiden ikke klarer å lese en PDF, for eksempel fordi den er skannet, får brukeren beskjed om å lime inn teksten i stedet.
3. **Få innsikt:**
   - *Gap-analyse:* hvilke krav i annonsen CV-en ikke dekker.
   - *Nøkkelordtreff:* KI-en henter ut nøkkelordene fra annonsen, og nettsiden teller hvor mange av dem som finnes i CV-en, for eksempel «7 av 10 = 70 %». Tellingen gjøres med en fast regel, ikke av KI-en, slik at resultatet er forutsigbart og kan testes.
4. **Velg modus:**
   - *Full generering:* KI-en skriver et søknadsbrev basert på CV-en og annonsen.
   - *Korrektur:* Brukeren legger inn sitt eget brev. KI-en lager en forbedret versjon, og nettsiden viser endringene markert i teksten, med fjernet tekst i rødt og ny tekst i grønt. Slik ser brukeren hva som er endret og beholder kontrollen over sin egen stemme.
   - *Tone og språk:* Brevet skrives alltid på norsk og i en formell tone.
5. **Last ned brevet** som Word (.docx) for å redigere videre, eller som PDF hvis brevet er ferdig. Word er valgt i stedet for Markdown fordi studenter flest redigerer i Word, og brevet bør kunne finpusses før det sendes.

Ingenting lagres mellom gangene i versjon 1. Når brukeren logger ut, forsvinner CV, annonse og brev fra nettsiden. Brukeren tar vare på brevet ved å laste det ned.

## Hva gjør dette annerledes

Mange av funksjonene i Søknadsassistenten finnes allerede i andre verktøy. Jobscan, Rezi, Teal og Kickresume tilbyr for eksempel både nøkkelordsjekk mot en stillingsannonse og KI-skrevne søknadsbrev (sjekket 10. oktober 2026, se kilder). Søknadsassistenten konkurrerer derfor ikke på antall funksjoner. Det som kan skille den fra de andre, er at nøkkelordtreffet regnes med en åpen telleregel som brukeren kan forstå og etterprøve, og at nettsiden forklarer begrepene for studenter som søker jobb for første gang. Valget mellom å la KI-en skrive brevet og å forbedre sitt eget er heller ikke bare en detalj i brukeropplevelsen: helt KI-genererte søknadsbrev har en kjent svakhet — de blir lett gjenkjennelige og generiske. Ved å tilby Korrektur som et likeverdig alternativ til Full generering, anerkjenner produktet det problemet direkte i stedet for å late som det ikke finnes.

Den ærlige begrensningen: det unike fortrinnet er ikke teknisk sofistikasjon, men at fokuset på studentmålgruppen og de to modusene gir en enkel, tydelig opplevelse fremfor bredde.

## Hvem dette er for

**Primær bruker:** studenter og nyutdannede som søker jobb eller praksisplass for første gang, og som mangler erfaring med hva som faktisk fungerer i en søknad. De vet gjerne hva de kan, men ikke hvordan det oversettes til det en rekrutterer eller et ATS-system leter etter.

Verktøyet er åpent for alle jobbsøkere fra start, men designet holder studentens situasjon som hovedfokus gjennomgående: lite arbeidserfaring, og behov for å oversette utdanning og prosjekter til relevante kvalifikasjoner.

Suksess for denne brukeren: en søknad som føles som *deres egen stemme*, ikke en generisk KI-tekst — og en konkret forståelse av hva som mangler i CV-en deres, ikke bare en følelse av å være godkjent eller avvist.

## Suksesskriterier

Kriteriene er laget for å kunne testes. Til testingen lages 2–3 **fiktive** CV-er og stillingsannonser med en fasit som er skrevet på forhånd. Fasiten sier hvilke krav som mangler, og hva nøkkelordtreffet skal være.

1. **Gap-analyse:** For hver test-CV med tilhørende annonse viser gap-analysen alle kravene som fasiten sier mangler i CV-en.
2. **Nøkkelordtreff:** Med en fast nøkkelordliste og en gitt CV gir nettsiden nøyaktig den prosenten fasiten sier.
3. **Skreddersøm:** Samme CV med to ulike annonser gir to søknadsbrev som nevner krav som er spesifikke for hver av annonsene.
4. **Korrektur:** Når brukeren legger inn et eget brev, vises minst én markert endring, og den nedlastede filen inneholder den ferdige teksten uten markeringer.
5. **Filer inn og ut:** En test-CV i PDF og den samme CV-en som innlimt tekst gir samme nøkkelordtreff. Brevet kan lastes ned som Word og PDF, og begge filene kan åpnes.
6. **Innlogging:** En ny bruker kan registrere seg og logge inn. Feil passord gir ikke tilgang. Testbrukeren fra README virker.
7. **Testmodus:** Nettsiden kan startes lokalt etter README og brukes i testmodus uten API-nøkkel.

## Omfang

### Inkludert i versjon 1
Funksjonene er beskrevet under «Løsningen». Kort oppsummert:

1. Registrering og innlogging
2. CV og stillingsannonse inn som PDF eller innlimt tekst
3. Gap-analyse og nøkkelordtreff
4. Full generering og Korrektur av søknadsbrev
5. Tone og språk: norsk og formell tone
6. Nedlasting som Word (.docx) og PDF
7. Testmodus

### Ikke inkludert i versjon 1
- **CV og ATS:** skrive og forbedre CV, og vurdere hvor lett et ATS kan lese dokumentet
- **Flere valg:** engelsk språk, valg av tone, og at brukeren kan rette nøkkelordlisten
- **Flere filformater:** CV inn som Word, nedlasting som Markdown, «Kopier tekst»-knapp og «spor endringer» i Word-filen
- **Lagring og sikkerhet:** lagre CV og brev mellom gangene, kryptering, glemt passord og bekreftelse på e-post

### Ikke en del av prosjektet
- Betalingsløsning
- Automatisk innsending av søknader til jobbportaler
- Oversikt over og sammenligning av mange tidligere søknader
- Mobilapp. Det lages en nettside først.

## Teknisk retning, personvern og testdata

- **KI-tjeneste:** Claude (Anthropic) via API. Modell, kostnad og håndtering av nøkkelen avklares i arkitekturen. API-nøkkelen ligger bare lokalt og legges aldri i Git.
- **Testmodus og testdata:** Nettsiden kan kjøre med ferdige, lagrede KI-svar. Det gjør at sensor og automatiske tester ikke trenger nøkkel, og at testing ikke koster penger. README forklarer hvordan nettsiden startes, og gir én ferdig testbruker. Fiktive test-CV-er, annonser og fasiter ligger i en egen mappe i repoet. Ekte CV-er legges aldri i Git.
- **Personvern:** CV-er og søknader inneholder personopplysninger. Siden de ikke lagres i versjon 1, er det bare brukerkontoen som ligger i den lokale databasen, med passordet lagret trygt (hashet). Brukeren får beskjed på nettsiden om at teksten sendes til en ekstern KI-tjeneste når testmodus ikke er på. Kryptering blir aktuelt når lagring kommer i en senere versjon.

## Visjon

Målet er en høyere andel studenter som får søknadene sine reelt vurdert av arbeidsgivere — fordi søknadene er skrevet på en god, akademisk måte som gjør arbeidsgiver oppmerksom og engasjert, i stedet for silt ut før noen har lest dem.

## Kilder

Sjekket 10. oktober 2026.

- Jobscan: [jobscan.co](https://www.jobscan.co/blog/7-reasons-jobscan-is-more-effective-than-word-cloud-tools/), [LMU Career Center](https://careers.lmu.edu/resources/jobscan/)
- Rezi: [rezi.ai, AI Keyword Targeting](https://www.rezi.ai/docs/ai-keyword-targeting-explained), [rezi.ai](https://rezi.ai/lp/home), [Scoutify, anmeldelse](https://scoutify.com/blog/rezi-review/)
- Teal: [Teal hjelpeside, Cover Letter Generator](https://tealhq.helpscoutdocs.com/article/68-using-ai-cover-letter-generator)
- Kickresume: [kickresume.com](https://www.kickresume.com)
