---
file: LICENSES/BLIND-SPOTS-LOG.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-23
canonical-ref: LICENSES/BLIND-SPOTS.md (方法論の本体・上位) / LICENSES/README.md (索引) / docs/architecture/file-size-budget.md (§2 / §4)
---

# LICENSES/BLIND-SPOTS-LOG.md

## What

**`BLIND-SPOTS.md` の適用の日次ログ** ——いつ、どの次元を使い、何が出たかの記録。
2026-09-10 / 09-20 / 09-22（前半・後半）の 4 節を収める。

## Why

**2026-09-23 に `BLIND-SPOTS.md` が Check 365 の 1,000 行上限に当たったため。**
**圧縮して黙らせるのではなく、テーマで割った。**

**分ける基準は「伸びるか」である** ——日次ログは増分ごとに必ず伸びるが、方法論は伸びない。
**伸び続ける側を出した。**

## How

4 節を丸ごと移し、本体には**指すだけ**の節を残した（**本体側に中身を写していない**
——写すと 2 箇所が drift する）。

## Constraints

- **一般形は本体へ書く。** この file に新しい節を足すときは、
  `BLIND-SPOTS.md` の方法論側に一般形が要るかを先に考えること。
  **日付の下に埋めた一般形は、次のセッションから見えない。**
- **advisory 900 / BLOCKING 1,000**（Check 52 / 365）。越えたら**また同じ基準で割る**。

## Change impact

- 新しい日次節はこちらへ。**`LICENSES/README.md` の索引に載っている**（Check 459）。
- 行数を変えたら `file-size-budget.md` §2 の実測行数も同じ commit で（Check 424）。

## Audience-specific notes

- **AI（実装者）**: 「まだ使っていない次元」を探すときは**本体**を読む。
  ここは**何を既に使ったか**の記録である。
- **監査人**: 分割前の履歴は `git log --follow` で `BLIND-SPOTS.md` 側に続く。
