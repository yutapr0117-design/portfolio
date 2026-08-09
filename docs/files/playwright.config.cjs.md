---
file: playwright.config.cjs
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: e2e/portfolio.spec.js / .github/workflows/playwright-regression.yml
---

# playwright.config.cjs

## What

Playwright 設定。CJS 形式 (Node 24 でも安全)。Chromium で e2e 実行、http-server で `./` を serve、snapshot 比較設定、retries 等。

## Why

ESM (config.mjs) を選ばずに CJS にしたのは Playwright v1.60 の安定性と CI 環境互換性のため。

## How (usage)

```
npx playwright test --config=playwright.config.cjs
  └─ webServer: npx http-server -p <port>
  └─ projects: chromium のみ
  └─ snapshot pixel diff threshold 設定
```

## Constraints

- **Check 23**: JS 構文 valid (node --check)
- **Check 51**: バージョン pin が runbook と一致 (1.60.0)

## このリポジトリの e2e で繰り返し踏んだ落とし穴（実測に基づく）

テストは「壊れる」より **「鈍る」** 形で失われる（前提が崩れて緑のまま無力化する）。以下はいずれも
**実際に vacuous なテストや false-red を生んだ**もので、書く前に知っておくと 1 サイクル節約できる。

| 落とし穴 | 何が起きるか | 正しい書き方 |
| :-- | :-- | :-- |
| `waitForLoadState('networkidle')` | 外部 Fonts / service worker の background fetch で CI が 30s ハングする flake（screenshot 以外では禁止・Check 111） | `domcontentloaded` + expect の auto-wait |
| **不変性の検査に `expect.poll`** | poll は**最初の観測で条件を満たした瞬間に成功**するため、その後に起きる変化を見逃す。「スクロール位置が動かないこと」を poll で書いたら 2 つの実バグ mutation が**両方素通り**した | settle を待ってから **1 度だけ**確定値を読む |
| 不在の検査（`toHaveCount(0)`）を goto 直後に評価 | async 描画とレースし「まだ無い」を「無い」と誤認する | 先に「在るはず」の要素の visible を待って描画を確定させる |
| `fill()` で入力を検証 | value を直接代入するため focus 喪失系のバグを検出できない（quiz 検索の focus 喪失が gate を素通りした） | 実キー入力の `type()` / `keyboard.insertText()` |
| `toBeFocused()` | 並列ワーカーで document が inactive になり `unexpected value "inactive"` で間欠 RED（8 回中 3 回） | `document.activeElement` を `evaluate` で読む |
| `offsetParent !== null` で可視判定 | **`position: fixed` の要素では常に null** になり、開いている drawer を「閉じている」と誤報告する | `getBoundingClientRect()` + computed style |
| 通常の `click()` で sticky 要素を検証 | actionability 判定でページがスクロールし、実機のタップ挙動と乖離する | `evaluate` 内の programmatic click |
| `--reporter=line` の出力を `tail -N` で読む | **失敗一覧はサマリの後に出る**ため、`tail -2` だと `2 failed` の行が切れて `27 passed` だけが見え、**失敗を成功と誤読する**（実際に 2 度踏み、既存テストを壊したまま PR を出した） | `grep -E "failed\|passed"` で明示的に拾う |
| `MUTATION_PROBE=1` を付けて SW 関連テストを回す | この env は **設計上 service worker を block** するため、SW 登録テストは必ず落ちる（config の env-gate 参照）。原因を製品側と誤診する | SW を含む検証は env なしで回す（CI と同条件） |
| mutation の `-g` を緩い語で当てる | 別の test に当たって「pass」と読み違える（実際に一度誤読した） | **正確な test title** を使う（Check 397 が一意解決を強制） |

## Change impact

- threshold 変更 → visual baseline の感度に影響
- webServer 変更 → http-server 等の依存と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `playwright-config`, `cjs-format`

### For human engineers (新卒レベル)
- e2e の設定。CSS 変更で snapshot diff が出るかの threshold もここ

### For third parties
- Boring Technology + e2e の組み合わせ実装例
