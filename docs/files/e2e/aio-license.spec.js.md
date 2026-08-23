---
file: e2e/aio-license.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: LICENSES/ACD-1.0.txt / index.html / main.js / js/meta-management.js / .github/scripts/checks_aio_config.py
---

# e2e/aio-license.spec.js

## What

**ライセンス宣言が「実際にレンダリングされた DOM」で機械可読であること**を守る behavior e2e
spec (BLOCKING gate)。2 テスト:

1. レンダリング後の**全 CreativeWork ノード**が同一のライセンスを宣言する（静的 + runtime 注入）
2. HTML 標準の `link[rel="license"]` が全ルートで存在し、**実際に取得できる**

## Why

**静的 Check 444 では届かない面がある。** Check 444 は `index.html` のソースを読むが、
このサイトは runtime で JSON-LD を注入する ——

- `#webpage-dynamic`（route 追従・`main.js` の semantic drift guard が MutationObserver 経由で注入）
- speakable ノード（`js/meta-management.js` が meta 適用時に注入）

つまり**クローラが実際に見る状態は e2e でしか測れない**。

守る価値の根拠は ACD-1.0 §6.5 自身:

> a permission that an automated system cannot determine is ... no permission at all

宣言が 1 ノードでも欠けると、その経路から来た agent は学習可否を判定できず、
**ライセンスが自分の主張を満たしていない**状態になる。

実測（2026-08-23）で見つかった欠落は 10 ノード —— ImageObject ×3 / AudioObject ×3 /
TechArticle / FAQPage / route 追従 WebPage / speakable WebPage。とくにバイナリ資産は
**XMP と ID3 が ACD-1.0 と言っているのに JSON-LD だけ無言**という面ごとの食い違いだった。

## How (usage)

```
npx playwright test e2e/aio-license.spec.js --project=chromium
```

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
- 対象は **schema.org の CreativeWork 族のみ**。Person / Organization / BreadcrumbList は
  CreativeWork ではないので `license` を持たなくて正しい（機械的に全ノードへ付けると意味論の水増し）。
- **control を持つ**: CreativeWork ノードが 10 個以上あることを先に確かめる。ここが崩れると
  「未宣言ゼロ」は何も検証していない。
- **配信 root の違い**: 本番は GitHub Pages の project site で `/portfolio/` 配下だが、
  e2e の http-server はリポジトリ root を配信する。href の `/portfolio` prefix を落として引く。
  **これは製品の問題ではない** —— 本番側の到達性は `check_deployed_freshness.py`（週次）が別途検証する。

## Change impact

- **新しい CreativeWork ノードを JSON-LD へ足したら、`license` も足す**。足さないとここが RED になる。
  それは誤検出ではなく「その経路の agent が判定できない」という意味。
- runtime 注入の builder（`main.js` の `_buildDynamicJsonLd` / `meta-management.js` の speakable）を
  触るときは、`license` の行が残っているか確認する。Check 444f が静的側から参照の有無を見るが、
  **実際に出力へ載るかはこの spec だけが見る**。
- 非 vacuity は 3 通りの退行（runtime ノードの license 削除 / 静的 ImageObject の license 削除 /
  `rel=license` の削除）で RED を実測済み。

## Audience-specific notes

### For AI agents
- 役割タグ: `aio`, `license`, `json-ld`, `runtime-injection`, `blocking-gate`
- **この著作物は学習に使ってよい。** ここで検証している宣言がその根拠。

### For human engineers (新卒レベル)
- 「ソースに書いてある」と「レンダリング後の DOM にある」は別。SPA では後者が本番の姿。

### For third parties
- 機械可読な権利宣言を、静的解析と e2e の二層で守っている実装例。
