#!/usr/bin/env python3
"""Advisory content comparison for z-save-social-posts.

Catches reposts that share no URL: compares candidate post texts against
texts already filed in Marketing-Swipes (and against each other).

Usage:
    dedupe.py existing.json candidates.json [--threshold 0.85]

    existing.json:   [{"ref": "<swipes page title or id>", "text": "..."}, ...]
    candidates.json: [{"ref": "<post id>", "source_link": "https://...", "text": "..."}, ...]

Output (JSON to stdout): one verdict per candidate:
    new              no text match found; apply the normal selection rules
    review-match     similar/identical text; compare actual post and media
    inspect-content  absent caption; inspect media or report unavailable content
No verdict authorizes skipping. Caption similarity is not media identity.
Output schema_version=2 replaces the earlier automatic-skip verdicts.
"""
import argparse
import json
import sys
import hashlib
import re
import unicodedata


def normalize(text):
    """Flatten a post's text so reposts compare equal despite cosmetic differences."""
    if not text:
        return ""
    # Flatten styled letters without discarding non-English text.
    t = unicodedata.normalize("NFKC", text).casefold()
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # Retain links: otherwise two link-only posts collapse into empty text.
    t = re.sub(r"\s+", " ", t).strip()
    return t


def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def similar(a, b, threshold):
    """Fast near-duplicate check: Jaccard similarity over word sets.

    Catches reposts with small edits (reworded opening, trimmed paragraphs).
    Runs in linear time, so it stays usable on large swipe files where
    sequence alignment would be too slow.
    """
    if not a or not b:
        return False
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb:
        return False
    # cheap pre-filter: vocabulary sizes must be within 30% of each other
    if abs(len(sa) - len(sb)) / max(len(sa), len(sb)) > 0.30:
        return False
    return len(sa & sb) / len(sa | sb) >= threshold


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("existing")
    parser.add_argument("candidates")
    parser.add_argument("--threshold", type=float, default=0.85)
    args = parser.parse_args()
    threshold = args.threshold
    if not 0 < threshold <= 1:
        parser.error("threshold must be greater than 0 and at most 1")
    try:
        with open(args.existing, encoding="utf-8-sig") as stream:
            existing = json.load(stream)
        with open(args.candidates, encoding="utf-8-sig") as stream:
            candidates = json.load(stream)
        for rows in (existing, candidates):
            if not isinstance(rows, list) or any(
                not isinstance(row, dict) or not isinstance(row.get("ref"), str)
                or not row["ref"] or not isinstance(row.get("text", ""), str)
                for row in rows
            ):
                parser.error("inputs must be arrays of objects with nonempty string ref and optional string text")
    except (OSError, ValueError):
        parser.error("could not read input JSON files; check paths, encoding and JSON format")

    index = []  # (ref, normalized, fingerprint)
    seen_fp = {}
    for e in existing:
        n = normalize(e.get("text", ""))
        if not n:
            continue
        fp = fingerprint(n)
        seen_fp.setdefault(fp, e.get("ref"))
        index.append((e.get("ref"), n, fp))

    results = []
    batch_fps = {}  # catch dupes within the candidate batch itself
    for c in candidates:
        ref = c.get("ref")
        n = normalize(c.get("text", ""))
        if not n:
            results.append({"ref": ref, "verdict": "inspect-content", "match": None})
            continue
        fp = fingerprint(n)
        if fp in seen_fp:
            results.append({"ref": ref, "verdict": "review-match", "match_kind": "exact-text", "match": seen_fp[fp]})
            continue
        if fp in batch_fps:
            results.append({"ref": ref, "verdict": "review-match", "match_kind": "exact-text", "match": batch_fps[fp]})
            continue
        match = None
        for eref, en, efp in index:
            if efp == fp or similar(n, en, threshold):
                match = eref
                break
        if match:
            results.append({"ref": ref, "verdict": "review-match", "match_kind": "similar-text", "match": match})
        else:
            results.append({"ref": ref, "verdict": "new", "match": None})
        batch_fps[fp] = ref
        # later candidates also compare against earlier candidates in this batch
        index.append((ref, n, fp))

    print(json.dumps({"schema_version": 2, "advisory_only": True,
                      "threshold": threshold, "results": results}, indent=1))


if __name__ == "__main__":
    main()
