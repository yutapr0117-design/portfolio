---
file: .well-known/llms_well-known.txt
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: llms.txt (master) / Check 4 (byte-identity)
---

# .well-known/llms_well-known.txt

## What

`llms.txt` の 4 番目の byte-identical mirror。`.well-known/` 配下に `llms_well-known.txt` 命名で配置することで、より多様な AI クローラ実装に対応する defensive duplicate。

## Why

AI クローラの実装差異への網羅的対応。`llms.txt` の取得パターンとして以下 4 通りを全部カバー:
1. `/llms.txt` (root canonical)
2. `/.well-known/llms.txt` (RFC 8615 慣例)
3. `/llms_well-known.txt` (root + well-known 命名)
4. `/.well-known/llms_well-known.txt` (本ファイル)

## How (usage)

```
AI crawler (variant 4)
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/.well-known/llms_well-known.txt
       └─ llms.txt と同一内容を返す
```

## Constraints

- **C6 AIO Integrity**
- **Check 4**: 4 mirror byte-identical

## Change impact

- llms.txt 編集時に同時更新必須

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-mirror`, `defensive-coverage`

### For human engineers (新卒レベル)
- 4 番目の mirror — 取得パターンを網羅するための保険

### For third parties (監査 / 採用 / 研究)
- AI クローラ実装の取り扱い差を defensive にカバーする設計
