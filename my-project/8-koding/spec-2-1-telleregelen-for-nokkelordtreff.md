---
title: 'Story 2.1: Telleregelen for nøkkelordtreff'
type: 'feature'
created: '2026-11-08'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '00cd88e01d48a8b19e40e66900b88383383846f2'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nettsiden har ingen regel for nøkkelordtreffet ennå. Uten én fast regel kan samme CV og annonse gi ulik prosent, og ingen kan forklare hvorfor (FR-16, FR-17).

**Approach:** En ny fil, `kjerne/telleregel.py`, er den eneste koden som avgjør treff og prosent (AD-6). Den får en nøkkelordliste og en CV-tekst og gir tilbake treff, ikke treff, antall og prosent. Ingen side bruker den ennå (det kommer i story 2.5).

## Boundaries & Constraints

**Always:**
- Én funksjon `tell_treff(nokkelord: list[str], cv: str) -> Nokkelordtreff`. `Nokkelordtreff` er en frossen dataclass med `treff` og `ikke_treff` (tupler med nøkkelordene slik de er skrevet, i samme rekkefølge som i listen), `antall_treff`, `antall` og `prosent` (heltall).
- Nøkkelord og CV sammenlignes med `casefold()`. Alle mellomrom (også linjeskift og tabulator) blir til ett vanlig mellomrom i både nøkkelord og CV før sammenligningen, så «Microsoft Office» treffer også når CV-en har linjeskift mellom ordene.
- Lengden på et nøkkelord telles etter `strip()` og `casefold()`. 4 tegn eller mer: treff også som del av et lengre ord. 1–3 tegn: treff bare som eget ord, med `(?<!\w)ord(?!\w)` og `re.escape`.
- Hvert nøkkelord telles én gang, også om det står flere ganger i CV-en. Tomme nøkkelord (etter `strip()`) hoppes over. To nøkkelord som er like etter rydding og `casefold()`, telles som ett, og den første skrivemåten beholdes.
- Prosenten er `antall_treff * 100 / antall`, rundet med `Decimal(...).quantize(Decimal("1"), rounding=ROUND_HALF_UP)`, aldri `round()`.
- En tom liste (også etter at tomme nøkkelord er fjernet) gir `ValueError`. Kontrollen av KI-svar (senere story) skal hindre at det skjer.
- README: begrensningen om «C» i en liste med bokstaver utvides med at «C» også gir treff i «C#» og «C++». Resten av teksten under «Kjente begrensninger» endres ikke.

**Never:**
- `kjerne/` importerer ikke flask eller andre biblioteker fra AD-2, og leser ingen filer. Bare `re`, `dataclasses` og `decimal` fra standardbiblioteket.
- Ingen bøyningsformer, ingen ordstammer, ingen NFKC og ingen andre regler enn de over.
- Ingen kobling til sider, maler, `Soknad` eller KI-en i denne storyen.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| 2 av 3 | 3 nøkkelord, 2 i CV-en | `antall_treff` 2, `antall` 3, `prosent` 67 | N/A |
| 1 av 8 | 8 nøkkelord, 1 i CV-en | `prosent` 13 (12,5 rundes opp) | N/A |
| 0 av Y | ingen i CV-en | `prosent` 0, alle i `ikke_treff` | N/A |
| Kort ord inne i ord | «C», CV «Center» | ikke treff | N/A |
| Kort ord med tegn | «C#», «C++», CV «C#, C++ og SQL» | begge treff | N/A |
| Kjent begrensning | «C», CV «C# og C++» | treff (tegnet etter «C» er ikke en bokstav) | N/A |
| Bindestrek | «python», CV «python-utvikler»; «år», CV «år-tall» | begge treff | N/A |
| Æøå | «Søknad», CV «søknadsbrev» | treff | N/A |
| Store og små | «SQL», CV «sql»; «python», CV «PYTHON» | treff | N/A |
| Står flere ganger | «SQL», CV «SQL ... SQL» | telles én gang | N/A |
| Linjeskift | «Microsoft Office», CV «Microsoft\nOffice» | treff | N/A |
| Like nøkkelord | «SQL», «sql» | `antall` 1, skrivemåten «SQL» | N/A |
| Tom liste | `[]` eller `["  "]` | — | `ValueError` |

</frozen-after-approval>

## Code Map

- `backend/soknad/kjerne/inndata.py` -- eksempel på stilen i kjernen: korte norske docstrings, `re` kompilert som konstant, ingen I/O.
- `backend/soknad/kjerne/okt.py` -- eksempel på frosne dataclasses i kjernen.
- `backend/tests/kjerne/test_inndata.py` -- lagsjekken (`FORBUDT_I_KJERNEN`, `KJERNE.glob("*.py")`) dekker den nye fila automatisk. Ikke endre. Testnavnene begynner med FR-nummeret (`test_fr17_...`), og hver test har en docstring som nevner kravet.
- `README.md` linje 84 -- punktet «Et nøkkelord kan gi treff inne i et annet ord». Bare den siste setningen utvides.

## Tasks & Acceptance

**Execution:**
- [x] `backend/soknad/kjerne/telleregel.py` (ny) -- `Nokkelordtreff` og `tell_treff` etter reglene over, med en kort modul-docstring som sier at dette er den eneste koden for treff og prosent (AD-6).
- [x] `backend/tests/kjerne/test_telleregel.py` (ny) -- én test per rad i matrisen, med navn `test_fr17_...` og docstring. Testen for 1 av 8 sjekker også at `round()` ville gitt 12, så det er tydelig hvorfor `Decimal` trengs.
- [x] `README.md` -- utvid punktet om «C» under «Kjente begrensninger».

**Acceptance Criteria:**
- Given `kjerne/telleregel.py`, when lagsjekken kjører, then finner den ingen forbudte importer.
- Given samme nøkkelordliste og CV to ganger, when `tell_treff` kalles, then er resultatet likt begge gangene.

## Implementation Notes

- En hjelpeagent skrev `telleregel.py`, 17 tester (15 testfunksjoner, én med tre varianter) og README-linjen. 169 tester grønne (152 før), `ruff check` og `ruff format --check` grønne.
- Hovedøkta forenklet `_finnes_i`: lengden måles på det samme ryddede nøkkelordet som sammenlignes (mellomrom slått sammen, `strip()` og `casefold()`), så funksjonen trenger ikke den opprinnelige skrivemåten.
- `treff` og `ikke_treff` har nøkkelordet akkurat slik det kom inn, også med eventuelle mellomrom foran og bak.
- Etter gjennomgangen (6 rettelser, bare i testene): 23 tester i `test_telleregel.py`, 175 i alt, `ruff check` og `ruff format --check` grønne. Hovedøkta prøvde fire feil i koden (grense 2, `>` i stedet for `>=`, uten `(?<!\w)`, uten `re.escape`), og hver av dem får minst én test til å feile.

## Spec Change Log

## Review Triage Log

Runde 1 (2026-11-08), tre lag: blind, grensetilfeller, testhull.

| # | Funn | Kilde | Vurdering | Begrunnelse | Rute |
|---|------|-------|-----------|-------------|------|
| 1 | Grensen på 4 tegn testes ikke på noen av sidene (grensen 2 eller `>` består alle testene) | testhull, blind | medium | Påvist av testhull-laget med en endret kopi. Ny test: «Java» i «JavaScript» gir treff, «SQL» i «MySQL» ikke | patch |
| 2 | `(?<!\w)` testes ikke, så «SQL» kunne gitt treff i «MySQL» | testhull | medium | Påvist: uten den består alle testene. Ny test: «SQL» i «MySQL» og «C» i «ABC» gir ikke treff | patch |
| 3 | Testen av «C++» sjekker ikke `re.escape` (`c++` er et gyldig mønster i Python 3.11+) | testhull | medium | Påvist: uten `re.escape` består alle testene. Ny test: «C++» gir ikke treff i «Jeg kan C og Java.» | patch |
| 4 | Tomme nøkkelord i en liste som ellers er fylt ut, testes ikke | blind | low | Riktig, og det er dette som vises som «X av Y». Ny test | patch |
| 5 | Tom CV testes ikke | blind | low | Riktig, og testen er én linje. Ny test: 0 av 1 = 0 % | patch |
| 6 | Testen av at samme input gir samme svar, heter `fr16`, men FR-16 er listen med treff og ikke treff | blind | low | Riktig. Testen heter nå `fr17`, og 2 av 3-testen nevner FR-16 | patch |
| 7 | Ingen NFC-normalisering: æøå skrevet som to tegn (fra PDF) gir ikke treff | grensetilfeller, blind | maybe-false | Riktig for slik tekst, men ukjent om pypdf eller innliming gir det. Spec-en sier «ingen andre regler». Avgjøres i story 6.1 | defer |
| 8 | Myk bindestrek, usynlige mellomrom og orddeling ved linjeslutt i tekst fra PDF gir ikke treff | grensetilfeller, blind | maybe-false | Samme som funn 7: hører til PDF-lesingen i story 6.1 | defer (med 7) |
| 9 | README nevner ikke at «SQL» ikke gir treff i «MySQL» | blind | low | Riktig, men låst del sier at resten av README-teksten ikke endres. Kristine bestemmer i story 8.1 | defer |
| 10 | Lengden måles etter `casefold()`, så «Fuß» (3) blir «fuss» (4) | grensetilfeller, blind | low | Koden følger spec-en ordrett. Nesten umulig i en norsk CV | avvist |
| 11 | Et nøkkelord med bare tegn, som «-», gir ikke treff i «år-tall» | grensetilfeller | low | Ingen KI gir et slikt nøkkelord, og rettingen krever en ny gren | avvist |
| 12 | `nokkelord` som tekst i stedet for liste teller hvert tegn | grensetilfeller | low | Ingen kaller funksjonen slik. Typen står i signaturen, og kontrollen av KI-svar gir alltid en liste | avvist |
| 13 | `None` i listen gir `TypeError` | grensetilfeller | false | En tydelig feil er riktig her. Kontrollen av KI-svar sørger for at listen bare har tekst | avvist |
| 14 | `cv=None` gir `TypeError` | grensetilfeller | false | En tydelig feil er riktig. Sjekken av inndata stopper en tom CV før telleregelen | avvist |
| 15 | `assert round(1 * 100 / 8) == 12` tester Python, ikke koden | blind | low | Spec-en ber om det, for å vise hvorfor `Decimal` trengs. Rettingen endrer spec-en | avvist |
| 16 | `ValueError("Nøkkelordlisten er tom.")` er tekst i kjernen, mot AD-9 | blind | false | AD-9 gjelder tekster brukeren ser. Dette er en feil i programmet som aldri vises | avvist |
| 17 | `antall` er et uklart navn ved siden av `antall_treff` | blind | low | Navnet er bestemt i den låste delen av spec-en | avvist |
| 18 | Spec-en og tester nevner ikke ValueError i akseptansekriteriene | blind | false | Står i Always og i matrisen («Tom liste»), og en test dekker det | avvist |
| 19 | En test av at resultatet er frosset tester en detalj FR-17 ikke ber om | blind | low | Spec-en krever en frossen dataclass. Testen er billig og vern for senere stories | avvist |
| 20 | «3 tegn gir aldri treff inne i produktnavn» er ikke testet | blind | low | Samme som funn 1 og 2, dekket av den nye testen | patch (med 1) |

## Design Notes

Mellomrom gjøres like fordi CV-er limt inn fra PDF ofte har linjeskift midt i et uttrykk med flere ord. Det endrer ikke regelen for korte ord, fordi mellomrom aldri er en bokstav.

Like nøkkelord telles som ett, så «X av Y» aldri teller samme ord to ganger, selv om KI-en skulle gi det dobbelt.

## Verification

**Commands:**
- `cd backend; uv run pytest` -- expected: alle tester grønne (152 før denne storyen)
- `cd backend; uv run ruff check; uv run ruff format --check` -- expected: ingen feil

**Manual checks:**
- Ingen i nettleseren: storyen har ingen side ennå.
