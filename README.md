> ⚠ **DISCONTINUED** — This project has been merged into
> [claude_usage_in_taskbar](https://github.com/SirBepy/claude_usage_in_taskbar).
> Please migrate: install the new app and click **Import** on first launch.

## Migration

- Download the latest [claude_usage_in_taskbar](https://github.com/SirBepy/claude_usage_in_taskbar) release.
- Run it; first launch offers to import your existing `obsidian_claude_remote` config.
- Confirm the automated channel is running in the new app.
- Uninstall `obsidian_claude_remote`:
  - Quit the tray app.
  - Delete the `.lnk` from `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`.
  - Delete the exe wherever you placed it.

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
python -m obsidian_claude_remote
```

Note: Python picks up the `src/` layout automatically if you `pip install -e .` first, otherwise set `PYTHONPATH=src`.

## Build the exe

```
python scripts/build.py
```

Output: `dist/obsidian_claude_remote.exe`. Move it somewhere stable (it self-registers in Startup, so the path it lives at when you first run it is the path Windows will launch on boot).

## Releases

Every push to `main` triggers `.github/workflows/build-release.yml`, which builds the exe on `windows-latest`, auto-bumps the patch version (latest `vX.Y.Z` tag + 1), pushes the new tag, and publishes a GitHub Release with the exe attached. Grab the latest from the Releases page.

## Files

```
obsidian_claude_remote/
├── src/obsidian_claude_remote/   # package
│   ├── __main__.py               # entry, `python -m obsidian_claude_remote`
│   ├── tray.py                   # pystray icon + menu
│   ├── picker.py                 # tk vault picker dialog
│   ├── launcher.py               # spawn / kill / restart claude subprocess
│   ├── config.py                 # read/write config.json
│   ├── vault_detector.py         # parse obsidian's vault list
│   ├── startup.py                # register .lnk in windows startup folder
│   └── logger.py                 # file logger
├── scripts/
│   ├── build.py                  # pyinstaller wrapper
│   ├── generate_icon.py          # regenerate icon.ico + favicon.png
│   └── _pyinstaller_entry.py     # shim so pyinstaller can import the package
├── assets/images/favicon.png
├── icon.ico
├── pyproject.toml
└── requirements.txt
```

## Logs

`%LOCALAPPDATA%\obsidian_claude_remote\app.log`

## TODO

- Multi-vault support (currently one vault per install)
- Mac / Linux support (launchd, systemd)
- Tray icon state colors (running / crashed)
- Auto-restart Claude if it dies
