# Suksesskriterier og sensorveiledning

## 2026-11-03 kl. 22:17 — Kristine

### Oppgave
Gå gjennom målene for prosjektet (suksesskriteriene), få en ærlig vurdering av brief og PRD, og sjekke at det jeg har gjort, passer med sensorveiledningen. Bekymringene og hullene som kom fram, skulle løses i dokumentene, ikke bare noteres. Til slutt: sjekke at konkurrentanalysen ikke kræsjer med brief, PRD eller UX.

### Plan
- Vise suksesskriteriene fra PRD-en (del 5). Milepældatoene i del 7 ses det bort fra.
- Ærlig vurdering av brief og PRD, med fem bekymringer lagret i `my-project/todo.md`.
- Sammenligne repoet med `Sensorveiledning.pdf` (sju kriterier) og rette hullene.
- Prøve branch og pull request én gang før kodingen.
- Løse de fem bekymringene én og én.
- Sammenligne konkurrentanalysen med brief, PRD og UX.
- Oppdatere README og prompt-loggen.

### Resultat
- **Bekymringer lagret** i `todo.md` (`2becca8`), og alle fem er løst:
  1. Omfang: to sjekkpunkter, 22. og 29. november, i risikotabellen i PRD-en, i stedet for regelen om forsinkede milepæler (`cb588bd`).
  2. KI-kriterium som feiler: plan B i innledningen til del 5 i PRD-en. Nye punkter i `todo.md`: teste promptene tidlig når de ekte KI-svarene til testmodus lages (FR-38), og lage testdata med tydelige hull (`bd22d65`).
  3. Fasit: NFR-3 krever en kort begrunnelse for hvert krav (`a967e9f`).
  4. Kriterium 13: «en person som ikke kjenner prosjektet» i stedet for «en medstudent», fordi jeg studerer på nett. Det blir en kollega (`702a54e`).
  5. Kilde på ATS: Harvard Business School Working Knowledge (Fuller, 2021) under Kilder i brief og PRD (`bca873b`). Tallet ble sjekket mot kilden: 63 % av arbeidsgiverne bruker et rekrutteringssystem, og over 90 % av dem bruker det til første utvalg. KI-en hadde først sagt «over 90 % av arbeidsgiverne», og det var feil.
- **Sensorveiledningen:** Planleggingen og prosessen passer godt. Hullene som ble rettet:
  - README lenker til alle plan- og prosessdokumentene (`ba955e3`).
  - Merknad under milepælene i PRD-en om hvorfor datoene ikke ble fulgt, med min forklaring (`ba955e3`).
  - NFR-8: README skal si hvem nettsiden er for. Gjort som **første pull request, PR #1**, som jeg merget selv (`a65bfe8`, merge `640eea4`). KI-en laget branchen uten å spørre først, og det står i PR-en og i prompt-loggen.
- **Konkurrentanalysen** kræsjer ikke med noe. PRD-en fikk en forsiktig formulert setning om norsk og KI-korrektur som fortrinn, og NFR-8 et krav om kjente begrensninger. Konkurrentanalysen sier nå hva den førte til (`5bace46`).
- **README** har nå hva nettsiden gjør, hvem den er for og kjente begrensninger, og overskrifter merket «kommer» for det som avhenger av koden (`3f7a5f4`).
- **Prompt-loggen:** prompt 175–193 og «Hva jeg lærte» for 3. november (`8beec49`).
- **Hva blir vanskelig å kode:** tre krevende punkter (markerte endringer i Korrektur, PDF-lesing, at testmodus kjenner igjen testdataene) og tre middels punkter (fast KI-format, PDF med æøå, telleregelen med æøå). Alle står i `todo.md` under arkitektur, sammen med to raske prøver før stories (`b2367ab`). Alt ble pushet til GitHub.
- **TO DO:** krysset av for første PR (`4170d38`). Nye seksjoner: «Under kodingen» med sjekkpunktene, og README-punktet under «Før innlevering».

### Åpne punkter
- Avtale med en kollega innen 20. november for kriterium 13. Testen gjøres etter 29. november.
- Sjekkpunkt søndag 22. november: virker innloggingen, telleregelen med tester og innleggingssiden? Hvis ikke, kutt punkt 1–3 på nødlisten.
- Sjekkpunkt søndag 29. november: virker hele flyten i testmodus? Hvis ikke, kutt punkt 4–5 på nødlisten.
- Stories: når de ekte KI-svarene til testmodus lages (FR-38), kjøre hver prompt tre ganger og sjekke mot fasiten.
- Testdata: lage CV-er med tydelige hull, ikke grensetilfeller.
- Før innlevering: fylle ut README-seksjonene merket «kommer», og legge til nye kjente begrensninger.
