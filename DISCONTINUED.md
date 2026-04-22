# Discontinued

This project has been discontinued and merged into
[claude_usage_in_taskbar](https://github.com/SirBepy/claude_usage_in_taskbar).
All functionality previously offered here is now a feature of the successor
app, which continues to receive updates and support.

## Why?

The successor project, `claude_usage_in_taskbar`, already needed to live in
the Windows system tray and talk to Claude, so folding the remote-control
launcher into it removed a duplicated tray icon, a duplicated startup entry,
and a duplicated Python runtime. On top of the original feature set, the new
app offers:

- The same automatic `claude --remote-control` channel inside an Obsidian
  vault on boot.
- Multi-vault / multi-project support (run more than one vault at a time).
- Live instance tracking in the tray menu so you can see which projects are
  currently connected.
- Shared session + notification infrastructure with the Claude usage meter,
  so only one tray icon is needed.

## Migration

- Download the latest
  [claude_usage_in_taskbar](https://github.com/SirBepy/claude_usage_in_taskbar)
  release from the Releases page.
- Run it. On first launch it detects an existing `obsidian_claude_remote`
  install and offers to **Import** your vault choice and startup settings
  in one click.
- Once imported, open the tray menu and confirm the automated channel is
  listed as **Running** for your vault.
- Uninstall the old app:
  - Quit the `obsidian_claude_remote` tray app (right-click tray icon ->
    Quit).
  - Delete the `obsidian_claude_remote.lnk` from
    `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\` so it no
    longer launches on boot.
  - Delete `obsidian_claude_remote.exe` from wherever you placed it.
  - Optional: delete `%APPDATA%\obsidian_claude_remote\` and
    `%LOCALAPPDATA%\obsidian_claude_remote\` to clear leftover config and
    logs.

## Issues / questions

File new issues against
[claude_usage_in_taskbar](https://github.com/SirBepy/claude_usage_in_taskbar/issues)
rather than this archived repo.
