---
title: 'Story 5.2.2: Kjøring 2 og 3 med ekte KI, og kriterium 12'
type: 'chore'
created: '2026-11-15'
baseline_commit: '6d83859eb7871d182290c87bae52e09a92bc8723'
status: 'done'
route: 'dispatch'
review_loop_iteration: 1
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-5-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Korrektur-prompten er bare kjørt én gang med ekte KI (story 5.2.1). Testplanen krever tre kjøringer som alle består fasiten før kriterium 12 (innhold, eksempler og rekkefølge beholdt) regnes som bestått, og kriterium 4 er ikke sjekket på svarene fra ekte KI (FR-38, NFR-12).

**Approach:** Kristine vurderer først kjøring 1 mot «Sjekkliste for Korrektur» i `fasit.md`. Så kjøres resten av runden med ekte KI, alle tre kjøringene sjekkes, plan B brukes ved feil (prompten forbedres én gang, og alle tre kjøres på nytt), og resultatet skrives i `my-project/testplan.md`, også når noe feiler.

## Boundaries & Constraints

**Always:** Hver kjøring gir `korrektur-1.json` og `korrektur-2.json`, og hvert av de to brevene sjekkes mot hvert punkt i «Sjekkliste for Korrektur». Kriterium 4 på datanivå: hvert svar består `kontroller()` mot `eget-brev.txt` og har minst én setning der `gammel != [ny]`. Claude lager et utkast til vurderingen, og Kristine bestemmer hva som er brudd og hva som godkjennes. Kjøringer med ekte KI starter først når Kristine har godkjent dem. Svar og terminallogg for hver kjøring ligger i `my-project/testkjoringer/5-2/<runde>/kjoring-<n>/`. Plan B brukes høyst én gang, og en endret prompt får en test i `tests/adaptere/test_ekte_ki.py`. Testene kaller aldri det ekte API-et.

**Never:** Ingen endring i nettsiden, i Full generering, i `brev.md` eller i brev-, gap- og nøkkelordsvarene. Ingen markeringer på brevsiden (story 5.3). Ikke målingen med et langt eget brev (deferred-work, eget punkt). Ikke kriterium 13.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Alle består | tre kjøringer, alle seks brevene består sjekklisten | kriterium 12 (og 4 på datanivå) står som bestått i testplanen | – |
| En kjøring feiler | Kristine finner et brudd | plan B: prompten forbedres én gang, runde 2 med tre nye kjøringer, kjøring 1 skriver `testdata/case-1-utvikler/ki-svar/` | – |
| Feiler etter plan B | brudd også i runde 2 | kriteriet står som ikke bestått, med hva som gikk galt | ingen ny plan B |
| Ubrukelig svar | skriptet gir feilkode for et KI-kall | ingenting skrives for kjøringen. Stopp og spør Kristine | `KI_FEILET` |

**Beslutning (Kristine, 2026-11-15):** kjøring 1 er godkjent. «Takk for at dere har lest søknaden.», «Jeg håper dere vil vurdere søknaden min.», «en fast fadder», «Git til versjonskontroll» og «imøtekommende» er omformuleringer innenfor reglene. Det viktigste er at ingenting som ikke står i CV-en, brevet eller annonsen, blir dratt inn i søknaden. Kjøring 2 og 3 i runde 1 kjøres med prompten som den er.
**Beslutning (Kristine, 2026-11-15):** de to uklarhetene i prompten rettes ikke (punktet fra 5.2.1 lukkes som godtatt). Å skrive om dårlig formulerte setninger, også KI-frasene, er det KI-en skal gjøre, og noe som absolutt ikke hører hjemme i en søknad (som «det var gøy»), kan fjernes.
**Regel for vurderingen:** et brudd er innhold som ikke står i CV-en, brevet eller annonsen, eller innhold fra brevet som mangler (utenom det som ikke hører hjemme i en søknad). Omformuleringer og en tydeligere kobling til annonsen er godkjent.
**Beslutning (Kristine, 2026-11-15, etter kodegjennomgangen):** «fungert godt / bra» for «gått ganske greit» er godkjent (ingenting nytt er dratt inn, og teksten skal ikke være mindre formell). De små endringene i ordlyd (funn 4) og tonen med «booke», «gruppa» og uendret «Jeg lærer nye ting fort …» (funn 5) er også godkjent. Kriterium 12 er bestått uten plan B.

</frozen-after-approval>

## Code Map

- `backend/scripts/lag_testsvar.py` -- kjøres uendret: `uv run python -m scripts.lag_testsvar --case case-1-utvikler --bare-korrektur --ut ../my-project/testkjoringer/5-2/<runde>/kjoring-<n>` (2 kall). Uten `--ut` skriver den `testdata/case-1-utvikler/ki-svar/` (kjøring 1 i en ny runde). Terminalen lagres som `logg.txt` i samme mappe.
- `my-project/testkjoringer/5-2/runde-1/kjoring-1/` -- kjøring 1 fra 5.2.1, med `logg.txt` (4 686 tokens inn, ca. 0,86 + 0,85 kr).
- `backend/testdata/case-1-utvikler/fasit.md` -- «Sjekkliste for Korrektur» (7 punkter). `eget-brev.txt` er originalen.
- `backend/soknad/kjerne/ki_svar.py` -- `kontroller("korrektur", tekst, "end_turn", eget_brev=...)` brukes av en kort sjekk i `$CLAUDE_JOB_DIR/tmp` (ikke i repoet) på kjøring 2 og 3: kontrollen, antall endrede og fjernede setninger, og de 17 frasene.
- `backend/prompts/korrektur.md` -- endres bare ved plan B.
- `backend/tests/adaptere/test_ekte_ki.py:613` -- `_korrektur_prompt()`. En ny regel får en test her ved plan B.
- `backend/tests/test_testdata.py:361` -- `test_fr23_fr24_korrektur_svarene_bestaar_kontrollen_uten_ki_fraser` må bestå hvis plan B skriver nye svar i `testdata/`.
- `my-project/testplan.md:16` -- raden for kriterium 12. Ny seksjon «Story 5.2.2: Korrektur og kriterium 12» etter «Hilsen, navn og to nye regler i brevet», bygd som de andre: runder med tabell per kjøring, brudd og godkjente omformuleringer (bestemt av Kristine), plan B, kostnad og tid.
- `_bmad-output/implementation-artifacts/deferred-work.md` -- de to punktene om 5.2.2 får `resolved:`.

## Tasks & Acceptance

**Execution:**
- [x] Ekte KI, etter Kristines godkjenning -- kjøring 2 og 3 i runde 1 (2 × 2 kall, ca. 3,4 kr). Ved brudd: plan B (prompt + test først), så runde 2 med tre kjøringer (ca. 5,1 kr, ny godkjenning) -- er et svar ubrukelig, stopp og spør
- [x] Sjekk i `$CLAUDE_JOB_DIR/tmp` -- `kontroller`, endrede setninger og frasene for hver kjøring -- kriterium 4 på datanivå
- [x] Utkast til vurdering mot sjekklisten -- vises Kristine i chatten, setning for setning der noe er usikkert -- hun bestemmer
- [x] `my-project/testplan.md` -- seksjonen og raden for kriterium 12 -- også ved feil
- [x] `deferred-work.md` -- `resolved:` på punktene som er lukket

**Acceptance Criteria:**
- Given tre kjøringer i én runde, when Kristine har vurdert dem, then står hver kjøring i testplanen med bestått eller ikke bestått per brev, med begrunnelse for hvert brudd
- Given svarene fra alle kjøringene, when sjekken kjører, then består de `kontroller()` og har minst én endret setning, og ingen `ny` har noen av de 17 frasene
- Given plan B, when runde 2 er ferdig, then består `uv run pytest -q` med de nye svarene i `testdata/`, og den nye regelen har en test

## Implementation Notes

- Implementert direkte i hovedøkten, ikke av en subagent, fordi storyen er betalte kjøringer og vurderinger som Kristine må bestemme underveis.
- Kjøring 2 (kl. 16.33) og 3 (kl. 16.34–16.35) kjørt etter Kristines godkjenning: 4 kall, 4 686 tokens inn hver, 3 014–3 103 ut, 1,77 + 1,74 kr. Alle besto `kontroller` på første forsøk. Loggen fra kjøring 2 ble lagret i cp1252 av terminalen og er gjort om til UTF-8. Kjøring 3 ble kjørt med `PYTHONUTF8=1`.
- Sjekken (`$CLAUDE_JOB_DIR/tmp/sjekk.py`): alle seks brevene består `kontroller` mot `eget-brev.txt`, 11–13 endrede setninger, 1 fjernet («Hei!»), 0 nye, ingen av de 17 frasene, ingen «du» og ingen av de muntlige ordene i den nye teksten.
- Kristine godkjente 15. november 2026 også «I et emneprosjekt» (står i CV-en) og «en stor del av løsningen» (for «mye av det») i kjøring 2. Kriterium 12 er bestått uten plan B, og `prompts/korrektur.md` og `testdata/` er ikke endret.
- `my-project/testplan.md`: raden for kriterium 12 og seksjonen «Story 5.2.2: Korrektur og kriterium 12». `deferred-work.md`: de to punktene fra 5.2.1 har fått `resolved:`.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | edge-case | Tabellen gir én dom per kjøring, ikke per brev, selv om AC sier «per brev» | low | Stemmer, bare teksten sier at alle seks består. Direkte tekstretting → patch |
| 2 | edge-case, blind | «18 setninger» og «ingen nye» stemmer ikke når setningen om butikkjobben er delt i to inne i samme `ny` (alle seks brevene) | low | Stemmer: 18 er oppføringer, og delingen er lov etter prompten (AD-5). Direkte tekstretting → patch |
| 3 | blind | «gått ganske greit stort sett» er blitt «stort sett fungert godt / bra», og prompten sier at KI-en ikke skal gjøre noe større enn det er. Ikke vurdert | low | Stemmer, er ikke vurdert av Kristine. Bare hun kan avgjøre om det er brudd → intent_gap (vurdering) |
| 4 | blind | Flere små endringer i mening er verken listet eller dekket av regelen: «ønsker å jobbe» for «vil veldig gjerne», «fortsatt har mye å lære», «nyttig i møter med kunder», «stillingen som junior utvikler», «hjalp … med pålogging» | low | Stemmer. Samme rot som 3: vurderingen er ikke fullstendig → intent_gap (vurdering) |
| 5 | blind | Merknaden om «booke» og «gruppa» har ingen konklusjon, og uendret «Jeg lærer nye ting fort …» er ikke vurdert mot formell tone | low | Stemmer. Samme rot som 3 → intent_gap (vurdering) |
| 6 | blind | «Prompten er ikke endret» er ikke vist, og kommandoen for kjøring 2 og 3 står ikke | low | Prompten ble committet i `35daffe` etter kjøring 1. Kodegjennomgangen av 5.2.1 rettet ikke prompten (funn 7 og 8 avvist), så den er den samme. Direkte tekstretting (commit og kommando) → patch |
| 7 | blind | Anslaget på 1,14 kr per søknad har ingen kilde og er et beste tilfelle | low | Stemmer: 0,10 + 0,17 er fra case 1 i story 4.4. Et langt eget brev gir mer ut (står i deferred-work). Direkte tekstretting → patch |
| 8 | blind | Kriterium 4 har ingen rad i tabellen, og testen for Word-fila er ikke nevnt | low | Tabellen har bare kriteriene med ekte KI, så raden avvises. Testnavnet `test_fr30_korrektur_filen_er_lik_brevet_paa_siden` legges inn → patch |
| 9 | blind | Bare ett kort testbrev er brukt, uten sammenslåing, uten overskrift og bare med «du» | low | Stemmer. Korrektur testes bare med case 1 (bestemt i 5.1). Én setning om at resultatet gjelder dette brevet → patch |
| 10 | blind | «ca. 22 sekunder» er tiden mellom to loggede kall, ikke målt | low | Stemmer. Direkte tekstretting → patch |
| 11 | verification-gap | Ingen hull funnet | – | – |

Funn 3–5 ble lagt fram for Kristine som et spørsmål om vurderingen. Hun godkjente alle tre (beslutningen står i den frosne blokken), så ingen kode måtte lages på nytt. Funn 1, 2, 6, 7, 8 (testnavnet) og 9–10 er rettet i `my-project/testplan.md`.

## Verification

**Commands:**
- `cd backend && uv run pytest -q` -- expected: alle tester består
- `cd backend && uv run ruff check && uv run ruff format --check` -- expected: ingen feil

**Manual checks (if no CLI):**
- Kristine leser utkastet til vurderingen og testplanseksjonen før commit.
