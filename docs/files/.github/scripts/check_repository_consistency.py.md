---
file: .github/scripts/check_repository_consistency.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/check-repository-consistency-map.md / docs/architecture/total-check-runbook.md §9
---

# .github/scripts/check_repository_consistency.py

## What

リポジトリ全体の機械強制 Check 1〜99 を一括実行する CI 中核スクリプト (約 3,600 行)。version 整合 / AIO 連鎖 / lint coverage / Stage 5 invariance / Claude Code config / Docs Phase 1+2 bijection 等を 99 個の Check で pre-commit 検証。

## Why

このリポジトリは AI 実装に全面依存しているため、`npm run verify` が exit 0 であることが安全運用の前提。99 個の Check は increment 毎に discover→document→systematize の規律で追加された invariant 群。

## How (usage)

```
npm run check (= npm run verify の一部)
  └─ python3 .github/scripts/check_repository_consistency.py
       └─ Check 1〜99 を順次実行
       └─ ERROR (BLOCKING) があれば exit 1
       └─ WARNING (ADVISORY) は exit に影響しない
       └─ 最後に "Repository consistency check passed" / "FAILED — N error(s)"
```

## Constraints

- **Check 10**: 自己の Python 構文 valid
- **Check 45**: docstring inventory ↔ `# ── N.` section header ↔ 実装の 3 者一致 (self-integrity)
- **Check 52** (ADVISORY): 3,600 行 ≤ 3,100 → over (本依頼で BUDGET 引き上げ予定)
- **Check 70**: runbook §9 の Check 総数値と実装最大 N 一致
- **Check 74**: `_lib_io.py` の 4 helper を import

## Change impact

- 新 Check 追加 → docstring inventory + `# ── N.` section header + 実装の 3 箇所同時更新 (Check 45)
- 既存 Check 修正 → 影響範囲が広いため慎重 review
- 文書同期: check-repository-consistency-map.md + total-check-runbook.md §9 + file-size-budget.md (Check 52)

## Audience-specific notes

### For AI agents
- 役割タグ: `consistency-check-monolith`, `self-integrity-protected`, `bijection-enforcer`
- Check 番号体系の唯一の真値
- helper は `_lib_io.py` に sibling 抽出済 (Plan C)

### For human engineers (新卒レベル)
- ここに Check を追加するときは `.claude/agents/check-author.md` sub-agent の手順に従う
- `npm run verify` が落ちたら大半はここの ERROR が原因

### For third parties (監査 / 採用 / 研究)
- リポジトリ全体の invariant カタログ。99 Check は AI 実装に安全に委任するための governance 機構
