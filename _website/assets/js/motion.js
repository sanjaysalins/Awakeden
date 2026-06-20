/** Ambient motion — respects prefers-reduced-motion via CSS; JS enhances mosaic + scroll reveal.
 *  Exposes window.awakedenReveal() so dynamically-rendered content (cards) can be scanned too. */

(function () {
  "use strict";

  function initMosaic() {
    var root = document.querySelector("[data-mosaic]");
    if (!root) return;
    var imgs = root.querySelectorAll("img");
    if (imgs.length < 2) {
      if (imgs[0]) imgs[0].classList.add("active");
      return;
    }
    var i = 0;
    imgs[0].classList.add("active");
    setInterval(function () {
      imgs[i].classList.remove("active");
      i = (i + 1) % imgs.length;
      imgs[i].classList.add("active");
    }, 4500);
  }

  var reduce =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canObserve = !reduce && "IntersectionObserver" in window;
  var observer = null;

  if (canObserve) {
    observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("revealed");
            observer.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
  }

  // Scan for un-revealed .reveal elements. Idempotent — safe to call after each render.
  function scanReveal() {
    var els = document.querySelectorAll(".reveal:not(.revealed)");
    if (!els.length) return;
    if (!canObserve) {
      els.forEach(function (el) {
        el.classList.add("revealed"); // never leave content hidden
      });
      return;
    }
    els.forEach(function (el) {
      observer.observe(el);
    });
  }

  window.awakedenReveal = scanReveal;

  function init() {
    initMosaic();
    scanReveal();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
