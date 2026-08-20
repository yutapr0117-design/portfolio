---
file: e2e/a11y-contrast.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-20
canonical-ref: e2e/a11y-axe.spec.js / playwright.config.cjs / .github/workflows/playwright-regression.yml / @axe-core/playwright / style.css
---

# e2e/a11y-contrast.spec.js

## What

**コントラストと「色だけに頼らない」知覚**の契約を守る behavior e2e spec (BLOCKING gate)。

- **WCAG 1.4.1 (Use of Color)** — 本文中リンクが色だけで判別されないこと (下線アフォーダンス)
- **WCAG 1.4.3 (Contrast Minimum・AA)** — ブランド primary が白に対し 4.5:1 以上。
  さらに **全ブランド × 全テーマ × 全ルート**で axe `color-contrast` 違反ゼロ。
  drawer / palette / toast を開いた状態も含む。
- **WCAG 1.4.11 ほか (利用者設定メディアの実効性)** — `forced-colors: active` /
  `prefers-contrast: more` が実際に効いていること。

## Why

`e2e/a11y-axe.spec.js` が **996 行**となり Check 365 の BLOCKING (1,000 行) まで
**残り 3 行**になったため、**当たる前に**このテーマの塊を切り出した
(CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。圧縮で誤魔化さず
「いま触っているクラスタ」を切り出すのが最も筋が良い (#927 と同じ判断)。

分離の境界を「コントラスト」に置いたのは、この面が

1. **axe の既定スキャンでは守れない** (render 系違反は render-neutral allowlist の外)
2. **ブランド × テーマの直積**という他と違う走査軸を持つ
3. かつて「知覚できる配色変更は C5 (人間の領域)」として defer されていたが、
   **それが委任範囲の読み違い**だったと canon 側で確定した経緯を持つ

という 3 点で、他の a11y 契約と独立しているため。

## How (usage)

```
npx playwright test e2e/a11y-contrast.spec.js --project=chromium
```

`E2E_HERMETIC=1` を付けると外部ホストが即 NOTFOUND になり goto が速くなる
(Check 416 が CI 側の設定を強制)。

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
  赤になったら rerun せず、落ちたテストを読んで直す (帰属は
  `docs/files/.github/workflows/playwright-regression.yml.md`)。
- **Check 365**: 1,000 行 BLOCKING。**Check 408**: BUDGET-DATA へ登録済であること。
- **Check 424**: `file-size-budget.md` §2 表の実測行数と一致すること。
- テーマの適用は **アプリ本来の経路** (`emulateMedia` の colorScheme + 既定 theme='system')
  を通す。`data-theme` を直接書き換えるとテーマ適用ロジックが壊れていても緑になる。

## Change impact

- 新しいブランドを足したら `CONTRAST_ROUTES` ではなく **ブランド側のループ**に追加する
  (現在は indigo / classic の 2 ブランド × light / dark の 4 組合せ)。
- 意味色トークンを触るときは、**その上に載る文字色**も同時に測ること。
  実測 (2026-08-20): 暗テーマで意味色を明るくしたら、その上の白文字が **1.44** まで落ちた。
- 分割元 (`a11y-axe.spec.js`) との間に共有ヘルパは無い (`focusRing` /
  `CONTRAST_ROUTES` / `expectNoContrastViolations` は本ファイルへ移設済)。

## Audience-specific notes

### For AI agents
- 役割タグ: `a11y`, `wcag-1.4.x`, `contrast`, `blocking-gate`
- 「axe が緑 = a11y が満たされている」ではない。axe は機械判定できる違反の**下限**。

### For human engineers (新卒レベル)
- コントラストは「色を 1 つ変えれば直る」ものではない。用途別
  (淡いチップ上 / プレーン背景上 / solid な意味色背景上) に前景トークンを分ける。

### For third parties
- AI 実装下で WCAG 1.4.3 を全ブランド × 全テーマで機械強制している実装例。
