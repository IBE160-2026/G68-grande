---
title: "Avstemming: product brief mot PRD"
kilde: my-project/1-product-brief/product-brief.md (status final, updated 2026-10-09)
sammenlignet med: prd.md, addendum.md (samme mappe)
dato: 2026-10-10
---

# Avstemming: product brief mot PRD

Bevisste endringer i `.memlog.md` er ikke regnet som hull: «app» -> «nettside», modus velges tidlig (FR-20), «kun søknad» kuttet, redigering i nettleseren kuttet, ordstamme kuttet, topp- og bunntekst kuttet, samtykke lagt til, suksesskriterium 5 utvidet. Rene ordlydsforskjeller er ikke tatt med.

Totalt: 7 hull (1 høy, 4 middels, 2 lav).

---

## 1. Målgruppens kjernebehov: oversette utdanning og prosjekter til kvalifikasjoner (HØY)

**Briefen sier** («Hvem dette er for»):
> «De vet gjerne hva de kan, men ikke hvordan det oversettes til det en rekrutterer eller et ATS-system leter etter.»
> «… designet holder studentens situasjon som hovedfokus gjennomgående: lite arbeidserfaring, og behov for å oversette utdanning og prosjekter til relevante kvalifikasjoner.»

**PRD-en sier:** «Hvem dette er for» er forkortet, og begge setningene er borte. Ingen FR sier at brevet skal løfte fram utdanning, studieprosjekter og frivillig arbeid som kvalifikasjoner når arbeidserfaringen er liten. FR-22 sier bare «basert på CV-en og stillingsannonsen».

**Hvorfor det betyr noe:** Dette er det som gjør verktøyet til et *studentverktøy* og ikke et generelt verktøy. Det må inn i KI-instruksen for brevet, og uten et krav blir det ikke testet. Det kan også se ut til å kollidere med FR-37 (ingen antakelser): å *omformulere* et studieprosjekt som en relevant kvalifikasjon er lov, å *finne på* erfaring er ikke lov. Grensen bør stå skrevet.

**Forslag:** Ta de to setningene tilbake i «Hvem dette er for» med brukerens ordlyd. Legg til en presisering i FR-22/FR-23 eller FR-37, for eksempel: «Brevet løfter fram utdanning og prosjekter fra CV-en som relevante kvalifikasjoner når arbeidserfaringen er liten, men legger ikke til noe som ikke står i CV-en.»

---

## 2. Visjonen fra briefen mangler: hvilken kvalitet brevet skal ha (MIDDELS)

**Briefen sier** («Visjon»):
> «Målet er en høyere andel studenter som får søknadene sine reelt vurdert av arbeidsgivere — fordi søknadene er skrevet på en god, akademisk måte som gjør arbeidsgiver oppmerksom og engasjert, i stedet for silt ut før noen har lest dem.»

**PRD-en sier:** Del 1 heter «Visjon», men inneholder sammendraget fra briefen. Selve visjonssetningen er ikke med. Om brevets kvalitet sier PRD-en bare «norsk og formell tone» (FR-24) og «nevner krav som er spesifikke for annonsen» (suksesskriterium 3).

**Hvorfor det betyr noe:** «God, akademisk måte» og «gjør arbeidsgiver oppmerksom og engasjert» sier mer om tonen enn «formell». Det er dette målet KI-instruksen skal styres mot, og det forklarer *hvorfor* produktet finnes.

**Forslag:** Legg visjonssetningen inn i del 1 med brukerens ordlyd (for eksempel som første eller siste avsnitt under «Visjon»). Vurder å utvide FR-24 med en kort beskrivelse av tonen, for eksempel «formell, saklig og engasjerende, ikke generisk».

---

## 3. «Hvorfor» bak nøkkelordtreffet: ATS-pekepinn for studenten (MIDDELS)

**Briefen sier** («Sammendrag»):
> «Mange arbeidsgivere bruker et ATS (Applicant Tracking System), altså programvare som sorterer søknader automatisk før et menneske leser dem. Nøkkelordtreffet gir studenten en enkel og forståelig pekepinn på hvordan CV-en kan bli vurdert.»

Problemdelen (som PRD-en har med) sier at studenter ikke vet om ATS og ikke forstår *hvorfor* de blir silt ut.

**PRD-en sier:** ATS nevnes bare i problemdelen. Del 2.3 forklarer hvordan treffet regnes ut (FR-17) og at det kan si imot gap-analysen (FR-18), men ingen FR sier at nettsiden forklarer brukeren *hva* nøkkelordtreffet betyr, altså at det er en pekepinn på ATS-filtrering, og at det er en pekepinn, ikke en garanti.

**Hvorfor det betyr noe:** Problemet briefen løser er delvis et kunnskapsproblem. Uten en forklaring ser studenten bare et tall.

**Forslag:** Utvid FR-18 eller legg til en ny FR: «Nettsiden forklarer kort hva et ATS er, og at nøkkelordtreffet er en enkel pekepinn på hvordan CV-en kan bli vurdert, ikke en garanti.» Legg gjerne til en setning i innledningen til 2.3 om hvorfor treffet finnes.

---

## 4. Designprinsippet «enkel og tydelig fremfor bredde» er borte (MIDDELS)

**Briefen sier** («Hva gjør dette annerledes»):
> «Den ærlige begrensningen: det unike fortrinnet er ikke teknisk sofistikasjon, men at fokuset på studentmålgruppen og de to modusene gir en enkel, tydelig opplevelse fremfor bredde.»

Og: «Ved å tilby Korrektur som et likeverdig alternativ til Full generering, anerkjenner produktet det problemet direkte i stedet for å late som det ikke finnes.»

**PRD-en sier:** Avsnittet er forkortet til én setning om Korrektur. «Den ærlige begrensningen» og prinsippet om enkelhet fremfor bredde er ikke med noe sted.

**Hvorfor det betyr noe:** Dette er et prinsipp UX og arkitektur skal bygge på, og det begrunner kuttlisten. Det er også brukerens egne ord (jf. ønsket om å beholde brukerens ordlyd).

**Forslag:** Ta inn «Den ærlige begrensningen …»-setningen i «Hva gjør dette annerledes» med brukerens ordlyd. Vurder å vise til den i innledningen til del 4 (Omfang).

---

## 5. Valg av KI-tjeneste (Claude via API) står ikke i PRD eller addendum (MIDDELS)

**Briefen sier** («Teknisk retning»):
> «KI-tjeneste: Claude (Anthropic) via API. Modell, kostnad og håndtering av nøkkelen avklares i arkitekturen.»

**PRD-en sier:** Bare «ekstern KI» (FR-32, FR-35, FR-36). Addendum «Til arkitektur» har bare filstørrelse.

**Hvorfor det betyr noe:** Det er en tatt beslutning som arkitekturen trenger, og den forsvinner hvis briefen ikke leses.

**Forslag:** Legg til i addendum, «Til arkitektur»: «KI-tjeneste: Claude (Anthropic) via API, valgt i briefen. Modell, kostnad og håndtering av nøkkelen avklares i arkitekturen.» (PRD-en kan gjerne fortsatt si «ekstern KI».)

---

## 6. Korrektur: begrunnelsen «beholder kontrollen over sin egen stemme» er tatt ut av funksjonen (LAV)

**Briefen sier** («Løsningen», punkt 4): «Slik ser brukeren hva som er endret og beholder kontrollen over sin egen stemme.»

**PRD-en sier:** FR-23 beskriver markeringen, men ikke hvorfor. «Egen stemme» står i del 1, så tanken er ikke helt borte.

**Forslag:** Legg til begrunnelsen som en setning i FR-23 eller i innledningen til 2.4. Kan også gi en føring for KI-instruksen: Korrektur skal forbedre brevet, ikke skrive det om til en ny tekst.

---

## 7. Testdata: fasitene og begrunnelsen for testmodus (LAV)

**Briefen sier** («Teknisk retning»): «Det gjør at sensor og automatiske tester ikke trenger nøkkel, og at testing ikke koster penger.» og «Fiktive test-CV-er, annonser og fasiter ligger i en egen mappe i repoet.»

**PRD-en sier:** NFR-3 sier at fiktive testdata ligger i en egen mappe, men nevner ikke fasitene. Begrunnelsen (gratis testing, automatiske tester uten nøkkel) er ikke med.

**Forslag:** Utvid NFR-3: «… fiktive test-CV-er, stillingsannonser og fasiter ligger i en egen mappe.» Begrunnelsen kan legges i innledningen til 2.6.

---

## Sjekket og funnet dekket

Problemet, primær bruker, «egen stemme»-suksess, Word-begrunnelsen, fast telleregel, PDF/tekst inn og uleselig PDF, markering rødt/grønt, norsk og formell tone, nedlasting .docx/PDF uten markeringer, ingen lagring mellom øktene, hashet passord, API-nøkkel og ekte CV-er utenfor Git, KI-merknad når testmodus er av, README med testbruker, alle 7 suksesskriterier, alle punkter under «Ikke inkludert» og «Ikke en del av prosjektet».
