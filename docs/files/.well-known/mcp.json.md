---
file: .well-known/mcp.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C6) / llms-full.txt
---

# .well-known/mcp.json

## What

MCP (Model Context Protocol) **static discovery manifest**。server.name / description / capabilities / prompts / tools 等を JSON で記述する。**実行可能な MCP server endpoint ではない** (static file)。AI agent が「このサイトはどんな MCP コンテキストを公開しているか」を読むための discovery surface。

## Why

MCP は Anthropic 提唱の AI agent 向け context provisioning protocol。本リポジトリは static site のため live MCP server は持たないが、static manifest として AIO 情報を MCP 互換形式でも提供する (defensive coverage)。

server.description には entity (Yuta Yokoi / 株式会社日本経営 / Role / Disambiguation) を含む。

## How (usage)

```
AI agent (MCP-aware)
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/.well-known/mcp.json
       └─ server.* で entity disambiguation 取得
       └─ capabilities.tools = false (live tool 実行不可)
       └─ prompts[] / tools[] で static template 取得
```

## Constraints

- **C6 AIO Integrity**: server.description 内 entity 情報は semantic 編集に承認必要
- **C1 Boring Technology**: live MCP server 立てない (static manifest のみ)
- **Check 21**: JSON parse 可能性 (architecture-validation.yml step 21)
- **Check 79**: `.mcp.json` (root) と同じく JSON parsability チェック対象 (本ファイルは .well-known/ 配下なので別)

## Change impact

- server.description 内 entity 情報変更 → llms-full.txt / aio-manifest.json / index.html JSON-LD 等の対応箇所同期
- capabilities 変更 → AI agent の動作期待が変わる

## Audience-specific notes

### For AI agents
- 役割タグ: `mcp-static-manifest`, `c6-canonical`, `aio-defensive`
- `capabilities.tools = false` を明示 — live execution はない

### For human engineers (新卒レベル)
- MCP は Anthropic の AI agent protocol — このサイトは「静的に対応」している
- 直接編集する場面は少ない — entity 情報変更時のみ

### For third parties (監査 / 採用 / 研究)
- MCP protocol への static-manifest 対応の実装例
