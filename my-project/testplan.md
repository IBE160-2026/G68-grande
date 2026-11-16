# Testplan

Testplanen viser resultatet for suksesskriteriene som ikke testes automatisk (NFR-12). Den fylles ut underveis, og gjøres ferdig i Epic 8 (hele flyten og README fra en ny kopi av repoet).

## Slik testes kriteriene med ekte KI

Kriterium 1, 3, 11, 12 og 14 testes med ekte KI (Claude), ikke i testmodus (PRD del 5). De kjøres tre ganger per testcase, og alle tre må bestå. Feiler én kjøring, forbedres prompten én gang, og alle tre kjøres på nytt (plan B). Feiler det fortsatt, står kriteriet her som ikke bestått, med hva som gikk galt.

Kjøringene gjøres med skriptet `backend/scripts/lag_testsvar.py` (se README). Kjøring 1 skriver de ferdige svarene i testmodus (`backend/testdata/<case>/ki-svar/`). Kjøring 2 og 3 skrives rett i `my-project/testkjoringer/`. Svarene og terminalloggen (tokens og pris) fra alle kjøringene ligger i `my-project/testkjoringer/<story>/<runde>/kjoring-<n>/`, så de kan sjekkes i etterkant, også etter at svarene i testmodus er laget på nytt.

| Kriterium | Hva | Hvordan det sjekkes | Status |
| --- | --- | --- | --- |
| 1 | Gap-analysen finner alle krav som mangler, og ingen dekkede krav står under «mangler» | `gap.json` mot tabellen «Krav» i `fasit.md` | Bestått for case 1 i begge rundene (story 4.4). Bestått for case 2 i begge rundene, og for case 1 på nytt i runde 2 (story 4.5). Bestått i begge rundene for case 1 og 2 etter de nye reglene i brevet (15. november) |
| 3 | Samme CV med to annonser gir brev med krav som er spesifikke for hver annonse | Brevene for CV-en i case 1 mot annonsen i case 1 og case 2 | Bestått i begge rundene: brevene nevner krav som er spesifikke for hver annonse. Brevene i runde 1 hadde to påstander som ikke står i CV-en (et brudd på kriterium 11), så alt ble kjørt på nytt etter plan B, og runde 2 besto også kriterium 11 (story 4.5). Bestått igjen i begge rundene etter de nye reglene i brevet (15. november) |
| 11 | Brevet nevner ingen erfaring, utdanning eller ferdigheter som ikke står i CV-en | `brev-1.json` mot CV-en og «Sjekkliste for brevet» i `fasit.md` | Case 1: ikke bestått i runde 1, bestått i runde 2 etter plan B (story 4.4), og bestått igjen i runde 2 i story 4.5 (runde 1 ble ikke kjørt for case 1). Case 2: bestått i begge rundene (story 4.5). CV-en fra case 1 mot annonsen fra case 2 (kriterium 3): ikke bestått i runde 1, bestått i runde 2 etter plan B (story 4.5). Slutningene under «Story 4.5» er godkjent av Kristine. Etter de nye reglene i brevet (15. november): case 1 og 2 bestått i begge rundene, kriterium 3 ikke bestått i runde 1 og bestått i runde 2 etter plan B. Slutningene er godkjent av Kristine |
| 12 | Korrektur beholder brukerens innhold, eksempler og rekkefølge | `korrektur-1.json` og `korrektur-2.json` mot `eget-brev.txt` og «Sjekkliste for Korrektur» i `fasit.md` | Bestått i alle tre kjøringene for case 1, uten plan B (story 5.2.1 og 5.2.2). Omformuleringene under «Story 5.2.2» er godkjent av Kristine. Etter de nye reglene om flyt (retro 5): bestått i runde 2 etter plan B (vage vurderinger fjernes). Godkjent av Kristine |
| 14 | Nøkkelordlisten har alle nøkkelordene fasiten markerer som viktige | `nokkelord.json` mot «Viktige nøkkelord» i `fasit.md` | Bestått for case 1 i begge rundene (story 4.4) og i runde 2 i story 4.5. Bestått for case 2 i begge rundene (story 4.5). Bestått for case 1 og 2 i begge rundene etter de nye reglene i brevet (15. november) |

## Story 4.4: ekte KI-svar for case 1 (14. november 2026)

Modell: `claude-opus-5-5`. Runde 1 brukte promptene fra story 4.1 og 4.2. Kriterium 11 feilet i runde 1, så brev-prompten ble forbedret én gang (plan B), og alle tre kjøringene ble gjort på nytt i runde 2. Svarene fra runde 2, kjøring 1, er de ferdige svarene i testmodus.

### Runde 1 (kl. 13.42–13.50)

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 1: gap-analysen | Bestått: 6 dekket og 4 mangler, nøyaktig som fasiten | Bestått | Bestått |
| 11: brevet | Ikke bestått | Ikke bestått | Bestått |
| 14: de viktige nøkkelordene | Bestått: alle 8 (19 nøkkelord i alt) | Bestått: alle 8 (19 i alt) | Bestått: alle 8 (18 i alt) |
| Nøkkelordtreffet (telleregelen) | 9 av 19 = 47 % | 9 av 19 = 47 % | 9 av 18 = 50 % |

Ingen av brevene påsto noe fra sjekklisten i `fasit.md`, men Kristine gikk gjennom merknadene og bestemte dette:

1. **Fakta som ikke står i CV-en er brudd på kriterium 11.** Det gjaldt «Linux kjenner jeg fra studiet» og «Linux har jeg brukt i studiet» (kjøring 1 `brev-1` og `brev-2`, kjøring 2 `brev-2`), «det jeg har jobbet mest med i studiet» og «Til daglig bruker jeg Git og GitHub» (kjøring 2 `brev-1`), og «bruker vi Git og GitHub» i bachelorprosjektet (kjøring 1 `brev-2`). CV-en har Linux og GitHub under Ferdigheter og Verktøy, men sier ikke hvor eller hvor ofte de er brukt. `brev-1` i kjøring 1 og 2 hadde slike fakta, så kriterium 11 feilet.
2. **Egenskaper lest ut av en jobb er greit.** For eksempel «møte kunder på en ryddig og vennlig måte» og «holde orden i travle perioder» om butikkjobben. Prompten tillater omformulering av det som står i CV-en.
3. **Brevet skal ikke nevne krav som CV-en ikke dekker.** Kjøring 2 `brev-2` skrev «SQL og relasjonsdatabaser er et område jeg ennå ikke har arbeidet med». Det er ærlig, men hullene står allerede i gap-analysen.
4. **Stillingen skal ha liten forbokstav i overskriften.** Fem av seks brev skrev «Søknad på stillingen som Junior utvikler», fordi tittelen står slik øverst i annonsen.

**Plan B:** `backend/prompts/brev.md` fikk tre nye regler: ikke skriv hvor, når eller hvor ofte en ferdighet er brukt når CV-en ikke sier det, ikke nevn krav som CV-en ikke dekker, og skriv stillingen med liten forbokstav i overskriften.

### Runde 2, etter plan B (kl. 14.18–14.22)

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 1: gap-analysen | Bestått: 6 dekket og 4 mangler, nøyaktig som fasiten | Bestått | Bestått |
| 11: brevet | Bestått | Bestått | Bestått |
| 14: de viktige nøkkelordene | Bestått: alle 8 (19 nøkkelord i alt) | Bestått: alle 8 (20 i alt) | Bestått: alle 8 (20 i alt) |
| Nøkkelordtreffet (telleregelen) | 10 av 19 = 53 % | 10 av 20 = 50 % | 10 av 20 = 50 % |

**Kriterium 1:** i alle seks kjøringene ga KI-en de samme ti kravene som fasiten, med ordlyden fra annonsen. SQL og relasjonsdatabaser, Docker, smidig utvikling og Scrum, og førerkort står under «mangler». Ingen dekkede krav står der. `gap.json` i testmodus er derfor lik den håndlagde fila fra story 2.2, og står ikke som endret i Git.

**Kriterium 11:** ingen av de seks brevene i runde 2 sier hvor eller hvor ofte en ferdighet er brukt uten at CV-en sier det. Linux knyttes bare til jobben som IT-assistent, og GitHub nevnes som noe hun kan («jeg kan også GitHub»). Ingen brev nevner krav som CV-en ikke dekker, og ingen påstår noe fra sjekklisten (SQL eller databaser, Docker, Scrum eller smidig utvikling, førerkort, at Sara alt er ferdig med graden, eller at hun har jobbet som utvikler før). Egenskaper lest ut av jobbene finnes fortsatt, for eksempel «løse konkrete problemer for brukere» om IT-assistent-jobben. Det er greit etter punkt 2 over. Alle brevene nevner stillingen og Testvik Utvikling AS, kobler minst to krav til CV-en, har «junior utvikler» med liten j i overskriften og bruker ingen av de 17 KI-frasene. De har 300–333 ord i 5 avsnitt, uten overskriften, hilsenen og navnet (regelen er 250–400 ord i 4–6 avsnitt), og ingen markdown.

**Merknad om formen (ikke kriterium 11):** `brev-1` i kjøring 3 slutter uten «Med vennlig hilsen» og navnet, selv om prompten ber om det. De andre fem brevene har det, også `brev-1` i testmodus. Ingen automatisk sjekk fanger dette for brev fra ekte KI. (Løst 15. november: nettsiden setter nå selv inn hilsenen og navnet, se «Hilsen, navn og to nye regler i brevet».)

**Kriterium 14:** KI-en skrev «førerkort klasse B» i stedet for «førerkort». Det regnes som med, fordi «førerkort» står som eget ord i nøkkelordet (se `fasit.md`). I runde 2 tok KI-en også med «IT», som gir treff i CV-en.

**Nøkkelordtreffet** gikk ned fra 64 % med de håndlagde svarene til 53 % i testmodus nå. KI-en tok med ord fra annonsen som «bachelorgrad», «informatikk», «relasjonsdatabaser», «tester» og noen ganger «webtjenester». CV-en sier «bachelor», så telleregelen, som søker ordrett, gir ikke treff for «bachelorgrad», selv om gap-analysen sier at kravet om graden er dekket. Det er en kjent begrensning (se README: bøyningsformer fanges ikke opp, og gap-analysen og nøkkelordtreffet kan si hverandre imot). Prosenten varierer også litt med listen fra KI-en (47–53 %). Kriterium 2 (nøyaktig prosent når listen er fast) testes automatisk med listen i `ki-svar/`.

### Kostnad og tid

Tallene er fra loggen i terminalen («KI-kall … tokens … ca. … kr»). En fullført søknad er nøkkelord, gap og ett brev. Kronene er regnet med 11 kr per dollar og prisene for `claude-opus-5-5` i `backend/soknad/innstillinger.py`.

| | Tokens inn (nøkkelord + gap + brev) | Tokens ut (nøkkelord + gap + brev) | Kroner per fullført søknad | Det andre brevet | Hele kjøringen |
| --- | --- | --- | --- | --- | --- |
| Runde 1, kjøring 1 | 1 501 + 2 060 + 3 129 = 6 690 | 138 + 190 + 2 243 = 2 571 | 0,10 + 0,13 + 0,63 = 0,86 kr | 0,65 kr | 1,51 kr |
| Runde 1, kjøring 2 | 6 690 | 138 + 190 + 1 360 = 1 688 | 0,10 + 0,13 + 0,44 = 0,67 kr | 0,62 kr | 1,29 kr |
| Runde 1, kjøring 3 | 6 690 | 132 + 499 + 1 291 = 1 922 | 0,10 + 0,20 + 0,42 = 0,72 kr | 0,45 kr | 1,16 kr |
| Runde 2, kjøring 1 | 1 501 + 2 060 + 3 432 = 6 993 | 135 + 353 + 2 305 = 2 793 | 0,10 + 0,17 + 0,66 = 0,93 kr | 0,53 kr | 1,46 kr |
| Runde 2, kjøring 2 | 6 993 | 141 + 385 + 2 141 = 2 667 | 0,10 + 0,18 + 0,62 = 0,90 kr | 0,52 kr | 1,42 kr |
| Runde 2, kjøring 3 | 6 993 | 141 + 348 + 1 752 = 2 241 | 0,10 + 0,17 + 0,54 = 0,81 kr | 0,65 kr | 1,46 kr |

En fullført søknad kostet 0,67–0,93 kr, under målet på 3 kr (NFR-11) og under overslaget på omtrent 2 kr i PRD-en. Den lengre brev-prompten i runde 2 gir ca. 300 flere tokens inn per brev. De seks kjøringene kostet ca. 8 kr i alt.

Tid per kall: nøkkelord og gap tok 2–5 sekunder hver, og et brev 16–47 sekunder. Det er innenfor tidsgrensen på 90 sekunder i `innstillinger.py`.

### Canva-CV-en

Kristine prøver om KI-en forstår teksten fra Canva-CV-en sin riktig (hva som er utdanning, jobb og oppsummering), med testmodus av. Hun skriver bare hva KI-en forsto og misforsto. Ingen personopplysninger fra CV-en, og ingen KI-svar som siterer den, legges i repoet.

| Dato | Hva KI-en forsto riktig | Hva den misforsto | Resultat |
| --- | --- | --- | --- |
| 14. november 2026 | Teksten ble kopiert fra Canva-PDF-en (`Ctrl+A`, `Ctrl+C`) og limt inn, sammen med annonsen fra case 1. CV-en har bare fiktive opplysninger (Ola Nordmann, example.com). KI-en skilte riktig mellom utdanning (bachelor i datateknologi, så master i informatikk, med skolene), jobb (programvareutvikler, så senior programvareutvikler, med firmaene), oppsummering (profilteksten ble brukt i innledningen) og kurs og ferdigheter (Udemy-kurset, JavaScript, React og Node.js). Alt brevet påstår, står i CV-en (sjekket av Kristine). Brevet følger reglene fra plan B: liten j i overskriften, hilsen og navn, og bare krav CV-en dekker | Ingenting misforstått. Kristine merket ikke at teksten ble rotete da den ble limt inn, eller at noe havnet feil på resultatsiden. Én setning er klønete: «Norsk og engelsk er de to språkene jeg oppgir i CV-en min» | Bestått |

## Story 4.5: case 2 og kriterium 3 (14. november 2026)

Modell: `claude-opus-5-5`. Case 2 (`case-2-okonomi`) er en økonomistudent, Jonas Eksempelsen, som søker som junior økonomimedarbeider i Prøvdal Regnskap AS. Claude laget utkastet til CV-en, annonsen og fasiten, og Kristine godkjente dem før de første kjøringene. Kriterium 3 kjører CV-en fra case 1 (Sara, IT-student) mot annonsen fra case 1 og mot annonsen fra case 2. Inndataene for CV-en fra case 1 med annonsen fra case 2 ligger i `my-project/testkjoringer/4-5/inndata/`.

Runde 1 brukte promptene fra story 4.4. Kriterium 11 feilet i runde 1 for brevene til kriterium 3, så brev-prompten ble forbedret én gang (plan B). Fordi prompten ble endret, ble alt kjørt tre ganger på nytt i runde 2: case 1, case 2 og kriterium 3. Svarene fra runde 2, kjøring 1, er de ferdige svarene i testmodus for begge casene. Svarene og loggene ligger i `my-project/testkjoringer/4-5/runde-1/` og `runde-2/`.

### Runde 1 (kl. 17.24–17.32)

Case 2:

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 1: gap-analysen | Bestått: 5 dekket og 4 mangler, nøyaktig som fasiten | Bestått | Bestått |
| 11: brevet | Bestått | Bestått | Bestått |
| 14: de viktige nøkkelordene | Bestått: alle 6 (16 nøkkelord i alt) | Bestått: alle 6 (16 i alt) | Bestått: alle 6 (16 i alt) |
| Nøkkelordtreffet (telleregelen) | 7 av 16 = 44 % | 7 av 16 = 44 % | 7 av 16 = 44 % |

Kriterium 3 (CV-en fra case 1 mot annonsen fra case 2):

| | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| Krav som bare står i annonsen fra case 2 | Kundekontakt, svar til kunder på telefon og e-post, at firmaet automatiserer | Det samme | Det samme |
| Kriterium 11 | Ikke bestått | Ikke bestått | Bestått |

Brevene for CV-en fra case 1 mot annonsen fra case 1 ble gjenbrukt fra runde 2 i story 4.4, fordi promptene ikke var endret siden da. Alle seks nevner Linux, som bare står i annonsen fra case 1, og ingen nevner kundekontakt. Brevene er altså tydelig ulike for de to annonsene.

Kristine gikk gjennom brevene og bestemte at to setninger er brudd på kriterium 11:

1. **«Python er språket jeg har jobbet mest med»** (kjøring 2, `brev-1`). CV-en sier ikke hva Sara har jobbet mest med. Det er samme type påstand som «det jeg har jobbet mest med i studiet» i story 4.4.
2. **«min første faste jobb»** (kjøring 1, `brev-2`). CV-en sier «min første jobb som utvikler».

I case 2 påsto ingen brev noe fra sjekklisten (Power BI, regnskapsprogram eller Tripletex, lønn, Python eller programmering, at Jonas alt er ferdig med graden, eller at han har jobbet som regnskapsfører før), og ingen nevnte krav som CV-en ikke dekker. Brevene leser egenskaper ut av jobbene, for eksempel «lært å forklare tall og beløp» om kundesenteret. Det er greit etter regelen fra story 4.4. `brev-2` i kjøring 3 manglet «Med vennlig hilsen» og navnet (en formfeil, som i story 4.4).

**Plan B:** `backend/prompts/brev.md` fikk en ny regel: ikke ranger eller sammenlign ferdighetene, verktøyene eller erfaringene til studenten når CV-en ikke gjør det, og ikke endre det CV-en sier om hvilken jobb studenten ser etter. Regelen har en test i `tests/adaptere/test_ekte_ki.py`.

### Runde 2, etter plan B (kl. 17.33–17.44)

Case 1 og case 2:

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 1: gap-analysen, case 1 | Bestått: 6 dekket og 4 mangler, nøyaktig som fasiten | Bestått | Bestått |
| 1: gap-analysen, case 2 | Bestått: 5 dekket og 4 mangler, nøyaktig som fasiten | Bestått | Bestått |
| 11: brevet, case 1 | Bestått | Bestått | Bestått |
| 11: brevet, case 2 | Bestått | Bestått | Bestått |
| 14: de viktige nøkkelordene, case 1 | Bestått: alle 8 (20 nøkkelord i alt) | Bestått: alle 8 (20 i alt) | Bestått: alle 8 (19 i alt) |
| 14: de viktige nøkkelordene, case 2 | Bestått: alle 6 (16 i alt) | Bestått: alle 6 (17 i alt) | Bestått: alle 6 (17 i alt) |
| Nøkkelordtreffet, case 1 | 10 av 20 = 50 % | 10 av 20 = 50 % | 10 av 19 = 53 % |
| Nøkkelordtreffet, case 2 | 7 av 16 = 44 % | 7 av 17 = 41 % | 7 av 17 = 41 % |

Kriterium 3:

| | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| Krav som bare står i annonsen fra case 1 (brevene for case 1 over) | Linux, Flask, fast fadder | Det samme | Det samme |
| Krav som bare står i annonsen fra case 2 | Kundekontakt, svar til kunder på telefon og e-post, at firmaet automatiserer | Det samme | Det samme |
| Kriterium 11 | Bestått | Bestått | Bestått |
| Resultat | Bestått | Bestått | Bestått |

**Kriterium 3:** alle tolv brevene for Saras CV nevner krav som bare står i sin egen annonse. Brevene mot annonsen fra case 1 handler om nettsider, Flask, Git, Linux og fadderen. Brevene mot annonsen fra case 2 handler om at firmaet automatiserer med Python, om kundekontakt og om opplæringen i regnskapsprogrammene. Ingen av brevene rangerer ferdighetene eller endrer hvilken jobb Sara ser etter.

**Kriterium 11:** ingen brev i runde 2 påstår noe fra sjekklistene. Ingen sier hvor, når eller hvor ofte en ferdighet er brukt uten at CV-en sier det («i studiet» står bare om emnene og prosjektene, som CV-en nevner). Alle tolv brevene for case 1 og 2 har hilsen og navn. Merknad: ett brev for case 1 (kjøring 1, `brev-1`) skriver «Annonsen nevner at dere bruker Git». Annonsen krever at søkeren bruker Git, så KI-en har lest annonsen litt feil, men brevet påstår ikke noe som ikke står i CV-en.

**Slutninger godkjent av Kristine (14. november 2026):** brevene som nå er de ferdige svarene i testmodus, har noen setninger som ikke står ordrett i CV-en, men som er lest ut av den. Kristine gikk gjennom dem og godkjente alle fire som omformuleringer av det CV-en sier, ikke brudd på kriterium 11:

- «hadde dermed ansvaret for økonomien til en organisasjon over et helt år» (case 2, `brev-2`). CV-en sier «2025–2026: Kasserer i studentforeningen».
- «I bachelorprosjektet har jeg sammen med to medstudenter laget en nettside» (case 1, `brev-2`). Prosjektet varer 2026–2027, men CV-en skriver «Laget i Python med Flask».
- «erfaring med å utvikle en webtjeneste» (case 1, `brev-2`). CV-en sier «en nettside».
- «forklare ting på en forståelig måte» om jobbene (case 1, `brev-1`). En egenskap lest ut av jobbene, som er greit etter regelen fra story 4.4.

**Svakhet ved plan B:** eksemplene i den nye regelen er tatt fra brevene som feilet, og runde 2 ble kjørt med samme CV. At runde 2 besto, viser derfor mest at KI-en unngår akkurat de setningene. Om regelen virker for andre CV-er, kan prøves med Canva-CV-en eller en ny CV.

**Gap-analysen og brevet kan si hverandre imot:** når CV-en fra case 1 kjøres mot annonsen fra case 2, sier gap-analysen i fem av seks kjøringer at Sara mangler kundekontakt. Brevene kobler likevel kundekontakt til butikkjobben hennes med kundeservice. Claude mener brevet har rett. Det er ikke testet mot noen fasit, fordi kriterium 1 bare sjekkes mot fasiten for hvert case.

### Kostnad og tid

Tallene er fra loggen i terminalen. En fullført søknad er nøkkelord, gap og ett brev. Kronene er regnet med 11 kr per dollar.

| | Tokens inn (nøkkelord + gap + brev) | Tokens ut (nøkkelord + gap + brev) | Kroner per fullført søknad | Det andre brevet | Hele kjøringen |
| --- | --- | --- | --- | --- | --- |
| Runde 1, case 2, kjøring 1 | 1 539 + 2 129 + 3 501 = 7 169 | 147 + 179 + 2 591 = 2 917 | 0,10 + 0,13 + 0,72 = 0,95 kr | 0,72 kr | 1,67 kr |
| Runde 1, case 2, kjøring 2 | 7 169 | 147 + 179 + 2 455 = 2 781 | 0,10 + 0,13 + 0,69 = 0,92 kr | 0,62 kr | 1,54 kr |
| Runde 1, case 2, kjøring 3 | 7 169 | 147 + 179 + 2 092 = 2 418 | 0,10 + 0,13 + 0,61 = 0,84 kr | 0,55 kr | 1,39 kr |
| Runde 1, kriterium 3, kjøring 1 | 1 539 + 2 098 + 3 470 = 7 107 | 147 + 593 + 2 272 = 3 012 | 0,10 + 0,22 + 0,65 = 0,97 kr | 0,70 kr | 1,67 kr |
| Runde 1, kriterium 3, kjøring 2 | 7 107 | 147 + 673 + 1 676 = 2 496 | 0,10 + 0,24 + 0,52 = 0,86 kr | 0,68 kr | 1,54 kr |
| Runde 1, kriterium 3, kjøring 3 | 7 107 | 151 + 605 + 2 332 = 3 088 | 0,10 + 0,23 + 0,67 = 1,00 kr | 0,68 kr | 1,68 kr |
| Runde 2, case 1, kjøring 1 | 1 501 + 2 060 + 3 586 = 7 147 | 141 + 190 + 1 880 = 2 211 | 0,10 + 0,13 + 0,57 = 0,80 kr | 0,68 kr | 1,48 kr |
| Runde 2, case 1, kjøring 2 | 7 147 | 141 + 190 + 2 574 = 2 905 | 0,10 + 0,13 + 0,72 = 0,95 kr | 0,54 kr | 1,49 kr |
| Runde 2, case 1, kjøring 3 | 7 147 | 135 + 190 + 2 112 = 2 437 | 0,10 + 0,13 + 0,62 = 0,85 kr | 0,59 kr | 1,44 kr |
| Runde 2, case 2, kjøring 1 | 1 539 + 2 129 + 3 655 = 7 323 | 147 + 179 + 2 802 = 3 128 | 0,10 + 0,13 + 0,78 = 1,01 kr | 0,73 kr | 1,74 kr |
| Runde 2, case 2, kjøring 2 | 7 323 | 402 + 179 + 1 723 = 2 304 | 0,16 + 0,13 + 0,54 = 0,83 kr | 0,69 kr | 1,52 kr |
| Runde 2, case 2, kjøring 3 | 7 323 | 151 + 179 + 2 705 = 3 035 | 0,10 + 0,13 + 0,76 = 0,99 kr | 0,72 kr | 1,71 kr |
| Runde 2, kriterium 3, kjøring 1 | 1 539 + 2 098 + 3 624 = 7 261 | 147 + 797 + 2 439 = 3 383 | 0,10 + 0,27 + 0,70 = 1,07 kr | 0,74 kr | 1,81 kr |
| Runde 2, kriterium 3, kjøring 2 | 7 261 | 147 + 561 + 2 441 = 3 149 | 0,10 + 0,22 + 0,70 = 1,02 kr | 0,47 kr | 1,49 kr |
| Runde 2, kriterium 3, kjøring 3 | 7 261 | 139 + 603 + 2 281 = 3 023 | 0,10 + 0,22 + 0,66 = 0,98 kr | 0,64 kr | 1,62 kr |

En fullført søknad kostet 0,80–1,07 kr, under målet på 3 kr (NFR-11). Den nye regelen i brev-prompten gir ca. 150 flere tokens inn per brev. De femten kjøringene i story 4.5 kostet ca. 24 kr i alt. Det er mer enn anslaget på ca. 8–9 kr pluss ca. 8 kr for plan B, fordi også kriterium 3 måtte kjøres på nytt i runde 2. Et brev tok 16–25 sekunder, innenfor tidsgrensen på 90 sekunder.

## Retro 4: måling med lange tekster (14. november 2026)

Nettsiden godtar CV og annonse på høyst 15 000 tegn hver (story 4.3.2), men tiden for KI-kallene var bare målt med testdataene, som har ca. 1 200–1 400 tegn per felt. Kallet strømmes ikke, så tidsgrensen på 90 sekunder i `backend/soknad/innstillinger.py` gjelder i praksis hele svaret (retro 4, funn B7, action item 4). Derfor ble skriptet `backend/scripts/lag_testsvar.py` kjørt én gang med ekte KI på en fiktiv CV og en fiktiv annonse som er nesten så lange som grensen.

Modell: `claude-opus-5-5`. Kjøringen ble gjort på commit `88a35a7` (branch `retro-4-rettinger-4`). Promptene i `backend/prompts/` er uendret siden story 4.5 (sist endret i `584ec6f`). Claude skrev CV-en og annonsen: en informatikkstudent, Ingrid Prøvesen, som søker som junior utvikler i Prøvestad Data AS. Personen, firmaene, adressene og telefonnumrene er fiktive. CV-en har 14 622 tegn og annonsen 14 584 tegn, telt med `antall_tegn` (samme telling som nettsiden). Inndataene ligger i `my-project/testkjoringer/retro-4/inndata/case-lang/`, og svarene og loggen i `my-project/testkjoringer/retro-4/kjoring-1/`. Caset har ingen fasit, så innholdet i svarene er ikke vurdert mot kriteriene.

### Kostnad og tid

Tallene er fra loggen i terminalen. Tiden for hvert kall er tiden fra forrige logglinje til logglinjen for kallet. For nøkkelordene er det tiden fra starten av kommandoen (kl. 22:00:09,966), så den tar også med oppstarten av skriptet. Kronene er regnet med 11 kr per dollar.

| Kall | Tokens inn | Tokens ut | Tid | Kroner |
| --- | --- | --- | --- | --- |
| Nøkkelord | 7 389 | 134 | ca. 12,0 s (med oppstarten) | 0,35 kr |
| Gap | 13 866 | 1 440 | 13,9 s | 0,93 kr |
| Brev 1 | 15 392 | 2 908 | 25,0 s | 1,32 kr |
| Brev 2 (det andre brevet) | 15 392 | 2 471 | 21,3 s | 1,22 kr |
| Hele kjøringen | 52 039 | 6 953 | 73 s | 3,82 kr |

En fullført søknad (nøkkelord, gap og ett brev) har 7 389 + 13 866 + 15 392 = 36 647 tokens inn og 134 + 1 440 + 2 908 = 4 482 tokens ut, og kostet 0,35 + 0,93 + 1,32 = 2,60 kr. Det er omtrent tre ganger så mye som med testdataene (0,67–1,07 kr), og over overslaget på omtrent 2 kr i PRD-en. Målet på 3 kr (NFR-11) gjelder en fullført søknad med ett brev, så 2,60 kr holder målet, men med liten margin. Med det andre brevet («Nytt forslag» i Epic 7) blir det 3,82 kr, så en søknad med lange tekster og «Nytt forslag» koster mer enn 3 kr.

**Hva det betyr for grensen på 90 sekunder:** det lengste kallet, det første brevet, tok 25 sekunder. Det er godt innenfor 90 sekunder. I denne ene kjøringen gjorde de lange tekstene særlig de korte kallene tregere: nøkkelordene tok ca. 12 sekunder (med oppstarten av skriptet) og gap-analysen 14 sekunder, mot 2–5 sekunder med testdataene, selv om nøkkelordene bare ga 134 tokens ut. Brevene tok 25 og 21 sekunder, omtrent like lenge som et brev med testdataene (16–47 sekunder). Målingen viser altså ikke at grensen bør endres. Det er bare én måling, og med testdataene varierte et brev mellom 16 og 47 sekunder, så et kall med lange tekster kan også ta lenger tid enn her.

### Merknader om svarene (Kristine vurderer)

Caset har ingen fasit, men disse feilene er sjekket mot CV-en og annonsen:

1. **Gap-analysen sier at «Har erfaring med React eller TypeScript» mangler.** CV-en har «React (grunnleggende)» og «TypeScript (grunnleggende)» under Ferdigheter.
2. **Gap-analysen har laget kravet «Tar sikkerhet og personvern på alvor».** Det står ikke i listene i annonsen. Annonsen skriver i avsnittet «Sikkerhet og personvern» at «vi forventer at du tar det på alvor». CV-en har emnet «Datanettverk og sikkerhet».
3. **Gap-analysen sier at «Tåler at ting endrer seg, og ser på tilbakemeldinger som en hjelp» mangler.** CV-en sier «Jeg tar gjerne imot tilbakemeldinger på koden min» (under «Slik jeg jobber»), men ikke noe om at ting endrer seg.
4. **`brev-2` kaller universell utforming «kravet deres».** I annonsen står «Kjenner til universell utforming og WCAG» under «Det er en fordel om du», ikke under kravene.
5. **`brev-1` skriver «Som studentassistent i Python og i databaser leser jeg andres kode …» i presens.** I CV-en er jobben i databaser bare «Våren 2026». Jobben i Python er «2025–i dag».

**Bestemt 15. november (Kristine):**

- **1–3 godtas**, og prompten for gap-analysen endres ikke:
  - 1: Annonsen spør om *erfaring*, og CV-en har React og TypeScript bare som «grunnleggende» under Ferdigheter, uten at de er brukt noe sted. Docker står også som «grunnleggende», men er brukt i et emneprosjekt, og der svarte gap-analysen «dekker». Gap-analysen fulgte regelen om at kravet hører til `mangler` ved tvil, og var konsekvent.
  - 2: «Vi forventer at du tar det på alvor» er et krav, selv om det står i et avsnitt og ikke i en liste. Et emne med karakter viser ikke helt at studenten tar det på alvor.
  - 3: Kravet har to deler, og CV-en dekker bare den ene. Ved tvil hører kravet til `mangler`.
- **4 og 5 rettes** med to nye regler i `backend/prompts/brev.md`: kall ikke noe et krav når annonsen sier at det er en fordel, og skriv om jobber og verv i nåtid bare når CV-en sier at de pågår, ellers i fortid. Kriteriene for brevet kjøres på nytt med ekte KI etterpå.
- I samme kjøring prøves plan B-regelen (ikke ranger ferdigheter) på en annen CV enn testdataene.
- «Med vennlig hilsen» og navnet skal alltid komme med i brevet. KI-en sender navnet fra CV-en i et eget felt, og nettsiden setter selv inn hilsenen og navnet til slutt, uten et nytt KI-kall. Står det ikke noe navn i CV-en, slutter brevet med «Med vennlig hilsen». De ferdige svarene i testmodus må få det nye feltet.

## Hilsen, navn og to nye regler i brevet (15. november 2026)

Modell: `claude-opus-5-5`. Branch `brev-hilsen-og-regler`. Brev-prompten fikk de to reglene fra «Bestemt 15. november» over, og KI-en gir navnet i et eget felt. Nettsiden setter alltid inn «Med vennlig hilsen» og navnet til slutt. Gap- og nøkkelordpromptene er ikke endret. Hver runde kjørte case 1, case 2 og kriterium 3 tre ganger hver, og den lange CV-en til Ingrid (`case-lang` fra retro 4) én gang. Svarene fra runde 2, kjøring 1, er de ferdige svarene i testmodus. Svarene og loggene ligger i `my-project/testkjoringer/brev-hilsen/runde-1/` og `runde-2/`.

### Runde 1 (kl. 11.01–11.10)

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 1: gap-analysen, case 1 og 2 | Bestått: nøyaktig som fasiten | Bestått | Bestått |
| 14: de viktige nøkkelordene, case 1 og 2 | Bestått | Bestått | Bestått |
| 11: brevet, case 1 og 2 | Bestått | Bestått | Bestått |
| 11: brevet, kriterium 3 | Bestått | Ikke bestått | Bestått |
| Hilsen og riktig navn, alle 18 brevene | Ja | Ja | Ja |

**Brudd (bestemt av Kristine):** «Python er en sentral del av utdanningen min» (kriterium 3, kjøring 2, `brev-2`). CV-en har Python under Ferdigheter og i to prosjekter, men sier ikke at Python er sentralt i studiet. Det er samme type påstand som «Python er språket jeg har jobbet mest med» i story 4.5.

**Godkjent av Kristine som omformuleringer:** «ansvar for kundeservice, kasse og varepåfylling» (CV-en: «Kundeservice, kasse og varepåfylling»), «er ferdig med bachelorgraden våren 2027» (betyr at hun blir ferdig da), «bruker Visual Studio Code» (står under Verktøy), «samarbeide om et større prosjekt» og «kan begynne i august 2027» (datoen står i annonsen).

**Ingrid-CV-en ble ikke kjørt ferdig:** det andre brevet feilte fordi kreditten på API-kontoen var brukt opp. Etter påfyll ble den kjørt i runde 2.

**Plan B:** regelen mot rangering i `backend/prompts/brev.md` ble utvidet. Brevet skal heller ikke si at en ferdighet, et verktøy eller en erfaring er sentral, viktig eller en stor del av studiet, et prosjekt eller en jobb, når CV-en ikke sier det. Regelen har en test i `tests/adaptere/test_ekte_ki.py`.

### Runde 2, etter plan B (kl. 11.22–11.32)

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 1: gap-analysen, case 1 | Bestått: 6 dekket og 4 mangler, nøyaktig som fasiten | Bestått | Bestått |
| 1: gap-analysen, case 2 | Bestått: 5 dekket og 4 mangler, nøyaktig som fasiten | Bestått | Bestått |
| 14: de viktige nøkkelordene, case 1 | Bestått: alle 8 (20 nøkkelord i alt) | Bestått: alle 8 (20 i alt) | Bestått: alle 8 (20 i alt) |
| 14: de viktige nøkkelordene, case 2 | Bestått: alle 6 (17 i alt) | Bestått: alle 6 (17 i alt) | Bestått: alle 6 (16 i alt) |
| Nøkkelordtreffet, case 1 | 10 av 20 = 50 % | 10 av 20 = 50 % | 10 av 20 = 50 % |
| Nøkkelordtreffet, case 2 | 7 av 17 = 41 % | 7 av 17 = 41 % | 7 av 16 = 44 % |
| 11: brevet, case 1 og 2 | Bestått | Bestått | Bestått |
| 3 og 11: brevet, kriterium 3 | Bestått | Bestått | Bestått |
| Hilsen og riktig navn, alle 18 brevene | Ja | Ja | Ja |

Case 2 har nå «lønn» som 17. nøkkelord. Det står ikke i CV-en, så tabellen «Nøkkelord» i `fasit.md` og prosenten er oppdatert til 7 av 17 = 41 %.

**Kriterium 3:** alle seks brevene for Saras CV mot annonsen fra case 2 nevner at firmaet automatiserer med Python, kundekontakt eller opplæringen i regnskapsprogrammene. Alle seks brevene mot annonsen fra case 1 nevner Linux og Flask. Brevene er tydelig ulike.

**Kriterium 11:** ingen brev påstår noe fra sjekklistene, rangerer ferdighetene, kaller en fordel for et krav eller nevner krav som CV-en ikke dekker. Jobber som er ferdige (IT-assistent sommeren 2025, kasserer 2025–2026), står i fortid, og jobber som pågår, i nåtid.

**Godkjent av Kristine som slutninger:** fire brev skriver at Sara møter kunder «hver arbeidsdag» eller «hver vakt» i butikkjobben. CV-en sier ikke hvor ofte, men det følger av at hun jobber med kundeservice i butikken. «Studiet er avsluttet før tiltredelsen i august 2027» stemmer med «fullføres våren 2027». «jeg lærer nye verktøy raskt» står ordrett i CV-en.

**Ingrid-CV-en (`case-lang`), plan B-regelen og merknad 4 og 5:**
- Plan B-regelen holder på en annen CV: CV-en har «I studiet har jeg jobbet mest med webutvikling, databaser og testing», men ingen av brevene tar med rangeringen. Begge beholder «min første faste jobb som utvikler», slik CV-en sier. Det svarer på svakheten ved plan B fra story 4.5.
- Merknad 4 er rettet: begge brevene sier at universell utforming er nevnt som en fordel.
- Merknad 5 er rettet: nåtid bare om det som pågår (kundeservice 2022–i dag, studentassistent i Python 2025–i dag). Jobben i databaser (våren 2026) er ikke nevnt.
- Brevene har 443 og 456 ord. Det er over 250–400 ord i prompten, fordi CV-en og annonsen er svært lange.
- Gap-analysen ga denne gangen bare «Tar sikkerhet og personvern på alvor» under `mangler`. React og TypeScript og «Tåler at ting endrer seg» ble regnet som dekket. Prompten er ikke endret, så det er variasjon fra KI-en mellom kjøringene (merknad 1–3 er godtatt over).

**Merknaden om hilsenen fra story 4.4 og 4.5 er løst:** i alle 38 brevene som ble ferdige, kommer «Med vennlig hilsen» og riktig navn til slutt, én gang.

### Kostnad og tid

Tallene er fra loggen i terminalen. Kronene er regnet med 11 kr per dollar.

| | Hele kjøringen |
| --- | --- |
| Runde 1, case 1 og 2 (kjøring 1, 2, 3) | 3,13 + 2,88 + 2,81 = 8,82 kr |
| Runde 1, kriterium 3 (kjøring 1, 2, 3) | 1,40 + 1,43 + 1,38 = 4,21 kr |
| Runde 1, Ingrid (stoppet etter tre kall) | 0,35 + 0,93 + 1,29 = 2,57 kr |
| Runde 2, case 1 og 2 (kjøring 1, 2, 3) | 3,50 + 3,22 + 3,38 = 10,10 kr |
| Runde 2, kriterium 3 (kjøring 1, 2, 3) | 1,46 + 1,59 + 1,62 = 4,67 kr |
| Runde 2, Ingrid | 0,35 + 0,93 + 1,36 + 1,38 = 4,02 kr |
| Alt | ca. 34 kr |

Brev-prompten er litt lengre, så et brev har nå ca. 4 050–4 120 tokens inn for testdataene, mot 3 590–3 660 før. En fullført søknad med de lange tekstene til Ingrid (nøkkelord, gap og ett brev) kostet 0,35 + 0,93 + 1,36 = 2,64 kr, mot 2,60 kr i retro 4. Med det andre brevet blir det 4,02 kr. Det lengste brevkallet tok ca. 25 sekunder.

## Story 5.2.2: Korrektur og kriterium 12 (15. november 2026)

Modell: `claude-opus-5-5`. Korrektur-prompten (`backend/prompts/korrektur.md`) fra story 5.2.1 er kjørt tre ganger på det egne brevet til Sara i case 1 (`eget-brev.txt`). Hver kjøring gir to brev, `korrektur-1.json` og `korrektur-2.json`. Kjøring 1 (kl. 15.57, story 5.2.1) er de ferdige svarene i testmodus. Kjøring 2 og 3 (kl. 16.33–16.35) ble skrevet rett i `my-project/testkjoringer/5-2/runde-1/` med `uv run python -m scripts.lag_testsvar --case case-1-utvikler --bare-korrektur --ut ../my-project/testkjoringer/5-2/runde-1/kjoring-<n>` fra `backend/`. Prompten er den som ble committet i `35daffe` (story 5.2.1). Kodegjennomgangen av 5.2.1 kom etter kjøring 1 og endret ikke prompten, så alle tre kjøringene brukte den samme prompten.

### Runde 1

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 12: innhold, eksempler og rekkefølge beholdt | Bestått: begge brevene | Bestått: begge brevene | Bestått: begge brevene |
| 4 (svarene): passer med det egne brevet, og minst én setning er endret | Bestått: 11 og 13 endret | Bestått: 12 og 13 endret | Bestått: 11 og 11 endret |
| Fjernede og nye setninger | 1 fjernet («Hei!»), ingen nye | Det samme | Det samme |
| De 17 KI-frasene i den nye teksten | Ingen | Ingen | Ingen |

Hvert svar har 18 oppføringer, én per setning i det egne brevet, og brevene har 214–223 ord. «Ingen nye» betyr at ingen oppføring har tom `gammel`. I alle seks brevene er den lange setningen om butikkjobben delt i to setninger inne i samme `ny` («… dagligvarebutikk. Der har jeg lært …»), slik prompten sier (AD-5). Alle seks brevene består `kontroller()` mot `eget-brev.txt`, altså at alle de gamle setningene satt sammen er hele det egne brevet. Kriterium 4 sier også at den nedlastede fila er uten markeringer. Det sjekker `test_fr30_korrektur_filen_er_lik_brevet_paa_siden` i `backend/tests/web/test_nedlasting.py` fra story 5.2.1. Markeringene på brevsiden kommer i story 5.3.

Resultatet gjelder testbrevet i case 1, som er kort og har en overskrift. Det slår ikke sammen setninger og blander «dere» og «du». Korrektur testes bare med case 1 (bestemt i story 5.1).

**Sjekklisten for Korrektur:** alle seks brevene beholder innholdet i samme rekkefølge: hvorfor Sara søker, ferdig våren 2027 og kan begynne i august, bachelorprosjektet med grupperom (Python, Flask, HTML, CSS, Git, tre på gruppa, JSON-filer), værdata-programmet, IT-assistent sommeren 2025 med pålogging og Linux, butikkjobben og kundeservicen, at hun lærer fort, og fadderordningen. Alle søker hos Testvik Utvikling AS og sier at hun liker å lage nettsider. «Jeg er lidenskapelig opptatt av» og «Takk for at du tok deg tid til å lese søknaden min» er skrevet om. «Hei!» er fjernet, og «midt i blinken», «det var gøy» og «ganske greit stort sett» er borte. Alle bruker «dere» hele veien, og overskriften er «Søknad på stillingen som junior utvikler». Hilsenen og navnet står som Sara skrev dem. Ingen brev legger til noe fra «Sjekkliste for brevet» (SQL, Docker, Scrum, førerkort og annet).

**Regelen for vurderingen (bestemt av Kristine):** det viktigste er at ingenting som ikke står i CV-en, brevet eller annonsen, blir dratt inn i søknaden. Å skrive om dårlig formulerte setninger, også KI-frasene, er det KI-en skal gjøre, og noe som ikke hører hjemme i en søknad (som «det var gøy»), kan fjernes.

**Godkjent av Kristine som omformuleringer:**
- Avslutningen: «Takk for at dere har lest søknaden.», «Jeg håper dere vil vurdere søknaden min.», «Takk for oppmerksomheten.» og «Takk for at dere vurderer søknaden min.»
- «en fast fadder» (alle brevene). Brevet sier «en fadder», og annonsen sier «en fast fadder». Det er en tydeligere kobling til annonsen.
- «Vi bruker Git til versjonskontroll» (alle brevene). CV-en sier «brukte Git til versjonskontroll».
- «imøtekommende» for «blid».
- «I et emneprosjekt har jeg også laget et lite program …» (kjøring 2, `korrektur-1`). Står i CV-en: «Emneprosjekt (2025)».
- «jeg har laget / utviklet en stor del av løsningen» (kjøring 2) for «jeg har laget mye av det».
- «det har stort sett fungert greit / godt / bra» for «det har gått ganske greit stort sett». (Erstattet i retro 5: vage vurderinger fjernes, se «Retro 5: langt eget brev og flyt i Korrektur».) «Godt» og «bra» er litt mer positivt enn det Sara skrev, men ingenting nytt er dratt inn, og teksten skal ikke være mindre formell enn det.
- Små endringer i ordlyd: «jeg ønsker å jobbe» for «jeg vil veldig gjerne jobbe», «fordi jeg fortsatt har mye å lære», «nyttig i møter med kunder» for «nyttig når jeg skal være med i møter med kunder», «stillingen som junior utvikler passer godt» (tittelen fra annonsen) og «hjalp jeg studenter med pålogging» for «hjalp jeg studenter som ikke fikk logget på».

**Godkjent av Kristine som formell nok tone:** kjøring 3 `korrektur-1` beholder «booke» og «gruppa». De står ikke blant de muntlige ordene i sjekklisten, og de andre brevene skriver «reservere» og «gruppen». Flere brev beholder «Jeg lærer nye ting fort og liker å jobbe sammen med andre» uendret.

**Prompten:** kodegjennomgangen av story 5.2.1 fant to uklarheter: prompten sier både «skriv frasen om» og «heller ikke omskrivinger», og eksempelet fjerner «Det var gøy». De er godtatt av Kristine og rettes ikke, fordi alle kjøringene besto, og en endring betyr tre nye kjøringer.

### Kostnad og tid

Tallene er fra loggen i terminalen. Kronene er regnet med 11 kr per dollar.

| | Tokens inn per brev | Tokens ut (`korrektur-1` + `korrektur-2`) | Hele kjøringen |
| --- | --- | --- | --- |
| Kjøring 1 | 4 686 | 2 956 + 2 934 | 0,86 + 0,85 = 1,71 kr |
| Kjøring 2 | 4 686 | 3 080 + 3 103 | 0,88 + 0,89 = 1,77 kr |
| Kjøring 3 | 4 686 | 3 014 + 3 030 | 0,87 + 0,87 = 1,74 kr |
| Alt | | | ca. 5,2 kr |

Et brev i Korrektur koster ca. 0,85–0,89 kr. Svaret er ca. 3 000 tokens ut, fordi det har hver setning både gammel og ny. En fullført søknad i Korrektur med testdataene koster da ca. 0,10 + 0,17 + 0,87 = 1,14 kr, under målet på 3 kr (NFR-11). Nøkkelord og gap er tallene for case 1 fra story 4.4, runde 2. Med lange tekster blir det mer: nøkkelord og gap kostet 0,35 + 0,93 kr med Ingrid-CV-en, og et langt eget brev gir flere tokens ut, fordi svaret har hver setning to ganger. Et langt eget brev er ikke målt ennå (et åpent punkt fra kodegjennomgangen av story 5.2.1). Det gikk ca. 22 sekunder mellom de to kallene i hver kjøring i loggen. Loggen viser bare når et kall er ferdig, så det er ikke en målt tid for hvert kall.

## Retro 5: langt eget brev og flyt i Korrektur (15. november 2026)

Modell: `claude-opus-5-5`. Branch `retro-5-rettinger-2` (runde B av rettingene etter retro 5). Korrektur-prompten (`backend/prompts/korrektur.md`) fikk to nye regler: KI-en kan bruke bindeord og slå sammen korte setninger i samme avsnitt, så brevet leses naturlig (retro 5, punkt 4), og de gamle setningene kopieres nøyaktig, med store og små bokstaver og tegnsetting (fordi kontrollen er streng fra runde A). Etter runde 1 kom en tredje regel (plan B, se under). Svarene og loggene ligger i `my-project/testkjoringer/retro-5/`.

### Målingen med et langt eget brev (kl. 21.15–21.19)

Nettsiden godtok et eget brev på 15 000 tegn (story 5.1), men svaret i Korrektur har hver setning to ganger, og et langt brev var ikke målt (retro 5, punkt 3). Claude skrev et fiktivt eget brev på 14 585 tegn (telt med `antall_tegn`) fra Ingrid Prøvesen, til CV-en og annonsen fra retro 4. Brevet har vanlige feil: «Hei!», muntlige ord, manglende komma, «du» og «dere» om hverandre og tre av KI-frasene. Inndataene ligger i `retro-5/inndata/case-lang/`.

Ett `korrektur`-kall ble kjørt med den nye prompten (commit `73f6ecd`), med `max_tokens` 48 000 og tidsgrense 600 s satt bare i målingen, ikke i koden. Da viser målingen hvor stort og tregt svaret faktisk blir. Svaret og tallene ligger i `retro-5/maling/`.

| | Målt | Grensen i koden |
| --- | --- | --- |
| Tokens inn | 22 595 | |
| Tokens ut | 28 686 | 16 000 (`KI_MAKS_TOKENS`) |
| Tid | 190 s | 90 s (`KI_TIDSGRENSE`) |
| `stop_reason` | `end_turn` | |
| `kontroller()` | Bestått | |
| Pris | ca. 7,31 kr | Målet for en hel søknad er under 3 kr (NFR-11) |

Med grensene i koden ville en bruker med et så langt brev fått KI-feilboksen hver gang, og hvert «Prøv på nytt» ville feilet likt. Ca. 11 000 av tokenene ut er selve svaret (35 804 tegn JSON med brevet to ganger), og resten er tenkingen før svaret. Svaret har 154 oppføringer, 31 sammenslåtte setninger, «Hei!» fjernet og ingen nye setninger. Innholdet er ikke vurdert mot noen fasit, fordi caset ikke har noen.

**Bestemt av Kristine:** brevfeltet i Korrektur godtar høyst 5 000 tegn (`MAKS_TEGN_EGET_BREV` i `backend/soknad/innstillinger.py`), med feilmeldingen «Ditt søknadsbrev: Teksten er for lang. Den kan være på høyst 5 000 tegn.». CV og annonse godtar fortsatt 15 000 tegn, og 16 000 tokens og 90 s er beholdt. Regnet ut fra målingen og testbrevet (ca. 2 tokens ut per tegn og ca. 150 tokens i sekundet) gir 5 000 tegn ca. 10 000 tokens og ca. 70–75 s. Et brev på 5 000 tegn koster da ca. 2,5 kr med CV og annonse som testdataene, og en hel søknad i Korrektur ca. 2,8 kr. Med CV og annonse nær 15 000 tegn koster selve brevet ca. 3,1 kr, og en hel søknad ca. 4,4 kr (med nøkkelord og gap fra retro 4), altså over målet på 3 kr (NFR-11). Det er det samme som for Full generering med «Nytt forslag» og lange tekster (TO DO, epic 7). Et søknadsbrev på én side er ca. 2 500–3 500 tegn. Valget mot dette var høyere `max_tokens` og tidsgrense for Korrektur, men da kunne brukeren ventet i over 3 minutter, og ett brev ville kostet over 7 kr. En tredje mulighet, mindre tenking for Korrektur (`KI_INNSATS`), ble ikke lagt fram. Tenkingen er den største delen av svaret, men mindre tenking kan gi dårligere brev og må måles og sjekkes mot kriteriene på nytt. 5 000 tegn er regnet ut, ikke målt, og marginen til 90 s er ca. 15–20 s.

### Runde 1 (kl. 21.26–21.29)

Kjøringene ble skrevet i `retro-5/runde-1/kjoring-<n>/` med `uv run python -m scripts.lag_testsvar --case case-1-utvikler --bare-korrektur --ut ../my-project/testkjoringer/retro-5/runde-1/kjoring-<n>` fra `backend/`.

Alle seks brevene besto `kontroller()`, kriterium 4 på datanivå (12 eller 13 endrede setninger) og sjekklisten for Korrektur, og brevene hadde bindeord og 1–2 sammenslåtte setninger. Kristine leste brevene som vanlige brev og godtok ikke «det har stort sett gått / fungert greit / godt / bra»: ingen skriver det i en søknad. Det erstatter godkjenningen av den setningen i story 5.2.2. Bindeordene «derfor» og «samtidig» i runde 1 ble godtatt.

**Plan B:** prompten fikk en regel om at vage vurderinger som ikke sier noe konkret («det har gått ganske greit stort sett», «det var gøy» og lignende), fjernes og ikke skrives om til en annen vag vurdering. Alle tre kjøringene ble kjørt på nytt.

### Runde 2, etter plan B (kl. 21.46–21.49)

Skrevet i `retro-5/runde-2/kjoring-<n>/` på samme måte. Kjøring 1 er de ferdige svarene i testmodus (`backend/testdata/case-1-utvikler/ki-svar/`).

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 12: innhold, eksempler og rekkefølge beholdt | Bestått: begge brevene | Bestått: begge brevene | Bestått: begge brevene |
| 4 (svarene): passer med det egne brevet, og minst én setning er endret | Bestått: 12 og 12 endret | Bestått: 12 og 12 endret | Bestått: 13 og 12 endret |
| Sammenslåtte, fjernede og nye setninger | 2 og 2 sammenslått, 1 fjernet («Hei!»), ingen nye | 1 og 2 sammenslått, ellers det samme | 2 og 2 sammenslått, ellers det samme |
| De 17 KI-frasene og vage vurderinger i den nye teksten | Ingen | Ingen | Ingen |

**Sjekklisten for Korrektur:** alle seks brevene beholder innholdet i samme rekkefølge, som i story 5.2.2, og legger ikke til noe fra «Sjekkliste for brevet». «Vi bruker Git og det har gått ganske greit stort sett.» er blitt «Vi bruker Git til versjonskontroll», og i alle seks brevene er den satt sammen med «Dataene lagres i JSON-filer.». «Det var gøy» om værdata-programmet er fjernet i alle seks. Alle bruker «dere» hele veien, overskriften er «Søknad på stillingen som junior utvikler», og hilsenen og navnet står som Sara skrev dem.

**Godkjent av Kristine:** runde 2 består kriterium 12 og leses naturlig. Avslutningene «Takk for at dere har lest søknaden min.», «Takk for at dere leste søknaden min.» og «Jeg takker for at dere vurderer søknaden min.» er godtatt. «Takk for at dere vurderer søknaden min.» og «Takk for oppmerksomheten.» var godkjent i story 5.2.2.

**Kjent svakt punkt, godtatt av Kristine:** i kjøring 3, `korrektur-2`, står det «Jeg lærer nye ting fort og liker å jobbe sammen med andre. Derfor setter jeg pris på at dere tilbyr en fast fadder de første månedene, siden jeg fortsatt har mye å lære.». «Derfor» er feil her, fordi det første ikke er grunnen til det andre, og det bryter regelen i prompten. Innholdet er det samme, så kriterium 12 er bestått. Brevet brukes ikke i testmodus, og en ny plan B ble ikke kjørt.

### Kostnad og tid

Tallene er fra loggen i terminalen. Kronene er regnet med 11 kr per dollar.

| | Tokens inn per brev | Tokens ut (`korrektur-1` + `korrektur-2`) | Hele kjøringen |
| --- | --- | --- | --- |
| Målingen (ett brev) | 22 595 | 28 686 | 7,31 kr |
| Runde 1, kjøring 1 | 4 923 | 2 785 + 3 273 | 0,83 + 0,94 = 1,77 kr |
| Runde 1, kjøring 2 | 4 923 | 3 203 + 3 187 | 0,92 + 0,92 = 1,84 kr |
| Runde 1, kjøring 3 | 4 923 | 3 166 + 3 136 | 0,91 + 0,91 = 1,82 kr |
| Runde 2, kjøring 1 | 5 108 | 3 005 + 2 969 | 0,89 + 0,88 = 1,77 kr |
| Runde 2, kjøring 2 | 5 108 | 2 841 + 2 920 | 0,85 + 0,87 = 1,72 kr |
| Runde 2, kjøring 3 | 5 108 | 3 019 + 2 949 | 0,89 + 0,87 = 1,76 kr |
| Alt | | | ca. 18,0 kr |

Prompten er litt lengre, så et brev har nå ca. 5 100 tokens inn med testdataene, mot 4 686 i story 5.2.2. Et brev i Korrektur koster fortsatt ca. 0,85–0,94 kr med testbrevet, og en fullført søknad i Korrektur med testdataene ca. 1,15 kr. Det gikk ca. 24 sekunder mellom de to kallene i hver kjøring.

## Story 6.1: PDF fra Word og tabellprøven (16. november 2026)

### Unicode i PDF-ene fra Word

PDF-ene i testdataene (`cv.pdf`, `annonse.pdf` og `eget-brev.pdf` i case 1, `cv.pdf` og `annonse.pdf` i case 2) er lagret fra Word med `backend/scripts/lag_testpdf.ps1`. Før normaliseringen i `pdf_inn.py` ble teksten fra pypdf målt: alle fem er NFC (og NFKC), og ingen har myk bindestrek (U+00AD), U+200B eller andre usynlige tegn. Teksten er lik `.txt`-fila etter vasken. Normaliseringen i `pdf_inn.py` er der for PDF-er fra andre programmer (Canva, Mac), som ikke er målt.

### Kriterium 5

Testes automatisk i `backend/tests/test_testdata.py`: for hvert testcase gir `cv.pdf` og `cv.txt` samme nøkkelordtreff med `nokkelord.json`, og PDF og `.txt` gir samme testcase, også blandet og med brevet i Korrektur. Bestått.

### Tabellprøven

En fiktiv CV (Tobias Tabellsen) med ferdighetene i en tabell med tre kolonner (ferdighet, nivå, brukt i) ble laget med python-docx og lagret som PDF i Word. Skriptet, PDF-en og teksten pypdf leste, ligger i `my-project/testkjoringer/6-1/` (`lag_tabellprove.py`, `tabell-cv.pdf`, `tabell-cv-lest.txt`).

| Dato | Hva som ble lest | Resultat |
| --- | --- | --- |
| 16. november 2026 | All teksten kom med, i riktig rekkefølge: overskriften «Ferdigheter», så tabellen rad for rad med cellene fra venstre mot høyre («Python God Bacheloroppgave og deltidsjobb»), så «Erfaring». En celle med tekst på to linjer i PDF-en ble to linjer i teksten, men rekkefølgen er riktig, og telleregelen ser bort fra linjeskift. | Bestått. Tabeller fra Word blir ikke en kjent begrensning, og settes ikke på kuttlisten |
