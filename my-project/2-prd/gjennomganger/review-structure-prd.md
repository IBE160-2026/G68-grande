# Strukturgjennomgang av PRD: Søknadsassistenten

**Dato:** 2026-10-11
**Linse:** struktur (organisering: rekkefølge, dobbeltinnhold, plassering, slå sammen eller dele opp). Formuleringene er ikke vurdert. Innholdet er ikke vurdert.
**Stilguide:** Microsoft Writing Style Guide. **Lesertype:** mennesker.

**Hvem dokumentet er for:** Dokumentet skal hjelpe sensor og Kristine selv (og senere UX, arkitektur og stories) å forstå hva Søknadsassistenten skal gjøre i versjon 1, hvorfor, hva som er kuttet, og hvordan resultatet testes.

**Strukturmodell:** Strategisk/kontekst (pyramide), som passer for PRD-er. Dokumentet følger modellen godt. Visjonen kommer først, kravene er gruppert etter flyten, og omfang, suksesskriterier, risiko og åpne spørsmål kommer etterpå. Funnene under er justeringer, ikke en omskriving av oppsettet.

**Ordtelling (word_metrics.py):** 4 364 ord totalt.

## Funn

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §2.4 FR-28: innledningen «Hvis KI-en ikke svarer, får brukeren en feilmelding:» med fire underpunkter (~95 ord) | QUESTION: Del underpunktene i to nivåer. Behold de to første (nettverksfeil, andre feil) under innledningen. Løft «Hvis KI-en svarer, men svaret ikke kan brukes …» og «Etter en feil er det brukeren har lagt inn, fortsatt der …» ut på samme nivå som innledningen, for eksempel som egne punkter i FR-28. Ordlyden beholdes. | Innledningen gjelder bare når KI-en *ikke* svarer, men punkt 3 handler om at KI-en *svarer* med et ubrukelig svar, og punkt 4 gjelder alle feilene. Nå ser det ut som om alt hører inn under «ikke svarer». Ingen ord spares (0 ord). |
| structure | §6 «Nødliste ved tidsnød» (129 ord), plassert under §6 Risiko etter Milepæler | MOVE til §4 «Omfang og kuttliste», som en egen underoverskrift etter «Ikke med i versjon 1». Risikoraden «Kodingen tar lengre tid …» henviser allerede til nødlisten og kan beholde henvisningen (bytt eventuelt «under» med «i kapittel 4»). | Nødlisten handler om omfang: hva som kan flyttes til kuttlisten. Lagt ved siden av kuttlisten ser sensor hele omfanget på ett sted: det som er kuttet, det som kuttes ved tidsnød, og det som aldri kuttes. 0 ord. |
| structure | §4 tabellen «Ikke med i versjon 1», de tre siste radene merket «(gjøres hvis det blir tid)» (~95 ord) | MOVE til en egen liten underoverskrift i §4, for eksempel «Gjøres hvis det blir tid», med samme tabell og samme tekst. Merknaden «(gjøres hvis det blir tid)» i hver rad kan da sløyfes, fordi overskriften sier det. | Tabellen blander to kategorier: ting som bevisst er utelatt, og ting som kan komme med hvis tiden strekker til. Dette er speilbildet av nødlisten (ting som er med, men kan kuttes). Med egne overskrifter blir det lettere å se forskjellen. Sparer ~15 ord hvis merknaden sløyfes, ellers 0. |
| structure | §6 «Milepæler» (103 ord), plassert under §6 Risiko | QUESTION: Vurder å gjøre Milepæler til et eget kapittel (for eksempel «Plan og milepæler») mellom §5 og §6, eller rett etter §4. | Milepælene er en plan, ikke en risiko. De henger sammen med risikoraden om tidsbruk, men står nå som en underseksjon av Risiko. Hvis nødlisten flyttes til §4, står milepælene alene under Risiko. 0 ord. |
| structure | §2.4 FR-23, setningen «Utgangspunktet er at brevet vises én gang i den nye versjonen, at endrede setninger er markert, og at brukeren kan klikke på en markert setning for å se den gamle.» (~31 ord) | QUESTION: Samme utgangspunkt står nå tre steder: i FR-23, i tabellen «Avgjøres i UX og arkitektur» (§7) og i addendum («Markeringer i Korrektur»). Vurder å la setningen stå bare i addendum, og beholde «Endelig løsning bestemmes i UX.» i FR-23. Hvis du vil at sensor skal se utgangspunktet direkte i kravet, er det også et godt valg å beholde den. | Kravet blander *hva* (vis endringene, beholde kontrollen, ikke bare farge) med et UX-forslag til *hvordan*. PRD-en sier selv i §7 at *hvordan* avgjøres i UX. Sparer ~31 ord (~0,7 %). Merk at «Slik ser brukeren …» da viser til «viser hva som er endret» tidligere i kravet. |
| structure | §2.6 FR-32 (~95 ord) og FR-34 (~75 ord), hver skrevet som ett langt avsnitt | QUESTION: Del opp i underpunkter på samme måte som FR-36, uten å endre ordlyden. FR-32 har tre deler: bytte mellom modusene, hva testmodus gjør, og hva som skjer uten API-nøkkel. FR-34 har to: hva som fungerer i testmodus, og hva testdataene inneholder. | FR-36 viser at underpunkter fungerer godt i dette kapittelet. FR-32 og FR-34 har like mange regler, men er tyngre å skanne for sensor og senere for den som skriver stories. 0 ord. |
| structure | §2.6 FR-38, setningen «README viser i tillegg to–tre skjermbilder av nettsiden med ekte KI på.» (~12 ord) | MERGE: Dette står også i README-listen i NFR-8 («to–tre skjermbilder med ekte KI på (FR-38)»). Vurder å la NFR-8 være eneste sted, siden NFR-8 er listen over hva README har. | Lite dobbeltinnhold. Henvisningen fra NFR-8 til FR-38 holder koblingen. Sparer ~12 ord. Lav prioritet. |
| structure | §2 «Flyten i korte trekk» (~60 ord) | PRESERVE | Ser ut som en gjentakelse av kapitlene under, men den gir leseren et kart over hele flyten med FR-numre før detaljene. Den forklarer også hvorfor numrene ikke står i rekkefølge. Behold. |
| structure | §7 «Avgjøres i UX og arkitektur» (256 ord), som overlapper med addendum og med korte henvisninger i FR-12, FR-23, FR-29 og NFR-11 | PRESERVE | Overlappen er bevisst og nyttig: tabellen er den samlede oversikten for sensor, med begrunnelse, mens addendum har detaljene. De korte henvisningene i kravene er pekere, ikke dobbeltinnhold. Behold. |

## Oppsummering

- **Antall anbefalinger:** 9 (3 MOVE, 4 QUESTION, 1 MERGE, 2 PRESERVE; den ene MOVE-raden kan gi en liten CUT av merknader).
- **Hvis alle godtas:** ca. 40–60 ord kortere (~1 % av 4 364 ord). Dokumentet er ikke for langt. Gevinsten ligger i at omfang, plan og risiko blir tydeligere skilt, og at FR-28 blir lettere å lese riktig.
- **Lengdemål:** ikke oppgitt.
- **Avveininger:** Hvis du flytter utgangspunktet i FR-23 til bare addendum, må sensor åpne addendum for å se forslaget ditt til markeringer. Det er et reelt tap hvis du vil vise at du har tenkt på løsningen. Ellers koster ingen av forslagene noe for leseren.
- Ingen funn om ordliste, kilder, suksesskriterier eller kapittel 1 Visjon. Rekkefølgen og plasseringen der fungerer.
