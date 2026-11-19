---
file: .github/scripts/measure_law_coverage.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-19
canonical-ref: LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md §18 (頼っている法の命題) / .github/scripts/add_law_snapshot.py (写しの置き方)
---

# .github/scripts/measure_law_coverage.py

## What

1.4 草案の条ごとに、§18 の「頼っている法の命題」の行と、rounds/ の法令・判例の写し（`*-snapshot.txt`）を結ぶ対応表を出す。要約は
§18 の行を持つ条・写しが当たる条・§18 に残る「未取得」の句・どの条にも当たっていない法令の写しを数える。`--table` で条ごとの表。

## Why

2026-11-20 の 5 人の分担（関連法令の一次資料を読む）の 9b の (2)。読んだ写しがどの条に当たったか、どの行がまだ法源を取っていない
かを条ごとに数で言えないと、分担の残りが見えない。最初の測定で、取得済みの写し（消費者契約法 8 条）を「未取得」と書き残した行が見つかった。

## How

写しが当たる条は、ヘッダの `Applied to: … Sections …`（add_law_snapshot.py の形）か、§18 の行と jurisdictions*.md の段がその写しの名を
引く所の §x.y から取る。法令・判例の写しは Source の URL の出所（gesetze-im-internet・legislation.gov.uk・e-Gov・Legifrance・Cornell LII・
EUR-Lex・WIPO・判例の公開元）で見分け、OSI の頁などは「当たっていない写し」に数えない。

## Constraints

「未取得」の句は、取った写しで行を直したかを語で見るだけで、行が名指す法令と写しの中身の一致は見ない。読み（その法源が命題を支えるか）は人が書く。

## Change impact

§18 の行の形（表の行と箇条の行）や写しのヘッダの形を変えたら、読み取りの正規表現を直す。

## Audience-specific notes

- **監査人**: 対応表の各写しはヘッダの URL から原文に当てて確かめられる。
