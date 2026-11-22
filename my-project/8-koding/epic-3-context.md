# Epic 3 Context: Få et søknadsbrev og laste det ned (Full generering)

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Fra resultatsiden trykker brukeren «Lag søknadsbrevet mitt», ser brevet på brevsiden, laster det ned som Word og får et vindu med «Lag ny søknad», «Logg ut» og «Bli her». Alt skjer fortsatt i testmodus med et håndlaget testbrev, som byttes ut med et ekte KI-svar i Epic 4. Epicen er viktig fordi Full generering og .docx-nedlasting står på «kuttes aldri»-listen, og fordi hele flyten i testmodus (Epic 1–3) skal virke til sjekkpunktet 29. november.

## Stories

- Story 3.1: Se søknadsbrevet
- Story 3.2: Laste ned brevet som Word
- Story 3.3: Vinduet etter nedlasting

## Requirements & Constraints

- **Brevet lages først etter bekreftelse:** brukeren ser analysen før brevet. Trykket på «Lag søknadsbrevet mitt» er bekreftelsen, uten ekstra spørsmål.
- **Brevet vises før nedlasting** og kan ikke redigeres på nettsiden. Videre redigering skjer i Word.
- **Venting og KI-feil** som i Epic 2: ventetegn, låst knapp, og et tomt brev eller et svar som ikke kan leses gir feilmelding, aldri en tom brevside. Resultatet og det brukeren har lagt inn, er fortsatt der.
- **Nedlasting som Word (.docx)** i denne epicen. PDF kommer i Epic 7. Filen har bare brevteksten med avsnittene, uten markeringer og uten topp- eller bunntekst.
- **Etter nedlasting** kan brukeren velge startsiden (ny søknad med tomme felt) eller logge ut. Vinduet kommer hver gang.
- **Personvern:** brevet ligger bare i minnet, aldri på disk, i cookien eller i loggen. Nedlastet fil lages ved forespørselen og sendes rett ut.
- **Tester:** brevsiden kan ikke åpnes før resultatet finnes, tomt brev gir feilmelding, brevteksten vises, den nedlastede filen åpnes med python-docx og har samme tekst som brevet uten topp- og bunntekst, filnavnet med datoen (enhetstest), og «Lag ny søknad» gir en tom søknad med testmodus beholdt.

## Technical Decisions

- **KI-grensesnittet:** `brev(cv, annonse, forslag: int)` i `adaptere/ki.py`. `TestKI` leser `testdata/<case>/ki-svar/brev-1.json` når `forslag` er oddetall (`-2` ved partall, brukes først i Epic 7). I denne epicen er `forslag` alltid 1.
- **Svarform:** `brev` = `{avsnitt: [str]}`. Testsvarfilen inneholder bare objektet. Svaret går gjennom `kjerne/ki_svar.kontroller()`, som gir `KIFeil(ubrukelig_svar)` når brevet er uten tekst. Claude lager utkastet til `brev-1.json`, Kristine godkjenner innholdet.
- **Steg og `SIDE_FOR_STEG`:** brevsteget (start < modus < innlegging < resultat < brev) må legges inn i `SIDE_FOR_STEG` i `web/flyt.py`, og testen i `test_modusvalg.py` som låser tabellen, må oppdateres (åpent punkt fra retrospektiven for Epic 2, til story 3.1). Samtidig: resultatsiden skal sende til innleggingen hvis analysen mangler, i stedet for å stole på at steget betyr at den finnes.
- **POST for brevet:** KI-kallet startes bare fra POST, med `opptatt` rundt. Lykkes det, lagres brevet i `Soknad.brev`, steget flyttes til brev, og det blir redirect til brevsiden. Feiler det, vises resultatsiden på nytt uten redirect. Startsiden og modusvalget skal ikke skrives over av et KI-kall som pågår (rettet før story 3.1, gjelder også brevkallet).
- **Nullstilling:** `sett_inndata` og `velg_modus` nullstiller `brev` og `lastet_ned`. Endrer brukeren noe tidligere i flyten, gjelder ikke det gamle brevet lenger.
- **Nedlasting:** `GET /last-ned/docx` lager filen, setter `lastet_ned` og sender filen. Word lages bare i `adaptere/fil_ut.py` med python-docx, ett avsnitt per element i `avsnitt`.
- **Filnavn:** bare i `kjerne/filnavn.py`. Fullt mønster er `Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>` (ae/o/a for æøå, ASCII, mellomrom blir bindestrek, bare `[A-Za-z0-9-]`, arbeidsgiver høyst 30 tegn). I denne epicen er filnavnet alltid `Soknad_<ÅÅÅÅ-MM-DD>.docx`. Arbeidsgiveren kommer i Epic 7. `arbeidsgiver` kan i dag være tom tekst og gjøres om til `None` i story 4.2.
- **Feil:** `FilFeil` er unntaket når filen ikke kan lages. Alle tekster (også nye feiltyper) i `web/tekster.py`.
- **`kjerne/`** importerer aldri `docx` og leser ingen filer, så filnavnet regnes i kjernen og filen lages i adapteren. JavaScript endrer aldri søknadsdata. Webtester bruker `create_app(test_config)`, `test_client` og `TestKI`. Hver testfil og testfunksjon nevner FR-nummeret.

## UX & Interaction Patterns

- **Resultatsiden:** «Tilbake» nederst til venstre og «Lag søknadsbrevet mitt» (hovedknapp) ved siden av.
- **Ventetegn:** samme som i Epic 2, med «Vi lager brevet ditt – det kan ta en liten stund.» Etterpå går fokus til brevoverskriften, eller til feilboksen ved KI-feil.
- **KI-feil når brevet lages:** feilboksen på resultatsiden med «Resultatet og det du har lagt inn, er ikke borte.» og «Prøv på nytt».
- **Brevsiden:** overskriften «Din ferdigstilte søknad!» (egen brevoverskrift-typografi, mindre på mobil). Brevet som hvitt ark (`letter-card`) med skygge, `rounded.md`, høyst 720 px bredt, god luft rundt teksten. Ett avsnitt per element. Ingen «Tilbake» på brevsiden. Fyrverkeri, «Last ned som PDF» og «Nytt forslag» kommer i Epic 7.
- **Nedlastingsknappen:** «Last ned som Word» (hovedknapp). Etter nedlasting blir den grønn (`button-done`) med «✓ Lastet ned som Word», og under står «Filnavn: Soknad_<dato>.docx».
- **«Filen kan ikke lages»:** feilboksen øverst på brevsiden med «Vi klarte ikke å lage filen. Prøv på nytt.» og «Prøv på nytt». Brevet er ikke borte.
- **Vinduet etter nedlasting:** `<dialog>` med `showModal()`, hvitt, sentrert, høyst 420 px, mørkt slør bak. «Brevet er lastet ned!», filnavnet (der leses det opp av skjermlesere) og «Vil du lage en ny søknad eller logge ut?». Knappene «Lag ny søknad» (hovedknapp), «Logg ut» og «Bli her». Fokus til «Bli her» når det åpnes, Esc og «Bli her» lukker, fokus tilbake til knappen som åpnet det. `aria-labelledby` til overskriften og `aria-describedby` til teksten. Mens vinduet er åpent, kan bare vinduet nås.
- **«Logg ut»** i hjørneraden logger ut med en gang også på brevsiden. Vinduet «Logg ut før nedlasting» kommer i Epic 7.
- **Generelt:** egen sidetittel for brevsiden, `h1` for overskriften, pynteikoner skjult for skjermlesere, fokusring på alt som kan trykkes på. Ingen rulling sidelengs ved 320, 375, 768 og 1280 px og ved 200 % zoom, ingen faste høyder og ingen `nowrap`.

## Cross-Story Dependencies

- Story 3.1 bygger på Epic 2 (resultatsiden, ventetegnet, KI-feilboksen, `Soknad`, stegmodellen og `TestKI`). Story 3.2 trenger brevet fra 3.1, og story 3.3 trenger nedlastingen fra 3.2.
- Før story 3.1: punkt 1–4 fra retrospektiven for Epic 2 tas i en egen liten branch og PR (blant annet at et KI-kall som pågår ikke skriver over en ny søknad).
- «Lag ny søknad» bruker regelen fra Epic 2 om at startsiden alltid lager en ny `Soknad` og beholder testmodus. «Logg ut» bruker utloggingen fra story 1.4.
- Mot senere epics: Epic 4 lager `EkteKI.brev` og `prompts/brev.md` og bytter `brev-1.json` ut med et ekte KI-svar (pluss `brev-2.json`). Epic 5 legger til brevsiden for Korrektur. Epic 7 legger til «Nytt forslag», PDF, fyrverkeri, arbeidsgiveren i filnavnet og vinduet «Logg ut før nedlasting».
- Sjekkpunkt 29. november: hele flyten i testmodus (Epic 1–3) skal virke.
