# Story 2.7.1: Ventetegn og «opptatt»

## 2026-11-10 kl. 19:34 — Kristine

### Oppgave
Kristine startet `/bmad-build 2.7` for story 2.7 «Ventetegn og feil fra KI-en»: nettsiden skal vise at den jobber, ikke la brukeren trykke flere ganger, og gi en tydelig melding hvis KI-en feiler.

### Plan
- Spec for hele 2.7 ble ca. 2300 tokens. Kristine valgte å dele: 2.7.1 (ventetegnet og «opptatt» på serveren) nå, 2.7.2 (KI-feilboksen med «Det du har lagt inn, er ikke borte.» og «Prøv på nytt») senere. 2.7.2 står i `deferred-work.md`.
- Spec: `_bmad-output/implementation-artifacts/spec-2-7-1-ventetegn-og-opptatt.md` (godkjent av Kristine, «Godkjenn og fortsett»).
- Branch `story/2-7-1-ventetegn-og-opptatt`. Hovedøkta skrev koden selv, som i 2.3–2.6. Tre hjelpeagenter gikk gjennom koden (blind, grensetilfeller, testhull).

### Resultat
- Commit `ba1b956` på branchen (ikke pushet):
  - `kjerne/okt.py`: ny `sett_opptatt`.
  - `web/ruter.py`: POST på innleggingen sender til siden for steget når søknaden er opptatt, uten KI-kall. `opptatt` settes rundt KI-kallene, og `finally` lagrer én gang uten `opptatt` (med analysen når kallene lyktes).
  - `templates/ventetegn.html` (nytt), `base.html` (ny blokk etter `<footer>`), `innlegging.html` (`data-vente` på «Sjekk CV-en min», `vente.js`), `resultat.html` (`h1` får fokus).
  - `static/js/vente.js` (nytt): ventetegnet, `inert` på resten av siden, `aria-disabled` og fokus på knappen, stopper nytt trykk.
  - `css/stil.css`: ventetegnet, prikkene, låst knapp og høykontrast.
  - Tester: ny `tests/web/test_ventetegn.py` og en test i `test_okt.py`. 32 nye, 421 i alt, alle grønne. `ruff check` og `ruff format --check` grønne.
- Gjennomgang: 15 funn. 3 rettet (én lagring i `finally`, smalere `location`-sjekk, docstring), 1 utsatt (ingen test kjører `vente.js`), 11 avvist med begrunnelse i spec-en. «To POST-er samtidig» ble avvist i tråd med Kristines beslutning fra 2026-11-09 (låsingen av knappen løser det).
- Sprint-status: 2.7 står på «in-progress» til 2.7.2 er ferdig, som for 2.5.
- Kristine spurte hvorfor overskriften på resultatsiden kunne få en blå ring, og bestemte at den skulle bort: commit `aaa4549`, ny test, 422 i alt.
- Kristine prøvde i nettleseren med Slow 4G, og alt virket.
- Commit `5864d8f`: spec-kopi i `my-project/9-koding/`, oversikten, TO DO og prompt-logg 290–294. Notat i `8-refleksjonsrapport/notater.md` (ikke i Git, mappen er ignorert).
- Branchen er pushet, og [PR #15](https://github.com/IBE160-2026/G68-grande/pull/15) er laget med merknad om KI-feilen (den doble lagringen).

### Åpne punkter
- Story 2.7.1: [PR #15](https://github.com/IBE160-2026/G68-grande/pull/15) er laget. Gjenstår: grønn CI, flette, og sette 2.7.1 til ferdig i TO DO og oversikten.
- Story 2.7.2 «KI-feilboksen med «Prøv på nytt»» med egen branch og PR (`bmad-build`), etter at 2.7.1 er flettet.
- Ingen automatisk test kjører `vente.js`. Vurdere nettlesertester i story 8.2, sammen med `innlegging.js` og `info.js`.
