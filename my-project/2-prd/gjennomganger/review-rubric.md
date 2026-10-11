# PRD-kvalitetsgjennomgang — Søknadsassistenten

Gjennomgangen følger kvalitetsrubrikken for PRD (sju dimensjoner). Hver dimensjon får en dom: *sterk / god nok / tynn / ødelagt*. Alvorlighetsgrad (kritisk / høy / middels / lav) sier hvor mye feilen skader PRD-ens nytte, ikke hvor vanskelig den er å rette. Nivået er tilpasset et soloprosjekt i IBE160 med frist rundt 9. desember 2026. Bevisste valg som står i `.memlog.md` (kuttliste, nødliste, ID-rekkefølge, de 9 `[ASSUMPTION]`-merkene som skal behandles senere) regnes ikke som feil.

## Samlet vurdering

PRD-en er god og ærlig: den tar tydelige valg, sier hva som er valgt bort og hvorfor, og har en konkret nødliste for tidsnød. Det meste er testbart og koblet til suksesskriterier. Det som står i fare, er selve kjernen som skal skille nettsiden fra andre verktøy: løftet om at nøkkelordtreffet alltid blir likt (FR-15) holder ikke på tvers av økter, telleregelen (FR-17) gir falske treff for korte nøkkelord som «C» eller «R», og kravet til tonen i brevet (FR-24) kan ikke testes og kolliderer med løftet om «deres egen stemme». Ingen av disse er store å rette, men de bør rettes før arkitektur og stories.

## Beslutningsklarhet — sterk

PRD-en tar valg i stedet for å «balansere» alt. Eksempler: Word er valgt i stedet for Markdown, med begrunnelse (§ 2.5, «Word er valgt i stedet for Markdown, som faglærer foreslo, fordi studenter flest redigerer i Word»). Kuttlisten (§ 4) har en egen begrunnelse for hvert punkt der det betyr noe, for eksempel OAuth, ordstamme-regel og «Kun søknad». Nødlisten (§ 6) sier i hvilken rekkefølge ting kuttes og hva som *aldri* kuttes. Det gjør det lett å ta beslutninger senere når tiden blir knapp.

Avsnittet «Hva gjør dette annerledes» (§ 1) er ærlig om at Jobscan, Rezi, Teal og Kickresume allerede gjør mye av det samme, og har kilder. Det er sjeldent og bra.

Det eneste som mangler, er et lite avsnitt med åpne spørsmål. Ett åpent punkt finnes bare i memloggen (om product brief regnes som proposal), og ikke i PRD-en.

### Funn
- **lav** Åpent spørsmål står bare i memloggen (§ 4 / `.memlog.md` linje 81) — Spørsmålet til faglærer om product brief regnes som proposal kan endre kuttlisten, men en leser av PRD-en ser det ikke. *Fix:* Legg til en kort del «Åpne spørsmål» med dette punktet, eller en `[NOTE FOR PM]` under § 4.

## Innhold fremfor pynt — sterk

Det er ingen personas som bare er pynt. Det er én primær bruker (§ 1, «studenter og nyutdannede som søker jobb eller praksisplass for første gang»), og den styrer faktiske valg: forklaring av begreper (FR-18), norsk språk (FR-24), og at KI-en skal oversette erfaring til kvalifikasjoner (FR-37). Visjonen er spesifikk for dette produktet og kan ikke flyttes til et annet verktøy uten endring. «Den ærlige begrensningen» i § 1 er det motsatte av innovasjonspynt.

De fleste ikke-funksjonelle kravene er konkrete (NFR-1 hashet passord, NFR-2 `.env.example`, NFR-8 15–20 minutter). Unntakene er NFR-6 og NFR-7, som er behandlet under «Tydelig ferdig».

### Funn
Ingen egne funn. (NFR-6/NFR-7 og FR-24 er tatt under «Tydelig ferdig».)

## Strategisk sammenheng — god nok

PRD-en har en tydelig tese (§ 1): det som skiller nettsiden fra andre, er (1) en åpen telleregel som brukeren kan forstå og sjekke selv, (2) at begrepene forklares for førstegangssøkere, og (3) Korrektur som likeverdig modus, slik at brevet beholder brukerens stemme. Rekkefølgen i nødlisten følger tesen: telleregelen og testene kuttes aldri, og Korrektur kuttes bare som «siste utvei».

Svakheten er at suksesskriteriene (§ 5) sjekker at funksjonene *virker riktig*, men ingen av dem sjekker at tesen holder. Ingen kriterium sjekker at forklaringen i FR-18 faktisk gjør at en student forstår hvorfor CV-en mangler noe, eller at Korrektur-brevet fortsatt høres ut som brukeren. For et skoleprosjekt holder det med en enkel manuell sjekk, men den bør finnes. I tillegg trekker FR-24 i motsatt retning av tesen (se funn H3 under «Tydelig ferdig»).

### Funn
- **middels** Ingen suksesskriterier sjekker tesen (§ 5, sammenlignet med § 1 «Hva brukeren sitter igjen med») — Kriteriene 1–11 tester riktighet, men ikke «en konkret forståelse av hva som mangler i CV-en» eller «deres egen stemme». *Fix:* Legg til ett eller to enkle manuelle kriterier, for eksempel: «I Korrektur er minst X % av setningene i brukerens brev beholdt eller bare lett endret» og/eller «En medstudent som leser resultatsiden kan forklare med egne ord hva nøkkelordtreffet betyr og hva det ikke betyr.»

## Tydelig ferdig — tynn

Dette er dimensjonen stories vil bygge mest på. Mange krav er svært gode: FR-1 (minst 8 tegn), FR-3 (eksakt feilmelding), FR-10 («Feil filtype, prøv PDF»), FR-17 (telleregel med eksempler og kjente begrensninger) og FR-28 (liste over når et KI-svar ikke kan brukes). Men noen av de viktigste kravene har hull som vil gi problemer når de skal testes.

### Funn
- **høy** H1 — «Alltid samme prosent» holder ikke på tvers av økter (FR-15, NFR-4, suksesskriterium 8) — FR-15 sier at nøkkelordlisten «lagres i økten» og at «samme annonse og samme CV gir derfor alltid samme prosent». Men NFR-4 sier at nøkkelordlisten ikke lagres mellom øktene, og FR-31 sier at en ny søknad starter med tomme felt. Limer brukeren inn samme annonse på nytt, henter KI-en ut en ny liste, og prosenten kan bli en annen. Suksesskriterium 8 («kjørt to ganger gir samme nøkkelordtreff») sier ikke om det gjelder i samme økt eller ikke, så det kan både bestås og feile avhengig av hvordan det tolkes. *Fix:* Skriv presist: «Innenfor samme søknad (samme økt) gir samme liste og samme CV alltid samme prosent. En ny søknad henter ut en ny liste, og prosenten kan da bli litt annerledes.» Gjør suksesskriterium 8 like presist (samme lagrede liste, to utregninger). Vurder å nevne dette kort i forklaringen i FR-18.
- **høy** H2 — Telleregelen gir falske treff for korte nøkkelord (FR-17) — Regelen sier at et nøkkelord er et treff «også som del av et lengre ord». Det betyr at nøkkelord som «C», «R», «Go», «AI» eller «UX» nesten alltid blir treff, fordi bokstavene finnes inne i vanlige ord. Kjente begrensninger nevner bare «Java» i «JavaScript», som er mye mildere. Siden tesen er at tallet skal være forståelig og etterprøvbart, kan dette undergrave hele poenget for nettopp IT-studenter. *Fix:* Legg til én enkel regel, for eksempel: «Nøkkelord på 1–3 tegn må stå som eget ord (ikke inne i et annet ord).» Legg til et testtilfelle for dette i NFR-9. Alternativt: skriv det tydelig som en kjent begrensning med eksemplet «C».
- **høy** H3 — Kravet til tone kan ikke testes og strider mot «egen stemme» (FR-24, § 1) — FR-24 sier «formell og akademisk tone som gjør arbeidsgiver oppmerksom og engasjert, og skal ikke høres ut som en generisk KI-tekst». Ingen av disse ordene kan sjekkes som bestått/ikke bestått. «Akademisk» er dessuten en uvanlig tone for et søknadsbrev. I Korrektur gjelder kravet også, og da vil KI-en skrive om brukerens brev til en akademisk tone, som går imot visjonen («føles som *deres egen stemme*») og FR-23 («beholder kontrollen over sin egen stemme»). *Fix:* Skill mellom modusene. Full generering: «formell, men personlig tone», med 2–3 sjekkbare regler (for eksempel: nevner stillingen og arbeidsgiveren ved navn, viser til minst to konkrete krav fra annonsen, ingen faste fraser fra en liste med typiske KI-fraser). Korrektur: «beholder brukerens tone og setningsbygning der den fungerer, og retter språk, struktur og kobling til annonsen».
- **middels** Uklare krav til utseende og tilgjengelighet (NFR-6, NFR-7) — «god kontrast», «ser bra ut og fungerer godt på PC, nettbrett og mobil» er adjektiver uten grenser. Det er ikke mulig å si når kravet er oppfylt. (At WCAG AA er valgt bort er et bevisst valg, og er ikke feilen.) *Fix:* Gi enkle grenser, for eksempel: «Alle sider kan brukes uten vannrett rulling ved 375 px, 768 px og 1280 px bredde» og «alle knapper og felt kan nås med Tab i logisk rekkefølge, og fokus er synlig».
- **middels** Suksesskriterium 1 sjekker bare halve gap-analysen (§ 5 kriterium 1, FR-14) — Kriteriet sjekker at alle krav fasiten sier *mangler* blir vist. En gap-analyse som sier at *alt* mangler, vil bestå. I tillegg kjøres gap-analysen av KI på nytt hver gang (FR-19), så svaret kan variere mellom kjøringer. *Fix:* Legg til at krav fasiten sier CV-en *dekker*, ikke skal stå under «mangler» (eventuelt med en liten feilmargin), og si hvor mange ganger hvert testtilfelle kjøres (for eksempel 3 ganger, alle må bestå).
- **middels** Uklart hvordan testmodus kjenner igjen testdata (FR-34, suksesskriterium 5) — FR-34 sier at «bare de fiktive testdataene» fungerer i testmodus, men ikke hvordan nettsiden ser at det er testdata. Suksesskriterium 5 (PDF og innlimt tekst gir samme treff) er ikke merket som «bare ekte KI», så det må også virke i testmodus. Da må testmodus kjenne igjen samme testdata både som PDF og som innlimt tekst. *Fix:* Skriv hva som skal gjenkjennes (for eksempel «teksten etter at mellomrom og linjeskift er fjernet, sammenlignes med testdataene»), eller send spørsmålet videre til arkitekturen som `[NOTE FOR PM]`.
- **middels** Markeringene i Korrektur har ingen nedre grense for kvalitet (FR-23, suksesskriterium 4) — Kriterium 4 krever bare «minst én markert endring». Hvis KI-en skriver om hele brevet, blir hele teksten rød og grønn, og brukeren mister oversikten og kontrollen som FR-23 lover. Kravet sier heller ikke om markeringene er per ord eller per setning. *Fix:* Si at endringene markeres per ord (eller per setning), og legg til en grense, for eksempel at minst halvparten av brukerens tekst skal være uendret. Henger sammen med H3.
- **lav** Ingen tidsgrense for når KI-en «ikke svarer» (FR-28) — Det står ikke hvor lenge nettsiden venter før den viser feilmelding. *Fix:* Legg inn en grense, for eksempel 60 sekunder, eller send tallet til arkitekturen sammen med filstørrelsen (FR-12).
- **lav** FR-7 utelukker strengt tatt registreringssiden (FR-7, FR-1) — «Det er ikke mulig å bruke nettsiden uten å være logget inn» gjelder bokstavelig talt også registrering. *Fix:* Legg til «unntatt innlogging og registrering».

## Ærlig omfang — sterk

Dette er PRD-ens sterkeste side. § 4 har en kuttliste med begrunnelse for hvert punkt, og en egen liste over det som ikke er en del av prosjektet i det hele tatt (betaling, automatisk innsending osv.). FR-16 og FR-26 sier tydelig hva brukeren *ikke* kan gjøre i versjon 1. Kjente begrensninger i telleregelen står rett i kravet (FR-17). Nødlisten i § 6 gjør nedskalering til et planlagt valg i stedet for noe som skjer i stillhet.

Antall åpne punkter er lavt: 9 `[ASSUMPTION]`, 0 `[NOTE FOR PM]`, 0 åpne spørsmål i selve PRD-en. Det passer godt for et studentprosjekt. De 9 `[ASSUMPTION]`-merkene er små og konkrete, og skal behandles i neste steg.

### Funn
Ingen egne funn utover det som står under «Beslutningsklarhet» (åpent spørsmål om proposal).

## Brukbarhet videre — god nok

PRD-en skal brukes videre til UX, arkitektur og stories, så denne dimensjonen betyr noe. ID-ene er unike og alle henvisninger peker til krav som finnes. Addendum er ryddig delt i «Til UX» og «Til arkitektur». Det som mangler, er en ordliste og en kort oversikt over sidene og flyten.

### Funn
- **middels** Ingen ordliste, og noen begreper har flere navn (hele PRD-en) — Eksempler: «vanlig bruk» (FR-32) / «testmodus av» (FR-35) / «vanlig modus» (suksesskriterium 9); «nøkkelordtreff» / «ordtelling» (FR-18) / «nøkkelordtellingen» (§ 6); «innleggingssiden» (FR-8) / «opplastingsfelt» (addendum); «økt» brukes i FR-15 og NFR-4 uten at det står hva en økt er (innlogging? én søknad?). Det siste henger direkte sammen med H1. *Fix:* Legg til en kort ordliste (5–10 ord): Full generering, Korrektur, gap-analyse, nøkkelordtreff, telleregel, økt, testmodus, vanlig modus, fasit, kjerneflyt. Bruk samme ord overalt.
- **middels** Ingen samlet oversikt over sidene og flyten (§ 2) — Flyten må settes sammen fra mange krav: startside (FR-5) → modusvalg (FR-20) → innleggingsside (FR-8) → resultatside (FR-18, FR-21) → brev (FR-22/23) → nedlasting (FR-29) → startside eller logg ut (FR-31). Siden der brevet vises har ikke noe navn. UX og stories vil trenge denne listen. *Fix:* Legg til et kort avsnitt øverst i § 2, «Flyten i korte trekk», med sidene i rekkefølge og hvilke FR-er som hører til hver side. Gi siden med brevet et navn (for eksempel «brevsiden»).

## Riktig form — sterk

Formen passer produktet. Nettsiden har én type bruker og én hovedflyt, så det er riktig å ikke ha mange personas eller lange brukerreiser. PRD-en er heller ikke overformalisert: den har ingen KPI-er eller forretningsmål som ikke passer et skoleprosjekt. Sensor er en viktig «bruker» av prosjektet, og det er godt håndtert gjennom NFR-8 (README og 15–20 minutter), NFR-12 (testplan) og FR-38 (ekte KI-svar i testmodus). Den eneste mangelen i formen er den korte flytoversikten nevnt over.

### Funn
Ingen egne funn (flytoversikt er tatt under «Brukbarhet videre»).

## Mekaniske merknader

- **ID-er:** FR-1 til FR-38 og NFR-1 til NFR-12 finnes alle, uten hull eller dobbelttelling. Rekkefølgen i dokumentet er ikke numerisk (FR-20 står før FR-8, FR-37 mellom FR-24 og FR-25, NFR-12 før NFR-11). Dette er et bevisst valg (memlog linje 25: «eksisterende ID-er beholdes») og er greit, men det kan være lurt å si det i én setning øverst i § 2, slik at ingen tror at noe mangler.
- **Henvisninger:** Alle henvisninger peker til noe som finnes (for eksempel FR-10–FR-12 i nødlisten, NFR-2/NFR-3/NFR-9/FR-38 i NFR-8).
- **`[ASSUMPTION]`-oversikt:** Det er 9 `[ASSUMPTION]` inne i teksten (FR-12, FR-17, FR-22, FR-23, FR-27, FR-28, FR-29, FR-31, FR-36), men ingen samlet liste på slutten. Siden de skal behandles i neste steg, kan listen lages da, eller merkene fjernes etter hvert som de avgjøres.
- **Ordbruk:** Se funnet om ordliste over. Modusnavnene er brukt konsekvent i par («Skriv nytt brev» = Full generering, «Forbedre mitt brev» = Korrektur), og det er bra.
- **Frontmatter:** `updated: 2026-10-09`, men PRD-en ble endret 10. oktober (kildesjekk og kilder). Oppdater datoen.
- **Deler som finnes:** Visjon, funksjoner, NFR, omfang, suksesskriterier, risiko og kilder er med. Det passer nivået. Det som mangler, er ordliste og (valgfritt) åpne spørsmål, se funn over.
