---
file: .github/scripts/probe_scope.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-04
canonical-ref: .github/scripts/mutation_probe.py (使う側) / .github/scripts/check_repository_consistency.py (import する側) / .github/workflows/mutation-probe.yml (所要の記録)
---

# .github/scripts/probe_scope.py

## What

mutation-probe が consistency gate を「名指した Check の module だけ」で走らせるための import hook。環境変数 `CHECK_ONLY_MODULE` があるときだけ、それ以外の `checks_*` module の `run` を何もしない関数へ差し替える（module 自体は import されるので、他 module が使う helper は残る）。値が `__monolith__` なら、すべての module の `run` を空にする。

## Why

probe は mutation 1 件ごとに gate 全体（約 60 module）を走らせていた。2026-11-03 の実 CI で 1 件 10.3 秒・shard あたり 25.7 分となり、timeout 30 分に対する余裕が 1.17 倍まで縮んだ。`mutation-probe.yml` は 2026-09-29 に「余裕が 1.5 倍を切ったら、分割ではなく gate 全体を走らせる構造を見直す」と記録していた（1 件あたりの所要は Check が増えるたびに伸び、分割では止まらない）。帰属は 2026-09-29 から「名指した Check が発火したか」で決まるので、まずその module だけで走らせる。ローカル実測で gate 1 回が 5.81 秒 → 0.23 秒。

## How

- `check_repository_consistency.py` が冒頭で `import probe_scope` する。**環境変数が無ければ何もしない**ので、通常の verify / CI の挙動は不変。
- `mutation_probe.py` の consistency ループは、`module_of_check()` で名指した Check の module を引き、`run_gate(only=…)` で走らせる。名指しどおり捕捉されればそれで決まり、捕捉されなかったときだけ gate 全体で走らせ直して従来どおり分類する（SURVIVED / MISATTRIBUTED / CRASHED の判定は変わらない）。

## Constraints

- 通常の gate で `CHECK_ONLY_MODULE` を設定しないこと（設定すると大半の Check が走らない）。
- 速い経路は「捕捉された」ことにしか使わない。捕捉されないときの結論は必ず gate 全体で出す。

## Change impact

- module の命名規則（`checks_*.py`）や、monolith が module を import して `run(_ctx)` を呼ぶ形を変えると、この hook は効かなくなる。効かなくても速い経路が外れるだけで、判定は gate 全体の走らせ直しで正しく出る。

## Audience-specific notes

- **AI**: probe の所要が timeout に近づいたら、まず速い経路が実際に使われているか（ログの所要）を確かめる。
