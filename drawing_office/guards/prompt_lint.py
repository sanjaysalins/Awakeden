"""Pure-code prompt guard — no LLM call.

Encodes failure mode #1 from this week's POC work: prompts using words like
"photograph", "museum artifact", "under glass", "display case" reliably
pulled the image model OUT of illustration mode into full photoreal/
photographed-prop renders (see round2_devices/index.html one_take_scroll
failures). One case even baked an actual legible English museum placard into
the image.

Two checks, both must pass:
  1. No banned photoreal-drift lexicon anywhere in the prompt.
  2. At least one illustration-mode anchor token is POSITIVELY present — it is
     not enough to merely avoid the banned words; the prompt must actively
     assert illustration mode.

This is the function pipeline code calls BEFORE spending money on a
generation (`assert_prompt_ok`) — it must be impossible to accidentally skip.
"""
from __future__ import annotations

BANNED_LEXICON = (
    "photograph",
    "photographed",
    "photorealistic",
    "photo-realistic",
    "photographic",
    "museum artifact",
    "museum case",
    "museum piece",
    "museum display",
    "under glass",
    "display case",
    "glass case",
    "archival photo",
    "archival photograph",
    "photo of",
    "studio photograph",
    "product photography",
    "hyperrealistic",
    "hyper-realistic",
)

REQUIRED_ANCHOR_TOKENS = (
    "illustration",
    "illustrated",
    "hand-drawn",
    "handdrawn",
    "ink",
    "painted",
    "painting",
    "drawn",
    "watercolor",
    "watercolour",
)


def lint_prompt(prompt: str) -> dict:
    """Check a prompt for photoreal-drift lexicon and a positive illustration
    anchor. Returns:
        {"ok": bool, "banned_hits": [...], "missing_anchor": bool, "reasons": [...]}
    `ok` is False if any banned lexicon hit OR no anchor token present."""
    text = (prompt or "").lower()

    banned_hits = [phrase for phrase in BANNED_LEXICON if phrase in text]
    missing_anchor = not any(tok in text for tok in REQUIRED_ANCHOR_TOKENS)

    reasons: list[str] = []
    for phrase in banned_hits:
        reasons.append(
            f"banned phrase found: '{phrase}' (drifts photoreal, see "
            "round2_devices/index.html one_take_scroll failures)"
        )
    if missing_anchor:
        reasons.append(
            "no illustration-mode anchor token present -- the prompt must "
            "positively assert illustration mode, not just avoid banned words "
            f"(need one of: {', '.join(REQUIRED_ANCHOR_TOKENS)})"
        )

    ok = not banned_hits and not missing_anchor
    return {
        "ok": ok,
        "banned_hits": banned_hits,
        "missing_anchor": missing_anchor,
        "reasons": reasons,
    }


def assert_prompt_ok(prompt: str) -> None:
    """Raise ValueError with the joined reasons if the prompt fails
    `lint_prompt`. This is the call site pipeline code actually uses before
    spending money on a generation."""
    result = lint_prompt(prompt)
    if not result["ok"]:
        raise ValueError("; ".join(result["reasons"]))


if __name__ == "__main__":
    cases = [
        (
            "should PASS",
            "A hand-drawn ink illustration of a shepherd standing beneath an "
            "olive tree, soft watercolor wash, warm dusk light.",
            True,
        ),
        (
            "should FAIL on banned lexicon",
            "A museum artifact photograph of an ancient bronze lamp under glass, "
            "studio lighting, illustration style.",
            False,
        ),
        (
            "should FAIL on missing anchor",
            "A shepherd standing beneath an olive tree at dusk, warm golden light, "
            "cinematic composition.",
            False,
        ),
    ]
    all_ok = True
    for label, prompt, expect_ok in cases:
        result = lint_prompt(prompt)
        got_ok = result["ok"]
        status = "PASS" if got_ok == expect_ok else "FAIL (unexpected)"
        if got_ok != expect_ok:
            all_ok = False
        print(f"[{status}] {label}: ok={got_ok} (expected {expect_ok})")
        print(f"         reasons={result['reasons']}")
        if not expect_ok:
            try:
                assert_prompt_ok(prompt)
                print("         !! assert_prompt_ok did NOT raise -- BUG")
                all_ok = False
            except ValueError as e:
                print(f"         assert_prompt_ok raised as expected: {e}")
        else:
            assert_prompt_ok(prompt)  # must not raise
            print("         assert_prompt_ok did not raise, as expected")
    print()
    print("ALL TEST CASES PASSED" if all_ok else "SOME TEST CASES FAILED")
