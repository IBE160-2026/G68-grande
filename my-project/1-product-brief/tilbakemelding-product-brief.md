# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G68 – G68-grande |
| **Product brief** | `my-project/product-brief.md` (commit `9dc5735`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

Vurdert fil: `my-project/product-brief.md`, som er den eneste briefen i repoet. Det finnes ennå ikke PRD, arkitektur eller epics på main. Repoet har GitHub Actions for testing og BMAD-oppsett.

## Samlet vurdering

- **Bør revideres før dere går videre.** Rett punktene markert «Endre» før dere lager PRD og arkitektur.

**Det som er bra:**

1. Briefen er godt skrevet og har en tydelig profil: studenter og nyutdannede som søker jobb for første gang, og to moduser, «Full generering» og «Korrektur». Begrunnelsen for Korrektur-modusen (at helt KI-genererte søknader blir generiske) er et reflektert valg som skiller dere fra en vanlig chatbot.
2. Dere tar personvern på alvor og skriver at CV-er og søknader er sensitive personopplysninger som «bør behandles som en reell del av produktet». Den ærlige vurderingen av at fortrinnet er fokus, ikke teknisk sofistikasjon, er også bra.

**De viktigste endringene:**

1. Gjør suksesskriteriene testbare. Dere skriver at kriteriene «holdes bevisst kvalitative … uten tallfestede terskelverdier», og «hele flyten fungerer feilfritt» kan ikke sjekkes. Legg til funksjonelle kriterier som kan bli testtilfeller, for eksempel «en CV i PDF og en annonse gir en gap-analyse som lister minst de tre kravene i annonsen som ikke står i CV-en». Lag to–tre fiktive CV-er og annonser med fasit.
2. Reduser omfanget av v1. Listen har ni punkter, og flere er store hver for seg: to moduser for både CV og søknadsbrev (fire kombinasjoner), lesing av PDF og Word, eksport til tre formater, to språk, ATS-vurdering i tre deler og innlogging med kryptert lagring. Velg en kjerneflyt først, for eksempel søknadsbrev i begge moduser pluss gap-analyse, med PDF/tekst inn og Markdown/PDF ut.
3. Definer ATS-vurderingen konkret. «Maskinlesbarhet» og «treffscore» høres presise ut, men hvordan beregnes de? Hvis en språkmodell bare «gir en score», kan dere ikke kontrollere den. Gjør nøkkelordtreffet regelbasert (andel av annonsens nøkkelord som finnes i CV-en), slik at det kan testes.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** 2) AI CV- og søknadsassistent (middels). Briefen er en utvidet versjon av dette forslaget, med to moduser og ATS-vurdering i tre deler.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Middels | Gap-analyse og ATS-score krever definerte regler. Uten definisjon blir dette uklart og vanskelig å kvalitetssikre. |
| Datamodell – antall entiteter og relasjoner mellom dem | Middels | Bruker, CV, stillingsannonse, søknad, generert dokument og analyse. |
| Brukere, roller og innlogging | Middels | Én rolle, men innlogging og kryptert lagring er krav. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Høy | Generering og korrektur for to dokumenttyper, to språk og valgfri tone, pluss gap-analyse. Mange prompts som må gi stabile resultater. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Middels | Språkmodell-API, og eventuelt en innloggingstjeneste. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Ingen. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Høy | Lesing av PDF og Word, og eksport til DOC, Markdown og PDF. Pålitelig lesing av CV-er med kolonner og tabeller er krevende. |
| Sikkerhet og personvern | Høy | CV-er inneholder navn, kontaktinfo og arbeidshistorikk. Kryptert lagring og innlogging må gjøres riktig, og data sendes til en ekstern KI-tjeneste. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer. Her er kjerneflyten: last opp CV og annonse, få gap-analyse og et skreddersydd søknadsbrev, og last det ned.

### Gjennomførbarhet med BMAD og Claude Code

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | Stor risiko | Som beskrevet er v1 stort, særlig for én person. Med redusert omfang er det realistisk. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Funksjonene er tydelig listet, men ATS-vurderingen og suksesskriteriene er for uklare til å bli presise krav. Det blir også mange stories med dagens omfang. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | Webapp med filopplasting, API-kall og eksport er godt egnet, selv om fillesing og eksport krever ekstra biblioteker. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Risiko | Dere kan vurdere om et søknadsbrev er godt. Men om en «ATS-score» er riktig, er vanskelig å vite uten en definert regel. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | Stor risiko | Suksesskriteriene er bevisst kvalitative, og ingen regler er definert. Lag fasiteksempler og regelbasert nøkkelordtreff. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | Risiko | Krever språkmodell-nøkkel og eventuelt innloggingstjeneste. Ingen plan for testmodus ennå. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | Risiko | Ikke beskrevet. Planlegg nøkkelhåndtering, kostnad og en testmodus med ferdige svar. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. V1: søknadsbrev i begge moduser, gap-analyse og regelbasert nøkkelordtreff. CV inn som PDF eller tekst, resultat ut som Markdown eller PDF. Legg CV-generering, Word-lesing, DOC-eksport og maskinlesbarhetsvurdering i neste trinn.
2. Start med enkel innlogging med ferdige testbrukere og lokal database, og vurder kryptering etter at kjerneflyten virker. Bruk bare fiktive CV-er i repoet og i testing.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Klart: skreddersydd CV og søknadsbrev med to moduser, gap-analyse og ATS-vurdering. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | Juster | Godt beskrevet, men tallene (97,8 % av Fortune 500, 99,7 % av rekrutterere) mangler kilde. Oppgi kilde eller fjern tallene, og knytt gjerne problemet til norske forhold. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | OK | Beskriver tydelig hva brukeren gjør og får (tekst og innsikt). |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Ærlig sammenligning med Jobscan, Rezi, Teal og Kickresume, og en nøktern vurdering av eget fortrinn. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | OK | Tydelig primærbruker med konkrete behov (oversette utdanning og prosjekter til kvalifikasjoner). |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Endre | Bevisst kvalitative og ikke testbare. Legg til funksjonelle kriterier med fasiteksempler. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Endre | Tydelig inn/ut, men alt står som «inkludert i produktet» uten skille mellom v1 og senere. Del i v1 og neste trinn, og reduser v1. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Kort og knyttet til kjerneverdien. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | README i `my-project` sier at BMAD-utkast bare ligger på deres PC. Sensor vurderer prosessen i repoet, så commit også utkast og mellomversjoner, ikke bare ferdige dokumenter. Lagre promptene. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Endre | For stort som beskrevet. En redusert v1 gir fortsatt rikelig funksjonalitet. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Endre | Kvalitative kriterier gir ikke testtilfeller. At dere allerede har satt opp GitHub Actions er bra, men det må finnes noe konkret å teste mot. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | OK | Tydelig bruker og flyt. Skisser hvordan valget mellom modusene og visningen av gap-analysen ser ut. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Teknologi er ikke valgt. Velg få og godt dokumenterte biblioteker for fillesing og eksport, og begrunn valgene i arkitekturen. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | Juster | Planlegg testmodus for KI og innlogging som virker lokalt uten ekstern tjeneste. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Struktur med README i hver mappe er ryddig. Legg fiktive test-CV-er i en egen mappe, og sørg for at nøkler og ekte CV-er aldri havner i Git. |

## 3. Neste steg for gruppen

1. Skriv om suksesskriteriene til funksjonelle, testbare kriterier med to–tre fiktive CV-er og annonser som fasit.
2. Del Scope i v1 og neste trinn, og reduser v1 til søknadsbrev, begge moduser, gap-analyse og regelbasert nøkkelordtreff.
3. Definer hvordan ATS-vurderingen beregnes, og velg KI-tjeneste med plan for testmodus før dere lager PRD.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
