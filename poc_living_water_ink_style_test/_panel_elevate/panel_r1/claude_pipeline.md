A. MY TOP 5 (written before reading the draft)

1. **Post 2-3 episodes now.** Twelve pieces, zero audience signal. Every other decision is a guess until a real 48h retention curve exists. Rework spend only pays off if you know what viewers reward.
2. **Fix props at the source with a shape ref.** One approved side-on cross image, chained into every page. The ep13 cross defect survived 3 wording fixes on 6+ pages. That is where its 70 rejects came from.
3. **Draft cheap, finalize once.** Check composition and caption legibility on a 15cr model first. Pay for nano-banana-pro only on approved layouts.
4. **Gate every clip before it enters assembly.** Pixel-diff and first/last-frame checks, with a $0 push-in fallback. You already learned these lessons, so make them code.
5. **Bake the lessons into one preflight file.** Banned shapes, digit scan, ending-shape check, title-once check. Run it before any paid call.

B. GRADING THE 7 DRAFT ITEMS

1. **CHANGE.** Only automate checks for defects that have a deterministic signature. Stray digits and a doubled title can be caught by OCR. X-cross, vanishing figures and panel wrap need Vision, which is flaky. Your own pack says Vision audits are "deliberately not auto-retried". Don't promise auto-retry on the soft ones.
2. **KEEP.** This has the best evidence behind it: it was a root cause across 6+ pages. Caveat: the ref must be validated on one page before it is chained everywhere. A bad ref copies the defect to all 9 pages.
3. **CHANGE.** Draft on a cheaper model only if that model's layout predicts nano-banana-pro's layout. Different models compose differently, and the pack shows Seedream and NBP disagree on pose. Test the correlation on one episode first. Otherwise you pay twice.
4. **KEEP.** This is cheap, and the pack's own lessons support it. Run it per clip, with the fallback written into the plan. Add a "needs real motion" flag so pages are not all downgraded to push-ins, which would make the episode flat.
5. **CHANGE.** The words process is already the gold standard, so making it a gate adds little. The ending-shape check is the new part. Keep that one and cut the rest.
6. **KEEP, but it's the owner's call.** I'd rank it first. It is the only item that produces new information. Post the 2-3 strongest, not the newest.
7. **DROP for now.** The bridge needs a live session either way. Batching saves chat turns, not dollars or rework. Ep13's cost came from rejects, not from bridge round-trips. Revisit after items 1-5.

C. WHAT THE DRAFT MISSED

**There is no per-defect cost accounting.** The pack says ep13 kept 70 rejects while ep1-5 and ep8 kept 0, and then it treats ep13 as the normal case. Ep13 is a prop-heavy outlier: a cross on 9 pages. The draft builds generic machinery from one episode. It also leaves out a **prop-risk triage at design time**. Before any render, score the episode's hard props and decide the camera angle and the ref up front. Also missing: the **rejects ledger**. SUPERSEDED files should be logged with a reason code (X-cross, digit, caption, motion). Without that, you can't say which checks pay for themselves. Finally, **the 70 rejects aren't counted in cost**. The ledger is split across names, so "~$19" probably understates the real total.

D. WRONG OR UNSUPPORTED CLAIMS

- "Ep13 ~$19" next to 70 rejects looks inconsistent. Either the rejects were cheap or the ledger misses spend. The pack itself calls the ledger rough.
- Older episodes with 0 rejects "may simply not have kept rejects". That means the defect rate is not comparable across episodes. Don't base priorities on it.
- "Don't build full gates yet, revisit after 4-5 clean episodes" is stale. It was written 2026-08-21, and 12 pieces have shipped since. The draft treats the gates as new, but the deferral condition is already met.
- Item 6 says "ends the hold early". The pack says the hold was set to reach 30 episodes. It doesn't say why. Check the reason before overriding it, since it could be channel-level (a consistent catalogue at launch).
- The "ep12 cut-off" playback bug is unresolved and not in the draft. A bug that can ship in a posted video is more urgent than most of the 7 items.

E. FIRST MOVE THIS WEEK

Post **one** already-finished episode, chosen for clean render quality and not for being newest, as a single test. Cost: $0 in spend, plus about an hour of owner time. In parallel, run **one $0 audit** on all 12 finished files: OCR for stray digits and double titles, a cut-off check on the ep12 mp4, and a loudness check. This tells you which items really occur before any build. Before the post, fix the Jacob's Ladder doubled title and the 10 s cover hold, or skip that piece.

F. CONFIDENCE: 6/10

I'd change my mind on three points.
- A reject log showing most waste is not in props. That would weaken item 2 and the preflight.
- A cheap-model layout test showing poor correlation with NBP. That would kill item 3.
- A reason for the 30-episode hold that goes beyond "catalogue depth". That would change my ranking of item 6.
