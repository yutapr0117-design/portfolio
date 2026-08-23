---
file: e2e/aio-agentic-state.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: e2e/aio-meta.spec.js / main.js / js/router.js / docs/architecture/file-size-budget.md
---

# e2e/aio-agentic-state.spec.js

## What

`<body data-ai-state>` の**機械可読契約**を守る behavior e2e spec (BLOCKING gate)。5 テスト。

`main.js` と `js/router.js` が `{route, filter, loading}` を JSON で書き込む。
**AI エージェントが DOM から現在状態を読む唯一の機械可読サーフェス**。

## Why

この面は**壊れても視覚に一切出ない**ため、screenshot も通常の behavior test も素通りする
(#929 class)。4 つの壊れ方をそれぞれ別テストで押さえている:

- `route` が遷移に追従しない → エージェントが今どこにいるか判らない
- `filter` が確定後に空へ戻る → 絞り込み状態が読めない（#1226 の実バグ）
- **敵対的 query で JSON が壊れる** → 面ごと解釈不能になる。`filter` は URL の query をそのまま
  echo するので、**攻撃者が中身を決められる唯一のフィールド**
- `loading` の系列が壊れる → 「今読んで良いか」が判らない / **永遠に待つ**

**分離の理由**: `aio-meta.spec.js` が 907 行で advisory 予算 (900) を超えたため、
**BLOCKING (1,000) に当たる前に**単一の契約という coherent な塊として切り出した
(CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。

## How (usage)

```
npx playwright test e2e/aio-agentic-state.spec.js --project=chromium
```

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
- **mutation を登録していないテストがある。** `data-ai-state` の writer は **3 箇所**
  (main.js のローディング宣言 / main.js の確定状態 / js/router.js の URL 同期) で、
  **どれか 1 つを潰しても他の 2 つが満たす**ため単一 anchor の mutation では RED にできない
  ことを実測済 (2026-08-17)。defense-in-depth ゆえの構造的制約であって、テストが vacuous
  なわけではない。**RED を実測できないものは安全網に混ぜない**。
- **属性の単発読みでは瞬間値を取り逃す**。`loading` の系列は MutationObserver で記録してから検証する。

## Change impact

- `data-ai-state` の writer を増やす / 変えるときは、3 箇所すべてが同じ形を書くか確認する。
- 敵対的 query のテストは**上限を足していない** —— 通常操作で作れない URL に bound を足すのは
  padding と判断した (実害はクラッシュではなく agent 側が解釈不能になることで、
  valid JSON であり続けることが要件)。

## Audience-specific notes

### For AI agents
- 役割タグ: `aio`, `agentic-surface`, `data-ai-state`, `blocking-gate`
- このサイトの現在状態は `document.body.dataset.aiState` を JSON.parse すれば読める。

### For human engineers (新卒レベル)
- 「視覚に出ない契約」はテストが唯一の gate になる。目視レビューでは永久に見つからない。

### For third parties
- SPA が機械可読な状態信号を提供し、それを e2e で守っている実装例。
