# TO DO

Ting som skal gjøres i prosjektet. Kryss av (`[x]`) når et punkt er gjort, og legg til nye punkter når vi oppdager dem.

Åpne punkter fra sesjonsloggene står også i `.logs/kristine/issues.md` (se `.logs/kristine/README.md`).

## Ferdigstilling av PRD

- [x] Steg 1: gjennomgang av beslutningsloggen (memlog)
- [x] Steg 2: kildesjekk mot brief, faglærers tilbakemelding, sensorveiledning og brief-memlog
- [x] Kilder for Jobscan, Rezi, Teal og Kickresume i PRD og product brief
- [x] Oppdatere beslutningsloggen for briefen (`brief-memlog.md`) med endringene fra PRD-arbeidet
- [x] Steg 3: gjennomgang der hjelpere leser PRD-en kritisk og ser etter svakheter
- [x] Steg 4: gå gjennom de 9 antakelsene (`[ASSUMPTION]`) og bestemme hver av dem
- [x] Steg 5: språkvask og struktur av PRD og addendum
- [x] Steg 6–7: sette PRD-en til ferdig (`status: final`), og fjerne «(under arbeid)» i README-ene

## Andre åpne punkter

- [x] Spørre faglærer om product brief regnes som proposal
- [x] Skrive «Hva jeg lærte» i prompt-loggen
- [ ] Bestemme lista over typiske KI-fraser (FR-24, ligger i addendum)

## Etter PRD-en

- [x] Prøve branch og pull request én gang med Claude før kodingen starter (PR #1, NFR-8 «hvem den er for», 3. november)
- [x] UX (skisser av modusvalget og resultatsiden, se addendum)
  - [x] Utseende: farger (Myk fersken), former, bevegelse, skrift og logo
  - [x] Brukerreise 1: Ingrid, Full generering
  - [x] Brukerreise 2: Eirik, Korrektur på mobil
  - [x] Brukerreise 3: Henrik, sensor og testmodus
  - [x] Skisser av modusvalget og resultatsiden
  - [x] Skisser av alle sidene, på PC og mobil
  - [x] Ferdigstille DESIGN.md og EXPERIENCE.md
    - [x] Runde 1: dokumentene skrevet ut fra beslutningsloggen og skissene
    - [x] Runde 2: hull, motsigelser og antakelser gått gjennom
    - [x] Runde 3: kritisk gjennomgang (A sjekkliste + B tilgjengelighet + C sensor-blikk), alle funn bestemt og lagt inn i dokumentene
    - [x] Oppdatere skissene med endringene fra runde 2 (FR-18-linjen, rammefarge, bryter, tomme lister, logg ut-vindu, fast rad nederst, tekst for skannet PDF, ingen 🧪)
    - [x] Oppdatere skissene med endringene fra runde 3 (resultatsiden i Korrektur, feiltekst under feltet, filnavn i vinduet, ny ventetekst, felt side om side fra 1000 px, «1 setning er fjernet», ekte `@media` og prøve 768 px)
    - [x] Språkvask og sette dokumentene til ferdig (`status: final`)
- [ ] Arkitektur
  - Fra PRD-en og addendumet:
  - [ ] Grensen for filstørrelse (FR-12), så UX-teksten «høyst X MB» får et tall
  - [ ] Hvordan teksten leses ut av PDF-filer (FR-8, FR-11)
  - [ ] Få og godt dokumenterte biblioteker for å lese PDF og lage Word og PDF, med begrunnelse (fra faglærer)
  - [ ] CV-er med kolonner og tabeller: støtte dem eller skrive det som kjent begrensning (jeg vil prøve å støtte tabeller)
  - [ ] KI-tjeneste (NFR-11): Claude-modell, kostnad og hvordan API-nøkkelen holdes utenfor Git
  - [ ] Hvor lenge nettsiden venter på KI-en før det regnes som at den ikke svarer (FR-28)
  - [ ] Mappene for testdata og fasit (NFR-3)
  - [ ] Hvordan testmodus kjenner igjen testdataene, også med ekstra mellomrom (FR-34)
  - [ ] Ett programmeringsspråk for hele nettsiden? (enklere installasjon for sensor, NFR-8)
  - [ ] Linter og formatterer som CI sjekker
  - Fra UX:
  - [ ] Bestemme om logoskriften Baloo 2 lastes fra Google Fonts eller ligger som fil i prosjektet
  - [ ] Bestemme hva nettleserens egen tilbakeknapp gjør midt i en søknad
  - [ ] Formatet på KI-svaret i Korrektur (setningspar `{ny, gammel}`)
  - [ ] Arbeidsgiveren i filnavnet som et ekstra felt i KI-svaret med nøkkelordene
  - [ ] Om «Nytt forslag» i testmodus gir det samme ferdige brevet eller et annet
  - [ ] Automatisk utlogging: helst ikke, men hvis ja, varsle minst 20 sekunder før
  - [ ] Krav uten skjermbilde: FR-15, avrundingen i FR-17, FR-24, FR-37, FR-38
  - To raske prøver før stories lages (fra vurderingen av hva som blir vanskelig å kode, 3. november):
  - [ ] Lese en fiktiv CV med to kolonner med PDF-biblioteket og se hva som kommer ut
  - [ ] Prøve Korrektur-prompten én gang og se om setningsparene `{ny, gammel}` blir gode
  - Vanskelig å kode, ha i bakhodet (🔴 krevende, 🟡 middels):
  - [ ] 🔴 Markerte endringer i Korrektur (FR-23): KI-en kan slå sammen, dele opp eller fjerne setninger. Løsning: setningspar `{ny, gammel}`. Reserve: nødlisten punkt 4
  - [ ] 🔴 Lese tekst fra PDF (FR-8, FR-11): kolonner og tabeller kan komme i feil rekkefølge, og «uleselig» er vanskelig å avgjøre. Løsning: velge bibliotek, eller kjent begrensning. Reserve: innlimt tekst, nødlisten punkt 5
  - [ ] 🔴 Testmodus kjenner igjen testdataene (FR-34): PDF-tekst og innlimt tekst blir ikke helt like. Løsning: «vaske» teksten (små bokstaver, mellomrom) før sammenligning
  - [ ] 🟡 Svar fra KI-en i fast format (FR-28): bruke JSON og sjekke svaret
  - [ ] 🟡 Word og PDF ut (FR-29): PDF trenger en skrifttype med æ, ø og å
  - [ ] 🟡 Telleregelen med æøå (FR-17): i JavaScript regnes ikke «ø» som bokstav når koden finner hele ord, Python gjør det riktig. Tas med når språket velges
  - Fra konkurrentanalysen:
  - [ ] Vurdere en kort grunn ved hver endring i Korrektur, som Kickresumes «What we changed» (passer det med setningsparene {ny, gammel}?)
- [ ] Epics og stories
  - [x] Holde omfanget stramt: 38 krav og bare helger igjen. Bruk nødlisten i PRD-en (del 4) tidlig heller enn sent (løst: sjekkpunkter 22. og 29. november i risikotabellen i PRD-en)
- [ ] Suksesskriteriene (bekymringer fra gjennomgangen av brief og PRD 3. november)
  - [x] Bestemme på forhånd hva jeg gjør hvis et kriterium med ekte KI (1, 3, 11, 12) feiler én av tre ganger, og skrive det ærlig i testplanen (løst: plan B i innledningen til del 5 i PRD-en)
  - [ ] Stories: når de ekte KI-svarene til testmodus lages (FR-38), kjøre hver prompt tre ganger og sjekke mot fasiten, så kriterium 1, 3, 11 og 12 testes tidlig
  - [ ] Testdata: lage CV-er med tydelige hull (for eksempel «førerkort» eller «SQL»), ikke grensetilfeller, særlig for gap-analysen (kriterium 1)
  - [x] Skrive fasiten for gap-analysen nøye, med en kort begrunnelse per krav (om et krav er dekket, er en skjønnsvurdering) (løst: lagt inn som krav i NFR-3 i PRD-en)
  - [ ] Avtale med en kollega innen 20. november for kriterium 13 (testen gjøres etter 29. november, gjerne helgen 5.–6. desember, på Teams eller med skjermbilde)
  - [x] Vurdere å legge til en kilde på at mange arbeidsgivere bruker ATS (problembeskrivelsen i brief og PRD) (løst: Harvard Business School-kilde under Kilder i begge)
- [x] Konkurrentanalyse av Jobscan, Rezi, Teal og Kickresume (anbefalt av faglærer, gjort etter UX, ligger i 4-konkurrentanalyse/)

## Før innlevering

## Hvis tid

- [ ] Mørk modus (fargene er lagret som variabler, så den kan legges til uten å bygge om)
- [ ] Prøve Teal, Rezi og Kickresume selv for å bekrefte funnene i konkurrentanalysen om det som mangler hos dem

## Under kodingen

- [ ] Sjekkpunkt søndag 22. november: virker innloggingen, telleregelen med tester og innleggingssiden? Hvis ikke, kutt punkt 1–3 på nødlisten (PRD del 4 og 6)
- [ ] Sjekkpunkt søndag 29. november: virker hele flyten i testmodus? Hvis ikke, kutt punkt 4–5 på nødlisten

## Før innlevering

- [ ] Fylle ut README-seksjonene merket «kommer» (installasjon, testdata og tester, skjermbilder, mappestruktur), og legge til nye kjente begrensninger (NFR-8)
- [ ] Sjekke på nytt at ingen av konkurrentene har fått norsk eller korrektur av eget brev med markerte endringer (konkurrentanalysen sier sjekk fra 7. november)
- [ ] Lage en kort prompt-logg med de viktigste valgene for hele prosjektet, til sensor (den lange loggen beholdes)
  - Ta med `3-ux/mine-valg-og-ki-feil.md` (UX er ferdig der), og legg til brief, PRD, arkitektur og koding
