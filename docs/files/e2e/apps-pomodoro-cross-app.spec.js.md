---
file: e2e/apps-pomodoro-cross-app.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-27
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / js/pomodoro-page.js / js/state.js
---

# e2e/apps-pomodoro-cross-app.spec.js

## What

ポモドーロと**他アプリの相互作用**に関する behavior e2e。「全リセット」が同時に生きている
複数の状態 (稼働中タイマー / quiz の検索語 / ノート本文) をまとめて初期化するか、裏で走る
タイマーの完了が別アプリの未送信入力を壊さないか、取り込み・別タブ・リロードが稼働中の
runtime をどう扱うか、を扱う。

## Why

ポモドーロは**このアプリで唯一「見ていない間も動き続ける」機能**なので、他の面と衝突する
経路が構造的に多い。過去に実バグが集中している (#1056 完了が別ページの入力を消す /
#1216 別タブの更新で黙って止まる / #1183 取り込みが稼働中の interval を残す)。
単体の挙動を見る `apps-pomodoro.spec.js` とは失敗の性質が違うので分けてある。

2026-08-27 に `apps-pomodoro.spec.js` が 922 行となり Check 52 の advisory (900) を超えたため、
**BLOCKING (Check 365 の 1,000 行) を踏む前に**このテーマを切り出した。

## How

複数タブ (`browser.newContext`) や決定論的な時計操作を使い、runtime (interval) と永続状態の
**両方**を見る。state だけ戻して interval を止め損ねると幽霊 tick が残るため、片方だけでは
捕捉できない。

## Constraints

- BLOCKING な behavior gate の一部。
- test 題名は静的リテラルで書く (template literal だと Check 379/397 が mutation を解決できない)。
- 稼働中の判定は「見えている表示」ではなく state と interval の両方で確かめる。

## Change impact

`js/pomodoro-page.js` の runtime 管理や `js/state.js` の cross-tab 採用を変えるときは本 spec を
同じ commit で見直す。行数を変えたら `docs/architecture/file-size-budget.md` の §2 表と
§4 BUDGET-DATA も同期する (Check 424 / Check 408 が BLOCKING で強制)。

## Audience-specific notes

- **監査人**: 「見ていない間に動くもの」を持つアプリが、他機能と衝突しないことをどう固定して
  いるかの実例。実バグ 3 件がこの面から出ている。
- **採用担当 / 第三者**: 単体では正しい機能同士が、同時に生きたときに壊れる —— という失敗の
  形を、テストの分け方に反映している。
