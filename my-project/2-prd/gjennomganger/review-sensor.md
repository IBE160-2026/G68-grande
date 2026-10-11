# Sensor-gjennomgang av PRD: Søknadsassistenten

- **Lest mot:** `Sensorveiledning.pdf` (IBE160, del 1, høst 2026, 7 sider)
- **Dokumenter:** `prd.md`, `addendum.md`, `reconcile-sensorveiledning.md`, `.memlog.md`
- **Dato:** 2026-10-11
- **Avgrensning:** Funnene H1–H8 i `reconcile-sensorveiledning.md` er allerede behandlet (memlog linje 62–84) og gjentas ikke. Bevisste valg i memloggen (kuttlisten, «nettside», testmodus uten API-nøkkel, ingen video osv.) regnes ikke som feil, med mindre de faktisk kan koste karakter.

## Samlet vurdering

Som sensor ville jeg blitt positivt overrasket over denne PRD-en. Den er konkret, ærlig (for eksempel «Den ærlige begrensningen» og de kjente begrensningene i telleregelen), har nummererte krav som kan spores videre, en begrunnet kuttliste og en nødliste, og memloggen viser at dokumentet faktisk er jobbet med over flere dager. Produktsiden av sensorveiledningen (kriterium 2, 4, 6 og 7) er godt dekket, og testmodus, FR-38 og NFR-8 gjør at sensor kan få nettsiden i gang uten API-nøkkel. Jeg fant **ingen kritiske feil**. Svakheten ligger et annet sted: PRD-en planlegger *produktet* godt, men sier lite om *hvordan kodingen skal foregå*. Det er nettopp det kriterium 1 (30 %) og kriterium 3 (15 %) måler, og de teller til sammen 45 %. Det mangler en tidsplan med datoer, en plan for branches, pull requests og kodegjennomgang, og de automatiske testene dekker bare en liten del av logikken. Hvis du følger PRD-en slik den er nå, ligger du an til omtrent B på produktkriteriene, men bare C på prosess og testing. De tre høye funnene under er billige å rette og kan løfte deg et helt trinn.

**Antall funn:** kritisk 0 · høy 3 · middels 4 · lav 4

---

## Høy

### S1. Ingen tidsplan med datoer, og nødlisten har ingen fast utløser

- **Kriterium:** 1 Prosess og KI-styring (30 %), s. 2: «Commit-historikk: jevn utvikling over tid fremfor én stor commit før fristen». Varseltegn s. 6: «Hele eller nesten hele koden er lagt inn i én eller noen få commits rett før fristen.» Også kriterium 2 (20 %), s. 3: «At kjerneflytene … fungerer fra start til slutt.»
- **Hvor i PRD:** Del 6, risiko 2: «Blir tiden knapp, kuttes flere funksjoner som ikke er en del av kjerneflyten, i rekkefølgen i nødlisten under».
- **Alvorlighet:** høy
- **Merknad:** Fristen er ca. 9. desember, og PRD, UX, arkitektur og epics gjenstår fortsatt før kodingen starter (se `todo.md`). Da er det kanskje 5–6 uker igjen til selve kodingen. «Blir tiden knapp» er noe man ofte oppdager for sent når man jobber alene. Uten datoer har du ingen fast dag der du må bestemme deg for å kutte, og risikoen er at mye av koden kommer i de siste ukene. Det er akkurat det sensor ser etter i commit-historikken.
- **Forslag:** Legg til en kort tabell «Milepæler» under risiko, for eksempel:
  - UX, arkitektur og epics/stories ferdig: ca. 25. oktober
  - Innlogging og telleregel med tester ferdig: ca. 1. november
  - Hele kjerneflyten i testmodus: ca. 15. november
  - Ekte KI koblet på: ca. 22. november
  - Funksjonsstopp (bare feilretting, README, testplan): ca. 1. desember
  - README testet på en ren klone: ca. 5. desember

  Skriv også i risiko 2: «Hvis en milepæl er mer enn tre dager forsinket, kuttes neste punkt på nødlisten.» Da blir nødlisten en regel og ikke bare en intensjon.

### S2. Arbeidsflyt og kodegjennomgang under kodingen er ikke planlagt

- **Kriterium:** 1 (30 %), s. 2: «Arbeidsflyt: bruk av branches, pull requests, issues eller tilsvarende for å organisere arbeidet» og «Sporbar KI-bruk: … eksempler på at gruppen har presisert krav, avvist, rettet eller forbedret KI-forslag». Kriterium 3 (15 %), s. 4: «Spor av kodegjennomgang, for eksempel kommentarer i pull requests eller beskrivelser av feil som ble funnet i KI-generert kode og hvordan de ble rettet.» A–B på kriterium 3, s. 3: «med konkrete eksempler på feil som ble avdekket og rettet.»
- **Hvor i PRD:** Del 6, risiko 5: «Én liten oppgave om gangen. Endringene leses gjennom før de committes, og commits gjøres ofte … Arbeidet følger stories som viser til FR-numrene i denne PRD-en.» Addendum, «Arbeidsmåte», nevner bare README.
- **Alvorlighet:** høy
- **Merknad:** Avstemmingen la dette under «Ikke PRD-innhold», og det er riktig at det ikke er en funksjon i nettsiden. Men PRD-en har allerede en risiko og en «Arbeidsmåte»-del som handler om hvordan du jobber, og der står det ingenting om branches, pull requests eller issues. Repoet har så langt bare `main`, og alle 31 commits går rett dit. «Endringene leses gjennom» er usynlig for sensor hvis det ikke etterlater spor. Prompt-loggen dekker planleggingen godt, men det finnes ingen plan for å skrive ned feil du finner i koden KI-en lager. Det er dette sensor trenger for å gi A–B på kriterium 1 og 3.
- **Forslag:** Utvid «Arbeidsmåte» i addendum (eller risiko 5) med noe slikt:
  - Hver story får en egen branch og en pull request til `main`. Tittelen på PR-en viser til story og FR-nummer.
  - I hver PR skriver jeg en kort kommentar om hva jeg sjekket, og om KI-en gjorde noe feil eller noe jeg ikke ba om, og hvordan det ble rettet.
  - CI (GitHub Actions) må være grønn før PR-en flettes inn.
  - Prompt-loggen fortsetter under kodingen, med en egen kolonne for «avvist eller rettet».

  Det er nok med én setning per PR. Etter seks uker har du da mange konkrete eksempler som sensor kan følge.

### S3. De automatiske testene dekker for lite av den sentrale logikken

- **Kriterium:** 3 Kvalitetssikring og testing (15 %), s. 4: «Automatiserte tester … som tester meningsfull logikk.» Nivå C, s. 4: «Det finnes tester og noe dokumentert kvalitetssikring, men dekningen er ujevn eller testene er overfladiske.» Kap. 3 punkt 7, s. 2: «Kjør testene … og vurder hva de faktisk tester.»
- **Hvor i PRD:** NFR-9: «Telleregelen for nøkkelordtreff (FR-17) og innloggingen (FR-1, FR-3) har automatiske tester med kjent input og fasit.»
- **Alvorlighet:** høy
- **Merknad:** Avstemmingen (H3) ble rettet ved at innloggingen fikk tester. Avgjørelsen om å kutte automatisk *ende-til-ende*-test er forståelig. Men det finnes mye logikk som er ren kode og like enkel å teste som telleregelen, og som nå bare testes for hånd. Når sensor kjører testene og bare ser en tekstsøk-funksjon og innlogging, er det nærmest ordrett beskrivelsen av nivå C: «dekningen er ujevn». Eksempler på slik logikk:
  - FR-28: kontrollen av om et KI-svar kan brukes (tom nøkkelordliste, begge gap-lister tomme, tomt brev, svar som ikke kan leses). Dette er ren kode og passer perfekt for enhetstester.
  - FR-9, FR-10, FR-12: tomme felt, feil filtype og for stor fil.
  - FR-15 og FR-19: at nøkkelordlisten gjenbrukes og gir samme prosent (suksesskriterium 8).
  - FR-30: at den nedlastede .docx-filen ikke har markeringer (en del av suksesskriterium 4).
  - FR-7: at sider uten innlogging sendes til innloggingen.
- **Forslag:** Utvid NFR-9: «I tillegg har kontrollen av KI-svar (FR-28), validering av input (FR-9, FR-10, FR-12), gjenbruk av nøkkelordlisten (FR-15) og at nedlastet fil er uten markeringer (FR-30) automatiske tester.» Alt dette kan testes uten ekte KI, fordi testmodus og ferdige svar allerede finnes. Det koster lite når KI-en skriver testene sammen med koden.

---

## Middels

### S4. Ingen plan for å holde PRD-en oppdatert når kodingen starter

- **Kriterium:** 1 (30 %), s. 2: «BMAD-dokumenter … som faktisk er brukt og oppdatert, ikke bare generert én gang» og «Sammenheng plan–kode: … at avvik fra planen er forklart.» Varseltegn s. 6: «Planleggingsdokumentene beskriver en annen app enn den som er levert».
- **Hvor i PRD:** Frontmatter: `status: draft`, `updated: 2026-10-09` (PRD-en ble endret mye 10. oktober). Addendum, «Arbeidsmåte»: bare «README oppdateres fortløpende».
- **Alvorlighet:** middels
- **Merknad:** Planen er å sette PRD-en til `final` (todo, steg 6–7). Etter det er det lett å la den ligge. Under kodingen kommer det nesten alltid avvik, og da beskriver PRD-en en litt annen nettside enn den du leverer. I tillegg finnes PRD-en i to kopier: arbeidskopien i `_bmad-output/` (ikke i Git) og kopien i `my-project/2-prd/` (det sensor ser). Hvis kopien ikke blir oppdatert, ser sensor en utdatert plan. Datoen i `updated` er allerede utdatert.
- **Forslag:** Legg til i «Arbeidsmåte»: «Når kodingen avviker fra PRD-en (et krav kuttes, endres eller legges til), oppdateres PRD-en og kopien i `my-project/2-prd/`, og avviket logges med dato og grunn i memloggen.» Vurder en kort del nederst i PRD-en, «Endringer etter at kodingen startet». Oppdater `updated` hver gang.

### S5. I testmodus får sensor lite å prøve selv

- **Kriterium:** 2 (20 %) og kap. 3 punkt 3, s. 2: «Test appen. Gå gjennom kjerneflytene … Prøv også feil input og uventet bruk.» Kriterium 6, s. 5: «Testdata eller testbrukere ved behov».
- **Hvor i PRD:** FR-34: «I testmodus fungerer bare de fiktive testdataene. Legger brukeren inn noe annet, får de beskjed om at bare testdata fungerer i testmodus.» FR-38: «README viser i tillegg to–tre skjermbilder».
- **Alvorlighet:** middels
- **Merknad:** Sensor vil nesten helt sikkert bruke testmodus. Da kan sensor bare laste opp testfilene og se ferdige svar. Det er fire hull:
  1. Telleregelen (FR-17) er ren kode og kunne vist seg på sensors egen CV-tekst, men FR-34 avviser alt annet enn testdata. Det beste beviset på at nettsiden faktisk regner selv, blir dermed borte.
  2. FR-34 sier at feilmeldingen for uleselig PDF virker i testmodus, men sensor har sjelden en skannet PDF for hånden. Testdataene har ingen slik fil og ingen fil av feil type (forslaget i avstemmingen H2 ble bare delvis tatt med).
  3. Feilmeldingene i FR-28 (nettverksfeil, ubrukelig KI-svar) kan ikke sees i testmodus.
  4. Det står ikke hvordan nettsiden kjenner igjen testdata (samme fil? samme tekst?). Hvis sensor limer inn teksten fra test-PDF-en med et ekstra linjeskift og får «bare testdata fungerer», ser det ut som en feil.
- **Forslag:** Endre FR-34 slik at telleregelen i testmodus brukes på *hvilken som helst* CV, med den ferdige nøkkelordlisten fra test-annonsen. Legg en skannet PDF og en .jpg eller .docx i testdata-mappen, slik at sensor kan prøve FR-10 og FR-11 med én gang. Vurder ett test-case med et ferdig «ubrukelig» KI-svar, slik at FR-28 kan vises. La arkitekturen bestemme hvor tolerant gjenkjenningen av testdata skal være. Sørg for at skjermbildene i FR-38 viser begge modusene, også markeringene i Korrektur.

### S6. Målet for README er det samme som sensors grense, og README testes ikke på en ren maskin

- **Kriterium:** 6 README og kjørbarhet (10 %), s. 5: «Sensor får appen til å kjøre ved å følge README uten avvik.» Kap. 3, s. 2: «Installer og start appen på en ren maskin eller i et rent miljø, kun etter oppskriften i README.md» og «Bruk rimelig innsats … (veiledende inntil 15–20 minutter).» Kriterium 2: «Dersom appen ikke lar seg kjøre … trekker det tydelig ned på kriterium 6 og begrenser hvor høyt kriterium 2 kan vurderes.»
- **Hvor i PRD:** NFR-8: «Sensor kan få nettsiden i gang på 15–20 minutter ved å følge README.»
- **Alvorlighet:** middels
- **Merknad:** 15–20 minutter er det *meste* sensor vil bruke, ikke et mål å sikte på. Et lite problem (feil versjon av Node eller Python, en pakke som feiler) spiser fort hele tiden. Hvis nettsiden ikke starter, trekker det ned både kriterium 6 og kriterium 2, altså 30 % til sammen. PRD-en krever heller ikke at README faktisk prøves på en ren klone, og det er der de fleste feilene viser seg (filer som bare finnes på din PC).
- **Forslag:** Endre NFR-8 til «… på under 10 minutter». Legg til i NFR-12 (testplanen): «README er prøvd fra en ny klone i en tom mappe, uten `.env` og uten lokale filer, og resultatet er skrevet ned med dato.» Gjør dette én gang før funksjonsstopp og én gang rett før innlevering.

### S7. Alternativtekst og kontrast er satt på kuttlisten, selv om sensor ser etter dem

- **Kriterium:** 4 Design og brukeropplevelse (10 %), s. 4: «Grunnleggende tilgjengelighet (universell utforming): lesbar kontrast, tastaturnavigasjon, alternativtekst og fornuftige skjemaetiketter.» A–B, s. 4: «grunnleggende tilgjengelighet er ivaretatt.»
- **Hvor i PRD:** Kuttlisten: «Kontrast som oppfyller WCAG AA, og alternativtekst på bilder og ikoner (gjøres hvis det blir tid) | Prioritert bort på grunn av tid.»
- **Alvorlighet:** middels
- **Merknad:** Dette er et bevisst valg (memlog linje 82), men det kan likevel koste. Sensor leser kuttlisten og ser at to av de fire punktene sensor ser etter under tilgjengelighet er «prioritert bort». Samtidig koster de nesten ingenting: nettsiden har få bilder og ikoner, så alternativtekst tar minutter, og kontrast sjekkes med et gratis verktøy når fargene velges i UX. Å kutte noe som er så billig, sender et uheldig signal.
- **Forslag:** Flytt de to punktene fra kuttlisten til NFR-6: «Bilder og ikoner har alternativtekst. Kontrasten sjekkes mot WCAG AA med et kontrastverktøy når fargene velges.» Hvis du vil beholde dem på kuttlisten, endre i hvert fall begrunnelsen, slik at det ikke ser ut som tilgjengelighet er valgt bort.

---

## Lav

### S8. Suksesskriteriene med ekte KI har ingen regel for når de er bestått

- **Kriterium:** 3 (15 %), s. 4: «Dokumenterte manuelle tester eller testplaner der automatiske tester ikke er hensiktsmessige.» A–B: «Testene er relevante».
- **Hvor i PRD:** Del 5: «Kriterium 1, 3 og 11 testes med ekte KI» og kriterium 1: «Gap-analysen viser alle krav som fasiten sier mangler.»
- **Alvorlighet:** lav
- **Merknad:** KI-svar varierer fra gang til gang. Det står ikke hvor mange ganger hvert case kjøres, og hva som regnes som bestått. Kriterium 1 sjekker bare at gap-analysen ikke *overser* noe, ikke at den sier «mangler» om ting CV-en faktisk dekker.
- **Forslag:** Skriv i NFR-12 eller del 5: «Hvert KI-kriterium kjøres for eksempel tre ganger per test-case. Resultatet (bestått eller ikke, og hva som var feil) skrives i testplanen.» Legg eventuelt til i kriterium 1: «… og ingen krav som fasiten sier er dekket, står under mangler.» Feil du finner her, er gode eksempler for S2.

### S9. FR-7 sperrer også registreringssiden, slik det står nå

- **Kriterium:** 2 (20 %), s. 3: «At kjerneflytene … fungerer fra start til slutt.»
- **Hvor i PRD:** FR-7: «Prøver brukeren å gå til en side på nettsiden uten å være logget inn, kommer de til innloggingen».
- **Alvorlighet:** lav
- **Merknad:** Ordrett betyr det at også registreringssiden er sperret, og da kan ingen registrere seg (FR-1). Det er åpenbart ikke meningen, men stories og tester skrives ofte rett fra kravteksten.
- **Forslag:** Legg til i FR-7: «Innloggingen og registreringen er de eneste sidene som kan brukes uten å være logget inn.»

### S10. Kravnumrene står ikke i rekkefølge

- **Kriterium:** 1 (30 %), s. 2: «at funksjoner i koden kan spores tilbake til krav og stories».
- **Hvor i PRD:** Del 2.2 starter med FR-20 før FR-8. FR-37 står mellom FR-24 og FR-25. NFR-12 står før NFR-11.
- **Alvorlighet:** lav
- **Merknad:** Det er et bevisst og godt valg å beholde gamle numre (memlog linje 25). Men en sensor som blar i dokumentet, kan tro at krav mangler eller at dokumentet er rotete.
- **Forslag:** Én setning øverst i del 2: «Kravene beholder numrene de fikk da de ble skrevet, slik at henvisninger i stories og memlogg ikke brytes. Derfor står de ikke alltid i rekkefølge.»

### S11. Ingenting om kodestil, og mulig to programmeringsspråk

- **Kriterium:** 5 Kodekvalitet og arkitektur (10 %), s. 5: «Konsekvent stil, gjerne støttet av linter eller formatterer» og «Fornuftig håndtering av konfigurasjon og avhengigheter.» Kriterium 6, s. 5: «Forutsetninger med versjoner».
- **Hvor i PRD:** Ikke nevnt. CI-filen (`.github/workflows/ci.yml`) er satt opp for både `frontend/` (JavaScript) og `backend/` (Python).
- **Alvorlighet:** lav
- **Merknad:** Dette hører mest hjemme i arkitekturen. Men to språk betyr to sett forutsetninger, to installasjonssteg og flere ting som kan feile for sensor (S6), og mer kode for én person på kort tid.
- **Forslag:** Legg til i addendum under «Til arkitektur»: «Vurder ett språk for hele nettsiden, slik at installasjonen blir enklere. Bruk en linter og en formatterer, og la CI sjekke dem.»
