// Fyrverkeriet rundt brevoverskriften (UX-DR18, story 7.4). Når brevsiden åpnes (også etter
// «Nytt forslag»), tegnes små utbrudd på venstre og høyre side av overskriften på et <canvas>
// bak teksten. Nye utbrudd i ca. 2,2 s, høyst 3 i sekundet (minst 350 ms mellom), og alt er
// borte etter ca. 3,2 s. Canvas dekker bare området rundt overskriften, så prikkene kommer
// aldri over brevet. Fargene leses fra CSS-variablene, så skriptet har ingen fargekoder. Ved
// redusert bevegelse tegnes ingenting. Skriptet endrer bare hvordan siden ser ut, aldri
// søknadsdata, og sender og lagrer ingenting (AD-1).
(function () {
  var NYE_UTBRUDD_MS = 2200;
  var FERDIG_MS = 3200;
  var MELLOM_UTBRUDD_MS = 350;
  var PARTIKLER_PER_UTBRUDD = 26;
  var MAKS_DT = 3;
  var FARGEVARIABLER = ["--fireworks-gold", "--primary", "--accent", "--dot-middle", "--success"];

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }
  var lerret = document.querySelector("canvas.fyrverkeri");
  if (!lerret || !lerret.getContext) {
    return;
  }
  var ctx = lerret.getContext("2d");
  var rute = lerret.getBoundingClientRect();
  var bredde = rute.width;
  var hoyde = rute.height;
  var skala = window.devicePixelRatio || 1;
  lerret.width = Math.round(bredde * skala);
  lerret.height = Math.round(hoyde * skala);
  ctx.scale(skala, skala);

  var stil = getComputedStyle(document.documentElement);
  var farger = FARGEVARIABLER.map(function (navn) {
    return stil.getPropertyValue(navn).trim();
  }).filter(function (farge) {
    return farge !== "";
  });
  if (!farger.length) {
    return;
  }

  var partikler = [];
  var start = null;
  var forrigeBilde = null;
  var forrigeUtbrudd = -Infinity;

  // Ett utbrudd: x i 10–30 % eller 70–90 % av bredden, så midten med teksten er fri.
  function utbrudd() {
    var side = Math.random() < 0.5 ? 0.1 + Math.random() * 0.2 : 0.7 + Math.random() * 0.2;
    var x = bredde * side;
    var y = hoyde * (0.25 + Math.random() * 0.5);
    var farge = farger[Math.floor(Math.random() * farger.length)];
    for (var i = 0; i < PARTIKLER_PER_UTBRUDD; i++) {
      var vinkel = (Math.PI * 2 * i) / PARTIKLER_PER_UTBRUDD;
      var fart = 1 + Math.random() * 2;
      partikler.push({
        x: x,
        y: y,
        vx: Math.cos(vinkel) * fart,
        vy: Math.sin(vinkel) * fart,
        liv: 1,
        farge: farge,
      });
    }
  }

  function tegn(tid) {
    if (start === null) {
      start = tid;
      forrigeBilde = tid;
    }
    var gatt = tid - start;
    // Stegene under er laget for 60 bilder i sekundet. dt skalerer dem etter tiden siden
    // forrige bilde, så farten er lik på alle skjermer. Høyst 3, så en fane som har stått i
    // bakgrunnen ikke gir et hopp.
    var dt = Math.min((tid - forrigeBilde) / (1000 / 60), MAKS_DT);
    forrigeBilde = tid;
    if (gatt < NYE_UTBRUDD_MS && tid - forrigeUtbrudd >= MELLOM_UTBRUDD_MS) {
      utbrudd();
      forrigeUtbrudd = tid;
    }
    ctx.clearRect(0, 0, bredde, hoyde);
    partikler.forEach(function (p) {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.vy += 0.03 * dt;
      p.liv -= 0.018 * dt;
      if (p.liv > 0) {
        ctx.globalAlpha = p.liv;
        ctx.fillStyle = p.farge;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 2.4, 0, Math.PI * 2);
        ctx.fill();
      }
    });
    ctx.globalAlpha = 1;
    if (gatt < FERDIG_MS) {
      window.requestAnimationFrame(tegn);
    } else {
      ctx.clearRect(0, 0, bredde, hoyde);
    }
  }

  window.requestAnimationFrame(tegn);
})();
