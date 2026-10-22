# Sensor-gjennomgang av UX: Søknadsassistenten

- **Lest mot:** `Sensorveiledning.pdf` (IBE160, del 1, høst 2026, 7 sider)
- **Dokumenter:** `DESIGN.md`, `EXPERIENCE.md`, `.memlog.md`, skissene i `.working/*.html`. Som kontekst: `prd.md`, `addendum.md`, `review-sensor.md` (PRD), `my-project/README.md`, `todo.md`, `prompt-logg.md` og `my-project/3-ux/`.
- **Dato:** 2026-10-22
- **Avgrensning:** Funn som gjelder selve PRD-en (S1–S11 i PRD-gjennomgangen) gjentas ikke. Bevisste valg i memloggen (bare lys modus, «nettside», systemskrift, testdata uten fylle-knapp, ingen rød ramme ved feil innlogging osv.) regnes ikke som feil, med mindre de kan koste karakter. At skissene skal flyttes til `mockups/` og oppdateres med endringene fra runde 2, er planlagt og regnes ikke som funn. Det samme gjelder at skissene ennå viser 🧪, raden nederst som ikke er festet, og at FR-18-linjen mangler.

## Samlet vurdering

Dette er et sterkt UX-arbeid for et enmannsprosjekt. Dokumentene dekker nesten alt sensor ser etter under kriterium 4 (Design og brukeropplevelse, 10 %): ett fargetema med tokens og utregnet kontrast, tastatur, etiketter, skjermlesertekster, redusert bevegelse, feilmeldinger og tomme tilstander, og PC og mobil for alle sider. Punktet «Spor av designarbeid i prosessen, for eksempel skisser, wireframes eller UX-beskrivelser» (s. 4) er oppfylt med god margin: det finnes skisser av alle sider, forkastede alternativer og en logg som viser hvorfor du valgte som du gjorde.

UX-delen hjelper også mye på kriterium 1 (Prosess og KI-styring, 30 %). Memloggen og prompt-loggen viser at du har rettet KI-en flere ganger (for eksempel «app», logg ut-knappen som manglet i skissen, «Testmodus» som ble vist feil, og brukerreisene som hjelperen skrev feil). Du har også valgt bort KI-ens forslag, for eksempel rammefargen #A77C8D. Det er nettopp den typen spor sensor ser etter for A–B.

Svakhetene ligger i to ting:

1. **Omfanget.** UX-en har lagt til mye pynt og noen nye små funksjoner som ikke står i nødlisten i PRD-en. Med ca. 7 helger igjen, og med arkitektur og epics som ikke er gjort ennå, er det en reell risiko for at pynten spiser tid fra kjerneflyten. Kriterium 2 (Funksjonalitet, 20 %) teller dobbelt så mye som kriterium 4. En stabil kjerneflyt er derfor viktigere enn fyrverkeri.
2. **Noen få steder der en utvikler (eller KI) må gjette.** Det gjelder særlig hvordan endrede setninger i Korrektur skal finnes, hva som skjer når man går tilbake til startsiden midt i en søknad, og hvordan «i»-boksen skal oppføre seg. Skissen har faktisk en liten feil i «i»-boksen.

**Hvordan det kan påvirke karakteren:** Hvis nettsiden blir bygd slik dokumentene beskriver, ligger kriterium 4 an til A–B. UX-arbeidet trekker også kriterium 1 opp mot B eller bedre. Hvis pynten derimot gjør at kjerneflyten eller testene blir halvferdige, taper du mer på kriterium 2 og 3 (til sammen 35 %) enn du vinner på kriterium 4 (10 %). De to høye funnene under er billige å rette nå, og de beskytter de kriteriene som teller mest.

**Kort svar på de fem spørsmålene:**

1. **Dekning av sensorveiledningen:** Kjerneflyter, feilhåndtering, tomme tilstander, tilgjengelighet, skjermstørrelser og testmodus er godt dekket. Sporbarheten fra krav (FR) til skjerm er god i tabellen over sidene, men UX-tilleggene står spredt (U8). Dokumentasjon av KI-feil finnes i prompt-loggen, men er lite synlig i UX-mappen (U9). Nettbrett er bare beskrevet, ikke prøvd (U5).
2. **Kan nettsiden bygges uten å gjette?** For det meste ja. Tekstene er ordrette, og tilstandene er beskrevet. Man må gjette på markeringene i Korrektur (U2), tilstanden ved retur til startsiden og testmodus over tid (U3), «i»-boksen (U4), arbeidsgivernavnet i filnavnet (U6) og fokus og sidetitler ved sidebytte (U7).
3. **For stort?** Ja, litt. Pynt og UX-tillegg bør få en egen kutterekkefølge (U1). Typografi- og avstandstokens er noe overspesifisert, men det koster lite (U12).
4. **Selvstendig tenkning:** Ja, tydelig, men den må letes fram i lange logger. En kort oversikt vil gjøre den synlig for sensor (U9).
5. **Uklart eller i konflikt med PRD-en:** Ingen alvorlige konflikter. Det er noen små avvik som bør samles og merkes som «tillegg i UX» (U8), og én tallfeil i kontrasten (U10).

**Antall funn:** kritisk 0 · høy 2 · middels 7 · lav 4

---

## Kritisk

Ingen.

---

## Høy

### U1. Pynt og UX-tillegg har ingen kutterekkefølge, og scope kan sprekke

- **Kriterium:** 2 Funksjonalitet og omfang (20 %), s. 3: «At kjerneflytene fra proposal og README fungerer fra start til slutt» og «Stabilitet: at appen tåler vanlig bruk, feil input og gjentatte handlinger uten å krasje». A–B, s. 3: «Kjernefunksjonaliteten er komplett og stabil.» Kriterium 4 (10 %), s. 4, A–B: «Appen fremstår gjennomarbeidet, konsistent og intuitiv.»
- **I dokumentene:** `DESIGN.md` § Elevation & Depth › Bevegelse (fyrverkeri, prosentlinje som fylles, ikon som vipper, prikker). `EXPERIENCE.md` § Component Patterns og § State Patterns: vindu etter *hver* nedlasting, vindu ved «Logg ut før nedlasting», «Gjenta passord», «Tilbake» fra innleggingen med bevaring av feltene, rad festet nederst, «i»-boks som åpnes på tre måter, filnavn med arbeidsgiver. PRD § 4 Nødliste nevner ingen av disse.
- **Problem:** Hver av disse tingene er liten, men til sammen er det mange timer med koding og testing, og de er ikke med i nødlisten. Fyrverkeriet alene har regler for varighet, antall utbrudd, plassering bak teksten, fem farger og redusert bevegelse. Ifølge PRD-en skal UX, arkitektur og epics være ferdige 25. oktober, altså denne helgen. Da er det ca. 6 helger igjen til koding, testing, README og testplan. Når du jobber alene, er det lett å bruke en hel helg på pynt fordi det er gøy, mens testene for FR-28 eller FR-9 venter. Sensor ser kjerneflyten og testene først. Fyrverkeriet gir lite hvis «Prøv igjen» ikke virker.
- **Forslag:** Legg til en kort del i `EXPERIENCE.md`, for eksempel «UX-kuttliste», med tre nivåer:
  - **Bygges til slutt, kuttes først:** fyrverkeri (erstattes av en enkel ✓ ved overskriften), prosentlinjen som fylles (vises ferdig fylt), ikonet som vipper, «Logg ut før nedlasting»-vinduet, filnavn med arbeidsgiver (bruk `Soknad_<dato>`).
  - **Kuttes ved tidsnød:** vinduet etter *hver* nedlasting (vis det bare etter første), «Tilbake» fra innleggingen, «Gjenta passord».
  - **Kuttes aldri:** feilmeldingene, tastatur og fokus, etiketter og skjermlesertekster, kontrast, ventetegnet, testmodus-merkelappen og KI-merknaden.

  Skriv i stories at pynten kommer i en egen story *etter* at kjerneflyten virker i testmodus (milepælen 18. november). Da er det lett å kutte, og kuttet kan forklares i PRD-en slik du allerede har planlagt.

### U2. Det står ikke hvordan «endret setning» i Korrektur skal finnes

- **Kriterium:** 1 (30 %), s. 2: «Sammenheng plan–kode: at funksjoner i koden kan spores tilbake til krav og stories, og at avvik fra planen er forklart.» Kriterium 2 (20 %), s. 3: «Stabilitet … feil input». Kap. 3 punkt 3, s. 2: «Prøv også feil input og uventet bruk.»
- **I dokumentene:** `EXPERIENCE.md` § Component Patterns › «Endret setning», § Key Flows › Reise 2 steg 7 og Reise 3 steg 8. PRD FR-23: «Endelig løsning bestemmes i UX.»
- **Problem:** UX-en sier hvordan en endret setning *ser ut* og *virker*, men ikke hvordan nettsiden vet *hvilke* setninger som er endret, eller hva den gamle setningen er. Dette er den vanskeligste delen av skjermbildene, og sensor prøver den (Henrik, steg 8, og suksesskriterium 4). En utvikler eller KI må gjette på mange ting:
  - Skal koden sammenligne gammelt og nytt brev selv (diff), eller skal KI-en svare med par av «ny setning» og «gammel setning»?
  - Hva skjer når KI-en slår sammen to setninger, deler én i to, legger til en ny setning eller fjerner en?
  - Hvordan deles teksten i setninger? Forkortelser som «f.eks.» og «bl.a.» lager falske setningsslutt.
  - Hva vises hvis ingen setninger er endret?

  Hvis dette ikke er bestemt, velger KI-en som koder, en løsning selv. Det er nettopp det PRD-en (risiko 5) vil unngå.
- **Forslag:** Skriv 4–5 linjer i `EXPERIENCE.md` (og merk det for arkitekturen):
  - KI-en svarer med en liste av setningspar `{ny, gammel}`. Er `gammel` tom, er setningen ny, og «Du skrev» viser «(Ny setning)».
  - Slås to setninger sammen, viser «Du skrev» begge de gamle.
  - Fjernede setninger vises ikke i brevet (eller: én linje under brevet, «X setninger er fjernet»).
  - Ingen endringer: «KI-en fant ingenting å endre i brevet ditt.» (Sjekk om det skal regnes som et ubrukelig svar etter FR-28.)
  - Viser det seg at dette er for vanskelig, gjelder nødlisten punkt 4 i PRD-en: brevet vises uten markeringer, og forklaringen over brevet skjules.

  Da kan svaret sjekkes med en automatisk test, og det er ekstra pluss på kriterium 3.

---

## Middels

### U3. Det står ikke hva som skjer med søknaden og testmodus når man går tilbake til startsiden

- **Kriterium:** 2 (20 %), s. 3: «Stabilitet: at appen tåler vanlig bruk, feil input og gjentatte handlinger». Kriterium 4 (10 %), s. 4: «Tydelig navigasjon og informasjonsstruktur; brukeren forstår hva som kan gjøres og hva som skjer.»
- **I dokumentene:** `EXPERIENCE.md` § Information Architecture › Navigasjon («Modusvalg → startsiden», «CV og annonse beholdes» ved Tilbake til modusvalget), § Testmodus, § State Patterns › «Samtykket». PRD FR-32: «Brukeren kan bare bytte på startsiden, ikke midt i en søknad.»
- **Problem:** Man kan gå resultatside → innlegging → modusvalg → startside med «Tilbake». Det står ikke om feltene da tømmes. Hvis de beholdes, kan brukeren slå testmodus av eller på mens det ligger data i feltene. Da er man «midt i en søknad», og det strider mot FR-32. Det kan gi rare feil, for eksempel testdata sendt til ekte KI, eller «bare testdata fungerer» på en ekte CV. Det står heller ikke:
  - om bryteren husker valget sitt når man kommer tilbake til startsiden i samme økt, og hva den står på etter ny innlogging
  - hvor man havner etter innlogging når man ble sendt til innloggingen med «Du må logge inn først» (FR-7): startsiden eller siden man prøvde å åpne?
- **Forslag:** Tre korte regler i `EXPERIENCE.md` § State Patterns:
  1. «Kommer man til startsiden, starter alltid en ny søknad med tomme felt og ny nøkkelordliste, som i FR-31.»
  2. «Bryteren husker valget i økten. Etter ny innlogging er testmodus av, eller på og låst hvis API-nøkkelen mangler.»
  3. «Etter innlogging kommer man alltid til startsiden.»

  Regel 1 gjør også koden enklere.

### U4. «i»-boksen skal åpnes på tre måter, og skissen har en feil

- **Kriterium:** 4 (10 %), s. 4: «Grunnleggende tilgjengelighet (universell utforming): … tastaturnavigasjon». Kriterium 3 (15 %), s. 4: «beskrivelser av feil som ble funnet i KI-generert kode og hvordan de ble rettet.»
- **I dokumentene:** `EXPERIENCE.md` § Interaction Primitives: «åpnes ved hover på PC, ved trykk på mobil og ved tastaturfokus. Nytt trykk lukker.» `.working/start-page-1.html` og `result-page-1.html`: `focus` setter boksen åpen, og `click` bytter mellom åpen og lukket.
- **Problem:** Regelen «åpnes ved fokus» og regelen «nytt trykk lukker» krasjer. I mange nettlesere (for eksempel Chrome på PC og Android) får knappen fokus i det man trykker. Da åpner fokus boksen, og trykket lukker den med en gang, slik at det ser ut som ingenting skjer. Skissen er laget slik og har sannsynligvis denne feilen. En KI som koder etter dokumentet, vil gjøre det samme. I tillegg står det ikke at man skal kunne flytte musa over boksen uten at den lukkes (WCAG 1.4.13).
- **Forslag:** Gjør regelen enklere: «Trykk, Enter eller mellomrom åpner og lukker. Esc lukker. På PC åpnes den også ved hover, og den holder seg åpen mens musa er over ikonet eller boksen.» Dropp «åpnes ved fokus». Prøv skissen i Chrome før den flyttes til `mockups/`. Skriv det i prompt-loggen hvis feilen bekreftes. Det er et godt og konkret eksempel på en KI-feil du fant.

### U5. Nettbrett (768 px) er ikke prøvd, og tre felt side om side blir trolig for trangt

- **Kriterium:** 4 (10 %), s. 4: «Tilpasning til relevante skjermstørrelser.» Kap. 3 punkt 4, s. 2: «prøv gjerne ulike skjermstørrelser». PRD NFR-7 (375, 768 og 1280 px).
- **I dokumentene:** `DESIGN.md` § Layout & Spacing: «Bruddpunkt: 700 px … også på nettbrett (768 px). Det er ingen egen nettbrettskisse.» `EXPERIENCE.md` § Responsive & Platform. Skissene bytter mellom PC og mobil med en knapp (`body.mobile`), ikke med ekte `@media`, så andre bredder er aldri prøvd.
- **Problem:** I Korrektur står tre innleggingsfelt side om side fra 700 px. Ved 768 px blir hvert felt ca. 230 px bredt, og det blir ca. 195 px til innhold. Knappene «Last opp PDF» og «Lim inn tekst» (12 × 20 px luft og 2 px ramme) trenger til sammen ca. 240 px. De brytes da over to linjer, filnavnet kuttes kraftig, og tekstboksen blir smal. Det er ikke en feil i NFR-7 (ingen rulling sidelengs), men det ser uferdig ut nettopp på den bredden sensor kanskje prøver.
- **Forslag:** Skriv i `DESIGN.md`: «Tre felt side om side først fra 1000 px. Mellom 700 og 1000 px står de tre feltene under hverandre (eller to og ett).» Alternativt kan knappene i feltet stå under hverandre når feltet er smalt. Bruk ekte `@media` i skissene når de flyttes, og prøv 768 px én gang i nettleseren (F12, enhetsvisning).

### U6. Filnavnet med arbeidsgiver er en skjult ny KI-oppgave

- **Kriterium:** 2 (20 %), s. 3: «At det som er utelatt eller endret fra proposal, er beskrevet og begrunnet.» Kriterium 3 (15 %), s. 4: «Automatiserte tester … som tester meningsfull logikk.»
- **I dokumentene:** `EXPERIENCE.md` § Filnavn ved nedlasting: «Arbeidsgivernavnet hentes fra annonsen (hvordan avgjøres i arkitekturen).» PRD § 6, risiko 3: «Hver KI-oppgave (nøkkelord, gap-analyse, brev, korrektur) får sin egen enkle instruks».
- **Problem:** En annonse har ikke et fast felt for arbeidsgiver. Navnet må enten hentes av KI-en eller gjettes med kode. Det er en femte KI-oppgave (eller et nytt felt i et KI-svar) som PRD-en ikke har. Den må også ha testdata, ferdige svar i testmodus og en regel for hva som skjer når KI-en svarer «Helse Bergen HF, Haukeland universitetssjukehus». Filnavnet blir da langt og rart.
- **Forslag:** Skriv i `EXPERIENCE.md`: «Arbeidsgiveren er et ekstra felt i det samme KI-svaret som nøkkelordene. Navnet kuttes til høyst 30 tegn. Mangler det, brukes `Soknad_<dato>`.» Sett det på UX-kuttlisten (U1). Lag selve funksjonen som gjør navnet om til et filnavn (æøå, mellomrom, lengde) som ren kode med en enhetstest. Den er lett å teste og er et godt eksempel for kriterium 3.

### U7. Fokus, sidetitler og overskrifter ved sidebytte er ikke beskrevet

- **Kriterium:** 4 (10 %), s. 4: «Grunnleggende tilgjengelighet (universell utforming): lesbar kontrast, tastaturnavigasjon, alternativtekst og fornuftige skjemaetiketter» og «brukeren forstår hva som kan gjøres og hva som skjer».
- **I dokumentene:** `EXPERIENCE.md` § Accessibility Floor beskriver fokus for feilboks og vinduer, men ikke hva som skjer når man kommer til en ny side.
- **Problem:** Hvis nettsiden lages slik at sidene byttes uten at hele siden lastes på nytt (vanlig når KI-en koder), blir fokus stående der knappen var, eller på ingenting. En tastaturbruker eller skjermleser får da ikke vite at man er på resultatsiden. Det står heller ikke:
  - hvilken `<title>` hver side har
  - om logoen eller sideoverskriften er hovedoverskriften (`h1`)
  - at språket er bokmål (`lang="nb"`; skissene bruker `lang="no"`)
  - at emoji i tekst («👋», «🎉» i «Bra jobbet!») blir lest opp som «vinkende hånd» og «festkonfekt»
- **Forslag:** Fire linjer i § Accessibility Floor: «Ved ny side flyttes fokus til sideoverskriften (h1). Logoen er ikke h1. Hver side har en egen tittel, for eksempel ‹Resultat – Søknadsassistenten›. `lang="nb"`. Emoji i tekst skjules for skjermlesere.» Dette koster nesten ingenting å bygge, og sensor merker det hvis han tester med tastatur.

### U8. UX-tilleggene og avvikene fra PRD-en står spredt

- **Kriterium:** 1 (30 %), s. 2: «Sammenheng plan–kode: … at avvik fra planen er forklart.» Varseltegn, s. 6: «Planleggingsdokumentene beskriver en annen app enn den som er levert».
- **I dokumentene:** Spredt i `EXPERIENCE.md`: «Tilbake» fra innleggingen («et tillegg i UX»), «Gjenta passord» (bare i memloggen, linje 95), samtykke hver gang man kommer til startsiden (PRD FR-36 sier «hver gang brukeren logger inn»), ingen rød ramme ved feil innlogging (memlog linje 136, avviker fra addendum), «Logg ut før nedlasting»-vinduet, KI-merknaden bare etter innlogging (FR-35 sier «hele tiden»), vindu etter *hver* nedlasting.
- **Problem:** Hvert valg er fornuftig, og flere er logget med grunn. Men sensor må lese hele memloggen for å finne dem. Når kodingen starter, er det også lett at en story følger PRD-en og en annen følger UX-en. Da får du nettopp de små avvikene sensor ser etter. Tabellen over sidene viser FR-numre, noe som er bra, men det finnes ingen samlet sjekk av at alle FR-ene med skjermbilder er dekket.
- **Forslag:** Lag en liten tabell nederst i `EXPERIENCE.md`, «Tillegg og avvik fra PRD-en»: hva, FR-nummer, grunn og memlog-linje (6–8 rader). Skriv én linje under: «FR-1–FR-38 er gått gjennom. Krav uten skjermbilde (FR-15, FR-17, FR-24, FR-37, FR-38) er arkitektur eller KI-instruks.» Dette gjør også epics og stories lettere å skrive.

### U9. Det er vanskelig å se hva du bestemte selv, og hva KI-en foreslo

- **Kriterium:** 1 (30 %), s. 2: «Sporbar KI-bruk: lagrede prompts og KI-økter, og eksempler på at gruppen har presisert krav, avvist, rettet eller forbedret KI-forslag.» A–B, s. 3: «Det finnes flere tydelige eksempler på at gruppen har vurdert, korrigert og styrt KI kritisk.» Varseltegn, s. 6: «Planleggingsdokumentene … er tydelig generert i etterkant.»
- **I dokumentene:** `.memlog.md` merker alt som `(decision)`, også ting KI-en foreslo og du bare godtok (for eksempel linje 87: «Kristine har ikke kommentert den», og linje 46: «forslag fra Kristine, ikke bekreftet», som står som `decision`). `DESIGN.md` er skrevet av en hjelper ut fra loggen (prompt-logg 146). De beste eksemplene på styring står i `prompt-logg.md` (118, 131, 135, 137, 141, 144, 146) og i memloggen (linje 82, 105–107, 128), men ikke samlet.
- **Problem:** Det selvstendige arbeidet *finnes*, og det er godt. Men DESIGN.md og EXPERIENCE.md ser polerte ut, og sensor kan tro at de er KI-generert i én omgang. Det er mye å lese for å finne ut hva som er ditt. Sensor har begrenset tid.
- **Forslag:** Lag en kort fil, `my-project/3-ux/mine-valg-og-ki-feil.md` (eller en del i README-en), med 8–10 punkter i to lister:
  - **Mine valg:** for eksempel at jeg valgte hovedfargen som ramme i stedet for KI-ens forslag, forkastet per ord-markering, krevde skisser av alle sider, flyttet FR-36-teksten tilbake og tolket 15–20 minutter riktig.
  - **KI-feil jeg fant:** for eksempel «app», manglende logg ut i skissen, «Testmodus» vist feil, brukerreisene skrevet feil av hjelperen, «i»-boksen (U4).

  Hvert punkt får en lenke til linjen i loggen. Du har allerede planlagt en kort prompt-logg før innlevering, så dette er samme jobb gjort litt tidligere.

---

## Lav

### U10. Kontrasttallet for hovedfargen står med to ulike verdier

- **Kriterium:** 4 (10 %), s. 4: «lesbar kontrast». PRD NFR-6: «Kontrasten sjekkes mot WCAG AA med et kontrastverktøy».
- **I dokumentene:** `DESIGN.md` § Colors: «Hvit tekst på denne fargen har kontrast 6,1:1» og lenger ned: «ramme i `{colors.primary}` (6,6:1 mot hvit)». Memlog linje 128 sier også 6,6:1.
- **Problem:** #A23E6C mot hvit er 6,1:1 (sjekket på nytt). 6,6 er feil. Det har ingen betydning for brukeren, siden begge er over 3:1, men et tall som er «regnet ut» og likevel er feil, svekker tilliten til de andre tallene. Lenkefargen (primary på bakgrunnen, 5,8:1) står heller ikke i lista. Grønn tekst på grønn (`success` på `success-tint`, 4,53:1) er så vidt over grensen. Ikke gjør den lysere.
- **Forslag:** Rett 6,6 til 6,1 i `DESIGN.md` og i memloggen. Legg til «primary på background 5,8:1 (lenker)». Skriv én gang hvilket verktøy du brukte (NFR-6).

### U11. Vinduet «Logg ut før nedlasting» mangler i oversikten

- **Kriterium:** 4 (10 %), s. 4: «Helhetlig og konsistent … komponenter».
- **I dokumentene:** `EXPERIENCE.md` § State Patterns › «Logg ut før nedlasting». Vinduet mangler i tabellen i § Information Architecture og i § Component Patterns. § Interaction Primitives sier «Esc lukker begge vinduene», men det er nå tre, og det står ikke hvilket valg som får fokus.
- **Problem:** Den som koder fra tabellene, kan glemme vinduet eller gi fokus til «Logg ut» (det farlige valget).
- **Forslag:** Legg vinduet inn i begge tabellene. Endre til «Esc lukker alle vinduene». Skriv «Fokus går til ‹Avbryt›». (Eller kutt vinduet, se U1.)

### U12. Noen verdier ligger utenfor skalaene

- **Kriterium:** 5 Kodekvalitet (10 %), s. 5: «Konsekvent stil» og kriterium 4, s. 4: «Helhetlig og konsistent visuelt uttrykk: farger, typografi, avstand og komponenter.»
- **I dokumentene:** `DESIGN.md`, frontmatter og § Shapes: `text-input` og `form-error` 13 px, `testmode-badge` 12 px og `ai-tag` 10 px, utenfor `rounded`-skalaen. Tekstboksen bruker 14 px og tekstfeltene 13 px. Brevet har luft på 26 × 30 px, og modus-kortet 22 × 18 px, utenfor `spacing`-skalaen. Det er 14 typografitokens, og flere er nesten like (1,1 / 1,2 / 1,3rem). § Typography har setningen «Logoen står i Baloo 2 ExtraBold (800).» to ganger.
- **Problem:** Det er småting, men KI-en som koder, kopierer tallene rett inn. Da får du mange enkeltverdier i CSS-en i stedet for noen få variabler.
- **Forslag:** Skriv én regel: «Verdier utenfor skalaen rundes til nærmeste token (13 → 14 px, 12/10 → 14 px, 26/30 → 24/32 px).» Slå gjerne sammen `heading-welcome` og `heading-page`. Ta den doble setningen med i språkvasken.

### U13. Venteteksten lover «noen sekunder», men brevet kan ta et halvt minutt

- **Kriterium:** 4 (10 %), s. 4: «Forståelige tilbakemeldinger … brukeren forstår hva som kan gjøres og hva som skjer.»
- **I dokumentene:** `EXPERIENCE.md` § Voice and Tone › Ventetegn: «Vi lager brevet ditt – det tar noen sekunder.» PRD § 8: «Et langt brev kan ta 20–30 sekunder.» Ventetegnet har ingen avbryt-knapp.
- **Problem:** Etter 15–20 sekunder med hoppende prikker og «noen sekunder» tror mange at siden har hengt seg, og laster den inn på nytt. Da mister de alt (NFR-4).
- **Forslag:** Endre til «Vi lager brevet ditt – det kan ta opptil et halvt minutt.» Legg eventuelt til at det etter 10 sekunder vises en ekstra linje: «Fortsatt i gang …». Det er én tekst og én tidtaker.

---

## Det som er sterkt

- **Skisser av alle sider på PC og mobil, også med forkastede alternativer.** Modusvalg A/B/C, nøkkelord A/B, nedlasting A/B/C, markering per setning eller per ord, fem fargetemaer og seks logoskrifter. Dette er det beste mulige svaret på «Spor av designarbeid i prosessen» (s. 4).
- **Feilmeldinger og tomme tilstander er skrevet ordrett,** med feltnavn først og hva man kan gjøre («CV: Vi klarer ikke å lese teksten i PDF-en … Lim inn teksten i stedet.»). Tomme lister har vennlige tekster. «Det du har lagt inn, er ikke borte» etter KI-feil er en fin detalj. Dette dekker «Forståelige tilbakemeldinger, feilmeldinger og tomtilstander» (s. 4) svært godt.
- **Tilgjengelighet er tenkt gjennom, ikke bare nevnt.** Rammefargen ble endret etter en egen kontrastskisse (1,4:1 → 6,1:1). Farge er aldri det eneste tegnet (✓/○, understreking, tekst). Det er skjermlesertekster for søppelbøtta og «i», fokus i vinduer og redusert bevegelse. Fyrverkeriet har en grense for blinking.
- **Testmodus er laget for sensor.** Det finnes en egen brukerreise for sensor (Henrik), en hjelpetekst om `testdata/`, en låst bryter uten API-nøkkel og feilmeldinger som virker i testmodus. Det gjør kap. 3 punkt 3 («Prøv også feil input») lett for sensor.
- **Sporbarhet til krav.** Tabellen over sidene og nesten hver tekst viser FR-nummer. «Ved konflikt gjelder dokumentet» og tydelige grenser mot arkitekturen (filstørrelse, tilbakeknapp, Baloo 2) viser at du vet hva som hører hjemme hvor.
- **Bevisste, begrunnede valg med din egen stemme.** «Så lun», «enkel og grei», «Dette kan du jobbe videre med» i stedet for «mangler» (mens PRD og tester beholder «mangler»), og «i» i stedet for utropstegn fordi det er mindre skremmende. Konflikter med PRD-en (FR-36, hover mot NFR-6/NFR-7) er oppdaget og løst uten å endre PRD-en i stillhet.
- **KI-styring er dokumentert.** Prompt-loggen viser flere ganger at du rettet KI-en, oppdaget hull i skissene og gjorde KI-ens tolkning av sensorveiledningen riktigere. Det er ekte bevis for kriterium 1.
