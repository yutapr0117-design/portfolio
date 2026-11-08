---
file: .github/scripts/mutation_samples_archive6.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-08
canonical-ref: .github/scripts/mutation_samples.py (hot log・新規はここへ足す) / .github/scripts/rotate_mutation_samples.py (rotate ツール) / docs/architecture/file-size-budget.md (行数予算)
---

# .github/scripts/mutation_samples_archive6.py

## What

consistency 側 mutation の **4 番目の archive**（退避先）。`MUTATIONS_ARCHIVE6` を定義し、`mutation_samples.py` が import して `MUTATIONS` へ連結する。

**新しい mutation はここへ足さない。** 追加先は常に `mutation_samples.py` の tail（`_MUTATIONS_TAIL.append(...)`）で、ここは rotate が押し出した古い entry の置き場である。

## Why

mutation は append-only で増え続けるため、hot log は放置すると Check 365 の 1,000 行 BLOCKING に当たる。`rotate_mutation_samples.py` が advisory を跨いだ時点で最古の entry を archive へ移す。archive 自身も無限には伸ばせないので、埋まったら次の番号を起こす ―― 本ファイルはその 4 本目（2026-11-04 に自動生成）。

**きっかけ**: 同日、Check 460 / 469 の face と Check の下位部を名指す mutation を大量に足した（Check 479c / 479d）。粒度を 1 段細かくして「名指した層が赤くなったか」で数えると、mutation の数は面・下位部の数に比例して増える。

## How

- 構造は最小限（docstring + `from mutation_samples_common import ROOT` + list）。
- `mutation_samples.py` 側に `from mutation_samples_archive4 import MUTATIONS_ARCHIVE6` と連結式への追加が**同時に**行われる（片方だけだと総数が減り、rotate の不変条件チェックが落ちる）。
- rebalance（`REBALANCE_TARGET` 950）の対象でもあり、溢れたら次の archive へ末尾から押し出される。chain は **disk から導出**されるので、本ファイルは追加した時点で自動的に対象に入る。

## Constraints

- **編集は rotate 時のみ。** 手で entry を足さない。
- advisory 予算は hard ceiling（1,000）未満に保つ（Check 443）。危険域（>800 行）に入ったら BUDGET-DATA への登録が必須（Check 454）。
- `Check 430` が「連結式より後の append は死ぬ」を守るので、連結式との前後関係を崩さない。

## Change impact

- 本ファイルが 950 行に近づいたら、rotate が `mutation_samples_archive6.py` を自動生成して配線する。**手で作る必要は無い。**
- 行数が変わったら §2 実測行数の同期が要る（Check 424）が、これも rotate ツールが自分で行う。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `mutation-data`, `archive`, `rotate-target`, `auto-generated`
- **ここへ直接 append しない。** 規約は「新規は hot log の tail」。破ると時系列順が壊れ、rotate の「最古から押し出す」前提が崩れる。
- 本ファイルの存在自体が「consistency 側の archive が 2 本では足りなくなった」という事実の記録である。

### For human engineers（新卒レベル）

テストの安全網を検証するための「わざと壊すパターン集」が増え続けるので、古いものを別ファイルへ移して 1 ファイルが大きくなりすぎないようにしている。その 3 冊目。移動は専用ツールが行い、人もエージェントも手では動かさない。

### For third parties / auditors

自動生成物であり、内容は既存 entry の移動のみ（新規の意味的追加はない）。移動の前後で mutation 総数が変わらないことを rotate ツールが `importlib` で検証しており、その不変条件が破れれば ツールが `SystemExit` で止まる。

**2026-11-08 新設**: archive5 が受け皿の余裕を失ったので、rotate ツールが自動で起こした 6 つ目の退避先。共有定数は `mutation_samples_common.py` の名前から導出して全部 import する (それまで雛形は 5 つの名前の決め打ちで、`APPLIED_ID` を使う entry を移そうとして NameError で止まった)。
