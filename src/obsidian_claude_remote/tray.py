import os
import sys
from pathlib import Path

import pystray
from PIL import Image

from . import __version__, launcher
from .logger import log


def resource_path(rel: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel)


def _load_icon_image() -> Image.Image:
    candidates = [
        resource_path("assets/images/favicon.png"),
        resource_path("favicon.png"),
        str(Path(__file__).resolve().parents[2] / "assets" / "images" / "favicon.png"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return Image.open(c)
    log.warning("icon image not found, using blank")
    return Image.new("RGBA", (64, 64), (124, 58, 237, 255))


def build_icon(
    on_show_terminal, on_open_web, on_settings, on_restart, on_quit
) -> pystray.Icon:
    image = _load_icon_image()
    menu = pystray.Menu(
        pystray.MenuItem(
            "Show terminal",
            lambda icon, item: on_show_terminal(),
            default=True,
        ),
        pystray.MenuItem(
            "Open in web",
            lambda icon, item: on_open_web(),
            visible=lambda item: launcher.get_web_url() is not None,
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Settings", lambda icon, item: on_settings()),
        pystray.MenuItem("Restart Claude", lambda icon, item: on_restart()),
        pystray.MenuItem(
            "Quit", lambda icon, item: (on_quit(), icon.stop())
        ),
    )
    return pystray.Icon(
        "obsidian_claude_remote",
        image,
        f"Obsidian Claude Remote - {__version__}",
        menu,
    )
