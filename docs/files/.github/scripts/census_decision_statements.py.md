---
file: .github/scripts/census_decision_statements.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-07
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

## Constraints

正規表現と手で選んだ差出人の一覧なので下限である。**対照が 1 つ外れている**: 入口が引く *"That is not a blocker."* はこの道具に掛からない。規則の語を含まない文は拾えない。`threads` の出力は未読の候補で、未読の証明ではない。

## Change impact

`LICENSES/ACD-1.0.reviewer-positions.md` §1.140 と `LICENSES/AS-OF.md` の数はこの道具の出力である。差出人や正規表現を変えると数が動く。

## Audience-specific notes

- AI: 読むのは出力であって、出力の件数は発見の件数ではない。文は原文の文脈で読む
