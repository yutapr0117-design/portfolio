---
description: Begin a new increment by following the discover → document → systematize → verify → deliver discipline. Sets up the change scaffold and reminds of constraints.
---

新しい increment を開始する手順を要約する。CLAUDE.md §5 「The loop」の規律に従い、Japanese で reply する。

## 手順

1. **Discover** — 何を変えるかを明示する。1〜2 文で目的を述べる。
2. **Document** — 既存 docs (`docs/architecture/*.md`) の関連 section を読み、現状認識を揃える。
3. **Systematize (機械強制)** — 新しい invariant が見つかったら、それを `check_repository_consistency.py` の Check として機械化する (`check-author` sub-agent を呼ぶ)。
4. **Verify** — `/verify` で `npm run verify` exit 0 を確認する。
5. **Deliver** — `/deliver` で increment を確定する (全ファイルブロック・パス一覧・commit 指示・summary)。

## Constraints reminder

- C1: Boring Technology — フレームワーク禁止
- C2: IIFE — main.js は単一 IIFE
- C3: ErrorBoundary — View Transition の error 境界必須
- C4: フレームワーク再提案禁止
- C5: AI のみが実装 (human is design + prompts only)
- C6: AIO published layer は orchestrator 承認なしに編集しない
- C7: KARTE CDN に SRI を提案しない

## branch / commit 規律

- `claude/<増分名-kebab-case>` で branch 切る
- `git add <明示パス>` のみ (`git add .` / `-A` は deny)
- commit message は HEREDOC で、末尾に `Co-Authored-By: Claude <noreply@anthropic.com>`
- `--no-verify` 禁止

## 出力

次にやるべきことを 3 行以内で reply する (BLUF):
- このセッションで取り組む対象 (1 文)
- 想定される Check 追加 (もしあれば)
- 想定される文書同期 (どの map / runbook)
