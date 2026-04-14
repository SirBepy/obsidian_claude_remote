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

    rc = subprocess.call(
        [sys.executable, str(ROOT / "scripts" / "write_version.py")],
        cwd=str(ROOT),
    )
    if rc != 0:
        print("write_version.py failed, aborting build")
        return rc

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
        "--add-data",
        "src/obsidian_claude_remote/ui/picker.html;ui",
        "--collect-all",
        "webview",
        "--name=obsidian_claude_remote",
        str(entry),
    ]
    print("running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


if __name__ == "__main__":
    sys.exit(main())
