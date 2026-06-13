---
file: .claude/agents/aio-guardian.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C6) / Check 78
---

# .claude/agents/aio-guardian.md

## What

AIO published-layer 編集の **C6 enforcement** sub-agent。orchestrator 承認の有無を確認し、pre-edit checklist (canary / canonical_url / origin alignment 等) と post-edit checklist (digest 再計算 / 各 check_*.py 実行) を機械的に走らせる。

## Why

C6 (AIO Integrity) は最重要制約。直接 main thread で AIO 編集を行うと忘れがちな手順 (digest 連鎖 / mirror 同期等) を sub-agent に責務委譲することで「必ず通る」運用を担保。

## How (usage)

```
main agent
  └─ Task tool で aio-guardian を起動
       └─ orchestrator approval check
       └─ pre-edit checklist (canary / origin / mirror byte-identity)
       └─ APPROVE / REJECT を返す
       └─ APPROVE 後に semantic 編集 → post-edit checklist
```

## Constraints

- **Check 78**: frontmatter (name + description)
- tools: Read / Bash / Grep のみ (編集権なし、検査専用)

## Change impact

- checklist 変更 → C6 enforcement の厳格度が変わる

## Audience-specific notes

### For AI agents
- 役割タグ: `c6-guardian`, `aio-gatekeeper`, `pre-post-checklist`

### For human engineers (新卒レベル)
- AIO 編集時は必ずこの agent を経由 — semantic drift / digest 漏れを防ぐ

### For third parties
- AI agent 階層での権限分離設計の実装例
