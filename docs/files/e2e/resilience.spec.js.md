---
file: e2e/resilience.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-17
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / js/store.js (validateAndNormalize) / js/settings-page.js
---

# e2e/resilience.spec.js

## What

ストレージ / import の resilience e2e。corrupt localStorage からの graceful 復帰 (FatalPage 回避)・schema version mismatch での安全 migration (旧データ snapshot + defaults reset)・malformed JSON import のエラー表示・valid JSON import の追記と永続・colliding slug の unique 化・upsert import の更新+追加 (data-loss 回帰)・strict import の user 層置換と defaults 保持・profile github/linkedin の import 生存と URL サニタイズ (XSS-safe) を検証する。

## Why

外部/破損データ ingestion の全経路が同じ正規化を通り crash しないこと (#93/#295 class) と import の data-fidelity を機能ゲートで守る。

### 「壊れたデータ」以外の resilience も本 spec が持つ

| 面 | 何を守るか | 由来 |
| :-- | :-- | :-- |
| 保存 flush | debounce (150ms) 前に離脱しても書きかけが失われない。守っているのは `state.js` の `visibilitychange(hidden) → saveNow()` の **1 本だけ** | #1095 |
| JS 無効 | `<noscript>` に説明 + `llms-full.txt` への導線が出る。追加前は **#content 空・可視の見出し 0 個の白紙**だった | #1103 |

どちらも「壊れ方がエラーとして出ない」class —— 前者は「戻ったら数文字前の状態」、
後者は「白紙」で、利用者は原因を知る手がかりを得られない。

**JS 無効テストを書くときの落とし穴 (実測)**:

- `javaScriptEnabled: false` のコンテキストでは `expect(body).toContainText(...)` が
  **`<noscript>` 配下を拾わず、中身が正しく描画されていても落ちる**
  (同じ状態で `h1.allTextContents()` は正しく返る)。要素そのものを locator で指す
- `a[href$="llms-full.txt"]` はスコープ無しだと **2 件**マッチする
  (sr-only の AIO ブロックにも同じリンクがある)。`noscript` 配下にスコープしないと
  **noscript が無くても通る vacuous な assertion** になる

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server (playwright.config.cjs testDir: ./e2e)
  └─ e2e/*.spec.js は testMatch デフォルト (**/*.spec.js) で自動 discovery
  └─ behavior assertions (screenshot は portfolio.spec.js に残置)
```

## Constraints

- **Check 28**: 全 e2e/*.spec.js に test() のネスト無し
- **Check 111**: networkidle 待ちは screenshot (portfolio.spec.js) 以外で禁止
- **Check 114**: test.only/describe.only 無し (false-green footgun 防止)
- **Check 151**: 全 e2e/*.spec.js 横断で test() title 一意
- **Check 108**: docs/files ミラー 1 対 1 bijection

## Change impact

- test 追加/削除 → CI 時間 + behavior gate カバレッジ + mutation-probe-e2e の対応
- spec ファイル rename → docs/files ミラー同期 (Check 108) + Check 28/111/114/151 の glob 対象

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `behavior-gate`, `resilience`
- portfolio.spec.js から 2026-07-07 に肥大化解消 (3,475 行) の一環でテーマ別分割された 1 ファイル

### For human engineers (新卒レベル)
- 新規 e2e は `e2e/<theme>.spec.js` 命名 (testMatch デフォルトが `.spec.js` を要求)
- test title は全 spec 横断で一意にする (Check 151 がブロック)

### For third parties
- AI 実装下での behavior e2e (機能ゲート) の実装例。テーマ別分割で 1 ファイル ≤1,000 行を維持
