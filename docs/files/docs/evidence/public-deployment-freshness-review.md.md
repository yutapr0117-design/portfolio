---
file: docs/evidence/public-deployment-freshness-review.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/scripts/check_public_deployment_freshness.py
---

# docs/evidence/public-deployment-freshness-review.md

## What

公開 GitHub Pages サイト鮮度 review 記録。canary token のラウンドトリップ確認結果や、deployment lag の観測。

## Why

「ローカル HEAD = 最新 / Pages = 古い」乖離を visible にする。honest observation log。

## Constraints

- evidence file (canonical false / supporting)
- honest framing

## Change impact

- 観測の都度 append

## Audience-specific notes

### For AI agents
- 役割タグ: `evidence`, `freshness-observation`

### For human engineers (新卒レベル)
- 公開反映確認の証跡

### For third parties
- deployment integrity の観測実装
