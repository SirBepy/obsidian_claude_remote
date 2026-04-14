import json
import os
from pathlib import Path

from logger import log


def detect() -> list[str]:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        log.warning("APPDATA not set")
        return []
    obsidian_json = Path(appdata) / "Obsidian" / "obsidian.json"
    if not obsidian_json.exists():
        log.info("obsidian.json not found at %s", obsidian_json)
        return []
    try:
        with open(obsidian_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        vaults = data.get("vaults", {})
        paths = []
        for v in vaults.values():
            p = v.get("path")
            if p and Path(p).exists():
                paths.append(p)
        log.info("detected %d vaults", len(paths))
        return paths
    except Exception as e:
        log.error("vault detect failed: %s", e)
        return []
