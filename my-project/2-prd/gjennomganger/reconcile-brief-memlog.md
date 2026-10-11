# Avstemming: brief-memlog mot PRD og addendum

**Kilde:** `my-project/1-product-brief/brief-memlog.md` (beslutningslogg fra product brief)
**Sjekket mot:** `prd.md`, `addendum.md` og `.memlog.md` (PRD-loggen). Senere beslutninger i PRD-loggen overstyrer brief-loggen og regnes ikke som hull.
**Dato:** 2026-10-10

## Konklusjon

Ingen alvorlige hull. Nesten alle beslutningene i brief-loggen er tatt med i PRD-en, enten som krav (FR/NFR), i kuttlisten eller i suksesskriteriene. Det som mangler, er noen få detaljer og begrunnelser: valget av KI-tjeneste (Claude), at OAuth er utelatt, og at noen ting skulle avklares i arkitekturen.

## Hull

### 1. Valget av KI-tjeneste (Claude/Anthropic) er ikke nevnt

- **Logglinje:** «(decision) KI-tjeneste: Claude (Anthropic) API, med testmodus med ferdige svar. Detaljer (modell, kostnad) avklares i arkitektur»
- **PRD:** Sier bare «ekstern KI» (FR-32, FR-35, FR-36) og «API-nøkkel» (NFR-2). Hverken PRD eller addendum sier at det er Claude-API-et som er valgt, eller at modell og kostnad skal avklares i arkitekturen.
- **Alvorlighet:** middels (beslutningen er tatt, og arkitekturen trenger den, men den hører strengt tatt ikke hjemme i FR-ene)
- **Forslag:** Legg et punkt i addendum under «Til arkitektur»: «KI-tjeneste: Claude (Anthropic) API er valgt i brief. Modell og kostnad avklares i arkitekturen.»

### 2. Metoden for å lese PDF skulle avklares i arkitekturen

- **Logglinje:** «(decision) PDF: appen leser tekst-PDF; skannet/uleselig PDF gir beskjed om å lime inn tekst. Metode avklares i arkitektur»
- **PRD:** FR-11 dekker oppførselen (uleselig PDF gir beskjed om å lime inn). At metoden skal avklares i arkitekturen, står ikke i addendum. Der står bare filstørrelsen.
- **Alvorlighet:** lav
- **Forslag:** Legg til under «Til arkitektur» i addendum: «PDF-lesing (FR-11): hvordan teksten hentes ut av PDF-en, avklares i arkitekturen.»

### 3. OAuth er ikke med i kuttlisten

- **Logglinje:** «(decision) Innlogging: enkel registrering e-post/passord (hashet), lokal database, én ferdig testbruker for sensor. Ikke glemt passord, e-postbekreftelse, OAuth eller kryptering i v1»
- **PRD:** Kuttlisten har med kryptering, glemt passord og bekreftelse på e-post, men ikke OAuth (innlogging med for eksempel Google). NFR-5 («fungerer lokalt uten noen ekstern tjeneste») utelukker det i praksis, men det står ikke uttrykkelig.
- **Alvorlighet:** lav
- **Forslag:** Utvid raden i kuttlisten til «… glemt passord, bekreftelse på e-post og innlogging med Google eller lignende (OAuth)».

### 4. Begrunnelsen for kun norsk har falt bort

- **Logglinje:** «(decision) Kun norsk i v1 for å halvere testomfang»
- **PRD:** Kuttlisten har «Engelsk språk og valg av tone» med den felles begrunnelsen «Kjerneflyten først». Den konkrete begrunnelsen (halvert testomfang) er borte. PRD-loggen sier at brukeren mente den felles begrunnelsen holder foreløpig, så dette er et bevisst valg.
- **Alvorlighet:** lav
- **Forslag:** Valgfritt: skriv «Halverer testomfanget» som begrunnelse for engelsk. Kan også la det stå, siden brukeren har godtatt den felles begrunnelsen.

### 5. «Ferdig testbruker» er noe uklart

- **Logglinje:** «… én ferdig testbruker for sensor»
- **PRD:** NFR-8 sier «med eksakte kommandoer og en testbruker», og suksesskriterium 6 sier «testbrukeren fra README virker». Det står ikke uttrykkelig at testbrukeren finnes ferdig i databasen når nettsiden startes, slik at sensor ikke trenger å registrere seg.
- **Alvorlighet:** lav
- **Forslag:** Presiser i NFR-8: «… og en ferdig opprettet testbruker (e-post og passord står i README)».

## Sjekket og funnet i orden

- V1 lager bare søknadsbrev, CV er bare input: Visjon og kuttlisten (CV-forbedring utsatt).
- PDF eller innlimt tekst inn: FR-8, FR-11.
- Word og PDF ut, begrunnelse for Word framfor Markdown: del 2.5, FR-29.
- Kun norsk og formell tone: FR-24, kuttlisten.
- Passord hashet, lokal database, ingen glemt passord, e-postbekreftelse eller kryptering: NFR-1, NFR-4, NFR-5, kuttlisten.
- Testmodus med ferdige KI-svar uten API-nøkkel: FR-32 til FR-34, suksesskriterium 7.
- Nøkkelordtreff regelbasert, KI lager listen, brukeren kan ikke rette den i v1: FR-15 til FR-17, kuttlisten.
- ATS beskrevet generelt, uten de udokumenterte tallene: Problemet i Visjon.
- Suksesskriterier med 2–3 fiktive CV-er og fasit; fiktive data i egen mappe; nøkler og ekte CV-er aldri i Git: del 5, NFR-2, NFR-3.
- Korrektur med rødt/grønt i appen og ren tekst ved nedlasting; spor endringer utsatt: FR-23, FR-30, kuttlisten.
- Både gap-analyse og nøkkelordtreff beholdt: FR-14 til FR-18.
- Ingen lagring av CV, annonse eller brev mellom gangene: NFR-4.
- «Kopier tekst» kuttet: kuttlisten.
- Beskjed i appen om ekstern KI: FR-35 (utvidet med samtykke i FR-36).
- Oversikt over tidligere søknader er ikke en del av prosjektet: del 4.
- Målgruppe og visjon (brukerens originaltekst gjenopprettet i brief): beholdt i Visjon.
