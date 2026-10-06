# fetch/2026-10-06 — portfolio-24（Mac）日次取得

バイト列は取得時のまま。分析はしていない。

| file | 要求 URL | 最終 URL | status | bytes | sha256[:16] | 取得 UTC |
|---|---|---|---|---|---|---|
| license-review_2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt | 200 | 400071 | bb7b6fc5de799aa9 | 2026-10-06T03:28:25Z |
| (未取得) license-review_2026-October.txt | https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-06T03:28:31Z |
| license-discuss_2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-September.txt | 200 | 29005 | aaef3c782edc42a0 | 2026-10-06T03:28:32Z |
| (未取得) license-discuss_2026-October.txt | https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt | — | HTTP Error 404: Not Found | — | — | 2026-10-06T03:28:33Z |
| opensource.org_code-of-conduct.html | https://opensource.org/code-of-conduct | https://opensource.org/codeofconduct/code-of-conduct-for-osi-mailing-lists | 200 | 188592 | 38bc5dff3f2c70aa | 2026-10-06T03:28:33Z |
| opensource.org_codeofconduct.html | https://opensource.org/codeofconduct | https://opensource.org/codeofconduct | 200 | 191354 | 3be3c0f0d1ec8986 | 2026-10-06T03:28:35Z |
| opensource.org_minutes.html | https://opensource.org/minutes | https://opensource.org/minutes | 200 | 211944 | cc50ca64a4c88485 | 2026-10-06T03:28:36Z |
| opensource.org_licenses.html | https://opensource.org/licenses | https://opensource.org/licenses | 200 | 255668 | 71ceecc5ed11e372 | 2026-10-06T03:28:37Z |
| events/oscl-official.html | https://conference.opensource.lu/ | https://conference.opensource.lu/ | 200 | 72926 | f0144c8993864e89 | 2026-10-06T03:28:38Z |
| events/oscl-pretalx-schedule.html | https://pretalx.com/open-source-conference-luxembourg-2026/schedule/ | https://pretalx.com/open-source-conference-luxembourg-2026/schedule/ | 200 | 42526 | 282cf650c4088a2e | 2026-10-06T03:28:41Z |
| events/ossummit-eu-2026.html | https://events.linuxfoundation.org/open-source-summit-europe/ | https://events.linuxfoundation.org/open-source-summit-europe/ | 200 | 267414 | 18e3fbea07b634a9 | 2026-10-06T03:28:42Z |

## 追加（クラウドの依頼 trig_01XQEAQ24ZR92kupieZSsExq への応答・2026-10-06 03:48 UTC）

| file | 要求 URL | status | 原本 bytes | 原本 sha256 | 取得 UTC |
|---|---|---|---|---|---|
| events/ato-2026-schedule-tuesday.pdf.txt | https://2026.allthingsopen.org/wp-content/uploads/2026/09/10.20.26.ATO_Schedule_Tuesday_09.10.26.pdf | 200 | 177218 | 9bc1bc3c625b30e5c085d683554017b1fbd3b06717aaeaf42bad7d38f4316363 | 2026-10-06T03:48:20Z |

PDF 原本は commit していない（Check 122）。.txt は pypdf 6 系の `extract_text()` の出力をそのまま保存したもの（1 ページ・13,808 字）で、**原本の逐語ではなく抽出物**である（段組の読み順・改行・"T o" のような字間の割れは抽出器による）。原本は上の URL と sha256 で再取得・照合できる。月曜の PDF（10.19.26.ATO_Schedules_Monday_09.10.26.pdf）は依頼の対象外なので取っていない。
