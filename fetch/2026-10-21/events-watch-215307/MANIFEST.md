# fetch/2026-10-21/events-watch-215307 — portfolio-01（Mac）イベント監視取得

バイト列は取得時のまま。**フォルダ名は JST、取得時刻は UTC。** 下の「手掛かり」は正規表現による抽出で、本文を読んだ判定ではない。

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| ato-sots.html | https://2026.allthingsopen.org/the-state-of-the-source | https://2026.allthingsopen.org/the-state-of-the-source | 200 | 89283 | c90b55940c4b6b10 | 2026-10-21T12:53:07Z |
| osi-events.html | https://opensource.org/events | https://opensource.org/events | 200 | 194624 | e8f5bcdd37af750a | 2026-10-21T12:53:09Z |
| osi-blog.html | https://opensource.org/blog | https://opensource.org/blog | 200 | 215446 | 51133c8fa2be6b77 | 2026-10-21T12:53:09Z |
| osi-blog-events.html | https://opensource.org/blog/category/events | https://opensource.org/blog/category/events | 200 | 213903 | f2c451199e91e046 | 2026-10-21T12:53:09Z |
| osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 200915 | 13303466564a9594 | 2026-10-21T12:53:09Z |
| yt-allthingsopen-videos-titles.txt | https://www.youtube.com/@allthingsopen/videos?hl=en&gl=US | https://www.youtube.com/@allthingsopen/videos?hl=en&gl=US | 200 | 1782 | 17e656fdf5e175e5 | 2026-10-21T12:53:09Z |
| yt-osi-videos-titles.txt | https://www.youtube.com/@OpenSourceInitiative/videos?hl=en&gl=US | https://www.youtube.com/@OpenSourceInitiative/videos?hl=en&gl=US | 200 | 1802 | 33603205eda46fde | 2026-10-21T12:53:10Z |
| ato-the-state-of-the-open-source-initiative.html | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | 200 | 51930 | 561475948c9528fd | 2026-10-21T12:53:10Z |
| ato-open-source-licensing-101.html | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | 200 | 51874 | 91afc5a3e415f8ec | 2026-10-21T12:53:11Z |
| ato-sharing-is-caring-open-data-for-open-source-compliance.html | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | 200 | 53930 | 50854c57cebaeefd | 2026-10-21T12:53:12Z |
| ato-is-open-source-dying-short-film-and-open-discussion.html | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | 200 | 52957 | 8e1911ebda0b057a | 2026-10-21T12:53:13Z |
| ato-the-latest-on-public-policy-and-open-source.html | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | 200 | 51966 | 840950806ce939bd | 2026-10-21T12:53:14Z |
| ato-the-state-of-open-source-ai-in-2026.html | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | 200 | 52039 | 65ef4e1f8a5d48c6 | 2026-10-21T12:53:15Z |
| ato-the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy.html | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | 200 | 53418 | 0fb2c1f3dd397161 | 2026-10-21T12:53:15Z |
| ato-what-makes-open-source-work-licensing-and-beyond.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | 200 | 52307 | 47023075cb5f786c | 2026-10-21T12:53:16Z |
| ato-what-makes-open-source-work-licensing-and-beyond-2.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | 200 | 52359 | 908d86a8838db521 | 2026-10-21T12:53:17Z |
| ato-welcome-social-panel-discussion.html | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | 200 | 56108 | 46aed36898f468de | 2026-10-21T12:53:18Z |

- 監視メモ（2026-10-21 21:53 JST）: 115609 と比較して変化なし。ブログ新記事 0・録画/スライド 0。YouTube は ATO の short 1 本（「17 years in restaurants…」）が入れ替わっただけで、ATO 2026 のセッション録画ではない。main には書かない。

**受け渡し漏れの是正（2026-10-22 09:0x JST）:** この回は MANIFEST だけを commit しており、本体 HTML / 題名一覧が未追跡のまま手元に残っていた（クラウドが 10-21 行で「バイトでは確かめられない」と指摘）。取得時のバイト列のまま、ここで追加 commit した（内容は取得時から未変更）。原因: 監視の commit を MANIFEST の明示パスだけにしていた。以後はフォルダ単位で add する。
