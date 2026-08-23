---
file: docs/architecture/acd-license-rationale.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: LICENSES/ACD-1.0.txt / LICENSE
---

# docs/architecture/acd-license-rationale.md

## What

ACD-1.0 の**設計根拠と申請ドシエ**。SPDX License List / OSI License Review への提出時に
必要になる材料を、提出者がそのまま使える形で置いてある。

- §1 gap 分析（OSI の必須要件「既存で埋まらない gap を埋めること」への回答）
- §2 既存ライセンス 11 種との比較表（非重複の証明）
- §3 **OSD 1–10 適合表**（OSI は提出者に OSD 3/5/6/9 の宣言を求める）
- §4 SPDX inclusion principles 適合表
- §5 主要な起草判断とその理由
- §7 **正直な弱点**
- §8 提出手順（人間しか行えない部分）

## Why

新しいライセンスは「自由に使える」だけでは通らない。OSI は proliferation 対策として
**既存で埋まらない gap を埋めることを明示的な要件**にし、SPDX も既存テキストとの非一致を
definitive requirement に置く。したがって**根拠文書が無いライセンスは提出できない**。

同時に、**通らない理由も先に書いておく**必要がある。§7 は実使用の薄さ・テキスト未凍結・
公有化型ツールに対する OSI の歴史的慎重論を隠さず記録している。都合の良い面だけを並べた
ドシエは、査読で覆されたときに信用を失う。

## How (usage)

提出前に §7 の ⚠️ 3 点（実使用・凍結・steward コミット）を解消してから、§8 の手順に従う。
提出そのものは人間の作業。

## Constraints

- **Check 436** の走査対象（`docs/architecture/`）に入るため、「オーナー裁可待ち」型の
  defer 理由を書けない。本書が「提出は人間しか行えない」と書くのは*作業主体*の記述であって
  裁可待ちではない。
- 出典 URL は §9 に集約する。主張の根拠が辿れない状態にしない。

## Change impact

- **ACD-1.0 の本文を変えたら、本書の §2 比較表と §3 OSD 表も同一 commit で見直す。**
  条項番号を参照している箇所が多いので、再採番すると本書が stale になる。
- 提出後に本文を凍結したら、§7-2 の記述を「凍結済み」へ更新する。

## Audience-specific notes

### For AI agents
- 役割タグ: `license-rationale`, `spdx-submission`, `osi-review`, `gap-analysis`

### For human engineers (新卒レベル)
- ライセンスは「気持ち」ではなく**審査基準に対する適合**で通る。基準は公開されているので、
  推測ではなく読んで照合する。

### For third parties
- 独自ライセンスを起草・申請しようとする人にとって、**却下要因を先に潰す**やり方の実例として
  読める。とくに CC0 が OSI で止まった理由（特許不許諾）への対処は再利用しやすい。
