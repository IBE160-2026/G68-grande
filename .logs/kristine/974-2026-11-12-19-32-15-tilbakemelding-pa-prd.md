# Tilbakemelding på PRD

## 2026-11-12 kl. 19:32 — Kristine

### Oppgave
Lese tilbakemeldingen på PRD-en fra Bård Pettersen (`my-project/2-prd/tilbakemelding-prd.md`) og ta med forbedringene Kristine er enig i. Kristine syntes punktet om milepælene var rart, fordi det alt var gjennomgått 3. november.

### Plan
- Forklare hvorfor milepælene ble flagget (tabellen, spørsmålet i §8 og `updated` viste fortsatt den gamle planen).
- Rette milepælene, legge til en kort brukerreise og skrive kostnad i tokens med grenser i NFR-11.

### Resultat
- `c5bf64a`: §7 merket som den opprinnelige planen (fremdriften følges i sprintplanen og sjekkpunktene i §6), spørsmålet i §8 lukket, `updated: 2026-11-12`.
- `9a2142e`: kort brukerreise (Ingrid) i §2 med henvisning til de tre reisene i UX. NFR-11 fikk kostnad i tokens, et overslag (Opus 5.5: 4/20 dollar per million tokens, omtrent 10 000 inn og 6 000 ut per søknad, rundt 2 kr, mål under 3 kr) og grenser (15 000 tegn per felt, 10 KI-kall per søknad). Kristine valgte «per søknad» i stedet for «per økt». TO DO og prompt-logg 335–337 er oppdatert.
- Bare `my-project/2-prd/prd.md` er endret. Kopien i `_bmad-output/` er eldre fra før og ble ikke rørt.
- `my-project/5-arkitektur/technology.md` fra Bård handler om et annet prosjekt (Pytagoras Forlag) og har ikke noe om tokens for dette prosjektet.

### Åpne punkter
- Epic 4: kode grensene fra NFR-11 (høyst 15 000 tegn per felt med egen feilmelding, høyst 10 KI-kall per søknad, logge tokens inn og ut) og vise tokens og kroner per søknad i testplanen.
- Tilbakemeldingen 4.3 og 4.5 er ikke tatt: hvor lang nøkkelordlisten fra KI-en skal være, og hvordan «C#», «C++» og «.NET» telles. Bestemme om de skal inn i epic 4.
