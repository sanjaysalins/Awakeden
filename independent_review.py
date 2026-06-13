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
    "cursor": {  # PRIMARY — the user's chosen independent reviewer
        "command": "cursor-agent", "args": ["-p", "--mode", "ask"], "mode": "stdin",
        "prefix": "", "timeout": 300,
    },
    "claude": {
        "command": "claude", "args": ["-p"], "mode": "stdin",
        "prefix": "", "timeout": 300,
    },
    "gemini": {
        "command": "gemini", "args": ["--approval-mode", "plan", "--output-format", "text"],
        "mode": "stdin", "timeout": 300,
        "prefix": "You are a critical reviewer. Output your critique text only. Do not run tools or ask for approval.",
    },
    "codex": {
        "command": "codex", "args": ["exec", "--sandbox", "read-only"], "mode": "stdin",
        "prefix": "", "timeout": 300,
    },
    "grok": {
        "command": "grok", "args": [
            "--no-auto-update", "--prompt-file", "{prompt_file}",
            "--permission-mode", "dontAsk", "--max-turns", "4", "--disable-web-search",
            "--disallowed-tools", "run_terminal_cmd,search_replace,write,web_fetch,web_search",
            "--rules", "You are a critical reviewer. Output your critique text only. Do not edit files or run shell commands.",
            "--output-format", "plain",
        ], "mode": "file", "prefix": "", "timeout": 360,
    },
}

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
- Landing does NEW work (not a tired generic 'will you trust Him?' close).
- Hook grips in the first ~5 seconds."""

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

REVIEW_TEMPLATE = """You are an INDEPENDENT, ADVERSARIAL reviewer. You did NOT write this and you
are NOT here to praise it or rewrite it. Find the problems. Default to skepticism.

ARTIFACT TYPE: {kind}

{lens}
{context}
Read the artifact below. Give concrete, specific findings (cite the exact line/phrase).
Then end your reply with EXACTLY this block:

VERDICT: PASS | REVISE | FAIL
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
    t = time.monotonic()
    try:
        r = subprocess.run(
            cmd, input=stdin_payload, capture_output=True, text=True, env=sub_env,
            encoding="utf-8", errors="replace", timeout=cfg["timeout"],
            stdin=None if stdin_payload is not None else subprocess.DEVNULL,
        )
        dur = time.monotonic() - t
        out = (r.stdout or "").strip()
        ok = r.returncode == 0 and len(out) > 40
        if not out:
            out = f"(no output; exit {r.returncode}; stderr: {(r.stderr or '')[:200]})"
        return name, ok, out, dur
    except subprocess.TimeoutExpired:
        return name, False, f"(timed out after {cfg['timeout']}s)", time.monotonic() - t
    finally:
        if tmp_file:
            tmp_file.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifact", help="path to the finished narration/plan file")
    ap.add_argument("--type", dest="kind", choices=["narration", "plan", "upload"], required=True)
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

    lens = {"narration": LENS_NARRATION, "plan": LENS_PLAN, "upload": LENS_UPLOAD}[args.kind]
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
            print(f"  [{'ok ' if ok else 'FAIL'}] {name:<7} {dur:5.0f}s  "
                  f"{'verdict: ' + out.split('VERDICT:')[-1].strip()[:40] if 'VERDICT:' in out else out[:50]}")

    # index
    idx = [f"# Independent review index — {art.name} ({args.kind})", f"stamp: {stamp}", ""]
    for n in names:
        ok, out, dur = results.get(n, (False, "(missing)", 0))
        verdict = out.split("VERDICT:")[-1].split("\n")[0].strip() if "VERDICT:" in out else "—"
        idx.append(f"- **{n}** — {'OK' if ok else 'FAILED'} ({dur:.0f}s) — verdict: {verdict} — `{n}.md`")
    (outdir / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(f"[review] done -> {outdir / 'INDEX.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
