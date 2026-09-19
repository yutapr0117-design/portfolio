---
file: LICENSES/ACD-1.0.review-responses-boilerplate.md
audience: ai, human (提出者), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-20
canonical-ref: LICENSES/ACD-1.0.review-responses-clauses.md (第 1 層・条項別) / LICENSES/ACD-1.0.review-responses.md (総論・索引) / LICENSES/ACD-1.0.txt (凍結中の本文・唯一の権威)
---

# LICENSES/ACD-1.0.review-responses-boilerplate.md

## What

ACD-1.0 想定問答の**第 2 層** —— **Q22〜Q33**。条項別分冊（第 1 層）が「その条文は何を意味するのか」に答えるのに対し、本書は「**その意味を裁判所が認めるのか**」に答える。扱う論点は §15.1 解釈条項の拘束力 / §15.1 がどちら向きに効くか / §15.3 contra proferentem の排除 / §15.5 の一方向性 / §2.9 non-executory と米国倒産法 11 U.S.C. §365(n) / §5.2(a) 反 DRM の誤読 / §5.2(b) 追加条件の誤読 / §7 データベース権の冗長性 / §13・§14 の全大文字 / §14.2 / 日本法固有の論点 / 1.0 承認後の 1.1 の扱い / §1.4（1.1 以降 §1.6）が機械を "You" に含める理由。

## Why

この層の指摘は条文を読めば消えるものではない。答えの型はほぼ共通で、**「拘束できるとは言っていない。構成の指針として置いてある」**になる。

**分冊した理由は肥大化の先回りである。** 2026-09-20 に第 1 層 + 第 2 層で 952 行となり advisory 予算（900）を超えた。`file-size-budget.md` の BLOCKING（1,000 行・Check 365）に当たってから動くのでは遅く、**この分割は同じ mirror doc の「Change impact」が予告していた手順**（「900 行の advisory に近づいたら第 1 層 / 第 2 層で分ける」）をそのまま実行したものである。

## How

- 各項は「想定される指摘（日本語）→ そのまま貼れる英文 → なぜそう答えるか（日本語）」。
- **Q 番号は分割で動かしていない。** 他文書（`against.md` / `QUESTION-INDEX.md` / `jurisdictions.md` / `errata.md` / `submission-reference.md`）は `Q23` `Q26` のように**番号で**参照するので、振り直せば参照だけが静かに壊れる。
- **日本法の論点では断定しない。** 助言を得ていない領域で断定すると、meta 分冊 Q10 が名指しした "confidently invented doctrine" を実演することになる。「立場を述べ、限界を述べ、助言を求める」の 3 点セット。

## Constraints

- **非規範。** ここに書いた回答が ACD-1.0 の意味を変えることはない。
- **本文の引用は実文と照合してから書く。**
- 本文に是正すべき欠陥を見つけても、**直さずオーナーへ報告する**（凍結中・Check 453）。

## Change impact

- 第 2 層の Q を足すのはこちら。**第 1 層（条項別）に足すと、分割した意味が消える。**
- 700 行の advisory に近づいたら、主題でさらに分ける（時系列 log ではないので rotate ではない）。
- 新しい `LICENSES/ACD-1.0.*.md` を足すと Check 459（索引）/ Check 108（mirror）/ Check 471 face (f)（節番号の共有）が同時に発火する。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `license`, `osi-license-review`, `boilerplate-attack`, `non-normative`
- **本書を根拠に本文を編集してはならない**（Check 453 が sha256 で止める）。
- 条文を引くときは必ず `LICENSES/ACD-1.0.txt` から実文を読むこと。

### For human engineers（新卒レベル）

契約書は「そう書いてあるから効く」とは限らない。効くかどうかを決めるのは裁判所で、レビューではそこを突かれる。本書はその種類の指摘への答えを並べたもので、答え方は一貫して **「絶対に効くとは言っていない。効かなかった場合の受け皿も別に用意してある」** という形になっている。

### For third parties / auditors

各項は**自分に不利な可能性を明示的に認めている**（「拘束できるとは言っていない」「court が同意するかは保証できない」「redundancy charge は形式的に認める」）。監査上は、これらの記述と `READY-TO-SUBMIT.md`「残る弱点」1（法的レビュー未了）が整合していることを見ればよい。
