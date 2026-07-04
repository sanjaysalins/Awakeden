/** Load catalog.json and render dynamic sections */

(function () {
  "use strict";

  function base() {
    return (window.SITE && window.SITE.base) || "";
  }

  function asset(p) {
    return base() + String(p || "").replace(/^\//, "");
  }

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function card(item, idx) {
    var preview = item.preview
      ? '<img src="' + esc(asset(item.preview)) + '" alt="" loading="lazy">'
      : '<div class="card-poster-fallback"></div>';
    var i = typeof idx === "number" ? idx % 6 : 0;
    return (
      '<a class="card reveal" style="--i:' + i + '" href="' +
      esc(asset("work/" + item.slug + ".html")) +
      '">' +
      '<div class="card-poster">' +
      preview +
      '<div class="card-poster-shade"></div>' +
      "</div>" +
      '<div class="card-body">' +
      '<span class="badge ' +
      esc(item.status_class) +
      '">' +
      esc(item.status_label) +
      "</span>" +
      '<span class="card-kind">' +
      esc(item.kind_label) +
      "</span>" +
      "<h3>" +
      esc(item.title) +
      "</h3>" +
      '<p class="card-ref">' +
      esc(item.ref) +
      "</p>" +
      '<p class="card-hook">' +
      esc(item.public_hook) +
      "</p>" +
      "</div></a>"
    );
  }

  function renderTicker(items, el) {
    if (!el) return;
    var active = items.filter(function (i) {
      return i.public_status === "in_production" || i.public_status === "studio_complete";
    });
    if (!active.length) active = items.slice(0, 6);
    var parts = active.map(function (i) {
      return (
        '<span class="ticker-item"><strong>' +
        esc(i.status_label) +
        "</strong> | " +
        esc(i.title) +
        " | " +
        esc(i.ref) +
        "</span>"
      );
    });
    el.innerHTML = parts.concat(parts).join("");
  }

  function renderStats(stats, root) {
    if (!root || !stats) return;
    root.innerHTML =
      '<div class="stat"><span class="stat-num">' +
      stats.studio_complete +
      '</span><span class="stat-label">Studio complete</span></div>' +
      '<div class="stat"><span class="stat-num">' +
      stats.in_production +
      '</span><span class="stat-label">In production</span></div>' +
      '<div class="stat"><span class="stat-num">' +
      stats.total +
      '</span><span class="stat-label">In catalogue</span></div>' +
      '<div class="stat"><span class="stat-num">' +
      stats.live +
      '</span><span class="stat-label">Live on YouTube</span></div>';
    root.classList.add("loaded");
  }

  function renderFeatured(items, el) {
    if (!el) return;
    var featured = items
      .filter(function (i) {
        return i.featured;
      })
      .sort(function (a, b) {
        return (a.featured_order || 99) - (b.featured_order || 99);
      });
    el.innerHTML = featured.map(card).join("");
    el.classList.add("loaded");
  }

  function renderMosaic(items, el) {
    if (!el) return;
    var withPreview = items.filter(function (i) {
      return i.preview && i.preview_approved;
    });
    var picks = withPreview.slice(0, 5);
    if (!picks.length) {
      el.innerHTML = '<div class="hero-mosaic-fallback" aria-hidden="true"></div>';
      el.classList.add("loaded");
      return;
    }
    el.innerHTML = picks
      .map(function (i, idx) {
        return (
          '<img class="' +
          (idx === 0 ? "active" : "") +
          '" src="' +
          esc(asset(i.preview)) +
          '" alt="">'
        );
      })
      .join("");
    el.classList.add("loaded");
  }

  function renderGrid(items, el, filter) {
    if (!el) return;
    var list = items.slice();
    if (filter && filter !== "all") {
      list = list.filter(function (i) {
        if (filter === "short") return i.kind === "short";
        if (filter === "long") return i.kind === "long";
        if (filter === "production") return i.public_status === "in_production";
        if (filter === "complete") return i.public_status === "studio_complete";
        if (filter === "live") return i.public_status === "live";
        return true;
      });
    }
    el.innerHTML = list.map(card).join("");
    el.classList.add("loaded");
    if (window.awakedenReveal) window.awakedenReveal();
  }

  function renderCluster(items, el) {
    if (!el) return;
    var beats = items
      .filter(function (i) {
        return i.cluster === "psalm-22" && i.cluster_order > 0;
      })
      .sort(function (a, b) {
        return a.cluster_order - b.cluster_order;
      });
    el.innerHTML = beats
      .map(function (i) {
        return (
          '<a class="cluster-beat" href="' +
          esc(asset("work/" + i.slug + ".html")) +
          '">' +
          '<span class="cluster-num">' +
          String(i.cluster_order).padStart(2, "0") +
          "</span>" +
          "<span><strong>" +
          esc(i.title) +
          '</strong><br><span class="ref">' +
          esc(i.ref) +
          "</span></span>" +
          '<span class="badge ' +
          esc(i.status_class) +
          '">' +
          esc(i.status_label) +
          "</span></a>"
        );
      })
      .join("");
    el.classList.add("loaded");
  }

  function renderRoadmap(roadmap, el) {
    if (!el || !roadmap) return;
    el.innerHTML =
      '<ul class="roadmap-list">' +
      roadmap
        .map(function (r) {
          return (
            "<li><h3>" +
            esc(r.title) +
            '</h3><p class="ref">' +
            esc(r.ref) +
            "</p><p>" +
            esc(r.note) +
            "</p></li>"
          );
        })
        .join("") +
      "</ul>";
  }

  function applyLaunch(data) {
    var cta = document.querySelector("[data-launch-cta]");
    if (!cta || !data.launch) return;
    cta.textContent = data.launch.cta_label || "Launching soon";
    if (
      data.launch.cta_enabled &&
      data.social &&
      data.social.youtube &&
      data.social.youtube.url
    ) {
      cta.href = data.social.youtube.url;
      cta.classList.remove("hero-cta--disabled");
      cta.removeAttribute("aria-disabled");
    }
  }

  function initFilters(items) {
    var grid = document.getElementById("catalogue-grid");
    var btns = document.querySelectorAll(".filter-btn");
    if (!grid || !btns.length) return;
    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        btns.forEach(function (b) {
          b.classList.remove("active");
        });
        btn.classList.add("active");
        renderGrid(items, grid, btn.getAttribute("data-filter"));
      });
    });
  }

  function boot() {
    fetch(asset("data/catalog.json"))
      .then(function (r) {
        if (!r.ok) throw new Error("catalog load failed");
        return r.json();
      })
      .then(function (data) {
        var items = data.items || [];
        renderTicker(items, document.getElementById("ticker"));
        renderStats(data.stats, document.getElementById("stats"));
        renderFeatured(items, document.getElementById("featured-grid"));
        renderMosaic(items, document.querySelector("[data-mosaic]"));
        renderGrid(items, document.getElementById("catalogue-grid"), "all");
        renderCluster(items, document.getElementById("cluster-beats"));
        renderRoadmap(data.roadmap, document.getElementById("roadmap-list"));
        applyLaunch(data);
        initFilters(items);
        if (window.awakedenReveal) window.awakedenReveal();
      })
      .catch(function (err) {
        console.error(err);
        var box = document.getElementById("catalogue-grid") || document.getElementById("stats");
        if (box) {
          box.innerHTML =
            '<p class="load-error">Catalogue could not load. Run <code>python build_catalog.py</code> and use a local server (not file://).</p>';
        }
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
