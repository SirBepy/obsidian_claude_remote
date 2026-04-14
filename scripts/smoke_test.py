import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

MODULES = [
    "obsidian_claude_remote",
    "obsidian_claude_remote.__main__",
    "obsidian_claude_remote.config",
    "obsidian_claude_remote.logger",
    "obsidian_claude_remote.launcher",
    "obsidian_claude_remote.picker",
    "obsidian_claude_remote.startup",
    "obsidian_claude_remote.tray",
    "obsidian_claude_remote.vault_detector",
]


def main() -> int:
    failed = []
    for m in MODULES:
        try:
            importlib.import_module(m)
            print(f"ok   {m}")
        except Exception as e:
            print(f"FAIL {m}: {type(e).__name__}: {e}")
            failed.append(m)
    if failed:
        print(f"\nsmoke test FAILED: {len(failed)}/{len(MODULES)} modules broken")
        return 1
    print(f"\nsmoke test OK: {len(MODULES)} modules imported")
    return 0


if __name__ == "__main__":
    sys.exit(main())
