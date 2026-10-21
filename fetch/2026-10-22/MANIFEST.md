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
