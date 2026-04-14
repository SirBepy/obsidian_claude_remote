import os
import sys
from pathlib import Path

import pystray
from PIL import Image

from logger import log


def resource_path(rel: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel)


def _load_icon_image() -> Image.Image:
    candidates = [
        resource_path("assets/images/favicon.png"),
        resource_path("favicon.png"),
        str(Path(__file__).parent / "assets" / "images" / "favicon.png"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return Image.open(c)
    log.warning("icon image not found, using blank")
    return Image.new("RGBA", (64, 64), (124, 58, 237, 255))


def build_icon(on_settings, on_restart, on_quit) -> pystray.Icon:
    image = _load_icon_image()
    menu = pystray.Menu(
        pystray.MenuItem("Settings", lambda icon, item: on_settings()),
        pystray.MenuItem("Restart Claude", lambda icon, item: on_restart()),
        pystray.MenuItem(
            "Quit", lambda icon, item: (on_quit(), icon.stop())
        ),
    )
    return pystray.Icon(
        "obsidian_claude_remote",
        image,
        "obsidian_claude_remote - running",
        menu,
    )
