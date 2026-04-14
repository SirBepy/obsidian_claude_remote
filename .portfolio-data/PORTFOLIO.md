## The What

A tiny Windows tray app that auto-launches Claude Code with `--remote-control` inside an Obsidian vault on PC boot, so the vault shows up as a remote session inside the Claude phone app. First run pops a picker listing Obsidian vaults detected from `%APPDATA%\Obsidian\obsidian.json`. Pick one, and from then on the app sits in the tray, spawns `claude` silently inside the chosen vault, and registers a shortcut in the Windows Startup folder so it keeps working across reboots with zero terminal interaction.

## The Why

The Claude phone app can already drive a Claude Code session running on a PC, but only if someone manually launches `claude --remote-control` from the right directory every time the machine reboots. That defeats the point of using the phone app in the first place. This closes the loop: boot the PC, and the vault is reachable from your phone. No terminal, no remembering the command, no broken session after an update.

## The How

The `--remote-control` flag displays sessions by folder name, which collides when multiple vaults are running, so the launcher passes `--remote-control-session-name-prefix` built from the vault directory name to keep sessions distinguishable. Killing the subprocess cleanly on Quit needed `psutil` to walk the process tree, because `claude` on Windows is a `.cmd` shim spawned via `shell=True`, and a plain `terminate` on the parent leaves orphan node processes behind. Startup registration only activates when frozen by PyInstaller, so running from source during development does not pollute the Startup folder.
