/** Base-path helper — works on Netlify, localhost, and file:// */
(function () {
  "use strict";
  var path = location.pathname.replace(/\\/g, "/");
  var depth = 0;
  if (/\/work\//.test(path) || /\/series\//.test(path)) depth = 1;
  var base = depth ? "../" : "";
  window.SITE = {
    base: base,
    asset: function (p) {
      return base + p.replace(/^\//, "");
    },
  };
})();
