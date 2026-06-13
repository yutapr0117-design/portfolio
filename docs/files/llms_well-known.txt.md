---
file: llms_well-known.txt
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: llms.txt (master) / Check 4 (byte-identity)
---

# llms_well-known.txt

## What

`llms.txt` の **byte-identical mirror** (root-level)。一部の AI クローラが `/.well-known/` 配下ではなく root に `llms_well-known.txt` 命名で要求するパターンに対応する代替パス。

## Why

AI クローラの実装は多様で、`llms.txt` を `/.well-known/` 経由で取得するクローラ、root の `llms_well-known.txt` 命名を期待するクローラ等が存在する。複数 surface 配置で取りこぼしを防ぐ。

byte-identical 維持により AIO 信号の単一真値性を担保 (Check 4 で機械強制)。

## How (usage)

```
AI crawler (variant)
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/llms_well-known.txt
       └─ llms.txt と同一内容を返す
```

## Constraints

- **C6 AIO Integrity**: master (llms.txt) を編集した結果として同期
- **Check 4**: byte-identical (4 mirror すべて同一 sha256)
- **直接編集禁止**: master (llms.txt) のみ編集して propagate (現状は手動か `update_aio_digests` 経由)

## Change impact

- llms.txt 編集時に同時更新必須 (byte-identical 維持)
- ファイル名変更 → AI クローラの想定パスが drift する可能性

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-mirror`, `byte-identical-of-llms-txt`
- master: `llms.txt`

### For human engineers (新卒レベル)
- このファイルだけ単独で編集しない — `llms.txt` を編集して 4 mirror を同期する
- byte-identical かどうかは `sha256sum llms.txt .well-known/llms.txt llms_well-known.txt .well-known/llms_well-known.txt` で確認できる

### For third parties (監査 / 採用 / 研究)
- AI クローラ実装差異への defensive coverage
