// Ventetegnet (FR-27, UX-DR14). Når en knapp med data-vente sender skjemaet, dekkes siden av
// ventetegnet til serveren svarer med en ny side. Resten av siden blir inert, også topplinjen
// og hjørneraden. Knappen får aria-disabled og beholder fokus (med disabled ville den mistet
// fokus). Et nytt trykk sender ingenting. Skriptet sender skjemaet som vanlig og endrer aldri
// søknadsdata (AD-1).
(function () {
  var venter = false;

  // Søsknene til knappen og til hver forelder opp til body blir inert. Knappen og foreldrene
  // blir ikke det, så knappen beholder fokus. Beholderen med ventetegnet sperres aldri.
  function sperrResten(knapp, beholder) {
    for (var node = knapp; node.parentElement && node !== document.body; node = node.parentElement) {
      Array.prototype.forEach.call(node.parentElement.children, function (sosken) {
        if (sosken !== node && sosken !== beholder) {
          sosken.inert = true;
        }
      });
    }
  }

  document.addEventListener("submit", function (hendelse) {
    if (venter) {
      hendelse.preventDefault();
      return;
    }
    var knapp = hendelse.submitter;
    var beholder = document.getElementById("vente");
    if (hendelse.defaultPrevented || !knapp || !knapp.hasAttribute("data-vente") || !beholder) {
      return;
    }
    venter = true;
    var tekst = knapp.getAttribute("data-vente");
    knapp.setAttribute("aria-disabled", "true");
    sperrResten(knapp, beholder);
    knapp.focus();
    document.getElementById("vente-tekst").textContent = tekst;
    document.getElementById("ventetegn").hidden = false;
    document.getElementById("vente-status").textContent = tekst;
  });
})();
