# Independent review — codex (OK, 224s)

**Findings**

- **Rule-change order is unsafe.** The plan says `DELIBERATELY revises §5's universal letter-by-letter reveal, pending panel`, but build step 5 updates `living-sketchbook/SKILL.md` before step 6 runs `External 5-CLI panel review`. Existing §5 currently mandates KJV Scribed Ink `letter-by-letter` ([SKILL.md](<C:/Users/sanjay/PycharmProjects/JesusInTheBible/.claude/skills/living-sketchbook/SKILL.md:142>)). The panel should review a draft patch before the locked skill changes.

- **`held_breath` is misused as emotion detection.** The claim `the narration's own fear drives the hand` assumes `held_breath` yields fear/panic. It does not. `energy_envelope()` is a silence damper: `1.0 during speech`, dipping toward a floor only during gaps ([held_breath.py](<C:/Users/sanjay/PycharmProjects/JesusInTheBible/panel_animator/held_breath.py:57>)). Feeding it into `0 calm ... 1 panic` will make all speech high-energy regardless of fear.

- **The proposed API does not exist in the referenced POC.** The plan says promote `_keeper_poc/_build_poc.py` into `KeeperEntry(...).compose(frame,t)` with `starve` and `interrupt_at`. The POC has free functions like `entry_events()` and `compose_at()`, not that API ([build_poc.py](<C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/storm/_keeper_poc/_build_poc.py:147>)). `interrupt` and `starve` are separate one-off logic in `_vault_poc`, not part of the keeper POC engine.

- **Two new transitions are being promoted without a taste gate.** The phrase `v1 ships torn_out ... plus two siblings` adds `slide_under` and `lift_away`, but Round 6 only kept Torn-Out Page and noted `we can have more such transition effects built in`. That is permission to explore, not approval to ship two new effects in a “promotion” round.

- **Foley duplicates an existing subsystem and hides a known asset gap.** The plan introduces `pencil_scratch`, `drop`, `dry-scratch/dip`, but existing `scriptorium_foley` already owns cue mapping and says new devices need `DEVICE_SOUND_MAP`, not parallel cue tables ([SKILL.md](<C:/Users/sanjay/PycharmProjects/JesusInTheBible/.claude/skills/scriptorium-foley/SKILL.md:71>)). It also states there are zero stationery/paper-craft recordings and current scratch assets are weak substitutes pending ear approval ([SKILL.md](<C:/Users/sanjay/PycharmProjects/JesusInTheBible/.claude/skills/scriptorium-foley/SKILL.md:24>)).

- **Skill registration is underspecified.** `SKILL.md registrations (/keeper-hand, ...)` is not enough. Existing skills include frontmatter, CLI usage, schema, guardrails, and verification steps. The plan does not define CLIs, spec JSON, assembler import points, or how these modules become callable in the current pipeline.

- **Self-tests miss the plan’s central laws.** The listed tests check jitter, byte stability, starve alpha, and interruption. They do not verify KJV exactness, Word-vs-Keeper separation, “Word never torn/bleeds/starves,” face/lane safety on moving clips, phone-scale legibility, or the §7 near-silence sound rule.

- **The review gate is filtered by the plan author.** `REVISE verdicts I dispute go to the user` is not independent review. All panel findings and terminal verdicts should go to the user, including FAILs and undisputed REVISE findings.

VERDICT: REVISE
TOP FIXES:
1. Reorder governance: panel/user approval before changing §5, and require gates for unproven transition siblings.
2. Replace the held-breath-as-fear assumption with a real authored/derived energy model, then extract a real keeper API from all relevant POCs.
3. Reuse `scriptorium_foley` and existing skill/CLI patterns, with explicit foley cost, asset, and ear-approval steps.
