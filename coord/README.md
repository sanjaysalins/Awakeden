# coord/ - two lanes, one coordinator

Lanes: **swirls** (Swirls of Life) and **comic** (Living Comic). Open ONE Claude session per lane,
plus one coordinator session. All three work in this same folder.

## Rules (all sessions)
1. Start with: `.venv\Scripts\python.exe coord/coord.py status`
2. Claim a piece before you touch it: `coord.py claim <piece> <lane> <session-name>`
3. Only edit inside your lane's folders. Check any doubtful path: `coord.py check <lane> <path>`
4. NEVER edit coordinator-only files (see BOARD.json): RESUME.md, STATE.md, tracker, pipeline/, publish tools, sound_library, _brand.
   Put what you learned in `coord.py note <lane> "text"` instead.
5. Do NOT run `git add/commit/push`. Only the coordinator commits (one shared git index).
6. Spend: nothing paid without a quoted price and the owner's own yes. Every paid call gets a row in data/spend_ledger.jsonl with "lane".
7. Swirls = OpenArt (needs a live session to service the bridge). Comic = Higgsfield. Do not cross providers.
8. Done? `coord.py ready <piece> <lane> <final.mp4>` and stop. The coordinator checks and ships it.

## Coordinator only
- Reads lane notes, copies them into RESUME.md/STATE.md.
- Runs: pipeline/thumbnails.py, cli_publish.py, release_check.py, build_upload_tracker.py.
- Owns the single combined spend/credit view.
- Commits.

## Starting prompts (paste as the first message in each session)
- `coord/LANE_SWIRLS.md`   - Swirls lane
- `coord/LANE_COMIC.md`    - Comic lane
- `coord/COORDINATOR.md`   - coordinator
