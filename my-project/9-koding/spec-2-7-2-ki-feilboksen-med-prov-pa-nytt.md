---
title: 'Story 2.7.2: KI-feilboksen med «Prøv på nytt»'
type: 'feature'
created: '2026-11-10'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Når KI-en feiler på innleggingen, står bare feilteksten i feilboksen. Brukeren får ikke vite at det som er lagt inn, er der fortsatt, og har ingen knapp i boksen for å prøve igjen (FR-28, UX-DR7).

**Approach:** Under feilteksten fra `ki_feiltekst` står «Det du har lagt inn, er ikke borte.» og hovedknappen «Prøv på nytt», som utseendet i skissen `input-page-1.html`. Knappen sender skjemaet på nytt som «Sjekk CV-en min» (`form=` på knappen, `name="handling" value="sjekk"`) og viser ventetegnet fra 2.7.1 (`data-vente` med «Vi sjekker CV-en din – det tar noen sekunder.»). Boksen har fortsatt `tabindex="-1"`, `autofocus` og ingen `role="alert"`, og ingen lenker. Tekstene står i `web/tekster.py`, ordrett fra EXPERIENCE. Knappen er bare så bred som teksten, som i skissen. Teksten for resultatsiden («Resultatet og det du har lagt inn, er ikke borte.») kommer i Epic 3.

</frozen-after-approval>

## Implementation Notes

- Branch: `story/2-7-2-ki-feilboksen-med-prov-pa-nytt`, fra `main` på `3c79f82`. Sprint-status: 2.7 står alt på «in-progress».
- `web/tekster.py`: `KI_FEIL_BEHOLDT_INNLEGGING` og `PROV_PA_NYTT_KNAPP`, rett under `KI_FEILTEKSTER`.
- `templates/innlegging.html`: skjemaet fikk `id="innlegging-skjema"`. I feilboksen står setningen i `<p class="feilboks-tekst">` og knappen i `<p class="feilboks-knapp">`. Avsnitt i stedet for `<div>`, så regex-en `<div class="feilboks"…>(.*?)</div>` i testene fortsatt finner hele boksen. `vente.js` er ikke endret: `submit`-hendelsen har knappen som `submitter` også med `form=`, og sperringen går fra knappen opp til `body`.
- `static/css/stil.css`: `.feilboks-tekst`, `.feilboks-knapp` og `.feilboks-knapp .hovedknapp` (`inline-block`, `width: auto`).
- Tester: 7 nye, 429 i alt, `ruff` grønn. I `test_innlegging.py` sjekker KI-feil-testen nå at feilteksten står først i boksen. Nye tester: setningen og knappen for hver `KIFeil`-type, at knappen sender skjemaet som «sjekk» med ventesetningen (og at begge knappene da har `data-vente`), at «Prøv på nytt» med KI som virker gir resultatsiden, og CSS-bredden. I `test_tekster.py`: tekstene ordrett. `test_fr27_bare_sjekk_knappen_har_ventetekst` (GET uten feil) gjelder fortsatt uendret.

- Etter gjennomgangen: docstringen til `_vis_innlegging` i `ruter.py` er rettet, og testene er strammet inn (se Review Triage Log). Sperren mot tekster i malen ser etter «er ikke borte» og ikke bare «ikke borte», fordi en eldre kommentar i `innlegging.html` sier at et linjeskift «ikke blir borte». 429 tester, `ruff` grønn.

## Review Triage Log

Runde 1 (2026-11-10), ett lag: blind (oneshot).

| # | Funn | Vurdering | Begrunnelse | Rute |
|---|------|-----------|-------------|------|
| 1 | Docstringen til `_vis_innlegging` sier at KI-feilen «står alene i feilboksen» | low | Riktig, ikke sant lenger | patch |
| 2 | Ingen test hindrer at «er ikke borte» og «Prøv på nytt» skrives rett i malen | low | Riktig. Lagt til i `test_fr27_tekstene_ligger_i_tekster_py` | patch |
| 3 | Testen for «Prøv på nytt» med KI som virker bruker ikke knappen | low | Riktig. POST-en bygges nå fra feilsiden: knappens `name`/`value` og tekstboksene | patch |
| 4 | `<p>` rundt knappen er valgt for å passe regex-en i testene, som kan kutte boksen | low | `<p>` rundt en knapp er gyldig HTML. Regex-en er et eldre mønster i flere tester, og boksen har ingen `<div>` inni | avvist |
| 5 | `.feilboks-knapp .hovedknapp` gjentar tre linjer fra `.knapperad.mellomrom .hovedknapp` | low | Kosmetisk. To steder med ulik plass på siden kan trenge ulike regler senere | avvist |
| 6 | Testen sjekker ikke klassen `feilboks-tekst` | low | Riktig. Regex-en krever nå `class="feilboks-tekst"` | patch |
| 7 | Knappetesten sammenligner alle attributtene og knekker ved et nytt attributt | false | Med vilje: et nytt attributt på knappen bør ses i testen | avvist |
| 8 | Ingen nettlesertest av at «Prøv på nytt» med `form=` sender feltene, viser ventetegnet og beholder fokus | medium | Riktig, samme hull som for `vente.js` i 2.7.1. Sjekkes for hånd i PR-en | utsatt |
| 9 | Spec-en er ikke kopiert til `my-project/9-koding/`, status er `in-progress`, og logg og notater mangler | false | Gjøres etter gjennomgangen, som i 2.7.1 | avvist |
| 10 | Docstringen til `test_fr27_bare_sjekk_knappen_har_ventetekst` gjelder bare siden uten feil | low | Riktig. Docstringen sier det nå | patch |

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alt grønt (429)
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Få fram en KI-feil: det går ikke med testdataene alene. Endre midlertidig `backend/testdata/case-1-utvikler/ki-svar/gap.json` til `{}` (gir «Noe gikk galt hos KI-tjenesten. Prøv på nytt.»), og sett fila tilbake etterpå.
- Feilboksen øverst: feilteksten, «Det du har lagt inn, er ikke borte.» og knappen «Prøv på nytt», bare så bred som teksten. Feltene er fortsatt fylt ut, og boksen har fokus.
- Sett fila tilbake og trykk «Prøv på nytt» (sett gjerne «Slow 4G» i F12): ventetegnet vises, Tab blir på knappen, og så kommer resultatsiden.
- 320 px og 200 % zoom: boksen og knappen får plass uten rulling sidelengs.
