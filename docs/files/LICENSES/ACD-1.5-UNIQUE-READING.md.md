---
file: LICENSES/ACD-1.5-UNIQUE-READING.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.5-DRAFT.txt / LICENSES/ACD-1.4-UNIQUE-READING.md
---

# LICENSES/ACD-1.5-UNIQUE-READING.md

## What

1.5 草案（縮約・50 条）の条ごとに、その語が許す最も強い別の読みを 1 つ以上書き、閉じている条・直す試作・
法律家への問いのどれかへ送る台帳。

## Why

1.5 は 1.4 を 1 日で書き直した本文なので、1.4 で閉じた読みの回帰だけでなく、短くした語が新しく開けた読みを
条の側から探す必要がある（議題 16 の条件 2）。出す版を 1.5 に替える議題は、この台帳が埋まってから出す。

## How

`measure_legal_uncertainty.py` の section19() が最新の版の台帳を読む（Check 468ac が行の形、468ad が
CHANGELIST との対応を照らす）。5 人が小節を分けて書く。

## Constraints

- 1.4 の台帳は 1.4 の条の記録として動かさない。条の対応は `CLAUSE-MAP-1.4-1.5.tsv`。
- 1.4 の条を引くときは版を名乗る。

## Change impact

条の語を動かしたら、その条の行を判定した人が当て直す（議題 16 の条件 4）。

## Audience-specific notes

- **法律家**: 「法の側」の行は `QUESTIONS-FOR-COUNSEL.md` の問いを名指す。
- **監査人**: 一意の判定は我々の読みで、法律家の判断ではない。
