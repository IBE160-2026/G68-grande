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

## 2026-11-22 kl. 21:55 — Kristine

### Oppgave
Kristine ba om en gjennomgang av den utsatte lista (`deferred-work.md`) og av det som alt er gjort der.

### Plan
- Sjekket hvert av de 21 punktene uten «resolved» mot koden, spec-ene og sprint-statusen.

### Resultat
- 14 punkter var gjort, men ikke merket, og har nå `resolved` med bevis:
  - Sju var deler av stories eller runder som er flettet: 2.4.2, 2.5.2, 2.7.2, 4.3.2, småtingene og målingen fra retro 4, og runde C i retro 5.
  - Seks er rettet i koden: tomme punkter (to punkter), logging av KI-feil, `SIDE_FOR_STEG`, testen av `brev-2.json` og docstringen i `ki.py`.
  - Ett er avklart: Korrektur med case 2.
- Sju står igjen. To av dem er 8.2.2, og fem er små tekniske ting som ikke rettes før levering: tilbakeknappen rett etter innlogging, flere avsnitt i ett element, reglene i brev-prompten, sammenslåing av setninger på tvers av avsnitt i Korrektur, og etikettsjekken i CI.
- `deferred-work.md` ligger i `_bmad-output/`, som er git-ignorert, så bare loggen er committet.

### Åpne punkter
Ingen nye.

## 2026-11-22 kl. 22:12 — Kristine

### Oppgave
Kristine spurte om punktene i den utsatte lista som ikke er gjort, og ba om en setning under «Kjente begrensninger». Hun sa: «så lenge alle disse har en merknad eller begrunnelse ved seg så er det bra!»

### Plan
- Forklarte de sju punktene som står igjen (to for 8.2.2 og fem små tekniske ting). Hvert punkt har en begrunnelse (`evidence`) i `deferred-work.md`.
- La til ett punkt i README for den eneste tingen brukeren kan merke: reglene i brev-prompten.

### Resultat
- README, «Kjente begrensninger»: koden sjekker ikke at brevet fra Claude følger reglene i `backend/prompts/brev.md`. Punktet viser til de tre kjøringene mot fasiten (kriterium 11) og til den automatiske sjekken av KI-frasene i testsvarene.
- De fire andre tekniske punktene og etikettsjekken blir stående i den utsatte lista med begrunnelse. De rettes ikke før levering.

### Åpne punkter
Ingen nye.

## 2026-11-22 kl. 22:41 — Kristine

### Oppgave
Kristine spurte om alt som var utsatt nå er løst eller har en begrunnelse, bortsett fra 8.2.2. Så ba hun om push og logg.

### Plan
- Sjekket `deferred-work.md`, `my-project/todo.md` og `issues.md` en siste gang.

### Resultat
- Bekreftet: i den utsatte lista er alt løst eller har en begrunnelse, bortsett fra 8.2.2. I TO DO og `issues.md` står bare det som er planlagt, og det som er valgfritt:
  - Planlagt: refleksjonsrapporten neste helg (28.–29. november), så 8.2.2 rett før levering.
  - Valgfritt («Hvis tid»): mørk modus, å prøve konkurrentene selv, og kriterium 13 med én person til.
- Pushet til GitHub i denne økten:
  - `862c158`: mappestrukturen
  - `ba50bc4`: «Slik bruker du nettsiden»
  - `38b7580`: den kjente begrensningen om brev-prompten
- Main er lik GitHub.

### Åpne punkter
Ingen nye. Rekkefølgen videre er refleksjonsrapporten, så 8.2.2, så levering.
