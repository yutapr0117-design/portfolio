# fetch/2026-10-27 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-27T03:04:37Z |
| license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | 200 | 18343 | f898a42f05b02de4 | 2026-10-27T03:04:39Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-27T03:04:40Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 38290 | 9ea5296efc131f2e | 2026-10-27T03:04:40Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 197026 | 12e451abb642ce57 | 2026-10-27T03:04:41Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 199868 | f1defc8cd62b9ab0 | 2026-10-27T03:04:44Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 220226 | 2a0983185b37a612 | 2026-10-27T03:04:44Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 263956 | cd7ef16d78551c65 | 2026-10-27T03:04:45Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-27T03:04:45Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 201175 | ffab38479a2e5870 | 2026-10-27T03:04:46Z |
| events/otr-symposium-official.html | https://symposium.opentechresearch.org/ | https://symposium.opentechresearch.org/ | 200 | 513887 | bbecb191dfc07686 | 2026-10-27T03:04:46Z |
| events/code-compliance-luma.html | https://luma.com/orc1026 | https://luma.com/orc1026 | 200 | 99659 | 8a19efcfc491307a | 2026-10-27T03:04:49Z |
| events/mozfest.html | https://www.mozillafoundation.org/en/festival/ | https://www.mozillafoundation.org/en/festival/ | 200 | 76370 | 5cdd33b8ae27b7c5 | 2026-10-27T03:04:49Z |

**前回取得（2026-10-25 04:52Z）との比較**: license-review 2026-October が**初めて 200**（18,343 bytes・前回まで 404）—— 新着 1 通: Moming Duan「ModelGo Attribution License, Version 2.0 FINAL CALL FOR COMMENTS」（2026-10-25 13:00Z）。license-discuss 2026-October は 35,049 → 38,290 bytes（増分あり・本文は main 側で読む）。9 月の 2 リスト・API は同一。CoC の modified_time は 2023 のまま・minutes 最新 2026-06-29・API 126 件。10-26 の日次は cron の 7 日失効で実行されなかった（2026-10-27 に再設定）。

- 2026-10-27 15:46 JST 監視: 12:00 の監視と比べ (a)〜(d) とも変化なし（YouTube 両チャンネル・ブログ記事・Discuss posts_count 同一。ブログの差は Popular posts 欄の入れ替わりのみ）。
