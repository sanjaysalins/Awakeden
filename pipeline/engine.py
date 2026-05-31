"""The Anthropic-powered narration engine: generate -> review -> revise.

Uses Claude Opus 4.7 with adaptive thinking. The constitution + full series
library form a stable system-prompt prefix that is prompt-cached, so the three
calls per run (and every subsequent run) reuse the cache. Role-specific
instructions live in a second, un-cached system block.
"""
from __future__ import annotations

import json
from functools import lru_cache

import anthropic

import config
from pipeline import kjv_check
from pipeline.models import Draft, GateResult, Review, Thread
from pipeline.series import Episode, Series, render_series_library
from pipeline.structures import Structure, render as render_structure


# --------------------------------------------------------------------------
# Client + shared (cached) context
# --------------------------------------------------------------------------
@lru_cache(maxsize=1)
def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=config.require_api_key())


@lru_cache(maxsize=1)
def _shared_context() -> str:
    """Constitution + series library — identical on every call, so it caches."""
    constitution = config.CONSTITUTION_PATH.read_text(encoding="utf-8")
    return constitution + "\n\n" + render_series_library()


def _call(role_instructions: str, user_text: str, model: str | None = None,
          label: str = "text") -> str:
    """One Opus 4.7 call. Returns the concatenated text (thinking omitted).

    In agent-mode (LLM_PROVIDER=agent) this routes to the in-chat agent via the
    file bridge instead of the metered API (no API key required).

    Otherwise uses streaming because the non-streaming SDK errors out for any
    call whose `max_tokens` could exceed the 10-minute non-streaming timeout. We
    target ~32K output for large scene plans, so streaming is the default."""
    if config.agent_mode():
        from pipeline import agent_bridge
        return agent_bridge.call_text(
            role=role_instructions,
            user=user_text,
            model=model or config.MODEL,
            shared=_shared_context(),
            label=label,
        )
    with _client().messages.stream(
        model=model or config.MODEL,
        max_tokens=config.MAX_TOKENS,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": _shared_context(),
                "cache_control": {"type": "ephemeral"},  # cache the stable prefix
            },
            {"type": "text", "text": role_instructions},
        ],
        messages=[{"role": "user", "content": user_text}],
    ) as stream:
        message = stream.get_final_message()
    return "".join(b.text for b in message.content if b.type == "text").strip()


def _extract_json(text: str) -> dict:
    """Pull a JSON object out of the model's reply, tolerant of fences/prose."""
    fence = text.find("```json")
    if fence != -1:
        start = text.find("\n", fence) + 1
        end = text.find("```", start)
        if end != -1:
            return json.loads(text[start:end].strip())
    # Fallback: first '{' to its matching last '}'.
    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1 and last > first:
        return json.loads(text[first : last + 1])
    raise ValueError(f"No JSON object found in model reply:\n{text[:500]}")


# --------------------------------------------------------------------------
# Episode context block (shared by all three stages)
# --------------------------------------------------------------------------
def _episode_block(
    series: Series, episode: Episode, kjv_text: str | None, notes: str
) -> str:
    verse = (
        f'VERIFIED KJV TEXT for {episode.primary_ref} (quote this VERBATIM):\n"{kjv_text}"'
        if kjv_text
        else (
            f"NOTE: the exact KJV text for {episode.primary_ref} could not be auto-"
            f"verified. Quote the King James Version from your knowledge and be precise."
        )
    )
    notes_line = f"\nCREATOR NOTES / ANGLE: {notes}" if notes.strip() else ""
    return (
        f"SERIES: {series.name}  (brand: {series.brand})\n"
        f"SERIES HOOK PATTERN: {series.hook_pattern}\n"
        f"SERIES CTA PATTERN: {series.cta_pattern}\n"
        f"SERIES GUARDRAILS (binding): {series.guardrails}\n\n"
        f"EPISODE: {episode.title}\n"
        f"PRIMARY SCRIPTURE: {episode.primary_ref}\n"
        f"SUPPORTING REFS: {', '.join(episode.refs)}\n"
        f"THEME: {episode.theme}\n\n"
        f"{verse}{notes_line}"
    )


# --------------------------------------------------------------------------
# Thread blocks — shared by generate / revise (the writer-side prompts) and
# by review / independent_review (the auditor-side prompts).
# --------------------------------------------------------------------------
def _thread_block(thread: Thread | None) -> str:
    """Writer-side: tell the model what thread to carry through hook->middle->CTA."""
    if thread is None or thread.is_empty:
        return ""
    return (
        "\n\n=== THREAD (carry this through hook -> middle -> CTA) ===\n"
        f"THREAD: {thread.thread}\n"
        f"LEVER: {thread.lever}\n"
        f"ANCHOR: {thread.anchor_ref} — {thread.anchor_detail}\n"
        f"WHY FRESH: {thread.why_fresh}\n"
        f"GOSPEL LANDING: {thread.gospel_landing}\n"
        "Open the hook on this thread, prove it in the proof beat, and mirror "
        "it in the landing. Do not abandon the thread halfway. Stay orthodox "
        "in the claim and the landing; freshness lives in the entry point only."
    )


def _thread_review_block(thread: Thread | None) -> str:
    """Reviewer-side: tell the auditor what thread the draft was written to carry,
    so the Jaded Scroller and Theologian can judge follow-through and honesty."""
    if thread is None or thread.is_empty:
        return ""
    return (
        "\n\n=== INTENDED THREAD (the draft was written to carry this) ===\n"
        f"THREAD: {thread.thread}\n"
        f"LEVER: {thread.lever}\n"
        f"ANCHOR: {thread.anchor_ref} — {thread.anchor_detail}\n"
        f"WHY FRESH: {thread.why_fresh}\n"
        f"GOSPEL LANDING: {thread.gospel_landing}\n"
        "Check whether the draft actually carries this thread from hook through "
        "proof to landing, and whether it remains exegetically honest — no "
        "contrarian eisegesis, no doctrinal hot take in the name of freshness."
    )


# --------------------------------------------------------------------------
# Stage 0 — discover_thread (the freshest TRUE thread for this topic)
# --------------------------------------------------------------------------
_THREAD_JSON_CONTRACT = """\
{
  "candidates": [
    {
      "thread": "<short evocative image or tension>",
      "lever": "overlooked-detail | original-language | nt-confirmed-ot-echo | cultural-historical",
      "anchor_ref": "Book chapter:verse",
      "anchor_detail": "<the specific true detail being surfaced>",
      "why_fresh": "<why this is not the obvious topic auto-complete>",
      "gospel_landing": "<how this carries through to a grace-anchored response to Jesus>"
    }
    // 3 or 4 candidates total, covering at least 3 of the 4 levers
  ],
  "chosen_index": 0,
  "chosen_rationale": "<why this candidate is the freshest yet exegetically honest pick>"
}"""


def discover_thread(
    series: Series, episode: Episode,
    kjv_text: str | None, passage: str | None,
    notes: str = "",
) -> Thread:
    """Mine the wider pericope for 3-4 candidate threads (the four levers from
    the charter), then pick the freshest that is exegetically honest and yields
    a clean gospel landing. The chosen thread runs through hook -> middle -> CTA."""
    role = f"""\
YOUR TASK: find the SHARPEST TRUE thread to carry this 60-second short.
Be surprising about the *text* (overlooked detail, original-language nuance,
NT-confirmed OT echo, cultural-historical context) — never about the *truth*.
Orthodoxy in the claim and the landing; novelty in the entry point only.

The four levers (your candidates should cover at least three of them):
1. OVERLOOKED DETAIL — a specific word, action, posture, or item in the verse
   that most takes skip past (e.g. "he kissed him" *before* any confession;
   "she left her waterpot"; "a great way off").
2. ORIGINAL-LANGUAGE REVEAL — a Greek/Hebrew nuance the KJV preserves but most
   English readers miss (splanchnizomai = bowels-yearning; tetelestai = paid
   in full). Surface honestly; do not smuggle in foreign doctrine.
3. NT-CONFIRMED OT ECHO — an OT passage Jesus or an apostle *explicitly*
   anchors this scene to. Real, cited echoes only — not a typological reach.
4. CULTURAL-HISTORICAL CONTEXT — a first-century reality that changes what the
   text feels like (a Jewish patriarch running was a public shame; a Samaritan
   woman at noon meant social exile).

EACH candidate must:
- Be a short, evocative IMAGE OR TENSION (not a doctrine summary, not a moral).
- Be pinned to one SPECIFIC TRUE detail and the SPECIFIC verse that anchors it
  in the passage below. If you cannot pin it to a verse, do not propose it.
- Yield a clean GOSPEL LANDING — a response to Jesus by grace, not application.
- NOT be the obvious topic auto-complete (e.g. prodigal -> "the son came home"
  is the auto-complete; "the father ran" or "fell on his neck and kissed him"
  is a fresh-yet-honest pick). Read the cliché blocklist in the charter.

Then choose the freshest candidate that remains EXEGETICALLY HONEST. If two are
equally fresh, prefer the one hardest to predict from the title alone. If a
"fresh" candidate is exegetically dishonest, do not choose it.

Return ONLY a JSON object (optionally inside a ```json fence):
{_THREAD_JSON_CONTRACT}
No prose outside the JSON object."""

    passage_block = (
        f"\n\nWIDER PERICOPE (mine THIS for the thread; cite specific verses):\n{passage}\n"
        if passage else ""
    )
    user = _episode_block(series, episode, kjv_text, notes) + passage_block
    reply = _call(role, user)
    return Thread.from_json(_extract_json(reply))


# --------------------------------------------------------------------------
# Stage 1 — generate
# --------------------------------------------------------------------------
def _json_contract(structure: Structure) -> str:
    beat_lines = ",\n    ".join(
        f'{{"id": "{b.id}", "text": "the {b.name} beat (~{b.word_guide} words)"}}'
        for b in structure.beats
    )
    return (
        "{\n"
        '  "title": "short punchy title for the video",\n'
        '  "hook_type": "curiosity | consequence | identity | time-pressure",\n'
        '  "beats": [\n    ' + beat_lines + "\n  ],\n"
        '  "scripture_reference": "Book chapter:verse",\n'
        '  "scripture_quoted": "the exact KJV words you quoted, verbatim",\n'
        '  "speakers": ["lowercase non-narrator voices whose quotes appear, e.g. jesus, disciples, crowd; empty if narrator-only"]\n'
        "}"
    )


def _generate_role(structure: Structure, variation: str = "") -> str:
    role = (
        "YOUR TASK: write ONE 60-second short narration for the episode below,\n"
        "following the charter, the series guardrails, and the STRUCTURE exactly.\n\n"
        f"{render_structure(structure)}\n\n"
        f"Total target: {config.TARGET_WORDS_MIN}-{config.TARGET_WORDS_MAX} words across all beats.\n"
        "Write one plain-prose text block per beat (no audio tags, no <speaker> markup,\n"
        "no headings, no emoji). Character speech goes in the proof beat as plain quotes.\n"
        "Honour grace-anchored conviction: no gain/loss framing, no manufactured pressure.\n"
        "If a THREAD block follows, that thread is the spine of this short — open the hook "
        "on it, prove it in the proof beat, and mirror it in the landing.\n\n"
        "THE FIVE QUESTIONS (answer before writing — the review enforces this as gate G8):\n"
        "1. WHAT AM I REALLY SAYING? One sentence; every beat serves it. Hook and body must "
        "carry the SAME idea — no drift between the hook's promise and the body's payoff.\n"
        "2. AM I SAYING IT PROFOUNDLY, NOT EXPLAINING IT? Make the viewer FEEL the truth via a "
        "concrete image/turn. Banned: lecture phrasing ('Notice the order', 'This teaches us', "
        "'The point is') — show, do not summarise.\n"
        "3. CORRECT STRUCTURE? One idea, one turn; conviction beat must PIERCE (feeling, not "
        "facts); the series signature must be present (QJA: the question turns onto the VIEWER).\n"
        "4. WHO IS THIS FOR? Write the hook + turn for ONE named real person (the doubter, the "
        "exhausted performer, the admirer who won't bow, the grieving, the ashamed). Not everyone. "
        "CRITICAL: this audience is a PLANNING answer for YOU only — it must NEVER appear as a spoken "
        "line in the narration. Banned in the script: 'This one's for…', 'If you're someone who…', "
        "'For the person who…'. Speak TO that person directly; never name them aloud.\n"
        "5. WHAT DO THEY TAKE AWAY? A CHANGE in how they see Christ + a response to Jesus by "
        "grace — never merely a fact learned.\n\n"
        "THE FIRST-HEARING TEST (clarity beats cleverness — G8 enforces this hardest):\n"
        "Write for a TIRED STRANGER who does not know this Bible story and will hear the words "
        "ONCE, at speed, with no rewind. Every beat must land on first hearing.\n"
        "- The SPINE must be a felt TRUTH, never a writerly conceit. Geography trivia, "
        "original-language nuance, grammar/word-order, and clever wordplay may SEASON one line, "
        "but they can NEVER be the point. Test: say the beat's idea plainly in 6 words — if "
        "nothing survives, the conceit WAS the point and the beat fails.\n"
        "- Assume ZERO prior Bible knowledge. If a beat only makes sense to someone who already "
        "knows the setting/the characters/the back-story, rewrite it so the stranger follows. "
        "Name who is speaking and where we are in plain terms before leaning on any detail.\n"
        "- NO logic-tricks. Do not smuggle in a syllogism the viewer must accept on faith "
        "(e.g. 'only one kind of man would do this') — it reads as a trap, not a truth.\n"
        "- NO self-contradiction. The landing must RESOLVE the thread, never reverse it. If the "
        "body says 'grace doesn't wait for your answer', the close cannot then demand an answer. "
        "Re-read hook->landing as one breath and cut any beat that fights another.\n"
        "If the freshest thread is also the cleverest-but-coldest, pick the CLEAREST true thread "
        "instead — a plain profound truth always beats a clever one the viewer can't follow.\n\n"
        "THE LANDING TEST (the close is where a short dies tired — judge it hardest):\n"
        "A strong hook earns nothing if the last 8 seconds feel heard-before. The landing must "
        "DELIVER, not summarise. Rules:\n"
        "- The final line must do NEW work — reveal the thread's last image, or name what is now "
        "true of Christ for THIS viewer. It must NOT restate the body in tireder words.\n"
        "- BANNED tired closers (you have heard them ten thousand times): a bare rhetorical "
        "'Will you trust Him? / Will you come to Him? / Will you follow Him?' tacked on as the "
        "last line; 'the choice is yours'; 'He's waiting for you'; 'all you have to do is believe'; "
        "any close that would fit ANY episode unchanged. If your last line could end a different "
        "short about a different verse, it is too generic — rewrite it around THIS thread's image.\n"
        "- Prefer ending ON a concrete picture or a quiet declarative of grace over ending on a "
        "question. A question close is allowed ONLY if it carries new weight the body has not "
        "already implied. When in doubt, do not end on a question.\n"
        "- GRACE-TUNED QUESTION (critical): if the close turns the verse's question onto the "
        "viewer, the ANSWER must point to grace / what God gives — NEVER demand the viewer "
        "PRODUCE it. A close that says 'so, what's your answer?' secretly preaches 'try harder to "
        "believe' and snaps the grace anchor on the last line. Frame the true answer as something "
        "received (the Father reveals it / puts it on your lips / opens your eyes), not achieved.\n"
        "- SCENE-SCOPE THEOLOGY: the landing's claim must be airtight to THIS scene and the wider "
        "pericope provided — do NOT import later theology the passage does not carry (e.g. before "
        "the resurrection, do not lean the close on 'He rose / empty tomb / alive from the grave'; "
        "'living' that means present-and-facing-you is safe, 'living' that means risen is an "
        "anachronism here). Freshness never licenses smuggling in a doctrine the text hasn't reached.\n"
        "- Read the hook and the landing back to back: the landing should feel like the hook's "
        "image RETURNING transformed by the gospel — not a generic altar-call bolted on.\n\n"
        "OPENING STRATEGY (smart-default): DEFAULT to problem-first — open on a REAL present ache "
        "the viewer feels in 3s, then turn. HARD GUARDRAIL (G8 enforces): the turn AND landing go to "
        "WHO CHRIST IS, never to 'your problem solved' — the ache is the doorway, Christ is the room; "
        "any 'and so your anxiety lifts / life improves' payoff is self-help and FAILS. OVERRIDE the "
        "default when the text is confrontational / identity-revealing / a direct claim of Christ "
        "(e.g. 'Who do you say I am?' is a confrontation, not a felt problem) — then cold-open in the "
        "scene, reverse, or go question-first. Pick the opening the TEXT earns.\n\n"
        "MULTI-VOICE DELIVERY (charter: \"Speakers — Let the Scene Breathe\"):\n"
        "- If the verified KJV text is from a PARABLE (Luke 15, Luke 10, Matt 13/25, etc.), "
        "render the parable quote as JESUS speaking. Introduce it in your own narrator "
        "prose (\"Jesus tells it like this:\") and put `jesus` in `speakers`.\n"
        "- INNER PARABLE CHARACTER LINES GET THEIR OWN VOICE. If a parable contains a "
        "character's line (the son's rehearsed confession, the steward's calculation, the "
        "Pharisee's prayer, the master's verdict), pull that line OUT of the surrounding "
        "narration AND out of Jesus' voice, attribute it in your own narrator prose, and "
        "let the character speak it as their own quoted line — for example, the prodigal "
        "should yield 4 turns in order: narrator (hook) → jesus (the running/kissing verse) "
        "→ narrator (pivot: \"He had rehearsed a third line on the road —\") → son "
        "(\"make me as one of thy hired servants.\"). DO NOT keep the inner line inside "
        "Jesus' voice; DO NOT leave it in narrator commentary. Add EVERY such inner "
        "character (e.g. `son`) to `speakers`.\n"
        "- If the KJV text itself is a CHARACTER speaking outside a parable (the Samaritan "
        "woman, the centurion, Peter, etc.), render their words as character speech with "
        "the attribution in your own narrator prose, and include that character in `speakers`.\n"
        "- Declare EVERY non-narrator voice used in `speakers` (lowercase, no \"narrator\"). "
        "A speaker whose words appear but who is missing from the list falls through to the "
        "narrator and the multi-voice intent is lost.\n"
        "- Narrator-only IS right when the verse is reflective/doctrinal/meditative rather "
        "than spoken-in-the-scene (an \"I AM\" reflection, a Pauline line). Do not force "
        "dialogue on a meditative short; do reach for it whenever the text gives you a voice.\n\n"
        + (variation + "\n\n" if variation else "")
        + "Return ONLY a JSON object (optionally inside a ```json fence) with the beat ids "
        f"exactly {structure.beat_ids} in this order:\n"
        f"{_json_contract(structure)}\n"
        "No prose outside the JSON object."
    )
    return role


def generate(
    series: Series, episode: Episode, kjv_text: str | None,
    structure: Structure, notes: str = "",
    thread: Thread | None = None,
) -> Draft:
    role = _generate_role(structure)
    user = _episode_block(series, episode, kjv_text, notes) + _thread_block(thread)
    return Draft.from_json(_extract_json(_call(role, user)))


# --------------------------------------------------------------------------
# Stage 1b — DRAFT TOURNAMENT (generate N divergent drafts -> judge the arc ->
# synthesize the winner + graft the strongest version of ANY beat from the other
# candidates + apply the judge's synthesis_notes). The fix for "feels over-used /
# the CTA is formulaic": explore several arcs instead of polishing the first one.
# (Grafting any beat — not just hook/CTA — lets the best conviction/proof from a
# runner-up combine with the winner's arc; see _collect_grafts.)
# --------------------------------------------------------------------------
_HOOK_STRATEGIES = [
    "COLD-OPEN IN THE SCENE — drop the viewer into a concrete sensory moment (a smell, a sound, a posture, the light) before any explanation.",
    "OVERLOOKED DETAIL AS THE DOOR — open on the one specific textual detail of the thread (the word, object, or gesture most readers skip past).",
    "A DIRECT SECOND-PERSON CONFRONTATION — name the viewer's real, present ache or false assumption in the very first line.",
    "A REVERSAL — state the expected/familiar reading first, then turn it on its head with what the text actually says.",
    "A PROVOCATIVE TRUE CLAIM — open on a sharp, surprising-but-orthodox statement that reframes the familiar story.",
    "A QUESTION THAT INDICTS — open on a question the viewer cannot answer comfortably, then let the text press it.",
]
_CTA_STRATEGIES = [
    "a fresh CONCRETE IMAGE that completes the thread's picture — end ON the scene (the open door, the dropped jar, the face with the wounds), not on an abstraction or a question. Let the image BE the invitation.",
    "a one-line CONFESSION the viewer is invited to echo / pray — words put in the viewer's mouth, not a question asked of them.",
    "a quiet DECLARATIVE turn toward Jesus — a statement of what is now true of Christ for the viewer ('He is already standing over you'), landing as good news, not as a demand.",
    "an IMAGE-ANCHORED call that mirrors the hook so the short loops (hook -> climax -> close echo) — re-enter the opening picture transformed by the gospel.",
    "a quiet GRACE statement that resolves on Jesus, then one small concrete move toward Him — no command, no fear, no rhetorical question.",
    "a single honest QUESTION — USE SPARINGLY: only if the question carries NEW weight the body has not already implied, and is impossible to answer with a shrug. NEVER a bare 'Will you trust Him? / Will you come?' summary-question that could close any episode.",
]
_CONVICTION_ANGLES = [
    "expose the gap between admiring Jesus and trusting Him.",
    "let the thread's detail convict — the Spirit presses, the script only holds the mirror up.",
    "show grace arriving BEFORE the viewer can perform — the gospel pre-empts the bargain.",
    "name the self-rescue the viewer reaches for, then set Christ in its place.",
]


def _candidate_thread(thread: Thread | None, i: int) -> Thread | None:
    """Build a single-thread object from the i-th discovered candidate so each
    tournament draft chases a DIFFERENT true thread. Falls back to the chosen
    thread if there are not enough candidates."""
    if thread is None:
        return None
    cands = getattr(thread, "candidates", None) or []
    if not cands:
        return thread
    c = cands[i % len(cands)]
    return Thread(
        thread=c.thread, lever=c.lever, anchor_ref=c.anchor_ref,
        anchor_detail=c.anchor_detail, why_fresh=c.why_fresh,
        gospel_landing=c.gospel_landing, rationale="", candidates=[],
    )


def _variation_directive(i: int) -> str:
    hook = _HOOK_STRATEGIES[i % len(_HOOK_STRATEGIES)]
    cta = _CTA_STRATEGIES[i % len(_CTA_STRATEGIES)]
    conv = _CONVICTION_ANGLES[i % len(_CONVICTION_ANGLES)]
    return (
        f"VARIATION DIRECTIVE (candidate #{i + 1} — be DISTINCT from the obvious take "
        "and from any other candidate):\n"
        f"- HOOK STRATEGY: {hook}\n"
        f"- CONVICTION ANGLE: {conv}\n"
        f"- CTA STRATEGY: {cta}\n"
        "- Treat the series CTA pattern as LOOSE direction only — your CTA must grow "
        "from THIS thread and be unlike a stock devotional close. NEVER use 'before you "
        "scroll', 'ask honestly', 'so today', or any formula that would fit any episode.\n"
        "- Commit fully to this thread + these strategies; do not hedge toward the safe, "
        "predictable version. Freshness in the entry point and CTA; orthodoxy in the claim "
        "and the landing on Jesus."
    )


def generate_candidates(
    series: Series, episode: Episode, kjv_text: str | None,
    structure: Structure, notes: str, thread: Thread | None, n: int,
    log=print,
) -> list[tuple[Draft, Thread | None]]:
    """Generate n DIVERGENT drafts in parallel, each on a different discovered
    thread + a distinct hook/conviction/CTA strategy. Returns (draft, thread_used)
    pairs (the thread is needed by the judge)."""
    import concurrent.futures

    def _one(i: int) -> tuple[Draft, Thread | None] | None:
        cand_thread = _candidate_thread(thread, i)
        role = _generate_role(structure, _variation_directive(i))
        user = _episode_block(series, episode, kjv_text, notes) + _thread_block(cand_thread)
        try:
            return Draft.from_json(_extract_json(_call(role, user))), cand_thread
        except Exception as e:
            log(f"      ! candidate #{i + 1} failed: {e}")
            return None

    out: list[tuple[Draft, Thread | None]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(n, 6)) as ex:
        for r in ex.map(_one, range(n)):
            if r is not None:
                out.append(r)
    return out


def _judge_role() -> str:
    return (
        "YOU ARE THE STRUCTURE JUDGE for a 60-second gospel short. Several DIVERGENT "
        "candidate drafts of the SAME episode follow, each chasing a different thread + "
        "hook + CTA. Judge the WHOLE ARC, hook -> point -> proof -> conviction -> landing "
        "-> CTA, and pick the strongest as a STRUCTURE that lands on Jesus.\n\n"
        "Score each candidate (0-10) on:\n"
        "- ARC: does the hook earn the watch, and does each beat ESCALATE to the landing "
        "(not flat, not a list)?\n"
        "- FRESHNESS: is the entry point a real 'I never noticed that', not the topic "
        "auto-complete? Is the CTA specific to THIS thread and NOT a stock formula?\n"
        "- LANDING (weighted — a tired close kills a strong hook): does the LAST line do NEW "
        "work, or does it just restate the body? HEAVILY PENALISE a bare rhetorical "
        "'Will you trust Him? / Will you come?' summary-close, and any landing that would fit a "
        "DIFFERENT episode unchanged (portable = generic). Reward a close that ends on THIS "
        "thread's concrete image or a quiet declarative of grace. When grafting a CTA, prefer the "
        "candidate whose close is the LEAST heard-before, not merely the punchiest. ALSO penalise "
        "a GRACE-TRAP close (a verse-question turned onto the viewer that demands they PRODUCE the "
        "answer — it secretly preaches 'try harder to believe'; the answer must be framed as "
        "received, not achieved) and an ANACHRONISTIC close (a claim that imports later theology "
        "the scene has not reached, e.g. a pre-resurrection passage leaning on 'He is risen').\n"
        "- GRACE-ANCHORED CONVICTION: does it pierce as grace (no moralism, no gain/loss, "
        "no manufactured pressure)?\n"
        "- LANDS ON JESUS: does the close resolve on Christ / the gospel, not application?\n"
        "- ONE-THREAD INTEGRITY: does a single thread run hook -> CTA?\n"
        "- FAITHFUL: KJV verbatim, claim sound in context, no eisegesis for the sake of fresh.\n"
        "- FIVE QUESTIONS (heavily weighted): does it say ONE clear thing (no hook/body drift); "
        "is it SHOWN profoundly, not EXPLAINED (penalise lecture phrasing like 'Notice the order'); "
        "is it written FOR ONE named audience (not everyone); is the takeaway a CHANGE in how the "
        "viewer sees Christ, not a fact? Prefer the candidate that best satisfies these.\n"
        "- FIRST-HEARING CLARITY (heavily weighted — clarity beats cleverness): would a TIRED "
        "STRANGER with no Bible background get every beat on ONE hearing? HEAVILY PENALISE any "
        "candidate whose SPINE is a writerly conceit (geography trivia, grammar/pronoun gymnastics, "
        "original-language nuance, wordplay) rather than a felt truth, that needs prior Bible "
        "knowledge to follow, that leans on a logic-trick, or whose landing contradicts its thread. "
        "Between a clever-but-cold candidate and a plain-but-profound one, the plain one WINS.\n\n"
        "Then decide the WINNER (best total arc that also best answers the Five Questions). "
        "Build the BEST POSSIBLE short by grafting onto the winner's arc the strongest version "
        "of ANY beat from another candidate — not just the hook and landing. If candidate A wins "
        "but candidate C has a stronger CONVICTION (or point, or proof), graft C's conviction. For "
        "each of the five beats, name the candidate whose version is strongest; omit a beat only "
        "where the winner's own is already best. Put any prose-level instruction (a fix to apply, a "
        "line to cut, two beats to merge) in `synthesis_notes` — these ARE applied, so be concrete.\n\n"
        "Return ONLY a JSON object (optionally inside a ```json fence):\n"
        "{\n"
        '  "scores": [{"candidate": 1, "arc": 0, "freshness": 0, "conviction": 0, "lands_on_jesus": 0, "thread": 0, "faithful": 0, "five_questions": 0, "total": 0, "note": "one line"}, ...],\n'
        '  "ranking": [<candidate numbers, best first>],\n'
        '  "winner": <candidate number>,\n'
        '  "grafts": [{"beat": "hook|point|proof|conviction|landing", "from": <candidate number>}, ... — any beats worth taking from a NON-winner; [] if the winner is best throughout],\n'
        '  "synthesis_notes": "concrete fixes or merges to apply when building the final draft (for example: cut the lecture phrase in the proof; merge the grace line from candidate 3 into the conviction); empty string if none",\n'
        '  "rationale": "why the winner is the strongest arc that lands on Jesus, and what to graft"\n'
        "}\n"
        "No prose outside the JSON object."
    )


def judge_drafts(
    series: Series, episode: Episode, kjv_text: str | None,
    structure: Structure, candidates: list[tuple[Draft, Thread | None]],
) -> dict:
    blocks = []
    for i, (d, th) in enumerate(candidates, 1):
        beats = "\n".join(f"  [{b.id}] {b.text}" for b in d.beats)
        blocks.append(
            f"=== CANDIDATE #{i} (thread: {th.thread if th else '(none)'}) ===\n"
            f"TITLE: {d.title}\nHOOK TYPE: {d.hook_type}\nSPEAKERS: {d.speakers}\n{beats}"
        )
    user = (
        _episode_block(series, episode, kjv_text, "")
        + "\n\n" + "\n\n".join(blocks)
    )
    reply = _call(_judge_role(), user, model=config.REVIEW_MODEL)
    return _extract_json(reply)


def _collect_grafts(judge: dict, winner_idx: int, candidates: list[tuple[Draft, Thread | None]]) -> list[str]:
    """Build the per-beat graft instructions from the judge verdict. Supports the
    general `grafts` list ([{beat, from}], any beat) AND the legacy
    graft_hook_from / graft_cta_from fields. A graft from the winner itself, or an
    out-of-range candidate, is ignored."""
    n = len(candidates)
    _LABEL = {"hook": "HOOK", "point": "POINT", "proof": "PROOF",
              "conviction": "CONVICTION", "landing": "LANDING/CTA"}
    pairs: list[tuple[str, int]] = []  # (beat_id, candidate_number)
    for g in (judge.get("grafts") or []):
        if not isinstance(g, dict):
            continue
        beat = str(g.get("beat", "")).strip().lower()
        frm = g.get("from")
        if beat in _LABEL and isinstance(frm, int):
            pairs.append((beat, frm))
    # legacy fields
    if isinstance(judge.get("graft_hook_from"), int):
        pairs.append(("hook", judge["graft_hook_from"]))
    if isinstance(judge.get("graft_cta_from"), int):
        pairs.append(("landing", judge["graft_cta_from"]))

    bits: list[str] = []
    seen: set[str] = set()
    for beat, num in pairs:
        if beat in seen or num == winner_idx or not (1 <= num <= n):
            continue  # winner's own beat is best, or invalid -> skip
        cand = candidates[num - 1][0]
        match = next((b.text for b in cand.beats if b.id == beat), None)
        if not match:
            continue
        seen.add(beat)
        bits.append(f"STRONGER {_LABEL[beat]} to adopt (from candidate #{num}):\n{match}")
    return bits


def synthesize_draft(
    series: Series, episode: Episode, kjv_text: str | None,
    structure: Structure, thread: Thread | None,
    winner: Draft, candidates: list[tuple[Draft, Thread | None]], judge: dict,
    winner_idx: int = 0,
) -> Draft:
    """One pass: keep the winner's arc, graft the strongest version of ANY beat the
    judge flagged from other candidates, and apply the judge's synthesis_notes.
    Returns the winner unchanged only when there is nothing to graft AND no notes."""
    graft_bits = _collect_grafts(judge, winner_idx, candidates)
    notes = str(judge.get("synthesis_notes", "")).strip()
    if not graft_bits and not notes:
        return winner

    winner_beats = "\n".join(f"[{b.id}] {b.text}" for b in winner.beats)
    role = (
        "YOUR TASK: produce the FINAL 60-second draft. Start from the WINNING draft's "
        "arc and thread (below). Graft in the stronger beats shown from other candidates "
        "AND apply the synthesis notes — adapt everything so it fits the winner's thread "
        "and voice; do not just paste. Keep ONE thread hook -> CTA, KJV verbatim (including "
        "terminal punctuation), grace-anchored conviction, the landing on Jesus, and the "
        "structure beat ids exactly.\n\n"
        f"{render_structure(structure)}\n\n"
        f"Total target: {config.TARGET_WORDS_MIN}-{config.TARGET_WORDS_MAX} words.\n"
        "Return ONLY a JSON object with the beat ids "
        f"{structure.beat_ids}:\n{_json_contract(structure)}\nNo prose outside the JSON."
    )
    graft_md = ("\n\n=== GRAFT THESE BEATS ===\n" + "\n\n".join(graft_bits)) if graft_bits else ""
    notes_md = (f"\n\n=== SYNTHESIS NOTES (apply these) ===\n{notes}") if notes else ""
    user = (
        _episode_block(series, episode, kjv_text, "")
        + _thread_block(thread)
        + f"\n\n=== WINNING DRAFT (keep this arc) ===\nTITLE: {winner.title}\n{winner_beats}"
        + graft_md + notes_md
    )
    try:
        return Draft.from_json(_extract_json(_call(role, user)))
    except Exception:
        return winner


def generate_best(
    series: Series, episode: Episode, kjv_text: str | None,
    structure: Structure, notes: str = "",
    thread: Thread | None = None, n: int = 4, synthesize: bool = True,
    log=print,
) -> Draft:
    """Tournament generation: N divergent drafts -> judge the arc -> synthesize the
    winner + graft. Falls back to single generate() if the tournament yields nothing."""
    log(f"      [tournament] generating {n} divergent candidates...")
    candidates = generate_candidates(series, episode, kjv_text, structure, notes, thread, n, log=log)
    if not candidates:
        log("      [tournament] no candidates produced — falling back to single draft.")
        return generate(series, episode, kjv_text, structure, notes, thread)
    if len(candidates) == 1:
        return candidates[0][0]
    judge = judge_drafts(series, episode, kjv_text, structure, candidates)
    winner_no = judge.get("winner")
    if not isinstance(winner_no, int) or not (1 <= winner_no <= len(candidates)):
        winner_no = (judge.get("ranking") or [1])[0]
    winner = candidates[winner_no - 1][0]
    won_thread = candidates[winner_no - 1][1]
    grafts = judge.get("grafts") or []
    graft_summary = ", ".join(
        f"{g.get('beat')}<-{g.get('from')}" for g in grafts if isinstance(g, dict)
    ) or f"hook<-{judge.get('graft_hook_from')} cta<-{judge.get('graft_cta_from')}"
    log(f"      [tournament] winner = candidate #{winner_no} "
        f"(\"{winner.hook[:50]}...\")  grafts: {graft_summary}")
    if synthesize:
        return synthesize_draft(series, episode, kjv_text, structure, won_thread,
                                winner, candidates, judge, winner_idx=winner_no)
    return winner


# --------------------------------------------------------------------------
# Stage 2 — red-team review (5-agent panel + 4-pillar + structure gates)
# --------------------------------------------------------------------------
def _review_role(structure: Structure) -> str:
    budgets = "; ".join(
        f"{b.name} ~{b.word_guide}w ({b.start}-{b.end}s)" for b in structure.beats
    )
    return f"""\
YOUR TASK: red-team the draft against the charter, the series guardrails, the
verified KJV text, AND the wider pericope provided. Be a genuine critic — a panel
that returns all STRONG verdicts on a first draft is not doing its job. Quote
the offending line in every note.

6-agent panel. Each: verdict (STRONG | CAUTION | REVISION NEEDED) + one concrete note:
1. The Scroll-Stopper — is the hook impossible to scroll past, and immediately relevant, or generic?
2. The Theologian — KJV verbatim? reference correct? claim SOUND IN CONTEXT (use the wider pericope)? no proof-texting / over-claiming? series guardrails honoured? IF a thread was intended, is the freshness exegetically honest (no contrarian eisegesis, no doctrinal hot take)?
3. The Skeptic (unchurched viewer) — any manipulation, gain/loss selling, fear, or manufactured pressure? would they stay in the room?
4. The Evangelist — does it pierce (conviction, not information) and land the response on JESUS by grace?
5. The Editor — structure conformance, word economy, every beat earns its place.
6. The Jaded Scroller — they have seen 10,000 Bible shorts. Could they predict every line from the title? Are the openers/framings on the cliché blocklist? Is this the topic auto-complete take (e.g. prodigal = "son came home"), or a real "I never noticed that"? IF a thread was intended, is it carried end-to-end (hook -> proof -> landing) or abandoned halfway? PAIRED with the Theologian — freshness without honesty is a fail, and so is honesty without surprise.

Quality gates — each PASS | CONDITIONAL | FAIL, with evidence quoted from the draft
and (if not PASS) a specific fix:
- G1 Biblical Accuracy: the quoted verse matches the verified KJV verbatim — EXACT wording AND exact terminal punctuation (a quote ending '!' in the KJV must not become '?' or '.'); the reference is correct; the Point/claim is sound when read in the wider pericope (no proof-texting, no over-claim). FAIL (not CONDITIONAL) on any statement that is exegetically FALSE or that a literate skeptic could disprove from the text (e.g. a strawman rebuttal, an over-tidy historical claim) — a false aside is worse than no aside. ALSO FAIL a SCENE-SCOPE OVERCLAIM: a claim that asserts a divine attribute or act the SCENE only implies (e.g. 'the One who made it' / Creator where the text shows only authority/lordship; a pre-resurrection text leaning on 'He is risen / the empty tomb'). True in the wider canon is NOT enough — the line must be airtight to what THIS pericope establishes; tighten the wording to the scene.
- G2 Relevance: the hook names a real, present human ache in the first beat and the short stays relevant to it.
- G3 Conviction: it creates holy tension and pierces — NOT mere information — AND is grace-anchored (FAIL on any gain/loss framing, fear-selling, or manufactured pressure). FAIL on SHAMING — a line that indicts the person in the text OR the viewer for a performance failure ('Only His own people panicked', 'if you had more faith', 'you should have known') is LAW, not grace; the pierce must expose the heart and point to grace (He acts/loves first), never assign blame for not being good/brave/faithful enough.
- G4 CTA Lands with Jesus: the close invites a response specifically to Jesus, by grace; not coercive, not cheesy. FAIL a GRACE-TRAP close — if the landing turns the verse's question onto the viewer, the ANSWER must be framed as something God GIVES (the Father reveals it / puts it on your lips / opens your eyes), never something the viewer must PRODUCE; a bare 'so, what's your answer?' secretly preaches 'try harder to believe' and snaps the grace anchor. The landing must also obey scene-scope (no imported doctrine) and do NEW work (no tired/portable closer).
- G5 Structure Conformance: all beats present in order ({structure.beat_ids}); each roughly within budget ({budgets}); the proof beat carries the scripture quote; total ~{config.TARGET_WORDS_MIN}-{config.TARGET_WORDS_MAX} words.
- G6 Craft: standalone (carries meaning muted); plain prose; clean pacing.
- G7 Freshness: the draft surfaces a non-obvious TRUE detail (the intended thread, if provided, carried hook -> proof -> landing) and avoids the cliché blocklist + the obvious topic auto-complete. FAIL when the draft is BOTH generic AND exegetically uninteresting — clichéd openers, banned framings/CTA tropes, or the headline take with no fresh angle. ALSO FAIL when a "fresh" reading is exegetically dishonest (Theologian veto): contrarian eisegesis fails this gate even if it surprises. PASS when the thread is carried end-to-end and stays honest.
- G8 The Five Questions (binding — see charter "THE FIVE QUESTIONS"): (1) ONE clear thing said, with NO drift between the hook's promise and the body's payoff; (2) it is SHOWN profoundly, not explained — FAIL on lecture phrasing ("Notice the order", "This teaches us", "The point is", or any beat that narrates the theology instead of making it felt); (3) the conviction beat actually PIERCES (feeling, not facts) and the series signature is present AND EXPLICIT — for a turn-onto-the-viewer series (QJA, Jesus-in-OT), the LANDING must aim the question/claim directly at YOU; FAIL a fully third-person close ('they stared at...', 'the disciples saw...') that only IMPLIES the turn instead of making it; (4) the script is clearly FOR ONE named audience (doubter / performer / admirer-who-won't-bow / grieving / ashamed) — FAIL if it is written for no one in particular; ALSO FAIL if the audience descriptor LEAKS into the spoken script as a meta-line (e.g. 'This one's for the person who…', 'If you're someone who…') — the audience is a planning answer, spoken TO directly, never named aloud; (5) the takeaway is a CHANGE in how the viewer sees Christ + a response to Jesus, not merely a fact learned. ALSO: if the short opens problem-first, the turn + landing MUST go to who Christ is — FAIL any 'and so your problem is solved / anxiety lifts / life improves' self-help payoff (the ache is only the doorway). (6) THE FIRST-HEARING TEST (clarity beats cleverness): would a TIRED STRANGER with ZERO Bible background get each beat on ONE hearing at speed? FAIL if the SPINE is a writerly conceit rather than a felt truth — geography trivia, grammar/word-order/pronoun gymnastics, original-language nuance, or wordplay carrying the point instead of merely seasoning it (test: state the beat plainly in 6 words — if nothing survives, the conceit was the point → FAIL); FAIL if a beat only makes sense to someone who already knows the setting/characters/back-story; FAIL on any logic-trick/smuggled syllogism the viewer must swallow ('only one kind of man would…'); FAIL if the landing CONTRADICTS the thread (e.g. body says grace needs no answer, close demands one). Quote the offending beat. FAIL if two or more of these (1)-(6) are unmet, or if (1) or (6) is unmet on its own.

Verdict rules:
- overall = LOCKED when NO gate is FAIL. CONDITIONAL or CAUTION notes are fine and
  expected — they are advisory craft notes, not blockers, so award LOCKED with them.
- overall = REVISE if any gate is FAIL but the concept is sound.
- overall = REWORK if the concept itself is broken.

Return ONLY a JSON object (optionally inside a ```json fence):
{{
  "panel": [{{"agent": "Scroll-Stopper", "verdict": "...", "note": "..."}}, ... 6 agents],
  "gates": [{{"gate": "G1 Biblical Accuracy", "verdict": "PASS|CONDITIONAL|FAIL", "evidence": "...", "fix": "..."}}, ... 8 gates (G1..G8)],
  "overall": "LOCKED | REVISE | REWORK",
  "priority_fixes": ["the most important fix first", "..."]
}}
No prose outside the JSON object."""


def _apply_kjv_gate(rev: Review, draft: Draft, passage: str | None) -> Review:
    """Deterministic KJV-verbatim override of G1 (calibration proposal #1). A
    'punctuation' mismatch (body matches, edge punctuation differs) forces G1 FAIL;
    a 'wording' near-miss downgrades G1 to at least CONDITIONAL. The LLM never sees
    this — it is a string compare the review kept missing."""
    full = "\n".join(b.text for b in draft.beats)
    issues = kjv_check.verbatim_mismatches(full, passage)
    if not issues:
        return rev
    hard = any(i["kind"] == "punctuation" for i in issues)
    summary = kjv_check.summarize(issues)
    fix = f"KJV not verbatim — fix to match the pericope exactly: {summary}"
    new_gates = []
    replaced = False
    for g in rev.gates:
        if g.gate.upper().startswith("G1"):
            replaced = True
            verdict = "FAIL" if hard else ("CONDITIONAL" if g.verdict.upper() == "PASS" else g.verdict)
            new_gates.append(GateResult(gate=g.gate, verdict=verdict,
                                        evidence=(g.evidence + " | DETERMINISTIC KJV CHECK: " + summary).strip(" |"),
                                        fix=(fix if g.verdict.upper() != "FAIL" else g.fix)))
        else:
            new_gates.append(g)
    if not replaced:
        new_gates.insert(0, GateResult(gate="G1 Biblical Accuracy",
                                       verdict="FAIL" if hard else "CONDITIONAL",
                                       evidence="DETERMINISTIC KJV CHECK: " + summary, fix=fix))
    overall = "REVISE" if (hard and rev.overall.upper() == "LOCKED") else rev.overall
    return Review(panel=rev.panel, gates=new_gates, overall=overall,
                  priority_fixes=([fix] + list(rev.priority_fixes)) if hard else list(rev.priority_fixes))


def review(
    series: Series, episode: Episode, draft: Draft,
    kjv_text: str | None, passage: str | None, structure: Structure,
    thread: Thread | None = None,
) -> Review:
    beats_rendered = "\n".join(
        f"[{b.id}] {b.text}" for b in draft.beats
    )
    passage_block = (
        f"\nWIDER PERICOPE (source of truth for in-context accuracy):\n{passage}\n"
        if passage else ""
    )
    user = (
        _episode_block(series, episode, kjv_text, "")
        + passage_block
        + _thread_review_block(thread)
        + "\n\n=== DRAFT UNDER REVIEW ===\n"
        + f"TITLE: {draft.title}\n"
        + f"HOOK TYPE: {draft.hook_type}\n"
        + f"WORD COUNT: {draft.word_count}\n"
        + f"BEAT IDS PRESENT: {draft.beat_ids}\n"
        + f"SCRIPTURE REFERENCE CLAIMED: {draft.scripture_reference}\n"
        + f"SCRIPTURE QUOTED: {draft.scripture_quoted}\n\n"
        + "NARRATION (by beat):\n"
        + beats_rendered
    )
    rev = Review.from_json(_extract_json(_call(_review_role(structure), user)))
    return _apply_kjv_gate(rev, draft, passage)


# --------------------------------------------------------------------------
# Stage 2b — INDEPENDENT red-team audit (standard practice, always run)
# --------------------------------------------------------------------------
_INDEPENDENT_PREAMBLE = """\
You are an INDEPENDENT red-team auditor brought in from outside the production
team. You did not write this and you did not run the internal review. Assume the
writer AND the internal review may be biased, over-confident, or have missed
things. Your job is to verify everything from scratch and to be hard to please:
- Do NOT give the benefit of the doubt. If something is unproven, it FAILs.
- The verified KJV text and the surrounding context are the source of truth for
  every scriptural claim — check the quote and the interpretation against them.
- Hunt specifically for: misquoted/altered scripture, a claim the verse does not
  actually support in context, manipulation or fear/gain-loss selling, a CTA that
  drifts from Jesus to self-help, and structure beats that are missing or bloated.
- Surface every real weakness as a CAUTION panel note or a CONDITIONAL gate; reserve
  a FAIL gate for something that genuinely falls short of the standard. Award LOCKED
  when no gate FAILs — a clean bill of health is allowed, but only after you have
  honestly tried to break it.

"""


def independent_review(
    series: Series, episode: Episode, draft: Draft,
    kjv_text: str | None, passage: str | None, structure: Structure,
    thread: Thread | None = None,
) -> Review:
    """A fresh, hostile, model-independent audit of the FINAL draft. Authoritative."""
    beats_rendered = "\n".join(f"[{b.id}] {b.text}" for b in draft.beats)
    passage_block = (
        f"\nWIDER PERICOPE (source of truth for in-context accuracy):\n{passage}\n"
        if passage else ""
    )
    user = (
        _episode_block(series, episode, kjv_text, "")
        + passage_block
        + _thread_review_block(thread)
        + "\n\n=== DRAFT UNDER INDEPENDENT AUDIT ===\n"
        + f"TITLE: {draft.title}\n"
        + f"BEAT IDS PRESENT: {draft.beat_ids}\n"
        + f"WORD COUNT: {draft.word_count}\n"
        + f"SCRIPTURE REFERENCE CLAIMED: {draft.scripture_reference}\n"
        + f"SCRIPTURE QUOTED: {draft.scripture_quoted}\n\n"
        + "NARRATION (by beat):\n"
        + beats_rendered
    )
    role = _INDEPENDENT_PREAMBLE + _review_role(structure)
    rev = Review.from_json(_extract_json(_call(role, user, model=config.REVIEW_MODEL)))
    return _apply_kjv_gate(rev, draft, passage)


# --------------------------------------------------------------------------
# Stage 3 — revise
# --------------------------------------------------------------------------
def revise(
    series: Series,
    episode: Episode,
    draft: Draft,
    review_result: Review,
    kjv_text: str | None,
    structure: Structure,
    thread: Thread | None = None,
) -> Draft:
    panel = "\n".join(f"- {a.agent}: {a.verdict} — {a.note}" for a in review_result.panel)
    gates = "\n".join(
        f"- {g.gate}: {g.verdict}"
        + (f" — FIX: {g.fix}" if g.verdict.upper() != "PASS" and g.fix else "")
        for g in review_result.gates
    )
    fixes = "\n".join(f"- {f}" for f in review_result.priority_fixes)
    beats_rendered = "\n".join(f"[{b.id}] {b.text}" for b in draft.beats)
    role = (
        "YOUR TASK: revise the draft to fix every issue the review raised, especially\n"
        "the FAIL gates and the priority fixes. Preserve what works. Keep the charter\n"
        "rules, the series guardrails, grace-anchored conviction, and the STRUCTURE.\n"
        "If a THREAD block follows, keep that thread as the spine — open the hook on it,\n"
        "prove it in the proof beat, mirror it in the landing. Do not swap threads to\n"
        "answer freshness/cliché feedback; reshape the lines to carry the same thread\n"
        "more cleanly.\n\n"
        f"{render_structure(structure)}\n\n"
        "Return ONLY a JSON object with the SAME keys as the original draft (same beat "
        f"ids {structure.beat_ids}, in order):\n"
        f"{_json_contract(structure)}\n"
        "No prose outside the JSON object."
    )
    user = (
        _episode_block(series, episode, kjv_text, "")
        + _thread_block(thread)
        + "\n\n=== CURRENT DRAFT (by beat) ===\n"
        + beats_rendered
        + "\n\n=== REVIEW PANEL ===\n"
        + panel
        + "\n\n=== GATES ===\n"
        + gates
        + "\n\n=== PRIORITY FIXES ===\n"
        + fixes
    )
    return Draft.from_json(_extract_json(_call(role, user)))
