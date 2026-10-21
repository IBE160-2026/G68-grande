---
name: Søknadsassistenten
status: draft
created: 2026-10-20
updated: 2026-10-21
sources:
  - ../../prds/prd-kode-prosjekt-2026-10-09/prd.md
  - ../../prds/prd-kode-prosjekt-2026-10-09/addendum.md
---

# Søknadsassistenten — EXPERIENCE

> Hvordan nettsiden oppfører seg. Hvordan den ser ut, står i `DESIGN.md`. Krav står i PRD-en og nevnes bare med nummer (for eksempel FR-14). **Ved konflikt mellom skisse og dette dokumentet gjelder dokumentet.**

## Foundation

- **Form:** én responsiv nettside som brukes på PC og på mobil (375 px). Det er en nettside, ikke en app. Ordet «app» brukes ikke i tekst eller dokumenter.
- **Ingen ferdig UI-pakke** er valgt. Komponentene lages selv etter `DESIGN.md`.
- **Visuell referanse:** `DESIGN.md`. Tokens nevnes med `{path.to.token}`.
- **Lys modus** bare. Mørk modus står på TO DO som «hvis tid».
- **Innsats:** skoleprosjekt som vurderes av sensor, ikke ekte brukere.
- **Stemning:** enkel, effektiv, levende.

## Information Architecture

| Side | Kommer fra | Hva den gjør | Krav |
|---|---|---|---|
| Innlogging | Åpne nettsiden · Logg ut · «Logg inn» på registreringen · prøve en side uten å være logget inn | Logge inn | FR-3, FR-4, FR-7 |
| Registrering | «Ny her? Registrer deg her» | Lage bruker, logges inn automatisk | FR-1, FR-2, FR-4 |
| Startside | Etter innlogging/registrering · «Tilbake» på modusvalget · «Lag ny søknad» i vinduet etter nedlasting | Velkomst, testmodus-bryter, samtykke, «Begynn å lage søknad» | FR-5, FR-32, FR-36 |
| Modusvalg | «Begynn å lage søknad» · «Tilbake» på innleggingen | Velge Full generering eller Korrektur | FR-20 |
| Innlegging (Full generering) | Modusvalg · «Tilbake» på resultatsiden | Felt for CV og stillingsannonse | FR-8–FR-13, FR-34 |
| Innlegging (Korrektur) | Som over | Felt for CV, eget søknadsbrev og stillingsannonse | FR-8–FR-13, FR-34 |
| Resultatside | «Sjekk CV-en min» | Gap-analyse, nøkkelordtreff, forklaringer, ATS | FR-14–FR-19, FR-21 |
| Brevside (Full generering) | «Lag søknadsbrevet mitt» | «Din ferdigstilte søknad!», brevet, nedlasting, nytt forslag | FR-22, FR-25–FR-30 |
| Brevside (Korrektur) | «Oppdater søknadsbrevet mitt» | «Din oppdaterte søknad er ferdig!», brevet med markerte setninger | FR-23, FR-25–FR-30 |
| Vindu etter nedlasting | «Last ned som Word/PDF» | Ny søknad, logg ut eller bli her | FR-31 |
| Vindu «Nytt forslag» | «Nytt forslag» | Bekrefte at brevet slettes | FR-25 |

**Faste elementer på alle sider etter innlogging:**

| Hvor | Hva | Når | Krav |
|---|---|---|---|
| Oppe til høyre | Testmodus-bryter | Bare på startsiden | FR-32 |
| Oppe til høyre | Merkelapp «Testmodus» (uten bryter) | Andre sider, bare når testmodus er på | FR-33 |
| Nede til venstre | «ⓘ Teksten behandles av ekstern KI» | Bare når testmodus er av | FR-35 |
| Nede til høyre | «Logg ut» | Alltid etter innlogging | FR-6 |

KI-merknaden og «Logg ut» står i en rad som er **festet til bunnen av skjermen**, så de synes hele tiden, også når man ruller (FR-35). Siden får like mye luft nederst som raden er høy, slik at raden aldri dekker innhold, heller ikke på mobil (375 px). Skissene viser raden nederst på siden, men det er dette dokumentet som gjelder.

**Logoen** «Søknadsassistenten» står øverst og sentrert på alle sider.

**Navigasjon:**

- Innlogging ⇄ registrering med lenkene under skjemaene.
- Startside → modusvalg → innlegging → resultatside → brevside er hovedveien (FR-5 → FR-20 → FR-8 → FR-14 → FR-22).
- «Tilbake» finnes på tre sider, alltid som hvit sekundærknapp:
  - **Modusvalg → startsiden.** Under kortene. Grunn: blant annet hvis sensor går videre uten å slå på testmodus, som bare kan slås på på startsiden.
  - **Innlegging → modusvalget.** Ved siden av «Sjekk CV-en min». Retter opp feil valg av modus. Dette er et tillegg i UX, ikke i strid med PRD-en. CV og annonse beholdes hvis de er fylt ut. Feltet for eget brev finnes bare i Korrektur.
  - **Resultatside → innleggingen.** Nederst ved siden av «Lag søknadsbrevet mitt» / «Oppdater søknadsbrevet mitt». Feltene er fortsatt fylt ut (FR-19).
- Brevsiden har ingen «Tilbake». Derfra går man videre med vinduet etter nedlasting, eller med «Logg ut».
- «Logg ut» fører til innloggingssiden.
- Hva nettleserens egen tilbakeknapp gjør midt i en søknad, bestemmes i arkitekturen, ikke i UX.

## Skisser

Alle sider har skisse på PC og mobil. Skissene viser oppsett og oppførsel. Ved konflikt gjelder dette dokumentet.

| Skisse | Viser |
|---|---|
| `mockups/login-register-1.html` | Innlogging og registrering, alle feilmeldinger, «Du må logge inn først» |
| `mockups/start-page-1.html` | Startsiden, samtykke med «i»-boks, testmodus av/på, uten API-nøkkel |
| `mockups/mode-select-1.html` | Modusvalget. **Variant A er valgt.** B og C er forkastet |
| `mockups/input-page-1.html` | Innleggingen i begge modusene, feilboks, testdata-hjelpetekst, ventetegn, KI-feil |
| `mockups/result-page-1.html` | Resultatsiden. **Nøkkelord variant B (to lister) er valgt.** A er forkastet |
| `mockups/letter-page-1.html` | Brevsiden i begge modusene, fyrverkeri, markeringer, nedlasting, vinduene, KI-feil |
| `mockups/download-options-1.html` | Tidlig forslag. Variant A ble valgt, med grønn hake fra B. Erstattet av brevsiden |
| `mockups/korrektur-markings-1.html` | Tidlig forslag. Per setning ble valgt, per ord er forkastet. Erstattet av brevsiden |
| `mockups/color-themes-1.html`, `mockups/color-themes-2.html`, `mockups/logo-fonts-1.html` | Valg av farger og logoskrift (se `DESIGN.md`) |

## Voice and Tone

Vennlig, personlig og enkel tekst. Korte setninger. Siden snakker til brukeren som «du». Teksten skal gjøre en usikker student trygg, for eksempel «Dette kan du jobbe videre med» i stedet for «mangler».

| Gjør | Ikke gjør |
|---|---|
| «Dette kan du jobbe videre med» | «Mangler» på skjermen (navnet «mangler» brukes fortsatt i PRD og tester, FR-14) |
| «Vi lager brevet ditt – det tar noen sekunder.» | «Laster …» |
| Si hvilket felt feilen gjelder og hva man kan gjøre | «Ugyldig input» |
| «Det du har lagt inn, er ikke borte.» | La brukeren lure på om alt er borte |
| «nettside» | «app» |

### Tekster per side

**Innlogging** (FR-3, FR-4, FR-7)

- Overskrift: «Logg inn». Felt: «E-post», «Passord». Knapp: «Logg inn».
- Under skjemaet: «Ny her? Registrer deg her» (lenke på «Registrer deg her»).
- Tomme felt: «Fyll inn e-post», «Fyll inn passord».
- Feil innlogging: «Feil e-post eller passord» (rød boks over skjemaet).
- Ikke logget inn: «Du må logge inn først» (rød boks over skjemaet).

**Registrering** (FR-1, FR-2, FR-4)

- Overskrift: «Registrer deg». Felt: «E-post», «Passord», «Gjenta passord». Knapp: «Registrer deg».
- Under passordfeltet fra starten: «Minst 8 tegn».
- Under skjemaet: «Har du allerede en bruker? Logg inn».
- Tomme felt: «Fyll inn e-post», «Fyll inn passord», «Gjenta passordet».
- For kort passord: «Passordet må ha minst 8 tegn» (fra skissen).
- E-posten finnes: «Denne e-posten er allerede registrert» (fra skissen).
- Er passordene ikke like, vises «Passordene er ikke like» ved «Gjenta passord», med rød ramme som i FR-4.

**Startside** (FR-5, FR-32, FR-36)

- «Velkommen! 👋» på én linje.
- Ingress: «Her lager du et søknadsbrev som passer til stillingen du vil søke på.» (én linje på PC, flere linjer på mobil).
- Linje over avkrysningsboksen: «Teksten din sendes til ekstern KI.»
- Avkrysningsboks: «Jeg samtykker til bruk av KI», med «i»-ikon ved siden av.
- «i»-boksen (fra skissen):
  - «**Hva samtykker jeg til?** Teksten du legger inn, altså CV, brev og stillingsannonse, sendes til en ekstern KI-tjeneste.»
  - «**Hvorfor sendes teksten?** KI-tjenesten trenger teksten for å finne kravene i annonsen og skrive brevet.»
  - «**Lagres noe?** Nei. Ingenting du legger inn, lagres etter at du logger ut.»
  - «**Personopplysninger:** Vi anbefaler at du fjerner adresse, telefonnummer og fødselsdato fra CV-en først. Det er ditt valg.»
- Uten samtykke: «Du må samtykke før du kan begynne».
- Knapp: «Begynn å lage søknad».
- Testmodus på: «Du er i testmodus. Nettsiden bruker ferdige svar, og ingenting sendes til ekstern KI.»
- Uten API-nøkkel: «Mangler API-nøkkel, se README».

**Modusvalg** (FR-20)

- Overskriften er «Hva vil du gjøre i dag?».
- Kort 1: ✨ «Full generering» · «Skriv nytt brev» · «Du legger inn CV-en og annonsen, så skriver vi et brev til deg.»
- Kort 2: ✏️ «Korrektur» · «Forbedre mitt brev» · «Du har skrevet et brev selv. Vi forbedrer språket og beholder innholdet ditt.»
- Knapp under kortene: «Tilbake».

**Innlegging** (FR-8–FR-13, FR-34)

- Overskrift Full generering: «Legg inn CV-en din og stillingsannonsen».
- Overskrift Korrektur: «Legg inn CV-en din, brevet ditt og stillingsannonsen».
- Felt: «📄 CV» (CV-en din) · «✉️ Ditt søknadsbrev» (Brevet du har skrevet selv, bare Korrektur) · «📢 Stillingsannonse» (Annonsen for jobben du søker på).
- Knapper i hvert felt: «Last opp PDF», «Lim inn tekst». Over tekstboksen: «Lim inn teksten her».
- Knapper nederst: «Tilbake», «Sjekk CV-en min».
- Bare i testmodus: «Testmodus: bruk filene i mappen testdata/ i prosjektet.»
- Feilboks, overskrift: «Noe må fikses før du kan gå videre:». Én linje per feil, med feltnavnet først (fra skissen):

| Feil | Tekst | Krav |
|---|---|---|
| Tomt felt | «CV: Fyll inn feltet. Last opp en PDF eller lim inn tekst.» | FR-9 |
| Feil filtype | «CV: Feil filtype, prøv PDF.» | FR-10 |
| Uleselig PDF | «CV: Vi klarer ikke å lese teksten i PDF-en. Den kan være skannet. Lim inn teksten i stedet.» | FR-11 |
| For stor fil | «CV: Filen er for stor. Den kan være på høyst X MB.» (tallet bestemmes i arkitekturen) | FR-12 |
| Ikke testdata i testmodus | «CV: I testmodus fungerer bare testdataene fra mappen testdata/.» | FR-34 |

Feltnavnet byttes ut: «CV», «Ditt søknadsbrev», «Stillingsannonse».

**Resultatside** (FR-14–FR-18, FR-21)

- Overskrift: «Slik passer CV-en din til stillingen».
- «Gap-analyse» med «i» og merket «Laget av KI». Undertekst: «Kravene fra annonsen, sammenlignet med CV-en din.»
- Lister: «Dette dekker CV-en din» og «Dette kan du jobbe videre med».
- «Nøkkelordtreff» med «i». Tallet: «X av Y = Z %», med «av nøkkelordene står i CV-en din».
- Lister: «Står i CV-en (antall)» og «Står ikke i CV-en (antall)».
- «i» ved gap-analyse (fra skissen): «En KI-vurdering av hvilke krav i annonsen CV-en dekker, og hvilke du kan jobbe videre med.»
- «i» ved nøkkelordtreff (fra skissen): «En ordtelling av hvor mange av annonsens nøkkelord som står i CV-en. Det er bare en pekepinn på hvordan et ATS kan vurdere CV-en, ikke en garanti.»
- ATS-forklaring (foldes ut): «Hva er ATS og hva betyr den for deg?» Tekst fra skissen: «Mange arbeidsgivere sender søknadene gjennom et ATS før et menneske leser dem. Et ATS er et dataprogram som blant annet ser etter ord fra annonsen.» og «Står flere av nøkkelordene i CV-en din, er det større sjanse for at den blir lest. Men prosenten over er bare en pekepinn, ikke en garanti.»
- Mellom gap-analysen og nøkkelordtreffet står en kort linje (FR-18): «Gap-analysen og nøkkelordtreffet kan si litt forskjellig. Gap-analysen er en vurdering KI-en gjør, mens nøkkelordtreffet bare teller ord.»
- Knapper: «Tilbake» og «Lag søknadsbrevet mitt» (Full generering) / «Oppdater søknadsbrevet mitt» (Korrektur).

**Brevside** (FR-22–FR-31)

- Overskrift Full generering: «Din ferdigstilte søknad!». Korrektur: «Din oppdaterte søknad er ferdig!».
- Bare Korrektur, over brevet: «Grønn og understreket = endret. Trykk på setningen for å se det du skrev.» Under en åpnet setning: «Du skrev» og den gamle setningen.
- Knapper: «Last ned som Word», «Last ned som PDF». Etter nedlasting: «✓ Lastet ned som Word» / «✓ Lastet ned som PDF».
- Under knappene etter nedlasting: «Filnavn: Soknad_Sykehuset_2026-10-21.docx».
- Under: «Nytt forslag».
- Vindu etter nedlasting: «Brevet er lastet ned!» · «Vil du lage en ny søknad eller logge ut?» · «Lag ny søknad», «Logg ut», «Bli her».
- Vindu ved nytt forslag: «Vil du ha et nytt forslag?» · «Brevet du ser nå, blir slettet. Har du ikke lastet det ned, er det borte.» · «Ja, lag nytt forslag», «Avbryt».

**Ventetegn** (FR-27)

- Overskrift i begge tilfeller: «På vei mot ny jobb».
- Etter «Sjekk CV-en min»: «Vi sjekker CV-en din – det tar noen sekunder.»
- Når brevet lages, og ved nytt forslag: «Vi lager brevet ditt – det tar noen sekunder.»

**KI-feil** (FR-28)

- Nettverksfeil: «Nettverksfeil, sjekk nettverkstilgangen.»
- Andre feil: «Noe gikk galt hos KI-tjenesten. Prøv på nytt.»
- Når KI-en svarer, men svaret ikke kan brukes (FR-28), vises «Noe gikk galt hos KI-tjenesten. Prøv på nytt.».
- Tekst under, per side: innlegging «Det du har lagt inn, er ikke borte.» · resultatside «Resultatet og det du har lagt inn, er ikke borte.» · brevside «Brevet du hadde, er beholdt.»
- Knapp: «Prøv igjen».

### Filnavn ved nedlasting (FR-29)

- Mønster: `Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>.docx` eller `.pdf`, for eksempel «Soknad_Sykehuset_2026-10-20.docx». Arbeidsgiveren står med, slik at søknadene er lette å skille.
- Ingen æ, ø eller å i filnavnet.
- Arbeidsgivernavnet hentes fra annonsen (hvordan avgjøres i arkitekturen). Finnes det ikke, brukes «Soknad_<dato>». Æ, ø og å byttes til ae, o og a, og mellomrom blir bindestrek.

## Component Patterns

Atferd. Utseende står i `DESIGN.md` under Components.

| Komponent | Brukes på | Regler |
|---|---|---|
| Hovedknapp / sekundærknapp | Alle sider | «Tilbake» er alltid sekundær og står til venstre for hovedknappen. Knappen som starter et KI-kall, låses mens man venter (FR-27). |
| «Begynn å lage søknad» | Startside | Den største knappen på siden. Krever samtykke når testmodus er av (FR-36). |
| Modus-kort | Modusvalg | Hele kortet er én knapp. Ett trykk går rett til innleggingen for den modusen. Ingen «Velg»-knapp i tillegg. |
| Innleggingsfelt | Innlegging | Tom tilstand: «Last opp PDF» og «Lim inn tekst». «Last opp PDF» åpner filvelgeren. Etter opplasting vises filnavnet med ✓. «Lim inn tekst» åpner en tekstboks i feltet, og markøren settes i den. |
| Søppelbøtte | Innleggingsfelt | Tømmer feltet med en gang, uten bekreftelse (FR-13). Feltet går tilbake til tom tilstand. Skjermlesertekst: «Tøm CV-feltet», «Tøm brevfeltet», «Tøm annonsefeltet». |
| Testmodus-bryter | Startside | Slår testmodus av og på (FR-32). Finnes bare på startsiden. Uten API-nøkkel er den låst på. |
| Merkelapp «Testmodus» | Alle andre sider | Bare visning, kan ikke trykkes på (FR-33). |
| Samtykke | Startside | Ikke krysset av når man kommer til startsiden etter innlogging (FR-36). Skjules i testmodus. |
| «i»-ikon | Startside, resultatside | Åpner en kort forklaring. Se Interaction Primitives. |
| ATS-forklaring | Resultatside | Overskrift som foldes ut og inn når man trykker. Lukket når siden åpnes. Ikke en «i». |
| Prosentlinje | Resultatside | Fylles når siden åpnes. Bare pynt, tallet står alltid som tekst (FR-17). |
| Nøkkelordlister | Resultatside | Kan ikke endres (FR-16). |
| Endret setning | Brevside (Korrektur) | Er en knapp. Trykk eller Enter åpner «Du skrev» med den gamle setningen rett under. Nytt trykk lukker. Flere kan være åpne samtidig. Brevet kan ikke redigeres (FR-26). |
| Nedlastingsknapper | Brevside | Laster ned filen, blir grønne med «✓ Lastet ned som …», viser filnavnet under, og åpner vinduet etter nedlasting. Vinduet kommer hver gang. Filen har ingen markeringer (FR-30). |
| «Nytt forslag» | Brevside | Åpner bekreftelsesvinduet. «Ja, lag nytt forslag» → ventetegn → nytt brev med nytt fyrverkeri. Nedlastingsknappene og filnavnet nullstilles. I Korrektur lages det nye forslaget fra det opprinnelige brevet (FR-25). |
| Vindu etter nedlasting | Brevside | «Lag ny søknad» → startsiden med tomme felt (FR-31). «Logg ut» → logger ut. «Bli her» lukker vinduet, slik at man kan laste ned det andre formatet. |
| Vindu «Nytt forslag» | Brevside | «Ja, lag nytt forslag» starter. «Avbryt» og Esc lukker. |
| Ventetegn | Innlegging, resultatside, brevside | Dekker siden mens KI-en jobber. Skissene har ingen avbryt-knapp. Teksten avhenger av hva som skjer (se Voice and Tone). |
| Feilboks | Innlegging, resultatside, brevside | Øverst på siden. Samler alle feilene. Se State Patterns. |
| Logg ut | Alle sider etter innlogging | Logger ut med en gang. Alt fra økten glemmes (NFR-4). |

## State Patterns

| Tilstand | Side | Hva skjer |
|---|---|---|
| Tomt skjema sendt | Innlogging, registrering | Hvert tomt felt får rød ramme og en kort tekst under (FR-4). Fokus flyttes til det første feltet med feil. |
| Feil e-post eller passord | Innlogging | Rød boks over skjemaet: «Feil e-post eller passord» (FR-3). |
| Ikke logget inn | Innlogging | Kommer man til en annen side uten å være logget inn, sendes man hit med «Du må logge inn først» i rød boks over skjemaet (FR-7). |
| E-post finnes | Registrering | Rød ramme og tekst ved e-postfeltet (FR-2). |
| Passord for kort / ikke like | Registrering | Rød ramme og tekst ved feltet. «Minst 8 tegn» står under passordfeltet hele tiden. |
| Registrert | Registrering | Logges inn automatisk og kommer til startsiden (FR-1). |
| Vanlig modus | Startside | Samtykke synlig og ikke krysset av. KI-merknad nede til venstre. |
| Uten samtykke | Startside | «Begynn å lage søknad» uten avkryssing → rød ramme rundt boksen og «Du må samtykke før du kan begynne». Fokus flyttes til avkrysningsboksen. |
| Testmodus på | Startside | Samtykket og KI-merknaden skjules. Teksten om testmodus vises. «Begynn å lage søknad» virker uten samtykke (FR-36). |
| Uten API-nøkkel | Startside | Bryteren er slått på og låst. «Mangler API-nøkkel, se README» står under bryteren (FR-32). |
| Testmodus på | Alle andre sider | Merkelappen «Testmodus» oppe til høyre. KI-merknaden er skjult (FR-33, FR-35). |
| Testmodus på | Innlegging | Hjelpeteksten om `testdata/` vises over feltene. |
| Tomme felt | Innlegging | Hvert felt viser «Last opp PDF» og «Lim inn tekst». |
| Fylt felt | Innlegging | Filnavn med ✓ og søppelbøtte, eller tekstboks med søppelbøtte. |
| Feil i det man har lagt inn | Innlegging | Feilboks øverst med alle feilene. Felt med feil får rød ramme. Siden ruller opp til boksen, fokus flyttes dit, og skjermlesere leser den opp. Feilboksen forsvinner når man prøver igjen uten feil. |
| Venter på KI | Innlegging, resultatside, brevside | Ventetegnet dekker siden. Knappen er låst, så det ikke sendes flere forespørsler (FR-27). |
| KI-feil | Innlegging, resultatside, brevside | Rød boks øverst på siden man sto på, med feiltekst, en tekst om at ingenting er borte, og «Prøv igjen». Siden ruller opp til boksen, og fokus flyttes dit. Det man har lagt inn, er der fortsatt (FR-28). Feiler «Nytt forslag», beholdes det gamle brevet. |
| Resultat | Resultatside | Gap-analysen først, så nøkkelordtreffet, så ATS-forklaringen (lukket). |
| Tom liste | Resultatside | Tom «Dette dekker CV-en din»: «CV-en din dekker ingen av kravene ennå. Se hva du kan jobbe videre med.» · Tom «Dette kan du jobbe videre med»: «Bra jobbet! CV-en din dekker alle kravene i annonsen. 🎉» · Tom «Står i CV-en (0)»: «Ingen av nøkkelordene står i CV-en ennå.» · Tom «Står ikke i CV-en (0)»: «Alle nøkkelordene står i CV-en din!» Er begge listene tomme, gjelder FR-28. |
| Brevet vises | Brevside | Fyrverkeri rundt overskriften når siden åpnes. |
| Nedlastet | Brevside | Knappen er grønn med ✓, filnavnet står under, vinduet åpnes. |
| Nytt forslag laget | Brevside | Nytt brev, nytt fyrverkeri, nedlastingsknappene er nullstilt. |

**Samtykket** må krysses av på nytt hver gang man kommer til startsiden, også i samme økt (via «Tilbake» på modusvalget eller «Lag ny søknad»). Avkrysningsboksen er alltid tom når startsiden åpnes.

**Logg ut før nedlasting:** trykker man «Logg ut» på brevsiden før brevet er lastet ned i noe format, åpnes et vindu: «Du har ikke lastet ned brevet. Vil du logge ut likevel? Brevet blir slettet.» med [Logg ut] og [Avbryt]. Esc og Avbryt lukker vinduet. Er brevet lastet ned, logges man ut med en gang (NFR-4).

## Interaction Primitives

- **Trykk og klikk** er hovedmåten å gjøre ting på. Ingen hurtigtaster er bestemt.
- **«i»-boksen** åpnes ved hover på PC, ved trykk på mobil og ved tastaturfokus. Nytt trykk lukker. Esc lukker. Den lukkes når fokus går videre. Slik virker den med mus, på mobil og med tastatur (NFR-6, NFR-7).
- **ATS-forklaringen** foldes ut og inn ved trykk, eller med Enter/mellomrom med tastatur.
- **Endret setning** åpnes og lukkes ved trykk, eller med Enter med tastatur.
- **Vinduer:** Fokus flyttes inn i vinduet når det åpnes, til det trygge valget («Bli her» eller «Avbryt»). Esc lukker begge vinduene. Når vinduet lukkes, går fokus tilbake til knappen som åpnet det.
- **Søppelbøtta** tømmer med en gang, uten bekreftelse.
- **«Nytt forslag»** krever bekreftelse, fordi brevet slettes.
- **Ingen ekstra bekreftelse** før brevet lages. Trykket på «Lag søknadsbrevet mitt» / «Oppdater søknadsbrevet mitt» er bekreftelsen (FR-21).
- **Hover** gir små animasjoner på knapper og kort på PC. På mobil er det ingen hover; alt virker med trykk.
- **Filvelgeren** og «Lim inn tekst» skal virke godt på mobil (FR-8).
- **Brukes ikke:** redigering av brevet på nettsiden (FR-26).

## Accessibility Floor

Atferd. Kontrast og farger står i `DESIGN.md`.

- **Bare tastatur:** alt kan brukes med Tab, Enter, mellomrom og Esc (NFR-6). Rekkefølgen følger lesingen. Alt man kan trykke på, har synlig fokusring (`{colors.focus-ring}`).
- **Etiketter:** alle felt har synlige etiketter (NFR-6). Hjelpetekst og feiltekst er koblet til feltet, slik at skjermlesere leser dem opp.
- **Ikoner:** ikoner som bare er pynt (📄 ✉️ 📢 ✨ ✏️ 👋, prikkene, fyrverkeriet), skjules for skjermlesere. Knapper med bare ikon har en tekst for skjermlesere: søppelbøtta («Tøm CV-feltet» osv.) og «i»-ikonene («Hva betyr samtykket?», «Hva er en gap-analyse?», «Hva er nøkkelordtreff?»).
- **Feil:** feilboksen og KI-feilboksen leses opp av skjermlesere, og fokus flyttes til boksen. På innloggingen flyttes fokus til det første feltet med feil. Felt med feil merkes som ugyldige for skjermlesere.
- **Farge er aldri det eneste tegnet:** feil har tekst og rød ramme (FR-4). Endringer i Korrektur er understreket i tillegg til grønne (FR-23). Nøkkelord har ✓ eller ○. Gap-listene har overskrifter. Nedlastet-knappen har ✓ og tekst.
- **Ventetegn:** skjermlesere får beskjed om ventetegnet og teksten.
- **Filnavn etter nedlasting** leses opp av skjermlesere.
- **Redusert bevegelse:** ved `prefers-reduced-motion` slås alle animasjoner av. Fyrverkeriet hoppes over, prosentlinjen vises ferdig, og siden hopper til feilboksen uten myk rulling.
- **Blinking:** fyrverkeriet blinker ikke mer enn tre ganger i sekundet og dekker ikke brevet.
- **Bredde:** alle sider kan brukes uten å rulle sidelengs ved 375, 768 og 1280 px (NFR-7).

## Responsive & Platform

| | PC | Mobil (375 px) |
|---|---|---|
| Logo | Stor, én linje | Mindre, fortsatt én linje |
| Startside-ingress | Én linje | Flere linjer, så skriften ikke blir for liten |
| «Begynn å lage søknad» | Ekstra stor (ca. 1,5 × vanlig skrift) | Hele bredden |
| Modus-kort | Side om side | Under hverandre |
| Innleggingsfelt | Side om side (2 eller 3) | Under hverandre |
| Tekstboks | Ca. 160 px høy | Ca. 200 px høy, stor nok til et helt brev |
| Gap-analyse | «Dekker» til venstre, «jobbe videre med» til høyre | «Dekker» øverst |
| Nøkkelordlister | Side om side | Under hverandre |
| Brevoverskrift | Større | Mindre |
| «i»-boks | Hover, trykk eller fokus | Trykk eller fokus |
| Filvelger | Vanlig filvelger | Telefonens filvelger, må virke godt |

Bruddpunktet er 700 px: under 700 px står alt under hverandre, og fra 700 px står ting side om side, også på nettbrett (768 px, NFR-7).

## Inspiration & Anti-patterns

- **Tre ord:** enkel, effektiv, levende.
- **«Levende»** er en blanding av farger, små animasjoner, små ikoner og vennlig tekst.
- **Anti-mønster:** en statisk og kjedelig nettside.
- **Bevisst vanlig:** innloggingen og registreringen ser ut slik innloggingssider stort sett gjør. Det levende spares til resten.
- **Forkastet:** markering per ord i Korrektur (for rotete), merkelapper for nøkkelord (mindre oversiktlig enn to lister), modusvalg med bare knapper eller med fil-liste, nedlasting med melding på siden eller med valgene alltid under brevet.

## Testmodus

- Slås av og på bare på startsiden (FR-32). På andre sider står bare merkelappen «Testmodus» (FR-33).
- I testmodus: ingen samtykke, ingen KI-merknad, ferdige svar, bare testdata virker (FR-34, FR-35, FR-36).
- Sensor laster opp filene fra `testdata/` selv (NFR-3, NFR-8). Innleggingen viser en liten hjelpetekst om mappen. Det finnes ingen knapp som fyller inn testdata, fordi det ville vært en ny funksjon.
- Feilmeldingene for tomme felt, feil filtype og uleselig PDF virker også i testmodus (FR-34).

## Key Flows

Stegene er slik Kristine bekreftet dem 2026-10-21.

### Reise 1 — Ingrid, Full generering på PC

Ingrid er 21 år og studerer sykepleie. Hun søker deltidsjobb ved siden av studiet. Hun har aldri søkt jobb før og er usikker. Hun bruker PC hjemme.

1. **Innlogging:** Ingrid åpner siden. Øverst står «Søknadsassistenten» som logo. Under innloggingsskjemaet står «Ny her? Registrer deg her».
2. **Registrering:** Hun lager en bruker og blir logget inn automatisk (FR-1).
3. **Startsiden og samtykket:** Hun blir usikker fordi CV-en sendes til ekstern KI. Hun åpner «i»-ikonet og leser at ingenting lagres etter utlogging, hvorfor teksten sendes, og at hun selv kan velge å fjerne personopplysninger fra CV-en. Hun blir trygg, krysser av for samtykket og trykker «Begynn å lage søknad».
4. **Modusvalg:** Hun velger «Full generering – Skriv nytt brev».
5. **Innlegging:** Hun laster opp CV-en som PDF og limer inn annonseteksten. Søppelbøtta kan tømme et felt. Hun trykker «Sjekk CV-en min».
6. **Venting:** Hoppende prikker, «På vei mot ny jobb» og «Vi sjekker CV-en din – det tar noen sekunder.»
7. **Resultatsiden:** Først «Dette dekker CV-en din», og ved siden av «Dette kan du jobbe videre med». Ingrid skjønner at hun faktisk er kvalifisert. Under står nøkkelordene og den utfoldbare «Hva er ATS og hva betyr den for deg?». Hun trykker «Lag søknadsbrevet mitt».
8. **Høydepunkt – brevet:** «Din ferdigstilte søknad!» med fyrverkeri i 2–3 sekunder. Under brevet står «Last ned som Word», «Last ned som PDF» og «Nytt forslag».
9. **Nedlasting:** Hun trykker «Last ned som Word». Knappen blir grønn med hake, og vinduet «Brevet er lastet ned!» åpnes. Hun trykker «Bli her» og laster ned PDF-en også. Den knappen blir også grønn, og vinduet kommer igjen. Da velger hun «Logg ut».

Feilvei: KI-en svarer ikke i steg 6 eller 8 → rød boks med «Prøv igjen», og det hun har lagt inn, er der fortsatt (FR-28).

### Reise 2 — Eirik, Korrektur på mobil

Eirik er 22 år og studerer finans. Han bruker telefonen. Han har søkt jobber før og har allerede skrevet et søknadsbrev. Han vil bare forbedre brevet, ikke få et nytt, fordi han har jobbet mye med det selv.

1. **Innlogging:** Eirik har en bruker fra før og logger inn.
2. **Startsiden:** Han krysser av for samtykket og trykker «Begynn å lage søknad».
3. **Modusvalg:** Han velger «Korrektur – Forbedre mitt brev».
4. **Innlegging:** Han laster opp CV-en, sitt eget brev og annonsen som PDF fra telefonen. «Lim inn tekst» virker også (FR-8).
5. **Venting:** De hoppende prikkene.
6. **Resultatsiden:** «Dette dekker CV-en din» øverst og «Dette kan du jobbe videre med» under. Så nøkkelordene og ATS-forklaringen. Nederst står «Tilbake» og «Oppdater søknadsbrevet mitt». Han trykker «Oppdater søknadsbrevet mitt».
7. **Høydepunkt – det oppdaterte brevet:** «Din oppdaterte søknad er ferdig!» med fyrverkeri. Endrede setninger er markert med grønt. Eirik trykker på noen av dem og ser hva han skrev før. Han ser at brevet er ferdig, men fortsatt hans eget.
8. **Nedlasting:** Han laster ned, knappen blir grønn med hake, og vinduet kommer med ny søknad, logg ut og «Bli her». Filen har ingen markeringer (FR-30).

Feilvei: vil han ha et annet forslag, trykker han «Nytt forslag» og bekrefter. Feiler det, beholdes det gamle brevet (FR-28).

### Reise 3 — Henrik, sensor i testmodus

Henrik er sensor i faget. Han har 10–15 minutter og har trolig sett slike prosjekter før. Han vil sjekke at begge modusene og feilmeldingene fungerer.

1. **Oppstart:** Henrik følger README og starter nettsiden. Han har ingen API-nøkkel, så siden starter i testmodus og viser «Mangler API-nøkkel, se README».
2. **Innlogging:** Han logger inn med testbrukeren fra README.
3. **Startsiden:** Testmodus-bryteren er slått på og låst. Samtykket er skjult. Han trykker «Begynn å lage søknad».
4. **Modusvalg:** Han velger «Full generering».
5. **Innlegging og feilmeldinger:** Han ser hjelpeteksten om `testdata/`. Først prøver han feilene med vilje: den skannede PDF-en, filen av feil type og en egen tekst («bare testdata fungerer i testmodus», FR-34). Feilboksen øverst sier hvilket felt det gjelder. Så laster han opp de riktige testfilene og trykker «Sjekk CV-en min».
6. **Resultatsiden:** Han trykker «Lag søknadsbrevet mitt».
7. **Brevet:** Fyrverkeri. Han laster ned og velger «Lag ny søknad» i vinduet.
8. **Korrektur:** Han går gjennom med testbrevet og trykker på noen grønne setninger.
9. **Logg ut.**

**Høydepunkt:** Nettsiden er i gang på 10–15 minutter (NFR-8), og så kommer Henrik gjennom begge modusene og feilmeldingene uten å stå fast.

Feilvei: går han videre fra startsiden uten testmodus (når API-nøkkel finnes), kan han trykke «Tilbake» på modusvalget for å komme til bryteren.
