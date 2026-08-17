---
file: e2e/projects-roundtrip.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-17
canonical-ref: playwright.config.cjs / js/store.js (validateAndNormalize) / js/project-detail-page.js / e2e/projects.spec.js
---

# e2e/projects-roundtrip.spec.js

## What

既定プロジェクトの詳細ページが **「保存 → 読み戻し」を跨いでも変質しない**ことを固定する
behavior e2e（normalize の冪等性）。

## Why

利用者が何か操作するたび store 全体が `validateAndNormalize` を通って localStorage へ書かれ、
次回以降はそれが読み戻される。**normalize が冪等でないと、操作するたびにデータが少しずつ
変質していく。**

もっとも痛い形は slug の非冪等。重複解消が自分自身を衝突とみなすと保存のたび `-2` が伸び、
**既存のブックマークや共有リンクが全部 404 になる**。一覧は普通に見えるし fatal も出ないので
目視では気付けない（#154 slug 一意化と同じ面の非冪等版）。

### このテストが検出しないもの（実測で確認・誤解防止）

「**normalize が既定データのフィールドを落とす**」class は検出**できない**。起動時の
`State.load()` も同じ normalize を通すので、比較する両辺がどちらも正規化後になるため。

実測: `tech: []` に潰す mutation を当てても両辺が同じく空になり **緑のままだった**。
（さらに前段で `highlights` を潰す mutation も試したが、そもそも詳細ページが `highlights` を
描画しないので当たらなかった —— **検査対象は「そのページが実際に描画するフィールド」から
選ぶ**・#1096 と同じ教訓。）

落とす class は import 往復テスト（`apps-settings-import-shape.spec.js` / #1035〜#1040）と、
そのフィールドを実際に描画するページの個別テストが担当する。

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server (playwright.config.cjs testDir: ./e2e)
```

## Constraints

- **Check 28**: 全 e2e/*.spec.js に test() のネスト無し
- **Check 111**: networkidle 待ちは screenshot (portfolio.spec.js) 以外で禁止
- **Check 114**: test.only/describe.only 無し
- **Check 151**: 全 e2e/*.spec.js 横断で test() title 一意
- **Check 108**: docs/files ミラー 1 対 1 bijection
- **Check 408**: e2e spec は file-size-budget.md の BUDGET-DATA へ登録必須
- **Check 420**: 登録する mutation の `find` は対象 file 内で一意

## Change impact

- `js/store.js` の `validateAndNormalize` / slug 重複解消を変更すると本 spec が RED になる
- 既定プロジェクトのスラッグを変えたら `ROUNDTRIP_SLUGS` も更新する
- spec ファイル rename → docs/files ミラー同期 (Check 108) + BUDGET-DATA 同期 (Check 408)

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `behavior-gate`, `data-fidelity`, `idempotence`
- **測定の作り方（実測で 2 度誤診した）**: スラッグは `js/store.js` の既定値から取る
  （実在しないスラッグは NotFound を返すが「ページは描画された」ようにも見えるので control で弾く）。
  hash 遷移は document を作り直さないので**各ページで reload してフルロードする**
  （しないと前ページの DOM を読み、2,232 文字のはずが一覧の 2,272 文字を掴む）

### For human engineers (新卒レベル)
- 「正規化」は**何度通しても同じ結果になる**必要がある。1 回目と 2 回目で結果が変わる
  正規化は、使うたびにデータを削っていく

### For third parties
- 冪等性という抽象的な性質を、**利用者に見える形**（共有リンクが 404 になる）へ翻訳して
  テストにした例
