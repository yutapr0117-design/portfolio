---
file: .github/scripts/census_decision_statements.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-11
canonical-ref: LICENSES/ACD-1.0.reviewer-positions.md (§1.140 が rules の出力を読んだ記録) / LICENSES/AUDIT-LEDGER.md
---

# .github/scripts/census_decision_statements.py

## What

OSI の 2 つのリストのアーカイブ全数から、決める側の発言だけを見る道具である。`rules` は承認や適合について規則の形をした文を抜き出し、`threads` はドシエの分析文書に 8 語連鎖がほとんど現れないスレッドを並べる。

実測（2026-11-07・全 508 か月）: 28,901 通、規則の形の文 1,278、うち受領者の条件についての文 181、残り 1,097。スレッドは 1,056 本のうち 771 本が未読の候補である。

## Why

規則の集計が 33 か月分しかなく、論点ごとに有利な 1 文を見つけると探すのをやめていた。全数で取ると、見つけた文を疑える。

## How

`DOSSIER_ARCHIVE_CACHE` に月次の写しを置いて手で走らせる。CI には入れない。

- **`first` は全体で最も早い通の日付（2026-11-11）**: 月の file は list ごとに時系列で読む（license-discuss の全期間のあとに license-review）ので、先に読んだ通を first にすると、2 つの list にまたがるスレッドで後の list の早い通（提出・"[PROPOSAL]" の起こし）を取り逃した（候補 778 本のうち 46 本・1 日以上ずれたのは 15 本で、うち 12 本は 2 つの list にまたがる）。Date 欄をタイムゾーンつきの時刻にして最も早いものを取る。`--pin` は一覧（THREAD-CANDIDATES.txt）の既存の行の日付もこの first に合わせ、出力に「一覧の日付が最初の通の日付と違う N 行」を出す。**限界**: スレッドは件名だけでまとめるので、年をまたいで同じ件名の別の会話は 1 本になる（"NOSA 2.0?" は 2016 と 2017 の会話がまとまり、first は 2016 になる）

## Constraints

正規表現と手で選んだ差出人の一覧なので下限である。**対照が 1 つ外れている**: 入口が引く *"That is not a blocker."* はこの道具に掛からない。規則の語を含まない文は拾えない。`threads` の出力は未読の候補で、未読の証明ではない。`threads` の母数は「いまの候補 ∪ `LICENSES/THREAD-CANDIDATES.txt` ∪ READ-THREADS」で、一度候補になったスレッドは外さない（2026-11-11。ドシエの語が増えただけで未読が減っていた）。`--pin` で新しい候補を一覧に足し、「いまの語では候補でないが一覧に在る（N 件・うち未読 M 件）」を出す。`threads` は `LICENSES/READ-THREADS.txt` の一覧だけを「読んだ」に数え（2026-11-09 に portfolio-00 と決めた。rounds/ の件名を数えると、別スレッドの通を 1 通だけ置いたときにそのスレッドまで読了になる。rounds にだけ在る候補は `<out>.rounds-only.json` と「rounds に在るが READ-THREADS に無い（候補内 N 件）」の行で名指す）、AS-OF の「未読スレッドの残り」と同じ形の 1 行（候補 N 本のうち M 本を読んだ。K 本は読んでいない）を出す（2026-11-09）。READ-THREADS の件名は候補に残す: 読むとドシエに語が足されて候補から外れ、母数が読むほど縮むため。

## Change impact

`LICENSES/ACD-1.0.reviewer-positions.md` §1.140 と `LICENSES/AS-OF.md` の数はこの道具の出力である。差出人や正規表現を変えると数が動く。

## Audience-specific notes

- AI: 読むのは出力であって、出力の件数は発見の件数ではない。文は原文の文脈で読む
