# Story 2.7.2: KI-feilboksen med «Prøv på nytt»

## 2026-11-10 kl. 21:43 — Kristine

### Oppgave
`/bmad-build 2.7.2`: andre halvdel av story 2.7. Når KI-en feiler på innleggingen, skal feilboksen også si «Det du har lagt inn, er ikke borte.» og ha knappen «Prøv på nytt» (FR-28, UX-DR7).

### Plan
- Intensjonen kom fra `deferred-work.md` (delt ut fra 2.7.1). Ingen åpne spørsmål og en liten endring, så `bmad-build` valgte den korte veien (oneshot): kode, én gjennomgangsagent (blind), rette, committe.
- Spec: [`my-project/9-koding/spec-2-7-2-ki-feilboksen-med-prov-pa-nytt.md`](../../my-project/9-koding/spec-2-7-2-ki-feilboksen-med-prov-pa-nytt.md).
- Branch `story/2-7-2-ki-feilboksen-med-prov-pa-nytt` fra `main` (`3c79f82`).

### Resultat
- `013341b` (kode): `tekster.py` fikk `KI_FEIL_BEHOLDT_INNLEGGING` og `PROV_PA_NYTT_KNAPP`. I `innlegging.html` fikk skjemaet `id="innlegging-skjema"`, og feilboksen fikk setningen og hovedknappen «Prøv på nytt» (`form=`, `handling=sjekk`, `data-vente`), så den viser ventetegnet fra 2.7.1. `vente.js` er ikke endret. CSS: knappen er bare så bred som teksten. Docstringen til `_vis_innlegging` er rettet.
- Tester: 7 nye, 429 i alt, `ruff` grønn.
- Gjennomgang (blind-laget): 10 funn, 5 rettet (blant annet at testen for «Prøv på nytt» ikke brukte knappen, **KI-feil**), 1 utsatt (ingen nettlesertest, i `deferred-work.md`) og 4 avvist.
- `b3453dc` (prosjektmappa): spec-kopi, rad i oversikten, TO DO, prompt-logg 304, notat i `notater.md` og sprint-status (story 2.7 på «review»).
- Kristine prøvde siden i nettleseren (KI-feil med tomt `gap.json`, som ble satt tilbake med `git checkout`, «Prøv på nytt», smal skjerm og zoom): «det fungerte», «det ser bra ut». Branchen er pushet, [PR #17](https://github.com/IBE160-2026/G68-grande/pull/17) er laget med merknad om KI-feil, og PR-en har fått en kommentar om nettlesertesten og en om at KI-en gikk rett på kodingen fordi den ikke lurte på noe.
- PR #17 er flettet av Kristine (CI grønn på Linux og Windows), og branchen er slettet. Story 2.7 er satt til ferdig i sprint-statusen (begge kopiene), oversikten og TO DO, og prompt-logg 305–311 er lagt inn. Alt er pushet til `main`.

### Åpne punkter
- Ingen automatisk test sjekker «Prøv på nytt» i en nettleser (sammen med `vente.js`, story 8.2 / issue #16).
