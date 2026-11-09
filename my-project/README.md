# My project

Her ligger **alt jeg lager selv** i prosjektet – dokumentene for Søknadsassistenten, og utkast som viser hvordan de har utviklet seg.

Hvert dokument har sin egen mappe, nummerert i den rekkefølgen dokumentene ble laget. I mappen ligger gjeldende versjon, utkast, tilbakemeldinger og beslutningslogg, slik at hele utviklingen av dokumentet kan følges på ett sted.

| Fil/mappe | Hva det er |
|---|---|
| **`1-product-brief/`** | |
| [`product-brief.md`](1-product-brief/product-brief.md) | Produktbrief: hva Søknadsassistenten er, og hvem den er for (gjeldende versjon) |
| [`forste-utkast-produktbrief.md`](1-product-brief/forste-utkast-produktbrief.md) | Første utkast av produktbriefen, før faglærers tilbakemelding |
| [`forste-utkast-memlog.md`](1-product-brief/forste-utkast-memlog.md) | Beslutningslogg fra første utkast (16. september), med en merknad om hvorfor oppgaveteksten ikke nevnes i briefen |
| [`tilbakemelding-product-brief.md`](1-product-brief/tilbakemelding-product-brief.md) | Faglærers tilbakemelding på første utkast |
| [`brief-memlog.md`](1-product-brief/brief-memlog.md) | Beslutningslogg: hva som ble bestemt og endret da briefen ble revidert, og hvorfor |
| **`2-prd/`** | |
| [`prd.md`](2-prd/prd.md) | PRD: kravene til Søknadsassistenten, med nummererte krav (FR og NFR) som stories og kode viser til |
| [`addendum.md`](2-prd/addendum.md) | Notater til UX og arkitektur som kom fram under PRD-arbeidet, for eksempel plassering av knapper |
| [`prd-memlog.md`](2-prd/prd-memlog.md) | Beslutningslogg for PRD-en: hva som ble bestemt og endret, og hvorfor |
| [`gjennomganger/`](2-prd/gjennomganger/) | Gjennomgangene av PRD-en: kildesjekk mot brief og tilbakemeldinger, kritisk gjennomgang, og gjennomgang av struktur og språk |
| **`3-ux/`** | |
| [`DESIGN.md`](3-ux/DESIGN.md) | Hvordan nettsiden ser ut: farger, skrift, former, knapper og bevegelse |
| [`EXPERIENCE.md`](3-ux/EXPERIENCE.md) | Hvordan nettsiden virker: sidene, tekstene, feilmeldingene, tilgjengelighet og de tre brukerreisene |
| [`ux-memlog.md`](3-ux/ux-memlog.md) | Beslutningslogg for UX: hvordan nettsiden skal se ut og fungere, og hvorfor |
| [`skisser/`](3-ux/skisser/) | Skisser av alle sidene på PC, nettbrett og mobil, og forslagene jeg valgte mellom (åpnes i nettleseren) |
| [`gjennomganger/`](3-ux/gjennomganger/) | Den kritiske gjennomgangen av UX: sjekkliste, tilgjengelighet og sensor-blikk, en samlet rapport (`validation-report.html`) og språkvasken (`review-struktur-og-sprak.md`) |
| [`mine-valg-og-ki-feil.md`](3-ux/mine-valg-og-ki-feil.md) | Kort oversikt over hva jeg bestemte selv i UX, og hvilke KI-feil jeg fant |
| **`4-konkurrentanalyse/`** | |
| [`konkurrentanalyse.md`](4-konkurrentanalyse/konkurrentanalyse.md) | Konkurrentanalyse av Jobscan, Rezi, Teal og Kickresume, gjort etter UX (se README i mappen) |
| [`konkurrentanalyse-memlog.md`](4-konkurrentanalyse/konkurrentanalyse-memlog.md) | Beslutningslogg for konkurrentanalysen: plan, kilder og påstander |
| [`sokenotater/`](4-konkurrentanalyse/sokenotater/) | Notatene fra hvert søk, som rapporten er skrevet ut fra |
| **`5-arkitektur/`** | |
| [`arkitektur.md`](5-arkitektur/arkitektur.md) | Arkitekturen: de tekniske valgene og reglene (AD-1 til AD-15) som koden skal følge |
| [`arkitektur-memlog.md`](5-arkitektur/arkitektur-memlog.md) | Beslutningslogg for arkitekturen: hva som ble bestemt, alternativene, og hvorfor |
| [`gjennomganger/`](5-arkitektur/gjennomganger/) | Den kritiske gjennomgangen av arkitekturen: mot PRD og UX, sjekkliste, versjoner og en «motstander» som lette etter hull |
| [`mine-valg-og-ki-feil.md`](5-arkitektur/mine-valg-og-ki-feil.md) | Kort oversikt over hva jeg bestemte selv i arkitekturen, og hvilke KI-feil som ble funnet |
| **`6-epics-og-stories/`** | |
| [`epics.md`](6-epics-og-stories/epics.md) | Epics og stories: kravene delt opp i 8 epics og 31 stories med akseptansekriterier, i den rekkefølgen de skal kodes |
| [`mine-valg-og-ki-feil.md`](6-epics-og-stories/mine-valg-og-ki-feil.md) | Kort oversikt over hva jeg bestemte selv i epics og stories, og hvilke KI-feil som ble funnet |
| **`7-sprint-planning/`** | |
| [`sprint-status.yaml`](7-sprint-planning/sprint-status.yaml) | Sprint-status: alle epics og stories med status (backlog, i arbeid, til gjennomgang, ferdig), oppdateres når en story blir ferdig |
| **`9-koding/`** | |
| [`epic-1-context.md`](9-koding/epic-1-context.md) | Sammendrag av planene for epic 1 (innlogging), som KI-en bruker når storiene i epicen kodes |
| [`spec-1-1-nettsiden-starter-fra-en-ny-kopi-av-repoet.md`](9-koding/spec-1-1-nettsiden-starter-fra-en-ny-kopi-av-repoet.md) | Planen for story 1.1 med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 25 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #2](https://github.com/IBE160-2026/G68-grande/pull/2)) |
| [`spec-1-2-logge-inn-med-testbrukeren.md`](9-koding/spec-1-2-logge-inn-med-testbrukeren.md) | Planen for story 1.2 med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 19 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #3](https://github.com/IBE160-2026/G68-grande/pull/3)) |
| [`spec-1-3-registrere-seg-som-ny-bruker.md`](9-koding/spec-1-3-registrere-seg-som-ny-bruker.md) | Planen for story 1.3 med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 16 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #4](https://github.com/IBE160-2026/G68-grande/pull/4)) |
| [`spec-1-4-logge-ut-og-bare-innloggede-kommer-inn.md`](9-koding/spec-1-4-logge-ut-og-bare-innloggede-kommer-inn.md) | Planen for story 1.4 med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 19 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #5](https://github.com/IBE160-2026/G68-grande/pull/5)) |
| [`epic-1-retro-2026-11-08.md`](9-koding/epic-1-retro-2026-11-08.md) | Retrospektiven for epic 1: hva som virket, funn på tvers av storiene, lærdommer om arbeidsmåten og 7 punkter som skal gjøres (godkjent med åpne punkter) |
| [`spec-retro-1-rettinger.md`](9-koding/spec-retro-1-rettinger.md) | Planen for rettingene etter retrospektiven for epic 1, og kodegjennomgangen: alle 13 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #6](https://github.com/IBE160-2026/G68-grande/pull/6)) |
| [`epic-2-context.md`](9-koding/epic-2-context.md) | Sammendrag av planene for epic 2 (gap-analyse og nøkkelordtreff i testmodus), som KI-en bruker når storiene i epicen kodes |
| [`spec-2-1-telleregelen-for-nokkelordtreff.md`](9-koding/spec-2-1-telleregelen-for-nokkelordtreff.md) | Planen for story 2.1 med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 20 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #7](https://github.com/IBE160-2026/G68-grande/pull/7)) |
| [`spec-2-2-fiktive-testdata-og-fasit-for-forste-testcase.md`](9-koding/spec-2-2-fiktive-testdata-og-fasit-for-forste-testcase.md) | Planen for story 2.2 med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 14 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #8](https://github.com/IBE160-2026/G68-grande/pull/8)) |
| [`spec-2-3-testmodus-kjenner-igjen-testdataene.md`](9-koding/spec-2-3-testmodus-kjenner-igjen-testdataene.md) | Planen for story 2.3 med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 15 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #9](https://github.com/IBE160-2026/G68-grande/pull/9)) |
| [`spec-2-4-1-flyten-fra-startsiden-til-innleggingen.md`](9-koding/spec-2-4-1-flyten-fra-startsiden-til-innleggingen.md) | Planen for story 2.4.1 (første halvdel av story 2.4) med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 13 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #10](https://github.com/IBE160-2026/G68-grande/pull/10)) |
| [`spec-2-4-2-testmodus-pa-startsiden-og-merkelappen.md`](9-koding/spec-2-4-2-testmodus-pa-startsiden-og-merkelappen.md) | Planen for story 2.4.2 (andre halvdel av story 2.4) med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 14 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #11](https://github.com/IBE160-2026/G68-grande/pull/11)) |
| [`spec-2-5-1-innleggingssiden.md`](9-koding/spec-2-5-1-innleggingssiden.md) | Planen for story 2.5.1 (første halvdel av story 2.5) med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 20 funn med vurdering, hva som ble rettet og hvorfor resten ble avvist ([PR #12](https://github.com/IBE160-2026/G68-grande/pull/12)) |
| [`spec-2-5-2-analysen-og-forste-resultatside.md`](9-koding/spec-2-5-2-analysen-og-forste-resultatside.md) | Planen for story 2.5.2 (andre halvdel av story 2.5) med oppgaver og akseptansekriterier, og kodegjennomgangen: alle 14 funn med vurdering, hva som ble rettet, hva som ble utsatt og hvorfor resten ble avvist ([PR #13](https://github.com/IBE160-2026/G68-grande/pull/13)) |
| **Felles** | |
| [`prompt-logg.md`](prompt-logg.md) | De viktigste forespørslene jeg har gitt KI-en (Claude Code) underveis, for alle dokumentene |
| [`todo.md`](todo.md) | TO DO-liste: hva som er gjort og hva som gjenstår, krysses av underveis |
| [`../.logs/kristine/`](../.logs/kristine/) | Sesjonsloggene: hva som ble gjort i hver arbeidsøkt, og listen over åpne punkter (`issues.md`). Ligger i roten av repoet, fordi faglærers regler sier det |

**Slik jobber jeg:** BMAD lager arbeidsutkast i `_bmad-output/` på min PC. Når et dokument er klart, legger jeg det her. Viktige mellomversjoner, beslutningslogger og prompts legges også her, slik at prosessen kan følges i Git-historikken.

Word-filer (`.docx`) bruker jeg bare som lesekopier på min PC. De lastes ikke opp til GitHub.
