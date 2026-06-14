---
file: docs/architecture/total-check-runbook.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/scripts/check_repository_consistency.py / Check 70
---

# docs/architecture/total-check-runbook.md

## What

`npm run verify` 検証 runbook + §9 「authoritative measured numbers」(Check 総数 = 99 / sitemap loc = 17 / JSON-LD / YAML / XML count 等)。

## Why

CI 各層 (check / lint:css / lint / lint:js) の期待値と現状実測値を単一ソースで管理。Check 70 が runbook §9 値と実装最大 Check 番号の整合を機械強制。

## How (usage)

session 復帰時に §9 を読んで現在 Check 総数を把握。新 Check 追加時に §9 を同期。

## Constraints

- **Check 70**: §9 の Check 総数 == 実装最大 Check 番号

## Change impact

- 新 Check 追加 → §9 の Check 総数 + 説明追記 (Check 70)

## Audience-specific notes

### For AI agents
- 役割タグ: `runbook`, `measured-numbers`, `check-count-source`

### For human engineers (新卒レベル)
- 「Check 何個あるんだっけ?」のときに見る

### For third parties
- 99 Check の運用真値
