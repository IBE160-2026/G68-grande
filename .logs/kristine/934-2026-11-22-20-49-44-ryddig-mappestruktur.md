# Ryddig mappestruktur

## 2026-11-22 kl. 20:49 — Kristine

### Oppgave
Kristine så at `my-project/` på GitHub hopper fra 7 til 9, fordi mappen med nr. 8 er git-ignorert. Ryddig mappestruktur gir poeng, så nummereringen skulle bli sammenhengende.

### Plan
- `git mv my-project/9-koding my-project/8-koding`, så historikken følger med.
- Den git-ignorerte mappen fikk nr. 9, og `.gitignore` er oppdatert.
- Alle henvisninger til `9-koding` er byttet ut i filene i repoet, i `_bmad-output/` og i KI-ens minne.

### Resultat
- Commit på main med `git mv` og 79 filer. Hver endret linje er bare mappenavnet, og linjeskiftene er beholdt.
- Ingen henvisninger til det gamle navnet er igjen.
- Alle relative lenker i `README.md` og `my-project/README.md` virker (sjekket med et skript).
- Den ignorerte mappen er fortsatt ignorert.
- Ikke endret: lenker i beskrivelsene av gamle PR-er på GitHub og Word-kopiene (`.docx`), som kan nevne det gamle navnet.

### Åpne punkter
Ingen.

## 2026-11-22 kl. 21:34 — Kristine

### Oppgave
Kristine spurte om README har en oppskrift på hele flyten, og senere om det er lenker til alt testmaterialet.

### Plan
- Sjekket README mot sensorveiledningen. Steg 3 sier at sensor går gjennom kjerneflytene som README beskriver, men README hadde ingen samlet oppskrift.
- Skrev avsnittet «Slik bruker du nettsiden» etter «Installasjon og oppstart». Knappenavnene, overskriftene og prosenten er sjekket mot `tekster.py` og `fasit.md`.

### Resultat
- README har fått åtte steg: innlogging, Full generering, innlegging, resultatsiden (10 av 20 = 50 %), brevet, nedlasting, Korrektur og feil input.
- Over stegene står en tabell med lenker til CV, annonse, eget brev og fasit for begge casene, og til filene som gir feil. Alle de 14 lenkene er sjekket.
- Kristine godkjente teksten.

### Åpne punkter
Ingen.
