# Tilgjengelighetsgjennomgang — Søknadsassistenten

> Gjennomgang av `DESIGN.md`, `EXPERIENCE.md`, `.memlog.md` og skissene i `.working/` mot WCAG 2.1/2.2 nivå AA og NFR-6/NFR-7 i PRD-en. Dato: 2026-10-22.
> Skissene er ikke oppdatert etter runde 2 (for eksempel rammefarge #A23E6C på skrivefelt og grått spor på bryteren). Det er ikke regnet som funn. Dokumentene (spinene) vinner over skissene.
> Funnene gjelder teksten i spinene. Der en skisse viser et problem som spinen ikke løser, er skissen nevnt som eksempel.

## Samlet vurdering

Grunnmuren er god. Alle fargeparene i tokenene består AA, farge er aldri det eneste tegnet, feilmeldingene sier hvilket felt det gjelder og hva man kan gjøre, og redusert bevegelse er tenkt på overalt. De største hullene gjelder **fokus og skjermleser i det som «dukker opp»**: den faste raden nederst kan dekke det som har fokus, vinduene og ventetegnet sperrer ikke resten av siden, og innholdet i «i»-boksen (der hele samtykkeforklaringen ligger) når ikke sikkert fram til skjermlesere. I tillegg sjekker spinen bare 375 px, mens WCAG krever at siden virker ved 320 px og ved 200 % tekststørrelse, og reglene om «alltid én linje» kan bryte med det. Ingen funn er kritiske. Alt kan rettes med noen setninger i spinene.

## Kontrasttabell

Regnet ut med WCAG-formelen (relativ luminans). Krav i AA: vanlig tekst 4,5:1, stor tekst (minst 24 px, eller 18,7 px fet) 3:1, rammer og deler av knapper/felt (UI) 3:1. Låste (deaktiverte) knapper og ren pynt har ikke krav.

| Forgrunn | Bakgrunn | Brukes til | Forhold | Krav | Resultat |
|---|---|---|---|---|---|
| text #3A2530 | background #FFF7F5 | Vanlig tekst på siden | 13,36 | 4,5 | Består |
| text #3A2530 | surface #FFFFFF | Tekst i kort, felt, brev | 14,12 | 4,5 | Består |
| text-muted #6E5560 | background #FFF7F5 | Ingress, KI-merknaden (0,78rem), gammel setning | 6,35 | 4,5 | Består |
| text-muted #6E5560 | surface #FFFFFF | Hjelpetekst, «Minst 8 tegn», forklaring i modus-kort | 6,71 | 4,5 | Består |
| primary #A23E6C | surface #FFFFFF | Sekundærknapp-tekst, lenker, «i», tallet «7 av 10» | 6,10 | 4,5 | Består |
| primary #A23E6C | background #FFF7F5 | Logo, lenkeknapper («Nytt forslag»), ATS-overskrift | 5,77 | 4,5 | Består |
| primary-contrast #FFFFFF | primary #A23E6C | Tekst på hovedknapper | 6,10 | 4,5 | Består |
| text #3A2530 | accent #F6B8A0 | «Testmodus», «Laget av KI» | 8,26 | 4,5 | Består |
| #FFFFFF | text #3A2530 | Tekst i «i»-boksen | 14,12 | 4,5 | Består |
| error #B4232F | error-tint #FBE6E8 | Feilboks, skjemafeil | 5,46 | 4,5 | Består |
| error #B4232F | surface #FFFFFF | Feiltekst under felt | 6,52 | 4,5 | Består |
| error #B4232F | background #FFF7F5 | Feiltekst på siden | 6,17 | 4,5 | Består |
| success #2F7A57 | success-tint #E4F3EB | Filnavn, «✓ Lastet ned som …», «Dette dekker …» | 4,53 | 4,5 | Består (knapt) |
| success #2F7A57 | surface #FFFFFF | ✓ i nøkkelordlista | 5,20 | 4,5 | Består |
| text #3A2530 | success-tint #E4F3EB | Endret setning i brevet | 12,32 | 4,5 | Består |
| text #3A2530 | changed-active #CFEBDC | Endret setning, åpen/hover | 11,14 | 4,5 | Består |
| success #2F7A57 | changed-active #CFEBDC | Understreking på åpen setning (UI) | 4,10 | 3 | Består |
| work-on #8A3A20 | work-on-tint #FDEEE8 | «Dette kan du jobbe videre med» | 6,86 | 4,5 | Består |
| text-muted #6E5560 | wait-slør (≈ #F3EAE9) | Ventetekst (verste tilfelle, mørk tekst bak sløret) | 5,67 | 4,5 | Består |
| primary #A23E6C | wait-slør (≈ #F3EAE9) | «På vei mot ny jobb» | 5,16 | 3 (stor) | Består |
| primary #A23E6C | surface #FFFFFF | Ramme på skrivefelt/tekstboks/avkrysning (UI) | 6,10 | 3 | Består |
| error #B4232F | surface #FFFFFF | Rød ramme ved feil (UI) | 6,52 | 3 | Består |
| focus-ring #3B5BDB | background #FFF7F5 | Fokusring (2 px luft, så ringen ligger mot bakgrunnen) | 5,36 | 3 | Består |
| focus-ring #3B5BDB | surface #FFFFFF | Fokusring inne i kort og brev | 5,67 | 3 | Består |
| focus-ring #3B5BDB | success-tint #E4F3EB | Fokus på søppelbøtta i filnavn-stripa | 4,94 | 3 | Består |
| focus-ring #3B5BDB | error-tint #FBE6E8 | Fokus på «Prøv igjen» inne i feilboksen | 4,75 | 3 | Består |
| focus-ring #3B5BDB | primary #A23E6C | Ring rett inntil en hovedknapp (uten luft) | 1,08 | 3 | **Stryker** – derfor *må* de 2 px luften alltid være med |
| text-muted #6E5560 (spor av) | background #FFF7F5 | Bryter av (UI) | 6,35 | 3 | Består |
| #FFFFFF (knott) | text-muted #6E5560 | Knotten på bryter av (UI) | 6,71 | 3 | Består |
| #FFFFFF (knott) | primary #A23E6C | Knotten på bryter på (UI) | 6,10 | 3 | Består |
| bryter låst, 60 % (≈ #A899A0) | surface #FFFFFF | Låst bryter | 2,72 | – | Unntatt (låst), se S-15 |
| hovedknapp låst, 55 % (≈ #CC91AA) | background | Låst knapp mens man venter | 2,42 (hvit tekst 2,56) | – | Unntatt (låst) |
| primary #A23E6C | border #EED7DD | Prosentlinjen, fyll mot spor | 4,47 | – | Pynt (tallet står som tekst) |
| border #EED7DD | surface #FFFFFF | Rammer på kort og innleggingsfelt | 1,36 | – | Pynt (godkjent, se under) |
| accent #F6B8A0 | background #FFF7F5 | Merkelapp-flate, 3. prikk | 1,62 | – | Pynt |
| dot-middle #C0618C / fireworks-gold #F2C14E | background | Prikk 2, fyrverkeri | 3,73 / 1,59 | – | Pynt |
| Plassholdertekst | – | – | – | 4,5 | Finnes ikke i spinen. Bra. Brukes den senere, må den ha `text-muted` (6,7), ikke nettleserens grå. |

Merk: rammen #EED7DD på modus-kort og innleggingsfelt er greit, fordi teksten inne i kortet viser at det er en knapp/et felt, og rød ramme ved feil har 6,5:1. Selve skrivefeltene har bringebær-ramme.

## Funn

### Kritisk

Ingen.

### Høy

- **[S-1] Den faste raden nederst kan dekke det som har fokus, og den har ingen bakgrunn** (EXPERIENCE.md § Information Architecture, «Faste elementer»; DESIGN.md § Components, Hjørnerad). WCAG 2.4.11 Fokus ikke skjult (2.2 AA), 1.4.10 Reflow, 1.4.3 Kontrast. Spinen sier at siden får «like mye luft nederst som raden er høy». Det hjelper bare helt nederst på siden. Når man tabber nedover midt på siden, ruller nettleseren akkurat så langt at knappen kommer inn i bildet, og da havner den ofte *bak* den faste raden. Rammen sier heller ikke hvilken bakgrunn raden har. Er den gjennomsiktig, ruller tekst under KI-merknaden, og da gjelder ikke kontrastene i tabellen. På mobil i liggende format, eller ved 200 % zoom, tar raden også mye av skjermen. *Forslag (legg til i «Faste elementer»):* «Raden har heltrukket bakgrunn `{colors.background}` og en tynn strek `{colors.border}` øverst. Siden har `scroll-padding-bottom` lik radens høyde, slik at et element med fokus aldri havner bak raden. Er skjermen lavere enn ca. 500 px (liggende mobil eller stor zoom), står raden ikke fast, men nederst på siden.»

- **[S-2] Vinduene sperrer ikke resten av siden** (EXPERIENCE.md § Interaction Primitives, «Vinduer»; § State Patterns, «Logg ut før nedlasting»). WCAG 2.4.3 Fokusrekkefølge, 1.3.1, 4.1.2. Spinen sier hvor fokus går inn og ut, og at Esc lukker. Men den sier ikke at Tab skal holde seg *inne* i vinduet. Uten det kan man tabbe ut til knappene bak sløret (også «Logg ut» i den faste raden), og skjermlesere kan lese siden bak. Spinen sier også «Esc lukker begge vinduene», men nå finnes det **tre** vinduer (etter nedlasting, «Nytt forslag», «Logg ut før nedlasting»), og det står ikke hvilken knapp som får fokus i det tredje. *Forslag:* «Vinduer: Når et vindu er åpent, kan man ikke nå resten av siden med Tab, mus eller skjermleser (bruk `<dialog>` med `showModal()`, eller `inert` på resten). Vinduet har `aria-labelledby` til overskriften og `aria-describedby` til teksten. Fokus går til det trygge valget: «Bli her», «Avbryt» eller «Avbryt» (logg ut-vinduet). Esc lukker alle tre vinduene.»

- **[S-3] Ventetegnet: fokus forsvinner, siden bak kan brukes, og opplesningen er usikker** (EXPERIENCE.md § Component Patterns, «Ventetegn»; § Accessibility Floor, «Ventetegn»). WCAG 2.4.3, 4.1.3 Statusbeskjeder. Når knappen låses (FR-27), mister den fokus, og fokus havner på «ingenting» (i skissene `disabled`). Ventetegnet dekker siden bare visuelt; man kan fortsatt tabbe til knappene bak. Skissene legger `role="status"` på et element som er skjult og så vises. Det leses ofte *ikke* opp, fordi skjermleseren må kjenne til området før teksten kommer. Spinen sier heller ikke hvor fokus går når ventingen er over (ny side, nytt brev eller KI-feil). *Forslag:* «Ventetegn: Resten av siden, også den faste raden, er `inert` mens man venter. Knappen låses med `aria-disabled="true"` og beholder fokus. Et statusområde (`role="status"`) finnes på siden hele tiden, og ventesetningen skrives inn i det når ventingen starter. Når ventingen er over, går fokus til overskriften på den nye siden (eller det nye brevet), eller til feilboksen ved KI-feil.»

- **[S-4] «i»-boksen: skjermlesere får ikke sikkert høre innholdet, og trykk og fokus kolliderer** (EXPERIENCE.md § Interaction Primitives, «i»-boksen; DESIGN.md § Components, `info-tip`). WCAG 1.3.1, 4.1.2, 1.4.13 Innhold ved hover eller fokus. Hele samtykkeforklaringen (FR-36) står bare her, så dette er viktig. Tre problemer: (1) Boksen er ikke koblet til knappen, så skjermlesere leser bare «Hva betyr samtykket?, knapp, utvidet», ikke teksten. Fire avsnitt med fet overskrift passer heller ikke i en `tooltip`. (2) «Åpnes ved tastaturfokus» + «nytt trykk lukker»: et klikk med mus gir først fokus (åpner) og så klikk (lukker), så boksen blinker bare. Det skjer i skissene. (3) Når boksen åpnes ved hover, må Esc lukke den uten at man flytter musa, og man må kunne flytte musa inn i boksen uten at den forsvinner. *Forslag:* ««i»-boksen er en utfoldbar forklaring: knappen har `aria-expanded` og `aria-controls`, og teksten står rett etter knappen i lesrekkefølgen. Den åpnes ved trykk/klikk og ved hover på PC. Den åpnes *ikke* av fokus alene (Enter/mellomrom åpner). Esc lukker den uansett hvor fokus eller mus er. Den holder seg åpen mens musa er over knappen eller boksen.»

- **[S-5] 320 px, 200 % tekst og «alltid én linje»** (DESIGN.md § Typography og § Layout & Spacing; EXPERIENCE.md § Responsive & Platform og § Accessibility Floor, «Bredde»). WCAG 1.4.10 Reflow, 1.4.4 Endre tekststørrelse, 1.4.12 Tekstavstand. Spinen sjekker 375, 768 og 1280 px (NFR-7). WCAG krever i tillegg at siden virker ved **320 px** uten sidelengs rulling, og ved 200 % tekststørrelse. Reglene «hele logoen på én linje» og «ingressen på én linje på PC» blir ofte laget med `white-space: nowrap` (slik skissene gjør), og da renner teksten ut av skjermen når brukeren gjør skriften større. Det samme gjelder merkelapper og filnavn med fast høyde. *Forslag:* (a) Legg til i § Accessibility Floor: «Bredde: siden virker også ved 320 px og ved 200 % zoom/tekststørrelse uten sidelengs rulling (WCAG 1.4.10).» (b) I § Typography: «Logoen og ingressen skal stå på én linje *ved vanlig tekststørrelse*. Blir skriften større enn det er plass til, får de bryte linjen. Ingen `nowrap` på tekst som kan bli lengre enn skjermen.» (c) «Ingen faste høyder på knapper, merkelapper eller bokser med tekst.»

### Middels

- **[S-6] Sidetittel og fokus når man går til ny side** (EXPERIENCE.md § Information Architecture; § Accessibility Floor). WCAG 2.4.2 Sidetitler, 2.4.3, 4.1.3. Spinen sier ikke hva som står i nettleserfanen (`<title>`) på hver side. Hvis sidene byttes uten at hele siden lastes på nytt (avgjøres i arkitekturen), merker en skjermleserbruker ikke at siden er byttet. *Forslag:* «Hver side har sin egen tittel, for eksempel «Logg inn – Søknadsassistenten», «Resultat – Søknadsassistenten». Byttes siden uten ny lasting, flyttes fokus til sidens hovedoverskrift.»

- **[S-7] Overskriftsnivåer og landemerker er ikke bestemt** (DESIGN.md § Typography; EXPERIENCE.md § Accessibility Floor). WCAG 1.3.1, 2.4.6, 2.4.1. Typografi-tabellen sier hvor store overskriftene er, men ikke hvilket nivå de har. I skissene er logoen et vanlig avsnitt og sideoverskriften `h2`, så siden mangler `h1`. «i»-knappen og «Laget av KI» står inne i overskriften, så skjermlesere leser overskriften som «Gap-analyse Hva er en gap-analyse? Laget av KI». *Forslag:* «Sideoverskriften er `h1` (for eksempel «Slik passer CV-en din til stillingen»). Boksoverskrifter («Gap-analyse», «Nøkkelordtreff», feltnavnene) er `h2`, og listeoverskriftene er `h3`. Logoen er ikke en overskrift. «i»-knappen og merket står ved siden av overskriften, ikke inne i den. Siden har landemerkene `header` (logo, testmodus), `main` og `footer` (den faste raden).»

- **[S-8] Like navn på knapper og tekstbokser i innleggingsfeltene** (EXPERIENCE.md § Component Patterns, «Innleggingsfelt»; § Voice and Tone, Innlegging). WCAG 2.4.6, 1.3.1, 4.1.2. Hvert felt har «Last opp PDF» og «Lim inn tekst», og hver tekstboks heter «Lim inn teksten her». I en liste over knapper hører en skjermleserbruker tre like «Last opp PDF». Søppelbøtta har allerede gode navn («Tøm CV-feltet»). *Forslag:* «Knappene og tekstboksen har feltnavnet med for skjermlesere: «Last opp PDF, CV», «Lim inn tekst, Stillingsannonse», tekstboksen «CV: Lim inn teksten her». Det synlige navnet er det samme som før. Filvelgeren viser bare PDF (`accept=".pdf"`), så færre velger feil fil (3.3.3).»

- **[S-9] Fokus etter søppelbøtte og opplasting** (EXPERIENCE.md § Component Patterns, «Søppelbøtte» og «Innleggingsfelt»). WCAG 2.4.3, 4.1.3. Etter «Lim inn tekst» settes markøren i tekstboksen. Bra. Men når søppelbøtta tømmer feltet, forsvinner knappen som hadde fokus, og fokus havner øverst på siden (slik i skissene). Etter opplasting sies det ikke hvor fokus går, eller om filnavnet leses opp. *Forslag:* «Etter tømming går fokus til «Last opp PDF» i samme felt, og skjermlesere hører «CV-feltet er tømt». Etter opplasting går fokus til søppelbøtta ved filnavnet, og skjermlesere hører «CV lastet opp: <filnavn>».»

- **[S-10] Endrede setninger er bare forklart med farge og strek** (EXPERIENCE.md § Component Patterns, «Endret setning»; § Voice and Tone, Brevside). WCAG 1.3.1, 1.3.3 Sensoriske egenskaper. Forklaringen «Grønn og understreket = endret» kan ikke brukes av den som ikke ser fargen eller streken. En skjermleser leser bare setningen som en knapp, uten å si at den er endret. *Forslag:* «Hver endret setning har en skjult tekst for skjermlesere: «Endret setning» (for eksempel med `aria-describedby`). Forklaringen over brevet får en skjult tilleggstekst: «Endrede setninger er knapper.» Knappen har `aria-expanded` og åpnes med Enter *og* mellomrom.»

- **[S-11] Feilboksen og feltene er ikke koblet sammen** (EXPERIENCE.md § State Patterns, «Feil i det man har lagt inn»; § Accessibility Floor, «Feil»). WCAG 3.3.1 Identifikasjon av feil, 1.3.1. Feilboksen sier hvilket felt det gjelder. Bra. Men innleggingsfeltet har ingen egen feiltekst, bare rød ramme, og «merkes som ugyldige for skjermlesere» går ikke når feltet bare har to knapper og ingen skrivefelt. Brukeren må selv finne feltet igjen. *Forslag:* «Hver linje i feilboksen er en lenke som flytter fokus til feltet den gjelder. Feltet med feil viser også feilteksten under feltnavnet (den samme teksten), koblet med `aria-describedby` til knappene og tekstboksen. Tekstboksen får `aria-invalid="true"`.»

### Lav

- **[S-12] Språket er satt til «no», ikke «nb»** (EXPERIENCE.md § Foundation; skissene bruker `lang="no"`). WCAG 3.1.1 Sidens språk. «no» er gyldig, men «nb» gir riktigere uttale i flere skjermlesere. *Forslag:* legg til i § Foundation: «Alle sider har `<html lang="nb">`.»

- **[S-13] Noen emojier og tegn mangler i lista over pynt** (EXPERIENCE.md § Accessibility Floor, «Ikoner»; § State Patterns, «Tom liste»). WCAG 1.1.1. Lista nevner 📄 ✉️ 📢 ✨ ✏️ 👋, men ikke **🎉** («Bra jobbet! … 🎉», leses som «festkjegle»), **ⓘ** i KI-merknaden (leses som «sirklet bokstav i», og ser ut som en knapp uten å være det), **→** og **○** i listene, og **✓** i «✓ Lastet ned som Word». *Forslag:* «Disse er også pynt og skjules for skjermlesere: 🎉, ⓘ, →, ✓ og ○. Listeoverskriftene og knappeteksten forteller det samme.»

- **[S-14] Feil tall og utdatert tekst om kontrast i DESIGN.md** (DESIGN.md § Colors). WCAG 1.4.11 (bare dokumentasjon). (1) «ramme i `{colors.primary}` (6,6:1 mot hvit)» er feil. Riktig er **6,1:1** (samme par som hvit tekst på primary, som står riktig). (2) «Lys rosa … er sporet i prosentlinjen *og bryteren*» stemmer ikke lenger; bryteren har `text-muted` når den er av (runde 2). (3) success på success-tint er 4,53:1, altså akkurat over kravet. *Forslag:* rett 6,6 til 6,1, stryk «og bryteren», og legg til: «success på success-tint har ingen margin; ikke gjør den grønne teksten lysere eller bakgrunnen mørkere.» Legg også til: «Fokusringen har alltid 2 px luft. Uten luft er kontrasten mot en bringebær knapp bare 1,1:1.»

- **[S-15] Den låste bryteren forsvinner for tastatur og skjermleser** (EXPERIENCE.md § Component Patterns, «Testmodus-bryter»; § State Patterns, «Uten API-nøkkel»). WCAG 4.1.2, 4.1.3. En vanlig låst (`disabled`) bryter kan ikke nås med Tab, så sensor med skjermleser hører verken «Testmodus, på» eller «Mangler API-nøkkel, se README». Når testmodus slås på, forsvinner samtykket uten at det sies fra. *Forslag:* «Bryteren er en `role="switch"` med synlig etikett «Testmodus». Låst: `aria-disabled="true"` (kan fortsatt nås med Tab), og «Mangler API-nøkkel, se README» er koblet til med `aria-describedby`. Teksten «Du er i testmodus …» står i et statusområde, slik at den leses opp når den kommer.»

- **[S-16] Innlogging: autofyll, liming og noen meldinger mangler** (EXPERIENCE.md § Voice and Tone, Innlogging/Registrering; § State Patterns). WCAG 1.3.5 Identifiser formål, 3.3.8 Tilgjengelig autentisering (2.2 AA), 3.3.1/3.3.3. Skissene har riktig `autocomplete`, men spinen sier det ikke, og da kan det bli borte i koden. Spinen sier ikke hvor fokus går ved «Feil e-post eller passord», og «Du må logge inn først» vises når siden lastes, da blir `role="alert"` ofte ikke lest opp. Det finnes ingen melding for e-post med feil form (for eksempel «ola@»). *Forslag:* «E-post har `autocomplete="email"`, passord `current-password` (innlogging) og `new-password` (registrering). Liming og passordbehandlere er alltid lov. Ved «Feil e-post eller passord» og «Du må logge inn først» går fokus til den røde boksen. Feil form på e-post: «Skriv e-posten slik: navn@eksempel.no».»

- **[S-17] Dobbel opplesning og filnavn som drukner** (EXPERIENCE.md § Accessibility Floor, «Feil» og «Filnavn etter nedlasting»). WCAG 4.1.3. Feilboksen skal både «leses opp» (`role="alert"`) og få fokus. Da leser mange skjermlesere den to ganger. Filnavnet leses opp samtidig som vinduet åpnes og fokus flyttes dit, så filnavnet blir ofte avbrutt. *Forslag:* «Feilboksen får fokus (`tabindex="-1"`), men ikke `role="alert"`. Vinduet etter nedlasting viser også filnavnet: «Brevet er lastet ned som Soknad_Sykehuset_2026-10-21.docx.»»

- **[S-18] Ingenting om tidsavbrudd i økten** (EXPERIENCE.md § Component Patterns, «Logg ut»; PRD Ordliste «Økt»). WCAG 2.2.1 Justerbar tid. PRD-en sier at økten varer til man logger ut. Legger arkitekturen inn automatisk utlogging (vanlig i innloggingsbiblioteker), mister brukeren det hen har lagt inn uten varsel. Det rammer særlig de som skriver sakte eller bruker skjermleser. Det er heller ikke sagt hva som skjer hvis KI-en aldri svarer. *Forslag:* «Nettsiden logger ikke ut av seg selv. Gjør arkitekturen det likevel, varsles brukeren minst 20 sekunder før, og kan velge «Fortsett». Svarer ikke KI-en innen en fast tid (bestemmes i arkitekturen), vises KI-feilen «Noe gikk galt hos KI-tjenesten. Prøv på nytt.»»

## Det som allerede er bra (kort)

- Alle tekst- og UI-par i tokenene består AA (se tabellen), og rammen på skrivefelt ble rettet til 6,1:1 i runde 2.
- Farge er aldri det eneste tegnet: feil har tekst og ramme, endringer er understreket, nøkkelord har ✓/○, gap-listene har overskrifter, nedlastet-knappen har ✓ og tekst.
- Feilmeldingene sier hvilket felt og hva man kan gjøre (3.3.1, 3.3.3), og «Det du har lagt inn, er ikke borte» gjør feil mindre skremmende.
- «Begynn å lage søknad» er ikke låst uten samtykke, men gir en tydelig feil og flytter fokus til avkrysningsboksen. Det er bedre enn en grå knapp.
- Redusert bevegelse slår av *alt*, også myk rulling. Fyrverkeriet er kort (ca. 2,5 s), blinker høyst tre ganger i sekundet og ligger bak teksten (2.3.1, 2.2.2).
- Synlig fokusring i egen blå farge, med 2 px luft, på alt man kan trykke på (2.4.7).
- Søppelbøtta og «i»-ikonene har skjermlesertekster, og pynteikonene skjules.
- Trykkflatene er store nok: «i» er 24 × 24 px (akkurat kravet i 2.5.8), bryteren 44 × 24 px med klikkbar etikett, søppelbøtta og «Logg ut» er større.
- Vinduene setter fokus på det trygge valget og sender fokus tilbake til knappen som åpnet dem.
- Ingen plassholdertekst brukes som etikett. Alle felt har synlige etiketter, og «Minst 8 tegn» står fra starten.
