# Fasit: case 1, junior utvikler

Alt i denne casen er fiktivt. Sara Eksempel, Testvik Utvikling AS, Ola Nordmann, skolene, e-postene og telefonnumrene finnes ikke.

Casen er en student i siste år på bachelor i IT som søker en stilling som junior utvikler. CV-en dekker de fleste kravene i annonsen, men har tydelige hull: SQL, Docker, Scrum og førerkort. Casen tester at gap-analysen finner hullene, og at nøkkelordtreffet gir nøyaktig prosenten under.

KI-svarene i `ki-svar/` er ekte svar fra Claude, laget med `backend/scripts/lag_testsvar.py` (FR-38), slik at nettsiden kan kjøres i testmodus uten API-nøkkel. Når svarene lages på nytt, oppdateres tabellen «Nøkkelord» og prosenten sammen med `ki-svar/nokkelord.json`. Tabellen «Krav», listen «Viktige nøkkelord» og sjekklisten for brevet endres ikke. KI-svarene sjekkes mot dem (suksesskriterium 1, 11 og 14).

## Krav

| Krav | Dekket | Begrunnelse |
| --- | --- | --- |
| Har eller fullfører en bachelorgrad i informatikk eller IT | Ja | Bachelor i IT, fullføres våren 2027. |
| Har erfaring med Python, gjerne med rammeverket Flask | Ja | Python og Flask står under Ferdigheter og er brukt i bachelorprosjektet. |
| Kan HTML og CSS | Ja | Står under Ferdigheter og er brukt i bachelorprosjektet. |
| Har erfaring med SQL og relasjonsdatabaser | Nei | CV-en nevner ingen databaser. Bachelorprosjektet lagrer dataene i JSON-filer. |
| Bruker Git til versjonskontroll | Ja | Git og GitHub står under Verktøy, og Git ble brukt i bachelorprosjektet. |
| Har jobbet med Linux | Ja | Står under Operativsystemer, og hun satte opp PC-er med Linux som IT-assistent. |
| Har erfaring med Docker | Nei | Docker står ikke i CV-en. |
| Kjenner smidig utvikling, gjerne Scrum | Nei | CV-en sier at de var tre på gruppa, men ikke hvordan de jobbet. Smidig utvikling og Scrum står ikke i CV-en. |
| Har førerkort klasse B | Nei | Førerkort står ikke i CV-en. |
| Snakker og skriver godt norsk og engelsk | Ja | Norsk er morsmål, og engelsk er flytende muntlig og skriftlig. |

## Viktige nøkkelord

Nøkkelordlisten fra KI-en skal ha alle disse (suksesskriterium 14). Et viktig nøkkelord er med når det står som eget ord i et av nøkkelordene i listen, så «førerkort klasse B» har med «førerkort». Listen er de åtte ferdighetene, verktøyene og sertifikatet som annonsen krever, valgt av Kristine 14. november 2026. Flask og Scrum står med «gjerne» i annonsen og er derfor ikke viktige. Graden (bachelor i informatikk eller IT) og språkene (norsk og engelsk) er krav, men ikke med i listen.

| Viktig nøkkelord |
| --- |
| Python |
| HTML |
| CSS |
| SQL |
| Git |
| Linux |
| Docker |
| førerkort |

## Nøkkelord

Tabellen har nøkkelordene fra `ki-svar/nokkelord.json`, i samme rekkefølge. «Står i CV-en» betyr at nøkkelordet står ordrett i CV-en, slik telleregelen søker. «bachelorgrad» er derfor Nei, selv om CV-en har «bachelor».

| Nøkkelord | Står i CV-en |
| --- | --- |
| bachelorgrad | Nei |
| informatikk | Nei |
| IT | Ja |
| Python | Ja |
| Flask | Ja |
| HTML | Ja |
| CSS | Ja |
| SQL | Nei |
| relasjonsdatabaser | Nei |
| Git | Ja |
| versjonskontroll | Ja |
| Linux | Ja |
| Docker | Nei |
| smidig utvikling | Nei |
| Scrum | Nei |
| førerkort klasse B | Nei |
| norsk | Ja |
| engelsk | Ja |
| tester | Nei |

10 av 19 = 53 %

## Sjekkliste for brevet

Brevet kan ikke påstå noe av dette, fordi det ikke står i CV-en:

- at Sara kan SQL eller har jobbet med databaser
- at hun har brukt Docker
- at hun har jobbet med Scrum eller smidig utvikling
- at hun har førerkort
- at hun alt er ferdig med bachelorgraden (hun blir ferdig våren 2027)
- at hun har jobbet som utvikler før
