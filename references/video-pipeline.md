# Video pipeline: download, understand, archive

A video post filed as just a link is a hollow entry — the substance is
inside the video. Run this pipeline for every video worth saving.

## 1. Download

- Prefer `yt-dlp`: `yt-dlp -f 'bv*[height<=720]+ba/b[height<=720]/b'
  --no-playlist -o '<name>.%(ext)s' '<url>'`
- 720p is enough for understanding; it keeps files small.
- Verify one real download per platform before promising archiving.

## 2. Understand

**Talking videos → transcript.** Run a speech-to-text model
(faster-whisper works well on CPU; base model is a good default).
Transcribe the audio, then summarize: what it teaches, key points, why
it's worth keeping.

**Music-only / no-speech videos → frame-watch.** If the transcript comes
back as just "music," the video has no narration. Extract ~6 frames
spread across the runtime (`ffmpeg -ss <t> -i <file> -frames:v 1
<frame>.jpg`), view them, and describe what the video shows: the build,
the demo, the before/after. Summarize from the visuals.

Note which method was used in the filed entry, so a reader knows what
the summary is based on.

## 3. Archive the file

Save the video file to the principal's video home — business and
personal videos go to separate homes. Platform links rot; files don't.

- Name per **z-files-folders**: lowercase, dashes, topic-first, sequence
  (e.g. `workshop-overhead-storage-woodwork-junkie-01.mp4`).
- Link the archived file from the knowledge-base / personal-notes entry.
- Keep pipeline intermediates (downloads, transcripts, frames) in the
  deployment's working area, not in temp directories that get wiped.

## 4. File

The summary + video link + original post link get filed per the normal
workflow (knowledge base for substantive content, personal notes for
personal). The video file itself lives in the video home; the entry
points to it.
