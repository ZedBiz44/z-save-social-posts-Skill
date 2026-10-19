"""Behavior checks using synthetic posts; no external services or writes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "dedupe.py"


class DedupeTests(unittest.TestCase):
    def run_helper(self, existing, candidates, *options):
        with tempfile.TemporaryDirectory() as folder:
            paths = [Path(folder) / name for name in ("existing.json", "candidates.json")]
            for path, rows in zip(paths, (existing, candidates)):
                path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), *map(str, paths), *options],
                                  capture_output=True, text=True)

    def result(self, existing, candidates, *options):
        run = self.run_helper(existing, candidates, *options)
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)["results"]

    def test_distinct_media_matching_captions_require_review(self):
        rows = self.result([{"ref": "video-a", "text": "Try this graphic"}],
                           [{"ref": "video-b", "text": "Try this graphic"}])
        self.assertEqual(rows[0]["verdict"], "review-match")
        self.assertEqual(rows[0]["match"], "video-a")

    def test_captionless_video_requires_inspection(self):
        self.assertEqual(self.result([], [{"ref": "video"}])[0]["verdict"], "inspect-content")

    def test_non_latin_text_is_not_discarded(self):
        rows = self.result([], [{"ref": "a", "text": "图形设计"}, {"ref": "b", "text": "社群营销"}])
        self.assertEqual([r["verdict"] for r in rows], ["new", "new"])

    def test_different_links_are_not_empty_or_exact_matches(self):
        rows = self.result([], [{"ref": "a", "text": "https://example.com/a"},
                               {"ref": "b", "text": "https://example.com/b"}])
        self.assertEqual([r["verdict"] for r in rows], ["new", "new"])

    def test_batch_reposts_remain_advisory(self):
        rows = self.result([], [{"ref": "a", "text": "Useful headline"},
                               {"ref": "b", "text": "USEFUL   headline"}])
        self.assertEqual(rows[1]["verdict"], "review-match")
        self.assertEqual(rows[1]["match"], "a")

    def test_threshold_formats(self):
        existing = [{"ref": "a", "text": "one two three four five six seven eight nine ten"}]
        candidate = [{"ref": "b", "text": "one two three four five six seven eight nine eleven"}]
        for options in [("--threshold", "0.8"), ("--threshold=0.8",)]:
            self.assertEqual(self.result(existing, candidate, *options)[0]["verdict"], "review-match")

    def test_invalid_threshold_rejected(self):
        for value in ("0", "1.1", "nan"):
            self.assertNotEqual(self.run_helper([], [], "--threshold", value).returncode, 0)

    def test_invalid_rows_rejected(self):
        self.assertNotEqual(self.run_helper([], [{"text": "missing ref"}]).returncode, 0)


if __name__ == "__main__":
    unittest.main()
