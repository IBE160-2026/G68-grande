# Story 4.2: Brevet fra Claude

## 2026-11-13 kl. 21:47 — Kristine

### Oppgave
Kode story 4.2 med `/bmad-build 4.2`: Claude skal kunne skrive søknadsbrevet ut fra bare CV og annonse, med reglene for tone og de 17 KI-frasene i prompten. Teksten fra KI-en skal renses, så Word-fila ikke feiler.

### Plan
- Planen: [spec-4-2-brevet-fra-claude.md](../../my-project/9-koding/spec-4-2-brevet-fra-claude.md) (originalen i `_bmad-output/implementation-artifacts/`).
- Kristine bestemte at brevet begynner rett på teksten og slutter med «Med vennlig hilsen» og navnet, at det er høyst én A4-side (250–400 ord i 4–6 avsnitt), at planen beholdes samlet (ca. 2400 tokens), og at hjelpeagenter kan brukes.
- En hjelpeagent kodet på branchen `story/4-2-brevet-fra-claude`, og tre hjelpere gikk gjennom koden.

### Resultat
- `backend/prompts/brev.md`: FR-24, FR-37 og de 17 KI-frasene. Etter gjennomgangen sier den også at Claude aldri gjetter arbeidsgiverens navn, og at FR-37 går foran når CV-en dekker færre enn to krav.
- `EkteKI.brev` sender bare CV og annonse, med skjemaet `{avsnitt}`.
- `kontroller` fjerner kontrolltegn, gjør linjeskift og tab om til mellomrom, fjerner tomme punkter og gjør tom arbeidsgiver om til `None`. Det gjelder også testmodus.
- Gjennomgangen fant 15 ting: 4 rettet, 3 utsatt (`deferred-work.md`) og resten avvist med begrunnelse.
- ruff er rent, og alle 655 tester er grønne. Nettsiden bruker fortsatt testmodus.
- Commits: `bfdb06c` (koden) og `390c2ca` (kopi av planen, oversikten, TO DO, prompt-logg 361–363 og sprint-status). Notatet til refleksjonsrapporten er lagt inn i `notater.md`, men den mappen ligger med vilje utenfor Git. Ikke pushet.
- Lukket i `issues.md`: tomme punkter i KI-svar, og rensingen av brevteksten.

### Åpne punkter
- PR for story 4.2: pushe branchen, lage PR med merknad om KI-feil, grønn CI og flette. Deretter sette 4.2 til done i sprint-statusen og krysse av i TO DO.
- Story 4.3/4.4: sjekke med ekte KI at brevet følger reglene (ingen KI-fraser, lengde, ett avsnitt per element og ingen markdown).
- Story 4.4: testen mot sjekklisten i `fasit.md` skal gjelde alle `brev-*.json`, ikke bare `brev-1.json`.
