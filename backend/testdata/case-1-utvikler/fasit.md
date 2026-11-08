# Fasit: case 1, junior utvikler

Alt i denne casen er fiktivt. Sara Eksempel, Testvik Utvikling AS, Ola Nordmann, skolene, e-postene og telefonnumrene finnes ikke.

Casen er en student i siste år på bachelor i IT som søker en stilling som junior utvikler. CV-en dekker de fleste kravene i annonsen, men har tydelige hull: SQL, Docker, Scrum og førerkort. Casen tester at gap-analysen finner hullene, og at nøkkelordtreffet gir nøyaktig prosenten under.

KI-svarene i `ki-svar/` er håndlagde, slik at nettsiden kan kjøres i testmodus uten API-nøkkel. I Epic 4 byttes de ut med ekte KI-svar (FR-38), og da oppdateres tabellen «Nøkkelord» og prosenten sammen med `ki-svar/nokkelord.json`. Tabellen «Krav» og sjekklisten for brevet endres ikke. De ekte KI-svarene sjekkes mot dem (suksesskriterium 1).

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

## Nøkkelord

| Nøkkelord | Står i CV-en |
| --- | --- |
| Python | Ja |
| Flask | Ja |
| HTML | Ja |
| CSS | Ja |
| SQL | Nei |
| Git | Ja |
| Linux | Ja |
| Docker | Nei |
| Scrum | Nei |
| førerkort | Nei |
| engelsk | Ja |

7 av 11 = 64 %

## Sjekkliste for brevet

Brevet kan ikke påstå noe av dette, fordi det ikke står i CV-en:

- at Sara kan SQL eller har jobbet med databaser
- at hun har brukt Docker
- at hun har jobbet med Scrum eller smidig utvikling
- at hun har førerkort
- at hun alt er ferdig med bachelorgraden (hun blir ferdig våren 2027)
- at hun har jobbet som utvikler før
