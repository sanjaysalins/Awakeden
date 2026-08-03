"""Build _STILLS_REVIEW.html for the Bronze Serpent LONG pilot -- all 68
spreads from _PLAN.md's table, in spread-number order, following the visual
pattern of poc_living_sketchbook/bronze_serpent/_STILLS_REVIEW.html (dark
card grid, status badges). Safe to re-run at any point during the batch --
each card's status reflects whatever is on disk right now (PENDING if the
PNG doesn't exist yet, RENDERED if it does).

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_build_review.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _s2_stills as s2

OUT_HTML = HERE / "_STILLS_REVIEW.html"

# (spread#, name, beat, window, one-line caption, approved?)
ROWS = [
    (1, "s01_wide", 1, "0.40-7.50s", "Wide establishing: aged Moses, wilderness camp behind", False),
    (2, "s02_triptych", 1, "7.50-17.00s", "Triptych memory-vignette: rod-to-serpent / Red Sea split / water from the rock", False),
    (3, "s03_eyes_haunted", 1, "17.00-21.50s", "Close on Moses's eyes, haunted -- \"follows me still\"", False),
    (4, "s04_icon_pole", 1, "21.50-27.50s", "THE ICON: pole in the sand, bronze serpent revealed", False),
    (5, "s05_graves", 1, "27.50-32.50s", "Graves being dug, the dying, grief -- wide", False),
    (6, "s06_dying_hand_eye", 1, "32.50-37.10s", "Close: a dying man's reaching hand, then an eye -- \"look not climb\"", False),
    (7, "s07_ungrateful_camp", 2, "37.10-43.00s", "Wide: the freed-but-ungrateful camp", False),
    (8, "s08_wandering_column", 2, "43.00-53.00s", "Wide: the wandering column, round Edom, barren road", False),
    (9, "s09_manna_scorned", 2, "53.00-61.52s", "Manna falling, faithfully, being turned from/scorned", False),
    (10, "s10_vc_discouraged", 2, "62.22-67.50s", "Verse card: \"the soul of the people was much discouraged...\"", False),
    (11, "s11_crowd_angry", 2, "68.20-76.04s", "Crowd turns angry, toward Moses and toward heaven", False),
    (12, "s12_vc_wherefore", 2, "76.74-87.62s", "Verse card: [the people] \"Wherefore have ye brought us up...\"", False),
    (13, "s13_vignette_calf", 2, "88.32-98.00s", "Memory-vignette: the sea / the rock / the golden calf under the cloud at Sinai", False),
    (14, "s14_serpent_hint", 2, "98.00-104.16s", "Something slides in the dust between the tents -- first hint of the serpents", False),
    (15, "s15_vc_fiery_serpents", 2, "104.86-112.06s", "Verse card: \"the LORD sent fiery serpents among the people...\"", False),
    (16, "s16_bite_closeup", 2, "112.76-117.00s", "Close: the bite, \"burned like a coal\" -- heat/glow, not graphic", False),
    (17, "s17_vignette_collapse", 2, "117.00-125.00s", "Vignette: a strong man collapsed + a mother cradling a child", False),
    (18, "s18_moses_empty_hands", 2, "125.00-131.61s", "Moses alone, hands empty, no remedy -- atmosphere beat", False),
    (19, "s19_people_kneel", 3, "131.61-137.56s", "The people kneel before Moses, posture shifts anger to contrition", False),
    (20, "s20_vc_we_have_sinned", 3, "138.26-147.38s", "Verse card: [the people] \"We have sinned, for we have spoken against the LORD...\"", False),
    (21, "s21_moses_intercede", 3, "148.08-154.00s", "Moses interceding, kneeling, arms raised in prayer", False),
    (22, "s22_moses_listening", 3, "154.00-163.84s", "Moses's face -- surprise the LORD did not simply remove the serpents; listening", False),
    (23, "s23_lord_presence", 3, "164.54-169.00s", "THE LORD's presence appears -- Moses shields his eyes, no figure, no face", True),
    (24, "s24_vc_make_thee", 3, "169.00-177.18s", "Illuminated Rubric verse card: [the LORD] \"Make thee a fiery serpent...\"", False),
    (25, "s25_moses_empty_negation", 3, "177.88-184.00s", "Moses processing -- no medicine offered, negation imagery", False),
    (26, "s26_moses_resolve_serpent", 3, "184.00-192.00s", "Moses looking at a live serpent on the ground -- resolve forming", False),
    (27, "s27_hands_gather_ore", 3, "192.00-196.28s", "Close-up hands, beginning the forge", False),
    (28, "s28_forge_acting", 3, "196.98-204.00s", "Acting spread: Moses hammering the bronze serpent into shape", False),
    (29, "s29_pole_first_healing", 3, "204.00-208.98s", "The pole now stands; the first bitten look up, first healing", False),
    (30, "s30_payoff_fever_breaks", 3, "209.68-228.25s", "Payoff: a man's fever breaks as he looks up at the pole", False),
    (31, "s31_moses_why_serpent", 4, "228.25-233.41s", "Close on Moses's face turning the question over: \"Why a serpent?\"", False),
    (32, "s32_pole_silhouette_dusk", 4, "233.41-259.03s", "Wide/mid: the serpent on its pole, silhouetted against the camp at dusk", False),
    (33, "s33_vignette_universal", 4, "259.03-272.61s", "Vignette: strong man / child / dying elder, all lifting their eyes the same way", False),
    (34, "s34_moses_walking_dusk", 4, "272.61-284.83s", "Moses walking alone at dusk, the riddle \"walking home with him every evening\"", False),
    (35, "s35_moses_honest_close", 5, "284.83-293.25s", "Close on elderly Moses's face, direct-address begins: \"I will be honest with you\"", False),
    (36, "s36_proud_man_turns_away", 5, "293.25-314.62s", "A proud man turning away from the pole while others look", False),
    (37, "s37_calf_flashback", 5, "314.62-325.48s", "FLASHBACK, soft-focus/silhouette: grinding the golden calf to powder", True),
    (38, "s38_dread_image", 5, "325.48-344.31s", "THE DREAD IMAGE: Moses holding the bronze serpent, staring at it", False),
    (39, "s39_moses_sleepless_candle", 5, "344.31-350.29s", "Close, night: Moses sleepless, \"had God bidden the very sin I had just broken?\"", False),
    (40, "s40_moses_resolve_returning", 5, "350.29-364.51s", "Moses's resolve returning, hand on the bronze but eyes lifted", False),
    (41, "s41_moses_long_road", 5, "364.51-382.80s", "Wide: Moses at the camp's edge, looking down a long empty road", False),
    (42, "s42_hands_finish_forge", 5, "382.80-387.84s", "Close on hands finishing the forge, quiet -- bookends spread 28", False),
    (43, "s43_insert_scholars_margin2", 6, "388.54-402.14s", "INSERT PAGE 1: Scholar's-Margin typology (Numbers 21 / John 3), Jesus teaching Nicodemus by night", False),
    (44, "s44_shadow_cross", 6, "402.84-410.00s", "Moses's realization: the bronze serpent's shadow, symbolically cross-shaped", False),
    (45, "s45_golgotha_wide", 6, "410.00-420.00s", "Golgotha: Christ lifted on the cross, wide, reverent, restrained", False),
    (46, "s46_thesis_pair", 6, "420.00-425.00s", "Paired composition: bronze serpent + the cross together -- the film's thesis image", False),
    (47, "s47_golgotha_midshot", 6, "425.00-433.48s", "Christ on the cross, reverent, leading into the Gal 3:13 quote", False),
    (48, "s48_vc_curse_for_us", 6, "434.18-441.54s", "Verse card: \"being made a curse for us: ... Cursed is every one that hangeth on a tree\"", False),
    (49, "s49_christ_radiant_begin", 6, "442.24-451.00s", "Christ lifted, radiant register beginning -- \"bore the judgment... taken in our place\"", False),
    (50, "s50_christ_close_words", 6, "451.00-456.48s", "Close, leading into Jesus's own words", False),
    (51, "s51_christ_draw_all_men", 6, "457.18-464.06s", "Red-letter: \"And I, if I be lifted up... will draw all men unto me\"", False),
    (52, "s52_moses_reflecting", 6, "464.76-475.54s", "Moses reflecting, resolved: \"it was never the bronze; it was the looking that God honoured\"", False),
    (53, "s53_moses_know_that_now", 6, "475.54-478.92s", "Brief, close on Moses: \"I know that now better than I once wished to\"", False),
    (54, "s54_timeshift_enshrined", 6, "478.92-486.11s", "TIME SHIFT (generations later): people burning incense before the enshrined serpent", False),
    (55, "s55_hezekiah_breaks", 6, "486.11-493.51s", "Hezekiah -- a YOUNG king -- breaks the bronze serpent to pieces, decisive not shameful", False),
    (56, "s56_moses_affirms", 6, "493.51-498.18s", "Moses's voice affirms: \"he was right to break it. The power was never in my handiwork\"", False),
    (57, "s57_bridge_moses_christ", 6, "498.18-507.64s", "Transition back to Christ/gold register: \"the power was in the God who said look and live\"", False),
    (58, "s58_vc_john316", 6, "508.34-517.38s", "Illuminated Rubric verse card (full ceremony): John 3:16", False),
    (59, "s59_moses_be_still", 7, "518.08-524.00s", "Moses direct-address: \"So hear me -- be still...\"", False),
    (60, "s60_vignette_selfeffort", 7, "524.00-532.00s", "Vignette: strong men trying to walk the fire off, each failing in his own way", False),
    (61, "s61_moses_thatisyou", 7, "532.00-539.00s", "Intimate close on Moses: \"That is you. That is me\"", False),
    (62, "s62_moses_neverasked", 7, "539.00-544.50s", "Close, resolute: \"you were never asked to\"", False),
    (63, "s63_vignette_least_last_child", 7, "544.50-553.00s", "Christ radiant lifted; three small figures below -- the least, the last, a child -- looking up", False),
    (64, "s64_moses_sit_with_that", 7, "553.00-559.00s", "Pause beat, near-silence: \"Sit with that\"", False),
    (65, "s65_christ_open_invite", 7, "559.00-565.00s", "Christ, plain and open: \"costs you nothing but a look\"", False),
    (66, "s66_moses_direct_question", 7, "565.00-576.00s", "Moses turning the question directly to the viewer -- most intimate direct-address", False),
    (67, "s67_insert_gilded_proclamation2", 7, "576.00-585.00s", "INSERT PAGE 2 (Gilded Proclamation echo): \"Not to the bronze, nor to me -- but to Jesus\"", False),
    (68, "s68_landing", 7, "585.00-590.08s (+hold)", "THE LANDING: \"Look to Him, and live.\" Torn-page device, gold light from beneath the tear", False),
]

CSS = """
  body { background:#16181d; color:#e8e4d8; font-family:Georgia, serif; line-height:1.55; padding:28px 18px 90px; }
  .wrap { max-width:1320px; margin:0 auto; }
  h1 { color:#e9c877; font-size:1.8rem; margin-bottom:6px; }
  .sub { color:#9aa0ad; margin-bottom:24px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:16px; }
  .card { background:#1e2129; border-radius:8px; overflow:hidden; border:2px solid transparent; }
  .card.ok { border-color:#3a4a3a; }
  .card.pending { border-color:#5a5a5a; }
  .card.fail { border-color:#8a2a2a; }
  .card img { width:100%; display:block; }
  .noimg { width:100%; aspect-ratio:9/16; display:flex; align-items:center; justify-content:center; color:#666; font-size:.85rem; background:#252830; }
  .cap { padding:10px 12px; font-size:.85rem; color:#c9c4b6; }
  .cap b { color:#e8e4d8; }
  .win { color:#8a95a8; font-size:.78rem; display:block; margin:3px 0 6px; }
  .status { display:inline-block; font-size:.72rem; padding:2px 7px; border-radius:4px; margin-top:6px; }
  .status.ok { background:#2a3a2a; color:#9fd39f; }
  .status.pending { background:#333; color:#aaa; }
  .status.fail { background:#3a2020; color:#e88; }
  .v { background:#1e2129; border-left:4px solid #e9c877; padding:12px 16px; border-radius:8px; margin-bottom:20px; }
"""


def build():
    ok_n = 0
    pending_n = 0
    fail_n = 0
    cards = []
    for num, name, beat, window, cap, pre_approved in ROWS:
        png = s2.OUT / f"{name}.png"
        exists = png.exists() and png.stat().st_size > 1000
        if exists:
            status_cls = "ok"
            status_txt = "APPROVED (pre-batch test gate)" if pre_approved else "RENDERED -- awaiting eye-QC"
            ok_n += 1
            img_html = f'<img src="stills/{name}.png" loading="lazy">'
        else:
            status_cls = "pending"
            status_txt = "PENDING -- not yet rendered"
            pending_n += 1
            img_html = '<div class="noimg">not rendered yet</div>'
        cards.append(f"""  <div class="card {status_cls}">{img_html}
    <div class="cap"><b>#{num:02d} {name}</b><span class="win">Beat {beat} · {window}</span>
    {cap}
    <div class="status {status_cls}">{status_txt}</div></div></div>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bronze Serpent LONG — living-sketchbook stills review</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>BRONZE SERPENT LONG — 68 spreads, living-sketchbook stills</h1>
<div class="sub">Full-length (~9:50) pilot, Numbers 21 / John 3:14 typology, source: the LOCKED
long-form "Types &amp; Shadows" narration (longform/EW04_Bronze_Serpent/v1/narration.md, 590.38s,
real ffprobe-verified turn timing). Plan: <code>_PLAN.md</code>. {ok_n} rendered / {pending_n} pending
/ {fail_n} failed of 68 total.</div>

<div class="v">
<b>Cast + doctrine carried forward from the short (poc_living_sketchbook/bronze_serpent/).</b>
Moses = cast/MOSES.md + moses_ref.png (elder, ~120yo, Deut 34:7) chained with the approved
s23_lord_presence.png as a second in-episode identity-lock reference on every Moses spread. Jesus =
cast/JESUS.md + jesus_ref.png chained with the short's approved s10_golgotha.png as a second
reference on every Jesus spread. Crowd faces capped at ≤3 sharp/detailed per frame (PEOPLE), with
exact-headcount variants for named multi-figure vignettes (spreads 17, 33, 60, 63). Bronze serpent
stays dull bronze/copper, gold reserved for Christ/the LORD only, golden calf renders LARGE and
tarnished (never gilded). Hezekiah (spread 55) is NEW — a young king in his mid-to-late twenties per
2 Kings 18:2, not an elderly "wise king." Insert pages 43 and 67 reuse the short's Scholar's-Margin
and Gilded Proclamation visual devices/registers with new content, no baked lettering (verse text is
a Scribed Ink overlay applied at assembly, not part of the AI render).
</div>

<div class="grid">
{chr(10).join(cards)}
</div>
</div>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[review] {ok_n} rendered, {pending_n} pending, {fail_n} failed -> {OUT_HTML}")


if __name__ == "__main__":
    build()
