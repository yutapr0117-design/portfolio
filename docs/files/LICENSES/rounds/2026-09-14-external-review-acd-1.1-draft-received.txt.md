---
file: LICENSES/rounds/2026-09-14-external-review-acd-1.1-draft-received.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-14
canonical-ref: LICENSES/ACD-1.0.discussion-log.md (ラウンド 0 が分解と分類) / LICENSES/ACD-OSI-BOTTLENECKS.md (B1 / B7 / B13) / LICENSES/ACD-1.1.txt (レビュー対象)
---

# LICENSES/rounds/2026-09-14-external-review-acd-1.1-draft-received.txt

## What

**`ACD-1.1.txt` 本文への、初めての実質的な外部レビューの逐語。**
良い点 4 件・重大事項 5 件・構造 2 件・優先順位 10 件からなる。

## Why

**このプロジェクトが受け取った、本文を読んだうえでの外部の批評はこれが最初である。**
`license-discuss` への投稿には返信がゼロで、`discussion-log.md` は実際の指摘が入らないまま在った。

**ただし、これが何で*ない*かのほうが重要である。** 出自は **Perplexity のレビューをオーナーが
受け取って共有したもの**（本人申告）。**リストには届いておらず、公開アーカイブにも無い。**
**OSI のフィードバックではなく、`license-review` 参加者の見解でもなく、法的レビューでもない ——
したがって B1（法的レビューの不在）を 1 ミリも動かさない。**

## How

オーナーが貼ったものをそのまま保存した。**この repository は取得していない。**

**唯一の改変**: 本文の引用リンクが AWS の presigned URL で、`AWSAccessKeyId` /
`Signature` / `x-amz-security-token` を含んでいた。**query string のみ
`[presigned-query-redacted]` に置換した。** 語は 1 つも足しても削っても並べ替えてもいない。

## Constraints

- **`LICENSES/rounds/` は無改変保存のディレクトリである。** 上の置換は**意図的な例外**で、
  **理由を file の header に書いてある** —— 無改変規約と「公開リポジトリに資格情報を置かない」が
  衝突し、**他者を守る側の規則を採った。** **この判断が誤りなら、直し方は
  「オーナーの控えから query string を復元する」であって、「この file が完全だと仮定する」ではない。**
- **Check 450（日本語への別スクリプト混入）は本ディレクトリを対象外**にしてある。
- **分析をここに書かない。** 分解・分類は `ACD-1.0.discussion-log.md`「ラウンド 0」が持つ。

## Change impact

新しい外部レビューを受け取ったら同じ形で `rounds/` へ足し、**`rounds/README.md` の在庫申告**を
同じ commit で更新する（**Check 465** が見出しの件数と表の行数を実 file 数と照合する）。

## Audience-specific notes

- **AI（次のセッション）**: **このレビューの優先順位を OSI の優先順位として読まないこと。**
  標本ではない（#109 と同じ誤り）。**採ってよいのは「我々の測定に無かった次元」だけ**で、
  本ラウンドではそれが 3 件（§15.1 の解釈規則 / 条文内の立法理由 / §8.4 の境界事例）と判定されている。
- **監査人**: 逐語はここ、判定は discussion-log、根拠は各判定行に実測として書いてある。
- **第三者**: **提出パケットでこれを第三者レビューとして提示してはならない。**
  **AI 起草への懸念が現に在る場で、AI 由来の批評を人手のレビューとして示すのは最悪の形である。**
