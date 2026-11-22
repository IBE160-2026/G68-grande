---
title: 'Rettinger etter retro 8: «Lag ny søknad» sletter ikke brevet, og små rettinger i tekst og papirer'
type: 'bugfix'
created: '2026-11-22'
status: 'done'
baseline_commit: '620b5a6a91d483a9af86dd924c6b7c24c9764011'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-8-retro-2026-11-22.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Når alle KI-kallene er brukt, har feilboksen på resultatsiden og innleggingen lenken «Lag ny søknad» til `/`. Har søknaden et brev (for eksempel etter tilbakeknappen fra brevsiden), sletter ett trykk brevet uten spørsmål (retro 8, A1). Kommentarene i malene og ved `SameSite` stemmer ikke, teksten på brevsiden viser til en vei som ikke finnes, og noen papirer er ikke avstemt (A3–A7, B2–B5, C2).

**Approach:** Tiltak 1 og 2 i retro 8 i én runde med én branch (`retro-8-rettinger`) og én PR. Lenken vises bare når søknaden ikke har et brev (`ferdig_brev`), med test. Tekstene og papirene rettes i samme PR.

**Beslutninger (Kristine, 2026-11-22, retro 8):** én runde nå, før andre prøve fra en ny kopi. A1 rettes. A6 (egen tekst på brevsiden) og B5 (halv setning om 47 % under «Skjermbilder») er med, og Kristine godkjenner ordlyden. A2 trengs ikke. Ekte KI trengs ikke.

**Beslutninger (Kristine, 2026-11-22, denne runden):** Har søknaden et brev, får boksen på resultatsiden og innleggingen den samme teksten som på brevsiden og lenken «Gå til brevet» (klassen `hovedknapp`) til brevsiden i stedet for «Lag ny søknad». Teksten i boksen (brevsiden, og de to andre sidene med brev): «Du har brukt alle KI-kallene for denne søknaden. Last ned brevet, så kan du lage en ny søknad i vinduet etter nedlastingen.» Under «Skjermbilder» i README: «Ekte KI kan gi en litt annen nøkkelordliste enn fasiten, så prosenten på resultatsiden er 47 % her, mens testmodus gir 50 %.» Spec-en beholdes hel (ca. 2 300 tokens).

## Boundaries & Constraints

**Always:** Tester nevner FR-/NFR-/UX-DR-nummeret og bruker `tests/web/hjelpere.py`. Endringer i en plan i `_bmad-output/` kopieres til samme fil i `my-project/` (kopiene er like i dag, bortsett fra linjeskift). Kristines egne formuleringer endres ikke utover det rettingen trenger. Ingen `style=`, ingen nye fargekoder.

**Never:** Ingen endring i `kjerne/` eller i hvordan GET / lager en ny søknad (CSRF og POST for ny søknad hører til før nettsiden legges på nett, A5). Ingen nytt vindu. B6 (ZIP) hører til 8.2.2. B7–B10 og B1 godtas uten endring.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Resultat uten brev, alle kall brukt | ekte KI, 10 kall, ingen brev, POST `/resultat` | feilboks med `KI_KALL_BRUKT` og lenken til `/` (som i dag) | – |
| Resultat med brev, alle kall brukt | som over, men søknaden har et brev | brevteksten og «Gå til brevet» (`/brev`), ingen lenke til `/`; brevet er der fortsatt | – |
| Innlegging med brev, alle kall brukt | brev i søknaden, feltene uendret, «Sjekk CV-en min» | brevteksten og «Gå til brevet», ingen lenke til `/`; brevet er der fortsatt | – |
| «Gå til brevet» trykkes | GET `/brev` fra boksen | brevsiden med brevet, søknaden uendret | – |
| Innlegging, feltene endret | brev i søknaden, CV endret, ingen plass | brevet er alt slettet av `sett_inndata`, så lenken vises | – |
| Brevsiden, alle kall brukt | «Nytt forslag» uten plass | egen tekst om å laste ned brevet, ingen lenke (som i dag) | – |
| Korrektur | samme som over med `korrektur` i stedet for `brev` | samme regel (`ferdig_brev`) | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/web/ruter.py:593-626` -- `_vis_innlegging` får `har_brev=ferdig_brev(soknad) is not None` (som `_vis_resultat:645`). Docstringene `:593-597` og `:629-640` nevner regelen. `soknad` i `innlegging()` er søknaden etter `sett_inndata`, så endrede felt har alt slettet brevet.
- `backend/soknad/web/templates/resultat.html:42-60`, `innlegging.html:15-32` -- med brev: `KI_KALL_BRUKT_BREV` som overskrift og lenken «Gå til brevet» (`url_for('web.brev')`), uten brev: som i dag. Rett kommentarene («uten lenker», «uten knappen»).
- `backend/soknad/web/templates/brev.html:40-52` -- overskriften i boksen: ny tekst når `prov_pa_nytt` er usann. `ki_feil` settes i `_med_ki:527` til `tekster.KI_KALL_BRUKT`; enklest er at malen velger `tekster.KI_KALL_BRUKT_BREV` når `not prov_pa_nytt`, eller at `_vis_brev` bytter teksten. Velg det som ikke endrer `_med_ki`.
- `backend/soknad/web/tekster.py:426-429` -- nye `KI_KALL_BRUKT_BREV` og `GA_TIL_BREVET_KNAPP = "Gå til brevet"`.
- `backend/soknad/web/static/js/innlegging.js:93` -- `".feilboks a"` → `'.feilboks a[href^="#"]'` (A7), kommentaren også. Nødvendig nå: `href="/brev"` ville ellers gitt `getElementById("brev")`.
- `backend/soknad/__init__.py:70-71` -- kommentaren: Lax stopper skjemaer (POST) fra andre nettsider, ikke vanlige lenker (A4).
- Tester: `backend/tests/web/test_grenser.py:296-315` (resultat) og `:229-250` (innlegging): nye tester med brev (`brev=`/`korrektur=` i `Soknad`, se `hjelpere.py` og `test_nytt_forslag.py`), sjekk at `LENKE_NY_SOKNAD` ikke er i boksen og at brevet er uendret. `test_nytt_forslag.py:385-396`: overskriften er den nye teksten. Kildetekst-test for velgeren i `innlegging.js` hvis det finnes et mønster i `tests/web/`.
- `README.md:23` (B5), `:151` (A5: en vanlig lenke til `/` fra en annen nettside lager en ny søknad, og da er det som er lagt inn og brevet borte).
- `my-project/testplan.md:7` «FR-nummeret» → «FR- eller NFR-nummeret» (B4). «Hele flyten for hånd» (`:515-524`): rad for lenken fra PR #55 (22. november 2026, Kristine, ekte KI, grensen satt til 2 KI-kall i den kjøringen, uten brev, «ser bra ut»), og en rad «Ikke prøvd ennå» for denne rettingen.
- `my-project/testkjoringer/8-2/maling-5000/maal_korrektur.py:11-13` -- kommandoen med `PYTHONPATH=.` (Git Bash) og `$env:PYTHONPATH="."` (PowerShell) (B3).
- `_bmad-output/implementation-artifacts/spec-8-2-1-testplan-og-forste-prove.md:49` = `my-project/8-koding/…` -- `[ ]` → `[x]` (B4).
- `_bmad-output/planning-artifacts/epics.md:745` = `my-project/6-epics-og-stories/epics.md` -- «På innleggingen og resultatsiden har meldingen lenken …» får «når søknaden ikke har et brev» og datoen for retro 8.
- `…/ux-designs/ux-kode-prosjekt-2026-10-20/EXPERIENCE.md:278` = `my-project/3-ux/EXPERIENCE.md` -- raden «KI-feil»: meldingen om alle KI-kallene, lenken og brevregelen (C2).
- `my-project/README.md` (oversikten over spec-ene) -- rad for `spec-retro-8-rettinger.md`, som for retro 7.
- Sprint-status-kopien er alt lik originalen (B4, tredje punkt): ingen endring.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/web/tekster.py`, `ruter.py`, de tre malene -- lenke- og tekstregelen over -- A1, A3, A6
- [x] `backend/soknad/web/static/js/innlegging.js` -- strammere velger -- A7
- [x] `backend/tests/web/test_grenser.py`, `test_nytt_forslag.py` -- tester for hver rad i matrisen -- A1, A6
- [x] `backend/soknad/__init__.py` -- kommentaren -- A4
- [x] `README.md`, `my-project/testplan.md`, `maal_korrektur.py`, spec 8.2.1, `epics.md`, `EXPERIENCE.md`, `my-project/README.md` -- som i Code Map, i begge kopiene -- A5, B2–B5, C2

**Acceptance Criteria:**
- Given en søknad med brev og alle KI-kallene brukt, when brukeren er på resultatsiden eller innleggingen og får feilboksen, then finnes ingen lenke i boksen som sletter brevet, og brevet er uendret i søknaden.
- Given koden etter rettingen, when `uv run pytest`, `ruff check` og `ruff format --check` kjøres fra `backend/`, then består alt.

## Implementation Notes

- Teksten i boksen velges i malene, ikke i `_med_ki`: `resultat.html` og `innlegging.html` viser `KI_KALL_BRUKT_BREV` når `har_brev and not prov_pa_nytt`, og `brev.html` når `not prov_pa_nytt`. `_vis_innlegging` får `har_brev=ferdig_brev(soknad) is not None`, som `_vis_resultat`.
- `tests/web/test_vindu_logg_ut.py` (`test_ux_dr17_alle_kall_brukt_uten_nedlasting_spor_fortsatt`) sjekket den gamle teksten på brevsiden og er rettet til `KI_KALL_BRUKT_BREV`. Den var ikke nevnt i Code Map.
- På resultatsiden med brev har også «Avbryt» i vinduet «Vil du ha et nytt forslag?» `autofocus` (bare når vinduet åpnes), så testen venter `["feilboks", "nytt-forslag-avbryt"]`.
- Kildetekst-testen for velgeren i `innlegging.js` står i `test_innlegging.py`, ved de andre testene som leser skriptet (`JS`).
- Testene: 1 423 (1 416 + 7 nye).
- Etter gjennomgangen og nettleserprøven (22. november, «det virket»): Kristine valgte at det utsatte punktet om «Tilbake» på modusvalget (punkt 9 i triage-loggen) står i README under «Brevet kan slettes uten å spørre på tre måter», uten endring i koden.

## Spec Change Log

## Review Triage Log

Gjennomgang 1 (2026-11-22): blind, edge-case og verification-gap over `git diff 620b5a6` (spec-kopien tatt ut av diffen med vilje, den er påstandene). Verification-gap fant ingen hull.

| # | Lag | Funn | Dom | Bevis | Vei |
|---|-----|------|-----|-------|-----|
| 1 | blind | Spec-kopien mangler i diffen | false | Tatt ut med vilje som påstandsfila. `my-project/8-koding/spec-retro-8-rettinger.md` er lagt til (`git add -N`) og kommer med i committen | avvist |
| 2 | blind | Teksten velges ut fra `prov_pa_nytt`, ikke ut fra feilen | low | Eneste som gir `prov_pa_nytt=False`, er `_med_ki:527` med `KI_KALL_BRUKT`, og docstringene sier at `False` betyr akkurat den meldingen. Bare en framtidig kaller kan treffe det, og rettingen er et nytt flagg | avvist (low, mer enn en direkte retting) |
| 3 | blind | Ingen test for vanlig KI-feil når søknaden har brev | low | `test_fr28_ki_feil_paa_resultatsiden_beholder_brevet` sjekker bare knappene, ikke overskriften eller at «Gå til brevet» mangler | patch |
| 4 | blind, edge | «Endrede felt» bare i Full generering | low | `test_nfr11_endrede_felt_…` er ikke parametrisert som de to andre | patch |
| 5 | edge | `med_brev` mangler `nokkelord_annonse`, så docstringen («gap, for … listen er de samme») stemmer ikke | low | `okt.py:127`: listen beholdes bare når `nokkelord_annonse` er satt. Testen gikk analyse-veien | patch |
| 6 | blind | `med_brev` har parametre ingen bruker | low | `steg` og `ki_kall` settes aldri av kallerne | patch (sletting) |
| 7 | blind, edge | Teksten lover vinduet etter nedlastingen, men uten JavaScript kommer det ikke | low | Vinduet åpnes bare av `nedlasting.js`. Uten JavaScript hadde brevsiden ingen vei til startsiden fra før (bare «Logg ut»). Teksten er Kristines, og nesten alle har JavaScript på | avvist (low, uvanlig, rettingen trenger en `<noscript>`-gren) |
| 8 | edge | Brevsiden i Korrektur har ingen test for den nye teksten | low | Linjen i `brev.html` har ingen gren for modus, så Korrektur gir samme tekst | avvist |
| 9 | blind | «Tilbake» på modusvalget (`modus.html:17`, GET /) sletter et brev uten spørsmål | medium | Innlegging → «Tilbake» (feltene uendret, brevet beholdes) → modusvalget → «Tilbake» → GET / lager en ny søknad (`ruter.py:120`). Fantes før denne runden, og README nevner det ikke | defer |
| 10 | blind | «Last ned brevet» på sider uten nedlastingsknapp | false | Kristine godkjente ordlyden for alle tre sidene, med «Gå til brevet» ved siden av | avvist |
| 11 | blind | Testplan-radene kan ikke gjentas («skript i scratchpad») | low | Radene sier ikke hvilken konstant som ble endret | patch |
| 12 | blind | Tom dato i raden for retro 8 | false | Raden står som «Ikke prøvd ennå» til Kristine prøver | avvist |
| 13 | blind | Dobbelt punktum i `EXPERIENCE.md` («….».) | low | Raden «KI-feil» | patch (begge kopiene) |
| 14 | blind | PowerShell-kommandoen lar `PYTHONPATH` stå igjen | low | `$env:` gjelder resten av økten | patch |
| 15 | blind | Setningen i docstringen til `_vis_innlegging` er tung | low | «… sett_inndata, så er feltene endret, er brevet …» | patch |
| 16 | blind | README låser 47 % mot 50 % | false | Alternativteksten til bildet sier 47 %, og setningen er Kristines. Tas bildet på nytt, må begge endres uansett | avvist |

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består (1 416 + de nye)
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil
- `cd backend && PYTHONPATH=. uv run python -c "import soknad"` -- expected: ingen `ModuleNotFoundError` (B3, uten å kalle KI-en)

**Manual checks:**
- Kristine: nettsiden med grensen satt til 3 KI-kall (analysen 2 + brevet 1; skript i scratchpad, som i PR #55): lag brevet, tilbakeknappen til resultatsiden, «Lag søknadsbrevet mitt» → «Ja» i vinduet → feilboksen uten «Lag ny søknad», brevet finnes fortsatt. Det samme på innleggingen med feltene uendret. Til slutt «Nytt forslag» på brevsiden: den nye teksten.
