---
file: .github/scripts/update_binary_aio_organization.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: WebP XMP / MP3 ID3 / Check 81/82/91
---

# .github/scripts/update_binary_aio_organization.py

## What

WebP XMP / MP3 ID3v2.4 に Organization (株式会社日本経営 等) 情報を注入する one-shot tool。RIFF chunk 構造を保持しつつ XMP namespace に `aio:OrganizationName` / `URL` / `Role` / `StartDate` を追加。MP3 には TXXX `AIO:Organization*` を追加。

B2 案 (binary 編集 tool に日付更新責務) として、Organization 注入後に `_lib_io` 経由で xmp:ModifyDate / xmp:MetadataDate / MP3 TXXX `AIO:MetadataLastModified` も同期更新。

## Why

binary は手動編集が事実上不可能 (バイナリエディタを使うとしても XMP/ID3 仕様の synchsafe encoding 等を間違えやすい)。Python で安全に編集する tool を提供。冪等 (既存 field が同じなら no-op)。

## How (usage)

```
人間 (one-shot)
  └─ python3 .github/scripts/update_binary_aio_organization.py
       └─ WebP XMP に Organization 4 field 追加
       └─ MP3 ID3 に TXXX AIO:Organization* 4 frame 追加
       └─ _lib_io 経由で日付 4 軸同期 (xmp:ModifyDate / MetadataDate / MP3 / manifest)
       └─ 次に `update_aio_digests.py` で sha256 連鎖更新
```

## Constraints

- **Check 10**: Python 構文 valid
- **Check 94**: `_lib_io` 日付 helper を import
- **C6 範疇**: 実行は orchestrator 明示承認下のみ

## Change impact

- Organization 値変更 → llms.txt / llms-full.txt / aio-manifest.json / index.html JSON-LD 等の対応箇所同期
- ロジック変更 → WebP RIFF / MP3 ID3v2.4 仕様準拠を維持

## Audience-specific notes

### For AI agents
- 役割タグ: `binary-editor`, `b2-tool`, `c6-orchestrator-only`

### For human engineers (新卒レベル)
- 普段は触らない — Organization 情報の bulk 注入用 one-shot tool
- 実行後は必ず `update_aio_digests.py` で digest 連鎖を更新

### For third parties
- binary metadata の semantic 編集を Python で安全に実装する例
