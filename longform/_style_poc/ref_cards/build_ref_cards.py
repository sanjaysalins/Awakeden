"""Build the CENTRAL inked reference-card catalogue (ref_library/).

Each card is a clean INKED anchor image (the locked identity of a character /
object / place) + a JSON sidecar holding its canonical description + tags. The
anchor is meant to be passed as --image on every future scene so the same face /
object / world is inherited, not re-invented — across ALL long AND short form.

Generate once, reuse forever (sibling to image_library / clip_library /
sound_library / music_library). seedream_v4_5, inked style, 9:16. Idempotent,
rate-limit-aware, 3-attempt retry. POC tooling; the catalogue itself is permanent."""
import re, json, shutil, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
ROOT = Path(__file__).resolve().parents[3]          # repo root
LIB = ROOT / "ref_library"
POC = Path(__file__).resolve().parents[1]            # longform/_style_poc
JESUS_GRID = POC / "jesus" / "JESUS__GRID.png"
ASPECT = "9:16"

# ---- the inked style spine (matches the locked Jesus look) -------------------
STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style: bold clean "
         "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D artwork, "
         "dramatic ink shadows. NOT a photograph, NOT photorealistic, NOT a glossy 3D render, NOT "
         "soft airbrushed anime — strong visible ink lines. Reverent and holy atmosphere, ancient "
         "Near-Eastern period-accurate, mature teen-and-up tone. No text, no lettering, no panels, "
         "no speech bubbles, no watermark, no signature.")
ONE = (" ONE single uninterrupted full-bleed illustration filling the entire frame — absolutely NO "
       "split screen, NO side panel, NO inset, NO grid, NO border or divider of any kind.")
CHARSHEET = (" A clean CHARACTER REFERENCE SHEET of this ONE same person, shown twice on a single "
             "plain neutral dark backdrop: a large head-and-shoulders CLOSE-UP of the face at the "
             "top (clear features, calm expression), and directly below the FULL STANDING FIGURE "
             "head to feet, correct adult human proportions (head about one-seventh of standing "
             "height), facing forward, neutral relaxed stance. Identical identity, face and "
             "clothing consistent in both views. No other people, no scenery, no props beyond what "
             "the figure wears or holds.")
PLATE = (" Establishing background plate, atmospheric, NO people and NO main subject — just the "
         "place and its light, as a reusable empty stage.")
OBJECT = (" Object reference: the subject isolated upright and centred, complete and clear, on a "
          "plain neutral background, no people, no scenery.")

# name -> (kind, canonical subject description, [tags], extra-prompt block)
CARDS = {
 "MOSES": ("character",
    "Moses, an aged Hebrew prophet and shepherd-leader of about eighty, weathered sun-darkened "
    "olive skin, a deeply lined noble face, long flowing grey hair and a full thick grey beard, "
    "deep-set wise weary eyes, wrapped in a rough heavy desert mantle over a simple robe, holding "
    "a tall plain wooden shepherd's staff",
    ["moses", "prophet", "wilderness", "law", "old-testament", "witness", "elder"], CHARSHEET),

 "NICODEMUS": ("character",
    "Nicodemus, an older Jewish Pharisee and teacher of about sixty, a thoughtful dignified face, "
    "greying dark beard and hair, a lined brow and deep searching eyes, wearing the fine layered "
    "robes and prayer-shawl of a respected rabbi",
    ["nicodemus", "pharisee", "rabbi", "seeker", "new-testament", "elder"], CHARSHEET),

 "BRONZE_SERPENT_STANDARD": ("object",
    "a tall straight rough-hewn bare wooden pole planted upright, with a single cast bronze serpent "
    "MOUNTED ON TOP at the very summit — its body raised and its head lifted high like a banner. The "
    "long lower shaft is completely BARE plain wood; the serpent does NOT spiral, wind or coil down "
    "the pole. A serpent SET UPON a pole (Num 21:8), lifted up — NOT a snake-wrapped staff, NOT the "
    "Rod of Asclepius, NOT a medical caduceus, NOT an occult charm",
    ["bronze-serpent", "standard", "pole", "numbers-21", "wilderness", "type-of-christ"], OBJECT),

 "WILDERNESS_CAMP": ("place",
    "an ancient Israelite wilderness encampment at dusk in the rocky Sinai desert: scattered rough "
    "goat-hair tents, low firelight, bare rocky sand, distant barren hills under a heavy dim sky",
    ["wilderness", "camp", "sinai", "desert", "encampment", "exodus", "dusk"], PLATE),

 "JERUSALEM_NIGHT_INTERIOR": ("place",
    "the interior of an ancient Jerusalem stone house at night: plain dressed-stone walls, a low "
    "stone ledge, a single small clay oil lamp casting warm light into deep darkness, simple "
    "period furnishings",
    ["jerusalem", "interior", "night", "stone-house", "oil-lamp", "intimate"], PLATE),
}

SUBDIR = {"character": "characters", "object": "objects", "place": "places"}


def render(prompt, dest):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}", flush=True); return "skip"
    args = [HF, "generate", "create", "seedream_v4_5", "--prompt", prompt,
            "--aspect_ratio", ASPECT, "--wait"]
    for attempt in (1, 2, 3):
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {dest.name}", flush=True); return "ok"
        low = blob.lower()
        transient = ("concurrent_jobs_limit" in low or "rate_limit" in low or "timeout" in low)
        tag = "retry" if (attempt < 3 and transient) else "FAIL"
        print(f"[{tag}] {dest.name} (rc={r.returncode})\n    {blob[-260:].strip()}", flush=True)
        if not transient:
            return "fail"
    return "fail"


def write_sidecar(name, kind, canonical, tags, anchor_rel, first_used="EW04_Bronze_Serpent"):
    (LIB / SUBDIR[kind] / f"{name}.json").write_text(json.dumps({
        "name": name, "kind": kind, "canonical": canonical, "tags": tags,
        "style": "inked", "anchor": anchor_rel, "first_used": first_used,
        "notes": "Pass `anchor` as --image to lock identity/world across scenes.",
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    for d in SUBDIR.values():
        (LIB / d).mkdir(parents=True, exist_ok=True)
    results = {}

    # 1) register the already-built Jesus grid into the central bank
    if JESUS_GRID.exists():
        dest = LIB / "characters" / "JESUS.png"
        if not dest.exists():
            shutil.copy2(JESUS_GRID, dest)
        write_sidecar("JESUS",
            "character",
            "Jesus of Nazareth, a Jewish man of about thirty, warm olive-brown skin, a calm noble "
            "face, long dark brown hair parted in the middle to the shoulders, a full dark brown "
            "beard, deep compassionate brown eyes; face + full standing body anchor grid (head "
            "about one-seventh of standing height)",
            ["jesus", "christ", "new-testament", "hero", "messiah"],
            "characters/JESUS.png")
        results["JESUS"] = "registered"
        print("[reg ] JESUS (grid registered)", flush=True)

    # 2) render the new cards
    for name, (kind, canonical, tags, block) in CARDS.items():
        dest = LIB / SUBDIR[kind] / f"{name}.png"
        # characters render a two-view sheet (face + body), so they skip the no-grid ONE clause
        prompt = canonical + "." + block + ("" if kind == "character" else ONE) + STYLE
        results[name] = render(prompt, dest)
        if results[name] in ("ok", "skip"):
            write_sidecar(name, kind, canonical, tags, f"{SUBDIR[kind]}/{name}.png")

    # 3) master manifest
    cat = []
    for sub in SUBDIR.values():
        for jp in sorted((LIB / sub).glob("*.json")):
            cat.append(json.loads(jp.read_text(encoding="utf-8")))
    (LIB / "catalogue.json").write_text(json.dumps(cat, indent=2), encoding="utf-8")
    print(f"\nDONE — {len(cat)} cards in {LIB}\n{json.dumps(results, indent=2)}", flush=True)
