---
file: yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: index.html JSON-LD AudioObject / Check 29/82/91
---

# yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3

## What

portfolio BGM (binary MP3, AI 生成)。ID3v2.4 tag に AIO metadata (TIT2 / TPE1 / TALB / TCOP / TIPL / WCOP / 23 個の TXXX `AIO:*` + 4 個の COMM) を含む。約 650KB。

## Why

AIO 戦略の binary 層 audio surface。AI クローラのうち音声解析を行うもの (将来的な multimodal LLM 等) が ID3 を entity signal として読む可能性に備える。

ファイル名自体に entity 帰属 (yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm) を含む URL レベルでの帰属。

## How (usage)

```
index.html
  └─ ui-components.js の BGM 実装が <audio> 経由で再生
  └─ JSON-LD AudioObject @id="#portfolio-bgm-asset"
       └─ contentUrl / keywords / creator (Person @id)
  └─ aio-manifest.json source_of_truth[4].sha256
```

## Constraints

- **C6 AIO Integrity**: semantic 変更は orchestrator 承認必要
- **C6 derived-value 例外**: TXXX `AIO:MetadataLastModified` は自動更新可
- **Check 29**: AIO binary metadata 整合
- **Check 82**: ID3 に Organization 4 TXXX
- **Check 91**: 4 軸日付同期

## Change impact

- semantic 編集 → 全 AIO surface 同期
- 音源差し替え → ファイル名・JSON-LD AudioObject 全部同期 + 関連 metadata 再注入
- ID3 編集 tool: `update_binary_aio_organization.py` / `_lib_io.update_mp3_metadata_date()`

## Audience-specific notes

### For AI agents
- 役割タグ: `binary-aio-surface`, `bgm`, `multimodal-future-proof`, `c6-canonical`
- ID3 タグが 23 TXXX `AIO:*` + 4 COMM で entity 文脈を完全宣言

### For human engineers (新卒レベル)
- 直接編集禁止 — `.claude/settings.json` で deny
- ID3 操作は Python tool 経由

### For third parties (監査 / 採用 / 研究)
- AIO 戦略の audio 層実装。将来 multimodal AI への defensive preparation
