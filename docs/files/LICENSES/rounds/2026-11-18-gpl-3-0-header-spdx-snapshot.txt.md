---
file: LICENSES/rounds/2026-11-18-gpl-3-0-header-spdx-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-18
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2026-11-18-gpl-3-0-header-spdx-snapshot.txt

## What

SPDX の license-list-data が保持する GPL-3.0 の本文の頭の 6 行（著作権の表示と「この文書の逐語の写しを複製し頒布することは誰にでも許されるが、変更は許されない」）を、GitHub の API で byte のまま取った写し。最後にその file を触った commit で固定した。

## Why

1.4 草案の §16.4 は、改変した本文を名と識別子の下で頒布することを制限する。THIRD §18.5 の台帳でその行は法源が無かった。承認済みのライセンスが自分の本文の改変そのものを禁じる先例で、§16.4（名と識別子に限る）より強い形。オーナーの依頼（2026-11-16）の portfolio-2f の受け持ち。

## How

`gh api` で raw の内容を取った（モデルを通さない）。gnu.org は接続が切れ（2f が 3 度・portfolio-50 が 1 度）、OSI の GPL-3.0 の頁にはこの前置きが無かった（50）。

## Constraints

SPDX の写しで、FSF 自身の file ではない。この文は GPL の本文（ライセンス文書）の改変を禁じるもので、GPL の下の著作物の改変を禁じるものではない。ACD を扱っていない。

## Change impact

THIRD §18.5 の §16.4 の行と SECOND の 883 行目の引用を直すときは、この commit の file で確かめる。

## Audience-specific notes

- **監査人**: 本文の改変の禁止がどの法で支えられるか（ライセンス文書の著作権か、商標か）は、この写しからは決まらない。
