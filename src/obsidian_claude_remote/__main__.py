import atexit
import os
import sys

from . import config, launcher, startup, vault_detector
from .logger import log
from .picker import pick_vault
from .tray import build_icon


def _paths_equal(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return False
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def ensure_vault(cfg: dict) -> str | None:
    if cfg.get("vault_path"):
        return cfg["vault_path"]
    vaults = vault_detector.detect()
    chosen = pick_vault(vaults)
    if not chosen:
        log.warning("user cancelled vault picker, exiting")
        return None
    cfg["vault_path"] = chosen
    config.save(cfg)
    return chosen


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
    chosen = pick_vault(vaults)
    if not chosen or chosen == cfg.get("vault_path"):
        return
    cfg["vault_path"] = chosen
    config.save(cfg)
    launcher.restart(chosen)


def on_restart(cfg: dict) -> None:
    if cfg.get("vault_path"):
        launcher.restart(cfg["vault_path"])


def on_quit() -> None:
    launcher.kill()


def main() -> int:
    log.info("=== obsidian_claude_remote starting ===")
    cfg = config.load()

    vault = ensure_vault(cfg)
    if not vault:
        return 1

    ensure_startup(cfg)
    launcher.launch(vault)
    atexit.register(launcher.kill)

    icon = build_icon(
        on_settings=lambda: on_settings(cfg),
        on_restart=lambda: on_restart(cfg),
        on_quit=on_quit,
    )
    log.info("entering tray loop")
    icon.run()
    log.info("tray loop exited")
    return 0


if __name__ == "__main__":
    sys.exit(main())
