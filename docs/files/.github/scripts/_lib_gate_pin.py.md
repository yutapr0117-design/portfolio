---
file: .github/scripts/_lib_gate_pin.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-25
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md (合議の記録・議題 29 / 31) / docs/architecture/check-repository-consistency-map.md (504)
---

# .github/scripts/_lib_gate_pin.py

## What

門の固定の印を読み、いまの草案の本文・変更の一覧・門の文・指示文の sha と照らす関数（Check 504・確定の道具・`moved_clauses.py --pin` が共有）。

## Why

CI は浅い履歴なので sha の一致だけを見て、日数・結果・git の履歴は確定の道具が見る。同じ読み方を 2 か所に持つと食い違う。

## How (usage)

```bash
python3 .github/scripts/moved_clauses.py --pin          # 動かしたら印を書き直す（since は今日 = 数え直し）
python3 .github/scripts/check_repository_consistency.py # Check 504
```

## Constraints

- 門の文は 8 つの句（結果を見た後に選んだ門・落ちたら・1.4 のまま・3 つ目の門は作らない・1 回だけ・PARTLY LISTED・全員一致・別の agent）を持つ。
- 印（GATE-PIN）と結果（GATE-RESULT）は 1 個ずつ。結果が在れば数え直せない。

## Change impact

草案の本文か変更の一覧を動かす PR は、門を置いた版では印も動かす。確定の道具は、日数が残る・結果が無い・落ちた・履歴が動いた、のどれかで止まる。

## Audience-specific notes

- **新卒**: 門は GATE.md が在る版だけで働く。
- **監査人**: 数え直しは差分に必ず出る。印の since だけを昔へ書き換える形は、確定の道具が git の履歴で見る。
- **エンジニア**: 日付は UTC。履歴は author の日で見る（rebase merge は committer の日を替える）。

## Touch points

`LICENSES/ACD-*-GATE.md`・`LICENSES/ACD-*-DRAFT.txt`・`LICENSES/CHANGES-ACD-*.txt`。

## Related

- `.github/scripts/moved_clauses.py`
- `.github/scripts/prepare_version_freeze.py`
