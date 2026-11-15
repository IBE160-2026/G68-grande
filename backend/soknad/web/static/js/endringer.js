// Endrede setninger i Korrektur (FR-23, UX-DR15): trykk på en setning åpner «Du skrev» rett
// under, og et nytt trykk lukker den. Flere kan være åpne samtidig. Setningen er et <span> med
// role="button" og tabindex="0", ikke en <button>, fordi en knapp ikke kan brytes over to linjer,
// og da så brevet ut som én setning per linje (sett av Kristine i retro 5, runde B). Derfor
// åpner skriptet også med Enter og mellomrom. Ingen Esc og ingen åpning med hover. Hva som er
// endret, står i siden fra serveren. Skriptet endrer bare visningen, aldri data (AD-1).
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".endret-setning").forEach(function (knapp) {
    var boks = document.getElementById(knapp.getAttribute("aria-controls"));
    if (!boks) {
      return;
    }

    function bytt() {
      var apen = knapp.getAttribute("aria-expanded") !== "true";
      boks.hidden = !apen;
      knapp.setAttribute("aria-expanded", String(apen));
    }

    knapp.addEventListener("click", bytt);
    knapp.addEventListener("keydown", function (hendelse) {
      // Mellomrom ville ellers rulle siden
      if (hendelse.key === "Enter" || hendelse.key === " ") {
        hendelse.preventDefault();
        bytt();
      }
    });
  });
});
