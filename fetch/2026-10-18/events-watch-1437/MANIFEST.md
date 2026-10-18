# fetch/2026-10-18/events-watch-1437 — portfolio-01（Mac）イベント監視取得

バイト列は取得時のまま。**フォルダ名は JST、取得時刻は UTC。** 下の「手掛かり」は正規表現による抽出で、本文を読んだ判定ではない。

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| ato-sots.html | https://2026.allthingsopen.org/the-state-of-the-source | https://2026.allthingsopen.org/the-state-of-the-source | 200 | 89283 | db3a8dd7549d00b0 | 2026-10-18T05:37:33Z |
| osi-events.html | https://opensource.org/events | https://opensource.org/events | 200 | 182435 | 04426f087b1f7d21 | 2026-10-18T05:37:33Z |
| osi-blog.html | https://opensource.org/blog | https://opensource.org/blog | 200 | 202158 | 6657f9f3c8c03aa6 | 2026-10-18T05:37:33Z |
| osi-blog-events.html | https://opensource.org/blog/category/events | https://opensource.org/blog/category/events | 200 | 200306 | c5b3ff8979034ab8 | 2026-10-18T05:37:33Z |
| osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 187395 | 0746cb3ea65c3129 | 2026-10-18T05:37:33Z |
| yt-allthingsopen-videos-titles.txt | https://www.youtube.com/@allthingsopen/videos?hl=en&gl=US | https://www.youtube.com/@allthingsopen/videos?hl=en&gl=US | 200 | 1784 | 0e31d86273743e98 | 2026-10-18T05:37:33Z |
| yt-osi-videos-titles.txt | https://www.youtube.com/@OpenSourceInitiative/videos?hl=en&gl=US | https://www.youtube.com/@OpenSourceInitiative/videos?hl=en&gl=US | 200 | 1802 | 33603205eda46fde | 2026-10-18T05:37:34Z |
| ato-the-state-of-the-open-source-initiative.html | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | 200 | 51930 | 267bd2b1e628262d | 2026-10-18T05:37:34Z |
| ato-open-source-licensing-101.html | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | 200 | 51874 | 485981395d3649ad | 2026-10-18T05:37:34Z |
| ato-sharing-is-caring-open-data-for-open-source-compliance.html | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | 200 | 53930 | 6f98267418faf6c0 | 2026-10-18T05:37:34Z |
| ato-is-open-source-dying-short-film-and-open-discussion.html | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | 200 | 52957 | 8fb91de304905c7b | 2026-10-18T05:37:34Z |
| ato-the-latest-on-public-policy-and-open-source.html | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | 200 | 51966 | eb320502dec716be | 2026-10-18T05:37:35Z |
| ato-the-state-of-open-source-ai-in-2026.html | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | 200 | 52039 | b0f964d3dae606f3 | 2026-10-18T05:37:35Z |
| ato-the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy.html | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | 200 | 53418 | 701b63546a28bc3a | 2026-10-18T05:37:35Z |
| ato-what-makes-open-source-work-licensing-and-beyond.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | 200 | 52307 | 3602f77b395947ad | 2026-10-18T05:37:35Z |
| ato-what-makes-open-source-work-licensing-and-beyond-2.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | 200 | 52359 | 794a3dbf08e66274 | 2026-10-18T05:37:35Z |
| ato-welcome-social-panel-discussion.html | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | 200 | 56108 | b13d7e391c59219e | 2026-10-18T05:37:35Z |

## 観測メモ
1. この回の yt-*-titles.txt は、YouTube が Accept-Language 無しの要求に自動翻訳の日本語題名を返したもので、**原題ではない**。次の回（events-watch-1437）から hl=en と Accept-Language を付けて原題を取っている。
2. 索引に出た the-open-source-initiative-announces-the-release-of-the-industrys-first-open-source-ai-definition は 2024 年の OSAID 公開告知で、新規の記事ではない。

## 観測メモ
1. ATO と OSI の YouTube チャンネルの最新 30 本に、ATO 2026 のセッション録画は無い（会期前・題名で照合）。
