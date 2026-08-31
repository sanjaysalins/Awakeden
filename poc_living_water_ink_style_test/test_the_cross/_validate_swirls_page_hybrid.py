"""$0 validation: prove swirls_page.py's panel_style="woodcut_hybrid" branch
reproduces the validated hybrid-panel test byte-for-byte. Content comes from
the SAME real PageSpec (Jacob's Ladder F08) the original test itself sliced
its content from -- not retyped here either -- so this validates assembly
logic only, same discipline as _validate_swirls_page.py /
_validate_swirls_page_hem.py. See NORTH_STAR_PROMPT.md's "Hybrid panel
variant" section and PRODUCTION_PIPELINE.md's migration-path pattern.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\_validate_swirls_page_hybrid.py
"""
import dataclasses
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT_DIR = HERE.parent / "swirls_pilot_01_jacobs_ladder"
HYBRID_TEST_DIR = PILOT_DIR / "_style_test_durer_woodcut"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PILOT_DIR))
sys.path.insert(0, str(HYBRID_TEST_DIR))

from swirls_page import assemble_still_prompt, _refs_clause  # noqa: E402
import render_hybrid_panels as hybrid_test  # noqa: E402 (imports render_jacobs_ladder itself)

f08_hybrid_spec = dataclasses.replace(hybrid_test.F08, panel_style="woodcut_hybrid")
generated = assemble_still_prompt(f08_hybrid_spec)
original = hybrid_test.PROMPT

# SECOND KNOWN, DISCLOSED deviation (fix, not a bug -- 2026-08-31): the original
# one-off test's own opening sentence never named "aged cream paper" (STYLE_OPEN_HYBRID
# used to open straight into "...laid out like a real found piece of production art",
# omitting the substrate clause STYLE_OPEN's plain-template sibling has always carried).
# Real-world consequence: episode 7 F01 rendered as a photo of the page taped to a
# wood-grain desk instead of the page filling the frame edge-to-edge -- every prior
# hybrid-style episode (2/4/5/8) happened not to trigger this, but the missing anchor
# was there the whole time. STYLE_OPEN_HYBRID now carries the same "aged cream paper"
# phrase as STYLE_OPEN plus an explicit no-desk/no-tape negative; this script's
# byte-identical check on the CORE PROSE is expected to diff starting at that clause.
# See swirls_episode_07_the_bier_he_touched/_f01_review.html for the defective render.

# KNOWN, DISCLOSED deviation (not a bug): render_hybrid_panels.py was a one-off style
# test that passed its refs only as `--image` CLI flags, never as a prompt-text
# manifest -- it predates this module's ref-chaining convention. Every other page in
# this pipeline (including F08's own REAL shipped ink-wash render) gets the manifest
# clause via _refs_clause(), per the locked "every recurring subject gets a ref" rule.
# The hybrid branch correctly includes it too; validate that exactly, rather than
# reproducing the one-off test's gap.
expected_refs_clause = _refs_clause(f08_hybrid_spec.refs)
core_generated, tail_generated = generated[:len(original)], generated[len(original):]

print("=== HYBRID STILL PROMPT DIFF (F08) ===")
if core_generated != original:
    print("MISMATCH in core prose (unexpected -- not just the disclosed refs-clause gap)")
    for k in range(min(len(core_generated), len(original))):
        if core_generated[k] != original[k]:
            print(f"  first diff at char {k}:")
            print(f"    generated: ...{core_generated[max(0, k - 40):k + 40]!r}...")
            print(f"    original:  ...{original[max(0, k - 40):k + 40]!r}...")
            break
elif tail_generated != expected_refs_clause:
    print("MISMATCH: core prose is byte-identical, but the trailing refs clause is not "
          "the module's own _refs_clause() output")
    print(f"  tail: {tail_generated!r}")
    print(f"  expected: {expected_refs_clause!r}")
else:
    print("BYTE-IDENTICAL on core prose (validated hybrid test) PASS")
    print(f"PLUS the disclosed refs-manifest clause ({len(expected_refs_clause)} chars, "
          "the module's standard _refs_clause() output, absent only because the "
          "one-off test never called it) -- confirmed exact match, PASS")
