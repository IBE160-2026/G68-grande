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

### Åpne punkter
- Story 2.5.2: prøve i nettleseren. Lim inn `cv.txt` og `annonse.txt` fra `backend/testdata/case-1-utvikler/` og se resultatsiden med fanetittelen «Resultat – Søknadsassistenten», 6 + 4 punkter og «7 av 11 = 64 %». Trykk F5 og se samme prosent. Skriv `/resultat` rett etter innlogging og havn på startsiden. Ingen rulling sidelengs ved 375 px. Deretter spec-kopi, oversikten, TO DO og prompt-logg, push, PR med merknad om KI-feil, grønn CI og fletting. Story 2.5 er da ferdig.
- Retro-punkt 7: funnet «to POST-er samtidig, den siste vinner» er nå avvist i to stories (2.5.1 og 2.5.2). Kristine bestemmer: la `opptatt` i story 2.7 løse det (forslaget), eller gjøre noe nå.
- Epic 4: `ki_svar.kontroller` bør fjerne tomme punkter i KI-svar, og KI-feil bør logges (oppgaven og feiltypen, aldri CV eller annonse).
