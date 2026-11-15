# Technology.md og Docker

## 2026-11-15 kl. 10:18 — Kristine

### Oppgave
Kristine spurte hvor Docker kommer inn i prosjektet, og ba meg se på `my-project/5-arkitektur/technology.md` fra Bård, som også nevner fillagring og Supabase.

### Plan
- Hente fra GitHub (ingenting nytt) og lese technology.md og lærerens commit (60c53f0, 12. november).
- Sammenligne med `my-project/5-arkitektur/arkitektur.md` (drift, database, øktlager).

### Resultat
- technology.md beskriver Bårds eget prosjekt (Pytagoras-nettsiden) og er lagt inn som referanse, ikke som krav. Prosjektet har ingen Docker-filer.
- Sammenligningen viste: nettsiden kjører bare lokalt (Bård bekreftet 4. november at publisering ikke er et krav), uv gjør oppsettet likt på alle maskiner, SQLite holder for testbrukeren, og CV og brev ligger bare i minnet, så det finnes ingen fillagring, med vilje.
- Kristine bestemte at ingenting av det i technology.md tas med i prosjektet.
- Det er ikke gjort noen endringer i koden eller arkitekturen.
- Etterpå gikk vi gjennom de tre punktene om brevet før epic 5. Kristine bestemte, og det står under «Bestemt 15. november» i `my-project/testplan.md`:
  - Av de fem merknadene fra målingen med lange tekster godtas 1–3 (gap-analysen), og 4 og 5 rettes med to nye regler i brev-prompten. Jeg kalte først nummer 1 (React og TypeScript) en ekte feil. Da jeg så nærmere på det, fulgte gap-analysen regelen: annonsen spør om erfaring, og CV-en har bare «grunnleggende» uten bruk.
  - Hilsenen: KI-en sender navnet i et eget felt, og nettsiden setter inn «Med vennlig hilsen» og navnet selv. Jeg foreslo først at nettsiden skulle ta «navnet fra CV-en», men koden kjenner ikke navnet. Det ble rettet før beslutningen.
  - Plan B-regelen prøves på en annen CV i samme kjøring med ekte KI.
- I `issues.md` er to punkter lukket (merknadene og hilsenen), og ett nytt er lagt til.

- Rettingene ble bygd med `bmad-build` på branchen `brev-hilsen-og-regler`. Spec: `my-project/9-koding/spec-brev-hilsen-og-regler.md`.
  - En hjelpeagent la til `navn` i brevskjemaet, `hele_brevet()` i `kjerne/ki_svar.py` (brukt på brevsiden og i Word-fila), fjerning av hilsen eller navn som KI-en likevel skriver til slutt, og de to nye reglene i `backend/prompts/brev.md`. AD-4 i arkitekturen er oppdatert.
  - Tre gjennomgangsagenter fant 15 ulike ting. Fire små ting ble rettet: navnet alene til slutt, «Mvh» og lignende, at «navn» i prompten bare gjelder avslutningen, og en test. De andre elleve ble avvist med begrunnelse (Review Triage Log i spec-en).
  - Ekte KI, runde 1: ett brudd på kriterium 11 («Python er en sentral del av utdanningen min»), bestemt av Kristine. Ingrid-kjøringen stoppet, og et lite prøvekall viste at kreditten på API-kontoen var brukt opp. Kristine fylte på.
  - Plan B: regelen mot rangering ble utvidet (ikke «sentral», «viktig» eller «en stor del av»), med en test. Runde 2 besto kriterium 1, 3, 11 og 14, og alle 38 brevene har hilsen og riktig navn. Ingrid-CV-en: plan B-regelen holder, og merknad 4 og 5 er rettet. Kristine godtok «hver arbeidsdag» og fem andre setninger som slutninger.
  - Case 2 fikk «lønn» som 17. nøkkelord, så `fasit.md` ble oppdatert (7 av 17 = 41 %).
  - Kostnad: ca. 34 kr for begge rundene. 860 tester grønne, ruff grønn.
  - Commit `8bf90a5` på branchen. Kristine prøvde brevsiden, Word-fila og «Nytt forslag» i testmodus med case 1 og 2 («ja alt ser bra ut!»). Pushet, og [PR #33](https://github.com/IBE160-2026/G68-grande/pull/33) er laget med merknad om KI-feilene og en kommentar om prøven. CI er grønn på Linux og Windows.

### Åpne punkter
- Flette PR #33. Deretter: krysse av punktet i TO DO, og starte epic 5 (story 5.1).
