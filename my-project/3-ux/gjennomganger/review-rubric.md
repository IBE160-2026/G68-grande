# Gjennomgang av DESIGN.md og EXPERIENCE.md — sjekkliste

Gjennomgått 2026-10-22 (runde 3, gjennomgang A). Kilder: `prd.md` og `addendum.md` (prd-kode-prosjekt-2026-10-09). Beslutninger i `.memlog.md` regnes som bevisste valg, ikke feil. At skissene ennå ikke er flyttet til `mockups/` og ikke har fått endringene fra runde 2, er ikke regnet som funn.

## Samlet vurdering

De to dokumentene fungerer godt som kontrakt. Alle krav i PRD-en som har med skjermen å gjøre, har en side og en oppførsel, alle fargetokens har fargekode, og alle tokenhenvisninger peker på noe som finnes. Det som må rettes før status `final`, er to ting: det tredje vinduet («Logg ut før nedlasting») er bare halvveis lagt inn, og det står ikke *når* feil i det man har lagt inn, blir sjekket. Ellers er det mest små hull i komponentlisten (avkrysningsboks, søppelbøtte, den faste raden nederst) og noen navn som ikke er like i de to filene.

Antall funn: **kritisk 0 · høy 2 · middels 8 · lav 22.**

| Kategori | Vurdering |
|---|---|
| 1. Brukerreiser og krav | strong |
| 2. Tokens | adequate |
| 3. Komponenter | thin |
| 4. Tilstander | adequate |
| 5. Skisser | adequate |
| 6. Overflødig tekst | strong |
| 7. Arv fra kildene | adequate |
| 8. Form | strong |

## 1. Brukerreiser og krav — strong

**Hva ble sjekket:** PRD-en har ingen navngitte brukerreiser. De tre reisene ble laget i UX (memlog). Hver reise ble sjekket for hovedperson, nummererte steg, høydepunkt og feilvei. Alle FR-er ble sjekket for en side eller oppførsel i dokumentene.

| Reise | Hovedperson | Steg | Høydepunkt | Feilvei |
|---|---|---|---|---|
| Reise 1 — Full generering på PC | Ingrid | 9 | Steg 8 | Ja |
| Reise 2 — Korrektur på mobil | Eirik | 8 | Steg 7 | Ja (svak, se under) |
| Reise 3 — Sensor i testmodus | Henrik | 9 | Eget avsnitt | Ja |

**Krav med skjermdel, alle dekket:** FR-1 til FR-23, FR-25 til FR-36 og NFR-6, NFR-7 og NFR-8. FR-15 (nøkkelordlisten gjenbrukes) og avrundingen i FR-17 er logikk, ikke noe som vises, og trenger ikke mer enn det som står. FR-24, FR-37 og FR-38 handler om prompten og README, og har ingen skjermdel.

### Funn

- **[lav]** Feilveien i reise 1 sier «KI-en svarer ikke i steg 6 eller 8». Feilen vises på siden man sto på, altså innleggingen (etter steg 5) eller resultatsiden (etter steg 7), ikke på brevsiden i steg 8 (EXPERIENCE.md § Key Flows, linje 337). *Forslag:* «KI-en svarer ikke etter steg 5 eller 7 → rød boks på innleggingen eller resultatsiden …».
- **[lav]** Feilveien i reise 2 er egentlig et annet valg («Nytt forslag»), ikke en feil. Det mangler en feil som hører til mobilen, for eksempel at en PDF fra telefonen er skannet (EXPERIENCE.md § Key Flows, linje 352). *Forslag:* legg til én linje: «PDF-en fra telefonen er skannet → feilboks øverst, han limer inn teksten i stedet (FR-11).»
- **[lav]** I reise 3, steg 1, «viser» siden «Mangler API-nøkkel, se README» med en gang den starter, men teksten står på startsiden under bryteren (linje 239), altså i steg 3. I steg 5 står teksten «bare testdata fungerer i testmodus», som ikke er den ekte feilmeldingen «CV: I testmodus fungerer bare testdataene fra mappen testdata/.» (linje 152) (EXPERIENCE.md § Key Flows, linje 358 og 362). *Forslag:* flytt API-nøkkel-teksten til steg 3, og bruk den ekte feilmeldingen.

## 2. Tokens — adequate

**Hva ble sjekket:** alle 18 fargetokens, 15 typografitokens, 5 `rounded`- og 9 `spacing`-tokens og 27 komponenter i frontmatter, og alle 44 ulike `{…}`-henvisninger i begge filene. Alle fargetokens har fargekode, og alle henvisninger peker på et token som finnes. Kontrasten er regnet ut på nytt med WCAG-formelen:

| Par | Utregnet | Står i DESIGN.md | Brukes til |
|---|---|---|---|
| primary-contrast på primary | 6,10:1 | 6,1:1 og 6,6:1 (se funn) | Hovedknapper |
| text på background | 13,36:1 | 13,4:1 | Brødtekst |
| text på surface | 14,12:1 | – | Tekst på kort |
| text-muted på background | 6,35:1 | 6,3:1 | Hjelpetekst, KI-merknad |
| text-muted på surface | 6,71:1 | – | Hjelpetekst på kort, bryterspor «av» |
| primary på background | 5,77:1 | – | Lenkeknapper og sekundærknapper på bakgrunnen |
| error på error-tint | 5,46:1 | 5,5:1 | Feilboks |
| error på surface | 6,52:1 | – | Feiltekst under felt |
| success på success-tint | 4,53:1 | 4,5:1 | «✓ Lastet ned som …», filnavn |
| success på changed-active | 4,10:1 | – | Hvis grønn tekst brukes i åpen setning (stryker) |
| text på changed-active | 11,14:1 | – | Åpen endret setning |
| work-on på work-on-tint | 6,86:1 | 6,9:1 | «Dette kan du jobbe videre med» |
| text på accent | 8,26:1 | 8,3:1 | «Testmodus», «Laget av KI» |
| hvit på text | 14,12:1 | 14,1:1 | «i»-boksen |
| focus-ring på background | 5,36:1 | 5,4:1 | Fokusring |
| focus-ring på surface | 5,67:1 | – | Fokusring på kort |
| primary på border (prosentlinje) | 4,47:1 | – | Fylt del mot sporet |
| border på surface | 1,36:1 | 1,4:1 | Bare pynt (bevisst) |
| hvit på låst knapp (55 %) | 2,56:1 | – | Låst knapp |
| låst bryter (60 %) | ca. 2,7:1 | – | Bryter uten API-nøkkel |

### Funn

- **[middels]** «På vei mot ny jobb» står i Baloo 2, ca. 1,5rem, men det finnes ikke noe typografitoken for det. `logo` har en annen størrelse (`clamp(...)`), og `components.wait-overlay` har ingen typografi (DESIGN.md § Typography, linje 282; frontmatter linje 223–227). Den som koder, må gjette. *Forslag:* legg til `typography.wait-title` (Baloo 2, 800, 1.5rem, `{colors.primary}`) og vis til det fra `wait-overlay`.
- **[lav]** Kontrasten for hovedfargen mot hvit står med to ulike tall: 6,1:1 (linje 253) og 6,6:1 (linje 274). Utregnet er den 6,10:1 (DESIGN.md § Colors). *Forslag:* rett linje 274 til 6,1:1.
- **[lav]** Kontrasten er ikke oppgitt for flere par som brukes mye: primary på background (5,77), error på surface (6,52), focus-ring på surface (5,67), text-muted på surface (6,71, bryterspor «av», krever 3:1) og prosentlinjen (4,47). Alle består. Den låste bryteren uten API-nøkkel har bare ca. 2,7:1. WCAG tillater det for låste knapper, og teksten «Mangler API-nøkkel» forklarer det (DESIGN.md § Colors, linje 272). *Forslag:* legg disse tallene inn i kontrastlinjen, og skriv at låste knapper og brytere bevisst har lavere kontrast.
- **[lav]** success på success-tint er 4,53:1, så vidt over grensen på 4,5. `changed-sentence` sier ikke hvilken tekstfarge den har. Brukes grønn tekst på den åpne setningen (`changed-active`), blir det bare 4,10:1, og det er for lite (DESIGN.md frontmatter, linje 211–214). *Forslag:* legg `foreground: '{colors.text}'` på `changed-sentence`.
- **[lav]** Noen verdier er skrevet rett inn i stedet for som tokens: `info-tip.foreground: '#FFFFFF'` (bør være `{colors.primary-contrast}`), hjørnene 13 px, 12 px og 10 px utenfor skalaen, `padding: '12px 20px'`, som er `{spacing.3} {spacing.5}`, og skyggene som `rgba(...)` (DESIGN.md frontmatter, linje 115–192; § Elevation & Depth, linje 317–319). Det gjør det vanskeligere å legge til mørk modus senere. *Forslag:* bytt til tokens der de finnes. Gjør 13 px om til et token (for eksempel `rounded.input`), og vurder `shadow`- og `shadow-hover`-tokens.
- **[lav]** «Bare fra skissene (… ikke egne avgjørelser i memloggen)» står ved `error-tint`, `work-on`, `work-on-tint`, `changed-active`, `dot-middle` og `fireworks-gold` (DESIGN.md linje 25 og 265). Den som koder, kan ikke vite om disse fargene er bestemt. *Forslag:* be Kristine bekrefte dem og ta bort forbeholdet.

## 3. Komponenter — thin

**Hva ble sjekket:** alle komponentnavn i begge filene, og om hver av dem har en rad i DESIGN.md § Components (utseende) *og* i EXPERIENCE.md § Component Patterns (oppførsel).

| Komponent | DESIGN.md | EXPERIENCE.md CP |
|---|---|---|
| Hovedknapp, sekundærknapp, stor knapp, nedlastet-knapp | Ja | Ja |
| Modus-kort, innleggingsfelt, testmodus-bryter, merkelapp «Testmodus» | Ja | Ja |
| «i»-ikon og «i»-boks, ATS-forklaring, endret setning, ventetegn, feilboks | Ja | Ja |
| Nøkkelordtreff (`score-meter`) | Ja | Som «Prosentlinje» og «Nøkkelordlister» |
| Vindu (`dialog`) | Ja | To av tre vinduer |
| Hjørnerad (`corner-row`) | Ja | Bare «Logg ut» |
| Lenkeknapp, tekstfelt, tekstboks, filnavn (`file-chip`), skjemafeil | Ja | **Nei** |
| Merket «Laget av KI», gap-lister, brevet, gammel setning | Ja | **Nei** |
| Forklaring i Korrektur, hjelpetekst for testdata | Ja | **Nei** |
| Søppelbøtte | **Nei** (bare nevnt) | Ja |
| Samtykke / avkrysningsboks | **Nei** (bare rammefarge) | Ja |
| Vindu «Logg ut før nedlasting» | **Nei** | **Nei** (bare i State Patterns) |

### Funn

- **[høy]** Vinduet «Du har ikke lastet ned brevet. Vil du logge ut likevel?» står bare i State Patterns (EXPERIENCE.md linje 255). Det mangler i IA-tabellen (linje 37–38) og i Component Patterns. Interaction Primitives sier «Esc lukker *begge* vinduene» og nevner bare «Bli her» og «Avbryt» som trygge valg (linje 263). Raden «Logg ut» i Component Patterns sier at man «logger ut med en gang» (linje 224), altså det motsatte av vinduet. En utvikler som leser Component Patterns, lager feil logg ut. *Forslag:* legg vinduet inn i IA-tabellen og Component Patterns, skriv «alle tre vinduene» i Interaction Primitives, og skriv unntaket i raden «Logg ut»: «… unntatt på brevsiden før nedlasting, se State Patterns».
- **[middels]** Avkrysningsboksen for samtykket har ingen komponent i DESIGN.md: størrelse, hvordan den ser ut når den er krysset av, og hvordan den ser ut ved feil. EXPERIENCE.md sier «rød ramme rundt boksen» (linje 237), men det er uklart om det betyr selve avkrysningsboksen eller hele samtykkeområdet (DESIGN.md § Components; § Colors, linje 274). *Forslag:* legg til `checkbox` i frontmatter og en linje i Components.
- **[middels]** Søppelbøtta har ingen egen komponent i DESIGN.md. Den er bare nevnt i teksten om filnavnet og i bevegelse-tabellen. Størrelse og trykkflate står ikke, og den er en knapp med bare ikon (DESIGN.md § Components, linje 365–366). *Forslag:* legg til `trash-button` med trykkflate på minst 24 × 24 px (WCAG 2.2, 2.5.8) og fokusring.
- **[middels]** Hjørneraden er beskrevet som «nederst på hver side» (DESIGN.md linje 381), uten bakgrunn eller høyde. EXPERIENCE.md sier at den er festet til bunnen av skjermen, og at siden får like mye luft nederst som raden er høy (linje 49). En fast rad trenger bakgrunn, ellers ruller innholdet under teksten, og den trenger en høyde å regne luften ut fra. *Forslag:* legg `background: '{colors.background}'` (eller surface), en høyde eller padding og en kantlinje eller skygge oppe i `components.corner-row`, og skriv «festet til bunnen av skjermen» i DESIGN.md.
- **[middels]** Tolv komponenter i DESIGN.md har ingen rad i Component Patterns (se tabellen). Flere av dem er bare visning, men det må stå, ellers vet ikke den som koder om de skal kunne trykkes på. Noen har ekte oppførsel som bare står i DESIGN.md: filnavnet kuttes med «…» (linje 365), og tekstboksen kan dras større (linje 366). *Forslag:* legg inn én kort rad per komponent, for eksempel «Merket «Laget av KI» · Resultatside · Bare visning».
- **[middels]** Ventetegnet: «Skissene har ingen avbryt-knapp» (EXPERIENCE.md linje 222) forteller hva skissen viser, ikke hva som er bestemt. PRD-en sier at et brev kan ta 20–30 sekunder (§ 8). Om man kan avbryte eller ikke, er en avgjørelse som arkitekturen og den som lager stories, trenger. *Forslag:* skriv «Ingen avbryt-knapp i versjon 1. Tar det for lang tid, kommer KI-feilen (FR-28).», eller legg til en avbryt-knapp.

## 4. Tilstander — adequate

**Hva ble sjekket:** hver side i IA-tabellen, og om den har tilstandene den trenger: tom, venter, fokus, feil, uten nett og ikke tilgang.

| Side | Tom | Venter | Feil | Fokus | Uten nett | Ikke tilgang |
|---|---|---|---|---|---|---|
| Innlogging / registrering | Ja | Mangler (lav) | Ja | Ja | – | Ja (FR-7) |
| Startside | Ja | – | Ja | Ja | – | – |
| Modusvalg | – | – | – | Ja | – | – |
| Innlegging | Ja | Ja (KI), mangler for PDF | Ja, men *når* er uklart | Ja | Ja (nettverksfeil) | – |
| Resultatside | Ja (tomme lister) | Ja | Ja | Ja | Ja | – |
| Brevside | Mangler (ingen endringer) | Ja | Ja (KI), mangler (nedlasting) | Ja | Ja | – |
| Vinduer | – | – | – | Ja | – | – |

### Funn

- **[høy]** Det står ikke *når* det man har lagt inn, blir sjekket. Kommer feil filtype (FR-10), for stor fil (FR-12), uleselig PDF (FR-11) og «bare testdata» (FR-34) med en gang filen er valgt, eller først når man trykker «Sjekk CV-en min»? (EXPERIENCE.md § State Patterns, linje 244; § Component Patterns, linje 208.) Svaret bestemmer når PDF-en leses (arkitektur), og hvordan stories og tester skrives. *Forslag:* bestem det og skriv det i State Patterns, for eksempel: «Filtype og størrelse sjekkes med en gang filen er valgt. Feltet får rød ramme, og feilboksen kommer. Tomme felt, uleselig PDF og testdata sjekkes når man trykker «Sjekk CV-en min».»
- **[middels]** Korrektur uten endringer: det står ikke hva brevsiden viser hvis KI-en ikke har endret en eneste setning. Forklaringen «Grønn og understreket = endret» blir da misvisende (EXPERIENCE.md § State Patterns). *Forslag:* legg til en tilstand, for eksempel «Vi fant ingenting å endre. Brevet ditt er bra som det er.», og skjul forklaringen.
- **[lav]** Ingen tilstand mens en PDF lastes opp og leses. På mobil kan det ta et øyeblikk (EXPERIENCE.md § State Patterns, «Fylt felt»). *Forslag:* si at filnavnet vises med en gang, eller legg inn en kort tekst, for eksempel «Leser filen …».
- **[lav]** Ingen tilstand når nedlastingen feiler, altså når Word- eller PDF-filen ikke kan lages (EXPERIENCE.md § State Patterns). *Forslag:* bruk feilboksen med «Prøv igjen», som ved KI-feil.
- **[lav]** «Nytt forslag» i testmodus: testmodus bruker ferdige svar (FR-38). Det står ikke om sensor får det samme brevet en gang til eller et annet ferdig svar. *Forslag:* skriv hva sensor ser, eller overlat det til arkitekturen og skriv det.
- **[lav]** Innlogging og registrering har ingen «sender»-tilstand, altså at knappen er låst mens innloggingen sjekkes. *Forslag:* én linje i State Patterns, eller skriv at det ikke trengs fordi innloggingen er lokal (NFR-5).
- **[lav]** Det står ikke hva som skjer med samtykket hvis man krysser av, slår testmodus på og så av igjen, mens man fortsatt er på startsiden (EXPERIENCE.md linje 253 gjelder bare når man *kommer til* startsiden). *Forslag:* «Slås testmodus av, er avkrysningsboksen tom.»

## 5. Skisser — adequate

**Hva ble sjekket:** `mockups/` og `wireframes/` finnes ikke ennå (det er planlagt). `imports/` er tom (memlog). `.working/` har 12 filer: `border-contrast-1`, `color-themes-1`, `color-themes-2`, `download-options-1`, `input-page-1`, `korrektur-markings-1`, `letter-page-1`, `login-register-1`, `logo-fonts-1`, `mode-select-1`, `result-page-1` og `start-page-1` (alle `.html`). Alle fargekoder i side-skissene er tokens fra DESIGN.md (bortsett fra bakgrunnen rundt skissen og telefonrammen). Alle tekstene i «Tekster per side» ble søkt opp i skissene, og alle fantes, bortsett fra én (se funn).

**Hvilke skisser bør lenkes fra hvilke seksjoner** (når de er flyttet til `mockups/`):

| Seksjon | Skisser |
|---|---|
| DESIGN § Brand & Style | `color-themes-1`, `color-themes-2` (lenket) |
| DESIGN § Colors | `border-contrast-1` (lenket) |
| DESIGN § Typography | `logo-fonts-1` (**ikke lenket**) |
| DESIGN § Layout & Spacing | `login-register-1`, `start-page-1`, `mode-select-1`, `input-page-1`, `result-page-1`, `letter-page-1` (lenket) |
| DESIGN § Elevation & Depth / Bevegelse | `mode-select-1` (kort ved hover), `input-page-1` (ventetegn), `result-page-1` (prosentlinje), `letter-page-1` (fyrverkeri) |
| DESIGN § Components | de seks sideskissene, og `korrektur-markings-1` (endret setning) og `download-options-1` (nedlastet-knapp) |
| EXPERIENCE § Skisser | alle (lenket), men **`border-contrast-1` mangler** |
| EXPERIENCE § State Patterns | `login-register-1`, `start-page-1`, `input-page-1`, `result-page-1`, `letter-page-1` |
| EXPERIENCE § Key Flows, reise 1 og 2 | `login-register-1` → `start-page-1` → `mode-select-1` → `input-page-1` → `result-page-1` → `letter-page-1` (reise 2 på mobil, Korrektur) |
| EXPERIENCE § Key Flows, reise 3 | `start-page-1` (testmodus, uten API-nøkkel), `input-page-1` (testmodus og feil), `letter-page-1` |

**Andre avvik mellom skisse og dokument enn runde 2:** resultatsiden i Korrektur (se funn), merkelappen «Testmodus» står i 0,78rem i skissen, men `typography.tag` er 0,75rem, og brevteksten står i 0,98rem i skissen, men `body` er 1rem. De to siste er så små at det holder å følge dokumentet.

### Funn

- **[lav]** Ingen skisse viser resultatsiden i Korrektur med knappen «Oppdater søknadsbrevet mitt». `result-page-1.html` viser bare Full generering. Avgjørelsen er fra reise 2 (memlog linje 66), ikke fra runde 2 (EXPERIENCE.md linje 75 og 167). *Forslag:* legg til en Full generering / Korrektur-bryter i `result-page-1.html` når skissene oppdateres.
- **[lav]** Skissetabellen i EXPERIENCE.md mangler `border-contrast-1.html`, selv om DESIGN.md viser til den (EXPERIENCE.md § Skisser, linje 69–79; DESIGN.md linje 274). *Forslag:* legg til en rad.
- **[lav]** DESIGN.md § Typography viser ikke til `logo-fonts-1.html`, men EXPERIENCE.md sier «se DESIGN.md» om den (EXPERIENCE.md linje 79). *Forslag:* legg til «→ Logoskrift: `mockups/logo-fonts-1.html` (Baloo 2 er valgt).»

## 6. Overflødig tekst — strong

**Hva ble sjekket:** pikselmål der tokens finnes, tekst som bare gjentar kildene, tekst der en tabell ville vært bedre, og seksjoner ingen vil lese. «Tekster per side» er lang, men nyttig. Den er tekstkontrakten for den som koder, og ikke overflødig.

### Funn

- **[lav]** § Testmodus gjentar FR-32 til FR-36 og rader som allerede står i IA-tabellen og State Patterns (EXPERIENCE.md linje 312–317). Bare to ting er nye: hjelpeteksten og at det ikke er noen knapp som fyller inn testdata. *Forslag:* kutt seksjonen ned til de to nye tingene, eller flytt dem til State Patterns og ta bort seksjonen.
- **[lav]** § Filnavn ved nedlasting står under Voice and Tone, men er en regel for hvordan nettsiden virker, ikke en tekst på skjermen (EXPERIENCE.md linje 193–197). *Forslag:* flytt den til Component Patterns («Nedlastingsknapper») eller til en egen underseksjon.
- **[lav]** Pikselmål som allerede er tokens, står en gang til i teksten om komponentene: «26 px hjørner» (linje 357), «24 × 64 px» (linje 359) og «høyst 720 px» (linje 376). Endres tokenet, blir teksten feil (DESIGN.md § Components). *Forslag:* skriv tokennavnet, for eksempel `{rounded.lg}`.

## 7. Arv fra kildene — adequate

**Hva ble sjekket:** `sources` i frontmatter: `../../prds/prd-kode-prosjekt-2026-10-09/prd.md` og `addendum.md` finnes fra arbeidsmappen. Begrepene fra ordlisten i PRD-en (Full generering, Korrektur, Gap-analyse, Nøkkelordtreff, Testmodus, Vanlig modus, Økt) brukes likt. «Mangler» / «Dette kan du jobbe videre med» er et bevisst valg og er forklart (EXPERIENCE.md linje 87). Den eneste tokenhenvisningen i EXPERIENCE.md, `{colors.focus-ring}`, finnes i DESIGN.md.

### Funn

- **[middels]** Komponentene har ikke de samme navnene i de to filene. «Nøkkelordtreff (`score-meter`)» i DESIGN.md heter «Prosentlinje» og «Nøkkelordlister» i EXPERIENCE.md. «Vindu (`dialog`)» heter «Vindu etter nedlasting» og «Vindu «Nytt forslag»». «Hjørnerad» heter «Faste elementer» og «Logg ut». Og «Filnavn» brukes om to ting: den grønne stripen på innleggingen (`file-chip`) og «Filnavn: Soknad_…» under nedlastingsknappene (DESIGN.md linje 365; EXPERIENCE.md linje 174 og 193). Den som lager stories, kan lage dobbelt eller blande dem sammen. *Forslag:* bruk ett navn per komponent i begge filene, gjerne med tokennavnet i parentes, og gi «Filnavn: …» under nedlastingsknappene et eget navn (for eksempel «Filnavn-linje»).
- **[lav]** FR-numrene står forskjellig for samme side: IA-tabellen sier FR-14–FR-19 og FR-21 for resultatsiden (linje 34), men «Tekster per side» sier FR-14–FR-18 og FR-21 (linje 156). Brevsiden har FR-22–FR-31, og det tar med FR-24, som ikke har noen skjermdel (linje 169). *Forslag:* bruk de samme numrene begge steder.
- **[lav]** Bevisste avvik fra kildene er ikke merket i dokumentene. Det gjelder «Feil e-post eller passord» uten rød ramme (avviker fra addendum, memlog linje 136; EXPERIENCE.md linje 231), samtykket på nytt hver gang man kommer til startsiden (strengere enn FR-36, linje 253), og «Gjenta passord» og «Tilbake» på innleggingen (tillegg i UX). Arkitekturen og den som lager stories, ser bare dokumentene. *Forslag:* skriv «(bevisst avvik fra addendum)» eller «(tillegg i UX)» der det står, eller lag en kort liste «Avvik fra PRD og addendum».

## 8. Form — strong

**Hva ble sjekket:** DESIGN.md har seksjonene i riktig rekkefølge: Brand & Style → Colors → Typography → Layout & Spacing → Elevation & Depth (med underseksjonen Bevegelse) → Shapes → Components → Do's and Don'ts. EXPERIENCE.md har alle de faste seksjonene: Foundation, Information Architecture, Voice and Tone, Component Patterns, State Patterns, Interaction Primitives, Accessibility Floor og Key Flows. Den har også Responsive & Platform, fordi det er et bruddpunkt (700 px). Egne seksjoner: «Skisser» fortjener plassen (henvisning til skissene, som `→ Composition reference` i eksemplene), «Tekster per side» fortjener plassen, og «Testmodus» bare delvis (se 6). At Bevegelse står under Elevation & Depth, er greit, fordi spesifikasjonen ikke har noen egen plass for det.

### Funn

- **[lav]** Responsive-tabellen har kolonnene «PC» og «Mobil (375 px)», men regelen går ved 700 px. Da er det uklart hvilken kolonne nettbrett (768 px) hører til, helt til man leser linjen under tabellen (EXPERIENCE.md § Responsive & Platform, linje 288–302). *Forslag:* kall kolonnene «Fra 700 px (PC og nettbrett)» og «Under 700 px (mobil)».

## Mekaniske merknader

- **Dobbel setning:** DESIGN.md linje 280 sier to ganger at logoen står i Baloo 2 ExtraBold (800). Ta bort den andre.
- **Plassholder:** EXPERIENCE.md linje 19 har `{path.to.token}`. Det er et eksempel fra malen, ikke et token. Et verktøy som slår opp henvisninger, vil ikke finne det. Skriv for eksempel «tokens skrives som `{colors.primary}`».
- **Forkortet henvisning:** DESIGN.md linje 291 og 299 skriver `{typography.heading-letter}` / `-mobile` og `{typography.button-hero}` / `-mobile`. Skriv hele navnene: `{typography.heading-letter-mobile}` og `{typography.button-hero-mobile}`.
- **Komponent som verdi:** `components.corner-row.logout: '{components.button-secondary}'` (DESIGN.md linje 230) viser til en komponent, ikke et token. Spesifikasjonen viser bare tokenhenvisninger. Det fungerer for mennesker, men et verktøy kan stoppe på det.
- **Ikke en CSS-verdi:** `testmode-toggle.size: '44px x 24px'` (linje 184). Del den opp i `width: 44px` og `height: 24px`.
- **Ingen reserveskrift:** `typography.logo.fontFamily: 'Baloo 2'` har ingen reserveskrift. Legg til `'Baloo 2', {typography.body.fontFamily}`, i tilfelle skriften ikke lastes.
- **Feil kontrasttall:** «6,6:1» på DESIGN.md linje 274 skal være 6,1:1 (se 2).
- **Frontmatter:** begge filene har `name`, `status: draft`, `created`, `updated` og `sources`, og `name` er lik i begge. DESIGN.md har også `description`. De ekstra feltene (`status`, `sources` osv.) er ikke med i DESIGN.md-spesifikasjonen, men er greie å ha.
- **Mermaid:** ingen diagrammer i noen av filene, så det er ingenting å sjekke.
- **Skissestier:** alle `mockups/…`-stier peker på filer som ennå ligger i `.working/`. Det er planlagt og regnes ikke som feil, men sjekk stiene når filene er flyttet.
