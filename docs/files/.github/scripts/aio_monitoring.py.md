---
file: .github/scripts/aio_monitoring.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/workflows/aio-monitoring.yml / docs/evidence/aio-monitoring-log.json
---

# .github/scripts/aio_monitoring.py

## What

AIO 引用効果の週次監視スクリプト。Gemini (主力) / OpenAI (任意) の AI API へ規定クエリを投げ、entity (Yuta Yokoi) への canary token 引用が観測されるかを記録。

## Why

「AIO-first 戦略の効果」は機械的計測が困難。本スクリプトは attempt log として **honest な観測** を保持 (引用ゼロでも 0 と記録)。捏造禁止。

## How (usage)

```
GitHub Actions (.github/workflows/aio-monitoring.yml)
  └─ 毎週月曜 10:00 JST + workflow_dispatch
       └─ python3 .github/scripts/aio_monitoring.py
            └─ Gemini / OpenAI に query 投げる
            └─ canary token 引用観測 → docs/evidence/aio-monitoring-log.json に append
```

## Constraints

- **Check 11**: summary dict に `enabled_engines` + `total_cited_count` キー
- **Check 25**: aio-monitoring-log.json に `evidence_policy` キー (attempt log only)
- **Check 44**: canary token 整合
- **捏造禁止**: 観測値以外を log に書かない

## Change impact

- query 内容変更 → 過去 log との比較困難に (慎重判断)
- new engine 追加 → API キー secret 追加 + summary dict 拡張

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-monitoring`, `canary-detection`, `honest-attempt-log`

### For human engineers (新卒レベル)
- 引用観測の捏造は禁止 — observed = 0 でもそのまま記録

### For third parties
- AIO 効果の honest dating 観測記録
