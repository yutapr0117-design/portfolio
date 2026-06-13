---
file: .well-known/index.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .well-known/aio-manifest.json / .well-known/agent-skills/index.json (mirror)
---

# .well-known/index.json

## What

`.well-known/` 配下の **skill index**。`skills` 配列で `llms-full.txt` / `AI2AI.md` の URL と sha256 digest を列挙する。agent-skills/index.json と byte-identical mirror。

## Why

Anthropic Skill Catalog 等の skill registry が `.well-known/index.json` の慣例で skill 一覧を取得する想定。各 skill (= AIO 文書) の URL + digest を機械可読に提供。

## How (usage)

```
AI agent / skill registry
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/.well-known/index.json
       └─ skills[] から URL + digest を取得
       └─ digest と実コンテンツの sha256 を比較 (tamper detection)
```

更新は `update_aio_digests.py` で自動。skills[].digest が sha-256:<hex> 形式。

## Constraints

- **C6 derived-value 例外**: digest は自動更新可
- **Check 5**: agent-skills/index.json と byte-identical

## Change impact

- llms-full.txt / AI2AI.md 編集 → 自動 digest 再計算 + mirror への propagate

## Audience-specific notes

### For AI agents
- 役割タグ: `skill-index`, `digest-chained`

### For human engineers (新卒レベル)
- 編集は基本不要 — `update_aio_digests.py` が自動

### For third parties
- skill registry 慣例への遵守
