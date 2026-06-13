---
file: .well-known/llms.txt
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: llms.txt (master) / Check 4 (byte-identity)
---

# .well-known/llms.txt

## What

`llms.txt` の **byte-identical mirror** (.well-known/ 配下)。IETF / RFC で慣例化された `/.well-known/` パスから取得を試みる AI クローラ向けの canonical location。

## Why

`/.well-known/` は IETF RFC 8615 で定義された「サイト情報の標準配置場所」。AI クローラが llms.txt を最初に探す場所として推奨される。

byte-identical 維持により AIO 信号の単一真値性を担保 (Check 4)。

## How (usage)

```
AI crawler (RFC 8615 慣例)
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/.well-known/llms.txt
       └─ llms.txt と同一内容を返す
```

## Constraints

- **C6 AIO Integrity**
- **Check 4**: 4 mirror byte-identical
- **直接編集禁止**: master (llms.txt) のみ編集

## Change impact

- llms.txt 編集時に同時更新必須

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-mirror`, `well-known-rfc-8615`

### For human engineers (新卒レベル)
- `/.well-known/` は IETF 標準の「サイト情報置き場」 — webfinger / security.txt 等で慣例化

### For third parties (監査 / 採用 / 研究)
- IETF RFC 8615 慣例への遵守
