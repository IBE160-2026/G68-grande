# Epic 7 Context: Ekstra valg og pynt (nødliste 1–3 og UX-kuttlisten)

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Brukeren kan be om et nytt forslag til brevet, laste ned brevet som PDF i tillegg til Word, og se om en endring i CV-en ga bedre treff, fordi prosenten regnes fra den samme nøkkelordlisten når bare CV-en er endret. Til slutt kommer pynten fra UX-kuttlisten: fyrverkeri på brevsiden, prosentlinjen som fylles, ikonet som vipper på modusvalget, vinduet «Logg ut før nedlasting» og arbeidsgiveren i filnavnet. Alt i epicen kan kuttes uten at kjerneflyten stopper. Storiene står i motsatt rekkefølge av nødlisten (det som kuttes først, bygges sist), og pynten kommer etter nødlistepunktene. Epicen er viktig fordi suksesskriterium 5 krever at både .docx og PDF kan åpnes, og kriterium 8 (samme annonse og CV gir samme treff i samme søknad) blir tydeligere med gjenbruken.

## Stories

- Story 7.1: Nytt forslag
- Story 7.2: Laste ned brevet som PDF
- Story 7.3: Gjenbruke nøkkelordlisten når bare CV-en er endret
- Story 7.4: Pynt: fyrverkeri og bevegelse
- Story 7.5: Logg ut før nedlasting, og arbeidsgiver i filnavnet

## Requirements & Constraints

- **Nytt forslag:** gir et nytt brev etter bekreftelse. I Korrektur lages det nye forslaget alltid fra brukerens opprinnelige eget brev. Nedlastingsknappene og filnavn-linjen nullstilles. Feiler KI-en, beholdes det gamle brevet, og feilboksen sier «Brevet du hadde, er beholdt.» med «Prøv på nytt». Hvert nytt forslag teller som ett av høyst 10 KI-kall per søknad.
- **PDF ut:** filen har bare den ferdige brevteksten med avsnittene, uten markeringer fra Korrektur og uten topp- eller bunntekst. Æ, ø og å skal vises riktig. Kan ikke filen lages, gjelder samme `FilFeil` («Vi klarte ikke å lage filen») som for Word. Kuttes 7.2, må kriterium 5 endres.
- **Gjenbruk av nøkkelordlisten:** listen gjenbrukes når den vaskede annonseteksten er lik (også med ekstra mellomrom), og hentes på nytt når annonsen er endret. Gap-analysen kjøres alltid på nytt. KI-en kalles ikke for nøkkelord når listen gjenbrukes. Kuttes 7.3, hentes listen på nytt hver gang, som i dag.
- **Pynt:** alle animasjoner slås av ved `prefers-reduced-motion`. Fyrverkeriet blinker ikke mer enn tre ganger i sekundet og dekker aldri brevet. Tallet i nøkkelordtreffet står alltid som tekst. Kuttes pynten, blir fyrverkeriet en enkel ✓, prosentlinjen vises ferdig fylt, og filnavnet blir `Soknad_<dato>`.
- **Filnavn:** `Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>.docx` eller `.pdf`. Æ → ae, ø → o, å → a, andre tegn til ASCII, mellomrom til bindestrek, alt annet enn `[A-Za-z0-9-]` fjernes, høyst 30 tegn for arbeidsgiveren. Uten arbeidsgiver: `Soknad_<dato>`. Filnavnet i vinduet og i filnavn-linjen er det samme som filen får.
- **Personvern:** loggen viser aldri CV, annonse eller brev. Ingenting lagres mellom øktene.
- **Tester:** hver testfil og testfunksjon nevner FR-nummeret (FR-15, FR-19, FR-25, FR-28, FR-29, FR-30). Felles hjelpere i `tests/web/hjelpere.py` brukes og kopieres ikke. Aldri det ekte API-et.

## Technical Decisions

- **Søknaden endres bare i kjernen:** `sett_inndata`, `velg_modus` og `nytt_forslag` i `kjerne/okt.py`. `nytt_forslag` øker `forslag` og nullstiller brevet og `lastet_ned`. `TestKI` gir `-1` ved oddetall og `-2` ved partall `forslag`, så forslag 1 og 2 gir ulike testbrev.
- **KI-kallet for nytt forslag** går gjennom den felles hjelperen `_med_ki` i `web/ruter.py` (innlogging, samtykke, plass til kallet, `opptatt` og telling). KI-kall startes bare fra POST, og steget flyttes bare etter en POST som lyktes.
- **Brevet settes sammen ett sted:** `ki_svar.hele_brevet()` legger til «Med vennlig hilsen» og navnet. Ruter og `fil_ut` setter aldri sammen brevet selv. Det gjelder også PDF og nytt forslag.
- **PDF ut bare i `adaptere/fil_ut.py`**, med fpdf2 og en TTF-skrift i `soknad/fonts/`. Skriften velges i 7.2: fri lisens og æøå (for eksempel Noto Sans eller DejaVu Sans), med lisensfilen ved siden av. Skrifter ligger lokalt. `kjerne/` importerer aldri fpdf. Nedlasting med `GET /last-ned/pdf`, som setter `lastet_ned`. Tester leser PDF-en med pypdf og sjekker at teksten med æøå er lik brevet.
- **Gjenbruken i `sett_inndata`:** den vaskede annonseteksten som listen ble laget fra, lagres alt med `sett_analyse` (samme vask som testdata-gjenkjenningen: NFKC, `casefold`, bare bokstaver og tall). Arbeidsgiveren kommer fra samme KI-svar som listen. Retro 6 bestemte at bare helt lik tekst beholder hele analysen (samme PDF på nytt). Det endres ikke her: 7.3 gjelder bare nøkkelordlisten.
- **Åpent fra retro 2 (avstemmes i 7.3):** vasken fjerner tegnsetting, så en annonse der bare «C++» er byttet til «C#», regnes som uendret. Arkitekturen sier at samme vask skal brukes. Avgjøres med Kristine.
- **Filnavn bare i `kjerne/filnavn.py`**, med enhetstester for æøå, mellomrom, spesialtegn, 30 tegn og manglende arbeidsgiver. Fra retro 4: `arbeidsgiver` renses først, fordi den kan ha linjeskift, kontrolltegn og tegn som `/` og `:`.
- **Pynten** bruker bare små skript uten rammeverk, og JavaScript endrer aldri søknadsdata.
- **Testfilene er store:** `test_brev.py` (ca. 1 150 linjer) og `test_innlegging.py` (ca. 1 550). Retro 5 foreslo å flytte testene for Korrektur til egen fil når «Nytt forslag» kommer.

## UX & Interaction Patterns

- **Brevsiden:** «Last ned som PDF» står ved siden av «Last ned som Word». Etter nedlasting blir knappen grønn med «✓ Lastet ned som PDF», filnavn-linjen viser `.pdf`, og vinduet etter nedlasting åpnes hver gang. «Bli her» lar brukeren laste ned det andre formatet. «Nytt forslag» står under nedlastingsknappene.
- **Vinduene** (`<dialog>` med `showModal()`, hvitt, høyst 420 px bredt, med `aria-labelledby` og `aria-describedby`): fokus til det trygge valget («Avbryt»), Esc lukker, og fokus går tilbake til knappen som åpnet.
  - «Vil du ha et nytt forslag?» · «Brevet du ser nå, blir slettet. Har du ikke lastet det ned, er det borte.» · «Ja, lag nytt forslag», «Avbryt». Etter «Ja» vises ventetegnet med «Vi lager brevet ditt – det kan ta en liten stund.», og så kommer nytt brev med nytt fyrverkeri.
  - Fra retro 3: samme vindu skal også spørre når «Lag søknadsbrevet mitt» trykkes på resultatsiden og et brev finnes (for eksempel etter nettleserens tilbakeknapp).
  - «Du har ikke lastet ned brevet. Vil du logge ut likevel? Brevet blir slettet.» · «Logg ut», «Avbryt». Bare på brevsiden før brevet er lastet ned i noe format. Er det lastet ned, logges brukeren ut med en gang.
- **Fyrverkeri** rundt brevoverskriften når brevsiden åpnes, også etter nytt forslag: nye utbrudd i ca. 2,2 s, borte etter ca. 3,2 s, høyst 3 utbrudd i sekundet, på venstre og høyre side, bak teksten. Fargene er `fireworks-gold`, `primary`, `accent`, `dot-middle` og `success`. Skjult for skjermlesere.
- **Prosentlinjen** (`score-meter`, 12 px høy) fylles på 1 s når resultatsiden åpnes.
- **Modus-kortet ved hover:** løftes 4 px, rammen blir `primary`, og ikonet vipper (−8°) og blir 10 % større (0,3 s). Ikonene er skjult for skjermlesere.
- **Redusert bevegelse:** fyrverkeriet vises ikke, prosentlinjen står ferdig fylt, og prikkene står stille.
- **Kjente fallgruver i CSS** (testene tegner ikke siden, så bare nettleseren finner dem): alt som får fokus fra et skript (her «Avbryt» i vinduene og knappen fokus går tilbake til), trenger også en `:focus`-regel, siden `:focus-visible` ikke vises etter museklikk. Overskrifter med `tabindex="-1"` skal ikke vise ring. I høykontrastmodus (`forced-colors: active`) forsvinner bakgrunner, så den grønne «Lastet ned»-knappen og vinduene trenger ramme i `CanvasText`, med sjekk i CSS-testen. Hver ny SVG (for eksempel i fyrverkeriet) trenger høyde i CSS. Ingen `style=`, ingen faste høyder og ingen `nowrap` (ingen rulling sidelengs ved 320 og 375 px).

## Cross-Story Dependencies

- Epic 3 (brevsiden, Word-nedlastingen, filnavn-linjen og vinduet etter nedlasting) og Epic 5 (Korrektur) er ferdige. Epic 7 bygger videre på dem.
- 7.1 og 7.2 endrer begge nedlastingsknappene og filnavn-linjen på brevsiden. 7.4 trenger 7.1 for fyrverkeriet etter nytt forslag.
- 7.5 bruker filnavnet i både Word og PDF, så den kommer etter 7.2. Vinduet «Logg ut før nedlasting» bruker `lastet_ned` fra begge formatene.
- 7.3 bygger på «Tilbake» fra resultatsiden (story 2.6) og på regelen fra retro 6 om helt lik tekst.
- Åpent hos Kristine: med lange tekster koster en søknad med «Nytt forslag» ca. 3,82 kr, over målet på 3 kr. Bestemme om det er greit.
- Kristine prøver i nettleseren og kommenterer PR-en. README sin statuslinje («PDF-nedlasting kommer») oppdateres i 7.2.
- Mot senere epics: story 8.1 (README) og 8.2 (testplanen) tar med at både .docx og PDF kan åpnes (kriterium 5).
