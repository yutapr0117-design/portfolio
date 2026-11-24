---
file: LICENSES/ACD-1.5-GATE.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-25
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md (合議の記録) / .github/scripts/_lib_gate_pin.py (Check 504)
---

# LICENSES/ACD-1.5-GATE.md

## What

出す版を 1.4 から 1.5 へ替える前の最後の門。門の文・読み手へ渡す指示文・固定の印・読みの結果（1 回だけ）を持つ。

## Why

1.5 の書き直しでは、読むたびに欠陥が出て、門の言い換えも 1 度した（議題 24・`against.md` #332）。結果を見てから基準を動かせないように、次の読みの前に基準・指示文・本文・一覧を固定し、動かせば日数を数え直す。

## How (usage)

```bash
python3 .github/scripts/moved_clauses.py --pin   # 固定する・動かしたら数え直す
```

## Constraints

- 門の文の 8 つの句は Check 504 が必須にする。印と結果は 1 個ずつ。
- 読みの結果が在れば数え直せない。

## Change impact

草案の本文か `CHANGES-ACD-1.5.txt` を動かす PR は、印も動かす（動かさないと Check 504 が RED）。

## Audience-specific notes

- **新卒**: pending の間は日数を数えていない。
- **監査人**: 落ちた門の後、1.5 は草案として残り、3 つ目の門は作らない。
- **エンジニア**: 日数・結果・履歴は `prepare_version_freeze.py` が見る。

## Touch points

`.github/scripts/_lib_gate_pin.py` / `.github/scripts/prepare_version_freeze.py` / `LICENSES/ACD-1.5-DRAFT.txt` / `LICENSES/CHANGES-ACD-1.5.txt`

## Related

- `LICENSES/ACD-1.5-CHANGELIST.md`
- `LICENSES/ACD-1.0.against.md`（#332）
