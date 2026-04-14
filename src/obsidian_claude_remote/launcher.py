import json
import os
import subprocess
import sys
import time
from pathlib import Path

import psutil

from .logger import log

_proc: subprocess.Popen | None = None
_hwnd: int = 0
_session_id: str | None = None


def _popen_flags() -> int:
    if sys.platform != "win32":
        return 0
    return subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP


def _find_hwnd_for_pid(pid: int) -> int:
    if sys.platform != "win32":
        return 0
    import win32gui
    import win32process

    found = {"hwnd": 0}

    def _cb(hwnd, _):
        try:
            _, wpid = win32process.GetWindowThreadProcessId(hwnd)
        except Exception:
            return True
        if wpid == pid:
            found["hwnd"] = hwnd
            return False
        return True

    try:
        win32gui.EnumWindows(_cb, None)
    except Exception:
        pass
    return found["hwnd"]


def _resolve_hwnd() -> int:
    global _hwnd
    if _proc is None:
        return 0
    for _ in range(20):
        hwnd = _find_hwnd_for_pid(_proc.pid)
        if hwnd:
            _hwnd = hwnd
            log.info("console hwnd resolved hwnd=%s pid=%s", hwnd, _proc.pid)
            return hwnd
        time.sleep(0.05)
    log.warning("console hwnd not resolved pid=%s", _proc.pid)
    return 0


def _find_claude_child_pid() -> int | None:
    if _proc is None:
        return None
    try:
        parent = psutil.Process(_proc.pid)
    except psutil.NoSuchProcess:
        return None
    try:
        for child in parent.children(recursive=True):
            try:
                name = (child.name() or "").lower()
            except psutil.Error:
                continue
            if "claude" in name or "node" in name:
                return child.pid
    except psutil.Error:
        return None
    return None


def _resolve_session_id() -> None:
    global _session_id
    sessions_dir = Path.home() / ".claude" / "sessions"
    for _ in range(15):
        pid = _find_claude_child_pid()
        if pid is not None:
            f = sessions_dir / f"{pid}.json"
            if f.exists():
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    sid = data.get("bridgeSessionId")
                    if sid:
                        _session_id = sid
                        log.info("session id resolved: %s", sid)
                        return
                except Exception as e:
                    log.warning("session json parse failed: %s", e)
        time.sleep(0.2)
    log.warning("session id not resolved within timeout")


def _post_launch_resolve() -> None:
    _resolve_hwnd()
    if _hwnd:
        hide_window()
    _resolve_session_id()


def launch(vault_path: str) -> None:
    global _proc, _hwnd, _session_id
    if _proc is not None and _proc.poll() is None:
        log.info("launch called but process already running pid=%s", _proc.pid)
        return
    prefix = os.path.basename(vault_path.rstrip("\\/")) or "ObsidianVault"
    try:
        _proc = subprocess.Popen(
            [
                "claude",
                "--remote-control",
                "--remote-control-session-name-prefix",
                prefix,
            ],
            cwd=vault_path,
            creationflags=_popen_flags(),
            shell=True,
        )
        _hwnd = 0
        _session_id = None
        log.info(
            "claude launched pid=%s cwd=%s prefix=%s",
            _proc.pid,
            vault_path,
            prefix,
        )
        import threading

        threading.Thread(
            target=_post_launch_resolve, name="launcher-resolve", daemon=True
        ).start()
    except Exception as e:
        log.error("launch failed: %s", e)
        _proc = None


def show_window() -> None:
    if sys.platform != "win32":
        return
    import win32con
    import win32gui

    hwnd = _hwnd or _resolve_hwnd()
    if not hwnd:
        log.warning("show_window: no hwnd")
        return
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        log.warning("show_window failed: %s", e)


def hide_window() -> None:
    if sys.platform != "win32":
        return
    import win32con
    import win32gui

    hwnd = _hwnd or _resolve_hwnd()
    if not hwnd:
        return
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    except Exception as e:
        log.warning("hide_window failed: %s", e)


def get_session_id() -> str | None:
    return _session_id


def get_web_url() -> str | None:
    if not _session_id:
        return None
    return f"https://claude.ai/code/{_session_id}"


def kill() -> None:
    global _proc, _hwnd, _session_id
    if _proc is None:
        return
    pid = _proc.pid
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for c in children:
            try:
                c.terminate()
            except psutil.NoSuchProcess:
                pass
        gone, alive = psutil.wait_procs(children, timeout=3)
        for c in alive:
            try:
                c.kill()
            except psutil.NoSuchProcess:
                pass
        try:
            parent.terminate()
            parent.wait(timeout=3)
        except psutil.TimeoutExpired:
            parent.kill()
        except psutil.NoSuchProcess:
            pass
        log.info("claude killed pid=%s", pid)
    except psutil.NoSuchProcess:
        log.info("claude process already gone pid=%s", pid)
    except Exception as e:
        log.error("kill failed pid=%s: %s", pid, e)
    finally:
        _proc = None
        _hwnd = 0
        _session_id = None


def restart(vault_path: str) -> None:
    kill()
    launch(vault_path)


def is_running() -> bool:
    return _proc is not None and _proc.poll() is None
