# Story 2.6 – hele resultatsiden med forklaringer og «Tilbake»

## 2026-11-10 kl. 18:32 — Kristine

### Oppgave
Kristine startet `bmad-build` for story 2.6. Resultatsiden skal bli ferdig: forklaringer («i»-knapper, «Laget av KI», ATS), fargede lister, nøkkelordlistene, tekster for tomme lister og «Tilbake» til innleggingen, slik at en student forstår hva som mangler og hva prosenten betyr.

### Plan
- Spec: `_bmad-output/implementation-artifacts/spec-2-6-hele-resultatsiden-med-forklaringer-og-tilbake.md` (kopi i `my-project/9-koding/` kommer sammen med PR-en). Ingen åpne spørsmål.
- Spec-en var på ca. 2200 tokens. Kristine minnet om at flere stories har vært på 2200, så den ble beholdt hel. Hun godkjente spec-en og ba meg fortsette.
- Branch `story/2-6-hele-resultatsiden-med-forklaringer-og-tilbake`. Hovedøkta skrev koden selv, og tre hjelpere gikk gjennom den (blind, grensetilfeller, testhull).
- Valg jeg tok selv: «i»-boksen styres med JavaScript (også hover), så skjermlesere får vite om den er åpen. «Lag søknadsbrevet mitt» venter til story 3.1. Prosentlinjen er fylt med en gang (animasjonen kommer i Epic 7).

### Resultat
- `web/templates/resultat.html`: hele siden i rekkefølgen gap-analyse, linjen om at de kan si litt forskjellig, nøkkelordtreff, ATS-forklaring og «Tilbake». «i»-knapper med `aria-expanded`/`aria-controls`, «Laget av KI», undertekst, grønn liste med ✓ og ferskenfarget med →, «Står i CV-en (7)» og «Står ikke i CV-en (4)», egne tekster for tomme lister. Pynteikonene er skjult for skjermlesere.
- Prosentlinjen ble en liten SVG, fordi prosjekttestene forbyr `style=` i malene og faste høyder i CSS.
- Ny `web/static/js/info.js`: «i»-boksen åpnes og lukkes med trykk, Enter og mellomrom, Esc lukker, hover med mus åpner, og et trykk utenfor lukker. Startsiden kan bruke den i Epic 4.
- `web/tekster.py`: alle nye tekster ordrett fra EXPERIENCE, også pynteikonene. `web/static/css/stil.css`: utseendet, listene side om side fra 700 px, ATS-pila ▾ til høyre, høykontrast.
- Tester: 27 nye, 388 i alt, alle grønne. `ruff` uten feil. Blant dem: samme tekst kjørt to ganger med «Tilbake» imellom gir samme treff (kriterium 8).
- Gjennomgang: 15 funn. 7 er rettet (lange ord på mobil, trykk utenfor lukker «i»-boksen, ATS-pila, høykontrast, ikonene i `tekster.py`, to tester), 2 er utsatt i `deferred-work.md` og 6 er avvist.
- Commit `8c114dc` på branchen (lokalt, ikke pushet). Sprint-status: story 2.6 står på `review`.

### Åpne punkter
- Story 2.6: prøve resultatsiden i nettleseren (rekkefølge, farger, «i» med mus, trykk, Enter, mellomrom og Esc, ATS-forklaringen, «Tilbake» og «Sjekk» igjen, 320/375 px og 200 % zoom), så PR med AI-feil-notat, spec-kopi, oversikten, TO DO og prompt-logg.
- Ingen automatisk test kjører `info.js` (samme som for `innlegging.js`). Vurdere nettlesertester i story 8.2.
- Epic 4: punkter med bare mellomrom i gap-listene vises som tomme punkter (samme årsak som før: `ki_svar.kontroller`).
