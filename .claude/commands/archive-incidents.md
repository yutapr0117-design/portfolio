---
description: Consolidate accumulated incident-artifacts (improvement-notes / decision records) into a track archive at a major-release boundary, keeping the folder lean without losing the proof-of-work trail. Run only at a major-release boundary or when the folder is hard to navigate, never reflexively in a daily increment.
---

incident-artifacts の集約（圧縮）コマンド。`docs/incident-artifacts/` に溜まった `improvement-notes-*.md` / `decision-*.md` を、**閉じたトラック単位で** archive へ畳んでフォルダの見通しを保つ。日常 increment では実行しない。

## 目的（なぜ集約するのか）

`docs/incident-artifacts/` の notes/decision は increment ごとに 1 本ずつ増える。これは `file-size-budget.md` の分類でいう **archive-growth-ok**（証跡として増えてよい肥大化）であり、**行数**で削減圧力をかけてはならない。しかし数十本がフラットに溜まると **ファイル数**の見通しが落ちる。`AI2AI.md` が Session Record を `AI2AI-archive.md` へ畳んでいるのと同じ哲学で、**閉じたトラックの notes を 1 つの archive ファイルへ時系列連結し、個別ファイルを畳む**。proof-of-work なので削除ではなく **集約（append-only な移設）** であり、文言は 1 バイトも改変しない。

## いつ実行するか（トリガー）

- `Pipeline-Version` の major bump（例 v80 → v90）を伴うリリース時
- Playwright baseline 取得 → Stage 5（`main.js` 物理分割）完了などの構造的マイルストーン到達時
- フォルダが運用上見通しづらい、とオーナー（横井雄太）が判断したとき
- **進行中トラックは畳まない**（毎回畳むと差分が騒がしく、現在進行の参照が切れる）。畳むのは「閉じたトラック」（例: foundation-correction phase の v74 系）に限る。

## 手順（非破壊・append-only）

1. **集約対象の選定**: 「閉じた」トラックの notes/decision を選ぶ。進行中・直近で参照される notes は残す。迷ったら残す（残す方が安全）。
2. **参照の確認（最重要・参照切れを作らない）**: 他文書（`docs/architecture/*` の各 map、`AI2AI.md`、`llms-full.txt`、`README.md`、`CLAUDE.md` 等）が個別 notes を参照していないか grep で確認する。参照の性質で扱いを分ける:
   - **Markdown リンク `](path)`** の場合 → 畳むとリンク切れ。(a) 残すか、(b) リンクを archive 内アンカーへ更新してから畳む。
   - **Session Record 等の「履歴言及」**（「v75 で decision-v75 を新規追加」のような **append-only な過去の作成事実**で、Markdown リンクでないもの）の場合 → その記述は当時の事実として正しく、ファイルの物理移動で偽にならない。**AIO 正本層（`AI2AI.md` / `llms-full.txt` / `AI2AI-archive.md`）を編集してはならない**（C6・digest 連鎖を避ける）。archive 側の各セクション見出しに元パスと由来（Session 番号等）を明記して追跡可能性を確保し、AIO 層は温存する。
   - 判定は `grep -rn "](.*<name>" <docs>` でリンク有無を機械確認する（リンクが無ければ全て履歴言及＝AIO 層温存可）。
3. **archive へ連結**: 集約先 `docs/session-records/incident-artifacts-archive-<track>.md`（`<track>` 例: `v74`）へ、対象を **時系列・内容改変なし** で連結する。**手入力転記を一切せず `cat` で byte 等価に連結**し（Copilot 型の取りこぼし/改変事故を物理的に排除）、各 note の冒頭に元ファイル名と元コミット SHA を註記する。集約先を `docs/session-records/` に置くのは、`Check 42`（incident-artifacts 直下の命名・配置）の対象外にして畳む過程で 42 を誤発火させないため。
4. **byte 等価の確認 → 個別ファイルの削除**: archive 行数＝（元ファイル合計 + メタ/区切り）で整合し、各原本の先頭行が archive に含まれることを確認してから、明示パスの `git rm` で個別ファイルを畳む（`git add -A` / `git rm -r .` は使わない）。
5. **digest 影響の確認**: 集約先・削除ファイルが digest 対象でないことを `update_aio_digests.py` の明示リスト（glob ではない）で確認する。`docs/session-records/` では **`AI2AI-archive.md` だけ**が digest-tracked ゆえ、新設 archive は非 digest（digest 再生成不要）。新 archive を digest-tracked にするか否かはオーケストレーター判断。
6. **機械整合の再取得**: `Check 42` は `iterdir()` で動的列挙し命名のみ検査する（本数を固定検査しない）ため、削除後も残りが規約通りなら緑。`Check 45`（docstring 自己整合）にも無影響。
7. **数値・参照の as-measured 同期**: `total-check-runbook.md §9`「追跡ファイル総数」を集約後の `git ls-files | wc -l` に同期する（runbook §7.2 の as-measured 同期義務）。`file-size-budget.md` §0 の集約記録も更新。
8. **検証**: `/verify`（`npm run verify` が exit 0）。AIO 正本層・binary・`style.css`・`main.js` が byte-identical であることを SHA-256 で証明する（集約は `docs/` 内に閉じるため、ここは必ず不変）。
9. **記録**: 集約の事実を `repository-maintainability-map.md` の changelog と、必要なら archive ヘッダのメタデータに残す（何を畳み何を残したか）。

## 非破壊の鉄則

- 集約は **削除ではなく移設**。proof-of-work の文言は 1 バイトも改変しない（`cat` 連結 + 行数整合で担保）。
- **AIO 正本層（`AI2AI.md` / `llms-full.txt` / `llms*` / `.well-known/*`）・binary・shipped コード（`main.js` / `index.html` / `*.js` / `style.css`）には触れない。** 集約は `docs/` 内に閉じる。履歴言及は append-only で温存する。
- 進行中トラックの参照を壊さない（手順 2 が要）。
- これは「肥大化解消」ではなく **証跡の整理**である。proof-of-work の総量は減らさない。
