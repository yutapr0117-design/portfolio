---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-privacy-evidence-and-operating-model-record.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-21
canonical-ref: AI2AI.md (Session Record #21) / CLAUDE.md §7
---

# improvement-notes-claude-v80-phase4-privacy-evidence-and-operating-model-record.md

## What

守秘前提の実績 evidence 公開（real-work-claims.md）+ privacy guard（Check 122）+ 運用モデル記述の超正確化（Q2）を、会話駆動の合意の下で遂行した run の**詳細 engineering 物語と教訓**。Session Record #21（簡潔 handoff）の詳細層。

## Why

privacy-critical（機微情報漏洩が最悪の失敗）な run ゆえ、抽象化方針・二段構えの根拠設計・約束破り→是正の control-loop・公/私 境界の terminal 判断・「推奨前に現物検証で捏造回避」という非自明な学びを次の AI に残すため。

## How (usage)

cold-start の後続 AI が「実績 evidence をどう守秘前提で公開したか」「運用モデルをどう超正確に記述したか」「なぜ公開面を今後 padding しないか」を把握する詳細層。Session Record #21 → 本ファイルの順で深掘り。

## Change impact

- 本 run の事実記録ゆえ原則 append-only（point-in-time 履歴・遡及改変しない）
- 新規 incident-artifact ゆえ README.md inventory（Check 75）と本 mirror（Check 108）が必要（追加済）

## Constraints

- **Check 75**: docs/incident-artifacts/README.md に列挙必須
- **Check 108**: docs/files mirror bijection（本ファイルがその mirror）
- **Check 122**: 原本 pdf/docx 等は tracked 禁止（本 run の privacy guard）
- 歴史層ゆえ Check 109（prose count-hardcode 禁止）対象外（point-in-time 記録）

## Audience-specific notes

### For AI agents
- 役割タグ: `incident-artifact`, `run-narrative`, `privacy-critical`, `operating-model-record`
- 「約束は守る／破ったら最優先回収」「推奨前に現物検証で捏造回避」「公開面を padding しない（公/私 境界）」が後続に有用

### For human engineers (新卒レベル)
- 守秘義務と公開のバランスを、固有名を伏せつつ能力をリポジトリで証明する二段構えで取った実例

### For third parties
- AI-only 自走運用で privacy-critical タスクを会話駆動の合意付きで遂行した透明な記録（約束破り→是正も honest に残す）
