---
file: .github/scripts/checks_license_declaration.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-08
canonical-ref: .github/scripts/check_repository_consistency.py (CHECK_SOURCE_FILES と run 呼び出し) / LICENSE (適用宣言の単一ソース)
---

# .github/scripts/checks_license_declaration.py

## What

**Check 444**（ライセンス宣言の cross-surface coherence）だけを持つ module。`LICENSE` が名乗る適用版を単一ソースとし、rel=license / JSON-LD (静的と実行時) / aio-manifest / sitemap / robots (bot ごとの group) / llms 層の宣言の文 / 画面のフッターと README / REUSE.toml / 日付と「適用している版」の主張が、同じ版を述べることを見る。

## Why

2026-11-08 の Check の監査で 444 の面を強めた結果、元の `checks_license_surfaces.py` が 938 行になり、Check 52 の advisory 900 を超えた。444 は他の Check と変数を共有しない塊なので切り出した。

## How (usage)

`check_repository_consistency.py` が `run(_ctx)` で呼ぶ。単体では走らせない。

## Constraints

- **面の記号をエラー文に付ける**: 誤りは `444a:` のように面の記号で始まる。週次 mutation-probe はこの記号で、狙った面が発火したかを判定する
- **版を値で書かない**: 適用する版は `LICENSE` の 2 行から導く。mutation も `APPLIED_ID` から当て先を作る

## Change impact

- 新しい適用面を足したら、ここに面を足し、版を確定する道具 (`prepare_version_freeze.py` の APPLY_FILES) にも足す

## Audience-specific notes

### For AI agents
- 役割タグ: `check-module`, `license`, `machine-readable`

### For human engineers (新卒レベル)
- 「宣言が在るか」ではなく「宣言がどの版を述べるか」を見る Check の実例

### For third parties (監査 / 採用 / 研究)
- ライセンスの宣言が全ての機械可読面で食い違わないことの機械強制
