"""Deterministic DOCTRINE-LANDMINE gate ($0, offline).

LLM panels grade doctrine by *recall* and share blind spots — the subtle traps
(John 19:36 "not a bone broken", "couldn't save Himself" inability-concession,
Ps 69-vs-Ps 22 on "I thirst", "died of thirst") were each caught LATE by only one
reviewer. This gate hard-codes the KNOWN recurring traps as pattern checks so they
are flagged EVERY time, regardless of which model remembers them — like the KJV
corpus gate, but for doctrine.

These are heuristic WARN flags for the HUMAN final guard (who reviews by audio),
NOT auto-FAILs — doctrine needs human judgment and the patterns can false-positive.
Every hit is surfaced in the lock report + spoken in the review digest.

Add a landmine when the panel/red-team catches a new doctrinal trap (so it can never
slip late again). See memory `pipeline-verification-hardening`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Landmine:
    name: str
    pattern: re.Pattern
    note: str


def _rx(p: str) -> re.Pattern:
    return re.compile(p, re.IGNORECASE)


# Each: (name, regex over the spoken text, the doctrinal note read aloud to the human)
LANDMINES: list[Landmine] = [
    Landmine("inability-concession",
             _rx(r"\b(could ?n'?t|could not|cannot|can'?t)\s+save\s+(himself|him)\b|\bthey were right\b"),
             "Conceding He COULDN'T save Himself denies His power (heresy). He WOULD not, by choice — voluntary substitution."),
    Landmine("broken-bones",
             _rx(r"\bhe was broken\b|\bbones?\b[^.]{0,25}\bbroke"),
             "John 19:36 / Psalm 34:20: not one of His bones was broken. Use 'crushed' (Isa 53:5) or 'pierced', not 'broken bones'."),
    Landmine("died-of-thirst",
             _rx(r"\bdied of thirst\b|\bthirst\b[^.]{0,15}\b(killed|died)\b"),
             "He thirsted but died by CRUCIFIXION, not of thirst. State the cause accurately."),
    Landmine("thirst-fulfils-ps22",
             _rx(r"\bI thirst\b[^.]{0,80}\b(psalm 22|fulfil|foretold|prophesied)\b|\bpsalm 22\b[^.]{0,40}\bI thirst\b"),
             "John 19:28 'I thirst' is referred to PSALM 69:21, not Psalm 22. Don't claim John cites/fulfils Ps 22 here."),
    Landmine("pierced-variant",
             _rx(r"\bthey pierced (my|his) hands\b|\bpierced my hands and (my )?feet\b"),
             "Psalm 22:16 'pierced' rests on a Masoretic textual variant (vs 'like a lion'). Don't lean on it as undisputed."),
    Landmine("universalism",
             _rx(r"\b(the world|everyone|all (people|men|mankind|humanity)|the whole world)\b[^.]{0,45}\b(brethren|family|God'?s (own )?children|saved|His own)\b"),
             "Risk of universalism: family/salvation is for those who COME to Christ, not the hostile world wholesale (Heb 2:11 = the sanctified)."),
    Landmine("trinity-severed",
             _rx(r"\b(trinity|godhead)\b[^.]{0,25}\b(broke|broken|sever|torn|split|divided)\b|\bgod turned (his |away )?(back|face)\b"),
             "The forsaken cry is judicial God-forsakenness borne as substitute — NOT the Trinity being severed/broken. Don't over-read."),
    Landmine("resurrection-overread",
             _rx(r"\b(psalm|the text|this verse|the song)\b[^.]{0,20}\b(proves|foretells|predicts|guarantees)\b[^.]{0,20}\bresurrection\b"),
             "Resurrection should be NT-WARRANTED (e.g. Heb 2:12), not 'proven' from the bare OT psalm."),
    Landmine("works-selfhelp",
             _rx(r"\b(try harder|clean (yourself|up|your life)|earn (your|it|his|God'?s)|your best life|be a better|do enough|measure up)\b"),
             "Works/self-help framing. The gospel is grace — Christ's finished work, not the viewer's effort."),
    Landmine("fear-pressure",
             _rx(r"\b(before it'?s too late|or you'?ll (go to|burn|end up)|don'?t risk|last chance|act now|time is running out)\b"),
             "Manufactured pressure / fear-selling. The Spirit convicts; the script invites by grace, never by fear or urgency-pressure."),
    Landmine("gain-loss",
             _rx(r"\b(what (you|do you) get|in it for you|so you (can|could) have|your (best|breakthrough|blessing|reward))\b"),
             "Gain/loss / self-interest framing in the call. Anchor the conviction in who Christ is, not what the viewer gets."),
]


def scan(spoken_text: str) -> list[dict]:
    """Return WARN findings: {landmine, matched, note}. Empty = no known trap hit."""
    out: list[dict] = []
    for lm in LANDMINES:
        m = lm.pattern.search(spoken_text)
        if m:
            out.append({"landmine": lm.name, "matched": m.group(0).strip(), "note": lm.note})
    return out


def summarize(findings: list[dict]) -> str:
    if not findings:
        return "no known doctrinal landmines detected"
    return "; ".join(f"[{f['landmine']}] '{f['matched']}' — {f['note']}" for f in findings)
