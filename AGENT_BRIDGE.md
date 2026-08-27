# AGENT_BRIDGE.md — agent-mode (run the engine on the Max sub, not the metered API)

`LLM_PROVIDER=agent` (the **default**) routes every engine LLM call to the in-chat
agent (Claude Code on the Max subscription) through a file bridge instead of the
metered Anthropic API. Zero API spend; no API key needed for the LLM steps.

`LLM_PROVIDER=api` reverts to the classic metered path (set this for unattended /
cron runs where no agent is in the loop to service the bridge).

## What it covers

- **Text** — all of `engine._call` (thread discovery, the draft tournament,
  judge, synthesize, review, independent audit, revise, scene planning,
  assembly planning). One funnel.
- **Vision** — both image audits: `visual_render._vision_call` (per-image content
  audit) and `assembly_render._verify_slot_vision` (per-slot doctrinal verify).
  I view the image with the Read tool — strictly better than the SDK audit.
- **Kling cut-planner** — `PythonProject1/jesus/image_to_kling.py` Stage A (Vision
  cut-plan director) + Stage A.5 (audit), via the same bridge. The bridge module
  is imported by path (`JITB_BRIDGE_PATH`) so it works under PythonProject1's venv;
  the orchestrator/handoff stamp the agent-mode env into every subprocess call
  (`config.inject_agent_env`).

NOT covered: ElevenLabs audio (no Anthropic), Kling Stage B render (not an LLM),
Higgsfield image gen.

## How it works

The engine writes a request file, prints a loud banner, then **blocks**, polling
for the reply. The agent writes the reply; the engine reads it and continues.

```
.agent_bridge/
  requests/<id>.request.md   <- engine writes the full prompt (human-readable)
  images/<id>.{png,jpg}       <- vision calls: the image to view with Read
  responses/<id>.txt          <- the AGENT writes the raw model reply here
  shared_context.md           <- constitution + series library (written once/run)
  archive/                    <- serviced request+reply pairs move here
```

## Operating pattern (the loop)

1. **Run the CLI in the background** (so it can block while you service it):
   ```
   # in chat: Bash run_in_background=true
   .venv\Scripts\python.exe cli.py --no-audio          # or cli_visual / cli_assemble / cli_pipeline
   ```
   (Subprocess Vision/Kling calls have `capture_output=True`, so their banners are
   not live — but the request FILES still appear. Watch the dir, not stdout.)
2. **Watch `.agent_bridge/requests/`** for a new `*.request.md`.
3. **Read the request** (and, for vision, Read the referenced image).
4. **Reason as the model would** and **Write `.agent_bridge/responses/<id>.txt`**
   containing ONLY the raw reply the engine expects (usually one JSON object,
   optionally in a ```json fence — no extra prose).
5. The engine unblocks, archives the pair, continues. Repeat until the background
   process exits. Parallel calls (e.g. the draft tournament's N candidates) produce
   N requests at once — answer all of them.

## Knobs (env)

| var | default | meaning |
|---|---|---|
| `LLM_PROVIDER` | `agent` | `agent` (bridge) or `api` (metered) |
| `AGENT_BRIDGE_DIR` | `<repo>/.agent_bridge` | bridge directory |
| `AGENT_BRIDGE_TIMEOUT` | `3600` | seconds the engine waits per call before erroring |
| `AGENT_BRIDGE_POLL` | `1.5` | poll interval seconds |
| `JITB_BRIDGE_PATH` | `<repo>/pipeline` | where image_to_kling.py imports the bridge from |

## Gotcha

If a run hangs, it is almost always an **unserviced request** — check
`.agent_bridge/requests/`. To kill the wait, write the reply, or stop the process
and re-run with `LLM_PROVIDER=api`.

## Image / video generation (OpenArt) — Swirls-of-Life pipeline only

Separate channel, separate reason. OpenArt (`poc_living_water_ink_style_test/`'s
image/video provider, replacing Higgsfield as of 2026-08-27 after a real-cost
bake-off, `openart/bakeoff_queen/_BAKEOFF_REVIEW.html`) has **no REST API or API
key at all** — it's MCP-only, OAuth ("no keys to create, rotate, or leak"). So
unlike `hf.exe` (a real CLI binary any script can subprocess), a standalone
script literally cannot call OpenArt itself. `test_the_cross/openart_bridge.py`
is the client half of the same file-bridge trick as above, on its own
directories so it can't collide with the text servicer:

```
.agent_bridge/
  gen_requests/<id>.request.json    <- swirls_page.py writes prompt+params here
  gen_responses/<id>.response.json  <- the AGENT writes the result here
  gen_archive/                       <- serviced pairs move here
```

**Request schema** (`kind: "still"`):
`{id, kind, model: "nano-banana-pro", mode: "text2image"|"image2image", prompt,
aspect_ratio, resolution: "2K", refs: [{path, subject}], out_path}`

**Request schema** (`kind: "anim"`):
`{id, kind, model: "kling-3-omni", mode: "image2video", prompt,
start_image_path, duration, resolution: "std"|"pro"|"4k", generate_sound: false,
out_path}`

**Response schema**: `{status: "ok"|"error", out_path, credits_spent, usd_est,
error?}`. `status != "ok"` (or a timeout) is terminal — `openart_bridge.py`
raises, and `swirls_page.py` does NOT fall back to Higgsfield automatically.
That is a deliberate, locked policy (user instruction, 2026-08-27): falling
back requires a human decision. To use HF for a run, set
`SWIRLS_GEN_PROVIDER=hf` yourself first.

**Servicing steps** (same loop as above — run the episode script in the
background, watch `.agent_bridge/gen_requests/`, but each file needs real MCP
tool calls, not a text reply):

1. Read the request JSON.
2. For each entry in `refs` (stills only): `openart_upload_sign` (mediaType
   image, size/contentType from the local file) → PUT the bytes to `signURL`
   with curl → build `{type:"image", id, url, label: subject}`.
3. Call `mcp__openart__openart_generate_image` (stills) or
   `..._generate_video` (anims) with the request's model/mode/prompt/params
   (`visualReferences` for stills with refs, `startFrame` for anims — use the
   uploaded/generation resource's own `{type, id, url, label}` object, not a
   bare URL).
4. `openart_creation_wait` until `COMPLETED` (may need several calls back to
   back — video often outlasts one wait window).
5. Download the result URL to the request's `out_path` (curl -sL -o).
6. Get a cost estimate via `openart_model_cost` for the same config (or diff
   `openart_account_get` before/after for the real figure) and write
   `gen_responses/<id>.response.json`: `{status:"ok", out_path, credits_spent,
   usd_est}`. On any failure: `{status:"error", error: "<what happened>"}` —
   never invent a fallback yourself.
7. Also append an entry to `data/spend_ledger.jsonl` (provider: "openart",
   same shape as existing HF entries) so `/spend` and `/cost` keep working —
   the script itself has no visibility into OpenArt credits, only the servicer
   does.

**Knobs (env)**: `SWIRLS_GEN_PROVIDER` (`openart` default | `hf`),
`SWIRLS_ANIM_RESOLUTION` (`pro` default, matches HF's quality bar | `std` for
~1.8x cheaper, bake-off-validated | `4k`), `OPENART_BRIDGE_TIMEOUT` (3600s
default), `OPENART_BRIDGE_POLL` (3s default).

## Watcher (don't lose track of a stuck request)

`watcher_service.py` (start once via `start_watcher.vbs`, keeps running in the
background with zero visible window — not even a flash, unlike a `.bat` launcher) polls `.agent_bridge/requests/` and flags an
unanswered request in the Claude Code **status line** once it's been waiting a
while — kept deliberately short so it doesn't get cut off in a narrow terminal:
dim "⏳ bridge 45s" at 30s, red "🚨 bridge 6m" at 5min (needs you now), red
"☠ bridge 5.9d" past 1hr (the engine has already given up and crashed — this
one's just debris, go delete/archive the request file). A count suffix like
"x2" appears if more than one request is stuck at once. The chip clears itself
within seconds of the underlying request being answered or archived — no
restart needed, it re-scans from scratch every ~10s. It also keeps the PC awake
only while a request is actively pending/stalled, so an unattended run doesn't
get killed by Windows sleep. It cannot write a real reply for you — it only
makes sure a stuck request shows up where you'll see it. See `watcher_service.py`
for the env knobs (`WATCHER_POLL_SEC`, `WATCHER_PENDING_SEC`, etc.).
