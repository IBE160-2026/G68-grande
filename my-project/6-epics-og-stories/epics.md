---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - my-project/2-prd/prd.md
  - my-project/2-prd/addendum.md
  - my-project/5-arkitektur/arkitektur.md
  - my-project/3-ux/DESIGN.md
  - my-project/3-ux/EXPERIENCE.md
---

# Søknadsassistenten - Epics og stories

## Oversikt

Dette dokumentet deler kravene fra PRD-en, UX (DESIGN.md og EXPERIENCE.md) og arkitekturen opp i epics og stories som kan bygges én og én.

**Rammer for planen:**

- Kristine jobber alene. Hun koder i helgene, og i tillegg noen timer på kveldene i uke 46, 47, 49 og 50.
- Kodestopp rundt 6. desember 2026. Uke 50 er til testplan, README og buffer, og eksamen i et annet fag er 11. desember.
- Rekkefølgen: først alt under «Kuttes aldri» (PRD §4), så Korrektur og PDF, og til slutt punktene på nødlisten (gjenbruken av nøkkelordlisten i FR-19, PDF ut i FR-29 og FR-25).
- Stories til kveldene skal være små og godt avgrenset.
- Sjekkpunkter (TO DO): søndag 22. november og søndag 29. november.

**Arbeidsmåte for hver story** (addendum, «Arbeidsmåte», og AD-15):

- Egen branch og pull request (PR) til `main`. PR-tittelen viser story og FR-nummer.
- I PR-en står én eller to setninger om hva som ble sjekket, og om KI-verktøyet gjorde noe feil eller noe som ikke var bedt om, og hvordan det ble rettet.
- Testene i CI må være grønne før PR-en flettes inn.
- README oppdateres i samme story når noe endres som påvirker hvordan nettsiden installeres, startes eller testes, eller hvor testdataene ligger.
- Prompt-loggen fortsetter under kodingen.
- Avviker koden fra PRD-en eller arkitekturen, oppdateres dokumentet og kopien i `my-project/`, og avviket skrives i beslutningsloggen med dato og grunn.

## Kravliste

### Funksjonelle krav

**2.1 Registrering og innlogging**

- FR-1: Brukeren kan registrere seg med e-post og passord. Passordet må være minst 8 tegn. Etter registrering blir brukeren logget inn automatisk.
- FR-2: Hvis e-posten allerede er registrert, får brukeren en feilmelding som sier at e-posten allerede er registrert.
- FR-3: Brukeren kan logge inn med e-post og passord. Ved feil e-post eller passord får brukeren feilmeldingen «Feil e-post eller passord».
- FR-4: Hvis et felt står tomt, får rammen rundt feltet rød farge, og det vises en kort feilmelding ved feltet, for eksempel «Fyll inn e-post», slik at feilen ikke bare vises med farge.
- FR-5: Etter innlogging havner brukeren på en startside med «Begynn å lage søknad». Derfra går brukeren videre til valget mellom Full generering og Korrektur (FR-20).
- FR-6: Brukeren kan logge ut fra nettsiden.
- FR-7: Det er ikke mulig å bruke nettsiden uten å være logget inn, unntatt innloggingen og registreringen. Prøver brukeren å gå til en annen side uten å være logget inn, kommer de til innloggingen med en feilmelding om at de må logge inn først.

**2.2 Valg av modus og PDF eller tekst inn**

- FR-20: Etter «Begynn å lage søknad» velger brukeren mellom «Full generering – Skriv nytt brev» (CV og stillingsannonse) og «Korrektur – Forbedre mitt brev» (CV, eget søknadsbrev og stillingsannonse). Knappene viser begge navnene.
- FR-8: Innleggingssiden har separate felt for CV og stillingsannonse, og i Korrektur også et felt for brukerens eget søknadsbrev. I hvert felt kan brukeren enten laste opp en PDF eller lime inn tekst.
- FR-9: Alle feltene som vises, må være fylt ut før brukeren kan gå videre. Mangler noe, får brukeren en feilmelding som sier hva som mangler.
- FR-10: Hvis brukeren laster opp en fil som ikke er PDF, får brukeren feilmeldingen «Feil filtype, prøv PDF».
- FR-11: Hvis nettsiden ikke klarer å lese teksten i en PDF, for eksempel fordi den er skannet, får brukeren beskjed om å lime inn teksten i stedet.
- FR-12: Grensen for filstørrelse er 5 MB per fil. Er filen for stor, får brukeren en feilmelding som sier dette.
- FR-13: Brukeren kan angre, altså fjerne eller bytte ut en fil eller tekst de har lagt inn, før de går videre.

**2.3 Gap-analyse og nøkkelordtreff**

- FR-14: Gap-analysen går gjennom kravene i stillingsannonsen og viser dem i to lister: krav CV-en dekker og krav CV-en mangler. Gap-analysen er merket som KI-generert.
- FR-15: KI-en henter ut nøkkelordene fra stillingsannonsen én gang. Listen lagres i økten, og prosenten regnes alltid fra den lagrede listen. Innenfor samme søknad gir samme annonse og CV alltid samme prosent. Ny søknad eller utlogging glemmer listen.
- FR-16: Brukeren ser nøkkelordlisten, med hvert nøkkelord merket som treff eller ikke treff. Listen kan ikke endres i versjon 1.
- FR-17: Nøkkelordtreffet regnes ut av nettsiden med en fast telleregel og vises som «X av Y = Z %». Treff også som del av et lengre ord, uavhengig av store og små bokstaver. Nøkkelord på 1–3 tegn må stå som eget ord. Hvert nøkkelord telles én gang. Prosenten rundes til nærmeste hele tall («2 av 3» = 67 %).
- FR-18: Resultatsiden forklarer kort ATS, nøkkelordtreff og gap-analyse, og at gap-analysen og nøkkelordtreffet kan si hverandre imot.
- FR-19: Brukeren kan gå tilbake til innleggingssiden etter resultatet, med feltene fortsatt fylt ut. Analysen kjøres på nytt når brukeren går videre. Er bare CV-en endret, gjenbrukes den lagrede nøkkelordlisten.
- FR-21: Brukeren ser gap-analysen og nøkkelordtreffet før brevet lages eller korrigeres. Brevet lages først når brukeren har bekreftet at de vil gå videre.

**2.4 Søknadsbrev: Full generering og Korrektur**

- FR-22: I Full generering skriver KI-en et søknadsbrev basert på CV-en og stillingsannonsen. Brevet vises på nettsiden før det lastes ned.
- FR-23: I Korrektur lager KI-en en forbedret versjon av brukerens eget brev. Brevet vises én gang i den nye versjonen, endrede setninger er markert (ikke bare med farge), og et klikk på en markert setning viser den gamle.
- FR-24: Brevet skrives på norsk, i formell og akademisk tone, og skal ikke høres ut som generisk KI-tekst. Det nevner stillingen og arbeidsgiveren ved navn, viser til minst to konkrete krav fra annonsen koblet til CV-en, og bruker ikke typiske KI-fraser. I Korrektur beholdes brukerens innhold, eksempler og rekkefølge.
- FR-37: KI-en kommer ikke med antakelser på vegne av brukeren. Brevet bygger bare på CV, annonse og eventuelt eget brev, og legger ikke til erfaring, utdanning eller ferdigheter som ikke står der. Omformulering og kobling til kravene er lov. Gjelder begge modusene.
- FR-25: Brukeren kan be om et nytt forslag. I Korrektur lages det nye forslaget fra brukerens opprinnelige brev.
- FR-26: Brukeren redigerer ikke brevet på nettsiden. Videre redigering gjøres i Word etter nedlasting.
- FR-27: Mens KI-en jobber, viser nettsiden et ventetegn med en kort tekst. Knappen som startet handlingen, kan ikke trykkes på nytt mens brukeren venter.
- FR-28: Hvis KI-en ikke svarer, får brukeren en feilmelding: ved nettverksfeil «Nettverksfeil, sjekk nettverkstilgangen», ellers en melding om å prøve på nytt. Et svar som ikke kan brukes (tom nøkkelordliste, tomme «dekker» og «mangler», tomt brev, svar som ikke kan leses) gir ikke noe resultat, men en feilmelding. Det brukeren har lagt inn, er fortsatt der.

**2.5 Word og PDF ut**

- FR-29: Når brevet er ferdig, kan brukeren laste ned brevet som Word (.docx) eller PDF.
- FR-30: Den nedlastede filen inneholder bare den ferdige brevteksten, uten markeringene fra Korrektur, og uten topp- eller bunntekst.
- FR-31: Etter nedlasting kan brukeren velge mellom å gå til startsiden eller logge ut. Startsiden starter en ny søknad med tomme felt.

**2.6 Testmodus og bruk av KI**

- FR-32: På startsiden kan brukeren slå testmodus av og på med en bryter, bare på startsiden. I testmodus brukes ferdige KI-svar, så nettsiden kan kjøres uten API-nøkkel. Uten API-nøkkel starter nettsiden i testmodus, bryteren er låst, og det står «Mangler API-nøkkel, se README».
- FR-33: Når testmodus er på, vises en tydelig merkelapp «Testmodus».
- FR-34: I testmodus fungerer bare de fiktive testdataene. Annet gir beskjed om at bare testdata fungerer. Feilmeldingene for tomme felt, feil filtype og uleselig PDF virker også i testmodus. Testdataene dekker begge modusene, med fiktivt søknadsbrev, en skannet PDF og en fil av feil type.
- FR-35: Når testmodus er av, vises en merknad hele tiden om at nettsiden bruker en ekstern KI.
- FR-36: Når testmodus er av, må brukeren samtykke til bruk av KI på startsiden før de kan begynne. Teksten over avkrysningsboksen forklarer samtykket. Uten avkryssing gir «Begynn å lage søknad» en feilmelding. I testmodus trengs ikke samtykke.
- FR-38: De ferdige svarene i testmodus er ekte KI-svar, laget ved å kjøre testdataene gjennom den eksterne KI-en. README viser to–tre skjermbilder med ekte KI på.

### Ikke-funksjonelle krav

- NFR-1: Passord lagres hashet, aldri som klartekst.
- NFR-2: API-nøkkelen ligger bare lokalt og havner aldri i Git. Repoet har en `.env.example` uten ekte verdier.
- NFR-3: Ekte CV-er havner aldri i Git. Bare fiktive testdata ligger i repoet, i en egen mappe, med en fasit for hver CV og annonse, med kort begrunnelse for hvert krav som er dekket eller mangler.
- NFR-4: CV, stillingsannonse, søknadsbrev og nøkkelordliste lagres ikke mellom øktene. Bare brukerkontoen lagres, i en lokal database.
- NFR-5: Innloggingen fungerer lokalt uten noen ekstern tjeneste.
- NFR-6: God kontrast (WCAG AA), kan brukes med bare tastatur, alle felt har synlige etiketter, bilder og ikoner har alternativtekst.
- NFR-7: Ser bra ut og fungerer på PC, nettbrett og mobil, uten å rulle sidelengs ved 375, 768 og 1280 px.
- NFR-8: Sensor får nettsiden i gang på 10–15 minutter med README. Databasen og testbrukeren lages automatisk ved første oppstart. README har installasjon, innstillinger (`.env.example`), testbruker, testdata og fasit, hvordan testene kjøres, kjente begrensninger og skjermbilder med ekte KI.
- NFR-9: Automatiske tester med kjent input og fasit for telleregelen (også korte nøkkelord), innloggingen (FR-1, FR-3), kontrollen av KI-svar (FR-28), sjekken av inndata (FR-9, FR-10, FR-12), gjenbruk av nøkkelordlisten (FR-15), at sider krever innlogging (FR-7) og at nedlastet fil er uten markeringer (FR-30).
- NFR-10: KI-instruksene (prompts) ligger i Git.
- NFR-11: Den eksterne KI-en er Claude fra Anthropic, via API.
- NFR-12: Skrevet testplan med resultat for suksesskriteriene som ikke testes automatisk, også hele flyten. Testplanen viser at README er prøvd fra en ny kopi av repoet i en tom mappe, før funksjonsstopp og rett før levering, med dato og resultat.

### Tilleggskrav fra arkitekturen

**Ingen ferdig startmal.** Prosjektet bygges fra bunnen etter «Startstruktur» i arkitekturen. Det påvirker første story i Epic 1:

- All kode i `backend/` (lærerens CI kjører testene der): `soknad/` med `web/`, `kjerne/`, `adaptere/`, `fonts/`, samt `prompts/`, `scripts/`, `testdata/`, `tests/`, `instance/`.
- uv med `pyproject.toml`, `uv.lock` og `.python-version` (Python ≥ 3.12). Versjoner som i Stack-tabellen (Flask 3.1.3, anthropic 2.4.0, pypdf 6.21.4, python-docx 1.2.0, fpdf2 2.9.0, python-dotenv 1.2.4, pytest 9.2.0, ruff 0.17.3).
- `create_app(test_config)` leser `.env`, lager databasen og testbrukeren ved første oppstart.
- Lærerens `.github/workflows/ci.yml` utvides i backend-jobben (byttes ikke ut): `ruff check`, `ruff format --check` og `pytest` på Linux og Windows ved hver PR. Ruff-regelen `PLW1514` slått på.
- `.gitignore`: legg til `!.env.example` og `instance/` (TO DO).
- README: én kommando for å installere uv på Windows og én på Mac, og så `cd backend`, `uv sync`, `uv run flask --app soknad run`.

**Reglene (AD-1–AD-15) som stories må følge:**

- AD-1: Python + Flask med Jinja-maler. Bare små JavaScript-skript uten rammeverk eller byggesteg. JavaScript endrer aldri søknadsdata.
- AD-2: `kjerne/` importerer aldri flask, anthropic, pypdf, docx, fpdf eller sqlite3 og leser ingen filer. Web- og adaptertester bruker `create_app(test_config)`, midlertidig SQLite, `test_client` og `TestKI`.
- AD-3: `adaptere/ki.py` har ett grensesnitt (`nokkelord`, `gap`, `brev`, `korrektur`) med to utgaver: `EkteKI` (Claude) og `TestKI` (leser `testdata/<case>/ki-svar/`, oddetall/partall `forslag` gir `-1`/`-2`). Web velger utgave ut fra `Innlogging.testmodus`.
- AD-4: Én prompt-fil og ett JSON-skjema per KI-oppgave (structured outputs). Faste svarformer. `kjerne/ki_svar.kontroller()` gir `KIFeil(ubrukelig_svar)` ved feil `stop_reason`, ugyldig JSON, tom nøkkelordliste, tomme gap-lister, tomt brev, eller når `gammel` i Korrektur ikke blir det opprinnelige brevet. Testsvarene lages av `scripts/lag_testsvar.py`.
- AD-5: Korrektur viser bare det KI-en sier (endret, ny, fjernet ut fra `ny`/`gammel`). Brevet som vises og lastes ned, er alle `ny` satt sammen. «Nytt forslag» sender alltid det opprinnelige brevet. Korrektur-prompten deler aldri én setning i to oppføringer: blir en lang setning til to, står begge i samme `ny`.
- AD-6: `kjerne/telleregel.py` er den eneste koden for treff og prosent: `casefold()`, ≥ 4 tegn treff i lengre ord, 1–3 tegn bare som eget ord med `re.escape`, `Decimal` med `ROUND_HALF_UP`. Tester: 2 av 3 = 67 %, 1 av 8 = 13 %, «C» i «Center», «C#», «python-utvikler».
- AD-7: `kjerne/okt.py` har `Innlogging(bruker_id, testmodus)` og `Soknad` med faste felt. Lagret i minnet (`adaptere/oktlager.py`), cookien har bare økt-id. Startsiden lager alltid en ny `Soknad` (testmodus beholdes). Ingen automatisk utlogging.
- AD-8: `kjerne/steg.py` eier stegene start < modus < innlegging < resultat < brev. Steg flyttes bare etter vellykket POST. Endringer bare via `sett_inndata`, `velg_modus`, `nytt_forslag`. Bryteren kan bare endres på startsteget. KI-kall bare fra POST, med `opptatt`. Etter innlogging alltid til startsiden. Nedlasting med `GET /last-ned/<docx|pdf>`.
- AD-9: Lukkede feiltyper i `kjerne/feil.py`. Inndatafeil som liste (`InndataFeil(felt, type)`), unntak bare for `KIFeil` og `FilFeil`. Egen 413-håndterer. Alle tekster i `web/tekster.py`.
- AD-10: `testdata_match.vask()` (NFKC, `casefold`, bare bokstaver og tall). CV-en avgjør testcaset, andre felt som ikke matcher, får `ikke_testdata`. Test per case for `.pdf` og `.txt`. Uten `ANTHROPIC_API_KEY` er testmodus låst på.
- AD-11: PDF inn bare i `adaptere/pdf_inn.py` (pypdf, under 50 bokstaver = uleselig, 5 MB per fil, `MAX_CONTENT_LENGTH` 16 MB). Word og PDF ut bare i `adaptere/fil_ut.py` (python-docx, fpdf2 med TTF-skrift). Filnavn bare i `kjerne/filnavn.py` (`Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>`).
- AD-12: Starter uten `.env` (tilfeldig `SECRET_KEY`, standardmodell `claude-opus-5-5`). Passord med `werkzeug.security`. SQLite i `instance/`. Loggen viser aldri CV, brev, passord eller nøkkel. Skrifter lokalt. Tekst sendes til Claude bare med samtykke. Filer åpnes med `encoding="utf-8"`.
- AD-13: `Anthropic(timeout=90, max_retries=1)`. Nettverksfeil gir `KIFeil(nettverk)`, andre feil `KIFeil(annet)`. Tokens og anslått pris skrives til terminalen. Budsjett 250 kr uten auto-reload.
- AD-14: `prompts/brev.md` og `prompts/korrektur.md` har kravene i FR-24 og FR-37 og listen over KI-fraser. `testdata/<case>/fasit.md` har sjekkliste for kriterium 11 og 12.
- AD-15: PR-tittel viser story og FR-nummer. Hver testfil og testfunksjon nevner FR-nummeret. Avvik fra arkitekturen oppdateres i begge kopiene og i beslutningsloggen.

**Konvensjoner:** norske domeneord uten æøå, `snake_case`, grenser i `soknad/innstillinger.py`, felles elementer bare i `base.html`, `tests/` speiler `soknad/`, ingen utkommentert kode i `main`, testplan i `my-project/testplan.md`.

**Åpne prøver og punkter fra TO DO som påvirker stories:**

- Prøvd 7. november: pypdf leser CV fra Word med to kolonner riktig med vanlig `extract_text()`. Fra Canva kommer all teksten, men overskriftene havner på feil sted. Ingen ny løsning i koden: reserven er innlimt tekst, og README skal si det under kjente begrensninger.
- Prøvd 7. november: formen `{ny, gammel, nytt_avsnitt}` klarer endret, slått sammen, fjernet, ny og uendret. Delte setninger ga feil «(Ny setning)», derfor regelen om deling i AD-5.
- Når ekte KI kobles på: prøve om KI-en forstår Canva-teksten riktig.
- Lista over typiske KI-fraser (FR-24) er bestemt 7. november (17 fraser i addendum). Promptene for brev og Korrektur tar den med, og en test kan sjekke at ingen av frasene står i testsvarene (FR-38).
- Når testsvarene lages (FR-38): kjøre hver prompt tre ganger og sjekke mot fasiten (kriterium 1, 3, 11, 12).
- Testdata med tydelige hull (for eksempel «førerkort», «SQL»).
- Konto i Claude Console, kreditt og API-nøkkel i `.env` når ekte KI kobles på.
- Avtale med en kollega innen 20. november for kriterium 13.

### UX-krav

- UX-DR1: Alle farger, skrifter, hjørner og avstander fra DESIGN.md som CSS-variabler på ett sted («Myk fersken»). Ingen fargekoder rett i koden. Bare lys modus.
- UX-DR2: Systemskrift overalt. Baloo 2 ExtraBold ligger lokalt og brukes bare i logoen og «På vei mot ny jobb». Logoen står sentrert øverst, på én linje også på 375 px (`clamp`), men får bryte ved stor tekst.
- UX-DR3: `base.html` med `lang="nb"`, egen sidetittel per side («Logg inn – Søknadsassistenten»), landemerkene `header` (logo, testmodus), `main` og `footer`. Hjørneraden (`corner-row`) er festet nederst med KI-merknaden til venstre (bare når testmodus er av) og «Logg ut» til høyre, med `scroll-padding-bottom`, og står nederst på siden i stedet når skjermen er under ca. 500 px høy.
- UX-DR4: Knapper: hovedknapp, sekundærknapp, stor knapp, nedlastet-knapp og lenkeknapp, med hover (løft 2 px, skygge), trykk (96 %) og låst (55 %). «Tilbake» er alltid sekundær og til venstre.
- UX-DR5: Fokusring 3 px `{colors.focus-ring}` med 2 px avstand på alt som kan trykkes på. Alt kan brukes med Tab, Enter, mellomrom og Esc.
- UX-DR6: Tekstfelt på innlogging og registrering: etikett over, hjelpetekst og feiltekst under og koblet til feltet, rød ramme og `aria-invalid` ved feil, `autocomplete` (email, current-password, new-password). Fokus til første felt med feil. «Feil e-post eller passord» og «Du må logge inn først» i en skjemafeil-boks som får fokus.
- UX-DR7: Feilboks øverst på siden med overskriften «Noe må fikses før du kan gå videre:», én lenke per feil til feltet, `tabindex="-1"` og fokus, rulling dit, uten `role="alert"`. KI-feil bruker samme boks med «Prøv på nytt» og en tekst per side om at ingenting er borte.
- UX-DR8: Innleggingsfelt med tilstandene tom, fil og tekst: «Last opp PDF» (`accept=".pdf"`) og «Lim inn tekst», filnavn med ✓ som kuttes med «…», søppelbøtte (minst 24 × 24 px) som tømmer uten bekreftelse, tekstboks som kan dras større (ca. 160 px PC, 200 px mobil). Fokus og skjermlesertekster som i EXPERIENCE (for eksempel «CV lastet opp: …», «Tøm CV-feltet», «CV-feltet er tømt», «Last opp PDF, CV»). Feiltekst under feltnavnet, koblet med `aria-describedby`.
- UX-DR9: Testmodus-bryter (`role="switch"`, etikett «Testmodus») bare på startsiden. Låst uten API-nøkkel med `aria-disabled="true"` og «Mangler API-nøkkel, se README» koblet til. Merkelapp «Testmodus» på de andre sidene. Teksten «Du er i testmodus …» i et statusområde. Hjelpetekst om `testdata/` på innleggingen.
- UX-DR10: Samtykke på startsiden med avkrysningsboks (22 px), tekst over, «i»-ikon og «i»-boks med de fire punktene. Alltid tom når startsiden åpnes. Uten avkryssing: rød ramme, «Du må samtykke før du kan begynne» og fokus til boksen. Skjules i testmodus.
- UX-DR11: «i»-ikon og «i»-boks: åpnes og lukkes med trykk, Enter og mellomrom, lukkes med Esc, åpnes med hover på PC (ikke av fokus alene), med `aria-expanded` og `aria-controls`.
- UX-DR12: Modusvalg med to kort side om side (under hverandre under 700 px). Hele kortet er én knapp. Hover løfter kortet 4 px, og ikonet vipper.
- UX-DR13: Resultatside: gap-lister (grønn med ✓, varm fersken med →), merket «Laget av KI», «i»-ikoner, FR-18-linjen, nøkkelordtreff «X av Y = Z %» med prosentlinje som fylles på 1 s, to nøkkelordlister med ✓ og ○ og antall, ATS-forklaring som foldes ut (lukket når siden åpnes), og tekstene for tomme lister.
- UX-DR14: Ventetegn som dekker siden: tre hoppende prikker, «På vei mot ny jobb» og ventetekst per handling. Resten av siden `inert` (også hjørneraden), knappen `aria-disabled` med fokus, et fast `role="status"`-område. Fokus etterpå til ny overskrift eller feilboksen.
- UX-DR15: Brevet som hvitt ark (høyst 720 px). Korrektur: forklaring over brevet, endrede setninger som knapper (grønn bakgrunn og understreking, skjult tekst «Endret setning»), «Du skrev» med den gamle setningen, «(Ny setning)», «1 setning er fjernet.», og «Vi fant ingenting å endre …». Flere setninger kan være åpne samtidig.
- UX-DR16: Nedlastingsknapper som blir grønne med «✓ Lastet ned som …», med filnavn-linjen under. Vinduet etter nedlasting kommer hver gang.
- UX-DR17: Tre vinduer (`<dialog>` med `showModal()`): etter nedlasting («Lag ny søknad», «Logg ut», «Bli her»), «Nytt forslag» («Ja, lag nytt forslag», «Avbryt») og «Logg ut før nedlasting» («Logg ut», «Avbryt»). Fokus til det trygge valget, Esc lukker, `aria-labelledby` og `aria-describedby`, fokus tilbake til knappen som åpnet.
- UX-DR18: Fyrverkeri rundt brevoverskriften (ca. 2,2 s, borte etter ca. 3,2 s, høyst 3 utbrudd i sekundet, bak teksten). Ved `prefers-reduced-motion` slås alle animasjoner av.
- UX-DR19: Responsivt: bruddpunkt 700 px, innleggingsfeltene side om side først fra 1000 px. Ingen rulling sidelengs ved 320, 375, 768 og 1280 px og ved 200 % zoom. Ingen faste høyder og ingen `nowrap` på tekst.
- UX-DR20: Alle brukertekster fra EXPERIENCE «Tekster per side» ligger i `web/tekster.py`. Vennlig «du»-tone, «nettside» og aldri «app», «Dette kan du jobbe videre med» på skjermen i stedet for «mangler».
- UX-DR21: Ikoner som bare er pynt, skjules for skjermlesere. Knapper med bare ikon har en tekst for skjermlesere.
- UX-DR22: Tillegg fra UX: «Gjenta passord» med «Passordene er ikke like», sjekk av e-postformen («E-posten er ikke gyldig»), «Tilbake» på modusvalget og innleggingen, samtykke på nytt hver gang startsiden åpnes, vinduet «Logg ut før nedlasting».
- UX-DR23: UX-kuttlisten: pynten (fyrverkeri, prosentlinjen som fylles, ikonet som vipper, vinduet «Logg ut før nedlasting», arbeidsgiver i filnavnet) bygges i en egen story etter at kjerneflyten virker i testmodus.
- UX-DR24: Hjelpetekst over feltene på innleggingssiden, i begge modusene: «Tips: PDF lagret fra Word leses best. Er CV-en laget i Canva eller et lignende program, kan teksten komme i feil rekkefølge. Lim den da heller inn.»

### FR Coverage Map

- FR-1: Epic 1 – registrere seg
- FR-2: Epic 1 – e-posten finnes fra før
- FR-3: Epic 1 – logge inn
- FR-4: Epic 1 – tomme felt med rød ramme og feiltekst
- FR-5: Epic 1 – startside etter innlogging (knappen «Begynn å lage søknad» i Epic 2)
- FR-6: Epic 1 – logge ut
- FR-7: Epic 1 – sider krever innlogging
- FR-8: Epic 2 (innlimt tekst), Epic 5 (brevfeltet), Epic 6 (PDF)
- FR-9: Epic 2 – alle felt må fylles ut
- FR-10: Epic 6 – feil filtype
- FR-11: Epic 6 – uleselig PDF
- FR-12: Epic 6 – grense på 5 MB
- FR-13: Epic 2 (tekst), Epic 6 (fil) – angre
- FR-14: Epic 2 – gap-analyse
- FR-15: Epic 2 – nøkkelordlisten lagres i økten
- FR-16: Epic 2 – nøkkelordlisten med treff og ikke treff
- FR-17: Epic 2 – telleregelen
- FR-18: Epic 2 – forklaringer på resultatsiden
- FR-19: Epic 2 (tilbake fra resultatet med feltene fylt ut), Epic 7 (gjenbruk av nøkkelordlisten)
- FR-20: Epic 2 (kortet Full generering), Epic 5 (kortet Korrektur) – valg av modus
- FR-21: Epic 2 – analysen vises før brevet
- FR-22: Epic 3 – brev i Full generering
- FR-23: Epic 5 – markerte endringer i Korrektur
- FR-24: Epic 4 (brev-prompten), Epic 5 (Korrektur-prompten)
- FR-25: Epic 7 – nytt forslag
- FR-26: Epic 3 – ingen redigering på nettsiden
- FR-27: Epic 2 – ventetegn og låst knapp
- FR-28: Epic 2 – feilmeldinger fra KI og kontroll av svaret
- FR-29: Epic 3 (Word), Epic 7 (PDF)
- FR-30: Epic 3 – filen er uten markeringer
- FR-31: Epic 3 – vinduet etter nedlasting
- FR-32: Epic 2 (bryteren, låst på), Epic 4 (kan slås av med API-nøkkel) – testmodus-bryteren
- FR-33: Epic 2 – merkelappen «Testmodus»
- FR-34: Epic 2 – bare testdata i testmodus
- FR-35: Epic 4 – KI-merknaden
- FR-36: Epic 4 – samtykke
- FR-37: Epic 4 (brev-prompten), Epic 5 (Korrektur-prompten)
- FR-38: Epic 4 (ekte KI-svar i testmodus), Epic 8 (skjermbilder i README)

## Epic-liste

### Epic 1: Registrere seg og logge inn

Brukeren kan registrere seg, logge inn og logge ut, og andre sider er stengt uten innlogging. Første story lager startstrukturen (mappene i `backend/`, uv, CI med ruff og pytest, `.gitignore`, `base.html` med fargene, databasen og testbrukeren).

**Sider:** innlogging, registrering, startside (velkomst og «Begynn å lage søknad»), faste elementer (logo og «Logg ut»).
**FRs covered:** FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7 · NFR-1, NFR-2, NFR-5

### Epic 2: Se gap-analyse og nøkkelordtreff i testmodus

Brukeren slår på testmodus, velger modus, limer inn CV og annonse og ser resultatsiden. Første fiktive testdata og fasit og telleregelen med tester kommer her.

**Sider:** startside (testmodus-bryteren, låst på, og «Begynn å lage søknad»), modusvalg (kortet Full generering), innlegging for Full generering (innlimt tekst), resultatside (med «Tilbake»), merkelappen «Testmodus».
**FRs covered:** FR-8 (innlimt tekst), FR-9, FR-13 (tekst), FR-14, FR-15, FR-16, FR-17, FR-18, FR-19 (tilbake), FR-20, FR-21, FR-27, FR-28, FR-32, FR-33, FR-34 · NFR-3, NFR-4

### Epic 3: Få et søknadsbrev og laste det ned (Full generering)

Brukeren ser brevet, laster det ned som Word og får vinduet med «Lag ny søknad» og «Logg ut».

**Sider:** brevside for Full generering, vindu etter nedlasting.
**FRs covered:** FR-22, FR-26, FR-29 (bare .docx), FR-30, FR-31

### Epic 4: Bruke ekte KI (Claude)

Med API-nøkkel kan testmodus slås av, og da bruker nettsiden Claude. Her kommer KI-merknaden, samtykket, promptene for nøkkelord, gap og brev med reglene og de 17 KI-frasene, og skriptet som lager de ekte testsvarene. Hver prompt kjøres tre ganger mot fasiten, og det kommer et testcase til (kriterium 3). Fram til denne epicen er testsvarene håndlagde.

**Sider:** startside (bryteren kan slås av, og samtykket), faste elementer (KI-merknaden).
**FRs covered:** FR-24, FR-32 (slå av), FR-35, FR-36, FR-37, FR-38 · NFR-10, NFR-11

### Epic 5: Korrektur av eget brev

Brukeren legger inn sitt eget brev og får en forbedret versjon med markerte endringer. Et klikk på en markert setning viser den gamle.

**Sider:** modusvalg (kortet Korrektur), innlegging for Korrektur (feltet for eget brev), brevside for Korrektur.
**FRs covered:** FR-8 (brevfeltet), FR-20 (kortet Korrektur), FR-23, FR-24 og FR-37 (Korrektur-prompten)

### Epic 6: Laste opp CV og annonse som PDF

Brukeren kan laste opp PDF i stedet for å lime inn tekst, med feilmelding ved feil filtype, uleselig PDF og for stor fil, og PDF-tipset.

**Sider:** innlegging («Last opp PDF» og PDF-tipset).
**FRs covered:** FR-8 (PDF), FR-10, FR-11, FR-12, FR-13 (fil)

### Epic 7: Ekstra valg og pynt (nødliste 1–3 og UX-kuttlisten)

Gjenbruk av nøkkelordlisten når bare CV-en er endret, «Nytt forslag», nedlasting som PDF, og pynten: fyrverkeri, prosentlinjen som fylles, ikonet som vipper, vinduet «Logg ut før nedlasting» og arbeidsgiveren i filnavnet.

**Sider:** resultatside (prosentlinjen som fylles), brevside («Nytt forslag», PDF og fyrverkeri), modusvalg (ikonet som vipper), vinduene «Nytt forslag» og «Logg ut før nedlasting».
**FRs covered:** FR-19 (gjenbruk), FR-25, FR-29 (PDF)

### Epic 8: Klar for sensor

Sensor kan installere nettsiden og vurdere den etter README. README er oppdatert underveis og gjøres ferdig her, testplanen skrives, skjermbildene med ekte KI tas, og README prøves fra en ny kopi av repoet: første gang før kodestopp (5.–6. desember), andre gang rett før levering.

**Sider:** ingen nye.
**FRs covered:** FR-38 (skjermbilder), NFR-8, NFR-12

UX-kravene og testene (NFR-6, NFR-7, NFR-9) følger med i storyen der hver ting bygges.

**Sjekkpunkter:** 22. november: Epic 1 og første del av Epic 2 (telleregelen og innleggingssiden). 29. november: Epic 1–3 (hele flyten i testmodus). Uke 49 og 5.–6. desember: Epic 4–6, og første prøve av README fra en ny kopi (story 8.2). Hvis tid: Epic 7. Uke 50: resten av Epic 8.

## Epic 1: Registrere seg og logge inn

Brukeren kan registrere seg, logge inn og logge ut, og andre sider er stengt uten innlogging. Første story lager startstrukturen.

### Story 1.1: Nettsiden starter fra en ny kopi av repoet

Som sensor
vil jeg starte nettsiden med tre kommandoer, uten å lage en `.env` først,
slik at jeg raskt kommer i gang med å vurdere den.

**Akseptansekriterier:**

**Gitt** en ny kopi av repoet uten `.env`
**Når** jeg kjører `cd backend`, `uv sync` og `uv run flask --app soknad run`
**Så** starter nettsiden på localhost uten feil
**Og** en tilfeldig `SECRET_KEY` lages ved oppstart (AD-12)

**Gitt** at nettsiden kjører
**Når** jeg åpner den i nettleseren
**Så** ser jeg logoen «Søknadsassistenten» sentrert øverst, i Baloo 2 fra en fil i prosjektet. Ingenting hentes fra Google Fonts (UX-DR2, AD-12)
**Og** logoen står på én linje ved 375 px, og ingen side ruller sidelengs ved 375, 768 og 1280 px (UX-DR19)

**Gitt** `base.html`
**Så** har den `lang="nb"`, en egen sidetittel og landemerkene `header`, `main` og `footer` (UX-DR3)
**Og** alle farger, skrifter, hjørner og avstander fra DESIGN.md er CSS-variabler på ett sted. Det står ingen fargekoder andre steder (UX-DR1)
**Og** hver side har én `h1`. Boksoverskrifter er `h2` og listeoverskrifter `h3`, og logoen er ikke en overskrift (EXPERIENCE, Accessibility Floor)

**Gitt** repoet
**Så** finnes `backend/` med `pyproject.toml`, `uv.lock`, `.python-version`, `soknad/__init__.py` med `create_app(test_config)`, `soknad/innstillinger.py`, `soknad/web/` og `tests/`. Andre mapper lages først når en story trenger dem
**Og** `.gitignore` får `instance/`. `!.env.example` står der fra før (sjekket 7. november), så `backend/.env.example` kommer med i Git. Den viser `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` og `SECRET_KEY` uten verdier (NFR-2)

**Gitt** en PR
**Så** kjører lærerens `ci.yml`, utvidet i backend-jobben, `ruff check`, `ruff format --check` og `pytest` på Linux og Windows, med `PLW1514` slått på, slik at ruff stopper `open()` uten `encoding`. Det sjekkes at regelen faktisk slår til, fordi noen ruff-regler krever `preview`. De andre jobbene er uendret
**Og** en første test bruker `create_app(test_config)` og `test_client` og sjekker at siden svarer med `lang="nb"` (AD-2, AD-15)
**Og** README har kommandoene for å installere uv (én for Windows og én for Mac) og starte nettsiden, og hvordan testene kjøres (NFR-8)

### Story 1.2: Logge inn med testbrukeren

Som sensor
vil jeg logge inn med testbrukeren fra README,
slik at jeg kan prøve nettsiden uten å registrere meg.

**Akseptansekriterier:**

**Gitt** at nettsiden startes for første gang
**Når** `create_app` kjører
**Så** lages `instance/brukere.db` med en tabell for brukere (e-post og passord-hash) og testbrukeren `test@example.com` / `testpassord1` (fra `innstillinger.py`) (NFR-8, AD-12)
**Og** neste oppstart lager ikke testbrukeren på nytt
**Og** passordet er lagret hashet med `werkzeug.security`, aldri som klartekst (NFR-1), og ingenting av dette trenger en ekstern tjeneste (NFR-5)

**Gitt** innloggingssiden med overskriften «Logg inn», feltene «E-post» og «Passord» med etiketter over og `autocomplete` (email, current-password), og knappen «Logg inn» (UX-DR4, UX-DR6)
**Når** jeg logger inn med riktig e-post og passord
**Så** får jeg en ny økt-id, `Innlogging(bruker_id, testmodus)` lagres i minnet, og cookien har bare økt-id-en (AD-7)
**Og** jeg kommer alltid til startsiden, med «Velkommen! 👋» og ingressen (FR-5, AD-8). Knappen «Begynn å lage søknad» kommer i Epic 2

**Når** e-posten eller passordet er feil
**Så** vises «Feil e-post eller passord» i en rød skjemafeil-boks over skjemaet, og boksen får fokus (FR-3, UX-DR6)

**Når** ett eller begge feltene er tomme
**Så** får hvert tomme felt rød ramme, `aria-invalid` og «Fyll inn e-post» eller «Fyll inn passord» under feltet, koblet til feltet. Begge feilene vises samtidig, og fokus går til det første feltet med feil (FR-4, AD-9)

**Gitt** at jeg ikke er logget inn
**Når** jeg prøver å åpne startsiden
**Så** kommer jeg til innloggingen (FR-7)

**Og** alt som kan trykkes på, har fokusringen og kan brukes med tastatur (UX-DR5). Tekstene ligger i `web/tekster.py` og feiltypene i `kjerne/feil.py` (UX-DR20, AD-9)
**Og** det er alltid lov å lime inn i feltene og bruke passordbehandler (EXPERIENCE)
**Og** README har e-post og passord til testbrukeren (NFR-8)
**Og** tester (NFR-9) dekker riktig innlogging, feil passord, ukjent e-post, tomme felt, at passordet er hashet og at testbrukeren bare lages én gang. Hver test nevner FR- eller NFR-nummeret

### Story 1.3: Registrere seg som ny bruker

Som student
vil jeg lage min egen bruker med e-post og passord,
slik at jeg kan bruke nettsiden.

**Akseptansekriterier:**

**Gitt** innloggingssiden
**Så** står «Ny her? Registrer deg her» under skjemaet, og lenken går til registreringen. På registreringen står «Har du allerede en bruker? Logg inn»

**Gitt** registreringen med overskriften «Registrer deg», feltene «E-post», «Passord» (med «Minst 8 tegn» under fra starten, koblet til feltet) og «Gjenta passord», og `autocomplete` (email, new-password) (UX-DR6, UX-DR22)
**Når** jeg fyller ut riktig og trykker «Registrer deg»
**Så** lagres brukeren med hashet passord, jeg blir logget inn automatisk med ny økt-id og kommer til startsiden (FR-1, NFR-1)

**Når** noe er feil
**Så** vises alle feilene samtidig, med rød ramme, `aria-invalid` og tekst under feltet, og fokus går til det første feltet med feil (FR-4, AD-9):
- tomme felt: «Fyll inn e-post», «Fyll inn passord», «Gjenta passordet»
- passord under 8 tegn: «Passordet må ha minst 8 tegn»
- feil form på e-posten (for eksempel «ola@»): «E-posten er ikke gyldig»
- passordene er ulike: «Passordene er ikke like»
- e-posten finnes fra før: «Denne e-posten er allerede registrert» (FR-2)

**Og** e-posten sammenlignes uten mellomrom foran og bak og uten forskjell på store og små bokstaver, så `Ola@x.no` og `ola@x.no` er samme bruker
**Og** tester (NFR-9) dekker registrering, e-post som finnes, for kort passord, ulike passord og ugyldig e-post (FR-1, FR-2)

### Story 1.4: Logge ut, og bare innloggede kommer inn

Som student
vil jeg kunne logge ut, og vite at ingen kommer inn på sidene uten å logge inn,
slik at ingen andre ser det jeg har lagt inn.

**Akseptansekriterier:**

**Gitt** at jeg er logget inn
**Så** står «Logg ut» nede til høyre i hjørneraden. Raden er festet nederst på skjermen, har `scroll-padding-bottom` og dekker aldri innhold, heller ikke ved 375 px. Under ca. 500 px skjermhøyde står den nederst på siden i stedet (UX-DR3)

**Når** jeg trykker «Logg ut»
**Så** slettes `Innlogging` fra minnet, og `Soknad` når den finnes (fra Epic 2), og jeg kommer til innloggingen (FR-6, AD-7, NFR-4)

**Gitt** at jeg ikke er logget inn
**Når** jeg prøver å åpne en annen side enn innloggingen eller registreringen
**Så** kommer jeg til innloggingen med «Du må logge inn først» i skjemafeil-boksen, og boksen får fokus (FR-7, UX-DR6)

**Gitt** en gyldig cookie, men ingen økt i minnet (etter at nettsiden er startet på nytt)
**Så** behandles jeg som utlogget (AD-7)

**Og** en test (NFR-9, FR-7) går gjennom alle sidene som finnes, unntatt innlogging, registrering og static, og sjekker at de sender til innloggingen. Da blir sider fra senere stories testet automatisk

## Epic 2: Se gap-analyse og nøkkelordtreff i testmodus

Brukeren velger Full generering i testmodus, limer inn CV og annonse fra testdataene og ser resultatsiden med gap-analysen og nøkkelordtreffet. Testsvarene er håndlagde fram til Epic 4.

### Story 2.1: Telleregelen for nøkkelordtreff

Som student
vil jeg at nøkkelordtreffet regnes ut med en fast og åpen regel,
slik at samme CV og annonse alltid gir samme prosent, og jeg kan forstå hvorfor.

**Akseptansekriterier:**

**Gitt** `kjerne/telleregel.py`, den eneste koden som avgjør treff og prosent (AD-6)
**Når** en nøkkelordliste og en CV-tekst sendes inn
**Så** returneres hvilke nøkkelord som er treff og ikke treff, antall treff, antall nøkkelord og prosenten (FR-16, FR-17)
**Og** nøkkelord og CV sammenlignes med `casefold()`
**Og** nøkkelord på 4 tegn eller mer gir treff også som del av et lengre ord
**Og** nøkkelord på 1–3 tegn gir treff bare som eget ord, med `(?<!\w)ord(?!\w)` og `re.escape`
**Og** hvert nøkkelord telles én gang, også om det står flere ganger i CV-en
**Og** prosenten rundes med `Decimal` og `ROUND_HALF_UP`, ikke `round()`

**Og** `kjerne/` importerer ikke flask eller andre biblioteker fra AD-2
**Og** tester (NFR-9, FR-17) sjekker: 2 av 3 = 67 %, 1 av 8 = 13 %, «C» gir ikke treff i «Center», «C#» og «C++» gir treff som eget ord, «python» gir treff i «python-utvikler», æøå («Søknad» i «søknadsbrev»), store og små bokstaver, og 0 av Y = 0 %
**Og** en test viser at «C» gir treff i «C#» og «C++» med denne regelen, fordi tegnet etter «C» ikke er en bokstav. Det skrives som kjent begrensning i README, sammen med begrensningene i FR-17

### Story 2.2: Fiktive testdata og fasit for første testcase

Som sensor
vil jeg ha fiktive testdata med en fasit,
slik at jeg kan prøve nettsiden og se om resultatet stemmer.

**Akseptansekriterier:**

**Gitt** mappen `backend/testdata/case-1-<navn>/`
**Så** finnes en fiktiv CV (`cv.txt`) og en fiktiv stillingsannonse (`annonse.txt`). Ingen ekte personer eller CV-er (NFR-3)
**Og** CV-en har tydelige hull mot annonsen, for eksempel «førerkort» og «SQL», ikke grensetilfeller
**Og** `fasit.md` lister alle kravene i annonsen, om CV-en dekker dem eller ikke, med en kort begrunnelse per krav, nøkkelordene med forventet treff og det forventede nøkkelordtreffet «X av Y = Z %» (NFR-3)
**Og** `ki-svar/nokkelord.json` og `ki-svar/gap.json` er håndlagde i formene fra AD-4 (`{nokkelord, arbeidsgiver}` og `{dekker, mangler}`), og stemmer med fasiten. De byttes ut med ekte KI-svar i Epic 4 (FR-38)
**Og** README sier hvor testdataene og fasiten ligger (NFR-8)
**Og** Claude lager utkastet, og Kristine sjekker og godkjenner innholdet før PR-en flettes

### Story 2.3: Testmodus kjenner igjen testdataene

Som sensor
vil jeg at testmodus kjenner igjen testdataene og gir de ferdige svarene,
slik at nettsiden kan kjøres uten API-nøkkel.

**Akseptansekriterier:**

**Gitt** `kjerne/testdata_match.vask(tekst)`
**Så** gjør den Unicode NFKC, `casefold()` og beholder bare bokstaver og tall (AD-10)
**Og** CV-en avgjør testcaset. En annonse som ikke hører til samme case, gir `InndataFeil(annonse, ikke_testdata)`. En CV som ikke er testdata, gir `InndataFeil(cv, ikke_testdata)` (FR-34, AD-9)

**Gitt** `adaptere/ki.py` med grensesnittet `nokkelord(annonse)` og `gap(cv, annonse)` og utgaven `TestKI` (AD-3)
**Når** `TestKI` kalles med testdata
**Så** leser den svaret fra `testdata/<case>/ki-svar/` og sender det gjennom `kjerne/ki_svar.kontroller()` (AD-4)
**Og** `kontroller()` gir `KIFeil(ubrukelig_svar)` ved ugyldig JSON, tom nøkkelordliste eller når både `dekker` og `mangler` er tomme (FR-28)

**Og** tester (NFR-9) sjekker: samme tekst med ekstra mellomrom, linjeskift og store bokstaver gjenkjennes som samme case (FR-34), tekst som ikke er testdata gir `ikke_testdata` på riktig felt, og hvert tilfelle av ubrukelig svar gir `KIFeil(ubrukelig_svar)` (FR-28)

### Story 2.4: Startsiden får testmodus og knappen videre, og modusvalget lages

Som sensor
vil jeg se at nettsiden er i testmodus og komme videre fra startsiden til valget av modus,
slik at jeg kan begynne på en søknad uten API-nøkkel.

**Akseptansekriterier:**

**Gitt** startsiden
**Så** står bryteren «Testmodus» oppe til høyre (`role="switch"`, synlig etikett). Fram til Epic 4 er den alltid slått på og låst med `aria-disabled="true"`. Uten `ANTHROPIC_API_KEY` står «Mangler API-nøkkel, se README» under, koblet med `aria-describedby` (FR-32, UX-DR9, AD-10)
**Og** teksten «Du er i testmodus. Nettsiden bruker ferdige svar, og ingenting sendes til ekstern KI.» står i et statusområde (UX-DR9)
**Og** knappen «Begynn å lage søknad» er den største knappen på siden (FR-5, UX-DR4)

**Gitt** at jeg kommer til startsiden
**Så** lages alltid en ny `Soknad`, og testmodus i `Innlogging` beholdes (AD-7)

**Når** jeg trykker «Begynn å lage søknad»
**Så** flyttes steget til modus, og jeg kommer til modusvalget (AD-8)

**Gitt** modusvalget med overskriften «Hva vil du gjøre i dag?»
**Så** finnes kortet ✨ «Full generering» · «Skriv nytt brev» med teksten fra EXPERIENCE. Hele kortet er én knapp. Kortet «Korrektur» kommer i Epic 5 (FR-20, UX-DR12)
**Og** «Tilbake» (sekundærknapp, til venstre) går til startsiden (UX-DR4)
**Og** et trykk på kortet lagrer modus med `velg_modus` og går til innleggingen

**Gitt** en side etter startsiden
**Så** står merkelappen «Testmodus» oppe til høyre, fra `base.html` (FR-33, UX-DR9)

**Gitt** `kjerne/steg.py` med stegene start < modus < innlegging < resultat < brev
**Så** kan en side bare vises når sidens steg ≤ `Soknad.steg`. Ellers sendes brukeren til siden for steget sitt, og steget flyttes bare etter en POST som har lyktes (AD-8)
**Og** etter en POST som har lyktes, sendes brukeren videre med redirect, så oppfriskning ikke sender skjemaet på nytt. Feiler POST-en, vises samme side på nytt uten redirect (AD-8)
**Og** tester sjekker at man ikke kan hoppe over et steg med adresselinjen, og at startsiden lager ny søknad med testmodus beholdt

### Story 2.5: Lime inn CV og stillingsannonse

Som student
vil jeg lime inn CV-en min og stillingsannonsen,
slik at nettsiden kan sammenligne dem.

**Akseptansekriterier:**

**Gitt** innleggingen for Full generering med overskriften «Legg inn CV-en din og stillingsannonsen»
**Så** finnes feltene «📄 CV» og «📢 Stillingsannonse», hver med «Lim inn tekst». «Last opp PDF» kommer i Epic 6 (FR-8, UX-DR8)
**Og** i testmodus står «Testmodus: bruk filene i mappen backend/testdata/ i prosjektet.» over feltene (UX-DR9)
**Og** fra 1000 px står feltene side om side, ellers under hverandre (UX-DR19)

**Når** jeg trykker «Lim inn tekst»
**Så** åpnes en tekstboks som kan dras større (ca. 160 px på PC, 200 px på mobil), og markøren settes i den (UX-DR8)

**Når** jeg trykker søppelbøtta
**Så** tømmes feltet uten bekreftelse, fokus går til «Lim inn tekst» i samme felt (til «Last opp PDF» fra Epic 6), og skjermlesere hører for eksempel «CV-feltet er tømt». Søppelbøtta er minst 24 × 24 px og har teksten «Tøm CV-feltet» for skjermlesere (FR-13, UX-DR8, UX-DR21)

**Når** jeg trykker «Sjekk CV-en min»
**Så** sjekkes alle feltene samtidig med `sett_inndata`. Tomme felt gir «CV: Fyll inn feltet. Last opp en PDF eller lim inn tekst.», og tekst som ikke er testdata, gir «CV: I testmodus fungerer bare testdataene fra mappen backend/testdata/.» (FR-9, FR-34, AD-9)
**Og** feilene vises i feilboksen øverst med overskriften «Noe må fikses før du kan gå videre:», én lenke per feil til feltet, og fokus til boksen (UX-DR7). Feltet med feil får rød ramme, og teksten står også under feltnavnet, koblet med `aria-describedby` (UX-DR8)
**Og** det som er riktig, beholdes (AD-9)

**Når** alt er riktig
**Så** henter nettsiden nøkkelordlisten og gap-analysen fra KI-en (her `TestKI`), lagrer nøkkelordlisten, `arbeidsgiver` og den vaskede annonseteksten i økten, og sender meg til resultatsiden (FR-15, FR-21)
**Og** resultatsiden viser i denne storyen overskriften «Slik passer CV-en din til stillingen», listene «Dette dekker CV-en din» og «Dette kan du jobbe videre med», og «X av Y = Z %» fra telleregelen (FR-14, FR-17)
**Og** CV, annonse og nøkkelordliste ligger bare i minnet, aldri på disk eller i cookien (NFR-4, AD-7)

**Når** jeg trykker «Tilbake»
**Så** kommer jeg til modusvalget, og CV og annonse er fortsatt fylt ut
**Og** det gjelder også tekst jeg har skrevet inn uten å trykke «Sjekk CV-en min»: «Tilbake» sender feltene til serveren, som lagrer dem uten å vise feil. JavaScript endrer aldri søknadsdata (AD-1, AD-8)

**Og** tester (NFR-9) dekker tomme felt, tekst som ikke er testdata, at alle feilene kommer samtidig, og at nøkkelordlisten lagres og gir samme prosent når siden lastes på nytt (FR-9, FR-15, FR-34)
**Og** en test sjekker at testcaset gir nøkkelordtreffet som står i `fasit.md` (kriterium 2, FR-17)

### Story 2.6: Hele resultatsiden med forklaringer og «Tilbake»

Som student som søker jobb for første gang
vil jeg forstå hva gap-analysen og nøkkelordtreffet betyr,
slik at jeg vet hva jeg kan gjøre med CV-en min.

**Akseptansekriterier:**

**Gitt** resultatsiden
**Så** kommer gap-analysen først, så nøkkelordtreffet, så ATS-forklaringen (EXPERIENCE)
**Og** «Gap-analyse» er merket «Laget av KI» og har undertekst og «i»-ikon med teksten fra EXPERIENCE (FR-14, UX-DR13)
**Og** «Dette dekker CV-en din» har grønn bakgrunn med ✓, og «Dette kan du jobbe videre med» varm fersken med → (UX-DR13)
**Og** mellom gap-analysen og nøkkelordtreffet står linjen «Gap-analysen og nøkkelordtreffet kan si litt forskjellig. …» (FR-18)
**Og** «Nøkkelordtreff» har «i»-ikon, «X av Y = Z %» med «av nøkkelordene står i CV-en din», en prosentlinje (uten animasjon, den kommer i Epic 7), og listene «Står i CV-en (antall)» med ✓ og «Står ikke i CV-en (antall)» med ○. Listene kan ikke endres (FR-16, FR-17)
**Og** «Hva er ATS og hva betyr det for deg?» foldes ut og inn, og er lukket når siden åpnes (FR-18, UX-DR13)

**Gitt** en tom liste
**Så** vises teksten fra EXPERIENCE, for eksempel «Bra jobbet! CV-en din dekker alle kravene i annonsen. 🎉» eller «Ingen av nøkkelordene står i CV-en ennå.» (UX-DR13)

**Gitt** et «i»-ikon
**Så** åpnes og lukkes boksen med trykk, Enter og mellomrom, lukkes med Esc og åpnes med hover på PC, men ikke av fokus alene. Ikonet har `aria-expanded` og `aria-controls` (UX-DR11)
**Og** ikoner som bare er pynt, er skjult for skjermlesere (UX-DR21)
**Og** siden ruller ikke sidelengs ved 320, 375, 768 og 1280 px eller ved 200 % zoom (UX-DR19, NFR-7)
**Og** testdata med tomme lister (i en test, ikke i `testdata/`) gir de riktige tekstene

**Gitt** resultatsiden
**Så** står «Tilbake» (sekundærknapp, til venstre) nederst (FR-19, UX-DR4)

**Når** jeg trykker «Tilbake»
**Så** kommer jeg til innleggingen med alle feltene fortsatt fylt ut (FR-19)

**Når** jeg går videre igjen
**Så** kjøres analysen på nytt gjennom `sett_inndata`, og resultater som ikke lenger gjelder (gap, brev, korrektur, `lastet_ned`), nullstilles (AD-8)
**Og** nøkkelordlisten hentes også på nytt. Gjenbruken når bare CV-en er endret, kommer i story 7.3 (nødlisten punkt 1)
**Og** endres noe i feltene, også via «Tilbake» til modusvalget, settes steget tilbake til innlegging til analysen har lyktes igjen, så resultatsiden aldri vises med gamle eller tomme resultater (AD-8)

**Og** en test sjekker at samme CV og annonse kjørt to ganger i samme søknad, med «Tilbake» imellom, gir samme nøkkelordtreff i testmodus (kriterium 8, FR-15)

### Story 2.7: Ventetegn og feil fra KI-en

Som student
vil jeg se at nettsiden jobber, og få en tydelig melding hvis noe går galt,
slik at jeg ikke trykker flere ganger eller tror at det jeg har lagt inn, er borte.

**Akseptansekriterier:**

**Gitt** at jeg trykker «Sjekk CV-en min»
**Så** dekker ventetegnet siden med tre hoppende prikker, «På vei mot ny jobb» og «Vi sjekker CV-en din – det tar noen sekunder.» (FR-27, UX-DR14)
**Og** resten av siden, også hjørneraden, er `inert`, knappen får `aria-disabled` og beholder fokus, og et fast `role="status"`-område leser opp teksten (UX-DR14)
**Og** etterpå går fokus til den nye overskriften eller til feilboksen (UX-DR14)
**Og** serveren setter `opptatt` rundt KI-kallet. Kommer en ny POST mens `opptatt` er sann, sendes brukeren til siden for steget, og det startes ikke et nytt kall (AD-8)
**Og** ved `prefers-reduced-motion` hopper ikke prikkene (UX-DR18)

**Gitt** at KI-en gir `KIFeil`
**Så** vises samme side på nytt med feilboksen øverst: ved `nettverk` «Nettverksfeil, sjekk nettverkstilgangen.», ellers «Noe gikk galt hos KI-tjenesten. Prøv på nytt.», med «Det du har lagt inn, er ikke borte.» og knappen «Prøv på nytt» (FR-28, UX-DR7)
**Og** det jeg har lagt inn, er fortsatt der, og steget flyttes ikke (AD-8, AD-9)
**Og** et ubrukelig svar gir aldri en tom resultatside (FR-28)

**Og** tester (NFR-9, FR-28) bruker en `TestKI` som gir hver type `KIFeil`, og sjekker riktig tekst, at feltene er beholdt, og at en ny POST mens `opptatt` er sann ikke starter et nytt kall

## Epic 3: Få et søknadsbrev og laste det ned (Full generering)

Brukeren ser brevet, laster det ned som Word og får vinduet med «Lag ny søknad» og «Logg ut». Etter denne epicen virker hele flyten i testmodus (sjekkpunkt 29. november).

### Story 3.1: Se søknadsbrevet

Som student
vil jeg få et søknadsbrev basert på CV-en min og stillingsannonsen,
slik at jeg har et utkast å sende.

**Akseptansekriterier:**

**Gitt** resultatsiden i Full generering
**Så** står knappen «Lag søknadsbrevet mitt» nederst. Brevet lages først når jeg trykker på den (FR-21)

**Når** jeg trykker «Lag søknadsbrevet mitt»
**Så** vises ventetegnet med «Vi lager brevet ditt – det kan ta en liten stund.» (FR-27, UX-DR14)
**Og** `brev(cv, annonse, forslag=1)` kalles i `TestKI`, som leser `testdata/<case>/ki-svar/brev-1.json` (AD-3). `brev-1.json` er håndlaget i formen `{avsnitt: [str]}` og byttes ut med et ekte KI-svar i Epic 4 (AD-4, FR-38)
**Og** `kontroller()` gir `KIFeil(ubrukelig_svar)` når brevet er uten tekst (FR-28)
**Og** steget flyttes til brev, og jeg kommer til brevsiden (AD-8)

**Gitt** brevsiden
**Så** er overskriften «Din ferdigstilte søknad!», og brevet vises som et hvitt ark på høyst 720 px, med ett avsnitt per element i `avsnitt` (FR-22, UX-DR15)
**Og** brevet kan ikke redigeres, og siden har ingen «Tilbake» (FR-26, EXPERIENCE)

**Gitt** en `KIFeil` når brevet lages
**Så** vises resultatsiden på nytt med feilboksen og «Resultatet og det du har lagt inn, er ikke borte.» (FR-28, UX-DR7)

**Og** tester sjekker at brevsiden ikke kan åpnes før resultatet finnes, at et tomt brev gir feilmelding, og at brevteksten vises (FR-22, FR-28)

### Story 3.2: Laste ned brevet som Word

Som student
vil jeg laste ned brevet som Word,
slik at jeg kan jobbe videre med det og sende det.

**Akseptansekriterier:**

**Gitt** brevsiden
**Så** står knappen «Last ned som Word» (FR-29)

**Når** jeg trykker på den
**Så** lager `GET /last-ned/docx` filen med `adaptere/fil_ut.py` (python-docx), setter `lastet_ned` og sender filen (AD-8, AD-11)
**Og** filen har bare brevteksten med avsnittene, uten topp- eller bunntekst (FR-30)
**Og** filnavnet lages bare i `kjerne/filnavn.py` og er `Soknad_<ÅÅÅÅ-MM-DD>.docx`. Arbeidsgiveren i filnavnet kommer i Epic 7 (AD-11)
**Og** knappen blir grønn med «✓ Lastet ned som Word», og under står «Filnavn: Soknad_<dato>.docx» (UX-DR16)

**Gitt** at filen ikke kan lages (`FilFeil`)
**Så** vises feilboksen øverst på brevsiden med «Vi klarte ikke å lage filen. Prøv på nytt.» og «Prøv på nytt», og brevet er ikke borte (AD-9, EXPERIENCE)

**Og** tester (NFR-9, FR-30) åpner den nedlastede filen med python-docx og sjekker at teksten er lik brevet, uten topp- og bunntekst. En enhetstest sjekker filnavnet med datoen

### Story 3.3: Vinduet etter nedlasting

Som student
vil jeg velge hva jeg gjør etter at brevet er lastet ned,
slik at jeg enkelt kan lage en ny søknad eller logge ut.

**Akseptansekriterier:**

**Gitt** at jeg har lastet ned brevet
**Så** åpnes et vindu (`<dialog>` med `showModal()`) hver gang, med «Brevet er lastet ned!», filnavnet og «Vil du lage en ny søknad eller logge ut?» (FR-31, UX-DR16, UX-DR17)
**Og** vinduet har knappene «Lag ny søknad», «Logg ut» og «Bli her»

**Når** jeg trykker «Lag ny søknad»
**Så** kommer jeg til startsiden, og en ny søknad starter med tomme felt (FR-31, AD-7)

**Når** jeg trykker «Logg ut»
**Så** logges jeg ut som i story 1.4 (FR-6)

**Når** jeg trykker «Bli her» eller Esc
**Så** lukkes vinduet, og fokus går tilbake til knappen som åpnet det (UX-DR17)

**Og** fokus går til «Bli her» når vinduet åpnes, og vinduet har `aria-labelledby` og `aria-describedby` (UX-DR17)
**Og** en test sjekker at «Lag ny søknad» gir en tom søknad med testmodus beholdt (FR-31)

## Epic 4: Bruke ekte KI (Claude)

Med API-nøkkel kan testmodus slås av, og da bruker nettsiden Claude. Testdataene får ekte KI-svar, og det kommer et testcase til.

### Story 4.1: Koble til Claude for nøkkelord og gap-analyse

Som student
vil jeg at nettsiden bruker ekte KI på min egen CV og annonse,
slik at jeg får en analyse av akkurat min søknad.

**Før storyen:** konto i Claude Console (platform.claude.com), kreditt (for eksempel 10 dollar), auto-reload slått av, og API-nøkkelen i `backend/.env` (AD-13, NFR-2).

**Akseptansekriterier:**

**Gitt** `adaptere/ki.py`
**Så** har `EkteKI` de samme signaturene som `TestKI` for `nokkelord(annonse)` og `gap(cv, annonse)` (AD-3, NFR-11)
**Og** klienten er `Anthropic(timeout=90, max_retries=1)`, med begge verdiene satt uttrykkelig, og modellen fra `ANTHROPIC_MODEL` eller `claude-opus-5-5` (AD-12, AD-13)

**Gitt** `prompts/nokkelord.md` og `prompts/gap.md` i Git (NFR-10)
**Så** sendes hver oppgave med sin prompt og sitt JSON-skjema med structured outputs (`output_config.format`), med `additionalProperties: false` og alle felt påkrevd (AD-4)
**Og** svaret går gjennom den samme `kontroller()` som i testmodus, som også gir `KIFeil(ubrukelig_svar)` når `stop_reason` ikke er `end_turn` (AD-4)
**Og** `nokkelord` gir også `arbeidsgiver` (eller `null`), som lagres i økten for Epic 7 (AD-4)
**Og** prompten for `nokkelord` ber om 8–20 nøkkelord på 1–3 ord hver, uten duplikater. En liste som er tom eller lengre enn 30 nøkkelord, gir `KIFeil(ubrukelig_svar)` (FR-15, endret i PRD-en 12. november)

**Gitt** en nettverksfeil
**Så** kastes `KIFeil(nettverk)`, og andre API-feil gir `KIFeil(annet)` (AD-13, FR-28)
**Og** svarer ikke Claude innen 90 s, heller ikke etter det ene nye forsøket, gir det `KIFeil(annet)` og «Noe gikk galt hos KI-tjenesten. Prøv på nytt.», ikke «Nettverksfeil» (EXPERIENCE, State Patterns). I anthropic-biblioteket er `APITimeoutError` en underklasse av `APIConnectionError`, så tidsavbrudd må sjekkes før tilkoblingsfeil

**Gitt** et KI-kall
**Så** skrives KI-oppgave, tokens og anslått pris til terminalen, og loggen viser aldri CV, annonse, brev, passord eller nøkkel (AD-12, AD-13)

**Og** testene (NFR-9) bruker en falsk Anthropic-klient og kaller aldri det ekte API-et. De sjekker riktig skjema, nettverksfeil, tidsavbrudd (gir `annet`), annen feil, feil `stop_reason` og ugyldig JSON (FR-28)
**Og** før kodingen sjekkes navnet på parameteren for structured outputs og verdiene for `stop_reason` mot dokumentasjonen for anthropic 2.4.0 (claude-api-skillen). Avviker de fra AD-4, oppdateres arkitekturen (AD-15)
**Og** nettsiden bruker fortsatt `TestKI` til bryteren kan slås av i story 4.3

### Story 4.2: Brevet fra Claude

Som student
vil jeg at brevet høres ut som et ekte, formelt søknadsbrev og bare bygger på det jeg har lagt inn,
slik at jeg kan sende det uten å skamme meg eller si noe som ikke stemmer.

**Akseptansekriterier:**

**Gitt** `prompts/brev.md` i Git (NFR-10)
**Så** inneholder den kravene i FR-24: norsk, formell og akademisk tone, stillingen og arbeidsgiveren ved navn, minst to konkrete krav fra annonsen koblet til CV-en, og listen over de 17 typiske KI-frasene fra addendum som ikke skal brukes (AD-14)
**Og** den inneholder FR-37: brevet bygger bare på CV og annonse og legger ikke til erfaring, utdanning eller ferdigheter som ikke står der. Omformulering og kobling til kravene er lov (AD-14)

**Gitt** `EkteKI.brev(cv, annonse, forslag)`
**Så** sendes bare CV og annonse, med skjemaet `{avsnitt: [str]}`, og svaret går gjennom `kontroller()` (AD-3, AD-4)

**Og** en test med falsk klient sjekker skjemaet og at bare CV og annonse sendes med (FR-37)
**Og** nettsiden bruker fortsatt `TestKI` til bryteren kan slås av i story 4.3. Brevet prøves med ekte KI der

### Story 4.3: Slå av testmodus, med samtykke og KI-merknad

Som student
vil jeg vite når teksten min sendes til ekstern KI, og selv samtykke til det,
slik at jeg bestemmer over mine egne opplysninger.

**Akseptansekriterier:**

**Gitt** at `ANTHROPIC_API_KEY` finnes
**Så** kan bryteren «Testmodus» slås av og på, bare på startsiden (`steg == start`). Valget lagres i `Innlogging.testmodus` og huskes til utlogging. Etter ny innlogging er den av (FR-32, AD-7, AD-8)
**Og** uten nøkkel er den fortsatt låst på som i story 2.4
**Og** web-laget velger `EkteKI` når testmodus er av og `TestKI` når den er på (AD-3)

**Gitt** startsiden med testmodus av
**Så** står «Teksten din sendes til ekstern KI.» over avkrysningsboksen (22 px) «Jeg samtykker til bruk av KI», med «i»-ikon og «i»-boksen med de fire punktene fra EXPERIENCE (FR-36, UX-DR10, UX-DR11)
**Og** avkrysningsboksen er alltid tom når startsiden åpnes, også i samme økt og etter at testmodus er slått på og av igjen (UX-DR10, UX-DR22)

**Når** jeg trykker «Begynn å lage søknad» uten avkryssing
**Så** får boksen rød ramme, «Du må samtykke før du kan begynne» vises, og fokus går til boksen (FR-36, UX-DR10)

**Gitt** testmodus på
**Så** er samtykket skjult, og «Begynn å lage søknad» virker uten (FR-36)

**Gitt** en side med testmodus av
**Så** står «ⓘ Teksten behandles av ekstern KI» nede til venstre i hjørneraden, fra `base.html` (FR-35, UX-DR3)

**Og** i vanlig modus sendes tekst til Claude bare når `Soknad.samtykke` er sann (AD-12)
**Og** tester sjekker: bryteren kan ikke endres etter startsiden, samtykke kreves når testmodus er av, ikke når den er på, og ingen KI-kall uten samtykke (FR-32, FR-36)
**Og** hvert innleggingsfelt godtar høyst 15 000 tegn, med egen feilmelding, og hver søknad kan bruke høyst 10 KI-kall, medregnet «Prøv på nytt» og «Nytt forslag». Deretter får brukeren en melding. Grensene ligger i `innstillinger.py` og har tester (NFR-11, endret i PRD-en 12. november)
**Og** Kristine prøver hele flyten én gang med ekte KI på testdataene: analysen, og brevet mot sjekklisten i `fasit.md` for kriterium 11 og 12 (AD-14). Hun noterer resultatet i PR-en, og hvor lang tid analysen og brevet tar, så 90 s kan justeres i `innstillinger.py` (arkitekturen, Utsatt)

### Story 4.4: Ekte KI-svar i testmodus

Som sensor
vil jeg at de ferdige svarene i testmodus er ekte KI-svar,
slik at testmodus viser hvordan nettsiden faktisk virker.

**Akseptansekriterier:**

**Gitt** `scripts/lag_testsvar.py`
**Når** det kjøres med API-nøkkel
**Så** kjører det `EkteKI` på hvert testcase og skriver `ki-svar/nokkelord.json`, `gap.json`, `brev-1.json` og `brev-2.json` (`forslag` 1 og 2) med bare objektet fra AD-4 (FR-38, AD-4)
**Og** de håndlagde svarene fra Epic 2 og 3 er byttet ut

**Gitt** promptene for nøkkelord, gap og brev
**Så** er hver kjørt tre ganger og sjekket mot fasiten, og resultatet for kriterium 1, 3, 11 og 12 står i `my-project/testplan.md`, også når noe feiler, med plan B fra PRD del 5 (NFR-12)

**Og** en test sjekker at ingen av de 17 KI-frasene står i `brev-1.json` og `brev-2.json` (FR-24, FR-38)
**Og** `fasit.md` markerer hvilke nøkkelord som er viktige, og i hver av de tre kjøringene har nøkkelordlisten fra KI-en alle de viktige (suksesskriterium 14, FR-15)
**Og** testplanen viser tokens og kroner per fullført søknad, fra loggen (mål: under 3 kr, NFR-11)
**Og** alle testene som bruker testdataene, går fortsatt gjennom med de nye svarene
**Og** README sier at testsvarene er ekte KI-svar, og hvordan skriptet kjøres (NFR-8, FR-38)
**Og** Kristine prøver om KI-en forstår teksten fra Canva-CV-en riktig (hva som er utdanning, jobb og oppsummering) og noterer det i testplanen

### Story 4.5: Et testcase til, og kriterium 3

Som sensor
vil jeg at nettsiden er prøvd på mer enn én CV og annonse,
slik at suksesskriteriene ikke bare holder for ett eksempel.

**Akseptansekriterier:**

**Gitt** `testdata/case-2-<navn>/`
**Så** finnes en annen fiktiv CV (`cv.txt`) og en annen stillingsannonse (`annonse.txt`), gjerne fra et annet fagfelt enn case 1, med tydelige hull mot annonsen (NFR-3)
**Og** CV-en er ulik CV-en i case 1, fordi CV-en avgjør testcaset (AD-10)
**Og** `fasit.md` har kravene med begrunnelse, nøkkelordene med de viktige markert (suksesskriterium 14) og det forventede nøkkelordtreffet, som i story 2.2 (NFR-3)
**Og** `scripts/lag_testsvar.py` har laget `ki-svar/` for case 2, og testene som går gjennom testcasene, dekker begge, også testen for kriterium 2 (FR-38)
**Og** case 2 er for Full generering. Korrektur (kriterium 4 og 12) testes med case 1, og README sier det (NFR-8)

**Gitt** kriterium 1 og 11
**Så** er de også kjørt tre ganger på case 2 med ekte KI, og resultatet står i testplanen (NFR-12)

**Gitt** kriterium 3 («samme CV med to ulike annonser»)
**Så** er CV-en fra case 1 kjørt med ekte KI mot annonsen fra case 1 og mot annonsen fra case 2, tre ganger hver, og testplanen viser om brevene nevner krav som er spesifikke for hver annonse (FR-22)

**Og** Claude lager utkastet til testdataene, og Kristine sjekker og godkjenner dem før PR-en flettes

## Epic 5: Korrektur av eget brev

Brukeren legger inn sitt eget brev og får en forbedret versjon med markerte endringer. Et klikk på en markert setning viser den gamle.

### Story 5.1: Velge Korrektur og legge inn eget brev

Som student som har skrevet et brev selv
vil jeg velge Korrektur og legge inn brevet mitt,
slik at jeg kan få det forbedret i stedet for å få et helt nytt.

**Akseptansekriterier:**

**Gitt** modusvalget
**Så** står kortet ✏️ «Korrektur» · «Forbedre mitt brev» · «Du har skrevet et brev selv. Vi forbedrer språket og beholder innholdet ditt.» ved siden av Full generering, og under hverandre under 700 px. Hele kortet er én knapp (FR-20, UX-DR12)

**Gitt** innleggingen i Korrektur med overskriften «Legg inn CV-en din, brevet ditt og stillingsannonsen»
**Så** finnes feltene «📄 CV», «✉️ Ditt søknadsbrev» og «📢 Stillingsannonse», med de samme tilstandene, tekstene og feilene som i story 2.5 (FR-8, FR-9, FR-13, UX-DR8)
**Og** et brev som ikke hører til samme testcase som CV-en, gir «Ditt søknadsbrev: I testmodus fungerer bare testdataene fra mappen backend/testdata/.» (FR-34, AD-10)
**Og** «Tilbake» til modusvalget beholder CV og annonse. Feltet for eget brev finnes bare i Korrektur (EXPERIENCE)

**Gitt** `testdata/case-1-<navn>/`
**Så** finnes et fiktivt `eget-brev.txt` til samme annonse, med ting som bør forbedres og minst én av KI-frasene fra addendum, og `fasit.md` har en sjekkliste for Korrektur (innhold, eksempler og rekkefølge beholdt, og at KI-frasen er skrevet om) (FR-34, NFR-3, AD-14)
**Og** README sier hvor testbrevet ligger (NFR-8)

**Gitt** resultatsiden i Korrektur
**Så** viser den gap-analysen og nøkkelordtreffet som i Full generering. Knappen videre til brevet kommer i story 5.2

**Og** tester sjekker at brevfeltet må fylles ut i Korrektur, ikke finnes i Full generering, og gir `ikke_testdata` på eget felt (FR-9, FR-34)

### Story 5.2: Forbedret brev fra KI-en

Som student
vil jeg få en forbedret versjon av brevet mitt som beholder innholdet mitt,
slik at brevet fortsatt er min egen stemme.

**Akseptansekriterier:**

**Gitt** `prompts/korrektur.md` i Git (NFR-10)
**Så** inneholder den kravene i FR-24 og FR-37 og listen over de 17 KI-frasene, og sier at brukerens innhold, eksempler og rekkefølge beholdes (FR-24, AD-14)
**Og** den sier at én setning aldri deles i to oppføringer. Blir en lang setning til to, står begge i samme `ny` (AD-5)
**Og** den sier at KI-en skriver om typiske KI-fraser hvis brukeren har brukt dem selv (addendum)

**Gitt** `korrektur(cv, annonse, eget_brev, forslag)` i `EkteKI` og `TestKI`
**Så** er svaret `{setninger: [{ny, gammel, nytt_avsnitt}]}` i brevets rekkefølge, med skjema og structured outputs (AD-3, AD-4)
**Og** `kontroller()` gir `KIFeil(ubrukelig_svar)` når alle `ny` er `null`, eller når alle `gammel` satt sammen og vasket ikke er lik det opprinnelige brevet, også vasket (AD-4, AD-10)

**Gitt** resultatsiden i Korrektur
**Så** står knappen «Oppdater søknadsbrevet mitt» nederst (EXPERIENCE)

**Når** jeg trykker «Oppdater søknadsbrevet mitt»
**Så** vises ventetegnet med «Vi lager brevet ditt – det kan ta en liten stund.», og jeg kommer til brevsiden med «Din oppdaterte søknad er ferdig!» (FR-23, FR-27)
**Og** brevet som vises, er alle `ny` som ikke er `null`, satt sammen med nytt avsnitt der `nytt_avsnitt` er sann, foreløpig uten markeringer (AD-5)
**Og** «Last ned som Word» og vinduet etter nedlasting virker som i Epic 3, og filen inneholder det samme brevet (FR-29, FR-30)

**Gitt** `scripts/lag_testsvar.py`
**Så** lager det også `korrektur-1.json` og `korrektur-2.json`, og Korrektur-prompten er kjørt tre ganger og sjekket mot fasiten, med resultatet i testplanen (FR-38, NFR-12)

**Og** tester sjekker `kontroller()` for Korrektur (`gammel` som ikke blir originalen, alle `ny` null) og at brevet settes riktig sammen med avsnitt (FR-28, FR-23)
**Og** en test sjekker at ingen av de 17 KI-frasene står i noen `ny` i `korrektur-1.json` og `korrektur-2.json` (FR-24, FR-38)

### Story 5.3: Se hva som er endret i Korrektur

Som student
vil jeg se hvilke setninger KI-en har endret, og hva jeg skrev før,
slik at jeg kan bestemme om jeg er enig i endringene.

**Akseptansekriterier:**

**Gitt** brevsiden i Korrektur
**Så** står «Grønn og understreket = endret. Trykk på setningen for å se det du skrev.» over brevet (UX-DR15)
**Og** en setning er endret når `gammel != [ny]`, ny når `gammel == []` og fjernet når `ny == null`. Visningen sammenligner aldri tekst selv (AD-5)
**Og** endrede og nye setninger er knapper med grønn bakgrunn og understreking og den skjulte teksten «Endret setning» for skjermlesere, så endringen ikke bare vises med farge (FR-23, UX-DR15)

**Når** jeg trykker på en endret setning (eller Enter eller mellomrom)
**Så** vises «Du skrev» med den gamle setningen rett under, og et nytt trykk lukker den. Flere kan være åpne samtidig (FR-23, UX-DR15)
**Og** to setninger som er slått sammen, viser begge de gamle. En ny setning viser «(Ny setning)»

**Gitt** fjernede setninger
**Så** står én linje under brevet: «1 setning er fjernet.» eller «2 setninger er fjernet.» (UX-DR15)

**Gitt** at ingenting er endret
**Så** står «Vi fant ingenting å endre. Brevet ditt er bra som det er.», og forklaringen over brevet er skjult (UX-DR15)

**Og** tester (NFR-9, FR-30) sjekker at den nedlastede filen ikke har noen markeringer, «Du skrev» eller «(Ny setning)», og at endret, ny, fjernet og uendret vises riktig ut fra `ny` og `gammel` (FR-23)
**Og** denne storyen er punkt 4 på nødlisten. Kuttes den, virker Korrektur som etter story 5.2

## Epic 6: Laste opp CV og annonse som PDF

Brukeren kan laste opp PDF i stedet for å lime inn tekst, med feilmelding ved feil filtype, uleselig PDF og for stor fil, og PDF-tipset.

### Story 6.1: Laste opp PDF

Som student
vil jeg laste opp CV-en og annonsen som PDF,
slik at jeg slipper å kopiere teksten selv.

**Akseptansekriterier:**

**Gitt** et innleggingsfelt i tom tilstand
**Så** står «Last opp PDF» ved siden av «Lim inn tekst», og filvelgeren har `accept=".pdf"`. Skjermlesere hører for eksempel «Last opp PDF, CV» (FR-8, UX-DR8)
**Og** over feltene står i begge modusene: «Tips: PDF lagret fra Word leses best. Er CV-en laget i Canva eller et lignende program, kan teksten komme i feil rekkefølge. Lim den da heller inn.» (UX-DR24)

**Når** jeg velger en fil
**Så** vises filnavnet med ✓ med en gang, et langt navn kuttes med «…», fokus går til søppelbøtta, og skjermlesere hører «CV lastet opp: <filnavn>» (UX-DR8)
**Og** filen sjekkes ikke før jeg trykker «Sjekk CV-en min» (EXPERIENCE)

**Når** jeg trykker søppelbøtta
**Så** fjernes filen, feltet går tilbake til tom tilstand, og fokus går til «Last opp PDF» (FR-13, UX-DR8)

**Når** jeg trykker «Sjekk CV-en min»
**Så** leses teksten bare i `adaptere/pdf_inn.py` med pypdf og vanlig `extract_text()`, og teksten og filnavnet lagres i økten, ikke på disk (AD-11, NFR-4)

**Gitt** hvert testcase i `testdata/`
**Så** finnes `cv.pdf` og `annonse.pdf`, og i case 1 også `eget-brev.pdf`, med samme tekst som `.txt`-filene, lagret fra Word
**Og** en test per case sjekker at `.pdf` og `.txt` gjenkjennes som samme case, og at `cv.pdf` og `cv.txt` gir samme nøkkelordtreff (kriterium 5, AD-10, FR-34)

**Gitt** en fiktiv CV med en tabell (for eksempel ferdighetene i en tabell), laget i Word og lagret som PDF
**Når** den leses med pypdf
**Så** står resultatet i PR-en og i testplanen. Kommer teksten ut i feil rekkefølge, blir det en kjent begrensning i README, og tabeller settes på kuttlisten i PRD-en, med dato og grunn i beslutningsloggen (arkitekturen, Utsatt; addendum)

### Story 6.2: Feilmeldinger for filer

Som student
vil jeg få en tydelig melding når en fil ikke kan brukes,
slik at jeg vet hva jeg skal gjøre i stedet.

**Akseptansekriterier:**

**Gitt** at jeg trykker «Sjekk CV-en min»
**Når** en fil ikke er PDF
**Så** vises «CV: Feil filtype, prøv PDF.» (FR-10, AD-9)

**Når** en fil er større enn 5 MB
**Så** vises «CV: Filen er for stor. Den kan være på høyst 5 MB.» (FR-12)
**Og** er hele forespørselen over `MAX_CONTENT_LENGTH` (16 MB), viser en egen 413-håndterer feilboksen med `for_stor` (AD-9, AD-11)

**Når** pypdf gir færre enn 50 bokstaver, for eksempel fra en skannet PDF
**Så** vises «CV: Vi klarer ikke å lese teksten i PDF-en. Den kan være skannet. Lim inn teksten i stedet.» (FR-11, AD-11)

**Og** feltnavnet byttes ut («CV», «Ditt søknadsbrev», «Stillingsannonse»), alle feilene vises samtidig i feilboksen i rekkefølgen tom → feil filtype → for stor → uleselig → ikke testdata, og felt uten feil beholdes (AD-9, UX-DR7)
**Og** feilene virker også i testmodus (FR-34)
**Og** grensene 5 MB, 16 MB og 50 bokstaver ligger i `innstillinger.py`

**Gitt** `testdata/feil/`
**Så** finnes `skannet.pdf` (bilde uten tekst) og `feil-type.docx` (FR-34, NFR-3)
**Og** `.gitignore` får unntaket `!backend/testdata/feil/feil-type.docx`, fordi regelen `*.docx` ellers skjuler filen fra Git. En test sjekker at filen finnes, så CI feiler hvis den mangler på GitHub
**Og** grensen på 50 bokstaver prøves med `skannet.pdf` og PDF-ene i testdataene, og justeres i `innstillinger.py` hvis den ikke skiller dem (arkitekturen, Utsatt)
**Og** tester (NFR-9) dekker feil filtype, for stor fil, uleselig PDF og 413 (FR-10, FR-11, FR-12)

## Epic 7: Ekstra valg og pynt (nødliste 1–3 og UX-kuttlisten)

«Nytt forslag», nedlasting som PDF, gjenbruk av nøkkelordlisten når bare CV-en er endret, og pynten fra UX-kuttlisten. Storiene står i motsatt rekkefølge av nødlisten: det som kuttes først, bygges sist. Pynten fra UX-kuttlisten kommer etter nødlistepunktene, i egne stories etter at kjerneflyten virker i testmodus (UX-DR23).

### Story 7.1: Nytt forslag

Som student
vil jeg kunne be om et nytt forslag til brevet,
slik at jeg kan velge det jeg liker best.

**Akseptansekriterier:**

**Gitt** brevsiden
**Så** står «Nytt forslag» under nedlastingsknappene (FR-25)

**Når** jeg trykker «Nytt forslag»
**Så** åpnes vinduet «Vil du ha et nytt forslag?» med «Brevet du ser nå, blir slettet. Har du ikke lastet det ned, er det borte.», «Ja, lag nytt forslag» og «Avbryt». Fokus går til «Avbryt», Esc lukker, og fokus går tilbake til knappen (UX-DR17)

**Når** jeg trykker «Ja, lag nytt forslag»
**Så** økes `forslag` med `nytt_forslag` i kjernen, ventetegnet vises, og jeg får et nytt brev. I testmodus gir oddetall `-1` og partall `-2` (AD-3, AD-8)
**Og** i Korrektur sendes alltid det opprinnelige `eget_brev` (FR-25, AD-5)
**Og** nedlastingsknappene og filnavn-linjen nullstilles, og `lastet_ned` settes til usann (UX-DR16, AD-8)

**Gitt** en `KIFeil` ved nytt forslag
**Så** beholdes det gamle brevet, og feilboksen sier «Brevet du hadde, er beholdt.» (FR-28, EXPERIENCE)

**Og** tester sjekker at forslag 1 og 2 gir ulike testbrev, at Korrektur bruker originalbrevet, og at det gamle brevet er beholdt ved feil (FR-25, FR-28)

### Story 7.2: Laste ned brevet som PDF

Som student
vil jeg også kunne laste ned brevet som PDF,
slik at jeg kan sende det med en gang uten å åpne Word.

**Akseptansekriterier:**

**Gitt** brevsiden
**Så** står «Last ned som PDF» ved siden av «Last ned som Word» (FR-29)

**Når** jeg trykker på den
**Så** lager `GET /last-ned/pdf` filen i `adaptere/fil_ut.py` med fpdf2 og TTF-skriften i `soknad/fonts/`, så æ, ø og å vises riktig (AD-11)
**Og** skriften velges i denne storyen: en TTF med fri lisens og æ, ø og å (for eksempel Noto Sans eller DejaVu Sans), med lisensfilen ved siden av (arkitekturen, Utsatt)
**Og** filen har bare brevteksten med avsnittene, uten markeringer og uten topp- eller bunntekst (FR-30)
**Og** knappen blir grønn med «✓ Lastet ned som PDF», filnavn-linjen viser `.pdf`, og vinduet etter nedlasting åpnes (UX-DR16, FR-31)
**Og** «Bli her» i vinduet lar meg laste ned det andre formatet

**Og** tester (NFR-9, FR-30) leser PDF-en med pypdf og sjekker at teksten med æøå er lik brevet, uten markeringer

### Story 7.3: Gjenbruke nøkkelordlisten når bare CV-en er endret

Som student
vil jeg at prosenten regnes fra den samme nøkkelordlisten når jeg bare har endret CV-en,
slik at jeg kan se om endringen min faktisk ga bedre treff.

**Akseptansekriterier:**

**Gitt** at jeg har gått tilbake fra resultatsiden (story 2.6)
**Når** jeg bare har endret CV-en og går videre igjen
**Så** er den vaskede annonseteksten lik, og `sett_inndata` beholder den lagrede nøkkelordlisten. Den hentes ikke på nytt fra KI-en (FR-15, FR-19, AD-8)
**Og** gap-analysen kjøres fortsatt på nytt

**Når** annonsen er endret
**Så** hentes en ny nøkkelordliste

**Og** tester (NFR-9, FR-15) sjekker at nøkkelordlisten gjenbrukes når bare CV-en er endret, også med ekstra mellomrom i annonsen, at den hentes på nytt når annonsen er endret, og at KI-en ikke kalles for nøkkelord når listen gjenbrukes
**Og** denne storyen er punkt 1 på nødlisten. Kuttes den, hentes nøkkelordlisten på nytt hver gang, som etter story 2.6

### Story 7.4: Pynt: fyrverkeri og bevegelse

Som student
vil jeg at nettsiden føles hyggelig å bruke,
slik at det blir litt gøy å bli ferdig med søknaden.

**Akseptansekriterier:**

**Gitt** brevsiden
**Når** den åpnes, også etter nytt forslag
**Så** vises fyrverkeri rundt brevoverskriften i ca. 2,2 s, borte etter ca. 3,2 s, med høyst 3 utbrudd i sekundet og bak teksten (UX-DR18)

**Gitt** resultatsiden
**Så** fylles prosentlinjen på 1 s når siden åpnes. Tallet står alltid som tekst (UX-DR13)

**Gitt** modusvalget
**Så** løftes kortet 4 px og ikonet vipper ved hover (UX-DR12)

**Og** ved `prefers-reduced-motion` slås alle animasjoner av (UX-DR18)
**Og** animasjonene bruker bare små skript uten rammeverk og endrer aldri søknadsdata (AD-1), og ikonene er skjult for skjermlesere (UX-DR21)

### Story 7.5: Logg ut før nedlasting, og arbeidsgiver i filnavnet

Som student
vil jeg bli advart før jeg logger ut uten å ha lastet ned brevet, og få filer som er lette å skille,
slik at jeg ikke mister brevet ved et uhell og finner riktig søknad senere.

**Akseptansekriterier:**

**Gitt** brevsiden før brevet er lastet ned i noe format
**Når** jeg trykker «Logg ut»
**Så** åpnes vinduet «Du har ikke lastet ned brevet. Vil du logge ut likevel? Brevet blir slettet.» med «Logg ut» og «Avbryt». Fokus går til «Avbryt», og Esc lukker (UX-DR17, UX-DR22)
**Og** er brevet lastet ned, logges jeg ut med en gang (NFR-4)

**Gitt** `arbeidsgiver` fra nøkkelordsvaret
**Så** blir filnavnet `Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>`: æ → ae, ø → o, å → a, andre tegn til ASCII, mellomrom til bindestrek, alt annet enn `[A-Za-z0-9-]` fjernet, høyst 30 tegn. Uten arbeidsgiver er det `Soknad_<dato>` (AD-11)
**Og** filnavnet i vinduet og i filnavn-linjen er det samme som filen får

**Og** enhetstester for `kjerne/filnavn.py` dekker æøå, mellomrom, spesialtegn, 30 tegn og manglende arbeidsgiver (AD-11)

## Epic 8: Klar for sensor

Sensor kan installere nettsiden og vurdere den etter README. README er oppdatert underveis og gjøres ferdig her, testplanen skrives, skjermbildene med ekte KI tas, og README prøves fra en ny kopi av repoet.

### Story 8.1: README for sensor

Som sensor
vil jeg ha en README som sier alt jeg trenger,
slik at jeg får nettsiden i gang på 10–15 minutter.

**Akseptansekriterier:**

**Gitt** `README.md` i roten av repoet, som er oppdatert underveis i hver story (se Arbeidsmåte)
**Så** har den (NFR-8):
- en kort beskrivelse av hva nettsiden gjør og hvem den er for
- forutsetninger med versjoner
- én kommando for å installere uv på Windows og én på Mac, og så `cd backend`, `uv sync` og `uv run flask --app soknad run`
- innstillingene, med henvisning til `.env.example` (NFR-2), og at nettsiden starter i testmodus uten API-nøkkel (FR-32)
- e-post og passord til testbrukeren
- hvor testdataene og fasiten ligger (NFR-3), og hvordan testene kjøres (NFR-9)
- kjente begrensninger, også telleregelen (FR-17, og at «C» gir treff i «C#»), testmodus (FR-34, og at Korrektur-testdataene ligger i case 1), PDF fra Canva (all teksten kommer med, men i rotete rekkefølge, så da kan teksten limes inn) og resultatet av prøven med tabell fra story 6.1
- to–tre skjermbilder med ekte KI på (FR-38)
- en oversikt over mappestrukturen
- lenker til planleggingsdokumentene og prompt-loggen

**Og** seksjonene som var merket «kommer», er fylt ut
**Og** lærerens CI-sjekk av at `README.md` og `my-project/1-product-brief/product-brief.md` finnes, går fortsatt gjennom

### Story 8.2: Testplan og prøve fra en ny kopi

Som sensor
vil jeg se hva som er testet for hånd, og med hvilket resultat,
slik at jeg kan vurdere suksesskriteriene som ikke har automatiske tester.

**Akseptansekriterier:**

**Gitt** `my-project/testplan.md`
**Så** har den resultatet for hvert suksesskriterium som ikke testes automatisk, med dato, hva som ble gjort, og bestått eller ikke bestått (NFR-12)
**Og** hele flyten er prøvd for hånd i begge modusene, både i testmodus og med ekte KI
**Og** sjekkene av tastatur, kontrast (WCAG AA), synlige etiketter og alternativtekst (NFR-6), og av 320, 375, 768 og 1280 px og 200 % zoom (NFR-7, UX-DR19), er skrevet inn
**Og** resultatet fra testen med kollegaen (kriterium 13) står der
**Og** resultatene med ekte KI fra story 4.4, 4.5 og 5.2 står der, med plan B der noe feilet

**Gitt** en ny kopi av repoet i en tom mappe
**Når** README følges fra start
**Så** er det gjort to ganger, med dato og resultat i testplanen (NFR-12):
- første gang før funksjonsstopp, helgen 5.–6. desember, med README slik den er etter Epic 1–6
- andre gang rett før levering, etter story 8.1
