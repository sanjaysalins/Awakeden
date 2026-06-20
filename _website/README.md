# Awakeden Series — www.awakeden.com

Static prelaunch/postlaunch catalogue site. Hosted on **Netlify**; DNS on **Cloudflare**.

## Local preview

From repo root:

```powershell
pip install -r _website/requirements.txt
python _website/build_catalog.py
cd _website
python -m http.server 8080
```

Open http://localhost:8080

Or with Netlify CLI: `netlify dev` from `_website/`.

## Build (Netlify)

Netlify runs automatically via `netlify.toml`:

- **Base directory:** `_website`
- **Command:** `pip install -r requirements.txt && python build_catalog.py`
- **Publish:** `.`

## Edit public content

1. **`manifest.yaml`** — catalogue items, public status, preview approval, YouTube IDs, copy.
2. **`config.yaml`** — site mode (`prelaunch` | `live`), social handles, noindex flag.
3. Re-run `build_catalog.py` (or push to GitHub — Netlify rebuilds).

### Public status values

| Value | Meaning on site |
|---|---|
| `planned` | On the slate |
| `in_production` | Actively being made |
| `studio_complete` | Signed off in studio; preview OK if approved |
| `live` | YouTube embed shown (needs `youtube_id` + `site.mode: live`) |

**`preview_approved: true`** is required before a preview image is shown (red-team gate).

## Deploy checklist

1. Connect GitHub repo to Netlify; set base `_website`.
2. Add custom domains `www.awakeden.com` + `awakeden.com` in Netlify.
3. Cloudflare DNS: `www` CNAME → Netlify; apex redirect per `netlify.toml`.
4. Cloudflare SSL: **Full (strict)**.
5. After first YouTube publish: set `youtube_id` on item, flip `site.mode` to `live`, set `noindex: false`.

## Preview images

Production PNGs are gitignored. The build script:

- Copies/resizes sources listed in `manifest.yaml` → `assets/previews/*.webp` when Pillow finds the file locally/CI.
- Falls back to styled SVG placeholders when missing.

Commit `.webp` previews from a local build if Netlify CI has no PNG sources:

```powershell
python _website/build_catalog.py
git add _website/assets/previews/
```
