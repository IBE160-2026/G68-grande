---
title: "PRD: Søknadsassistenten"
status: final
created: 2026-10-09
updated: 2026-10-12
---

# PRD: Søknadsassistenten

## 1. Visjon

Søknadsassistenten er et nettbasert verktøy som hjelper studenter med å skrive et søknadsbrev som er skreddersydd til én konkret stilling. Brukeren velger om KI-en skal skrive brevet fra bunnen av (**Full generering**) eller forbedre et brev brukeren har skrevet selv (**Korrektur**), legger inn CV-en sin og en stillingsannonse, og får se hva CV-en mangler.

### Problemet

Det tar tid å skrive en god søknad som er tilpasset hver enkelt stilling. Studenter uten mye arbeidserfaring vet ofte ikke hva som skiller en søknad som blir lest, fra en som blir silt ut. I dag ender mange opp med å:

- gjenbruke det samme søknadsbrevet med små justeringer, som gir generiske søknader som treffer dårlig
- be en generell KI-chatbot om å «skrive en søknad», uten at den kjenner CV-en deres eller sier hva som mangler
- ikke vite at mange arbeidsgivere bruker ATS-systemer som filtrerer søknader på nøkkelord før et menneske ser dem

Resultatet er søknader som aldri blir lest av et menneske, og studenter som ikke forstår *hvorfor* de blir silt ut.

### Hvem dette er for

**Primær bruker:** studenter og nyutdannede som søker jobb eller praksisplass for første gang, og som mangler erfaring med hva som faktisk fungerer i en søknad. Verktøyet er åpent for alle jobbsøkere, men designet holder studentens situasjon som hovedfokus.

### Hva brukeren sitter igjen med

En søknad som føles som *deres egen stemme*, ikke en generisk KI-tekst — og en konkret forståelse av hva som mangler i CV-en deres, ikke bare en følelse av å være godkjent eller avvist.

### Hva gjør dette annerledes

Mange av funksjonene i Søknadsassistenten finnes allerede i andre verktøy. Jobscan, Rezi, Teal og Kickresume tilbyr for eksempel både nøkkelordsjekk mot en stillingsannonse og KI-skrevne søknadsbrev (sjekket 10. oktober 2026, se kilder). Søknadsassistenten konkurrerer derfor ikke på antall funksjoner. Det som kan skille den fra de andre, er at nøkkelordtreffet regnes ut med en åpen telleregel som brukeren kan forstå og etterprøve, og at nettsiden forklarer begrepene for studenter som søker jobb for første gang. Korrektur er et likeverdig alternativ til Full generering fordi helt KI-genererte søknadsbrev lett blir gjenkjennelige og generiske.

Den ærlige begrensningen: det unike fortrinnet er ikke teknisk sofistikering, men en åpen telleregel og forklaringer for studenter som gir en enkel, tydelig opplevelse fremfor bredde.

## 2. Funksjoner

Kravene beholder numrene de fikk da de ble skrevet, slik at henvisninger ikke brytes. Derfor står de ikke alltid i rekkefølge.

**Flyten i korte trekk:** Innlogging eller registrering (FR-1–FR-4, FR-6, FR-7) → startside med samtykke og «Begynn å lage søknad» (FR-5, FR-36) → valg av modus (FR-20) → innleggingsside (FR-8–FR-13) → resultatside med gap-analyse og nøkkelordtreff (FR-14–FR-19, FR-21) → siden «Din ferdigstilte søknad!» med brevet (FR-22–FR-28, FR-37) → nedlasting (FR-29, FR-30) → startsiden eller logg ut (FR-31).

### 2.1 Registrering og innlogging

- **FR-1:** Brukeren kan registrere seg med e-post og passord. Passordet må være minst 8 tegn. Etter registrering blir brukeren logget inn automatisk.
- **FR-2:** Hvis e-posten allerede er registrert, får brukeren en feilmelding som sier at e-posten allerede er registrert.
- **FR-3:** Brukeren kan logge inn med e-post og passord. Ved feil e-post eller passord får brukeren feilmeldingen «Feil e-post eller passord».
- **FR-4:** Hvis et felt står tomt, får rammen rundt feltet rød farge, og det vises en kort feilmelding ved feltet, for eksempel «Fyll inn e-post», slik at feilen ikke bare vises med farge.
- **FR-5:** Etter innlogging havner brukeren på en startside med en tydelig måte å begynne på en ny søknad, for eksempel «Begynn å lage søknad». Derfra går brukeren videre til valget mellom Full generering og Korrektur (FR-20).
- **FR-6:** Brukeren kan logge ut fra nettsiden.
- **FR-7:** Det er ikke mulig å bruke nettsiden uten å være logget inn, unntatt innloggingen og registreringen. Prøver brukeren å gå til en annen side på nettsiden uten å være logget inn, kommer de til innloggingen med en feilmelding som sier at de må logge inn først.

### 2.2 Valg av modus og PDF eller tekst inn

- **FR-20:** Etter «Begynn å lage søknad» velger brukeren mellom to muligheter:
  - **«Skriv nytt brev»** (Full generering): brukeren legger inn CV og stillingsannonse.
  - **«Forbedre mitt brev»** (Korrektur): brukeren legger inn CV, sitt eget søknadsbrev og stillingsannonse.

  Knappene viser begge navnene, for eksempel «Full generering – Skriv nytt brev» og «Korrektur – Forbedre mitt brev», slik at brukeren ikke kan misforstå hva knappene gjør. Hvordan det ser ut, bestemmes i UX.
- **FR-8:** Innleggingssiden har separate felt for CV og stillingsannonse, og i Korrektur også et felt for brukerens eget søknadsbrev. I hvert felt kan brukeren enten laste opp en PDF eller lime inn tekst.
- **FR-9:** Alle feltene som vises, må være fylt ut før brukeren kan gå videre. CV og stillingsannonse er alltid med, fordi gap-analysen og nøkkelordtreffet bygger på dem. Mangler noe, får brukeren en feilmelding som sier hva som mangler.
- **FR-10:** Hvis brukeren laster opp en fil som ikke er PDF, får brukeren feilmeldingen «Feil filtype, prøv PDF».
- **FR-11:** Hvis nettsiden ikke klarer å lese teksten i en PDF, for eksempel fordi den er skannet, får brukeren beskjed om å lime inn teksten i stedet.
- **FR-12:** Nettsiden har en øvre grense for filstørrelse. Er filen for stor, får brukeren en feilmelding som sier dette. Selve grensen bestemmes i arkitekturen.
- **FR-13:** Brukeren kan angre, altså fjerne eller bytte ut en fil eller tekst de har lagt inn, før de går videre.

### 2.3 Gap-analyse og nøkkelordtreff

KI-en brukes til å finne kravene og nøkkelordene, og koden brukes til å telle, slik at tallet kan testes.

- **FR-14:** Gap-analysen går gjennom kravene i stillingsannonsen og viser dem i to lister: krav CV-en **dekker** og krav CV-en **mangler**. Gap-analysen er merket som KI-generert.
- **FR-15:** KI-en henter ut nøkkelordene fra stillingsannonsen én gang. Listen lagres i økten, og prosenten regnes alltid fra den lagrede listen, ikke fra et nytt KI-kall. Innenfor samme søknad gir samme annonse og samme CV derfor alltid samme prosent. Starter brukeren en ny søknad eller logger ut, glemmes listen. Da lager KI-en en ny liste, og prosenten kan bli litt annerledes.
- **FR-16:** Brukeren ser nøkkelordlisten, med hvert nøkkelord merket som treff eller ikke treff. Listen kan ikke endres av brukeren i versjon 1.
- **FR-17:** Nøkkelordtreffet regnes ut av nettsiden med en fast regel og vises som «X av Y = Z %», for eksempel «7 av 10 = 70 %».
  - **Telleregel:** Et nøkkelord er et treff hvis det finnes i CV-teksten, også som del av et lengre ord, uavhengig av store og små bokstaver. «Python» er altså et treff i «python-utvikler». Nøkkelord på 1–3 tegn må likevel stå som eget ord, så «C» er et treff i CV-teksten «Kan C og Python», men ikke i «Center».
  - **Kjente begrensninger:** Bøyningsformer fanges ikke opp, så «prosjektledelse» er ikke et treff i «prosjektleder». Et nøkkelord på 4 tegn eller mer kan gi treff inne i et annet ord, for eksempel «Java» i «JavaScript». Et kort nøkkelord kan gi feil treff hvis det står alene i en annen betydning, for eksempel «C» i en liste nummerert med bokstaver (A, B, C).
  - **Telling og avrunding:** Hvert nøkkelord telles bare én gang, selv om det står flere ganger i CV-en. Prosenten rundes til nærmeste hele tall, så «2 av 3» vises som «67 %».
- **FR-18:** På resultatsiden forklarer nettsiden kort tre begreper:
  - **ATS:** et system mange arbeidsgivere sender søknadene gjennom før et menneske leser dem.
  - **Nøkkelordtreff:** en ordtelling av hvor mange av annonsens nøkkelord som står i CV-en. Det er bare en pekepinn på hvordan CV-en kan bli vurdert av et ATS, ikke en garanti.
  - **Gap-analyse:** en KI-vurdering av hvilke krav i annonsen CV-en dekker og mangler.

  Nettsiden forklarer også at gap-analysen og nøkkelordtreffet derfor kan si hverandre imot. For eksempel kan gap-analysen si at «SQL mangler» selv om ordtellingen fant «SQL».
- **FR-19:** Brukeren kan gå tilbake til innleggingssiden etter å ha sett resultatet. CV, annonse og eventuelt eget søknadsbrev er da fortsatt fylt ut. Når brukeren går videre igjen, kjøres analysen på nytt. Er bare CV-en endret, gjenbrukes den lagrede nøkkelordlisten.
- **FR-21:** Brukeren ser gap-analysen og nøkkelordtreffet før brevet lages eller korrigeres. Brevet lages først når brukeren har bekreftet at de vil gå videre.

### 2.4 Søknadsbrev: Full generering og Korrektur

- **FR-22:** I Full generering skriver KI-en et søknadsbrev basert på CV-en og stillingsannonsen. Brevet vises på nettsiden, slik at brukeren kan lese det før det lastes ned.
- **FR-23:** I Korrektur lager KI-en en forbedret versjon av brukerens eget brev, basert på CV-en og stillingsannonsen. Nettsiden viser hva som er endret, uten at brukeren må lese brevet to ganger. Utgangspunktet er at brevet vises én gang i den nye versjonen, at endrede setninger er markert, og at brukeren kan klikke på en markert setning for å se den gamle. Endelig løsning bestemmes i UX. Slik ser brukeren hva som er endret og beholder kontrollen over sin egen stemme. Endringene vises ikke bare med farge, men også på en annen måte, for eksempel med understreking.
- **FR-24:** Brevet skrives alltid på norsk, i formell og akademisk tone som gjør arbeidsgiver oppmerksom og engasjert, og skal ikke høres ut som en generisk KI-tekst. Dette gjelder begge modusene. Det betyr at brevet:
  - nevner stillingen og arbeidsgiveren ved navn
  - viser til minst to konkrete krav fra stillingsannonsen og kobler dem til noe i CV-en
  - ikke bruker typiske KI-fraser (listen ligger i addendum)

  I Korrektur betyr det at KI-en retter språk og ordvalg mot formell og akademisk tone, men beholder brukerens innhold, eksempler og rekkefølge. Slik beholder brukeren sin egen stemme (FR-23).
- **FR-37:** KI-en skal ikke komme med antakelser på vegne av brukeren. Brevet bygger bare på det som står i CV-en, stillingsannonsen og eventuelt brukerens eget brev. KI-en legger ikke til erfaring, utdanning eller ferdigheter som ikke står der. KI-en får omformulere det som står i CV-en og koble det til kravene i stillingsannonsen, for eksempel et gruppeprosjekt til «erfaring med samarbeid og prosjektarbeid». Dette gjelder begge modusene.
- **FR-25:** Brukeren kan be om et nytt forslag hvis de ikke er fornøyd med brevet. I Korrektur lages det nye forslaget fra brukerens opprinnelige brev.
- **FR-26:** Brukeren redigerer ikke brevet på nettsiden. Videre redigering gjøres i Word etter nedlasting.
- **FR-27:** Mens KI-en jobber, viser nettsiden et ventetegn med en kort tekst. Knappen som startet handlingen, kan ikke trykkes på nytt mens brukeren venter, slik at det ikke sendes flere forespørsler samtidig.
- **FR-28:** Hvis KI-en ikke svarer, får brukeren en feilmelding:
  - Ved nettverksfeil: «Nettverksfeil, sjekk nettverkstilgangen».
  - Ved andre feil: en feilmelding som ber brukeren prøve på nytt.

  Hvis KI-en svarer, men svaret ikke kan brukes, viser nettsiden ikke noe resultat. I stedet får brukeren en feilmelding som ber dem prøve på nytt. Et svar kan ikke brukes når:
  - nøkkelordlisten er tom
  - både «dekker» og «mangler» i gap-analysen er tomme
  - søknadsbrevet er tomt
  - nettsiden ikke klarer å lese svaret

  Etter en feil er det brukeren har lagt inn, fortsatt der, slik at de ikke må begynne på nytt.

### 2.5 Word og PDF ut

Word er valgt i stedet for Markdown, som faglærer foreslo, fordi studenter flest redigerer i Word, og brevet bør kunne finpusses før det sendes.

- **FR-29:** Når brevet er ferdig, finnes det en nedlastingsknapp der brukeren kan laste ned brevet som Word (.docx) eller PDF. Filnavnet bestemmes i UX.
- **FR-30:** Den nedlastede filen inneholder bare den ferdige brevteksten, uten markeringene fra Korrektur, og uten topp- eller bunntekst.
- **FR-31:** Etter nedlasting kan brukeren velge mellom å gå til startsiden eller logge ut. Går brukeren til startsiden, starter de en ny søknad med tomme felt.

### 2.6 Testmodus og bruk av KI

- **FR-32:** Allerede på startsiden kan brukeren bytte til testmodus med en bryter.
  - I testmodus kan brukeren bytte tilbake til vanlig modus med den samme bryteren. Brukeren kan bare bytte på startsiden, ikke midt i en søknad.
  - I testmodus bruker nettsiden ferdige KI-svar i stedet for å sende tekst til en ekstern KI, slik at nettsiden kan kjøres uten API-nøkkel.
  - Finnes det ingen API-nøkkel, starter nettsiden i testmodus, det er ikke mulig å bytte tilbake til vanlig modus, og det vises en kort forklaring, for eksempel «Mangler API-nøkkel, se README».
- **FR-33:** Når testmodus er på, vises en tydelig merkelapp, for eksempel «Testmodus», slik at brukeren ser det.
- **FR-34:** I testmodus fungerer bare de fiktive testdataene.
  - Legger brukeren inn noe annet, får de beskjed om at bare testdata fungerer i testmodus.
  - Feilmeldingene for tomme felt, feil filtype og uleselig PDF virker også i testmodus.
  - Testdataene dekker både Full generering og Korrektur, også med et fiktivt søknadsbrev til Korrektur. Testdataene har også en skannet PDF og en fil av feil type, slik at sensor kan prøve feilmeldingene.
- **FR-35:** Når testmodus er av, vises en merknad i et hjørne av nettsiden hele tiden, som sier at nettsiden bruker en ekstern KI.
- **FR-36:** Når testmodus er av, må brukeren på startsiden samtykke til bruk av KI før de kan begynne å lage en søknad. Samtykket gis på nytt hver gang brukeren logger inn.
  - Over avkrysningsboksen står en tekst som forklarer hva samtykket gjelder, altså at teksten brukeren legger inn, sendes til en ekstern KI.
  - Brukeren huker av boksen og trykker deretter «Begynn å lage søknad».
  - Trykker brukeren «Begynn å lage søknad» uten å ha huket av, får de en feilmelding som sier at de må samtykke først.
  - I testmodus trengs ikke samtykke, fordi ingen tekst sendes til en ekstern KI.
- **FR-38:** De ferdige svarene i testmodus er ekte KI-svar, laget ved å kjøre de fiktive testdataene gjennom den eksterne KI-en. README viser i tillegg to–tre skjermbilder av nettsiden med ekte KI på.

## 3. Ikke-funksjonelle krav

### Sikkerhet og personvern

- **NFR-1:** Passord lagres hashet, aldri som klartekst.
- **NFR-2:** API-nøkkelen ligger bare lokalt og havner aldri i Git. Repoet har en `.env.example` som viser hvilke innstillinger som trengs, uten ekte verdier.
- **NFR-3:** Ekte CV-er havner aldri i Git. Bare fiktive testdata ligger i repoet, i en egen mappe, sammen med en fasit for hver CV og stillingsannonse.
- **NFR-4:** CV, stillingsannonse, søknadsbrev og nøkkelordliste lagres ikke mellom øktene. Bare brukerkontoen lagres, i en lokal database.
- **NFR-5:** Innloggingen fungerer lokalt uten noen ekstern tjeneste.

### Tilgjengelighet og skjermstørrelser

- **NFR-6:** Nettsiden har god kontrast, kan brukes med bare tastatur, og alle felt har synlige etiketter. Bilder og ikoner har alternativtekst. Kontrasten sjekkes mot WCAG AA med et kontrastverktøy når fargene velges.
- **NFR-7:** Nettsiden ser bra ut og fungerer godt på PC, nettbrett og mobil. Alle sider kan brukes uten å rulle sidelengs ved 375 px (mobil), 768 px (nettbrett) og 1280 px (PC) bredde.

### Kjørbarhet og testing

- **NFR-8:** Sensor kan få nettsiden i gang på 10–15 minutter ved å følge README. Første gang nettsiden startes, lages databasen og testbrukeren automatisk. README har:
  - en kort beskrivelse av hva nettsiden gjør
  - forutsetninger med versjoner
  - eksakte kommandoer for installasjon og oppstart
  - hvilke innstillinger som trengs, med henvisning til `.env.example` (NFR-2)
  - e-post og passord til testbrukeren
  - hvor testdataene og fasiten ligger (NFR-3)
  - hvordan testene kjøres (NFR-9)
  - to–tre skjermbilder med ekte KI på (FR-38)
  - en oversikt over mappestrukturen
  - lenker til planleggingsdokumentene og prompt-loggen
- **NFR-9:** Telleregelen for nøkkelordtreff (FR-17), også regelen for korte nøkkelord, og innloggingen (FR-1, FR-3) har automatiske tester med kjent input og fasit. Det samme gjelder kontrollen av KI-svar (FR-28), sjekken av det brukeren legger inn (FR-9, FR-10, FR-12), gjenbruk av nøkkelordlisten (FR-15), at sider krever innlogging (FR-7), og at nedlastet fil er uten markeringer (FR-30). README viser hvordan testene kjøres.
- **NFR-10:** KI-instruksene (prompts) ligger i Git, slik at endringer i dem kan følges.
- **NFR-12:** Det finnes en skrevet testplan med resultat for suksesskriteriene som ikke testes automatisk, også hele flyten fra start til slutt. Testplanen viser også at README er prøvd fra en ny kopi av repoet i en tom mappe, uten `.env` og andre lokale filer, før funksjonsstopp og rett før levering, med dato og resultat.

### KI-tjeneste

- **NFR-11:** Den eksterne KI-en er Claude fra Anthropic, brukt via API. Modell og kostnad avklares i arkitekturen.

## 4. Omfang og kuttliste

Fristen er kort, og kjerneflyten skal være ferdig og stabil før noe annet legges til. Derfor er følgende bevisst utelatt fra versjon 1.

### Ikke med i versjon 1 (kan komme senere)

| Hva | Hvorfor utelatt |
|---|---|
| Skrive og forbedre CV, og vurdere hvor lett et ATS kan lese dokumentet | Kjerneflyten først |
| Engelsk språk og valg av tone | Kjerneflyten først |
| At brukeren kan rette nøkkelordlisten | Kjerneflyten først |
| CV inn som Word, nedlasting som Markdown, «Kopier tekst»-knapp og «spor endringer» i Word-filen | Kjerneflyten først |
| Lagre CV og brev mellom gangene, kryptering, glemt passord og bekreftelse på e-post | Kjerneflyten først |
| Innlogging med Google eller andre eksterne kontoer (OAuth) | Krever en ekstern tjeneste, og innloggingen skal virke lokalt uten det (NFR-5) |
| Ordstamme-regel, slik at «prosjektledelse» er et treff i «prosjektleder» | Mer komplisert å bygge og mindre forutsigbart enn den enkle telleregelen (FR-17) |
| «Kun søknad», altså Korrektur uten CV | Krever en ekstra analysevariant (søknad mot annonse), flere KI-instrukser og flere tester. KI-delen er det mest risikable i prosjektet |
| Redigere brevet i nettleseren | Studenter redigerer i Word. Visningen med markerte endringer i Korrektur er vanskelig å gjøre redigerbar, og «nytt forslag» ville overskrevet endringene |
| Topp- og bunntekst i den nedlastede filen (dato, navn, stilling) | KI-en kan hente feil navn eller stilling, og det blir mer å teste. Brukeren legger det til i Word |

### Gjøres hvis det blir tid

| Hva | Hvorfor utelatt |
|---|---|
| Telleregelen på hvilken som helst CV i testmodus, med nøkkelordlisten fra test-annonsen | Ny funksjon, prioritert bort på grunn av tid. Telleregelen vises fortsatt med testdataene og har automatiske tester (NFR-9) |
| Beholde CV-en når brukeren går til startsiden for å lage en ny søknad, slik at de kan søke på flere stillinger uten å laste opp CV-en på nytt | Ny funksjon, prioritert bort på grunn av tid. I versjon 1 starter en ny søknad med tomme felt (FR-31) |
| Automatisk test av hele flyten i testmodus | Prioritert bort på grunn av tid. Flyten testes manuelt og skrives inn i testplanen (NFR-12) |

### Nødliste ved tidsnød

Disse funksjonene er med i versjon 1, men kuttes i denne rekkefølgen hvis tiden ikke strekker til:

**Kuttes først (lite tap):**

1. Tilbake-knappen gjenbruker ikke nøkkelordlisten. Analysen kjøres bare på nytt. (FR-19)
2. Bare .docx ved nedlasting, ikke PDF. (FR-29)
3. Ingen «nytt forslag»-knapp. Brukeren kan gå tilbake og kjøre på nytt. (FR-25)

**Kuttes deretter (merkbart, men flyten virker fortsatt):**

4. Ingen markeringer i Korrektur. Brukeren får det forbedrede brevet uten å se hva som er endret. (FR-23)
5. Bare innlimt tekst, ikke PDF-opplasting. Suksesskriterium 5 må da endres. (FR-8, FR-10–FR-12)

**Siste utvei:**

6. Hele Korrektur. Den gjør at brukeren kan beholde sin egen stemme, og kuttes bare når alt annet er prøvd.

**Kuttes aldri:** testmodus, innlogging, gap-analysen, nøkkelordtreffet med telleregelen og testene, Full generering, .docx-nedlasting, samtykke og FR-37.

### Ikke en del av prosjektet

Betaling, automatisk innsending, oversikt over tidligere søknader og mobilapp.

## 5. Suksesskriterier

Kriteriene testes mot 2–3 fiktive CV-er og stillingsannonser med fasit. Kriterium 1, 3, 11 og 12 testes med ekte KI, ikke i testmodus. De kjøres tre ganger per testcase, og alle tre må bestå. Resultatet skrives i testplanen (NFR-12).

1. Gap-analysen viser alle krav som fasiten sier mangler, og ingen krav som fasiten sier er dekket, står under «mangler». (FR-14)
2. Nøkkelordtreffet gir nøyaktig den prosenten fasiten sier, når nøkkelordlisten er fast. (FR-17)
3. Samme CV med to ulike annonser gir brev som nevner krav som er spesifikke for hver annonse. (FR-22)
4. Korrektur viser minst én markert endring, og den nedlastede filen har ingen markeringer. (FR-23, FR-30)
5. PDF og innlimt tekst gir samme treff, både for CV, stillingsannonse og eget søknadsbrev, og både .docx og PDF kan åpnes. (FR-8, FR-29)
6. En ny bruker kan registrere seg, feil passord gir ikke tilgang, og testbrukeren fra README virker. (FR-1, FR-3, NFR-8)
7. Nettsiden kan kjøres lokalt etter README i testmodus uten API-nøkkel. (FR-32, NFR-8)
8. Samme stillingsannonse og CV kjørt to ganger i samme søknad gir samme nøkkelordtreff. (FR-15)
9. I vanlig modus kommer brukeren ikke videre uten å ha huket av for samtykke. (FR-36)
10. Feil filtype, tomme felt og en uleselig PDF gir riktig feilmelding. (FR-4, FR-9, FR-10, FR-11)
11. Brevet nevner ingen erfaring, utdanning eller ferdigheter som ikke står i den fiktive CV-en. Sjekkes manuelt mot fasit. (FR-37)
12. I Korrektur beholder det forbedrede brevet brukerens innhold, eksempler og rekkefølge. Sjekkes manuelt med testdataene. (FR-23, FR-24)
13. En medstudent som ser resultatsiden for en av test-CV-ene, kan med egne ord forklare hva som mangler i CV-en, og hva nøkkelordtreffet betyr og ikke betyr. (FR-14, FR-18)

## 6. Risiko

| Risiko | Hva jeg gjør med det |
|---|---|
| **Gap-analysen og nøkkelordtreffet er vanskelig å få til** | Telleregelen (FR-17) bygges først, med automatiske tester. Den er ren kode og lettest å få riktig. Gap-analysen bygges etterpå. |
| **Kodingen tar lengre tid enn planlagt** | Kjerneflyten bygges i rekkefølge: innlogging → inndata → analyse → brev → nedlasting. Blir tiden knapp, kuttes flere funksjoner som ikke er en del av kjerneflyten, i rekkefølgen i nødlisten i del 4, og de flyttes til kuttlisten med begrunnelse. Hvis en milepæl er mer enn tre dager forsinket, kuttes neste punkt på nødlisten. Kjerneflyten kuttes aldri. |
| **KI-funksjonen i nettsiden løser ikke problemet slik den skal, eller blir for avansert** | Hele flyten bygges først med testmodus og ferdige KI-svar. Ekte KI kobles på til slutt, når resten virker. Hver KI-oppgave (nøkkelord, gap-analyse, brev, korrektur) får sin egen enkle instruks (prompt) som kan testes hver for seg. Tellingen gjøres av koden, ikke av KI-en. |
| **KI-en i nettsiden skriver ting i brevet som ikke stemmer**, for eksempel erfaring som ikke står i CV-en | Eget krav (FR-37). Instruksen til KI-en sier at brevet bare skal bygge på det brukeren har lagt inn. Testes med fiktive CV-er og fasit (suksesskriterium 11). |
| **KI-en jeg bruker når jeg koder, gjør endringer jeg ikke har bedt om, eller legger til ting jeg ikke får med meg** | Én liten oppgave om gangen. Endringene leses gjennom før de committes, og commits gjøres ofte, slik at det er lett å se hva som er endret og gå tilbake. Arbeidet følger stories som viser til FR-numrene i denne PRD-en. Hver story får egen branch og pull request, med en kort kommentar om feil KI-en gjorde og hvordan de ble rettet (se addendum, «Arbeidsmåte»). |

## 7. Milepæler

Prosjektet leveres 15. desember 2026. Datoene er et utgangspunkt og vurderes på nytt uken etter 11. oktober, når tiden til andre fag er klar.

| Milepæl | Dato |
|---|---|
| PRD ferdig | 11. oktober |
| UX, arkitektur og epics/stories ferdig | 25. oktober |
| Innlogging og telleregel med tester | 1. november |
| Hele kjerneflyten i testmodus | 18. november |
| Ekte KI koblet på | 27. november |
| Funksjonsstopp (bare feilretting, README og testplan) | 6. desember |
| README testet på en ren klone | 11. desember |
| Levering | 15. desember |

## 8. Åpne spørsmål

| Spørsmål | Eier | Når |
|---|---|---|
| Regnes product brief som proposal? Hvis ikke, kan kuttlisten måtte endres. | Kristine (spør faglærer) | Før arkitekturen |
| Hvilke fraser skal stå på listen over typiske KI-fraser (FR-24)? | Kristine | Før prompten for brevet skrives |
| Passer milepælsdatoene, når tiden til andre fag er klar? | Kristine | Uken etter 11. oktober |

### Avgjøres i UX og arkitektur

PRD-en sier *hva* nettsiden skal gjøre. *Hvordan* den ser ut, bestemmes i UX, og *hvordan* den lages, bestemmes i arkitekturen. Disse punktene er bevisst ikke bestemt her. Det er fordi de enten må prøves ut på skisser, eller fordi de avhenger av tekniske valg som ikke er tatt ennå. Detaljer og mine første ideer står i addendum.

| Hva | Avgjøres i | Hvorfor ikke nå |
|---|---|---|
| Hvordan endringene markeres i Korrektur (FR-23) | UX | Må prøves på skisse. Utgangspunkt og et alternativ ligger klart |
| Filnavnet på det nedlastede brevet (FR-29) | UX | Det er noe brukeren ser, og det henger sammen med hvordan nedlastingen ser ut |
| Utseende og plassering av knapper, ventetegn, testmodus-bryter og feilmarkering | UX | PRD-en bestemmer at de finnes, UX bestemmer hvordan de ser ut |
| Grensen for filstørrelse (FR-12) | Arkitektur | Avhenger av hvor nettsiden kjøres og hva KI-tjenesten tåler |
| KI-modell og kostnad (NFR-11) | Arkitektur | Krever at modellene sammenlignes på pris og kvalitet |
| Hvor lenge nettsiden venter på KI-en (FR-28) | Arkitektur | Avhenger av modellen og må måles. Et langt brev kan ta 20–30 sekunder |
| Hvordan PDF leses, og hvordan Word og PDF lages (FR-8, FR-11, FR-29) | Arkitektur | Valg av biblioteker er et teknisk valg |
| CV-er med kolonner og tabeller (FR-11) | Arkitektur | Avhenger av hva biblioteket for PDF klarer |
| Hvordan testmodus kjenner igjen testdataene (FR-34), og mappene for testdata (NFR-3) | Arkitektur | Teknisk løsning |

## Ordliste

- **Full generering** («Skriv nytt brev»): KI-en skriver et nytt søknadsbrev ut fra CV-en og stillingsannonsen.
- **Korrektur** («Forbedre mitt brev»): KI-en forbedrer brukerens eget brev og viser hva som er endret.
- **Gap-analyse:** KI-ens liste over hvilke krav i stillingsannonsen CV-en dekker, og hvilke som mangler.
- **Nøkkelordtreff:** hvor mange av annonsens nøkkelord som står i CV-en. Det regnes ut av koden med telleregelen (FR-17).
- **Telleregel:** den faste regelen koden bruker for å regne ut nøkkelordtreffet.
- **Økt:** fra brukeren logger inn til brukeren logger ut. Ingenting fra en økt lagres etter at brukeren logger ut (NFR-4).
- **Testmodus:** nettsiden bruker ferdige KI-svar og bare de fiktive testdataene, og trenger ingen API-nøkkel.
- **Vanlig modus:** nettsiden bruker ekte KI.
- **Fasit:** det riktige svaret for hvert testcase. Fasiten ligger sammen med testdataene.

## Kilder

Sjekket 10. oktober 2026.

- Jobscan: [jobscan.co](https://www.jobscan.co/blog/7-reasons-jobscan-is-more-effective-than-word-cloud-tools/), [LMU Career Center](https://careers.lmu.edu/resources/jobscan/)
- Rezi: [rezi.ai, AI Keyword Targeting](https://www.rezi.ai/docs/ai-keyword-targeting-explained), [rezi.ai](https://rezi.ai/lp/home), [Scoutify, anmeldelse](https://scoutify.com/blog/rezi-review/)
- Teal: [Teal hjelpeside, Cover Letter Generator](https://tealhq.helpscoutdocs.com/article/68-using-ai-cover-letter-generator)
- Kickresume: [kickresume.com](https://www.kickresume.com)
