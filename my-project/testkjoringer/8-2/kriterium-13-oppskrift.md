# Oppskrift: kriterium 13

**Kriteriet (PRD del 5):** En person som ikke kjenner prosjektet, helst en student eller noen som har søkt jobb nylig, ser resultatsiden for en av test-CV-ene, og kan med egne ord forklare hva som mangler i CV-en, og hva nøkkelordtreffet betyr og ikke betyr.

## Før testen

1. Velg en person som ikke har sett nettsiden før, helst en student eller noen som har søkt jobb nylig.
2. Start nettsiden, logg inn med testbrukeren og slå på testmodus.
3. Velg Full generering, og lim inn `cv.txt` og `annonse.txt` fra `backend/testdata/case-1-utvikler/`.
4. Gå til resultatsiden. Den skal vise 50 %.

Testen kan gjøres ved siden av hverandre, på Teams med delt skjerm, eller med et skjermbilde av hele resultatsiden.

## Under testen

Si bare dette: «Dette er en side som sammenligner en CV med en stillingsannonse. Se på siden, og ta den tiden du trenger.»

- Ikke forklar noe på siden, og ikke pek på noe.
- Personen kan gjerne trykke på «i»-knappene og «Hva er ATS og hva betyr det for deg?». De er en del av siden.
- Still så de to spørsmålene, og skriv ned svaret med personens egne ord:
  1. «Hva mangler i CV-en?»
  2. «Hva betyr 50 % her, og hva betyr det ikke?»

Ikke rett på personen eller gi hint underveis. Er noe uklart, skriver du det ned. Det er et funn.

## Fasit (bare for deg, ikke vis den)

**Spørsmål 1:** gap-analysen i testmodus sier at CV-en mangler SQL og relasjonsdatabaser, Docker, smidig utvikling (Scrum) og førerkort klasse B.

**Spørsmål 2:**
- Hva 50 % betyr: 10 av 20 nøkkelord fra annonsen står i CV-en. Det er en ordtelling.
- Hva 50 % ikke betyr: ikke sjansen for å få jobben, ikke en karakter på CV-en og ingen garanti. Ord som betyr det samme, men skrives annerledes, telles ikke. For eksempel har CV-en «bachelor», men ikke «bachelorgrad».

## Bestått når (godkjent av Kristine 22. november 2026)

- **Spørsmål 1:** personen nevner det som mangler, med egne ord. Alle fire må ikke nevnes, men svaret må vise at personen fant listen «Dette kan du jobbe videre med» og forsto den.
- **Spørsmål 2:** personen sier at prosenten teller ord fra annonsen som står i CV-en, og at den ikke er en garanti, en karakter eller sjansen for å få jobben.

Resultatet føres inn i tabellen «Kriterium 13» i `my-project/testplan.md`: dato, hvem (ikke navn, for eksempel «student, økonomi»), hva personen forklarte, og bestått eller ikke bestått.
