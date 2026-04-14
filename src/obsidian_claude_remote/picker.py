import os
import sys
import threading
from pathlib import Path
from typing import Callable, Optional

import webview

from .logger import log

WINDOW_TITLE = "obsidian_claude_remote - pick vault"

_host_ready = threading.Event()


def _resource_path(rel: str) -> str:
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return os.path.join(base, rel)
    return str(Path(__file__).resolve().parent / rel)


def _icon_path() -> Optional[str]:
    candidates = [
        _resource_path("icon.ico"),
        str(Path(__file__).resolve().parents[2] / "icon.ico"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def _set_window_icon(title: str, ico: str) -> None:
    try:
        import win32api
        import win32con
        import win32gui

        hwnd = 0
        for _ in range(50):
            hwnd = win32gui.FindWindow(None, title)
            if hwnd:
                break
            threading.Event().wait(0.05)
        if not hwnd:
            log.warning("picker window hwnd not found, icon not set")
            return
        big = win32gui.LoadImage(
            0, ico, win32con.IMAGE_ICON, 32, 32, win32con.LR_LOADFROMFILE
        )
        small = win32gui.LoadImage(
            0, ico, win32con.IMAGE_ICON, 16, 16, win32con.LR_LOADFROMFILE
        )
        win32api.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, big)
        win32api.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, small)
    except Exception as e:
        log.warning("failed to set picker icon: %s", e)


class _Api:
    def __init__(self, vaults: list[str], result: dict):
        self._vaults = vaults
        self._result = result
        self.window: Optional[webview.Window] = None

    def get_vaults(self) -> list[str]:
        return list(self._vaults)

    def browse(self) -> Optional[str]:
        if not self.window:
            return None
        picked = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        if not picked:
            return None
        return picked[0]

    def submit(self, path: Optional[str]) -> None:
        self._result["path"] = path
        if self.window:
            self.window.destroy()


def start_host(on_ready: Callable[[], None]) -> None:
    """Start the pywebview event loop on the current (main) thread.

    Creates a hidden persistent window so the loop stays alive across
    multiple picker invocations. Calls on_ready from a background thread
    once the loop is running. Returns when shutdown() is called.
    """
    webview.create_window(
        "__ocr_host__",
        _resource_path("ui/blank.html"),
        hidden=True,
        width=1,
        height=1,
    )

    def _fire_ready():
        _host_ready.set()
        try:
            on_ready()
        except Exception:
            log.exception("on_ready callback failed")

    webview.start(_fire_ready)


def shutdown() -> None:
    """Destroy all webview windows so start_host returns."""
    for w in list(webview.windows):
        try:
            w.destroy()
        except Exception:
            pass


def show_picker(vaults: list[str]) -> Optional[str]:
    """Show the picker dialog. Safe to call from any thread after start_host."""
    if not _host_ready.wait(timeout=10):
        log.error("webview host never became ready")
        return None

    result: dict = {"path": None}
    api = _Api(vaults, result)
    html_path = _resource_path("ui/picker.html")

    window = webview.create_window(
        WINDOW_TITLE,
        html_path,
        js_api=api,
        width=560,
        height=420,
        resizable=True,
        background_color="#111111",
    )
    api.window = window

    ico = _icon_path()
    if ico:
        def _on_shown():
            threading.Timer(0.1, lambda: _set_window_icon(WINDOW_TITLE, ico)).start()
        window.events.shown += _on_shown

    done = threading.Event()
    window.events.closed += lambda: done.set()
    done.wait()
    return result["path"]
