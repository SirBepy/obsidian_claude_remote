import json
import os
import sys
from pathlib import Path

from logger import log

APP_NAME = "obsidian_claude_remote"

DEFAULT = {
    "vault_path": None,
    "auto_registered_startup": False,
}


def config_dir() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    p = Path(base) / APP_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def config_path() -> Path:
    return config_dir() / "config.json"


def load() -> dict:
    path = config_path()
    if not path.exists():
        return dict(DEFAULT)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(DEFAULT)
        merged.update({k: data.get(k, v) for k, v in DEFAULT.items()})
        return merged
    except Exception as e:
        log.warning("config load failed, using defaults: %s", e)
        return dict(DEFAULT)


def save(data: dict) -> None:
    path = config_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        log.info("config saved to %s", path)
    except Exception as e:
        log.error("config save failed: %s", e)
