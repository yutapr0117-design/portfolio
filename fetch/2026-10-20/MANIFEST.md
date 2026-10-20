# fetch/2026-10-20 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-20T00:13:10Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-20T00:13:12Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-20T00:13:12Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 35049 | 189350a08cc07004 | 2026-10-20T00:13:13Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 196518 | d024f1819a86d3cb | 2026-10-20T00:13:14Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 199551 | 35bcf3feb113285f | 2026-10-20T00:13:14Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 219982 | 8e128e7caca35960 | 2026-10-20T00:13:14Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 263629 | af9b6a7f732e5f3c | 2026-10-20T00:13:14Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-20T00:13:14Z |
| events/osi-blog-state-of-the-source-ato-2026.html | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | 200 | 202097 | 5946226035552434 | 2026-10-20T00:13:14Z |
| events/ato-2026-schedule.html | https://2026.allthingsopen.org/schedule | https://2026.allthingsopen.org/schedule | 200 | 165568 | e8e6cc8e23656780 | 2026-10-20T00:13:14Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 200784 | 48df82c7f5cf411b | 2026-10-20T00:13:17Z |

## 前日（2026-10-19）とのバイト比較

- 一致: license-review 9 月 / license-discuss 9・10 月 / api/licenses / ATO schedule は可視テキスト差 0（92 bytes の差はマークアップのみ）。
- 差: opensource.org の 6 ページ（licenses / minutes / CoC 2 本 / ATO ブログ / AI salon）が各 +13.4KB。可視テキストの差は 6 ページで同一の 74 行・削除 0 行で、ナビメニューに "Policy & Standards" 系の項目が足された分（10-19 告知のサイト刷新の続き）。本文の変化は無い。
- 新着メッセージ 0（10-19T01:11Z 以降）。license-review 10 月は引き続き 404（当月投稿なし）。CoC の modified_time は不変（2023-05-04 / 2023-11-02）。minutes 最新 2026-06-29、api 126 件・最新承認 20260629 で不変。
- サイト刷新による URL 移動は無し: 日次の URL はすべて 200、最終 URL も前日と同じ（code-of-conduct → mailing-lists CoC への転送は従来どおり）。
