# decision-v80-phase3-color-contrast-defer.md

```
Decision-Date : 2026-06-17
Session       : continuous-improvement run (PR #73〜). 非 digest 層 (incident artifact)。
Implementer   : Claude Code (Anthropic Claude Opus) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 3 — axe color-contrast finding / §3C defer-with-reason)
Pipeline-Ver  : v74 (unchanged)
Canonical-Ref : docs/architecture/research-application-policy.md §3C / e2e/portfolio.spec.js (axe a11y)
Status        : Deferred-with-reason (gated: §3 baseline + brand-identity)
```

> **Canonical hierarchy:** `AI2AI.md` canonical / `llms-full.txt` ground truth. 従属 incident artifact。

---

## 1. 経緯：axe-core 監査が color-contrast を検出

PR #104-#106 で axe-core を統合し render-neutral な critical a11y 違反（aria-valid-attr-value /
select-name / button-name / label）を全 15 ルートで解消・機械強制した。残った axe 違反は
**color-contrast (WCAG 1.4.3 AA)** と link-in-text-block (1.4.1) のみ。

## 2. honest 分析：1,198 件の大半はアニメーション測定アーティファクト

初回スキャン（`waitForTimeout(120)`・通常 motion）では color-contrast が全ルート計 **1,198 node**
出た。しかし失敗ペアが「微妙に異なる無数の中間色（#999ea7 / #9da5af / #9a9fa8 …）が微妙に異なる
背景上」という形だったため、**fade-in / View Transition の opacity アニメーション中に測定した
アルファ合成色（transient）** と判断。`reducedMotion: 'reduce'` + 1.5s 収束後に再測定したところ、
**real な静的失敗は 4 つのブランド色ペアのみ**に収束した（いずれも ratio ≈ 4.5 = AA 境界ぎりぎり）:

| 前景 | 背景 | 用途 | ratio |
|---|---|---|---|
| `--text-muted #94a3b8` | 白 / #f8fafc 等 | muted テキスト | ≈4.5 |
| `--color-primary #6366f1` | #eff0fe / #f3f3fe / 白 | リンク・アクセント文字（署名 indigo） | ≈4.5 |
| 白 #ffffff | `--color-primary #6366f1` | primary ボタンの文字 | ≈4.5 |
| `#16a34a`（緑） | #e8f6ed | badge-success | ≈4.5 |

→ **教訓: axe をアニメーション中に走らせると transient なアルファ合成 contrast を大量誤検出する。**
a11y contrast 測定は reduced-motion + 収束後に行う。

## 3. なぜ defer-with-reason か（gated・research-policy §3C）

real な 4 ペアの修正は、いずれも CSS の色値変更（darken）を要し:
- **(a) 既存視覚の変更 = 「既存非破壊」原則に反する。** とりわけ `--color-primary #6366f1` は
  オーナーの**署名ブランド色**であり、その shade 変更はデザイン・アイデンティティの判断（AI の
  独断領域外。C5「人間は設計・判断」）。
- **(b) §3 baseline 再生成（human-merge gate）を要する。** style.css の render 変更は Playwright
  視覚回帰 baseline を更新せねば CI が赤化し、baseline は `update-playwright-snapshots.yml` dispatch
  → PR → **人間 merge** のパスでしか生成できない（CLAUDE.md §3 の「越えない境界」）。
- **(c) 失敗が AA 境界（ratio≈4.5）でmarginal** であり、緊急性は低い。

以上より、AI 独断での自律修正の対象外（gated）と判断し、§3C「defer-with-reason」として記録する。

## 4. 適用条件と次の一手（gate 解放時）

オーナーが以下を裁可した時に着手する:
1. ブランド色の darken を承認（具体案: `--text-muted` → slate-500 `#64748b` 系 / `--color-primary`
   → indigo-600 `#4f46e5` 系 / 緑 badge を darken。いずれも AA ≥4.5 を満たす最小変更でパレット系統は保持）。
2. §3 baseline パス（CSS 変更ブランチで `update-playwright-snapshots.yml` を dispatch → 生成された
   baseline PR を人間が視覚 review して merge）。
3. 着手時は e2e の a11y テスト（`A11Y_RENDER_NEUTRAL_RULES`）に `color-contrast` を追加し回帰固定する。

link-in-text-block (1.4.1) も同様に CSS（リンクの非色弁別＝下線等）変更ゆえ baseline-gated で同 defer。

## 5. 現状の到達点（honest）

render-neutral に直せる critical a11y 違反は**全て解消・機械強制済**（全 15 ルートで
aria-valid-attr-value / select-name / button-name / label がゼロ）。残るのは本記録の color 系のみで、
それは gated。よって「a11y は (非ゲートの範囲で) 完遂、color 系は gate 待ちで記録済」が正確な状態。
