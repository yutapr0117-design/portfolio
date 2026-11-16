---
file: LICENSES/rounds/2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt

## What

ベルリンの弁護士 Till Kreutzer 氏による、CC0 1.0 のドイツ著作権法上の有効性の分析（2011 年頃・Research Data Alliance が公開）から、7 つの段（著作権の放棄は無効・fallback の許諾は有効で撤回不能かつ無条件の許諾を与えられる・fallback が無くても公有の宣言は無条件の公の許諾と読み替えられるのが通説・不行使の約束は有効で拘束力ある pactum de non petendo・32c 条 3 項の Linux 条項・人格権の包括的な放棄は無効）を取り出した。バイト単位の写しではない。

## Why

法律家への問い 1（§3 の放棄と §4 の許諾は並んで立つか）に、構造が最も近い CC0 の、同じ問いについての弁護士の公開の分析。McCoy Smith 氏が 2020-03-30 に `license-review`（Unlicense のレガシー承認）で引いた。オーナーの依頼（2026-11-16）の portfolio-2f の受け持ち（承認済み・同型の文書の公開の法的分析を条ごとに当てる）。

## How

WebFetch が PDF を読めず保存したので、Python の標準ライブラリ（zlib）で本文の流れを解いて文字を取り出した。フォントの符号化で化けた 3 種（ダッシュ・引用符・§）を戻し、それ以外は変えていない。

## Constraints

判決でも条文でもなく、1 人の弁護士の意見（"according to my opinion"）。CC0 についての分析で、ACD を扱っていない。ACD の §4.4 は fallback ではなく独立の許諾なので、[2] の「fallback は有効」は ACD の §4 にそのまま当たるとは言えない —— ただし [3] の通説（公有の宣言そのものが公の許諾と読み替えられる）は、§4 が独立であることにも、§3 だけでも同じ帰結に向く。[7] の文は最初の版で切れていたが、同じ取り出しから続き（許諾そのものは無効にならず、作者は例えば作品の歪曲を禁じうる）を補った。

## Change impact

この写しを引く問い 1・5、`jurisdictions.md` のドイツの節、THIRD §18.1 の §3・§4 と §18.2 の §5 の行を直すときは、元の PDF で確かめる。

## Audience-specific notes

- **監査人**: 2011 年頃の分析で、その後のドイツの判例と法改正（2021 年の著作権法改正など）は反映していない。
