# Workflows (automatiske sjekker)

Filene her styrer **GitHub Actions**: sjekker som kjører automatisk på GitHub.

## Når kjører de?
- Hver gang du laster opp (pusher) endringer til `main`
- Når noen lager en pull request
- Når du starter dem manuelt: gå til **Actions**-fanen → velg **CI** → **Run workflow**

## Hvor ser jeg resultatet?
Under **Actions**-fanen på GitHub. ✅ betyr at alt gikk bra, ❌ betyr at noe feilet. Klikk på kjøringen for å se hva som gikk galt.

## Hva sjekker `ci.yml`?
| Sjekk | Hva den gjør |
|---|---|
| **Sjekk prosjektet** | Kontrollerer at `README.md` og `my-project/product-brief.md` finnes |
| **Frontend (JavaScript)** | Kjører testene i `frontend/` – hopper over seg selv til mappen finnes |
| **Backend (Python)** | Kjører testene i `backend/` – hopper over seg selv til mappen finnes |

> Flytter eller gir du nytt navn til filene over, må `ci.yml` oppdateres også – ellers blir sjekken ❌.
