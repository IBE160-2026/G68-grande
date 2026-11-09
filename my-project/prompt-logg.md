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

**Dette har jeg blitt oppmerksom på under arbeidet med PRD:**

1. **Spør når du ikke forstår, i stedet for å si ja.** Flere av de viktigste endringene kom fordi jeg sa at jeg ikke skjønte noe. Forskjellen på ATS, gap-analyse og nøkkelordtreff (prompt 40–43) endte med at nettsiden skal forklare begrepene for brukeren. Det hjalp også å be KI-en ta ett funn om gangen (26, 48).
2. **KI-en tar feil, og jeg må sjekke det.** KI-en formulerte kuttlisten feil (11), flyttet briefen uten å rette CI-sjekken (18) og hadde en påstand om konkurrentene som ikke stemte (54). Alle tre ble oppdaget fordi jeg stilte spørsmål.
3. **Påstander trenger kilder.** Faglærer påpekte at prosentene i briefen manglet kilder, og det samme gjaldt navnene på verktøyene. Da vi sjekket, viste påstanden seg å være feil.
4. **Krav må kunne testes og passe til tiden.** Jeg kuttet bevisst ting som ordstamme-regel, redigering i nettleseren og automatisk flyttest, la til en nødliste og koblet kravene til sensorveiledningen (46, 47).
5. **Forskjellen på product brief og PRD.** Har lært at Produktbrief er en kort beskrivelse av hva som skal bli produktet, mens det er i PRD man utdyper hva produktet skal inneholde og gjøre.
6. **Arbeidsmåte og sporbarhet.** Beslutningslogg og prompt-logg er to forskjellige ting, arbeidet må inn i GitHub underveis, og en TO DO-liste hindrer at ting blir glemt.

### 2026-10-11 – Status for PRD og «Hva jeg lærte» (egen terminal, mens steg 3 pågikk)

| # | Min prompt | Resultat |
|---|---|---|
| 59 | «hei, nå jobber vi med PRD i naboterminalen, hvor mye er igjen av PRD før denne er ferdig?» | Oversikt over ferdigstillingen: steg 1–2 ferdig, steg 3 i gang, steg 4–7 gjenstår |
| 60 | «jeg har spurt om dette med proposal, ikke fått svar så ikke huk av ennå. Vi kan skrive hva vi har lært. Men lurer på hva jeg skal dekke, altså hva jeg lærte under skrivingen av PRD?» | Proposal-punktet står åpent; KI-en foreslo seks temaer hentet fra prompt-loggen |
| 61 | «nei det er ikke vits, jeg liker punktene du har satt opp […] Bruk dette som overskrift: dette har jeg blitt oppmerksom på uner arbeidet med PRD. for punkt 5: Har lært at Produktbrief er en kort beskrivelse av hva som skal bli produktet, mens det er i PRD man utdyer hva produktet skal inneholde og gjøre.» | Delen «Dette har jeg blitt oppmerksom på under arbeidet med PRD» lagt inn over, med min tekst i punkt 5 |
| 62 | «push» | Pushet til GitHub |
| 63 | «ligger det prompts og memlog også?» | Alt til og med steg 2 ligger på GitHub; endringene fra steg 3 kopieres når steget er ferdig |
| 64 | «ja takk» | Denne delen av prompt-loggen |

### 2026-10-11 – Finalize steg 3: gjennomgang av PRD-en

| # | Min prompt | Resultat |
|---|---|---|
| 65 | «1 og 2» | To hjelpere leste PRD-en kritisk: én mot BMADs kvalitetssjekkliste og én som «sensor» mot sensorveiledningen. 6 høye, 11 middels og 7 lave funn |
| 66 | «ja enig med du, for vi skal ikke overlagre noe data, hvis du logger ut er alt som ble gjort forrige gang glemt» / «supert» | FR-15 og suksesskriterium 8: samme prosent gjelder innenfor samme søknad |
| 67 | «jeg ser dette kan bli vanskelig å kode, men vi kan ikke ha sånn at hver enkeltbokstav skal sammenliknes det blir for dumt» / «men det er jo en god del forkortelser som bare er på to bokstaver og» | KI-en viste med eksempler at «AI» fortsatt er treff i «AI-modeller», men ikke i «mail». FR-17: nøkkelord på 1–3 tegn må stå som eget ord |
| 68 | «hmm, ja ser problemene. Jeg antar at folk vil skrive en akademisk søknad fordi det høres mer troverdig ut, så jeg ønsker at den skal være akademisk fortsatt. har du et forslag til hvordan vi kan gjøre det mindre motsigende?» | FR-24 beholder akademisk tone, men fikk tre sjekkbare regler. Korrektur retter språket, men beholder innhold, eksempler og rekkefølge (egen stemme). Lista over KI-fraser er et åpent punkt |
| 69 | «jeg skal levere hele prosjektet innen 15 desember, regner med å bli ferdig med PRD i dag» / «vi kan ha det som et utgangspunkt også kan vi revurdere den ila neste uke når jeg får kontroll på resterende fag» | Ny tabell med milepæler fram til 15. desember, og regel: mer enn tre dager forsinket betyr at neste punkt på nødlisten kuttes |
| 70 | «jeg har hørt om dette, men skjønner ikke hvordan det fungerer. […] hva mener du med PR?» / «alt dette med main og branch kommer kun inn når vi jobber med koding?» | KI-en forklarte branch og pull request med en tegning. Fra første story: én branch og én PR per story, med en kort kommentar om feil KI-en gjorde |
| 71 | «så story er koding?» / «okei så du kommer til å huske at vi skal gjøre a til e når vi kommer så langt i prosjektet?» | KI-en forklarte forskjellen på epic, story og koding, og lagret arbeidsmåten i addendum, TO DO-lista og sin egen hukommelse |
| 72 | «kan du utdype s3?» / «ja» | NFR-9: automatiske tester også for kontroll av KI-svar, input, gjenbruk av nøkkelordlisten, innloggingskrav og nedlastet fil |
| 73 | «jeg vil gjerne ta punkt for punkt» | De middels og lave funnene ble gått gjennom ett og ett |
| 74 | «ja altså når du har registrert deg kan du logge inn. Du skal ikke logge inn for så å registrere, det blir feil» | FR-7: registreringen og innloggingen krever ikke innlogging |
| 75 | «jeg skjønner ikke helt hensikten her?» / «1» | KI-en forklarte hvorfor åpne spørsmål hører hjemme i PRD-en. Ny del «7. Åpne spørsmål» |
| 76 | «søknad gir ikke mening men de andre er br» / «analyse kanskje» / «ja da beholder vi søknad og tar det ut av listen» | Ordliste lagt inn. KI-en påpekte at «analyse» kunne blandes med gap-analyse, og at knappen heter «Begynn å lage søknad», så «søknad» ble beholdt |
| 77 | «JA det virker greit, jeg vil ha Din ferdigstilte søknad! istedenfor brevsiden» | Oversikt over flyten øverst i del 2. Siden med brevet heter «Din ferdigstilte søknad!» |
| 78 | «enig i det du sier» / «ja vi kan flytte dem inn» | Testdataene får en skannet PDF og en fil av feil type. Alternativtekst og WCAG-kontrast flyttet fra kuttlisten inn i NFR-6 |
| 79 | «1 ingen grense, 2 setning» / «tilbake til B8 var det en god avgjørelse» / «hmm ja det kan bli et problem, suksesskriteriet er bra, men blir tungt å skulle lese en søknad dobbelt opp fordi alt kommer på nytt» / «jeg liker anbefaling 2, men er nok lurt å ta det i UX steget» | Jeg spurte om valget mitt var lurt, og KI-en pekte på at brevet kunne bli vist dobbelt. FR-23: brukeren ser endringene uten å lese brevet to ganger, og UX bestemmer hvordan. Nytt suksesskriterium 12 |
| 80 | «for B8, dette står det vel noe om i breifen også, om det gjør det så må det endres på må det ikke?» / «ja det er greit» | Briefen rettet tilsvarende (rødt og grønt fjernet) |
| 81 | «vet ikke» / «kanskje 10-15, for er vel satt at sensor skal bruke 15-20?» / «ja det kan være lurt» | NFR-8: 10–15 minutter. NFR-12: README prøves fra en ny, tom kopi før funksjonsstopp og før levering |
| 82 | «hvorfor skal man blande inn en medstudent her? gjennom gapanalsyen får de vite hva de mangler» / «åja da skjønte jeg hva du mente, ja vi kan ta det med» | Nytt suksesskriterium 13: en medstudent kan forklare resultatsiden med egne ord |
| 83 | «ja, og ja 3 er bra» / «ja det er greit» (x2) | Kriterium 1 sjekker begge sider av gap-analysen, og KI-testene kjøres tre ganger. Punkter om oppdatering av PRD-en under kodingen og om linter og språk lagt i addendum |
| 84 | «ja push alt nå» / «så da er alt av logger og tabeller og huskeliste osv pushet» / «ja takk» | Pushet. Gjennomgangene og kildesjekkene kopiert til `2-prd/gjennomganger/`. KI-en oppdaget at prompt-loggen manglet steg 3 og la den inn |

### 2026-10-11 – Finalize steg 4: antakelsene i PRD-en

| # | Min prompt | Resultat |
|---|---|---|
| 85 | «vi kan ta de steg for setg» | KI-en foreslo å avgjøre alle 9 antakelsene samtidig, men vi gikk gjennom dem én og én |
| 86 | «utsett» / «vi utsetter» | FR-12: grensen for filstørrelse bestemmes i arkitekturen. FR-29: filnavnet bestemmes i UX, og det ble lagt et punkt i addendum |
| 87 | «ja» (x6) | FR-17 (hvert nøkkelord telles én gang, og prosenten rundes av), FR-22, FR-23 (ikke bare farge), FR-27, FR-28 og FR-36 (ikke samtykke i testmodus) ble vanlige krav |
| 88 | «jeg tenker vi tar A+B» | FR-31: en ny søknad starter med tomme felt. «Beholde CV-en ved ny søknad» ligger på kuttlisten |
| 89 | «er det tydelig skrevet hvilke ting som avgjøres i senere deler av prosjektet som f.eks UX? og en begrunnelse på hvorfor?» / «detser bra ut legg det inn» | KI-en svarte at det bare var delvis tydelig: det var spredt og manglet begrunnelse. Ny del «Avgjøres i UX og arkitektur» med en tabell over hva, hvor og hvorfor ikke nå |
| 90 | «du kan pushe alt, memlog og prompts også» | Denne delen av prompt-loggen. Alt er pushet |

### 2026-10-11/12 – Finalize steg 5: struktur og språk i PRD-en og addendumet (pågår)

| # | Min prompt | Resultat |
|---|---|---|
| 91 | «ja fortsett med steg 5» | KI-en kjørte en strukturgjennomgang av PRD-en og addendumet (to hjelpere samtidig). Språket ventet til etterpå, så tekst som skulle flyttes, ikke ble vasket først |
| 92 | «jeg må ta de en og en» | KI-en foreslo å godkjenne alle anbefalingene samtidig, men vi gikk gjennom dem én og én |
| 93 | «ja» (x5) | PRD: FR-28 delt i tre deler, nødlisten flyttet til del 4, egen tabell for «Gjøres hvis det blir tid», Milepæler som eget kapittel, FR-32 og FR-34 delt i underpunkter. Ordlyden uendret |
| 94 | «ja» / «beholde begge» / «behold» | Fulgte KI-ens råd om å beholde: setningen om utgangspunktet i FR-23, skjermbildene både i FR-38 og NFR-8, og hele punktet «KI-tjeneste» i addendumet |
| 95 | «jeg skjønte ikke helt» / «ja» | KI-en forklarte enklere at addendumet er delt etter hvem som skal bruke det. KI-frasene fikk egen seksjon, «Til prompten for brevet» |
| 96 | «ja» (x3) / «ja til a) , skjønte ikke b» / «ha det likt» | Addendumet: punktene gruppert, skissene øverst i «Til UX», kodestil flyttet til Arbeidsmåte, like mellomrom, og kilden skrevet likt («fra product brief») |
| 97 | «ja hvis lista med 10 først» / «ja til alle» | Språkgjennomgang: 11 skrive- og kommafeil rettet samlet (KI-en hadde først telt feil og sagt 10) |
| 98 | «kan du comitte og pushe endringene nå, må gå» | Pushet. Gjennomgangene lagt i `2-prd/gjennomganger/` |
| 99 | «ja det høres bra ut, men hva mener du med C i python det er ikke c i python» / «så du mener at dersom noen har nummerert etter bokstaver også bare C skal skjønne at C: Python er en greie?» / «ja begge» | FR-17: «kort nøkkelord» ble «4 tegn eller mer», og eksempelet ble «Kan C og Python». Jeg fant en svakhet i telleregelen: «C» i en liste nummerert med bokstaver gir feil treff. Den er lagt inn som kjent begrensning |
| 100 | «ja» (x3) | FR-34: «Full generering og Korrektur» i stedet for «begge modusene». Ordlisten: ingenting lagres etter at brukeren logger ut. Tre steder fikk «Korrektur» i stedet for knappenavnet |
| 101 | «kan vi gå over 4 en gang til så jeg får det helt klart for meg» / «synes egt det ble litt rotete» / «jeg synes det var vanskelig å skille dem to fra hverandre modus og knapp» / «korrektur og full generering» | Forskjellen på knapp og modus var vanskelig å holde styr på. Nå har hver modus ett navn overalt: Korrektur og Full generering |
| 102 | «på knappene ønsker jeg at det skal stå begge deler så det ikke går an å misforstås» / «A» / «ja» | FR-20: knappene på nettsiden viser begge navnene, for eksempel «Korrektur – Forbedre mitt brev». En endring i nettsiden, ikke bare i teksten |
| 103 | «jeg må gå igjen, kan du lagre de nye endringene» / «vi kan pushe, push alt av memlog, promptlog og alle dokumemtene vi har endret på» | Committet, og senere pushet sammen med denne delen av prompt-loggen. 12 av 16 språkfunn gjenstår |
| 104 | «/bmad-prd» / «ja» / «ja» | Fortsatte språkgjennomgangen fra funn 5. FR-36: «på startsiden» flyttet fram, så det er klart at samtykket gis der. Del 1: «regnes ut» i stedet for «regnes med» |
| 105 | «A» / «A» | FR-19: eget søknadsbrev er også fortsatt fylt ut når brukeren går tilbake. FR-32: «bryter» i stedet for «knapp» for testmodus, som i addendumet |
| 106 | «jeg mener jo at dette produktet ikke nødvendigvis har så mye nytt eller annerledes, det mener jeg vi ryddet på at det er kun denne telleregelen som gir en spesifikk pprosent, pluss forklaringer på begrepene som skiller seg ut» / «ja begge» | Tre steder sa ulike ting om hva som skiller nettsiden fra andre. «Den ærlige begrensningen» og nødlisten punkt 6 sier nå det samme som resten av del 1: telleregelen og forklaringene |
| 107 | «ja» / «ja» | «Sofistikering» i stedet for «sofistikasjon», og punktlisten i FR-24 uten komma og punktum. Ferdig med funnene i PRD-en |
| 108 | «jeg husker ikke» / «det han skriver er at det er krevende, nevner han at jeg må ha det med?» / «vi kan prøve B, men dersom det blir vanskelig settes det på kuttlisten» | KI-en sjekket faglærers tilbakemelding: tabeller er nevnt som krevende, ikke som krav. Addendumet sier nå at jeg prøver å støtte tabeller, og at det settes på kuttlisten hvis det blir vanskelig |
| 109 | «ja» / «ja» / «b» | Addendumet: «KI-verktøyet jeg koder med (for eksempel Claude Code)» i PR-regelen, «Programmeringsspråk» i stedet for «Språk», og FR-3 i stedet for FR-7 ved røde felt |
| 110 | «jeg skkjlønner ikke» / «ja» | KI-en forklarte enklere hva henvisninger er. FR-8 lagt til der PDF-lesing nevnes. Språkgjennomgangen er ferdig |
| 111 | «ja til 1 og 2, vent med å sette final, da ønsker jeg på ny push av begge loggene også og evt andre dokumenter som er endret på» | Product brief rettet så den sier det samme som PRD-en om fortrinnet. Committet og pushet med begge loggene. PRD-en er ikke satt til ferdig ennå |
| 112 | «det eneste jeg lurer på før vi gjør det er, er det noe som ikke stemmer overens med hverandre nå i briefen og PRD, og har det skjedd noen endringer jeg ikke har bedt om?» / «A, og siden det ikke hat gått tre dager siden milepæl datoen går det fint, den er mest for min egen del» | KI-en gikk gjennom alle endringene ord for ord. Ingen endringer i innholdet var gjort uten at jeg hadde sagt ja. Brief-en hadde en annen rekkefølge i flyten enn PRD-en (modus valgt etter analysen). Den er nå rettet, så modus velges først, som i PRD-en |
| 113 | «ja, og om det er noe mer som skal med i readme så må det med også» | PRD-en satt til ferdig (`status: final`). «(under arbeid)» fjernet i README-ene. README-en i my-project fikk en rad for `gjennomganger/`, som manglet, og README-en i roten fikk en lenke til addendumet. Committet og pushet |
| 114 | «tusen takk,, briefen tilsvarer proposal» | Det åpne spørsmålet om proposal er avklart i PRD-en (del 8) og krysset av i TO DO-listen. Kuttlisten trenger ikke endres |

## 2026-10-20 – UX, del 1: utseende og Ingrids brukerreise (pågår)

Verktøy: Claude Code med BMAD-skillen `bmad-ux` (grundig vei, med visuelle forslag). Alle beslutninger er logget i `3-ux/ux-memlog.md`, og forslagene jeg valgte mellom ligger i `3-ux/skisser/`.

| # | Min prompt | Resultat |
|---|---|---|
| 115 | «1 og 2, skoleprosjekt, grundig vei, da forstår jeg bedre» | Kildene er PRD-en og addendumet. KI-en hentet ut alt om skjermer, krav og åpne UX-spørsmål |
| 116 | «1) enkel, effektiv, levende 2) ikke en statisk og kjedelig nettside 3) ingen skisser» / «1) en kombinasjon av farger, bevegelse, mindre illustrasjoner og vennlig tekst» | Stemningen for nettsiden. KI-en spurte hva «levende» betyr, i stedet for å gjette |
| 117 | «2) er det vanskelig å ha begge deler» / «A» | KI-en forklarte at mørk modus dobler kontrastsjekk og testing. Bare lys modus. Mørk modus står under «Hvis tid» i TO DO-lista |
| 118 | «ok, husk dette er en nettside, ikke app» | Jeg rettet KI-en, som hadde kalt den «appen». Forslagene vises som nettside |
| 119 | «jeg er veldig glad i lilla så likte nummer 5 best, men usikker på om den er like appelerende for alle dersom den er rosa/lilla» / «jeg må si det er den samme som i sta som appelerer best til meg, den er så lun» | KI-en laget fem lilla varianter for å teste tvilen min. Jeg valgte likevel fargetemaet «Myk fersken» |
| 120 | «jeg liker teksten slik den er nå, enkel og grei» / «1) Baloo 2, så lenge man får hele overskriften på en linje på PC og telefon» | Systemskrift på hele siden. Bare logoen «Søknadsassistenten» har en egen skrift (Baloo 2) |
| 121 | «først, er dette en slik story som det er snakk om? som vi skal lage sammen med epics?» | KI-en forklarte forskjellen på brukerreise (UX) og user story (koding) |
| 122 | «2) jeg ville blitt usikker, da det er personalia hennes som sendes av gårde med CV» / «teksten kan anbefale at man fjerner personalia, men må ikke det er en hvers valg» | Samtykket forklarer at ingenting lagres, og anbefaler å fjerne personopplysninger. Det er brukerens eget valg. Ingen PRD-endring |
| 123 | «legger bare pilen over også popper det opp en boks» / «enig i forslaget ditt, sånn at det fungerer for alle tre tilfellene» | KI-en pekte på at bare hover ikke virker på mobil og med tastatur (NFR-6, NFR-7). «i»-boksen åpnes med hover, trykk og tastatur |
| 124 | «kjapt spørsmål, må vi ikke ha med testmodus her? tenkte å ha det oppe i hjørnet» / «1) kun på startsiden» | Testmodus oppe til høyre, logg ut nede til høyre og KI-merknaden nede til venstre. Det skal lages en egen reise for sensor |
| 125 | «mener vi skrev i PRD at man må samtykke når man velger modus» / «A, det er jeg som surrer, jeg glemte startsiden» | KI-en sjekket PRD-en: samtykket står på startsiden (FR-36). Vi følger PRD-en |
| 126 | «Dette kan du jobbe videre med er hyggeligere å se» | Lista over det CV-en mangler, heter «Dette kan du jobbe videre med» på skjermen. I PRD og tester heter den fortsatt «mangler» |
| 127 | «Mulig å få noe fyrverkeri?» / «hver gang ett nytt forslag er skrevet, fyrverkeri» | Fyrverkeri rundt «Din ferdigstilte søknad!» i 2–3 sekunder, men ikke for dem som har valgt redusert bevegelse |
| 128 | «tenker man skal ha mulighet til å både laste ned som PDF og word, så en bli her knapp er fint» | Vinduet etter nedlasting har tre valg: ny søknad, logg ut og bli her. Ingrids reise er ferdig i ni steg |
| 129 | «jeg gir meg for i dag, kan du commite det vi har gjort i dag under UX» | Beslutningslogg og forslag kopiert til `3-ux/`, og committet |

## 2026-10-21 – UX, del 2: Eiriks og Henriks brukerreiser, skisser av alle sidene og ferdigstilling (pågår)

Verktøy: Claude Code med BMAD-skillen `bmad-ux`. Alle beslutninger er logget i `3-ux/ux-memlog.md`, og skissene ligger i `3-ux/skisser/`. Utkastene til `DESIGN.md` og `EXPERIENCE.md` ligger i `3-ux/`.

| # | Min prompt | Resultat |
|---|---|---|
| 130 | «1) med tanke på steg 8 og 9, hvordan løser vi dette må å kunne laste ned både pdf og word?» / «ja takk» | KI-en laget en skisse med tre måter å laste ned både Word og PDF på |
| 131 | «Jeg likte A best, men likte at det ble grønt på B når brevet er lastet ned, videre så mangler A en logg ut knapp. Usikker på om jeg har skrvet at det skal være en logg ut knapp hele tiden stemmer ikke det?» | Jeg oppdaget at KI-en hadde glemt logg ut-knappen og KI-merknaden i skissen, selv om de var bestemt. Vinduet etter nedlasting beholdes, og knappen blir grønn med hake |
| 132 | «1) ser riktig ut, 2) tror vi skal endre til steg 8 når fyrverkeriet kommer» | Ingrids reise er bekreftet. Høydepunktet er når brevet kommer med fyrverkeri |
| 133 | «Eirik, 22, finans, han har allerede skrevet en søknad som han ønsker å forbedre, søkt på jobber før, på telefon, ønsker kun å forbedre fordi han har jobbet mye med sitt eget» / «ja han har en bruker fra før» / «a i størst grad, men har jo skrevet i PRD at man skal lime inn tekst også så det må gå an det også» | Brukerreise 2 med Eirik, Korrektur på mobil. Både opplasting og innliming må virke på mobil |
| 134 | «Oppdater søknadsbrevet mitt» / «"Din oppdaterte søknad er ferdig!" 2at brevet er ferdig, men fortsatt hans» | Knappen og overskriften i Korrektur. Høydepunktet er at brevet er ferdig, men fortsatt Eiriks eget |
| 135 | «jeg foretrakk nummer 1, mindre rotete og du får likevel sammenliknet det nye mot det gamle ved å trykke på teksten 2) fyrverkeri ved overskrift, og ja testmodus skal ikke vises med mindre man er i testmodus» | Endringer i Korrektur markeres per setning, og et trykk viser det gamle. Jeg rettet KI-en, som hadde vist «Testmodus» i en skisse der den ikke skulle stå |
| 136 | «6, er det ingen tilbakeknapp? mener vi har tatt med det i PRD både for full generering og korrigering?» / «1) b. 2) tilbake er bra det» / «ja vi bør jo ha en tilbakeknapp der også, dee» | Jeg fant at tilbakeknappen fra FR-19 manglet. «Tilbake» står nå ved siden av hovedknappen på resultatsiden og på innleggingssiden |
| 137 | «Henrik, har 10-15 minutter, ettersom at han er sensor i faget må jeg anta at han har vært borti dette før, 2) vil sjekke at moduser og feilmeldinger fungerer 3) vet ikke» / «b» / «1) alt er gjort innen 15 minutter, 2) b» / «1) trodde det sto i sensorveiledningen at alt skulle ta 15-20 minutter? 2) enig» / «a» | Brukerreise 3 med Henrik, sensor i testmodus. KI-en sjekket sensorveiledningen: 15–20 minutter gjelder installering og oppstart. Hjelpetekst om testdata i testmodus, og feilmeldinger i en boks øverst |
| 138 | «vi kan fortsette nå» / «a absolutt best! tilbakeknapp her også i tilfelle sensor går videre uten å trykke testmodus» | Modusvalget: to store kort med ikon, og «Tilbake» til startsiden |
| 139 | «1) supert, veldig bra! 2) liker det! 3) Likte B best, mer oversiktlig, 4) bra det» | Resultatsiden: merket «Laget av KI», en prosentlinje og nøkkelordene i to lister |
| 140 | «har vi tatt for oss hvordan registreringssiden ser ut?» / «1) ja samme, 2) b, 3) fra start 4) ja en mulighet til å gå tilbake om du hat bruker» | Jeg fant at registreringssiden ikke var tegnet. Den har nå «Gjenta passord», regelen «Minst 8 tegn» under feltet og en lenke tilbake til innloggingen |
| 141 | «kan vi gå over å se hvilke vi har laget for nå? usikker om vi har laget for mobil og PC for alle stegene i de ulike modusene» / «burde vi ikke ha noen skisser av alle?» | Oversikten viste at tre viktige sider manglet skisse. Jeg ville ha skisser av alle sidene, og det er laget |
| 142 | «1) vedlig bra, eneste er at på PC ønsker jeg hele setningen på en linje, på telefon må det bli flere linjer for at det ikke skal bli for smått […] 2) ønsker ikke at AI teksten skal stå som en del av startsiden, kun en sånn samtykker til bruk av KI med boks ved siden av samt denne i'en som man kan trykke på som da gjør at teksten popper frem. 3) likte det du har gjort med testmodus» / «[…] angående denne ekstern KI så er B et bra alternativ» / «supert, eneste er at på PC så kan denne begynn å lage søknad være enda større» | Startsiden. KI-en pekte på at ønsket mitt brøt med FR-36. Jeg valgte å følge PRD-en med én kort linje over avkrysningsboksen |
| 143 | «storfornøyd med det jeg ser! 1) supert, 2) supert 3) ja det er greit, 4) supert» / «1 og 2 er bra» | Innleggingssiden og brevsiden er godkjent |
| 144 | «kan du vise meg oversikten du viste i sta på nytt nå så jeg ser om vi mangler noe?» / «vi legger dem inn i skissene» / «supert, og ja enig at det blir beholdt dersom noe går galt» | Tre feilmeldinger fra PRD-en manglet skisse (KI-feil, for stor fil, «Du må logge inn først»). De er lagt inn. Feiler «Nytt forslag», beholdes det gamle brevet |
| 145 | «push» | Pushet til GitHub |
| 146 | «vi kan ferdigstille nå» | En hjelper skrev DESIGN.md og EXPERIENCE.md ut fra loggen og skissene. Hjelperen kunne ikke se samtalen, så KI-en rettet brukerreisene etterpå til stegene jeg hadde bekreftet |
| 147 | «b» / «hull 2) vil du vise meg fargen det er snakk om? hull 3) enig» / «foretrekker hovedfargen» | FR-18-forklaringen står mellom gap-analysen og nøkkelordtreffet. Rammen rundt skrivefelt hadde for svak kontrast, og jeg valgte hovedfargen etter å ha sett en sammenligning. Bruddpunkt på 700 px |
| 148 | «om testmodusknappen, ja det er greit, hull 4) b , 5) a» / «hull 6) kan du ha byttet om de to nederste? hull 7) b» / «ja det gir mening» | Samtykket krysses av på nytt hver gang, og man får en advarsel ved utlogging før nedlasting. Tekster for tomme lister. KI-en forklarte hvorfor tekstene ikke var byttet om |
| 149 | «1b, 2b, 3a, 4b, 5b» / «ok på alle» | Fem motsigelser mellom loggen og skissene er løst, og sju antakelser er bekreftet |
| 150 | «jeg synes vi skal gjøre det, men det blir i morgen, jeg ønsker at du legger inn punktet med baloo2 skriften på to do listen, deretter comitte alt vi har gjort i dag, og push alt til github med de loggene vi skal ha med» | Baloo 2 og nettleserens tilbakeknapp står på TO DO-lista under Arkitektur. Committet og pushet med beslutningslogg, prompt-logg, utkast og skisser. Den kritiske gjennomgangen tas i morgen |

## 2026-10-22 – UX, del 3: kritisk gjennomgang (runde 3) (pågår)

Verktøy: Claude Code med BMAD-skillen `bmad-ux`. Tre hjelpere leste dokumentene hver for seg: A sjekkliste, B tilgjengelighet og C sensor-blikk. Rapportene og den samlede rapporten ligger i `3-ux/gjennomganger/`. Alle beslutningene er logget i `3-ux/ux-memlog.md`.

| # | Min prompt | Resultat |
|---|---|---|
| 151 | «A+B+C» | Tre hjelpere gikk gjennom DESIGN.md og EXPERIENCE.md. Ingen kritiske funn, 9 høye, 21 middels og 33 lave. Rundt ti av dem var det samme funnet sett av flere |
| 152 | «A» / «jeg skjønner ikke hva alle disse tingene er» / «enig» | Jeg ba om forklaring på hver ting før jeg bestemte meg. Pynten fikk en kutteliste i tre nivåer, og bygges etter kjerneflyten |
| 153 | «1» / «1) ja, 2) a» | Korrektur: KI-en svarer med par av ny og gammel setning. Fjernede setninger nevnes under brevet. Alt det man legger inn, sjekkes når man trykker «Sjekk CV-en min» |
| 154 | «ja» / «ja er enig, men hvordan åpner jeg den linken i chrome?» / «det funker både med tab og med å legge musa over» / «funker det og» | Vinduene, den faste raden, ventetegnet og «i»-boksen virker med tastatur og skjermleser. Jeg testet «i»-boksen selv i Chrome, og den virket, selv om to hjelpere mente at den hadde en feil |
| 155 | «ja det funker for meg så lenge det ser likt ut som nå i vanlig størrelse så er jeg fornøyd» | Siden skal virke ved 320 px og 200 % zoom, men se lik ut ved vanlig størrelse |
| 156 | «Vi lager brevet ditt - det kan ta en liten stund» / «Vil se dem først» / «alle er fine» / «E-posten er ikke gyldig» | Jeg skrev min egen ventetekst og valgte den korte e-postteksten. Jeg ville se de seks fargene fra skissene før jeg godkjente dem. Startsiden starter alltid en ny søknad, og feltene står side om side først fra 1000 px |
| 157 | «ja den husker at du var i testmodus når du kommer tilbake til startsiden» / «etter innlogging kommer du alltid til startsiden» | Testmodus-bryteren husker valget så lenge man er logget inn. Etter innlogging kommer man til startsiden |
| 158 | «ja den er fin, men den inneholder jo kun info fra i dag» / «A» | `3-ux/mine-valg-og-ki-feil.md` er laget for UX. En samlet fil for hele prosjektet lages før innlevering |
| 159 | «jeg vil se dem før jeg godkjenner dem» / «jeg må si jeg ikke helt skjønner hva jeg leser på her» / «ja til alt» | Jeg ville se presiseringene før jeg godkjente dem. KI-en skilte ut de to som endrer det man ser, og jeg godtok alle |
| 160 | «kan vi ta det et og ett steg» / «ja» | Skissene ble oppdatert med endringene fra runde 2, én side om gangen, og jeg så på hver skisse i nettleseren før vi gikk videre. Skissene av modusvalget og resultatsiden viser nå bare forslagene jeg valgte |
| 161 | «ja» (om vinduet ved utlogging etter «Nytt forslag») / «ser bra ut, commit» | Etter «Nytt forslag» er brevet nytt og ikke lastet ned, så vinduet om utlogging kommer igjen |
| 162 | «push» / «fortsett» / «ja» | Skissene ble oppdatert med endringene fra runde 3, én side om gangen. Alle sidene fikk en knapp for nettbrett (768 px) og følger nå den ekte bredden. Jeg sjekket hver skisse i nettleseren før vi gikk videre |
| 163 | «ja» (om Eiriks krav og nøkkelord) | Resultatsiden fikk en Korrektur-variant med Eirik og Fjordbanken. Kravene og nøkkelordene var KI-ens forslag, og jeg godtok dem |
| 164 | «fortsette» / «jA» | Skissene ble flyttet til `mockups/`. Fire hjelpere leste dokumentene, én for struktur og én for språk per dokument |
| 165 | «OK» / «GODTA» / «EN OG EN» | Jeg godtok de rene feilene og flyttingen samlet, men ville ta forslagene som rørte ved mine tekster, ett og ett |
| 166 | «PRØV PÅ NYTT OVER ALT» | KI-en foreslo «Prøv igjen» overalt, men jeg valgte «Prøv på nytt» overalt |
| 167 | «SÅ LENGE JEG HAR EN SIDE SOM SENSOR KAN SE PÅ NÅR JEG GODKJENTE OG KODEREN FINNER HVA FARGENE BRUKES TIL ER JEG FORNØYD» | Fargene fra skissene ble flettet inn i hovedlista etter bruk, og godkjenningen står i `mine-valg-og-ki-feil.md` |
| 168 | «BEHOLDE» (to ganger) / «JA SETT SOM FERDIG» | Jeg beholdt to ting slik de var. DESIGN.md og EXPERIENCE.md er satt til ferdig (`status: final`) |

## 2026-10-27 – Faglærers sesjonslogg og konkurrentanalyse

Verktøy: Claude Code med faglærers skill `sesjonslogg` og BMAD-skillen `bmad-deep-recon` (typen «competitive»). Beslutningene for konkurrentanalysen er logget i `4-konkurrentanalyse/konkurrentanalyse-memlog.md`.

| # | Min prompt | Resultat |
|---|---|---|
| 169 | «git pull» | KI-en hentet `CLAUDE.md` og skillen `sesjonslogg`, som faglærer hadde lagt rett i repoet |
| 170 | «supert, jeg ønsker egentlig å fortsette å logge slik jeg gjør i dag, dajeg ønsker en kontinuitet gjennom hele prosjektet, men at jeg kan ha med sesjonsloggen også siden læreren har kommet med den som en anbefaling. […] Kanskje issues er er hoved også legger vi inn to do der?» / «ja ser bra ut, ønsker også en readme for to do og issues!» | Jeg fortsetter med mine egne logger og bruker sesjonsloggen i tillegg. Jeg foreslo `issues.md` som hovedliste, men KI-en anbefalte `todo.md` fordi den har vært med fra starten, og jeg godtok det. En README i `.logs/kristine/` forklarer begge deler |
| 171 | «ja det ser bra ut, men logs/kristine er det i repoet mitt?» | KI-en forklarte at mappa ligger i repoet, men kan være skjult fordi navnet begynner med punktum |
| 172 | «jeg ønsker også at du kjører en bmad-deep-recon og competetive research om det er en egen ting, dette er noe læreren anbefalte oss å gjøre, skulle helst vært gjort før PRD, men tenker vi kan gjøre det nå og legge inn funnene i en egen mappe så jeg kan vise til dette eventuelt» | Jeg valgte at KI-en skulle gjøre søket selv, sjekke både posisjoneringen og hva vi kan lære, og bare se på de fire konkurrentene fra briefen |
| 173 | «så lenge resultatet ikke endrer på noe vi allerede har laget er det bare å kjøre» | Fem hjelpere søkte i to runder. Differensieringen i briefen holder: ingen av de fire forklarer hvordan poengsummen regnes ut, ingen har KI-korrektur av eget brev med markerte endringer, og ingen støtter norsk. Brief, PRD og UX er ikke endret. Funnene ligger i `4-konkurrentanalyse/` |
| 174 | «COMMIT» / «JA» | Committet, og denne delen av prompt-loggen er skrevet |

## 2026-11-03 – Suksesskriterier, sjekk mot sensorveiledningen og første pull request

Verktøy: Claude Code. Ingen BMAD-skill, bare samtale, nettsøk og GitHub.

| # | Min prompt | Resultat |
|---|---|---|
| 175 | «git pull» | Ingenting nytt fra faglærer |
| 176 | «hvilke mål har vi satt for prosjektet som vi må nå for å lykkes med prosjektet?» | KI-en viste visjonen, de 13 suksesskriteriene og det som aldri kuttes, og sa at jeg lå bak milepælene |
| 177 | «akkurat den tidsplanen er det bare å se bort i fra, men okei så vi har suksesskriterier, det er det viktigste for meg» | KI-en måler nå fremdriften mot suksesskriteriene, ikke mot milepældatoene |
| 178 | «ikke helt ennå, er synes du produkt briefen min og prd min er bra?» | Ærlig vurdering: suksesskriteriene kan testes, differensieringen er ærlig og nødlisten er god. Fem bekymringer: stort omfang, strengt «tre av tre» med ekte KI, fasit som skjønnsvurdering, medstudent til kriterium 13 og ingen kilde på ATS |
| 179 | «kan du lagre disse bekymringene?» | Lagt inn i `todo.md` |
| 180 | «takk, videre kan du se om det jeg har gjort passer til sensorveiledningen?» | Planleggingen og prosessen passer godt. Fem hull: arkitektur og stories mangler, ingen branch eller PR ennå, README lenket ikke til alt, milepælene var ikke forklart, og NFR-8 manglet «hvem den er for» |
| 181 | «4) hvor ligger denne listen? skal den være synlig for læreren?» / «okei, A ikke hatt tid og ventet på at læreren skal begynne med sitt prosjekt så jeg kan følge undervisningen» | Jeg valgte å beholde milepælene og legge til en merknad med min forklaring, i stedet for å slette dem |
| 182 | «readme må også oppdateres så den viser til alt» | README lenker nå til UX, konkurrentanalysen, sesjonsloggene og TO DO, i en ny seksjon om prosess og KI-bruk |
| 183 | «ja vi må jo ha med en hvem den er for, trodde dette sto både i brief og prd?» | Målgruppen sto der, men NFR-8 sa ikke at README skal fortelle det. **KI-feil:** KI-en laget en branch uten å spørre meg først |
| 184 | «jeg skjønner ikke dette med main og branch, trodde dette ikke kom før kodingen?» / «A» / «ferdig, git pull» | KI-en forklarte main, branch og pull request. Jeg valgte å prøve det nå. Første pull request (PR #1), som jeg merget selv på GitHub |
| 185 | «står det beskrevet hvorfro vi gjorde denne mergen? det er jo en litt rar merge» | Grunnen står i PR #1 og i commit-meldingen. Merge-commiten viser bare til PR-en |
| 186 | «få se bekymringene på nytt» / «nei, men jeg ønsker å løse dem» | Vi gikk gjennom de fem bekymringene én og én |
| 187 | «1) er forsåvidt enig, min forståelse på læreren er at denne uken blir vi ferdig han ferdig med UX og arkitektur […] er 22 november mulig da?» / «ja det er bedre» | KI-en foreslo at hele flyten skulle virke 22. november. Jeg spurte om det var mulig, og etter å ha regnet på helgene sa KI-en at det var for tidlig. Nå er det to sjekkpunkter i risikotabellen i PRD-en: 22. og 29. november |
| 188 | «videre til 2) hva er sannsynligheten for at vi ikke får det til? og er det bedre å være føre-var?» / «ja» | Gap-analysen har størst risiko. Plan B ligger i del 5 i PRD-en. Promptene testes tidlig når de ekte KI-svarene til testmodus lages (FR-38) |
| 189 | «ok» | NFR-3: fasiten skal ha en kort begrunnelse for hvert krav |
| 190 | «kan hvem som helst gjøre dette? ettersom at jeg studerer på nett kjenner jeg ingen andre på studie» / «ja det er bra, det blir en kollega» | Kriterium 13 sier nå «en person som ikke kjenner prosjektet» i stedet for «en medstudent» |
| 191 | «det er greit, beholde nøkkelord» | Kilde på ATS fra Harvard Business School lagt til i brief og PRD. **KI-feil:** KI-en sa først «over 90 % av arbeidsgiverne», men da kilden ble sjekket, var det 63 %, og over 90 % av dem. Tallet 88 % fra omtalene fantes ikke i kilden |
| 192 | «videre så lurer jeg på om det analysen vi gjorde deep recon som havnet under konkurrentanalyse kræsjer med noe vi har laget så langt» / «1) hva mener du med dette? […]» / «okei men hvis vi kjører en ny analyse, og det har kommet endringer vil dette få konsekvenser for oss?» / «okei da er jeg enig i endringene» | Ingen motsigelser. PRD-en fikk en forsiktig formulert setning om norsk og KI-korrektur som fortrinn, og et krav om kjente begrensninger i README (NFR-8). Konkurrentanalysen sier nå hva den førte til |
| 193 | «jeg skjønte ikke helt dette med NRF-8» / «vi kan oppdaterer readme nå da, sånn at den har alt som den skal inneholde» / «supert» | README fikk det som er sant nå (hva nettsiden gjør, hvem den er for og kjente begrensninger), og overskrifter merket «kommer» for resten, slik at den ikke beskriver kode som ikke finnes |

**Hva jeg lærte om å styre KI-en:** Under PRD-arbeidet oppdaget jeg at jeg er veldig nøye og vil se alt KI-en gjør til punkt og prikke. Det gir kontroll, men tar mye tid. For å bli ferdig i tide må jeg stole mer på KI-ens avgjørelser i det som er lett å rette, og heller bruke tiden på det som er viktig.

**3. november:** Lært hvordan man gjennomfører en PR, med branch og main. Ble også påminnet at det er viktig å sjekke kildene ordentlig før man tar dem i bruk.

## 2026-11-04 – Arkitektur

Verktøy: Claude Code med BMAD-skillen `bmad-architecture` (veiledet). Alle beslutninger er logget i [`arkitektur-memlog.md`](5-arkitektur/arkitektur-memlog.md).

| # | Min prompt | Resultat |
|---|---|---|
| 194 | `/bmad-architecture` | KI-en leste PRD, addendum, UX og TO DO, og spurte om arbeidsmåte og hvem som skal lese dokumentet |
| 195 | «1) Veiledet 2) altså dette skal også inn i github og skal være synlig for lærer og sensor også» | Veiledet arbeidsmåte. Kopi i `my-project/5-arkitektur/` |
| 196 | «jeg har aldri kodet før så alt dette er nytt, det som er viktigst for meg er hva som er enklest, men som kan levere ett godt resultat» | Python + Flask, ett språk for hele nettsiden |
| 197 | «1) jeg vet ikke, jeg har laget en bruker slik at jeg kan bruke claude code […] Jeg ønsker ikke bruke mer enn 250kr. 2) kan bruke opus. 3) hva betyr .env? og 4) hvordan vet jeg når jeg trekkes […]» | Claude Opus 5.5. Tak på 250 kr med forhåndsbetalt kreditt og auto-reload slått av. Pris per KI-kall vises i terminalen. KI-en forklarte `.env` |
| 198 | «Ja pypdf høres bra ut» | pypdf for å lese PDF. Kolonner og tabeller prøves først, ellers blir det en kjent begrensning |
| 199 | «1) ser bra ut 2) stusser litt over denne med formatet på KI-svaret i korrektur […] stusser også over neste med arbeidsgiver i filnavnet? Kan du ta meg kjapt gjennom FR-34 igjen […] 3) da mener du at det skal være en begrunnelse for hvilke endringer som er gjort i CV'en […]» | Lagdelingen godkjent. KI-en forklarte at formatet er dataene bak UX-visningen, at filnavnet allerede var bestemt i UX, og hvordan testmodus vasker teksten |
| 200 | «2a og 2b da skjønner jeg, 3) ja det hørtes veldig bra ut, men enig at det legges til dersom tid» | «Kort grunn ved hver endring» settes under «Gjøres hvis det blir tid» i PRD-en |
| 201 | «ja du kan gjøre alt sammen, du trenger ikke lage word kopi […] feil nummer to om økt, hva mener du med det og dette med å runde opp osv med 12,5% er dette for designet?» | KI-en forklarte økten og avrundingen. Arkitekturen satt til ferdig, PRD og UX fikk 5 MB, og alt ble kopiert hit. **KI-feil:** se [mine valg og KI-feil](5-arkitektur/mine-valg-og-ki-feil.md) |
| 202 | «fått dette av læreren min, jeg begynte med å logge inn på vercel, men når jeg skal sjekke innstillingene finner jeg ikke alle innstillingene» / «okei så vercel skal jeg egentlig ikke bry meg om?» | KI-en viste hvor innstillingene er skjult, men rådet meg til å vente, fordi det ikke finnes kode ennå, og fordi Vercel passer dårlig med øktene, databasen og API-nøkkelen. GitHub CLI var allerede installert og innlogget |
| 203 | «kan du formulere en kort melding til læreren angående vercel» / «kortere og mindre teknisk» / læreren svarte at det «IKKE er et krav» | Vercel er ikke et krav, og nettsiden kjøres lokalt etter README. Svaret er ført inn i beslutningsloggen for arkitekturen |
| 204 | «kan du nå da sjekke at vi ligger i stand til å svare på sensorveiledningen på en god måte?» / «1) A til de andre) supert» | Godt dekket, men KI-en fant at lærerens CI bare kjører testene i `backend/`. Arkitekturen fikk mappa `backend/`, regel AD-15 (sporbarhet fra plan til kode) og konvensjoner for ryddig kode, testplan og README |

## 2026-11-07 – Epics og stories

Verktøy: Claude Code med BMAD-skillen `bmad-create-epics-and-stories`. Planen ligger i [`6-epics-og-stories/`](6-epics-og-stories/).

| # | Min prompt | Resultat |
|---|---|---|
| 205 | `/bmad-create-epics-and-stories` / «hva er steg 1?» | KI-en forklarte steg 1: kravene fra PRD, UX og arkitekturen samlet i fire lister (38 FR, 12 NFR, tilleggskrav fra arkitekturen og 24 UX-krav) |
| 206 | «jeg har ikke godkjent den» / «c» | **KI-feil:** KI-en sa at steg 1 var godkjent fordi det sto i fila, men jeg hadde ikke godkjent det. Kravlistene ble lagt fram på nytt, og jeg godkjente dem |
| 207 | «hvis jeg forstår rett nå så er epics og stories kodingen?» | KI-en forklarte at epics og stories er planen for kodingen, ikke selve kodingen |
| 208 | «sånn jeg ser det er det jo fler av sidene som mangler i epicsen, typ startsiden?» / «dette ser bra ut, C» | Epicene var skrevet ut fra kravnumrene, så sidene var vanskelige å se. Hver epic fikk en linje «Sider:», og jeg godkjente de 8 epicene |
| 209 | «JA» / «Det er enkelte ting her jeg ikke henger med på, mye linker osv så for meg blir det rotetem men det ser jo for så vidt greit ut» / «har du en enkel epic 1» / «epic 1 ser bra ut, det som er bestemt av deg ser også bra ut» | Storiene ble vist med mange koder og filnavn. Nå får jeg en enkel utgave i chatten, og detaljene står bare i fila for den som skal kode |
| 210 | «ja, eneste jeg lurer på er hvor startsiden er, for nå går vi rett fra innlogging til modusvalg ser det ut som (full generering/ forbedre)» / «ja gjør det» | KI-en viste at startsiden bygges i tre runder (Epic 1, 2 og 4). Tittelen på story 2.4 ble tydeligere |
| 211 | «hva mente du med koden mot claude» / «ja» | KI-en forklarte delen av nettsiden som sender teksten til Claude og tar imot svaret, og hvorfor den kommer før bryteren |
| 212 | «ja» / «nei det er fint» / «ja» | Epic 3–8 godkjent. Pynten kommer etter punktene på nødlisten |
| 213 | «synes du jeg skal la flere agenter se på det?» / «C» | KI-en rådet meg til å gå rett til sluttsjekken i stedet for Party Mode, fordi grunnlaget allerede var gjennomgått. Sjekken fant og rettet tre stories som ventet på en senere story |
| 214 | `/code-review` / `/effort max` / «nå som vi har satt max, kan du ta en ny sjekk?» | **KI-feil:** Den første sluttsjekken så bare etter kravnumre. Den grundige sjekken leste kravteksten og fant 8 feil (se [mine valg og KI-feil](6-epics-og-stories/mine-valg-og-ki-feil.md)). `/code-review` fant feil i loggen fra forrige økt |
| 215 | «1) ok 2) ok 3) hva mener du med feil type? 4) ok 5) ok 6) ok 7) ok 8) ok og ok til de små tilleggene» / «c» | Alt rettet, og planen har 31 stories. KI-en forklarte at «feil type» er en fil som ikke er PDF, og at `.gitignore` ville skjult Word-filen |
| 216 | `/bmad-sprint-planning` | KI-en sjekket at planen er klar til koding (PRD, UX, arkitektur og epics henger sammen) og laget `sprint-status.yaml` med alle 31 stories. Den fant ett lite hull: kriterium 5 trenger PDF ut, som står på nødlisten |
| 217 | «kan du sjekke at vi ligger riktig an med tanke på sensorveiledning, og om det står noe om refleskjonsrapporten i denne sensorveiledningen?» / «ja» | KI-en sjekket repoet mot de sju kriteriene og fant at vi ligger godt an. Refleksjonsrapporten (30 %) nevnes bare kort og manglet i planen, så den kom inn i TO DO. README fikk lenker til epics, sprint-status og mine valg i epics |
| 218 | «Her får du den slik at du kan lagre den, og ta med deg ting på veien mens vi jobber» (limte inn malen for refleksjonsrapporten) | Malen ble lagret, sammen med en notatfil der KI-en samler stoff underveis (KI-feil, utfordringer og lærdommer), sortert etter delene i malen |
| 219 | «usikker på om dette skal inn på github ettersom at det ikke er en del av del 1» / «ja» | KI-en anbefalte å holde malen og notatene utenfor GitHub, fordi de hører til del 2 og malen er faglærers dokument. Mappen ble lagt i `.gitignore` før den ble pushet, og ligger bare på min PC |

## 2026-11-08 – Story 1.1: Nettsiden starter fra en ny kopi av repoet

Verktøy: Claude Code med BMAD-skillen `bmad-build`. Planen og kodegjennomgangen ligger i [`9-koding/`](9-koding/), og koden i [PR #2](https://github.com/IBE160-2026/G68-grande/pull/2).

| # | Min prompt | Resultat |
|---|---|---|
| 220 | `/bmad-build` / «Ja, story 1.1» / «Ja, bruk dem» (hjelpeagenter) | KI-en laget en egen branch og et sammendrag av planene for epic 1, og skrev planen (spec) for story 1.1 |
| 221 | «Behold samlet» / «Godkjenn og fortsett» | Planen var lengre enn anbefalt, men jeg valgte å holde den samlet fordi alt er grunnmuren. En hjelpeagent kodet storyen, og tre andre leste koden kritisk. **KI-feil:** 8 av 25 funn var ekte og ble rettet, blant annet port 5000 på Mac og en test som manglet for tomme verdier i `.env` (se [spec-en](9-koding/spec-1-1-nettsiden-starter-fra-en-ny-kopi-av-repoet.md)) |
| 222 | «jeg skjønte ikke hva jeg skulle gjøre i den andre terminalen» | KI-en startet nettsiden for meg i stedet, så jeg bare trengte å åpne adressen i nettleseren |
| 223 | «jeg får opp verktøyvinduet, men får ikke den til mobilstørrelse» / «jeg fikk det til nå, hadde ikke åpnet verktøysiden helt» | KI-en forklarte mobil-ikonet i verktøyvinduet (F12). Jeg sjekket siden ved 375 px |
| 224 | «ja det ser veldig bra ut! regner med at startsiden ikke er ferdig, da det i de neste stegene kommer mer om begynn søknad og KI-samtykke osv?» | KI-en bekreftet at startsiden bygges videre i story 1.2–1.4, 2.4 og 4.3 |
| 225 | «push» / «jeg har flettet nå» | Branchen ble pushet og PR #2 laget. CI var grønn på Linux og Windows, og jeg flettet PR-en. Story 1.1 er satt til ferdig |
| 226 | «du kan pushe, husk å ha med promptlog og memlog også om det er nødvendig […] skulle gjerne hatt at PR #2 heter Story 1.1 ferdig eller noe i den duren der. Skal jeg trykke på den knappen som heter delete branch nå?» | Prompt-loggen ble oppdatert, og planen og kodegjennomgangen ble kopiert til `9-koding/`. PR #2 fikk nytt navn |

## 2026-11-08 – Story 1.2: Logge inn med testbrukeren

Verktøy: Claude Code med BMAD-skillen `bmad-build`. Planen og kodegjennomgangen ligger i [`9-koding/`](9-koding/spec-1-2-logge-inn-med-testbrukeren.md), og koden i [PR #3](https://github.com/IBE160-2026/G68-grande/pull/3).

| # | Min prompt | Resultat |
|---|---|---|
| 227 | `/bmad-build` / «1.2» | KI-en laget en egen branch og skrev planen (spec) for story 1.2: database med testbrukeren, innloggingssiden og innlogging som krav for startsiden |
| 228 | «Behold hele» / «Godkjenn og fortsett» / «Ja, bruk agenter» | Planen var lengre enn anbefalt, men jeg holdt den samlet. En hjelpeagent kodet storyen, og tre andre leste koden kritisk. **KI-feil:** 9 av 19 funn var ekte og ble rettet, blant annet en test som aldri kunne feile (sjekk av at passordet ikke logges), at knappen fortsatt hoppet ved redusert bevegelse, og at «testmodus på» sto to steder (se [spec-en](9-koding/spec-1-2-logge-inn-med-testbrukeren.md)) |
| 229 | «du kan starte den for meg» / «det det ser bra ut, alt funker, push!» | KI-en startet nettsiden, og jeg prøvde testbrukeren, tomme felt og feil passord i nettleseren. Branchen ble pushet og PR #3 laget |
| 230 | «jegg har flettet nå» | CI var grønn på Linux og Windows, og jeg flettet PR #3. Story 1.2 er satt til ferdig, og sprint-statusen og TO DO er oppdatert |
## 2026-11-08 – Story 1.3: Registrere seg som ny bruker

Verktøy: Claude Code med BMAD-skillen `bmad-build`. Planen og kodegjennomgangen ligger i [`9-koding/`](9-koding/spec-1-3-registrere-seg-som-ny-bruker.md), og koden i [PR #4](https://github.com/IBE160-2026/G68-grande/pull/4).

| # | Min prompt | Resultat |
|---|---|---|
| 231 | `/bmad-build` / «1.3» | KI-en laget en egen branch og skrev planen (spec) for story 1.3: registreringssiden, alle feilmeldingene og lenkene mellom innlogging og registrering |
| 232 | «Behold hele» / «Godkjenn og fortsett» / «Ja» (hjelpeagenter) | Planen var lengre enn anbefalt, men jeg holdt den samlet. En hjelpeagent kodet storyen, og tre andre leste koden kritisk. **KI-feil:** 3 av 16 funn var ekte og ble rettet, alle i testene: sjekken av at ingenting hentes utenfra, så ikke på den nye siden, testen av escaping kunne bestått selv om e-posten forsvant, og koblingen av «Minst 8 tegn» og feilteksten ble ikke testet ved for kort passord (se [spec-en](9-koding/spec-1-3-registrere-seg-som-ny-bruker.md)) |
| 233 | «ja start siden for meg» / «det funket utmerket, push» | KI-en startet nettsiden, og jeg prøvde ny bruker, alle feilene og innlogging med den nye brukeren i nettleseren. Branchen ble pushet og PR #4 laget |
| 234 | «flettet» | CI var grønn på Linux og Windows, og jeg flettet PR #4. Story 1.3 er satt til ferdig, og sprint-statusen og TO DO er oppdatert |

## 2026-11-08 – Story 1.4: Logge ut, og bare innloggede kommer inn

Verktøy: Claude Code med BMAD-skillen `bmad-build`. Planen og kodegjennomgangen ligger i [`9-koding/`](9-koding/spec-1-4-logge-ut-og-bare-innloggede-kommer-inn.md), og koden i [PR #5](https://github.com/IBE160-2026/G68-grande/pull/5).

| # | Min prompt | Resultat |
|---|---|---|
| 235 | `/bmad-build` / «1.4» | KI-en laget en egen branch og skrev planen (spec) for story 1.4: «Logg ut» i hjørneraden, «Du må logge inn først» når man ikke er logget inn, og en test som går gjennom alle sidene |
| 236 | «Beholde hele» / «Godkjenn og fortsett» | Planen var lengre enn anbefalt, men jeg holdt den samlet. En hjelpeagent kodet storyen, og tre andre leste koden kritisk. **KI-feil:** 6 av 19 funn ble rettet. Den viktigste: trykket man tilbake rett etter innlogging, sto «Du må logge inn først» og «Logg ut» på samme side. Meldingen kom også for alle verdier i adressen, og en test for gammel cookie på innloggingssiden manglet. Ett funn er utsatt til README (se [spec-en](9-koding/spec-1-4-logge-ut-og-bare-innloggede-kommer-inn.md)) |
| 237 | «denne siden fungerer ikke» | Nettsiden kjørte ikke. KI-en startet den, og jeg prøvde innlogging, «Logg ut» og «Du må logge inn først». Alt virket |
| 238 | «det virket ikke, jeg kommer tilbake til velkommen» / «det fungerer ikke nå heller» / «Lite skript» | **KI-feil:** tilbakeknappen etter utlogging viste fortsatt «Velkommen». Beskjeden til nettleseren om ikke å lagre sidene holder ikke i nyere Chrome og Edge, og det andre forsøket (å be nettleseren slette lagrede sider) hjalp heller ikke. Jeg valgte et lite skript som laster siden på nytt, og da sender serveren til innloggingen |
| 239 | «ja nå stemmer det, push» | Tilbakeknappen virket med skriptet. Branchen ble pushet og PR #5 laget |
| 240 | «flettet» | CI var grønn på Linux og Windows, og jeg flettet PR #5. Story 1.4 og hele epic 1 er satt til ferdig, og sprint-statusen og TO DO er oppdatert |

## 2026-11-08 – Retrospektiv for epic 1

Verktøy: Claude Code med BMAD-skillen `bmad-retrospective`. Dokumentet ligger i [`9-koding/`](9-koding/epic-1-retro-2026-11-08.md).

| # | Min prompt | Resultat |
|---|---|---|
| 241 | «du kan lukke den nå, og ja vi kjører en retrospectiv» | KI-en stoppet nettsiden, samlet commitene, PR-ene, spec-ene og sesjonsloggene for epic 1, prøvde hele flyten med en ekte server, og lot tre hjelpere gå gjennom all koden i epicen samlet. Ingen feil for brukeren, men 4 småting i koden bør ordnes før epic 2, og bredde og zoom er bare delvis prøvd |
| 242 | «Hva mente du med punkt 1?» / «ok til startsiden» | KI-en forklarte at økten ryddes to steder i koden, og hva som skjer når man er innlogget og åpner innloggingen. Jeg valgte at man da sendes til startsiden |
| 243 | «vil dette med startsiden dersom du er logget inn fra før stride imot PRD?» | KI-en sjekket PRD-en, UX og arkitekturen: det strider ikke imot noe, det fyller et hull i planen |
| 244 | «Godkjent med punkter» / «jeg ønsker at du gjør rettingene nå» | Epic 1 er godkjent med 7 åpne punkter i sprint-statusen. De fire småtingene i koden rettes nå i en egen PR |
| 245 | «Samlet i én PR» / «Godkjenn og fortsett» | KI-en laget en egen branch og plan for de fire rettingene. En hjelpeagent kodet dem, og tre andre gikk gjennom koden. **KI-feil:** to tester sjekket noe som alltid var sant (testen slettet selv det den skulle sjekke at ble slettet), og sjekken av lagene i koden forbød ikke biblioteker som leser filer eller går på nett, selv om arkitekturen sier det. Begge er rettet. 152 tester |
| 246 | «jeg kommer ikke til velkommen når jeg skriver inn 127.0.0.1:5000/logg-inn …» / «da skjønner jeg, det funket nå» | Serverloggen viste at jeg ikke var logget inn: nettsiden var startet på nytt, og da glemmer den alle innlogginger. Etter ny innlogging virket det |
| 247 | «det funker med bredden også» / «ja fikk også prøvd zoom, push» | Jeg prøvde 320 px, 768 px og 200 % zoom, og alt så riktig ut. Branchen ble pushet, og PR-en ble laget |
| 248 | «flettet» | CI var grønn på Linux og Windows, og jeg flettet PR #6. Punkt 1–5 fra retrospektiven er krysset av i sprint-statusen og TO DO. Punkt 6 og 7 (arbeidsmåten) gjelder fra story 2.1 |

## 2026-11-08 – Story 2.1: Telleregelen for nøkkelordtreff

Verktøy: Claude Code med BMAD-skillen `bmad-build`. Planen og kodegjennomgangen ligger i [`9-koding/`](9-koding/spec-2-1-telleregelen-for-nokkelordtreff.md), og koden i [PR #7](https://github.com/IBE160-2026/G68-grande/pull/7).

| # | Min prompt | Resultat |
|---|---|---|
| 249 | `/bmad-build` / «2.1» / «Ja, bruk hjelpeagenter» | KI-en laget en egen branch, en hjelpeagent samlet det viktigste for epic 2 i [`epic-2-context.md`](9-koding/epic-2-context.md), og KI-en skrev planen (spec) for telleregelen |
| 250 | «er du ferdig eller skjedde det en feil nå» | **KI-feil:** KI-en stoppet midt i arbeidet uten å si fra, rett før den skulle skrive planen. Ingenting var feil, og den fortsatte |
| 251 | «Behold hele» / «Godkjenn og fortsett» | En hjelpeagent kodet telleregelen, og tre andre leste koden kritisk. **KI-feil:** alle testene var grønne, men de ville ikke oppdaget tre feil i selve regelen: om grensen på 4 tegn ble flyttet, om «SQL» ga treff i «MySQL», eller om «C++» ga treff i en CV med bare «C». 21 funn: 6 rettelser i testene, 2 punkter utsatt (tekst fra PDF i story 6.1 og en ny linje i README i story 8.1), resten avvist med begrunnelse. 175 tester |
| 252 | «ja» | Branchen ble pushet, og PR #7 ble laget med merknad om KI-feilene |
| 253 | «hvorfor lager vi ikke alt bare på main da?» / «ja ta det med til refleksonsrapport» | KI-en forklarte at branch og PR gir en CI-sjekk før koden kommer inn i main og et spor sensor kan følge (kriterium 1 og 3), selv når jeg jobber alene. Jeg beholdt arbeidsmåten, og forklaringen er lagt inn i notatene til refleksjonsrapporten |
| 254 | «Pull request successfully merged and closed» / «pleier også å få en sånn delete knapp» | CI var grønn på Linux og Windows, og jeg flettet PR #7. Branchen ble ikke slettet automatisk, og knappen for å slette den manglet, fordi jeg hadde pushet to commits (rad 253 og loggen) etter at PR-en var flettet. GitHub viser ikke knappen når branchen har noe som ikke er flettet. KI-en la de to endringene inn i main for hånd. Story 2.1 er satt til ferdig, og sprint-statusen og TO DO er oppdatert |
| 255 | «hvorfor skal du slette dem? eller er det fordi de allerede er i main?» / «du kan pushe og slette branchene» | KI-en forklarte at en flettet branch bare er en kopi av noe som alt er i main, og at PR-ene og historikken blir liggende. Branchene ligger under organisasjonen, på github.com/IBE160-2026/G68-grande/branches. Main ble pushet, og de flettede branchene for story 1.3, 1.4 og 2.1 ble slettet på GitHub og lokalt |

## 2026-11-08 – Story 2.2: Fiktive testdata og fasit for første testcase

Verktøy: Claude Code med BMAD-skillen `bmad-build`. Planen og kodegjennomgangen ligger i [`9-koding/`](9-koding/spec-2-2-fiktive-testdata-og-fasit-for-forste-testcase.md), og koden i [PR #8](https://github.com/IBE160-2026/G68-grande/pull/8).

| # | Min prompt | Resultat |
|---|---|---|
| 256 | `/bmad-build` / «2.2» / «Ja, hele økta» | KI-en laget en egen branch og skrev planen (spec) for testdataene: en fiktiv student-CV og en annonse for junior utvikler med tydelige hull (blant annet SQL og førerkort), en fasit, to håndlagde KI-svar og en test som sjekker at fasiten og telleregelen gir samme prosent |
| 257 | «Godkjenn og fortsett» | En hjelpeagent laget utkastet (7 av 11 nøkkelord = 64 %), og tre andre gikk gjennom det. **KI-feil:** testen sjekket bare nøkkelordene som er treff, så «MySQL» i CV-en kunne gitt «SQL = Nei» uten at noe feilet. Tabellen med kravene ble aldri lest, en tom arbeidsgiver ble godtatt, og README beskrev innliming i testmodus som om den alt fantes. KI-en tømte også fasiten ved en feil da den prøvde om testen virket, men la den tilbake fra en kopi. 14 funn: 6 rettet, 8 avvist med begrunnelse. 182 tester |
| 258 | «kan du åpne alle for meg» / «push» | KI-en åpnet CV-en, annonsen og fasiten i Notisblokk, og jeg leste dem og godkjente innholdet. Branchen ble pushet, og PR #8 ble laget med merknad om KI-feilene |
| 259 | «da var den flettet, ser vi kun har 5 prosent igjen til vi når 100 så venter med 2.3» | CI var grønn, og jeg flettet PR #8. Story 2.2 er satt til ferdig, og sprint-statusen og TO DO er oppdatert. Story 2.3 venter til neste økt, fordi bruksgrensen hos Claude snart var nådd |

## 2026-11-09 – Story 2.3: Testmodus kjenner igjen testdataene

Verktøy: Claude Code med BMAD-skillen `bmad-build`. Planen og kodegjennomgangen ligger i [`9-koding/`](9-koding/spec-2-3-testmodus-kjenner-igjen-testdataene.md), og koden i [PR #9](https://github.com/IBE160-2026/G68-grande/pull/9).

| # | Min prompt | Resultat |
|---|---|---|
| 260 | `/bmad-build` «2.3, åpne spec-en når den er klar så jeg kan lese den» | KI-en skrev planen (spec) og åpnet den i Notisblokk: testmodus vasker teksten (mellomrom, linjeskift og store bokstaver betyr ikke noe) og kjenner igjen testdataene, CV-en avgjør testcaset, feilen havner på riktig felt, og de ferdige KI-svarene sjekkes før de brukes. KI-en valgte selv at begge feltene får feil når både CV og annonse er feil |
| 261 | «Behold samlet» / «Godkjenn og fortsett» | KI-en laget en egen branch og skrev koden, og tre hjelpeagenter gikk gjennom den. **KI-feil:** et KI-svar der alle nøkkelordene var tomme tekster, ble godtatt og ville krasjet senere i tellingen, selv om testen for testdataene hadde en strengere regel. Akseptansekriteriet «ingen advarsel om `TestKI`» var bare sjekket én gang for hånd, og ingenting ville stoppet det hvis det ble brutt. 15 funn: 6 rettet, 9 avvist med begrunnelse. 231 tester |
| 262 | «ja supert» | Branchen ble pushet, og PR #9 ble laget med merknad om KI-feilene |
| 263 | «da var det flettet» | CI var grønn på Linux og Windows, og jeg flettet PR #9. Story 2.3 er satt til ferdig, og sprint-statusen og TO DO er oppdatert. Branchen ble slettet på GitHub da PR-en ble flettet, og de flettede branchene for story 2.2 og 2.3 er slettet på PC-en |
