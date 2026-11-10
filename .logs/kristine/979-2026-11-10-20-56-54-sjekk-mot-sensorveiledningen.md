# Sjekk mot sensorveiledningen

## 2026-11-10 kl. 20:56 — Kristine

### Oppgave
Sjekke om noe i prosjektet nå avviker fra `Sensorveiledning.pdf` (del 1, sju kriterier), etter at epic 1 og det meste av epic 2 er kodet. Først et spørsmål om vi brukte en annen designskill (lærerens Impeccable/SVG) eller bare BMAD sin UX-skill.

### Plan
- Se i prompt-loggen og `ux-memlog.md` hvilken skill UX ble laget med.
- Lese sensorveiledningen og den forrige sjekken ([suksesskriterier-og-sensorveiledning](998-2026-11-03-22-17-50-suksesskriterier-og-sensorveiledning.md)).
- Sjekke repoet mot de sju kriteriene: README, `.gitignore`, filer i roten, hemmeligheter i historikken, tester og ruff, commit-historikk, PR-er, issues, branches og lenker.

### Resultat
- **UX:** laget bare med BMAD-skillen `bmad-ux`, ingen Impeccable. SVG er bare brukt i prosentlinjen (story 2.6). Kristine bestemte at Impeccable ikke trengs.
- **Det som er i orden:**
  - Prosess: 241 commits fra september til november, 15 PR-er med FR-numre i tittelen og «Hva KI-en gjorde feil» i beskrivelsen, spec med kodegjennomgang for hver story i `my-project/9-koding/`, prompt-logg og sesjonslogger.
  - Testing: 422 tester grønne, `ruff check` og `ruff format --check` grønne, CI på Linux og Windows.
  - Repoet: ingen `.env`, database eller nøkler i historikken, `.mcp.json` bruker bare en miljøvariabel, `.venv` og `instance/` er ignorert, ingen TODO eller utkommentert kode i `backend/`, og alle lenker i README og `my-project/README.md` virker.
  - Design: DESIGN.md, EXPERIENCE.md, skisser og tilgjengelighetsgjennomgang finnes.
- **Avvik som er funnet:**
  1. README er utdatert (kriterium 6 og varseltegnet «README stemmer ikke med koden»): statuslinjen sier at kodingen begynner nå, testdata-avsnittet sier «når innleggingssiden er ferdig (story 2.5)», mappestrukturen står som «kommer» selv om koden finnes, og «Prosess og KI-bruk» lenker ikke til `9-koding/` (kodegjennomgangene og retroen).
  2. Ferdige branches er ikke slettet: 5 lokalt og 2 på GitHub (`story/2-4-1-…` og `story/2-4-2-…`). Lite, kriterium 7.
  3. PR-ene har ingen kommentarer eller reviews på GitHub. Gjennomgangen står i PR-beskrivelsen og i spec-filene, så det holder ifølge veiledningen («for eksempel»). Ingen endring nødvendig.
  4. Ingen GitHub-issues. `issues.md` og `todo.md` regnes som «tilsvarende». Ingen endring nødvendig.
- Allerede planlagt og ikke avvik nå: skjermbilder og bevis for ekte KI (story 8.1 og epic 4), nettlesertester for JavaScript (story 8.2).
- Ingen filer er endret i denne økten.

### Åpne punkter
- Oppdatere README nå: statuslinjen, testdata-avsnittet, mappestrukturen og lenke til `my-project/9-koding/` under «Prosess og KI-bruk». Venter på Kristines svar.
- Slette ferdige story-branches lokalt og på GitHub (`story/2-4-1-…` og `story/2-4-2-…`). Venter på Kristines svar.
