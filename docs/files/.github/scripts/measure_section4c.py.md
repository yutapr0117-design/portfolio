---
file: .github/scripts/measure_section4c.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-01
canonical-ref: LICENSES/ACD-1.0.submission-reference.md (§4c の表) / LICENSES/ACD-1.1-CHANGELIST.md (§0.13 確定手順) / .github/scripts/checks_license_self_reporting.py (Check 460 face (n))
---

# .github/scripts/measure_section4c.py

## What

**提出パケット §4c の「機械で確かめたこと」を、任意の版について測り直す道具。** 定義語（数・未使用 0・最少使用回数）、
節の連番、非 ASCII バイト、内部 `Section N.M` 参照の解決、authoritative language の条、本文の `shall` / `must`、
条数と語数、記述子の `clause` の解決を 1 回で出す。

## Why

§4c は「弁護士が読んでいない」への答えで、**後継版も同じ機械監査を通る**ことを 1 行で主張する。その行は版を
確定するたびに手で測り直していた。Check 460 face (n) は §4c の数値を 1.0 についてだけ強制するので、出す版の
値を確定日に 1 コマンドで得る経路が要った（portfolio-25 の依頼・2026-11-01）。

## How

```sh
python3 .github/scripts/measure_section4c.py        # 現行草案（導出）
python3 .github/scripts/measure_section4c.py 1.3    # 版を指定
```

1.0 で回すと §4c の記録値（定義語 10・最少 3 回 = Contribution と Machine-Generated Material・節 16・非 ASCII 0・
§15.8・記述子 33/33）と一致する —— 道具の較正はこれで取った。

## Constraints

- **Check ではない**。1.0 の値は Check 460 (n) / 441b / 441d が強制している。
- 本文は区切り線（`-` × 80）より後。草案の状態ブロックは本文に数えない（語数は本文と file 全体の両方を出す）。
- authoritative language は「authoritative」の語で決める（English + translation で探すと §16 の翻訳の文を拾った）。

## Change impact

§4c に行を足したら、ここにも測る項目を足す。出力の件数は版で変わるので、この doc には書かない。

## Audience-specific notes

- **AI**: 版確定の日に回し、§4c の「successor」行を出力で書き換える。
- **監査人**: 1.0 で回して記録値と一致することが、道具自体の検証になる。
