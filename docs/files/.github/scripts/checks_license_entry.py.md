---
file: .github/scripts/checks_license_entry.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-26
canonical-ref: .github/scripts/checks_license_submission.py (Check 472 の本体) / docs/architecture/check-repository-consistency-map.md (472)
---

# .github/scripts/checks_license_entry.py

## What

審査者が最初に開く入口の面が、原文と提出対象に合うかを見る Check 472 の下位部（472l〜472p）だけを持つ split module。472l = OSI の FAQ として引く文が保存した本文に在る、472m = 入口の短い経路の表の語数、472n = 入口の斜体の引用が原文か確認済みの hash で解決する、472o = 送る材料が述べる版が提出対象、472p = 添付の本文の欄が再現のコマンドの出力と一致。

## Why

`checks_license_references.py` が advisory の 600 行を越えた（678 行）。そちらは「参照は解決する」の 1 つの invariant を持ち、入口の面の下位部は別の面なので分けた。本文は無改変で移した。

## How (usage)

```bash
python3 .github/scripts/check_repository_consistency.py
```

## Constraints

- 番号の inventory は Check 472 の本体（`checks_license_submission.py`）が持つ。ここは下位部だけ。

## Change impact

入口（`REVIEWERS.md`）・材料（`ACD-1.0.submission.md` §A・§B.0）・objection-map の形を変えたら、ここの読み方も見直す。

## Audience-specific notes

- **新卒**: 472l〜472p の失敗の文はここから出る。
- **監査人**: 分けた日の consistency の OK の行の集合は、分ける前と同じ（PR の本文に照合を書く）。
- **エンジニア**: `_h472p` は関数の中で import する（元のまま）。

## Touch points

`LICENSES/REVIEWERS.md` / `LICENSES/ACD-1.0.submission.md` / `LICENSES/ACD-1.0.objection-map.md` / `LICENSES/rounds/`

## Related

- `.github/scripts/checks_license_references.py`
- `.github/scripts/checks_license_submission.py`
