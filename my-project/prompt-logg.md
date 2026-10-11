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
