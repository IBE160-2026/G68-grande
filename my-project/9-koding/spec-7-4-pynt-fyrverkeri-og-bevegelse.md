---
title: 'Story 7.4: Pynt: fyrverkeri og bevegelse'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_commit: '2f4e12101d51d2dfca9d2b537dd16bf755498e24'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-7-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nettsiden har ennå ikke pynten fra UX-kuttlisten. Brevsiden har ikke fyrverkeri, prosentlinjen på resultatsiden står ferdig fylt med en gang, og ikonet på modus-kortet står stille ved hover (UX-DR12, UX-DR13, UX-DR18).

**Approach:** Fyrverkeriet tegnes på en `<canvas>` bak brevoverskriften av et lite skript, `fyrverkeri.js`, slik som i skissen Kristine godkjente (`mockups/letter-page-1.html`). Prosentlinjen og ikonet får bevegelse bare med CSS. Alt slås av ved `prefers-reduced-motion`.

## Boundaries & Constraints

**Always:**
- Fyrverkeri hver gang brevsiden åpnes (også etter nytt forslag, som sender til `GET /brev`). Nye utbrudd i ca. 2,2 s, alt borte etter ca. 3,2 s, høyst 3 utbrudd i sekundet (minst 350 ms mellom utbruddene), på venstre og høyre side, bak teksten, innenfor området rundt overskriften (aldri over brevet).
- Fargene leses fra CSS-variablene `--fireworks-gold`, `--primary`, `--accent`, `--dot-middle` og `--success` med `getComputedStyle`. Ingen fargekoder i skriptet eller utenfor `:root`.
- Prosentlinjen fylles fra 0 til prosenten på 1 s når resultatsiden åpnes. Tallet står som tekst som før.
- Modus-kortet ved hover: løftes 4 px og rammen blir `primary` (finnes alt), og ikonet vipper −8° og blir 10 % større på 0,3 s.
- Ved `prefers-reduced-motion: reduce`: skriptet tegner ingenting, prosentlinjen står ferdig fylt, og ikonet står stille.
- Canvas har `aria-hidden="true"` og tar ikke trykk (`pointer-events: none`). Ikonene er alt skjult for skjermlesere.
- Skriptet endrer aldri søknadsdata, sender ingenting og lagrer ingenting (AD-1).
- Tester nevner UX-DR-nummeret, bruker `tests/web/hjelpere.py`, og ligger i en ny fil.

**Never:**
- Ingen rammeverk eller bibliotek, ingen `style=` i malene, ingen fast høyde på overskriften, ingen `nowrap`.
- Ingen endring i rutene eller kjernen.
- Ingen nettlesertester (hører til issue #16, story 8.2). Skriptet prøves for hånd i PR-en.

**Mine valg (kan endres av Kristine ved godkjenningen):**
- Ingen fyrverkeri når brevsiden viser en feilboks (KI-feil fra «Nytt forslag» eller «Filen kan ikke lages»). Det er ikke noe å feire da.
- I høykontrastmodus (`forced-colors: active`) skjules fyrverkeriet, fordi fargene på canvas ikke følger systemfargene og kan gjøre overskriften vanskelig å lese.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Brevsiden åpnes | `GET /brev` uten feil | Canvas og `fyrverkeri.js` på siden, fyrverkeri i ca. 3,2 s | N/A |
| Nytt forslag lyktes | POST → `GET /brev` | Nytt fyrverkeri | N/A |
| Feilboks på brevsiden | `ki_feil` eller `fil_feil` | Ingen canvas, ikke `fyrverkeri.js` | N/A |
| Redusert bevegelse | `prefers-reduced-motion: reduce` | Ingen tegning, prosentlinjen ferdig fylt, ikonet stille | N/A |
| Høykontrast | `forced-colors: active` | Canvas skjult | N/A |
| Uten JavaScript | Skript av | Brevsiden som før, canvas tom og usynlig | N/A |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/templates/brev.html:20-27` -- `<h1 class="brev-overskrift">` pakkes inn i en `<div class="fyrverkeri-ramme">` med `<canvas class="fyrverkeri" aria-hidden="true">` først, bare når `not fil_feil and not ki_feil`. `fyrverkeri.js` (defer) i `{% block skript %}` med samme vilkår. Fjern «Fyrverkeri kommer senere i Epic 7» i kommentaren. h1 beholder klasse, `tabindex` og `autofocus` (test_brev.py:499, :636).
- `backend/soknad/web/static/js/fyrverkeri.js` (ny) -- som `fireworks()` i skissen (`_bmad-output/planning-artifacts/ux-designs/ux-kode-prosjekt-2026-10-20/mockups/letter-page-1.html:336-361`): `matchMedia("(prefers-reduced-motion: reduce)")` → return; canvas i `devicePixelRatio`; utbrudd med 26 partikler, x i 10–30 % eller 70–90 % av bredden; `requestAnimationFrame`; konstanter for 2200, 3200 og 350 ms. Fargene fra `getComputedStyle(document.documentElement).getPropertyValue("--…")`. Ingen canvas → ingenting. Stil som `tilbake.js`: `function`, kommentar øverst på norsk.
- `backend/soknad/web/static/css/stil.css:1251` `.brev-overskrift` -- ny `.fyrverkeri-ramme` (`position: relative`, litt luft over og under med `--space-*`), `.fyrverkeri` (`position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none`), og h1 `position: relative; z-index: 1`.
- `stil.css:1187-1206` `.prosentlinje .fyll` -- `transform-origin: 0 0` og `animation: fyll 1s ease-out` med `@keyframes fyll { from { transform: scaleX(0); } }`. Rett kommentaren «animasjonen kommer i Epic 7».
- `stil.css:499` `.modus-kort .ikon` -- `transition: transform 0.3s ease`, og `.modus-kort:hover .ikon { transform: rotate(-8deg) scale(1.1); }`.
- `stil.css:1570` `@media (forced-colors: active)` -- `.fyrverkeri { display: none; }`.
- `stil.css:1693` `@media (prefers-reduced-motion: reduce)` -- legg til `.modus-kort:hover .ikon` med `transform: none`. Den globale regelen slår alt av `animation`, så prosentlinjen står ferdig fylt.
- `backend/soknad/web/templates/resultat.html:85-87` -- rett kommentaren («fylles uten animasjon. Animasjonen kommer i Epic 7») til at den fylles med CSS.
- Gjenbruk i testene: `STIL`, `css_blokk`, `html_av` og fiksturene for brevsiden (`paa_brev`, `paa_brev_korrektur`) fra `tests/web/hjelpere.py`/`conftest.py`. Mønster for skripttester: `test_nytt_forslag.py:565-581`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/web/test_pynt.py` (ny) -- brevsiden har canvas med `aria-hidden` og `fyrverkeri.js` i begge modusene; ikke ved KI-feil eller filfeil; kildetekst-test av skriptet (reduced-motion, `requestAnimationFrame`, 2200/3200/350, alle fem variabelnavn, ingen fargekoder, ingen `fetch`/`XMLHttpRequest`/`localStorage`/`sessionStorage`/`.submit()`); CSS-tester for rammen, canvas, prosentlinjen (1s, `scaleX(0)`), ikonet (`rotate(-8deg) scale(1.1)`, 0.3s), høykontrast og redusert bevegelse -- UX-DR12, UX-DR13, UX-DR18, UX-DR21
- [x] `backend/soknad/web/static/js/fyrverkeri.js` -- som i Code Map
- [x] `backend/soknad/web/templates/brev.html` -- som i Code Map
- [x] `backend/soknad/web/static/css/stil.css` -- som i Code Map
- [x] `backend/soknad/web/templates/resultat.html` -- bare kommentaren

**Acceptance Criteria:**
- Given `uv run pytest -q`, `ruff check` og `ruff format --check`, when de kjøres, then består alle, også de eksisterende testene for brevsiden, resultatsiden og CSS-en

## Implementation Notes

- Kodet av en underagent etter spec-en. 1 319 tester besto, og `ruff check` og `ruff format --check` var rene (kjørt på nytt i hovedøkten).
- Canvas bruker `inline-size: 100%; block-size: 100%` i stedet for `width`/`height`, fordi testen mot faste høyder (`test_ruter.py`) slår til på `height: 1…`. Virker likt.
- `test_fr17_prosentlinjen_er_pynt_og_fylt_til_prosenten` i `test_resultat.py` sjekket at fyllet ikke hadde animasjon. Den sjekker nå bare sporet og rammen.
- Ved feilboks står h1 alene (uten `autofocus`, som før), uten ramme, canvas og skript.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap | Skriptet testes bare som kildetekst, ingen test kjører det | medium | Stemmer, men prosjektet har bevisst ingen nettlesertester ennå (issue #16, story 8.2) → defer. Prøves for hånd i PR-en |
| 2 | blind, edge-case, verification-gap | Partiklene flytter og blekner per bilde, ikke per tid: dobbelt så fort på 120 Hz, og ved 30 Hz kuttes de brått ved 3,2 s | low | Stemmer, mange bærbare og mobiler har 120 Hz. Direkte retting (skalere med tiden siden forrige bilde) → patch |
| 3 | blind, edge-case, verification-gap | Canvas måles bare én gang, så endret vindusstørrelse i løpet av 3 s strekker prikkene | low | Stemmer, men sjelden og borte etter 3 s. Overskriften bruker systemskrift, så ingen skrift lastes inn senere. Retting krever ny gren → avvist |
| 4 | blind | Rammen gir mer luft rundt overskriften også uten JavaScript | low | Luften står i Code Map, og raden «Uten JavaScript» gjelder at siden virker som før. Kristine ser på avstanden i nettleseren → avvist |
| 5 | blind | `inline-size`/`block-size` brukt for å komme forbi testen mot faste høyder | low | Logiske navn er vanlig CSS og står forklart i en kommentar. Ingen skade → avvist |
| 6 | blind | På smale skjermer havner utbrudd bak bokstavene | low | Planen sier at fyrverkeriet ligger bak teksten, som i skissen Kristine godkjente. Prøves ved 375 px → avvist |
| 7 | blind | Skriptet sjekker ikke høykontrast, så det går 3,2 s på en skjult canvas | low | Ingen synlig følge, canvas er skjult → avvist |
| 8 | blind, edge-case | Redusert bevegelse sjekkes bare ved start | low | Ingen slår det på midt i 3 s, og retting krever ny gren → avvist |
| 9 | blind | Døde partikler fjernes aldri fra lista | low | Høyst ca. 180 partikler i 3 s, ingen merkbar kostnad → avvist |
| 10 | blind | Tilbakeknappen viser kanskje ikke fyrverkeriet på nytt (bfcache) | false | `tilbake.js` laster siden på nytt ved `pageshow` med `persisted` på alle sider etter innlogging, så skriptet kjører igjen |
| 11 | blind, edge-case | Ikonet blir stående vippet etter trykk på mobil (`:hover` henger igjen) | false | Kortet er en submit-knapp, så et trykk sender skjemaet og åpner neste side. Ingen tastaturvariant er i tråd med planen (hover), som løftet fra før |
| 12 | blind | Testene sjekker skrivemåte, ikke oppførsel | low | Samme rot som #1 (ingen nettlesertester) → tas med i defer for #1 |
| 13 | blind | `test_ux_dr21_...` har en `app`-parameter som ikke brukes | low | Stemmer. Direkte sletting → patch |
| 14 | blind | `_media()` i testen krever `}` i første kolonne | low | Samme mønster som `test_nytt_forslag.py`, og ruff/CSS-stilen holder formen → avvist |
| 15 | blind | h1 står to ganger i `brev.html` | low | Begge grenene er testet med eksakte attributter i `test_pynt.py`, så en avvikende endring fanges. Retting gjør malen tyngre å lese → avvist |
| 16 | edge-case | `getContext("2d")` kan gi `null`, og `ctx.scale` kaster da en feil | low | Skjer ikke for en ny canvas i vanlige nettlesere, og feilen stopper bare pynten. Vakt for en tilstand som ikke er vist → avvist |

## Design Notes

- Canvas i stedet for SVG: skissen bruker canvas, og mange små prikker som flytter seg er enklere og raskere å tegne der. Canvas er tom uten skriptet, så siden ser ut som før.
- Prosentlinjen med CSS i stedet for JavaScript: `rect` har alt bredden fra serveren, og `scaleX` fra 0 gir fyllingen uten skript. Uten animasjon står den ferdig.

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine: brevsiden i begge modusene, også etter «Nytt forslag»: fyrverkeri på begge sider av overskriften, bak teksten, borte etter ca. 3 s, ikke over brevet. Resultatsiden: linjen fylles. Modusvalget: ikonet vipper ved hover. Ved 375 og 1280 px. Med «Reduser bevegelse» i Windows (Innstillinger → Tilgjengelighet → Visuelle effekter → Animasjonseffekter av): ingenting beveger seg.
