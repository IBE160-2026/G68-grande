# Kildesjekk: tilbakemelding fra faglærer mot PRD

| | |
|---|---|
| **Kilde** | `my-project/1-product-brief/tilbakemelding-product-brief.md` (faglærer, 2026-10-06) |
| **Sjekket mot** | `prd.md`, `addendum.md` og `.memlog.md` i denne mappen |
| **Dato** | 2026-10-10 |

Ting som er bevisst bestemt i memloggen, regnes ikke som hull. Rene forskjeller i ordlyd er ikke tatt med.

## Dekket (ingen tiltak)

- **Testbare suksesskriterier med fasit** (tilbakemeldingen, endring 1 og Neste steg 1): del 5 med 11 kriterier og 2–3 fiktive CV-er og annonser med fasit.
- **Redusert v1** (endring 2, forslag 1): bare søknadsbrev i begge moduser, gap-analyse og nøkkelordtreff, og PDF eller tekst inn. CV-generering, Word inn, maskinlesbarhet, engelsk og tone ligger på kuttlisten.
- **Word ut i stedet for Markdown**: avviker fra forslaget, men er et bevisst valg som er begrunnet i del 2.5. Ikke et hull.
- **Regelbasert nøkkelordtreff** (endring 3): FR-15–FR-17 og NFR-9.
- **Kilder til tallene i problemet** (del 1, The Problem): tallene er fjernet fra PRD-en.
- **Innlogging lokalt med testbruker, kryptering utsatt** (forslag 2): NFR-5, NFR-8 og kuttlisten.
- **Testmodus og nøkler** (Kjørbar for sensor, Avhengigheter): FR-32–FR-34, NFR-2 og suksesskriterium 7.
- **Fiktive CV-er, hemmeligheter og ekte CV-er utenfor Git** (kriterium 7): NFR-2 og NFR-3.
- **Data sendes til ekstern KI** (Sikkerhet og personvern): FR-35, FR-36 og NFR-4.

## Hull

### 1. Det er uklart om de KI-avhengige suksesskriteriene testes med ekte KI eller i testmodus — middels

- **Tilbakemeldingen:** Testbarhet: «det må finnes noe konkret å teste mot». Kontroll på KI-ens arbeid: «Mange prompts som må gi stabile resultater».
- **PRD-en:** Kriteriene 1, 3 og 11 (gap-analyse, brev tilpasset annonsen, ingen oppdiktet erfaring) avhenger av KI-en. I testmodus er svarene ferdiglagde, så der blir disse kriteriene oppfylt uansett. PRD-en sier ikke hvilken modus kriteriene skal kjøres i.
- **Forslag:** Skriv i del 5 at kriteriene 1, 3 og 11 sjekkes med ekte KI, og de øvrige kan kjøres i testmodus. Kriterium 2 bruker en fast nøkkelordliste fra testdataene.

### 2. Det er ikke beskrevet hva som skjer hvis KI-en svarer, men i feil form — middels

- **Tilbakemeldingen:** KI-funksjonalitet er vurdert som «Høy»: «… håndtering av usikre svar».
- **PRD-en:** FR-28 dekker bare tilfellet der KI-en ikke svarer (nettverksfeil eller annen feil). Det står ingenting om svar som ikke kan brukes, for eksempel en nøkkelordliste som ikke kan leses, en tom liste eller en gap-analyse uten de to listene.
- **Forslag:** Utvid FR-28, eller legg til et nytt krav: hvis KI-svaret ikke har forventet form, får brukeren feilmeldingen «prøv på nytt», og det brukeren har lagt inn, er fortsatt der. Kan testes med et ødelagt testsvar i testmodus.

### 3. V1 sier ikke hva som kuttes først hvis tiden blir knapp — middels

- **Tilbakemeldingen:** Tid og omfang er vurdert som «Stor risiko … særlig for én person». Og: «Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer». Kjerneflyten er: last opp CV og annonse, få gap-analyse og brev, last ned.
- **PRD-en:** Risiko 2 sier at «kjerneflyten kuttes aldri», men det står ikke hvilke v1-funksjoner som er utenfor kjerneflyten og kan kuttes først. Eksempler er Korrektur med markerte endringer, PDF ut i tillegg til .docx, bytte av testmodus på nettsiden og tilpasning til nettbrett og mobil. Memloggen fører dette som et åpent, valgfritt punkt, så det er ikke bestemt.
- **Forslag:** Legg en kort prioritert liste i del 4 eller risiko 2 over hva som kuttes først, og skill tydelig mellom kjerneflyt og resten av v1.

### 4. Det er ikke valgt KI-tjeneste, og kostnad er ikke nevnt — middels

- **Tilbakemeldingen:** Neste steg 3: «velg KI-tjeneste med plan for testmodus før dere lager PRD». Avhengigheter og kostnader: «Planlegg nøkkelhåndtering, kostnad og en testmodus».
- **PRD-en:** Nøkkelhåndtering (NFR-2) og testmodus (FR-32) er dekket. Hvilken KI-tjeneste som skal brukes og hva den vil koste, står verken i PRD-en eller i addendumet.
- **Forslag:** Før det opp i addendumet under «Til arkitektur»: velge KI-tjeneste og begrunne valget, og anslå kostnaden for utvikling og testing. Alternativt kan PRD-en ha et krav om at sensor ikke trenger en betalt konto (er delvis dekket av FR-32).

### 5. PDF med kolonner og tabeller, og valg av biblioteker, er ikke ført videre — lav

- **Tilbakemeldingen:** Filhåndtering er vurdert som «Høy»: «Pålitelig lesing av CV-er med kolonner og tabeller er krevende». Kriterium 5: «Velg få og godt dokumenterte biblioteker for fillesing og eksport, og begrunn valgene i arkitekturen».
- **PRD-en:** FR-11 dekker skannede PDF-er. CV-er med kolonner og tabeller er ikke nevnt. Suksesskriterium 5 (PDF og innlimt tekst gir samme treff) kan feile for slike CV-er. Under «Til arkitektur» i addendumet står bare filstørrelsen.
- **Forslag:** Legg til under «Til arkitektur»: biblioteker for å lese PDF og lage .docx og PDF, med begrunnelse. Bestem om en av de fiktive test-CV-ene skal ha to kolonner, eller skriv ned enspaltet CV som en kjent begrensning.

### 6. Skisser av modusvalget og visningen av gap-analysen er ikke ført videre til UX — lav

- **Tilbakemeldingen:** Kriterium 4: «Skisser hvordan valget mellom modusene og visningen av gap-analysen ser ut.»
- **PRD-en:** FR-14, FR-16, FR-18 og FR-20 beskriver innholdet. Under «Til UX» i addendumet står ingenting om disse to skjermbildene.
- **Forslag:** Legg et punkt under «Til UX» i addendumet om at modusvalget og resultatsiden (gap-analysen, nøkkelordlisten og forklaringen fra FR-18) skal skisseres.

### 7. «ATS-delen» står fortsatt i risikotabellen — lav

- **Tilbakemeldingen:** Endring 3: ATS-vurderingen må defineres konkret.
- **PRD-en:** Maskinlesbarheten er kuttet, og nøkkelordtreffet er definert. Likevel står «ATS-delen» i risiko 1, og det kan få leseren til å tro at det fortsatt finnes en egen ATS-score i v1.
- **Forslag:** Skriv «Gap-analysen og nøkkelordtellingen er vanskelig å få til» i risiko 1, eller forklar at nøkkelordtreffet er det som er igjen av ATS-vurderingen.

### 8. Problemet er ikke knyttet til norske forhold — lav

- **Tilbakemeldingen:** The Problem: «knytt gjerne problemet til norske forhold».
- **PRD-en:** Problemet er beskrevet generelt. Det er nevnt at brevet skrives på norsk (FR-24), men ikke norske forhold.
- **Forslag:** Faglærer skrev «gjerne», så dette er valgfritt. Eventuelt kan én setning om norske studenter og norske stillingsannonser legges til.

## Ikke PRD-innhold

- **Commit utkast og mellomversjoner, og lagre promptene** (kriterium 1): gjøres allerede, se `my-project/` og memloggen. NFR-10 dekker promptene i selve nettsiden.
- **Oppdater product brief i repoet** (siste avsnitt): gjelder briefen, ikke PRD-en.
- **Begrunn teknologivalg i arkitekturen** (kriterium 5): hører hjemme i arkitekturen, se hull 4 og 5.
