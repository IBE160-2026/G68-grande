---
name: Søknadsassistenten
description: Nettside som hjelper studenter å skrive søknadsbrev. Fargetema «Myk fersken», systemskrift, runde hjørner og små animasjoner. Bare lys modus.
status: final
created: 2026-10-20
updated: 2026-10-23
sources:
  - ../../prds/prd-kode-prosjekt-2026-10-09/prd.md
  - ../../prds/prd-kode-prosjekt-2026-10-09/addendum.md
colors:
  # Valgt fargetema «Myk fersken» (memlog). Alle navn er roller, ikke fargenavn,
  # slik at mørk modus kan legges til senere som egne tokens med -dark på slutten.
  primary: '#A23E6C'
  primary-contrast: '#FFFFFF'
  accent: '#F6B8A0'
  background: '#FFF7F5'
  surface: '#FFFFFF'
  text: '#3A2530'
  text-muted: '#6E5560'
  border: '#EED7DD'
  success: '#2F7A57'
  success-tint: '#E4F3EB'
  error: '#B4232F'
  focus-ring: '#3B5BDB'
  # Fra skissene, godkjent av Kristine i runde 3 (sketch-colors-1.html):
  error-tint: '#FBE6E8'
  work-on: '#8A3A20'
  work-on-tint: '#FDEEE8'
  changed-active: '#CFEBDC'
  dot-middle: '#C0618C'
  fireworks-gold: '#F2C14E'
typography:
  # Systemskrift overalt. Ingen nettskrift, unntatt logoen.
  logo:
    fontFamily: "'Baloo 2', {typography.body.fontFamily}"
    fontWeight: '800'
    fontSize: 'clamp(1.35rem, 5vw, 2.4rem)'
    lineHeight: '1.2'
  wait-title:
    fontFamily: '{typography.logo.fontFamily}'
    fontWeight: '800'
    fontSize: 1.5rem
  body:
    fontFamily: '"Segoe UI", system-ui, -apple-system, sans-serif'
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: '1.5'
  heading-page:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.2rem
    fontWeight: '700'
    lineHeight: '1.3'
  heading-welcome:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.3rem
    fontWeight: '700'
  heading-letter:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.5rem
    fontWeight: '700'
  heading-letter-mobile:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.25rem
    fontWeight: '700'
  heading-box:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.1rem
    fontWeight: '700'
  score:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.6rem
    fontWeight: '700'
  label:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 0.92rem
    fontWeight: '600'
  small:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 0.88rem
    fontWeight: '400'
  caption:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 0.78rem
    fontWeight: '400'
  tag:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 0.75rem
    fontWeight: '600'
  button-hero:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.5rem
    fontWeight: '600'
  button-hero-mobile:
    fontFamily: '{typography.body.fontFamily}'
    fontSize: 1.25rem
    fontWeight: '600'
rounded:
  xs: 8px
  sm: 14px
  md: 18px
  lg: 26px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 20px
  '6': 24px
  '7': 32px
  page-side: 20px
  page-side-mobile: 16px
components:
  button-primary:
    background: '{colors.primary}'
    foreground: '{colors.primary-contrast}'
    border: '2px solid {colors.primary}'
    radius: '{rounded.lg}'
    padding: '{spacing.3} {spacing.5}'
    fontWeight: '600'
  button-secondary:
    background: '{colors.surface}'
    foreground: '{colors.primary}'
    border: '2px solid {colors.primary}'
    radius: '{rounded.lg}'
    padding: '{spacing.3} {spacing.5}'
  button-hero:
    background: '{colors.primary}'
    foreground: '{colors.primary-contrast}'
    radius: '{rounded.lg}'
    typography: '{typography.button-hero}'
    padding: '24px 64px'
  button-done:
    background: '{colors.success-tint}'
    foreground: '{colors.success}'
    border: '2px solid {colors.success}'
    radius: '{rounded.lg}'
  link-button:
    background: 'none'
    foreground: '{colors.primary}'
    textDecoration: 'underline'
  mode-card:
    background: '{colors.surface}'
    border: '2px solid {colors.border}'
    borderHover: '2px solid {colors.primary}'
    radius: '{rounded.lg}'
    padding: '22px 18px'
  text-input:
    background: '{colors.surface}'
    border: '2px solid {colors.primary}'
    borderError: '2px solid {colors.error}'
    radius: '{rounded.sm}'
    padding: '10px 12px'
  upload-field:
    background: '{colors.surface}'
    border: '2px solid {colors.border}'
    borderError: '2px solid {colors.error}'
    errorText: '{colors.error}'
    radius: '{rounded.lg}'
    padding: 18px
  file-chip:
    background: '{colors.success-tint}'
    foreground: '{colors.success}'
    radius: '{rounded.sm}'
  trash-button:
    background: 'none'
    minSize: 24px
    focus: '3px solid {colors.focus-ring}'
  checkbox:
    size: 22px
    border: '2px solid {colors.primary}'
    checked: '{colors.primary}'
    outlineError: '2px solid {colors.error}'
  error-box:
    background: '{colors.error-tint}'
    foreground: '{colors.error}'
    border: '2px solid {colors.error}'
    radius: '{rounded.md}'
  form-error:
    background: '{colors.error-tint}'
    foreground: '{colors.error}'
    border: '1px solid {colors.error}'
    radius: '{rounded.sm}'
  info-icon:
    background: '{colors.surface}'
    foreground: '{colors.primary}'
    border: '2px solid {colors.primary}'
    size: 24px
    radius: '{rounded.full}'
  info-tip:
    background: '{colors.text}'
    foreground: '{colors.primary-contrast}'
    radius: '{rounded.sm}'
    width: 'min(300px, 78vw)'
  testmode-toggle:
    trackOff: '{colors.text-muted}'
    trackOn: '{colors.primary}'
    width: 44px
    height: 24px
  testmode-badge:
    background: '{colors.accent}'
    foreground: '{colors.text}'
    radius: '{rounded.sm}'
  ai-tag:
    background: '{colors.accent}'
    foreground: '{colors.text}'
    radius: '{rounded.sm}'
  gap-covers:
    background: '{colors.success-tint}'
    heading: '{colors.success}'
    radius: '{rounded.md}'
  gap-work-on:
    background: '{colors.work-on-tint}'
    heading: '{colors.work-on}'
    radius: '{rounded.md}'
  score-meter:
    track: '{colors.border}'
    fill: '{colors.primary}'
    height: 12px
    radius: '{rounded.xs}'
  letter-card:
    background: '{colors.surface}'
    border: '1px solid {colors.border}'
    radius: '{rounded.md}'
    maxWidth: 720px
  changed-sentence:
    foreground: '{colors.text}'
    background: '{colors.success-tint}'
    backgroundActive: '{colors.changed-active}'
    underline: '2px {colors.success}'
  old-sentence:
    background: '{colors.background}'
    foreground: '{colors.text-muted}'
    borderLeft: '4px solid {colors.text-muted}'
  dialog:
    background: '{colors.surface}'
    radius: '{rounded.lg}'
    maxWidth: 420px
  wait-overlay:
    dot1: '{colors.primary}'
    dot2: '{colors.dot-middle}'
    dot3: '{colors.accent}'
    dotSize: 16px
    title: '{colors.primary}'
    titleTypography: '{typography.wait-title}'
  corner-row:
    background: '{colors.background}'
    borderTop: '1px solid {colors.border}'
    padding: '{spacing.3} {spacing.4}'
    kiNote: '{colors.text-muted}'
    logoutBackground: '{colors.surface}'
    logoutForeground: '{colors.primary}'
    logoutBorder: '2px solid {colors.primary}'
---

# Søknadsassistenten — DESIGN

> Skissene ligger i `mockups/` (se lenker under hver del). **Ved konflikt mellom skisse og dette dokumentet gjelder dokumentet.** Hvordan nettsiden *oppfører seg*, står i `EXPERIENCE.md`.

## Brand & Style

Søknadsassistenten er en nettside for studenter som skal søke jobb, ofte for første gang. Mange er usikre. Siden skal føles som en vennlig hjelper, ikke som et skjema.

De tre ordene er **enkel, effektiv, levende**. «Levende» betyr en blanding av farger, små animasjoner, små ikoner og vennlig, personlig tekst. Det motsatte, en statisk og kjedelig nettside, er det vi vil unngå.

Innloggingen og registreringen er bevisst vanlige og enkle, slik innloggingssider stort sett ser ut. Det levende spares til resten av siden: kortene som løfter seg, prikkene som hopper mens vi venter, prosentlinjen som fylles og fyrverkeriet når brevet er ferdig.

Bare lys modus i versjon 1. Mørk modus står på TO DO som «hvis tid».

→ Fargevalget: `mockups/color-themes-1.html`, `mockups/color-themes-2.html` (bare «Myk fersken», variant A / nr. 5, er valgt).

## Colors

Fargetemaet heter «Myk fersken». Det ble valgt fordi det er «så lunt». Alle farger er navngitte tokens, slik at mørk modus senere kan legges til som egne tokens (for eksempel `background-dark`).

- **Bringebær (`{colors.primary}` #A23E6C)** er hovedfargen. Brukes på hovedknapper, logoen, lenker, «i»-ikoner, prosentlinjen og aktiv bryter. Hvit tekst på denne fargen har kontrast 6,1:1.
- **Hvit (`{colors.primary-contrast}`)** er tekst på hovedfargen.
- **Fersken (`{colors.accent}` #F6B8A0)** er pyntefargen. Brukes på merkelappen «Testmodus», merket «Laget av KI» og den tredje ventetegn-prikken. Aldri som tekstfarge.
- **Lys fersken (`{colors.background}` #FFF7F5)** er bakgrunnen på alle sider.
- **Hvit (`{colors.surface}`)** er bakgrunnen på kort, felt, brevet og vinduer.
- **Mørk plomme (`{colors.text}` #3A2530)** er vanlig tekst. Kontrast mot bakgrunnen er 13,4:1. Den brukes også som bakgrunn i «i»-boksen, med hvit tekst.
- **Dempet plomme (`{colors.text-muted}` #6E5560)** er hjelpetekst, ingress, KI-merknaden og den gamle setningen i Korrektur. Den er også sporet i testmodus-bryteren når bryteren er av.
- **Lys rosa (`{colors.border}` #EED7DD)** er rammer og sporet i prosentlinjen.
- **Grønn (`{colors.success}` / `{colors.success-tint}`)** betyr «dette er bra» eller «ferdig»: «Dette dekker CV-en din», nøkkelord som står i CV-en, filnavnet etter opplasting, endrede setninger i Korrektur og knappen «✓ Lastet ned som …».
- **`{colors.changed-active}`** (#CFEBDC): endret setning når man holder over den, eller når den er åpnet.
- **`{colors.work-on}` / `{colors.work-on-tint}`** (#8A3A20 på #FDEEE8): lista «Dette kan du jobbe videre med». Varm, ikke rød, fordi det ikke er en feil.
- **Rød (`{colors.error}` / `{colors.error-tint}`)** brukes bare til feil: røde rammer, feiltekst og feilboksene.
- **Blå (`{colors.focus-ring}` #3B5BDB)** er fokusringen for tastatur. Den er blå med vilje, så den skiller seg fra bringebær og rød.
- **`{colors.dot-middle}`** (#C0618C): den midterste ventetegn-prikken.
- **`{colors.fireworks-gold}`** (#F2C14E): én av fem fyrverkeri-farger (de andre er primary, accent, dot-middle og success).

work-on, work-on-tint, changed-active, dot-middle og fireworks-gold (og error-tint) kom fra skissene. Kristine så dem i `mockups/sketch-colors-1.html` og godkjente dem i runde 3.

### Kontrast

Kontrast (WCAG AA, regnet ut):

| Farge | Mot | Kontrast | Merknad |
|---|---|---|---|
| text-muted | background | 6,3:1 | |
| error | error-tint | 5,5:1 | |
| success | success-tint | 4,5:1 | |
| work-on | work-on-tint | 6,9:1 | |
| text | accent | 8,3:1 | |
| hvit | text | 14,1:1 | |
| focus-ring | background | 5,4:1 | |
| primary | background | 5,8:1 | lenker |
| error | surface | 6,5:1 | |
| text-muted | surface | 6,7:1 | også bryteren når den er av |
| focus-ring | surface | 5,7:1 | |
| primary | border | 4,47:1 | prosentlinjen, bare pynt |

Låste knapper (55 % synlig) og den låste bryteren (60 % synlig) har bevisst lavere kontrast, ca. 2,6:1 og 2,7:1. WCAG krever ikke kontrast for låste knapper, og teksten «Mangler API-nøkkel, se README» forklarer den låste bryteren.

`{colors.success}` på `{colors.success-tint}` (4,5:1) har ingen margin. Ikke gjør den grønne teksten lysere eller bakgrunnen mørkere.

Fokusringen har alltid 2 px luft. Uten luft er kontrasten mot en bringebærfarget knapp bare 1,1:1.

Tekstfelt, tekstbokser og avkrysningsbokser har ramme i `{colors.primary}` (6,1:1 mot hvit), fordi `{colors.border}` bare har 1,4:1 og WCAG AA krever 3:1 for rammer rundt felt (NFR-6). Kort og bokser beholder den lyse `{colors.border}`, fordi rammen der bare er pynt. Sammenligningen ligger i `mockups/border-contrast-1.html`.

→ Fargene fra skissene slik de brukes: `mockups/sketch-colors-1.html`. Rammefargene: `mockups/border-contrast-1.html`.

## Typography

Systemskrift på hele siden: Segoe UI på Windows, San Francisco på Mac osv. Ingen nettskrift. Grunn: «enkel og grei».

Unntakene er **logoen «Søknadsassistenten»** og **«På vei mot ny jobb» i ventetegnet**. Begge står i **Baloo 2 ExtraBold (800)**. Hele logoen skal stå på én linje både på PC og på mobil (375 px), ved vanlig tekststørrelse. Derfor skalerer størrelsen med skjermbredden: `{typography.logo.fontSize}` (skissene bruker 1,45rem på 375 px). Logoen står øverst og sentrert på alle sider.

Blir teksten større enn det er plass til (for eksempel ved 200 % zoom), får logoen og ingressen på startsiden bryte linjen. Ingen `nowrap` på tekst. Ved vanlig tekststørrelse skal alt se ut akkurat som i skissene.

«På vei mot ny jobb» står i Baloo 2 ExtraBold, ca. 1,5rem, i `{colors.primary}`, som i skissene (`{typography.wait-title}`). Det gjør ventetegnet mer levende.

Om Baloo 2 lastes fra Google Fonts eller ligger som fil i prosjektet, avgjøres i arkitekturen. Lastes den ikke, brukes systemskriften.

| Rolle | Token | Brukes til |
|---|---|---|
| Logo | `{typography.logo}` | «Søknadsassistenten» |
| Sideoverskrift | `{typography.heading-page}` | «Hva vil du gjøre i dag?», «Legg inn CV-en din …», «Slik passer CV-en din til stillingen» |
| Velkomst | `{typography.heading-welcome}` | «Velkommen! 👋» |
| Brevoverskrift | `{typography.heading-letter}` / `{typography.heading-letter-mobile}` | «Din ferdigstilte søknad!», «Din oppdaterte søknad er ferdig!» |
| Boksoverskrift | `{typography.heading-box}` | «Gap-analyse», «Nøkkelordtreff», feltnavn |
| Tall | `{typography.score}` | «7 av 10 = 70 %» |
| Brødtekst | `{typography.body}` | Alt annet |
| Etikett | `{typography.label}` | Feltetiketter, knapper i felt |
| Liten | `{typography.small}` | Hjelpetekst, forklaring under feltnavn |
| Bildetekst | `{typography.caption}` | KI-merknaden |
| Merkelapp | `{typography.tag}` | «Testmodus», «Laget av KI» |
| Stor knapp | `{typography.button-hero}` / `{typography.button-hero-mobile}` | «Begynn å lage søknad» |
| Ventetittel | `{typography.wait-title}` | «På vei mot ny jobb» |

Hvilket overskriftsnivå (h1–h3) hver rolle har, står i `EXPERIENCE.md` under Accessibility Floor.

→ Logoskrift: `mockups/logo-fonts-1.html` (Baloo 2 er valgt).

## Layout & Spacing

Skalaen er 4 / 8 / 12 / 16 / 20 / 24 / 32 px (`{spacing.1}`–`{spacing.7}`). Tallene er hentet fra skissene. Verdier utenfor skalaen rundes til nærmeste token, for eksempel 26 × 30 → 24 × 32 px. Hvordan hjørnene er rundet av, står under Shapes.

**Bruddpunkt: 700 px.** Under 700 px står alt under hverandre. Fra 700 px og oppover står ting side om side, også på nettbrett (768 px). Det er ingen egen nettbrettskisse, men skissene har en knapp for nettbrett (768 px).

**Unntak: innleggingsfeltene står side om side først fra 1000 px.** Under 1000 px står de under hverandre, også på nettbrett (768 px). 700 px gjelder fortsatt for modusvalget, gap-analysen og nøkkelordlistene.

- Innholdet er sentrert. Brevet er høyst 720 px bredt. Skjemaene på innlogging og registrering er høyst 360 px brede.
- Sidemarg: `{spacing.page-side}` på PC, `{spacing.page-side-mobile}` på mobil.
- **PC:** ting står side om side — modus-kortene (2), innleggingsfeltene (2 i Full generering, 3 i Korrektur, først fra 1000 px), gap-analysens to lister («dekker» til venstre) og nøkkelordenes to lister.
- **Mobil (375 px):** alt står under hverandre i én kolonne. «Begynn å lage søknad» går over hele bredden.
- Ingen side skal rulle sidelengs ved 375, 768 og 1280 px (NFR-7). Siden skal også virke ved 320 px bredde og 200 % zoom uten rulling sidelengs (WCAG 1.4.10).
- Ingen faste høyder på knapper, merkelapper eller bokser med tekst.

→ Oppsett per side: `mockups/login-register-1.html`, `mockups/start-page-1.html`, `mockups/mode-select-1.html`, `mockups/input-page-1.html`, `mockups/result-page-1.html`, `mockups/letter-page-1.html`. Skissene har knapper for PC, nettbrett (768 px) og mobil (375 px), og oppsettet følger den ekte bredden.

## Elevation & Depth

Dybde kommer fra en **myk, farget skygge**: `0 8px 24px rgba(162, 62, 108, 0.14)`, altså bringebær med lav styrke. Den brukes på kort, felt, skjemaer, brevet og vinduer.

- Når man holder over et modus-kort, blir skyggen sterkere: `0 12px 30px rgba(162, 62, 108, 0.22)`.
- Knapper får skyggen bare når man holder over dem.
- Vinduer legger et mørkt slør over siden: `{colors.text}` med 45 % styrke.
- Ventetegnet dekker siden med `{colors.background}` med 94 % styrke.

### Bevegelse

Visuelle regler. Når og hvorfor ting beveger seg, står i `EXPERIENCE.md`. Fyrverkeriet, prosentlinjen som fylles og ikonet på modus-kortet som vipper, kuttes først hvis tiden blir knapp (se UX-kuttliste i `EXPERIENCE.md`).

| Hva | Bevegelse |
|---|---|
| Knapper, hover | Løfter seg 2 px og får skygge. 0,15 s, `ease`. |
| Knapper, trykk | Krymper til 96 %. |
| Modus-kort, hover | Løfter seg 4 px, rammen blir `{colors.primary}`, ikonet vipper (−8°) og blir 10 % større (0,3 s). |
| Modus-kort, trykk | Krymper til 97 %. |
| Søppelbøtte, hover | Blir 15 % større. |
| Ventetegn | Tre prikker (16 px) som hopper 14 px, 1 s per hopp, uendelig, med 0,15 s forsinkelse mellom prikkene. Farger: `{colors.primary}`, `{colors.dot-middle}`, `{colors.accent}`. |
| Prosentlinjen | Fylles fra 0 til Z % på 1 s når resultatsiden åpnes. |
| Vinduer, «i»-boks, filnavn etter opplasting | Toner inn på 0,15–0,2 s. |
| ATS-pila (▾) | Snur seg 180° når forklaringen åpnes. |
| Fyrverkeri | Rundt overskriften på brevsiden. Nye utbrudd i ca. 2,2 s, og alt er borte etter ca. 3,2 s. Høyst 3 utbrudd i sekundet. Utbruddene kommer på venstre og høyre side av overskriften, ligger bak teksten og dekker aldri brevet. Ingen blinking mer enn tre ganger i sekundet. |

**Redusert bevegelse:** Ved `prefers-reduced-motion: reduce` slås *alle* animasjoner og overganger av. Fyrverkeriet vises ikke, prosentlinjen står ferdig fylt, prikkene står stille.

## Shapes

Runde, myke former fra temaet «Myk fersken».

- `{rounded.lg}` (26 px): knapper, kort, felt, skjemaer, vinduer, ATS-forklaringen.
- `{rounded.md}` (18 px): feilboksen, gap-listene, brevet, forklaringen i Korrektur.
- `{rounded.sm}` (14 px): tekstboksen, filnavnet etter opplasting, «i»-boksen. Også tekstfeltene i skjemaene, skjemafeilen og merkelappene «Testmodus» og «Laget av KI» (13, 12 og 10 px i skissene er rundet til 14 px).
- `{rounded.xs}` (8 px): prosentlinjen, den gamle setningen.
- `{rounded.full}`: «i»-ikonet (sirkel) og bryteren.

## Components

Atferd (hva som skjer når man trykker) står i `EXPERIENCE.md` under Component Patterns.

### Knapper

- **Hovedknapp (`button-primary`)** — `{colors.primary}` fylt, hvit tekst, `{rounded.lg}` hjørner. «Logg inn», «Registrer deg», «Sjekk CV-en min», «Lag søknadsbrevet mitt», «Last ned som Word/PDF», «Last opp PDF», «Prøv på nytt», «Ja, lag nytt forslag», «Lag ny søknad». Låst knapp: 55 % synlig, ingen bevegelse.
- **Sekundærknapp (`button-secondary`)** — hvit med bringebærfarget ramme og tekst. «Tilbake», «Lim inn tekst», «Avbryt», «Logg ut».
- **Stor knapp (`button-hero`)** — «Begynn å lage søknad». Den største knappen på startsiden. På PC ca. 1,5 ganger vanlig skrift med god luft (`{components.button-hero.padding}`). På mobil 1,25rem og hele bredden.
- **Nedlastet-knapp (`button-done`)** — nedlastingsknappen etter nedlasting: grønn, med «✓ Lastet ned som Word» / «✓ Lastet ned som PDF».
- **Lenkeknapp (`link-button`)** — understreket bringebærfarget tekst uten ramme. «Nytt forslag», «Bli her», «Registrer deg her», «Logg inn».
- **Modus-kort (`mode-card`)** — hvitt kort med stort ikon (✨ eller ✏️, 2,4rem), modusnavnet med små store bokstaver i `{colors.text-muted}` («FULL GENERERING»), handlingen i fet, bringebærfarget 1,25rem («Skriv nytt brev») og en kort forklaring. Hele kortet er en knapp.

### Skjema og felt

- **Tekstfelt (`text-input`)** — etikett over feltet, ramme `{colors.primary}`, rød ramme ved feil, fet feiltekst i `{colors.error}` under feltet. Hjelpetekst («Minst 8 tegn») i `{colors.text-muted}`.
- **Avkrysningsboks (`checkbox`)** — samtykket på startsiden. 22 × 22 px, ramme og hake i `{colors.primary}`. Ved feil får selve avkrysningsboksen en rød ramme (2 px `{colors.error}` med 2 px avstand), som i skissen.
- **Innleggingsfelt (`upload-field`)** — hvitt kort med ikon og feltnavn (📄 CV, ✉️ Ditt søknadsbrev, 📢 Stillingsannonse), en kort forklaring og to knapper side om side: «Last opp PDF» (hoved) og «Lim inn tekst» (sekundær). Ved feil får feltet rød ramme, og feilteksten står i `{colors.error}` under feltnavnet (den samme teksten som i feilboksen).
- **Tekstboks** — ca. 160 px høy på PC og 200 px på mobil, kan dras større. Søppelbøtta står over den, til høyre for «Lim inn teksten her».
- **Filnavn (`file-chip`)** — grønn stripe med ✓, filnavnet (kuttes med «…» hvis det er langt) og søppelbøtte-ikonet 🗑️ til høyre.
- **Søppelbøtte (`trash-button`)** — 🗑️ uten ramme eller bakgrunn. Trykkflaten er minst 24 × 24 px (WCAG 2.5.8), og den har fokusring.
- **Hjelpetekst for testdata** — hvit boks med stiplet bringebærfarget ramme: «Testmodus: bruk filene i mappen `testdata/` i prosjektet.»

### Feil

- **Feilboks (`error-box`)** — rosa boks med rød ramme og rød tekst, øverst på siden. Fet overskrift og en liste med feilene. Hver linje i listen er en lenke til feltet med feilen. KI-feil bruker den samme boksen med en «Prøv på nytt»-knapp.
- **Skjemafeil (`form-error`)** — mindre rød boks over skjemaet på innloggingen: «Feil e-post eller passord», «Du må logge inn først».

### Merkelapper og hjelp

- **«i»-ikon (`info-icon`) og «i»-boks (`info-tip`)** — liten sirkel med «i» (ikke utropstegn, fordi «i» er mindre skremmende). Boksen er mørk (`{colors.text}`) med hvit tekst og runde hjørner.
- **Testmodus-bryter (`testmode-toggle`)** — bryter oppe til høyre på startsiden, med teksten «Testmodus». Låst bryter er 60 % synlig.
- **Merkelapp «Testmodus» (`testmode-badge`)** — liten ferskenfarget merkelapp oppe til høyre på de andre sidene.
- **Merket «Laget av KI» (`ai-tag`)** — liten ferskenfarget merkelapp ved overskriften «Gap-analyse».

### Resultat

- **Gap-lister (`gap-covers`, `gap-work-on`)** — to bokser. «Dette dekker CV-en din» er grønn med ✓ foran hvert punkt. «Dette kan du jobbe videre med» er varm ferskenfarget med → foran hvert punkt.
- **Nøkkelordtreff (`score-meter`)** — «X av Y = Z %» stort og bringebærfarget, med «av nøkkelordene står i CV-en din» ved siden av. Under: prosentlinje 12 px høy. Under den to lister: «Står i CV-en (antall)» med ✓ i grønt og «Står ikke i CV-en (antall)» med ○ i dempet farge.
- **ATS-forklaring** — hvit boks med overskriften «Hva er ATS og hva betyr det for deg?» i bringebær og en ▾ til høyre.

### Brev og Korrektur

- **Brevet (`letter-card`)** — hvitt ark med skygge, høyst `{components.letter-card.maxWidth}` bredt, god luft rundt teksten (`{spacing.6}` × `{spacing.7}` på PC, `{spacing.4}` på mobil).
- **Endret setning (`changed-sentence`)** — lys grønn bakgrunn og 2 px grønn understreking. Teksten har vanlig tekstfarge (`{colors.text}`), ikke grønn. Mørkere grønn når den er åpen. Den gamle setningen (`old-sentence`) står under, med en strek til venstre og overskriften «DU SKREV».
- **Forklaring i Korrektur** — liten hvit boks over brevet: «Grønn og understreket = endret. Trykk på setningen for å se det du skrev.»

### Ramme rundt sidene

- **Vindu (`dialog`)** — hvitt, sentrert, høyst 420 px bredt, med mørkt slør bak. Overskrift, tekst og knapper på rad. Brukes til de tre vinduene: etter nedlasting, «Nytt forslag» og «Logg ut før nedlasting».
- **Ventetegn (`wait-overlay`)** — dekker siden. Tre hoppende prikker, «På vei mot ny jobb» stort i bringebær (`{typography.wait-title}`), og en ventetekst under i `{colors.text-muted}`.
- **Hjørnerad (`corner-row`)** — festet til bunnen av skjermen på hver side etter innlogging, med bakgrunn `{colors.background}` og en tynn strek `{colors.border}` øverst, så innholdet ikke synes gjennom raden. På lave skjermer (under ca. 500 px høyde) står raden nederst på siden i stedet (se `EXPERIENCE.md`). I raden: KI-merknaden «ⓘ Teksten behandles av ekstern KI» til venstre (`{typography.caption}`, dempet) og en liten «Logg ut»-knapp (sekundær, liten) til høyre.
- **Fokusring** — 3 px heltrukket `{colors.focus-ring}` med 2 px avstand, på alt man kan trykke på.

## Do's and Don'ts

| Gjør | Ikke gjør |
|---|---|
| Bruk tokens for alle farger, slik at mørk modus kan legges til senere | Skriv fargekoder rett i koden |
| Systemskrift overalt | Baloo 2 andre steder enn i logoen og «På vei mot ny jobb» |
| Hele logoen på én linje, også på 375 px, ved vanlig tekststørrelse | La logoen brytes over to linjer ved vanlig tekststørrelse |
| La tekst bryte linjen når den blir større enn det er plass til | `nowrap`, eller faste høyder på knapper, merkelapper og bokser med tekst |
| Rød bare for feil | Rød på «Dette kan du jobbe videre med» (det er ikke en feil) |
| Vis feil med tekst og ramme, ikke bare farge | Bare rød farge som tegn på feil |
| Vis endringer i Korrektur med understreking *og* farge | Bare farge |
| Små, raske animasjoner (under 0,3 s) på knapper og kort | Lange eller store animasjoner som tar oppmerksomheten fra innholdet |
| Fyrverkeri rundt overskriften, bak teksten | Fyrverkeri over brevet, eller blinking mer enn tre ganger i sekundet |
| Slå av alle animasjoner ved redusert bevegelse | Animasjoner som ikke kan slås av |
| «i» i en sirkel for forklaringer | Utropstegn (virker skremmende) |
| Ikoner som pynt, skjult for skjermlesere | Ikoner som eneste forklaring |
| Kall det en nettside | Ordet «app» |
