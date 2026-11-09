# Story 2.5.2 – analysen og første resultatside

## 2026-11-09 kl. 22:49 — Kristine

### Oppgave
Kristine startet `bmad-build` for story 2.5.2, andre halvdel av story 2.5. Når CV og annonse er riktige, skal «Sjekk CV-en min» hente gap-analysen og nøkkelordlisten (testsvarene), lagre dem og vise en første resultatside med «X av Y = Z %».

### Plan
- Spec: `_bmad-output/implementation-artifacts/spec-2-5-2-analysen-og-forste-resultatside.md` (kopi i `my-project/9-koding/` kommer sammen med PR-en). Ingen åpne spørsmål. Ca. 1550 tokens, så ingen deling.
- Kristine spurte om «7 av 11 = 64 %» bare gjelder testen. Svar: ja, tallet kommer fra testcase 1. Egen tekst og ekte KI kommer i Epic 4 (4.1–4.4). Prosenten regnes alltid med telleregelen fra den lagrede listen.
- Kristine godkjente spec-en og ba meg fortsette. Branch `story/2-5-2-analysen-og-forste-resultatside`. Hovedøkta skrev koden selv, og tre hjelpere gikk gjennom den (blind, grensetilfeller, testhull).

### Resultat
- `kjerne/okt.py`: ny `sett_analyse`, som lagrer listen, den vaskede annonsen, arbeidsgiveren og gap-analysen. Steget blir minst resultat.
- `web/ruter.py`: «Sjekk CV-en min» kaller `nokkelord` og så `gap` når feltene er riktige, og sender til `/resultat`. En KI-feil gir innleggingen på nytt med feilteksten, og feltene er fortsatt fylt ut. Ny side `/resultat` (`resultat.html`) med «Slik passer CV-en din til stillingen», «Gap-analyse» med de to listene, og «Nøkkelordtreff» med «7 av 11 = 64 %».
- `web/flyt.py`: resultatsteget har nå en side. `web/tekster.py`: de nye tekstene.
- Tester: 28 nye, 361 i alt, alle grønne. `ruff check` og `ruff format --check` uten feil. Testen for suksesskriterium 2 leser tallene fra `fasit.md`. `FeilendeKI` ligger i `tests/web/hjelpere.py`, så story 2.7 kan bruke den.
- Gjennomgang: 14 funn. 9 er rettet (de fleste i testene, pluss en kommentar), 2 er utsatt til Epic 4 i `deferred-work.md` (tomme punkter i KI-svar og logging av KI-feil), og 3 er avvist. Testhull-laget fant ingen hull.
- Commit `083e295` på branchen (lokalt, ikke pushet). Sprint-status: story 2.5 står på `review`.
- Kristine prøvde resultatsiden i nettleseren, og alt så bra ut. Hun spurte om ventetegnet, som kommer i story 2.7.
- Commit `87f8687`: spec-kopi i `my-project/9-koding/`, oversikten, TO DO og prompt-logg 278–281. Notatet i `notater.md` er lagt inn (mappen er git-ignorert).

### Åpne punkter
- Story 2.5.2: grønn CI og flette [PR #13](https://github.com/IBE160-2026/G68-grande/pull/13). Deretter story 2.5 til `done` i sprint-statusen og TO DO.
- Retro-punkt 7: Kristine bestemte at låsingen av knappen (`opptatt`) i story 2.7 løser «to POST-er samtidig» (løst).
- Epic 4: `ki_svar.kontroller` bør fjerne tomme punkter i KI-svar, og KI-feil bør logges (oppgaven og feiltypen, aldri CV eller annonse).
