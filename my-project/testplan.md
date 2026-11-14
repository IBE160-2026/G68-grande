# Testplan

Testplanen viser resultatet for suksesskriteriene som ikke testes automatisk (NFR-12). Den fylles ut underveis, og gjøres ferdig i Epic 8 (hele flyten og README fra en ny kopi av repoet).

## Slik testes kriteriene med ekte KI

Kriterium 1, 3, 11, 12 og 14 testes med ekte KI (Claude), ikke i testmodus (PRD del 5). De kjøres tre ganger per testcase, og alle tre må bestå. Feiler én kjøring, forbedres prompten én gang, og alle tre kjøres på nytt (plan B). Feiler det fortsatt, står kriteriet her som ikke bestått, med hva som gikk galt.

Kjøringene gjøres med skriptet `backend/scripts/lag_testsvar.py` (se README). Kjøring 1 skriver de ferdige svarene i testmodus (`backend/testdata/<case>/ki-svar/`). Kjøring 2 og 3 skrives rett i `my-project/testkjoringer/`. Svarene og terminalloggen (tokens og pris) fra alle kjøringene ligger i `my-project/testkjoringer/<story>/<runde>/kjoring-<n>/`, så de kan sjekkes i etterkant, også etter at svarene i testmodus er laget på nytt.

| Kriterium | Hva | Hvordan det sjekkes | Status |
| --- | --- | --- | --- |
| 1 | Gap-analysen finner alle krav som mangler, og ingen dekkede krav står under «mangler» | `gap.json` mot tabellen «Krav» i `fasit.md` | Bestått for case 1 i begge rundene (story 4.4). Bestått for case 2 i begge rundene, og for case 1 på nytt i runde 2 (story 4.5) |
| 3 | Samme CV med to annonser gir brev med krav som er spesifikke for hver annonse | Brevene for CV-en i case 1 mot annonsen i case 1 og case 2 | Bestått i begge rundene: brevene nevner krav som er spesifikke for hver annonse. Brevene i runde 1 hadde to påstander som ikke står i CV-en (et brudd på kriterium 11), så alt ble kjørt på nytt etter plan B, og runde 2 besto også kriterium 11 (story 4.5) |
| 11 | Brevet nevner ingen erfaring, utdanning eller ferdigheter som ikke står i CV-en | `brev-1.json` mot CV-en og «Sjekkliste for brevet» i `fasit.md` | Case 1: ikke bestått i runde 1, bestått i runde 2 etter plan B (story 4.4), og bestått igjen i runde 2 i story 4.5 (runde 1 ble ikke kjørt for case 1). Case 2: bestått i begge rundene (story 4.5). CV-en fra case 1 mot annonsen fra case 2 (kriterium 3): ikke bestått i runde 1, bestått i runde 2 etter plan B (story 4.5). Slutningene under «Story 4.5» er godkjent av Kristine |
| 12 | Korrektur beholder brukerens innhold, eksempler og rekkefølge | Korrektur-svarene mot det opprinnelige brevet | Testes i Epic 5 (trenger Korrektur) |
| 14 | Nøkkelordlisten har alle nøkkelordene fasiten markerer som viktige | `nokkelord.json` mot «Viktige nøkkelord» i `fasit.md` | Bestått for case 1 i begge rundene (story 4.4) og i runde 2 i story 4.5. Bestått for case 2 i begge rundene (story 4.5) |

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

**Merknad om formen (ikke kriterium 11):** `brev-1` i kjøring 3 slutter uten «Med vennlig hilsen» og navnet, selv om prompten ber om det. De andre fem brevene har det, også `brev-1` i testmodus. Ingen automatisk sjekk fanger dette for brev fra ekte KI.

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
