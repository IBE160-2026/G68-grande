# Testplan

Testplanen viser resultatet for alle de 14 suksesskriteriene i PRD-en (del 5) og for testene som gjøres for hånd (NFR-12). Kriteriene som har automatiske tester, viser til testfila. De andre har dato, hva som ble gjort, og bestått eller ikke bestått. Testplanen viser også hele flyten prøvd for hånd i begge modusene, sjekkene av tilgjengelighet og skjermbredder, skriptene som bare prøves for hånd, tokens og kroner per søknad, og prøvene av README fra en ny kopi av repoet. Første prøve ble gjort i story 8.2.1. Kriterium 13 ble gjort i story 8.2.2, og andre prøve fra en ny kopi kommer rett før levering.

## Oversikt over suksesskriteriene

Testfilene ligger i `backend/tests/` og kjøres med `uv run pytest` fra `backend/` (se README). Hver test nevner FR- eller NFR-nummeret, og noen nevner også kriteriet.

| Kriterium | Hva | Hvordan | Resultat |
| --- | --- | --- | --- |
| 1 | Gap-analysen viser alle krav som mangler, og ingen dekkede krav under «mangler» | For hånd med ekte KI, tre kjøringer per testcase | Bestått 14. og 15. november 2026 (se «Slik testes kriteriene med ekte KI» under) |
| 2 | Nøkkelordtreffet gir nøyaktig prosenten i fasiten når listen er fast | Automatisk: [test_testdata.py](../backend/tests/test_testdata.py) (`test_fr17_fasiten_gir_samme_treff_og_prosent_som_telleregelen`) og [test_resultat.py](../backend/tests/web/test_resultat.py) (`test_fr17_kriterium_2_…` for case 1 og 2) | Bestått |
| 3 | Samme CV med to annonser gir brev med krav som er spesifikke for hver annonse | For hånd med ekte KI, tre kjøringer | Bestått 14. og 15. november 2026 (se «Slik testes kriteriene med ekte KI») |
| 4 | Korrektur viser minst én markert endring, og den nedlastede fila har ingen markeringer | Automatisk: [test_ki_svar.py](../backend/tests/kjerne/test_ki_svar.py) (`test_fr23_visningen_av_de_ekte_testsvarene`), [test_nedlasting.py](../backend/tests/web/test_nedlasting.py) (`test_fr30_korrektur_…`) og [test_fil_ut.py](../backend/tests/adaptere/test_fil_ut.py) (`test_fr30_filen_har_ingen_markeringer`). Svarene fra ekte KI er sjekket i «Story 5.2.2» og «Retro 5» | Bestått |
| 5 | PDF og innlimt tekst gir samme treff, og både .docx og PDF kan åpnes | Treffet automatisk: [test_testdata.py](../backend/tests/test_testdata.py) (`test_fr8_pdf_og_txt_gir_samme_nokkelordtreff`, `test_fr34_pdf_ene_gir_samme_testcase_som_txt`), [test_pdf_inn.py](../backend/tests/adaptere/test_pdf_inn.py) og [test_innlegging.py](../backend/tests/web/test_innlegging.py). At filene kan åpnes: for hånd i «Hele flyten for hånd» | Treffet: bestått. Åpne filene: bestått 22. november 2026 |
| 6 | En ny bruker kan registrere seg, feil passord gir ikke tilgang, og testbrukeren fra README virker | Automatisk: [test_registrering.py](../backend/tests/web/test_registrering.py) (`test_fr1_…`, `test_fr2_testbrukeren_finnes_fra_for`) og [test_innlogging.py](../backend/tests/web/test_innlogging.py) (`test_fr3_feil_passord_eller_ukjent_epost_gir_skjemafeil`). Testbrukeren er også prøvd i «Prøven fra en ny kopi» | Bestått |
| 7 | Nettsiden kan kjøres lokalt etter README i testmodus uten API-nøkkel | For hånd: «Prøven fra en ny kopi» | Første prøve bestått 21. november 2026. Andre prøve kommer i 8.2.2 |
| 8 | Samme annonse og CV kjørt to ganger i samme søknad gir samme nøkkelordtreff | Automatisk: [test_resultat.py](../backend/tests/web/test_resultat.py) (`test_fr15_kriterium_8_samme_treff_etter_tilbake`) og [test_gjenbruk_nokkelord.py](../backend/tests/web/test_gjenbruk_nokkelord.py) | Bestått |
| 9 | I vanlig modus kommer brukeren ikke videre uten samtykke | Automatisk: [test_samtykke.py](../backend/tests/web/test_samtykke.py) (`test_fr36_begynn_uten_samtykke_gir_feilen_ved_boksen`) | Bestått |
| 10 | Feil filtype, tomme felt og en uleselig PDF gir riktig feilmelding | Automatisk: [test_innlegging.py](../backend/tests/web/test_innlegging.py) (`test_fr9_…`, `test_fr10_…`, `test_fr11_…`), [test_inndata.py](../backend/tests/kjerne/test_inndata.py), og [test_innlogging.py](../backend/tests/web/test_innlogging.py) og [test_registrering.py](../backend/tests/web/test_registrering.py) (`test_fr4_…`) | Bestått |
| 11 | Brevet nevner ingenting som ikke står i CV-en | For hånd med ekte KI, tre kjøringer per testcase | Bestått etter plan B 14. og 15. november 2026 (se «Slik testes kriteriene med ekte KI») |
| 12 | Korrektur beholder innholdet, eksemplene og rekkefølgen | For hånd med ekte KI, tre kjøringer | Bestått 15. november 2026 (se «Slik testes kriteriene med ekte KI») |
| 13 | En person som ikke kjenner prosjektet, forklarer resultatsiden med egne ord | For hånd: «Kriterium 13» | Bestått 22. november 2026, med en merknad (se «Kriterium 13») |
| 14 | Nøkkelordlisten har alle de viktige nøkkelordene i fasiten | For hånd med ekte KI, tre kjøringer per testcase. Svarene i testmodus sjekkes også automatisk i [test_testdata.py](../backend/tests/test_testdata.py) (`test_fr15_nokkelordlisten_har_alle_de_viktige`) | Bestått 14. og 15. november 2026 (se «Slik testes kriteriene med ekte KI») |

Kriterium 1, 3, 11, 12 og 14 er ikke kjørt på nytt i story 8.2.1. De er bestått, og promptene i `backend/prompts/` er ikke endret siden.

## Kostnad per søknad

Tallene er samlet fra «Kostnad og tid» i hver runde under. Kronene er regnet med 11 kr per dollar og prisene for `claude-opus-5-5` (4 dollar per million tokens inn og 20 dollar per million tokens ut). En fullført søknad i Full generering er nøkkelord, gap og ett brev. I Korrektur er det nøkkelord, gap og ett forbedret brev. Målet er under 3 kr (NFR-11).

| Søknad | Tokens inn | Tokens ut | Kroner | Hvor |
| --- | --- | --- | --- | --- |
| Full generering, testdataene (case 1 og 2, også kriterium 3) | 6 690–7 323 | 1 688–3 383 | 0,67–1,07 kr | Story 4.4 og 4.5 |
| Full generering, CV og annonse nær 15 000 tegn | 36 647 | 4 482 | 2,60 kr (2,64 kr etter de nye reglene i brevet) | Retro 4 og «Hilsen, navn og to nye regler i brevet» |
| Full generering med «Nytt forslag», CV og annonse nær 15 000 tegn | 52 039 | 6 953 | 3,82 kr (4,02 kr etter de nye reglene) | Samme. Over målet, godtatt 17. november |
| Korrektur, testdataene (case 1) | ca. 8 670 (5 108 for brevet) | ca. 3 300–3 500 | ca. 1,15 kr | Retro 5, runde 2, med nøkkelord og gap fra story 4.4 |
| Korrektur, eget brev på 5 000 tegn | | | ca. 2,8 kr, eller ca. 4,4 kr med CV og annonse nær 15 000 tegn | Regnet ut i retro 5 |
| Korrektur, bare brevet: eget brev på 4 954 tegn, CV og annonse nær 15 000 tegn | 18 521 | 10 000 | 3,02 kr (0,2741 dollar) | Målt 22. november, «Måling av grensen på 5 000 tegn». Med nøkkelord og gap fra retro 4 blir en hel søknad ca. 4,3 kr, over målet, som regnet ut |
| Full generering, case 1, i nettleseren i story 8.2.1 (22. november 2026) | 7 635 (1 503 nøkkelord, 2 069 gap, 4 063 brev) | 2 377 (138, 190, 2 049) | 0,86 kr (0,0781 dollar) | «Hele flyten for hånd» |

Med testdataene koster en fullført søknad ca. 0,7–1,2 kr i begge modusene. Med svært lange tekster holder Full generering med ett brev målet, men med liten margin. Med «Nytt forslag», eller i Korrektur med lange tekster, blir det mer enn 3 kr.

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

**Bestemt av Kristine:** brevfeltet i Korrektur godtar høyst 5 000 tegn (`MAKS_TEGN_EGET_BREV` i `backend/soknad/innstillinger.py`), med feilmeldingen «Ditt søknadsbrev: Teksten er for lang. Den kan være på høyst 5 000 tegn.». CV og annonse godtar fortsatt 15 000 tegn, og 16 000 tokens og 90 s er beholdt. Regnet ut fra målingen og testbrevet (ca. 2 tokens ut per tegn og ca. 150 tokens i sekundet) gir 5 000 tegn ca. 10 000 tokens og ca. 70–75 s. Et brev på 5 000 tegn koster da ca. 2,5 kr med CV og annonse som testdataene, og en hel søknad i Korrektur ca. 2,8 kr. Med CV og annonse nær 15 000 tegn koster selve brevet ca. 3,1 kr, og en hel søknad ca. 4,4 kr (med nøkkelord og gap fra retro 4), altså over målet på 3 kr (NFR-11). Det er det samme som for Full generering med «Nytt forslag» og lange tekster (TO DO, epic 7). Et søknadsbrev på én side er ca. 2 500–3 500 tegn. Valget mot dette var høyere `max_tokens` og tidsgrense for Korrektur, men da kunne brukeren ventet i over 3 minutter, og ett brev ville kostet over 7 kr. En tredje mulighet, mindre tenking for Korrektur (`KI_INNSATS`), ble ikke lagt fram. Tenkingen er den største delen av svaret, men mindre tenking kan gi dårligere brev og må måles og sjekkes mot kriteriene på nytt. 5 000 tegn er regnet ut, ikke målt, og marginen til 90 s er ca. 15–20 s. Grensen ble målt 22. november 2026, se «Måling av grensen på 5 000 tegn» under.

### Måling av grensen på 5 000 tegn (22. november 2026)

Målt fordi grensen bare var regnet ut (åpent punkt fra gjennomgangen av runde B, godkjent av Kristine, ca. 3 kr). Skriptet [maal_korrektur.py](testkjoringer/8-2/maling-5000/maal_korrektur.py) korter ned brevet fra Ingrid Prøvesen til [eget-brev-5000.txt](testkjoringer/8-2/maling-5000/eget-brev-5000.txt) (4 954 tegn): overskriften, «Hei!», de første avsnittene og avslutningen med hilsenen, kuttet ved hele avsnitt og setninger. CV-en og annonsen er de nær 15 000 tegn fra retro 4, altså det verste tilfellet. Ett `korrektur`-kall gikk gjennom `EkteKI` med de samme grensene som nettsiden (90 s og 16 000 tokens) og prompten slik den er nå, men uten nytt forsøk, så et tidsavbrudd ikke ble skjult. Svaret og tallene ligger i [korrektur.json](testkjoringer/8-2/maling-5000/korrektur.json) og [resultat.json](testkjoringer/8-2/maling-5000/resultat.json).

| | Målt | Regnet ut i retro 5 | Grensen i koden |
| --- | --- | --- | --- |
| Tokens inn | 18 521 | | |
| Tokens ut | 10 000 | ca. 10 000 | 16 000 (`KI_MAKS_TOKENS`) |
| Tid | 68,6 s | ca. 70–75 s | 90 s (`KI_TIDSGRENSE`) |
| `stop_reason` | `end_turn` | | |
| `kontroller()` | Bestått | | |
| Pris | ca. 3,02 kr | ca. 3,1 kr | |

Bestått: et brev på 5 000 tegn går gjennom i Korrektur med grensene i koden, også med de lengste CV-ene og annonsene. Marginen er ca. 21 s til tidsgrensen og ca. 6 000 tokens til `KI_MAKS_TOKENS`. Målingen er én kjøring, så tiden kan variere. Innholdet i brevet er ikke vurdert mot noen fasit, fordi caset ikke har noen.

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

Kriterium 5 krever også at både .docx og PDF kan åpnes. Det prøves for hånd under «Hele flyten for hånd».

### Tabellprøven

En fiktiv CV (Tobias Tabellsen) med ferdighetene i en tabell med tre kolonner (ferdighet, nivå, brukt i) ble laget med python-docx og lagret som PDF i Word. Skriptet, PDF-en og teksten pypdf leste, ligger i `my-project/testkjoringer/6-1/` (`lag_tabellprove.py`, `tabell-cv.pdf`, `tabell-cv-lest.txt`).

| Dato | Hva som ble lest | Resultat |
| --- | --- | --- |
| 16. november 2026 | All teksten kom med, i riktig rekkefølge: overskriften «Ferdigheter», så tabellen rad for rad med cellene fra venstre mot høyre («Python God Bacheloroppgave og deltidsjobb»), så «Erfaring». En celle med tekst på to linjer i PDF-en ble to linjer i teksten, men rekkefølgen er riktig, og telleregelen ser bort fra linjeskift. | Bestått. Tabeller fra Word blir ikke en kjent begrensning, og settes ikke på kuttlisten |

## Story 6.2: Feilmeldinger for filer (16. november 2026)

### Grensen på 50 bokstaver

Bokstavene (`isalpha`) i teksten pypdf leser, telt med `les_pdf`. `skannet.pdf` (CV-en fra case 1 som et bilde uten tekst) og `feil-type.docx` ligger i `backend/testdata/feil/` og lages med `backend/scripts/lag_feilfiler.ps1`.

| Fil | Bokstaver |
| --- | --- |
| `feil/skannet.pdf` | 0 |
| `case-1-utvikler/annonse.pdf` | 896 |
| `case-1-utvikler/cv.pdf` | 993 |
| `case-1-utvikler/eget-brev.pdf` | 952 |
| `case-2-okonomi/annonse.pdf` | 952 |
| `case-2-okonomi/cv.pdf` | 1 038 |

Grensen på 50 skiller dem godt, så `MIN_BOKSTAVER_PDF` i `innstillinger.py` er beholdt. Testes automatisk i `backend/tests/adaptere/test_pdf_inn.py`.

### Over 16 MB med den ekte utviklingsserveren

`flask --app soknad run`, innlogget med testbrukeren, og `POST /innlegging` med en fil på 17 MB fra Python `urllib`. Svaret var status 413 med innleggingssiden og «Filene er for store. Hver fil kan være på høyst 5 MB.» i feilboksen, og forbindelsen ble ikke brutt. Prøvd i nettleseren av Kristine (PR #43): en fil på 17 MB ga siden med feilboksen.

## Prøven fra en ny kopi

README er prøvd i en tom mappe uten `.env` og andre lokale filer. Planen sa at første prøve skulle bruke README slik den var etter Epic 1–6, før story 8.1. Story 8.1 ble ferdig først, så første prøve bruker README slik den er 21. november 2026 (commit `8e13bf1` på main), før kodestopp. Hensikten er den samme: å finne feil i README tidlig. Loggen fra terminalen ligger i [ny-kopi-1.txt](testkjoringer/8-2/ny-kopi-1.txt), og skriptet for innloggingen og søknaden i [http_prove.py](testkjoringer/8-2/http_prove.py).

| Prøve | Dato | Hva som ble gjort | Resultat |
| --- | --- | --- | --- |
| 1 | 21. november 2026 | Claude i terminalen (Git Bash på Windows 11). `git clone` fra GitHub til en ny, tom mappe, uten `.env` og uten `ANTHROPIC_API_KEY`. Så README steg for steg: `cd backend`, `uv sync`, `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` og `uv run flask --app soknad run`. Mens nettsiden kjørte: innlogging med testbrukeren fra README, og en søknad i Full generering i testmodus med CV og annonse fra case 1, over HTTP, til og med nedlasting som Word og PDF og «Logg ut» | Bestått. Databasen og testbrukeren ble laget ved første oppstart, testbrukeren logget inn, og startsiden viste «Mangler API-nøkkel, se README». Alle 1 393 testene besto, og ruff fant ingen feil. Resultatsiden ga 10 av 20 = 50 %, som i `fasit.md`, brevet hadde «Med vennlig hilsen», og begge filene ble lastet ned. Klokketiden fra kopien til første søknad var ca. 4 minutter, men `uv run pytest` kjørte samtidig med nettsiden og søknaden over HTTP, så tiden er ikke stegene etter hverandre. Hvert steg for seg: `git clone` og `uv sync` ca. 15 sekunder, `uv run pytest` 179 sekunder (ca. 3 minutter), og oppstarten, innloggingen og søknaden over HTTP noen sekunder. Etter hverandre blir det ca. 3,5 minutter med skriptet, og lenger når søknaden gjøres for hånd i nettleseren. uv var installert fra før, og Python og pakkene lå i mellomlageret til uv, så for en sensor som begynner helt fra bunnen, tar det lenger tid. Ingen feil i README |
| 2 | | Rett før levering | Kommer i 8.2.2 |

**Merknad til README:** README sa «Start nettsiden fra mappen der repoet ligger», men ikke hvordan repoet hentes (`git clone` eller ZIP-fila fra GitHub). Det var ikke en feil, og prøven gikk gjennom uten. Kristine bestemte 22. november 2026 at det skal være så enkelt som mulig for sensor, så README har nå steget «1. Hent koden» med begge måtene, også `cd G68-grande` etter `git clone`. Steget prøves i andre prøve fra en ny kopi (8.2.2).

## Hele flyten for hånd

Hele flyten prøves i nettleseren i begge modusene, i testmodus med testdataene i case 1, og én gang med ekte KI (ca. 1 kr). Filene som lastes ned, åpnes i Word og i en PDF-leser (kriterium 5).

| Hva | Dato | Hva som ble gjort | Resultat |
| --- | --- | --- | --- |
| Full generering, testmodus, case 1 (over HTTP) | 21. november 2026 | Claude, i prøven fra en ny kopi: innlogging, modusvalget, innleggingen, resultatsiden, brevsiden, nedlasting som Word og PDF og «Logg ut». Filene begynner som en ekte Word-fil (`PK`) og en ekte PDF (`%PDF`), men er ikke åpnet | Bestått |
| Full generering, testmodus, case 1 (nettleseren) | 22. november 2026 | Kristine: fra innloggingen til brevet er lastet ned, og «Logg ut». CV-en lastet opp som `cv.pdf`, annonsen limt inn fra `annonse.txt`, feilboksen for tomme felt, søppelbøtta, «Nytt forslag», «Logg ut» før nedlasting, nedlasting som Word og PDF, og tilbakeknappen etter «Logg ut» | Bestått. Resultatsiden ga 50 %, som i `fasit.md` |
| Korrektur, testmodus, case 1 (nettleseren) | 22. november 2026 | Kristine: CV, annonse og `eget-brev.txt` fra case 1, de markerte endringene og «Du skrev», nedlasting og «Logg ut» | Bestått |
| Full generering, ekte KI, case 1 (nettleseren) | 22. november 2026 | Kristine: testmodus av, samtykket, hele flyten og nedlasting. Tokens og kroner lest fra terminalen av Claude | Bestått. 7 635 tokens inn og 2 377 ut, ca. 0,86 kr (se «Kostnad per søknad») |
| .docx åpnes | 22. november 2026 | Kristine: fila fra nedlastingen åpnes i Word | Bestått |
| PDF åpnes | 22. november 2026 | Kristine: fila fra nedlastingen åpnes i en PDF-leser | Bestått |
| «Lag ny søknad» når alle KI-kallene er brukt (PR #55) | 22. november 2026 | Kristine: ekte KI, med grensen satt til 2 KI-kall i den kjøringen: `MAKS_KI_KALL` (i `backend/soknad/innstillinger.py`, brukt i `soknad/kjerne/okt.py`) ble satt til 2 i minnet før appen ble laget, uten å endre fila. Uten brev. Analysen brukte begge kallene, og «Lag søknadsbrevet mitt» ga feilboksen med «Lag ny søknad», som førte til startsiden | Bestått («ser bra ut») |
| «Gå til brevet» når alle KI-kallene er brukt og søknaden har et brev (retro 8) | 22. november 2026 | Kristine: ekte KI, med grensen satt til 3 KI-kall i den kjøringen (analysen 2 og brevet 1): `MAKS_KI_KALL` (i `backend/soknad/innstillinger.py`, brukt i `soknad/kjerne/okt.py`) settes til 3 i minnet før appen lages, uten å endre fila. Brevet lages, tilbakeknappen til resultatsiden, «Lag søknadsbrevet mitt» og «Ja» i vinduet: feilboksen har «Gå til brevet» og ikke «Lag ny søknad», og brevet finnes fortsatt. Det samme på innleggingen med feltene uendret. Til slutt «Nytt forslag» på brevsiden: den nye teksten om å laste ned brevet | Bestått: feilboksen hadde den nye teksten og «Gå til brevet», ikke «Lag ny søknad», på resultatsiden og innleggingen, og brevet var der etter trykket. Brevsiden hadde den nye teksten (Kristine: «det virket») |

## Tilgjengelighet og skjermbredder

Sjekkene for NFR-6 (kontrast, tastatur, synlige etiketter og alternativtekst) og NFR-7 (bredder og zoom). 320 px er med i tillegg til 375, 768 og 1280 px i PRD-en, fordi det er den smaleste vanlige mobilbredden.

| Sjekk | Dato | Hva som ble gjort | Resultat |
| --- | --- | --- | --- |
| Kontrast (WCAG AA) | 21. november 2026 | Claude: [kontrast.py](testkjoringer/8-2/kontrast.py) leser fargene i `backend/soknad/web/static/css/stil.css` og regner ut kontrasten for 25 fargepar som brukes sammen. Krav: 4,5:1 for tekst og 3:1 for rammer rundt felt, fokusringen og bryteren. Tabellen ligger i [kontrast.txt](testkjoringer/8-2/kontrast.txt). Den samme sjekken kjører med de andre testene og på GitHub i [test_kontrast.py](../backend/tests/web/test_kontrast.py) (`test_nfr6_kontrast_fargeparene_i_stilen_holder_wcag_aa`), så en ny farge med for lav kontrast gir en test som feiler | Bestått: alle 24 parene med krav består. Lavest er grønn tekst på lysegrønt (`success` på `success-tint`, 4,53:1), som DESIGN.md alt sier har ingen margin. Prosentlinjen (4,47:1) er bare pynt, fordi prosenten står som tekst |
| Etiketter og navn i HTML-en | 21. november 2026 | Claude: [etiketter.py](testkjoringer/8-2/etiketter.py) logger inn med testbrukeren og henter 14 sider i testmodus med case 1: registreringen og innloggingen, og i både Full generering og Korrektur startsiden, modusvalget, innleggingen, innleggingen med feilene for tomme felt, resultatsiden og brevsiden. Hvert steg sjekker at nettsiden kom til riktig side. Hvert felt skal ha en etikett (`<label>`, `aria-label` eller `aria-labelledby`), hver knapp tekst eller `aria-label` (tekst med `aria-hidden` teller ikke), hver `aria-labelledby`, `aria-describedby` og `aria-controls` skal peke på noe som finnes, og ingen id kan stå to ganger. Om etiketten synes på skjermen, kan skriptet ikke se. Feiltilstander som feil passord, KI-feilboksen og meldingen når alle KI-kallene er brukt, er ikke med. Tabellen ligger i [etiketter.txt](testkjoringer/8-2/etiketter.txt). Avkrysningsboksen for samtykket vises bare med API-nøkkel, så den er sjekket i malen (`start.html`): den ligger inni sin `<label>` | Bestått: 14 sider, ingen feil. Filvelgerne er skjult (`hidden`) og åpnes med knappen «Last opp PDF», som har `aria-label` |
| Synlige etiketter i nettleseren | 22. november 2026 | Kristine: hvert felt har en etikett man ser, ikke bare en plassholder | Bestått: hvert felt har en tekst over seg, og ingen felt har grå tekst inni |
| Alternativtekst | 21. november 2026 | Claude: [etiketter.py](testkjoringer/8-2/etiketter.py) fant ingen `<img>` på de 14 sidene, og prosentlinjen (`<svg>`) og fyrverkeriet (`<canvas>`) er skjult for skjermlesere (`aria-hidden="true"`), fordi det samme står som tekst. Ikonene (for eksempel ✓, →, «i», søppelbøtta og ikonene på modus-kortene) er `<span>`-er, og dem sjekker ikke skriptet. Claude har sett i malene at alle har `aria-hidden="true"`, og knappene med et ikon har `aria-label`. Skjermbildene i README har alternativtekst (story 8.1) | Bestått |
| Bare tastatur | 22. november 2026 | Kristine: hele flyten med Tab, Shift+Tab, Enter, mellomrom og Esc, uten mus. Fokusringen skal alltid synes | Bestått: alt kan nås med tastaturet. Tab går også gjennom nettleserens egne knapper (adresselinja og fanene) før nettsiden, så det tar litt tid. Det er vanlig i nettlesere og ikke en feil i nettsiden |
| 320 px | 22. november 2026 | Kristine: alle sidene, ingen rulling sidelengs. Bredden valgt i utviklerverktøyene (F12) | Bestått |
| 375 px (mobil) | 22. november 2026 | Kristine: alle sidene, ingen rulling sidelengs. Bredden valgt i utviklerverktøyene (F12) | Bestått |
| 768 px (nettbrett) | 22. november 2026 | Kristine: alle sidene, ingen rulling sidelengs. Bredden valgt i utviklerverktøyene (F12) | Bestått |
| 1280 px (PC) | 22. november 2026 | Kristine: alle sidene, ingen rulling sidelengs. Bredden valgt i utviklerverktøyene (F12) | Bestått |
| 200 % zoom | 22. november 2026 | Kristine: alle sidene på 1280 px med 200 % zoom, alt kan leses og brukes | Bestått |

## Skriptene som prøves for hånd

Prosjektet har ingen nettlesertester (bestemt av Kristine 21. november 2026, issue #16). De automatiske testene leser bare HTML-en fra serveren og kildeteksten til skriptene, så ingen test kjører dem i en nettleser. Hvert skript er prøvd for hånd i nettleseren i PR-ene der det ble laget eller endret, og prøves en siste gang her. Det står også under «Kjente begrensninger» i README. Skriptene ligger i `backend/soknad/web/static/js/`.

| Skript | Hva det gjør | Laget eller endret i | Siste prøve for hånd (8.2.1) |
| --- | --- | --- | --- |
| `innlegging.js` | «Last opp PDF» og «Lim inn tekst» på innleggingen, søppelbøtta som tømmer feltet, og fokus fra feilboksen til feltet | Story 2.5.1 (PR #12) og 6.1 (PR #42) | Bestått 22. november 2026 |
| `info.js` | «i»-boksene: trykk, Enter og mellomrom åpner og lukker, Esc lukker, og hover med mus | Story 2.6 (PR #14) | Bestått 22. november 2026 (trykk, Esc og hover) |
| `vente.js` | Ventetegnet mens KI-en jobber: siden sperres, og et nytt trykk sender ingenting. Også «Prøv på nytt» i KI-feilboksen | Story 2.7.1 (PR #15) og 2.7.2 (PR #17) | Bestått 22. november 2026 (ventetegnet og et nytt trykk). «Prøv på nytt» ble ikke prøvd, fordi ingen KI-feil kom |
| `nedlasting.js` | Knappen blir grønn med «✓ Lastet ned som …», filnavnet (`.docx` eller `.pdf`) vises, vinduet etter nedlasting åpnes med fokus på «Bli her», og feilboksen for samme format skjules | Story 3.2 (PR #20), 3.3 (PR #21), 7.1 (PR #45), 7.2 (PR #47), 7.5 (PR #50) og retro 7 (PR #51) | Bestått 22. november 2026 |
| `endringer.js` | «Du skrev» under en endret setning i Korrektur åpnes og lukkes med trykk, Enter og mellomrom, og flere kan være åpne | Story 5.3 (PR #37) og PR #40 | Bestått 22. november 2026 |
| `bekreft.js` | Vinduet «Vil du ha et nytt forslag?» («Ja» lager nytt brev, «Avbryt» og Esc lukker), og vinduet «Du har ikke lastet ned brevet.» før «Logg ut» | Story 7.1 (PR #45) og 7.5 (PR #50) | Bestått 22. november 2026 |
| `fyrverkeri.js` | Fyrverkeriet rundt overskriften på brevsiden, borte etter ca. 3 sekunder, og ingenting med redusert bevegelse | Story 7.4 (PR #49) | Bestått 22. november 2026 (fyrverkeriet vises og blir borte). Redusert bevegelse er prøvd i story 7.4 (ikke noe fyrverkeri med animasjonene slått av i Windows), og skriptet er ikke endret siden |
| `tilbake.js` | Etter «Logg ut» gir nettleserens tilbakeknapp innloggingen, ikke en side fra minnet | Story 1.4 (PR #5) | Bestått 22. november 2026 |

## Kriterium 13

En person som ikke kjenner prosjektet, helst en student eller noen som har søkt jobb nylig, ser resultatsiden for en av test-CV-ene og forklarer med egne ord hva som mangler i CV-en, og hva nøkkelordtreffet betyr og ikke betyr.

Planen var at testen skulle gjøres etter 29. november, sjekkpunktet for at hele flyten virker i testmodus. Sjekkpunktet ble nådd 12. november, og kriteriet har ingen dato i PRD-en, så testen ble gjort 22. november. Den ble gjort etter [kriterium-13-oppskrift.md](testkjoringer/8-2/kriterium-13-oppskrift.md): resultatsiden for case 1 i testmodus (50 %), én fast setning til personen, og to spørsmål: «Hva mangler i CV-en?» og «Hva betyr 50 % her, og hva betyr det ikke?». Kravene for bestått står i oppskriften og ble godkjent av Kristine før testen.

| Dato | Hvem (ikke navn) | Hva personen forklarte | Resultat |
| --- | --- | --- | --- |
| 22. november 2026 | Kollega av Kristine, kjente ikke prosjektet | Spørsmål 1: det som mangler, er det som står under «Står ikke i CV-en» og under «Dette kan du jobbe videre med». Spørsmål 2: bare 50 % av nøkkelordene fra annonsen står i CV-en. Da Kristine spurte på nytt om hva det ikke betyr: det er «kun fakta», noe du treffer på med antall ord, «ikke noe mer». Han trykket på «i»-knappene og «Hva er ATS og hva betyr det for deg?» for å se hva det betydde, og forsto siden greit | Bestått, med en merknad. Spørsmål 1 er bestått: han fant og forsto listene over det som mangler. Spørsmål 2 er bestått med egne ord: tallet er bare en ordtelling og ikke noe mer. Merknad: det han sa om hva tallet ikke betyr, kom først da han ble spurt på nytt, og han nevnte ikke selv at det ikke sier noe om sjansen for å få jobben. Kristine kan prøve med én person til senere |
