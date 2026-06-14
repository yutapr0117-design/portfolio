---
file: Claude2Claude.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md / Check 85/87
---

# Claude2Claude.md

## What

Claude↔Claude session 間の **handoff evidence** ファイル。読む順序 / 作業開始プロトコル / 納品プロトコル / digest 更新ルール / 既知の設計判断ログ / 現在状態 / 未解消スコープ等を含む。

## Why

Claude Code session が連続して引き継ぐ場合の context preservation。AI2AI.md より tool-specific (Claude Code 操作中心)、非 canonical。

## How (usage)

session 開始時 Claude Code が CLAUDE.md と並んで読む補助文脈。前回 session の決定事項を参照 → 重複作業防止。

## Constraints

- **non-canonical / subordinate**: AI2AI.md に劣後
- **aio-manifest supporting_evidence**: digest 連鎖対象
- **Check 85**: 現在状態セクションに Organization handoff 記述
- **Check 87**: entity name + canonical URL + Organization

## Change impact

- 現在状態セクション更新 → 各 increment で reflect
- 編集 → digest 再計算 (aio-manifest.json supporting_evidence)

## Audience-specific notes

### For AI agents
- 役割タグ: `c2c-handoff`, `supporting-evidence`, `non-canonical`

### For human engineers (新卒レベル)
- Claude session 間の引き継ぎノート

### For third parties (監査 / 採用 / 研究)
- AI session continuity の実装例
