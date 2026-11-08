# Epic 2 Context: Se gap-analyse og nøkkelordtreff i testmodus

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Brukeren går fra startsiden via modusvalget (kortet Full generering) til innleggingen, limer inn CV og stillingsannonse fra testdataene og ser resultatsiden med gap-analysen og nøkkelordtreffet. Alt skjer i testmodus, uten API-nøkkel, med håndlagde testsvar fram til Epic 4. Epicen lager også telleregelen, de første fiktive testdataene med fasit, gjenkjenningen av testdata, stegmodellen og `Soknad` i økten. Den er viktig fordi det meste av «kuttes aldri»-listen ligger her, og fordi sensor skal kunne kjøre nettsiden i testmodus etter README og få nøyaktig prosenten fra fasiten.

## Stories

- Story 2.1: Telleregelen for nøkkelordtreff
- Story 2.2: Fiktive testdata og fasit for første testcase
- Story 2.3: Testmodus kjenner igjen testdataene
- Story 2.4: Startsiden får testmodus og knappen videre, og modusvalget lages
- Story 2.5: Lime inn CV og stillingsannonse
- Story 2.6: Hele resultatsiden med forklaringer og «Tilbake»
- Story 2.7: Ventetegn og feil fra KI-en

## Requirements & Constraints

- **Telleregel:** treff uavhengig av store og små bokstaver, også som del av et lengre ord. Nøkkelord på 1–3 tegn må stå som eget ord. Hvert nøkkelord telles én gang. Vises som «X av Y = Z %», rundet til nærmeste hele tall («2 av 3» = 67 %). Kjente begrensninger (bøyningsformer, «Java» i «JavaScript», «C» i «C#»/«C++» og i lister med A, B, C) skrives i README.
- **Nøkkelordlisten** hentes fra KI-en én gang og lagres i økten. Prosenten regnes alltid fra den lagrede listen, så samme CV og annonse gir samme prosent i samme søknad. Ny søknad eller utlogging glemmer listen. Listen kan ikke endres.
- **Gap-analysen** viser kravene i to lister (dekker / mangler, på skjermen «Dette kan du jobbe videre med») og er merket som KI-generert. Analysen vises før brevet lages.
- **Resultatsiden** forklarer kort ATS, nøkkelordtreff og gap-analyse, og at de to kan si hverandre imot.
- **Innlegging:** alle feltene må fylles ut, og alle feilene vises samtidig. Brukeren kan tømme et felt. «Tilbake» fra resultatsiden gir feltene fortsatt fylt ut, og analysen kjøres på nytt når man går videre (gjenbruk av listen når bare CV-en er endret kommer i Epic 7).
- **Testmodus:** bryter bare på startsiden, låst på uten API-nøkkel og alltid på fram til Epic 4. Merkelappen «Testmodus» på de andre sidene. Bare de fiktive testdataene virker, annet gir beskjed om det på riktig felt.
- **Venting og KI-feil:** ventetegn med kort tekst, og knappen kan ikke trykkes på nytt. Nettverksfeil, andre feil og ubrukelige svar gir feilmelding, aldri en tom resultatside, og det brukeren har lagt inn, er fortsatt der.
- **Personvern og testdata:** CV, annonse og nøkkelordliste ligger bare i minnet, aldri på disk eller i cookien. Bare fiktive testdata i repoet, i egen mappe, med fasit og kort begrunnelse per krav. README sier hvor testdataene og fasiten ligger.
- **Tester:** telleregelen (2 av 3 = 67 %, 1 av 8 = 13 %, «C» ikke i «Center», «C#» og «C++», «python-utvikler», æøå, 0 av Y = 0 %), gjenkjenning av testdata, kontroll av KI-svar, sjekk av inndata, at nøkkelordlisten gir samme prosent ved ny lasting og etter «Tilbake», og at man ikke kan hoppe over steg.
- **Suksesskriterier:** nøkkelordtreffet gir nøyaktig prosenten i fasiten (2), nettsiden kjører i testmodus uten API-nøkkel (7), samme CV og annonse to ganger i samme søknad gir samme treff (8). Resultatsiden må også være forståelig nok til at en medstudent kan forklare hva som mangler og hva prosenten betyr og ikke betyr (13).

## Technical Decisions

- **Telleregelen** ligger bare i `kjerne/telleregel.py`: `casefold()`, ≥ 4 tegn gir treff i lengre ord, 1–3 tegn bare med `(?<!\w)ord(?!\w)` og `re.escape`. Prosent med `Decimal(...).quantize(..., ROUND_HALF_UP)`, aldri `round()`.
- **KI-grensesnittet** i `adaptere/ki.py` har faste signaturer (`nokkelord(annonse)`, `gap(cv, annonse)`, senere `brev` og `korrektur`). I denne epicen trengs `TestKI`, som finner testcaset med `kjerne/testdata_match` og leser `testdata/<case>/ki-svar/`. Web velger utgave ut fra `Innlogging.testmodus` og vet ellers ikke hvilken som brukes.
- **Svarformer:** `nokkelord` = `{nokkelord: [str], arbeidsgiver: str | null}`, `gap` = `{dekker: [str], mangler: [str]}`. Testsvarfilene inneholder bare objektet. Alt går gjennom `kjerne/ki_svar.kontroller()`, som gir `KIFeil(ubrukelig_svar)` ved ugyldig JSON, tom nøkkelordliste eller når både `dekker` og `mangler` er tomme.
- **Gjenkjenning av testdata:** `kjerne/testdata_match.vask()` gjør NFKC, `casefold()` og beholder bare bokstaver og tall. CV-en avgjør testcaset. Annonse som ikke hører til samme case, får `ikke_testdata` på sitt eget felt.
- **`Soknad`** i `kjerne/okt.py` har faste felt (`steg`, `modus`, `samtykke`, `cv`/`annonse`/`eget_brev` med `tekst` og `filnavn`, `nokkelord` med den vaskede annonseteksten, `arbeidsgiver`, `gap`, `brev`/`korrektur`, `forslag`, `lastet_ned`, `opptatt`). Ingen løse strengnøkler. Å komme til startsiden lager alltid en ny `Soknad`, men testmodus i `Innlogging` beholdes. Utlogging sletter begge.
- **Steg:** `kjerne/steg.py` eier start < modus < innlegging < resultat < brev. En side vises bare når sidens steg ≤ `Soknad.steg`, ellers redirect til siden for steget. Steget flyttes bare etter en vellykket POST. Søknaden endres bare via `sett_inndata`, `velg_modus` (og senere `nytt_forslag`), som nullstiller resultater som ikke lenger gjelder. Endres feltene, settes steget tilbake til innlegging til analysen har lyktes igjen. Bryteren kan bare endres på startsteget.
- **POST og KI-kall:** lykkes POST-en, redirect. Feiler den (inndatafeil eller KI-feil), vises samme side på nytt uten redirect, med det som er lagret. KI-kall bare fra POST, med `opptatt` rundt. En ny POST mens `opptatt` er sann sendes til siden for steget uten nytt kall.
- **Feil:** `InndataFeil(felt, type)` returneres som liste. Nye typer her er `tom` og `ikke_testdata` (rekkefølge per felt: tom → … → ikke_testdata). `KIFeil(type)` med `nettverk`, `annet` eller `ubrukelig_svar` er unntak. Alle tekster i `web/tekster.py`, og alle feiltyper kjernen kan lage, må ha en tekst der.
- **«Tilbake» fra innleggingen** sender feltene til serveren, som lagrer dem uten å vise feil. JavaScript endrer aldri søknadsdata.
- **Testdata:** `backend/testdata/case-1-<navn>/` med `cv.txt`, `annonse.txt`, `fasit.md` og håndlagde `ki-svar/nokkelord.json` og `ki-svar/gap.json` som stemmer med fasiten. CV-en skal ha tydelige hull (for eksempel «førerkort», «SQL»), ikke grensetilfeller. Claude lager utkastet, Kristine godkjenner innholdet.
- **`kjerne/`** importerer aldri flask, anthropic, pypdf, docx, fpdf eller sqlite3 og leser ingen filer. Webtester bruker `create_app(test_config)`, `test_client` og `TestKI`. Hver testfil og testfunksjon nevner FR-nummeret.

## UX & Interaction Patterns

- **Startside:** «Velkommen! 👋», ingressen og «Begynn å lage søknad» som største knapp (`button-hero`, hele bredden på mobil). Bryteren «Testmodus» oppe til høyre (`role="switch"`, synlig etikett, låst med `aria-disabled="true"` og 60 % synlig). Uten nøkkel står «Mangler API-nøkkel, se README» under, koblet med `aria-describedby`. «Du er i testmodus. Nettsiden bruker ferdige svar, og ingenting sendes til ekstern KI.» står i et statusområde. Samtykket er skjult i testmodus.
- **Modusvalg:** «Hva vil du gjøre i dag?» med kortet ✨ «Full generering» · «Skriv nytt brev» · «Du legger inn CV-en og annonsen, så skriver vi et brev til deg.» Hele kortet er én knapp, uten egen «Velg». «Tilbake» under kortene. Ikonet som vipper kommer i Epic 7.
- **Merkelappen «Testmodus»** (fersken, bare visning) oppe til høyre på alle sider etter startsiden, fra `base.html`.
- **Innlegging:** «Legg inn CV-en din og stillingsannonsen», feltene «📄 CV» og «📢 Stillingsannonse» med «Lim inn tekst» (sekundær). Hjelpeboks med stiplet ramme: «Testmodus: bruk filene i mappen testdata/ i prosjektet.» Tekstboksen kan dras større (ca. 160 px PC, 200 px mobil), og markøren settes i den. Søppelbøtta (minst 24 × 24 px, «Tøm CV-feltet» for skjermlesere) tømmer uten bekreftelse, fokus går til «Lim inn tekst», og skjermlesere hører «CV-feltet er tømt». Knappene og tekstboksen har feltnavnet med for skjermlesere. Feltene står side om side først fra 1000 px. Knapper nederst: «Tilbake» (til venstre) og «Sjekk CV-en min».
- **Feilboks:** øverst, «Noe må fikses før du kan gå videre:», én lenke per feil til feltet, `tabindex="-1"`, fokus og rulling dit, uten `role="alert"`. Feltet får rød ramme, og samme tekst står under feltnavnet, koblet med `aria-describedby`. Tekstene: «CV: Fyll inn feltet. Last opp en PDF eller lim inn tekst.» og «CV: I testmodus fungerer bare testdataene fra mappen testdata/.» (feltnavnet byttes ut).
- **Resultatside:** «Slik passer CV-en din til stillingen». Rekkefølge: gap-analysen, linjen om at de kan si litt forskjellig, nøkkelordtreffet, ATS-forklaringen. «Gap-analyse» med «i» og merket «Laget av KI». «Dette dekker CV-en din» grønn med ✓, «Dette kan du jobbe videre med» varm fersken med → (aldri rød). «X av Y = Z %» stort med «av nøkkelordene står i CV-en din», prosentlinje uten animasjon (den kommer i Epic 7), og listene «Står i CV-en (antall)» med ✓ og «Står ikke i CV-en (antall)» med ○. ATS-forklaringen foldes ut og inn og er lukket når siden åpnes. Tomme lister har egne tekster fra EXPERIENCE. «Tilbake» nederst til venstre, ved siden av «Lag søknadsbrevet mitt» (brevet kommer i Epic 3).
- **«i»-ikon:** åpnes og lukkes med trykk, Enter og mellomrom, lukkes med Esc, åpnes med hover på PC men ikke av fokus alene, med `aria-expanded` og `aria-controls`. Skjermlesertekster som «Hva er en gap-analyse?».
- **Overskrifter:** `h1` for siden, `h2` for «Gap-analyse», «Nøkkelordtreff» og feltnavnene, `h3` for listene. Egen sidetittel, for eksempel «Resultat – Søknadsassistenten». Ikoner som bare er pynt (📄 📢 ✨ 👋 ✓ ○ → 🎉), skjules for skjermlesere.
- **Ventetegn:** dekker siden (bakgrunn med 94 %), tre hoppende prikker, «På vei mot ny jobb» i Baloo 2 og «Vi sjekker CV-en din – det tar noen sekunder.» Resten av siden, også hjørneraden, er `inert`. Knappen får `aria-disabled` og beholder fokus, og et fast `role="status"`-område får ventesetningen. Etterpå går fokus til den nye overskriften eller feilboksen. Ved `prefers-reduced-motion` står prikkene stille.
- **KI-feil:** samme feilboks med «Nettverksfeil, sjekk nettverkstilgangen.» eller «Noe gikk galt hos KI-tjenesten. Prøv på nytt.», teksten per side («Det du har lagt inn, er ikke borte.» på innleggingen, «Resultatet og det du har lagt inn, er ikke borte.» på resultatsiden) og knappen «Prøv på nytt».
- **Bredder:** bruddpunkt 700 px for modus-kort, gap-lister og nøkkelordlister. Ingen rulling sidelengs ved 320, 375, 768 og 1280 px og ved 200 % zoom. Ingen faste høyder og ingen `nowrap`.

## Cross-Story Dependencies

- Story 2.1 (telleregelen) og 2.2 (testdata) kan lages først og hver for seg. Story 2.3 trenger testdataene fra 2.2.
- Story 2.4 lager `Soknad`, stegmodellen, bryteren og merkelappen. Story 2.5 bygger på 2.1, 2.3 og 2.4, og story 2.6 og 2.7 bygger på 2.5.
- Fra Epic 1: `Innlogging.testmodus` finnes alt, og utlogging skal nå også slette `Soknad`. Testen for at alle sider krever innlogging skal fange de nye sidene automatisk.
- Mot senere epics: Epic 3 legger brevsiden bak «Lag søknadsbrevet mitt». Epic 4 lar bryteren slås av, legger til samtykke og KI-merknad, og bytter de håndlagde testsvarene ut med ekte KI-svar. Epic 5 legger til kortet Korrektur og brevfeltet. Epic 6 legger til «Last opp PDF» og filfeilene. Epic 7 legger til gjenbruk av nøkkelordlisten, prosentlinjen som fylles og ikonet som vipper.
- Sjekkpunkt 22. november: telleregelen og innleggingssiden skal være ferdige. 29. november: hele flyten i testmodus (Epic 1–3).
