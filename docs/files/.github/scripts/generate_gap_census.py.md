---
file: .github/scripts/generate_gap_census.py
audience: ai, human (新卒), 監査人, OSI license-review participants, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.gap-census.md (この script の生成物) / .github/scripts/measure_gap_claim.py (同じ母集団で送る本文の主張を測る script)
---

# .github/scripts/generate_gap_census.py

## What

`LICENSES/ACD-1.0.gap-census.md`（ACD-1.0 の 3 つの gap を、OSI 承認済みで非 deprecated の全ライセンスに当てた全数表）を**生成する script**。
3 つの動作を持つ:

- `--fetch` —— SPDX `license-list-data` から本文を取得し、sha256 と取得時刻をキャッシュ（`GAP_CENSUS_CACHE`・既定 `/tmp/gap-census-cache`）に記録する
- 引数なし —— キャッシュから census を書き出す
- `--check` —— 書き換えずに、生成結果が現在の census と一致するかだけを見る

## Why

census は「承認済み N 本の全数に当てた」と主張する文書で、**誰でも同じ数を出し直せなければ主張は検証できない**（`measure_gap_claim.py` が「the command is in the repository」を真にするために在るのと同じ理由）。
2026-09-25 の初版は一時ディレクトリの生成スクリプトで作られ、リポジトリに残っていなかった。

## How

- **本文中の件数はすべて表を数えて出す**。手で書いた数は無い（Check 460 / 476 の教訓: 手で書いた数は他の更新に巻き込まれて drift する）
- **手で判定したもの**（特許許諾の分類 `明示` / `M-免責` / `M-方針` … と範囲 `S1` / `S2` / `S3`）は script 内の定数に**データとして**置いてある。判定の根拠は census 本文の「判定基準」節
- **`READ_PATENT`** は 2026-09-25 に本文を読んで分類した `patent` を含む本の全集合（3.29.0・82 本）。新しい版でここに無い本が `patent` を含んでいたら**生成を止める** —— 読まずに既定値 `明示` / `S1` に落ちるのを防ぐため
- 移植の証明: 一時ディレクトリの版と同じキャッシュから生成した出力が、既存の census と**バイト単位で一致**することを `--check` で確認した。安全装置は、既読集合から 1 本外すと止まる（exit 1）ことを確認した

## Constraints

- **CI では走らせない** —— 外部取得は壊れやすい（`CLAUDE.md` §7）。`spdx.org` は一部の環境から 403 になるため、GitHub 上の同一データ（`raw.githubusercontent.com/spdx/license-list-data`）を使う
- 取得に失敗した本は 0 件として数えず `failed` に記録し、exit 1 を返す

## Change impact

SPDX の新しい版を当てるときは `--fetch` → 生成 → 差分を読む。本が増えて止まったら、その本文を読んで分類定数と `READ_PATENT` に足す。
census 本文を手で直すと、次の生成で上書きされる（または `--check` が DRIFT を返す）。

## Audience-specific notes

- **審査者**: 分類は機械判定ではなく人が読んだもの。別の読み手なら `CECILL-2.1` の不行使約束を `明示` に入れないかもしれない —— census の「不利な材料」節がその限界を述べている
