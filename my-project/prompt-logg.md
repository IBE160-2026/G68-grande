# Prompt-logg

De viktigste forespørslene jeg har gitt KI-en (Claude Code) i prosjektet, og hva de førte til. Prompts er gjengitt slik jeg skrev dem. Nye økter legges til nederst.

## 2026-10-07/08 – Revisjon av product brief etter faglærers tilbakemelding

Verktøy: Claude Code med BMAD-skillen `bmad-product-brief` (oppdatering). Alle beslutninger er logget i `brief-memlog.md`.

| # | Min prompt | Resultat |
|---|---|---|
| 1 | «hei, jeg har fått en tilbakmelding på productbriefen min, kan du hente ut denne fra GitHUb» | Hentet `tilbakemelding-product-brief.md` fra GitHub og oppsummerte den |
| 2 | «ser du hvilke problemer vi må endre på og løse før vi går videre på oppgaven. Ser jo nå at dette er et krevene prosjekt kun for meg og deg, så vi må gjøre det mer spesifikt og versjon 1 må ha mindre applikajsoner» | Liste over problemer og forslag til hva som kunne kuttes i versjon 1 |
| 3 | «vi tar kun norsk for å gjøre det enkelt, videre så vil jeg ha en enkel innloging […] versjon 1 lager kun søknad. Enig at vi må ha både PDF og tekst inn, og ut vil jeg ha word, samt PDF […]» | Beslutninger om språk, innlogging, input og output |
| 4 | «[…] var ikke klar over at disse tallene sto der […] Det fjerner vi også får det foreløpig stå litt mer generelt om statestikken. Foretrekker B på innlogging» | Udokumentert statistikk fjernet; registrering med e-post/passord valgt |
| 5 | «Ser nå at vi har 10 kriterier for versjon 1 som er enda mer enn det vi hadde og læreren sa det var for mye» | KI-en forklarte forskjellen og foreslo flere kutt; jeg valgte de endelige punktene selv |
| 6 | «jeg forstår ikke helt dette for å være ærlig, hvorfor har vi med nøkkelordtreff i utgangspunktet» / «men må jeg ha med gap analyse da?» | Forklaring og alternativer; jeg valgte å beholde begge, fordi nøkkelordtreff er testbart |
| 7 | «1) tror vi gjør det enklest mulig i versjon 1 […] 3) også vil jeg ha et eget punkt som tar for seg tone og språk» | Ingen lagring i versjon 1; eget punkt for tone og språk |
| 8 | «tror du kan gå over alle punktene å fjerne litt for ser ut som mye av det samme står både under løsning og under versjon 1» | Fjernet dobbeltbeskrivelser |
| 9 | «jeg legger også merke til at hvem dette er for og visjon blir stadig mindre» | KI-en hadde forkortet teksten min uten å spørre; originalteksten ble satt tilbake |
| 10 | «vent litt, jeg glemte jo å spørre om vi hadde gått over alle punktene som læreren hadde bedt oss om å se på» | Gjennomgang av tilbakemeldingen punkt for punkt; README, prompt-logg og begrunnelse for Word lagt til |

**Hva jeg lærte om å styre KI-en:** Det lønner seg å sjekke at KI-en ikke endrer mer enn jeg har bedt om, og å spørre når jeg ikke forstår et forslag i stedet for å godta det.

## 2026-10-09 – PRD (første utkast)

Verktøy: Claude Code med BMAD-skillen `bmad-prd` (veiledet vei, inngang: visjon + funksjoner). Alle beslutninger er logget i `prd-memlog.md`.

| # | Min prompt | Resultat |
|---|---|---|
| 1 | «Bruk Brief-en» | Visjonen ble hentet fra product brief, med min ordlyd |
| 2 | «dette er jo omtrent som produkt briefen, hva er forskjellen?» | Forklaring på forskjellen mellom brief og PRD; jeg valgte å beholde visjonen som den var |
| 3 | «en kjapp ting vi må få på plass, dette er en nettside ikke en app» | «appen» byttet til «nettsiden» i hele PRD-en |
| 4 | «i forhold til gruppe 3, kan du ta med dette i tankene når vi skal utforme denne delen?» (limte inn tilbakemelding om nøkkelordlisten) | Nøkkelordlisten lagres i økten og vises; KI-en pekte på at «rette nøkkelordlisten» var kuttet i briefen, og jeg valgte å beholde kuttet |
| 5 | «da velger i A) så får det være en del av neste versjon å ha med ordstamme-regel.» | Enkel telleregel i FR-17; ordstamme-regel satt på kuttlisten |
| 6 | «Nå begynte jeg å tenke litt, […] det stemmer jo at vi tillatter å legge inn brukerens egen søknad også. dette må oj komme som et alternativ tidligere i prosessen» | Modus velges tidlig (FR-20); jeg valgte at CV alltid er med, og «kun søknad» ble satt på kuttlisten |
| 7 | «spørsmål til gruppe 4, mener du det er bedre om de kan endre i nettleseren?» | Fordeler og ulemper; redigering i nettleseren satt på kuttlisten |
| 8 | «C) ingen topp eller bunnlinje i versjon 1, dette kommer senere» | Ingen topp- eller bunntekst i nedlastet fil (FR-30) |
| 9 | «jeg er ikke helt ferdig ennå ser jeg, vi må få inn at allerede på startsiden så i et hjørne så kan man switche til testmodus […]» | Bytte til testmodus på startsiden (FR-32) og samtykke til KI med avkrysningsboks (FR-36) |
| 10 | «Ja det er viktig, KI-en i nettleseren skal ikke komme med antagelser på vegne av brukeren» | Nytt krav FR-37 og suksesskriterium 11 |
| 11 | «du sier hvis tiden blir kanpp så fjerner vi fra kuttlisten. Men kuttlisten er jo en liste over ting vi allerede har kuttet?» | KI-en hadde formulert risikotiltaket feil; teksten ble rettet |
| 12 | «min forståelse er at det ikke vil havne i GitHub hvis den ligger i output?» | PRD-en kopiert til `my-project/prd.md`, slik at den committes underveis og sensor kan se historikken |
