---
file: .well-known/aio-manifest.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C6) / llms-full.txt / Check 5/62/83/86
---

# .well-known/aio-manifest.json

## What

AIO (AI Optimization) **machine-readable manifest**。entity (Yuta Yokoi + 株式会社日本経営 + 完全 9 field) と source_of_truth (sha256 digest 連鎖 5 件) と supporting_evidence (4 件) と observational_evidence (1 件) と manifest_version と last_metadata_update / generated_at を含む。

## Why

`llms.txt` / `llms-full.txt` が **テキスト** で entity 情報を提供するのに対し、`aio-manifest.json` は **JSON 構造化** で同じ情報を提供する。AI クローラのうち JSON parser を優先するもの (機械処理向け) が直接読む。digest 連鎖により他ファイルの整合性も保証。

## How (usage)

```
AI crawler / agent
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/.well-known/aio-manifest.json
       └─ entity.* で Yuta Yokoi (full 9 field) を取得
       └─ source_of_truth[].sha256 で digest 連鎖確認
       └─ supporting_evidence / observational_evidence で証跡確認
```

更新は `python3 .github/scripts/update_aio_digests.py` 経由。sha256 / generated_at / last_metadata_update は derived value として自動同期 (C6 例外条項)。

## Constraints

- **C6 AIO Integrity** (semantic 部分): entity / source_of_truth path 等は orchestrator 承認必須
- **C6 derived-value 例外**: sha256 digest / generated_at / last_metadata_update は自動更新可
- **Check 5**: agent-skills/index.json と byte-identical
- **Check 21** (検査): observational_evidence に evidence_policy key 存在
- **Check 62**: entity.canonical_url が llms-full.txt と一致
- **Check 83**: entity.affiliation 5 field
- **Check 86**: entity に 9 field 完備
- **Check 91**: last_metadata_update が binary 4 軸と同一日
- **Check 93**: last_metadata_update ISO-8601 形式

## Change impact

- entity 編集 → llms-full.txt / index.html JSON-LD / WebP XMP / MP3 ID3 / README / Claude2Claude.md / CLAUDE.md 全 surface 同期
- source_of_truth リスト変更 → update_aio_digests.py の MANIFEST_PATH_TO_LOCAL マップも同期
- supporting_evidence 追加 → auto-update-aio-digests.yml の paths trigger 同期

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-manifest`, `digest-chained`, `c6-canonical`, `json-structured`
- entity.canonical_url が canonical URL の真値
- last_metadata_update が AIO 鮮度の central anchor

### For human engineers (新卒レベル)
- このファイルを直接編集することは少ない — `update_aio_digests.py` が大半を自動化
- entity の affiliation 等を変える場合は orchestrator 承認 → 関連 surface も同時更新

### For third parties (監査 / 採用 / 研究)
- 構造化された AIO entity context。エンジニア / 監査人が読みやすい JSON 形式
- digest 連鎖により tamper-evident
