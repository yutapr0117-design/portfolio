---
file: LICENSES/ACD-1.0.review-rules.md
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-15
canonical-ref: LICENSES/ACD-1.0.review-corpus.md (切り出し元・アーカイブ全体の測定) / LICENSES/ACD-1.0.review-precedents.md (個別スレッドの読み) / LICENSES/ACD-1.0.board-decisions.md (理事会の決定) / LICENSES/rounds/ (原典の保存)
---

# LICENSES/ACD-1.0.review-rules.md

## What

**OSI が公表しているページを、原典で読んだ記録。** 収めているのは §1.70（新規ライセンスの
承認基準 8 条）/ §1.76（提出の要件リスト）/ §1.81（Code of Conduct の棚卸し）/
§1.82（本文を変えたい提出者に課される手続き）/ §1.86（CoC を 1 項ずつ当てた結果）、
および §1.70 配下の §1.70a・§1.70b（明晰さの測定と、その二度の訂正）。

## Why

**資料の種類で分けている。** 本リポジトリのドシエは、同じ出来事についての 4 種類の記録を持つ:

| file | 何の記録か |
| :-- | :-- |
| **本 file** | **OSI が公表しているページ＝規則** |
| `ACD-1.0.review-corpus.md` | メーリングリストのアーカイブ**全体**を測ったこと |
| `ACD-1.0.review-precedents.md` | **個別スレッド**の読み |
| `ACD-1.0.board-decisions.md` | **理事会**という別の発話主体の**決定** |

**公表ページは規則を、リストは議論を、理事会は決定を残す。** 1 つの file に置くと
**「誰が言ったか」が節の位置から読めなくなる**（#139 は、この区別を持たずに測ったせいで
「決定の記録を議論の記録から読んでいた」という構造的な穴を作った）。

切り出しの直接の引き金は、2026-09-15 に corpus が **1,000 行の BLOCKING（Check 365）**に
当たったことである。**圧縮せず、いま触っているクラスタを切り出した**（house pattern）。

## How

**節番号は動かしていない。** §1.70 は §1.70 のまま本 file にある ——**既存の参照をすべて
有効に保つため**。名指しの参照（`` `review-corpus.md` §1.81 ``）は **Check 471 face (d) が
即座に RED にした**ので、7 file を追従させた。**gate が移動の後始末を列挙してくれた形である。**

**新しい節をどこに足すかの規則**:

- **公表ページの逐条** → 本 file
- **アーカイブ全体の測定** → `review-corpus.md`
- **個別スレッドの読み** → `review-precedents.md`
- **理事会の決定** → `board-decisions.md`

## Constraints

- **`§1.xx` は 4 → 5 file に分かれた共有採番である。** 新しい節を足すときは
  **その番号がどの file にも無いことを導出して確かめる**（**Check 471 face (f)** が新しい衝突を
  BLOCKING で禁じる。既存の §1.67 / §1.68 / §1.69 は grandfather）。
- **公表ページは動く。** 本 file が引くページは `rounds/` に取得日つきで pin してある
  （`2026-09-14-osi-normative-pages-snapshot.txt` / `2026-09-15-osi-mailing-list-code-of-conduct-snapshot.txt`）。
  **pin していないページを引かないこと** ——更新された瞬間、我々の読みが誤りだったのか
  ページが動いたのかを区別できなくなる。

## Change impact

- 節を足したら `LICENSES/README.md` の索引（**Check 459** が到達性を強制）と、
  行数を `docs/architecture/file-size-budget.md` §2 表（**Check 424**）へ同じ commit で。
- **公表ページの更新を観測したら、本 file の「まだ更新されていない」系の記述も直す** ——
  これは状態についての主張であり、古くなる。

## Audience-specific notes

- **AI（実装者）**: **「読んだ」と「1 条ずつ当てた」は別である**（§1.81 / §1.86 がその実例）。
  規範文書を引くときは、**条文を 1 つずつ当てて、当たらなかった項目も書く。**
- **監査人**: 各節は取得日を持ち、逐語は `rounds/` に在る。
- **第三者**: ここに在るのは**公表ページの引用と、それを我々に当てた結果**であって、
  OSI の見解の要約ではない。
