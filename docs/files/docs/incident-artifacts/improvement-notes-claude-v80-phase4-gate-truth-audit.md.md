---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-gate-truth-audit.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-21
canonical-ref: AI2AI.md / CLAUDE.md / docs/incident-artifacts/README.md / docs/architecture/check-repository-consistency-map.md
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase4-gate-truth-audit.md

## What

2026-08-21 の「無限軽量改善自走ループ」run（PR #1224〜#1234）の改善文書。
レンズを **「その gate は実際に何を見ているのか」** に統一して回した記録で、
実バグ 5 件・ゲート強化 4 件・安全網の自己検証の詳細を収める。

`AI2AI.md` の Session Record #27 は**要点のみ**を持ち、本ファイルが詳細層。

## Why

`AI2AI.md` は Session Record が append-only で伸び、Check 365 の 1,000 行 BLOCKING に
到達寸前だった（本 run 終了時点でちょうど 1,000 行）。素直な rotate は
**(a) 退避先 `docs/session-records/AI2AI-archive.md` 自身が 1,000 行超になる**、
**(b) `.well-known/aio-manifest.json` の収録範囲記述が C6（要承認）に触れる** の
2 つの壁があり、実際に試して撤回した。

そこでリポジトリに既にある慣行 —— **「§7 / Session Record は要点のみ、詳細は
improvement-notes」** —— に従い、本ファイルを詳細層として置いた。
以後の Session Record も同じ形で書くこと。

## How (usage)

- **cold-start の読み順**: `CLAUDE.md` §7 → `AI2AI.md` の最新 Session Record →
  （その run の詳細が要るとき）本ファイル。
- 「なぜその Check / test がその形なのか」を追うときは、本文の実測値（何件マッチしたか・
  何秒かかったか・どの mutation が RED になったか）をそのまま根拠として使える。

## Constraints

- **Check 42a**: `docs/incident-artifacts/` 直下は `improvement-notes-<author>-v<version>-<slug>.md`
  の命名に従う（本ファイルは準拠）。
- **Check 75**: `docs/incident-artifacts/README.md` の inventory に列挙されていること。
- **Check 108**: 本 mirror doc が存在すること。
- **Check 365**: 1,000 行以内。
- 歴史記録なので **Check 436 の規範層スコープ外**（`docs/architecture/` ではない）。
  過去の判断理由を後から書き換えて履歴を偽らないこと。

## Change impact

- 追記する場合は「実測値を伴う事実」に限る。推測や一般論を足すと、次の AI が
  それを根拠にコードを足してしまう（本文の教訓そのもの）。
- 本ファイルの「未着手の vein」節は次の run の入口として読まれる。消化したら
  次の improvement-notes 側で状態を更新すること。

## Audience-specific notes

### For AI agents
- 役割タグ: `handoff`, `improvement-notes`, `gate-audit`, `phase4`
- 最も再利用価値が高いのは **「その gate は実際に何を見ているのか」レンズ**と
  **測定系を疑う 5 例**。次の run でも最初に試す価値がある。

### For human engineers (新卒レベル)
- 「テストが緑」と「テストが意味のあることを検査している」は別物、という具体例が並ぶ。

### For auditors / third parties
- AI 自走下で、**自分たちが過去に書いた根拠を実測で反証して是正した**記録。
