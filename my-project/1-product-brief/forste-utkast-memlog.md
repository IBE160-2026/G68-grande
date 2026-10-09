---
topic: AI CV & Job Application Assistant
updated: 2026-09-16T13:49
---

> **Merknad lagt til 2026-10-09:** Idéen er hentet fra eksempel 2 fra faglærer, slik første linje i loggen sier. Linjen om at dokumentet skal «lese som egeninitiert idé» var ikke for å skjule for noen hvor jeg har fått inspirasjon fra, men for at KI-en skulle forstå hvordan jeg ville at formuleringen av teksten skulle være. Jeg ønsket ikke henvisninger til oppgaveteksten i selve produktbriefen, fordi det kræsjet med tekstens innhold. Loggen under er ellers uendret.

- (decision) Idé er lærerforeslått: AI CV & Job Application Assistant, fra oppgavetekst i IBE160-kurset
- (decision) To moduser, ingen betaling: Full generering (AI skriver fra stikkord) og Korrektur (AI forbedrer brukerens egen tekst) — 'dyrere/billigere'-språk droppet fordi oppgaveteksten krever 'Kjøp/salg over nettet: Nei'
- (decision) Filformat for output: DOC, MD, PDF (fra oppgaveteksten, ingen egen .docx-variant)
- (decision) Språk: norsk og engelsk
- (decision) Solo-prosjekt, bruker Claude (API), brief-frist ~2026-09-23, prosjektfrist ellers åpen (semesterslutt høst 2026)
- (decision) Målgruppe: primært studenter/nyutdannede (matcher oppgavebeskrivelse og motivasjon om å komme i jobb etter studier), med anerkjennelse at konseptet i prinsippet passer alle jobbsøkere
- (decision) Innlogging kreves — begrunnelse: (a) oppgavekrav om sikkerhet for personopplysninger/dokumenter, kryptert lagring anbefalt, (b) bevisst valgt for å heve prosjektets vanskelighetsgrad
- (event) Første utkast av brief.md skrevet, med [ANTAKELSE]-tagger på: bredere målgruppe utover studenter, formell vurderingsrubrikk, innloggingsmetode/krypteringsdetaljer, visjon utover semesteret
- (change) Fjernet kurs-/personattribusjon (IBE160, 15 studiepoeng, 'bygget solo av Kristine', 'kurskrav', 'semester') gjennomgående — briefen leser nå som et produktdokument, ikke en skoleoppgave-merket tekst. Faktiske krav fra oppgaveteksten (sikkerhet, ingen betaling) beholdt som produktkrav.
- (change) Fjernet alle referanser til 'oppgaveteksten' som ekstern kilde — kravene (sikkerhet/innlogging, ingen betaling) fremstår nå som egne produktbeslutninger, ikke sitert fra en lærer-oppgave. Bevisst presentasjonsvalg fra bruker: dokumentet skal lese som egeninitiert idé.
- (decision) Alle 4 [ANTAKELSE]-punkter avklart: (1) målgruppe åpen for alle fra start, studenter er gjennomgående hovedfokus; (2) suksesskriterier holdes kvalitative, ingen prosenttall; (3) sikker innlogging er et krav, implementasjonsdetaljer avklares i PRD/arkitektur; (4) visjon = høyere andel studenter får søknadene reelt vurdert pga. god akademisk skriving som engasjerer arbeidsgiver
- (change) Oversatte gjenværende engelske ord til norsk: 'Executive Summary'->'Sammendrag', 'Hvem dette serves'->'Hvem dette er for' (var skrivefeil), 'moaten'->'det unike fortrinnet', 'parseability'/'match-score'->'maskinlesbarhet'/'treffscore', 'Product Brief'->'Produktbrief' i H1
- (decision) Produktnavn valgt: 'Søknadsassistenten' (norsk, ikke bærer 'KI' i selve navnet). Tittel, H1 og innledningssetning i Sammendrag oppdatert. KI-elementet gjøres eksplisitt i første setning i stedet.
- (decision) Utvidet omfang: verktøyet skal generere/forbedre BÅDE CV og søknadsbrev, ikke bare gi forbedringsforslag til CV. Full generering/Korrektur-modusene gjelder for begge dokumenttyper. Input inkluderer nå eksplisitt en valgfri egenskrevet søknad brukeren allerede har. Oppdatert i Sammendrag, Løsningen, Omfang og Suksesskriterier.
- (change) Lagt til forklaring av ATS (Applicant Tracking System) ved første forekomst i Sammendraget, for lesere som ikke kjenner begrepet
- (change) Byttet 'maskinell parsing' med norsk forklaring: 'tolkes riktig av automatiske systemer' (docx-regenerering venter til filen lukkes i Word)
- (change) La til '(parsing)' i parentes som fagbegrep. Skrev om Suksesskriterier fra +-tegn-liste til løpende prosa (Funksjonelt/Brukeropplevd som avsnitt). docx-regenerering venter fortsatt på at filen lukkes i Word.
- (change) Byttet 'Funksjonelt/Brukeropplevd' til 'Funksjonalitet/Brukeropplevelse' i Suksesskriterier. docx fortsatt låst i Word.
- (change) La til konkret 'Data inn / Data ut'-liste i Suksesskriterier > Funksjonalitet. Word-fil var nå lukket, docx regenerert og synkronisert med alle ventende endringer (parsing i parentes, prosa-omskriving, Funksjonalitet/Brukeropplevelse-navngiving, Data inn/ut-liste).
- (change) Fjernet duplisert Data inn/ut-liste fra Suksesskriterier — den informasjonen ligger allerede naturlig i Løsningen-seksjonen. Suksesskriterier er nå ren prosa (Funksjonalitet/Brukeropplevelse). docx venter på at filen lukkes i Word.
- (change) Byttet Omfang-overskrifter fra 'Med i versjon 1 / Utenfor versjon 1' til 'Inkludert i produktet / Ikke inkludert (bevisst)'. docx venter på at filen lukkes i Word.
- (change) Full klarhetsrunde: fjernet nesten alle skråstreker og nøstede parenteser, skrev om til løpende prosa der det var mulig, byttet 'Input'/'Output' med norske ord, rettet gjenværende 'AI' til 'KI' for konsistens. Også: økt linje-/avsnittsavstand og la til Heading 3 for Omfang-underoverskrifter i docx-generatoren for et ryddigere visuelt uttrykk.
- (change) Satt alle overskrifter (tittel, H1-H3) til svart tekst i docx-generatoren i stedet for standard blå Word-temafarge, på brukerens ønske
- (event) Laget brief-revidert.md/.docx som egen fil (ikke overskrevet original) med de 5 editorial-funnene anvendt: kondensert Sammendrag (fjernet duplisering med Løsningen), kondensert Suksesskriterier>Funksjonalitet (fjernet duplisering med Omfang), flyttet 'åpent for alle'-avsnitt rett etter Primær bruker, la til manglende punktum i Løsningen punkt 2, fjernet dobbel 'de'-bruk i Sammendrag. Original brief.md/.docx er urørt for sammenligning.
- (decision) Bruker godkjente revidert versjon (fra editorial-gjennomgangen). Forfremmet brief-revidert.md/.docx til kanonisk brief.md/.docx, slettet de midlertidige *-revidert-filene.
- (decision) Bruker erklærte produktbriefen ferdig. Status satt til 'final' i frontmatter. Brief avsluttet.
