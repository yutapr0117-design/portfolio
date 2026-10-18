# fetch/2026-10-18/events-watch-1430 — portfolio-01（Mac）イベント監視取得

バイト列は取得時のまま。**フォルダ名は JST、取得時刻は UTC。** 下の「手掛かり」は正規表現による抽出で、本文を読んだ判定ではない。

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| ato-sots.html | https://2026.allthingsopen.org/the-state-of-the-source | https://2026.allthingsopen.org/the-state-of-the-source | 200 | 89283 | ddcb3d521ac65745 | 2026-10-18T05:30:53Z |
| osi-events.html | https://opensource.org/events | https://opensource.org/events | 200 | 187992 | c58ad1fdc41c4b1a | 2026-10-18T05:30:55Z |
| osi-blog.html | https://opensource.org/blog | https://opensource.org/blog | 200 | 201936 | 212d1354058f9351 | 2026-10-18T05:30:55Z |
| osi-blog-events.html | https://opensource.org/blog/category/events | https://opensource.org/blog/category/events | 200 | 205823 | 70c74b422d28510c | 2026-10-18T05:30:55Z |
| osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 187306 | 7e1c9a687387c64b | 2026-10-18T05:30:55Z |
| ato-the-state-of-the-open-source-initiative.html | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | 200 | 51930 | 08b51de34a040edc | 2026-10-18T05:30:55Z |
| ato-open-source-licensing-101.html | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | 200 | 51874 | 8ee639a2287bdf90 | 2026-10-18T05:30:56Z |
| ato-sharing-is-caring-open-data-for-open-source-compliance.html | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | 200 | 53930 | 9cc6619134bc3b64 | 2026-10-18T05:30:57Z |
| ato-is-open-source-dying-short-film-and-open-discussion.html | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | 200 | 52957 | 262ae0f492754da0 | 2026-10-18T05:30:57Z |
| ato-the-latest-on-public-policy-and-open-source.html | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | 200 | 51966 | 8518e1ad2b69dafe | 2026-10-18T05:30:58Z |
| ato-the-state-of-open-source-ai-in-2026.html | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | 200 | 52039 | 100e5b4f44ff7f01 | 2026-10-18T05:30:59Z |
| ato-the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy.html | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | 200 | 53418 | d84f5ff407b27580 | 2026-10-18T05:31:00Z |
| ato-what-makes-open-source-work-licensing-and-beyond.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | 200 | 52307 | d4ca8a90046e2213 | 2026-10-18T05:31:00Z |
| ato-what-makes-open-source-work-licensing-and-beyond-2.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | 200 | 52359 | 5b1f4c4772bbb158 | 2026-10-18T05:31:01Z |
| ato-welcome-social-panel-discussion.html | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | 200 | 56108 | fe88e2fb43b4cb96 | 2026-10-18T05:31:02Z |

## 観測メモ（portfolio-01・事実の指し先のみ）
1. ATO の全ページに出る youtube.com/allthingsopen と slideshare.net/AllThingsOpen はサイト共通のフッタで、セッション個別の録画・スライドではない（10 セッション全ページに同一）。
2. OSI ブログ索引の記事のうち、この取得時点で受け渡しブランチに一度も取られていなかった 6 本を ../osi-posts/ に取得した。
