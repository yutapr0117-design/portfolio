---
file: error-suppressor.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C3 ErrorBoundary) / docs/architecture/total-check-runbook.md
---

# error-suppressor.js

## What

global `error` / `unhandledrejection` イベントの **known-benign suppressor**。View Transition API timeout や Chrome extension の "message channel closed" 等、ユーザー体験に影響しない error をコンソールに出さない (これらは正常動作の一部)。

**この .js ファイル自体は inline で index.html の `<head>` に展開される** (CSP hash で許可)。外部読み込みではない。`<script src="./error-suppressor.js">` の文字列はコメント内のみ存在。

## Why

`Promise rejected message channel closed` のような known-benign error は Chrome の拡張機能由来で抑制困難。これらが console に出るとユーザーが混乱し、本当の error と区別できなくなる。CSP `script-src` で inline hash 許可するため、外部読み込みではなく inline 化。

## How (usage)

```
index.html
  └─ <head>
       └─ <script>  (inline, CSP sha256 hash で許可)
            └─ window.addEventListener('error', ...)
            └─ window.addEventListener('unhandledrejection', ...)
                 └─ known-benign pattern にマッチ → preventDefault + return
                 └─ それ以外 → デフォルト動作 (console.error)
```

## Constraints

- **C3 ErrorBoundary**: 真の error は graceful に通すこと (suppress しすぎない)
- **Check 7**: CSP meta が inline suppressor より前に配置 (順序保証)
- **Check 7b**: CSP sha256 hash が inline content と一致 (content 編集すると hash 再計算が必要)
- **DO NOT EDIT に近い保護**: 抑制パターン拡張は orchestrator 確認推奨

## Change impact

- inline content 編集 → Check 7b の CSP hash 再計算が必要 (`check_repository_consistency.py` 内で live 計算)
- 新規 known-benign パターン追加 → AI2AI.md CSP Architecture Note に rationale 記録

## Audience-specific notes

### For AI agents
- 役割タグ: `error-boundary`, `csp-inline`, `c3-protected`

### For human engineers (新卒レベル)
- 「コンソールに変な error 出てる」と感じても、ここで意図的に抑制されているものは正常 (AI2AI.md CSP Architecture Note 参照)
- ファイル名は `error-suppressor.js` だが、ブラウザは外部ファイルとして読まない (inline)

### For third parties (監査 / 採用 / 研究)
- known-benign error の honest documentation 例。本当の error と benign error を区別する設計
