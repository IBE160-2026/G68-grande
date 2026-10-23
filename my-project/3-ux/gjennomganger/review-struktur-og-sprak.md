# Språkvask av DESIGN.md og EXPERIENCE.md (2026-10-23)

Fire hjelpere leste dokumentene før de ble satt til ferdig: én for struktur og én for språk per dokument (bmad-review, linsene `structure` og `prose`). Språk-hjelperne fikk se funnene fra struktur-hjelperne, så de ikke foreslo det samme. Ingen forslag endret innholdet. Kristine bestemte alt, og hver beslutning står i `.memlog.md`.

## Hva hjelperne fant

| Hjelper | Forslag | Beholdt som det var |
|---|---|---|
| Struktur, DESIGN.md | 10 | 4 |
| Struktur, EXPERIENCE.md | 10 + 1 spørsmål | 5 |
| Språk, DESIGN.md | 17 + 3 små | — |
| Språk, EXPERIENCE.md | 24 + 2 spørsmål om UI-tekster | — |

## Hva Kristine bestemte

Forslagene ble delt i tre grupper.

**Gruppe 1, rene feil (godtatt samlet).** 30 rettelser: stavefeil («innforstått», «leserekkefølgen»), særskriving («bringebærfarget», «ferskenfarget»), komma, doble punktum etter sitat, bestemt form («temaet», «addendumet», «PRD-en og testene»), samme ord for det samme («Tekstfelt», «avkrysningsboksen»), «som i skissen», «liste med», ordstilling og liten bokstav etter kolon. Ingen UI-tekster ble endret.

**Gruppe 2, flytte ting (godtatt samlet).** Ingen tekst ble skrevet om.
- DESIGN.md: Components delt i grupper med undertitler, bruddpunktet flyttet over PC/mobil-lista, avrunding av hjørner bare i Shapes, kontrasttallene som tabell under «Kontrast», lenkene til skissene sist i hver del, «15 % større ved hover» bare i tabellen for bevegelse.
- EXPERIENCE.md: kopier i State Patterns byttet med «se …», fokusregler samlet i Accessibility Floor, tastaturregler bare i Interaction Primitives, «Skisser» flyttet til slutten, utseendet på hjørneraden bare i DESIGN.md, bruddpunktet over tabellen i Responsive.

**Gruppe 3, én og én (Kristine valgte å ta dem enkeltvis).**

| # | Forslag | Valg |
|---|---|---|
| 1 | «Hva er ATS og hva betyr den for deg?» → «… det …» | Endret |
| 2 | «Prøv på nytt» / «Prøv igjen» → samme ord overalt | Endret, men til **«Prøv på nytt»** overalt (KI-en foreslo «Prøv igjen») |
| 3 | «Hele ordet» → «Hele logoen» | Endret |
| 4 | «fordi det er mindre skremmende» → «fordi «i» er …» | Endret |
| 5 | «akkurat som nå» → «akkurat som i skissene» | Endret |
| 6 | «sjekkes først når» → «sjekkes ikke før» | Endret |
| 7 | «bare testdata i testmodus» → «filer eller tekst som ikke er testdata, i testmodus» | Endret |
| 8 | «så det ikke blir avbrutt» → «så opplesingen …» | Endret |
| 9 | «Det synlige navnet er det samme.» → «Den synlige teksten er den samme, uten feltnavnet …» | Endret |
| 10 | «Da kan ikke testmodus byttes» → «Slik …» | Endret |
| 11 | «ikonet som vipper» → «ikonet på modus-kortet som vipper» | Endret |
| 12 | «er arkitektur eller KI-instruks» → «hører til arkitekturen …» | Endret |
| 13 | Fyrverkeri «ca. 2,5 s» tatt bort (skissen bruker 2,2 s og 3,2 s) | Endret |
| 14 | «små store bokstaver (kapitéler)» | Beholdt |
| 15 | Flette fargene fra skissene inn i hovedlista | Kristines eget valg: flettet inn etter bruk, med én linje om at hun godkjente dem i runde 3, og punkt 10 i `mine-valg-og-ki-feil.md` |
| 16 | Flytte skjermleserdetaljer ut av tabellcellene | Beholdt |

To ganger justerte KI-en sitt eget forslag etter at Kristine hadde godtatt det. I nr. 7 la den til «eller tekst», fordi innlimt tekst også gir feilen i testmodus. I nr. 9 tok den bort «som før», fordi det var uklart. Begge justeringene ble vist til Kristine.
