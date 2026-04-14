import subprocess
import sys

import psutil

from logger import log

_proc: subprocess.Popen | None = None


def _popen_flags() -> int:
    if sys.platform != "win32":
        return 0
    return subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP


def launch(vault_path: str) -> None:
    global _proc
    if _proc is not None and _proc.poll() is None:
        log.info("launch called but process already running pid=%s", _proc.pid)
        return
    try:
        _proc = subprocess.Popen(
            ["claude", "--remote-control"],
            cwd=vault_path,
            creationflags=_popen_flags(),
            shell=True,
        )
        log.info("claude launched pid=%s cwd=%s", _proc.pid, vault_path)
    except Exception as e:
        log.error("launch failed: %s", e)
        _proc = None


def kill() -> None:
    global _proc
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


def restart(vault_path: str) -> None:
    kill()
    launch(vault_path)


def is_running() -> bool:
    return _proc is not None and _proc.poll() is None
