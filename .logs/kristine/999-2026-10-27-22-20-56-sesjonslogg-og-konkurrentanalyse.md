# Sesjonslogg og konkurrentanalyse

## 2026-10-27 kl. 22:20 — Kristine

### Oppgave
Hente faglærers nye regler (`CLAUDE.md` og skillen `sesjonslogg`) og bestemme hvordan de skal brukes sammen med loggene jeg allerede har. Deretter kjøre en konkurrentanalyse med `bmad-deep-recon`, som faglærer anbefalte. Den skulle helst vært gjort før PRD-en, så den skal ligge i en egen mappe og ikke endre noe vi allerede har laget.

### Plan
- `git pull` for å hente faglærers filer.
- Fortsette med egne logger (prompt-logg, beslutningslogger, `todo.md`) og bruke sesjonsloggen i tillegg. `todo.md` er hovedlista, og `issues.md` speiles inn i den.
- Konkurrentanalyse av Jobscan, Rezi, Teal og Kickresume. Fire hjelpere søkte samtidig (én per konkurrent), og én hjelper sjekket hullene i runde 2. Planen er logget i `my-project/4-konkurrentanalyse/konkurrentanalyse-memlog.md`.

### Resultat
- Hentet `CLAUDE.md` og `.claude/skills/sesjonslogg/` fra faglærer (commit `b7b8eb4`).
- `.logs/kristine/README.md` forklarer hvorfor jeg fortsetter med egne logger, og at `todo.md` er hovedlista (`a4d2448`).
- Konkurrentanalysen ligger i `my-project/4-konkurrentanalyse/` med rapport, beslutningslogg, søkenotater og README. Konklusjonen er at differensieringen i briefen holder: ingen av de fire forklarer hvordan poengsummen regnes ut, ingen har KI-korrektur av eget søknadsbrev med markerte endringer, og ingen støtter norsk. Lav pris skiller oss ikke ut. Det ble 8 bekreftede påstander, 11 ubekreftede og 1 forkastet. Brief, PRD og UX er ikke endret (`c742ae3`).
- `my-project/README.md` og `todo.md` er oppdatert med den nye mappa og tre nye punkter (`c742ae3`).
- Prompt-loggen har fått oppføringene 169–174 og «Hva jeg lærte»: jeg må stole mer på KI-ens avgjørelser i det som er lett å rette, for å bli ferdig i tide (`e47a3b4`).
- Ny arbeidsmåte fra nå av: KI-en bestemmer rutinesaker selv og forteller om dem etterpå. Jeg sjekker mine egne ord, det som endrer nettsiden, store arkitekturvalg og PR-er.

### Åpne punkter
- Arkitektur: vurdere en kort grunn ved hver endring i Korrektur, slik Kickresumes «What we changed» gjør (passer det med setningsparene `{ny, gammel}`?).
- Før innlevering: sjekke på nytt at ingen av konkurrentene har fått norsk eller korrektur av eget brev med markerte endringer (sjekk fra 7. november).
- Hvis tid: prøve Teal, Rezi og Kickresume selv for å bekrefte funnene som bygger på at vi ikke fant noe i dokumentasjonen deres.
