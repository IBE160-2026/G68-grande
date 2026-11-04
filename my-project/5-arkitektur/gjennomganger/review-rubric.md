---
title: 'Gjennomgang av arkitekturen mot sjekklisten for en god arkitektur'
reviewed: 'ARCHITECTURE-SPINE.md (status draft, 2026-11-04)'
also_read: ['.memlog.md', 'prd.md (final, 2026-10-12)', 'EXPERIENCE.md (utdrag)']
date: '2026-11-04'
---

# Gjennomgang: arkitekturen for Søknadsassistenten

## Konklusjon

Arkitekturen er god og passer for en nybegynner. Den låser de fleste stedene der stories ellers ville gjort ting ulikt: formen på KI-svarene, telleregelen, testmodus bak samme grensesnitt, øktdata bare i minnet, feiltypene og filnavnet. Den bør likevel ikke godkjennes før to hull er tettet: **(1)** hvordan nettsiden starter uten `.env` (`SECRET_KEY`), og **(2)** hvordan feilmeldinger ved feltene og det brukeren har lagt inn overlever POST → redirect → GET. I tillegg bør fire mindre regler gjøres skarpere. Ingen av endringene gjør arkitekturen større. De fleste er én eller to setninger.

**Alvorlighet:** HØY = to stories vil nesten sikkert gjøre det ulikt, eller sensor kan bli stoppet. MIDDELS = sannsynlig avvik eller en regel som ikke kan følges slik den står. LAV = pynt eller en liten presisering.

## Sjekkliste

| Punkt | Vurdering |
| --- | --- |
| Låser stedene der stories kan gjøre ting ulikt, og mangler ingen | **Delvis.** Mangler: feil og inndata gjennom redirect, `SECRET_KEY`, hva som skjer når økten er borte, felles sidemal, hvordan web-laget testes, og hvordan ferdige KI-svar lages (funn 1, 2, 4, 5, 6, 7) |
| Hver regel (AD) kan sjekkes og hindrer det den sier | **Stort sett.** AD-2 kan ikke følges slik den står (funn 4). AD-10 hindrer ikke det den sier den hindrer, hvis PDF-teksten skiller seg fra .txt på mer enn mellomrom (funn 3) |
| Ingenting under «Utsatt» kan få to deler til å bli ulike | **Ett unntak:** «hvordan malene deles opp» (funn 7). De andre utsatte punktene er trygge |
| Navngitt teknologi er gjeldende | **Ja, ifølge beslutningsloggen.** Versjonene ble sjekket på PyPI 2026-11-04. Jeg har ikke sjekket dem på nytt. Små punkter står i funn 12 |
| Dekker FR-1–FR-38 og NFR-1–NFR-12 | **Nesten.** NFR-6 og NFR-7 mangler i kravtabellen (de hører til UX, men det bør stå). Feilen «Filen kan ikke lages» fra UX har ingen feiltype (funn 9). Hvordan FR-38 lages, er ikke bestemt (funn 6) |
| Drift/miljøer, sikkerhet og hvordan nettsiden kjøres er bestemt, utsatt eller et åpent spørsmål | **Delvis.** Lokal kjøring, logging og kostnad er bestemt. `SECRET_KEY`, debug-modus og Python-versjonen i CI er ikke bestemt (funn 1, 5, 12) |
| Ingen kompleksitet som en nybegynner ikke trenger | **Bra.** Lagdelingen, de to KI-utgavene og øktlageret i minnet har alle en grunn i et krav. To små ting kan gjøres enklere (funn 10, 11) |

## Funn

### 1. HØY — `SECRET_KEY` og oppstart uten `.env` er ikke bestemt (AD-7, AD-12, Drift)

AD-7 bygger på en *signert* Flask-cookie, og den krever `SECRET_KEY`. Arkitekturen sier ikke hvor den kommer fra. NFR-12 krever at README prøves fra en ny kopi **uten `.env`**, og suksesskriterium 7 krever at nettsiden virker i testmodus uten API-nøkkel. Står `SECRET_KEY` i `.env` uten en reserve, krasjer nettsiden for sensor. Hardkodes den i stedet, havner en hemmelighet i Git.

**Forslag (AD-12):** «`SECRET_KEY` leses fra `.env`. Mangler den, lages en tilfeldig nøkkel ved oppstart med `secrets.token_hex()`. Det er trygt fordi øktene uansett forsvinner ved omstart (AD-7). Nettsiden skal starte uten `.env`, og da er testmodus låst på.» Nevn `SECRET_KEY` i `.env.example`.

### 2. HØY — POST → redirect → GET sier ikke hvordan feil og inndata kommer frem (AD-8, AD-9; FR-4, FR-9–FR-12, FR-28)

AD-8 sier at *alle* skjema bruker POST → redirect → GET. FR-4 krever rød ramme og tekst *ved feltet*, og FR-28 krever at det brukeren har lagt inn, står der etter en feil. Etter en redirect er begge deler borte, med mindre de lagres et sted. Arkitekturen sier ikke hvor. Den som lager innloggings-storyen, vil trolig vise skjemaet på nytt direkte fra POST (et unntak fra regelen). Den som lager innleggings-storyen, vil kanskje bruke `flash()`. Da blir feilvisningen ulik på hver side, og det er nettopp det AD-9 skal hindre.

**Forslag (AD-8/AD-9), velg én av disse:**
- (a) «Ved feil i skjemaet lages siden på nytt direkte fra POST, med `feil: {felt: tekst}` og det brukeren skrev. Redirect brukes bare når det går bra.» Dette er enklest for en nybegynner og vanlig i Flask.
- (b) «Feil og inndata legges i øktlageret (`okt.feil`) før redirect, og GET-siden viser dem og tømmer dem.»

Bestem også hvordan innloggings- og registreringssidene gjør det, siden de kommer før det finnes noe øktlager.

### 3. MIDDELS–HØY — Gjenkjenning av testdata kan svikte mellom PDF og .txt (AD-10; FR-34, suksesskriterium 5 og 7)

AD-10 fjerner bare mellomrom og gjør teksten om til små bokstaver. pypdf kan gi tekst som skiller seg fra den innlimte teksten på mer enn mellomrom: orddeling med bindestrek på slutten av linjen, ligaturer (`ﬁ`), punkttegn (`•`), andre anførselstegn og rekkefølgen i topp- og bunntekst. Svikter gjenkjenningen, får sensor «bare testdata fungerer» på en ekte testfil. Testmodus står på listen over det som aldri kuttes. Regelen sier heller ikke om det sammenlignes med `cv.txt` eller med teksten pypdf leser ut av `cv.pdf`.

**Forslag:** «Hver testfil gjenkjennes hvis den vaskede teksten er lik den vaskede `.txt` **eller** den vaskede teksten som `pdf_inn` leser ut av testcasets egen `.pdf`.» Legg til en test for hvert testcase i `tests/` som sjekker at PDF og .txt gjenkjennes som samme case. Vurder også å fjerne alle tegn som ikke er bokstaver eller tall (`[^\w]`), ikke bare mellomrom.

### 4. MIDDELS — AD-2 kan ikke følges slik den står, og det er ikke bestemt hvordan web-laget testes (AD-2, konvensjonen for tester; NFR-9)

AD-2 sier: «Alle regler som NFR-9 krever tester av, ligger i `kjerne/`.» Men NFR-9 krever også tester av innloggingen (FR-1, FR-3: `db.py` og werkzeug), av at sider krever innlogging (FR-7: web) og av at den nedlastede filen er uten markeringer (FR-30: `fil_ut.py`). Disse kan ikke ligge i `kjerne/`. Uten en bestemt testmåte for web-laget vil hver story finne sin egen.

**Forslag:** Endre AD-2 til «Regler uten I/O ligger i `kjerne/`.» Legg til i konvensjonene: «Web- og adaptertester bruker `create_app(test_config)` med en midlertidig database (`tmp_path`), `app.test_client()` og `TestKI`. Ingen test bruker nett eller API-nøkkel.» `create_app` må da ta imot innstillinger, for eksempel stien til databasen.

### 5. MIDDELS — Hva som skjer når økten er borte men cookien er der, er ikke bestemt (AD-7, AD-8; FR-7)

Cookien har økt-id og bruker-id, men søknadsdataene ligger i minnet. Etter en omstart, og med `flask run --debug` etter **hver lagring av en kodefil**, finnes cookien fortsatt, mens økten er borte. Er det `bruker-id` i cookien eller økten i minnet som avgjør om brukeren er logget inn? Ruter som slår opp `oktlager[id]`, vil krasje (`KeyError`) eller oppføre seg ulikt. Arkitekturen sier heller ikke at det lages en ny økt-id ved innlogging (som hindrer at noen overtar en gammel økt).

**Forslag (AD-7):** «Brukeren er logget inn bare når økt-id-en i cookien finnes i øktlageret. Ukjent økt-id betyr ikke logget inn: cookien tømmes og brukeren sendes til innloggingen (FR-7). Ved innlogging og registrering lages alltid en ny økt-id.» Da trengs kanskje ikke `bruker-id` i cookien i det hele tatt. Den kan ligge i økten.

### 6. MIDDELS — Det er ikke bestemt hvordan de ferdige KI-svarene lages og holdes oppdatert (AD-3, AD-4, AD-10; FR-38)

FR-38 krever at svarene i `testdata/*/ki-svar/*.json` er ekte KI-svar. Arkitekturen har ikke noe skript eller noen regel for hvordan de lages. Endres en prompt eller et JSON-skjema, blir de gamle svarene feil uten at noen merker det, og TestKI viser da noe annet enn EkteKI ville gjort.

**Forslag:** Legg til `scripts/lag_testsvar.py`, som kjører EkteKI på hvert testcase og lagrer svarene, i startstrukturen. Legg til regelen: «Testsvarene lages bare med dette skriptet og lages på nytt når en prompt eller et skjema endres. En test sjekker at alle testsvar består kontrollen i `kjerne/ki_svar`.»

### 7. MIDDELS — «Hvordan malene deles opp» er utsatt, men felles elementer avhenger av det (Utsatt; FR-33, FR-35, FR-6)

Testmodus-merket (FR-33), KI-merknaden (FR-35), «Logg ut» (FR-6), statusområdet for ventetegnet og feilboksen skal stå på *alle* sider etter innlogging (EXPERIENCE.md: «Faste elementer på alle sider», hjørneraden). Uten en felles grunnmal bygger hver story disse på sin egen måte. CSS kan vente, men det å ha en felles mal kan ikke.

**Forslag (konvensjoner):** «Alle sider arver fra `templates/base.html`, som har `header` (logo, testmodus-merket), `main`, hjørneraden og statusområdet. Malene får `testmodus` og `innlogget` fra én `context_processor`.» Flytt resten av punktet (CSS) til «Utsatt».

### 8. LAV–MIDDELS — Filnavnet renses ikke for alle tegn som er ulovlige i et filnavn (AD-11)

Arbeidsgiveren kommer fra KI-en og kan inneholde `/`, `:`, `"`, `&` eller `.`. AD-11 bytter bare ut æøå og mellomrom. Det kan gi et ødelagt filnavn eller en ødelagt `Content-Disposition`-header (nedlastingen svikter, særlig på Windows).

**Forslag:** «Etter at æøå er byttet ut, beholdes bare `A–Z a–z 0–9 -`. Blir arbeidsgiveren tom, brukes `Soknad_<dato>`.» Det passer allerede inn i enhetstesten som UX krever.

### 9. LAV–MIDDELS — Feilen «Filen kan ikke lages» har ingen feiltype (AD-9, AD-11; UX-brevsiden)

UX har feilmeldingen «Filen kan ikke lages» (EXPERIENCE.md, mockups for brevsiden). AD-9 har bare `InndataFeil`, `PdfFeil` og `KIFeil`. Uten en egen feiltype vil `fil_ut.py` kaste en vanlig Python-feil, og brukeren får en standard 500-side.

**Forslag:** Legg til `FilFeil` i AD-9, eller si at `fil_ut` bruker `PdfFeil(lage_fil)`.

### 10. LAV — Regelen om å avvise en ny POST mens KI jobber er uklar (AD-8; FR-27)

«En ny POST mens et KI-kall pågår i samme økt avvises» sier verken *hvordan* (et flagg i økten?), *hva brukeren får se*, eller *hva som skjer hvis flagget blir stående* etter en feil. Hvis det blir stående, er brukeren låst til hun logger ut. Med én bruker på localhost og en knapp som er låst i JavaScript (FR-27), er dette mest et sikkerhetsnett.

**Forslag:** Enten «Flagget `okt.ki_pagar` settes og tømmes alltid i `try/finally`. En ny POST mens det er satt, sendes tilbake til siden den kom fra (redirect)», eller kutt regelen og la låsen i JavaScript og POST → redirect → GET være nok. Det siste er enklere.

### 11. LAV — `ruff format --check` i CI kan stoppe hver PR (konvensjonen for tester)

For en som aldri har kodet, blir en PR som feiler bare på grunn av formatering, støy. Behold kontrollen, men si i konvensjonen at `uv run ruff format` kjøres før commit, og legg kommandoen i README eller i en pre-commit-hook.

### 12. LAV — Små punkter om drift og stack (Stack, Drift, AD-13)

- **Python-versjon:** «≥ 3.12 (utviklet på 3.14)», men versjonen i CI er ikke bestemt. Legg en `.python-version` i repoet (uv og `setup-uv` i CI leser den), slik at lokalt, CI og sensor bruker samme Python.
- **Debug-modus:** si at README starter **uten** `--debug`. Werkzeug-debuggeren kan kjøre kode og skal ikke være på hos sensor. Med `--debug` lastes nettsiden også inn på nytt ved hver kodeendring og tømmer øktene (se funn 5).
- **Nye forsøk i SDK-et:** anthropic-SDK-et prøver selv på nytt (standard `max_retries=2`). AD-13 sier 1 nytt forsøk. Da må `max_retries=1` settes på klienten, ellers blir det 3 × 90 s ventetid.
- **Structured outputs:** `output_config.format` og modellnavnet `claude-opus-5-5` kommer fra Anthropic-dokumentasjonen bufret 2026-10-06. Sjekk at SDK 2.4.0 tar imot parameteren når ekte KI kobles på. Det valgfrie feltet `grunn?` må stå som ikke-påkrevd i JSON-skjemaet.
- **Testbrukeren:** det står ikke hvor e-post og passord til testbrukeren ligger (konstant i `innstillinger.py`?). README trenger dem (NFR-8).
- **Beslutningsloggen:** linjen «pip + venv + requirements.txt» er erstattet av uv-beslutningen lenger ned. Merk den som erstattet, slik at faglærer og sensor ikke blir forvirret.

### 13. LAV — Det er ikke bestemt hva som lagres for en opplastet fil (AD-7; FR-13, FR-19)

Når brukeren går tilbake til innleggingen (FR-19), skal feltene fortsatt være fylt ut, og UX viser filnavnet med ✓. Da må økten lagre både teksten og filnavnet. AD-7 sier bare «CV». Si i AD-7: «For hvert felt lagres `tekst` og `kilde` (`pdf` + filnavn, eller `innlimt`). Selve PDF-filen lagres ikke.» Det hindrer også at noen lagrer PDF-bytene i minnet.

### 14. LAV — Kravtabellen mangler NFR-6 og NFR-7 (Krav → arkitektur)

Tilgjengelighet og skjermstørrelser bestemmes i UX, men tabellen bør si det («NFR-6, NFR-7 → DESIGN.md/EXPERIENCE.md, ingen AD»). Da ser sensor at de ikke er glemt. Det samme gjelder hvor testplanen for NFR-12 skal ligge (for eksempel `docs/testplan.md` i startstrukturen).

## Er noe unødvendig komplisert for en nybegynner?

Stort sett nei. Hver del har en grunn i et krav:

- **Tre lag (web, kjerne, adaptere):** trengs fordi NFR-9 krever tester uten nettleser og uten nøkkel. Mappenavnene er enkle, og regelen er lett å sjekke med et søk etter `import`.
- **EkteKI og TestKI bak ett grensesnitt:** trengs fordi testmodus aldri kuttes og fordi PRD-en sier at hele flyten bygges i testmodus først.
- **Øktlager i minnet i stedet for Flasks vanlige økt:** trengs fordi en CV kan være større enn 4 KB og NFR-4 forbyr disk. En vanlig `dict` i én modul er det enkleste som virker.
- **Egen `login_required` i stedet for Flask-Login:** enklere og lettere å forklare. Bra valg.
- **To kontroller av KI-svar (skjema + kjerne):** billig og gjør FR-28 testbart.

To ting kan gjøres enklere: låsen mot en ny POST mens KI-en jobber (funn 10) og at formateringen må være perfekt før en PR godtas (funn 11). Funn 2 (a) er også det enkleste for en nybegynner.

## Utsatte punkter: kan de føre til ulikheter?

| Utsatt | Trygt å utsette? |
| --- | --- |
| CV-er med kolonner og tabeller | Ja. Det handler bare om pypdf og er avgrenset av prøven |
| Feltet `grunn` | Ja. Plassen er satt av i AD-4 |
| TTF-skriften | Ja. Den brukes bare i `fil_ut.py` |
| CSS og hvordan malene deles opp | **Delvis nei.** Grunnmalen må bestemmes nå (funn 7) |
| CSRF | Ja, når nettsiden bare kjører lokalt. Nevn i README at CSRF mangler og må legges til før nettsiden legges på nett |
| Eksakt tidsgrense og grensen på 50 bokstaver | Ja. Det er konstanter som ligger ett sted. Men de står allerede som bestemte tall i AD-11 og AD-13. Skriv «startverdi» der, så det ikke ser ut som en motsigelse |
| Listen over KI-fraser | Ja. Den brukes bare i `prompts/brev.md` |
