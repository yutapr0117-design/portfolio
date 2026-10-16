# fetch/2026-10-16/events — portfolio-24 監視セッション（Mac）によるイベント掘削

オーナー依頼（2026-10-16「イベントを掘りまくって」）による追加取得。バイト列は取得時のまま。**フォルダ名の日付は JST、取得時刻は UTC。** 取得は python urllib + ブラウザ相当 UA。最終 URL は転送が確認できたものだけ要求 URL と変えて書いた。

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得時刻（UTC） |
|---|---|---|---|---|---|---|
| osi-events.html | https://opensource.org/events | https://opensource.org/events | 200 | 188089 | 31ac42acf0c5a1a4 | 2026-10-16T12:35:17Z |
| osi-blog.html | https://opensource.org/blog | https://opensource.org/blog | 200 | 208700 | 46a16f673a3542b1 | 2026-10-16T12:35:17Z |
| osi-blog-feed.xml | https://opensource.org/feed | https://opensource.org/feed | 200 | 110552 | 8999405c8956f769 | 2026-10-16T12:35:18Z |
| osi-codeofconduct-mailing-lists.html | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 188702 | ee13f44757e68fd6 | 2026-10-16T12:35:18Z |
| osi-ai-salon.html | https://opensource.org/ai-salon | https://opensource.org/ai-salon | 200 | 192829 | 97541aa62d6f3fc7 | 2026-10-16T12:35:18Z |
| osi-open-source-ai.html | https://opensource.org/ai | https://opensource.org/ai | 200 | 228970 | d231df644bf7627e | 2026-10-16T12:35:19Z |
| ato-2026-schedule.html | https://2026.allthingsopen.org/schedule | https://2026.allthingsopen.org/schedule | 200 | 163931 | 3bb1634d929b6129 | 2026-10-16T12:35:21Z |
| ato-2026-speakers.html | https://2026.allthingsopen.org/speakers | https://2026.allthingsopen.org/speakers | 200 | 203567 | b9c73ee44060ef7b | 2026-10-16T12:35:23Z |
| otr-symposium-official.html | https://symposium.opentechresearch.org/ | https://symposium.opentechresearch.org/ | 200 | 463348 | 28d6fe965ae101c8 | 2026-10-16T12:35:27Z |
| (未取得) otr-symposium-programme.html | https://symposium.opentechresearch.org/programme | — | 下表 | — | — | — |
| (未取得) barcelona-open-tech-week.html | https://opentechweek.barcelona/ | — | 下表 | — | — | — |
| code-compliance-luma.html | https://luma.com/orc1026 | https://luma.com/orc1026 | 200 | 98720 | 1414fe3b6a3341ef | 2026-10-16T12:35:30Z |
| mozfest.html | https://www.mozillafoundation.org/en/festival/ | https://www.mozillafoundation.org/en/festival/ | 200 | 75243 | 9eceed16d0b3263b | 2026-10-16T12:35:31Z |
| ossummit-eu-2026.html | https://events.linuxfoundation.org/open-source-summit-europe/ | https://events.linuxfoundation.org/open-source-summit-europe/ | 200 | 263205 | a4ae2f9c6db77586 | 2026-10-16T12:35:32Z |
| osseu-2026-2RahK.html | https://osselceu2026.sched.com/event/2RahK | https://osselceu2026.sched.com/event/2RahK | 200 | 59312 | 4255443766251671 | 2026-10-16T12:35:33Z |
| osseu-2026-2RaXq.html | https://osselceu2026.sched.com/event/2RaXq | https://osselceu2026.sched.com/event/2RaXq | 200 | 58889 | 3db166be4a8d583e | 2026-10-16T12:35:34Z |
| osseu-2026-2XrR8.html | https://osselceu2026.sched.com/event/2XrR8 | https://osselceu2026.sched.com/event/2XrR8 | 200 | 57459 | ad49a1ab68ccfb8a | 2026-10-16T12:35:35Z |
| osseu-2026-2RaXA.html | https://osselceu2026.sched.com/event/2RaXA | https://osselceu2026.sched.com/event/2RaXA | 200 | 59225 | 252a23a949d76ebd | 2026-10-16T12:35:36Z |
| osseu-2026-2RaaY.html | https://osselceu2026.sched.com/event/2RaaY | https://osselceu2026.sched.com/event/2RaaY | 200 | 63911 | 2e74f951c9dd8046 | 2026-10-16T12:35:37Z |
| osseu-2026-2Raim.html | https://osselceu2026.sched.com/event/2Raim | https://osselceu2026.sched.com/event/2Raim | 200 | 58707 | 72edca952e5d2745 | 2026-10-16T12:35:38Z |
| duke-convening-search.html | https://opensource.org/?s=convening | https://opensource.org/?s=convening | 200 | 197644 | c87bdfad089f25ba | 2026-10-16T12:35:39Z |
| osi-blog-unga81.html | https://opensource.org/blog/open-enables-a-lot-the-osi-at-unga81 | https://opensource.org/blog/open-enables-a-lot-the-osi-at-unga81 | 200 | 202161 | 955d935d1a918b5d | 2026-10-16T12:36:06Z |
| osi-blog-top-50-conferences-2026.html | https://opensource.org/blog/top-50-open-source-conferences-in-2026 | https://opensource.org/blog/top-50-open-source-conferences-in-2026 | 200 | 208656 | 0ba374be6e3f9e87 | 2026-10-16T12:36:06Z |
| osi-event-all-things-open-2.html | https://opensource.org/events/all-things-open-2 | https://opensource.org/events/all-things-open-2 | 200 | 191179 | d88d3e3d2fa924e9 | 2026-10-16T12:36:06Z |
| osi-event-mozilla-festival.html | https://opensource.org/events/mozilla-festival | https://opensource.org/events/mozilla-festival | 200 | 188385 | 6b555ee13d8ff3fb | 2026-10-16T12:36:07Z |
| osi-event-otr-symposium.html | https://opensource.org/events/open-technology-research-symposium | https://opensource.org/events/open-technology-research-symposium | 200 | 189766 | 7030ec684f35f793 | 2026-10-16T12:36:08Z |
| ato-2026-home.html | https://2026.allthingsopen.org/ | https://2026.allthingsopen.org/ | 200 | 233899 | deaef6d1cac29f88 | 2026-10-16T12:36:10Z |
| ato-2026-session-welcome-social-panel-discussion.html | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | https://2026.allthingsopen.org/sessions/welcome-social-panel-discussion | 200 | 56108 | f13412a0ee028400 | 2026-10-16T12:37:03Z |
| ato-2026-session-the-state-of-the-open-source-initiative.html | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | https://2026.allthingsopen.org/sessions/the-state-of-the-open-source-initiative | 200 | 51930 | a08036699f262630 | 2026-10-16T12:37:03Z |
| ato-2026-session-open-source-licensing-101.html | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | https://2026.allthingsopen.org/sessions/open-source-licensing-101 | 200 | 51874 | fb5e5bd4f1ddda5f | 2026-10-16T12:37:04Z |
| ato-2026-session-what-makes-open-source-work-licensing-and-beyond.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond | 200 | 52307 | 77016b6620e825bf | 2026-10-16T12:37:05Z |
| ato-2026-session-sharing-is-caring-open-data-for-open-source-compliance.html | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | https://2026.allthingsopen.org/sessions/sharing-is-caring-open-data-for-open-source-compliance | 200 | 53930 | dda9c80bebed1c08 | 2026-10-16T12:37:07Z |
| ato-2026-session-what-makes-open-source-work-licensing-and-beyond-2.html | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | https://2026.allthingsopen.org/sessions/what-makes-open-source-work-licensing-and-beyond-2 | 200 | 52359 | 174adf4d093ccbf8 | 2026-10-16T12:37:08Z |
| ato-2026-session-is-open-source-dying-short-film-and-open-discussion.html | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | https://2026.allthingsopen.org/sessions/is-open-source-dying-short-film-and-open-discussion | 200 | 52957 | 92152e3f85930896 | 2026-10-16T12:37:09Z |
| ato-2026-session-the-latest-on-public-policy-and-open-source.html | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | https://2026.allthingsopen.org/sessions/the-latest-on-public-policy-and-open-source | 200 | 51966 | 915423a7fbd737e4 | 2026-10-16T12:37:10Z |
| ato-2026-session-the-state-of-open-source-ai-in-2026.html | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | https://2026.allthingsopen.org/sessions/the-state-of-open-source-ai-in-2026 | 200 | 52039 | 5098c90abcda50da | 2026-10-16T12:37:11Z |
| ato-2026-session-the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy.html | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | https://2026.allthingsopen.org/sessions/the-osi-must-do-more-when-it-comes-to-open-source-education-and-advocacy | 200 | 53418 | 09813857cfd917bd | 2026-10-16T12:37:12Z |
| lf-legal-summit.html | https://events.linuxfoundation.org/lf-legal-summit/ | https://events.linuxfoundation.org/lf-legal-summit/ | 200 | 126757 | 87723974f00eda2a | 2026-10-16T12:37:56Z |
| lf-legal-summit-program.html | https://events.linuxfoundation.org/lf-legal-summit/program/schedule/ | https://events.linuxfoundation.org/one-summit-north-america/ | 200 | 199184 | 704df9a45b929be9 | 2026-10-16T12:37:57Z |
| community-over-code.html | https://communityovercode.org/ | https://communityovercode.apache.org/ | 200 | 14072 | e2279b77dc0a6934 | 2026-10-16T12:37:59Z |
| community-over-code-schedule.html | https://communityovercode.org/schedule/ | https://communityovercode.apache.org/events/glasgow-2026/schedule | 200 | 14229 | 3a5ba2819bc58010 | 2026-10-16T12:38:01Z |
| seagl.html | https://seagl.org/ | https://seagl.org/ | 200 | 25722 | 47836f52264e5c3f | 2026-10-16T12:38:01Z |
| pytorch-conf-2026.html | https://events.linuxfoundation.org/pytorch-conference-2026/ | https://events.linuxfoundation.org/pytorch-conference-north-america/ | 200 | 306457 | 79a8a3f0d66a41f1 | 2026-10-16T12:38:02Z |
| latinoware.html | https://latinoware.org/ | https://latinoware.org/ | 200 | 992076 | a7c23315c73a4a6c | 2026-10-16T12:38:09Z |
| osi-blog-open-source-ai-fellowship.html | https://opensource.org/blog/open-source-ai-fellowship-announced-at-un-open-source-week | https://opensource.org/blog/open-source-ai-fellowship-announced-at-un-open-source-week | 200 | 190416 | 32c29dcc3483e6cb | 2026-10-16T12:39:24Z |
| osi-blog-category-events.html | https://opensource.org/blog/category/events | https://opensource.org/blog/category/events | 200 | 205602 | 6bf8d67460f6c1f1 | 2026-10-16T12:39:25Z |
| osi-blog-state-of-the-source-ato-2026.html | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | https://opensource.org/blog/osi-brings-the-state-of-the-source-to-all-things-open-2026 | 200 | 194218 | a2d066e30a87cca6 | 2026-10-16T12:39:25Z |

## 取れなかったもの

| URL | 理由 | 取得時刻（UTC） |
|---|---|---|
| https://symposium.opentechresearch.org/programme | HTTP 404（推測した URL。プログラムはトップページに載っている） | 2026-10-16T12:35:27Z |
| https://opentechweek.barcelona/ | DNS 解決不能（推測した URL） | 2026-10-16T12:35:29Z |
| Community over Code（Glasgow）のセッション一覧 | `community-over-code-schedule.html` は Cvent の JS 埋め込みで、静的 HTML に講演名が無い | — |
| OSS Summit Europe 6 セッションの録画 | YouTube 検索（4 クエリ・2026-10-16 12:4x UTC）で該当する動画は見つからなかった。**検索に出なかっただけで、存在しないとは言えない**。検索結果ページは保存していない | — |

## 取得役の観測メモ（分析ではない —— 本文を当たって確かめるのはクラウド側）

1. **ATO の 10/18（日）は在る**: `ato-2026-schedule.html` の埋め込み JSON に `"date":"October 18, 2026"` —— 12:00–18:00 *Early Check-in*（Convention Center）と 18:00 *Welcome Social & Panel Discussion*（Sheraton・パネル題 "Open Source in the Age of AI"・Dana Fine / Nithya Ruff / Wallon Walusayi）。**10-05 取得分にも同じ行がある**（読まれていなかった）。OSI の `/events` と `/events/all-things-open-2`、Top 50 の記事も **October 18–20** と書く。本会議は 10/19–20 のまま。
2. **ライセンスの講演が State of the Source の外にもう 1 本**: *What Makes Open Source Work: Licensing and Beyond*（Peter Farkas）10/20 12:00 Room 307 と 1:00 pm Ballroom B の 2 回。10-05 取得分にも在る。
3. **Licensing 101（McCoy Smith）の概要に "tips for understanding the OSI license approval process"** —— `ato-2026-session-open-source-licensing-101.html`。
4. **Sharing is caring の登壇者は 3 名**（Alyssa Wright・Brian Duran・Nick Vidal）。10-05 取得分から同じ。
5. ATO の全セッション数は 10-05: 265 → 10-14: 274 → 今回 275。ライセンス/OSI 関連の行で変わったのは時刻 1 件（Awards Ceremony 4:30→4:00）と無関係な 1 件の追加だけ。
6. **Linux Foundation Legal Summit が 10 月にある**（イベント表に無い）: 公式 `lf-legal-summit.html` は **October 20-21, 2026・San Jose**・LF の Platinum/Gold/Silver 会員企業の法務担当が招待される形。公開の時間割は "Legal Summit Presentations" だけで講演名は無い。**OSI の Top 50 記事は "October 21–22, 2026 (North America, TBD)" と書いており食い違う**（公式ページの方が具体的）。
7. **Barcelona の AI Salon は 10/27（火）17:00–18:00・"UB library"**、OTR 公式トップに *"The event will take place at the UB library"*、登壇欄に Katie Steen-James（OSI）。10-05 取得分にも同じ文がある。
8. **Raleigh の AI Salon から会場名 "The Gables Hotel" が消えている**: 10-05 取得分には在り、10-14 と今回の `/ai-salon` には無い（`article:modified_time` 2026-10-06T17:34:09）。
9. OTR Symposium のプログラムは 10-05 から大きく変わった（登壇者の追加・時刻の移動・講演の入れ替え）。OSI の Katie Steen-James は 10/26 の Plenary（17:35–18:20）と閉会、10/27 の Breakout（15:05–16:05）にも名前がある。
10. Code & Compliance（Luma）は 10/27 07:30–16:30 UTC のまま。会場は **Maison de la Poste, Rue Picard 7, Brussels**（10-05 取得分から同じ）。
11. OSI ブログに 10/8 公開の **"Open Enables a Lot: The OSI at UNGA81"**（9/21 の国連デジタル協力の日のパネル・OSAID への言及あり）。イベント自体は 9 月。同記事は Duke と 6 月に始めた **Open Source AI Fellowship** に触れる（`osi-blog-open-source-ai-fellowship.html`）。Opening Convening（10/21）の詳細は State of the Source 記事で "More information will be announced soon" のまま（本文は 10-14 取得分から不変）。
12. Mailing list 用 CoC `/codeofconduct/code-of-conduct-for-osi-mailing-lists` は 200・`article:modified_time` **2023-05-04**・本文に AI への言及は見当たらない（ナビゲーションを除いて grep）。
13. OSS Summit EU の sched 6 件: スライドが付いているのは引き続き 2RaXA だけ（hosted-files の PDF 1 件）。
14. OSI の Top 50 記事が挙げる 10 月の他のイベント（取得はトップページのみ）: Community over Code（ASF・Glasgow・10/11–14）/ Latinoware（10/14–16）/ PyTorch Conference NA（10/20–21・San Jose）/ SeaGL（10/23–24）。
