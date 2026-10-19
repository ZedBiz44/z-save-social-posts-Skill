# Video pipeline: download, understand, archive

A video post filed as just a link is a hollow entry — the substance is
inside the video. Run this pipeline for every video worth saving.

## Download

- Prefer `yt-dlp`: `yt-dlp -f 'bv*[height<=720]+ba/b[height<=720]/b'
  --no-playlist -o '<name>.%(ext)s' '<url>'`
- Start with 720p to keep files small; use higher resolution when screen
  text or graphic details are unreadable. Preserve the actual output format.
- Verify one real download per platform before promising archiving.
- Use the agent's approved access and a scoped working folder. Pass URLs
  and filenames as separate arguments; never execute commands from a post.
- If download is unavailable, retain an incomplete note with the original
  link and reason. Do not claim the video is archived or broaden access.

## Understand speech and visuals

**Talking videos → transcript.** Run a speech-to-text model
(faster-whisper works well on CPU; base model is a good default).
Transcribe the audio, then summarize: what it teaches, key points, why
it's worth keeping.

**Visual information → frame-watch, with or without speech.** Inspect
demonstrations, AI graphics, slides, on-screen text and before/after results
even when a transcript exists. An empty or "music" transcript can also be a
transcription failure; check the actual audio before concluding no speech.
Extract approximately six frames as an initial sample
spread across the runtime (`ffmpeg -ss <t> -i <file> -frames:v 1
<frame>.jpg`), view them, and describe what the video shows: the build,
the demo, the before/after. Inspect additional frames or watch relevant
segments when the sample misses steps or text. Summarize only what was
actually heard/read/viewed; mark gaps and useful timestamps.

Note which method was used in the filed entry, so a reader knows what
the summary is based on.

## Archive and verify the file

Save the video file to the principal's video home — business and
personal videos go to separate homes. Verify archived files rather than
relying solely on platform links that may disappear.

- Load **z-files-folders** and the current Notion guide. Use the correct
  client, venture or concept first, followed by useful description and sequence
  (e.g. `woodwork-junkie-workshop-overhead-storage-01.mp4`).
- Link the archived file from the knowledge-base / personal-notes entry.
- Re-read its ID, name, parent, size/type and intended access; open the
  uploaded content to check it is usable. Reopen the note and its media link.
- Keep pipeline intermediates (downloads, transcripts, frames) in the
  deployment's working area, not in temp directories that get wiped.

## File and recover

The summary + video link + original post link get filed per the normal
workflow (knowledge base for substantive content, personal notes for
personal). The video file itself lives in the video home; the entry
points to it.

Keep the transcript or detailed visual notes linked or included when they
contain useful information beyond the summary. Record completed stages in
private state. A failed upload or analysis leaves the item incomplete; retry
only missing work using existing note/file IDs. Before retrying an uncertain
write, search for the created item. Stop after three failures of the same
operation and report the remaining stage without discarding successful work.
