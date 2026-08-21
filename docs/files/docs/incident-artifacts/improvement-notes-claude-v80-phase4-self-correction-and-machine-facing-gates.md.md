---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-self-correction-and-machine-facing-gates.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-21
canonical-ref: AI2AI.md / CLAUDE.md / docs/incident-artifacts/improvement-notes-claude-v80-phase4-critical-path-and-self-correction.md / docs/files/playwright.config.cjs.md
---

# improvement-notes-claude-v80-phase4-self-correction-and-machine-facing-gates.md

## What

2026-08-21 の run（PR #1245〜#1251）の改善文書。前 run で入れた遅延読み込みの後始末を続けつつ、
レンズを **「機械可読面の契約は誰が見ているのか」** と **「自分の測定を疑う」** へ寄せた記録。

`AI2AI.md` の Session Record #29 は**要点のみ**で、本ファイルが詳細層。

## Why

この run で最も再利用価値が高いのは **失敗の型**である。

- **非 vacuity 検証の誤診 2 型**（見ていない属性を壊す／mutation が当たっていないのに緑）
- **測定系を疑って 3 回とも当たった**（`localStorage` 注入の unload flush で 4 回誤診、
  SW が shell を返すという思い込み、`page.coverage` の精度）
- **信号が出ないなら何も作らない**（`page.coverage` の探索を打ち切った記録）
- **制御できないものを Check にしない**（`Cache-Control` は GitHub Pages 固定）

個別のバグより、これらの方が次の run で効く。

## How (usage)

- **cold-start の読み順**: `CLAUDE.md` §7 → `AI2AI.md` の最新 Session Record →（詳細が要るとき）本ファイル。
- **e2e を書く前**は `docs/files/playwright.config.cjs.md` の落とし穴表を読むこと。
  本 run で追加した「大量データ seed は `addInitScript` で起動前に仕込む」は特に costly な学び。

## Constraints

- **Check 42a**: `improvement-notes-<author>-v<version>-<slug>.md` の命名（準拠）。
- **Check 75**: `docs/incident-artifacts/README.md` の inventory に列挙されていること。
- **Check 108**: 本 mirror doc が存在すること。
- **Check 365**: 1,000 行以内。
- 歴史記録なので **Check 436 の規範層スコープ外**。過去の判断理由を書き換えないこと。

## Change impact

- 追記は「実測値を伴う事実」に限る。推測を足すと次の AI がそれを根拠にコードを足す。
- 「未着手の vein」を消化したら、次の improvement-notes 側で状態を更新すること。

## Audience-specific notes

### For AI agents
- 役割タグ: `handoff`, `improvement-notes`, `machine-facing`, `self-correction`, `measurement-pitfalls`

### For human engineers (新卒レベル)
- 「テストが緑」＝「意味のあることを検査している」ではない、の具体例が並ぶ。
  特に **壊した対象がその test の検査範囲に入っているか**を先に確かめる習慣。

### For auditors / third parties
- AI 自走下で、**自分の測定ミスと自分が書いた誤りを繰り返し発見・訂正した**実例。
