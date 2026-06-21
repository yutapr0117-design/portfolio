---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-operating-model-and-a-group-run.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-21
canonical-ref: AI2AI.md (Session Record #20) / CLAUDE.md §5・§7
---

# improvement-notes-claude-v80-phase4-operating-model-and-a-group-run.md

## What

v80+ phase4 の operating-model 検証 + A 群（AI 自己生成案）自走実装 run の**詳細 engineering 物語と教訓**。Session Record #20（簡潔 handoff）の詳細層。

## Why

repo の improvement-notes 層（§7 router が「newest = current state of play」として後続 AI を誘導）に本 run の詳細記録が無かったため。実バグ・機械強制拡張・A 群実装・git mishap の教訓を残し、次の AI が同じ轍を踏まず文脈を活かせるようにする（flywheel = onboarding 精度）。

## How (usage)

cold-start の後続 AI が「直近 run で何が起き何を学んだか」を把握する詳細層として読む。Session Record #20 → 本ファイルの順で深掘り。

## Change impact

- 本 run の事実記録ゆえ原則 append-only（point-in-time 履歴・遡及改変しない）
- 新規 incident-artifact ゆえ README.md inventory（Check 75）と本 mirror（Check 108）が必要（追加済）

## Constraints

- **Check 75**: docs/incident-artifacts/README.md に列挙必須
- **Check 108**: docs/files mirror bijection（本ファイルがその mirror）
- 歴史層ゆえ Check 109（prose count-hardcode 禁止）対象外（point-in-time 記録）

## Audience-specific notes

### For AI agents
- 役割タグ: `incident-artifact`, `run-narrative`, `lessons-learned`
- git mishap 復旧手順（force/reset 不使用）と reflect-then-organize の実証が後続に有用

### For human engineers (新卒レベル)
- 「この回で何をして何を学んだか」の詳細ノート

### For third parties
- AI-only 自走 run の透明な engineering 記録（成功も mishap も honest に残す）例
