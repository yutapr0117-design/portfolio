---
file: LICENSES/ACD-1.0.submission-reference.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-09-09
canonical-ref: LICENSES/ACD-1.0.submission.md (送る文面は §B.0) / LICENSES/ACD-1.0.against.md / LICENSES/AS-OF.md
---

# LICENSES/ACD-1.0.submission-reference.md

## What

**提出文の背後にある参考資料。§1〜§5。** なぜ新しいライセンスが要るか（§1・§1a〜§1d）／
既存の承認済みライセンスとの差（§2）／OSD 逐条（§3）と**反対側から書いた同じ逐条**（§3b）と
OSI 自身の却下理由リスト（§3c）／意図的な不在（§4）／どのトラックか（§4a）／
**提出者専用ではないことの実証**（§4b）／**弁護士が読んでいないことに対置する機械的検証**（§4c）／
開示（§5）。

**貼らない。** 送るのは `ACD-1.0.submission.md` §B.0 だけである。

## Why

**読み手が違う。** `submission.md` は「何を送るか」で読み手は**送る人**、本書は
「送ったあとに審査者が具体的な質問をしたときに指す先」で読み手は**審査者**である。
**同居している限り「§1〜§5 を貼るな」という警告が要り、実際 §B.0 は 3 度書いていた** ——
分割でその危険は構造的に消える。

規模の理由もある: 分割前の `submission.md` は 976 行で advisory (950) を越えていた。
**BLOCKING (1000) に当たってからでは遅い。**

## How

- 2026-09-09 に `ACD-1.0.submission.md` から切り出した
- **節番号は変えていない**ので、既存の `submission.md §4c` のような参照は本書の同じ節へ解決する
  （`comparison.md` → `review-precedents.md` と同じ手）
- `checks_license_dossier.py` の Check 460 は §4c の自己申告 3 種（不利な事実の件数 /
  clause pointer / 定義語の最小使用回数）を読むので、**読む先の path も同じ commit で変えた** ——
  message だけ直して path を残すと、Check は存在しない節を探して黙る

## Constraints

- **本文（`ACD-1.0.txt`）は凍結中**。本書は本文について述べるが、本文を動かす根拠にはならない
- 自己申告の数は Check 460 が実測と照合する（申告を足したら実測も同じ commit で）
- Check 108 が `docs/files/` mirror との 1 対 1 を、Check 459 が索引の網羅を強制する

## Change impact

節番号を変えると、他 file の `§4c` 等の参照が**静かに**壊れる（Check 441b は解決を見るが、
**節が移動して別の内容になる**形は見ない）。**節は追加してよいが、既存の番号は動かさない。**

## Audience-specific notes

- **審査者**: 具体的な質問への答えはここに在る。§3b は**我々自身が書いた反対論**である
- **後任 AI**: 次に advisory を越えたら §3 系を切り出す（disposition は
  `file-size-budget.md` に事前に書いてある）。**事前計画から外れるときは、外れた理由をそこへ書く**
