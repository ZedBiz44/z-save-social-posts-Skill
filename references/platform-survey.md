# Platform survey: how to set up intake on a new platform

Run this survey before promising intake on any platform. Record the answers
in the deployment's configuration.

## 1. Read access

- Is there a connector, CLI, or API the agent can use?
- Can it read posts by URL? (Pasted links must go through the platform's
  own read path, never a generic browser scrape, for reliable content.)
- Can it read the principal's own saved items?

## 2. Saved-items capability

- Does the platform have saved items / bookmarks the API can read?
- Can saved items be organized into named collections via the API?
- Can the agent list a collection's contents and tell new items from old
  (stable item IDs)?

**If yes:** create a standing inbox collection (name it after the intake,
e.g. "Mary-Muse"), and set a scheduled check. Track handled item IDs in a
state file (see `assets/state-template.json`). The schedule should fit the
platform and the principal's pace — 4-hourly is a sane default; adjust.

**If no:** intake is manual. Either the principal pastes links, or a
browser route checks on a schedule. Say which one it is and don't present
manual intake as automatic.

## 3. Videos

- Can the agent get a downloadable video URL or file?
- `yt-dlp` handles most public social video URLs; platform CLIs sometimes
  expose media URLs directly. Verify with one real download before
  promising video archiving on a new platform.

## 4. Writes

This skill never needs platform writes except creating the inbox
collection itself (once, with the principal's approval). It never posts,
comments, reacts, or publishes. If a platform's saved-items API is
read-only for collections, the principal creates the inbox by hand and the
agent only reads it.

## Known results (2026-10-19)

| Platform | Saved-items API | Intake |
|---|---|---|
| Facebook | Yes (collections) | Standing inbox + scheduled check |
| Instagram | Yes (saved collections) | Standing inbox + scheduled check |
| Threads | No | Manual links only |
| LinkedIn | No connector | Manual links or browser route |

Re-survey a platform if its API changes; don't assume today's answer is
permanent.
