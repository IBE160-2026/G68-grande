---
title: 'Adversarial gjennomgang av ARCHITECTURE-SPINE.md'
reviewed: 'ARCHITECTURE-SPINE.md (draft, 2026-11-04)'
lens: 'Motstander: to enheter som følger alle AD-er til punkt og prikke, men likevel ikke passer sammen'
date: '2026-11-04'
---

# Adversarial gjennomgang — Søknadsassistenten

## Dom

Ryggraden er god på lagdeling, KI-former og feilklasser, men den **beskriver data med ord og ikke med navn**. Øktobjektet (AD-7), `steg` (AD-8) og feiltypene (AD-9) er de tre stedene der to stories som begge følger reglene, kan bygge ting som ikke passer sammen. For en nybegynner som koder med en KI-assistent, økt for økt, er dette det mest sannsynlige stedet for feil: hver ny KI-økt finner på sine egne feltnavn og sin egen tolkning av «steg».

Ingen av hullene krever ny arkitektur. Alle lukkes med en strammere regel eller én ny liten kjernefil.

## Slik er hullene funnet

For hvert hull er det laget to enheter ett nivå ned (to stories eller to moduler, laget i hver sin KI-økt). Begge følger alle AD-ene bokstavelig. Så vises hvor de kolliderer, og hvilken minste regel som lukker hullet.

Alvorlighet: **Kritisk** = flyten brytes, og det merkes først når stories settes sammen. **Høy** = sannsynlig feil som gir krasj eller feil resultat i et suksesskriterium. **Middels** = feil i kanttilfeller eller ved sensors første kjøring. **Lav** = kosmetisk eller lett å rette.

---

## H1 — Øktobjektet har ingen fast form · Kritisk

**AD-er som følges:** AD-7 lister innholdet med ord: «modus, steg, CV, annonse, eget brev, nøkkelord, gap, brev, lastet ned, samtykke, testmodus».

**Enhet A — story «Innlegging» (FR-8–FR-13):** lagrer `okt["cv"] = tekst` og `okt["annonse"] = tekst`, og brukerens eget brev som `okt["brev"]` (det heter jo «brev» i skjemaet).

**Enhet B — story «Brevside» (FR-22–FR-25):** lagrer det ferdige brevet fra KI som `okt["brev"] = {"avsnitt": [...]}`, og i Korrektur `okt["brev"] = {"setninger": [...]}`.

**Kollisjon:**
- «Eget brev» og «brev» havner på samme nøkkel. «Nytt forslag» i Korrektur skal bruke det opprinnelige brevet (AD-5), men det er overskrevet.
- Story «Nedlasting» leser `okt["brev"]["avsnitt"]` og krasjer i Korrektur, der formen er `setninger`.
- Når brukeren går tilbake til innleggingen (FR-19), skal UX vise filnavnet med ✓ (EXPERIENCE.md linje 198, 266). Enhet A lagret bare teksten, så siden kan ikke vise «cv.pdf ✓». En tredje story legger til `okt["cv_fil"]`, en fjerde `okt["cv_filnavn"]`.
- Arbeidsgiveren fra `nokkelord`-kallet (AD-4) står ikke i lista i AD-7. Analyse-storyen lagrer bare `okt["nokkelord"] = liste`, og filnavn-storyen finner ingen arbeidsgiver.
- Feltene som AD-8 og AD-10 forutsetter (låsen for pågående KI-kall, hvilket testcase som er gjenkjent, hvilket forslag som vises), finnes ikke i lista. Hver story finner på sitt eget.

**Minste regel (stram AD-7):**
> Øktdata har én form, definert som dataklasser i `soknad/kjerne/okt.py` (ren Python, ingen Flask). `oktlager.py` lagrer bare instanser av den. Ingen kode bruker `okt["..."]` med strengnøkler. Formen er delt i to:
>
> - `Innlogging`: `bruker_id`, `testmodus: bool`, `soknad: Soknad`
> - `Soknad`: `steg`, `modus` (`full` | `korrektur`), `cv`, `annonse`, `eget_brev` (hver av typen `Inndata(tekst: str, filnavn: str | None)` eller `None`), `samtykke: bool`, `testcase: str | None`, `nokkelord: NokkelordSvar | None` (hele AD-4-svaret, med arbeidsgiver), `nokkelord_annonse: str | None`, `gap: GapSvar | None`, `brev: BrevSvar | None`, `korrektur: KorrekturSvar | None`, `forslag: int`, `lastet_ned: bool`, `ki_pagar: bool`
>
> Nye felt legges til i `okt.py`, aldri i en rute.

---

## H2 — Ingen eier `steg`, og «riktig steg» kan tolkes på to måter · Kritisk

**AD-er som følges:** AD-8: «Hver side sjekker innlogging og steg, og sender brukeren til riktig side hvis steget ikke passer.» UX (linje 257): «Kommer til startsiden → det starter alltid en ny søknad med tomme felt.»

**Enhet A — story «Analyse og resultatside»:** sjekker `if okt.steg != "resultat": redirect(...)`. Steget settes til `resultat` *før* KI kalles, «så siden er klar».

**Enhet B — story «Tilbake-knapper» (FR-19):** «Tilbake» på resultatsiden er en lenke (GET) til `/innlegging`. Innleggingssiden sjekker `okt.steg == "innlegging"`, ser `resultat`, og sender brukeren tilbake til resultatsiden. FR-19 virker ikke.

**Enhet C — story «Startside»:** følger UX bokstavelig og tømmer søknaden i `GET /start`. Nettleserens tilbakeknapp eller en bokmerket `/start` midt i en søknad sletter da alt, mens AD-8 sier at brukeren skal sendes til riktig side.

**Kollisjon:**
- «Passer» kan bety *likt* (`==`) eller *ikke lenger fram enn* (`<=`). To stories velger ulikt.
- Settes steget før KI-kallet og kallet feiler, står økten på `resultat` uten gap (AD-9 sier «alt beholdes»), og resultatsiden krasjer på `None`.
- En GET som endrer tilstand, bryter med hele poenget med POST → redirect → GET.

**Minste regel (stram AD-8):**
> `soknad/kjerne/steg.py` eier stegene som en ordnet liste og to funksjoner:
> - `kan_vise(side, steg) -> bool`: en side kan vises når den ikke ligger etter `steg` (`side <= steg`). Brukeren kan altså alltid gå bakover med GET, aldri forover.
> - `ga_til(soknad, nytt_steg)`: den eneste måten å endre `steg` på. Kalles bare fra en POST, og bare **etter** at KI-kallet og kontrollen har lyktes.
>
> GET endrer aldri økten. Søknaden tømmes i `POST /begynn` («Begynn å lage søknad»), ikke når startsiden vises. Startsiden viser alltid tom samtykkeboks uansett hva som ligger i økten, så UX-kravet om tomme felt og ny samtykke er oppfylt.

---

## H3 — Hvem tømmer gamle resultater når inndata endres? · Høy

**AD-er som følges:** AD-6 (nøkkelord hentes på nytt bare når annonsen er endret), AD-7 («Lag ny søknad tømmer søknaden»), FR-19.

**Enhet A — story «Innlegging»:** ved ny POST fra innleggingen erstattes `cv` og `annonse`. Ingenting annet røres.

**Enhet B — story «Gjenbruk av nøkkelordlisten» (FR-19):** sammenligner `okt.annonse` med den nye annonsen som rå tekst.

**Kollisjon:**
- Brukeren går tilbake, endrer CV-en og trykker videre. Gap kjøres på nytt, men det gamle **brevet** og `lastet_ned = True` ligger igjen. Nettleserens tilbakeknapp til `/brev` (som er lov hvis H2 bruker `<=` på feil måte) viser et brev laget fra den gamle CV-en.
- Enhet A har allerede skrevet den nye annonsen inn i `okt.annonse` før Enhet B sammenligner, så B ser alltid «uendret» og gjenbruker en gammel nøkkelordliste for en ny annonse. Rekkefølgen er ikke bestemt noe sted.
- Samme annonse lastet opp som PDF første gang og limt inn andre gang er ulik som rå tekst, og gir et nytt KI-kall og kanskje en annen prosent (suksesskriterium 8).
- Bytter brukeren modus fra Korrektur til Full via «Tilbake», ligger `eget_brev` og `korrektur` igjen, og brevsiden kan vise feil mal.
- «Nytt forslag» skal nullstille nedlastingsknappene (UX linje 217). Brev-storyen og nedlastings-storyen kan begge tro at den andre gjør det.

**Minste regel (ny i AD-6/AD-7):**
> Bare `Soknad.sett_inndata(cv, annonse, eget_brev)` i `kjerne/okt.py` endrer inndata. Den sletter alltid `gap`, `brev`, `korrektur`, `forslag` og `lastet_ned`, og sletter `nokkelord` bare når `vask(annonse) != vask(nokkelord_annonse)` (samme vask som AD-10). Den sammenligner før den skriver. `Soknad.nytt_forslag()` sletter `brev`/`korrektur` og `lastet_ned` og øker `forslag`. `Soknad.velg_modus(m)` sletter alt etter modus hvis modus endres. Rutene kaller disse og skriver aldri feltene selv.

---

## H4 — KI-grensesnittet har navn, men ikke signaturer, og TestKI har tilstand som ikke har noe hjem · Høy

**AD-er som følges:** AD-3 (fire metoder, web vet ikke hvilken utgave), AD-4 (former), AD-10 (testcase gjenkjennes; «Nytt forslag» bytter mellom `brev-1` og `brev-2`), FR-38 (svarene er ekte KI-svar).

**Enhet A — story «TestKI» (bygges først, i testmodus):** `TestKI.brev(okt)` tar hele økten, finner testcaset selv og teller hvor mange ganger den er kalt i en variabel på objektet for å bytte mellom `brev-1` og `brev-2`. Leser `ki-svar/brev-1.json` og returnerer en `dict`.

**Enhet B — story «EkteKI» (bygges sent, uke 27. nov):** `EkteKI.brev(cv, annonse)` tar tekster og returnerer en dataklasse `BrevSvar`.

**Enhet C — et lite skript som lager `ki-svar/*.json` (FR-38):** lagrer hele API-svaret (`message.model_dump_json()`), med `content[0].text` som en JSON-*streng* inni, eller lagrer `content[0].text` direkte.

**Kollisjon:**
- Rutene er skrevet mot TestKI sin signatur. Når EkteKI kobles på, må alle rutene skrives om — akkurat det AD-3 skulle hindre.
- TestKI-objektet lages per økt, eller én gang for hele appen. Lages det én gang, deler alle brukere telleren for «Nytt forslag». Lages det per forespørsel, starter telleren alltid på 1, og knappen gir alltid samme brev.
- TestKI leser JSON-filene i et annet format enn EkteKI får fra API-et, og «kontrolleres to ganger» (AD-4) blir bare kjørt på den ene utgaven.
- Hvem kaller `testdata_match`? Innleggings-storyen (for å vise feilen `ikke_testdata` i feilboksen, UX linje 141), eller TestKI inni hvert kall (da kommer feilen først etter et ventetegn og vises som KI-feil)?

**Minste regel (stram AD-3 og AD-10):**
> Signaturene er faste og tar bare tekst og tall, ikke økten:
> `nokkelord(annonse) -> NokkelordSvar`, `gap(cv, annonse) -> GapSvar`, `brev(cv, annonse, forslag: int) -> BrevSvar`, `korrektur(cv, annonse, eget_brev, forslag: int) -> KorrekturSvar`. Svartypene er dataklasser i `kjerne/ki_svar.py`.
> Begge utgavene sender rå `dict` gjennom samme `kjerne.ki_svar.kontroller(oppgave, data)`, som lager dataklassen eller kaster `KIFeil(ubrukelig_svar)`.
> `forslag` telles i økten (H1) og sendes inn av web. EkteKI ignorerer den. TestKI velger fil nr. `(forslag - 1) % 2 + 1`.
> Testcaset gjenkjennes i POST fra innleggingen, sammen med de andre inndatafeilene, og lagres i `soknad.testcase`. `TestKI(case_mappe)` lages per forespørsel fra denne verdien.
> Filene i `ki-svar/` er nøyaktig AD-4-objektet (ikke hele API-svaret), lagret som UTF-8 med `ensure_ascii=False`, og lages av `scripts/lag_testsvar.py`, som bruker `EkteKI`.

---

## H5 — Feiltypene er ikke lukket, og én feil om gangen passer ikke med UX · Høy

**AD-er som følges:** AD-9 nevner `InndataFeil(felt, type)`, `PdfFeil(type)`, `KIFeil(type)` og sier at `type` er `nettverk`, `annet` eller `ubrukelig_svar`. AD-10 bruker `InndataFeil(ikke_testdata)` (uten felt). AD-11 bruker `PdfFeil(uleselig)`. AD-8 krever POST → redirect → GET.

**Enhet A — `kjerne/inndata.py`:** kaster `InndataFeil("cv", "tom")` ved første tomme felt.

**Enhet B — `web/tekster.py`:** har nøklene `("cv", "mangler")`, `("fil", "feil_type")` og `("fil", "for_stor")`.

**Enhet C — `adaptere/pdf_inn.py`:** kaster `PdfFeil("for_stor")` og `PdfFeil("feil_filtype")`, fordi det er der filen leses.

**Kollisjon:**
- Typelista i AD-9 gjelder tydelig bare `KIFeil`. Typene for `InndataFeil` og `PdfFeil` er ikke lukket, så A, B og C finner på hvert sitt navn. Resultatet er `KeyError` i tekster eller en tom feilmelding.
- Feil filtype og for stor fil kan kastes fra to lag med to klasser.
- `MAX_CONTENT_LENGTH` (16 MB) gir Werkzeugs `RequestEntityTooLarge` (413), som ikke er noen av de tre klassene. Ingen story eier den, og sensor får en engelsk standardside.
- UX (linje 267) krever at **alle** feil vises samtidig i én feilboks. Et unntak stopper ved første feil.
- Innloggingsfeil (FR-2–FR-4) har ingen klasse i det hele tatt.
- Med POST → redirect → GET forsvinner feilen ved redirect. En story bruker `flash()`, en annen `okt["feil"]`, en tredje rendrer siden direkte.

**Minste regel (stram AD-9):**
> `kjerne/feil.py` definerer klassene og lukkede lister (`Enum` eller `Literal`) for typene:
> - `InndataFeil(feil: list[tuple[felt, type]])`, med `felt` i `epost | passord | samtykke | cv | annonse | eget_brev | testdata` og `type` i `tom | for_kort | finnes | feil_innlogging | feil_filtype | for_stor | uleselig | ikke_testdata`
> - `KIFeil(type)`, med `type` i `nettverk | annet | ubrukelig_svar`
>
> `PdfFeil` fjernes eller gjøres til en underklasse av `InndataFeil`, slik at én feilboks kan vise alt. Sjekken samler alle feil og kaster én gang. Filtype og størrelse sjekkes bare i `kjerne/inndata.py` (med filnavn og antall byte som inndata); `pdf_inn` kaster bare `uleselig`. En `errorhandler(413)` gjør 413 om til `InndataFeil(for_stor)`.
> `web/tekster.py` har én tekst per (felt, type), og en test sjekker at hver kombinasjon som kan kastes, har en tekst.
> Unntak fra POST → redirect → GET: når en POST feiler, vises samme side direkte med feilen (status 400 for inndata, 502 for KI). Bare vellykket POST redirecter.

---

## H6 — Tegnkoding og tekstvask på Windows · Høy

**AD-er som følges:** AD-10 (vask = små bokstaver, fjern mellomrom), AD-4 (prompt-filer i `prompts/`), konvensjonene (CI kjører pytest).

**Enhet A — `adaptere/ki.py` og `TestKI`:** `open("prompts/brev.md").read()` og `json.load(open(...))`.

**Enhet B — testdata-storyen:** `cv.txt` skrives for hånd i VS Code, og `cv.pdf` lages fra den i Word.

**Kollisjon:**
- På Kristines Windows-PC med Python 3.14 bruker `open()` uten `encoding` fortsatt Windows-koding (cp1252). Prompter og testsvar med æøå blir rotete, eller lesingen krasjer. CI kjører på Linux med UTF-8 og er grønn, så feilen vises bare på PC-en til Kristine og sensor.
- pypdf gir ofte tegn som ikke finnes i den håndskrevne `.txt`-fila: kulepunkter (`•`, ``), sammenslåtte bokstaver (`ﬁ`), orddeling med bindestrek ved linjeskift, sidetall og topptekst, og «å» som to tegn (a + ring, NFD). Vasken i AD-10 fjerner bare mellomrom, så PDF-versjonen gjenkjennes ikke som testdata, mens `.txt` gjør det. Det bryter suksesskriterium 5 og 7.
- «Alle tegn med mellomrom» er tvetydig: mellomrom bare, eller alle blanke tegn (`\s`, også linjeskift og tab)?

**Minste regel (ny konvensjon + stram AD-10):**
> All fil-lesing og -skriving bruker `encoding="utf-8"`. Ruff-regelen `PLW1514` (open uten encoding) er slått på, og CI kjører også på `windows-latest`.
> `vask(tekst)` ligger i `kjerne/testdata_match.py` og gjør: `unicodedata.normalize("NFKC")` → `casefold()` → fjern alt som ikke er bokstav eller tall (`[\W_]`). Samme `vask` brukes av FR-19-sammenligningen (H3).
> En test går gjennom alle testcase og sjekker at både `pdf_inn(cv.pdf)` og `cv.txt` (og det samme for annonse og eget brev) gjenkjennes som samme case.

---

## H7 — Oppstart og økt etter omstart · Middels

**AD-er som følges:** AD-7 (cookien har økt-id og bruker-id, objektet ligger i minnet), AD-12 (innstillinger fra `.env`), NFR-12 (README prøves uten `.env`).

**Enhet A — `create_app`:** leser `SECRET_KEY` fra `.env` som de andre innstillingene og krasjer hvis den mangler.

**Enhet B — `login_required`:** sjekker bare at cookien har `bruker_id`.

**Kollisjon:**
- Sensor kloner repoet uten `.env` (NFR-12). Appen skal starte i testmodus, men krasjer på manglende `SECRET_KEY`, eller bruker en fast nøkkel som ligger i Git.
- Flask-utviklingsserveren startes på nytt (eller laster koden på nytt ved endring). Cookien er fortsatt gyldig med `bruker_id`, `login_required` slipper brukeren inn, og første oppslag i øktlageret gir `KeyError` og en 500-feil.

**Minste regel (stram AD-7 og AD-12):**
> `SECRET_KEY` leses fra `.env` hvis den finnes, ellers lages en tilfeldig nøkkel med `secrets.token_hex()` ved oppstart. `login_required` godtar bare en cookie der økt-id-en finnes i øktlageret. Ellers tømmes cookien, og brukeren sendes til innloggingen med «Du må logge inn først» (FR-7).

---

## H8 — Korrektur-reglene mangler kanttilfeller · Middels

**AD-er som følges:** AD-5 (endret/ny/fjernet; brevet = alle `ny` satt sammen, med avsnitt der `nytt_avsnitt` er sann), AD-4 (kontroll etter FR-28).

**Enhet A — malen for Korrektur-visningen (Jinja + litt JS):** viser fjernede setninger som overstreket tekst på sin plass, og bruker `nytt_avsnitt` på den fjernede setningen.

**Enhet B — `fil_ut.py`:** hopper over fjernede setninger, og mister dermed avsnittsskiftet som sto på dem. Setter sammen setningene uten mellomrom.

**Kollisjon:**
- Sto `nytt_avsnitt = true` på en fjernet setning, får visningen og den nedlastede fila ulike avsnitt.
- `gammel != [ny]` med et ekstra mellomrom fra KI-en gjør en uendret setning til «endret». Visning og test kan da rapportere ulikt.
- FR-28 sier ikke hva som er et ubrukelig korrektursvar. Er alle `ny` lik `null`, blir brevet tomt, men kontrollen i `ki_svar` (skrevet fra FR-28-lista) slipper det gjennom.
- `fil_ut` får enten `BrevSvar` eller `KorrekturSvar`, og to stories skriver hver sin `if`.

**Minste regel (stram AD-5):**
> `kjerne/korrektur.py` har `status(setning)` (`uendret | endret | ny | fjernet`, sammenligner etter `strip()`) og `til_avsnitt(svar) -> list[str]`. Et `nytt_avsnitt` på en fjernet setning flyttes til neste setning som ikke er fjernet. Setninger settes sammen med ett mellomrom. Både visningen og `fil_ut` bruker disse. `fil_ut` tar bare `list[str]` (avsnitt) og vet ikke om modus. Et korrektursvar er ubrukelig når `til_avsnitt` gir en tom liste.

---

## H9 — Låsen for KI-kall har ingen eier · Middels

**AD-er som følges:** AD-8 («En ny POST mens et KI-kall pågår i samme økt avvises»), AD-9 («Ved feil beholdes alt i økten»).

**Enhet A — analyse-storyen:** setter `okt.ki_pagar = True` før kallet og `False` etter.

**Enhet B — brev-storyen:** bruker en `threading.Lock()` på modulnivå i `ki.py`.

**Kollisjon:**
- Kaster KI-kallet en feil i Enhet A, blir `ki_pagar` aldri satt tilbake, og økten er låst til brukeren logger ut.
- Enhet B låser for *alle* brukere, ikke per økt.
- «Avvises» er ikke definert: feilmelding, 409 eller redirect? Ingen tekst finnes i UX.
- Flask-utviklingsserveren kjører forespørsler i tråder, så «sjekk, så sett» kan slippe gjennom to dobbeltklikk.

**Minste regel (stram AD-8):**
> Én kontekstbehandler `ki_las(okt)` i `web/` setter `ki_pagar` og nullstiller den i `finally`. Sjekk og sett skjer under én `threading.Lock` i `oktlager`. En avvist POST redirecter stille til siden for gjeldende steg (ingen feilmelding).

---

## H10 — Filnavnet er ikke helt bestemt · Lav

**AD-er som følges:** AD-11 (`Soknad_<Arbeidsgiver>_<ÅÅÅÅ-MM-DD>`, æøå byttet ut, mellomrom til bindestrek, 30 tegn).

**Enhet A — `kjerne/filnavn.py`:** æ→ae, ø→oe, å→aa; legger til `.docx`.

**Enhet B — nedlastingsruten:** legger også til `.docx`/`.pdf`, og bruker `datetime.now()` inni ruten.

**Kollisjon:** «byttet ut» kan bety to ulike tabeller (UX-eksemplet bestemmer ikke). Tegn som `/`, `:`, `&`, `é` og `"` i arbeidsgivernavn («Aker BP / Equinor») gir ugyldige filnavn på Windows eller en ødelagt `Content-Disposition`. Endelsen kan komme to ganger (`.docx.docx`). Datoen lest inne i funksjonen gjør testen avhengig av dagen den kjøres.

**Minste regel (stram AD-11):**
> `lag_filnavn(arbeidsgiver, dato) -> str` gir bare stammen uten endelse. Den bytter æ→ae, ø→o, å→a (og store bokstaver tilsvarende), fjerner alt som ikke er `A–Z`, `a–z`, `0–9` eller `-`, slår sammen bindestreker, og kutter til 30 tegn. Datoen sendes inn som argument. Ruten legger til endelsen.

---

## Mindre funn

- **Samtykke og testmodus i «søknadsdata».** AD-7 lister begge som søknadsdata, men UX sier at bryteren huskes hele innloggingen (linje 262), mens samtykket må krysses av hver gang startsiden vises (linje 279). Dekkes av delingen `Innlogging`/`Soknad` i H1. Merk også at UX linje 279 er strengere enn PRD FR-36 («på nytt hver gang brukeren logger inn»). Det er ikke en motsigelse, men det bør stå i spinen hvilken som gjelder.
- **Hvem håndhever samtykket (AD-12)?** Én funksjon `velg_ki(innlogging)` i `web/` bør være eneste sted som lager `EkteKI`, og den kaster hvis `soknad.samtykke` er usann. Da kan ingen rute sende tekst til Claude uten samtykke.
- **Låst testmodus.** «Mangler `ANTHROPIC_API_KEY` → testmodus låst på» bør leses ett sted (`app.config["TESTMODUS_LAST"]` satt i `create_app`), og `Innlogging.testmodus` settes fra den ved innlogging.
- **Gap-oppgavens inndata.** Det er ikke bestemt om `gap` får nøkkelordlista som inndata. Signaturen i H4 sier nei; det bør stå eksplisitt, siden FR-18 forventer at de to kan si hverandre imot.

## Prioritert liste

| # | Hull | Alvor | Minste rettelse |
| --- | --- | --- | --- |
| H1 | Øktobjektet har ingen fast form | Kritisk | Dataklasser i `kjerne/okt.py`, delt i `Innlogging` og `Soknad`, ingen strengnøkler |
| H2 | `steg` har ingen eier, `==` eller `<=` | Kritisk | `kjerne/steg.py` med `kan_vise` (`<=`) og `ga_til` bare etter vellykket POST; GET endrer aldri økten |
| H3 | Ingen tømmer gamle resultater | Høy | `sett_inndata`, `nytt_forslag`, `velg_modus` er eneste vei inn; nøkkelord sammenlignes på vasket annonse |
| H4 | KI-signaturer og TestKI-tilstand | Høy | Faste signaturer med `forslag: int`, felles `kontroller()`, testcase i økten, `ki-svar` = rent AD-4-objekt |
| H5 | Feiltyper ikke lukket, én feil om gangen | Høy | `kjerne/feil.py` med lukkede lister, feil samlet i én `InndataFeil`, 413-handler, feil rendres uten redirect |
| H6 | Tegnkoding og vask på Windows | Høy | `encoding="utf-8"` + ruff `PLW1514` + Windows i CI; vask = NFKC + casefold + fjern ikke-alfanumerisk; test PDF og txt per case |
| H7 | `SECRET_KEY` og økt etter omstart | Middels | Tilfeldig nøkkel uten `.env`; `login_required` sjekker øktlageret |
| H8 | Korrektur-kanttilfeller | Middels | `kjerne/korrektur.py` med `status` og `til_avsnitt`; `fil_ut` tar bare `list[str]` |
| H9 | KI-lås uten eier | Middels | `ki_las(okt)` med `finally` og lås i `oktlager`; avvist POST redirecter stille |
| H10 | Filnavn uklart | Lav | Fast bytte-tabell, bare `[A-Za-z0-9-]`, dato som argument, ruten legger til endelse |
