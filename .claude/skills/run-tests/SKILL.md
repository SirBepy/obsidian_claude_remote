---
name: run-tests
description: Project-level smoke test for obsidian_claude_remote. Invoked by /commit before staging.
---

# /run-tests (project-level)

> Import-check smoke test. Catches syntax errors, broken relative imports, and missing deps. Does not cover runtime logic (full tray launch is interactive and cannot run unattended).

## Steps

1. From the repo root, run:

```
python scripts/smoke_test.py
```

2. Exit code 0 = pass. Exit code non-zero = fail.

3. On failure: print the full output from the script so the caller can see exactly which module broke and why. Do not attempt to fix automatically - the /commit flow will abort and surface the error to the user.

## Notes

- Never uses `-m` module form because the script inserts `src/` onto `sys.path` itself - users do not need `PYTHONPATH=src` or `pip install -e .` set up for the smoke test to run.
- Full app launch (`python -m obsidian_claude_remote`) is intentionally **not** run: it spawns a tray loop + the `claude` subprocess, which cannot terminate on its own.
