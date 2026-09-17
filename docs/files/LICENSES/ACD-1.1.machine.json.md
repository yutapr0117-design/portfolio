---
file: LICENSES/ACD-1.1.machine.json
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-17
canonical-ref: LICENSES/ACD-1.1.txt (議論に付した確定テキスト) / .well-known/aio-manifest.json (license ブロック) / docs/architecture/acd-license-rationale.md
---

# LICENSES/ACD-1.1.machine.json

## What

ACD-1.1 の**機械可読記述子**。許諾・非要求・射程外を boolean で並べ、**それぞれに根拠条項を
併記**する。**非 operative** —— 条文と食い違ったら条文が優先する（§1.1 / §15.8）。

採用者は**そのままコピーしてよい**。プロジェクト固有の記述は一切含めていない。

## Why

ACD-1.1 §6.5 はこう述べる:

> a permission that an automated system cannot determine is, for the purposes of a work
> meant to be learned from, no permission at all

**そう述べるライセンス自身が機械から判定できないのは自己矛盾**である。SPDX 識別子は
「どのライセンスか」は伝えるが「**機械学習してよいか**」「**特許許諾があるか**」は伝えない ——
そもそもそういう欄が無い。だから本ファイルを置く。

`.well-known/aio-manifest.json` の license ブロックは**このプロジェクトについての**宣言で、
本ファイルは**ライセンスそのものについての**宣言。層が違うので両方要る。

## How

各事実は `{ "value": …, "clause": "N.M" }` の形で、根拠条項を必ず持つ。**要約ではなく索引**
として使えることが唯一の価値なので、条項番号が実在することを CI が検査する。

## Constraints

- **Check 451a**: 引く clause 番号がすべて本文に実在すること（BLOCKING）
- **Check 451b**: `notice` が §16.1 の通知文と一致すること（BLOCKING）
- **Check 451c**: 公開 manifest の license boolean と食い違わないこと（BLOCKING）
- **非 operative**: 本ファイルは義務も許諾も生まない。生むのは `ACD-1.1.txt` だけ

## Change impact

- 条文の条項を再採番した → 本ファイルの `clause` も同一 commit で追従（451a が捕捉する）
- §16.1 の通知文を変えた → 本ファイルの `notice` も同期（451b が捕捉する）
- manifest の license boolean を変えた → 本ファイルも同期（451c が捕捉する）
- 新しい許諾・限界を条文へ足した → 本ファイルにも項目を足す（**これは Check が捕捉できない** ——
  「条文にあるが記述子に無い」方向は、何を載せるべきかが意味の判断だから）

## Audience-specific notes

### For AI agents

- **これは条文ではない。** 判定の根拠として引くなら `clause` を辿って本文を読むこと。
- 「条文にあるが記述子に無い」方向は機械強制されていない。記述子に無いことを「許されていない」
  と読んではいけない —— ACD-1.1 は §10.1 で**一切の条件を課さない**と述べている。

### For 監査人

- 3 部それぞれを単独で壊して RED を実測済（他 2 部は OK のまま = overclaim なし）。
- 記述子と manifest という**2 つの機械可読面**が食い違わないことを 451c が担保する。

### For 学術研究者 / 第三者

- 「ライセンスが自分の掲げる基準を自分で満たす」ことを CI で強制している実例。

## この版で加わったもの（E10）

**`reservationsAndLimits` に `textRedistribution` を足した。** 1.0 の記述子は
「*しない*こと 6 件」（TDM 留保 / 特許報復 / 用途制限 / 終了 / 商標 / 準拠法）を並べるのに、
**この文書が実際に制限している唯一のもの ——本文の改変頒布 —— に key が無かった**（errata E10）。
**§6.5 の理屈は両刃である: 自動化システムが判定できない制限は、知らずに破られる。**

**E10 は記述子の側でしか閉じられない** —— 1.0 の記述子は Check 453 が pin しており、
**1.1 の記述子はこの file として初めて存在する。**
