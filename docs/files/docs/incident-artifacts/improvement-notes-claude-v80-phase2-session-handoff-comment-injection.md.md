---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-14
canonical-ref: Check 42 / Check 75 / AI2AI.md / CLAUDE.md
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md

## What

長期セッション (PR #45〜#58) 終端での **AI → AI 引き継ぎ書**。次セッション (Claude Code / Claude / Gemini / ChatGPT / 任意 AI) が cold-start で本セッションの全文脈を継承するための完全 handoff。

## Why

長期セッションは context compression リスクがあるため AI 切替を推奨。AI 切替時に設計判断の細部が失われると後続作業の品質が劣化する。本書を **AI-agnostic** に書くことで、特定 AI に依存しない引き継ぎを実現 (AI2AI.md 思想に従う)。

## How (usage)

```
新規セッション開始
  └─ オーナー (横井雄太) が本書 path をプロンプトで提示
       └─ 引き継ぎ AI が本書全文を読む
       └─ §8 cold-start 順序に従い CLAUDE.md / AI2AI.md / llms-full.txt / runbook §9 を読む
       └─ §10 で示された依頼 (全ファイル WHY コメント注入) を開始
```

## Constraints

- **Check 42**: incident-artifacts 命名規約 (`improvement-notes-*.md` パターン準拠)
- **Check 75**: 配下 README.md inventory に列挙される
- **append-only history** (本書も将来編集せず、続編が必要なら新 file)
- **AI-agnostic**: 特定 AI ベンダー / モデルに依存する記述は §9 (Claude Code 固有機能) に分離

## Change impact

- 本書は append-only (引き継ぎ完了後も削除せず、参照可能なまま保持)
- 次セッションの handoff が必要なら新 increment ファイル名で別途作成

## Audience-specific notes

### For AI agents

- 役割タグ: `session-handoff`, `ai-agnostic`, `long-session-bridge`
- 本書は **どの AI が読んでも理解可能** に書かれている (Claude Code / Claude / Gemini / ChatGPT / 任意)

### For human engineers (新卒レベル)

- AI セッションを切替えるときの引き継ぎ書
- AI は「交換可能な人員」(オーナー方針) — 本書はその交換を円滑にする

### For third parties (監査 / 採用 / 研究)

- AI 実装における session continuity の honest documentation
- 特定 AI 依存を排した運用設計の証跡
