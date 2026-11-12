# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G68 – G68-grande |
| **PRD vurdert** | `my-project/2-prd/prd.md` (status `final`, sist endret 2026-11-07, commit a93ff79). Addendum i samme mappe er også lest. |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

Dette er en sterk PRD med en tydelig tese, ærlig konkurranseforståelse og krav som stort sett kan bli testtilfeller. KI-delen er godt kontrollert: telling i kode, gjenbrukt nøkkelordliste, testmodus, samtykke og kriterier som kjøres tre ganger. Risikoen ligger mest i fremdriften (milepælene er passert uten oppdatering) og i noen få hull som UX og story-arbeidet vil snuble i: ingen brukerreise, uspesifisert nøkkelordliste fra KI og kostnadsgrenser som er skjøvet til arkitekturen.

## 2. Dette fungerer godt

- **Ærlig tese og avgrensning (§1):** «Søknadsassistenten konkurrerer derfor ikke på antall funksjoner». Dere navngir konkurrentene, sier hva som er sjekket i dokumentasjon og hva som ikke er prøvd, og lander på en åpen telleregel og forklaringer til førstegangssøkere.
- **Testbare krav og kontroll av KI (§2.3, §5):** FR-17 har telleregel, eksempler («C» i «Kan C og Python», men ikke i «Center»), kjente begrensninger og avrunding. FR-28 lister når et KI-svar er ubrukelig. Suksesskriteriene har fasit og regel for tre kjøringer med ekte KI.
- **Prioritering som kan brukes i epics (§4):** kuttliste, «gjøres hvis det blir tid», nødliste i rekkefølge og «Kuttes aldri». Dette er sjeldent konkret og gjør rekkefølgen på stories nesten gitt.

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | sterk | Valg og avveininger står eksplisitt (Word framfor Markdown, ingen redigering i nettleseren, hva som avgjøres i UX/arkitektur). |
| Substans | sterk | Ingen pynt; konkurrentsammenligning og ATS-kilde er konkrete. |
| Strategisk sammenheng | sterk | Funksjonene tjener tesen (etterprøvbart treff + eget språk via Korrektur). |
| Testbarhet | god | De fleste FR-er har konkrete feilmeldinger og tall. Svakt for nøkkelordlisten fra KI og kostnadsgrenser. |
| Scope og avgrensning | god | Svært eksplisitt, men omfanget er stort for én person og datoene er ikke justert. |
| Brukbarhet for neste fase | god | FR/NFR-numre er komplette og krysshenvisningene stemmer. Mangler brukerreise, og noen begreper glir. |
| Formtilpasning | god | Passer et webprodukt med én rolle. Flyten er en pilkjede, ikke en reise med unntak. |

## 4. Viktigste forbedringer

### 4.1 Milepæler og status er utdatert
- **Alvorlighet:** høy
- **Hvor:** §7 «Merknad (3. november): Datoene ble ikke fulgt», §8 «Passer milepælsdatoene …», frontmatter `updated: 2026-10-12`, §6 sjekkpunktene 22. og 29. november.
- **Problem og hvorfor det betyr noe:** Tabellen viser «Innlogging og telleregel» 1. november og «PRD ferdig» 11. oktober, mens PRD-en selv sier at de ikke ble fulgt. Det åpne spørsmålet om datoene står uavklart, og frontmatter er eldre enn innholdet. Kutt-sjekkpunktene i §6 henger på datoer, så epics og sprintplan arver et uklart utgangspunkt.
- **Forslag:** Sett nye datoer baklengs fra levering 15. desember og oppdater `updated`. Eksempel: «Innlogging + telleregel med tester: 19. nov. Hele flyten i testmodus: 29. nov. Ekte KI: 4. des. Funksjonsstopp: 8. des.» Flytt sjekkpunktene tilsvarende og lukk det åpne spørsmålet.

### 4.2 Mangler en brukerreise som UX kan tegne fra
- **Alvorlighet:** medium
- **Hvor:** §2 «Flyten i korte trekk» og §1 «Hvem dette er for».
- **Problem og hvorfor det betyr noe:** Primærbrukeren er beskrevet, men ingen konkret person går gjennom flyten. Unntakene (skannet PDF, gap-analyse og treff som motsier hverandre, nytt forslag) ligger spredt i FR-ene. UX-skissene dere skal lage og kriterium 13 trenger én sammenhengende scene.
- **Forslag:** Legg til UJ-1 i en kort mal: «Mia, siste året på bachelor, søker sommerjobb. Hun logger inn, krysser av samtykke, velger «Forbedre mitt brev», limer inn CV, annonse og eget brev, ser at 6 av 10 nøkkelord treffer og at «SQL» mangler, bekrefter, leser brevet med markerte endringer og laster ned .docx. Unntak: PDF-en er skannet, og hun limer inn teksten.» Henvis til UJ-1 fra FR-ene.

### 4.3 Nøkkelordlisten fra KI er ikke spesifisert
- **Alvorlighet:** medium
- **Hvor:** FR-15, FR-17 «X av Y», kriterium 2.
- **Problem og hvorfor det betyr noe:** Hele «åpen telleregel»-tesen hviler på listen, men PRD-en sier ikke hvor lang den skal være eller hva som er et nøkkelord. Kriterium 2 tester bare telling med fast liste, ikke kvaliteten på listen KI-en lager. Én annonse kan gi 3 nøkkelord, en annen 40, og prosenten betyr da ulike ting.
- **Forslag:** Legg til konsekvenser i FR-15: «Listen har 8–20 nøkkelord, hvert på 1–3 ord, uten duplikater. Ligger listen utenfor dette, regnes svaret som ubrukelig (FR-28).» Legg til et kriterium: «For hver test-annonse inneholder listen minst de nøkkelordene fasiten markerer som obligatoriske.»

### 4.4 Kostnad og grenser for KI-bruk er utsatt
- **Alvorlighet:** medium
- **Hvor:** NFR-11 «Modell og kostnad avklares i arkitekturen», FR-12, §8.
- **Problem og hvorfor det betyr noe:** Filgrensen (5 MB) sier ingenting om hvor mye tekst som sendes til KI-en, og det finnes ingen øvre grense for antall KI-kall. Med egen API-nøkkel og «nytt forslag» (FR-25) kan kostnaden bli uforutsigbar, og arkitekturen får ingen mål å velge modell mot.
- **Forslag:** Sett rammer nå og la arkitekturen velge innenfor dem: «Hvert innleggingsfelt godtar maks 15 000 tegn. Maks 10 KI-kall per økt; deretter får brukeren en melding. Kostnad per fullført søknad måles i testplanen og skal ligge under 2 kr.» Tallene er eksempler.

### 4.5 Presiser telleregel og begrepene søknad og økt
- **Alvorlighet:** lav
- **Hvor:** FR-17 «må likevel stå som eget ord», FR-15/Ordliste «Økt», FR-12.
- **Problem og hvorfor det betyr noe:** «Eget ord» er udefinert for «C#», «C++» og «.NET», som er vanlige i IT-annonser, og testene vil kreve en avgjørelse. FR-15 sier at listen glemmes ved ny søknad, mens ordlisten definerer økt som innlogging til utlogging. «Søknad» brukes både om brevet og om arbeidsrunden, og er ikke i ordlisten. FR-12 sier 5 MB, men §8 sier at arkitekturen bestemmer.
- **Forslag:** Legg til tre testcaser i FR-17 («C#» i «Kan C# og SQL» = treff; «C» i «C#» = ikke treff, eller motsatt, velg og skriv det). Definer «Søknad» i ordlisten og skriv «per søknad» i FR-15. Fjern 5 MB fra §8-tabellen.

## 5. Mekaniske funn

- FR-1–FR-38 og NFR-1–NFR-12 er komplette uten duplikater. Rekkefølgen er bevisst forklart i §2.
- Ingen `[ASSUMPTION]`-tagger; antakelsene ligger i åpne spørsmål og «Avgjøres i UX og arkitektur». Det fungerer.
- Begrepsdrift: «annonse» / «stillingsannonse», «brev» / «søknadsbrev» / «søknad», og siden «Din ferdigstilte søknad!» er ikke i ordlisten.
- §8-tabellen bruker kolonnen «Når» til svar på avklarte spørsmål. Flytt dem til en «Avklart»-liste.
- FR-23 sier at endelig løsning bestemmes i UX, men FR-30 og kriterium 4 hviler på at markeringene finnes. Det er greit, men skriv hva som er minstekravet hvis UX-løsningen kuttes.
- PRD-en viser til «arkitekturen, AD-4», et dokument PRD-en ikke selv inneholder.
- PRD og addendum navngir én student i åpne spørsmål og UX-notater. Ikke noe sensitivt, men vurder å skrive «jeg» eller rolle.

## 6. Før dere går videre

**Må avklares før UX, arkitektur og epics:**
- Nye milepælsdatoer og nye kutt-sjekkpunkter (4.1).
- Nøkkelordlistens format (4.3) og tekst- og kall-grenser for KI (4.4), siden arkitekturen skal ta modellvalg ut fra dem.
- Minstekravet for markeringer i Korrektur, hvis UX-løsningen blir for tung.

**Kan vente:** filnavn, utseende, ventetid på KI, biblioteker for PDF/Word, struktur på testdata (alle er allerede riktig plassert i «Avgjøres i UX og arkitektur»).

**Oppfølging av briefen: ja.** Suksesskriteriene er nå testbare med fiktive CV-er og fasit, v1 er redusert og kuttlisten er tydelig, nøkkelordtreffet er regelbasert, ATS-tallet har kilde, og testmodus, lokal innlogging og skille mellom testdata og ekte CV-er er på plass. Valget av Word framfor Markdown er begrunnet.

## 7. Refleksjonsspørsmål

1. FR-17 forklarer at «Java» treffer i «JavaScript». Var dette en feil dere oppdaget ved testing, eller noe KI-en foreslo? Hvordan avgjorde dere at det er en akseptabel begrensning og ikke en feil som bør rettes?
2. 38 FR-er og en solo-innsats med fem uker igjen: hvilke tre FR-er ville dere kuttet først hvis KI-en dere koder med bruker dobbelt så lang tid som planlagt, og stemmer det med nødlisten i §4?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
