---
file: LICENSES/rounds/2026-11-16-us-asset-marketing-v-gagnon-consideration-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2026-11-16-us-asset-marketing-v-gagnon-consideration-snapshot.txt

## What

米国第 9 巡回区控訴裁判所の Asset Marketing Systems v. Gagnon（2008）の、許諾が撤回できない理由を「対価が払われたから」とし、「対価に支えられた非独占の許諾は契約である」「対価を伴う黙示の許諾が任意に撤回できるなら契約は見せかけになる」と述べた段。法律事務所が置いた判決の PDF から、この session で圧縮を解いて取り出した。バイト単位の写しではなく、裁判所の頁からでもない。

## Why

1.4 草案は許諾を撤回不能と呼び（§2.2・§3.1・§4.1・§8.1）、誰にも見返りを求めない（§4.3・§10.1）。THIRD §18.3 は、米英では対価の無い許諾が撤回可能と読まれうると記録した。この判決は、撤回不能の理由を対価に置く —— 反対から読めば、対価の無い ACD の許諾の撤回不能は、許諾そのものからは立たない。不利な側の一次法源。オーナーの依頼（2026-11-16）の portfolio-2f の受け持ち（米国と EU）。

## How

WebFetch が PDF を読めず保存したので、Python の標準ライブラリ（zlib）で本文の流れを解いて文字を取り出した。改行による語の分割（"consid-eration"）はそのまま残した。justia の写しは 403。

## Constraints

判決は対価が払われた場合の判断で、対価の無い許諾が撤回できると判示してはいない（反対の読みは我々の推論）。ACD の §2.5（信頼と禁反言）と §5 の約束が、対価の無い場合の別の足場になるかは、この判決からは決まらない。取り出しは PDF の本文の流れからで、組版の都合で語順が乱れていないかは裁判所の写しで確かめる。

## Change impact

この写しを引く THIRD §18 の §2.2・§4.1・§8.1・§8.2 の当て、法律家への問い 1・2 を直すときは、ここの番号の片を裁判所の写しで確かめる。

## Audience-specific notes

- **監査人**: Lulirama（第 5 巡回区 1997）と Nimmer の引用は判決の中の引用で、それぞれの原典は取っていない。
