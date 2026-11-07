# Mine valg og KI-feil jeg fant (epics og stories)

En kort oversikt over hva jeg bestemte selv da kravene ble delt opp i epics og stories, og hvilke feil som ble funnet i det KI-en laget. Tallene viser til radene i [prompt-loggen](../prompt-logg.md). Selve planen står i [`epics.md`](epics.md).

## Mine valg

1. **Åtte epics i fast rekkefølge.** Først det som aldri kuttes, så Korrektur og PDF, og til slutt det som står på nødlisten. Det som kuttes først, bygges sist. (208)
2. **Sidene skal synes i planen.** Jeg så at startsiden var vanskelig å finne. Nå har hver epic en linje som sier hvilke sider den bygger. (208, 210)
3. **Enkel utgave i chatten.** Storiene med alle kodene og filnavnene ble for rotete for meg. Jeg får en enkel utgave, og detaljene står i fila til den som skal kode. (209)
4. **Valgene KI-en tok, godkjente jeg:** testbrukeren `test@example.com`, at knappen «Begynn å lage søknad» kommer sammen med modusvalget, at Korrektur-kortet kommer i Epic 5, og at bryteren er låst på fram til ekte KI er koblet på. (209, 210)
5. **Pynten sist.** Fyrverkeri og annen pynt kommer etter punktene på nødlisten. (212)
6. **Ingen ekstra runde med flere agenter,** men en grundigere sluttsjekk. (213, 214)
7. **«Tilbake» fra resultatsiden er en del av kjerneflyten, og det kommer et testcase til.** Det gir litt mer arbeid, men PRD-en og suksesskriteriene krever det. (215)

## KI-feil jeg fant

1. **Steg 1 var ikke godkjent.** KI-en sa at jeg hadde godkjent kravlistene, fordi det sto i fila fra forrige økt. Det hadde jeg ikke. (206)
2. **Sidene var skjult bak kravnumre.** Epicene var skrevet ut fra kravnumrene, så det så ut som startsiden manglet. (208)
3. **For tekniske stories.** Den første utgaven hadde mange koder og filnavn, og det var vanskelig for meg å sjekke innholdet. (209)
4. **Den første sluttsjekken var for overfladisk.** Den sjekket bare at hvert kravnummer sto i en story. Den fant tre stories som ventet på en senere story (213), men ikke de åtte feilene som den grundige sjekken fant (214):
   - «Tilbake» fra resultatsiden lå i en epic som kan kuttes, men PRD-en lar bare kutte gjenbruken av nøkkelordlisten.
   - Det fantes bare ett testcase, men suksesskriteriene skal testes på 2–3, og kriterium 3 trenger samme CV med to ulike annonser.
   - `.gitignore` skjuler alle Word-filer, så testfilen av feil type ville aldri kommet med til sensor.
   - README skulle bare skrives i uke 50, men den skal oppdateres underveis og prøves fra en ny kopi før kodestopp.
   - I Epic 4 kunne testmodus slås av før brevet fra Claude fantes.
   - Et tidsavbrudd fra Claude ville vist «Nettverksfeil» i stedet for «Noe gikk galt hos KI-tjenesten».
   - CV med tabell var aldri prøvd, selv om arkitekturen sier at det skal gjøres.
   - Regelen om at KI-en skal skrive om KI-frasene i mitt eget brev (Korrektur) manglet.
5. **Feil i loggen fra forrige økt.** `/code-review` fant blant annet at loggen sier at en commit ikke er pushet, selv om den er det. (214)
