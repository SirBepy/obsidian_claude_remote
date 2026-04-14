import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main() -> int:
    for d in ("build", "dist"):
        p = ROOT / d
        if p.exists():
            shutil.rmtree(p)
    spec = ROOT / "obsidian_claude_remote.spec"
    if spec.exists():
        spec.unlink()

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--icon=icon.ico",
        "--add-data",
        "assets/images/favicon.png;assets/images",
        "--add-data",
        "icon.ico;.",
        "--name=obsidian_claude_remote",
        "main.py",
    ]
    print("running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


if __name__ == "__main__":
    sys.exit(main())
