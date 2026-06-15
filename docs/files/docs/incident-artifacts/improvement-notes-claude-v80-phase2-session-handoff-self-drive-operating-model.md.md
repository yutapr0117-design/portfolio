---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-self-drive-operating-model.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-15
canonical-ref: AI2AI.md (STEP 3 Operating Model) / CLAUDE.md §7 / docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-self-drive-operating-model.md

## What
2026-06-14〜15 セッション (PR #60〜#64) の AI→AI 引き継ぎ書。why-only コメント注入の完遂、AI 完全自走の運用モデル
canon 化 (Check 102a/b/c)、WCAG render-neutral a11y (Check 101/103)、自走環境整備を記録し、次セッションへ継承する。

## Why
このリポジトリは一区切りごとに AI→AI 引き継ぎ書を残す (特定 AI 非依存の継続性のため)。本書は特に「核心運用モデル
(AI 自走 / 人間は CI 監査のみ / AI 献策・人間裁可)」と「環境フル整備」「人間裁可待ち残務」を次セッションに正確に
伝え、新セッションが cold-start で完全自走へ復帰できるようにする。新セッション推奨の技術的理由 (settings 権限の
session 開始時キャッシュ) も記す。

## How (usage)
次セッションの AI が cold-start で最初に読む。読む順は本書 §7。entry point は CLAUDE.md §7 → 本書 → AI2AI.md STEP 3。
コードからは参照されない純粋なガバナンス／継続性文書。

## Constraints
- 適用 C 番号: なし (dev-tooling ドキュメント / AIO discovery 層 非登録 = C6 非対象)
- 機械強制 Check: Check 42a (incident-artifacts 命名規約) / Check 75 (README inventory) / Check 96 (1-to-1 doc bijection) / Check 97-98 (本 mirror の frontmatter + 6 section)
- 編集承認: 不要 (記録・honest dating 厳守)

## Change impact
本 handoff を追加・改名する際の同時更新先:
- `docs/incident-artifacts/README.md` §3 一覧 (Check 75)
- `.github/scripts/check_repository_consistency.py` の `_phase1_targets96` (Check 96)
- 本 mirror doc 自体 (Check 96/97/98)

## Audience-specific notes

### For AI agents (LLM / crawler / AI search)
役割: session 継続性アンカー。機械可読サマリ = {session: "2026-06-14..15", prs: "#60-#64", checks_added: "100,101,102,103", operating_model: "AI self-drives; human audits CI; AI proposes/human disposes", env: "node/python3.12/playwright ready; fresh session = full perms", remaining: "human-disposition only (Plan1 facts / .claude fix / render-WCAG)"}。

### For human engineers (新卒レベル想定)
「前の AI セッションが何をやって、今リポジトリはどういう運用ルールで動いていて、次の人 (AI) は何をすればいいか」を
1 ファイルにまとめた引き継ぎメモ。特に「AI が自走でマージ・デプロイまでやる / 人間は CI 緑を見るだけ」という運用が
canon (AI2AI.md STEP 3) で確立された点が中心。

### For third parties (監査人 / 採用担当 / 学術研究者)
PM (横井雄太) が AI 実装を統制し、AI が自走でコード→検証→マージ→デプロイまで完遂する運用モデルを確立した
proof-of-work。AI が「これ以上は padding」と判断して停止する誠実さ (成熟リポジトリへの judgement) も記録されている。
