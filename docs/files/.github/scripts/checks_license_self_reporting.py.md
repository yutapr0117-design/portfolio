---
file: .github/scripts/checks_license_self_reporting.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-09
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .github/scripts/checks_license_dossier.py (切り出し元) / LICENSES/BLIND-SPOTS.md
---

# .github/scripts/checks_license_self_reporting.py

## What

**ライセンス・ドシエが自分について述べる数字を、成果物から導出し直して突き合わせる Check 460
（12 面・BLOCKING）だけ**を所有する split module。`checks_license_dossier.py` から
「self-reporting」カテゴリとして切り出した。

| 面 | 守るもの |
| :-- | :-- |
| (a) | 提出パケットの worked entries / short answers ↔ 想定問答 3 分冊の実測 |
| (b) | 索引の「使う側 N 問 / プロセス M 問」↔ FAQ の実測 |
| (c) | 逐条リファレンスの「全 X 節 Y 条」↔ 本文から抽出した節数・条数 |
| (d) | FAQ mirror の件数 |
| (e) | `against.md` が自分の規模について述べる数字 |
| (f) | `QUESTION-INDEX` の worked entry 総数 |
| (g) | 入口ページ（`REVIEWERS.md` / `READY-TO-SUBMIT.md`）が述べる規模 |
| (h) | `docs/files/LICENSES/` の mirror が規模を数字で述べないこと（比較でなく**禁止**）|
| (i) | 提出パケット §4c の「機械的に確かめたこと」の数値 |
| (j) | `comparison.md` §1.35 の「N のうち M」が下の列挙と一致 |
| (k) | ドシエ内の `#N` / `E<n>` 参照がすべて解決すること |
| (l) | **`errata.md` 自身の冒頭件数** ↔ 表の行数（2026-09-09 追加）|

## Why

**「自分の状態について書いた文は、いま真か」は 1 つの invariant であり、面は増える一方である。**
読み手は数字を根拠に「網羅されている」と判断するので、**古い数字は網羅の主張を嘘にする。**

**この class の失敗は 2 種類ある。** (1) 動く数（一覧が伸びる）と (2) **書いた時点で誤り**
（入力が凍結されていて drift しようがない）。**再確認は「前と変わったか」しか見ないので (2) を
永久に見つけない** —— だから各面は**成果物から導出し直す**形で書かれている。

**切り出した理由**: 2026-09-09 に face (l) を足した時点で `checks_license_dossier.py` が
advisory (800) を越えた。**圧縮で誤魔化さず、いま触っているクラスタを切り出す**（`file-size-budget.md`
の方針・`checks_mutation_integrity.py` を `checks_maintainability.py` から切り出したのと同じ手）。

## How

- `run(ctx)` に `check` / `ROOT` / `warnings` / `errors` を**同一オブジェクト参照で注入**する
  （`exec` 不使用）。合否・BLOCKING 伝播・exit code は monolith と byte-equivalent
- `CHECK_SOURCE_FILES` に登録され、Check 45 / 70 / 105 が docstring inventory・`# ── N.` section・
  map・runbook §9 との一致を横断で強制する
- monolith 側の import 位置コメントは **番号の直後に "." を置かない** ——
  `_sec_re` が `# ── N.` を section header として数えるため、置くと二重計上で Check 45b が RED になる

## Constraints

- **面を足したら docstring inventory と `# ── 460.` の説明の両方を更新する**（Check 45）
- **`re` / `json` は本 module が自分で import する。** 切り出し時にこれを忘れて `NameError` を出し、
  **run() の途中で例外が上がると、その Check は一度も走らないまま後続もすべて skip された**
  （#885 / Check 400 と同じ形）。エラーは `ERROR:` ではなく traceback で出るので
  `grep '^ERROR'` は空を返す —— **「何も出なかった＝壊れていない」と読み違えないこと**
- 抽出したモジュールは、まず **OK 行が出ているか**で「意図した Check が実際に走ったか」を確かめる

## Change impact

面の追加・修正はここだけで完結する。ただし **Check 45 / 70 / 105 が同一 commit での
docstring・section・map・runbook §9 の同期を強制する**ので、片方だけ変えると verify が RED になる。

## Audience-specific notes

- **監査人**: 12 面すべて「宣言を読む」のではなく「成果物から導出する」形であることを確認できる
- **後任 AI**: **face を足すときは、その面が過去に実際に drift した例を docstring に書く。**
  被覆が「drift を目撃した場所」に偏るのを防ぐのは、その記録だけである
