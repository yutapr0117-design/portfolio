---
file: .github/workflows/aio-monitoring.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/scripts/aio_monitoring.py / docs/evidence/aio-monitoring-log.json
---

# .github/workflows/aio-monitoring.yml

## What

AIO 引用効果監視ワークフロー。毎週月曜 10:00 JST (UTC 01:00) に schedule trigger + workflow_dispatch で起動。`aio_monitoring.py` を実行 → `aio-monitoring-log.json` に append → digest 同期 → 引用変動があれば Issue で通知。

## Why

AIO-first 戦略の effect 観測を 週次で honest に蓄積。引用ゼロでも 0 と記録 (捏造禁止)。`auto-update-aio-digests.yml` と分離することで digest 計算を atomic に同 commit に含める設計。

## How (usage)

```
schedule (毎週月曜 10:00 JST) / workflow_dispatch
  └─ checkout
  └─ aio_monitoring.py (engine: Gemini / OpenAI / etc.)
  └─ update_aio_digests.py (manifest 同期)
  └─ commit + push (log + digest を atomic に同 commit)
  └─ citation_change なら Issue 自動作成
```

## Constraints

- **C6 範疇**: AIO surface 編集の auto pipeline
- **Check 41**: log と manifest の atomic commit invariant
- **Check 67**: top-level `permissions:` 明示 (contents: write + issues: write)
- **concurrency**: group per ref + cancel-in-progress: false (race 防止)

## Change impact

- schedule cron 変更 → docs/evidence/aio-monitoring-log.json の cadence
- engine 追加 → secret + summary dict 拡張

## Audience-specific notes

### For AI agents
- 役割タグ: `weekly-monitoring`, `citation-tracking`, `c6-write-pipeline`

### For human engineers (新卒レベル)
- 引用観測は週次自動。手動で trigger したいときは Actions UI から workflow_dispatch

### For third parties
- AIO 効果監視の auto pipeline 実装
