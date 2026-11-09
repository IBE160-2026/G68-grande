# Story 2.3: Testmodus kjenner igjen testdataene

## 2026-11-09 kl. 17:48 — Kristine

### Oppgave
Kristine ba om story 2.3 med `/bmad-build`, og ville at spec-en skulle åpnes når den var klar, så hun kunne lese den. Målet er at testmodus kjenner igjen de fiktive testdataene og gir de ferdige KI-svarene, slik at nettsiden kan kjøres uten API-nøkkel.

### Plan
- Spec: [`spec-2-3-testmodus-kjenner-igjen-testdataene.md`](../../my-project/9-koding/spec-2-3-testmodus-kjenner-igjen-testdataene.md) (kopi av `_bmad-output/implementation-artifacts/`), åpnet i Notisblokk.
- Kristine valgte å beholde spec-en samlet (ca. 2100 tokens) og godkjente og fortsatte.
- Egen branch `story/2-3-testmodus-kjenner-igjen-testdataene`. Hovedøkta skrev koden, og tre hjelpeagenter gikk gjennom den (blind, grensetilfeller, testhull).
- Valg tatt av KI-en: når både CV og annonse er feil, får begge feltene feilen (alle feilene vises samtidig).

### Resultat
- Ny kode: `kjerne/testdata_match.py` (`vask`, `finn_case`), `kjerne/ki_svar.py` (`kontroller`), `adaptere/ki.py` (`KI`, `TestKI`, `les_testcaser`). `feil.py` har fått `ikke_testdata` og `KIFeil`, og `tekster.py` har fått tekstene fra UX.
- Gjennomgangen: 15 funn, 6 rettet og 9 avvist med begrunnelse. Viktigst: et KI-svar med bare tomme nøkkelord ble godtatt. `pyproject.toml` gjør nå advarselen om at pytest ikke kan samle en klasse som `TestKI`, til en feil (prøvd med vilje).
- 231 tester grønne (182 før), `ruff check` og `ruff format --check` grønne.
- Commits på branchen: `e88e470` (koden) og `2677f3d` (spec-kopi, `my-project/README.md` med radene for epic 2 og story 2.1–2.3, TO DO og prompt-logg 260–261). Notatene til refleksjonsrapporten er oppdatert (4.2).
- Sprint-status: story 2.3 er satt til `review`.
- Ingen side bruker koden ennå. Det kobles på i story 2.5.
- Branchen ble pushet, og [PR #9](https://github.com/IBE160-2026/G68-grande/pull/9) ble laget med merknad om KI-feilene. CI var grønn på Linux og Windows, og Kristine flettet PR-en.
- Etter flettingen, på main: story 2.3 er satt til `done` i sprint-statusen, og `f2a64d5` har PR-lenken i `my-project/README.md`, TO DO og prompt-logg 262–263. De flettede branchene for story 2.2 og 2.3 er slettet på PC-en.
- `issues.md`: punktet «Neste steg: story 2.3» er lukket.
- Main er pushet etter at Kristine ba om det («push»): `f2a64d5` og loggcommiten, opp til `6e8a11f`.

### Åpne punkter
- Neste steg: story 2.4 «Startsiden får testmodus og knappen videre, og modusvalget lages» med egen branch og PR (`bmad-build`).
