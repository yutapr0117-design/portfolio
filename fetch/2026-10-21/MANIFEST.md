# fetch/2026-10-21 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-21T00:13:09Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-21T00:13:10Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-21T00:13:10Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 35049 | 189350a08cc07004 | 2026-10-21T00:13:11Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 196752 | f69ca25198db1f45 | 2026-10-21T00:13:11Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 199594 | c3a4e2e65d01983a | 2026-10-21T00:13:12Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 219936 | b907a6a08536f658 | 2026-10-21T00:13:12Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 263659 | 8b8096b5410f4a8e | 2026-10-21T00:13:12Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-21T00:13:12Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 200964 | c3a34ce6d62cc3e2 | 2026-10-21T00:13:12Z |

**前日（fetch/2026-10-20）とのバイト比較**: 一致 = license-review/discuss 9 月・license-discuss 10 月・api/licenses.json。不一致 = CoC 2 URL・minutes・licenses・ai-salon。ただし script/style を除いた可視テキストの差分は 5 件とも 0 語（nonce 等の埋め込み差のみ）。license-review 10 月は引き続き 404（当月投稿なし）。新着メッセージ 0（since 2026-10-20T00:13Z）。CoC modified_time 不変・minutes 最新 2026-06-29・API 126 件で最新承認 20260629 は不変。10/21 から ato を外した（会期 10/19–20 終了）。
