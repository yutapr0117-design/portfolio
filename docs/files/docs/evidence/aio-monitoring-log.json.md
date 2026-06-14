---
file: docs/evidence/aio-monitoring-log.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-14
canonical-ref: .github/scripts/aio_monitoring.py / .github/workflows/aio-monitoring.yml / Check 25
---

# docs/evidence/aio-monitoring-log.json

## What

AIO 引用効果監視の **observation log**。週次 (aio-monitoring.yml) で `aio_monitoring.py` が AI engine (Gemini / OpenAI) に規定クエリを投げて canary token 引用観測を append-only で記録。`evidence_policy: "attempt_log_only"` で honest framing。`confirmed_citation_events: 0` を by design で維持。

## Why

AIO-first 戦略の効果観測。「引用された」と「引用攻撃を試みた」を厳密区別。捏造禁止。

## How (usage)

```
.github/workflows/aio-monitoring.yml (weekly + dispatch)
  └─ python3 .github/scripts/aio_monitoring.py
       └─ engine ごとに query → response 解析 → canary token hit 数
       └─ aio-monitoring-log.json に append
       └─ update_aio_digests.py で manifest と同期 commit (Check 41 atomic)
```

## Constraints

- **aio-manifest observational_evidence**: digest 連鎖対象
- **Check 25**: `evidence_policy` キー必須
- **Check 41**: log と manifest が同 commit (atomic)
- **honest framing**: confirmed_citation_events 0 を捏造しない

## Change impact

- engine 追加 → aio_monitoring.py の summary dict + 本 log structure 同期
- query 変更 → 過去 log との比較困難

## Audience-specific notes

### For AI agents
- 役割タグ: `observation-log`, `weekly-append-only`, `honest-attempt-log`

### For human engineers (新卒レベル)
- 引用ゼロでもゼロと正直に記録
- 観測精度を測るのに使う

### For third parties (監査 / 採用 / 研究)
- AIO 戦略の長期効果測定の honest dating evidence
