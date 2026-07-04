---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-bloat-reduction-and-behavioral-bughunt.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: CLAUDE.md §7 (要点 handoff) / AI2AI.md (canon) / total-check-runbook.md §9
---

# improvement-notes-claude-v80-phase4-bloat-reduction-and-behavioral-bughunt.md

## What

「終わりなき改善」phase4 後続 run（#555〜#566・2026-07-04〜05）の**詳細 engineering 物語と教訓**。肥大化解消の継続完遂（shipped JS 全 ≤824 行・葉 factory 抽出）+ Check 361/362 新設（1,000 行しきい値の機械化）+ 実バグ 3 件修正（AIPage stuck / snapshot 未正規化 crash / TodoPage a11y leak）+ 抽出後 dead-param 掃除 + 抽出済ページ再監査（クリーン）。CLAUDE.md §7 の 1 エントリ（要点 handoff）に対する詳細層。

## Why

トークン枯渇に備えた「まともな引き継ぎ書」。handoff-first discipline（CLAUDE.md §5）に従い §7 は薄く速く、本ファイルは同一 run の意思決定・教訓・次の vein 候補を厚く残し、cold-start の後続 AI が確実に復帰できるようにするため。

## How (usage)

cold-start の後続 AI はまず CLAUDE.md §7 → 本ファイルの順で深掘りする。「肥大化をどう byte-equivalent に解消したか」「1,000 行しきい値をどう BLOCKING Check へ昇華したか」「実バグ 3 件の class（外部 ingestion 正規化 / a11y leak / stuck fail-safe）」「次の genuine vein 候補（router・store edge-case / vacuous-gate 掘り）」を把握する。

## Change impact

- 本 run の事実記録ゆえ原則 append-only（point-in-time 履歴・遡及改変しない）
- 新規 incident-artifact ゆえ README.md inventory（Check 75）と本 mirror（Check 108）が必要（追加済）

## Constraints

- **Check 75**: docs/incident-artifacts/README.md に列挙必須
- **Check 108**: docs/files mirror bijection（本ファイルがその mirror）
- **Check 361/362**: 本 run で新設した js-leaf 予算 bijection + mutation anchor 整合
- 歴史層ゆえ Check 109（prose count-hardcode 禁止）対象外（point-in-time 記録）

## Audience-specific notes

### For AI agents
- 役割タグ: `incident-artifact`, `run-narrative`, `bloat-reduction`, `behavioral-bughunt`, `session-handoff`
- 「肥大化は Check で機械封じ」「抽出後は dead-param を awk 確認（ESLint は destructured param を見ない）」「外部 ingestion 全正規化」「merge 後は branch を切ってから編集」が後続に有用

### For human engineers (新卒レベル)
- 肥大化解消 = 挙動を変えず（byte-equivalent）大ファイルを小モジュールへ分割。Check にする = 人間/AI が忘れても機械が止める

### For third parties
- 構造改善（肥大化解消）と品質改善（実バグ 3 件・各 BLOCKING e2e）を並走させた透明な記録。プロセス slip（main 直 push）も honest に記録し memory で再発防止
