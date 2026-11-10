// «i»-knappene (UX-DR11): trykk, Enter og mellomrom åpner og lukker boksen, og Esc lukker
// den. Med mus åpner hover boksen, og den holder seg åpen mens musa er over knappen eller
// boksen. Fokus alene åpner den ikke. Skriptet endrer bare visningen, aldri data (AD-1).
document.addEventListener("DOMContentLoaded", function () {
  // Så lenge venter boksen før den lukkes når musa går ut, så musa rekker over glippen
  // mellom knappen og boksen.
  var LUKK_ETTER_MS = 200;

  document.querySelectorAll(".info").forEach(function (info) {
    var knapp = info.querySelector(".info-knapp");
    var boks = document.getElementById(knapp.getAttribute("aria-controls"));
    var lukkes = null;
    // Åpnet med trykk: da lukker ikke musa boksen når den går ut, bare et nytt trykk eller Esc.
    var festet = false;

    function vis(apen) {
      window.clearTimeout(lukkes);
      boks.hidden = !apen;
      knapp.setAttribute("aria-expanded", String(apen));
      if (!apen) {
        festet = false;
      }
    }

    // En <button> gir click også for Enter og mellomrom. Er boksen åpnet med hover, blir den
    // stående åpen etter trykket i stedet for å lukkes.
    knapp.addEventListener("click", function () {
      if (festet) {
        vis(false);
      } else {
        vis(true);
        festet = true;
      }
    });

    // Esc lukker, uansett hvor fokus er.
    document.addEventListener("keydown", function (hendelse) {
      if (hendelse.key === "Escape" && !boks.hidden) {
        vis(false);
      }
    });

    // Et trykk utenfor knappen og boksen lukker den, så en boks åpnet på mobil (uten Esc)
    // ikke blir liggende over listene. Et trykk på den andre «i»-knappen lukker denne.
    document.addEventListener("click", function (hendelse) {
      if (!boks.hidden && !info.contains(hendelse.target)) {
        vis(false);
      }
    });

    // Bare mus. Et trykk på mobil gir også pointerenter, og da ville trykket lukke boksen
    // som hover nettopp åpnet.
    info.addEventListener("pointerenter", function (hendelse) {
      if (hendelse.pointerType === "mouse") {
        vis(true);
      }
    });
    info.addEventListener("pointerleave", function (hendelse) {
      if (hendelse.pointerType === "mouse" && !festet) {
        window.clearTimeout(lukkes);
        lukkes = window.setTimeout(function () {
          vis(false);
        }, LUKK_ETTER_MS);
      }
    });
  });
});
