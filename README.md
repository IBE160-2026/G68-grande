# G68 — Grande

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Medlemmer

- Kristine Rosland Grande

## Søknadsassistenten

> **Status:** Planleggingen er ferdig (brief, PRD, UX og konkurrentanalyse). Arkitektur og koding pågår. Seksjonene merket «kommer» fylles ut når nettsiden er laget.

Søknadsassistenten er en nettside som hjelper studenter med å skrive et søknadsbrev som er skreddersydd til én konkret stilling. Brukeren legger inn CV-en sin og en stillingsannonse, og velger om KI-en skal skrive brevet fra bunnen av (**Full generering**) eller forbedre et brev brukeren har skrevet selv (**Korrektur**). Før brevet skrives, viser nettsiden hvilke krav i annonsen CV-en dekker og mangler (**gap-analyse**), og hvor mange av annonsens nøkkelord som står i CV-en (**nøkkelordtreff**, for eksempel «7 av 10 = 70 %»). Brevet kan lastes ned som Word eller PDF.

**Hvem den er for:** studenter og nyutdannede som søker jobb eller praksisplass for første gang, og som mangler erfaring med hva som fungerer i en søknad. Nettsiden er åpen for alle jobbsøkere, men forklaringene er laget for studenter.

## Installasjon og oppstart

*Kommer.* Her kommer forutsetninger med versjoner, eksakte kommandoer for installasjon og oppstart, innstillingene i `.env.example`, og e-post og passord til testbrukeren. Nettsiden kan kjøres i testmodus uten API-nøkkel.

## Testdata og tester

*Kommer.* Her kommer hvor de fiktive testdataene og fasiten ligger, og hvordan de automatiske testene kjøres.

## Skjermbilder

*Kommer.* To–tre skjermbilder av nettsiden med ekte KI på.

## Kjente begrensninger

Disse er bestemt i [PRD-en](my-project/2-prd/prd.md). Flere kan komme til når nettsiden er laget.

- **Nøkkelordtreffet er bare en ordtelling** og en pekepinn på hvordan et ATS kan vurdere CV-en, ikke en garanti.
- **Bøyningsformer fanges ikke opp:** «prosjektledelse» er ikke et treff i «prosjektleder».
- **Et nøkkelord kan gi treff inne i et annet ord:** «Java» er et treff i «JavaScript». Korte nøkkelord på 1–3 tegn må stå som eget ord, men «C» kan likevel gi feil treff i en liste nummerert med bokstaver.
- **Gap-analysen og nøkkelordtreffet kan si hverandre imot,** fordi gap-analysen er en vurdering KI-en gjør, mens nøkkelordtreffet bare teller ord.
- **I testmodus virker bare de fiktive testdataene.**
- **Ingenting lagres mellom øktene.** CV, annonse og brev forsvinner når brukeren logger ut, så brevet må lastes ned.
- **Brevet skrives bare på norsk** i versjon 1.

## Mappestruktur

*Kommer når koden er på plass.* Foreløpig ligger alle plan- og prosessdokumentene i [`my-project/`](my-project/README.md).

## Plandokumenter

- [Product brief](my-project/1-product-brief/product-brief.md): hva Søknadsassistenten er, og hvem den er for
- [PRD](my-project/2-prd/prd.md): kravene til Søknadsassistenten, med nummererte krav (FR og NFR)
- [Addendum til PRD](my-project/2-prd/addendum.md): notater til UX og arkitektur fra PRD-arbeidet
- UX:
  - [DESIGN.md](my-project/3-ux/DESIGN.md): hvordan nettsiden ser ut, med farger, skrift, former, knapper og bevegelse
  - [EXPERIENCE.md](my-project/3-ux/EXPERIENCE.md): hvordan nettsiden virker, med sidene, tekstene, feilmeldingene, tilgjengelighet og brukerreisene
  - [Skisser](my-project/3-ux/skisser/): skisser av alle sidene på PC, nettbrett og mobil (åpnes i nettleseren)
- [Konkurrentanalyse](my-project/4-konkurrentanalyse/konkurrentanalyse.md): Jobscan, Rezi, Teal og Kickresume, sammenlignet med Søknadsassistenten

## Prosess og KI-bruk

- [Oversikt over alle dokumentene](my-project/README.md): hvert dokument med utkast, tilbakemeldinger, gjennomganger og beslutningslogger
- [Prompt-logg](my-project/prompt-logg.md): de viktigste forespørslene jeg har gitt KI-en underveis
- [Mine valg og KI-feil i UX](my-project/3-ux/mine-valg-og-ki-feil.md): hva jeg bestemte selv, og hvilke feil KI-en gjorde
- [Sesjonslogger](.logs/kristine/README.md): hva som ble gjort i hver arbeidsøkt, med [åpne punkter](.logs/kristine/issues.md)
- [TO DO-liste](my-project/todo.md): hva som er gjort, og hva som gjenstår
