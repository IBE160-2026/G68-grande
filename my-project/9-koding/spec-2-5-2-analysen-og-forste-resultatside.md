---
title: 'Story 2.5.2: Analysen og første resultatside'
type: 'feature'
created: '2026-11-09'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '656a3436a75b8c7444147c369e84f4733f65e431'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Når alt er riktig på innleggingen, vises bare samme side på nytt. Brukeren får verken gap-analysen eller nøkkelordtreffet (FR-14, FR-15, FR-17, FR-21).

**Approach:** Uten feil henter «Sjekk CV-en min» nøkkelordlisten og gap-analysen fra `ki()` (`TestKI`), lagrer dem i søknaden og sender til en ny resultatside med overskriften, de to gap-listene og «X av Y = Z %». Dette er andre halvdel av story 2.5. Resten av resultatsiden («i»-ikoner, farger, nøkkelordlistene, ATS, «Tilbake») kommer i 2.6, og ventetegn og hele KI-feilen i 2.7.

## Boundaries & Constraints

**Always:**
- KI-kall bare fra POST, og bare når `sjekk_innlegging` ikke gir feil. Først `nokkelord(annonse)`, så `gap(cv, annonse)`. Søknaden endres først når begge har lyktes.
- Ny `sett_analyse` i `kjerne/okt.py` lagrer `nokkelord` (tuple), `nokkelord_annonse` (annonsen vasket med `testdata_match.vask`, samme vask som AD-10), `arbeidsgiver`, `gap`, og steget blir minst resultat. Så redirect til `/resultat`.
- `KIFeil`: innleggingen vises på nytt (200, ingen redirect) med feltene fylt ut, steget uendret, og feilboksen med `tekster.ki_feiltekst(feil)` som eneste tekst (ingen lenker). Samme `tabindex="-1"` og `autofocus`.
- `/resultat` (GET) krever innlogging og steg resultat. Prosenten regnes med `tell_treff` fra den lagrede listen og den lagrede CV-en hver gang siden vises, aldri lagret.
- Resultatsiden: tittel «Resultat», `h1` «Slik passer CV-en din til stillingen», `h2` «Gap-analyse» med `h3` «Dette dekker CV-en din» og `h3` «Dette kan du jobbe videre med», hver med sin liste, og `h2` «Nøkkelordtreff» med «X av Y = Z %».
- Alle nye tekster i `web/tekster.py`. Nøkkelordlisten, CV og annonse ligger bare i øktlageret i minnet, cookien har bare `okt_id`.

**Never:**
- Ikke «i»-ikon, «Laget av KI», farger, ✓/→, tekster for tomme lister, nøkkelordlistene, prosentlinje, ATS-forklaring, «Tilbake» eller «Lag søknadsbrevet mitt» (2.6).
- Ikke ventetegn, `opptatt`, «Det du har lagt inn, er ikke borte.» eller «Prøv på nytt» (2.7).
- Ikke gjenbruk av nøkkelordlisten (Epic 7). Ikke endre `telleregel.py`, `testdata_match.py`, `ki_svar.py`, `adaptere/ki.py` eller `testdata/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Riktig | `cv.txt` og `annonse.txt` fra case 1, `handling=sjekk` | 302 til `/resultat`, søknaden har listen, vasket annonse, «Testvik Utvikling AS», `gap`, steg resultat | – |
| Fasit | GET `/resultat` etter riktig | «7 av 11 = 64 %», tallene lest fra `fasit.md` (kriterium 2) | – |
| Ny lasting | GET `/resultat` to ganger | samme tekst begge gangene | – |
| Inndatafeil | tom CV | som i 2.5.1, ingen KI-kall | – |
| KI-feil | `ki()` gir `KIFeil(nettverk)` på `gap` | 200, «Nettverksfeil, sjekk nettverkstilgangen.», feltene fylt ut, steg innlegging, `nokkelord` er `None` | feilboks |
| For tidlig | GET `/resultat` på steg innlegging | 302 til `/innlegging` | – |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/okt.py` -- ny `sett_analyse(soknad, *, nokkelord: dict, gap: dict) -> Soknad`, med svarformene fra AD-4. Importerer `vask` fra `testdata_match.py`. `sett_inndata`, `velg_modus` og `begynn` endres ikke.
- `backend/soknad/web/flyt.py` -- `Steg.RESULTAT: "web.resultat"` i `SIDE_FOR_STEG`.
- `backend/soknad/web/ruter.py` -- `innlegging()`: etter sjekken uten feil, KI-kallene i `try/except KIFeil`. `_vis_innlegging` får `ki_feil: str | None = None`. Ny `resultat()` med `@login_required` og `@krever_steg(Steg.RESULTAT)`.
- `backend/soknad/web/tekster.py` -- resultattekstene og en funksjon for «X av Y = Z %». `ki_feiltekst` finnes alt.
- `backend/soknad/web/templates/innlegging.html` -- feilboksen viser `ki_feil` når den er satt.
- `backend/soknad/web/templates/resultat.html` -- ny, bygger på `base.html`. Ingen ny CSS.
- Tester: `tests/kjerne/test_okt.py`, `tests/web/test_innlegging.py` (testen `test_fr8_testdata_gir_samme_side_uten_feilboks` skrives om til redirect), ny `tests/web/test_resultat.py`, og `test_modusvalg.py` linje 116 (`SIDE_FOR_STEG` har nå også resultat). Gjenbruk `sett_soknad`, `soknaden`, `tagger_i`, `main` fra `hjelpere.py`. En KI som feiler, settes inn med `app.extensions["test_ki"]` (beholder `caser`).

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/okt.py` -- `sett_analyse`, med tester (feltene, vasket annonse, steg minst resultat, steg brev beholdes).
- [x] `backend/soknad/web/flyt.py`, `ruter.py`, `tekster.py` -- KI-kallene, KI-feilen og `/resultat`.
- [x] `innlegging.html` og ny `resultat.html` -- som i Always.
- [x] Tester -- én per rad i matrisen, overskriftsnivåene, punktene fra `gap.json` i begge listene, og at cookien bare har `okt_id`. FR-nummer i navn og docstring.

**Acceptance Criteria:**
- Given hele testsamlingen, when `uv run pytest` kjører, then er alt grønt (333 før denne storyen), og `ruff check` og `ruff format --check` har ingen feil.
- Given testdataene fra case 1 limt inn i nettleseren, when jeg trykker «Sjekk CV-en min», then kommer jeg til «Slik passer CV-en din til stillingen» med seks punkter under «Dette dekker CV-en din», fire under «Dette kan du jobbe videre med» og «7 av 11 = 64 %».

## Implementation Notes

- Branch: `story/2-5-2-analysen-og-forste-resultatside`.
- Hovedøkta skrev koden selv (ingen hjelpeagent), som i story 2.3–2.5.1.
- `sett_analyse` gir `steg=max(steg, RESULTAT)`, så et steg lenger fram (brev, Epic 3) beholdes når analysen kjøres på nytt med samme tekster.
- KI-kallene skjer bare når det ikke er feil i feltene. Lykkes analysen, kjøres den på nytt også når tekstene er uendret. Gjenbruken av listen kommer i Epic 7.
- KI-feilen står alene i feilboksen (`p.feilboks-overskrift`), uten «Noe må fikses …» og uten lenker. Story 2.7 legger til resten.
- Tomme gap-lister gir en tom `<ul>`. Tekstene for tomme lister kommer i 2.6, og testdataene har aldri tomme lister.
- Testene bruker `FeilendeKI` (i `tests/web/hjelpere.py`, så story 2.7 kan bruke den), som har de samme testcasene som `TestKI`, lar én oppgave gi `KIFeil` og husker hvilke oppgaver som ble kalt.
- `test_fr8_testdata_gir_samme_side_uten_feilboks` er skrevet om til `test_fr15_testdata_gir_analysen_og_resultatsiden`, og `test_modusvalg.py` venter nå resultatsteget i `SIDE_FOR_STEG`.
- Tester: 28 nye, 361 i alt etter gjennomgangen, `ruff` grønn.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-09), tre lag: blind, grensetilfeller, testhull. Testhull-laget fant ingen hull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | To «Sjekk» samtidig (dobbeltklikk, to faner) med ulik tekst: den tregeste vinner | grensetilfeller | low | Riktig, men samme funn som #4 i 2.5.1. `opptatt` i story 2.7 stopper en ny POST mens analysen pågår. Tas opp med Kristine (retro-punkt 7) | avvist |
| 2 | `/resultat` gir 500 når steget er resultat uten `nokkelord` eller `gap` | grensetilfeller, blind | false | Bare `sett_analyse` setter steg resultat, og den setter begge. `sett_inndata` og `velg_modus` setter steget tilbake til innlegging når de nullstiller. Ny søknad starter på steg start | avvist |
| 3 | Tom «dekker» eller «mangler» gir en overskrift med tom liste | grensetilfeller | low | Riktig med ekte KI, men tekstene for tomme lister står i Never (story 2.6) | avvist |
| 4 | Punkter med bare mellomrom i gap-listene vises som tomme punkter | grensetilfeller | low | `ki_svar.kontroller` slipper gjennom tomme tekster ved siden av ekte. Kan ikke skje med testdataene, bare med ekte KI i Epic 4 | utsatt |
| 5 | Kommentaren sier at søknaden endres først etter KI-kallene, men feltene er alt lagret | blind | low | Riktig. Kommentaren er rettet | patch |
| 6 | KI-feil-testen sjekker ikke `nokkelord_annonse` | blind | low | Riktig. Lagt til | patch |
| 7 | Ingen test av rekkefølgen nøkkelord → gap, og at gap ikke kalles når nøkkelord feiler | blind | low | Riktig. Ny test `test_fr15_forst_nokkelord_saa_gap` | patch |
| 8 | KI-feil ved ny kjøring fra steg resultat beholder steget og den gamle analysen | blind | false | Ønsket: tekstene er like, så den gamle analysen gjelder fortsatt, og steget flyttes bare etter en vellykket POST | avvist |
| 9 | Testene sammenligner escapet HTML med rå tekst | blind | low | Riktig. `liste`, `nokkelordtreff` og KI-feil-testen bruker nå `html.unescape` | patch |
| 10 | Arbeidsgiveren er skrevet inn i testen i stedet for lest fra `nokkelord.json` | blind | low | Riktig. Leses nå fra fila | patch |
| 11 | Fasit-testen er låst til «7 av 11 = 64 %» og gir en uklar feil hvis linjen mangler | blind | low | Riktig. Tallene leses bare fra `fasit.md`, med en tydelig melding | patch |
| 12 | FR-nummer mangler i noen docstrings | blind | low | Riktig. Lagt til | patch |
| 13 | KI-feil logges ikke | blind | low | Riktig, men prosjektet logger ingenting ennå. Viktig først med ekte KI | utsatt |
| 14 | `FeilendeKI` ligger i en testfil og bruker navnet `type` | blind | low | Riktig, og story 2.7 trenger den. Flyttet til `hjelpere.py` med `feiltype` | patch |

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Logg inn, «Begynn å lage søknad», Full generering. Lim inn `cv.txt` og `annonse.txt` fra `backend/testdata/case-1-utvikler/` og trykk «Sjekk CV-en min»: resultatsiden med fanetittelen «Resultat – Søknadsassistenten», de to listene og «7 av 11 = 64 %».
- Trykk F5 på resultatsiden: samme prosent.
- Skriv `/resultat` i adressefeltet rett etter innlogging: du sendes til startsiden, ikke til resultatsiden.
- Gjør vinduet 375 px: ingenting ruller sidelengs.
