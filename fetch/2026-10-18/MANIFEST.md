# fetch/2026-10-18 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-18T05:26:17Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-18T05:26:18Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-18T05:26:18Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 35049 | 189350a08cc07004 | 2026-10-18T05:26:19Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 188656 | 124f9b3ecb51fde9 | 2026-10-18T05:26:19Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 191498 | abd878da5c1951cc | 2026-10-18T05:26:20Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 211980 | 272c7d247ae6ea39 | 2026-10-18T05:26:21Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 250145 | d3267e4c00afce89 | 2026-10-18T05:26:21Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-18T05:26:22Z |
| events/osi-blog-state-of-the-source-ato-2026.html | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | 200 | 188691 | fd0b2f8e05023f8b | 2026-10-18T05:26:22Z |
| events/ato-2026-schedule.html | https://2026.allthingsopen.org/schedule | https://2026.allthingsopen.org/schedule | 200 | 165316 | f907880c4e11d361 | 2026-10-18T05:26:22Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 187343 | 125c981cba43d5b2 | 2026-10-18T05:26:25Z |

**取得者注記**: この日次は portfolio-01（Mac・2026-10-18 新規起動）が取得した。見出しの「portfolio-24」はスクリプトの固定文字列で、portfolio-24 は既に存在しない。前日（fetch/2026-10-17・08:52 UTC 取得）とのバイト比較: license-discuss 2026-October・9 月の 2 アーカイブ・api/licenses はバイト一致（新着 0 通・取得 05:26 UTC 時点）。license-review 2026-October は 404。HTML は script 等を含むため比較していない。
