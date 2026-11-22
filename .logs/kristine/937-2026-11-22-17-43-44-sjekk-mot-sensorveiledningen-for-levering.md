# Sjekk mot sensorveiledningen før levering

## 2026-11-22 kl. 17:43 — Kristine

### Oppgave
Kristine spurte om det bare var fire punkter igjen, eller om noe annet lå og lurte, og ba om en ny sjekk mot sensorveiledningen (`Sensorveiledning.pdf`, del 1) for å se om noe manglet.

### Plan
- Gå gjennom de åpne punktene i `issues.md`, `todo.md` og sprint-statusen.
- Sjekke repoet mot alle de sju kriteriene: commits og PR-er, CI, tester, README (versjoner, `.env.example`, testbruker, mappestruktur, lenker), hemmeligheter i hele historikken, filer i repoet som ikke hører hjemme der (`.env`, `venv`, database), og rester i koden (TODO, `print`, utkommentert kode).

### Resultat
- Ingenting mangler av betydning. CI er grønn på `main`. Det eneste i historikken som ligner en nøkkel, er den falske nøkkelen i `backend/tests/adaptere/test_ekte_ki.py`. Det finnes ingen TODO-er eller utkommentert kode i `backend/soknad`.
- To småting er rettet i commit `2c9a232`:
  - Story 8.2 sto som `backlog` i kopien `my-project/7-sprint-planning/sprint-status.yaml`, men som `in-progress` i `_bmad-output`. Den er nå satt til `in-progress`.
  - README pekte ikke til kuttlisten, selv om sensorveiledningen (kriterium 2) ser etter at det som er utelatt fra proposal, er begrunnet. Kristine godkjente et nytt avsnitt, «Hva er med, og hva er kuttet», under «Hvem den er for».
- Rad 507 er lagt til i `my-project/prompt-logg.md`.
- Disse åpne punktene er utenfor selve nettsiden: to punkter til refleksjonsrapporten (spørre faglærer om del 2, og svare på Bårds to spørsmål), og to frivillige punkter (mørk modus, og å prøve konkurrentene selv).

### Åpne punkter
Ingen nye.

## 2026-11-22 kl. 18:12 — Kristine

### Oppgave
Kristine leste den korte prompt-loggen. Hun forsto ikke punktet om nettlesertester, og la merke til at brevsiden ikke har «Tilbake». Hun ville ikke ha mer kode, men ønsket at grunnen til valget ble skrevet ned.

### Plan
- Forklare punktet om nettlesertester med enklere ord, og vise tabellen «Skriptene som prøves for hånd» fra testplanen.
- Finne ut om det var bestemt at brevsiden ikke skal ha «Tilbake», og skrive grunnen inn i `EXPERIENCE.md`.

### Resultat
- Det var bestemt i UX (`EXPERIENCE.md`, linje 65), men grunnen sto ikke der. Den er nå skrevet inn i begge kopiene (`my-project/3-ux/` og `_bmad-output`): brevet kan slettes uten spørsmål hvis man går tilbake og endrer noe, «Nytt forslag» gir et annet brev, og nettleserens tilbakeknapp virker. Kristine godkjente teksten. Det er sjekket i `ruter.py` at vinduet «Vil du ha et nytt forslag?» kommer først når det alt finnes et brev.
- `my-project/prompt-logg-kort.md` har fått enklere tekst om skriptene og et nytt punkt om brevsiden. Rad 508 er lagt til i `prompt-logg.md`.
- Commit: «Grunnen til at brevsiden ikke har «Tilbake» …». Ingen ny kode.

### Åpne punkter
Ingen nye.
