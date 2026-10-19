"""Build only declared runtime resources and record their hashes/source commit."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
if subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip():
    raise SystemExit("Commit the reviewed source before building a package tied to that commit.")
target = root / "dist" / "z-save-social-posts"
if target.exists():
    raise SystemExit("Package already exists; choose a fresh build workspace rather than overwrite it.")
paths = [root / "SKILL.md"]
for line in (root / "package-resources.txt").read_text(encoding="utf-8").splitlines():
    path = (root / line).resolve()
    if not path.is_relative_to(root) or not path.exists():
        raise SystemExit("Invalid runtime resource")
    paths.extend(sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path])
receipt = {"source_commit": subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(), "files": {}}
for path in paths:
    relative = path.relative_to(root)
    output = target / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, output)
    receipt["files"][relative.as_posix()] = hashlib.sha256(output.read_bytes()).hexdigest()
(root / "dist" / "package-receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
print(json.dumps(receipt, indent=2))
