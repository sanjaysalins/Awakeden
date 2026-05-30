"""Build reusable Baroque background PLATES via HF nano_banana_2.

Thread-neutral settings only — NO named figures / NO Jesus / NO central portrait
subject (crowd = distant anonymous backs). House style = engine VISUAL_STYLE_BASE/TAIL.

Usage:
    python _build_plates.py <slug>           # build one plate by slug
    python _build_plates.py ALL              # build every remaining plate
Writes: _library/plates/<slug>/<slug>.png + <slug>.meta.json
"""
import json, subprocess, sys, urllib.request
from pathlib import Path

HF = r"C:\Users\sanjay\bin\hf.exe"
LIB = Path(__file__).resolve().parent / "_library" / "plates"

STYLE_BASE = ("Masterpiece Flemish Baroque oil painting in the style of Peter Paul Rubens, "
    "Caravaggio dramatic chiaroscuro, Rembrandt golden lighting; richly textured "
    "visible brushwork and impasto, deep luminous shadow, a single warm light "
    "source, reverent devotional sacred-art atmosphere")
STYLE_TAIL = ("vertical 9:16 composition, cinematic depth, museum-quality fine-art oil "
    "painting, rich earthen palette with gold and crimson accents, no text, no "
    "watermark, no modern objects, no lettering")
# Every plate is a SETTING — keep it empty of identifiable people.
NEUTRAL = ("an empty landscape setting with NO central figure, NO portrait subject, "
    "NO identifiable person, NO Jesus")

# slug -> (motif, subject description)
PLATES = {
    "storm-sea":       ("storm-sea", "a violent night storm over the Sea of Galilee, towering black waves, churning water, heavy storm clouds and lightning, a small empty wooden fishing boat tossed far in the distance"),
    "calm-shore":      ("calm-sea", "the calm Sea of Galilee at dawn, still glassy water, a quiet pebbled lakeshore, distant soft hills, gentle golden morning light"),
    "charcoal-fire":   ("fire", "a low charcoal fire of glowing red coals on a sandy lakeshore at dawn, thin wisps of smoke rising, scattered embers, warm firelight on the sand"),
    "wilderness":      ("desert", "a vast rocky Judean wilderness, barren desert hills and dry scrub, cracked earth, harsh light, a distant empty horizon"),
    "jerusalem-street":("street", "a narrow ancient Jerusalem stone street, worn stone steps and archways, clay and limestone walls, deep shadow and a shaft of warm light"),
    "synagogue":       ("interior", "the interior of an ancient stone synagogue, rows of weathered columns, hanging oil lamps, a scroll niche, dust in shafts of light"),
    "crowd":           ("crowd", "a great crowd of robed ancient Judean people gathered on a hillside seen from behind, anonymous distant backs of figures, dusty earth, hazy light"),
    "dawn-sky":        ("sky", "a dramatic dawn sky over distant dark hills, golden light breaking through heavy storm clouds, rays of light, an empty sweeping landscape"),
    "stone-well":      ("well", "an ancient stone well under harsh midday heat, a worn circular stone rim, a clay water jar resting on the edge, dusty cracked ground"),
    "olive-grove":     ("grove", "an ancient olive grove at dusk, gnarled twisted olive trunks, silver-grey leaves, long deep shadows, a solemn Gethsemane mood"),
    "empty-tomb":      ("tomb", "the exterior of an empty rock-hewn tomb cut into a hillside, a large round stone rolled aside from a dark doorway, soft dawn light at the entrance"),
    "lamplit-room":    ("interior", "a humble ancient stone room at night, rough plaster walls, a single small oil lamp casting a warm pool of light, deep surrounding shadow"),
}

def build(slug):
    motif, subject = PLATES[slug]
    out_dir = LIB / slug; out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{slug}.png"
    if png.exists():
        print(f"[skip] {slug} already built"); return True
    prompt = f"{STYLE_BASE}, {subject}; {NEUTRAL}, {STYLE_TAIL}"
    print(f"[{slug}] generating...")
    r = subprocess.run([HF, "generate", "create", "nano_banana_2",
                        "--prompt", prompt, "--aspect_ratio", "9:16",
                        "--wait", "--wait-timeout", "10m", "--json"],
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    url = None
    for line in out.splitlines():
        line = line.strip()
        if '"result_url"' in line:
            url = line.split('"result_url"', 1)[1].split('"')[1]; break
    if not url:
        # try parse whole stdout as json
        try:
            d = json.loads(r.stdout)
            if isinstance(d, list): d = d[0]
            url = d.get("result_url") or (d.get("results") or [{}])[0].get("url")
        except Exception:
            pass
    if not url:
        print(f"[{slug}] NO URL. raw tail:\n{out[-500:]}"); return False
    urllib.request.urlretrieve(url, png)
    (out_dir / f"{slug}.meta.json").write_text(json.dumps(
        {"slug": slug, "motif": motif, "style": "baroque-rubens",
         "reusable": True, "subject": subject, "source_url": url,
         "episodes_used_in": []}, indent=2), encoding="utf-8")
    print(f"[{slug}] OK -> {png}  ({png.stat().st_size} bytes)")
    return True

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    slugs = list(PLATES) if arg == "ALL" else [arg]
    ok = sum(build(s) for s in slugs)
    print(f"\nDONE {ok}/{len(slugs)}")
