---
file: .github/scripts/checks_license_quotation.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-14
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .github/scripts/checks_license_dossier.py (切り出し元) / .github/scripts/verify_dossier_quotations.py (外部 source 側の道具) / LICENSES/AUDIT-LEDGER.md
---

# .github/scripts/checks_license_quotation.py

## What

**引用符の中身は、帰属先に実在する** —— この 1 つの invariant だけを所有する split module。
現在の内容は **Check 470（BLOCKING）**。

ドシエ (`LICENSES/**`) が `§X の "…"` / `§X says "…"` の形で ACD-1.0 の条項に語を帰属させて
いるとき、その語が**当の条項に実在すること**を、リポジトリ内に凍結された `ACD-1.0.txt` と
突き合わせる。

## Why

**ドシエは審査者に「本文を当たれ」と言う文書である。** その本文の語を引いたとき、引用が当の
条項に無ければ、審査者は**我々が読んでいない条項について論じている**と読む。弁護士のレビューが
無いという最大の弱点に対して我々が対置しているのは「機械的に確かめられること」なので、
**引用が外れていると節ごと逆の証拠になる。**

**この class の欠陥はどの層にも出ない。** 視覚にも behavior e2e にも出ず、公開面の sha256 照合
（`check_deployed_freshness.py`）はバイト一致しか見ない。**引用の忠実性だけを見る層が無ければ、
どの層も見ていない。**

2026-09-14 の敵対的検証（`AUDIT-LEDGER.md` の主張の種類 5 =「§X が Y を担保する」型）で、
**実測 5 件**が出た:

| 記述 | 実体 |
| :-- | :-- |
| 法への参照規則を **§15.6** に帰属（**提出文書 `submission-reference.md` と `AS-OF.md` の 2 面**）| §15.2。§15.6 は代理・組合の否認で、法への参照を 1 つも持たない |
| `"reformed to the minimum extent"` を **§15.2** に帰属 | §15.4 |
| §16.4 を `"continues to denote one fixed text"` と引用 | 本文は `"continue"` |
| §10.5・§11.3・§11.4 が **each** `"not a condition upon Your use of the Work"` と言う、と記述 | **この語句はライセンス全文に 0 回**。§11.3/§11.4 は `"not a condition upon You"`、§10.5 は `"Nothing in Section 16 is a condition upon Your use of the Work"` |
| §11.4 を `"and nothing else"` と引用 | `"It reaches nothing else"` |

**どれも E14 と同じ形である** —— 条項を指す矢印が、指した先に無いものを述べる。

## How

1. `LICENSES/ACD-1.0.txt` から条項本文を切り出す。**境界は行頭 2 空白**で決まる（本文は 7 空白
   の字下げなので、折り返し行が `8.3 rejects…` で始まっても条項見出しには見えない）。
   **初版はこれを取り違えて §8.3 の本文を §8.4 の途中から取り、正しい引用を「実在しない」と
   報告しかけた** —— 検出器の側が誤っていた例。
2. `LICENSES/*.md` を**段落**（空行で区切られた行の塊＝1 つの主張の文脈）に割り、その段落が
   挙げる条番号を集める。**行単位では折り返しで条番号が前の行に落ち、正しい記述を誤検出する**
   （実測 1 件）。
3. 段落中の 5 語以上の英語引用のうち、**ACD-1.0 のどの条項に在るかが一意に決まるものだけ**を
   母数にする（実測 112 件）。語句がライセンス本文でないもの —— 審査者の発言・我々自身の
   英文・1.1 草案の案文 —— は**そもそも母数に入らない**ので、帰属を推測する必要がない。
4. その条項が段落の挙げる条番号に覆われていなければ RED。

## Constraints

- **⚠ 射程を正直に書く**（#1172 の規律）。2026-09-14 の敵対的検証が出した実欠陥 5 件のうち、
  **本 Check が捕捉するのは 1 件だけ**である（`AS-OF.md` の §15.6）。残る 4 件は
  **掃引が見つけたのであって gate が見つけたのではない**:

  | 捕捉しない欠陥 | なぜ捕捉しないか |
  | :-- | :-- |
  | `submission-reference.md` の同じ §15.6 取り違え | **同じ段落が §15.2 も挙げる**ので covered と判定される |
  | `"reformed to the minimum extent"` の §15.2↔§15.4 | 同上（段落が §15.4 も挙げる）|
  | §16.4 を `"continues to denote"` と引用 | **本文に無い語**なので母数に入らない（owner が決まらない）|
  | `"not a condition upon Your use of the Work"` を 3 条が **each** 言うと記述 | 同上（**この語句は全文に 0 回**）|

- **より広い形は測ったうえで採らなかった**（#977 / #1212 と同じ「Check にしない判断も成果物」）:
  帰属の近さで当てる形は母数 26・誤検出 0 だが**実欠陥を 1 件も捕捉しない**。
  「同じ文に条項参照と英語引用があれば当てる」形は母数 107 中 **35 件が RED** になり、その大半は
  **審査者の発言・我々自身の英文・1.1 草案の案文**を引いた正当な記述だった。
  **正当な記述を RED にする gate は、正しい書き方を避けさせる分だけ害がある。**
- **外部 source（審査者の発言）の引用はこのモジュールの射程外。** そちらは
  `verify_dossier_quotations.py` が公開アーカイブを取得して照合するが、**外部フォーラムへ fetch
  するので CI には載せない**（脆い）。本モジュールが見るのは**リポジトリ内に凍結された本文**
  だけなので offline で決定的に検証できる。

## Change impact

- Check を足すときは docstring inventory の `  N.` と `# ── N.` セクションの**両方**を同じ
  commit で（Check 45 が bijection を強制）。`check-repository-consistency-map.md` と
  `total-check-runbook.md` §9 も同じ commit で（Check 105 / 70）。
- 本 file の行数を変えたら `docs/architecture/file-size-budget.md` §2 表も同じ commit で
  （Check 424）。

## Audience-specific notes

- **AI（実装者）**: 引用が RED になったら、**まず本文を読んでから直す**。条番号を直すのか、
  引用をやめて記述にするのかは意味の判断であり、機械には決められない。**言い換えを引用符で
  囲まない**のが最も安全な書き方。
- **監査人**: 本 Check は**ドシエ側**しか直さない。`ACD-1.0.txt` は凍結中（Check 453 が sha256 を
  pin）なので、本文の側を引用に合わせる修正は**できないし、してはならない**。
- **本 Check を「引用の忠実性は守られている」と読まないこと。** 守っているのは
  **証明できる取り違えだけ**で、それは実測した欠陥の 5 分の 1 である。
