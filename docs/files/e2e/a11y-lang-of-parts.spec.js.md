---
file: e2e/a11y-lang-of-parts.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: e2e/a11y-axe.spec.js / js/pure-utils.js / playwright.config.cjs / .github/workflows/playwright-regression.yml / docs/architecture/file-size-budget.md
---

# e2e/a11y-lang-of-parts.spec.js

## What

**WCAG 3.1.2 (Language of Parts・Level AA)** だけを守る behavior e2e spec (BLOCKING gate)。

`html lang="ja"` の文書の中に**英語だけの塊**があるとき、その要素に `lang="en"` が
付いていることを検査する。4 テストで構成する:

1. **全 16 ルート**を歩いて未指定の塊を検出する一般ゲート (絵文字や `→` を含む見出しも対象)
2. quiz 限定の走査 (章題・ラベルが英語のみになりやすい面)
3. 固定リテラルの英語文字列 (home / about)
4. **data 由来**のテキスト (home の badge = `featured.category` / resume の職種 = `profile.title`)

## Why

日本語の SR は `lang` が `ja` のままの英語を**日本語の音韻で読み上げる**。
"Executive Summary" が「エグゼクティブ サマリー」ではなく綴り字を日本語読みした音になり、
何の見出しか判別できなくなる。

**この面で behavior e2e が唯一の gate である理由**: axe には該当ルールが無い
(`html-lang-valid` は文書全体の lang しか見ない)。行の言語は data 側で混在しうるので
静的 Check でも決められず、**描画時に文字種で判定する**しかない
(判定の実体は `js/pure-utils.js` の `langOfText` に一本化されている)。

**なぜ独立した spec なのか**: `a11y-axe.spec.js` が **950 行**となり advisory 予算 (900) を
超え、Check 365 の BLOCKING (1,000) まで 50 行に迫っていた。**当たってから慌てるのではなく
手前で**、単一の達成基準という coherent な塊として切り出した
(CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。
先行例の `a11y-contrast.spec.js` (残り 3 行で切り出し) より早い段階で動けている。

## How (usage)

```
npx playwright test e2e/a11y-lang-of-parts.spec.js --project=chromium
```

`E2E_HERMETIC=1` を付けると外部ホストが即 NOTFOUND になり goto が速くなる
(Check 416 が CI 側の設定を強制)。

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
  赤になったら rerun せず、落ちたテストを読んで直す。
- **Check 365**: 1,000 行 BLOCKING。**Check 408**: BUDGET-DATA へ登録済であること。
- **Check 424**: `file-size-budget.md` §2 表の実測行数と一致すること。
- **意図的に対象外**にしている塊がある (機械的に全部へ `lang` を付けるのは意味論の水増し):
  英単語 1 つだけのラベル / メールアドレス・URL・版数のような識別子 / 固有名詞だけの塊。
  除外条件はコード中に書いてあり、**緩めると RED になる**。

## Change impact

- **新しい英語の可視文字列を足したら、ここが RED になる**。それは誤検出ではなく
  「`lang="en"` を付け忘れた」の意。除外条件を緩めて黙らせてはならない。
- 抽出元 (`a11y-axe.spec.js`) との間に共有 module は**無い**。e2e は spec 完全自己完結が
  house pattern なので、`A11Y_ROUTES` と `settleContent` は**複製**してある。
  抽出時にこれを持ってこなかったため `ReferenceError: settleContent is not defined` で
  1 件が **332ms の早期 throw** となり、a11y 回帰に見える形で失敗した (2026-08-23 に是正)。
  **spec を割るときは、抽出範囲の外にある共有物が同行しているかを必ず確かめること。**
- `settleContent` を消すと「見出しは変わったが本文はまだ」の状態を走査してしまい、
  **違反ゼロと誤報告する**。見出しの変化だけでは待ちとして不足する。

## Audience-specific notes

### For AI agents
- 役割タグ: `a11y`, `wcag-3.1.2`, `language-of-parts`, `blocking-gate`
- 「axe が緑 = a11y が満たされている」ではない。axe は機械判定できる違反の**下限**であり、
  本ファイルが守る達成基準はそこに含まれない。

### For human engineers (新卒レベル)
- `lang` 属性は「見た目に出ない」ので、目視レビューでは永久に見つからない。
  だからこそ機械が見る層が要る。

### For third parties
- 多言語混在ページで WCAG 3.1.2 を e2e で機械強制している実装例。
  判定を静的解析でなく**描画後の DOM の文字種**で行っている点が要点。
