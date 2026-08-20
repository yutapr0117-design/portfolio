---
file: e2e/apps-input-contract.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-20
canonical-ref: e2e/apps-task.spec.js / js/apps.js / playwright.config.cjs
---

# e2e/apps-input-contract.spec.js

## What

task / todo の**テキスト入力欄の契約**を守る behavior e2e spec (BLOCKING gate)。

- 空 / 空白だけの入力は項目を作らない (trim ガード)
- **表示だけの操作** (絞り込み) の巻き添えで未送信の入力を消さない (#1055)
- Enter の連打 / キーリピートで同じ項目を二重登録しない (#1061)

## Why

三つとも「**利用者が打った文字が黙って失われる / 意図せず増える**」class。視覚的には
一瞬の出来事なので、**気付いたときには理由が分からない**のが共通点で、だからこそ
機械で押さえる価値がある。

- 絞り込みで入力が消える件は実バグだった (#1055・8 文字 → 0)。原因は「表示だけの操作」
  なのに `window.render()` で `#content` ごと作り直していたこと。
- Enter 連打の二重登録も実バグ (#1061)。入力欄が空になるのは**非同期な再描画の副作用**
  なので、連打では `e.target.value` がまだ元の文字列を持つ。

元は `e2e/apps-task.spec.js` にあったが、同 file が **957 行**となり Check 365 の
BLOCKING (1,000 行) まで**残り 43 行**になったため、**当たる前に**切り出した
(CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。

## How (usage)

```
npx playwright test e2e/apps-input-contract.spec.js --project=chromium
```

`E2E_HERMETIC=1` を付けると外部ホストが即 NOTFOUND になり goto が速くなる (Check 416)。

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
- **Check 365** (1,000 行) / **Check 408** (BUDGET-DATA 登録必須) /
  **Check 424** (§2 表の実測行数一致)。
- 「連打」は `press()` の連続で表現しない —— 1 回目が起こす**再描画の速さ次第で 2 回目
  以降が新しい空の要素に当たる**ため、ローカルで再現しても CI では再描画が勝つ。
  同期的に keydown を投げる (落とし穴表を参照)。

## Change impact

- 入力欄を新設したら、**この 3 つの契約を満たすか**をここで確認する。特に
  「表示だけの操作」で再描画を起こす実装 (`State.update`) を入れると (2) が壊れる ——
  Check 130 が静的に、この spec が振る舞いで、二層で守っている。

## Audience-specific notes

### For AI agents
- 役割タグ: `behavior-e2e`, `input-contract`, `data-loss`, `blocking-gate`

### For human engineers (新卒レベル)
- 「表示を変えるだけ」の操作で全体を作り直すと、**利用者が打ちかけた文字を巻き添えで消す**。
  再描画の範囲は「変わったもの」に限る。

### For third parties
- 入力の消失という**再現しにくい体験バグ**を、機械で恒久的に押さえている実装例。
