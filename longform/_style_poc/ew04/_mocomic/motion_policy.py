"""Animation MOTION POLICY (pipeline guardrail).

Maps a scene's motion class to an i2v prompt tail, so generated clips behave with
the comic framing and the narration:

  static      — world breathes (fire/smoke/light), slow push-in, figures still.
  directional — a single one-way motion happens once, then settles; NEVER looped/reversed
                downstream (fill guardrail holds the last frame).
  talk        — TALKING scenes: face/mouth/head HELD still so they don't fight the
                narration; only ambient light moves; an almost-imperceptible push-in.

Identity/style lock is appended to every clip.
"""

TAIL = (" Keep the exact same inked biblical graphic-novel art style, the exact same face and "
        "identity, the same clothing and composition. No morphing, no style change, no photoreal "
        "look, no added or removed figures or objects, no text, no captions, steady reverent light, "
        "no glitter, no sparkles.")

TALK = (" Cinematic motion: ONLY faint ambient detail moves — a lamp or fire flame flickers softly "
        "and its warm light wavers, a wisp of smoke or dust drifts. The face, mouth, eyes, head, "
        "hands and body stay COMPLETELY STILL — no lip movement, no talking, no head turn, no "
        "gesture. An almost imperceptible, very slow push-in.")

STATIC = (" Cinematic motion: the world breathes — firelight flickers, smoke and dust drift, cloth "
          "and hair stir very gently; the figures hold their pose. A slow reverent push-in.")

DIRECTIONAL = (" Cinematic motion: the single one-way movement happens slowly ONCE and then settles; "
               "everything else stays still. A slow push-in. (Downstream this clip is never reversed.)")

POLICY = {"static": STATIC, "directional": DIRECTIONAL, "talk": TALK}


def prompt_for(motion_class, scene_desc=""):
    return (scene_desc + POLICY.get(motion_class, STATIC) + TAIL).strip()
