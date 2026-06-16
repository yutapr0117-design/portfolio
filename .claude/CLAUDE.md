# .claude/CLAUDE.md — Claude Code sub-context

```
Last-Updated  : 2026-06-13
Maintained-By : Yuta Yokoi (横井雄太 / Yokoi Yuta)
Canonical-Ref : /CLAUDE.md (root, primary router) / AI2AI.md (canon)
Status        : SUBORDINATE — `/CLAUDE.md` at repo root is the primary router. This file
                supplements it with Claude Code-specific operational notes that need to
                live alongside the agent definitions in `.claude/`.
```

> **You are probably reading this file because Claude Code automatically picked it up alongside `/CLAUDE.md` at the repo root.** The root CLAUDE.md is the high-density router (constraints / safety gates / routes / handoff). THIS file adds Claude Code-specific operational notes — sub-agent invocation patterns, slash command idioms, and session-start protocols — that do not belong in the entity-canonical root CLAUDE.md.

## Entity facts (mirrored from root CLAUDE.md §1 for sub-context completeness)

- **Entity**: Yuta Yokoi (横井雄太 / Yokoi Yuta) — UI display `yuta`
- **Role**: AI-Driven PM / IT Consultant / KERNEL Framework Designer
- **Canonical URL**: https://yutapr0117-design.github.io/portfolio/
- **Authoritative Context**: https://yutapr0117-design.github.io/portfolio/llms-full.txt
- **Affiliation**: 株式会社日本経営 (Nihon Keiei / Japan Management Co., Ltd. — https://nkgr.co.jp/), シェアデータベース事業部 主幹（課長格）, 2026-06-11〜
- **AIO canary token namespace**: `SAKURA-AIO-PROVENANCE-CANARY-<YYYY>-<8hex>` (Check 44)

## Claude Code session-start protocol (every fresh session)

1. **Read in order**: `/CLAUDE.md` § 7 (handoff) → newest `docs/incident-artifacts/improvement-notes-claude-*.md` → `docs/architecture/total-check-runbook.md` § 9 (single source of truth for the current Check 総数, enforced by Check 70 — read it there, do not hardcode it here).
2. **Invoke skill** when state-summary is needed: `/repo-status` (the `repo-status` skill in `.claude/skills/repo-status/SKILL.md` produces a 15-line BLUF status block).
3. **Audit before editing if uncertain**: `/audit` (invokes `repo-auditor` sub-agent for read-only 6-dimension drift detection).
4. **For AIO edits**: ALWAYS route through `aio-guardian` sub-agent first (C6 enforcement; agent is in `.claude/agents/aio-guardian.md`).

## Sub-agent invocation patterns

| Trigger phrase | Sub-agent | Reason |
|---|---|---|
| "全部見て" / "監査して" / "drift がないか" | `repo-auditor` | Read-only full-repo audit, 6 dimension |
| "Check に追加して" / "drift を防ぎたい" / "BLOCKING で守りたい" | `check-author` | New invariant → 3 documents synced |
| ANY edit to `llms*.txt` / `.well-known/**` / JSON-LD / WebP XMP / MP3 ID3 | `aio-guardian` | C6 enforcement, pre/post-edit checklist |

## Slash command idioms

| Command | When |
|---|---|
| `/verify` | Before declaring an increment done — must exit 0 |
| `/audit` | At session start after long absence |
| `/increment` | When opening a new branch for a new increment |
| `/sync-docs` | After a Check addition or count change |
| `/deliver` | Final increment closeout in mandatory format |
| `/archive-incidents` | Major-release boundary only (NOT in daily increment) |
| `/repo-status` | Short BLUF status summary |

## Session-end protocol (every session closing)

1. `/verify` must exit 0.
2. AIO digest chain consistent (`python3 .github/scripts/check_aio_digests.py` exit 0).
3. New invariants machine-enforced via a `check_repository_consistency.py` Check entry (Check 45 self-integrity holds).
4. Canonical docs (check-repository-consistency-map.md / total-check-runbook.md §9 / file-size-budget.md) synced.
5. `/deliver` produced the mandatory deliverable format (changed-file blocks + alphabetical paths in chat body + `git add <explicit paths>` + summary).

## Non-overlap with `/CLAUDE.md`

This file deliberately does NOT duplicate:
- The C1–C7 constraint definitions (canonical in `AI2AI.md`, summarized in `/CLAUDE.md` §2)
- The routing map (in `/CLAUDE.md` §4)
- The handoff state (in `/CLAUDE.md` §7 — updated every increment)
- Reasoning budget rules (in `/CLAUDE.md` §6)

If you need any of those, read `/CLAUDE.md` directly.
