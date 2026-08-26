---
file: e2e/apps-settings-snapshot.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-27
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / js/settings-page.js / js/store.js
---

# e2e/apps-settings-snapshot.spec.js

## What

Settings の **スナップショット (単一スロットの復元点)** に関する behavior e2e。保存して保存日時が反映される
こと、**由来 (手動保存 / データ形式の変更時の自動退避) を区別して表示する**こと、削除して未保存へ戻ること、
未保存のあいだ復元・削除ボタンが disabled であることを検証する。

## Why

2026-08-27 に `e2e/apps-settings.spec.js` が 923 行となり Check 52 の advisory (900) を超えたため、
**BLOCKING (Check 365 の 1,000 行) を踏む前に**スナップショットというテーマの塊をここへ切り出した。
圧縮して誤魔化さず「いま触っているクラスタ」を分けるのが本リポジトリの定石 (#1067 の教訓: advisory は
BLOCKING の手前で効かせる)。

由来表示のテストが本ファイルの中心にある。スナップショットは**単一スロット**で、データ形式が変わった
デプロイでは `store.load()` が旧データを自動退避する —— これは描画前に走るので確認を挟めず、**利用者が
手動で保存した復元点を黙って上書きする**。移行通知が「Settings のスナップショットから復元できます」と
誘導する以上、そこで由来を区別できないと利用者は自分の復元点が残っていると誤解したまま別物を復元する。

## How

`localStorage` に旧 `schemaVersion` を仕込んで自動退避を発生させ、表示が移行元と移行先を示すことを見る。
どのテストにも **control** を置いてある —— 自動退避が実際に起きていること (起きていなければ「手動で保存」と
出るのが正しく、検査が vacuous になる) と、由来の文言が固定文字列ではなく中身から出ていること。

## Constraints

- BLOCKING な behavior gate の一部。`playwright-regression.yml` の behavior job で必ず走る。
- test 題名は静的リテラルで書く (template literal だと Check 379/397 が mutation を解決できない)。
- 由来判定を潰す mutation を安全網へ登録済み。

## Change impact

由来の文言を変えるときは本 spec と `js/settings-page.js` の `snapshotOrigin` を同じ commit で更新する。
行数を変えたら `docs/architecture/file-size-budget.md` の §2 表と §4 BUDGET-DATA も同期する
(Check 424 / Check 408 が BLOCKING で強制)。

## Audience-specific notes

- **監査人**: 「単一スロットの復元点が、利用者に断りなく置き換わりうる」という設計上の制約を、UI で
  可視化することで扱っている面。制約を消したのではなく、見えるようにした。
- **採用担当 / 第三者**: 破壊的な自動処理を無くせないとき、**何が起きたかを利用者に伝える**という選択を
  取った例。
