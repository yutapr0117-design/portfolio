# fetch/2026-10-23 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-23T03:05:49Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-23T03:05:50Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-23T03:05:51Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 35049 | 189350a08cc07004 | 2026-10-23T03:05:51Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 196653 | 10bf1ea7c1ab2b42 | 2026-10-23T03:05:52Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 199574 | 2e9e43ce9a36efa7 | 2026-10-23T03:05:52Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 220079 | e442aab093e8d58b | 2026-10-23T03:05:52Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 263655 | b20d11aedb83d557 | 2026-10-23T03:05:52Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-23T03:05:53Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 200806 | 8d617ceab4a73863 | 2026-10-23T03:05:53Z |

**前日（2026-10-22）とのバイト比較:** license-review 9 月 / license-discuss 9 月・10 月 / api_licenses.json は byte 一致。code-of-conduct ×2・minutes・licenses・osi-ai-salon は byte が違うが、script/style を除いた本文テキストの差分は 0 行（埋め込み JS の nonce 等のみ）。license-review 10 月は引き続き 404（当月の投稿なし）。新着メッセージ 0 件（since 2026-10-21T23:24:51Z）。CoC の modified_time・minutes 最新（2026-06-29）・API 件数 126 も前日と同じ。ato は 10/21 以降の規定どおり外した（otr/cc/mozfest は 10/26 から）。
