# Epic 5 Context: Korrektur av eget brev

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Brukeren velger Korrektur, legger inn CV, sitt eget søknadsbrev og stillingsannonsen, ser gap-analysen og nøkkelordtreffet som i Full generering, og får en forbedret versjon av brevet sitt. Endrede setninger er markert, og et trykk på en markert setning viser hva brukeren skrev. Epicen er viktig fordi Korrektur er et likeverdig alternativ til Full generering: helt KI-skrevne brev blir lett generiske, og her beholder brukeren sin egen stemme. Ingen av konkurrentene har korrektur av eget brev med markerte endringer. Suksesskriterium 4 (minst én markert endring, og fila er uten markeringer) og 12 (innhold, eksempler og rekkefølge beholdt) vises her.

## Stories

- Story 5.1: Velge Korrektur og legge inn eget brev
- Story 5.2: Forbedret brev fra KI-en
- Story 5.3: Se hva som er endret i Korrektur

## Requirements & Constraints

- **Modusvalget** får kortet Korrektur ved siden av Full generering. Innleggingen i Korrektur har tre felt (CV, eget brev, annonse) med de samme tilstandene, tekstene og feilene som før. Alle tre må fylles ut. Brevfeltet godtar høyst 5 000 tegn, CV og annonse 15 000 (bestemt av Kristine etter målingen i retro 5, runde B). CV og annonse fra case 2 gir den vanlige teksten for testdata på brevfeltet (bestemt i 5.1). Feltet for eget brev finnes bare i Korrektur, og «Tilbake» til modusvalget beholder CV og annonse.
- **Testmodus:** et eget brev som ikke hører til samme testcase som CV-en, gir `ikke_testdata` på brevfeltet. `testdata/case-1-<navn>/` får et fiktivt `eget-brev.txt` til samme annonse, med ting som bør forbedres og minst én av de 17 KI-frasene, og `fasit.md` får en sjekkliste for Korrektur. README sier hvor testbrevet ligger, og at Korrektur bare testes med case 1.
- **Brevet i Korrektur:** retter språk, ordvalg og flyt mot formell og akademisk tone, men beholder brukerens innhold, eksempler og rekkefølge. Bindeord og sammenslåtte korte setninger i samme avsnitt er lov, nye setninger med innhold er ikke. Vage vurderinger som «det har stort sett gått greit» fjernes. Overskriften rettes til «Søknad på stillingen som …», «Hei!» fjernes, og «dere» brukes når brevet blander «dere» og «du» (bestemt av Kristine i 5.2 og retro 5). Ingen av de 17 KI-frasene, og KI-en skriver dem om hvis brukeren har brukt dem selv. Bygger bare på CV, annonse og eget brev, og legger ikke til erfaring, utdanning eller ferdigheter.
- **Ubrukelig svar** gir KI-feilboksen, og det brukeren har lagt inn, er fortsatt der: når alle `ny` er `null`, eller når alle `gammel` satt sammen ikke er lik det opprinnelige brevet ordrett (se Svarformen under).
- **Nedlastet fil** har bare den ferdige brevteksten, uten markeringer, «Du skrev» eller «(Ny setning)».
- **Ekte testsvar:** skriptet lager også `korrektur-1.json` og `korrektur-2.json`. Korrektur-prompten kjøres tre ganger med ekte KI og sjekkes mot fasiten (kriterium 4 og 12), og resultatet står i `my-project/testplan.md`, også når noe feiler. En test sjekker at ingen av de 17 frasene står i noen `ny` i testsvarene.
- **Personvern og logg:** eget brev sendes til Claude bare når `Soknad.samtykke` er sann. Loggen viser aldri CV, annonse eller brev (heller ikke det egne).
- **Nødlisten:** story 5.3 (markeringene) er punkt 4. Kuttes den, virker Korrektur som etter 5.2, og forklaringen over brevet skjules.

## Technical Decisions

- **Grensesnittet:** `korrektur(cv, annonse, eget_brev, forslag: int)` i både `EkteKI` og `TestKI`. `TestKI` bruker `korrektur-1` ved oddetall og `korrektur-2` ved partall `forslag`. `anthropic` importeres bare i `adaptere/ki.py`.
- **Svarformen:** `{setninger: [{ny: str | null, gammel: [str], nytt_avsnitt: bool}]}` i brevets rekkefølge, med `prompts/korrektur.md` og eget JSON-skjema sendt med structured outputs (`additionalProperties: false`, alle felt påkrevd). Svaret går gjennom den samme `kjerne/ki_svar.kontroller()`, som også sjekker `stop_reason` og ugyldig JSON. Sammenligningen av `gammel` mot originalen er ordrett med store bokstaver og tegnsetting, men uten mellomrom, linjeskift, usynlige formattegn og tegn Word ikke tåler, og en tom `gammel` avvises (endret fra `testdata_match.vask` i retro 5). I testmodus sjekkes svaret mot casets egen `eget-brev.txt`.
- **Visningen regner aldri ut endringer selv:** en setning er endret når `gammel != [ny]`, ny når `gammel == []` og fjernet når `ny == null`. Brevet som vises og lastes ned, er alle `ny` som ikke er `null`, satt sammen, med nytt avsnitt der `nytt_avsnitt` er sann. Ruter og `fil_ut` setter ikke sammen brevet hver for seg.
- **Deling av setninger:** prompten sier at én setning aldri deles i to oppføringer. Blir en lang setning til to, står begge i samme `ny`. Ellers blir andre halvdel feilaktig vist som «(Ny setning)» (funnet i prøven 7. november).
- **Hilsen og navn:** i Full generering setter `ki_svar.hele_brevet()` inn «Med vennlig hilsen» og `navn` fra KI-en. Dette ble med vilje ikke gjort for Korrektur. Brukerens eget brev har kanskje allerede hilsen og navn, og de må i så fall stå i `gammel`, ellers stemmer ikke sjekken mot originalen. Bestemt i 5.2: hilsen og navn står slik brukeren skrev dem, og mangler de, legges ingenting til.
- **Rensing:** brevteksten i Full generering renses i `kontroller` (kontrolltegn, linjeskift og tab), fordi et kontrolltegn ellers gir `FilFeil` i `lag_docx` hver gang. `ny` i Korrektur går også til Word og har samme risiko.
- **Økten:** `Soknad` får `eget_brev` (med `tekst` og `filnavn`) og `korrektur`, med de navnene. `sett_inndata` og `velg_modus` nullstiller `korrektur` når den ikke lenger gjelder. Stegene er de samme (start < modus < innlegging < resultat < brev).
- **KI-kallet:** den nye ruten for «Oppdater søknadsbrevet mitt» bruker hjelperen `_med_ki` i `web/ruter.py` (samtykke og valg av KI fra samme innlogging, utlogget til innloggingen, plass under 10 KI-kall, `opptatt` og telling). Ingen egen kopi av rekkefølgen. KI-kall bare fra POST.
- **Tester:** falsk Anthropic-klient og sperren mot nettverk i `conftest.py`, aldri det ekte API-et. Felles hjelpere ligger i `tests/web/hjelpere.py` og kopieres ikke. Hver testfil og testfunksjon nevner FR-nummeret (FR-8, FR-9, FR-20, FR-23, FR-24, FR-28, FR-30, FR-34, FR-37, FR-38).
- **Prompt-endringer samles** før kjøringene med ekte KI, fordi hver endring betyr at alle kriteriene må kjøres på nytt. Kristine bestemmer.

## UX & Interaction Patterns

- **Kortet:** ✏️ «Korrektur» · «Forbedre mitt brev» · «Du har skrevet et brev selv. Vi forbedrer språket og beholder innholdet ditt.» Hele kortet er én knapp. Kortene står under hverandre under 700 px.
- **Innleggingen:** overskriften «Legg inn CV-en din, brevet ditt og stillingsannonsen», feltene «📄 CV», «✉️ Ditt søknadsbrev» og «📢 Stillingsannonse». Feltene står side om side først fra 1000 px. Feilteksten for testdata på brevfeltet begynner med «Ditt søknadsbrev:».
- **Resultatsiden:** som i Full generering, med «Tilbake» og «Oppdater søknadsbrevet mitt» nederst. Ventetegnet viser «Vi lager brevet ditt – det kan ta en liten stund.».
- **Brevsiden:** overskriften «Din oppdaterte søknad er ferdig!», brevet som hvitt ark (høyst 720 px), «Last ned som Word» og vinduet etter nedlasting som i Epic 3. Over brevet en liten hvit boks: «Grønn og understreket = endret. Trykk på setningen for å se det du skrev.», med skjult tilleggstekst «Endrede setninger er knapper.».
- **Endret setning:** et `<span>` med `role="button"` og `tabindex="0"`, ikke en `<button>`, så setningen brytes over linjer som resten av avsnittet (retro 5, runde B). Lys grønn bakgrunn (`success-tint`) og 2 px grønn understreking, vanlig tekstfarge, mørkere (`changed-active`) ved hover og når den er åpen, og skjult tekst «Endret setning». Trykk, Enter eller mellomrom åpner og lukker «Du skrev» rett under, med den gamle setningen i dempet farge og strek til venstre (`old-sentence`). Flere kan være åpne samtidig. Sammenslåtte setninger viser begge de gamle, en ny setning viser «(Ny setning)».
- **Fjernet og uendret:** én linje under brevet, «1 setning er fjernet.» eller «2 setninger er fjernet.». Er ingenting endret: «Vi fant ingenting å endre. Brevet ditt er bra som det er.», og forklaringen over brevet skjules. Er ingen setning endret, men noen fjernet, skjules forklaringen også (bestemt i 5.3).
- **Kjente fallgruver i CSS** (testene tegner ikke siden, så bare nettleseren finner dem): alt som får fokus fra et skript, trenger også en `:focus`-regel, siden `:focus-visible` ikke vises etter museklikk. Overskrifter med `tabindex="-1"` skal ikke vise ring. I høykontrastmodus (`forced-colors: active`) forsvinner bakgrunner, så de grønne setningene og forklaringsboksen trenger ramme eller understreking i `CanvasText`, med sjekk i CSS-testen. Hver ny SVG trenger høyde i CSS. Ingen `style=` og ingen faste høyder.

## Cross-Story Dependencies

- **Før 5.1:** bestemme hva Korrektur gjør med CV og annonse fra case 2, som ikke har noe `eget-brev.txt` (åpent punkt, og `annen_case` finnes bare for annonsefeltet).
- 5.1 lager kortet, brevfeltet, `eget_brev` i økten og testbrevet. Resultatsiden i Korrektur har ingen knapp videre før 5.2.
- 5.2 trenger 5.1. Den legger til `korrektur` i begge KI-utgavene, prompten, skjemaet, kontrollen, knappen, ruten via `_med_ki`, brevsiden uten markeringer og testsvarene med skriptet. Kjøringene med ekte KI koster penger (taket er 250 kr), så Kristine godkjenner før de starter.
- 5.3 trenger 5.2 og legger bare markeringene på brevsiden. Kristine prøver i nettleseren (375 og 1280 px, tastatur, høykontrast).
- Mot senere epics: Epic 6 legger til PDF for alle tre feltene. Epic 7 lager «Nytt forslag», som i Korrektur alltid sender det opprinnelige `eget_brev` og bruker `korrektur-2.json` i testmodus, og fyrverkeriet rundt brevoverskriften.
