import atexit
import os
import sys
import threading
import webbrowser

from . import config, launcher, picker, startup, vault_detector
from .logger import log
from .tray import build_icon


def _paths_equal(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return False
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def ensure_startup(cfg: dict) -> None:
    if not getattr(sys, "frozen", False):
        log.info("running from source, skipping startup registration")
        return
    target = sys.executable
    current = startup.registered_target()
    if _paths_equal(current, target):
        return
    if current:
        log.info(
            "startup .lnk target mismatch, re-registering (old=%s new=%s)",
            current,
            target,
        )
    startup.register(target)
    cfg["auto_registered_startup"] = True
    config.save(cfg)


def on_settings(cfg: dict) -> None:
    vaults = vault_detector.detect()
    chosen = picker.show_picker(vaults)
    if not chosen or chosen == cfg.get("vault_path"):
        return
    cfg["vault_path"] = chosen
    config.save(cfg)
    launcher.restart(chosen)


def on_restart(cfg: dict) -> None:
    if cfg.get("vault_path"):
        launcher.restart(cfg["vault_path"])


def _bootstrap(cfg: dict) -> None:
    vault = cfg.get("vault_path")
    if not vault:
        vaults = vault_detector.detect()
        vault = picker.show_picker(vaults)
        if not vault:
            log.warning("user cancelled vault picker, exiting")
            picker.shutdown()
            return
        cfg["vault_path"] = vault
        config.save(cfg)

    ensure_startup(cfg)
    launcher.launch(vault)
    atexit.register(launcher.kill)

    def on_quit():
        launcher.kill()
        picker.shutdown()

    def on_open_web():
        url = launcher.get_web_url()
        if url:
            log.info("opening web: %s", url)
            webbrowser.open(url)
        else:
            log.warning("open_web: session id not yet available")

    icon = build_icon(
        on_show_terminal=launcher.show_window,
        on_open_web=on_open_web,
        on_settings=lambda: on_settings(cfg),
        on_restart=lambda: on_restart(cfg),
        on_quit=on_quit,
    )
    log.info("entering tray loop")
    threading.Thread(target=icon.run, name="tray", daemon=True).start()


def main() -> int:
    log.info("=== obsidian_claude_remote starting ===")
    cfg = config.load()

    def _on_ready():
        threading.Thread(
            target=_bootstrap, args=(cfg,), name="bootstrap", daemon=True
        ).start()

    picker.start_host(_on_ready)
    log.info("webview host exited")
    return 0


if __name__ == "__main__":
    sys.exit(main())
