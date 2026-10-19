#!/usr/bin/env python3
"""Content dedupe for the social-swipe-intake skill.

Catches reposts that share no URL: compares candidate post texts against
texts already filed in Marketing-Swipes (and against each other).

Usage:
    dedupe.py existing.json candidates.json [--threshold 0.85]

    existing.json:   [{"ref": "<swipes page title or id>", "text": "..."}, ...]
    candidates.json: [{"ref": "<post id>", "source_link": "https://...", "text": "..."}, ...]

Output (JSON to stdout): one verdict per candidate:
    new         keep it
    exact-dupe  normalized text identical to an existing entry -> skip
    near-dupe   text >= threshold similar to an existing entry -> skip, review match
    empty       no usable text -> skip, flag for manual check
Each dupe verdict names the matched existing ref.
"""
import json
import sys
import hashlib
import re
import unicodedata


def normalize(text):
    """Flatten a post's text so reposts compare equal despite cosmetic differences."""
    if not text:
        return ""
    # Decompose stylized unicode (e.g. mathematical bold "𝗗𝗲𝗲𝗽𝗦𝗲𝗲𝗸") to plain ASCII
    t = unicodedata.normalize("NFKD", text)
    t = "".join(c for c in t if ord(c) < 128)
    t = t.lower()
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"https?://\S+", " ", t)      # links rot / get shortened; ignore them
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
    threshold = 0.85
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--threshold"):
            threshold = float(a.split("=")[1])
    existing = json.load(open(args[0]))
    candidates = json.load(open(args[1]))

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
            results.append({"ref": ref, "verdict": "empty", "match": None})
            continue
        fp = fingerprint(n)
        if fp in seen_fp:
            results.append({"ref": ref, "verdict": "exact-dupe", "match": seen_fp[fp]})
            continue
        if fp in batch_fps:
            results.append({"ref": ref, "verdict": "exact-dupe", "match": batch_fps[fp]})
            continue
        match = None
        for eref, en, efp in index:
            if efp == fp or similar(n, en, threshold):
                match = eref
                break
        if match:
            results.append({"ref": ref, "verdict": "near-dupe", "match": match})
        else:
            results.append({"ref": ref, "verdict": "new", "match": None})
        batch_fps[fp] = ref
        # later candidates also compare against earlier candidates in this batch
        index.append((ref, n, fp))

    print(json.dumps({"threshold": threshold, "results": results}, indent=1))


if __name__ == "__main__":
    main()
