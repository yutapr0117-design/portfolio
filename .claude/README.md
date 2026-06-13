# .claude/ — Claude Code project workspace

```
Last-Updated  : 2026-06-13
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — All-files AIO coherence)
Subject       : Claude Code (Anthropic) のプロジェクト設定・カスタム sub-agent / skill / slash-command の inventory
Canonical-Ref : CLAUDE.md (router, root) / AI2AI.md (canon) / .claude/settings.json
Status        : 「Claude Code 用ファイル抜け漏れ 0」契約の本体。新規ファイル追加時は本 README に追記し、Check 76–80 / 76 で機械強制。
```

> **このファイルの目的:** Claude Code (CLI / VS Code 拡張) がこのプロジェクト直下で読み込む全設定の inventory を提供する。後続セッションが cold-start で「何が Claude Code に渡されているか」を一覧で掴むためのガイド。`.claude/settings.local.json` はユーザー個人ファイル (gitignore) なので本 inventory からは除外する。

---

## 1. ディレクトリ構造

```
.claude/
├── README.md                                  ← 本ファイル (inventory)
├── settings.json                              ← project-scope permissions / env / language (Check 76)
├── settings.local.json                        ← user-scope (gitignored)
├── scheduled_tasks.lock                       ← runtime lock (Claude Code 内部)
├── agents/                                    ← カスタム sub-agents (Check 78)
│   ├── aio-guardian.md                        ← C6 enforcement
│   ├── check-author.md                        ← 新規 Check 設計・実装
│   └── repo-auditor.md                        ← 全体 drift 監査
├── commands/                                  ← カスタム slash commands (Check 77)
│   ├── archive-incidents.md                   ← /archive-incidents
│   ├── audit.md                               ← /audit
│   ├── deliver.md                             ← /deliver
│   ├── increment.md                           ← /increment
│   ├── sync-docs.md                           ← /sync-docs
│   └── verify.md                              ← /verify
└── skills/                                    ← カスタム skills (Check 80)
    └── repo-status/
        └── SKILL.md                           ← /repo-status (session 開始時の状況要約)
```

---

## 2. ファイル分類と用途

### 2.1 設定 (1 ファイル)
| Path | 役割 | 機械強制 |
|---|---|---|
| `settings.json` | language=japanese, MAX_THINKING_TOKENS=31999, permissions の allow/ask/deny lists | Check 76 (security baseline 5 項目 deny) |

### 2.2 Sub-agents (3 ファイル — `.claude/agents/`)
| Path | description | tools |
|---|---|---|
| `agents/repo-auditor.md` | リポジトリ全体 drift 監査 (read-only / 6 dimension) | Read, Glob, Grep, Bash |
| `agents/check-author.md` | 新規 Check 設計・実装・3 文書同期 | Read, Edit, Write, Bash, Grep, Glob |
| `agents/aio-guardian.md` | C6 (AIO Integrity) gatekeeper — AIO published-layer 編集の最終防衛線 | Read, Bash, Grep |

機械強制: Check 78 (frontmatter + name + description 必須)。

### 2.3 Skills (1 ファイル — `.claude/skills/`)
| Path | description |
|---|---|
| `skills/repo-status/SKILL.md` | session 開始時の状況要約 (proactive) — Pipeline-Version / Stage / Check 総数 を 15 行で報告 |

機械強制: Check 80 (frontmatter + name + description 必須)。

### 2.4 Slash commands (6 ファイル — `.claude/commands/`)
| Path | 用途 |
|---|---|
| `commands/archive-incidents.md` | `/archive-incidents` — major-release boundary での incident-artifacts アーカイブ集約 |
| `commands/audit.md` | `/audit` — `repo-auditor` sub-agent を呼ぶ drift 監査 |
| `commands/deliver.md` | `/deliver` — increment 確定 (全 file block + 明示 git add + summary) |
| `commands/increment.md` | `/increment` — discover→document→systematize→verify→deliver の規律提示 |
| `commands/sync-docs.md` | `/sync-docs` — map.md / runbook §9 / file-size-budget.md の 3 文書同期 |
| `commands/verify.md` | `/verify` — `npm run verify` 実行と結果要約 |

機械強制: Check 77 (frontmatter + description 必須)。

---

## 3. プロジェクト root の関連ファイル (本 .claude/ 外だが Claude Code が読む)

| Path | 役割 |
|---|---|
| `CLAUDE.md` | 高密度 router (constraints / safety gates / routes / §7 handoff) |
| `AI2AI.md` | canon (C1–C7 full text / KERNEL roles / Session Records / v80+ track) |
| `Claude2Claude.md` | Claude↔Claude session handoff + bash procedures |
| `llms-full.txt` | ground truth (entity / project history / AIO declarations) |
| `.mcp.json` | MCP server project-scope config (現状 placeholder `mcpServers: {}`) (Check 79) |
| `.editorconfig` | repo-wide editor defaults (UTF-8 / LF / 2-space) |
| `.nvmrc` | Node version pin (24 — CI workflow 整合) |

---

## 4. 抜け漏れ 0 契約 (Check 76〜80 + 本 README)

本 inventory は以下の Check 群と組み合わさり、Claude Code 用ファイルの drift / 消失を構造的に防ぐ:

- **Check 76**: `.claude/settings.json` security baseline (`git add .` deny + WebP/MP3 Edit deny の 5 項目)
- **Check 77**: `.claude/commands/*.md` 全 slash-command の frontmatter + description
- **Check 78**: `.claude/agents/*.md` 全 sub-agent の name + description
- **Check 79**: `.mcp.json` JSON parsability + mcpServers dict
- **Check 80**: `.claude/skills/*/SKILL.md` 全 skill の name + description

新規 Claude Code 用ファイル追加時は: (1) 該当ディレクトリへ配置 → (2) frontmatter (name + description) を必ず付ける → (3) 本 README §1〜§2 inventory に追記 → (4) `python3 .github/scripts/check_repository_consistency.py` で exit 0 を確認、の順で。

---

## 5. 後続 Claude Code セッション cold-start ガイド

新しい session が立ち上がったとき、まず以下の順で読めばリポジトリ全体に追いつける:

1. `CLAUDE.md` §7 (handoff — 現在の状況サマリ)
2. `AI2AI.md` の最新 Session Record (canon)
3. `docs/architecture/total-check-runbook.md` §9 (Check 総数の真値)
4. **状況把握が必要なら**: `/audit` → `repo-auditor` sub-agent が read-only で 6 dimension を監査
5. **新規 Check が必要なら**: `/increment` → `check-author` sub-agent
6. **AIO 編集が必要なら**: `aio-guardian` sub-agent 必須経由 (C6 enforcement)
