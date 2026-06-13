---
file: .github/scripts/update_aio_digests.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .well-known/aio-manifest.json / .well-known/index.json / Check 5/91/93
---

# .github/scripts/update_aio_digests.py

## What

AIO digest 連鎖を再計算する自動更新スクリプト。`.well-known/aio-manifest.json` (source_of_truth / supporting_evidence / observational_evidence の sha256 + generated_at + last_metadata_update) と `.well-known/index.json` + `.well-known/agent-skills/index.json` を同期。

C6 derived-value 例外 (Plan B1) として、binary 編集 (WebP / MP3) が伴う場合は `_lib_io.update_webp_xmp_dates()` / `update_mp3_metadata_date()` 経由で日付フィールドも同期更新。

## Why

semantic 編集後の digest / 日付の手動同期は drift しやすい。tool で原子的に更新することで「人間が忘れても CI が拾う」運用を担保。冪等 (`write_if_changed`)。

## How (usage)

```
人間 / CI workflow
  └─ python3 .github/scripts/update_aio_digests.py
       └─ index.json digest 再計算
       └─ aio-manifest.json sha256 再計算
       └─ binary が変わったら xmp:ModifyDate / xmp:MetadataDate / MP3 TXXX も同期
       └─ generated_at + last_metadata_update を ISO-8601 で更新
       └─ write_if_changed で冪等
```

## Constraints

- **Check 10**: Python 構文 valid
- **Check 94**: `_lib_io` 日付 helper を import (B1 案 責務)
- **冪等性**: 全 digest が現物と一致なら no-op

## Change impact

- MANIFEST_PATH_TO_LOCAL マップ更新 → aio-manifest.json source_of_truth リストと整合
- 自動同期ロジック変更 → C6 derived-value 例外条項の運用契約に影響

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-digest-updater`, `b1-tool`, `c6-derived-sync`

### For human engineers (新卒レベル)
- AIO surface (llms.txt / 等) を編集したら必ず `python3 .github/scripts/update_aio_digests.py` を実行 → digest が同期される

### For third parties
- semantic 編集と digest / 日付の atomic 同期の実装例
