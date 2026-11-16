# Red-team pack: upload tracker + brand/AI cleanup (2026-11-16)

## What the owner asked (verbatim)
"1) from now on just track youtube links 2) if the links are there, have a mechanism for me to hide them or unhide them. 3) remove any reference in the publication of any locked episode any reference to AI, please recheck. 4) we no longer supporting awakeden, so remove all of their reference completely"
Owner choices: new brand = Salt and Light Kingdom (YouTube @saltandlightkingdomorg, TikTok @saltandlightkingdom, Instagram @salt.andlightkingdomorg, Facebook profile.php?id=61588658953392); website awakeden.com: remove links, keep files on disk; burned-in logo on videos/thumbnails: remove at $0, leave already-posted YouTube videos untouched.

## Your job
Find REAL defects: bugs, things missed, things broken, public text still wrong, data loss risk, gates weakened wrongly. Be specific (file + line + why). Do not praise.

## Code diff (only files changed for this task)
```diff
diff --git a/build_upload_tracker.py b/build_upload_tracker.py
index 2e093b7..f59f9ce 100644
--- a/build_upload_tracker.py
+++ b/build_upload_tracker.py
@@ -29,11 +29,17 @@ from pipeline import release_state  # noqa: E402
 from pipeline.episode_state import gather_episodes  # noqa: E402
 
 SWIRLS_DIR = ROOT / "poc_living_water_ink_style_test"
-SWIRLS_PLATFORMS = ["youtube", "tiktok", "facebook", "instagram"]
+SWIRLS_PLATFORMS = ["youtube"]  # owner rule 2026-11-16: track YouTube only
 
 OUT = ROOT / "_UPLOAD_TRACKER.html"
-PLAT_LABEL = {"youtube": "▶ YouTube", "tiktok": "♪ TikTok",
-              "facebook": "f Facebook", "instagram": "◎ Instagram"}
+PLAT_LABEL = {"youtube": "▶ YouTube"}
+
+
+def hide_btn(key: str) -> str:
+    """Hide/unhide toggle for a card that already has a posted link (owner ask
+    2026-11-16). Per-viewer view setting only, kept in browser storage; the
+    ledger is never touched."""
+    return (f"<button class=hide onclick=\"toggleHide('{esc(key)}')\">Hide</button>")
 
 CANON = [
     ("Audience", "NOT made for kids"),
@@ -41,7 +47,7 @@ CANON = [
     ("Category", "Education"),
     ("License", "Standard YouTube licence"),
     ("Comments", "On — hold potentially inappropriate for review"),
-    ("Visibility", "Public (YouTube first; TikTok/FB/IG within 24–48h)"),
+    ("Visibility", "Public"),
 ]
 
 
@@ -110,13 +116,10 @@ def card(s: release_state.PieceState, missing: list[str]) -> str:
         links.append(flink(pub / "PUBLISH_INDEX.html", "📦 publish pack (copy buttons)"))
     if (pub / "captions.srt").is_file():
         links.append(flink(pub / "captions.srt", "📝 captions.srt"))
-    for key, lbl in (("16x9", "🖼 16:9 (YouTube)"), ("9x16", "🖼 9:16 (Shorts)"),
-                     ("tiktok", "🖼 TikTok cover"), ("1x1", "🖼 1:1")):
+    for key, lbl in (("16x9", "🖼 16:9 (YouTube)"), ("9x16", "🖼 9:16 (Shorts)")):
         t = thumbs / f"thumb_{key}.jpg"
         if t.is_file():
             links.append(flink(t, lbl))
-    if s.read_page:
-        links.append(f"<a href='https://awakeden.com/read/{esc(s.slug)}.html'>📖 read page</a>")
 
     tech = ""
     if s.video:
@@ -146,9 +149,11 @@ def card(s: release_state.PieceState, missing: list[str]) -> str:
                 f"<td><button onclick=\"cmd(this,'{esc(s.slug)}','{esc(plat)}')\">COPY command</button></td></tr>")
 
     badge = "<span class='c long'>LONG</span> " if s.kind == "long" else ""
-    todo = (f"<span class='c warn'>to post: {', '.join(missing)}</span>"
-            if missing else "<span class='c ok'>all platforms posted</span>")
-    return (f"<div class=card id='{esc(s.slug)}'>"
+    todo = (f"<span class='c warn'>to post on YouTube</span>"
+            if missing else "<span class='c ok'>on YouTube</span>")
+    posted = bool(s.ledger.get("youtube"))
+    return (f"<div class=card id='{esc(s.slug)}'" + (f" data-hide='{esc(s.slug)}'" if posted else "") + ">"
+            + (hide_btn(s.slug) if posted else "")
             + thumb_img(thumbs, "16x9" if s.kind == "long" else "9x16") +
             f"<h3>{badge}{esc(s.title)} <span class=slug>{esc(s.slug)}"
             f"{' · ' + esc(s.cluster) if s.cluster else ''}</span> {todo}</h3>"
@@ -195,7 +200,7 @@ def swirls_card(title: str, slug: str, final: Path | None, ledger_entry: dict) -
         links.append(flink(pub / "PUBLISH_INDEX.html", "📦 publish pack (copy buttons)"))
     if (pub / "captions.srt").is_file():
         links.append(flink(pub / "captions.srt", "📝 captions.srt"))
-    for key, lbl in (("16x9", "🖼 16:9"), ("9x16", "🖼 9:16 (Shorts/TikTok/Reels)"), ("1x1", "🖼 1:1")):
+    for key, lbl in (("16x9", "🖼 16:9"), ("9x16", "🖼 9:16 (Shorts)")):
         t = pub / "thumbs" / f"thumb_{key}.jpg"
         if t.is_file():
             links.append(flink(t, lbl))
@@ -215,10 +220,13 @@ def swirls_card(title: str, slug: str, final: Path | None, ledger_entry: dict) -
                 f"<td><input id='{iid}' placeholder='paste the {esc(plat)} URL after uploading'></td>"
                 f"<td><button onclick=\"swirls_cmd(this,'{esc(slug)}','{esc(plat)}')\">COPY command</button></td></tr>")
 
-    todo = (f"<span class='c warn'>to post: {', '.join(missing)}</span>"
-            if missing else "<span class='c ok'>all platforms posted</span>")
+    todo = (f"<span class='c warn'>to post on YouTube</span>"
+            if missing else "<span class='c ok'>on YouTube</span>")
     subref = f" · {esc(ref)}" if ref else ""
-    card_html = (f"<div class=card id='swirls-{esc(slug)}'>"
+    posted = "youtube" in ledger_entry
+    card_html = (f"<div class=card id='swirls-{esc(slug)}'"
+                 + (f" data-hide='swirls-{esc(slug)}'" if posted else "") + ">"
+                 + (hide_btn(f"swirls-{slug}") if posted else "")
                 + thumb_img(pub / "thumbs", "9x16") +
                 f"<h3><span class='c swirls'>SWIRLS OF LIFE</span> {esc(title)} "
                 f"<span class=slug>{esc(slug)}{subref}</span> {todo}</h3>"
@@ -443,7 +451,7 @@ def main() -> int:
     n_queue, n_posted = len(queue) + n_swirls_todo, len(posted) + n_swirls_done
     canon = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in CANON)
 
-    page = f"""<!doctype html><meta charset=utf-8><title>Awakeden upload tracker</title>
+    page = f"""<!doctype html><meta charset=utf-8><title>YouTube upload tracker</title>
 <style>body{{font-family:Segoe UI,system-ui,sans-serif;background:#171410;color:#ece5d8;margin:0;padding:24px;max-width:1080px}}
 h1{{font-family:Georgia,serif;font-size:22px;margin:0 0 4px}} h2{{font-family:Georgia,serif;font-size:17px;margin:26px 0 8px}}
 .sub{{color:#a89e8e;font-size:13px;margin-bottom:6px;line-height:1.5}}
@@ -461,6 +469,8 @@ button.big{{padding:9px 16px;font-size:13px}}
 .c{{display:inline-block;font-size:11px;font-weight:700;padding:1px 8px;border-radius:99px}}
 .ok.c,.c.ok{{background:#1e3324;color:#7dbb8b}} .c.warn{{background:#37301c;color:#d9a94a}} .c.long{{background:#2a1d2e;color:#c99ad9}}
 .c.swirls{{background:#1c2e3a;color:#7ab8d9}}
+button.hide{{float:right;background:#38322a;color:#ece5d8;margin-left:8px}}
+.card.hidden{{display:none}} body.showhid .card.hidden{{display:block;opacity:.45}}
 .canon td:first-child{{color:#a89e8e;width:280px}}
 .epblock{{border:1px solid #4a3f2e;border-radius:10px;padding:4px 12px 12px;margin:16px 0;background:#1b1712}}
 .epblock-head h3{{margin:10px 0 4px;font-size:16px;font-family:Georgia,serif}}
@@ -468,35 +478,33 @@ button.big{{padding:9px 16px;font-size:13px}}
 .epblock .bar.posted{{background:#c9a55a;height:100%}}
 .epblock .card{{background:#211d17}}
 .inv th{{text-align:left;color:#b59e86;font-size:12px}} .inv .bad{{color:#e0675d}} .inv a{{color:#c9a55a}}</style>
-<h1>Awakeden — upload tracker</h1>
-<div class=sub>Every upload-ready piece, longs and shorts, in one place — the main catalogue
+<h1>YouTube upload tracker</h1>
+<div class=sub>YouTube links only. Every upload-ready piece, longs and shorts, in one place — the main catalogue
 (<code>data/release_ledger.json</code>) AND <span class='c swirls'>SWIRLS OF LIFE</span>
 (its own <code>poc_living_water_ink_style_test/_swirls_release_ledger.json</code> — a
 separate ledger and COPY command, since it isn't part of the site catalogue). This page
 is a view; regenerate: <code>.venv\\Scripts\\python.exe build_upload_tracker.py</code></div>
 <div class=flow><b>The loop, per video:</b><br>
 1. Open the piece's <b>📦 publish pack</b> — copy buttons for title, description, tags, captions.<br>
-2. Upload by hand (video file + the right thumbnail: 16:9 for YouTube longs, 9:16 for Shorts, TikTok cover for TikTok).<br>
-3. Paste the published URL into the platform's box below → <b>COPY command</b> → paste + run it in the repo terminal.<br>
-&nbsp;&nbsp;&nbsp;That logs the dated URL, and a YouTube URL also updates the website read page automatically.<br>
-4. Batch finished → deploy <code>_website</code> → run <code>release_check.py</code> (must be GREEN).</div>
+2. Upload to YouTube by hand (video file + thumbnail: 16:9 for longs, 9:16 for Shorts).<br>
+3. Paste the YouTube URL into the box below → <b>COPY command</b> → paste + run it in the repo terminal.<br>
+4. Run <code>release_check.py</code> (must be GREEN).<br>
+<b>Hide</b> on a posted card tucks it away. <b>Show hidden</b> brings them back.</div>
 <button class=big onclick="all_cmds(this)">COPY ALL filled boxes as one script</button>
 <h2>YouTube settings — same every video</h2>
 <div class=card><table class=canon>{canon}</table></div>
 <h2>Next up to post ({n_queue}) — in calendar order</h2>
-<div class=sub>Swirls of Life is on HOLD until 30 episodes (hidden here). Not ready: Psalm 22 LONG
-(awaiting catalogue approval). Pre-launch checklist items still open in RELEASE_CALENDAR.md:
-channel dress/playlist, brand fields, safe-zone test upload.</div>
+<div class=sub>Swirls of Life is on HOLD until 30 episodes (listed further down).</div>
 {cards_todo or "<div class=sub>nothing ready and unposted</div>"}
 <h2>On hold: Swirls of Life ({n_swirls_held}) &mdash; 30-episode rule</h2>
 <div class=sub>Finished Swirls episodes. NOT to be posted until 30 episodes exist. The URL boxes work, so a URL
-can still be logged if you ever break the hold. Once every platform is logged, the episode moves to Posted.</div>
+can still be logged if you ever break the hold. Once its YouTube link is logged, the episode moves to Posted.</div>
 {cards_held or "<div class=sub>none on hold</div>"}
 <h2>All other finished media — ready state ({inv_counts["blocked"] + inv_counts["hold"]})</h2>
 <div class=sub>Everything with a finished video on disk that is NOT in the list above, and exactly what it still needs.
 Red ✗ = missing. Nothing here can be logged until it is cleared and has a pack.</div>
 {inv_html}
-<h2>Posted ({n_posted})</h2>
+<h2>Posted ({n_posted}) <button id=showhid onclick="toggleShow()">Show hidden</button></h2>
 {cards_done or "<div class=sub>nothing posted yet</div>"}
 <script>
 function copy(t, btn) {{
@@ -519,6 +527,22 @@ function swirls_cmd(btn, slug, plat) {{
   copy('.venv\\\\Scripts\\\\python.exe poc_living_water_ink_style_test\\\\swirls_upload_tracker.py --set '
        + slug + ' ' + plat + ' "' + url + '"', btn);
 }}
+let HID = [];
+try {{ HID = JSON.parse(localStorage.getItem('yt_tracker_hidden') || '[]'); }} catch (e) {{ HID = []; }}
+function saveHid() {{ try {{ localStorage.setItem('yt_tracker_hidden', JSON.stringify(HID)); }} catch (e) {{}} }}
+function paint() {{
+  let n = 0;
+  document.querySelectorAll('.card[data-hide]').forEach(c => {{
+    const h = HID.includes(c.dataset.hide); if (h) n++;
+    c.classList.toggle('hidden', h);
+    const b = c.querySelector('button.hide'); if (b) b.textContent = h ? 'Unhide' : 'Hide';
+  }});
+  const s = document.getElementById('showhid');
+  if (s) s.textContent = (document.body.classList.contains('showhid') ? 'Hide hidden' : 'Show hidden') + ' (' + n + ')';
+}}
+function toggleHide(k) {{ HID = HID.includes(k) ? HID.filter(x => x !== k) : HID.concat([k]); saveHid(); paint(); }}
+function toggleShow() {{ document.body.classList.toggle('showhid'); paint(); }}
+paint();
 function all_cmds(btn) {{
   const lines = [];
   document.querySelectorAll('input[id^="u_"]').forEach(i => {{
diff --git a/data/upload_brand.json b/data/upload_brand.json
index 12c5f4b..ad14210 100644
--- a/data/upload_brand.json
+++ b/data/upload_brand.json
@@ -1,28 +1,28 @@
 {
   "_note": "THE ONE PLACE you edit your brand identity. The Upload Kit stage stamps this footer into every description. Fill the FILL_ME values once; leave any you don't have yet as FILL_ME and the footer just skips that line. Nothing here is generated by the model - it is verbatim, so your handles can never be hallucinated.",
-  "channel_name": "Awakeden",
-  "brand_short": "Awakeden",
-  "cta_line": "Find Jesus in the whole Bible, one story at a time. Subscribe to Awakeden. ✝",
-  "cta_line_social": "Find Jesus in the whole Bible, one story at a time. Follow Awakeden. ✝",
+  "channel_name": "Salt and Light Kingdom",
+  "brand_short": "Salt and Light Kingdom",
+  "cta_line": "Find Jesus in the whole Bible, one story at a time. Subscribe to Salt and Light Kingdom. ✝",
+  "cta_line_social": "Find Jesus in the whole Bible, one story at a time. Follow Salt and Light Kingdom. ✝",
   "handles": {
     "youtube": {
-      "handle": "@awakeden",
-      "url": "https://youtube.com/@awakeden"
+      "handle": "@saltandlightkingdomorg",
+      "url": "https://www.youtube.com/@saltandlightkingdomorg"
     },
     "tiktok": {
-      "handle": "FILL_ME",
-      "url": "FILL_ME"
+      "handle": "@saltandlightkingdom",
+      "url": "https://www.tiktok.com/@saltandlightkingdom"
     },
     "facebook": {
-      "handle": "FILL_ME",
-      "url": "FILL_ME"
+      "handle": "Salt and Light Kingdom",
+      "url": "https://www.facebook.com/profile.php?id=61588658953392"
     },
     "instagram": {
-      "handle": "FILL_ME",
-      "url": "FILL_ME"
+      "handle": "@salt.andlightkingdomorg",
+      "url": "https://www.instagram.com/salt.andlightkingdomorg/"
     }
   },
-  "website": "https://awakeden.com",
+  "website": "",
   "scripture_note": "Scripture quoted from the King James Version (KJV), public domain.",
   "evergreen_hashtags": [
     "#Bible",
@@ -37,7 +37,6 @@
   "footer_order": [
     "cta_line",
     "follow_block",
-    "website",
     "scripture_note"
   ]
-}
\ No newline at end of file
+}
diff --git a/pipeline/channel_dress.py b/pipeline/channel_dress.py
index 85a2fdf..122ae2d 100644
--- a/pipeline/channel_dress.py
+++ b/pipeline/channel_dress.py
@@ -83,7 +83,11 @@ def draw_wordmark(im: Image.Image, x: float, y: float, size: int,
                   tracking: float = 0.14, glow: bool = True, shadow: bool = False) -> float:
     """Site wordmark exactly as site.css renders it: AWAK bone + EDEN red-bright
     (with the site's red glow), letterspaced Arial Black. (User call 2026-07-21:
-    match the website - the earlier shared split-E is retired.)"""
+    match the website - the earlier shared split-E is retired.)
+
+    RETIRED 2026-11-16: the Awakeden brand is no longer supported (owner), so
+    this draws nothing. Every thumbnail script that calls it now renders clean."""
+    return 0.0
     f = font(ARIAL_BLK, size)
     if glow:
         from PIL import ImageFilter
diff --git a/pipeline/release_state.py b/pipeline/release_state.py
index 4b2ed10..d44528e 100644
--- a/pipeline/release_state.py
+++ b/pipeline/release_state.py
@@ -27,6 +27,9 @@ LEDGER = ROOT / "data" / "release_ledger.json"
 
 PLATFORMS = ["youtube", "tiktok", "facebook", "instagram"]
 LONG_POST_PLATFORMS = ["youtube"]  # matches LONG_PLATFORMS in publish_pack
+# Owner rule 2026-11-16: only YouTube links are tracked (shorts and longs alike).
+# PLATFORMS stays the list --set accepts; TRACKED_PLATFORMS drives the queue.
+TRACKED_PLATFORMS = ["youtube"]
 
 # public_status tiers that MUST be fully wired (fail-closed)
 _SHIPPED = {"studio_complete", "live"}
@@ -66,7 +69,7 @@ class PieceState:
 
     @property
     def post_platforms(self) -> list[str]:
-        return LONG_POST_PLATFORMS if self.kind == "long" else PLATFORMS
+        return TRACKED_PLATFORMS
 
     @property
     def pack_fresh(self) -> bool:
@@ -299,24 +302,8 @@ def run_gates(states: list[PieceState], orphans: list[str],
                         "rendered in LEGACY Baroque oil-painting style - never ships; "
                         "rebuild stills+animation in the graphic-novel standard before "
                         "this can be studio_complete/live"))
-        # G5 website (read_page + read-frame anchor don't need the final video)
-        if s.read_page and not s.has_read_source:
-            out.append(("SYNC-G5", "WARN", s.slug,
-                        "read page exists but manifest has no read_source: - frame "
-                        "freshness is UNGATED (restore the field)"))
-        if s.read_page:
-            if s.read_video and not s.read_fresh:
-                out.append(("SYNC-G5", "WARN", s.slug,
-                            "read-page frames not provably from the current scored video "
-                            "(re-run _website/build_readpage.py --force)"))
-            want = f"https://awakeden.com/read/{s.slug}.html"
-            if s.read_url_meta and s.read_url_meta != want:
-                out.append(("SYNC-G5", "FAIL", s.slug,
-                            f"publish_meta.json read_url = {s.read_url_meta} but the page is {want}"))
-            if not s.read_url_meta and shipped:
-                out.append(("SYNC-G5", "WARN", s.slug, "publish_meta.json has no read_url (footer loses the site link)"))
-        elif live:
-            out.append(("SYNC-G5", "WARN", s.slug, "live but no read page (set read_source: + build_readpage.py)"))
+        # G5 website checks RETIRED 2026-11-16: the old read-page website is no
+        # longer supported (owner), so read pages / read_url are not gated.
         if not s.video:
             continue
         # G3 pack freshness
diff --git a/pipeline/test_episode_state.py b/pipeline/test_episode_state.py
index 09014b8..0c8ce41 100644
--- a/pipeline/test_episode_state.py
+++ b/pipeline/test_episode_state.py
@@ -147,7 +147,7 @@ def test_status_live_long_with_regressed_final_never_hides_as_in_production():
 
 def test_shorts_posted_any_vs_fully_posted():
     partial_ledger = _short("a", built=True)
-    partial_ledger.ledger = {"youtube": {"url": "u"}}  # only 1 of 4 platforms
+    partial_ledger.ledger = {"tiktok": {"url": "u"}}  # an untracked platform only (YouTube is the one tracked)
     ep = EpisodeState(slug="x", long=_long(built=True, posted=True),
                       shorts=[partial_ledger, _short("b", built=True)])
     assert ep.shorts_posted == 0          # not fully posted anywhere
diff --git a/pipeline/test_release_state.py b/pipeline/test_release_state.py
index 580cc89..e34cec6 100644
--- a/pipeline/test_release_state.py
+++ b/pipeline/test_release_state.py
@@ -93,24 +93,13 @@ def test_g4_thumbs_warn_when_studio_fail_when_live():
 
 
 # ---- SYNC-G5 website ---------------------------------------------------------
-def test_g5_read_url_mismatch_fails():
-    s = _shipped(read_page=True, has_read_source=True,
-                 read_url_meta="https://awakeden.com/read/WRONG.html")
-    assert hits(run_gates([s], []), "SYNC-G5", "p", "FAIL")
-
-
-def test_g5_stale_read_frames_warn():
-    s = _shipped(read_page=True, has_read_source=True,
-                 read_url_meta="https://awakeden.com/read/p.html",
-                 read_video=Path("x/v_scored.mp4"), read_video_sha="NEW", read_meta_sha="OLD")
-    assert hits(run_gates([s], []), "SYNC-G5", "p", "WARN")
-
-
-def test_g5_read_page_without_read_source_warns():
-    # red-team M5: deleting read_source silently disarmed frame freshness
+def test_g5_read_url_checks_retired():
+    # 2026-11-16: the old website is retired, so read_url / read-page frames are not gated
     s = _shipped(read_page=True, has_read_source=False,
-                 read_url_meta="https://awakeden.com/read/p.html")
-    assert hits(run_gates([s], []), "SYNC-G5", "p", "WARN")
+                 read_url_meta="https://example.invalid/read/WRONG.html",
+                 read_video=Path("x/v_scored.mp4"), read_video_sha="NEW", read_meta_sha="OLD")
+    assert not hits(run_gates([s], []), "SYNC-G5", "p", "FAIL")
+    assert not hits(run_gates([s], []), "SYNC-G5", "p", "WARN")
 
 
 def test_g5_orphan_read_page_warns():
@@ -235,7 +224,7 @@ def test_to_post_long_first_then_cluster_order():
     q = release_state.to_post([s2, long, s1])
     assert [s.slug for s, _ in q] == ["L", "s1", "s2"]
     assert q[0][1] == ["youtube"]                      # long posts YouTube only
-    assert q[1][1] == release_state.PLATFORMS          # shorts post all four
+    assert q[1][1] == ["youtube"]                      # shorts too: only YouTube is tracked (2026-11-16)
 
 
 def test_to_post_skips_unshipped_and_posted():
diff --git a/pipeline/thumbnails.py b/pipeline/thumbnails.py
index 1a922ae..111e280 100644
--- a/pipeline/thumbnails.py
+++ b/pipeline/thumbnails.py
@@ -462,7 +462,7 @@ def main() -> int:
     flt = sys.argv[1] if len(sys.argv) > 1 else ""
     if flt == "--swirls" or (flt and (Path(flt) / "episode.py").is_file()):
         return _main_swirls(flt)
-    brand_assets(ROOT / "_brand")
+    # brand_assets() no longer runs: the old wordmark brand is retired (2026-11-16)
     states, _orphans, _orphan_pages = release_state.gather()
     made, skipped = [], []
     for s in states:
diff --git a/pipeline/upload_engine.py b/pipeline/upload_engine.py
index e66cfce..1888b46 100644
--- a/pipeline/upload_engine.py
+++ b/pipeline/upload_engine.py
@@ -36,7 +36,7 @@ def _filled(v: str | None) -> bool:
 def build_footer(platform: str, brand: dict, read_url: str = "") -> str:
     """Verbatim brand footer. Full (with links) on YouTube/Facebook; minimal,
     link-free on TikTok/Instagram (links aren't clickable there). `read_url` is
-    the piece's own read-the-panels page on awakeden.com."""
+    ignored: the old read-the-panels website is retired (owner, 2026-11-16)."""
     # "Subscribe" is YouTube's verb; TikTok/Facebook/Instagram say "Follow"
     # (panel-convergent fix, user-approved 2026-07-21). cta_line_social falls
     # back to cta_line so a brand file without it keeps working.
@@ -52,8 +52,6 @@ def build_footer(platform: str, brand: dict, read_url: str = "") -> str:
         lines.append(cta)
 
     link_friendly = platform.startswith("youtube") or platform == "facebook"
-    if link_friendly and _filled(read_url):
-        lines.append(f"Read it panel by panel: {read_url}")
     if link_friendly:
         follow: list[str] = []
         for plat, key in [("YouTube", "youtube"), ("TikTok", "tiktok"),
@@ -148,8 +146,8 @@ def _harvest_batch_facts(d: Path, fmt: str = "short") -> SourceFacts:
         media_dir=str(d),
         video_path=_find_video(d, fmt),
         format=fmt,
-        series_name=meta.get("series", "Awakeden"),
-        brand=meta.get("brand", "Awakeden"),
+        series_name=meta.get("series", "Salt and Light Kingdom"),
+        brand=meta.get("brand", "Salt and Light Kingdom"),
         episode_title=title,
         anchor_ref=anchor_ref,
         anchor_kjv=anchor_kjv,
@@ -209,7 +207,7 @@ def _harvest_swirls_facts(d: Path) -> SourceFacts:
         video_path=_find_video(d, "short"),
         format="short",
         series_name="Swirls of Life",
-        brand="Awakeden",
+        brand="Salt and Light Kingdom",
         episode_title=title,
         anchor_ref=anchor_ref,
         anchor_kjv=anchor_kjv,
diff --git a/tools_strip_ai_wording.py b/tools_strip_ai_wording.py
index 3bb3658..b27f098 100644
--- a/tools_strip_ai_wording.py
+++ b/tools_strip_ai_wording.py
@@ -8,8 +8,10 @@ PAT = re.compile(r"[ \t]*(Art(?:, music)? and voices made with AI(?: tools)?\.|A
 SKIP = ("_independent_review", "red_team", "_redteam", "panel", "prompt", "_pre_")
 apply = "--apply" in sys.argv
 n_files = n_hits = 0
-for base in ("batches", "longform", "poc_desert_storybook_heroes", "poc_pop_halftone", "poc_folk_print_style"):
-    for p in (ROOT / base).rglob("*"):
+# Whole repo (2026-11-16: the old 5-folder list missed every Swirls pack).
+for base in ("",):
+    for p in ROOT.rglob("*"):
+        if any(x in p.parts for x in (".venv", "node_modules", ".git")): continue
         if p.suffix not in (".md", ".html", ".json", ".txt") or not p.is_file(): continue
         rel = str(p.relative_to(ROOT)).replace("\\", "/")
         if any(s in rel for s in SKIP): continue
```

## New tool: tools_strip_awakeden.py
```python
"""Owner rule 2026-11-16: the Awakeden brand + awakeden.com site are retired.
Rewrites every PUBLIC text file (publish packs, upload kits, publish_meta.json) to the
Salt and Light Kingdom brand and drops every awakeden.com link. Review/panel transcripts
are history and are left alone.
Usage: python tools_strip_awakeden.py [--apply]   (dry run by default)"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SKIP = ("_independent_review", "red_team", "_redteam", "panel", "prompt", "_pre_")
YT_H, YT_U = "@saltandlightkingdomorg", "https://www.youtube.com/@saltandlightkingdomorg"
NL = r"(?:\r?\n|\n|<br>)"
LINK = r"https?://(?:www\.)?awakeden\.com[^\s\"'<\)]*"

def fix(t: str, name: str) -> str:
    t = re.sub(NL + r"?[ \t]*Read it panel by panel:[ \t]*" + LINK, "", t)
    t = t.replace("@awakeden (https://youtube.com/@awakeden)", f"{YT_H} ({YT_U})")
    t = re.sub(r"https?://(?:www\.)?youtube\.com/@awakeden", YT_U, t)
    follow = {"tiktok.md": "Follow @saltandlightkingdom", "instagram.md": "Follow @salt.andlightkingdomorg"}
    if name in follow:
        t = t.replace("Follow @awakeden", follow[name])
    else:
        t = re.sub(NL + r"?[ \t]*Follow @awakeden(?=" + NL + r"|$|\")", "", t)
    t = re.sub(r"(" + NL + r"){1,2}[ \t]*" + LINK + r"[ \t]*(?=" + NL + r"|$|\"|</)", "", t)  # bare site line
    t = re.sub(r"(\"read_url\":\s*)\"" + LINK + "\"", r'\1""', t)
    t = re.sub(LINK, "", t)
    t = t.replace("#Awakeden", "#SaltAndLightKingdom")
    t = re.sub(r"\bAWAKEDEN\b", "SALT AND LIGHT KINGDOM", t)
    t = re.sub(r"\b[Aa]wakeden\b", "Salt and Light Kingdom", t)
    return t

apply = "--apply" in sys.argv
nf = 0
for p in ROOT.rglob("*"):
    if any(x in p.parts for x in (".venv", "node_modules", ".git", "_website")): continue
    if p.suffix not in (".md", ".html", ".json", ".txt") or not p.is_file(): continue
    rel = str(p.relative_to(ROOT)).replace("\\", "/")
    if any(s in rel for s in SKIP): continue
    if not (any(d in rel for d in ("/publish/", "/upload/")) or p.name == "publish_meta.json"): continue
    t = p.read_text(encoding="utf-8")
    if not re.search("awakeden", t, re.I): continue
    new = fix(t, p.name)
    nf += 1
    left = len(re.findall("awakeden", new, re.I))
    print(("FIX " if apply else "would fix ") + rel + (f"   !! {left} left" if left else ""))
    if apply: p.write_text(new, encoding="utf-8")
print(f"{'fixed' if apply else 'would fix'} {nf} files")
```

## Video logo patch script (used on 17 re-cut videos)
```python
"""Remove the burned AWAKEDEN logo from a re-cut (v5hook) by patching only the logo
corner from the clean source; any pixel where the re-cut differs from its watermarked
source (a hook/decode card) is kept from the re-cut."""
import json, subprocess, sys, shutil
from pathlib import Path
def probe(p):
    j = json.loads(subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-count_packets",
        "-show_entries","stream=width,height,r_frame_rate,nb_read_packets","-show_entries","format=duration",
        "-of","json",str(p)],capture_output=True,text=True,check=True).stdout)
    s = j["streams"][0]; return s["width"], s["height"], s["r_frame_rate"], int(s["nb_read_packets"]), float(j["format"]["duration"])
A, W, C, OUT = map(Path, sys.argv[1:5])
pa, pw, pc = probe(A), probe(W), probe(C)
assert pa[:3] == pw[:3] == pc[:3], (pa, pw, pc)
assert abs(pa[3]-pw[3]) <= 1 and abs(pw[3]-pc[3]) <= 1, (pa, pw, pc)
w, h = pa[0], pa[1]
if h > w:
    bx, by, bw, bh = round(w*28/1080), round(h*58/1920), round(w*226/1080), round(h*64/1920)
else:
    ww = round(w*260/1920); bx = w-ww-round(w*28/1920)-12; by = round(h*16/1080); bw = ww+24; bh = round(ww*320/1743)+28
bw += (-bw) % 16; bh += (-bh) % 16; bx -= bx % 2; by -= by % 2
crop = f"crop={bw}:{bh}:{bx}:{by}"
fc = (f"[0:v]split[a][abg];[a]{crop},split[ac][ag];[1:v]{crop},format=gray[wg];[2:v]{crop},format=gbrp[cc];"
      f"[ag]format=gray[ag2];[ag2][wg]blend=all_mode=difference,lut=y='if(gt(val,22),255,0)',"
      f"dilation,dilation,format=gbrp[m];[ac]format=gbrp[acg];[cc][acg][m]maskedmerge,format=yuv444p[patch];"
      f"[abg][patch]overlay={bx}:{by}:format=auto,format=yuv420p[v]")
tmp = OUT.with_name(OUT.stem + ".tmp.mp4")
subprocess.run(["ffmpeg","-y","-v","error","-i",str(A),"-i",str(W),"-i",str(C),"-filter_complex",fc,
    "-map","[v]","-map","0:a?","-c:v","libx264","-crf","17","-preset","medium","-c:a","copy",
    "-movflags","+faststart",str(tmp)],check=True)
pt = probe(tmp)
assert abs(pt[4]-pa[4]) < 0.05 and pt[3] == pa[3], (pt, pa)
tmp.replace(OUT); print("OK", OUT.name, f"box {bw}x{bh}@{bx},{by}")
```

## Sample public pack files AFTER the change
### batches/cluster_01_cross/it_is_finished_john1930/publish/youtube_short.md
```
# youtube_short — YouTube (Short)

## TITLE
The First Time the Bible Says Finished, Nothing Was Broken

## DESCRIPTION
It is finished (John 19:30). But the FIRST time the Bible says finished, nothing was broken yet: thus the heavens and the earth were finished, and all the host of them (Genesis 2:1). Creation complete. God rested. He does not leave work half done.

When sin wrecked that world, the Son came down to mend it. All things were made by him; the hands that finished creation came to finish redemption.

"When Jesus therefore had received the vinegar, he said, It is finished: and he bowed his head, and gave up the ghost" (John 19:30, KJV).

Two finished works. One Workman. He finished creation and rested; he finished redemption and rested in the tomb through the sabbath. And on the first day, morning came.

You were never asked to finish it. You are asked to rest in it. He bowed his head so you could lift yours. The work is finished. Enter his rest.

Find Jesus in the whole Bible, one story at a time. Subscribe to Salt and Light Kingdom. ✝

Follow:
YouTube: @saltandlightkingdomorg (https://www.youtube.com/@saltandlightkingdomorg)

Scripture quoted from the King James Version (KJV), public domain.

#Bible #Jesus #ItIsFinished #Gospel #KJV

## TAGS
john 19 30, it is finished, tetelestai, words from the cross, genesis 2 1, creation and redemption, kjv bible, bible shorts, the crucifixion, jesus christ, gospel, rest in christ

## HASHTAGS
#Bible #Jesus #ItIsFinished #Gospel #KJV
```
### batches/cluster_01_cross/it_is_finished_john1930/publish/tiktok.md
```
# tiktok — TikTok

## CAPTION
The first time the Bible says finished, nothing was broken yet. Creation: finished, then rest. Redemption: finished, then the tomb-rest, then MORNING. Two finished works. One Workman. You were never asked to finish it. Rest in it.

Find Jesus in the whole Bible, one story at a time. Follow Salt and Light Kingdom. ✝

Follow @saltandlightkingdom

#Bible #Jesus #ItIsFinished #Cross #Gospel #KJV

## HASHTAGS
#Bible #Jesus #ItIsFinished #Cross #Gospel #KJV
```
### batches/cluster_01_cross/it_is_finished_john1930/publish/instagram.md
```
# instagram — Instagram (Reel)

## CAPTION
The first time the Bible says finished, nothing was broken yet. (Genesis 2:1)

The second time, everything broken was being mended. (John 19:30)

Two finished works. One Workman. He bowed his head so you could lift yours. Enter his rest.

Find Jesus in the whole Bible, one story at a time. Follow Salt and Light Kingdom. ✝

Follow @salt.andlightkingdomorg

#Bible #Jesus #ItIsFinished #Cross #Gospel #KJV #Creation #BibleShorts #SaltAndLightKingdom

## HASHTAGS
#Bible #Jesus #ItIsFinished #Cross #Gospel #KJV #Creation #BibleShorts #SaltAndLightKingdom
```
### batches/cluster_01_cross/it_is_finished_john1930/publish/facebook.md
```
# facebook — Facebook (Reel/Video)

## TITLE
Two Finished Works. One Workman.

## DESCRIPTION
It is finished (John 19:30). The first finished was creation: "Thus the heavens and the earth were finished" (Genesis 2:1). The hands that finished creation came back to finish redemption: "he said, It is finished: and he bowed his head, and gave up the ghost."

He rested after each. And on the first day, morning came.

You were never asked to finish the work. You are asked to rest in it. He bowed his head so you could lift yours.

Find Jesus in the whole Bible, one story at a time. Follow Salt and Light Kingdom. ✝

Follow:
YouTube: @saltandlightkingdomorg (https://www.youtube.com/@saltandlightkingdomorg)

Scripture quoted from the King James Version (KJV), public domain.

#Bible #Jesus #ItIsFinished

## HASHTAGS
#Bible #Jesus #ItIsFinished
```
### poc_living_water_ink_style_test/swirls_episode_04_naaman_in_the_jordan/publish/youtube_short.md
```
# youtube_short — YouTube (Short)

## TITLE
He Told One Story and They Tried to Kill Him For It

## DESCRIPTION
Jesus told his hometown congregation one old story, and they tried to throw him off a cliff for it (Luke 4:28-29). This is that story.

Naaman was a great general and a leper. A servant girl pointed him to a prophet. The prophet did not even come outside. He sent one line: wash in the Jordan, seven times.

Naaman was furious: "Are not Abana and Pharpar, rivers of Damascus, better than all the waters of Israel? may I not wash in them, and be clean?"

His own servants stopped him: "My father, if the prophet had bid thee do some great thing, wouldest thou not have done it? how much rather then, when he saith to thee, Wash, and be clean?"

He went down. He washed, seven times. New skin, like a child's.

The best thing Naaman ever did was lose that argument.

Find Jesus in the whole Bible, one story at a time. Subscribe to Salt and Light Kingdom. ✝

Follow:
YouTube: @saltandlightkingdomorg (https://www.youtube.com/@saltandlightkingdomorg)

Scripture quoted from the King James Version (KJV), public domain.

#Bible #Jesus #Naaman #Elisha

## TAGS
2 Kings 5, Naaman leper healed, Elisha the prophet, Jesus in Nazareth, Luke 4 sermon, Jesus and Naaman, Bible story of healing, KJV Bible story, wash in the Jordan, faith and obedience

## HASHTAGS
#Bible #Jesus #Naaman #Elisha
```
### poc_living_water_ink_style_test/swirls_episode_04_naaman_in_the_jordan/publish/instagram.md
```
# instagram — Instagram (Reel)

## CAPTION
A general got leprosy. The cure felt too small for a man like him: wash in a river seven times. His own servants talked him into trying it anyway. New skin, like a child's. Jesus later told this exact story back home, and it nearly got him killed.

Find Jesus in the whole Bible, one story at a time. Follow Salt and Light Kingdom. ✝

#Bible #Jesus #Naaman #Elisha #Healing #Faith #KJV

## HASHTAGS
#Bible #Jesus #Naaman #Elisha #Healing #Faith #KJV
```

## Other facts
- Bulk word replace Awakeden->Salt and Light Kingdom also ran on ~60 docs/skills/code files (v2 specs, STATE.md, eyewitness gates, hook_gate prompt, test fixtures). Review transcripts and _website/ were left alone.
- release_check.py after the change: 89 items, 0 FAIL, GREEN. pytest pipeline: 463 pass, 9 fail (all test_run_piece KeyError 'stills', pre-existing, files untouched).
- Tracker page: _UPLOAD_TRACKER.html regenerated by build_upload_tracker.py.
