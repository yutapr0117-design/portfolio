---
file: .github/scripts/checks_license_dossier.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .github/scripts/checks_governance_sync.py (分割元) / LICENSES/README.md (対象ディレクトリの索引)
---

# .github/scripts/checks_license_dossier.py

## What

ACD-1.0 ドシエ（`LICENSES/`）が**自分自身について述べる事実**を実測と突き合わせる Check 群。
`checks_governance_sync.py` から 2026-09-05 に切り出した split module で、`run(ctx)` により monolith
から呼ばれる。内包する Check:

- **458**（a/b）— 投稿先 (venue) の記録が `LICENSES/FROZEN.md` の `VENUE-DATA` 単一ソースと一致し、
  宣言外の venue へ「投稿済み」と主張していないこと。
- **459** — `LICENSES/*.md` がすべて索引 `LICENSES/README.md` から到達できること。
- **459b** — その索引の**冒頭 20 行に英語の入口案内**があること（ディレクトリを開いた審査者が
  最初に見る自動描画ページなので、日本語しか無ければ英語の入口の存在自体を伝えられない）。
- **460**（a〜g）— ドシエが自己申告する件数が実測と一致すること。提出パケット / FAQ / 逐条
  リファレンス / FAQ mirror / `against.md` の自己規模 / `QUESTION-INDEX.md` の総数 /
  **入口ページ `REVIEWERS.md` と `READY-TO-SUBMIT.md` の規模**の各面。
- **461b**（ADVISORY）— `LICENSES/*.md` の frontmatter `last-updated` が 14 日以上 stale でないこと。

## Why

守っている invariant は 1 つの族である —— **ドシエは自分自身について事実を述べており、その事実は
実測と一致する**（投稿先 / 到達性 / 入口の言語 / 自己申告の件数 / 日付の鮮度）。ドシエは OSI 審査の
往復を短くするために「疑問はリポジトリを見れば潰せる」形で書かれており、**自分について述べた数字や
状態が古いと、網羅の主張そのものが嘘になる**（実測: 入口ページが不利な事実を 14 件と申告し実体
57 件だった 2026-09-05 の #58）。

分割の直接の動機は肥大化。同日にドシエ側の Check が育って `checks_governance_sync.py` が 966 行に
達し Check 52 の advisory (950) が鳴ったので、**圧縮で黙らせず、いま触っている塊を切り出した**
（CLAUDE.md §7 に繰り返し記録されている応答）。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置**（Check 458 があった位置）で
  `checks_license_dossier.run(_ctx)` を呼ぶ。
- `run()` は `ROOT` / `check` / `warnings` を ctx から unpack し、`re` / `json` / `subprocess` /
  `datetime` を module import する。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイルを含む）を横断集約する。

## Constraints

- **module-global 結合なし**: 依存はすべて `ctx` 経由。`exec` 不使用。
- **自己整合（Check 45/70/105/431）**: docstring inventory と `# ── N.` section は 1 対 1、monolith と
  合わせて bijection。`CHECK_SOURCE_FILES` への登録と `run(_ctx)` の呼び出しがそろって初めて機能する。
- **凍結との関係**: 本 module は `LICENSES/ACD-1.0.txt` などの**本文を検査しない**。凍結中の本文は
  Check 453 が sha256 で pin しており、本文の性質を検査する Check は定義により vacuous になる。
  ここが見るのは本文の**周辺文書**が述べる事実である。

## Change impact

Check を足す / 面を足すときは、docstring inventory・`# ── N.` section header・実装の 3 つを同時に
更新する（Check 45 が bijection を BLOCKING 強制）。行数を変えたら
`docs/architecture/file-size-budget.md` §2 の実測行数も同 commit で同期する（Check 424）。

## Audience-specific notes

- **監査人**: 本 module が緑であることは「ドシエの記述が実測と一致する」ことの機械的な保証であり、
  内容の正しさの保証ではない。内容の反対材料は `LICENSES/ACD-1.0.against.md` にある。
- **学術研究者 / 第三者**: 自己申告の件数を検査する層が要る理由は `against.md` #52 / #55 / #58 に
  実例つきで記録されている（いずれも「書いた数字が翌日には古い」形で起きた）。
