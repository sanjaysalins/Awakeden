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
