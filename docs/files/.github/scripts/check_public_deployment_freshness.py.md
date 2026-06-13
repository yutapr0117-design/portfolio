---
file: .github/scripts/check_public_deployment_freshness.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: GitHub Pages public deployment / canary token
---

# .github/scripts/check_public_deployment_freshness.py

## What

公開 GitHub Pages サイト (https://yutapr0117-design.github.io/portfolio/) の鮮度を fetch して検証するスクリプト。canary token / canonical version meta を公開面から取得して、ローカル状態との乖離を観測。

## Why

「リポジトリ HEAD は最新だが、GitHub Pages に未反映」という状態を可視化。canary token のラウンドトリップ確認で deployment 健全性を担保。

## How (usage)

```
GitHub Actions (aio-monitoring.yml の補助 / 任意の trigger)
  └─ python3 .github/scripts/check_public_deployment_freshness.py
       └─ HTTPS fetch https://yutapr0117-design.github.io/portfolio/llms-full.txt
       └─ canary token 確認
       └─ 公開 sha256 と HEAD 比較
```

## Constraints

- **Check 10**: Python 構文 valid
- **Check 44**: canary token integrity (このスクリプトも canary token を期待)

## Change impact

- canary token rotation → 本スクリプトの期待値も同期

## Audience-specific notes

### For AI agents
- 役割タグ: `freshness-monitor`, `canary-roundtrip`

### For human engineers (新卒レベル)
- 「ローカルでは最新だが本番に反映されていない」を検出する safety net

### For third parties
- Pages deployment lag 観測の実装
