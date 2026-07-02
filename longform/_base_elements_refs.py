#!/usr/bin/env python
"""Base-elements REFERENCE builder (Step 2 of the base-elements library).

Reads the authored card specs in ref_library/cards/*.json (one canonical
description per indexed element) and renders ONE locked reference image per
element via HF seedream_v4_5 (inked style, 9:16), writes a per-element JSON
sidecar, and rebuilds ref_library/catalogue.json — the permanent reusable base
layer that every future short/long render references (pass `anchor` as --image).

Generalises longform/_style_poc/ref_cards/build_ref_cards.py (which had the
cards hard-coded) into a data-driven driver over the whole corpus index.

Idempotent (existing PNG = skip), rate-limit-aware (3-attempt retry).
seedream_v4_5 = ~1 credit / image.

Run:
  # cost plan only, render nothing:
  .venv\\Scripts\\python.exe longform\\_base_elements_refs.py --plan
  # render the reusable ATOMS (characters + objects + places), skip motifs:
  .venv\\Scripts\\python.exe longform\\_base_elements_refs.py --kinds character,object,place
  # render everything incl. motif plates:
  .venv\\Scripts\\python.exe longform\\_base_elements_refs.py --kinds character,object,place,motif
  # only the high-reuse ones (used in >=N pieces):
  .venv\\Scripts\\python.exe longform\\_base_elements_refs.py --min-count 2
"""
from __future__ import annotations
import argparse, glob, json, os, re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "ref_library"
CARDS_DIR = LIB / "cards"
ASPECT = "9:16"

# ---- inked style spine (matches the locked Jesus look + the POC builder) -----
STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style: bold clean "
         "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D artwork, "
         "dramatic ink shadows. NOT a photograph, NOT photorealistic, NOT a glossy 3D render, NOT "
         "soft airbrushed anime — strong visible ink lines. Reverent and holy atmosphere, ancient "
         "Near-Eastern period-accurate, mature teen-and-up tone. ABSOLUTELY NO text, letters, words, "
         "numbers, captions, labels, titles, inscriptions, speech bubbles, scrolls of legible writing, "
         "watermark or signature ANYWHERE in the image — any surface that could bear writing (scrolls, "
         "tablets, coins, signs, pediments, banners) must be left blank or show only vague illegible "
         "non-letter texture.")
ONE = (" ONE single uninterrupted full-bleed illustration filling the entire frame — absolutely NO "
       "split screen, NO side panel, NO inset, NO grid, NO border or divider of any kind.")
CHARSHEET = (" A clean CHARACTER REFERENCE SHEET of this ONE same person, shown twice on a single "
             "plain neutral dark backdrop: a large head-and-shoulders CLOSE-UP of the face at the "
             "top, and directly below the FULL STANDING FIGURE head to feet, correct adult human "
             "proportions (head about one-seventh of standing height), facing forward, neutral "
             "relaxed stance. Identical identity, face and clothing consistent in both views. No "
             "other people, no scenery, no props beyond what the figure wears or holds. The two views "
             "sit on ONE single continuous unbroken backdrop with NO dividing line, NO vertical seam, "
             "NO border, NO panel split and NO frame between them. Eyes are normal natural human eyes "
             "— NOT glowing, NOT luminous, NOT red, NOT yellow, NOT supernatural. Natural human hair "
             "and skin colours only, no unnatural green/blue tints. Do NOT write the character's name, "
             "NO caption, NO label, NO text of any kind anywhere.")
PLATE = (" Establishing background plate, atmospheric, NO people and NO main subject — just the "
         "place and its light, as a reusable empty stage.")
OBJECT = (" Object reference: the subject isolated upright and centred, complete and clear, on a "
          "plain neutral background, no people, no scenery.")
MOTIF = (" A single clear symbolic composition of this motif, centred, reverent, on an atmospheric "
         "period background, readable at a glance as a reusable visual.")
GROUP = (" A GROUP / ensemble reference: SEVERAL of these figures together in ONE scene on a plain "
         "neutral or simple period backdrop, a consistent shared period look across all of them, "
         "full bodies visible, natural grouping. This is a crowd/group, NOT a single individual.")
GLORY = (" Depict the divine presence reverently as ONLY a HIGH radiant glory in the upper sky: a "
         "small brilliant warm-golden source of holy light set HIGH near the top of the frame, soft "
         "rays fanning gently outward in ALL directions across a wide pale dawn sky with thin wispy "
         "clouds drifting horizontally, a very low faraway wilderness horizon far below. The light "
         "source is small and high, NOT a mass rising from the ground. CRITICAL: NO central vertical "
         "column, NO rising shaft, NO tall billowing single cloud, NO dark trunk or stalk, NO "
         "mushroom or atom-bomb shape, NO explosion. The frame is EMPTY OF ANY BEING: NO person, NO "
         "figure, NO face, NO body, NO throne, NO halo, NO human or god form of any kind — only a "
         "gentle high radiance and open sky.")

BLOCKS = {"charsheet": CHARSHEET, "object": OBJECT, "plate": PLATE, "motif": MOTIF,
          "group": GROUP, "glory": GLORY}
SUBDIR = {"character": "characters", "object": "objects", "place": "places", "motif": "motifs"}


def load_cards():
    cards, seen = [], {}
    for fp in sorted(glob.glob(str(CARDS_DIR / "*.json"))):
        for c in json.load(open(fp, encoding="utf-8")):
            name = c["name"]
            if name in seen:        # de-dupe if a name lands in two card files
                continue
            seen[name] = True
            cards.append(c)
    return cards


_UPLOAD_CACHE = {}

def hf_upload(path):
    """Upload a local image once, return the seedream input_images object {id,type,url}."""
    path = str(path)
    if path in _UPLOAD_CACHE:
        return _UPLOAD_CACHE[path]
    r = subprocess.run([HF, "upload", "create", path, "--json"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=180)
    obj = json.loads((r.stdout or "").strip())
    obj = {"id": obj["id"], "type": obj.get("type", "image"), "url": obj["url"]}
    _UPLOAD_CACHE[path] = obj
    return obj


def render(prompt, dest, refs=None, quality="high"):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}", flush=True); return "skip"
    args = [HF, "generate", "create", "seedream_v4_5", "--prompt", prompt,
            "--aspect_ratio", ASPECT, "--quality", quality, "--wait"]
    if refs:
        args += ["--input_images", json.dumps(refs)]
    for attempt in (1, 2, 3):
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "awakeden/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {dest.name}", flush=True); return "ok"
        low = blob.lower()
        transient = ("concurrent_jobs_limit" in low or "rate_limit" in low or "timeout" in low)
        tag = "retry" if (attempt < 3 and transient) else "FAIL"
        print(f"[{tag}] {dest.name} (rc={r.returncode})\n    {blob[-220:].strip()}", flush=True)
        if not transient:
            return "fail"
    return "fail"


def build_prompt(card):
    block = BLOCKS.get(card.get("block", "object"), OBJECT)
    body = card["canonical"] + "." + block
    # character sheets are intentionally a two-view grid, so they skip the no-grid ONE clause
    if card.get("block") != "charsheet":
        body += ONE
    return body + STYLE


# seedream_v4_5 has NO negative_prompt channel: a concrete object named in the
# per-card canonical (even to forbid it) tends to get DRAWN. These regexes flag
# the materials that actually leaked as artifacts (memory: seedream-no-negative-
# channel). Warn-only, never blocks — describe the desired END-STATE instead.
POISON = [
    (re.compile(r"\b(glow(?:ing)?|luminous)\b|\b(?:light|radiance)\s+on\s+(?:the|his|her)\b", re.I),
     "glow/light-on-body -> renders as neon limbs; use 'plain even daylight'"),
    (re.compile(r"\b(welts?|stripes?|lash(?:es)?|abrasions?|gash(?:es)?)\b", re.I),
     "welt/stripe/lash line -> draws as X-stitches; use bruise-only ('smooth unbroken skin, deep red/purple blotches')"),
    (re.compile(r"\b(blind|clouded eyes|closed eyes|eyes (?:gently )?closed)\b", re.I),
     "blind/eye wording -> draws sunglasses; drop it, show infirmity via posture/crutches"),
    (re.compile(r"\b(nails?|spikes?|studs?)\b", re.I),
     "metal nails -> render as studs; for the risen Christ use 'round dark healed scar, closed flat and level'"),
    (re.compile(r"\byoung (?:son|boy|child)\b|\b(?:bound|naked|nude) (?:child|boy|son)\b", re.I),
     "young child near altar/knife -> trips nsfw filter; render the doctrinal icon instead (e.g. the substitute ram)"),
]
NEG_RE = re.compile(r"\b(no|not|without|never)\b", re.I)


def lint_canonical(name, text):
    """Print pre-flight warnings for known seedream poison tokens in a card's canonical."""
    warns = [why for rx, why in POISON if rx.search(text)]
    negs = len(NEG_RE.findall(text))
    for w in warns:
        print(f"  [WARN] {name}: {w}", flush=True)
    if negs:
        print(f"  [note] {name}: {negs} negation word(s) -- seedream has NO negative channel, "
              f"describe the end-state, don't name what to omit", flush=True)
    return bool(warns)


def write_sidecar(card):
    kind = card["kind"]
    sub = SUBDIR[kind]
    (LIB / sub).mkdir(parents=True, exist_ok=True)
    (LIB / sub / f"{card['name']}.json").write_text(json.dumps({
        "name": card["name"], "kind": kind, "canonical": card["canonical"],
        "tags": card.get("tags", []), "style": "inked",
        "anchor": f"{sub}/{card['name']}.png",
        "first_used": card.get("first_used", ""), "count": card.get("count", 1),
        "notes": "Pass `anchor` as --image to lock identity/world across scenes.",
    }, indent=2), encoding="utf-8")


def rebuild_catalogue():
    cat = []
    for sub in SUBDIR.values():
        for jp in sorted((LIB / sub).glob("*.json")):
            cat.append(json.loads(jp.read_text(encoding="utf-8")))
    (LIB / "catalogue.json").write_text(json.dumps(cat, indent=2), encoding="utf-8")
    return len(cat)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kinds", default="character,object,place,motif",
                    help="comma list of kinds to render")
    ap.add_argument("--min-count", type=int, default=1, help="only elements used in >= N pieces")
    ap.add_argument("--names", default="", help="comma list of exact element names to render (test-gate)")
    ap.add_argument("--limit", type=int, default=0, help="cap number of renders (0 = no cap)")
    ap.add_argument("--plan", action="store_true", help="cost plan only, render nothing")
    args = ap.parse_args()

    kinds = set(k.strip() for k in args.kinds.split(","))
    only = set(n.strip() for n in args.names.split(",") if n.strip())
    cards = [c for c in load_cards()
             if ((c["name"] in only) if only else
                 (c["kind"] in kinds and c.get("count", 1) >= args.min_count))]

    todo, have = [], 0
    for c in cards:
        dest = LIB / SUBDIR[c["kind"]] / f"{c['name']}.png"
        if dest.exists() and dest.stat().st_size > 0:
            have += 1
        else:
            todo.append(c)
    if args.limit:
        todo = todo[:args.limit]

    print(f"cards matched: {len(cards)}  already-rendered: {have}  to-render: {len(todo)}")
    print(f"est. seedream cost: ~{len(todo)} credits (1 cr/image)")

    # pre-flight lint: surface poison tokens BEFORE spending any credit
    flagged = sum(lint_canonical(c["name"], c["canonical"]) for c in todo)
    if flagged:
        print(f"  ({flagged} card(s) carry seedream poison tokens — review above before render)", flush=True)

    if args.plan:
        from collections import Counter
        kc = Counter(c["kind"] for c in todo)
        print("to-render by kind:", dict(kc))
        return

    results = {}
    for c in todo:
        dest = LIB / SUBDIR[c["kind"]] / f"{c['name']}.png"
        refs = None
        r = c.get("ref")
        if r:
            abs_ref = r if os.path.isabs(r) else str((LIB / r).resolve())
            refs = [hf_upload(abs_ref)]
        res = render(build_prompt(c), dest, refs=refs)
        results[c["name"]] = res
        if res in ("ok", "skip"):
            write_sidecar(c)
    # ensure sidecars exist for already-rendered too
    for c in cards:
        dest = LIB / SUBDIR[c["kind"]] / f"{c['name']}.png"
        sc = LIB / SUBDIR[c["kind"]] / f"{c['name']}.json"
        if dest.exists() and not sc.exists():
            write_sidecar(c)

    n = rebuild_catalogue()
    ok = sum(1 for v in results.values() if v == "ok")
    fail = sum(1 for v in results.values() if v == "fail")
    print(f"\nDONE — rendered {ok}, failed {fail}; catalogue now {n} cards")


if __name__ == "__main__":
    main()
