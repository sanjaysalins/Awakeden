# Independent review — claude (OK, 289s)

The code agent confirmed my review and surfaced **two concrete factual defects I want to add**:

### Addendum — verified facts to fix

- **MC-R1's model id is wrong.** The spec locks `seedream-4-5-251128`. But the actual generator `byteplus_seedream.py:32` defaults to **`seedream-4-0-250828`** (4.0, not 4.5). The `4-5` id only appears in the *bake-off/reshoot* scripts. So the LOCKED recipe cites a model the production script doesn't use. Pin the real one (and if 4.5 is genuinely the winner, fix the generator default, not just the spec).

- **§6 "`add_music_sfx.py` is aspect-clean" is false.** It's hard-coded to specific paths + `.mp4` with no aspect abstraction — it'll need work for 16:9, not a free pass.

- **`kinetic_caption.py` isn't a clean param swap either.** `PAGE_W, PAGE_H = 1080, 1920` at line 13 **and** line 45 scales fonts by `pw / 1080.0` — there's baked-in 1080 baseline math, so 16:9 needs real re-tuning, reinforcing fix #6 (the "parameterize 3 spots" build step is undersized).

None of these change the verdict — they harden fixes #1 and #6. The `seedream-4-5` vs `4-0` mismatch is the sharpest: a **LOCKED spec should never cite a model string the code doesn't run.**

My verdict stands: **REVISE** — the short half is proven and the reuse is real, but the long half is LOCKED-without-a-render, the invariant chain leaves LF-INV-3 contradicting it, several gates are proposed-not-built while the preamble claims otherwise, and the model id is factually wrong.
