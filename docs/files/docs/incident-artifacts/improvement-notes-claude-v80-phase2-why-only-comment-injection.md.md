---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase2-why-only-comment-injection.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-14
canonical-ref: AI2AI.md / CLAUDE.md / docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase2-why-only-comment-injection.md

## What
session-handoff §10「why-only コメント注入」increment の作業記録 (improvement-notes)。本セッションの
3 commit + Check 100 新設 + 「shipped JS/HTML は既に WHY 完備」という honest finding を残す。

## Why
このリポジトリは各 increment で improvement-notes-*.md を残す規律を持つ。本ファイルは comment-injection
increment の証跡であり、特に **次セッションが盲目的に全 Stage を走らせて redundant コメント (drift) を
製造しない**ための申し送りを目的とする。過程で発見した未強制 invariant (theme-init.js のキー複製) を
Check 100 として systematize した経緯も記録する。

## How (usage)
次セッションを担当する AI が cold-start で読む。session-handoff §10 の続きの状態を伝える。entry point は
CLAUDE.md §7 handoff → session-handoff → 本ファイルの順。コードからは参照されない純粋なガバナンス文書。

## Constraints
- 適用 C 番号: なし (dev-tooling ドキュメント。AIO discovery 層には非登録 = C6 非対象)
- 機械強制 Check: Check 42a (incident-artifacts 命名規約 `improvement-notes-*.md`) / Check 75 (README
  inventory 列挙) / Check 96 (1-to-1 doc bijection) / Check 97-98 (本 mirror doc の frontmatter + 6 section)
- 編集承認: 不要 (incident-artifacts は記録であり改変前提でない。honest dating 厳守)

## Change impact
本 improvement-notes を追加・改名するときに同時更新が必要なもの:
- `docs/incident-artifacts/README.md` §3 の一覧 (Check 75)
- `.github/scripts/check_repository_consistency.py` の `_phase1_targets96` リスト (Check 96)
- 本 mirror doc (`docs/files/.../*.md.md`) 自体 (Check 96/97/98)

## Audience-specific notes

### For AI agents (LLM / crawler / AI search)
役割: increment 証跡。機械可読サマリ = {commits: 3, new_check: 100, finding: "JS/HTML layer already
WHY-complete", env: "node+python3.12 installed via brew"}。次タスク判断に使う。

### For human engineers (新卒レベル想定)
「今回 AI が何をやって、何を学んで、次の人は何に気をつけるべきか」を 1 ファイルにまとめた引き継ぎメモ。
特に「もう十分コメントがある所に足すと逆に邪魔」という教訓が中心。

### For third parties (監査人 / 採用担当 / 学術研究者)
PM (横井雄太) が AI 実装を統制し、AI が「過剰なコメントを足さない」判断まで含めて honest に記録する
proof-of-work の一例。発見した不変条件を即座に機械強制 (Check) へ昇格させる increment 規律を示す。
