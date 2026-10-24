# fetch/2026-10-24 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-24T06:41:11Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-24T06:41:12Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-24T06:41:12Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 35049 | 189350a08cc07004 | 2026-10-24T06:41:13Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 197158 | dd6072689ac5b4e2 | 2026-10-24T06:41:13Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 199923 | 202739514b210daa | 2026-10-24T06:41:16Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 220381 | 543adb9183cce91a | 2026-10-24T06:41:17Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 264087 | ded2019b5fe86e25 | 2026-10-24T06:41:18Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-24T06:41:18Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 201279 | 928480a5aa5e59e1 | 2026-10-24T06:41:19Z |

**前日（2026-10-23）とのバイト比較:** license-review 9 月・license-discuss 9 月/10 月・api_licenses.json は同一。code-of-conduct / codeofconduct / minutes / licenses / events/osi-ai-salon の HTML 5 件はバイト差分ありだが、script/style を除いた本文テキストの差はサイト共通ナビへの「Bylaws」リンク 2 箇所の追加のみ（CoC の modified_time は 2023 のまま・minutes 最新 2026-06-29・API 126 件で不変）。license-review 10 月は引き続き 404。前回（2026-10-23T03:05:49Z）以降の新着メッセージ 0 件。
