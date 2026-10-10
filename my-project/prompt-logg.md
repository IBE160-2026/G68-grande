# Prompt-logg

De viktigste forespørslene jeg har gitt KI-en (Claude Code) i prosjektet, og hva de førte til. Prompts er gjengitt slik jeg skrev dem. Nye økter legges til nederst.

Promptene fra den første økten med product brief (16. september 2026) er ikke med, fordi jeg ikke visste da at de skulle logges. Avgjørelsene fra den økten står i [beslutningsloggen for første utkast](1-product-brief/forste-utkast-memlog.md).

## 2026-10-07/08 – Revisjon av product brief etter faglærers tilbakemelding

Verktøy: Claude Code med BMAD-skillen `bmad-product-brief` (oppdatering). Alle beslutninger er logget i `brief-memlog.md`.

| # | Min prompt | Resultat |
|---|---|---|
| 1 | «hei, jeg har fått en tilbakmelding på productbriefen min, kan du hente ut denne fra GitHUb» | Hentet `tilbakemelding-product-brief.md` fra GitHub og oppsummerte den |
| 2 | «ser du hvilke problemer vi må endre på og løse før vi går videre på oppgaven. Ser jo nå at dette er et krevene prosjekt kun for meg og deg, så vi må gjøre det mer spesifikt og versjon 1 må ha mindre applikajsoner» | Liste over problemer og forslag til hva som kunne kuttes i versjon 1 |
| 3 | «vi tar kun norsk for å gjøre det enkelt, videre så vil jeg ha en enkel innloging […] versjon 1 lager kun søknad. Enig at vi må ha både PDF og tekst inn, og ut vil jeg ha word, samt PDF […]» | Beslutninger om språk, innlogging, input og output |
| 4 | «[…] var ikke klar over at disse tallene sto der […] Det fjerner vi også får det foreløpig stå litt mer generelt om statestikken. Foretrekker B på innlogging» | Udokumentert statistikk fjernet; registrering med e-post/passord valgt |
| 5 | «Ser nå at vi har 10 kriterier for versjon 1 som er enda mer enn det vi hadde og læreren sa det var for mye» | KI-en forklarte forskjellen og foreslo flere kutt; jeg valgte de endelige punktene selv |
| 6 | «jeg forstår ikke helt dette for å være ærlig, hvorfor har vi med nøkkelordtreff i utgangspunktet» / «men må jeg ha med gap analyse da?» | Forklaring og alternativer; jeg valgte å beholde begge, fordi nøkkelordtreff er testbart |
| 7 | «1) tror vi gjør det enklest mulig i versjon 1 […] 3) også vil jeg ha et eget punkt som tar for seg tone og språk» | Ingen lagring i versjon 1; eget punkt for tone og språk |
| 8 | «tror du kan gå over alle punktene å fjerne litt for ser ut som mye av det samme står både under løsning og under versjon 1» | Fjernet dobbeltbeskrivelser |
| 9 | «jeg legger også merke til at hvem dette er for og visjon blir stadig mindre» | KI-en hadde forkortet teksten min uten å spørre; originalteksten ble satt tilbake |
| 10 | «vent litt, jeg glemte jo å spørre om vi hadde gått over alle punktene som læreren hadde bedt oss om å se på» | Gjennomgang av tilbakemeldingen punkt for punkt; README, prompt-logg og begrunnelse for Word lagt til |

**Hva jeg lærte om å styre KI-en:** Det lønner seg å sjekke at KI-en ikke endrer mer enn jeg har bedt om, og å spørre når jeg ikke forstår et forslag i stedet for å godta det.

## 2026-10-09 – PRD (første utkast)

Verktøy: Claude Code med BMAD-skillen `bmad-prd` (veiledet vei, inngang: visjon + funksjoner). Alle beslutninger er logget i `prd-memlog.md`.

| # | Min prompt | Resultat |
|---|---|---|
| 1 | «Bruk Brief-en» | Visjonen ble hentet fra product brief, med min ordlyd |
| 2 | «dette er jo omtrent som produkt briefen, hva er forskjellen?» | Forklaring på forskjellen mellom brief og PRD; jeg valgte å beholde visjonen som den var |
| 3 | «en kjapp ting vi må få på plass, dette er en nettside ikke en app» | «appen» byttet til «nettsiden» i hele PRD-en |
| 4 | «i forhold til gruppe 3, kan du ta med dette i tankene når vi skal utforme denne delen?» (limte inn tilbakemelding om nøkkelordlisten) | Nøkkelordlisten lagres i økten og vises; KI-en pekte på at «rette nøkkelordlisten» var kuttet i briefen, og jeg valgte å beholde kuttet |
| 5 | «da velger i A) så får det være en del av neste versjon å ha med ordstamme-regel.» | Enkel telleregel i FR-17; ordstamme-regel satt på kuttlisten |
| 6 | «Nå begynte jeg å tenke litt, […] det stemmer jo at vi tillatter å legge inn brukerens egen søknad også. dette må oj komme som et alternativ tidligere i prosessen» | Modus velges tidlig (FR-20); jeg valgte at CV alltid er med, og «kun søknad» ble satt på kuttlisten |
| 7 | «spørsmål til gruppe 4, mener du det er bedre om de kan endre i nettleseren?» | Fordeler og ulemper; redigering i nettleseren satt på kuttlisten |
| 8 | «C) ingen topp eller bunnlinje i versjon 1, dette kommer senere» | Ingen topp- eller bunntekst i nedlastet fil (FR-30) |
| 9 | «jeg er ikke helt ferdig ennå ser jeg, vi må få inn at allerede på startsiden så i et hjørne så kan man switche til testmodus […]» | Bytte til testmodus på startsiden (FR-32) og samtykke til KI med avkrysningsboks (FR-36) |
| 10 | «Ja det er viktig, KI-en i nettleseren skal ikke komme med antagelser på vegne av brukeren» | Nytt krav FR-37 og suksesskriterium 11 |
| 11 | «du sier hvis tiden blir kanpp så fjerner vi fra kuttlisten. Men kuttlisten er jo en liste over ting vi allerede har kuttet?» | KI-en hadde formulert risikotiltaket feil; teksten ble rettet |
| 12 | «min forståelse er at det ikke vil havne i GitHub hvis den ligger i output?» | PRD-en kopiert til `my-project/prd.md`, slik at den committes underveis og sensor kan se historikken |

### 2026-10-09 – Opprydding i repoet (etter PRD-økten)

| # | Min prompt | Resultat |
|---|---|---|
| 13 | «vi kan endre app til nettside i briefen» | «appen» byttet til «nettsiden» i product brief, slik at brief og PRD bruker samme begrep |
| 14 | «hva er forskjell på en memlog og en prompt log, for finner inen memlogg for i dag» | Forklaring; beslutningsloggen for PRD-en lagt i repoet, og loggen for briefen fikk navnet `brief-memlog.md` |
| 15 | «er det sånn at jeg kan rydde mer opp i github repoet mitt? for eksempel samle alle memloggene en plass alle promtloggene en plass eller hva ser du som hensiktsmessig?» | KI-en foreslo mapper etter filtype |
| 16 | «ja det så veldig bra ut, men burde ikke første utkastet av briefen ligge sammen med den gjeldende?» | Jeg valgte i stedet én mappe per dokument (`1-product-brief/`, `2-prd/`) |
| 17 | «hva tenker du, bør sensorveiledningen være med så sensor ser jeg har brukt den gjennom oppgaven?» | Sensorveiledningen holdes utenfor repoet (lagt i `.gitignore`), fordi den er kursmateriell |
| 18 | «jeg fikk en mail fra github om at siste push feilet? står et rødt kryss ved sjekk prosjketet» | KI-en hadde flyttet briefen uten å oppdatere CI-sjekken; stien ble rettet og sjekken ble grønn igjen |
| 19 | «den research mappen ser jeg egt på som unødvendog» | Tom research-mappe fjernet |
| 20 | «kan de bli kaldt Productbrief og PRD uten tallene foran?» / «aha det var derfor du hadde tallene, ja vel da må nesten de tallene være der» | Mappene ble omdøpt, men endringen ble angret før push for å beholde rekkefølgen |
| 21 | «I dag har vi hatt det problemet at når vi jobber her så lagres alt i en mappe, bmadoutput er det vel på PC, men det vil aldri komme over på github, det er jo tungvindt, kan vi gjøre noe med det?» | `_bmad-output/` forblir lokal kladdebok; KI-en kopierer dokumenter og logger til `my-project/` underveis |
| 22 | «er det noe mer vi har produsert men som ikke har kommet med til github?» | `addendum.md` og loggen fra første brief-økt lagt i repoet |
| 23 | «jeg tenker A, men at det kan være greit å legge ved en forklaring på hvorfor jeg skrev som jeg skrev […]» | Merknad om bakgrunnen for formuleringen «egeninitiert idé» lagt øverst i loggen fra første utkast |
| 24 | «alt det som vi har gjort nå, er dette logget noe sted og lagt inn i github? sånn med tanke på oppryddingen?» | Denne delen av prompt-loggen |

### 2026-10-10 – Ferdigstilling av PRD, steg 1: gjennomgang av beslutningsloggen

| # | Min prompt | Resultat |
|---|---|---|
| 25 | «ja fortsett med steg 1» | KI-en sjekket hver linje i beslutningsloggen mot PRD-en og fant tre tekster som ikke stemte med flytendringen fra i går |
| 26 | «jeg må si jeg ikke henger med på noen av de» | KI-en forklarte flyten på nytt, enklere, og tok ett funn om gangen |
| 27 | «ja» / «ja» | FR-5 og første avsnitt i visjonen rettet, slik at valget mellom «Skriv nytt brev» og «Forbedre mitt brev» kommer først |
| 28 | «har du et annet ord for portal?» | KI-en foreslo «felt», «opplastingsfelt» og «boks» |
| 29 | «opplastingsfelt er bra, videre så vil jeg bytte jobbutlysningen med jobbannonsen og brukeren eget brev med brukerens eget søknadsbrev» | Addendumet bruker nå mine ord, og har med feltet for eget søknadsbrev |
| 30 | «vi kan bruke stillingsannonse» | Addendumet og PRD-en bruker samme ord |
| 31 | «push» / «to commits?» | Rettingene pushet; KI-en forklarte hvorfor det ble to commits |
| 32 | «burde jeg cleare det vinduet her og deretter ta opp arbeidet på nytt?» / «hvordan blir memlog og promt log lagret hvis jeg clearer» | Beslutningsloggen er en fil og overlever `/clear`, men prompt-loggen må skrives inn for hånd. Derfor ble denne delen skrevet før `/clear` |

### 2026-10-10 – Ferdigstilling av PRD, steg 2: kildesjekk

KI-en sendte fire hjelpere (underagenter) som hver sjekket én kilde mot PRD-en: product brief, faglærers tilbakemelding, sensorveiledningen og beslutningsloggen fra briefen. Funnene ble gått gjennom ett om gangen.

| # | Min prompt | Resultat |
|---|---|---|
| 33 | «begynn på steg 2» | Fire kilder sjekket mot PRD-en; 2 viktige funn, rundt 10 middels og noen små |
| 34 | «hva er det du egentlig lurer på under viktig 1 og 2» | KI-en forklarte de to viktigste funnene enklere, med eksempel |
| 35 | «ja på 1, til nummer to, hva anbefaler du?» | FR-37 sier nå at KI-en får omformulere det som står i CV-en, men ikke legge til noe nytt. KI-en anbefalte ekte KI-svar som testsvar og skjermbilder i README |
| 36 | «viktig å få med at KI ikke kan finne opp ting, håper det står skrevet.» | KI-en viste de tre stedene i PRD-en der det står |
| 37 | «viktig 2, vi gjør din anbefaling» | Ny FR-38: testmodus bruker ekte KI-svar, og README har skjermbilder |
| 38 | «ja, men kan vel være greit at det står i PRD at jeg har tenkt å bruke claude også, bare for å understreke det?» | Ny NFR-11 om Claude i PRD-en, og detaljene i addendumet |
| 39 | «ja, forslaget ditt var bra» | FR-24 sier nå at tonen skal være formell og akademisk og ikke høres ut som generisk KI-tekst |
| 40 | «[…] er det riktig at det står CV der? for ATS systemet er vel noe som arbeidsgiverne sender søknadene gjennom?» | KI-en forklarte at ATS leser hele søknaden, men at nøkkelordtreffet bare teller CV-en; ordlyden ble presisert |
| 41 | «jeg lurer fortsatt på noe angående forrige punkt. for er ATS, gap analyse og nøkkelordtreff tre forskjellige ting?» | KI-en forklarte forskjellen i en tabell. «ATS-delen» fjernet fra risiko 1, fordi nettsiden ikke har en egen ATS-del |
| 42 | «ja til første, punkt 28 må du spesifisere» | FR-28 lister nå fire tilfeller der et KI-svar ikke kan brukes |
| 43 | «jeg får ikke dette helt til å stemme» / «skal vi ha med på nettsiden en forklaring på de tre begrepene tenker du?» | FR-18 skrevet om: resultatsiden forklarer kort ATS, nøkkelordtreff og gap-analyse |
| 44 | «ja ta det med» | Kriterium 1, 3 og 11 testes med ekte KI, ikke i testmodus. Feilmeldingene virker også i testmodus (FR-34) |
| 45 | «skal det ikke stå i readme hvordan sensor skal gjøre det?» / «automatisk, kan vi skrie i addundet at vi skal oppdatere readme kontinuerlig gjennom hele prosjektet?» | Database og testbruker lages automatisk (NFR-8). Ny del «Arbeidsmåte» i addendumet |
| 46 | «tror vi må tenke tid her, men at det står til kravene gitt av faglærer i sensorveiledning» / «ut ifra krav 3, skal jeg ha manuell eller automatisk test av flyten? ende til ende?» | KI-en sjekket kriterium 3: én testtype holder. Automatiske tester for telleregel og innlogging, skrevet testplan (NFR-12), automatisk flyttest på kuttlisten |
| 47 | «har du forslag til hva vi kan kutte ved dårlig tid?» / «jeg trodde det som står under kuttes først allerede var på kuttlisten?» | KI-en foreslo en nødliste og forklarte forskjellen fra kuttlisten. Nødlisten lagt inn under risiko |
| 48 | «kan vi ta stegene hver for seg?» | De små funnene gått gjennom ett om gangen: OAuth på kuttlisten, begrunnelse i FR-23, fasit ved testdataene |
| 49 | «mener du det er bra dersom alt ligger i en mappe?» | Eksempel på mappestruktur for testdata lagt i addendumet |
| 50 | «ja jeg vil ha den med, men står det da også de titngene som PRD allerede dekker?» / «[…] mener at readme allerede nå har lenker til filene?» | NFR-8 gjort om til en samlet sjekkliste for README |
| 51 | «jeg har ingen proposal så vidt jeg vet» | Ingen endring i PRD-en; åpent punkt: spørre faglærer om product brief regnes som proposal |
| 52 | «kan vi sette dette på en liste som kan være med hvis vi har tid?» | WCAG AA og alternativtekst på kuttlisten som «gjøres hvis det blir tid», begrunnet med tid |
| 53 | «kan du sende en litt mer detaljert liste på endringene vi har gjort» / «[…] vil det da si at den er skrevet men bare ikke gjort noe med» | Oversikt over alle endringer i steg 2; KI-en forklarte at gjentatte trykk står som en antakelse i FR-27, som gås gjennom i steg 4 |
| 54 | «jeg kom på en ting, i produktbriefen står det nevnt noen navn eller selskap som bruker ATS […]» / «[…] jeg trenger kanskje kilder for disse verktøyene som lærer poengterte om prosentene jeg hadde tidligere» | KI-en sjekket Jobscan, Rezi, Teal og Kickresume på nett: alle tilbyr både nøkkelordsjekk og KI-søknadsbrev, så påstanden i briefen og PRD-en stemte ikke |
| 55 | «skiller egentlig søknadsassistenten seg fra noen av de andre, for hvis ikke er det ikke noe vits å ha det med?» | KI-en vurderte hvilke forskjeller som holder; den sterkeste er den åpne telleregelen |
| 56 | «jeg vil ha den originale overskriften, og at teksten under deretter skal forklare at dette ikke nødvendigvis er annereledes» / «jeg likte ikke introduksjonssetningen […]» / «1» | «Hva gjør dette annerledes» skrevet om i PRD-en med kilder nederst |
| 57 | «ja rett opp produktbrief også» | Samme retting og kildeliste i product brief |
| 58 | «[…] lurer på om det er ting vi har merket oss som vi skal gjøre senere men som ikke står noe sted?» / «jeg ønsker vi opretter en TO DO liste som vi kan sjekke av […]» | TO DO-liste opprettet (`todo.md`); brief-memlog oppdatert med endringene i briefen fra PRD-arbeidet |
