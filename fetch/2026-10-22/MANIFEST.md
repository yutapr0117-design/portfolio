# fetch/2026-10-22 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-21T23:24:51Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-21T23:24:52Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-21T23:24:53Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 35049 | 189350a08cc07004 | 2026-10-21T23:24:53Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 196653 | ed6df2420eab5958 | 2026-10-21T23:24:54Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 199495 | cff344718192691c | 2026-10-21T23:24:56Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 219953 | e9b83f7a4c8ab82d | 2026-10-21T23:24:57Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 263681 | 21950eeb5cb61f7e | 2026-10-21T23:24:58Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-21T23:24:59Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 200893 | 82aa2b102be599a1 | 2026-10-21T23:25:00Z |

**前日（2026-10-21）とのバイト比較（2026-10-22 08:27 JST）:** list アーカイブ 3 件（review 9 月 / discuss 9 月・10 月）と API JSON は byte 一致。review 10 月は 404 のまま（10 月の投稿なし）。HTML 5 件の差はすべて WordPress の plugin 版数クエリと `EM` nonce で、本文の変化は無い。since 2026-10-21T00:13Z 以降の新着メッセージ 0。CoC modified_time 不変（2023-05-04 / 2023-11-02）・minutes 最新 2026-06-29・API 126 本・licenses ページの ModelGo / OpenMDW 言及 0。

## 追加取得（ad hoc・2026-10-22 08:3x JST・`adhoc_fetch.py`）

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] |
|---|---|---|---|---|---|
| events/ato-2026-session-licensing-101.html | (下記) | | 200 | 51874 | 9f09b0676a9cd134 |
| events/discuss-1441-modelgo-status.json | (下記) | | 200 | 15495 | b58bcf31e7af11b6 |
| events/discuss-1451-state-of-the-source.json | (下記) | | 200 | 12237 | 68f792d746ce6039 |
| events/discuss-1454-new-website.json | (下記) | | 200 | 11726 | cf1598ca29664c2e |
| events/discuss-latest.json | (下記) | | 200 | 41470 | e33db8fcdef1b076 |
| events/haxx-osi-approved-the-curl-license.html | (下記) | | 200 | 61631 | 919773d11293e9f8 |
| events/osi-approval.html | (下記) | | 200 | 205332 | 6341a7e5a1b1c304 |
| events/osi-blog-index.html | (下記) | | 200 | 215095 | 845c94c363a17c39 |
| events/osi-blog-new-website.html | (下記) | | 200 | 196472 | 40843b4fa7547f9e |
| events/osi-blog-open-weights-are-good.html | (下記) | | 200 | 199959 | 416a598412c30339 |
| events/osi-blog-opening-new-paths.html | (下記) | | 200 | 210671 | 612ad69cf3ba6f80 |
| events/osi-blog-state-of-the-source-ato-2026.html | (下記) | | 200 | 202207 | 9570f00b6725a9f0 |
| events/osi-common-reasons-rejection.html | (下記) | | 200 | 193843 | 3be7087b0e1022e3 |
| events/osi-license-w3c.html | (下記) | | 200 | 195573 | 0690d85ab5f70bc3 |
| events/osi-licenses-alphabetical.html | (下記) | | 200 | 198940 | 25db2687804c6490 |
| events/osi-osd.html | (下記) | | 200 | 195197 | 7ef4a835ea4f608a |
| events/osi-proliferation-report.html | (下記) | | 200 | 202705 | d6aa7d58e488474c |
| events/osi-review-process.html | (下記) | | 200 | 205332 | c49663e4bbe4d7f4 |

URL の対応: haxx-* = daniel.haxx.se/blog/2026/10/15/osi-approved-the-curl-license/ ／ discuss-<id>-*.json = discuss.opensource.org/t/<id>.json ／ discuss-latest.json = discuss.opensource.org/latest.json ／ osi-* = opensource.org の同名パス（approval は licenses/review-process へ、licenses/alphabetical は /license へ、license/w3c は license/w3c-20150513 へリダイレクト）／ ato-2026-session-licensing-101.html = 2026.allthingsopen.org/sessions/open-source-licensing-101。

**観測メモ（分析は main 側）:** (1) OSI サイトは 2026-10-19 に新構成（ブログ「New website reflects OSI's evolving mission」）。ドシエが依拠する 7 URL はすべて 200 で解決し、review-process（modified 2024-03-13）と rejection-reasons（2024-03-12）は更新されていない。(2) OSI Discuss フォーラム t/1441（2026-07-28・Moming Duan 氏）: ModelGo の審査状況を問う投稿で、1/27・5/26・7/26 の追送に返信が無く「moderation 保留か spam 扱いか」を尋ねている。取得時点で返信 0。(3) curl ライセンスの steward（Daniel Stenberg 氏）のブログ 2026-10-15: 2026-04-17 の承認に「数か月後まで気付かなかった」。提出者は第三者（Christoph Röth 氏）。(4) ATO・State of the Source・Opening Convening の録画/スライド/報告ブログはまだ無い。

**偽の手掛かり（2026-10-22 08:4x JST）:** 検索で出た `digitalcommons.kennesaw.edu/ato/2026ato/presentations/` は Kennesaw State University の **All Things Open（開かれた教育のカンファレンス・2026-04-06〜07・オンライン）**で、Raleigh の All Things Open とは別物。ライセンス関連は「Creative Commons Licenses 101」だけで ACD への当たりなし。バイト列は events/kennesaw-ato-202{5,6}-presentations.html。
