# Gjennomgang av UX (runde 3) — Søknadsassistenten

- **DESIGN.md:** `DESIGN.md`
- **EXPERIENCE.md:** `EXPERIENCE.md`
- **Laget:** 2026-10-22 22:01

## Samlet vurdering

De to dokumentene fungerer godt som kontrakt for arkitektur og stories. Alle FR-er med en skjermdel har en side og en oppførsel, alle fargetokens har fargekode, og alle tokenhenvisninger peker på noe som finnes. Ingen av de tre hjelperne fant kritiske feil.

Det som må rettes før status final: det tredje vinduet («Logg ut før nedlasting») er bare halvveis lagt inn, det står ikke når det man legger inn blir sjekket, og det står ikke hvordan endrede setninger i Korrektur skal finnes. Tilgjengelighetshjelperen fant fem høye funn om fokus og skjermleser i det som «dukker opp» (fast rad, vinduer, ventetegn, «i»-boks) og om 320 px / 200 % tekst. Sensor-hjelperen mener UX-delen ligger an til A–B på kriterium 4, men advarer om at pynten trenger en kutterekkefølge så den ikke spiser tid fra kjerneflyten og testene.

Flere funn går igjen hos to eller tre hjelpere (se «Samme som»). Til sammen: kritisk 0 · høy 9 · middels 21 · lav 33. Det er 63 funn, men rundt ti av dem er det samme funnet sett av flere hjelpere.

## Vurdering per kategori (sjekklisten)

- 1. Brukerreiser og krav — sterk
- 2. Tokens — god nok
- 3. Komponenter — tynn
- 4. Tilstander — god nok
- 5. Skisser — god nok
- 6. Overflødig tekst — sterk
- 7. Arv fra kildene — god nok
- 8. Form — sterk

## Funn etter alvorlighet

### Kritisk (0)

Ingen.

### Høy (9)

**A-10 [Sjekkliste – Komponenter]** — Vinduet «Logg ut før nedlasting» er bare halvveis lagt inn (§ EXPERIENCE § State Patterns l. 255; § Component Patterns l. 224; § Interaction Primitives l. 263)  
Står bare i State Patterns. Raden «Logg ut» sier «logger ut med en gang». «Esc lukker begge vinduene», men det er tre.  
*Samme som U11 og delvis S-2*  
Forslag: Legg vinduet inn i IA-tabellen og Component Patterns, «alle tre vinduene», unntak i raden «Logg ut», fokus til «Avbryt».

**A-16 [Sjekkliste – Tilstander]** — Det står ikke NÅR det man legger inn, blir sjekket (§ EXPERIENCE § State Patterns l. 244; § Component Patterns l. 208)  
Feil filtype, for stor fil, uleselig PDF og «bare testdata»: med en gang filen er valgt, eller ved «Sjekk CV-en min»?  
Forslag: Bestem og skriv det, f.eks.: filtype og størrelse med en gang; tomme felt, uleselig PDF og testdata ved trykk.

**S-1 [Tilgjengelighet]** — Den faste raden nederst kan dekke det som har fokus, og har ingen bakgrunn (§ EXPERIENCE § IA «Faste elementer»; DESIGN Hjørnerad)  
WCAG 2.4.11. Når man tabber, kan knappen havne bak raden.  
*Samme som A-13*  
Forslag: Heltrukket bakgrunn og strek, scroll-padding-bottom, og ikke fast når skjermen er lavere enn ca. 500 px.

**S-2 [Tilgjengelighet]** — Vinduene sperrer ikke resten av siden (§ EXPERIENCE § Interaction Primitives «Vinduer»)  
WCAG 2.4.3, 4.1.2. Man kan tabbe ut av vinduet. Det tredje vinduet mangler.  
*Henger sammen med A-10*  
Forslag: <dialog> med showModal() eller inert; aria-labelledby; fokus til det trygge valget; Esc lukker alle tre.

**S-3 [Tilgjengelighet]** — Ventetegnet: fokus forsvinner, siden bak kan brukes (§ EXPERIENCE § Component Patterns «Ventetegn»)  
WCAG 2.4.3, 4.1.3. role=status på et skjult element leses ofte ikke opp.  
Forslag: Resten av siden inert, aria-disabled på knappen, statusområde som alltid finnes, fokus til ny overskrift eller feilboks etterpå.

**S-4 [Tilgjengelighet]** — «i»-boksen: skjermlesere hører ikke innholdet, og trykk og fokus kolliderer (§ EXPERIENCE § Interaction Primitives; DESIGN info-tip)  
WCAG 1.3.1, 4.1.2, 1.4.13. Fokus åpner og klikket lukker, så boksen bare blinker.  
*Samme som U4*  
Forslag: Utfoldbar forklaring med aria-expanded/aria-controls; åpnes ved trykk og hover, ikke ved fokus alene; Esc lukker.

**S-5 [Tilgjengelighet]** — 320 px, 200 % tekst og «alltid én linje» (§ DESIGN § Typography, § Layout; EXPERIENCE § Accessibility Floor)  
WCAG 1.4.10, 1.4.4. nowrap får tekst til å renne ut av skjermen.  
Forslag: Siden virker ved 320 px og 200 % zoom; én linje bare ved vanlig tekststørrelse; ingen faste høyder på ting med tekst.

**U1 [Sensor]** — Pynt og UX-tillegg har ingen kutterekkefølge (§ DESIGN § Bevegelse; EXPERIENCE § Component/State Patterns; PRD § 4 Nødliste)  
Fyrverkeri, animasjoner, ekstra vinduer, filnavn med arbeidsgiver m.m. kan ta tid fra kjerneflyt og tester (kriterium 2 og 3, til sammen 35 %).  
Forslag: UX-kuttliste med tre nivåer (kuttes først / ved tidsnød / aldri), og pynten i en egen story etter kjerneflyten.

**U2 [Sensor]** — Det står ikke hvordan endrede setninger i Korrektur skal finnes (§ EXPERIENCE «Endret setning»; Reise 2 steg 7; Reise 3 steg 8)  
Diff eller setningspar fra KI? Sammenslåtte, delte, nye og fjernede setninger? Ingen endringer?  
*Inkluderer A-17*  
Forslag: KI-en svarer med par {ny, gammel}; regler for nye, sammenslåtte og fjernede; reserve fra nødlisten punkt 4.

### Middels (21)

**A-4 [Sjekkliste – Tokens]** — Mangler typografitoken for «På vei mot ny jobb» (§ DESIGN § Typography, l. 282)  
Baloo 2, ca. 1,5rem, men ikke noe token. Den som koder, må gjette.  
Forslag: Legg til typography.wait-title (Baloo 2, 800, 1.5rem, {colors.primary}) og vis til den fra wait-overlay.

**A-11 [Sjekkliste – Komponenter]** — Avkrysningsboksen for samtykket har ingen komponent i DESIGN.md (§ DESIGN § Components)  
Størrelse, avkrysset og feil står ikke.  
Forslag: Legg til checkbox i frontmatter og en linje i Components.

**A-12 [Sjekkliste – Komponenter]** — Søppelbøtta har ingen egen komponent (§ DESIGN § Components, l. 365–366)  
Størrelse og trykkflate står ikke.  
Forslag: Legg til trash-button med minst 24 × 24 px og fokusring.

**A-13 [Sjekkliste – Komponenter]** — Den faste raden nederst har ingen bakgrunn eller høyde (§ DESIGN l. 381; EXPERIENCE l. 49)  
Uten bakgrunn ruller innholdet under teksten.  
*Samme som S-1*  
Forslag: Legg background, høyde/padding og strek øverst i components.corner-row.

**A-14 [Sjekkliste – Komponenter]** — Tolv komponenter i DESIGN.md mangler rad i Component Patterns (§ EXPERIENCE § Component Patterns)  
Lenkeknapp, tekstfelt, tekstboks, file-chip, skjemafeil, «Laget av KI», gap-lister, brevet, gammel setning, forklaring, hjelpetekst.  
Forslag: Én kort rad per komponent, f.eks. «Bare visning».

**A-15 [Sjekkliste – Komponenter]** — Ventetegnet: om man kan avbryte, er ikke bestemt (§ EXPERIENCE l. 222)  
«Skissene har ingen avbryt-knapp» beskriver skissen, ikke en avgjørelse.  
*Henger sammen med S-18 og U13*  
Forslag: «Ingen avbryt-knapp i versjon 1. Tar det for lang tid, kommer KI-feilen (FR-28).»

**A-17 [Sjekkliste – Tilstander]** — Korrektur uten endringer har ingen tilstand (§ EXPERIENCE § State Patterns)  
Forklaringen «Grønn og understreket = endret» blir misvisende.  
*Samme som del av U2*  
Forslag: «Vi fant ingenting å endre. Brevet ditt er bra som det er.» og skjul forklaringen.

**A-29 [Sjekkliste – Arv fra kildene]** — Komponentene har ulike navn i de to filene (§ DESIGN l. 365; EXPERIENCE l. 174, 193)  
score-meter = «Prosentlinje»/«Nøkkelordlister»; dialog = to vinduer med egne navn; «Hjørnerad» = «Faste elementer»; «Filnavn» brukes om to ting.  
Forslag: Ett navn per komponent i begge filene; kall linja under nedlastingsknappene «Filnavn-linje».

**S-6 [Tilgjengelighet]** — Sidetittel og fokus ved ny side (§ EXPERIENCE § IA; § Accessibility Floor)  
WCAG 2.4.2.  
*Samme som U7*  
Forslag: Egen <title> per side; fokus til hovedoverskriften ved sidebytte.

**S-7 [Tilgjengelighet]** — Overskriftsnivåer og landemerker er ikke bestemt (§ DESIGN § Typography)  
WCAG 1.3.1, 2.4.6. Skissene mangler h1.  
*Samme som del av U7*  
Forslag: Sideoverskrift h1, bokser h2, lister h3; «i» og merket ved siden av overskriften; header/main/footer.

**S-8 [Tilgjengelighet]** — Like knappenavn i de tre innleggingsfeltene (§ EXPERIENCE § Component Patterns «Innleggingsfelt»)  
WCAG 2.4.6. Tre like «Last opp PDF».  
Forslag: Feltnavnet med for skjermlesere («Last opp PDF, CV»); accept=".pdf".

**S-9 [Tilgjengelighet]** — Fokus etter søppelbøtte og opplasting (§ EXPERIENCE § Component Patterns)  
WCAG 2.4.3.  
Forslag: Etter tømming til «Last opp PDF»; etter opplasting til søppelbøtta, med opplest melding.

**S-10 [Tilgjengelighet]** — Endrede setninger forklares bare med farge og strek (§ EXPERIENCE «Endret setning»)  
WCAG 1.3.1, 1.3.3.  
Forslag: Skjult tekst «Endret setning»; aria-expanded; Enter og mellomrom.

**S-11 [Tilgjengelighet]** — Feilboksen og feltene er ikke koblet sammen (§ EXPERIENCE § State Patterns; § Accessibility Floor)  
WCAG 3.3.1.  
Forslag: Linjene i feilboksen er lenker til feltet; feiltekst under feltnavnet med aria-describedby.

**U3 [Sensor]** — Tilbake til startsiden: tømmes feltene, og kan testmodus byttes midt i en søknad? (§ EXPERIENCE § IA Navigasjon; § Testmodus; PRD FR-32)  
Kan stride mot FR-32. Også uklart hva bryteren husker, og hvor man havner etter innlogging.  
*Henger sammen med A-22*  
Forslag: Startsiden starter alltid ny søknad; bryteren husker valget i økten; etter innlogging alltid til startsiden.

**U4 [Sensor]** — «i»-boksen skal åpnes på tre måter, og skissen har trolig feil (§ EXPERIENCE § Interaction Primitives; start-page-1.html, result-page-1.html)  
Fokus åpner og klikket lukker med en gang.  
*Samme som S-4*  
Forslag: Trykk/Enter/mellomrom åpner og lukker, Esc lukker, hover på PC; dropp «åpnes ved fokus». Prøv skissen i Chrome og logg KI-feilen.

**U5 [Sensor]** — Nettbrett (768 px) er ikke prøvd; tre felt side om side blir trolig trangt (§ DESIGN § Layout & Spacing; EXPERIENCE § Responsive)  
Ca. 195 px innhold per felt i Korrektur.  
Forslag: Tre felt side om side først fra 1000 px; ekte @media i skissene; prøv 768 px i nettleseren.

**U6 [Sensor]** — Filnavnet med arbeidsgiver er en skjult ny KI-oppgave (§ EXPERIENCE § Filnavn ved nedlasting)  
PRD har fire KI-oppgaver; dette blir en femte, med testdata og regler.  
Forslag: Ekstra felt i samme KI-svar som nøkkelordene, maks 30 tegn, reserve Soknad_<dato>; på kuttlisten; enhetstest for filnavnfunksjonen.

**U7 [Sensor]** — Fokus, sidetitler og overskrifter ved sidebytte (§ EXPERIENCE § Accessibility Floor)  
*Samme som S-6, S-7, S-12*  
Forslag: Fokus til h1 ved ny side, egen <title>, lang="nb", emoji skjules.

**U8 [Sensor]** — UX-tillegg og avvik fra PRD står spredt (§ EXPERIENCE (flere steder))  
Sensor må lese hele memloggen. Stories kan følge PRD og UX ulikt.  
*Samme som A-31*  
Forslag: Tabell «Tillegg og avvik fra PRD-en» nederst i EXPERIENCE.md (6–8 rader).

**U9 [Sensor]** — Vanskelig å se hva du bestemte selv, og hva KI-en foreslo (§ memlog; prompt-logg)  
Dokumentene ser polerte ut; styringen må letes fram.  
Forslag: Kort fil my-project/3-ux/mine-valg-og-ki-feil.md med 8–10 punkter og lenker.

### Lav (33)

**A-1 [Sjekkliste – Brukerreiser og krav]** — Feilveien i reise 1 viser til feil steg (§ EXPERIENCE § Key Flows, l. 337)  
Feilen vises etter steg 5 eller 7 (innlegging/resultatside), ikke i steg 6 eller 8.  
Forslag: «KI-en svarer ikke etter steg 5 eller 7 → rød boks på innleggingen eller resultatsiden …»

**A-2 [Sjekkliste – Brukerreiser og krav]** — Reise 2 mangler en ekte feil (§ EXPERIENCE § Key Flows, l. 352)  
«Nytt forslag» er et valg, ikke en feil.  
Forslag: Legg til: «PDF-en fra telefonen er skannet → feilboks, han limer inn teksten i stedet (FR-11).»

**A-3 [Sjekkliste – Brukerreiser og krav]** — Reise 3: API-nøkkel-tekst i feil steg og ikke ordrett feilmelding (§ EXPERIENCE § Key Flows, l. 358 og 362)  
Teksten står på startsiden (steg 3), og steg 5 bruker ikke den ekte feilmeldingen.  
Forslag: Flytt teksten til steg 3, og bruk «CV: I testmodus fungerer bare testdataene fra mappen testdata/.»

**A-5 [Sjekkliste – Tokens]** — Kontrasttallet for hovedfargen står som både 6,1:1 og 6,6:1 (§ DESIGN § Colors, l. 274; memlog)  
Riktig er 6,10:1.  
*Samme som S-14 og U10*  
Forslag: Rett 6,6 til 6,1 (og i memloggen).

**A-6 [Sjekkliste – Tokens]** — Kontrast mangler for flere par som brukes mye (§ DESIGN § Colors, l. 272)  
primary på background 5,77, error på surface 6,52, focus-ring på surface 5,67, bryterspor 6,71. Alle består.  
Forslag: Legg tallene inn, og skriv at låste knapper og brytere bevisst har lavere kontrast.

**A-7 [Sjekkliste – Tokens]** — Grønn tekst på åpen endret setning stryker (4,10:1) (§ DESIGN frontmatter, l. 211–214)  
changed-sentence sier ikke hvilken tekstfarge den har.  
Forslag: Legg foreground: '{colors.text}' på changed-sentence.

**A-8 [Sjekkliste – Tokens]** — Noen verdier er skrevet rett inn i stedet for som tokens (§ DESIGN frontmatter, l. 115–192)  
#FFFFFF, hjørner 13/12/10 px, padding 12px 20px, skygger som rgba.  
*Samme som U12*  
Forslag: Bytt til tokens der de finnes; vurder rounded.input og shadow-tokens.

**A-9 [Sjekkliste – Tokens]** — Seks farger står bare «fra skissene» (§ DESIGN l. 25 og 265)  
error-tint, work-on, work-on-tint, changed-active, dot-middle, fireworks-gold er ikke bekreftet i memloggen.  
Forslag: Kristine bekrefter dem, og forbeholdet tas bort.

**A-18 [Sjekkliste – Tilstander]** — Ingen tilstand mens PDF leses (§ EXPERIENCE § State Patterns)  
Kan ta et øyeblikk på mobil.  
Forslag: Filnavnet vises med en gang, eller «Leser filen …».

**A-19 [Sjekkliste – Tilstander]** — Ingen tilstand når nedlastingen feiler (§ EXPERIENCE § State Patterns)  
Forslag: Feilboks med «Prøv igjen», som ved KI-feil.

**A-20 [Sjekkliste – Tilstander]** — «Nytt forslag» i testmodus er uklart (§ EXPERIENCE § Testmodus)  
Samme ferdige brev en gang til, eller et annet?  
Forslag: Skriv hva sensor ser, eller overlat det til arkitekturen.

**A-21 [Sjekkliste – Tilstander]** — Innlogging har ingen «sender»-tilstand (§ EXPERIENCE § State Patterns)  
Forslag: Én linje, eller skriv at det ikke trengs (lokal innlogging, NFR-5).

**A-22 [Sjekkliste – Tilstander]** — Samtykke når testmodus slås på og av igjen (§ EXPERIENCE l. 253)  
*Henger sammen med U3*  
Forslag: «Slås testmodus av, er avkrysningsboksen tom.»

**A-23 [Sjekkliste – Skisser]** — Ingen skisse viser resultatsiden i Korrektur (§ result-page-1.html; EXPERIENCE l. 75, 167)  
Knappen «Oppdater søknadsbrevet mitt» finnes ikke i noen skisse.  
Forslag: Legg til Full generering / Korrektur-bryter i result-page-1.html.

**A-24 [Sjekkliste – Skisser]** — Skissetabellen mangler border-contrast-1.html (§ EXPERIENCE § Skisser, l. 69–79)  
Forslag: Legg til en rad.

**A-25 [Sjekkliste – Skisser]** — DESIGN § Typography lenker ikke til logo-fonts-1.html (§ DESIGN § Typography)  
Forslag: Legg til lenken (Baloo 2 er valgt).

**A-26 [Sjekkliste – Overflødig tekst]** — § Testmodus gjentar FR-32–FR-36 (§ EXPERIENCE l. 312–317)  
Bare hjelpeteksten og «ingen fylle-knapp» er nytt.  
Forslag: Kutt ned til de to nye tingene, eller flytt dem til State Patterns.

**A-27 [Sjekkliste – Overflødig tekst]** — § Filnavn ved nedlasting står under Voice and Tone (§ EXPERIENCE l. 193–197)  
Det er en regel, ikke en tekst på skjermen.  
Forslag: Flytt til Component Patterns.

**A-28 [Sjekkliste – Overflødig tekst]** — Pikselmål gjentatt i teksten (§ DESIGN § Components, l. 357, 359, 376)  
Endres tokenet, blir teksten feil.  
Forslag: Skriv tokennavnet, f.eks. {rounded.lg}.

**A-30 [Sjekkliste – Arv fra kildene]** — FR-numrene står forskjellig for samme side (§ EXPERIENCE l. 34, 156, 169)  
Forslag: Bruk de samme numrene begge steder.

**A-31 [Sjekkliste – Arv fra kildene]** — Bevisste avvik fra kildene er ikke merket (§ EXPERIENCE l. 231, 253 m.fl.)  
Feil innlogging uten rød ramme, samtykke hver gang, «Gjenta passord», «Tilbake».  
*Samme som U8*  
Forslag: Merk «(tillegg i UX)» / «(bevisst avvik)», eller lag en liste.

**A-32 [Sjekkliste – Form]** — Kolonnenavnene i Responsive-tabellen passer ikke med 700 px (§ EXPERIENCE § Responsive & Platform, l. 288–302)  
Uklart hvor nettbrett hører hjemme.  
Forslag: «Fra 700 px (PC og nettbrett)» og «Under 700 px (mobil)».

**S-12 [Tilgjengelighet]** — lang="no" i stedet for "nb" (§ EXPERIENCE § Foundation)  
WCAG 3.1.1.  
*Samme som del av U7*  
Forslag: <html lang="nb">.

**S-13 [Tilgjengelighet]** — Noen emojier og tegn mangler i lista over pynt (§ EXPERIENCE § Accessibility Floor)  
🎉, ⓘ, →, ✓, ○.  
Forslag: Skjul dem for skjermlesere.

**S-14 [Tilgjengelighet]** — Feil kontrasttall og utdatert tekst om bryteren (§ DESIGN § Colors)  
6,6 → 6,1; bryteren er ikke lenger rosa; grønn har ingen margin; fokusringen trenger alltid 2 px luft (1,1:1 uten).  
*Samme som A-5 og U10*  
Forslag: Rett tallene og legg til de to setningene.

**S-15 [Tilgjengelighet]** — Den låste bryteren forsvinner for tastatur og skjermleser (§ EXPERIENCE «Testmodus-bryter»)  
WCAG 4.1.2.  
Forslag: role=switch, aria-disabled (kan nås med Tab), «Mangler API-nøkkel» med aria-describedby.

**S-16 [Tilgjengelighet]** — Innlogging: autofyll, fokus og e-post med feil form (§ EXPERIENCE § Voice and Tone, Innlogging)  
WCAG 1.3.5, 3.3.8.  
Forslag: autocomplete-verdier, liming lov, fokus til rød boks, «Skriv e-posten slik: navn@eksempel.no».

**S-17 [Tilgjengelighet]** — Dobbel opplesning og filnavn som drukner (§ EXPERIENCE § Accessibility Floor)  
WCAG 4.1.3.  
Forslag: Feilboksen får fokus, men ikke role=alert; filnavnet står i vinduet.

**S-18 [Tilgjengelighet]** — Ingenting om tidsavbrudd i økten (§ EXPERIENCE «Logg ut»)  
WCAG 2.2.1.  
*Henger sammen med A-15*  
Forslag: Ingen automatisk utlogging; KI-feil etter fast tid.

**U10 [Sensor]** — Kontrasttallet for hovedfargen står med to verdier (§ DESIGN § Colors; memlog)  
*Samme som A-5 og S-14*  
Forslag: Rett 6,6 til 6,1; legg til primary på background 5,8:1; nevn verktøyet.

**U11 [Sensor]** — Vinduet «Logg ut før nedlasting» mangler i oversikten (§ EXPERIENCE § IA, § Component Patterns)  
*Samme som A-10*  
Forslag: Legg det inn; «Esc lukker alle vinduene»; fokus til «Avbryt».

**U12 [Sensor]** — Noen verdier ligger utenfor skalaene (§ DESIGN frontmatter, § Shapes)  
*Samme som A-8*  
Forslag: Regel: verdier utenfor skalaen rundes til nærmeste token; vurder å slå sammen like typografitokens.

**U13 [Sensor]** — Venteteksten lover «noen sekunder», men brevet kan ta 30 (§ EXPERIENCE § Voice and Tone «Ventetegn»; PRD § 8)  
Folk kan tro siden har hengt seg.  
*Henger sammen med A-15*  
Forslag: «… det kan ta opptil et halvt minutt.» Eventuelt «Fortsatt i gang …» etter 10 sekunder.

## Mekaniske merknader

- DESIGN.md l. 280 sier to ganger at logoen står i Baloo 2 ExtraBold (800).
- EXPERIENCE.md l. 19 har plassholderen {path.to.token} fra malen.
- DESIGN.md l. 291 og 299 forkorter tokennavn (…-mobile). Skriv hele navnene.
- components.corner-row.logout viser til en komponent, ikke et token.
- testmode-toggle.size: '44px x 24px' er ikke en CSS-verdi. Del opp i width og height.
- typography.logo.fontFamily mangler reserveskrift.
- Mockup-stier peker på filer som ennå ligger i .working/. Sjekk stiene etter flyttingen.

## Rapportene fra hjelperne

- `review-rubric.md` (A sjekkliste)
- `review-tilgjengelighet.md` (B tilgjengelighet)
- `review-sensor.md` (C sensor-blikk)
