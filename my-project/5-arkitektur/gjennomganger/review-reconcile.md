# Avstemming: arkitektur-spine mot PRD, addendum og UX

- **Gjennomgått:** `ARCHITECTURE-SPINE.md` (2026-11-04) og `.memlog.md`
- **Kilder:** `prd.md`, `addendum.md`, `EXPERIENCE.md`, `DESIGN.md` (bare tekniske punkter)
- **Dato:** 2026-11-04
- **Spinen er ikke endret.**

## Konklusjon

Spinen dekker de store valgene godt. Alle punktene PRD-en sendte til arkitekturen (filstørrelse, KI-modell og kostnad, ventetid, PDF-bibliotek, kolonner og tabeller, gjenkjenning av testdata, mapper, ett språk) er besvart, og det samme gjelder UX-spørsmålene (Korrektur-formatet, tilbakeknappen, «Nytt forslag» i testmodus, Baloo 2 lokalt). Men noen stille krav har falt ut, og tre regler går mot kildene. Det gjelder: (1) hvor lenge hver del av øktdataene skal vare, (2) at feil skal kastes som unntak, mens UX vil vise alle feilene samtidig, og (3) at nettsiden må starte uten `.env`. Ingen av funnene stopper arbeidet, men 1–3 bør rettes før epics og stories lages.

Alvorlighet: **kritisk** = blokkerer et suksesskriterium eller en sensorflyt · **høy** = en AD-regel går mot en kilde, eller den vil føre til feil kode · **middels** = stille krav som mangler et sted å høre til · **lav** = presisering.

---

## Høy

### R-1 — Øktdataene har ikke regler for hvor lenge hver del varer (AD-7 mot UX)

- **Spine:** AD-7 (linje 95) legger «modus, steg, CV, …, samtykke, testmodus» i *ett* objekt, og sier at «Lag ny søknad» tømmer søknaden.
- **Kilder:**
  - Bryteren for testmodus skal huske valget **så lenge man er logget inn** (EXPERIENCE linje 203 og 262). Altså skal den *ikke* tømmes med søknaden.
  - Samtykket skal krysses av på nytt **hver gang startsiden åpnes**, også i samme økt (EXPERIENCE linje 279, og tabellen med avvik på linje 421, som er strengere enn FR-36).
  - Å **komme til startsiden** (også via «Tilbake» på modusvalget) starter alltid en ny søknad med tomme felt og ny nøkkelordliste (EXPERIENCE linje 257). Spinen nevner bare «Lag ny søknad».
  - «Tilbake» fra innleggingen til modusvalget beholder CV og annonse (EXPERIENCE linje 63), også når man bytter modus.
  - «Lastet ned» nullstilles når man ber om «Nytt forslag» (EXPERIENCE linje 217 og 276).
- **Risiko:** Leser en utvikler AD-7 bokstavelig, blir testmodus slått av ved «Lag ny søknad», eller samtykket blir stående til neste søknad. Det bryter FR-32 og FR-36 (suksesskriterium 9).
- **Forslag:** Del objektet i to: *innlogging* (bruker-id, testmodus) og *søknad* (alt det andre, også samtykket). Skriv regelen: «GET startsiden = ny søknad (søknaden tømmes, samtykket nullstilles), testmodus beholdes.»

### R-2 — AD-9 kaster feil som unntak, men UX vil vise alle feilene samtidig

- **Spine:** AD-9 (linje 107): kjernen og adapterne «kaster bare `InndataFeil(felt, type)` …».
- **Kilde:** EXPERIENCE linje 267: alt sjekkes først når man trykker «Sjekk CV-en min», og «feilboksen [kommer] øverst med alle feilene samtidig», én linje per felt (linje 133–143). FR-9 sier også at brukeren får vite hva som mangler.
- **Risiko:** Når koden kaster et unntak, stopper den ved den første feilen. Er både CV-en tom og annonsen av feil filtype, ser brukeren bare den ene feilen. Det samme gjelder registreringen (e-post finnes og passordene er ikke like).
- **Forslag:** Sjekken av inndata *returnerer* en liste med `InndataFeil`, i stedet for å kaste. Unntak brukes bare for KI-, PDF- og filfeil. Skriv også ned alle verdiene `type` kan ha for hver feiltype. Linje 107 sier nå at `type` er «nettverk, annet eller ubrukelig_svar» for *alle* tre feiltypene. Det stemmer bare for `KIFeil`. `InndataFeil` trenger for eksempel `tom`, `feil_filtype`, `for_stor`, `ikke_testdata`, `epost_finnes`, `epost_ugyldig`, `passord_kort`, `passord_ulike` og `feil_innlogging`, og `PdfFeil` trenger `uleselig`.

### R-3 — Nettsiden må starte uten `.env`, og `SECRET_KEY` er ikke nevnt

- **Spine:** AD-12 (linje 130): «Innstillingene leses fra `.env`». AD-10 (linje 113): mangler nøkkelen, er testmodus låst på.
- **Kilder:** NFR-12 (prd linje 171): README prøves fra en ny kopi av repoet «uten `.env` og andre lokale filer». Suksesskriterium 7 (prd linje 239): nettsiden kjører i testmodus uten API-nøkkel. NFR-8 (prd linje 158) sier 10–15 minutter.
- **Hull:** Den signerte cookien i AD-7 krever en `SECRET_KEY`. Spinen sier ikke hvor den kommer fra. Hvis koden krever den fra `.env`, krasjer nettsiden for sensor.
- **Forslag:** Ny regel i AD-12: nettsiden starter uten `.env`. Mangler `SECRET_KEY`, lages en tilfeldig nøkkel ved oppstart. Det går fint, fordi øktene uansett forsvinner ved omstart. Mangler `ANTHROPIC_MODEL`, brukes standardmodellen. Bare `ANTHROPIC_API_KEY` slår på vanlig modus.

---

## Middels

### R-4 — AD-2 påstår at alt NFR-9 krever tester av, ligger i `kjerne/`

- **Spine:** AD-2 (linje 58): «Alle regler som NFR-9 krever tester av, ligger i `kjerne/`.»
- **Kilde:** NFR-9 (prd linje 169) krever også tester av innloggingen (FR-1, FR-3: `adaptere/db.py` og werkzeug), av at sider krever innlogging (FR-7: `login_required` i `web/`) og av at nedlastet fil er uten markeringer (FR-30: `adaptere/fil_ut.py`).
- **Forslag:** Endre setningen til at regler *uten I/O* ligger i kjernen. Legg til at web- og adaptertester bruker Flask sin test-klient med `TestKI` og en midlertidig SQLite-database. Da står det også hvordan FR-7 og FR-30 testes.

### R-5 — Telleregelen: avrundingen og ordet «ord-grenser»

- **Spine:** AD-6 (linje 89): «med Pythons `re` og ord-grenser som gjelder æ, ø og å».
- **Kilde:** FR-17 (prd linje 76–78):
  - Nøkkelord på 4 tegn eller mer gir treff **også som del av et lengre ord** («Python» i «python-utvikler»). Bare nøkkelord på 1–3 tegn må stå som eget ord.
  - Prosenten rundes til **nærmeste hele tall** («2 av 3 = 67 %»).
- **Risiko:**
  - «Ord-grenser» kan leses som at alle nøkkelord må stå som eget ord. Det går mot regelen om delord.
  - Pythons `round()` runder halve tall til nærmeste partall: `round(12.5)` gir 12, mens vanlig avrunding gir 13 (for eksempel 1 av 8). Det kan gi feil mot fasiten (suksesskriterium 2).
  - `\b` virker ikke for korte nøkkelord med tegn som ikke er bokstaver, for eksempel «C#», «C++» og «.NET».
- **Forslag:** Skriv regelen rett inn i AD-6: delord og uten forskjell på store og små bokstaver (`casefold`) for 4 tegn eller mer. For 1–3 tegn: bokstaven eller tallet foran og bak er ikke en bokstav eller et tall (`(?<!\w)…(?!\w)` med `re.UNICODE`). Avrunding med `Decimal(...).quantize(ROUND_HALF_UP)` eller `int(x + 0.5)`. Ta med testtilfeller for 12,5 % og for «C#».

### R-6 — Ingen regel for hvor FR-24 og FR-37 hører hjemme

- **Spine:** I tabellen Krav → arkitektur (linje 220) står FR-37 under AD-3–AD-5, AD-9 og AD-13. Ingen av dem sier noe om innholdet i brevet. FR-24 er ikke nevnt i det hele tatt (bare listen over KI-fraser, under Utsatt).
- **Kilder:** FR-24 (prd linje 92–97): brevet er på norsk og i formell tone, nevner stillingen og arbeidsgiveren, viser til minst to krav og bruker ingen KI-fraser. I Korrektur beholdes innhold, eksempler og rekkefølge. FR-37 (prd linje 98) står blant «Kuttes aldri» (prd linje 223). Suksesskriterium 11 og 12 sjekker begge.
- **Forslag:** En kort AD eller konvensjon: `prompts/brev.md` og `prompts/korrektur.md` *skal* inneholde reglene i FR-24 og FR-37, og KI-en får bare CV, annonse og eventuelt eget brev. `fasit.md` har en sjekkliste for kriterium 11 og 12. Spinen bør også si om KI-en får stillingstittelen. Memlog linje 23 sier «arbeidsgiver/stilling», men skjemaet i AD-4 (linje 74) har bare `arbeidsgiver`.

### R-7 — Nedlastingen passer ikke med «POST → redirect → GET», og «Filen kan ikke lages» har ingen feiltype

- **Spine:** AD-8 (linje 101): «Alle skjema bruker POST → redirect → GET». AD-9 har bare `InndataFeil`, `PdfFeil` og `KIFeil`.
- **Kilder:**
  - Nedlastingen gir en fil, ikke en redirect. Knappen skal deretter bli grønn, filnavnet skal vises, og vinduet skal åpnes (EXPERIENCE linje 216).
  - Serveren må vite at brevet er lastet ned (vinduet «Logg ut før nedlasting», linje 277).
  - «Vi klarte ikke å lage filen. Prøv på nytt.» skal vises som en rød boks på brevsiden (EXPERIENCE linje 170 og 275).
- **Forslag:** Skriv nedlastingen som et unntak fra regelen: `GET /last-ned/<docx|pdf>` lager filen, setter `lastet_ned` i økten og sender filen. Litt JavaScript oppdaterer knappen og åpner vinduet. Legg til `FilFeil` i AD-9 og en tekst for den i `tekster.py`.

### R-8 — For stor forespørsel (413) og opplastede filer etter en feil

- **Spine:** AD-11 (linje 120): høyst 5 MB per fil, og `MAX_CONTENT_LENGTH` er 16 MB.
- **Kilder:** FR-12 sier at brukeren får en feilmelding om at filen er for stor. EXPERIENCE linje 140 har teksten «Den kan være på høyst X MB». FR-28 og EXPERIENCE linje 183 sier at det brukeren har lagt inn, ikke er borte.
- **Hull:**
  1. En fil over 16 MB gir Flask sin vanlige side for «413 Request Entity Too Large». Brukeren ser ikke feilboksen, og alt i skjemaet er borte.
  2. Når siden vises på nytt etter en feil i innleggingen, er filfeltene i nettleseren tomme. Det er umulig å fylle dem ut igjen fra serveren. Skal feltene som var riktige, fortsatt vise «filnavn ✓», må serveren lagre teksten og filnavnet i økten. AD-7 har ikke filnavnet med.
- **Forslag:** En egen feilhåndterer for 413 som viser feilboksen med «for stor fil». Felt uten feil lagres i økten med filnavnet, selv om et annet felt har feil.

### R-9 — FR-38: det finnes ikke noe skript som lager de ferdige KI-svarene

- **Kilde:** FR-38 (prd linje 139): de ferdige svarene er *ekte* KI-svar, laget ved å kjøre testdataene gjennom KI-en. AD-10 krever to brev og to korrekturer per testcase.
- **Spine:** Startstrukturen (linje 179–197) har ikke noe verktøy for dette. Den sier heller ikke at svarene lagres slik `EkteKI` får dem, før kontrollen.
- **Forslag:** Legg til `scripts/lag_testsvar.py` (eller en egen `flask`-kommando). Det kjører `EkteKI` på hvert testcase og skriver `ki-svar/*.json`. `TestKI` sender svarene gjennom den samme kontrollen i `kjerne/` (AD-4). Da er det sikkert at testmodus og vanlig modus får samme form på svarene (AD-3).

### R-10 — Gjenkjenningen av testdata: hvilket felt får feilen, og tåler den PDF-tekst?

- **Spine:** AD-10 (linje 113): teksten vaskes («alle tegn med mellomrom fjernes»), og et testcase gjenkjennes når CV, annonse og eget brev matcher *samme* case.
- **Kilder:**
  - Feilen gjelder ett felt: «CV: I testmodus fungerer bare …» (EXPERIENCE linje 141 og 394).
  - Addendum linje 36 sier at gjenkjenningen skal tåle ekstra linjeskift og mellomrom.
  - Suksesskriterium 5 (prd linje 237) krever at PDF og innlimt tekst gir samme treff.
- **Hull:**
  1. Spinen sier ikke hvilket felt feilen gjelder når CV-en hører til case 1 og annonsen til case 2, eller når ingenting matcher.
  2. Tekst fra pypdf kan skille seg fra `.txt`-filen på mer enn mellomrom: orddeling, ligaturer som «ﬁ», tegn for punktlister og sidetall. Bare å fjerne mellomrom holder kanskje ikke.
  3. Ordene «alle tegn med mellomrom» er uklare. Memlog linje 29 sier «alt mellomrom og alle linjeskift».
- **Forslag:** Sjekk hvert felt for seg. Gi `ikke_testdata` på feltet som ikke matcher noe case, eller på det som ikke matcher samme case som CV-en. Vask med Unicode-normalisering (`NFKC`) og fjern alt som ikke er bokstaver eller tall. Eller kjenn igjen en PDF på en hash av filen, i tillegg til vasket tekst. Prøv dette i den første PDF-storyen sammen med prøven av kolonner.

### R-11 — AD-5 kan ikke oppdage at KI-en har sløyfet en setning

- **Spine:** AD-5 (linje 83): «Nettsiden sammenligner aldri tekst selv.»
- **Kilder:** FR-24 og suksesskriterium 12 sier at innholdet og rekkefølgen beholdes. UX viser «N setninger er fjernet» (EXPERIENCE linje 162 og 231).
- **Risiko:** Tar KI-en bort en gammel setning uten å sende den med `ny: null`, forsvinner innholdet uten at brukeren får vite det. Telleren for fjernede setninger blir da feil. FR-28 sier heller ikke hva et ubrukelig korrektursvar er. Er alle `ny` null, blir brevet tomt.
- **Forslag:** Tillat én kontroll i `kjerne/ki_svar`: settes alle `gammel` sammen, skal de (vasket) bli det opprinnelige brevet. Hvis ikke, kastes `KIFeil(ubrukelig_svar)`. Legg også til at et brev uten setninger (alle `ny` er null) er ubrukelig. Visningen sammenligner fortsatt ikke selv.

---

## Lav

- **R-12 — Mangler økten etter en omstart:** Etter en omstart er minnet tomt, men nettleseren har fortsatt en gyldig cookie med bruker-id. `login_required` slipper da brukeren gjennom, men det finnes ingen økt. Regel: mangler økten, behandles brukeren som utlogget og får «Du må logge inn først» (FR-7). Økter som aldri logges ut, ligger i minnet til omstart. Det er greit lokalt, men skriv det ned.
- **R-13 — Til startsiden etter innlogging:** EXPERIENCE linje 251 sier at man alltid kommer til startsiden etter innlogging, også når man ble sendt dit med «Du må logge inn først». Den vanlige `login_required` legger til `next=`. Skriv at `next` ikke brukes.
- **R-14 — Filnavnet:** AD-11 (linje 123) sier «æøå byttet ut». UX sier mer presist æ → ae, ø → o, å → a (EXPERIENCE linje 240). Andre tegn som ikke er lov i filnavn (`/ \ : * ? " < > |`, `&`, é og ü i navnet på arbeidsgiveren) er ikke nevnt. Gjør om til ASCII og ta bort alt annet enn `[A-Za-z0-9-]`.
- **R-15 — Ventetiden for hele handlingen:** AD-13 sier 90 s per kall med 1 nytt forsøk. «Sjekk CV-en min» gjør to kall (nøkkelord og gap), så verste fall er rundt 6 minutter med ventetegn og uten avbryt-knapp (EXPERIENCE linje 221). Vurder en grense for hele handlingen. Dessuten sier Utsatt (linje 236) at «eksakt tidsgrense» er utsatt, mens AD-13 fastsetter 90 s. Skriv «90 s som startverdi».
- **R-16 — Avvist POST mens KI jobber:** AD-8 (linje 101) avviser POST mens et kall pågår, men sier ikke hva brukeren ser. Trolig blir brukeren sendt tilbake til siden for steget. Skriv det ned. Øktlageret trenger en lås, fordi Flask sin utviklingsserver kjører flere tråder.
- **R-17 — Testmodus kan bare byttes på startsiden:** FR-32 sier at testmodus ikke kan byttes midt i en søknad. Serveren bør avvise at bryteren endres hvis steget ikke er `start`. Spinen sier det ikke uttrykkelig.
- **R-18 — Feilene i testmodus kommer i en bestemt rekkefølge:** FR-34 og EXPERIENCE linje 346: tomt felt, feil filtype og uleselig PDF skal virke også i testmodus. Sjekken av testdata må altså komme *etter* disse. Skriv rekkefølgen.
- **R-19 — `binds` lover mer enn spinen gir:** Front-matter binder NFR-1–NFR-12, men NFR-6 og NFR-7 (tilgjengelighet og bredder) er ikke med i tabellen Krav → arkitektur. NFR-12 (testplanen) har ikke noe sted i mappestrukturen. Legg til en linje: «NFR-6 og NFR-7: maler og CSS etter DESIGN.md og EXPERIENCE.md», og et sted for testplanen (for eksempel `docs/testplan.md`).
- **R-20 — JavaScript-listen i AD-1:** Listen (linje 52) nevner Korrektur-klikk, vinduer, ventetegn og låste knapper. UX trenger også dette:
  - innleggingsfeltene (filnavnet vises med en gang, «Lim inn tekst» åpner en tekstboks, søppelbøtta)
  - «i»-boksen
  - fyrverkeriet og prosentlinjen
  - fokus og `inert`
  - bryteren for testmodus

  Skriv at listen er eksempler, ikke alt, så ingen tror at mer JavaScript er forbudt.
- **R-21 — Tabeller i CV-en:** Addendum linje 21 sier at Kristine vil prøve å støtte tabeller, og at de settes på kuttlisten i PRD-en hvis det blir vanskelig. Spinen (Utsatt, linje 231) nevner bare README. Etter regelen om PRD-en under kodingen (addendum linje 56) skal PRD-en og beslutningsloggen også oppdateres.

## Avstemt uten avvik (stikkprøve)

- Fra PRD-en til arkitekturen: filstørrelsen (5 MB), modellen og kostnaden (Opus 5.5, tak på 250 kr), ventetiden (90 s), pypdf, python-docx og fpdf2, kolonner (prøve, ellers README), gjenkjenning av testdata og mappene for den, ett språk (Python).
- Fra UX til arkitekturen: formatet på korrekturen (setningspar), tilbakeknappen i nettleseren (AD-8), «Nytt forslag» i testmodus (bytter mellom brev-1 og brev-2), Baloo 2 lokalt (AD-12, DESIGN linje 333), arbeidsgiver i nøkkelordsvaret, ingen automatisk utlogging.
- NFR-1, NFR-2, NFR-3, NFR-4, NFR-5, NFR-10 og NFR-11 er dekket av AD-7, AD-12 og AD-13 og konvensjonene.
- Gammel regel i memlog: pip og `requirements.txt` (linje 33) er erstattet av uv (linje 39). Spinen bruker uv, og det stemmer.
