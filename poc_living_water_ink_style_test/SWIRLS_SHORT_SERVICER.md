# Swirls SHORT servicer rules (design v3.2, section 5.2)

You are the live Claude Code session that services OpenArt requests for a Swirls SHORT episode.
These rules are for the GUARDED folder only. Never watch `gen_requests\` for these (that is the old
protocol); never call an OpenArt generate tool without a claim.

Folders under `F:\slk\PycharmProjects\JesusInTheBible\.agent_bridge\`:
`gen_requests_guarded\` (watch this) , `gen_claimed\` , `gen_staging\` , `gen_receipts\` , `gen_responses\` ,
`gen_requests_guarded\cancelled\`.

1. **Claim first.** `os.replace(gen_requests_guarded\<id>.request.json, gen_claimed\<id>.<your-session>.json)`.
   If the rename fails, someone else (or the client's cancel) has it: skip. A claim is the only licence to
   call a generate tool.
2. **Refuse** if the request's `not_after` has passed, or its heartbeat file (`heartbeat` in the request) has
   not been touched for 60 s: move the claim to `gen_requests_guarded\cancelled\` and write an error reply.
3. **Send exactly the request's parameters.** Clips are `generateSound: false`. Do not "improve" a prompt.
   The request's `priced` block is what the guard priced; the creation must match it.
4. **The moment the generate tool returns**, write `gen_claimed\<id>.submitted.json` with the `creation_id`,
   BEFORE you wait for the render.
5. **When it completes, download to `gen_staging\<id>.<ext>`** (png / mp4), never to `out_path`. The client
   moves it after the receipt checks.
6. **Receipt.** Call `openart_creation_show(creation_id)` and save its raw result to `gen_receipts\<id>.json`.
   Copy `sent_params` and `credits_spent` FROM THAT RECORD. Never type them from the call, a quote, or a
   balance difference. A field the record does not show is written as `null`.
7. **Reply** to `gen_responses\<id>.response.json`: `{"status": "ok"|"error", "creation_id": ..., "error": ...}`.
   A reply (success or error) always carries `creation_id` when one exists. An error with a `creation_id`
   is settled by `swirls_episode.py <episode> fetch <id>`, never by a new render.

Banned: any direct call to a generate tool outside these steps; a second generate for the same request;
typing a number into a receipt. `swirls_episode.py <episode> reconcile --dump <openart_creation_list dump>`
looks afterwards for creations that are not in the spend log.
