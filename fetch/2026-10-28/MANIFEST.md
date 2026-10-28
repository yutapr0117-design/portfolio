
- 03:46 JST watch（events-watch-034611）: 21:46 と比べ (a)〜(d) 変化なし（discuss の posts_count 不変・t/1441 動きなし）。
# fetch/2026-10-28 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。**フォルダ名の日付は JST、表の取得時刻は UTC（ISO 8601 の Z）。**

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-28T00:13:14Z |
| license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | 200 | 18343 | f898a42f05b02de4 | 2026-10-28T00:13:15Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-28T00:13:16Z |
| license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | 200 | 38290 | 9ea5296efc131f2e | 2026-10-28T00:13:17Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 195938 | 6f22510ad05cb826 | 2026-10-28T00:13:18Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 198832 | e4fc4a7a24538aef | 2026-10-28T00:13:18Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 193577 | ddc60422c6a46c94 | 2026-10-28T00:13:18Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 262872 | 560041086fddcb30 | 2026-10-28T00:13:20Z |
| opensource.org_api_licenses.json | https://opensource.org/api/licenses | https://opensource.org/api/licenses | 200 | 84269 | a1d1471f11d10523 | 2026-10-28T00:13:20Z |
| events/osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 200158 | 1f81bf95b07d9fd8 | 2026-10-28T00:13:20Z |
| events/otr-symposium-official.html | https://symposium.opentechresearch.org/ | https://symposium.opentechresearch.org/ | 200 | 513899 | 2f3dd8a20ada0a40 | 2026-10-28T00:13:20Z |
| events/code-compliance-luma.html | https://luma.com/orc1026 | https://luma.com/orc1026 | 200 | 101897 | edf6004d5d1fde96 | 2026-10-28T00:13:23Z |
| events/mozfest.html | https://www.mozillafoundation.org/en/festival/ | https://www.mozillafoundation.org/en/festival/ | 200 | 76452 | 7d4aa03c2f64117c | 2026-10-28T00:13:23Z |

## 日次取得 2026-10-28T00:13Z（portfolio-01・since 2026-10-27T03:04:37Z・args salon otr cc mozfest）

- 新着メッセージ: **0 通**（license-review / license-discuss の 9 月・10 月とも前日と byte 一致）。
- api_licenses.json: 前日と byte 一致（126 件・最新承認 20260417 / 20260629）。licenses ページは本文テキスト差分なし（ModelGo 0 / OpenMDW 0）。
- **minutes ページ（220,226 → 193,577 bytes）**: 「Last modified on October 27, 2026」。**ページ分割になっただけ**で、1 ページ目は直近 12 回（2025-06-20〜2026-06-29）と「Next Page」。2〜4 ページ目に 2025-05-16〜2022-07-15 が実在することを `?query-0-page=2..4` で確認した（00:2xZ）。旧 1 ページ目にあったリンク無しの 2005〜2020 の日付一覧は 1 ページ目から消えている（後続ページにあるかは未確認）。**新しい議事録は無い**: 最新は 2026-06-29 のままで、7〜9 月の理事会議事録はまだ掲載されていない。
- CoC 2 ページ / salon / otr / mozfest: テキスト差分は UI 文言のみ（Magazine・Notify 等）。code-compliance (luma): 「Past Event」表記が付いた（会期終了）。録画・スライドは無い。
- ACD への当たり: なし（main には書かない）。
- 19:12 JST watch（events-watch-191216）: 03:46 と比べ (a)〜(d) 変化なし（blog の差分は Popular posts サイドバーの入れ替えのみ・luma の Past Event は日次で既出・discuss 不変・t/1441 動きなし）。
- 21:46 JST watch（events-watch-214611）: 19:12 と比べ (a)〜(d) 変化なし（全ページのテキスト差分ゼロ・discuss 不変・t/1441 動きなし）。
