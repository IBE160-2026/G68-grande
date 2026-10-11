# Strukturgjennomgang: addendum.md (Søknadsassistenten)

**Formål og lesere:** Addendumet finnes for at Kristine (og agentene som lager UX-, arkitektur- og story-dokumentene) skal finne detaljene og de første ideene fra PRD-arbeidet. Detaljene sorteres etter hvilket dokument de skal brukes i. PRD-ens tabell «Avgjøres i UX og arkitektur» (§7) peker hit.

**Strukturmodell:** Referanse/database (MECE). Leseren slår opp ett punkt om gangen, for eksempel «hva står om FR-23?». Det trengs ingen fortelling, men gruppene må være rene og punktene i samme form. Modellen passer godt. Dokumentet er allerede bygget som tre bøtter med merkede punkter.

**Ordtelling (word_metrics):** totalt 724 ord. Innledning 18, Til UX 221, Til arkitektur 335, Arbeidsmåte 139.

Ingen funn handler om ordlyd. Alle forslag flytter, grupperer eller fjerner hele punkter, og teksten i hvert punkt beholdes slik den står.

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §Til arkitektur: rekkefølgen på de 10 punktene (335 ord) | MOVE: grupper punktene som hører sammen, uten å endre teksten. **PDF og filer:** Filstørrelse (FR-12), Lese tekst fra PDF (FR-11), Biblioteker, CV-er med kolonner og tabeller (FR-11). **KI-en:** KI-tjeneste (NFR-11), Ventetid på KI-en (FR-28). **Testdata:** Testdata og fasit (NFR-3), Gjenkjenning av testdata (FR-34). **Kode:** Kodestil og språk. | Nå er beslektede punkter spredt. «Kodestil og språk» står mellom de to testdata-punktene, og «Ventetid på KI-en» står fem punkter etter «KI-tjeneste». Den nye rekkefølgen følger også omtrent PRD-tabellen i §7, slik at det blir lettere å gå fra tabellen til detaljene. (0 ord spart) |
| structure | §Til arkitektur: «Typiske KI-fraser (FR-24)» med eksempelliste (~45 ord) | MOVE: til en egen seksjon (for eksempel «Til prompten for brevet») eller sist i addendumet som eget punkt | Dette er ikke et arkitekturvalg. Det er innhold til instruksen til KI-en og et åpent punkt som Kristine eier (PRD §7: «Før prompten for brevet skrives»). Under «Til arkitektur» kan det se ut som om arkitekten skal bestemme listen. PRD-en (FR-24) sier bare «listen ligger i addendum», så en egen overskrift gjør listen lettere å finne. (0 ord spart) |
| structure | §Til UX: «Skisser (fra faglærer)» står sist (~25 ord) | MOVE: først i «Til UX» | Punktet sier hvilke skisser UX-arbeidet skal lage, og rammer dermed inn resten. De andre punktene er detaljer om enkeltelementer. Det viktigste bør stå først. (0 ord spart) |
| structure | §Til arkitektur: «Lese tekst fra PDF (FR-11)» (~17 ord) og «Biblioteker (fra faglærer)» (~20 ord) | MERGE: sett dem rett etter hverandre, eller slå dem sammen til ett punkt med begge setningene | Begge punktene sier at arkitekturen skal velge hvordan PDF leses. «Biblioteker» dekker i tillegg .docx og PDF ut. PRD-tabellen har dem allerede som én rad («Hvordan PDF leses, og hvordan Word og PDF lages»). (opptil ~5 ord spart hvis den ene overskriften faller bort) |
| structure | §Til arkitektur: «KI-tjeneste (NFR-11)», setningene «Claude (Anthropic) via API» og «API-nøkkelen ligger bare lokalt og legges aldri i Git.» | QUESTION: skal de vedtatte delene stå her fortsatt? De står nå i PRD-en som NFR-11 og NFR-2. Det åpne spørsmålet («modell, kostnad og håndtering av nøkkelen avklares i arkitekturen») er det eneste som bare finnes her. | Dette er ekte dobbeltlagring av vedtatte krav. Hvis PRD-en endres senere, kan addendumet bli stående med en gammel versjon. Forfatteren avgjør dette. Dobbeltlagringen kan også ses som nyttig kontekst for arkitekten. (~15 ord spart hvis kuttet) |
| structure | §Til arkitektur: «Kodestil og språk» (~30 ord) | QUESTION: dele punktet? Linter, formatterer og CI-sjekk passer under «Arbeidsmåte», ved siden av PR-regel 3 («CI må være grønne»). «Ett språk for hele nettsiden (NFR-8)» blir stående under arkitektur. | Punktet blander en arbeidsregel og et arkitekturvalg. Begge plasseringene kan forsvares, så dette er et spørsmål og ikke et krav. (0 ord spart) |
| structure | §Til UX: tomme linjer mellom punktene (noen punkter har tom linje imellom, de tre første har ikke) | CONDENSE: bruk samme avstand mellom alle punktene i lista | Når avstanden varierer, ser det ut som om de tre første punktene er en egen undergruppe, men det er de ikke. I Markdown blir lista også vist med ulik avstand. (0 ord) |
| structure | Overlapp med PRD §7 «Avgjøres i UX og arkitektur» (for eksempel 20–30 sekunder, Korrektur-alternativene, filnavn) | PRESERVE | PRD-tabellen er et sammendrag som peker hit, og addendumet har detaljene og begrunnelsen (for eksempel hvorfor visningen «per setning» ble avvist). Dette er bevisst forsterkning og ikke unødvendig dobbeltlagring. Eksempelet med mappestrukturen for testdata og den nummererte PR-lista er også visuelle hjelpemidler som bør stå. |

1 mindre funn til: hvor kilden står, er skrevet på to måter. Noen ganger står den i den uthevede tittelen («(fra faglærer)»), og noen ganger i en egen setning til slutt («(Fra product brief.)»). Si fra hvis du vil ha det utdypet.

## Oppsummering

- **Anbefalinger:** 8 rader (5 handlinger: MOVE ×3, MERGE ×1, CONDENSE ×1; 2 QUESTION; 1 PRESERVE), pluss 1 mindre funn.
- **Mulig reduksjon hvis alt godtas:** ~20 ord av 724 (~3 %). Addendumet er allerede kort. Det som er å hente er grupperingen, ikke lengden.
- **Lengdemål:** ikke oppgitt.
- **Avveiinger for forståelsen:** ingen. Ingen av forslagene fjerner eksempler, begrunnelser eller visuelle hjelpemidler.
