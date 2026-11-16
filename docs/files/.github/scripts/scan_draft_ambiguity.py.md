---
file: .github/scripts/scan_draft_ambiguity.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt / .github/scripts/scan_draft_terms.py
---

# .github/scripts/scan_draft_ambiguity.py

## What

草案の文のうち、法的な読みが割れうる型を 11 の型で洗い出す道具（読む候補を出す・止めない）。型: (a) 定義語の小文字の使用、(b) 定義の無い大文字の語、(c) 使われない定義、(d) §15.5 が覆う語の重ね書き（person or entity）、(e) 事実の評価に委ねる基準の語、(f) shall / must / will、(g) 古い指示語、(h) 小項の中の "this Section"、(i) and/or、(j) 優先の連鎖と循環、(k) 免責の条が同じ文書の約束を呑むか（1c の依頼・問い 9 (a) の型）。

## Why

オーナーの依頼（2026-11-16）「ACD-1.4-DRAFT.txt の法的解釈の不確実性を『５人』で減らし続けてください」。`scan_draft_terms.py` は条どうしの語の揺れ、`--compare` は試作の差分を見る。変えていない文に元から在る「読みが割れる型」を全体で数える道具が無かった。

## How

`python3 .github/scripts/scan_draft_ambiguity.py [本文]`。2026-11-16 の草案で: (a) 4・(d) 8・(e) 7・(f) 3・(h) 5・(j) 1・(k) 1（§14.1 の "ARISING OUT OF THIS DEDICATION" が §5・§8.6・§12 などの約束 13 条を外していない）、(b)(c)(g)(i) は 0。

## Constraints

どれも候補で、欠陥の証拠ではない。(k) は責任を外す条だけを数える（保証と依拠の否認は約束の違反の責任を外さないので、初版の 26 件の雑音を除いた）。

## Change impact

候補は 1c（試作）、30（反例）、50（法律家への問い）、2f（先例）へ回す。

## Audience-specific notes

- **AI / 後任**: 型を足すときは docstring の一覧と `names` の辞書を同じ commit で直す。
