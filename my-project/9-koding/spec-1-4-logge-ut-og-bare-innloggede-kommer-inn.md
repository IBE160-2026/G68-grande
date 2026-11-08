---
title: 'Story 1.4: Logge ut, og bare innloggede kommer inn'
type: 'feature'
created: '2026-11-08'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'e1bbf9d50d0c0c24fefba3acf61eb1f3f442e98f'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** En innlogget student kan ikke logge ut, og en som ikke er logget inn, sendes til innloggingen uten å få vite hvorfor (FR-6, FR-7).

**Approach:** «Logg ut» står i hjørneraden nederst på alle sider etter innlogging. Den sletter økten i minnet og sender til innloggingen. Alle sider unntatt innlogging, registrering og static sender den som ikke er logget inn, til innloggingen med «Du må logge inn først» i skjemafeil-boksen, som får fokus.

## Boundaries & Constraints

**Always:**
- «Logg ut» er en knapp i et `<form method="post">` mot `POST /logg-ut` (endepunkt `web.logg_ut`, med `login_required`). Ingen JavaScript. Utloggingen sletter `Innlogging` fra øktlageret og tømmer cookien, og sender så til `/logg-inn` uten melding.
- Hjørneraden står i `<footer>` i `base.html` og vises bare når brukeren er logget inn. Knappen står til høyre (plass til KI-merknaden til venstre i Epic 4). Den er en liten sekundærknapp: hvit, ramme og tekst i `--primary`, med hover, trykk og fokusring som hovedknappen.
- Raden er festet nederst på skjermen (`position: sticky; bottom: 0`), med `--background` og en tynn strek i `--border` øverst. `html` får `scroll-padding-bottom` omtrent like høy som raden. Under 500 px skjermhøyde står raden nederst på siden i stedet (`position: static`, ingen `scroll-padding-bottom`). Ingen faste høyder.
- Ikke innlogget (ingen cookie, ukjent økt-id eller økt borte etter omstart): cookien tømmes, og brukeren sendes til `/logg-inn?ikke_innlogget=1`. Der vises «Du må logge inn først» i skjemafeil-boksen med `autofocus`, slik «Feil e-post eller passord» gjør i dag. Teksten ligger i `tekster.py`. Cookien får aldri annet enn økt-id-en, så meldingen går i adressen.
- Sider med `login_required` sendes med `Cache-Control: no-store`, så tilbakeknappen etter utlogging ikke viser en gammel side.
- Innlogging etter meldingen gir startsiden som før (`next=` brukes ikke).

**Never:**
- Ingen `flash` eller annet i cookien. Ingen automatisk utlogging. Ingen melding etter utlogging.
- Ingen `Soknad` ennå (Epic 2). Ingen KI-merknad i raden (Epic 4). Ingen vindu «Logg ut før nedlasting» (Epic 7).
- Ingen nye avhengigheter, ingen CSRF. Testene skriver aldri til den ekte `backend/instance/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Logge ut | innlogget, `POST /logg-ut` | 302 til `/logg-inn`, økten borte fra lageret, `okt_id` ikke i cookien | N/A |
| Etter utlogging | `GET /` med samme klient | 302 til `/logg-inn?ikke_innlogget=1` | N/A |
| Ikke innlogget | `GET /` uten cookie | 302 til `/logg-inn?ikke_innlogget=1`, siden der viser meldingen med fokus | N/A |
| Etter omstart | gyldig cookie, økten ikke i minnet | Som «Ikke innlogget», og cookien tømmes | N/A |
| Logg ut uten økt | `POST /logg-ut` uten innlogging | 302 til `/logg-inn?ikke_innlogget=1` | Ingen feil |
| `GET /logg-ut` | hvem som helst | 405 | N/A |
| Melding + feil innlogging | POST fra siden med meldingen, feil passord | Bare «Feil e-post eller passord» | N/A |
| Innloggingen vanlig | `GET /logg-inn` | Ingen skjemafeil-boks, ingen hjørnerad | N/A |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/innlogging.py` -- `OKT_ID`, `oktlager()`, `gjeldende_innlogging()`, `login_required`, `logg_inn_bruker`. Legg til `logg_ut_bruker()` (slett i lageret + `session.clear()`, med kommentar om at `Soknad` slettes her fra Epic 2). `login_required` endrer redirect og setter `Cache-Control`.
- `backend/soknad/adaptere/oktlager.py` -- `slett(okt_id)` finnes og tåler `None`. Ikke endre.
- `backend/soknad/web/ruter.py` -- `felles_tekster` (context processor) kan også gi `innlogget`. `logg_inn` GET og `_vis_skjema` (fokus: første feltfeil, ellers `"skjemafeil"`) må kunne vise meldingen som skjemafeil.
- `backend/soknad/web/templates/base.html` -- `<footer class="bunn">` er tom. Hjørneraden legges inn der.
- `backend/soknad/web/templates/logg_inn.html` -- skjemafeil-boksen (`#skjemafeil`, `tabindex="-1"`, `autofocus`) finnes og gjenbrukes uendret.
- `backend/soknad/web/static/css/stil.css` -- bare `var(--…)` utenfor `:root` (testen `test_ux_dr1_*`), ingen `nowrap`, ingen `height: <tall>`. `.hovedknapp` viser hover/trykk/låst. `prefers-reduced-motion`-blokken må også dekke den nye knappen.
- `backend/tests/web/test_innlogging.py` -- `logg_inn`, `tagger_i`, `med_autofocus`, `er_innlogget`. `test_fr6_fr7_ingen_utlogging_ennaa` fjernes. `test_fr7_startsiden_uten_okt_...` og `test_fr7_gammel_cookie_...` venter `/logg-inn` og må endres.
- `backend/tests/conftest.py` -- `app`, `client`, `innlogget_client`.
- Skissen `_bmad-output/planning-artifacts/ux-designs/ux-kode-prosjekt-2026-10-20/mockups/start-page-1.html` (`.corners`, `.logout`) viser raden. DESIGN.md `corner-row` og `button-secondary` gjelder ved konflikt.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/web/tekster.py` -- `LOGG_UT_KNAPP = "Logg ut"`, `MA_LOGGE_INN = "Du må logge inn først"`.
- [x] `backend/soknad/web/innlogging.py` -- `logg_ut_bruker()`, ny redirect og `Cache-Control: no-store` i `login_required`.
- [x] `backend/soknad/web/ruter.py` -- `POST /logg-ut`, `innlogget` i context processoren, meldingen på `GET /logg-inn` når `ikke_innlogget` finnes i adressen.
- [x] `backend/soknad/web/templates/base.html` -- hjørneraden med skjemaet og knappen i `<footer>`, bare når innlogget.
- [x] `backend/soknad/web/static/css/stil.css` -- hjørneraden, `.sekundaerknapp` (tokens fra `button-secondary`) med en liten variant, `scroll-padding-bottom`, `@media (max-height: 500px)`, redusert bevegelse.
- [x] `backend/tests/web/test_utlogging.py` (ny) -- matrisen over, hjørneraden (bare innlogget, `footer` har skjemaet med `method="post"` og `action="/logg-ut"`, én knapp «Logg ut»), meldingen med `autofocus` på `#skjemafeil`, `Cache-Control`, og CSS-reglene (sticky, bottom, scroll-padding, max-height 500px).
- [x] `backend/tests/web/test_alle_sider.py` (ny, NFR-9/FR-7) -- går gjennom `app.url_map.iter_rules()` unntatt `web.logg_inn`, `web.registrer` og `static`, sender hver metode (uten HEAD og OPTIONS) uten innlogging og venter 302 til `/logg-inn?ikke_innlogget=1`. Argumenter i adressen får en eksempelverdi, og testen feiler hvis den ikke kan lage en. Den sjekker også at `web.start` og `web.logg_ut` var med.
- [x] `backend/tests/web/test_innlogging.py` -- fjern `test_fr6_fr7_ingen_utlogging_ennaa`, rett de to `test_fr7_*` til den nye adressen.

**Acceptance Criteria:**
- Given innlogget, when en side vises, then har `footer` «Logg ut», og alt kan nås med tastatur med synlig fokusring.
- Given utlogget med «Logg ut», when brukeren logger inn igjen, then kommer brukeren til startsiden med en ny økt-id.
- Given siden i nettleseren ved 375 og 1280 px, then ruller ingenting sidelengs, og raden dekker ikke innhold eller felt med fokus.

## Implementation Notes

- Etter implementeringen: 129 tester (110 før), `ruff check` og `ruff format --check` grønne.
- Footeren får klassen `hjornerad` og skjemaet med «Logg ut» bare når brukeren er innlogget. Ellers er den tom som før.
- `html` har `scroll-padding-bottom: 4.5rem` (raden er ca. 3,6rem høy). Under 500 px skjermhøyde er den 0.
- `test_alle_sider.py` lager eksempelverdier etter type, og `any(...)` får den første verdien i alfabetisk rekkefølge.
- Etter gjennomgangen (6 rettelser): 132 tester, `ruff check` og `ruff format --check` grønne.
- KI-en har ikke prøvd sidene i nettleseren, fordi sidene etter innlogging krever en innlogget økt. Kristine sjekker 375 og 1280 px.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-08), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | En innlogget som går tilbake til `/logg-inn?ikke_innlogget=1` (tilbakeknappen rett etter innlogging), ser «Du må logge inn først» og «Logg ut» samtidig | blind, grensetilfeller | low | Riktig: `logg_inn` GET sjekker ikke om brukeren er innlogget. Tilbake etter innlogging er vanlig. Meldingen vises nå bare når ingen er innlogget | patch |
| 2 | Meldingen vises for alle verdier av `ikke_innlogget` (`=0`, tom) | blind, grensetilfeller | low | Riktig. Sjekken er nå `== "1"`, samme verdi som `login_required` sender | patch |
| 3 | Ingen test av at en gammel cookie (økten borte) ikke gir hjørneraden på innloggingen og registreringen | testhull | low | Riktig: alle testene med gammel cookie går gjennom `login_required`, som tømmer cookien først. Ny test | patch |
| 4 | `test_alle_sider.py` bruker Werkzeugs private `regel._converters` | blind | low | Riktig, og det finnes ingen offentlig måte. En kommentar forklarer hvorfor | patch |
| 5 | `justify-content: flex-end` gjør det samme som `margin-left: auto` på skjemaet | blind | low | Riktig. Bare `margin-left: auto` virker når KI-merknaden kommer til venstre i Epic 4. Linjen er slettet | patch |
| 6 | `logg_ut` mangler docstring | blind | low | Riktig, de andre nye funksjonene har det. Én linje lagt til | patch |
| 7 | README sier ikke at CSRF mangler | blind, grensetilfeller | medium | Arkitekturgjennomgangen (`review-rubric.md` linje 135) sier at README skal nevne det. Det gjelder hele nettsiden, ikke bare denne storyen, og README skrives ferdig i story 8.1 | defer |
| 8 | `scroll-padding-bottom` er satt på alle sider og er en fast verdi | blind | low | Raden er ca. 3,6rem, under 4,5rem, også med zoom (rem vokser med). På innloggingen gjør den ingen synlig forskjell. Raden kan bli to linjer først med KI-merknaden i Epic 4 | avvist |
| 9 | Testen som går gjennom alle sidene, sjekker ikke gammel cookie og `no-store` per side | blind | low | Gammel cookie og ingen cookie går gjennom samme kode (`gjeldende_innlogging()` gir None). `no-store` settes i `login_required` selv, så alle sider med den får det | avvist |
| 10 | Testene henter hjelpere fra en annen testfil | blind | low | Samme som funn 7 i story 1.3: virker på Linux og Windows med `pythonpath = ["."]` | avvist |
| 11 | `html.count("Logg ut") == 1` brekker når flere «Logg ut»-knapper kommer | blind | false | Testen gjelder startsiden. De andre «Logg ut»-knappene (vinduene i Epic 3 og 7) står på brevsiden | avvist |
| 12 | Den lille knappvarianten `.liten` testes ikke | blind | low | Bare utseende, og den vises i nettleseren. Samme vurdering som testene av CSS-tekst i story 1.3 | avvist |
| 13 | `logg_ut` og tester nevner ikke AD-9-valget | blind | low | Står i Design Notes i spec-en. Ingen feil å rette | avvist |
| 14 | Dobbeltklikk på «Logg ut» eller utlogging i en annen fane gir «Du må logge inn først» | grensetilfeller | low | Bestemt i spec-ens låste del (raden «Logg ut uten økt»). Brukeren er logget ut uansett | avvist |
| 15 | `render_template` utenfor en forespørsel feiler i context processoren | grensetilfeller | false | Ingen kode lager maler utenfor en forespørsel, og ingen e-post eller jobber finnes i arkitekturen | avvist |
| 16 | Åpne sider vist mens man er innlogget, får ikke `no-store` | grensetilfeller | low | Krever at en innlogget åpner innloggingen, logger ut og så trykker tilbake. Etter funn 1 er det enda sjeldnere. Rettingen trenger en ny hook | avvist |
| 17 | Andre nettsider kan logge brukeren ut (CSRF, `SameSite` ikke satt) | grensetilfeller | low | CSRF står under «Never» i spec-en og er utsatt i arkitekturen. Nettsiden kjører bare lokalt, og å bli logget ut er ufarlig. README-delen er funn 7 | avvist |
| 18 | `regel.build` kan gi None for regler med host eller subdomene | grensetilfeller | low | Ingen slike regler finnes. Testen ville feilet tydelig på den regelen | avvist |
| 19 | Ruter med `redirect_to` ville feilet med 308 | grensetilfeller | false | Ingen slike ruter finnes, og en tydelig feil er riktig: da må testen vurderes | avvist |

## Design Notes

Meldingen er ikke en `InndataFeil` (AD-9 har ingen type for den), så `_vis_skjema` får en valgfri skjemafeil-tekst i stedet for en ny `FeilType`. Context processoren kaller `gjeldende_innlogging()`, så raden kommer automatisk på sider fra senere epics.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alle tester grønne
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Kristine logger inn, ser «Logg ut» nede til høyre, logger ut, trykker tilbake i nettleseren, og åpner `http://127.0.0.1:5000/` uten å være logget inn.
