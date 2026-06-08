---
description: Produce the increment deliverable in this repo's mandatory format.
---

Close out the current increment in this repo's required delivery format (in Japanese, BLUF first). Do not stop short — all four parts are mandatory:

1. **Changed-file blocks** — the complete final content of every file you changed or created (not diffs-only if a full block is clearer for the orchestrator).
2. **Alphabetical repository-relative paths, in the chat body** (not only an appendix), grouped as 新規 / 変更 / 削除. This explicit in-body path list is a hard requirement.
3. **Commit instructions + commit message** — use **explicit `git add <path> <path> …`**, never `git add .` / `-A` / `--all` (those are denied by settings). Provide a single clear commit message.
4. **Summary of decisions and reasoning** — what changed, why, what was deferred (with reason), and the verification result.

Preconditions to assert before delivering:
- `npm run verify` exits 0 (run `/verify` if unsure).
- Any new invariant is machine-enforced (a Check in `check_repository_consistency.py`) with its docstring inventory + `# ── N.` header + implementation all in sync (Check 45), and canonical docs citing changed numbers are synced.
- Files that must stay byte-identical (AIO published layer, binary, `style.css`, `main.js` unless this increment's purpose is to change them) are unchanged — prove with SHA-256 against the prior state.
- Never fabricate things that cannot be done here (real CI dispatch, Playwright baseline generation, public Pages reflection, citation counts). State them as Not-possible.
