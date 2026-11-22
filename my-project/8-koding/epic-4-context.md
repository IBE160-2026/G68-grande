# Epic 4 Context: Bruke ekte KI (Claude)

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Med API-nøkkel kan testmodus slås av, og da bruker nettsiden Claude til nøkkelord, gap-analyse og brev. Epicen legger til KI-merknaden og samtykket på startsiden, promptene med reglene for brevet og de 17 typiske KI-frasene, og skriptet som bytter ut de håndlagde testsvarene med ekte KI-svar. Hver prompt kjøres tre ganger mot fasiten, og det kommer et testcase til (kriterium 3). Epicen er viktig fordi ekte KI (Claude via API), ekte testsvar og samtykke er krav i PRD-en, og fordi suksesskriterium 1, 3, 9 og 11 bare kan vises her.

## Stories

- Story 4.1: Koble til Claude for nøkkelord og gap-analyse
- Story 4.2: Brevet fra Claude
- Story 4.3: Slå av testmodus, med samtykke og KI-merknad
- Story 4.4: Ekte KI-svar i testmodus
- Story 4.5: Et testcase til, og kriterium 3

## Requirements & Constraints

- **Bryteren:** med `ANTHROPIC_API_KEY` kan testmodus slås av og på, men bare på startsiden. Valget huskes til utlogging, og etter ny innlogging er testmodus av. Uten nøkkel er bryteren fortsatt låst på med «Mangler API-nøkkel, se README».
- **Samtykke:** når testmodus er av, må brukeren krysse av før «Begynn å lage søknad» virker. Boksen er alltid tom når startsiden åpnes, også i samme økt og etter at testmodus er slått på og av igjen. I testmodus trengs ikke samtykke. Tekst sendes til Claude bare når `Soknad.samtykke` er sann.
- **KI-merknaden** vises hele tiden når testmodus er av, og er skjult i testmodus.
- **Brevet:** norsk, formell og akademisk tone, nevner stillingen og arbeidsgiveren ved navn, minst to konkrete krav fra annonsen koblet til CV-en, og ingen av de 17 typiske KI-frasene (listen Kristine bestemte 7. november, i addendum til PRD-en). Brevet bygger bare på CV og annonse og legger ikke til erfaring, utdanning eller ferdigheter. Omformulering og kobling til kravene er lov.
- **Feiltekster:** nettverksfeil gir «Nettverksfeil, sjekk nettverkstilgangen.». Andre feil, tidsavbrudd og svar som ikke kan brukes gir «Noe gikk galt hos KI-tjenesten. Prøv på nytt.». Det brukeren har lagt inn, er fortsatt der.
- **Logg og personvern:** etter hvert kall skrives KI-oppgave, tokens og anslått pris til terminalen. Loggen viser aldri CV, annonse, brev, passord eller nøkkel. KI-feil skal nå logges med oppgave og feiltype (utsatt fra Epic 2), og `FilFeil` likeså (utsatt fra Epic 3).
- **Kostnad:** forhåndsbetalt kreditt i Claude Console, auto-reload av, tak 250 kr. Overslaget i PRD-en (12. november) er omtrent 2 kr per søknad i Full generering. Målet er under 3 kr per fullført søknad, og testplanen viser tokens og kroner per søknad (4.4).
- **Nøkkelordlisten (FR-15, endret 12. november):** prompten ber om 8–20 nøkkelord på 1–3 ord hver, uten duplikater. En liste som er tom eller lengre enn 30, er et ubrukelig svar (lagt inn i 4.1). `fasit.md` markerer de viktige nøkkelordene, og listen fra KI-en skal ha alle (suksesskriterium 14, 4.4 og 4.5).
- **Grenser (NFR-11, endret 12. november):** hvert innleggingsfelt godtar høyst 15 000 tegn, med egen feilmelding. Hver søknad kan bruke høyst 10 KI-kall, medregnet «Prøv på nytt» og «Nytt forslag», og deretter får brukeren en melding (4.3).
- **Telleregelen (FR-17, endret 12. november):** «#», «+» og «.» søkes som vanlige tegn, så «C#» og «.NET» gir treff. Den nåværende `telleregel` gjør dette allerede (sjekket 13. november).
- **Ekte testsvar:** de ferdige svarene i testmodus er ekte KI-svar. README sier det og viser hvordan skriptet kjøres.
- **Suksesskriterier med ekte KI:** kriterium 1 (gap-analysen mot fasiten), 3 (samme CV med to annonser gir brev med krav som er spesifikke for hver annonse) og 11 (ingenting i brevet som ikke står i CV-en) kjøres tre ganger per testcase, og alle tre må bestå. Resultatet står i `my-project/testplan.md`, også når noe feiler. Kriterium 12 (Korrektur) hører til Epic 5. Kriterium 2 (nøyaktig prosent) skal testes for alle caser.
- **Tester** bruker en falsk Anthropic-klient og kaller aldri det ekte API-et, heller ikke i CI. De dekker skjema, nettverksfeil, tidsavbrudd (gir `annet`), annen feil, feil `stop_reason`, ugyldig JSON, at bare CV og annonse sendes til brevet, at bryteren ikke kan endres etter startsiden, at samtykke kreves når testmodus er av og ikke når den er på, at ingen KI-kall skjer uten samtykke, og at ingen av KI-frasene står i `brev-1.json` og `brev-2.json`.

## Technical Decisions

- **Ett grensesnitt, to utgaver:** `adaptere/ki.py` har `nokkelord(annonse)`, `gap(cv, annonse)`, `brev(cv, annonse, forslag: int)` (og senere `korrektur`). `EkteKI` får de samme signaturene som `TestKI`. Weblaget velger utgave ut fra `Innlogging.testmodus` og vet ellers ikke hvilken som brukes. `anthropic` importeres bare i `adaptere/ki.py`, aldri i `kjerne/`.
- **Klienten:** `Anthropic(timeout=90, max_retries=1)` med begge verdiene satt uttrykkelig. 90 s er en startverdi i `innstillinger.py` og justeres etter målingen i story 4.3. Modellen er `ANTHROPIC_MODEL` eller `claude-opus-5-5`.
- **Structured outputs:** én prompt-fil i `prompts/` (i Git) og ett JSON-skjema per oppgave, sendt med `output_config.format`. Skjemaene har `additionalProperties: false`, alle felt påkrevd, og `null` når en verdi mangler. Før kodingen sjekkes parameternavnet og verdiene for `stop_reason` mot dokumentasjonen for anthropic 2.4.0 (claude-api-skillen). Avviker de, oppdateres arkitekturen og beslutningsloggen.
- **Svarformene:** `nokkelord` = `{nokkelord: [str], arbeidsgiver: str | null}`, `gap` = `{dekker: [str], mangler: [str]}`, `brev` = `{avsnitt: [str]}`. Alle svar går gjennom den samme `kjerne/ki_svar.kontroller()` som i testmodus, som også gir `KIFeil(ubrukelig_svar)` når `stop_reason` ikke er `end_turn` eller JSON-en er ugyldig.
- **Feiltyper:** nettverksfeil gir `KIFeil(nettverk)`, andre API-feil `KIFeil(annet)`. `APITimeoutError` er en underklasse av `APIConnectionError`, så tidsavbrudd må sjekkes først, ellers blir det feilaktig «Nettverksfeil».
- **`arbeidsgiver`** kommer fra `nokkelord` og lagres i økten for filnavnet i Epic 7.
- **`EkteKI.brev`** sender bare CV og annonse (FR-37), med skjemaet `{avsnitt: [str]}`.
- **`scripts/lag_testsvar.py`** kjører `EkteKI` på hvert testcase og skriver `ki-svar/nokkelord.json`, `gap.json`, `brev-1.json` og `brev-2.json` (`forslag` 1 og 2), med bare objektet. Filer åpnes med `encoding="utf-8"`.
- **Testdata:** `testdata/case-2-<navn>/` med `cv.txt`, `annonse.txt` og `fasit.md` (krav med begrunnelse, nøkkelordene, forventet nøkkelordtreff og sjekkliste for kriterium 11). CV-en avgjør testcaset, så den må være ulik case 1. Case 2 er bare for Full generering. Claude lager utkastet, Kristine godkjenner.
- **Flyt:** KI-kall bare fra POST, med `opptatt`. Bryteren endres bare på startsteget. Alle brukertekster i `web/tekster.py`.
- **Tester:** `create_app(test_config)`, `test_client`, `TestKI` og hjelperne i `tests/web/hjelpere.py` (for eksempel `FeilendeKI` og `sett_testmodus`). Ingen testfil henter noe fra en annen testfil. Hver testfil og testfunksjon nevner FR-nummeret.

## UX & Interaction Patterns

- **Startsiden med testmodus av:** «Teksten din sendes til ekstern KI.» over avkrysningsboksen (22 px) «Jeg samtykker til bruk av KI», med «i»-ikon (skjermlesertekst «Hva betyr samtykket?») og «i»-boksen med de fire punktene fra EXPERIENCE (hva, hvorfor, lagres noe, personopplysninger). «i»-boksen åpnes og lukkes med trykk, Enter og mellomrom, lukkes med Esc, åpnes med hover på PC men ikke av fokus alene, med `aria-expanded` og `aria-controls`.
- **Uten avkryssing:** rød ramme rundt boksen, «Du må samtykke før du kan begynne» koblet til boksen, og fokus til boksen.
- **Testmodus på:** samtykket og KI-merknaden er skjult, og «Du er i testmodus. Nettsiden bruker ferdige svar, og ingenting sendes til ekstern KI.» vises i statusområdet.
- **Bryteren:** `role="switch"` med etiketten «Testmodus». Med nøkkel er den ikke lenger `aria-disabled`.
- **KI-merknaden:** «ⓘ Teksten behandles av ekstern KI» nede til venstre i hjørneraden, fra `base.html`, med «Logg ut» til høyre.
- **Ventetegnet** er det samme som før, men med ekte KI tar et kall flere sekunder (et brev 20–30 s). Etterpå går fokus til ny overskrift eller til feilboksen.

## Fra retrospektivene (kjente fallgruver)

**Kode som skal inn i storiene:**

- **`ki()` (Epic 2):** velger KI ut fra testmodus og har grensesnittet som type, ikke `TestKI`. I dag bruker en rute `ki().caser`, som bare `TestKI` har, så med testmodus av ville `TestKI` blitt kalt og gitt en KI-feil som aldri går over (4.1/4.3). Tidsgrensen på KI-kallet hindrer at `opptatt` henger (4.1). Tom `arbeidsgiver` gjøres om til `None` (4.2).
- **Brevteksten renses i `kontroller("brev")` (Epic 3):** kontrolltegn (for eksempel `\u000b`) fjernes eller gir `ubrukelig_svar`, og linjeskift og tab blir mellomrom. I dag gir et kontrolltegn `FilFeil` i `lag_docx` hver gang, så «Prøv på nytt» kan aldri lykkes, og linjeskift og tab blir linjeskift og tab i Word, men ett mellomrom på siden, så fila er ikke lik brevet. En test kjører `kontroller` og `lag_docx` sammen. I samme omgang: `kontroller` fjerner tomme punkter (eller bare mellomrom) i `nokkelord`, `dekker` og `mangler`, så resultatsiden ikke viser tomme punkter.
- **Story 4.5 (Epic 2):** CV-er og annonser må være unike på tvers av caser. `nokkelord` velger i dag case ut fra annonsen og `gap` ut fra CV-en, så to caser med samme annonse kan blande svarene. De skal bruke samme case. Testene i `test_testdata.py` skal gjelde alle caser, ikke bare case 1. Tydelig feil når en fil eller hele `testdata/` mangler (i dag stopper en manglende fil oppstarten, og mangler hele mappen, blir all tekst «ikke testdata» uten feil). Egen tekst når CV og annonse er fra ulike caser.

**Fallgruver i CSS (testene tegner ikke siden, så bare prøving i nettleseren har funnet dem):**

- **Fokusring etter museklikk:** den felles ringen bruker `:focus-visible`, og nettleseren viser den ikke når et skript flytter fokus etter et museklikk. Det skjedde to ganger: «Lim inn tekst» (2.5.1, rettet med `.lim-inn:focus`) og «Bli her» i vinduet (3.3, rettet med `#bli-her:focus`). Alt som får fokus fra et skript, for eksempel avkrysningsboksen etter feilen, trenger også en `:focus`-regel og en sjekk i CSS-testen. Omvendt: overskrifter med `tabindex="-1"` skal ikke vise ring (`.side-overskrift[tabindex="-1"]:focus { outline: none; }`, bestemt av Kristine i 2.7.1).
- **Høykontrastmodus (Windows):** bakgrunner og skygger fjernes, så elementer som bare vises med bakgrunn, forsvinner. Det gjaldt sporet og knotten i bryteren (2.4.2), gap-boksene (2.6), prikkene i ventetegnet (2.7.1) og vinduet (3.3). Rettet med `@media (forced-colors: active)` og ramme i `CanvasText` (og `forced-color-adjust: none` der fargene må beholdes), med sjekk i CSS-testen. Gjelder nå bryteren av og på, den røde rammen på avkrysningsboksen, «i»-boksen og KI-merknaden.
- **SVG-høyde:** den felles regelen `svg { height: auto }` overstyrte `height="12"`, så prosentlinjen ble ca. 120 px høy (12 % av bredden) i 2.6. Rettet med `min-height`/`max-height: 12px` på `.prosentlinje` og en test. Hver ny SVG (for eksempel et ikon) trenger høyde i CSS. Prosjekttestene forbyr `style=` og faste høyder.

**Prosess:** sjekk statusen før et funn avvises med henvisning til et retro-punkt. Avvises samme funn i to stories, tas det opp med Kristine.

## Cross-Story Dependencies

- **Før story 4.1:** konto i Claude Console, kreditt, auto-reload av og API-nøkkelen i `backend/.env`. Rettingene etter retrospektiven for Epic 3 (punkt 1–3) er alt flettet (PR #22).
- Story 4.2 bygger på klienten, feilhåndteringen og loggingen fra 4.1. Fram til 4.3 bruker nettsiden fortsatt `TestKI`.
- Story 4.3 kobler `EkteKI` til weblaget og trenger 4.1 og 4.2. Kristine prøver hele flyten én gang med ekte KI mot sjekklisten i `fasit.md`, og noterer i PR-en hvor lang tid analysen og brevet tar.
- Story 4.4 trenger 4.1–4.3. Alle testene som bruker testdataene, skal fortsatt gå gjennom med de nye svarene. Kristine prøver også om KI-en forstår teksten fra Canva-CV-en riktig og noterer det i testplanen.
- Story 4.5 trenger skriptet fra 4.4. Kriterium 3 kjører CV-en fra case 1 mot annonsen fra case 1 og fra case 2, tre ganger hver.
- Mot senere epics: Epic 5 legger til `korrektur` i `EkteKI`, `prompts/korrektur.md` og testsvarene for Korrektur med samme skript. Epic 7 bruker `arbeidsgiver` i filnavnet og `brev-2.json` til «Nytt forslag». Epic 8 tar skjermbildene med ekte KI til README.
