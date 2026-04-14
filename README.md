# obsidian_claude_remote

Windows tray app. Auto-launches Claude Code with `--remote-control` inside an Obsidian vault on PC boot. Lets you reach the vault from the Claude phone app without ever opening a terminal.

## What it does

- On first run, detects Obsidian vaults from `%APPDATA%\Obsidian\obsidian.json` and shows a picker.
- Saves choice to `%APPDATA%\obsidian_claude_remote\config.json`.
- Launches `claude --remote-control` inside that vault with no visible window.
- Sits in the system tray. Right click for **Settings**, **Restart Claude**, **Quit**.
- When packaged as `.exe`, registers itself in the Windows Startup folder so it runs on boot.

## Run from source

```
pip install -r requirements.txt
python main.py
```

## Build the exe

```
python build.py
```

Output: `dist/obsidian_claude_remote.exe`. Move it somewhere stable (it self-registers in Startup, so the path it lives at when you first run it is the path Windows will launch on boot).

## Releases

Every push to `main` triggers `.github/workflows/build-release.yml`, which builds the exe on `windows-latest`, auto-bumps the patch version (latest `vX.Y.Z` tag + 1), pushes the new tag, and publishes a GitHub Release with the exe attached. Grab the latest from the Releases page.

## Files

| File | Purpose |
| --- | --- |
| `main.py` | Entry point, wires everything together |
| `tray.py` | Pystray icon + menu |
| `picker.py` | Tk vault picker dialog |
| `launcher.py` | Spawn / kill / restart Claude subprocess |
| `config.py` | Read/write `config.json` |
| `vault_detector.py` | Parse Obsidian's vault list |
| `startup.py` | Register `.lnk` in Windows Startup folder |
| `logger.py` | File logger to `%LOCALAPPDATA%\obsidian_claude_remote\app.log` |
| `generate_icon.py` | Generates `icon.ico` + `assets/images/favicon.png` via PIL |
| `build.py` | PyInstaller wrapper |

## Logs

`%LOCALAPPDATA%\obsidian_claude_remote\app.log`

## TODO

- Multi-vault support (currently one vault per install)
- Mac / Linux support (launchd, systemd)
- Tray icon state colors (running / crashed)
- Auto-restart Claude if it dies
