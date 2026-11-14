# Fasit: case 2, junior økonomimedarbeider

Alt i denne casen er fiktivt. Jonas Eksempelsen, Prøvdal Regnskap AS, Kari Nordmann, skolene, e-postene og telefonnumrene finnes ikke.

Casen er en student i siste år på bachelor i økonomi og administrasjon som søker en stilling som junior økonomimedarbeider i et regnskapsbyrå. CV-en dekker en del av kravene i annonsen, men har tydelige hull: Power BI, regnskapsprogram, lønnskjøring og Python. Casen tester at gap-analysen finner hullene i et annet fagfelt enn case 1, og at nøkkelordtreffet gir nøyaktig prosenten under. Case 2 er bare for Full generering. Korrektur testes med case 1.

Annonsen brukes også i kriterium 3, sammen med CV-en fra case 1 (se testplanen). Python, kundekontakt og norsk og engelsk er krav som også CV-en fra case 1 dekker.

KI-svarene i `ki-svar/` er ekte svar fra Claude, laget med `backend/scripts/lag_testsvar.py` (FR-38), slik at nettsiden kan kjøres i testmodus uten API-nøkkel. Når svarene lages på nytt, oppdateres tabellen «Nøkkelord» og prosenten sammen med `ki-svar/nokkelord.json`. Tabellen «Krav», listen «Viktige nøkkelord» og sjekklisten for brevet endres ikke. KI-svarene sjekkes mot dem (suksesskriterium 1, 11 og 14).

## Krav

| Krav | Dekket | Begrunnelse |
| --- | --- | --- |
| Har eller fullfører en bachelorgrad i økonomi og administrasjon eller i regnskap og revisjon | Ja | Bachelor i økonomi og administrasjon, fullføres våren 2027. |
| Kan regnskap og kjenner norske regnskapsregler | Ja | Emnet finansregnskap med norske regnskapsregler, bokføring, avstemming og årsoppgjør under Ferdigheter, og regnskapet i studentforeningen. |
| Er god i Excel | Ja | Pivottabeller, formler og diagrammer under Ferdigheter, og Excel er brukt i begge prosjektene. |
| Har erfaring med Power BI | Nei | Power BI står ikke i CV-en. |
| Har brukt et regnskapsprogram, gjerne Tripletex | Nei | CV-en nevner ikke noe regnskapsprogram. Regnskapet i studentforeningen sier ikke hvilket verktøy som ble brukt. |
| Har erfaring med lønnskjøring | Nei | Lønn står ikke i CV-en. |
| Har erfaring med Python | Nei | CV-en nevner ingen programmering. |
| Liker kundekontakt | Ja | Jobber deltid i kundeservice og svarer kunder på telefon og e-post. |
| Snakker og skriver godt norsk og engelsk | Ja | Norsk er morsmål, og engelsk er flytende muntlig og skriftlig. |

## Viktige nøkkelord

Nøkkelordlisten fra KI-en skal ha alle disse (suksesskriterium 14). Et viktig nøkkelord er med når det står som eget ord i et av nøkkelordene i listen, så «erfaring med Python» har med «Python». Listen er de seks fagkunnskapene og verktøyene som annonsen krever, foreslått av Claude og godkjent av Kristine 14. november 2026. Tripletex står med «gjerne» i annonsen og er derfor ikke viktig. Graden, kundekontakt og språkene (norsk og engelsk) er krav, men ikke med i listen.

| Viktig nøkkelord |
| --- |
| regnskap |
| Excel |
| Power BI |
| regnskapsprogram |
| lønnskjøring |
| Python |

## Nøkkelord

Tabellen har nøkkelordene fra `ki-svar/nokkelord.json`, i samme rekkefølge. «Står i CV-en» betyr at nøkkelordet står ordrett i CV-en, slik telleregelen søker. «bachelorgrad» er derfor Nei, selv om CV-en har «bachelor», og «avstemme kontoer» er Nei, selv om CV-en har «avstemming».

| Nøkkelord | Står i CV-en |
| --- | --- |
| bachelorgrad | Nei |
| økonomi og administrasjon | Ja |
| regnskap og revisjon | Nei |
| regnskap | Ja |
| norske regnskapsregler | Ja |
| Excel | Ja |
| Power BI | Nei |
| regnskapsprogram | Nei |
| Tripletex | Nei |
| lønnskjøring | Nei |
| Python | Nei |
| kundekontakt | Ja |
| norsk | Ja |
| engelsk | Ja |
| avstemme kontoer | Nei |
| rapporter | Nei |

7 av 16 = 44 %

## Sjekkliste for brevet

Brevet kan ikke påstå noe av dette, fordi det ikke står i CV-en:

- at Jonas har brukt Power BI
- at han har brukt et regnskapsprogram, for eksempel Tripletex
- at han har kjørt lønn
- at han kan Python eller annen programmering
- at han alt er ferdig med bachelorgraden (han blir ferdig våren 2027)
- at han har jobbet som regnskapsfører før
