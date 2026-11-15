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

### Åpne punkter
- Før epic 5: to nye regler i brev-prompten, navnet i et eget felt og hilsenen satt inn av nettsiden (også i testsvarene), og kriteriene for brevet kjørt på nytt med ekte KI, sammen med prøven av plan B på en annen CV.
