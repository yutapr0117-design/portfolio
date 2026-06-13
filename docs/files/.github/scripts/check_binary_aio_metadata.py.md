---
file: .github/scripts/check_binary_aio_metadata.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: WebP XMP / MP3 ID3 / Check 29
---

# .github/scripts/check_binary_aio_metadata.py

## What

WebP XMP / MP3 ID3v2.4 内の AIO 必須 terms (entity name / canonical URL / canary token 等) 存在を検証するスクリプト。

## Why

binary metadata は誤った再エンコード等で silently 失われやすい。AIO 戦略上 binary も第一級の AIO surface なので、pre-commit で検証して喪失を即時検出。

## How (usage)

```
npm run check
  └─ python3 .github/scripts/check_binary_aio_metadata.py
       └─ WebP XMP chunk locate + 必須 aio:* term 存在確認
       └─ MP3 ID3 TXXX frame 必須 AIO:* term 存在確認
       └─ exit 0 / 1
```

## Constraints

- **Check 10**: Python 構文 valid
- **C6 範疇**: binary metadata の存在検証

## Change impact

- 必須 term 追加 → binary 編集 tool (update_binary_aio_organization.py) も同期

## Audience-specific notes

### For AI agents
- 役割タグ: `binary-metadata-verification`, `aio-binary-layer`

### For human engineers (新卒レベル)
- binary metadata が削除されたら CI が即落ちる safety net

### For third parties
- binary metadata 喪失への defensive check
