#!/usr/bin/env python
"""Register Woman Behold Thy Son (John 19:26) NEW assets: 6 stills + their Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="woman_behold_john1926", piece_title="Woman Behold Thy Son (John 19:26)",
              verse="John 19:25-27 + Luke 2:35", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "simeon_baby_temple": ("aged Simeon lifting the swaddled infant in temple light", ["Simeon", "infant Jesus", "Mary"], ["temple columns", "light shaft"], "temple", "specific", "Simeon's blessing (Luke 2:28,34)"),
 "mary_infant_shadow": ("young Mary clutching the infant, a cold sword-line shadow across her robe", ["Mary", "infant Jesus"], ["sword shadow", "temple stone"], "temple", "specific", "a sword shall pierce thy own soul (Luke 2:35)"),
 "mary_at_cross": ("veiled Mary looking up from the foot of the cross", ["Mary", "Christ crucified"], ["cross", "storm light"], "Golgotha", "specific", "there stood by the cross his mother (John 19:25)"),
 "jesus_looks_down": ("thorn-crowned Christ looking down in compassion from the cross", ["Christ"], ["crown of thorns", "storm sky"], "Golgotha", "hero", "when Jesus saw his mother (John 19:26)"),
 "mary_and_john": ("the beloved disciple wrapping his arm around grieving Mary at the cross foot", ["Mary", "John"], ["cross base", "storm light"], "Golgotha", "specific", "the disciple standing by, whom he loved (John 19:26)"),
 "john_leads_home": ("John gently leading Mary along a dusk road toward a walled town gate", ["Mary", "John"], ["town gate", "dusk road", "bare hill behind"], "road from Golgotha", "specific", "took her unto his own home (John 19:27)"),
}

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"wb_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, temple gold to storm grey to dusk warm",
                 "mood": "a mother's wound, the Son who sees it", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "john1926", "mary"],
                 "used_in": ["woman_behold_john1926 short"]})
n_clips = 0
for slug, s in STILLS.items():
    clip = V / "clips" / f"{slug}.mp4"
    if not clip.exists():
        continue
    n_clips += 1
    ax.register({**COMMON, "id": f"wb_{slug}_clip", "type": "clip", "media": "video",
                 "path": clip, "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "john1926", "kling"],
                 "used_in": ["woman_behold_john1926 short"]})
print(f"registered {len(STILLS)} stills + {n_clips} clips")
