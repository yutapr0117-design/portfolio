---
description: Run the full verification suite and report pass/fail per layer.
allowed-tools: Bash(npm run verify), Bash(npm run check), Bash(npm run lint), Bash(npm run lint:js), Bash(npm run lint:css), Bash(python3 .github/scripts/*)
---

Run `npm run verify` and report the result concisely in Japanese:

- Overall exit code (must be 0).
- Per layer: `check` (consistency + AIO digests + binary metadata), `lint:css` (Stylelint), `lint` (ESLint — report `N errors / M warnings`), `lint:js` (`node --check`).
- If anything fails, name the exact failing check/line and the minimal fix. Do NOT attempt the fix yet — report first, then await direction unless the fix is trivial and clearly in scope.
- Do not restate counts that are already authoritative in `docs/architecture/total-check-runbook.md` §9 unless they changed; if a count changed, flag that the canonical docs need syncing (per the increment discipline).

Keep it short: this is a status check, not a report.
