---
file: .github/workflows/architecture-validation.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/scripts/check_repository_consistency.py
---

# .github/workflows/architecture-validation.yml

## What

main / PR 用の **メイン CI workflow**。CSP 検査 / AIO 検査 / JSON-LD 検査 / Trusted Types 検査 / version 整合 / lint:js / ESLint / Stylelint / repository consistency (Check 1-99) / binary metadata 検査 / CSP inline handler 監査の 30 step を含む。

## Why

push / pull_request で全 invariant を pre-merge 検証する **non-destructive** workflow (本番書き込みなし)。

## How (usage)

```
GitHub Actions
  ├─ on: push to main / pull_request to main
  └─ job: validate-level-constraints
       └─ setup-node@v6 (Node 24 pin) + npm ci
       └─ 30 step (CSP / AIO / JSON-LD / Stylelint / ESLint / Check 1-99 / 等)
       └─ exit 0 = mergeable
```

## Constraints

- **Check 23**: YAML 構文 valid
- **Check 55**: bash globstar 有効化 (js/**/*.js を全 leaf に展開)
- **Check 67**: top-level permissions: read 明示

## Change impact

- step 追加/削除 → CI 時間と検出能力に影響
- node-version pin 変更 → 全 workflow と package.json engines.node 同期

## Audience-specific notes

### For AI agents
- 役割タグ: `main-ci`, `non-destructive`, `30-steps`

### For human engineers (新卒レベル)
- ここが落ちる = merge できない
- 大半は `check_repository_consistency.py` の Check N: ERROR を確認

### For third parties
- AI 実装に安全に委任する CI 多層防御の実装例
