# z-save-social-posts

This repository holds the z-save-social-posts skill: save social media
posts to a knowledge base or personal notes, with video download,
transcription and Drive archiving.

## Purpose

Give any agent a repeatable way to file social posts worth keeping —
dedupe them, judge them against two worthiness rules, route personal
saves to personal notes and everything else to the knowledge base, and
handle videos properly instead of filing hollow links.

## When to use

Use this skill when the principal saves posts for later, asks to pull
posts from a platform or author, or wants a standing save inbox on any
social platform the agent can reach.

## Do not use

Do not use this skill to post, comment, react, publish, or delete
anything on any platform — it is read-and-file only. Do not use it for
general web research, for tracking or profiling people, or as a
publishing pipeline.

## SKILL.md authority

`SKILL.md` is authoritative for how the skill operates. References hold
detail; scripts hold repeatable helpers. If this README and `SKILL.md`
ever disagree, `SKILL.md` wins.

## Layout

- `SKILL.md` — the operating instructions
- `references/worthiness.md` — the two worthiness rules
- `references/platform-survey.md` — how to set up intake on a new platform
- `references/video-pipeline.md` — download → understand → archive
- `references/jack-configuration.md` — the complete worked deployment
  this skill was built from (Facebook + Instagram, Notion + Evernote +
  Drive); copy the pattern, substitute your own access
- `scripts/dedupe.py` — content dedupe (URL pass won't catch reposts)
- `assets/state-template.json` — handled-item tracking for inbox checks

## Companion skills

- **z-files-folders** — all file/folder naming
- Read its live Notion guide for client, venture and concept-first naming,
  destination authority and read-back checks. “Project” is reserved for Asana.
- **z-agent-communication** — wording for reports and human-facing messages

## Validate

Run the z-ai-skill-developer validator before release:

`python3 <z-ai-skill-developer-root>/scripts/validate_skill.py --repository .`

The skill must pass, contain no secrets, and complete one real test
before wider installation. Jack approves wider ZedBiz installation.

For authoring checks run `python -m unittest discover -s tests -v`.
After committing the source, run `python scripts/build_package.py`; the clean
`dist/z-save-social-posts/` folder contains only declared runtime resources.
`dist/package-receipt.json` records the source commit and each file's SHA-256.
Validate that folder with the Z validator and the target platform's validator
before installation. Tests, authoring records and README stay out of the package.

The maintained human SOP is in [Notion](https://www.notion.so/3fea3e33d581802695d6f279a802055e).
Mary's working Facebook/Instagram setup remains fully documented for handover.
This revised shared package is a release candidate, not a verified deployment;
no installation or change to Mary's schedule is implied by publishing it.

Duplicate-helper output schema v2 is intentionally advisory. Callers must
handle `review-match` and `inspect-content` without automatic skipping.
Existing handled-ID lists are retained in the state template; new item records
track incomplete stages. For videos require content analysis, upload, media
verification and note verification before completion. Never reset live state
from this empty template. No live caller or state migration has been performed.

## Safety and approval boundary

Never store secrets, tokens, or credentials in this skill. Creating new
destinations (databases, notebooks, drives, collections) needs the
principal's approval once; the standing inbox is then reused. After three
failed attempts at the same operation, stop and report — never switch
identities or routes to bypass a denial.

## Risk level

Operational: reads platform APIs, runs commands, writes to the
principal's knowledge systems within the limits above.
