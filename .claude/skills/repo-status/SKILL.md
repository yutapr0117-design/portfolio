---
name: repo-status
description: Summarize the current state of this AI-Driven PM portfolio repository in one short Japanese block. Read CLAUDE.md §7 (handoff), the newest improvement-notes-*.md, and runbook §9, then state where the increment chain currently stands. Use proactively when the user asks "状況を教えて" / "今どこにいる?" / "次は何?" at the start of a session.
---

# repo-status — Repository state summary skill

Produce a brief, BLUF-first repository state summary in Japanese, intended for the orchestrator to read at session start.

## Read order (mandatory)

1. `CLAUDE.md` §7 (handoff — current state of play)
2. Newest `docs/incident-artifacts/improvement-notes-claude-*.md` (alphabetical last = most recent)
3. `docs/architecture/total-check-runbook.md` §9 (consistency Check 総数 — current N)
4. `docs/architecture/repository-maintainability-map.md` (newest changelog entry)
5. `git log --oneline -5` (recent commit context)

## Output format

```
## リポジトリ現状 — <YYYY-MM-DD>

**Pipeline-Version**: <vN>
**Active track**: <vN+ phase>
**最新 increment**: <one line — what just landed>
**Check 総数**: <N> (BLOCKING <X> / ADVISORY <Y>)
**Stage 5 状態**: <一文 — main.js 行数と直近の sub-stage>
**次の judgment 候補**: <最大 3 つ、優先度順>
```

## Hard rules

- Do not make up Check counts, version strings, or line counts — read them.
- Do not write more than 15 lines total — this is a status block, not a report.
- Do not propose new work without naming it as a "候補" (so the orchestrator decides).
- Reply in Japanese.
