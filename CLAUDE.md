## Project

Type: other (Python 3.10+ Windows desktop tray app)
Deploy: other (GitHub Releases via `.github/workflows/build-release.yml`, PyInstaller onefile exe)

## Structure

src-layout: `src/obsidian_claude_remote/` package (entry `__main__.py`), `scripts/build.py` + `scripts/generate_icon.py` + `scripts/_pyinstaller_entry.py`, `assets/images/favicon.png`, `icon.ico` at root, `pyproject.toml`, `requirements.txt`.

## Rules

- Relative imports only inside the package (`from .logger import log`), never `from logger import log`.
- Run from source as `python -m obsidian_claude_remote` (requires `src/` on PYTHONPATH, or `pip install -e .`). Never `python main.py`.
- Build with `python scripts/build.py` from project root, not from inside `scripts/`.
- Runtime config lives in `%APPDATA%\obsidian_claude_remote\config.json`, logs in `%LOCALAPPDATA%\obsidian_claude_remote\app.log`. Never write config next to the exe.
- `launcher.py` must keep `shell=True` on Windows: `claude` is a `.cmd` shim, Popen without shell raises FileNotFoundError.
- Startup `.lnk` registration is gated on `sys.frozen` so dev runs never touch the Windows Startup folder.
- Icon regeneration: `python scripts/generate_icon.py` writes both `assets/images/favicon.png` and `icon.ico` in one shot via Pillow.
