---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-machine-readable-license-and-inert-warning-layer.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: AI2AI.md / CLAUDE.md / LICENSES/ACD-1.0.txt / docs/architecture/file-size-budget.md
---

# improvement-notes — machine-readable license and inert warning layer

## What

2026-08-23 の run (PR #1266) の増分記録。3 つの発見を扱う:

1. **ライセンスが機械可読な 7 面すべてで宣言ゼロだった** —— ACD-1.0 §6.5 自身が
   「自動化システムが判定できない許諾は許諾ではない」と述べているので、
   本文が発見できない状態は**ライセンスが自分の主張を満たしていない**ことを意味した
2. **早期警告が構造的に一度も出ない file が 6 つあった** —— advisory 予算 = hard ceiling
3. **mutation anchor が一意なまま別ノードへ silent に移動していた** —— Check 362 も 420 も捕捉不能

## Why

増分の what/why は commit へ書くが、**run 全体を貫く軸**と**再利用できる教訓**は
散らばると次の AI が拾えない。AI2AI.md の Session Record を薄く保つ (Check 365 の
1,000 行制約) ため、要点は Session Record、詳細は本 doc という二層にしている。

## How (usage)

cold-start では `CLAUDE.md` §7 → `AI2AI.md` Session Record #31 → 本 doc の順に降りる。
「なぜその Check があるのか」を調べるときは Check 番号 (443 / 444) で本 doc を検索する。

## Constraints

- **Check 75**: `docs/incident-artifacts/README.md` の inventory に列挙されていること
- **Check 108**: 本 mirror doc が存在すること
- **Check 42a/42b**: 命名規約 (`improvement-notes-*.md`) と配置
- **Check 436 の対象外**: `docs/incident-artifacts/` は性質上の歴史記録なので、
  「裁可待ち」型の記述に超越注記を強制しない (履歴を濁さないための線引き)

## Change impact

- 本 doc は**歴史記録**なので、後から実態が変わっても書き換えない。訂正が要る場合は
  新しい run の notes で「この記述は後に反証された」と述べる (#977 / #1245 と同じ扱い)。

## Audience-specific notes

### For AI agents
- 役割タグ: `improvement-notes`, `machine-readable-license`, `advisory-layer`, `mutation-anchor`
- 再利用できる教訓は §5 に集約してある。とくに **「mutation が anchor する file を編集したら
  その場で probe を回せ」** は、静的 Check では原理的に代替できない。

### For human engineers (新卒レベル)
- 「宣言を数え上げて、それぞれに見ている層があるかを突き合わせる」という棚卸しの手法は、
  この run だけで 7 つの穴を出した。汎用性が高い。

### For third parties
- AI 実装が**自分のゲートの欠陥を自分で見つけて直す**過程の記録。Check 443 の初版が
  正しい設定を誤検出し、それを非 vacuity 検証で発見して射程を狭めた経緯を含む。
