---
file: .github/scripts/check_aio_digests.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .well-known/aio-manifest.json / update_aio_digests.py
---

# .github/scripts/check_aio_digests.py

## What

AIO digest 連鎖検証スクリプト。`.well-known/aio-manifest.json` の `source_of_truth[].sha256` / `supporting_evidence[].sha256` / `observational_evidence[].sha256` と `.well-known/index.json` `skills[].digest` が実ファイル sha256 と一致することを検証。

## Why

C6 (AIO Integrity) の改ざん耐性を担保。digest 不一致は AIO 信号の tamper sign。`npm run check` から実行されて pre-commit で fail させる。

## How (usage)

```
npm run check
  └─ python3 .github/scripts/check_aio_digests.py
       └─ 全 manifest entry vs 実ファイル sha256 比較
       └─ 不一致 → ERROR + exit 1
       └─ 一致 → OK + exit 0
```

## Constraints

- **Check 10**: Python 構文 valid
- **exit 0 = green**: CI 全段の前提

## Change impact

- 検証ロジック変更 → 既存 manifest の互換性に影響

## Audience-specific notes

### For AI agents
- 役割タグ: `verification`, `aio-digest-chain`, `tamper-detection`

### For human engineers (新卒レベル)
- このスクリプトが落ちる = AIO 関連ファイルが編集されて digest が古いまま
- 解決: `python3 .github/scripts/update_aio_digests.py` で digest 再計算

### For third parties
- AIO 信号の tamper-evident 担保
