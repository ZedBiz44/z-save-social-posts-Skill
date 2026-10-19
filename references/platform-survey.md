# Platform survey: how to set up intake on a new platform

Run this survey before promising intake on any platform. Record the answers
in the deployment's configuration.

## 1. Read access

- Is there a connector, CLI, or API the agent can use?
- Can it read full posts and media by URL? Prefer a verified connector or
  CLI; otherwise use an approved browser session, not search snippets.
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

**If no:** accept pasted links or use an approved browser route. Call it
scheduled only after a real authorized scheduler and unattended access have
been verified. A skill cannot supply background execution by itself.

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

## Mary's reported access (2026-10-19)

These results describe Mary's tools and account, not universal platform API
capabilities. Preserve them for handover; verify the next agent's actual tools.

| Platform | Saved-items API | Intake |
|---|---|---|
| Facebook | Available through Mary's tools | Standing inbox + scheduled check |
| Instagram | Available through Mary's tools | Standing inbox + scheduled check |
| Threads | Not available in Mary's recorded setup | Manual links |
| LinkedIn | No connector in Mary's recorded setup | Manual links or browser route |

Facebook first and Instagram next are the present scope. TikTok, Threads,
LinkedIn, X and other platforms need their own access survey when requested.

Re-survey a platform if its API changes; don't assume today's answer is
permanent.
