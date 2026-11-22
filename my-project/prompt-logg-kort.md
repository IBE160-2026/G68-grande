# Kort prompt-logg: de viktigste valgene

Dette er en kort utgave av [prompt-loggen](prompt-logg.md) for sensor. Den samler de viktigste valgene jeg tok og de viktigste feilene i det KI-en laget, for hele prosjektet. Den lange loggen er beholdt, med over 500 rader og promptene slik jeg skrev dem. Tall i parentes er rader i den lange loggen, og PR-numrene viser til pull requestene på GitHub.

Verktøy: Claude Code med BMAD, gjennom hele prosjektet. Claude Opus 5.5 er også KI-en i selve nettsiden.

## Slik jobbet jeg med KI-en

- **Jeg tok de store valgene, KI-en rutinevalgene.** I begynnelsen ville jeg se alt KI-en gjorde. Fra slutten av oktober tok KI-en rutinevalg og fortalte hva den hadde valgt, mens jeg sjekket ordlyden, det brukeren ser, og de store valgene.
- **Én branch og én PR per story.** Hver PR sier hva KI-en gjorde feil. Jeg prøvde hver side i nettleseren før jeg flettet.
- **Logg i hver økt.** Sesjonslogg i `.logs/kristine/`, åpne punkter i `issues.md`, og en TO DO-liste i [`todo.md`](todo.md).

**Hva jeg lærte om å styre KI-en:**
- Det lønner seg å sjekke at KI-en ikke endrer mer enn jeg har bedt om, og å spørre når jeg ikke forstår et forslag i stedet for å godta det (product brief).
- Jeg er veldig nøye og vil se alt KI-en gjør. Det gir kontroll, men tar mye tid. For å bli ferdig i tide måtte jeg stole mer på KI-en i det som er lett å rette, og bruke tiden på det som er viktig (PRD).
- Grønne tester viser bare at koden følger planen. Flere feil ble bare funnet fordi jeg prøvde selv i nettleseren, eller fordi en egen gjennomgang leste koden (koding).

## Product brief (september–oktober)

**Mine valg**
- Etter faglærers tilbakemelding gjorde jeg versjon 1 mindre: bare norsk, enkel innlogging, og nettsiden lager bare søknadsbrev. CV og annonse kan legges inn som PDF eller tekst, og brevet lastes ned som Word og PDF.
- Udokumentert statistikk ble fjernet.
- Jeg beholdt både nøkkelordtreff og gap-analyse, fordi nøkkelordtreffet kan testes.
- Eget punkt for tone og språk i brevet.

**KI-feil:** KI-en forkortet teksten min om hvem nettsiden er for, og visjonen, uten å spørre. Originalteksten ble satt tilbake.

## PRD (oktober)

**Mine valg**
- En enkel telleregel for nøkkelordtreff (FR-17). En regel for ordstammer ble satt på kuttlisten.
- Korrektur av brukerens eget brev som eget valg tidlig i flyten (FR-20), og CV-en er alltid med.
- Testmodus på startsiden (FR-32), og samtykke med avkrysning før ekte KI brukes (FR-36).
- KI-en i nettsiden skal ikke anta ting på vegne av brukeren. Det ble et eget krav (FR-37) og suksesskriterium 11.

**KI-feil:** KI-en kalte nettsiden en «app» flere ganger. Et risikotiltak sa at vi skulle «fjerne fra kuttlisten», men kuttlisten er det som allerede er kuttet.

## UX (oktober)

Hele oversikten står i [Mine valg og KI-feil (UX)](3-ux/mine-valg-og-ki-feil.md). De viktigste:
- Fargetemaet «Myk fersken», og «Dette kan du jobbe videre med» i stedet for «Mangler».
- Fyrverkeri når brevet er ferdig, men bygget sist og kuttet først hvis tiden blir knapp.
- Endringene i Korrektur markeres per setning, ikke per ord, fordi det er mindre rotete.
- Skisser av alle sidene på PC og mobil. Det var slik jeg fant at KI-en hadde glemt «Logg ut», tilbakeknappen og registreringssiden.
- KI-en mente at «i»-boksen i en skisse ikke virket. Jeg testet den selv, og den virket.

## Konkurranseanalyse (27. oktober, sjekket på nytt 22. november)

Jobscan, Rezi, Teal og Kickresume har alle KI-skrevne brev og nøkkelordsjekk. Ingen av dem har en telleregel brukeren kan regne etter, KI-korrektur av eget brev med markerte endringer, eller norsk. Det stemte fortsatt 22. november. Se [konkurrentanalysen](4-konkurrentanalyse/konkurrentanalyse.md).

## Arkitektur (november)

Hele oversikten står i [Mine valg og KI-feil (arkitektur)](5-arkitektur/mine-valg-og-ki-feil.md). De viktigste:
- Det enkleste som gir et godt resultat. Jeg hadde aldri kodet før, så det ble Python og Flask, ett språk for hele nettsiden.
- Claude Opus 5.5 og et tak på 250 kr, med forhåndskjøpt kreditt uten automatisk påfylling.
- Ingen publisering på nett. Jeg spurte faglærer, og nettsiden kjøres lokalt etter README.
- Koden ligger i `backend/`, fordi lærerens CI bare kjører testene der.

**KI-feil:** avrundingen ville gjort 12,5 % til 12 %, men fasiten sier 13 %. KI-en tok for gitt at Python var installert på PC-en min. Den overså også lærerens CI-fil, så testene ville blitt hoppet over uten at noen merket det.

## Epics og stories (7. november)

Hele oversikten står i [Mine valg og KI-feil (epics og stories)](6-epics-og-stories/mine-valg-og-ki-feil.md). De viktigste:
- Åtte epics i fast rekkefølge. Det som aldri kuttes, kommer først, og det som kuttes først, bygges sist.
- «Tilbake» fra resultatsiden er en del av kjerneflyten, og det kom et testcase til.

**KI-feil:** KI-en sa at jeg hadde godkjent et steg, fordi det sto i en fil. Det hadde jeg ikke. Den første sluttsjekken var for overfladisk, og den grundige sjekken fant åtte feil.

## Kodingen (8.–22. november)

**Mine valg**
- **Grensen på 10 KI-kall gjelder bare med ekte KI**, fordi den er der for kostnaden (story 4.3.2, PR #26, 381–385).
- **Personen først i brevet.** Med ekte KI handlet brevet bare om erfaring. Jeg bestemte at et avsnitt om studenten som person skal komme først (story 4.3.1, 370–373).
- **Samtykketeksten.** KI-en ville skrive at Anthropic kan lagre teksten i opptil 30 dager. Jeg holdt fast ved at teksten skal si at nettsiden ikke lagrer noe, og at den nevner Claude fra Anthropic (story 4.3.1, 376–379).
- **Brudd på kriterium 11.** Med ekte KI skrev to brev ting som ikke står i CV-en. Jeg bestemte at det var brudd, og prompten fikk en ny regel (story 4.5, PR #28).
- **Hva er en omformulering i Korrektur?** Regelen min er at ingenting som ikke står i CV-en, brevet eller annonsen, skal dras inn (story 5.2.2, 440–442).
- **Lavere grense for brevfeltet i Korrektur (5 000 tegn).** Et brev på nesten 15 000 tegn tok 190 s og kostet ca. 7 kr. Jeg valgte 5 000 tegn, og 22. november målte vi det med ekte KI: 68,6 s og ca. 3 kr (retro 5, [testplanen](testplan.md)).
- **Skriptene prøves for hånd, ikke med automatiske tester.** Det som bare skjer i nettleseren, for eksempel «Lim inn tekst», vinduene og fyrverkeriet, har ingen automatiske tester. Jeg valgte å prøve alt dette selv i nettleseren. Testplanen har en tabell over hvor hvert skript er prøvd, og det står som kjent begrensning i README (story 8.2.1, PR #53).
- **Ingen «Tilbake» på brevsiden.** Valget er fra UX-arbeidet. Går man tilbake og endrer noe, kan brevet slettes uten spørsmål, så en knapp ville gjort det lettere å miste brevet. «Nytt forslag» gir et annet brev. Grunnen står i `EXPERIENCE.md`.
- **README så enkel som mulig for sensor**, med et eget steg for å hente koden (`git clone` eller ZIP) (story 8.2.1, 503).
- **Kriterium 13 bestått med en merknad.** Testpersonen forsto hva 50 % ikke betyr først da jeg spurte på nytt. Vi skrev det ærlig i stedet for å runde det opp (story 8.2.2, PR #54, 504).
- **«Lag ny søknad» når alle KI-kallene er brukt**, men ikke på brevsiden, fordi brevet da ville blitt borte (PR #55, 505).

**De viktigste KI-feilene** (funnet av meg i nettleseren eller av en egen gjennomgang, ikke av testene)
- **Tilbakeknappen etter utlogging** viste fortsatt «Velkommen», selv om alle testene var grønne. KI-en gjettet feil to ganger før et lite skript løste det. Funnet da jeg prøvde selv (story 1.4).
- **Prosentlinjen** var ca. 120 px høy i stedet for 12 px, med alle 388 testene grønne. Funnet da jeg så på siden (story 2.6).
- **Fokusringen** manglet første gang et vindu ble åpnet. Det var den samme feilen som i 2.5.1, og KI-en brukte ikke løsningen som alt lå i koden. Funnet da jeg prøvde selv (story 3.3).
- **CV-en kunne sendes til Claude uten samtykke**, hvis en annen fane slo av testmodus midt i analysen (story 4.3.1, PR #25).
- **Filer over 500 KB ble lagret på disken**, selv om nettsiden lover at ingenting lagres (story 6.1).
- **Tester som ikke kunne feile.** KI-en skrev flere ganger tester som var grønne uten å sjekke regelen, og gjorde i story 7.1 fem tester svakere for å få sin egen endring til å passe.
- **Teksten om sikkerhet lovet for mye** om hva `SameSite=Lax` stopper (story 8.1).
- **KI-ens egne sjekker kunne si «bestått» uten å sjekke noe** (story 8.2.1, PR #53).
