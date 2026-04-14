import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "obsidian_claude_remote" / "_version.py"

TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def _run(args: list[str]) -> str:
    return subprocess.run(
        args,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _latest_tag() -> str | None:
    try:
        tag = _run(["git", "describe", "--tags", "--abbrev=0"])
        return tag or None
    except Exception:
        return None


def _commits_ahead(tag: str) -> int:
    try:
        return int(_run(["git", "rev-list", f"{tag}..HEAD", "--count"]))
    except Exception:
        return 0


def _bump_patch(tag: str) -> str:
    m = TAG_RE.match(tag)
    if not m:
        return tag
    maj, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    return f"v{maj}.{minor}.{patch + 1}"


def from_git() -> str:
    try:
        subprocess.run(
            ["git", "fetch", "--tags", "--quiet"],
            cwd=str(ROOT),
            capture_output=True,
            check=False,
        )
    except Exception:
        pass

    tag = _latest_tag()
    if tag is None:
        return "v0.1.0"

    if _commits_ahead(tag) == 0:
        return tag

    return _bump_patch(tag)


def main() -> int:
    if len(sys.argv) > 1:
        version = sys.argv[1]
    else:
        version = os.environ.get("OCR_VERSION") or from_git()
    OUT.write_text(f'__version__ = "{version}"\n', encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} = {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
