---
file: .github/scripts/_lib_io.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/check-repository-consistency-map.md §1
---

# .github/scripts/_lib_io.py

## What

CI scripts 共通の純 I/O helper module。`read()` / `read_bytes()` / `extract()` / `csp_sri_hash()` / `now_iso8601()` / `update_webp_xmp_dates()` / `update_mp3_metadata_date()` の 7 public 関数を export。

## Why

`check_repository_consistency.py` の肥大化 (3,500+ 行) を抑え、Plan C で「番号体系の外」にある純関数 helper をここに集約。Phase 2 の C6 derived-value 例外条項の binary 日付同期 helper もここに統合 (6 案 helper 統一)。

## How (usage)

```python
# check_repository_consistency.py や update_aio_digests.py / update_binary_aio_organization.py から
from _lib_io import read, read_bytes, extract, csp_sri_hash
from _lib_io import now_iso8601, update_webp_xmp_dates, update_mp3_metadata_date
```

sibling import なので sys.path 操作不要 (`.github/scripts/` 配下に同居)。

## Constraints

- **Check 10**: Python 構文 valid
- **Check 74**: 4 helper API 契約 (read / read_bytes / extract / csp_sri_hash)
- **Check 95**: 3 date helper 存在 (now_iso8601 / update_webp_xmp_dates / update_mp3_metadata_date)

## Change impact

- helper API 変更 → check_repository_consistency.py / update_aio_digests.py / update_binary_aio_organization.py の caller 全部に影響
- 日付 helper の挙動変更 → C6 derived-value 例外の運用契約に影響 (Check 91)

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-helper`, `lib-io`, `c6-derived-helper`

### For human engineers (新卒レベル)
- ここに共通 helper を集約 — 複数 script で同じロジックを書きそうになったら、ここに移動を検討

### For third parties
- monolithic CI script の安全な解体の第一歩 (純関数 helper の sibling 抽出)
