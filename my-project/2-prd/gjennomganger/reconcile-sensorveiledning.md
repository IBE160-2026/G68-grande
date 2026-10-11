# Avstemming: Sensorveiledning del 1 mot PRD

- **Kilde:** `Sensorveiledning.pdf` (IBE160, del 1, høst 2026, 7 sider)
- **Sammenlignet med:** `prd.md`, `addendum.md`, `.memlog.md` (i samme mappe)
- **Dato:** 2026-10-10
- Beslutninger som står i `.memlog.md` (for eksempel kuttlisten, «nettside» i stedet for «app», testmodus uten API-nøkkel) regnes ikke som hull.

## Kort oppsummert

PRD-en dekker det meste av det sensorveiledningen sier om selve produktet: feilmeldinger og validering (FR-4, FR-9–FR-12), sikkerhet og hemmeligheter (NFR-1–NFR-3), tilgjengelighet (NFR-6), skjermstørrelser (NFR-7), kjøring etter README på 15–20 minutter (NFR-8), testmodus uten API-nøkkel (FR-32), prompts i Git (NFR-10), kuttliste med begrunnelser (del 4) og sporbarhet med FR-numre (risiko 5). Hullene under handler mest om **hva sensor faktisk kan prøve i testmodus**, **testing ut over telleregelen**, og **hva README må inneholde**.

## Hull

### H1. Sensor kan bare se testmodus – det trengs bevis for at ekte KI virker
- **Kriterium (s. 2, kap. 3 og s. 3, kriterium 2):** «Sett av tid til å kjøre appen selv.» / «Dersom appen ikke lar seg kjøre, vurderes funksjonalitet ut fra kode, tester, skjermbilder og video i repoet» / «At kjerneflytene fra proposal og README fungerer fra start til slutt.»
- **PRD:** FR-32 sørger for at nettsiden kan kjøres uten API-nøkkel, med ferdige KI-svar. Sensor har sannsynligvis ingen API-nøkkel, og ser derfor bare ferdige svar. Ingenting i PRD-en sier hvordan sensor kan se at gap-analysen, brevet og Korrektur virker med ekte KI.
- **Alvorlighet:** høy (kriterium 2 teller 20 %)
- **Forslag:** Nytt NFR, for eksempel: «Repoet inneholder skjermbilder eller en kort video av hele flyten med ekte KI (begge modusene), og eksempler på ekte KI-svar for testdataene. README viser til dem.» Eventuelt også: README forklarer hvordan sensor kan legge inn sin egen API-nøkkel.

### H2. Hva fungerer i testmodus – feil input og testdata
- **Kriterium (s. 2, kap. 3 punkt 3):** «Test appen. Gå gjennom kjerneflytene … Prøv også feil input og uventet bruk.» Og s. 5, kriterium 6: «Testdata eller testbrukere ved behov».
- **PRD:** FR-34 sier at bare fiktive testdata fungerer i testmodus. Det står ikke om valideringen (tomme felt, feil filtype, uleselig PDF, for stor fil – FR-4, FR-9–FR-12) skjer *før* testdata-sjekken, slik at sensor kan prøve feil input i testmodus. Det står heller ikke at testdataene må dekke begge modusene (eget søknadsbrev til «Forbedre mitt brev») og feiltilfellene (for eksempel en skannet PDF), eller at README sier hvor testdataene ligger (NFR-3 sier bare «i en egen mappe»).
- **Alvorlighet:** middels
- **Forslag:** Presiser i FR-34: «Valideringen i FR-4 og FR-9–FR-12 virker også i testmodus.» Legg til at testdataene har CV, stillingsannonse og eget søknadsbrev, både som PDF og tekst, og minst én uleselig PDF og én fil av feil type, og at README peker på mappen.

### H3. Testing ut over telleregelen
- **Kriterium (s. 4, kriterium 3):** «Automatiserte tester (enhets-, integrasjons- eller ende-til-ende-tester) som kan kjøres etter beskrivelsen i README, og som tester meningsfull logikk.» / «Dokumenterte manuelle tester eller testplaner der automatiske tester ikke er hensiktsmessige.»
- **PRD:** NFR-9 krever automatiske tester bare for telleregelen (FR-17). Suksesskriteriene (del 5) sier hva som skal testes, men ikke at det skal være automatisk der det går, eller at de manuelle sjekkene (for eksempel nr. 3 og 11, KI-svar mot fasit) skal skrives ned som testplan med resultat. README-kravet om hvordan testene kjøres mangler også (se H4).
- **Alvorlighet:** middels (kriterium 3 teller 15 %)
- **Forslag:** Utvid NFR-9 eller legg til et NFR: «Innlogging, validering av input og hele flyten i testmodus har automatiske tester. Suksesskriterier som må sjekkes manuelt (KI-svar), har en skrevet testplan med resultat i repoet.» Testmodus gjør det mulig å teste hele flyten uten ekte KI.

### H4. README-innhold er bare delvis dekket
- **Kriterium (s. 5, kriterium 6):** «Forutsetninger med versjoner», «Konfigurasjon: hvilke miljøvariabler som trengs, med en eksempelfil (for eksempel .env.example)», «hvordan testene kjøres», «Oversikt over mappestrukturen og lenker til planleggings- og prosessdokumentasjonen», «gjerne med skjermbilde».
- **PRD:** NFR-8 nevner eksakte kommandoer og testbruker; NFR-2 nevner `.env.example`. Forutsetninger med versjoner, hvordan testene kjøres, mappestruktur og lenker til BMAD-dokumenter og prompt-logg står ikke.
- **Alvorlighet:** lav–middels (dette er mest README-arbeid, men et krav i PRD-en gjør at det blir en story og ikke glemmes)
- **Forslag:** Utvid NFR-8: «README har: hva nettsiden gjør (med skjermbilde), forutsetninger med versjoner, installasjon og oppstart med eksakte kommandoer, miljøvariabler (viser til `.env.example`), testbruker, testdata, hvordan testene kjøres, mappestruktur og lenker til planleggingsdokumentene og prompt-loggen.»

### H5. Testbrukeren og den lokale databasen på en ren maskin
- **Kriterium (s. 2, kap. 3 punkt 2 og s. 6, kriterium 7):** «Installer og start appen på en ren maskin … kun etter oppskriften i README.md» / «En .gitignore som holder byggeartefakter … og lokale filer ute av repoet.»
- **PRD:** NFR-4 sier at brukerkontoen lagres i en lokal database, og NFR-8 at det finnes en testbruker. Det står ikke hvordan testbrukeren finnes på en ren maskin. Hvis databasefilen ikke skal i Git (lokal fil), må den lages og fylles med testbrukeren automatisk eller med én kommando.
- **Alvorlighet:** middels (kan stoppe sensor helt, som trekker på kriterium 6 og begrenser kriterium 2)
- **Forslag:** Legg til i NFR-4 eller NFR-8: «Databasen lages ved første oppstart (eller med én kommando i README), og testbrukeren opprettes da automatisk. Databasefilen ligger ikke i Git.»

### H6. Endringer fra proposal er ikke koblet til proposal
- **Kriterium (s. 3, kriterium 2):** «At det som er utelatt eller endret fra proposal, er beskrevet og begrunnet.» Og s. 2, kap. 3 punkt 1: sensor leser «gruppens godkjente proposal og eventuell product brief».
- **PRD:** Kuttlisten (del 4) er begrunnet, men den bygger på product brief. PRD-en nevner ikke proposal. Endringer som Word i stedet for Markdown (del 2.5) er begrunnet, men det finnes ingen samlet oversikt over hva som er endret fra proposal.
- **Alvorlighet:** lav (kuttlisten dekker det meste, hvis briefen følger proposal)
- **Forslag:** Én setning i del 4: «Kuttlisten viser hva som er utelatt fra proposal og product brief», eller en kort tabell «Endret fra proposal» hvis proposal lovet noe som ikke står i briefen. Sjekk proposal mot briefen.

### H7. Tilgjengelighet: alternativtekst og målbar kontrast
- **Kriterium (s. 4, kriterium 4):** «Grunnleggende tilgjengelighet (universell utforming): lesbar kontrast, tastaturnavigasjon, alternativtekst og fornuftige skjemaetiketter.»
- **PRD:** NFR-6 dekker kontrast, tastatur og etiketter. Alternativtekst mangler. «God kontrast» er ikke målbart.
- **Alvorlighet:** lav
- **Forslag:** Legg til i NFR-6: «Bilder og ikoner har alternativtekst. Kontrasten følger WCAG 2.1 nivå AA.»

### H8. Stabilitet ved gjentatte handlinger
- **Kriterium (s. 3, kriterium 2):** «Stabilitet: at appen tåler vanlig bruk, feil input og gjentatte handlinger uten å krasje.»
- **PRD:** Dekket for KI-kall (FR-27, som [ASSUMPTION]) og feil fra KI (FR-28). Gjentatte trykk på nedlasting, tilbake-knappen i nettleseren og «nytt forslag» mange ganger er ikke nevnt.
- **Alvorlighet:** lav
- **Forslag:** Gjør antakelsen i FR-27 til et krav, og eventuelt et generelt NFR: «Nettsiden krasjer ikke ved gjentatte trykk, nettleserens tilbake-knapp eller oppdatering av siden; brukeren får en forståelig melding.»

## Ikke PRD-innhold

Dette vurderer sensor, men det hører hjemme i prosess, kode eller repo, ikke i PRD-en:

- Kriterium 1: jevn commit-historikk, små commits med gode meldinger, branches, pull requests og issues, lagrede prompts fra utviklingen og eksempler på at KI-forslag er avvist eller rettet (prompt-loggen dekker dette), dokumenterte valg av teknologi (hører i arkitekturen).
- Kriterium 3: spor av kodegjennomgang og beskrivelser av feil i KI-generert kode som ble rettet.
- Kriterium 4: skisser eller wireframes (hører i UX-dokumentet; addendum har allerede notater «Til UX»).
- Kriterium 5: mappestruktur som stemmer med arkitekturen, lesbar kode, lite død kode, linter eller formatterer.
- Kriterium 7: `.gitignore` for `node_modules`/`venv`/byggemapper, ingen løse filer i rotmappen, ingen hemmeligheter i historikken.
- Varseltegn (s. 6–7): planleggingsdokumenter som er «generert i etterkant» – PRD-en committes underveis (memlog linje 42), så dette er ivaretatt.
