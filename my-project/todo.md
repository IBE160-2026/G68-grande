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
- [x] Bestemme lista over typiske KI-fraser (FR-24, ligger i addendum) (bestemt 7. november: 17 fraser i fem grupper)

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
- [x] Arkitektur (ferdig 4. november, se `5-arkitektur/`)
  - Fra PRD-en og addendumet:
  - [x] Grensen for filstørrelse (FR-12), så UX-teksten «høyst X MB» får et tall (løst: 5 MB)
  - [x] Hvordan teksten leses ut av PDF-filer (FR-8, FR-11) (løst: pypdf)
  - [x] Få og godt dokumenterte biblioteker for å lese PDF og lage Word og PDF, med begrunnelse (fra faglærer) (løst: pypdf, python-docx, fpdf2)
  - [x] CV-er med kolonner og tabeller: støtte dem eller skrive det som kjent begrensning (jeg vil prøve å støtte tabeller) (løst: prøves i første PDF-story, ellers kjent begrensning)
  - [x] KI-tjeneste (NFR-11): Claude-modell, kostnad og hvordan API-nøkkelen holdes utenfor Git (løst: Opus 5.5, tak 250 kr, nøkkelen i `.env`)
  - [x] Hvor lenge nettsiden venter på KI-en før det regnes som at den ikke svarer (FR-28) (løst: 90 s og ett nytt forsøk)
  - [x] Mappene for testdata og fasit (NFR-3)
  - [x] Hvordan testmodus kjenner igjen testdataene, også med ekstra mellomrom (FR-34) (løst: vasket tekst, AD-10)
  - [x] Ett programmeringsspråk for hele nettsiden? (enklere installasjon for sensor, NFR-8) (løst: Python)
  - [x] Linter og formatterer som CI sjekker (løst: ruff og pytest i GitHub Actions)
  - Fra UX:
  - [x] Bestemme om logoskriften Baloo 2 lastes fra Google Fonts eller ligger som fil i prosjektet (løst: fil i prosjektet)
  - [x] Bestemme hva nettleserens egen tilbakeknapp gjør midt i en søknad (løst: AD-8)
  - [x] Formatet på KI-svaret i Korrektur (setningspar `{ny, gammel}`) (løst: AD-4 og AD-5)
  - [x] Arbeidsgiveren i filnavnet som et ekstra felt i KI-svaret med nøkkelordene
  - [x] Om «Nytt forslag» i testmodus gir det samme ferdige brevet eller et annet (løst: to ferdige brev per testcase)
  - [x] Automatisk utlogging: helst ikke, men hvis ja, varsle minst 20 sekunder før (løst: ingen automatisk utlogging)
  - [x] Krav uten skjermbilde: FR-15, avrundingen i FR-17, FR-24, FR-37, FR-38 (løst: AD-4, AD-6, AD-14)
  - To raske prøver før stories lages (fra vurderingen av hva som blir vanskelig å kode, 3. november):
  - [x] Lese en fiktiv CV med to kolonner med PDF-biblioteket og se hva som kommer ut (gjort 7. november med Ola Nordmann-CV fra Word: æøå riktig, venstre kolonne først og så høyre, ingenting blandet. Overskrift og første linje havner på samme linje, men det går fint for KI-en. Vanlig `extract_text()` holder. Samme dag med Ola Nordmann-CV fra Canva: all tekst og æøå kommer med, og linjer som hører sammen står sammen, men overskriftene havner på feil sted (for eksempel «Personalia» etter utdanningen og «Kurs og sertifiseringer» etter kurset), og layout-modusen ga ingenting. Ingen ny løsning i koden: reserven er innlimt tekst)
  - [ ] README, kjente begrensninger: PDF-lesingen er testet med CV-er fra Word og Canva. Fra Canva kommer all teksten med, men i rotete rekkefølge, så da kan teksten limes inn i stedet (story 8.1)
  - [ ] Når ekte KI kobles på: prøve om KI-en forstår Canva-teksten riktig (hva som er utdanning, jobb og oppsummering) (story 4.4)
  - [x] Prøve Korrektur-prompten én gang og se om setningsparene `{ny, gammel}` blir gode (gjort 7. november i chatten med et fiktivt brev fra Ola Nordmann til Nordlys Data AS: formen fra AD-4 klarer endret, slått sammen, fjernet, ny og uendret, og sjekken «alle `gammel` satt sammen = originalbrevet» gikk gjennom. Funn: når én setning deles i to, blir andre halvdel en «ny setning» med tom `gammel`, selv om innholdet var der fra før. Ikke testet med API-et ennå)
  - [x] Korrektur-prompten: regel om at en setning aldri deles i to oppføringer. Blir en lang setning til to, står begge i samme `ny`. Da betyr «ny setning» bare innhold som er helt nytt (lagt inn i arkitekturen, AD-5, 7. november. Storyen for Korrektur-prompten må følge den)
  - Vanskelig å kode, ha i bakhodet (🔴 krevende, 🟡 middels):
  - [ ] 🔴 Markerte endringer i Korrektur (FR-23): KI-en kan slå sammen, dele opp eller fjerne setninger. Løsning: setningspar `{ny, gammel}`. Reserve: nødlisten punkt 4
  - [ ] 🔴 Lese tekst fra PDF (FR-8, FR-11): kolonner og tabeller kan komme i feil rekkefølge, og «uleselig» er vanskelig å avgjøre. Løsning: velge bibliotek, eller kjent begrensning. Reserve: innlimt tekst, nødlisten punkt 5
  - [ ] 🔴 Testmodus kjenner igjen testdataene (FR-34): PDF-tekst og innlimt tekst blir ikke helt like. Løsning: «vaske» teksten (små bokstaver, mellomrom) før sammenligning
  - [ ] 🟡 Svar fra KI-en i fast format (FR-28): bruke JSON og sjekke svaret
  - [ ] 🟡 Word og PDF ut (FR-29): PDF trenger en skrifttype med æ, ø og å
  - [ ] 🟡 Telleregelen med æøå (FR-17): i JavaScript regnes ikke «ø» som bokstav når koden finner hele ord, Python gjør det riktig. Tas med når språket velges
  - Fra konkurrentanalysen:
  - [x] Vurdere en kort grunn ved hver endring i Korrektur, som Kickresumes «What we changed» (passer det med setningsparene {ny, gammel}?) (løst: «Gjøres hvis det blir tid» i PRD-en)
- [x] Spørre faglærer om publisering på Vercel er et krav, eller om det holder at sensor kjører nettsiden lokalt etter README. Er det et krav: lage en utgave som bare kjører testmodus, mot slutten (arkitekturen må da endres for økt og brukere) (avklart 4. november: ikke et krav, lokal kjøring etter README holder)
- [x] Første kode-story: i `.gitignore` legge til `!.env.example` (regelen `.env.*` skjuler den nå, NFR-2) og `instance/` (databasen, AD-12) (lagt inn i story 1.1. `!.env.example` står allerede i `.gitignore`, så bare `instance/` mangler) (gjort 8. november i story 1.1)
- [ ] Når ekte KI skal kobles på: lage konto i Claude Console (platform.claude.com), kjøpe kreditt (for eksempel 10 dollar) og la auto-reload være AV. Lage API-nøkkel og legge den i `.env` (før story 4.1)
- [x] Epics og stories (ferdig 7. november: 8 epics og 31 stories, se `6-epics-og-stories/`)
  - [x] Holde omfanget stramt: 38 krav og bare helger igjen. Bruk nødlisten i PRD-en (del 4) tidlig heller enn sent (løst: sjekkpunkter 22. og 29. november i risikotabellen i PRD-en)
- [ ] Suksesskriteriene (bekymringer fra gjennomgangen av brief og PRD 3. november)
  - [x] Bestemme på forhånd hva jeg gjør hvis et kriterium med ekte KI (1, 3, 11, 12) feiler én av tre ganger, og skrive det ærlig i testplanen (løst: plan B i innledningen til del 5 i PRD-en)
  - [ ] Stories: når de ekte KI-svarene til testmodus lages (FR-38), kjøre hver prompt tre ganger og sjekke mot fasiten, så kriterium 1, 3, 11 og 12 testes tidlig (story 4.4, 4.5 og 5.2)
  - [ ] Testdata: lage CV-er med tydelige hull (for eksempel «førerkort» eller «SQL»), ikke grensetilfeller, særlig for gap-analysen (kriterium 1) (story 2.2 og 4.5)
  - [x] Skrive fasiten for gap-analysen nøye, med en kort begrunnelse per krav (om et krav er dekket, er en skjønnsvurdering) (løst: lagt inn som krav i NFR-3 i PRD-en)
  - [ ] Avtale med en kollega innen 20. november for kriterium 13 (testen gjøres etter 29. november, gjerne helgen 5.–6. desember, på Teams eller med skjermbilde)
  - [x] Vurdere å legge til en kilde på at mange arbeidsgivere bruker ATS (problembeskrivelsen i brief og PRD) (løst: Harvard Business School-kilde under Kilder i begge)
- [x] Konkurrentanalyse av Jobscan, Rezi, Teal og Kickresume (anbefalt av faglærer, gjort etter UX, ligger i 4-konkurrentanalyse/)

## Før innlevering

## Hvis tid

- [ ] Mørk modus (fargene er lagret som variabler, så den kan legges til uten å bygge om)
- [ ] Prøve Teal, Rezi og Kickresume selv for å bekrefte funnene i konkurrentanalysen om det som mangler hos dem

## Under kodingen

- [x] Sprint planning (`bmad-sprint-planning`) (ferdig 7. november: planen er klar til koding, `sprint-status.yaml` har 8 epics og 31 stories, se `7-sprint-planning/`)
- [x] Story 1.1 med egen branch og PR (`bmad-build`). Kopien av `sprint-status.yaml` i `my-project/7-sprint-planning/` oppdateres når en story blir ferdig (ferdig 8. november: PR #2 flettet, CI grønn på Linux og Windows)
- [x] Story 1.2 «Logge inn med testbrukeren» med egen branch og PR (`bmad-build`) (ferdig 8. november: PR #3 flettet, CI grønn på Linux og Windows)
- [x] Story 1.3 «Registrere seg som ny bruker» med egen branch og PR (`bmad-build`) (ferdig 8. november: PR #4 flettet, CI grønn på Linux og Windows)
- [x] Story 1.4 «Logge ut, og bare innloggede kommer inn» med egen branch og PR (`bmad-build`) (ferdig 8. november: PR #5 flettet, CI grønn på Linux og Windows. Epic 1 er ferdig)
- [ ] Etter retrospektiven for epic 1: rette fire småting i en egen PR før story 2.1 (oppryddingen av økten ett sted, innlogget bruker sendes til startsiden fra innloggingen og registreringen, testhjelperne i én fil, og to strengere tester). Se [`9-koding/epic-1-retro-2026-11-08.md`](9-koding/epic-1-retro-2026-11-08.md)
- [ ] Prøve innloggingen, registreringen og startsiden med «Logg ut» ved 320 px, 768 px og 200 % zoom (fra retrospektiven for epic 1)
- [ ] Fra retrospektiven: når en story lover noe om nettleseren (tilbakeknapp, fokus, bredde), skal planen si nøyaktig hva jeg prøver i nettleseren før push. Avvises samme funn i to stories, skal jeg få det som en beslutning
- [ ] Neste steg: story 2.1 «Telleregelen for nøkkelordtreff» med egen branch og PR (`bmad-build`)
- [ ] README, kjente begrensninger: nettsiden har ingen CSRF-beskyttelse, og den må legges til før nettsiden legges på nett (fra kodegjennomgangen av story 1.4, story 8.1)
- [ ] Hvis story 7.2 (PDF ut) kuttes: kriterium 5 sier at både .docx og PDF kan åpnes, så kriteriet må da endres, slik PRD-en allerede sier for punkt 5 på nødlisten
- [ ] Story 6.1: prøve pypdf på en fiktiv CV med tabell (7. november ble bare CV-er med kolonner prøvd)
- [ ] Story 2.5 er den største: del den i to hvis den tar mer enn en helgedag
- [ ] Test som sjekker at ingen av KI-frasene i addendum står i brevene (story 4.4 og 5.2)
- [ ] Sjekkpunkt søndag 22. november: virker innloggingen, telleregelen med tester og innleggingssiden? Hvis ikke, kutt punkt 1–3 på nødlisten (PRD del 4 og 6)
- [ ] Sjekkpunkt søndag 29. november: virker hele flyten i testmodus? Hvis ikke, kutt punkt 4–5 på nødlisten

## Før innlevering

- [ ] Refleksjonsrapporten (del 2, teller 30 % av karakteren). Sensorveiledningen for del 1 sier bare at refleksjonen over prosessen vurderes i del 2
  - [x] Få malen for rapporten (fått 7. november, forventet lengde 3000–5000 ord. Malen og notatene ligger bare på min PC, fordi de hører til del 2)
  - [ ] Samle stoff underveis i notatene (KI-feil fra PR-ene, tekniske utfordringer, lærdommer)
  - [ ] Spørre faglærer om fristen for rapporten, hvis den ikke står noe sted
  - [ ] Sette av tid til rapporten i planen (uke 50 er allerede satt av til testplan, README og buffer, og eksamen i et annet fag er 11. desember)
  - Råmateriale som allerede finnes: prompt-loggen, «mine valg og KI-feil» for hvert dokument, beslutningsloggene og sesjonsloggene
- [ ] Fylle ut README-seksjonene merket «kommer» (installasjon, testdata og tester, skjermbilder, mappestruktur), og legge til nye kjente begrensninger (NFR-8)
- [ ] Sjekke på nytt at ingen av konkurrentene har fått norsk eller korrektur av eget brev med markerte endringer (konkurrentanalysen sier sjekk fra 7. november)
- [ ] Lage en kort prompt-logg med de viktigste valgene for hele prosjektet, til sensor (den lange loggen beholdes)
  - Ta med `3-ux/mine-valg-og-ki-feil.md` (UX er ferdig der), og legg til brief, PRD, arkitektur og koding
