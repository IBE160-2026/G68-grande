# Story 7.5: logg ut før nedlasting, og arbeidsgiver i filnavnet

## 2026-11-20 kl. 19:54 — Kristine

### Oppgave
`/bmad-build 7.5` skulle lage siste story i epic 7. Når man trykker «Logg ut» på brevsiden før brevet er lastet ned, skal vinduet «Du har ikke lastet ned brevet.» komme først. Filnavnet skal bli `Soknad_<Arbeidsgiver>_<dato>`, med arbeidsgiveren renset (UX-DR17, UX-DR22, AD-11, retro 4 punkt B9).

### Plan
- `git fetch` ved start: ingen nye endringer på GitHub.
- KI-en spurte om storyen skulle deles i to (vinduet og filnavnet). Kristine valgte én story og sa ja til underagenter.
- Spec: [spec-7-5-logg-ut-for-nedlasting-og-arbeidsgiver-i-filnavnet.md](../../_bmad-output/implementation-artifacts/spec-7-5-logg-ut-for-nedlasting-og-arbeidsgiver-i-filnavnet.md) (kopi i `my-project/9-koding/`). Vinduet følger skissen `mockups/letter-page-1.html`. Det bruker `bekreft.js` fra «Nytt forslag».
- To valg fra KI-en, som Kristine godkjente med planen: flere bindestreker etter hverandre blir én, og uten JavaScript logges man ut med en gang. Hun beholdt hele spec-en (ca. 2 300 tokens).
- Branch `story-7-5-logg-ut-og-filnavn`. En underagent kodet, og tre underagenter gikk gjennom koden (blind, edge case, verification gap).

### Resultat
- `kjerne/filnavn.py`: `lag_filnavn(dato, endelse, arbeidsgiver=None)` renser arbeidsgiveren slik:
  - Æøå skrives om, og ß, ł, đ, þ og œ likeså. Andre tegn blir ASCII.
  - Mellomrom blir bindestrek, og annet fjernes.
  - Arbeidsgiveren får høyst 30 tegn.
  - `ruter.py` sender arbeidsgiveren med både ved nedlasting og på brevsiden.
- Vinduet før utlogging, i ny mal `vindu_logg_ut.html`:
  - «Logg ut» i `base.html` får `data-bekreft` bare når `advar_utlogging` er sann, altså på brevsiden før nedlasting.
  - `nedlasting.js` tar bort `data-bekreft` når brevet lastes ned.
  - Nye tekster står i `tekster.py`.
  - `stil.css` har fått en `:focus`-regel for «Avbryt».
- Nye testfiler: `test_vindu_logg_ut.py` og `test_filnavn_arbeidsgiver.py`. `test_filnavn.py` har flere tester. Eksisterende tester er oppdatert for `autofocus` på «Avbryt» og for det nye filnavnet.
- Gjennomgangen ga 16 punkter, ført i Review Triage Log i spec-en:
  - 5 rettet: ß, ł og andre slike bokstaver, to svake tester, en docstring og to kommentarer.
  - 1 utsatt i `deferred-work.md`.
  - 10 avvist. Blant dem er advarsel på resultatsiden: planen sier bare brevsiden. Også store bokstaver («BÆRUM» blir `BAeRUM`) og tankestrek ble avvist, fordi spec-en og AD-11 sier hva som skjer.
- 1 385 tester består, og `ruff check` og `ruff format --check` er rene.
- Commits på branchen: `cea817e` (story 7.5) og `359be61` (prompt-logg 493). Ikke pushet.
- Sprint-status: 7.5 = `review`, og retro-punkt 30 (rense arbeidsgiveren) = `done`. TO DO har et nytt punkt for 7.5, og 8.2-punktet nevner det nye vinduet. Notatet for refleksjonsrapporten er skrevet i `notater.md`.
- Løst i `issues.md`: «Story 7.5: `arbeidsgiver` renses før den brukes i filnavnet» (fra retrospektiven for epic 4).

### Åpne punkter
- Prøve story 7.5 i nettleseren, så push, PR med kommentar (med merknad om KI-feil), grønn CI og fletting. Dette skal prøves:
  - Brevsiden i begge modusene. «Logg ut» før nedlasting gir vinduet med fokus på «Avbryt». Esc og «Avbryt» lukker vinduet og gir fokus tilbake. «Logg ut» i vinduet logger ut.
  - Last ned, så «Bli her» og «Logg ut»: brukeren logges ut med en gang.
  - Etter «Nytt forslag» kommer vinduet igjen.
  - Filnavnet `Soknad_Testvik-Utvikling-AS_<dato>` i vinduet, linjen og fila.
  - Alt ved 375 og 1280 px og i høykontrast.
- Utsatt (`deferred-work.md`): ingen automatisk test kjører vinduet før utlogging i en nettleser. Det hører til issue #16 (story 8.2).

## 2026-11-21 kl. 12:04 — Kristine

### Oppgave
Kristine ba om å få nettsiden åpnet («åpne»), prøvde story 7.5 i nettleseren og sa «alt fungerer». Så skulle branchen pushes og PR-en lages.

### Plan
- Starte nettsiden fra branchen (`uv run flask --app soknad run`) og åpne den i nettleseren.
- Etter testen: stoppe nettsiden, oppdatere TO DO og prompt-loggen, pushe og lage PR med merknad om KI-feil og kommentar om nettlesertesten.

### Resultat
- Kristine prøvde vinduet før utlogging, utlogging med en gang etter nedlasting, vinduet igjen etter «Nytt forslag» og filnavnet med arbeidsgiveren. Alt virket.
- Nettsiden er stoppet.
- Commit `a8eef85`: TO DO (7.5 prøvd i nettleseren) og prompt-logg 494. Branchen er pushet.
- [PR #50](https://github.com/IBE160-2026/G68-grande/pull/50) er laget, med «Feil KI-en gjorde» og kommentar om nettlesertesten. CI kjørte da loggen ble skrevet.
- Løst i `issues.md`: prøve story 7.5 i nettleseren, push og PR (delvis: grønn CI og fletting står igjen).

### Åpne punkter
- Grønn CI og fletting av [PR #50](https://github.com/IBE160-2026/G68-grande/pull/50). Etter flettingen: 7.5 til ferdig i sprint-statusen, kopien og TO DO, og slette branchen `story-7-5-logg-ut-og-filnavn`.
