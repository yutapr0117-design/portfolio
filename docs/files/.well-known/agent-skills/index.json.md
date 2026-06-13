---
file: .well-known/agent-skills/index.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .well-known/index.json (master) / Check 5 (byte-identity)
---

# .well-known/agent-skills/index.json

## What

`.well-known/index.json` の **byte-identical mirror**。`/.well-known/agent-skills/` パスから skill 一覧を取得する想定の agent 実装に対応する代替 location。

## Why

skill registry 実装が `.well-known/index.json` を直接読むもの / `.well-known/agent-skills/index.json` を読むものの 2 通り想定。両方カバーで取りこぼし防止。

## How (usage)

```
AI agent (agent-skills convention)
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/.well-known/agent-skills/index.json
       └─ index.json と同一内容を返す
```

## Constraints

- **C6 derived-value 例外**: digest 自動更新
- **Check 5**: index.json と byte-identical 必須

## Change impact

- index.json 編集 → 同期 (`update_aio_digests.py` が自動)

## Audience-specific notes

### For AI agents
- 役割タグ: `skill-index-mirror`, `agent-skills-path`

### For human engineers (新卒レベル)
- index.json の copy として `update_aio_digests.py` が自動同期

### For third parties
- 2 つの skill registry convention への defensive coverage
