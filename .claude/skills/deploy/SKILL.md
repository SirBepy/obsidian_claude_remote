---
name: deploy
description: Project-local skill. Commits + pushes, then rebuilds the exe and relaunches the tray so the running instance matches HEAD.
---

# /deploy

> Ship to GitHub and reload the local tray in one go. For `obsidian_claude_remote` only.

## Steps

### 1. Commit and push

Invoke the global `/commit push` skill. If it aborts (smoke test fail, lint fail, nothing to commit, etc.), **stop immediately**. Do not build, do not touch the running tray. Print why it stopped.

### 2. Kill any running tray instance

Use psutil from an inline python call to find and terminate any process named `obsidian_claude_remote.exe`, plus its children. Example (run from repo root):

```
python -c "import psutil; killed = 0; [ (p.terminate(), p.wait(timeout=3), None) for p in psutil.process_iter(['name']) if (p.info.get('name') or '').lower() == 'obsidian_claude_remote.exe' and (killed := killed + 1) ]; print(f'killed {killed} instance(s)')"
```

If that one-liner is awkward, write a short `py -c` block with a for-loop. Goal: no `obsidian_claude_remote.exe` left running before Step 4.

### 3. Remove stale Startup shortcut

Delete `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\obsidian_claude_remote.lnk` if it exists, so the freshly launched exe re-registers pointing at the new `dist/` path. Use the Bash tool:

```
rm -f "$APPDATA/Microsoft/Windows/Start Menu/Programs/Startup/obsidian_claude_remote.lnk"
```

### 4. Clean and build

```
rm -rf dist build
python scripts/build.py
```

If the build exits non-zero, stop and print the tail of PyInstaller output. Do not launch.

### 5. Launch the new exe

From the repo root:

```
start "" "dist/obsidian_claude_remote.exe"
```

(On Windows Git Bash, `start` works. Fallback: `cmd //c start "" "dist/obsidian_claude_remote.exe"`.)

### 6. Confirm

Tell the user: commits pushed, build succeeded, tray relaunched from `<repo>/dist/obsidian_claude_remote.exe`. Startup `.lnk` will re-register itself on next run (the frozen exe handles it via `ensure_startup`).

## Notes

- Never run the deploy flow from source (`python -m obsidian_claude_remote`) - the whole point is to exercise the packaged `.exe`.
- If psutil reports 0 kills, that is fine - it just means the tray was not running when you started.
- The repo's `dist/` path is the permanent home of the installed exe. If Joe ever moves or deletes the repo, the Windows Startup `.lnk` will break. That is an accepted tradeoff.
