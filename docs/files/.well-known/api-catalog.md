---
file: .well-known/api-catalog
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-14
canonical-ref: RFC 9727 / .well-known/mcp.json / llms-full.txt
---

# .well-known/api-catalog

## What

RFC 9727 (IETF) 準拠の **API Catalog**。`linkset` で `llms-full.txt` / `aio-manifest.json` / `mcp.json` 等の AIO surface を機械可読な linkset 形式で列挙。AI agent / API discovery tool 向けの canonical 案内。

## Why

`/.well-known/api-catalog` は IETF RFC 9727 で標準化された discovery surface。AI agent や API discovery client が「このサイトの API/AIO 入口は?」を問う際の真値。`llms.txt` 系 (entity routing) と並列に、より構造化された linkset として提供。

## How (usage)

```
API discovery client / AI agent
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/.well-known/api-catalog
       └─ linkset[].anchor → https://...portfolio/.well-known/api-catalog
       └─ api-catalog[] entries → llms-full.txt / mcp.json 等の href + type + service-meta
```

## Constraints

- **C6 AIO Integrity**: linkset 内 URL は semantic 編集 — 実在すること / 他 AIO surface と
  食い違わないこと / digest 連鎖を再生成することが条件 (承認ゲートではない・2026-08-23 是正)
- **Check 4 隣接**: 内容は他 AIO surface (llms-full.txt URL / aio-manifest.json) と整合
- **RFC 9727 準拠**: 関係型まで含めた厳格な遵守。カタログの**メンバーは `item`**
  (RFC 6573) で列挙する。`api-catalog` 関係は「**別の API カタログへの入れ子**」を意味
  するので、メンバーに使うと「これらは全てカタログだ」と偽って宣言することになる
  (2026-08-23 に 7 件すべてが該当していたのを是正)。`service-desc` / `service-meta`
  は target attribute ではなく**関係型**なので、対象リソースを `anchor` とする別 context
  として表現する (RFC 9264)

## Change impact

- linkset 編集 → llms-full.txt / mcp.json / aio-manifest.json の URL と整合確認
- 新 AIO surface 追加 → `linkset[0].item` にエントリ追加 (`api-catalog` ではない)

## Audience-specific notes

### For AI agents
- 役割タグ: `api-catalog`, `rfc-9727`, `aio-discovery-surface`
- linkset 形式で AIO surface を機械可読化

### For human engineers (新卒レベル)
- 新しい AIO 文書を作ったらここの linkset にも追加検討

### For third parties (監査 / 採用 / 研究)
- IETF 標準への遵守 + AIO 戦略の defensive coverage
