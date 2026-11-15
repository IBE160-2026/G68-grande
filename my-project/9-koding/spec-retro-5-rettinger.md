---
title: 'Rettinger etter retro 5, runde A: strammere sjekk av Korrektur-svarene'
type: 'bugfix'
created: '2026-11-15'
status: 'done'
baseline_commit: '78297dbdec9808c858b7cd2a1f8583c4b44a5c1c'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-5-retro-2026-11-15.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Kontrollen i Korrektur sjekker `gammel` mot det egne brevet bare etter vasken (store bokstaver, tegnsetting og mellomrom teller ikke). Derfor kan «Du skrev» vise noe brukeren ikke skrev, og en endring bare i tegnsetting kan bli usynlig (retro 5, punkt 1). Testen av de ekte Korrektur-svarene sjekker heller ikke ordene i «Sjekkliste for brevet», og «minst én endret» teller også fjernede setninger (punkt 2).

**Approach:**
- `kjerne/ki_svar._stemmer_med` krever at alle `gammel` satt sammen med ett mellomrom er lik det egne brevet renset på samme måte (`_rens_avsnitt`, med Unicode NFC på begge sider). Bare mellomrom og linjeskift kan være ulike.
- `TestKI.korrektur` kontrollerer svaret mot casets egen `eget-brev.txt`, ikke mot det brukeren limte inn. Caset er alt funnet med vasken, og svarfila hører til fila.
- `tests/test_testdata.py` sjekker sjekklisteordene i alle `ny` og bruker `korrektur_visning(...)["antall_endret"] >= 1`.
- Testene for kontrollen rettes til den nye regelen.
- AD-4 i `ARCHITECTURE-SPINE.md` og `epic-5-context.md` sier det samme som koden.

**Beslutning (Kristine, 2026-11-15):** retro 5 deles i runde A (dette), B (langt brev og flyt) og C (avstemming av planene). Punkt 1 og 2 fra retro 5 er godkjent.

</frozen-after-approval>

## Implementation Notes

- `kjerne/ki_svar._stemmer_med`: `" ".join(alle gammel)` mot `_rens_avsnitt(eget_brev)`, med NFC på begge sider. `vask` brukes ikke lenger i `ki_svar.py`, så importen er fjernet. En tom `gammel` gir to mellomrom på rad og avvises. Det tar også funnet om tom tekst i `gammel` fra retro 5 (edge-case 4).
- Oppdaget underveis: `TestKI.korrektur` sendte det innlimte brevet til `kontroller`. Med den strenge sjekken ville testmodus feile når teksten har andre store bokstaver (`test_ki.py` limer inn med store bokstaver) eller kommer fra en PDF (Epic 6). Nå sjekkes svaret mot casets egen `eget-brev.txt`. Caset er alt funnet med vasken.
- Alle åtte ekte svarene består den strenge sjekken (sjekket i retroen), og `test_testdata.py` sjekker de to i `ki-svar/`.
- `tests/test_testdata.py`: sjekklisteordene i alle `ny`, og `korrektur_visning(...)["antall_endret"] >= 1`.
- `tests/kjerne/test_ki_svar.py`: testen «ser bort fra tegnsetting» er nå «ser bort fra mellomrom og linjeskift» (med NFC). En ny test viser at store bokstaver, tegnsetting og tom `gammel` gir `KIFeil`.
- AD-4 og AD-10 i `ARCHITECTURE-SPINE.md` og Svarformen i `epic-5-context.md` er rettet, med kopier i `my-project/5-arkitektur/arkitektur.md` og `my-project/9-koding/epic-5-context.md`.
- 1033 tester består, og ruff er uten feil.
- Etter gjennomgangen: sjekken ser bort fra alle mellomrom (også mellom setninger) og usynlige formattegn (Cf), men ikke fra store bokstaver og tegnsetting (`_uten_mellomrom`). En tom `gammel` avvises med en egen regel. NFC er flyttet inn i `_rens_avsnitt`, så teksten som lagres og vises, også får NFC. `TestKI.korrektur` gir `KIFeil(annet)` når `eget-brev.txt` ikke kan leses. 1038 tester består, og 8 av 8 ekte svar består.

## Review Triage Log

| # | Kilde | Funn | Verdict | Begrunnelse |
|---|-------|------|---------|-------------|
| 1 | blind | Mangler mellomrom etter punktum i brevet («butikk.Det»), og KI-en deler setningene, gir `ubrukelig_svar` for et riktig svar | medium | Stemmer: `" ".join` la til et mellomrom som ikke sto i brevet. Rettet: sammenligningen ser bort fra alle mellomrom, med test → patch |
| 2 | blind | Tom `gammel` passer ikke med regelen «bare mellomrom kan være ulike» | low | Stemmer. Tom `gammel` avvises nå med en egen regel, og docstringen og AD-4 sier det → patch |
| 3 | blind | NFC gjelder bare i sjekken, ikke i teksten som lagres, så `gammel` i NFD og `ny` i NFC blir markert som endret | low | Stemmer. NFC er flyttet til `_rens_avsnitt`, med test → patch |
| 4 | blind | Usynlige formattegn (myk bindestrek, nullbreddemellomrom, BOM) gir falsk avvisning | medium | Stemmer: kategori Cf ble beholdt, og tekst fra Word og PDF (Epic 6) har ofte slike tegn. Rettet, med test → patch |
| 5 | blind | Ingen test låser de seks kjøringene i `my-project/testkjoringer/` | low | De er arkiv og brukes ikke av nettsiden. De to i `ki-svar/` testes, og alle åtte er sjekket for hånd. Avvist |
| 6 | blind | Prompten sier «ord for ord», som passet til vasken | low | Ingen feil i dag (8 av 8 består). En endring i prompten krever nye kjøringer → utsatt til runde B (deferred-work) |
| 7 | blind | Linje 20 i `epic-5-context.md` sier fortsatt «vasket» | low | Stemmer. Rettet, med kopi → patch |
| 8 | blind | AD-4 og konteksten nevner ikke tegnene Word ikke tåler, eller NFC | low | Stemmer. Tekstene er rettet → patch |
| 9 | blind | `TestKI.korrektur` leser fila uten `try/except`, og reserven for `None` er død kode | low | Stemmer. Gir nå `KIFeil(annet)` som for svarfilene, uten reserve, med test → patch |
| 10 | blind | Docstringen sier at «Du skrev» viser det brukeren skrev, men i testmodus er det teksten i fila | low | Stemmer. Docstringen og AD-4 sier det nå → patch |
| 11 | blind | To docstrings i `test_ki.py` er utdaterte | low | Stemmer. Rettet → patch |
| 12 | blind | Linjebrudd midt i docstringen til `kontroller` | low | Stemmer. Rettet → patch |
