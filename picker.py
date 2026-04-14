import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional


def pick_vault(vaults: list[str]) -> Optional[str]:
    result: dict[str, Optional[str]] = {"path": None}

    root = tk.Tk()
    root.title("obsidian_claude_remote - pick vault")
    root.geometry("520x360")
    root.attributes("-topmost", True)

    tk.Label(
        root,
        text="Pick an Obsidian vault to host Claude Code:",
        anchor="w",
        padx=12,
        pady=8,
    ).pack(fill="x")

    listbox = tk.Listbox(root, height=10)
    for v in vaults:
        listbox.insert(tk.END, v)
    if vaults:
        listbox.select_set(0)
    listbox.pack(fill="both", expand=True, padx=12, pady=4)

    if not vaults:
        tk.Label(
            root,
            text="No vaults auto-detected. Use Browse to pick one manually.",
            fg="#888",
            padx=12,
        ).pack(fill="x")

    def on_browse() -> None:
        path = filedialog.askdirectory(title="Select vault folder")
        if path:
            listbox.insert(tk.END, path)
            listbox.select_clear(0, tk.END)
            listbox.select_set(tk.END)

    def _close() -> None:
        try:
            root.quit()
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass

    def on_ok() -> None:
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Pick vault", "Select a vault first.")
            return
        result["path"] = listbox.get(sel[0])
        _close()

    def on_cancel(*_args) -> None:
        result["path"] = None
        _close()

    btns = tk.Frame(root)
    btns.pack(fill="x", padx=12, pady=8)
    tk.Button(btns, text="Browse...", command=on_browse).pack(side="left")
    tk.Button(btns, text="Cancel", command=on_cancel).pack(side="right")
    tk.Button(btns, text="OK", command=on_ok).pack(side="right", padx=4)

    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.bind("<Escape>", on_cancel)
    root.mainloop()
    return result["path"]
