// Vinduet som spør før et nytt brev lages («Vil du ha et nytt forslag?», FR-25, UX-DR17). En
// knapp med data-bekreft="<id>" er en vanlig submit-knapp. Et trykk på den stopper sendingen og
// åpner vinduet med den id-en med showModal(), så bare vinduet kan nås mens det er åpent.
// Fokus går til «Avbryt» (autofocus), det trygge valget. «Ja» (data-bekreft-ja) lukker vinduet
// og sender skjemaet med knappen som åpnet det (requestSubmit), så vente.js viser ventetegnet
// som vanlig. «Avbryt» og Esc lukker vinduet, og fokus går tilbake til knappen. Uten
// JavaScript sendes skjemaet uten vinduet. Skriptet endrer aldri søknadsdata (AD-1).
// Det samme gjelder vinduet «Du har ikke lastet ned brevet.» (story 7.5, UX-DR17): «Logg ut»
// nede til høyre på brevsiden har data-bekreft="vindu-logg-ut" før brevet er lastet ned, og
// «Logg ut» i vinduet (data-bekreft-ja) sender utloggingsskjemaet. nedlasting.js tar bort
// data-bekreft når brevet lastes ned, og da sendes skjemaet med en gang.
(function () {
  // Knappen som åpnet vinduet, og vinduet. Fokus går tilbake til knappen når vinduet lukkes.
  var apner = null;
  var apentVindu = null;

  document.addEventListener("click", function (hendelse) {
    var knapp = hendelse.target.closest("[data-bekreft]");
    if (knapp) {
      var vindu = document.getElementById(knapp.getAttribute("data-bekreft"));
      // Mens ventetegnet vises (aria-disabled), stopper vente.js sendingen, og vinduet åpnes
      // ikke. Finnes ikke vinduet, sendes skjemaet som uten JavaScript.
      if (!vindu || vindu.open || knapp.getAttribute("aria-disabled") === "true") {
        return;
      }
      hendelse.preventDefault();
      apner = knapp;
      apentVindu = vindu;
      vindu.showModal();
      var trygg = vindu.querySelector("[autofocus]");
      if (trygg) {
        trygg.focus();
      }
      return;
    }
    var ja = hendelse.target.closest("[data-bekreft-ja]");
    if (ja && apner && apentVindu && apentVindu.contains(ja)) {
      var sender = apner;
      apentVindu.close();
      sender.form.requestSubmit(sender);
    }
  });

  // «Avbryt», Esc og «Ja» lukker vinduet. Fokus går tilbake til knappen som åpnet det. Etter
  // «Ja» har vente.js alt gitt den fokus.
  Array.prototype.forEach.call(document.querySelectorAll("dialog"), function (vindu) {
    vindu.addEventListener("close", function () {
      if (vindu === apentVindu && apner) {
        apner.focus();
        apner = null;
        apentVindu = null;
      }
    });
  });
})();
