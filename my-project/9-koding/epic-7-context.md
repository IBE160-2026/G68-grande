# Epic 7 Context: Ekstra valg og pynt (nødliste 1–3 og UX-kuttlisten)

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Brukeren kan be om et nytt forslag til brevet, laste ned brevet som PDF i tillegg til Word, og se om en endring i CV-en ga bedre treff, fordi prosenten regnes fra den samme nøkkelordlisten når bare CV-en er endret. Til slutt kommer pynten fra UX-kuttlisten: fyrverkeri på brevsiden, prosentlinjen som fylles, ikonet som vipper på modusvalget, vinduet «Logg ut før nedlasting» og arbeidsgiveren i filnavnet. Alt i epicen kan kuttes uten at kjerneflyten stopper. Storiene står i motsatt rekkefølge av nødlisten (det som kuttes først, bygges sist), og pynten kommer etter nødlistepunktene. Epicen er viktig fordi suksesskriterium 5 krever at både .docx og PDF kan åpnes, og kriterium 8 (samme annonse og CV gir samme treff i samme søknad) blir tydeligere med gjenbruken. Story 7.1 og 7.2 er ferdige (flettet). Neste er 7.3.

## Stories

- Story 7.1: Nytt forslag (ferdig)
- Story 7.2: Laste ned brevet som PDF (ferdig)
- Story 7.3: Gjenbruke nøkkelordlisten når bare CV-en er endret
- Story 7.4: Pynt: fyrverkeri og bevegelse
- Story 7.5: Logg ut før nedlasting, og arbeidsgiver i filnavnet

## Requirements & Constraints

- **Nytt forslag (ferdig):** nullstiller brevet, nedlastingsknappene, filnavn-linjen og `lastet_ned`. I Korrektur lages det alltid fra det opprinnelige `eget_brev`. Ved KI-feil beholdes det gamle brevet. Hvert forslag teller som ett av høyst 10 KI-kall per søknad. Kristine har godtatt ca. 3,82 kr per søknad med ett nytt forslag (lange tekster), uten egen grense.
- **PDF ut:** filen har bare den ferdige brevteksten med avsnittene, uten markeringer fra Korrektur og uten topp- eller bunntekst. Æ, ø og å skal vises riktig. Kan ikke filen lages, gjelder samme `FilFeil` («Vi klarte ikke å lage filen») som for Word. Kuttes 7.2, må kriterium 5 endres.
- **Gjenbruk av nøkkelordlisten:** listen gjenbrukes når den vaskede annonseteksten er lik (også med ekstra mellomrom), og hentes på nytt når annonsen er endret. Gap-analysen kjøres alltid på nytt. KI-en kalles ikke for nøkkelord når listen gjenbrukes. Kuttes 7.3, hentes listen på nytt hver gang, som i dag.
- **Pynt:** alle animasjoner slås av ved `prefers-reduced-motion`. Fyrverkeriet blinker ikke mer enn tre ganger i sekundet og dekker aldri brevet. Tallet i nøkkelordtreffet står alltid som tekst. Kuttes pynten, blir fyrverkeriet en enkel ✓, prosentlinjen vises ferdig fylt, og filnavnet blir `Soknad_<dato>`.
- **Filnavn:** `Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>.docx` eller `.pdf`. Æ → ae, ø → o, å → a, andre tegn til ASCII, mellomrom til bindestrek, alt annet enn `[A-Za-z0-9-]` fjernes, høyst 30 tegn for arbeidsgiveren. Uten arbeidsgiver: `Soknad_<dato>`. Filnavnet i vinduet og i filnavn-linjen er det samme som filen får.
- **Personvern:** loggen viser aldri CV, annonse eller brev. Ingenting lagres mellom øktene.
- **Tester:** hver testfil og testfunksjon nevner FR-nummeret (FR-15, FR-19, FR-29, FR-30 og så videre). Felles hjelpere i `tests/web/hjelpere.py` brukes og kopieres ikke. Aldri det ekte API-et. Nye tester legges i egne filer, slik 7.1 gjorde med `test_nytt_forslag.py`, så `test_brev.py` og `test_innlegging.py` ikke vokser mer.

## Technical Decisions

- **Søknaden endres bare i kjernen:** `sett_inndata`, `velg_modus` og `nytt_forslag` i `kjerne/okt.py`. KI-kall bare fra POST gjennom `_med_ki` i `web/ruter.py`, og steget flyttes bare etter en POST som lyktes.
- **Brevet settes sammen ett sted:** `ki_svar.hele_brevet()` legger til «Med vennlig hilsen» og navnet. Ruter og `fil_ut` setter aldri sammen brevet selv. Det gjelder også PDF.
- **PDF ut bare i `adaptere/fil_ut.py`**, med fpdf2 og en TTF-skrift i `soknad/fonts/`. Skriften er Noto Sans 11 pt (fri lisens OFL, bestemt av Kristine i 7.2), med OFL.txt i `soknad/fonts/`. Skrifter ligger lokalt. `kjerne/` importerer aldri fpdf. Nedlasting med `GET /last-ned/pdf`, som setter `lastet_ned`. Tester leser PDF-en med pypdf og sjekker at teksten med æøå er lik brevet.
- **Gjenbruken i `sett_inndata`:** den vaskede annonseteksten som listen ble laget fra, lagres alt med `sett_analyse` (samme `vask` som testdata-gjenkjenningen: NFKC, `casefold`, bare bokstaver og tall). Arbeidsgiveren kommer fra samme KI-svar som listen. Regelen fra retro 6 om at bare helt lik tekst beholder hele analysen, endres ikke: 7.3 gjelder bare nøkkelordlisten.
- **Åpent (avstemmes i 7.3):** vasken fjerner tegnsetting, så en annonse der bare «C++» er byttet til «C#», regnes som uendret. Arkitekturen sier at samme vask skal brukes. Avgjøres med Kristine.
- **Filnavn bare i `kjerne/filnavn.py`**, med enhetstester for æøå, mellomrom, spesialtegn, 30 tegn og manglende arbeidsgiver. `arbeidsgiver` renses først, fordi den kan ha linjeskift, kontrolltegn og tegn som `/` og `:`.
- **Pynten** bruker bare små skript uten rammeverk, og JavaScript endrer aldri søknadsdata. Skript testes bare som kildetekst (ingen nettlesertester), så de prøves for hånd i PR-en.

## UX & Interaction Patterns

- **Brevsiden:** «Last ned som PDF» står ved siden av «Last ned som Word». Etter nedlasting blir knappen grønn med «✓ Lastet ned som PDF», filnavn-linjen viser `.pdf`, og vinduet etter nedlasting åpnes hver gang. «Bli her» lar brukeren laste ned det andre formatet. «Nytt forslag» står under nedlastingsknappene.
- **Vinduene** (`<dialog>` med `showModal()`, `aria-labelledby` og `aria-describedby`): fokus til det trygge valget («Avbryt»), Esc lukker, og fokus går tilbake til knappen som åpnet. Vinduet «Nytt forslag» og `bekreft.js` finnes fra 7.1.
  - «Du har ikke lastet ned brevet. Vil du logge ut likevel? Brevet blir slettet.» · «Logg ut», «Avbryt». Bare på brevsiden før brevet er lastet ned i noe format. Er det lastet ned, logges brukeren ut med en gang.
- **Fyrverkeri** rundt brevoverskriften når brevsiden åpnes, også etter nytt forslag: nye utbrudd i ca. 2,2 s, borte etter ca. 3,2 s, høyst 3 utbrudd i sekundet, på venstre og høyre side, bak teksten. Fargene er `fireworks-gold`, `primary`, `accent`, `dot-middle` og `success`. Skjult for skjermlesere.
- **Prosentlinjen** (`score-meter`, 12 px høy) fylles på 1 s når resultatsiden åpnes.
- **Modus-kortet ved hover:** løftes 4 px, rammen blir `primary`, og ikonet vipper (−8°) og blir 10 % større (0,3 s). Ikonene er skjult for skjermlesere.
- **Redusert bevegelse:** fyrverkeriet vises ikke, prosentlinjen står ferdig fylt, og prikkene står stille.
- **Kjente fallgruver i CSS** (bare nettleseren finner dem): alt som får fokus fra et skript, trenger også en `:focus`-regel, siden `:focus-visible` ikke vises etter museklikk. Overskrifter med `tabindex="-1"` skal ikke vise ring. I høykontrastmodus (`forced-colors: active`) trenger den grønne «Lastet ned»-knappen og vinduene ramme i `CanvasText`, med sjekk i CSS-testen. Hver ny SVG (for eksempel i fyrverkeriet) trenger høyde i CSS. Ingen `style=`, ingen faste høyder og ingen `nowrap` (ingen rulling sidelengs ved 320 og 375 px).

## Cross-Story Dependencies

- Epic 3 (brevsiden, Word-nedlastingen, filnavn-linjen og vinduet etter nedlasting), Epic 5 (Korrektur) og story 7.1 er ferdige. Resten av epicen bygger videre på dem.
- 7.2 endrer nedlastingsknappene og filnavn-linjen som 7.1 nullstiller ved nytt forslag. 7.4 viser fyrverkeriet også etter nytt forslag.
- 7.5 bruker filnavnet i både Word og PDF, så den kommer etter 7.2. Vinduet «Logg ut før nedlasting» bruker `lastet_ned` fra begge formatene.
- 7.3 bygger på «Tilbake» fra resultatsiden (story 2.6) og på regelen fra retro 6 om helt lik tekst.
- Kristine prøver i nettleseren og kommenterer PR-en. README sin statuslinje («PDF-nedlasting kommer») oppdateres i 7.2.
- Mot senere epics: story 8.1 (README) og 8.2 (testplanen) tar med at både .docx og PDF kan åpnes (kriterium 5). Nettlesertester for skriptene hører til issue #16 (story 8.2).
