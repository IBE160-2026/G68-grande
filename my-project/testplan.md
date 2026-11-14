# Testplan

Testplanen viser resultatet for suksesskriteriene som ikke testes automatisk (NFR-12). Den fylles ut underveis, og gjøres ferdig i Epic 8 (hele flyten og README fra en ny kopi av repoet).

## Slik testes kriteriene med ekte KI

Kriterium 1, 3, 11, 12 og 14 testes med ekte KI (Claude), ikke i testmodus (PRD del 5). De kjøres tre ganger per testcase, og alle tre må bestå. Feiler én kjøring, forbedres prompten én gang, og alle tre kjøres på nytt (plan B). Feiler det fortsatt, står kriteriet her som ikke bestått, med hva som gikk galt.

Kjøringene gjøres med skriptet `backend/scripts/lag_testsvar.py` (se README). Kjøring 1 skriver de ferdige svarene i testmodus (`backend/testdata/<case>/ki-svar/`). Kjøring 2 og 3 skrives rett i `my-project/testkjoringer/`. Svarene og terminalloggen (tokens og pris) fra alle kjøringene ligger i `my-project/testkjoringer/<story>/<runde>/kjoring-<n>/`, så de kan sjekkes i etterkant, også etter at svarene i testmodus er laget på nytt.

| Kriterium | Hva | Hvordan det sjekkes | Status |
| --- | --- | --- | --- |
| 1 | Gap-analysen finner alle krav som mangler, og ingen dekkede krav står under «mangler» | `gap.json` mot tabellen «Krav» i `fasit.md` | Bestått for case 1 i begge rundene (story 4.4). Case 2 testes i story 4.5 |
| 3 | Samme CV med to annonser gir brev med krav som er spesifikke for hver annonse | Brevene for CV-en i case 1 mot annonsen i case 1 og case 2 | Testes i story 4.5 (trenger case 2) |
| 11 | Brevet nevner ingen erfaring, utdanning eller ferdigheter som ikke står i CV-en | `brev-1.json` mot CV-en og «Sjekkliste for brevet» i `fasit.md` | Case 1: ikke bestått i runde 1, bestått i runde 2 etter plan B (story 4.4). Case 2 testes i story 4.5 |
| 12 | Korrektur beholder brukerens innhold, eksempler og rekkefølge | Korrektur-svarene mot det opprinnelige brevet | Testes i Epic 5 (trenger Korrektur) |
| 14 | Nøkkelordlisten har alle nøkkelordene fasiten markerer som viktige | `nokkelord.json` mot «Viktige nøkkelord» i `fasit.md` | Bestått for case 1 i begge rundene (story 4.4). Case 2 testes i story 4.5 |

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
