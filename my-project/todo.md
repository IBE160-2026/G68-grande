# TO DO

Ting som skal gjøres i prosjektet. Kryss av (`[x]`) når et punkt er gjort, og legg til nye punkter når vi oppdager dem.

## Ferdigstilling av PRD

- [x] Steg 1: gjennomgang av beslutningsloggen (memlog)
- [x] Steg 2: kildesjekk mot brief, faglærers tilbakemelding, sensorveiledning og brief-memlog
- [x] Kilder for Jobscan, Rezi, Teal og Kickresume i PRD og product brief
- [x] Oppdatere beslutningsloggen for briefen (`brief-memlog.md`) med endringene fra PRD-arbeidet
- [x] Steg 3: gjennomgang der hjelpere leser PRD-en kritisk og ser etter svakheter
- [x] Steg 4: gå gjennom de 9 antakelsene (`[ASSUMPTION]`) og bestemme hver av dem
- [x] Steg 5: språkvask og struktur av PRD og addendum
- [x] Steg 6–7: sette PRD-en til ferdig (`status: final`), og fjerne «(under arbeid)» i README-ene

## Andre åpne punkter

- [x] Spørre faglærer om product brief regnes som proposal
- [x] Skrive «Hva jeg lærte» i prompt-loggen
- [ ] Bestemme lista over typiske KI-fraser (FR-24, ligger i addendum)

## Etter PRD-en

- [ ] Prøve branch og pull request én gang med Claude før kodingen starter (for eksempel en liten endring i README)
- [x] UX (skisser av modusvalget og resultatsiden, se addendum)
  - [x] Utseende: farger (Myk fersken), former, bevegelse, skrift og logo
  - [x] Brukerreise 1: Ingrid, Full generering
  - [x] Brukerreise 2: Eirik, Korrektur på mobil
  - [x] Brukerreise 3: Henrik, sensor og testmodus
  - [x] Skisser av modusvalget og resultatsiden
  - [x] Skisser av alle sidene, på PC og mobil
  - [x] Ferdigstille DESIGN.md og EXPERIENCE.md
    - [x] Runde 1: dokumentene skrevet ut fra beslutningsloggen og skissene
    - [x] Runde 2: hull, motsigelser og antakelser gått gjennom
    - [x] Runde 3: kritisk gjennomgang (A sjekkliste + B tilgjengelighet + C sensor-blikk), alle funn bestemt og lagt inn i dokumentene
    - [x] Oppdatere skissene med endringene fra runde 2 (FR-18-linjen, rammefarge, bryter, tomme lister, logg ut-vindu, fast rad nederst, tekst for skannet PDF, ingen 🧪)
    - [x] Oppdatere skissene med endringene fra runde 3 (resultatsiden i Korrektur, feiltekst under feltet, filnavn i vinduet, ny ventetekst, felt side om side fra 1000 px, «1 setning er fjernet», ekte `@media` og prøve 768 px)
    - [x] Språkvask og sette dokumentene til ferdig (`status: final`)
- [ ] Arkitektur
  - [ ] Bestemme om logoskriften Baloo 2 lastes fra Google Fonts eller ligger som fil i prosjektet
  - [ ] Bestemme hva nettleserens egen tilbakeknapp gjør midt i en søknad
- [ ] Epics og stories

## Før innlevering

## Hvis tid

- [ ] Mørk modus (fargene er lagret som variabler, så den kan legges til uten å bygge om)

## Før innlevering

- [ ] Lage en kort prompt-logg med de viktigste valgene for hele prosjektet, til sensor (den lange loggen beholdes)
  - Ta med `3-ux/mine-valg-og-ki-feil.md` (UX er ferdig der), og legg til brief, PRD, arkitektur og koding
