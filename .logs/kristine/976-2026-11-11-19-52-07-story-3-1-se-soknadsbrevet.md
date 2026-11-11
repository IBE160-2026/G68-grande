# Story 3.1: Se søknadsbrevet

## 2026-11-11 kl. 19:52 — Kristine

### Oppgave
Kristine startet `/bmad-build 3.1`: første story i epic 3. Resultatsiden skal få «Lag søknadsbrevet mitt», og brukeren skal se brevet på en egen brevside.

### Plan
- En hjelper samlet planene for epic 3 i `_bmad-output/implementation-artifacts/epic-3-context.md` (kopi i `my-project/9-koding/`).
- KI-en leste koden, UX, arkitekturen og testdataene og skrev spec-en [`spec-3-1-se-soknadsbrevet.md`](../../my-project/9-koding/spec-3-1-se-soknadsbrevet.md), med et utkast til testbrevet til Sara.
- Kristine valgte å beholde spec-en samlet (ca. 2500 tokens) og godkjente den («Godkjenn og fortsett»).
- En hjelper kodet storyen, og tre hjelpere gikk gjennom koden (blind, kanttilfeller, testhull).

### Resultat
- Branch `story/3-1-se-soknadsbrevet` fra `main` på `d1b9540`. Commit `2912ceb` (koden) og `6f417bd` (spec-kopi, epic 3-kontekst, oversikten, TO DO, prompt-logg 321–322, sprint-status). Ikke pushet.
- Resultatsiden: «Tilbake» til venstre og «Lag søknadsbrevet mitt» til høyre, med ventetegnet «Vi lager brevet ditt – det kan ta en liten stund.». POST `/resultat` henter brevet med `opptatt` rundt og sender til `/brev`.
- Brevsiden `/brev`: «Din ferdigstilte søknad!» og brevet som et hvitt ark (høyst 720 px), ingen «Tilbake», kan ikke redigeres. Sidetittel «Søknadsbrev».
- KI-feil: resultatsiden med feilboksen, «Resultatet og det du har lagt inn, er ikke borte.» og «Prøv på nytt».
- Nytt testbrev `backend/testdata/case-1-utvikler/ki-svar/brev-1.json`. Tester sjekker at det består kontrollen, ikke har KI-frasene fra addendum og ikke nevner noe fra sjekklisten i `fasit.md`.
- Fra retrospektiven for epic 2: brevsteget står i `SIDE_FOR_STEG`, og resultatsiden sender til innleggingen når analysen mangler.
- Kodegjennomgangen: 15 funn, 5 rettet (blant annet at tomme avsnitt i et brev fjernes, og en test for utlogging midt i brevkallet), 0 utsatt, 10 avvist med begrunnelse i spec-en.
- 512 tester grønne, `ruff check` og `ruff format --check` grønne. Ikke prøvd i nettleseren ennå.
- Sprint-status: epic 3 «in-progress», story 3.1 «review». `notater.md` har fått et punkt om testbrevet og FR-37 (lokal fil).

### Åpne punkter
- Kristine leser og godkjenner testbrevet til Sara (`brev-1.json`, teksten står også under «Design Notes» i spec-en).
- Prøve story 3.1 i nettleseren etter de manuelle sjekkene i spec-en (ventetegnet, fokus, KI-feil med kopi av `brev-1.json`, tilbakeknappen, 320/768/1280 px og 200 % zoom). Se også om avstanden mellom «Med vennlig hilsen» og «Sara Eksempel» ser bra ut.
