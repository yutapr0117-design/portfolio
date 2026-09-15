---
file: .github/scripts/measure_list_verbosity.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-15
canonical-ref: LICENSES/ACD-1.0.review-corpus.md §1.85 (測定結果) / LICENSES/rounds/2026-09-15-offlist-nick-vidal-round3.txt (問いの出所) / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md B14
---

# .github/scripts/measure_list_verbosity.py

## What

**我々が OSI の 2 つのメーリングリストへ送ったメールの長さと密度を、同じ窓の他の参加者と
比べる道具。** 公開アーカイブを月単位で取得し、1 通ずつ測って分布・パーセンタイル・
参加者別の総量順位を出す。**Check ではない**（外部取得が要る）。

## Why

**2026-09-15、OSI の moderator が steward へ直接この測定を求めた** ——
*"Map out the **length and density** of your emails and compare it with the length and density of
other emails sent to these two mailing lists by humans."*

**測れる問いに散文で答えるのは、入口ページが掲げる *check us* に反する。** だから道具を置いて、
**誰でも同じ数を出せる**ようにした。結果は `review-corpus.md` §1.85。

## How

**長さを 2 つに分けて数えるのが要点である。**

| 指標 | 何を数えるか | 何の問いに答えるか |
| :-- | :-- | :-- |
| **delivered** | 受け手の inbox に届いた本文全体（貼り付けた条文・引用を含む）| **時間と注意を消費するのはこちら** |
| **prose** | その人が新しく書いた散文だけ（引用行 `>`・署名・フッタ・MIME の次パート以降を除く）| **「長い文章を書く人か」を見るのはこちら** |

**片方だけで語ると、有利にも不利にも見せられる。** 実例: 2026-08-26 の ACD 投稿は
**delivered 5,778 語 / prose 867 語**（条文を本文へ貼り付けたため）。**どちらも真だが、
答える問いが違う。**

密度の代理指標は **1 文あたりの語数**と **1 段落あたりの語数**。
**短い文・短い段落は読みやすさの側**なので、**「長い」と「密である」は別に測る**。

steward の From 行は pipermail が日本語表示名を RFC 2047 で符号化するため、
**素の綴りと符号化後の両方**を見る（片方だけだと自分の投稿を 3 通見落とす）。

```
python3 .github/scripts/measure_list_verbosity.py --fetch
python3 .github/scripts/measure_list_verbosity.py --months 2026-June,2026-July
```

## Constraints

- **CI には入れない（意図的）。** 公開アーカイブの取得が要り、CLAUDE.md §7 が「自動監視は CI に
  入れない」と定めている。`verify_dossier_quotations.py` / `measure_clause_clarity.py` と同じ扱い。
- **窓を変えたら結果も変わる。** 既定は 2026-07〜09 で、§1.85 の数はその窓のものである。
  **別の窓の数を §1.85 の数として引かないこと。**
- **比較は弁明ではない。** 「他にも長い人がいる」は、我々が短くする理由を消さない
  （§1.85 の「この節が establish しないこと」）。

## Change impact

- 指標の定義（delivered / prose の切り方、密度の代理指標）を変えたら、
  **`review-corpus.md` §1.85 の表も同じ commit で測り直す。** 数字だけ動かして定義を据え置くと、
  `measure_clause_clarity.py` が直した当の欠陥（**方法が記録されていない数字**）を作り直すことになる。

## Audience-specific notes

- **AI（実装者）**: **数字を出す前に定義を書け。** そして **2 つの長さを必ず併記せよ** ——
  片方だけを出すのは、この道具が防ぐために在る失敗そのものである。
- **監査人**: 再現できる。取得元は pipermail の月次 mbox、切り分けは docstring の表のとおり。
- **第三者**: アーカイブは公開されている。同じコマンドで同じ数が出る。
