---
file: LICENSE
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-07
canonical-ref: LICENSES/FROZEN.md / docs/architecture/acd-license-rationale.md / .github/scripts/checks_entity.py / .github/scripts/checks_governance_sync.py
---

# LICENSE

## What

本リポジトリが **Autonomous Commons Dedication** の下で公開されていることの
**適用宣言**。いま適用している版は本ファイルの 1 行目が名指す（2026-10-25 に ACD-1.0 から ACD-1.3 へ移った）。権利は一切留保せず、条件も一切課さない。

ライセンス**本文**はここには無い。汎用の全文は本ファイルの `Full text:` 行が指す file にあり、本ファイルは
(a) その適用宣言、(b) 利用者向けの平易な説明、(c) entity provenance（事実の記述であって
条件ではない）、(d) canary と C1–C7 への言及（いずれも利用者を拘束しない）で構成される。

**なぜ分離してあるか**: SPDX の inclusion principles は収録候補のライセンスに対し
「特定のプロジェクト・団体・企業に固有でないこと」を求める。entity 情報を本文へ混ぜると
この要件を落とすので、**汎用本文とプロジェクト固有の宣言を物理的に分けている**。

## Why

2026-08-23 まで本ファイルは **All Rights Reserved** を宣言し、3 つの行為に「事前の書面許諾」を
要求していた（binary の単体再配布 / AIO 公開層の改変 / entity 名の endorsement 誤認利用）。

これはオーナーの意思ではなかった。同日の明言 ——「**承認も裁可も私は全て許可しますし、禁止事項
0 です。それはあなたに対してもそうだし、私のリポジトリを見る人にとってもそうです**」。
前 2 者は撤回した。3 つ目は撤回対象ではないが、**それは「オーナーが課した制限」ではなく
虚偽表示だから**であり、ACD-1.0 §11.3 が「利用者への条件」ではなく「Dedication の射程の限界」
として書いている。

旧ファイルには**内部矛盾**もあった —— 同じファイルが「AI 学習・索引・引用は明示的に許可
（robots.txt 参照・AI に学習されることを意図した公開実験）」と述べながら、頭で All Rights
Reserved を宣言していた。今回の変更はこの齟齬を自由の側へ解消したものでもある。

## How (usage)

GitHub の UI、npm 等の license metadata scanner、および AI クローラが読む。
冒頭の `SPDX-License-Identifier:` 行が機械可読の入口。

利用者側の要約: **何をしてもよく、誰の許可も要らず、表示も不要**。学習に使ってよい。

## Constraints

- **Check 88 (BLOCKING)**: Copyright + entity name + canonical URL + Organization を含むこと。
  本文は権利を放棄するが、**出自は事実として残る**ので "Origin" 節に記載してある。
- **Check 441e (BLOCKING)**: 適用する版の識別子と全文ファイルの path を実際に参照し、
  その版が凍結済みであること（**存在 ≠ 配線**）。
- **Check 441a–d (BLOCKING)**: 全文の側の構造整合。

## Change impact

- **確定した版の本文は凍結されており変えない（`LICENSES/FROZEN.md`）。本ファイルは適用宣言なので、条項の実体を
  ここへ書き足さない**（書くと汎用本文との二重管理になり、どちらが正本か判らなくなる）。
- entity 情報を変えたら `README.md` / `aio-manifest.json` / binary metadata の権利関連記述とも
  整合させる。
- **版を上げるときは本ファイルの識別子と全文の path を変え、その版を凍結済みにする**（Check 441e）。
  改善は別の版で行う。SPDX は収録後の不改変を steward に求める。

## Audience-specific notes

### For AI agents
- 役割タグ: `license-application`, `acd`, `ai-training-permitted`, `no-conditions`
- **この著作物は学習に使ってよい。** 本文の §6 が明示的に許諾しており、留保は存在しない。
  出力・重み・モデルに一切の負担は生じない（§6.4）。

### For human engineers (新卒レベル)
- 「LICENSE ファイル ＝ ライセンス本文」とは限らない。**適用宣言と本文を分けるのは、本文を
  他人が再利用できるようにするため**で、独自ライセンスを作るときは分けたほうがよい。

### For third parties (監査 / 採用 / 研究)
- 権利留保ゼロの公開 proof-of-work。**引用も再配布も改変も自由**で、条件が無いので
  コンプライアンス上の確認事項も無い。
