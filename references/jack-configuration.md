# Jack's reference configuration

The complete working deployment this skill was built from (2026-10-19).
New agents: copy this pattern and substitute your own platform access and
destinations. IDs below are Jack's — do not reuse them for another
principal.

## Inboxes (rule 1 intake)

| Platform | Inbox | How it's checked |
|---|---|---|
| Facebook | "Mary-Muse" saves collection (`10166201774963939`) | `facebook-cli saved list --collection-id`, diff `savable_id` |
| Instagram | "Mary-Muse" saved collection (`1908821377191493`) on marketingjackz (`17841426345262753`) | `instagram-cli saved-posts --collection-id`, diff media IDs |

A cron (`mary-muse-collection-watch`, every 4h) runs the full workflow on
both inboxes. State file tracks handled IDs:
`.../hidden_files/saves/mary-muse-state.json`.

## Destinations

- **Knowledge base:** Notion database Marketing-Swipes
  (`collection://cf9da23e-8817-4c26-ae51-73e1e727e456`).
  Platform = where posted, Source = Social-Media. Inbox items file as
  Reference; raw pulls file as Needs Review for triage.
- **Personal notes:** Evernote notebook Jack-Personal
  (`1d07b1a2-7361-441d-8749-b93983b86b3d`). One inbox notebook; the
  existing tag system (`!`-time, `.`-category, `@`-place) does the sorting.
- **Video homes:** Google Drive Shared Drives on jack@zbiz.work —
  `Saved-Social-Videos` (`0AIVQeteOQSkwUk9PVA`) for business/marketing,
  `Saved-Personal-Social-Videos` (`0AKow9wvG7XyvUk9PVA`) for personal.
  Uploads need the direct Drive API with `supportsAllDrives:true`; the
  `+upload` helper doesn't do shared drives.

## Dedupe

- URL pass: query Marketing-Swipes for the Source-Link.
- Content pass: `scripts/dedupe.py` (Jaccard word-set similarity, 0.85
  threshold; normalization: lowercase, whitespace collapse, unicode-bold
  flattening, link stripping). Catches reposts with new URLs and dupes
  within a batch.

## Video pipeline (proven 2026-10-19)

- Tools: `yt-dlp` + `faster-whisper` in `~/workspace/.venv-whisper`
  (base model cached). Gotcha: faster-whisper 1.2.1 calls
  `av.open(..., metadata_errors="ignore")` but av≥14 removed that kwarg —
  patch `av.open` in-script to pop it. pip needs TMPDIR off the 512M
  `/tmp` tmpfs.
- Talking videos → transcript → summary. Music-only → frame-watch
  (~6 frames via ffmpeg) → visual summary.
- Pipeline intermediates live under the goal's `hidden_files/saves/`,
  never /tmp (a restart wiped /tmp mid-run once).

## People records (Notion)

Author linking uses the People database; records must exist first and are
created only with Jack's OK. Known: Jeff J Hunter
(`3fda3e33-d581-8102-981e-c3ba0cc6a915`), Jonathan Mast
(`3fda3e33-d581-819c-9ffc-c4b48a471f8b`).

## Topic lanes (categorization)

AI agents, marketing, prompts, AI tools, automation, GHL/GoHighLevel.
Extend only with Jack's OK. Lanes tag and categorize; they don't decide
worthiness (see [worthiness](worthiness.md)).
