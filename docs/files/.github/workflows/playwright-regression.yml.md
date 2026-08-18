---
file: .github/workflows/playwright-regression.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: e2e/portfolio.spec.js / playwright.config.cjs
---

# .github/workflows/playwright-regression.yml

## What

PR 用の **Playwright 視覚回帰 + 振る舞いテスト** workflow。index.html / main.js / js/** / style.css / asset 等の関連 path が変更されたら Chromium で e2e + 視覚回帰 (toHaveScreenshot) を実行。

## Why

「コードが動くか」「画面が変わっていないか」を AI 実装変更時に pre-merge で確認。Stage 5 物理分割の安全ゲートとして取得済の visual baseline を活用。

## How (usage)

```
on:
  pull_request to main
  paths: [index.html, main.js, js/**, style.css, AIO 系...]
└─ checkout + setup-node + npm ci + playwright install
└─ npx playwright test (Chromium)
└─ snapshot diff があれば fail
└─ artifact upload (test-results + diff PNG)
```

## Constraints

- **Check 23**: YAML 構文 valid
- **Check 67**: permissions: contents:read
- **Check 51**: Playwright pin (1.60.0) が runbook と一致

## 赤の帰属（この job が赤いとき最初に読むこと）

この job の赤は **2 種類あり、正しい対処が正反対**:

| 赤の種類 | 意味 | 対処 |
|---|---|---|
| behavior gate が **失敗** | gate は実行され、回帰を検出した | **rerun してはいけない**。落ちたテストを読んで直す |
| behavior gate が **skipped** | gate は**一度も実行されていない**（依存インストール等が step timeout） | 何も検証されていない。`gh run rerun <run-id> --failed` |

job は失敗時に **`Explain failure attribution`** step で、どちらなのかを
`$GITHUB_STEP_SUMMARY` に書く。まずそれを読む（ジョブ API を掘る必要はない）。

**なぜこの層が要るか**: 2026-08-18 の PR #1136 で、依存インストールが 15m15s 粘って
job 全体の timeout が発火し、behavior gate は一度も走らないまま `playwright-validation`
が赤くなった。rerun したら 6m25s で全緑 = 回帰はゼロ。つまり**「検証していない」が
「壊れている」と同じ見た目で表示されていた**。オーナーの runtime 役割は「制御と監査」で
監査の入口は CI 表示なので、区別できない赤は「検証された」と誤読される。

**実測済みの前提**: step-level `timeout-minutes` は **その step を `failure` にして job を続行する**
（`cancelled` ではない）。使い捨て probe PR #1137 で timeout を 1 分にして観測し、
`install => failure` / `behavior => skipped` / `Explain failure attribution => success` を確認した。
job ごと cancel される仕様だったら後続 step は動かず、この設計は成立しなかった。

## install step を「速くしよう」と思ったら先に読むこと（2026-08-18 実測）

install は job 時間の大半を占め、CI 停滞の発生源でもある（本日 2 件: #1136 が 15m15s、
#1143 が 8 分 step timeout）。だが**素朴な最適化はどちらも実測で否定された**。

| 内訳 | 実測 |
|---|---|
| `npm ci` | **2s**（setup-node の npm cache が効いている） |
| `--with-deps` の apt | **2m41s（全体の ~94%）** |
| ブラウザ DL（Chromium + FFmpeg + headless shell） | **11s** |

- **ブラウザを `actions/cache` する → 効果 11 秒。** 「ブラウザ DL が重いからキャッシュする」
  という最初の仮説は実測で外れた。ボトルネックは apt 側。
- **`--with-deps` を外す → 不可（probe PR #1144 で実測）。** Chromium は起動し 300+ テストの
  うち 1 件を除いて通るが、`#/quiz` の描画コストが **636ms / 896ms（2 回とも再現）** と
  実測基準 11〜25ms から桁で悪化する（おそらくフォント関連の共有ライブラリが欠け、
  24,500 文字のページが遅い fallback 経路に落ちる）。**他の全テストは緑**だったので、
  #1028 で足した描画コストのテスト 1 本だけが捕捉層だった。

したがって install 停滞への正しい対処は「速くする」ではなく、**infra の赤と回帰の赤を
区別して rerun させる**こと（上の帰属セクション）。

## Change impact

- paths 拡張 → 新 shipped surface も視覚回帰対象
- Chromium バージョン更新 → baseline 再取得 (update-playwright-snapshots.yml)
- install の step timeout (8 分) を変えるときは job timeout (20 分) との差が
  behavior + screenshot の実測所要 (~6 分) を下回らないようにする

## Audience-specific notes

### For AI agents
- 役割タグ: `visual-regression`, `e2e`, `chromium-pinned`

### For human engineers (新卒レベル)
- CSS / DOM 構造を変えると Playwright が落ちる
- 意図的な変更なら `update-playwright-snapshots.yml` で baseline 更新 → PR 経由でレビュー

### For third parties
- AI 実装下での視覚回帰防止 + 段階的 baseline 更新の実装例
