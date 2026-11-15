---
title: 'Story 5.3: Se hva som er endret i Korrektur'
type: 'feature'
created: '2026-11-15'
status: 'done'
baseline_commit: 'c9f1792af1740167047043964052623a17ad49cb'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-5-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Brevsiden i Korrektur viser bare det forbedrede brevet. Studenten ser ikke hvilke setninger KI-en har endret, eller hva hen skrev før, og kan ikke vurdere endringene (FR-23, UX-DR15).

**Approach:** Kjernen lager en visning av Korrektur-svaret: avsnittene med hver setning merket som endret eller uendret ut fra `ny` og `gammel` (AD-5), og antallet fjernede. Brevsiden viser endrede og nye setninger som grønne, understrekede knapper som åpner og lukker «Du skrev» med den gamle setningen, forklaringen over brevet og linjen om fjernede setninger under. Word-fila er som før, uten markeringer.

## Boundaries & Constraints

**Always:** En setning er endret når `gammel != [ny]` (ny når `gammel == []`), fjernet når `ny` er `null`, ellers uendret. Bare kjernen avgjør dette, aldri malen eller skriptet. Avsnittene på siden og i Word-fila kommer fra samme gruppering i kjernen, så teksten er lik. Alle tekster ligger i `tekster.py`. Skriptet endrer bare visningen (AD-1). Ingen `style=`, ingen faste høyder, og høykontrast (`forced-colors`) har ramme eller strek i `CanvasText` for de grønne setningene, «Du skrev» og forklaringsboksen. Hver test nevner FR-nummeret. Testene kaller aldri det ekte API-et.

**Never:** Ingen endring i Full generering, i promptene, i `kontroller()` eller i svarene i `testdata/`. Ingen ny sammenligning av tekst (heller ikke vask) i visningen. Ikke «Nytt forslag» eller fyrverkeri (Epic 7), ikke PDF (Epic 6/7).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Endret | `gammel: ["Jeg vil jobbe her"]`, `ny: "Jeg ønsker å jobbe her."` | grønn knapp med skjult «Endret setning». Trykk åpner «Du skrev» + den gamle, nytt trykk lukker | – |
| Slått sammen | `gammel` har to setninger | «Du skrev» viser begge, hver på sin linje | – |
| Ny | `gammel: []` | grønn knapp, «Du skrev» viser «(Ny setning)» | – |
| Uendret | `gammel == [ny]` | vanlig tekst, ingen knapp | – |
| Fjernet | 1 eller 2 setninger med `ny: null` | vises ikke. Under brevet: «1 setning er fjernet.» / «2 setninger er fjernet.» | – |
| Ingenting endret | alle uendret, ingen fjernet | «Vi fant ingenting å endre. Brevet ditt er bra som det er.» i stedet for forklaringen | – |
| Flere åpne | to knapper trykket | begge «Du skrev» er åpne | – |
| Word | «Last ned som Word» | fila = `korrigert_brev`, uten «Du skrev», «(Ny setning)», «Endret setning» eller forklaring | `FilFeil` som før |
| Bare fjernet | ingen endret, 1 fjernet | ingen forklaring over brevet, «1 setning er fjernet.» under | – |
| Full generering | modus Full generering | brevsiden som før, uten forklaring og uten skript for markeringene | – |

**Beslutning (Kristine, 2026-11-15):** er ingen setning grønn, men noen er fjernet, skjules forklaringen over brevet. Bare linjen om fjernede setninger står under brevet.

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/ki_svar.py:122` -- `korrigert_brev`. Del ut grupperingen i en hjelper som gir avsnitt som lister av setninger (samme regel for `nytt_avsnitt` og fjernet setning foran). Ny `korrektur_visning(korrektur) -> dict`: `avsnitt` (lister av `{"ny", "gammel", "endret"}`, bare setninger med `ny`), `fjernet` (antall `ny is None`), `endret` (antall markerte). `korrigert_brev` = hver gruppe satt sammen med ett mellomrom, uendret oppførsel.
- `backend/soknad/web/ruter.py:502` -- `_vis_brev`: i Korrektur sendes `visning=korrektur_visning(soknad.korrektur)`, ellers `None`. `brev()` og `last_ned()` bruker `ferdig_brev` som før. Rett docstringen.
- `backend/soknad/web/tekster.py:204` -- `KORREKTUR_FORKLARING`, `KORREKTUR_FORKLARING_SKJERMLESER = "Endrede setninger er knapper."`, `ENDRET_SETNING_SKJERMLESER = "Endret setning"`, `DU_SKREV = "Du skrev"`, `NY_SETNING = "(Ny setning)"`, `INGENTING_ENDRET`, `fjernet(antall)`.
- `backend/soknad/web/templates/brev.html:21-26` -- med `visning`: boksen `.korrektur-forklaring` over arket (eller «Vi fant ingenting …»), hver setning i `<p>` med ett mellomrom mellom, endret setning som `<button type="button" class="endret-setning" aria-expanded="false" aria-controls="du-skrev-A-S">` med `<span class="skjult">` først, og `<span class="du-skrev" id="du-skrev-A-S" hidden>` rett etter med «Du skrev» og én `<span>` per gammel setning. `<p class="fjernet-linje">` under arket når `fjernet > 0`. Skriptet lastes bare når `visning` finnes. Rett kommentaren om story 5.3. Uten `visning` er arket som før.
- `backend/soknad/web/static/js/endringer.js` (ny) -- som `info.js`: for hver `.endret-setning` bytter klikk `aria-expanded` og `hidden` på boksen i `aria-controls`. `<button>` gir klikk for Enter og mellomrom. Ingen Esc, ingen hover-åpning.
- `backend/soknad/web/static/css/stil.css:1198` -- etter `.brevark`: `.korrektur-forklaring` (hvit boks, høyst 720 px, i midten), `.endret-setning` (`font: inherit`, `color: var(--text)`, `background: var(--success-tint)`, 2 px understreking i `var(--success)`, ingen ramme, `text-align: left`, `:hover` og `[aria-expanded="true"]` med `var(--changed-active)`, `:focus-visible`-ring), `.du-skrev` (`display: block`, `var(--background)`, `var(--text-muted)`, 4 px strek til venstre, liten skrift, overskrift med store bokstaver) og `.du-skrev[hidden] { display: none; }` (`display: block` vinner ellers over `[hidden]` på L716). I `@media (forced-colors: active)` (L1385): ramme i `CanvasText` på `.endret-setning`, `.du-skrev` og `.korrektur-forklaring`, og tykkere ramme når den er åpen.
- Tester: `tests/kjerne/test_ki_svar.py:269-` (`korrektur_visning` for hver rad i matrisen, og at `" ".join` av hver gruppe er `korrigert_brev`), `tests/web/test_brev.py:565` (5.2.1-testen «uten markeringer» blir testen for markeringene, `avsnitt()` på L57 må hoppe over `.skjult` og `.du-skrev`), `tests/web/test_nedlasting.py:79` (fila uten markeringstekstene), CSS-test med `css_blokk` og forced-colors som `test_vindu_etter_nedlasting.py:209`, JS-test som `test_resultat.py:542`. `korrektur_svar()` og `KorrekturTestKI` i `tests/web/hjelpere.py:40-75` og fixturen `paa_brev_korrektur` gjenbrukes.
- Ikke endre: `ferdig_brev` (`kjerne/okt.py:155`), `fil_ut.lag_docx`, `_med_ki`, `info.js`, `prompts/`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/ki_svar.py` -- felles gruppering, `korrektur_visning`, `korrigert_brev` på grupperingen -- kjernen først, så siden og fila deler avsnittene
- [x] `backend/soknad/web/tekster.py`, `ruter.py` -- tekstene, `fjernet()` og `visning` til malen
- [x] `backend/soknad/web/templates/brev.html`, `static/js/endringer.js`, `static/css/stil.css` -- forklaringen, knappene, «Du skrev», linjen om fjernede, høykontrast
- [x] `backend/tests/...` -- én test per rad i matrisen, escaping av `ny` og `gammel`, unike id-er og `aria-controls`, tekstene i `tekster.py`, CSS og skriptet

**Acceptance Criteria:**
- Given brevsiden i Korrektur med minst én endret setning, when siden vises, then står forklaringen med den skjulte «Endrede setninger er knapper.» over brevet, og hver endret setning er en knapp med `aria-expanded="false"` og en lukket «Du skrev»
- Given brevsiden i Korrektur, when teksten i hvert avsnitt leses uten de skjulte tekstene og «Du skrev», then er den lik avsnittene i Word-fila
- Given `ny` eller `gammel` med `<script>`, when siden vises, then er teksten escapet

## Implementation Notes

- Implementert av en egen utvikler-agent ut fra spec-en. 1 027 tester besto, og ruff var uten feil før gjennomgangen.
- `[hidden] { display: none !important; }` fantes alt (L716), så `.du-skrev[hidden]` er ekstra, men skader ikke.
- `.fjernet-linje` har negativ toppmarg, så linjen står nær brevarket. Det er agentens valg, og Kristine ser på det i nettleseren.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | verification-gap, blind | `endringer.js` testes bare som tekst. At klikk åpner og lukker, og at flere kan være åpne, kjøres aldri | low | Stemmer, men repoet har ingen måte å kjøre JS i testene på, og det er praksisen for alle skriptene. Nettlesersjekken i Verification dekker åpne, lukke og flere åpne. Utsatt (deferred-work) |
| 2 | blind | Uten JavaScript gjør knappene ingenting | low | Stemmer, men det er bestemt i Design Notes og er likt «i»-boksene. Retting = ny reserveløsning. Avvist |
| 3 | blind, edge-case | En `<button>` brytes som en boks, så en lang endret setning begynner på ny linje | low | Stemmer, og står i Design Notes (som i skissen). `display: inline` hjelper ikke på en knapp. Kristine ser på det ved 375 px. Avvist |
| 4 | blind | Den skjulte «Endret setning » blir med når brukeren kopierer brevet fra siden | low | Stemmer: `.skjult` skjuler med `clip-path`, men teksten er markerbar. Direkte retting: `user-select: none` → patch |
| 5 | blind | «Du skrev» står over «(Ny setning)» | false | Slik står det i EXPERIENCE.md («Du skrev» viser «(Ny setning)»). Avvist |
| 6 | blind | `endret` er både sann/usann per setning og antallet øverst i visningen | low | Stemmer, lett å blande i malen. Direkte retting: `antall_endret` → patch |
| 7 | blind, edge-case | En tom `gammel` etter rensingen gir en tom linje i «Du skrev», eller en uendret setning blir grønn | low | Mulig bare hvis KI-en sender en tom tekst i `gammel`, og kontrollen godtar det. Ikke sett i noen svar. Retting = ny vakt. Avvist |
| 8 | edge-case | En fjernet oppføring med to gamle setninger gir «1 setning er fjernet.», og en med `gammel: []` telles som fjernet | low | Stemmer: det telles oppføringer, ikke setninger. Direkte retting: tell setningene i `gammel` → patch |
| 9 | blind | Negativ marg på `.fjernet-linje` avhenger av margen under brevarket | low | Bare utseende, og Kristine ser på siden i nettleseren. Avvist |
| 10 | blind | I høykontrast blir rammen 3 px når setningen åpnes, så teksten flytter seg litt | low | Stemmer, men bare 2 px i høykontrast, og det viser hvilken som er åpen. Avvist |
| 11 | blind | `avsnitt` brukes ikke av malen i Korrektur | false | `avsnitt` fra `ferdig_brev` brukes fortsatt til «uten brev» i `brev()` og til Word-fila. At siden og fila er like, er testet (`test_fr30_korrektur_med_markeringer_filen_er_lik_teksten_paa_siden`). Avvist |
| 12 | blind | Ingen test av markeringene på siden med feilboksen | low | Den samme `_vis_brev` lager markeringene, og `test_ad9_filfeil_i_korrektur_gir_brevsiden_med_feilboksen` viser brevet. Avvist |
| 13 | blind | `test_ki_svar.py` leser `eget-brev.txt` når fila lastes, ikke i testen | low | Fila er påkrevd av mange tester, og `test_testdata.py` passer på den. Avvist |
| 14 | blind | «overskriften» brukes om både h1 og første linje i brevet i én docstring | low | Stemmer. Direkte tekstretting → patch |
| 15 | blind | Docstringen sier at visningen aldri sammenligner vasket tekst | false | Det stemmer: `gammel != [ny]` sammenligner renset tekst, ikke vasket (`vask`). Avvist |

Funn 4, 6, 8 og 14 er rettet av utvikler-agenten: `user-select: none` på den skjulte teksten i knappen, `antall_endret`, fjernede telles som setninger i `gammel` (to nye tester), og docstringen. Etterpå: 1 029 tester besto, og ruff var uten feil. Funn 1 står i `deferred-work.md`.

## Design Notes

Knappen er en ekte `<button>`, som i skissen (`letter-page-1.html`) Kristine godkjente. En knapp brytes ikke over flere linjer som vanlig tekst, så en lang endret setning begynner på en ny linje. Det prøves i nettleseren (375 px). «Du skrev» viser `gammel` slik KI-en skrev den. Kontrollen godtar små forskjeller i tegnsetting og store bokstaver mot originalen (funn 6 i 5.2.1), og det godtas her. Uten JavaScript åpnes «Du skrev» ikke, som «i»-boksene.

```html
<p>Søknad på stillingen som junior utvikler</p>
<p><button type="button" class="endret-setning" aria-expanded="false" aria-controls="du-skrev-2-1"><span class="skjult">Endret setning </span>Jeg søker …</button><span class="du-skrev" id="du-skrev-2-1" hidden><span class="du-skrev-overskrift">Du skrev</span><span>Jeg vil søke …</span></span> Jeg har …</p>
```

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine prøver Korrektur i testmodus med case 1 til brevsiden ved 375 og 1280 px: grønne setninger, trykk åpner og lukker «Du skrev», flere åpne samtidig, «1 setning er fjernet.» under brevet. Med tastatur: Tab til en setning, Enter og mellomrom åpner og lukker, fokusringen synes. I høykontrast (Windows: venstre Alt + venstre Shift + Print Screen) synes setningene, «Du skrev» og forklaringsboksen. Word-fila har ingen markeringer. Full generering er som før.
