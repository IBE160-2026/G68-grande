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
- **Rettet etterpå:**
  - README oppdatert (`9e467b7`, pushet): statuslinjen sier hva som virker i testmodus nå, testdata-avsnittet, mappestrukturen med `backend/soknad/web`, `kjerne` og `adaptere`, og ny lenke til `my-project/9-koding/` og PR-ene under «Prosess og KI-bruk».
  - De 5 flettede story-branchene er slettet på PC-en. På GitHub var 2.4.1 og 2.4.2 alt borte (KI-en hadde lest en avkuttet liste). Bare `story/2-6-…` var igjen, og Kristine slettet den selv. Nå er bare `main` igjen på GitHub.
  - **GitHub-issues prøvd én gang:** [issue #16](https://github.com/IBE160-2026/G68-grande/issues/16) «Nettlesertester for JavaScript-filene». Lukkes med «Closes #16» i PR-en for story 8.2, og det står i `todo.md`. Kristine bestemte at det ikke lages issue for hver ting fremover.
  - **PR-kommentarer:** kommentarer på PR #5, #7, #11, #12, #13, #14 og #15 om det som skjedde etter at PR-en ble laget (retroen, branchen som ikke kunne slettes, CI på `main`, «to trykk samtidig» løst i #15, og issue #16). De andre 8 hadde ingenting å nevne. Fremover får hver PR en kort kommentar etter at Kristine har prøvd siden, når det er noe å nevne.
  - Prompt-loggen fikk rad 297–303 for økten.

### Åpne punkter
- Story 8.2: skrive «Closes #16» i PR-en.
