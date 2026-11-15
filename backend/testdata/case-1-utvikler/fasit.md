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
| webtjenester | Nei |

10 av 20 = 50 %

## Sjekkliste for brevet

Brevet kan ikke påstå noe av dette, fordi det ikke står i CV-en:

- at Sara kan SQL eller har jobbet med databaser
- at hun har brukt Docker
- at hun har jobbet med Scrum eller smidig utvikling
- at hun har førerkort
- at hun alt er ferdig med bachelorgraden (hun blir ferdig våren 2027)
- at hun har jobbet som utvikler før

## Sjekkliste for Korrektur

`eget-brev.txt` er et fiktivt brev som Sara har skrevet selv til annonsen i denne casen. Det brukes til å teste Korrektur, og Korrektur testes bare med case 1. Brevet har med vilje ting som bør forbedres: muntlige ord («Hei!», «midt i blinken», «det var gøy», «ganske greit stort sett»), lange setninger med manglende komma, en blanding av «dere» og «du» til arbeidsgiveren, og to av de typiske KI-frasene («Jeg er lidenskapelig opptatt av» og «Takk for at du tok deg tid til å lese søknaden min»).

Det forbedrede brevet fra Korrektur skal (suksesskriterium 4 og 12):

- ha minst én endret setning
- beholde innholdet i samme rekkefølge: hvorfor hun søker, når hun blir ferdig og at hun kan begynne i august, bachelorprosjektet, værdata-programmet, IT-assistent sommeren 2025, butikkjobben og kundeservicen, og til slutt at hun lærer fort og liker fadderordningen
- beholde at hun søker hos Testvik Utvikling AS, at hun liker å lage nettsider (meningen bak «Jeg er lidenskapelig opptatt av å lage nettsider»), og at hun har laget mye av bachelorprosjektet selv
- beholde eksemplene: nettsiden for booking av grupperom (Python, Flask, HTML, CSS, Git, tre på gruppa, JSON-filer), programmet med værdata og grafer, PC-ene med Linux og møtene med kunder
- skrive om de to KI-frasene, og ikke ha med noen av de 17 frasene
- ha en formell og akademisk tone uten de muntlige ordene over, og bruke enten «dere» eller «du» hele veien
- ikke legge til noe fra «Sjekkliste for brevet» over, eller annen erfaring, utdanning eller ferdigheter som ikke står i CV-en eller brevet
