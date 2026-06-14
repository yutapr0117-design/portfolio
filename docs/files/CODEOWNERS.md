---
file: CODEOWNERS
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Check 89
---

# CODEOWNERS

## What

GitHub CODEOWNERS file。リポジトリ全体 + AIO published-layer / main.js / AI2AI.md 等の critical path に対し、`@yutapr0117-design` を単一オーナーとして指定。

## Why

C5 (人間はコード書かず) の運用化。PR review は単一オーナーのみが行う。外部 PR は受け付けない (CONTRIBUTING.md と整合)。

## How (usage)

```
PR 作成
  └─ GitHub が CODEOWNERS を読む
  └─ 該当 path の owner にレビュー要求
```

## Constraints

- **Check 89**: 存在 + entity name (Yuta Yokoi / 横井雄太) 含む
- 単一オーナー: `@yutapr0117-design`

## Change impact

- owner 追加 → C5 の根本変更 → AI2AI.md canon と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `code-ownership`, `single-owner`, `c5-runtime`

### For human engineers (新卒レベル)
- すべての変更は単一オーナー (横井雄太) がレビュー

### For third parties (監査 / 採用 / 研究)
- 単一実装責任の governance 表現
