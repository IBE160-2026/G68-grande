// Endrede setninger i Korrektur (FR-23, UX-DR15): trykk på en setning åpner «Du skrev» rett
// under, og et nytt trykk lukker den. Flere kan være åpne samtidig. En <button> gir click også
// for Enter og mellomrom. Ingen Esc og ingen åpning med hover. Hva som er endret, står i
// siden fra serveren. Skriptet endrer bare visningen, aldri data (AD-1).
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".endret-setning").forEach(function (knapp) {
    var boks = document.getElementById(knapp.getAttribute("aria-controls"));
    if (!boks) {
      return;
    }

    knapp.addEventListener("click", function () {
      var apen = knapp.getAttribute("aria-expanded") !== "true";
      boks.hidden = !apen;
      knapp.setAttribute("aria-expanded", String(apen));
    });
  });
});
