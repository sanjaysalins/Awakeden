# veed_io

A small, typed Python wrapper around **VEED's subtitle model on fal.ai**
(`veed/subtitles`). Give it a video, get back an MP4 with **styled, burned-in
captions**.

This package is **self-contained and independent** of the gospel-shorts engine
in the rest of this repo — nothing here imports from `pipeline/` and nothing in
the engine imports from here.

---

## What the model does

`veed/subtitles` takes a video URL, auto-transcribes the audio, applies a style
**preset**, and returns a rendered video with the captions burned in. You can
also skip transcription by supplying your own SRT.

- **Auto-transcribe** or **bring your own SRT** (`srt_file_url` / `srt_content`)
- **27 presets** in two price tiers (dynamic = 2×, basic = 1×)
- **~150 source languages** (improves transcription accuracy)
- **Customization**: vertical position, shadow, and per-tier font/weight/colour
  for `baseline` vs `highlighted` words

**Output:** `{ video: { url, content_type, file_name, file_size } }`

**Pricing:** base **$0.10/min**; dynamic presets ×2. A 60s Short ≈ **$0.10**
(basic) / **$0.20** (dynamic). `estimate` is a client-side guess — fal.ai is
authoritative.

### Spend control (built in, fail-closed)

Every billable `subtitle` run is **gated**:

1. It probes the video duration (ffprobe; falls back to a 60s worst-case) and
   prints a **loud bright-red ANSI spend banner** with the dollar estimate.
2. It then **refuses to spend** unless you either type `yes` at the prompt or
   pass `--yes`. Non-interactive + no `--yes` = **abort, $0 spent** (exit 3).
3. After a job finishes it reprints a **CHARGED (est.)** banner so the number is
   impossible to miss.

`presets` and `estimate` never spend and never need a key.

---

## Setup

```powershell
# from the repo root, using the repo venv
.venv\Scripts\python.exe -m pip install -r veed_io\requirements.txt

# get a key at https://fal.ai/dashboard/keys
$env:FAL_KEY = "your-fal-api-key"
```

(or copy `veed_io/.env.example` → `veed_io/.env` and load it yourself).

---

## CLI

```powershell
# list presets by price tier (no key needed)
.venv\Scripts\python.exe -m veed_io.cli presets

# estimate cost for a 60s clip (no key needed)
.venv\Scripts\python.exe -m veed_io.cli estimate --seconds 60 --preset glass

# subtitle a HOSTED clip, download the result into .\out\
.venv\Scripts\python.exe -m veed_io.cli subtitle `
    --video https://example.com/clip.mp4 --preset glass --out .\out\

# subtitle a LOCAL file (auto-uploads to fal storage first)
.venv\Scripts\python.exe -m veed_io.cli subtitle `
    --video .\clip.mp4 --preset simple --language en-US --out .\out\

# style overrides: bottom position, highlighted words gold + bold
.venv\Scripts\python.exe -m veed_io.cli subtitle --video .\clip.mp4 `
    --preset glass --position bottom --shadow mid `
    --highlight-color "#FFD400" --highlight-weight 800 --out .\out\

# long video: submit to the queue, fetch later
.venv\Scripts\python.exe -m veed_io.cli subtitle --video .\long.mp4 --async
.venv\Scripts\python.exe -m veed_io.cli fetch --request-id <id> --out .\out\
```

---

## Library

```python
from veed_io import SubtitleRequest, VeedSubtitlesClient
from veed_io.models import PresetCustomization, TextCustomization

client = VeedSubtitlesClient()                  # reads FAL_KEY

req = SubtitleRequest(
    video_url=client.upload_file("clip.mp4"),   # or a public URL / data URI
    preset="glass",
    language="en-US",
    customization=PresetCustomization(
        position="bottom",
        shadow="mid",
        highlighted=TextCustomization(color="#FFD400", weight=800),
    ),
)

print(client.estimate(60, req.preset))          # ~$0.20 (...)
result = client.subtitle(req, on_log=print)     # blocking, streams logs
client.download(result, "out/")                 # -> out/<file_name>.mp4
```

Async / queue (long videos, servers):

```python
request_id = client.submit(req, webhook_url="https://you/webhook")
# ... later / on webhook ...
result = client.result(request_id)
```

See `examples/quickstart.py` for a runnable end-to-end script.

---

## Layout

```
veed_io/
  __init__.py        public exports
  client.py          VeedSubtitlesClient (subscribe / submit / status / result / upload / download)
  models.py          SubtitleRequest, SubtitleResult, PresetCustomization, TextCustomization
  presets.py         preset tiers, positions, shadows, language hints
  pricing.py         estimate_cost() — base $0.10/min, dynamic 2x
  cli.py             `python -m veed_io.cli ...`
  requirements.txt   fal-client
  .env.example       FAL_KEY
  examples/quickstart.py
  tests/test_offline.py   no key / no install required
```

## Tests

```powershell
.venv\Scripts\python.exe -m veed_io.tests.test_offline
```

## Notes / gotchas

- **Fonts** must be from VEED's Google-Fonts allow-list
  (<https://www.veed.io/api/v1/subtitle-renders/fonts>) or the API returns 400.
- **Large local files**: the client uploads them to fal storage rather than
  inlining base64 (better performance).
- **`language`** is the *source-audio* language, not the output subtitle
  language.
- Supplying `srt_file_url` **or** `srt_content` skips transcription (faster,
  exact timing); supplying both is rejected client-side.

Built against the `veed/subtitles` fal.ai schema (Python client).
