# Epic 1 Context: Registrere seg og logge inn

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Brukeren kan registrere seg, logge inn og logge ut, og alle andre sider er stengt uten innlogging. Epicen lager også hele startstrukturen som resten av prosjektet bygger på: Flask-appen i `backend/`, uv, CI med ruff og pytest, `base.html` med fargene og de faste elementene, den lokale databasen og testbrukeren. Den er viktig fordi innlogging står på «kuttes aldri»-listen, og fordi sensor må kunne starte nettsiden fra en ny kopi av repoet og logge inn med testbrukeren fra README uten noe oppsett.

## Stories

- Story 1.1: Nettsiden starter fra en ny kopi av repoet
- Story 1.2: Logge inn med testbrukeren
- Story 1.3: Registrere seg som ny bruker
- Story 1.4: Logge ut, og bare innloggede kommer inn

## Requirements & Constraints

- Registrering med e-post og passord (minst 8 tegn) og så automatisk innlogging. Gjenta passord må være likt, og e-posten må ha gyldig form. E-post som finnes fra før, gir egen feil. E-post sammenlignes uten mellomrom foran og bak og uten forskjell på store og små bokstaver.
- Innlogging med e-post og passord. Feil gir «Feil e-post eller passord», uten rød ramme på feltene.
- Tomme felt får rød ramme og en kort tekst ved feltet, for eksempel «Fyll inn e-post». Feil vises aldri bare med farge, og alle feilene vises samtidig.
- Etter innlogging eller registrering kommer brukeren alltid til startsiden («Velkommen! 👋» og ingressen). Knappen «Begynn å lage søknad» kommer i Epic 2.
- Brukeren kan logge ut. Alle sider unntatt innlogging, registrering og static krever innlogging. Ellers sendes man til innloggingen med «Du må logge inn først».
- Passord lagres bare hashet. Innloggingen virker lokalt uten noen ekstern tjeneste. API-nøkkelen havner aldri i Git, og `.env.example` viser innstillingene uten verdier.
- Sensor skal få nettsiden i gang på 10–15 minutter med README. Databasen og testbrukeren (`test@example.com` / `testpassord1`) lages automatisk ved første oppstart, og bare én gang.
- Tilgjengelighet: WCAG AA-kontrast, alt kan brukes med bare tastatur, synlige etiketter. Ingen rulling sidelengs ved 320, 375, 768 og 1280 px og ved 200 % zoom.
- Automatiske tester for innlogging (riktig, feil passord, ukjent e-post, tomme felt, hashing, testbrukeren én gang), registrering (e-post finnes, for kort passord, ulike passord, ugyldig e-post) og at alle sider krever innlogging. Testen for innlogging skal gå gjennom alle registrerte ruter, så sider fra senere epics blir testet automatisk.
- Suksesskriterium: en ny bruker kan registrere seg, feil passord gir ikke tilgang, og testbrukeren fra README virker.

## Technical Decisions

- **Lagdelt monolitt:** Python + Flask med Jinja-maler. Lagene er `soknad/web/` (ruter, maler, tekster, innloggingssjekk), `soknad/kjerne/` (regler uten I/O) og `soknad/adaptere/` (database, øktlager). `kjerne/` importerer aldri flask, sqlite3 eller andre I/O-biblioteker og leser ingen filer. JavaScript bare i små skript uten rammeverk, og det endrer aldri data.
- **Startstruktur:** all kode i `backend/`. I Epic 1 trengs `pyproject.toml`, `uv.lock`, `.python-version` (Python ≥ 3.12), `soknad/__init__.py` med `create_app(test_config)`, `soknad/innstillinger.py`, `soknad/web/` og `tests/`. Andre mapper lages først når en story trenger dem. Versjoner: Flask 3.1.3, python-dotenv 1.2.4, pytest 9.2.0, ruff 0.17.3.
- **Oppstart uten `.env`:** `create_app` leser `.env` hvis den finnes. Mangler `SECRET_KEY`, lages en tilfeldig. Databasen er SQLite i `instance/brukere.db`, og `instance/` står i `.gitignore`. Alle filer åpnes med `encoding="utf-8"`.
- **Passord:** `werkzeug.security`. Loggen viser aldri passord eller nøkkel.
- **Økt:** `kjerne/okt.py` har `Innlogging(bruker_id, testmodus)`, lagret i minnet i `adaptere/oktlager.py` og nøklet på en tilfeldig økt-id. Den signerte cookien har bare økt-id-en. Innlogging gir alltid ny økt-id. Utlogging sletter `Innlogging` (og `Soknad` når den finnes). En gyldig cookie uten økt i minnet (etter omstart) betyr utlogget. Ingen automatisk utlogging. Ingen løse strengnøkler.
- **Ruter:** `login_required` på alt unntatt innlogging og registrering. Etter innlogging alltid til startsiden, og `next=` brukes ikke. Lykkes en POST, sendes brukeren videre med redirect. Feiler den, vises samme side på nytt uten redirect.
- **Feil:** lukkede typer i `kjerne/feil.py`. Inndatafeil returneres som en liste av `InndataFeil(felt, type)`. Typene i denne epicen er `tom`, `epost_finnes`, `epost_ugyldig`, `passord_kort`, `passord_ulike` og `feil_innlogging`. Alle brukertekster ligger i `web/tekster.py`, og grenser og konstanter (også testbrukeren) i `innstillinger.py`.
- **CI:** lærerens `.github/workflows/ci.yml` utvides i backend-jobben, den byttes ikke ut. Den kjører `ruff check`, `ruff format --check` og `pytest` på Linux og Windows. Ruff-regelen `PLW1514` slås på, og det må sjekkes at den faktisk slår til (kan kreve `preview`).
- **Tester:** `tests/` speiler `soknad/`. Webtester bruker `create_app(test_config)` med midlertidig SQLite og `test_client`. Hver testfil og testfunksjon nevner FR- eller NFR-nummeret.
- **Konvensjoner:** norske domeneord uten æøå, `snake_case`, felles elementer bare i `base.html`, ingen utkommentert kode i `main`.
- **Arbeidsmåte:** egen branch og PR per story med story og FR-nummer i tittelen, en kort merknad om hva KI-verktøyet gjorde feil, og grønn CI før fletting. README oppdateres i samme story når installasjon, oppstart eller testing endres.

## UX & Interaction Patterns

- **Design-tokens («Myk fersken»):** alle farger, skrifter, hjørner og avstander er CSS-variabler på ett sted, hentet fra token-blokken øverst i DESIGN.md. Ingen fargekoder andre steder. Bare lys modus. Felt og avkrysningsbokser har ramme i `primary` (kontrast), og kort har den lyse `border`.
- **Skrift:** systemskrift overalt. Baloo 2 ExtraBold ligger som lokal fil og brukes bare i logoen. Ingenting hentes fra Google Fonts. Logoen «Søknadsassistenten» står sentrert øverst, på én linje ved 375 px (`clamp`), men får bryte ved stor tekst. Ingen `nowrap` og ingen faste høyder.
- **`base.html`:** `lang="nb"`, egen sidetittel per side («Logg inn – Søknadsassistenten»), og landemerkene `header` (logo), `main` og `footer`. Hver side har én `h1`, og logoen er ikke en overskrift.
- **Hjørneraden (`corner-row`):** etter innlogging står «Logg ut» (liten sekundærknapp) nede til høyre. Raden er festet nederst med `scroll-padding-bottom`, dekker aldri innhold og står nederst på siden i stedet under ca. 500 px skjermhøyde. KI-merknaden til venstre kommer i Epic 4.
- **Skjema (innlogging og registrering):** enkle og vanlige, høyst 360 px brede. Etikett over feltet, og hjelpetekst og feiltekst under, koblet til feltet. Ved feil: rød ramme, `aria-invalid` og fokus til første felt med feil. «Feil e-post eller passord» og «Du må logge inn først» står i en skjemafeil-boks over skjemaet som får fokus. `autocomplete`: email, current-password (innlogging), new-password (registrering). Liming og passordbehandler er alltid lov. «Minst 8 tegn» står under passordfeltet fra starten.
- **Lenker:** «Ny her? Registrer deg her» på innloggingen og «Har du allerede en bruker? Logg inn» på registreringen (lenkeknapper).
- **Knapper:** hovedknapp («Logg inn», «Registrer deg»), sekundærknapp («Logg ut») og lenkeknapp, med hover (løft 2 px og skygge), trykk (96 %) og låst (55 %). Fokusring 3 px `focus-ring` med 2 px avstand på alt som kan trykkes på. Ved `prefers-reduced-motion` slås alle animasjoner av.
- **Tone:** vennlig «du»-tone, «nettside» og aldri «app». Den eksakte ordlyden for alle feil står i EXPERIENCE under «Tekster per side».

## Cross-Story Dependencies

- Story 1.1 er grunnmuren (app, `base.html`, CI og første test) og må være ferdig før de andre.
- Story 1.2 lager databasen, testbrukeren, øktlageret, feiltypene og `tekster.py`. Story 1.3 og 1.4 bygger på dem.
- Story 1.4 bruker øktmodellen fra 1.2. Testen for at sider krever innlogging skal også fange sidene fra senere epics.
- Mot senere epics: Epic 2 legger knappen «Begynn å lage søknad», testmodus-bryteren og `Soknad` til startsiden. Utlogging skal da også slette `Soknad`. `Innlogging.testmodus` må finnes alt nå: uten API-nøkkel er testmodus låst på, og fram til Epic 4 er den alltid på. Epic 3 (brevsiden) logger ut på samme måte som story 1.4. Epic 4 legger KI-merknaden inn i hjørneraden.
- Sjekkpunkt 22. november: Epic 1 skal være ferdig.
