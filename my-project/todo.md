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
  - [x] README, kjente begrensninger: PDF-lesingen er testet med CV-er fra Word og Canva. Fra Canva kommer all teksten med, men i rotete rekkefølge, så da kan teksten limes inn i stedet (story 8.1) (gjort: står i README under «Kjente begrensninger», sjekket 17. november i retro 6)
  - [x] Når ekte KI kobles på: prøve om KI-en forstår Canva-teksten riktig (hva som er utdanning, jobb og oppsummering) (story 4.4) (gjort 14. november: riktig, se testplanen)
  - [x] Prøve Korrektur-prompten én gang og se om setningsparene `{ny, gammel}` blir gode (gjort 7. november i chatten med et fiktivt brev fra Ola Nordmann til Nordlys Data AS: formen fra AD-4 klarer endret, slått sammen, fjernet, ny og uendret, og sjekken «alle `gammel` satt sammen = originalbrevet» gikk gjennom. Funn: når én setning deles i to, blir andre halvdel en «ny setning» med tom `gammel`, selv om innholdet var der fra før. Ikke testet med API-et ennå)
  - [x] Korrektur-prompten: regel om at en setning aldri deles i to oppføringer. Blir en lang setning til to, står begge i samme `ny`. Da betyr «ny setning» bare innhold som er helt nytt (lagt inn i arkitekturen, AD-5, 7. november. Storyen for Korrektur-prompten må følge den)
  - Vanskelig å kode, ha i bakhodet (🔴 krevende, 🟡 middels):
  - [x] 🔴 Markerte endringer i Korrektur (FR-23): KI-en kan slå sammen, dele opp eller fjerne setninger. Løsning: setningspar `{ny, gammel}`. Reserve: nødlisten punkt 4 (løst 15. november i story 5.3, PR #37)
  - [ ] 🔴 Lese tekst fra PDF (FR-8, FR-11): kolonner og tabeller kan komme i feil rekkefølge, og «uleselig» er vanskelig å avgjøre. Løsning: velge bibliotek, eller kjent begrensning. Reserve: innlimt tekst, nødlisten punkt 5
  - [ ] 🔴 Testmodus kjenner igjen testdataene (FR-34): PDF-tekst og innlimt tekst blir ikke helt like. Løsning: «vaske» teksten (små bokstaver, mellomrom) før sammenligning
  - [ ] 🟡 Svar fra KI-en i fast format (FR-28): bruke JSON og sjekke svaret
  - [ ] 🟡 Word og PDF ut (FR-29): PDF trenger en skrifttype med æ, ø og å
  - [ ] 🟡 Telleregelen med æøå (FR-17): i JavaScript regnes ikke «ø» som bokstav når koden finner hele ord, Python gjør det riktig. Tas med når språket velges
  - Fra konkurrentanalysen:
  - [x] Vurdere en kort grunn ved hver endring i Korrektur, som Kickresumes «What we changed» (passer det med setningsparene {ny, gammel}?) (løst: «Gjøres hvis det blir tid» i PRD-en)
- [x] Spørre faglærer om publisering på Vercel er et krav, eller om det holder at sensor kjører nettsiden lokalt etter README. Er det et krav: lage en utgave som bare kjører testmodus, mot slutten (arkitekturen må da endres for økt og brukere) (avklart 4. november: ikke et krav, lokal kjøring etter README holder)
- [x] Første kode-story: i `.gitignore` legge til `!.env.example` (regelen `.env.*` skjuler den nå, NFR-2) og `instance/` (databasen, AD-12) (lagt inn i story 1.1. `!.env.example` står allerede i `.gitignore`, så bare `instance/` mangler) (gjort 8. november i story 1.1)
- [x] Når ekte KI skal kobles på: lage konto i Claude Console (platform.claude.com), kjøpe kreditt (for eksempel 10 dollar) og la auto-reload være AV. Lage API-nøkkel og legge den i `.env` (før story 4.3, der ekte KI prøves første gang. Story 4.1 og 4.2 trenger den ikke, fordi testene bruker en falsk Claude-klient) (gjort 13. november: konto som individuell, kreditt kjøpt med auto-reload av, nøkkel i `backend/.env`, som Git overser)
- [x] Epics og stories (ferdig 7. november: 8 epics og 31 stories, se `6-epics-og-stories/`)
  - [x] Holde omfanget stramt: 38 krav og bare helger igjen. Bruk nødlisten i PRD-en (del 4) tidlig heller enn sent (løst: sjekkpunkter 22. og 29. november i risikotabellen i PRD-en)
- [ ] Suksesskriteriene (bekymringer fra gjennomgangen av brief og PRD 3. november)
  - [x] Bestemme på forhånd hva jeg gjør hvis et kriterium med ekte KI (1, 3, 11, 12) feiler én av tre ganger, og skrive det ærlig i testplanen (løst: plan B i innledningen til del 5 i PRD-en)
  - [x] Stories: når de ekte KI-svarene til testmodus lages (FR-38), kjøre hver prompt tre ganger og sjekke mot fasiten, så kriterium 1, 3, 11 og 12 testes tidlig (story 4.4, 4.5 og 5.2) (4.4 gjort 14. november for kriterium 1, 11 og 14. 4.5 gjort 14. november for case 2 og kriterium 3. 5.2.2 gjort 15. november for kriterium 12: bestått i alle tre kjøringene uten plan B)
  - [x] Testdata: lage CV-er med tydelige hull (for eksempel «førerkort» eller «SQL»), ikke grensetilfeller, særlig for gap-analysen (kriterium 1) (story 2.2 og 4.5) (case 2 laget 14. november: hull i Power BI, regnskapsprogram, lønnskjøring og Python)
  - [x] Skrive fasiten for gap-analysen nøye, med en kort begrunnelse per krav (om et krav er dekket, er en skjønnsvurdering) (løst: lagt inn som krav i NFR-3 i PRD-en)
  - [x] Avtale med en kollega innen 20. november for kriterium 13 (testen gjøres etter 29. november, gjerne helgen 5.–6. desember, på Teams eller med skjermbilde) (løst 20. november: jeg har flere som kan prøve nettsiden)
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
- [x] Etter retrospektiven for epic 1: rette fire småting i en egen PR før story 2.1 (oppryddingen av økten ett sted, innlogget bruker sendes til startsiden fra innloggingen og registreringen, testhjelperne i én fil, og to strengere tester). Se [`9-koding/epic-1-retro-2026-11-08.md`](9-koding/epic-1-retro-2026-11-08.md) (ferdig 8. november: PR #6 flettet, CI grønn på Linux og Windows, 152 tester)
- [x] Prøve innloggingen, registreringen og startsiden med «Logg ut» ved 320 px, 768 px og 200 % zoom (fra retrospektiven for epic 1) (gjort 8. november: alt ser riktig ut)
- [x] Fra retrospektiven: når en story lover noe om nettleseren (tilbakeknapp, fokus, bredde), skal planen si nøyaktig hva jeg prøver i nettleseren før push. Avvises samme funn i to stories, skal jeg få det som en beslutning (gjort i hele epic 2, bekreftet i retrospektiven 10. november)
- [x] Story 2.1 «Telleregelen for nøkkelordtreff» med egen branch og PR (`bmad-build`) (ferdig 8. november: PR #7 flettet, CI grønn på Linux og Windows, 175 tester)
- [x] Story 2.2 «Fiktive testdata og fasit for første testcase» med egen branch og PR (`bmad-build`). Claude lager utkastet, jeg godkjenner innholdet (ferdig 8. november: PR #8 flettet, CI grønn på Linux og Windows, 182 tester)
- [x] Story 2.3 «Testmodus kjenner igjen testdataene» med egen branch og PR (`bmad-build`) (ferdig 9. november: PR #9 flettet, CI grønn på Linux og Windows, 231 tester)
- [x] Story 2.4 «Startsiden får testmodus og knappen videre, og modusvalget lages» med egen branch og PR (`bmad-build`). Delt i to 9. november (ferdig 9. november):
  - [x] Story 2.4.1 «Flyten fra startsiden til innleggingen» (ferdig 9. november: PR #10 flettet, CI grønn på Linux og Windows, 272 tester)
  - [x] Story 2.4.2 «Testmodus på startsiden og merkelappen» (ferdig 9. november: PR #11 flettet, CI grønn på Linux og Windows, 288 tester)
- [x] Story 2.5 «Lime inn CV og stillingsannonse» med egen branch og PR (`bmad-build`). Delt i to 9. november (ferdig 9. november):
  - [x] Story 2.5.1 «Innleggingssiden» (ferdig 9. november: PR #12 flettet, CI grønn på Linux og Windows, 333 tester)
  - [x] Story 2.5.2 «Analysen og første resultatside» (ferdig 9. november: PR #13 flettet, CI grønn på Linux og Windows, 361 tester)
- [x] Story 2.6 «Hele resultatsiden med forklaringer og «Tilbake»» med egen branch og PR (`bmad-build`) (ferdig 10. november: PR #14 flettet, CI grønn på Linux og Windows, 389 tester)
- [x] Story 2.7 «Ventetegn og feil fra KI-en» med egen branch og PR (`bmad-build`). Den løser også «to trykk samtidig» (retro-punkt 7). Delt i to 10. november:
  - [x] Story 2.7.1 «Ventetegn og «opptatt»» (ferdig 10. november: PR #15 flettet, CI grønn på Linux og Windows, 422 tester)
  - [x] Story 2.7.2 «KI-feilboksen med «Prøv på nytt»» (ferdig 10. november: PR #17 flettet, CI grønn på Linux og Windows, 429 tester)
- [x] Etter retrospektiven for epic 2: rette fire ting i en egen PR før story 3.1. Se [`9-koding/epic-2-retro-2026-11-10.md`](9-koding/epic-2-retro-2026-11-10.md): (ferdig 10. november: PR #18 flettet, CI grønn på Linux og Windows, 441 tester)
  - [x] Startsiden i en annen fane mens KI-en jobber: den nye søknaden vinner (bestemt 10. november)
  - [x] Test som sjekker at KI-en kalles på nytt etter «Tilbake» fra resultatsiden
  - [x] Utlogging i en annen fane midt i «Sjekk CV-en min» gir innloggingen, ikke en feilside (bestemt 10. november)
  - [x] Hjelpeteksten sier `backend/testdata/` i koden, UX, epics og README (bestemt 10. november). Jeg ser på feilteksten «… fra mappen testdata/» i PR-en (bestemt etter prøvingen: feilteksten sier også `backend/testdata/`)
- [ ] Prøve resultatsiden og ventetegnet ved 768 og 1280 px (fra retrospektiven for epic 2)
- [ ] Fra retrospektiven for epic 2: punkter som skal inn i senere stories (4.5 flere testcaser, epic 4 valg av KI og tidsgrense, 3.1, 6.1 og 7.3). Står i retro-dokumentet (4.5 gjort 14. november i PR #28) (7.3 gjort 19. november: samme vask som testmodus, bestemt av meg)
- [x] Story 3.1 «Se søknadsbrevet» med egen branch og PR (`bmad-build`) (ferdig 11. november: PR #19 flettet, CI grønn på Linux og Windows, 512 tester. Testbrevet er godkjent som plassholder til epic 4)
- [x] Story 3.2 «Laste ned brevet som Word» med egen branch og PR (`bmad-build`) (ferdig 11. november: PR #20 flettet, 549 tester. Prøvd i nettleseren og i Word. Feilboksen har ikke «Brevet er ikke borte.»)
- [x] Story 3.3 «Vinduet etter nedlasting» med egen branch og PR (`bmad-build`) (ferdig 12. november: PR #21 flettet, CI grønn på Linux og Windows, 560 tester. Prøvd i nettleseren. Fokusringen på «Bli her» ble rettet etter prøvingen)
- [x] Etter retrospektiven for epic 3: rette tre småting i en egen PR før epic 4 (ferdig 12. november: PR #22 flettet, CI grønn på Linux og Windows, 562 tester. Margene er sjekket i Word). Se [`9-koding/epic-3-retro-2026-11-12.md`](9-koding/epic-3-retro-2026-11-12.md):
  - [x] Testen for «Logg ut» på brevsiden ser bare på hjørneraden
  - [x] Testhjelperne samles igjen, og ingen testfil henter fra en annen testfil (en ny test passer på det)
  - [x] Word-fila får 2,5 cm marger rundt hele (bestemt 12. november), og README à jour (status, Word-fila, lenker til retrospektivene)
- [x] Fra retrospektiven for epic 3: brevteksten renses i epic 4, vinduet «Nytt forslag» spør også på resultatsiden i epic 7, og kjente fallgruver (fokusring, høykontrast, svg-høyde) skrives inn i konteksten for epic 4. Filnavnet over midnatt og vinduet som åpnes ved trykket er godtatt for godt (bestemt 12. november) (fallgruvene står i konteksten for epic 4 fra 13. november. Brevteksten renses fra story 4.2. Vinduet spør på resultatsiden fra story 7.1, 17. november)
- [x] Story 4.1 «Koble til Claude for nøkkelord og gap-analyse» med egen branch og PR (`bmad-build`). Nettsiden bruker fortsatt testmodus til 4.3, så det er ingenting nytt å prøve i nettleseren (ferdig 13. november: [PR #23](https://github.com/IBE160-2026/G68-grande/pull/23) flettet, CI grønn på Linux og Windows, 614 tester)
- [x] Story 4.2 «Brevet fra Claude» med egen branch og PR (`bmad-build`). Brevet begynner nå med overskriften «Søknad på stillingen som …», og den er prøvd i nettleseren i testmodus (ferdig 13. november: [PR #24](https://github.com/IBE160-2026/G68-grande/pull/24) flettet, CI grønn på Linux og Windows, 655 tester)
- [x] Story 4.3.1 «Slå av testmodus, med samtykke og KI-merknad» med egen branch og PR (`bmad-build`). Prøve i nettleseren med nøkkel, og kjøre hele flyten én gang med ekte KI på case 1: notere i PR-en hvor lang tid analysen og brevet tar, og sjekke brevet mot sjekklisten i `fasit.md` (ferdig 14. november: [PR #25](https://github.com/IBE160-2026/G68-grande/pull/25) flettet, CI grønn på Linux og Windows, 709 tester. Flyten er prøvd én gang med ekte KI: ca. 3 s + 3 s for analysen, under 42 s for brevet, ca. 0,74 kr. Brevet har nå et avsnitt om studenten som person rett etter overskriften. Tastatur, høykontrast, 320 px og sjekklisten i `fasit.md` er også prøvd, uten feil)
- [x] Story 4.3.2 «Grensene» (høyst 15 000 tegn per felt og høyst 10 KI-kall per søknad), andre halvdel av story 4.3 (delt 13. november) (ferdig 14. november: [PR #26](https://github.com/IBE160-2026/G68-grande/pull/26) flettet, CI grønn på Linux og Windows, 744 tester. Tegngrensen er prøvd i nettleseren. Grensen på KI-kall gjelder bare med ekte KI, og «Nytt forslag» må telles i Epic 7)
- [x] Story 4.4 «Ekte KI-svar i testmodus» med egen branch og PR (`bmad-build`) (ferdig 14. november: [PR #27](https://github.com/IBE160-2026/G68-grande/pull/27) flettet, CI grønn på Linux og Windows, 757 tester. Skriptet `lag_testsvar.py` lager svarene. Tre kjøringer mot fasiten, med plan B for brevet etter runde 1. Kriterium 1, 11 og 14 besto i runde 2, og en søknad koster 0,67–0,93 kr. Testplanen er laget, og testmodus og Canva-CV-en er prøvd i nettleseren)
- [x] Story 4.5 «Et testcase til, og kriterium 3» med egen branch og PR (`bmad-build`) (ferdig 14. november: [PR #28](https://github.com/IBE160-2026/G68-grande/pull/28) flettet, CI grønn på Linux og Windows, 789 tester. Case 2 (økonomi) er laget og godkjent, og testmodus tåler flere caser. Kriterium 1, 11 og 14 besto på case 2, og kriterium 3 besto etter plan B for brevet. Ca. 24 kr. Case 2 er prøvd i nettleseren)
- [x] Retrospektiv for epic 4 (`bmad-retrospective`), valgfri. Alle storyene i epic 4 er ferdige (14. november) (ferdig 14. november: godkjent med åpne punkter, 8 punkter. Se [`9-koding/epic-4-retro-2026-11-14.md`](9-koding/epic-4-retro-2026-11-14.md))
- [x] Etter retrospektiven for epic 4: rettinger før epic 5, delt i to runder (bestemt 14. november). Runde 1 er punktet om KI-kallet (branch `retro-4-rettinger`), og resten tas i en ny runde:
  - [x] KI-kallet på innleggingen og resultatsiden samles i én hjelper (samtykket og valget av KI leser samme innlogging, og utlogging på resultatsiden sender til innloggingen) (ferdig 14. november: [PR #29](https://github.com/IBE160-2026/G68-grande/pull/29) flettet, CI grønn på Linux og Windows, 793 tester. Prøvd i nettleseren med testmodus og ekte KI)
  - [x] Test gjennom det ekte Anthropic-SDK-et, én webtest gjennom `EkteKI`, og sperre mot nettverk i testene (ferdig 14. november: [PR #30](https://github.com/IBE160-2026/G68-grande/pull/30) flettet, CI grønn på Linux og Windows, 798 tester)
  - [x] Småting: `med_nokkel` samles i `hjelpere.py`, gamle kommentarer om «4.3», README-rader og lenke til retrospektiven, kjent begrensning om øktlageret, og de seks gamle branchene slettes (branchene slettet 14. november, på GitHub av meg og på PC-en av KI-en. Resten ferdig 14. november: [PR #31](https://github.com/IBE160-2026/G68-grande/pull/31) flettet, CI grønn på Linux og Windows, 801 tester)
  - [x] Én måling med CV og annonse på nær 15 000 tegn hver (ca. 1 kr) (ferdig 14. november: [PR #32](https://github.com/IBE160-2026/G68-grande/pull/32) flettet, 801 tester. Det lengste kallet tok 25 s, og en søknad kostet 2,60 kr. Kjøringen kostet 3,82 kr, ikke ca. 1 kr. Merknadene om svarene er eget punkt under)
- [ ] Fra retrospektiven for epic 4: `arbeidsgiver` renses før den brukes i filnavnet (story 7.5). «</cv>» i teksten og traceback i skriptet er godtatt for godt, og samtykketeksten står (bestemt 14. november)
- [x] Vurdere de fem merknadene om svarene fra målingen med lange tekster i `testplan.md` (React og TypeScript, egne krav, «krav» om noe som er en fordel, nåtid om en ferdig jobb) (bestemt 15. november: 1–3 godtas, 4 og 5 rettes i brev-prompten)
- [x] Før epic 5: hilsen og navn fra nettsiden, og to nye regler i brev-prompten (ikke «krav» om det som er en fordel, nåtid bare om jobber som pågår), med egen branch og PR (`bmad-build`). Kriteriene for brevet kjøres på nytt med ekte KI, og plan B-regelen prøves på Ingrid-CV-en (branch `brev-hilsen-og-regler`. Kjørt 15. november: kriterium 1, 3, 11 og 14 bestått etter plan B i runde 2, 860 tester, ca. 34 kr. Ferdig 15. november: [PR #33](https://github.com/IBE160-2026/G68-grande/pull/33) flettet, CI grønn på Linux og Windows, prøvd i nettleseren)
- [x] Story 5.1 «Velge Korrektur og legge inn eget brev» med egen branch og PR (`bmad-build`) (ferdig 15. november: [PR #34](https://github.com/IBE160-2026/G68-grande/pull/34) flettet, CI grønn på Linux og Windows, 914 tester, prøvd i nettleseren. Kodegjennomgangen fant en feil i planen, så koden ble laget på nytt i runde 2)
- [x] Story 5.2.1 «Forbedret brev fra KI-en» med egen branch og PR (`bmad-build`) (ferdig 15. november: [PR #35](https://github.com/IBE160-2026/G68-grande/pull/35) flettet, CI grønn på Linux og Windows, 1002 tester, prøvd i nettleseren. Kjøring 1 med ekte KI kostet ca. 1,71 kr)
- [x] Story 5.2.2: kjøring 2 og 3 med ekte KI, sjekk mot «Sjekkliste for Korrektur» (kriterium 12, og 4 på datanivå), plan B ved feil, og resultatet i `testplan.md`. Vurdere også om «Takk for at dere har lest søknaden.» er en omskriving av KI-frasen (ferdig 15. november: [PR #36](https://github.com/IBE160-2026/G68-grande/pull/36) flettet, CI grønn på Linux og Windows. Kriterium 12 bestått i alle tre kjøringene uten plan B, ca. 5,2 kr for hele runden. Setningen er godkjent som omformulering, og prompten rettes ikke. Story 5.2 er ferdig)
- [x] Story 5.3 «Se hva som er endret i Korrektur» med egen branch og PR (`bmad-build`) (ferdig 15. november: [PR #37](https://github.com/IBE160-2026/G68-grande/pull/37) flettet, CI grønn på Linux og Windows, 1029 tester, prøvd i nettleseren. Epic 5 er ferdig)
- [x] Etter story 5.3: bedre flyt i brevet fra Korrektur, med egen branch og PR (`bmad-build`). Brevet leser som setninger på rad uten bindeord (sett av Kristine i nettleseren 15. november). Prompten får lov til å bruke bindeord og slå sammen korte setninger i samme avsnitt, men beholder innhold og rekkefølge. Tre nye kjøringer med ekte KI (ca. 5 kr, Kristine godkjenner først) og ny sjekk mot «Sjekkliste for Korrektur» (kriterium 12) (gjort i runde B etter retro 5, [PR #39](https://github.com/IBE160-2026/G68-grande/pull/39))
- [x] Retrospektiv for epic 5 (`bmad-retrospective`), valgfri. Alle storyene i epic 5 er ferdige (15. november) (ferdig 15. november: godkjent med åpne punkter, 7 punkter. Se [`9-koding/epic-5-retro-2026-11-15.md`](9-koding/epic-5-retro-2026-11-15.md))
- [x] Etter retrospektiven for epic 5, før epic 6: rettinger i tre runder (bestemt 15. november):
  - [x] Runde A: «Du skrev» sjekkes ordrett, og testen av Korrektur-svarene sjekker sjekklisten (ferdig 15. november: [PR #38](https://github.com/IBE160-2026/G68-grande/pull/38) flettet, CI grønn på Linux og Windows, 1038 tester)
  - [x] Runde B: en måling med et langt eget brev og bedre flyt i brevet (Kristine godkjenner kostnaden), og prompten sier at `gammel` kopieres nøyaktig (ferdig 15. november: [PR #39](https://github.com/IBE160-2026/G68-grande/pull/39) flettet, CI grønn på Linux og Windows, 1038 tester. Grensen for brevfeltet er 5 000 tegn, og kriterium 12 besto i runde 2. Rettingen av brevsiden etter nettlesertesten kommer i [PR #40](https://github.com/IBE160-2026/G68-grande/pull/40))
  - [x] Runde C: beslutningene fra epic 5 i `epics.md`, UX-en, epic-konteksten og README, og de fire flettede branchene slettes. Også fra runde B: grensen på 5 000 tegn for brevfeltet i NFR-11 i PRD-en og i epics.md, og at vage vurderinger fjernes i Korrektur (ferdig 16. november: [PR #41](https://github.com/IBE160-2026/G68-grande/pull/41))
- [x] Retrospektiv for epic 6 (`bmad-retrospective`), valgfri. Alle storyene i epic 6 er ferdige (17. november) (ferdig 17. november: godkjent med åpne punkter, 5 punkter. Se [`9-koding/epic-6-retro-2026-11-17.md`](9-koding/epic-6-retro-2026-11-17.md))
- [x] Etter retrospektiven for epic 6, før epic 7: én runde `retro-6-rettinger` med egen branch og PR (bestemt 17. november). PDF-lesingen strammes inn (teksten kuttes ved tegngrensen, mellomrom før linjeskift, unntak per side, pypdf-loggen), testene for filfeltet, rettingen av spec-en og testen for «samme tekst, nytt navn», beslutningene fra 6.1 og 6.2 i `epics.md`, UX-en og AD-9, README-statusen, testplanen, de utsatte punktene merkes som løst, prompt-loggen og oversikten for epic 6, og de to flettede branchene slettes (ferdig 17. november: [PR #44](https://github.com/IBE160-2026/G68-grande/pull/44) flettet, 1 206 tester. Punkt 5 står i KI-ens minne)
  - [x] Prøve i nettleseren at opplasting av PDF virker som før etter retro 6 (`cv.pdf` og `annonse.pdf` fra case 1 gir resultatsiden). Ikke prøvd før fletting, fordi nettsiden ikke kjørte (gjort 17. november etter flettingen: virket, kommentar i PR #44)
- [x] Story 7.1 «Nytt forslag» med egen branch og PR (`bmad-build`) (ferdig 19. november: [PR #45](https://github.com/IBE160-2026/G68-grande/pull/45) flettet, CI grønn på Linux og Windows, 1 244 tester, prøvd i nettleseren)
- [x] Story 7.2 «Laste ned brevet som PDF» med egen branch og PR (`bmad-build`) (ferdig 19. november: [PR #47](https://github.com/IBE160-2026/G68-grande/pull/47) flettet, CI grønn på Linux og Windows, 1 288 tester, prøvd i nettleseren. Skriften er Noto Sans 11 pt)
- [x] Story 7.3 «Gjenbruke nøkkelordlisten når bare CV-en er endret» med egen branch og PR (`bmad-build`) (ferdig 19. november: [PR #48](https://github.com/IBE160-2026/G68-grande/pull/48) flettet, CI grønn på Linux og Windows, 1 305 tester, prøvd i nettleseren. Annonsen sammenlignes med samme vask som testmodus)
- [x] Story 7.4 «Pynt: fyrverkeri og bevegelse» med egen branch og PR (`bmad-build`) (ferdig 20. november: [PR #49](https://github.com/IBE160-2026/G68-grande/pull/49) flettet, CI grønn på Linux og Windows, 1 319 tester, prøvd i nettleseren. Ikke fyrverkeri ved feilboks eller i høykontrast)
- [x] Story 7.5 «Logg ut før nedlasting, og arbeidsgiver i filnavnet» med egen branch og PR (`bmad-build`) (ferdig 21. november: [PR #50](https://github.com/IBE160-2026/G68-grande/pull/50) flettet, CI grønn på Linux og Windows, 1 385 tester, prøvd i nettleseren. Arbeidsgiveren renses i filnavnet)
- [x] Egen tekst i vinduet «Nytt forslag» på resultatsiden, der brevet ikke vises: «Du har alt et brev. Det blir slettet hvis du trykker på «Ja, lag nytt forslag».» (bestemt 19. november). Brevsiden beholder sin tekst (ferdig 19. november: [PR #46](https://github.com/IBE160-2026/G68-grande/pull/46) flettet, CI grønn på Linux og Windows, 1 246 tester, prøvd i nettleseren)
- [x] Retrospektiv for epic 7 (`bmad-retrospective`), valgfri. Alle storyene i epic 7 er ferdige (21. november) (ferdig 21. november: godkjent med åpne punkter, 4 punkter. Se [`9-koding/epic-7-retro-2026-11-21.md`](9-koding/epic-7-retro-2026-11-21.md))
- [x] Etter retrospektiven for epic 7, før epic 8: én runde `retro-7-rettinger` med egen branch og PR (bestemt 21. november). En test for advarselen før utlogging når «Nytt forslag» feilet, Word-nedlastingen skjuler ikke feilboksen for PDF, prosentlinjen står stille når resultatsiden har en feilmelding, to rettinger av tekster i koden, beslutningene fra 7.2–7.5 i `epics.md`, UX-en og arkitekturen, README (statuslinja og tre kjente begrensninger), oversikten for spec 7.2–7.5, epic-konteksten og `issues.md` (koden, testene og papirene er gjort på branchen 21. november, 1 392 tester består. Prøvd i nettleseren av Kristine 21. november: «ser bra ut». Ferdig 21. november: [PR #51](https://github.com/IBE160-2026/G68-grande/pull/51) flettet, CI grønn på Linux og Windows)
- [x] Epic 7: med lange tekster koster en søknad med «Nytt forslag» 3,82 kr, over målet på 3 kr. Bestemme om det er greit (bestemt 17. november: godtatt. Grensen på 10 KI-kall per søknad og taket på 250 kr gjelder)
- [x] Retro-punkt 7: «to trykk på «Sjekk CV-en min» samtidig, det siste vinner» er avvist i både 2.5.1 og 2.5.2. Bestemme om låsingen av knappen i story 2.7 skal løse det (forslaget), eller om noe gjøres nå (bestemt 9. november: story 2.7 løser det)
- [x] Epic 4: tomme punkter i KI-svar fjernes, og KI-feil logges (oppgaven og feiltypen, aldri CV eller annonse) (fra kodegjennomgangen av story 2.5.2 og 2.6) (KI-feil logges fra story 4.1. Tomme punkter fjernes i 4.2, og tom arbeidsgiver blir «ingen») (gjort 13. november)
- [x] Epic 4: grensene fra NFR-11 i PRD-en (tilbakemeldingen på PRD-en, 12. november). Høyst 15 000 tegn per innleggingsfelt, med egen feilmelding. Høyst 10 KI-kall per søknad, medregnet «Prøv på nytt» og «Nytt forslag», med en melding etterpå. Antallet tokens inn og ut logges for hvert KI-kall (aldri teksten), og testplanen viser tokens og kroner per fullført søknad (mål: under 3 kr) (tokens og pris logges fra story 4.1. Grensene står i story 4.3 og testplanen i 4.4 i epics fra 13. november. Story 4.3 er delt, og grensene er story 4.3.2) (grensene ferdig 14. november i PR #26, tokens og kroner per søknad i testplanen i PR #27)
- [x] Epic 4: nøkkelordlisten fra KI-en (FR-15 og suksesskriterium 14, fra tilbakemeldingen på PRD-en). Instruksen ber om 8–20 nøkkelord på 1–3 ord, kontrollen av KI-svaret gir «ubrukelig» når listen er tom eller har mer enn 30, og fasiten for hver testcase markerer hvilke nøkkelord som er viktige (instruksen og kontrollen er gjort i story 4.1. Fasiten står i story 4.4 og 4.5 i epics fra 13. november) (case 1 gjort 14. november i PR #27, case 2 i PR #28)
- [ ] Story 8.2: ingen automatisk test kjører `innlegging.js`, `info.js` («i»-boksen), `vente.js` (ventetegnet og «Prøv på nytt») eller `nedlasting.js` (den grønne knappen og vinduet etter nedlasting) eller `endringer.js` («Du skrev» i Korrektur) eller `bekreft.js` (vinduet «Vil du ha et nytt forslag?» og vinduet «Du har ikke lastet ned brevet.») eller `fyrverkeri.js` (fyrverkeriet på brevsiden) i en nettleser, eller at vinduet etter nedlasting viser `.pdf`-filnavnet etter «Last ned som PDF». Vurdere nettlesertester, ellers prøves de for hånd i hver PR (fra kodegjennomgangen av story 2.5.1, 2.6, 2.7.1, 2.7.2, 3.2, 3.3, 5.3, 7.1, 7.2, 7.4 og 7.5). Står som [issue #16](https://github.com/IBE160-2026/G68-grande/issues/16): skriv «Closes #16» i PR-en for story 8.2
- [x] Story 6.1: sjekke om tekst fra PDF har æøå som to tegn, myke bindestreker eller usynlige mellomrom, som gjør at telleregelen ikke gir treff (fra kodegjennomgangen av story 2.1) (sjekket 16. november i story 6.1: PDF-er fra Word har ingen slike tegn. Teksten fra PDF renses likevel, for Canva og Mac er ikke målt)
- [x] README, kjente begrensninger: bestemme om «korte nøkkelord gir ikke treff inne i lengre ord, for eksempel «SQL» i «MySQL»» skal inn (fra kodegjennomgangen av story 2.1, story 8.1) (bestemt 21. november: tatt med i punktet om telleregelen i README, story 8.1)
- [x] README, kjente begrensninger: nettsiden har ingen CSRF-beskyttelse, og den må legges til før nettsiden legges på nett (fra kodegjennomgangen av story 1.4, story 8.1) (gjort 21. november i story 8.1. I tillegg er `SESSION_COOKIE_SAMESITE="Lax"` satt i `create_app`)
- [x] Hvis story 7.2 (PDF ut) kuttes: kriterium 5 sier at både .docx og PDF kan åpnes, så kriteriet må da endres, slik PRD-en allerede sier for punkt 5 på nødlisten (ikke kuttet: story 7.2 ble ferdig 19. november, så kriterium 5 står som før)
- [x] Story 6.1: prøve pypdf på en fiktiv CV med tabell (7. november ble bare CV-er med kolonner prøvd) (prøvd 16. november i story 6.1: teksten kom i riktig rekkefølge, så tabeller blir ikke en kjent begrensning. Se testplan.md)
- [x] Story 2.5 er den største: del den i to hvis den tar mer enn en helgedag (delt i 2.5.1 og 2.5.2 9. november, fordi spec-en var for lang)
- [x] Test som sjekker at ingen av KI-frasene i addendum står i brevene (story 4.4 og 5.2) (4.4 gjort 14. november: `brev-1.json` og `brev-2.json`. 5.2.1 gjort 15. november: `korrektur-1.json` og `korrektur-2.json`)
- [x] Sjekkpunkt søndag 22. november: virker innloggingen, telleregelen med tester og innleggingssiden? Hvis ikke, kutt punkt 1–3 på nødlisten (PRD del 4 og 6) (nådd alt 12. november: epic 1 og 2 er ferdige)
- [x] Sjekkpunkt søndag 29. november: virker hele flyten i testmodus? Hvis ikke, kutt punkt 4–5 på nødlisten (nådd alt 12. november: epic 1–3 er ferdige, ingenting kuttes)

## Før innlevering

- [ ] Refleksjonsrapporten (del 2, teller 30 % av karakteren). Sensorveiledningen for del 1 sier bare at refleksjonen over prosessen vurderes i del 2
  - [x] Få malen for rapporten (fått 7. november, forventet lengde 3000–5000 ord. Malen og notatene ligger bare på min PC, fordi de hører til del 2)
  - [ ] Samle stoff underveis i notatene (KI-feil fra PR-ene, tekniske utfordringer, lærdommer)
  - [ ] Spørre faglærer om fristen for rapporten, hvis den ikke står noe sted
  - [ ] Sette av tid til rapporten i planen (uke 50 er allerede satt av til testplan, README og buffer, og eksamen i et annet fag er 11. desember)
  - Råmateriale som allerede finnes: prompt-loggen, «mine valg og KI-feil» for hvert dokument, beslutningsloggene og sesjonsloggene
- [ ] Fylle ut README-seksjonene merket «kommer» (installasjon, testdata og tester, skjermbilder, mappestruktur), og legge til nye kjente begrensninger (NFR-8) (tekstene er fylt ut 21. november i story 8.1. Gjenstår bare de tre skjermbildene i `my-project/skjermbilder/`, som Kristine tar med ekte KI)
- [ ] Sjekke på nytt at ingen av konkurrentene har fått norsk eller korrektur av eget brev med markerte endringer (konkurrentanalysen sier sjekk fra 7. november)
- [ ] Lage en kort prompt-logg med de viktigste valgene for hele prosjektet, til sensor (den lange loggen beholdes)
  - Ta med `3-ux/mine-valg-og-ki-feil.md` (UX er ferdig der), og legg til brief, PRD, arkitektur og koding
