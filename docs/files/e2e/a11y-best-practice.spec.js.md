---
file: e2e/a11y-best-practice.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-21
canonical-ref: e2e/a11y-axe.spec.js / e2e/a11y-contrast.spec.js / playwright.config.cjs / .github/workflows/playwright-regression.yml / @axe-core/playwright
---

# e2e/a11y-best-practice.spec.js

## What

axe の **`best-practice` タグ**の違反を全 16 ルートで走査し、**既知の 1 パターン以外が
新たに入らないこと**を BLOCKING で守る behavior e2e spec。

## Why

`e2e/a11y-axe.spec.js` は **WCAG タグの rule だけ**を allowlist で強制する。
`best-practice` タグの rule —— WCAG の達成基準ではないが ARIA / HTML の**規範的な
適合要件**を見るもの —— は、違反が何件出ても **どのゲートにも現れなかった**。
新しい違反が入っても永久に無音で、リポジトリが繰り返し踏んできた
「**宣言されているのに、それを見ている層が一つも無い**」class そのものだった。

実測 (2026-08-21・全 16 ルート・既定内容) では、現状の best-practice 違反は
**1 ルール / 2 ルート / 23 ノード**しかない:

| rule | impact | ルート | ノード |
| --- | --- | --- | --- |
| `aria-allowed-role` | minor | `#/projects` | 18 |
| `aria-allowed-role` | minor | `#/apps` | 5 |

いずれも `<article role="listitem">`。ARIA in HTML が `<article>` に許す role は
application / document / feed / main / none / presentation / region で `listitem` は含まれない。

### なぜ「既知の例外」として据え置くのか (変更しない判断も成果物)

実 a11y ツリー (CDP `Accessibility.getFullAXTree`) を測ると **Chromium はこの上書きを
正しく honor している** —— `list=1 / listitem=18 / article=0`。つまり #1013 が入れた
リスト意味論は実際に機能しており、`<article>` 自身の意味論は**上書きで既に失われて
いる**ので `div` へ変えても失うものは無い。だが**得られるものも測れない**:
他エンジン (Firefox / WebKit) は本リポジトリにインストールされておらず、
「そちらで壊れる」は実測できない仮定にとどまる。一方コストは実在し、
`e2e/**` の `article` 参照は 70 箇所ある。

CLAUDE.md §7「一般論を根拠にコードを足すな —— 必要性を実測で示せないなら padding」
に従い、**変更せず・可視化する**を選んだ。この spec がその可視化層である。

## How (usage)

```
npx playwright test e2e/a11y-best-practice.spec.js --project=chromium
```

`E2E_HERMETIC=1` を付けると外部ホストが即 NOTFOUND になり goto が速くなる
(Check 416 が CI 側の設定を強制)。

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
- pin するのは **`ルート + rule` の組**であって**ノード数ではない**。プロジェクトを
  1 件足せば 18→19 になるが、それは同じ既知パターンであって新しい違反ではない。
  別ルート・別 rule で出たときだけ RED になる。
- axe は View Transition のアニメーション中に走らせると**過大に出る**
  (実測 #1158: 3 ルートで待ち 120ms なら 594 件 / settle 後は 30 件)。
  `waitForTimeout(350)` はそのための settle。
- **control を 2 つ持つ**: 全ルートを走査できたか / 既知の例外すら検出できているか。
  後者が無いと `withTags(['best-practice'])` が効かなくなった時に
  「違反ゼロ」と区別が付かず vacuous に緑になる。

## Change impact

- 新しいルートを足したら `BP_ROUTES` に追加する。
- `BP_KNOWN` を**増やすのは既知の例外を増やす行為**なので、増やす前に
  「なぜ直さないのか」を実測付きでここに書くこと。安易に baseline を緩めると
  ESLint baseline (#278) と同じ「名ばかりの regression guard」になる。
- axe を bump したときは新 rule が best-practice タグで増えうる。RED になったら
  **まず実バグかを実測**し、そのうえで直すか例外にするかを決める。

## Audience-specific notes

### For AI agents
- 役割タグ: `a11y`, `axe`, `best-practice`, `baseline`, `blocking-gate`
- 「axe が緑 = a11y が満たされている」ではない。axe は機械判定できる違反の**下限**で、
  さらにその既定スキャンは**タグで絞られている**。射程の外は誰も見ていない。

### For human engineers (新卒レベル)
- 「今は違反が無い」ことより「**新しい違反が入ったら気付ける**」ことが大事。
  baseline を pin するのはそのための最小の仕掛け。

### For third parties
- ゲートの射程外を「無いこと」にせず、実測して baseline 化した実装例。
