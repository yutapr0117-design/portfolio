# fetch/2026-10-14 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-14T14:14:39Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-14T14:14:41Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-14T14:14:41Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 8414 | 2db43ab6533dcf78 | 2026-10-14T14:14:42Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 188705 | 477e262839fb1194 | 2026-10-14T14:14:42Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 191197 | d02727fc6b7ef07c | 2026-10-14T14:14:44Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 212047 | e8c29d135bea484b | 2026-10-14T14:14:44Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 255713 | bcf96ecc3d425e19 | 2026-10-14T14:14:45Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-14T14:14:46Z |
| events/osi-blog-state-of-the-source-ato-2026.html | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | 200 | 194122 | f1da73c4a55758f3 | 2026-10-14T14:14:46Z |
| events/ato-2026-schedule.html | https://2026.allthingsopen.org/schedule | https://2026.allthingsopen.org/schedule | 200 | 163574 | 9d0615dfa3661315 | 2026-10-14T14:14:47Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 192907 | 810cec902b222850 | 2026-10-14T14:14:47Z |

## 受け渡しの注記（取得側・分析ではない）

- **今日の日次は cron が発火せず、14:14 UTC に手動で取得した**（予定は 10-13 23:13 UTC）。前回取得 10-12 23:43 UTC から約 38.5 時間空いている。
- `license-discuss_2026-October.txt` が**初めて 200 になった**（10-12 23:43 UTC までは 404）。中身は **2 通**で、ヘッダの値は次のとおり:
  - Date `Sun, 11 Oct 2026 17:21:06 +0700` / Subject *Pre-submission discussion: Zero-Clause BSD with Patent Grant (0BSD-P)* —— **Date が前回取得時刻より前**なので、「前回以降の Date」で絞ると漏れる（取得スクリプトの新着表示もこの 1 通を出さなかった）。
  - Date `Wed, 14 Oct 2026 15:23:07 +0200` / Subject *Call for feedback on FLA-2.1_RC*（2026-09-17 の同題への返信）。
- `license-review_2026-October.txt` は依然 404。
- `events/ato-2026-schedule.html` は 1 分前の別取得（scratchpad）と sha256 が異なる（a60a71af… / 9d0615df…・同じ 163,574 bytes）。
