# G68 — Grande

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Medlemmer

- Kristine Rosland Grande

## Søknadsassistenten

> **Status:** Planleggingen er ferdig (brief, PRD, UX, konkurrentanalyse, arkitektur, epics og stories, og sprint planning). Kodingen begynner nå, én story om gangen. Seksjonene merket «kommer» fylles ut når nettsiden er laget.

Søknadsassistenten er en nettside som hjelper studenter med å skrive et søknadsbrev som er skreddersydd til én konkret stilling. Brukeren legger inn CV-en sin og en stillingsannonse, og velger om KI-en skal skrive brevet fra bunnen av (**Full generering**) eller forbedre et brev brukeren har skrevet selv (**Korrektur**). Før brevet skrives, viser nettsiden hvilke krav i annonsen CV-en dekker og mangler (**gap-analyse**), og hvor mange av annonsens nøkkelord som står i CV-en (**nøkkelordtreff**, for eksempel «7 av 10 = 70 %»). Brevet kan lastes ned som Word eller PDF.

**Hvem den er for:** studenter og nyutdannede som søker jobb eller praksisplass for første gang, og som mangler erfaring med hva som fungerer i en søknad. Nettsiden er åpen for alle jobbsøkere, men forklaringene er laget for studenter.

## Installasjon og oppstart

**Forutsetninger:** [uv](https://docs.astral.sh/uv/) versjon 0.12 eller nyere. uv henter selv riktig Python (3.14, låst i `backend/.python-version`, minst 3.12) og alle pakkene. Du trenger ikke installere Python først.

**1. Installer uv** (bare første gang):

- Windows (PowerShell):

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- Mac og Linux:

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

Lukk og åpne terminalen igjen etterpå, så kommandoen `uv` blir funnet.

**2. Start nettsiden** fra mappen der repoet ligger:

```bash
cd backend
uv sync
uv run flask --app soknad run
```

Åpne så <http://127.0.0.1:5000> i nettleseren. Stopp nettsiden med `Ctrl+C` i terminalen. Er port 5000 opptatt (ofte på Mac), starter du med `uv run flask --app soknad run --port 5001` og åpner <http://127.0.0.1:5001>.

**Innstillinger (valgfritt):** nettsiden starter uten noe oppsett. Vil du endre innstillingene, kopierer du `backend/.env.example` til `backend/.env` og fyller inn verdiene der. `.env` havner aldri i Git.

| Innstilling | Hva den gjør | Hvis den er tom |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | Nøkkel til Claude API | Nettsiden kjører i testmodus |
| `ANTHROPIC_MODEL` | Hvilken Claude-modell som brukes | `claude-opus-5-5` |
| `SECRET_KEY` | Signerer innloggingen | En tilfeldig nøkkel lages ved hver oppstart |

*Kommer:* e-post og passord til testbrukeren. Nettsiden kan kjøres i testmodus uten API-nøkkel.

## Testdata og tester

De automatiske testene og kodesjekken kjøres fra `backend/`:

```bash
cd backend
uv run pytest
uv run ruff check
uv run ruff format --check
```

`uv run pytest` kjører alle testene. `uv run ruff check` sjekker koden, blant annet at alle filer åpnes med en oppgitt `encoding` (vi bruker alltid utf-8), og `uv run ruff format --check` sjekker formateringen. De samme sjekkene kjører automatisk på GitHub (fanen «Actions») på både Linux og Windows ved hver PR.

*Kommer:* hvor de fiktive testdataene og fasiten ligger.

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
- [Arkitektur](my-project/5-arkitektur/arkitektur.md): de tekniske valgene (Python og Flask, Claude Opus 5.5, pypdf) og reglene koden skal følge
- [Epics og stories](my-project/6-epics-og-stories/epics.md): kravene delt opp i 8 epics og 31 stories med akseptansekriterier, i den rekkefølgen de skal kodes
- [Sprint-status](my-project/7-sprint-planning/sprint-status.yaml): status for hver story, oppdateres når en story blir ferdig

## Prosess og KI-bruk

- [Oversikt over alle dokumentene](my-project/README.md): hvert dokument med utkast, tilbakemeldinger, gjennomganger og beslutningslogger
- [Prompt-logg](my-project/prompt-logg.md): de viktigste forespørslene jeg har gitt KI-en underveis
- [Mine valg og KI-feil i UX](my-project/3-ux/mine-valg-og-ki-feil.md): hva jeg bestemte selv, og hvilke feil KI-en gjorde
- [Mine valg og KI-feil i arkitekturen](my-project/5-arkitektur/mine-valg-og-ki-feil.md): hva jeg bestemte selv, og hvilke feil gjennomgangen fant
- [Mine valg og KI-feil i epics og stories](my-project/6-epics-og-stories/mine-valg-og-ki-feil.md): hva jeg bestemte selv, og hvilke feil sjekkene fant
- [Sesjonslogger](.logs/kristine/README.md): hva som ble gjort i hver arbeidsøkt, med [åpne punkter](.logs/kristine/issues.md)
- [TO DO-liste](my-project/todo.md): hva som er gjort, og hva som gjenstår
