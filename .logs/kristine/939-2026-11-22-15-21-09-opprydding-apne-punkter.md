# Opprydding i de åpne punktene

## 2026-11-22 kl. 15:21 — Kristine

### Oppgave
Kristine ville bli helt ferdig med prosjektet før refleksjonsrapporten, og ba om å starte med de åpne punktene i `issues.md` mens hun ventet på testpersonen til kriterium 13. Hvert punkt ble forklart enkelt, og hun bestemte hva som skulle gjøres.

### Plan
- Krysse av punkter som alt var gjort, og føre beslutningene i story 8.2 inn i `epics.md`.
- Gå gjennom de sju åpne punktene ett for ett med Kristine.
- Punkt 2: lenke til startsiden når alle KI-kallene er brukt.
- Punkt 4: måle grensen på 5 000 tegn i Korrektur med ekte KI (ca. 3 kr, godkjent av Kristine: «ja gjør det»).
- Kristine prøver lenken i nettleseren.

### Resultat
Branch `opprydding-apne-punkter`, tre commits:
- `a3498a6`: punkter som alt var gjort, er krysset av i `todo.md`, `issues.md` og sprint-statusen (768/1280 px, de gamle risikopunktene, suksesskriteriene, punkter fra retro 2 og 4). Story 8.2 i `epics.md` (begge kopiene) har fått fem «Og»-linjer med beslutningene: ingen nettlesertester / #16, delingen i 8.2.1 og 8.2.2, tidspunktet for første prøve, steget «Hent koden» i README, og kriterium 13 gjort tidligere.
- `742aeb6`: feilboksen for «alle KI-kallene er brukt» har knappen «Lag ny søknad» (lenke til startsiden) på innleggingen og resultatsiden. Den er bevisst ikke på brevsiden, fordi GET / lager en ny søknad, og da ville brevet blitt borte uten spørsmål. Brevet kan lastes ned, og vinduet etter nedlastingen har «Lag ny søknad». Tester i `test_grenser.py` og `test_nytt_forslag.py`. Beslutningen er ført inn i story 4.3.2 i `epics.md`. 1416 tester bestått, ruff rent.
- `d5e95ed`: grensen på 5 000 tegn målt med ekte KI. Et eget brev på 4 954 tegn, med CV og annonse nær 15 000 tegn, ga 18 521 tokens inn og 10 000 ut, tok 68,6 s (`end_turn`), og `kontroller()` besto. Ca. 3,02 kr. Marginen er ca. 21 s og ca. 6 000 tokens. Ført inn i testplanen («Måling av grensen på 5 000 tegn») og i kommentaren i `innstillinger.py`. Skriptet og resultatet ligger i `my-project/testkjoringer/8-2/maling-5000/`.

Beslutninger fra Kristine:
- Punkt 1 (den tomme raden oppe til høyre): plager henne ikke, blir som det er.
- Punkt 3 (gap-analysen og kundekontakt når casene blandes), 5 (innlimt tekst over 500 KB) og 6 (nytt forsøk etter feil i gap): droppet.
- Punkt 7 (`GET /last-ned`): blir stående som kjent begrensning i README.

Nettleserprøven: nettsiden ble startet én gang med grensen satt til 2 KI-kall (et skript i scratchpad satte `okt.MAKS_KI_KALL = 2` før appen ble laget, koden ble ikke endret). Kristine så at «Lag ny søknad» kom i feilboksen og virket: «ser bra ut». Etterpå ble nettsiden stoppet. `MAKS_KI_KALL` er fortsatt 10 i koden.

Lukket i `issues.md`: punktene på linje 59, 118, 129, 159, 168, 179 og 194.

### Åpne punkter
- Flette PR-en for branchen `opprydding-apne-punkter` når CI er grønn.
