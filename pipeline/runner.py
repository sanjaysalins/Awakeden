"""Orchestrate one narration: generate -> review -> revise (loop) -> handoff."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import config
from pipeline import engine, handoff, scripture, structures
from pipeline.models import Draft, Review, Thread
from pipeline.series import Episode, Series
from pipeline.structures import Structure


@dataclass
class RunResult:
    draft: Draft
    review: Review            # authoritative verdict (independent audit if enabled)
    self_review: Review       # the internal review that drove revisions
    kjv_text: str | None
    folder: Path
    unknown_speakers: list[str]
    revisions_used: int
    structure: Structure
    thread: Thread | None = None  # the chosen freshness thread (if THREAD_DISCOVERY on)


def _log_conformance(draft: Draft, structure: Structure, log) -> None:
    log(f'      "{draft.hook[:80]}"  ({draft.word_count} words)')
    if draft.beat_ids != structure.beat_ids:
        log(f"      ! beat mismatch: got {draft.beat_ids}, expected {structure.beat_ids}")


def create_narration(
    series: Series,
    episode: Episode,
    notes: str = "",
    run_audio: bool = True,
    log=print,
) -> RunResult:
    structure = structures.get_structure()
    log(f"\n=== {series.name} — {episode.title} ({episode.primary_ref}) ===")
    log(f"    structure: {structure.name}")

    log("[1/6] Fetching exact KJV text + wider pericope...")
    kjv = scripture.fetch_kjv(episode.primary_ref)
    passage = scripture.fetch_kjv_passage(episode.primary_ref, window=config.PASSAGE_WINDOW)
    log("      " + (f'KJV "{kjv[:70]}..."' if kjv else "NOT verified (offline?) — flagged for review"))
    if passage:
        log(f"      pericope: {len(passage.splitlines())} verses (window=±{config.PASSAGE_WINDOW})")
    else:
        log("      pericope: NOT fetched — review will run without wider context.")

    thread: Thread | None = None
    if config.THREAD_DISCOVERY:
        log("[2/6] Discovering thread (4 levers, exegetically honest)...")
        thread = engine.discover_thread(series, episode, kjv, passage, notes)
        if thread.is_empty:
            log("      ! thread discovery returned empty — proceeding without a thread.")
            thread = None
        else:
            log(f"      THREAD: {thread.thread}  [{thread.lever}]")
            log(f"      anchor: {thread.anchor_ref} — {thread.anchor_detail[:80]}")
            log(f"      candidates considered: {len(thread.candidates)}")
    else:
        log("[2/6] Thread discovery disabled (THREAD_DISCOVERY=0) — skipping.")

    if config.ENGINE_TOURNAMENT:
        log(f"[3/6] Generating draft — TOURNAMENT ({config.ENGINE_CANDIDATES} divergent "
            "candidates -> judge arc -> synthesize)...")
        draft = engine.generate_best(
            series, episode, kjv, structure, notes, thread=thread,
            n=config.ENGINE_CANDIDATES, synthesize=config.ENGINE_SYNTHESIZE, log=log,
        )
    else:
        log("[3/6] Generating draft (Opus 4.7)...")
        draft = engine.generate(series, episode, kjv, structure, notes, thread=thread)
    _log_conformance(draft, structure, log)

    log("[4/6] Self-review (4 pillars + structure + craft + freshness)...")
    self_review = engine.review(series, episode, draft, kjv, passage, structure, thread=thread)
    log(f"      {self_review.overall}  ({len(self_review.failed_gates)} FAIL gate(s))")

    revisions = 0
    while self_review.failed_gates and revisions < config.MAX_REVISIONS:
        revisions += 1
        log(f"      revising (pass {revisions}/{config.MAX_REVISIONS})...")
        draft = engine.revise(series, episode, draft, self_review, kjv, structure, thread=thread)
        self_review = engine.review(series, episode, draft, kjv, passage, structure, thread=thread)
        log(f"      {self_review.overall}  ({len(self_review.failed_gates)} FAIL gate(s))")

    # Independent red-team audit — STANDARD PRACTICE, always run. Its verdict is
    # authoritative; we never ship on our own self-review alone. The loop stops on
    # zero FAIL gates (a hostile auditor rarely awards a clean LOCKED).
    review = self_review
    if config.INDEPENDENT_REVIEW:
        log("[5/6] INDEPENDENT red-team audit (authoritative)...")
        review = engine.independent_review(series, episode, draft, kjv, passage, structure, thread=thread)
        log(f"      independent: {review.overall}  ({len(review.failed_gates)} FAIL gate(s))")
        while review.failed_gates and revisions < config.MAX_REVISIONS:
            revisions += 1
            log(f"      revising from independent audit (pass {revisions}/{config.MAX_REVISIONS})...")
            draft = engine.revise(series, episode, draft, review, kjv, structure, thread=thread)
            review = engine.independent_review(series, episode, draft, kjv, passage, structure, thread=thread)
            log(f"      independent: {review.overall}  ({len(review.failed_gates)} FAIL gate(s))")
        if review.failed_gates:
            log("      ! independent audit still has FAIL gate(s) - see review report before publishing.")

    log("[6/6] Writing narration folder...")
    folder, unknown = handoff.write_narration_folder(
        series, episode, draft, review, kjv, structure,
        self_review=self_review, thread=thread,
    )
    log(f"      {folder}")
    if unknown:
        log(f"      NOTE: no voice mapping for speaker(s): {', '.join(unknown)} "
            f"(they will read as the narrator). Add them to config.VOICE_MAP.")

    if run_audio:
        mode = (
            f"Shorts ~{config.SHORTS_TARGET_SECONDS:.0f}s"
            if config.SHORTS_MODE
            else "natural-length"
        )
        log(f"\n--- Audio pipeline ({mode}) ---")
        code = handoff.run_audio_pipeline(folder)
        log(f"--- Audio pipeline exit code: {code} ---")
    else:
        log("\n(audio pipeline skipped — run it later with:)")
        if config.SHORTS_MODE:
            log(f'  python "{config.NARRATION_PIPELINE_SCRIPT}" "{folder}" --stage verify')
            log(f'  python "{config.NARRATION_PIPELINE_SCRIPT}" "{folder}" --stage tag')
            log(f'  python "{config.NARRATION_PIPELINE_SCRIPT}" "{folder}" --stage audit')
            log(f'  python "{config.PER_TURN_SYNTH_SCRIPT}" "{folder}" '
                f"--target {config.SHORTS_TARGET_SECONDS:.0f} "
                f"--pre-quote-pause {config.SHORTS_PRE_QUOTE_PAUSE} "
                f"--stability {config.SHORTS_STABILITY}")
        else:
            log(f'  python "{config.NARRATION_PIPELINE_SCRIPT}" "{folder}"')

    return RunResult(
        draft=draft,
        review=review,
        self_review=self_review,
        kjv_text=kjv,
        folder=folder,
        unknown_speakers=unknown,
        revisions_used=revisions,
        structure=structure,
        thread=thread,
    )
