#!/usr/bin/env python
"""Register Thirty Pieces (Zech 11) NEW assets in the global index: 9 stills + 6 Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="thirty_pieces_zech11", piece_title="Thirty Pieces of Silver (Zechariah 11:12-13)",
              verse="Zechariah 11:12-13", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "thirty_coins_scatter": ("silver coins scattering across the torchlit temple floor", [], ["coins", "temple floor", "torch"], "temple court, night", "neutral", "the thirty pieces cast down (Matt 27:5)"),
 "coin_on_scroll": ("a silver coin resting on an ancient scroll by lamplight", [], ["coin", "scroll", "oil lamp"], "scribe's table", "neutral", "the price written five centuries early (Zech 11:12)"),
 "weighing_scales_silver": ("hands weighing silver pieces on a hanging balance", [], ["balance scale", "silver", "torch"], "stone chamber", "neutral", "so they weighed for my price (Zech 11:12)"),
 "potter_at_wheel": ("a potter's clay hands shaping a vessel on a stone wheel", ["potter"], ["wheel", "clay vessel"], "workshop", "neutral", "cast it unto the potter (Zech 11:13)"),
 "judas_bag_priests": ("Judas head bowed clutching the money bag, priests watching", ["Judas", "priests"], ["money bag", "coins", "torches"], "temple chamber", "specific", "the covenant for thirty pieces (Matt 26:15)"),
 "judas_casting_coins": ("Judas hurling the silver across the temple hall, priests recoiling", ["Judas", "priests"], ["coins mid-air", "temple columns"], "temple hall", "specific", "he cast down the pieces of silver (Matt 27:5)"),
 "zechariah_casting": ("the prophet flinging silver coins toward a potter's stall at night", ["Zechariah"], ["coins mid-air", "potter's stall", "torches"], "temple court, night", "specific", "I took the thirty pieces and cast them (Zech 11:13)"),
 "potters_field": ("a bleak clay field strewn with broken pottery under a grey sky", [], ["pottery shards", "clay field"], "potter's field", "neutral", "the field of blood (Matt 27:7-8)"),
 "silver_and_blood": ("worn silver coins on pale stone with a dark red stream between them", [], ["coins", "blood stream", "stone"], "temple floor", "neutral", "the price of blood (Matt 27:6)"),
}
KLING = ["thirty_coins_scatter", "weighing_scales_silver", "judas_bag_priests",
         "judas_casting_coins", "potter_at_wheel", "silver_and_blood"]

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"tp_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, torch ambers and temple stone",
                 "mood": "prophetic ledger, betrayal, ransom", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "zech11", "thirty-pieces"],
                 "used_in": ["thirty_pieces_zech11 short"]})
for slug in KLING:
    s = STILLS[slug]
    ax.register({**COMMON, "id": f"tp_{slug}_clip", "type": "clip", "media": "video",
                 "path": V / "clips" / f"{slug}.mp4", "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "zech11", "kling"],
                 "used_in": ["thirty_pieces_zech11 short"]})
print(f"registered {len(STILLS)} stills + {len(KLING)} clips")
