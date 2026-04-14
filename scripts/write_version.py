import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "obsidian_claude_remote" / "_version.py"


def from_git() -> str:
    try:
        r = subprocess.run(
            ["git", "describe", "--tags", "--always", "--dirty"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return r.stdout.strip() or "dev"
    except Exception:
        return "dev"


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
