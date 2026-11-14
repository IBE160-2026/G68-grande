# Testplan

Testplanen viser resultatet for suksesskriteriene som ikke testes automatisk (NFR-12). Den fylles ut underveis, og gjøres ferdig i Epic 8 (hele flyten og README fra en ny kopi av repoet).

## Slik testes kriteriene med ekte KI

Kriterium 1, 3, 11, 12 og 14 testes med ekte KI (Claude), ikke i testmodus (PRD del 5). De kjøres tre ganger per testcase, og alle tre må bestå. Feiler én kjøring, forbedres prompten én gang, og alle tre kjøres på nytt (plan B). Feiler det fortsatt, står kriteriet her som ikke bestått, med hva som gikk galt.

Kjøringene gjøres med skriptet `backend/scripts/lag_testsvar.py` (se README). Kjøring 1 skriver de ferdige svarene i testmodus (`backend/testdata/<case>/ki-svar/`). Kjøring 2 og 3 skrives rett i `my-project/testkjoringer/`. Svarene og terminalloggen (tokens og pris) fra alle tre kjøringene ligger i `my-project/testkjoringer/<story>/kjoring-<n>/`, så de kan sjekkes i etterkant, også etter at svarene i testmodus er laget på nytt.

| Kriterium | Hva | Hvordan det sjekkes | Status |
| --- | --- | --- | --- |
| 1 | Gap-analysen finner alle krav som mangler, og ingen dekkede krav står under «mangler» | `gap.json` mot tabellen «Krav» i `fasit.md` | Bestått for case 1 (story 4.4). Case 2 testes i story 4.5 |
| 3 | Samme CV med to annonser gir brev med krav som er spesifikke for hver annonse | Brevene for CV-en i case 1 mot annonsen i case 1 og case 2 | Testes i story 4.5 (trenger case 2) |
| 11 | Brevet nevner ingen erfaring, utdanning eller ferdigheter som ikke står i CV-en | `brev-1.json` mot CV-en og «Sjekkliste for brevet» i `fasit.md` | Bestått for case 1 mot sjekklisten. Venter på Kristines vurdering av merknadene (story 4.4). Case 2 testes i story 4.5 |
| 12 | Korrektur beholder brukerens innhold, eksempler og rekkefølge | Korrektur-svarene mot det opprinnelige brevet | Testes i Epic 5 (trenger Korrektur) |
| 14 | Nøkkelordlisten har alle nøkkelordene fasiten markerer som viktige | `nokkelord.json` mot «Viktige nøkkelord» i `fasit.md` | Bestått for case 1 (story 4.4). Case 2 testes i story 4.5 |

## Story 4.4: ekte KI-svar for case 1 (14. november 2026)

Modell: `claude-opus-5-5`. Promptene er de fra story 4.1 og 4.2, uten endringer. Skriptet ble kjørt tre ganger etter hverandre, kl. 13.42, 13.48 og 13.49.

### Resultat

| Kriterium | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| 1: gap-analysen | Bestått: 6 dekket og 4 mangler, nøyaktig som fasiten | Bestått: samme som kjøring 1 | Bestått: samme som kjøring 1 |
| 11: brevet mot sjekklisten | Bestått (merknader) | Bestått (merknader) | Bestått (merknader) |
| 14: de viktige nøkkelordene | Bestått: alle 8 (19 nøkkelord i alt) | Bestått: alle 8 (19 i alt) | Bestått: alle 8 (18 i alt, uten «webtjenester») |
| Nøkkelordtreffet (telleregelen) | 9 av 19 = 47 % | 9 av 19 = 47 % | 9 av 18 = 50 % |

**Kriterium 1:** alle tre kjøringene ga de samme ti kravene som fasiten, med ordlyden fra annonsen. SQL og relasjonsdatabaser, Docker, smidig utvikling og Scrum, og førerkort står under «mangler». Ingen dekkede krav står der. `gap.json` fra kjøring 1 er derfor lik den håndlagde fila fra story 2.2, og står ikke som endret i Git.

**Kriterium 14:** KI-en skrev «førerkort klasse B» i stedet for «førerkort». Det regnes som med, fordi «førerkort» står som eget ord i nøkkelordet (se `fasit.md`). Nøkkelordlisten var lik i kjøring 1 og 2. I kjøring 3 manglet bare «webtjenester», som ikke er et viktig nøkkelord.

**Nøkkelordtreffet** gikk ned fra 64 % med de håndlagde svarene til 47 %. KI-en tok med ord fra annonsen som «bachelorgrad», «informatikk», «relasjonsdatabaser», «tester» og «webtjenester». CV-en sier «bachelor» og «IT», så telleregelen, som søker ordrett, gir ikke treff, selv om gap-analysen sier at kravet om graden er dekket. Det er en kjent begrensning (se README: bøyningsformer fanges ikke opp, og gap-analysen og nøkkelordtreffet kan si hverandre imot). Prosenten varierer også litt med listen fra KI-en (47 eller 50 %). Kriterium 2 (nøyaktig prosent når listen er fast) testes automatisk med listen i `ki-svar/`.

**Kriterium 11:** ingen av brevene (`brev-1.json` i hver kjøring, og også `brev-2.json`) påstår noe fra sjekklisten: ikke SQL eller databaser, Docker, Scrum eller smidig utvikling, førerkort, at Sara alt er ferdig med graden, eller at hun har jobbet som utvikler før. Alle brevene nevner stillingen og Testvik Utvikling AS, kobler minst to krav til CV-en og bruker ingen av de 17 KI-frasene.

Merknader. Prompten tillater at KI-en omformulerer det som står i CV-en og kobler det til kravene, for eksempel et gruppeprosjekt til «erfaring med samarbeid og prosjektarbeid». Det står derfor ikke her. Det som står her, er av to slag:

1. **Fakta som ikke står i CV-en** (hvor, når eller hvor ofte):
   - «Linux kjenner jeg fra studiet» eller «Linux har jeg brukt i studiet» (kjøring 1 `brev-1` og `brev-2`, kjøring 2 `brev-2`). CV-en har emnet operativsystemer og Linux under Ferdigheter, men sier ikke at Linux ble brukt i studiet.
   - «det jeg har jobbet mest med i studiet: webutvikling i Python» og «Til daglig bruker jeg Git og GitHub» (kjøring 2 `brev-1`). CV-en sier ikke hva hun har jobbet mest med, eller hvor ofte.
   - «bruker vi Git og GitHub til versjonskontroll» i bachelorprosjektet (kjøring 1 `brev-2`). CV-en har Git og GitHub under Verktøy, men knytter bare Git til prosjektet.
2. **Egenskaper KI-en har lest ut av en jobb** (står ikke i CV-en, men er en tolkning av kundeservice og IT-assistent):
   - «holde orden i travle perioder» (kjøring 3 `brev-1`)
   - «finne ut hva folk trenger hjelp til, og forklare løsninger på en enkel måte» (kjøring 1 `brev-2`)
   - «møte folk med ulike behov og å forklare ting på en enkel måte» (kjøring 2 `brev-1`)
   - «lytte til hva folk trenger, og å forklare ting enkelt» (kjøring 2 `brev-2`)
   - «møte kunder på en ryddig og vennlig måte» og «bli enige om løsninger underveis» (kjøring 3 `brev-2`)

I tillegg:

- **Et hull nevnt ærlig:** «SQL og relasjonsdatabaser er et område jeg ennå ikke har arbeidet med» (kjøring 2 `brev-2`). Det er ingen påstand, men den automatiske sjekklistetesten ville feilet hvis dette brevet var i `ki-svar/`, fordi den ikke godtar at brevet nevner SQL i det hele tatt. `brev-2` er «Nytt forslag» (Epic 7) og hører ikke til en fullført søknad.
- **Stor bokstav:** fem av seks brev har overskriften «Søknad på stillingen som Junior utvikler», med stor J fordi tittelen står slik i annonsen. Midt i en setning skrives stillingen vanligvis med liten bokstav. Dette gjelder også `brev-1` i testmodus.

Kristine vurderer om merknadene er brudd på kriterium 11, og om en ærlig omtale av et hull er lov. Er de brudd, er det plan B: prompten for brevet forbedres én gang (også for stor bokstav i overskriften), og alle tre kjøringene gjøres på nytt.

### Kostnad og tid

Tallene er fra loggen i terminalen («KI-kall … tokens … ca. … kr»). En fullført søknad er nøkkelord, gap og ett brev. Kronene er regnet med 11 kr per dollar og prisene for `claude-opus-5-5` i `backend/soknad/innstillinger.py`.

| | Kjøring 1 | Kjøring 2 | Kjøring 3 |
| --- | --- | --- | --- |
| Tokens inn (nøkkelord + gap + brev) | 1 501 + 2 060 + 3 129 = 6 690 | 6 690 | 6 690 |
| Tokens ut (nøkkelord + gap + brev) | 138 + 190 + 2 243 = 2 571 | 138 + 190 + 1 360 = 1 688 | 132 + 499 + 1 291 = 1 922 |
| Kroner per fullført søknad | 0,10 + 0,13 + 0,63 = 0,86 kr | 0,10 + 0,13 + 0,44 = 0,67 kr | 0,10 + 0,20 + 0,42 = 0,72 kr |
| Det andre brevet (`brev-2`) | 0,65 kr | 0,62 kr | 0,45 kr |
| Hele kjøringen av skriptet | 1,51 kr | 1,29 kr | 1,16 kr |

En fullført søknad kostet 0,67–0,86 kr, under målet på 3 kr (NFR-11) og under overslaget på omtrent 2 kr i PRD-en. De tre kjøringene kostet ca. 4 kr i alt.

Tid per kall: nøkkelord og gap tok 2–5 sekunder hver, og et brev 17–29 sekunder. Det er godt innenfor tidsgrensen på 90 sekunder i `innstillinger.py`.

### Canva-CV-en

Kristine prøver om KI-en forstår teksten fra Canva-CV-en sin riktig (hva som er utdanning, jobb og oppsummering), med testmodus av. Hun skriver bare hva KI-en forsto og misforsto. Ingen personopplysninger fra CV-en, og ingen KI-svar som siterer den, legges i repoet.

| Dato | Hva KI-en forsto riktig | Hva den misforsto | Resultat |
| --- | --- | --- | --- |
| *(Kristine fyller inn)* | | | |
