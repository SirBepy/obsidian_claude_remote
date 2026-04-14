import os
from pathlib import Path

from .logger import log

SHORTCUT_NAME = "obsidian_claude_remote.lnk"


def startup_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA not set")
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
    )


def shortcut_path() -> Path:
    return startup_dir() / SHORTCUT_NAME


def is_registered() -> bool:
    return shortcut_path().exists()


def register(target_exe: str) -> None:
    try:
        from win32com.client import Dispatch
    except ImportError as e:
        log.error("pywin32 missing, cannot register startup: %s", e)
        return
    try:
        startup_dir().mkdir(parents=True, exist_ok=True)
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path()))
        shortcut.Targetpath = target_exe
        shortcut.WorkingDirectory = str(Path(target_exe).parent)
        shortcut.WindowStyle = 7
        shortcut.Description = "obsidian_claude_remote tray"
        shortcut.save()
        log.info("startup shortcut registered at %s", shortcut_path())
    except Exception as e:
        log.error("register startup failed: %s", e)


def unregister() -> None:
    try:
        sp = shortcut_path()
        if sp.exists():
            sp.unlink()
            log.info("startup shortcut removed")
    except Exception as e:
        log.error("unregister failed: %s", e)
