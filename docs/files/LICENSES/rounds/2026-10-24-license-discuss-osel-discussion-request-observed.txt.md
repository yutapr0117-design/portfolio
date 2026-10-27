---
file: LICENSES/rounds/2026-10-24-license-discuss-osel-discussion-request-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-10-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/OSI-EVENTS-2026-10.md / LICENSES/PEER-REVIEW-WATCH.md
---

# LICENSES/rounds/2026-10-24-license-discuss-osel-discussion-request-observed.txt

## What

`license-discuss` の **"Discussion request: Open Source Evolution License 0.2"**（OpenReciprocal・2026-10-24）。2026-10-27 03:04 UTC に portfolio-01 が取得。
**我々宛ではなく、ACD についてでもない。**

## Why

単独の提出者が `license-review` ではなく `license-discuss` へ議論を求め、commit を固定し、弁護士のレビューが無いこと・採用ゼロを自分で開示した ——**我々が 2026-08-26 に取ったのとほぼ同じ形**である。この形にリストがどう応じるかを、我々の沈黙（`against.md` #109）と並べて観測するために残す。

**⚠ この file が establish しないこと**: リストの応答（取得時点で返信は無い）／OSEL の中身が承認されうるか（中身は一方向の付け替えで、ACD の gap とは重ならない）。

## How

`https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-October.txt` を portfolio-01 が
**ブラウザ相当の UA** で取得し（受け渡し `86592ef`）、該当メッセージ・ブロックを月次ファイルからバイト列のまま切り出した
（月次ファイルの部分列であることを書き出し前に assert 済み）。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。他人の誤字も直さない。
- **観測（`-observed`）であって受領ではない。**

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: 引用は逐語でこの file から取る。
- **監査人**: 取得元 URL の同スレッドと突き合わせれば再現できる。
