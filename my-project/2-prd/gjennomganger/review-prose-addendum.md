# Språkgjennomgang: addendum.md (Søknadsassistenten)

**Formål og lesere:** Addendumet finnes for at Kristine og agentene som lager UX-, arkitektur- og story-dokumentene, skal finne detaljene og de første ideene fra PRD-arbeidet, sortert etter hvilket dokument de skal brukes i.

**Stil som skal beholdes:** Kort, saklig bokmål med uthevede punkttitler og FR-/NFR-henvisninger i parentes. Kristine omtales i tredje person i UX-delen. Fragmentsetninger etter kolon («ligger i et hjørne av startsiden») og engelske fagord (branch, pull request, story, linter, CI) er bevisste valg. Det samme gjelder komma foran «og hvor/og hva» mellom to leddsetninger, som også brukes i PRD-en. Ingenting av dette er flagget.

Gjennomgangen tar bare med reelle feil, uklare setninger, begreper som ikke stemmer med PRD-en, og henvisninger som peker feil. Ingen forslag til omskriving for stilens skyld. Kodeblokken med mappestrukturen er ikke gjennomgått.

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| prose | «Bestem om testdataene skal ha en CV med to kolonner, eller om CV-er med én kolonne skal skrives ned som en kjent begrensning.» (Til arkitektur, CV-er med kolonner og tabeller) | Vurder: «… eller om det skal skrives ned som en kjent begrensning at bare CV-er med én kolonne støttes.»? | Slik setningen står, ser det ut som om CV-er med *én* kolonne er begrensningen. Problemet er CV-er med *flere* kolonner (neste setning). Punkttittelen nevner også tabeller, men teksten sier ingenting om dem. Vurder om tabeller skal nevnes, eller om «og tabeller» skal ut av tittelen. |
| prose | «om KI-en gjorde noe feil eller noe jeg ikke ba om» (Arbeidsmåte, PR-regel 2) | Vurder: «om KI-verktøyet (for eksempel Claude Code) gjorde noe feil eller noe jeg ikke ba om»? | I resten av addendumet og i hele PRD-en betyr «KI-en» KI-en *inni nettsiden* (Claude via API, NFR-11). Her menes KI-en som hjelper deg å kode. En agent som leser dette, kan blande de to. |
| prose | «**Språk:** Vurder om hele nettsiden kan lages i ett språk, slik at installasjonen for sensor blir enklere (NFR-8).» | Vurder: «**Programmeringsspråk:** Vurder om hele nettsiden kan lages i ett programmeringsspråk, …»? | «Språk» kan leses som norsk/engelsk på nettsiden. FR-24 i PRD-en handler om at brevet skal være på norsk. Det er bare begrunnelsen om installasjonen som viser at du mener programmeringsspråk. |
| prose | «**Tomme felt (FR-4) og manglende innlogging (FR-7):** feltene får rød ramme.» | Vurder: si hvilke felt det gjelder ved manglende innlogging, for eksempel «feltene på innloggingssiden får rød ramme»? | I FR-7 er det ingen felt. Der sendes brukeren til innloggingen med en feilmelding. Det er uklart hvilke felt som skal bli røde. Hvis du mente feil e-post eller passord, er det FR-3. |
| prose | «der bare ordene som er endret vises i rødt og grønt» (Til UX, Markeringer i Korrektur) | «der bare ordene som er endret, vises i rødt og grønt» | Kommaregel: det skal være komma etter en leddsetning («som er endret») som står inni en annen setning, foran verbet («vises»). |
| prose | «Bruk en linter og en formatterer, og la CI sjekke dem.» (Arbeidsmåte, Kodestil) | «Bruk en linter og en formaterer, …» (eller det engelske «formatter», som «linter») | På bokmål staves det «formatere/formaterer» med én t. «Formatterer» er en blanding av norsk og engelsk. |
| prose | «**Lese tekst fra PDF (FR-11, fra product brief):**» | Vurder: «(FR-8, FR-11, fra product brief)»? | FR-11 handler bare om PDF-er som *ikke* kan leses. Kravet om at brukeren kan laste opp PDF, er FR-8. PRD §7 bruker også FR-11 for denne raden. Hvis du endrer, bør du endre begge stedene, så henvisningene fortsatt stemmer overens. Lav prioritet. |
| prose | «feltene får rød ramme.» (Tomme felt) | «Feltene får rød ramme.» | Etter kolon har de andre punktene med hel setning stor forbokstav («Kristine vet …», «Arkitekturen bestemmer …»). Dette er det eneste punktet med hel setning og liten bokstav. Det er bare et spørsmål om å være konsekvent. |

## Kontrollert uten funn

- Alle FR-/NFR-henvisninger ble sjekket mot prd.md: FR-4, 6, 7, 8, 11, 12, 13, 14, 16, 18, 20, 23, 24, 27, 28, 29, 32, 34 og NFR-3, 8, 11. Alle unntatt de to som er nevnt i tabellen (FR-7 og FR-11), peker på riktig krav. «Suksesskriterium 5» stemmer (PDF og innlimt tekst gir samme treff).
- Begrepene stemmer med PRD-en og ordlisten: Korrektur, «Forbedre mitt brev», innleggingsside, resultatside, gap-analyse, nøkkelordliste, testmodus, fasit, testcase, ventetegn.
- «Logg ut-knapp» med bindestrek er riktig skrevet.

**Antall funn:** 8 (2 uklare setninger med fare for feil tolkning, 1 begrep som kolliderer med PRD-en, 1 uklar henvisning (FR-7), 1 kommafeil, 1 stavefeil, 1 henvisning som kan gjøres mer presis (FR-11), 1 sak om å være konsekvent).
