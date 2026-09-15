---
file: LICENSES/rounds/2026-09-15-osi-mailing-list-code-of-conduct-snapshot.txt
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-15
canonical-ref: LICENSES/ACD-1.0.review-corpus.md §1.86 (1 項ずつ当てた結果) / LICENSES/rounds/2026-09-13-osi-code-of-conduct-pre-update-snapshot.txt (もう一方の URL) / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md B14
---

# LICENSES/rounds/2026-09-15-osi-mailing-list-code-of-conduct-snapshot.txt

## What

**OSI の「メーリングリスト用」Code of Conduct（`/code-of-conduct`）の全文を、取得日つきで
保存したもの。** 2026-09-15 取得。ページ自身は *"Page created on February 6, 2013 |
Last modified on May 4, 2023"* と述べている。

## Why

**理由が 2 つあり、どちらも「近い文書は、その文書ではない」という同じ形をしている。**

**(1) 我々は 2 つある CoC のうち別の方を pin していた。**

| URL | 自称 | 我々の扱い |
| :-- | :-- | :-- |
| `/codeofconduct` | created 2007-11-19 / modified **2023-11-02** | 2026-09-13 に pin |
| `/code-of-conduct` | **"Code of Conduct for OSI Mailing Lists"**・created 2013-02-06 / modified **2023-05-04** | **本 file（2026-09-15）** |

**実測すると本文はほぼ同一**（776 語 対 789 語・差は箇条書きの番号と markup であって中身では
ない）。**だから前の pin から引いた結論に誤りは無い。** それでも pin し直したのは、
**リストを規律しているのは後者であり、条を引かれた相手も後者だから**である。

**(2) 予告された更新が、まだ起きていない。** 2026-09-09 に moderators は CoC を
*"updated to better reflect the use of AI"* にすると述べた。**6 日後の時点で両ページとも
変わっていない**（自称更新日はそのまま、本文に AI の条項は 1 つも無い）。
**したがって steward に引かれた規則は Code of Conduct には無く、moderators のリスト投稿に在る。**

**⚠ この事実を反論に使わないこと。** リストを運営しているのは moderators であり、
**published かどうかは、その方針が実在するかとは別の問いである。**
記録するのは「どの文書に何が書いてあるか」であって、「だから従わなくてよい」ではない。

## How

ブラウザ相当の UA で取得し、HTML をテキストへ落とした。**本文はページ自身の
"Page created on ..." 行から始まり、サイトフッタの直前で終わる。**
サイトナビゲーションは**除外**する —— 全ページに繰り返され、その語（例: "Open Source AI"）が
本文として数えられてしまう。**本リポジトリは一度それをやって数を誤っている**（`BLIND-SPOTS.md`）。

## Constraints

- **無改変で保存する。** このディレクトリで byte を変えることは規約違反である。
- **更新されたら、この file は「更新前の姿」になる。削除しない。**
  **我々の 2 通が送られた時点で効力を持っていた文は、更新後のライブページからは取れない。**
- **もう一方の URL の snapshot も残す。** 2 つ在ることが分かるのは、2 つ在るときだけである。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。
- **CoC が実際に更新されたら、その日に取り直して新しい file を作る**（本 file は上書きしない）。
  そのとき `review-corpus.md` §1.86 の「まだ起きていない」も同じ commit で直す ——
  **これは状態についての主張であり、古くなる。**

## Audience-specific notes

- **AI（実装者）**: §1.86 は本 file の 3 つの小項目に 1 つずつ当てた結果である。
  **1 つに当たり、2 つには当たらない。**「2 つに当たらない」を「条に当たらない」と読まないこと ——
  CoC 自身が *"followed in spirit as much as in the letter"* と述べている。
- **監査人**: 取得日・取得元・抽出範囲はすべて file 冒頭にある。同じ URL を同じ UA で再現できる。
- **第三者**: 公開ページである。ここに在るのは 2026-09-15 時点の姿にすぎない。
