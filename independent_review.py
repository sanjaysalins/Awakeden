"""independent_review.py — enforced INDEPENDENT review of my finished work.

After I (Claude Code) produce a LOCKED narration or a SIGNIFICANT plan, this fans
the finished artifact out to several local AI CLIs as ADVERSARIAL reviewers
(cursor primary, + claude / gemini / codex / grok), saves each raw review, and
leaves a merged verdict for me to address before declaring the work done.

This replicates the user's ai-panel independent-review pattern, self-contained in
this project. Reviewers run on the user's local CLI subscriptions — NO metered API.

Usage:
  .venv\\Scripts\\python.exe independent_review.py "<artifact.md>" --type narration
  .venv\\Scripts\\python.exe independent_review.py "<plan.md>"      --type plan
  ... --providers cursor,claude            # subset
  ... --context "<extra brief / series-bible path or text>"

Output: <artifact_dir>/_independent_review/<stamp>/{prompt.txt, <provider>.md, INDEX.md}
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# ---- provider invocation (mirrors the user's ai-panel config) ----------------
# mode: "stdin" => prompt piped on stdin; "file" => prompt written, path put in args via {prompt_file}
PROVIDERS = {
    # Model pinned per voice so panel diversity is DETERMINISTIC (5 distinct families:
    # Cursor/Composer, Anthropic, Google, OpenAI, xAI) — never silently collapsed by a
    # CLI changing its default model.
    # Per-reviewer timeouts scale by REVIEW_TIMEOUT_MULT (env, default 1.0). Raised for
    # heavy plan reviews: codex/gemini died at exactly their caps on 6KB artifacts they
    # were fact-checking against the repo (panel rounds 2026-07-14) while perfectly
    # healthy on the doctor's smoke test.
    "cursor": {  # PRIMARY — Cursor's own Composer model (= the default that earned 98% OK)
        "command": "cursor-agent",
        "args": ["-p", "--mode", "ask", "--model", "composer-2.5-fast"], "mode": "stdin",
        "prefix": "", "timeout": 300,
    },
    "claude": {
        "command": "claude", "args": ["-p"], "mode": "stdin",
        "prefix": "", "timeout": 600,
    },
    "gemini": {  # Google voice ROUTED VIA cursor-agent: the native gemini CLI free tier
        # was killed 2026 ("IneligibleTierError: migrate to Antigravity") and had a 48%
        # fail rate. cursor's subscription serves gemini-3.1-pro headlessly today.
        "command": "cursor-agent",
        "args": ["-p", "--mode", "ask", "--model", "gemini-3.1-pro"], "mode": "stdin",
        "prefix": "", "timeout": 300,
    },
    "codex": {
        "command": "codex", "args": ["exec", "--sandbox", "read-only"], "mode": "stdin",
        "prefix": "", "timeout": 300,
    },
    "grok": {
        "command": "grok", "args": [
            "--no-auto-update", "--prompt-file", "{prompt_file}",
            # max-turns raised 4->8: grok spends turns reading files to fact-check, then
            # hit the cap BEFORE emitting the review (35% of runs died with only a
            # preamble line). The rules also demand the VERDICT block in the final reply.
            "--permission-mode", "dontAsk", "--max-turns", "8", "--disable-web-search",
            "--disallowed-tools", "run_terminal_cmd,search_replace,write,web_fetch,web_search",
            "--rules", "You are a critical reviewer. Output your critique text only. Do not edit files or run shell commands. You MUST finish with the full review ending in the VERDICT block — never stop after a status line.",
            "--output-format", "plain",
        ], "mode": "file", "prefix": "", "timeout": 360,
    },
}

# A panel run with fewer OK voices than this (capped at the number requested) is
# DEGRADED — the script exits 3 so callers fail closed instead of locking on it.
MIN_HEALTHY = 4

# ---- review lenses -----------------------------------------------------------
LENS_NARRATION = """LENS — judge this NARRATION on (be specific, cite the exact line/phrase):
- Doctrinal soundness: evangelical, biblically faithful; NO invented doctrine, NO contrarian/
  clickbait/contested readings used to chase freshness.
- KJV verbatim: every word inside quotation marks must be exact KJV. Flag any altered word.
- Clarity on first hearing: a listener with zero Bible knowledge must follow it; no clever-but-
  confusing conceit, no logic trick, no self-contradiction.
- Grace-anchored conviction: NO fear / gain-loss / self-interest / works framing; the Spirit
  convicts, the script invites.
- Freshness = faithful depth: surprising about the TEXT, orthodox in the claim and the landing.
- One thread spine from hook -> middle -> CTA (no thread-swapping).
- SCORE THE HOOK 1-10 (state the number): would a stranger stop scrolling in the first
  ~5 seconds? A template open ("Did you know / Imagine / What if I told you") caps at 5.
- SCORE THE LANDING 1-10 (state the number): is the closing CTA built from THIS piece's
  own image/verb, and does it land in the bones? Ask: "could this exact final sentence
  end a DIFFERENT piece?" If yes ("Come to Jesus", "turn to Him", "look to Jesus"), it is
  a stock closer — cap at 5. Anything under 8 on either score = VERDICT REVISE."""

LENS_PLAN = """LENS — judge this PLAN on (be specific, cite the exact step/claim):
- Feasibility against the real codebase / tools (does it assume things that exist?).
- Hidden risks, false assumptions, single points of failure.
- Over-engineering / premature building before the idea is proven.
- Missing steps, edge cases, or verification gaps.
- Reuse: does it duplicate tools that already exist instead of reusing them?
- Cost / spend and whether it's justified."""

LENS_UPLOAD = """LENS — judge this UPLOAD-METADATA KIT (titles / descriptions / tags /
hashtags for YouTube, TikTok, Facebook, Instagram). Be specific, cite the exact
platform + phrase:
- HOOKY BUT HONEST: does any title clickbait, sensationalise, or overclaim doctrine
  or history? A curiosity hook is fine ONLY if it is true to the text. Flag any lie
  or bait-and-switch (metadata promising what the video doesn't deliver).
- KJV verbatim: any quoted verse must be exact KJV. Flag an altered word.
- Doctrine: evangelical, Christ-pointing, no fear / gain-loss / works framing.
- Platform fit: right tone + a strong FIRST line for TikTok/Instagram; long-form vs
  short framing correct; hashtag counts sane; tags are real search keywords.
- SEO honesty: keywords/tags are relevant to the actual content (no tag-stuffing).
- Forgettable / templated titles that won't earn the click honestly.
- Brand: CTA-to-Jesus present; footer/links not mangled."""

LENS_EYEWITNESS = """LENS — judge this AWAKEDEN EYEWITNESS NARRATION (a named biblical
witness recounts a moment they lived, then it turns to reveal Christ). Be specific,
cite the exact line/phrase:
- KJV verbatim + attribution (EW-INV-4): every word inside `**"..."**` quotes must be
  exact KJV, and the speaker must be attributed before quoting. Flag any altered word or
  misattributed quote.
- CTA-on-Jesus (EW-INV-2): the close must name Jesus/Christ and invite to Him,
  grace-anchored — NO fear / gain-loss / self-interest / manufactured pressure; NO tired
  bare 'will you trust Him?' template; the response (faith / come / turn / receive) must be
  NAMED, not vague.
- The REVEAL is earned (EW-G7): the type->Christ turn is SHOWN from the text the witness
  lived, not merely asserted ('and at last I understood…' must be earned, not announced).
- The WRESTLING is the real steel-man (EW-G8): the witness's honest doubt/question is the
  genuine strongest objection, internalized in their own voice — not a strawman.
- Doctrine sound (EW-G9): evangelical, biblically faithful; the SUBSTITUTION is named
  (the penalty + what Christ bore); NO supersession; no invented/contrarian reading.
- VOICE / character (EW-G10): a consistent, characterful FIRST-PERSON witness — not the
  detached essay narrator wearing a costume.
- First-hearing clarity: a listener with zero Bible knowledge must follow it.
- The hook grips in the first lines; the spine holds — ONE witness, ONE thread, no swap.
- SCORE THE HOOK 1-10 and SCORE THE LANDING 1-10 (state both numbers): the hook must stop
  a stranger scrolling; the landing must be built from THIS witness's own moment/verb —
  if the exact final sentence could end a different piece, it is stock: cap at 5.
  Under 8 on either = VERDICT REVISE."""

LENS_EYEWITNESS_SHORT = (LENS_EYEWITNESS + """
- SHORT form: is it TIGHT (~90s, ~220-320 spoken words) and does the SINGLE moment land —
  no sag, no second thread crowding the one witnessed moment?""")

LENS_EYEWITNESS_LONG = (LENS_EYEWITNESS + """
- LONG form: do the added beats / dialogue / interior wrestling EARN the runtime (~9-11 min),
  or does the piece SAG — padding, repetition, a beat that adds no new turn?""")

LENS_BIBLICAL_FACTS = """LENS — judge this BIBLICAL FACT SHEET (the Scripture-cited facts about
location / time / place / customs / characters that a set of devotional paintings must
honour). Be specific, cite the exact fact + reference:
- CITATION TRUTH (most important): for every fact, does the quoted KJV text (shown under
  each fact) ACTUALLY support the claim? Flag any claim the cited verse does NOT state, any
  over-reach beyond what the verse says, and any citation that looks wrong/misapplied.
- NO INVENTED FACTS: nothing asserted as biblical that Scripture does not actually say.
  Tradition or commonplace-but-unbiblical detail (e.g. a number, a colour, an object the
  text never mentions) must NOT be in the 'specified' bucket.
- BUCKETS ARE HONEST: 'specified' = the Bible explicitly states this visual fact; 'constrained'
  = not stated but a depiction could contradict the text; 'free' = artistic licence. Flag any
  fact in the wrong bucket (especially licence dressed up as 'specified').
- HISTORY STAYS SECONDARY: any historical_note must never override or contradict Scripture; flag
  any that does, or that is presented as if it were biblical.
- CHRIST-LENS INTACT: the facts must not distort the passage's witness to Christ / its typology.
- COVERAGE: are there obvious, checkable biblical facts about these scenes that are MISSING
  (a specified detail the painting could easily get wrong and no fact guards it)?"""

REVIEW_TEMPLATE = """You are an INDEPENDENT, ADVERSARIAL reviewer. You did NOT write this and you
are NOT here to praise it or rewrite it. Find the problems. Default to skepticism.

ARTIFACT TYPE: {kind}

{lens}
{context}
Read the artifact below. Give concrete, specific findings (cite the exact line/phrase).
Then end your reply with EXACTLY this block (on the VERDICT line write exactly ONE word —
PASS or REVISE or FAIL — never the list of options):

VERDICT: <PASS or REVISE or FAIL>
TOP FIXES:
1. <most important fix>
2. <second>
3. <third>

----- ARTIFACT START -----
{artifact}
----- ARTIFACT END -----
"""


def resolve(command: str) -> str | None:
    return shutil.which(command)


def build_cmd(exe: str, args: list[str]) -> list[str]:
    if os.name == "nt" and exe.lower().endswith((".cmd", ".bat")):
        return ["cmd.exe", "/c", exe, *args]
    return [exe, *args]


def run_one(name: str, prompt: str, outdir: Path) -> tuple[str, bool, str, float]:
    cfg = PROVIDERS[name]
    exe = resolve(cfg["command"])
    if not exe:
        return name, False, f"(not installed: {cfg['command']})", 0.0
    full = (cfg.get("prefix", "") + "\n\n" + prompt).strip() if cfg.get("prefix") else prompt
    tmp_file: Path | None = None
    args = list(cfg["args"])
    stdin_payload: str | None = None
    if cfg["mode"] == "file":
        fd, p = tempfile.mkstemp(suffix=".txt", prefix=f"{name}_review_")
        os.close(fd)
        tmp_file = Path(p)
        tmp_file.write_text(full + "\n", encoding="utf-8")
        args = [a.replace("{prompt_file}", str(tmp_file)) for a in args]
    else:
        stdin_payload = full
    cmd = build_cmd(exe, args)
    # SPEND FIX: strip metered API keys from the reviewer subprocess so each CLI uses
    # its (free) SUBSCRIPTION login — e.g. `claude` -> Max plan, `gemini` -> oauth —
    # instead of billing ANTHROPIC_API_KEY / GEMINI_API_KEY. Set JITB_PANEL_USE_API=1
    # to keep the keys (metered) if a CLI has no subscription fallback.
    sub_env = dict(os.environ)
    if os.getenv("JITB_PANEL_USE_API", "0") not in ("1", "true", "yes"):
        for k in ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY"):
            sub_env.pop(k, None)
    tmo = round(cfg["timeout"] * float(os.getenv("REVIEW_TIMEOUT_MULT", "1")))
    t = time.monotonic()
    try:
        r = subprocess.run(
            cmd, input=stdin_payload, capture_output=True, text=True, env=sub_env,
            encoding="utf-8", errors="replace", timeout=tmo,
            stdin=None if stdin_payload is not None else subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        dur = time.monotonic() - t
        out = (r.stdout or "").strip()
        ok = r.returncode == 0 and len(out) > 40
        if not out:
            out = f"(no output; exit {r.returncode}; stderr: {(r.stderr or '')[:200]})"
        return name, ok, out, dur
    except subprocess.TimeoutExpired:
        return name, False, f"(timed out after {tmo}s)", time.monotonic() - t
    finally:
        if tmp_file:
            tmp_file.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifact", help="path to the finished narration/plan file")
    ap.add_argument("--type", dest="kind",
                    choices=["narration", "plan", "upload", "eyewitness-short", "eyewitness-long",
                             "biblical-facts"],
                    required=True)
    ap.add_argument("--providers", default="cursor,claude,gemini,codex,grok")
    ap.add_argument("--context", default="", help="extra brief, or a path to one")
    ap.add_argument("--red-team", dest="red_team", action="store_true",
                    help="adversarial RED-TEAM via a NON-Claude subscription CLI "
                         "(default codex) — independent of the Claude main loop, no metered API. "
                         "Override the model with --providers.")
    args = ap.parse_args()

    if args.red_team and args.providers == "cursor,claude,gemini,codex,grok":
        args.providers = os.getenv("JITB_REDTEAM_PROVIDER", "codex")  # non-Claude, subscription

    art = Path(args.artifact)
    if not art.is_file():
        print(f"artifact not found: {art}", file=sys.stderr)
        return 2
    artifact_text = art.read_text(encoding="utf-8").strip()

    ctx = args.context
    if ctx and Path(ctx).is_file():
        ctx = Path(ctx).read_text(encoding="utf-8").strip()
    ctx_block = f"\nADDITIONAL CONTEXT / BRIEF:\n{ctx}\n" if ctx else ""

    lens = {"narration": LENS_NARRATION, "plan": LENS_PLAN, "upload": LENS_UPLOAD,
            "eyewitness-short": LENS_EYEWITNESS_SHORT,
            "eyewitness-long": LENS_EYEWITNESS_LONG,
            "biblical-facts": LENS_BIBLICAL_FACTS}[args.kind]
    if args.red_team:
        lens = ("RED-TEAM LENS — you are a HOSTILE adversary. Assume it is flawed and PROVE it. "
                "Hunt doctrinal error, Scripture misquote/overclaim, cheesy/tired lines, and anything "
                "that would embarrass a careful pastor. Default to REVISE/FAIL unless it is clearly clean.\n\n"
                + lens)
    prompt = REVIEW_TEMPLATE.format(kind=args.kind, lens=lens, context=ctx_block,
                                    artifact=artifact_text)

    names = [n.strip() for n in args.providers.split(",") if n.strip() in PROVIDERS]
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir = art.parent / "_independent_review" / stamp
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "prompt.txt").write_text(prompt, encoding="utf-8")

    print(f"[review] {art.name} ({args.kind}) -> {len(names)} reviewer(s): {', '.join(names)}")
    print(f"[review] artifact {len(artifact_text)} chars · out -> {outdir}")

    results: dict[str, tuple[bool, str, float]] = {}
    with ThreadPoolExecutor(max_workers=len(names)) as ex:
        futs = {ex.submit(run_one, n, prompt, outdir): n for n in names}
        for f in as_completed(futs):
            name, ok, out, dur = f.result()
            results[name] = (ok, out, dur)
            (outdir / f"{name}.md").write_text(
                f"# Independent review — {name} ({'OK' if ok else 'FAILED'}, {dur:.0f}s)\n\n{out}\n",
                encoding="utf-8")
            line = (f"  [{'ok ' if ok else 'FAIL'}] {name:<7} {dur:5.0f}s  "
                    f"{'verdict: ' + out.split('VERDICT:')[-1].strip()[:40] if 'VERDICT:' in out else out[:50]}")
            # console may be cp1252 — never let a fancy character kill the run
            print(line.encode("ascii", "replace").decode("ascii"))

    # index
    idx = [f"# Independent review index — {art.name} ({args.kind})", f"stamp: {stamp}", ""]
    for n in names:
        ok, out, dur = results.get(n, (False, "(missing)", 0))
        verdict = out.split("VERDICT:")[-1].split("\n")[0].strip() if "VERDICT:" in out else "—"
        idx.append(f"- **{n}** — {'OK' if ok else 'FAILED'} ({dur:.0f}s) — verdict: {verdict} — `{n}.md`")
    healthy = sum(1 for ok, _, _ in results.values() if ok)
    quorum = min(MIN_HEALTHY, len(names))
    idx.append(f"\nhealthy voices: {healthy}/{len(names)} (quorum {quorum})"
               + ("" if healthy >= quorum else " — **DEGRADED PANEL — do not lock on this run**"))
    (outdir / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(f"[review] done -> {outdir / 'INDEX.md'}")
    if healthy < quorum:
        print(f"[review] DEGRADED PANEL: only {healthy}/{len(names)} voices answered "
              f"(quorum {quorum}). Fix the dead reviewers and re-run — do NOT lock on this.",
              file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
