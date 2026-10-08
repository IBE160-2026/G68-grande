---
title: "Søknadsassistenten"
status: final
created: 2026-09-16
updated: 2026-09-16
---

# Produktbrief: Søknadsassistenten

## Sammendrag

Søknadsassistenten er et nettbasert verktøy der KI gjør jobben med å skreddersy både CV og søknadsbrev til en konkret stilling. Brukeren laster opp CV-en sin, en stillingsannonse og eventuelt en søknad de allerede har skrevet, og velger mellom to moduser: **Full generering**, der KI-en skriver fra bunnen, eller **Korrektur**, der KI-en forbedrer en tekst brukeren allerede har skrevet. Verktøyet peker i tillegg på manglende kvalifikasjoner gjennom en gap-analyse, og gir en ATS-vurdering. ATS står for Applicant Tracking System — programvaren mange arbeidsgivere bruker til å sortere og filtrere søknader automatisk, før et menneske leser dem.

Verdien ligger ikke bare i et fungerende produkt, men i å gi en realistisk opplevelse av hvordan KI faktisk brukes i rekrutteringsprosesser i dag — noe som gjør det direkte relevant for målgruppen: studenter på vei ut i arbeidslivet.

## Problemet

Å skrive en god, skreddersydd søknad for hver enkelt stilling er tidkrevende, og de fleste jobbsøkere — spesielt studenter uten mye erfaring — vet ikke hva som faktisk skiller et dokument som blir lest av en rekrutterer fra ett som blir silt ut automatisk. I dag løses dette typisk ved å:

- Gjenbruke samme søknadsbrev med små justeringer, noe som gir generiske, lite treffsikre søknader
- Bruke generiske KI-chatboter til å "skrive en søknad", uten kontekst om egen CV eller reell tilbakemelding på hva som mangler
- Ikke vite at de aller fleste store arbeidsgivere bruker ATS-systemer som automatisk filtrerer bort dårlig formaterte eller dårlig matchede dokumenter — hele 97,8 % av Fortune 500-selskapene gjør dette, og 99,7 % av rekrutterere bruker nøkkelordfiltre aktivt

Kostnaden er søknader som aldri blir lest av et menneske, og studenter som ikke vet *hvorfor* de blir silt ut.

## Løsningen

Verktøyet kobler brukerens CV, en konkret stillingsannonse og — om den finnes — en søknad brukeren allerede har skrevet, og produserer to typer verdi:

1. **Tekstproduksjon** — komplette utkast til søknadsbrev og CV i Full generering-modus, eller konkrete forbedringsforslag til en tekst brukeren selv har skrevet i Korrektur-modus. Alltid tilpasset ønsket tone, stil og språk, norsk eller engelsk.
2. **Innsikt** — en gap-analyse som viser hvilke kvalifikasjoner i annonsen CV-en ikke dekker, og en ATS-vurdering med tre deler: hvor lett dokumentet lar seg lese av automatiske systemer (dette kalles parsing), hvor godt det treffer nøkkelordene i annonsen, og en samlet treffscore.

Resultatet kan lastes ned som DOC, Markdown eller PDF, slik at brukeren kan gå videre og redigere i verktøyet de selv foretrekker.

## Hva gjør dette annerledes

Sammenlignbare verktøy, som Jobscan, Rezi, Teal og Kickresume, dekker typisk enten ATS-matching eller KI-tekstgenerering — sjelden begge deler i samme flyt, og sjelden med et tydelig valg mellom å la KI-en gjøre alt eller å beholde sin egen stemme og bare forbedre den. Det siste er ikke bare en detalj i brukeropplevelsen: helt KI-genererte søknadsbrev har en kjent svakhet — de blir lett gjenkjennelige og generiske. Ved å tilby Korrektur som et likeverdig alternativ til Full generering, anerkjenner produktet det problemet direkte i stedet for å late som det ikke finnes.

Den ærlige begrensningen: det unike fortrinnet er ikke teknisk sofistikasjon, men at fokuset på studentmålgruppen og de to modusene gir en enkel, tydelig opplevelse fremfor bredde.

## Hvem dette er for

**Primær bruker:** studenter og nyutdannede som søker jobb eller praksisplass for første gang, og som mangler erfaring med hva som faktisk fungerer i en søknad. De vet gjerne hva de kan, men ikke hvordan det oversettes til det en rekrutterer eller et ATS-system leter etter.

Verktøyet er åpent for alle jobbsøkere fra start, men designet holder studentens situasjon som hovedfokus gjennomgående: lite arbeidserfaring, og behov for å oversette utdanning og prosjekter til relevante kvalifikasjoner.

Suksess for denne brukeren: en søknad som føles som *deres egen stemme*, ikke en generisk KI-tekst — og en konkret forståelse av hva som mangler i CV-en deres, ikke bare en følelse av å være godkjent eller avvist.

## Suksesskriterier

Suksess måles på to nivåer:

**Funksjonalitet.** Hele flyten fungerer feilfritt fra opplasting til ferdig dokument, med innlogging og kryptert lagring på plass gjennom hele prosessen.

**Brukeropplevelse.** En testbruker skal kunne se en konkret, spesifikk forskjell mellom resultatene for to ulike stillingsannonser med samme CV. Teksten skal altså oppleves som reelt skreddersydd, ikke som en generisk mal.

Kriteriene holdes bevisst kvalitative i denne fasen, uten tallfestede terskelverdier.

## Omfang

### Inkludert i produktet
- Opplasting og lesing av CV som PDF, Word-dokument eller ren tekst
- Registrering av stillingsannonse, nøkkelord og ønsket tone
- Valgfri opplasting av en søknad brukeren allerede har skrevet
- To moduser som gjelder både CV og søknadsbrev: Full generering og Korrektur
- Gap-analyse som viser manglende kvalifikasjoner mot annonsen
- ATS-vurdering: maskinlesbarhet, nøkkelordtreff og treffscore
- Nedlasting som DOC, Markdown eller PDF
- Støtte for norsk og engelsk
- Innlogging og kryptert lagring av personopplysninger og dokumenter

### Ikke inkludert (bevisst)
- Ekte betalingsløsning, kjøp eller salg over nettet
- Automatisk innsending av søknader til jobbportaler
- En egen funksjon for å lagre og sammenligne flere tidligere søknader, utover å bruke dem som utgangspunkt for KI-en
- Mobilapp — nettside først

## Sikkerhet og personvern

Verktøyet håndterer personopplysninger og dokumenter, så innlogging kreves og kryptert lagring anbefales. Dette er ikke en formalitet: CV-er og søknadsbrev er sensitive personopplysninger, og bør behandles som en reell del av produktet.

Sikker innlogging er et krav. Konkret innloggingsmetode og krypteringsløsning avklares i neste fase av prosjektet.

## Visjon

Målet er en høyere andel studenter som får søknadene sine reelt vurdert av arbeidsgivere — fordi søknadene er skrevet på en god, akademisk måte som gjør arbeidsgiver oppmerksom og engasjert, i stedet for silt ut før noen har lest dem.
