#!/usr/bin/env python
"""Pre-render VALIDATION GATE for still PROMPTS — catches lazy / repetitive / non-biblical prompting
BEFORE we spend a credit. Built because a bespoke terse renderer bypassed the repo's quality machinery
and produced tired, interchangeable, non-grounded stills (user 2026-07-02: "very lazy prompting").

REUSES (does not duplicate):
  - render_lint.lint(prompt, stage="still")  -> per-prompt rule findings (poison tokens, biblical
       traps incl. the new crucifixion-feet rule, arm/pose guidance, anachronisms)
  - corpus_diversity.content_words / jaccard  -> the SET-level near-duplicate detection (the real gap:
       no existing tool compares a SET of prompt texts). Cross-checks NEW vs NEW and NEW vs EXISTING.

ADDS the checks that catch the rot:
  1. GROUNDING   every still must cite a Bible verse + carry a distinct shot_type + a pinned pose
                 (a terse untagged template prompt = lazy -> FAIL)
  2. DEDUP       subject near-duplicate (jaccard on subject words, style boilerplate stripped) across
                 the whole set incl. existing stills -> FAIL on look-alikes
  3. SHOT_VAR    no shot_type over-used -> forces visual variety
  4. POSE_PINNED any Christ/figure prompt must state an explicit arm/hand position (kills the recurring
                 prayer-hand-from-chest default)

$0, deterministic, no API. Reads still_specs.json (grounded) + render_new16 (terse) + render_fresh
(existing, for cross-dedup).

  ...python longform/02_Psalm_22_Song_From_The_Cross/still_validate.py
"""
import importlib.util, itertools, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from render_lint.lint import lint                       # per-prompt rules
from corpus_diversity import content_words, jaccard     # set dedup helpers


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


rf = _load("render_fresh_16x9")     # existing PROMPTS + CH
rn = _load("render_new16_16x9")     # new PROMPTS
SPECS = json.loads((HERE / "still_specs.json").read_text(encoding="utf-8"))["specs"]

DEDUP_FAIL = 0.55        # subject-word jaccard at/above -> near-duplicate
DEDUP_WARN = 0.42
SHOT_MAX = 4             # a shot_type used more than this across the film -> monotony
# style boilerplate to strip so dedup reflects the SUBJECT, not the shared house style
STYLE_STOP = set("inked biblical graphic novel wide cinematic composition bold black ink outlines "
                 "cel flat color colour dramatic cross hatched hatching shadow reverent 1st century "
                 "warm light hard soft golden radiant scene view close macro tight extreme frame the "
                 "a an of in on and with his her their toward into out only no not a man early thirties "
                 "near eastern face beard hair dark brown olive skin deep eyes high cheekbones".split())
FIGURE = ("christ", "crucified", "risen", "jesus", "david", "scribe", "scholar", "mocker", "soldier")
POSE_WORDS = ("arm", "arms", "hand", "hands", "palm", "palms", "reaching", "raised", "nailed", "hanging",
              "spread", "lifted", "open", "bowed", "kneel", "seated", "standing", "clutch", "cradl")


def subj(text):
    return set(content_words(text)) - STYLE_STOP


def expand(p):
    return p.replace("{CH}", rf.CH).replace("{INK}", getattr(rf, "INK", ""))


def build_records():
    recs, done = [], set()
    for slug, s in SPECS.items():                         # grounded redesigns (new OR existing being re-rendered)
        recs.append(dict(slug=slug, prompt=expand(s["prompt"]), shot=s["shot"], verse=s.get("verse"),
                         arms=s.get("arms"), grounded=True)); done.add(slug)
    for slug, (terse, ref) in rn.PROMPTS.items():         # new stills not yet grounded -> lazy
        if slug in done:
            continue
        recs.append(dict(slug=slug, prompt=expand(terse), shot=None, verse=None, arms=None, grounded=False))
    return recs


def validate():
    recs = build_records()
    # cross-dedup pool = existing stills we are NOT re-rendering (don't flag a redesign vs its own old prompt)
    existing = {slug: expand(p) for slug, (p, ref) in rf.PROMPTS.items() if slug not in SPECS}
    fails, warns = [], []

    # per-prompt lint + grounding + pose
    for r in recs:
        for f in lint(r["prompt"], stage="still"):
            (fails if f["severity"] == "block" else warns).append(
                f"{r['slug']:24} [lint:{f['axis']}] {f['message'][:90]}")
        if not r["grounded"]:
            fails.append(f"{r['slug']:24} [grounding] LAZY: terse template prompt — no cited verse / "
                         f"distinct shot / pinned pose. Move it to still_specs.json and ground it.")
        else:
            low = r["prompt"].lower()
            if any(fig in low for fig in FIGURE) and not any(w in low for w in POSE_WORDS) and not r["arms"]:
                fails.append(f"{r['slug']:24} [pose] a figure with no explicit arm/hand position "
                             f"(prayer-hand-from-chest risk) — pin the pose.")

    # SET dedup: new vs new
    for a, b in itertools.combinations(recs, 2):
        j = jaccard(subj(a["prompt"]), subj(b["prompt"]))
        if j >= DEDUP_FAIL:
            fails.append(f"{a['slug']} ~= {b['slug']}  [dedup {j:.2f}] near-identical subject — "
                         f"differentiate shot/moment/detail.")
        elif j >= DEDUP_WARN:
            warns.append(f"{a['slug']} ~ {b['slug']}  [dedup {j:.2f}] similar subject.")
    # SET dedup: new vs existing (catches new stills that duplicate ones we already have)
    for r in recs:
        for eslug, etext in existing.items():
            j = jaccard(subj(r["prompt"]), subj(etext))
            if j >= DEDUP_FAIL:
                fails.append(f"{r['slug']} ~= (existing) {eslug}  [dedup {j:.2f}] duplicates a still we "
                             f"already have — reuse it or differentiate.")

    # shot variety
    from collections import Counter
    shots = Counter(r["shot"] for r in recs if r["shot"])
    for shot, n in shots.items():
        if n > SHOT_MAX:
            warns.append(f"[shot-variety] '{shot}' used {n}x — vary the framing.")

    print(f"== still_validate: {len(recs)} stills checked - {sum(r['grounded'] for r in recs)} grounded ==")
    if fails:
        print(f"\nBLOCK ({len(fails)}):")
        for f in fails: print("  X " + f)
    if warns:
        print(f"\nWARN ({len(warns)}):")
        for w in warns: print("  ! " + w)
    if not fails:
        print("\nGATE GREEN - no blocking issues.")
    print(f"\n{'FAIL' if fails else 'PASS'}: {len(fails)} block, {len(warns)} warn")
    return len(fails)


if __name__ == "__main__":
    sys.exit(1 if validate() else 0)
