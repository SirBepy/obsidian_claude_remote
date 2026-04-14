import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    for d in ("build", "dist"):
        p = ROOT / d
        if p.exists():
            shutil.rmtree(p)
    spec = ROOT / "obsidian_claude_remote.spec"
    if spec.exists():
        spec.unlink()

    entry = ROOT / "scripts" / "_pyinstaller_entry.py"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--icon=icon.ico",
        "--paths",
        "src",
        "--add-data",
        "assets/images/favicon.png;assets/images",
        "--add-data",
        "icon.ico;.",
        "--name=obsidian_claude_remote",
        str(entry),
    ]
    print("running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


if __name__ == "__main__":
    sys.exit(main())
