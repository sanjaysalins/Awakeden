/* THE ARC — shared behaviour for the porch and the road.
   Discipline (LAW 1, from the films): nothing here ever animates a
   .kjv block. Scripture is never letter-revealed, faded in, or slid
   in — it is simply on the page, whole, before the reader arrives.
   The only moving things are the reader's own position (the thread
   rail), plate/heading settles, and the one annotator's circle. */
(function () {
  "use strict";

  document.documentElement.classList.remove("nojs");
  document.documentElement.classList.add("js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- reveals: plates and headers only, never scripture ---------- */
  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  // Safety net for LAW 1: strip .reveal from anything that contains scripture.
  reveals = reveals.filter(function (el) {
    if (el.querySelector(".kjv") || el.closest(".kjv")) {
      el.classList.add("on");
      return false;
    }
    return true;
  });

  // Anything already inside the first viewport is shown at once — a reader
  // must never wait for an observer to hand them content they can already see.
  // The observer only handles what lies below the fold.
  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("on"); });
  } else {
    var below = [];
    reveals.forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight * 1.05) {
        el.classList.add("on");
      } else {
        below.push(el);
      }
    });
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("on"); ro.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    below.forEach(function (el) { ro.observe(el); });
  }

  /* ---------- the one annotator's circle (around "looketh") ---------- */
  var circ = document.getElementById("lookethCirc");
  if (circ) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      circ.classList.add("on");
    } else if (circ.getBoundingClientRect().top < window.innerHeight) {
      // already on the first screen: the CSS transition delays give the
      // reader a beat to start the verse before the circle draws
      circ.classList.add("on");
    } else {
      var co = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { circ.classList.add("on"); co.unobserve(circ); }
        });
      }, { threshold: 0.9 });
      co.observe(circ);
    }
  }

  /* ---------- the thread rail: five knots, one gold thread ---------- */
  var rail = document.getElementById("rail");
  if (!rail) return;

  var knots = Array.prototype.slice.call(rail.querySelectorAll(".knot"));
  var fill = document.getElementById("railFill");
  var nowLabel = document.getElementById("nowLabel");
  var sections = knots.map(function (k) {
    return document.getElementById(k.getAttribute("href").slice(1));
  });

  var vertical = window.matchMedia("(min-width: 1120px)");

  function update() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    var progress = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    if (fill) {
      fill.style.transform = vertical.matches
        ? "scaleY(" + progress + ")"
        : "scaleX(" + progress + ")";
    }

    // current stop = the last section whose top has crossed 45% of the viewport
    var line = window.scrollY + window.innerHeight * 0.45;
    var current = 0;
    sections.forEach(function (s, i) {
      if (s && s.offsetTop <= line) current = i;
    });
    // at the very bottom, the last knot is tied
    if (progress > 0.995) current = knots.length - 1;

    knots.forEach(function (k, i) {
      k.classList.toggle("passed", i < current);
      k.classList.toggle("current", i === current);
      if (i === current) { k.setAttribute("aria-current", "true"); }
      else { k.removeAttribute("aria-current"); }
    });
    if (nowLabel) {
      nowLabel.textContent = knots[current].querySelector(".klabel").textContent;
    }
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () { update(); ticking = false; });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  update();
})();
