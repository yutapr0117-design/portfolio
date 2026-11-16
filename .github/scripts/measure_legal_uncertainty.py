#!/usr/bin/env python3
"""measure_legal_uncertainty.py — 草案の法的解釈の不確実性の台帳: 節ごとに開いている法的な問いを数え、基準線からの増減を出す。

**なぜ在るか (2026-11-16)**: オーナーの依頼「ACD-1.4-DRAFT.txt の法的解釈の不確実性を『５人』で減らし続けてください」。
「減らし続ける」の進み具合を数で言えるように、5 人で決めた台帳 (2f の案に 30 と 50 が重ねた) を道具にした。

**数えるもの** (節 = 草案の第 1〜16 節。§12.1 to §12.5 のような範囲は節に畳む):
  Q  `QUESTIONS-FOR-COUNSEL.md` の問い (`## N. … (§…)` の見出しが名指す節)
  P  `QUESTIONS-FOR-PRACTITIONERS.md` の問い (同じ形)
  J  `ACD-1.0.jurisdictions*.md` (分けた先も) の「**確立していないこと**」の段 (段の中の § か、無ければ直前の「本文の手当て」の段の §)
  E  `ACD-1.0.errata.md` の開いている行 (「N.M 草案で閉じた」の印が無い行・2 列目の §)
  R  `ACD-1.4-THIRD-CLARITY-TRIAL.md` §18 の記録の行 (下の形)。①②③ と状態ごとに数える

**§18 の記録の行の形** (2 つの形を読む。50 の §18.3 と 1c の §18.1 が先に表の形を使った):
    | §14.1 *"…"* | <頼っている法の命題> | <当て・法源は rounds/<file>> | **②** … |
  表の形では、分類の欄 (最後の欄) の最初の ①②③ を読み、行に rounds/ の file 名が在れば「狭まった」に数える。行の形:
    - §14.1 | 命題: <その条が頼る法の命題> | ② | 状態: 出典あり | 法源: rounds/<file>
  ① どこでも真 (記録だけ) / ② 語を変えれば法域に依らなくできる (試作の種) / ③ 語では消せない (法律家への問いか jurisdictions へ)
  状態: 出典なし / 出典あり (法源の rounds/ の file が在る) / 本文で消えた (試作で命題が要らなくなった) / 法律家のみ
  「狭まった」= 状態が「出典あり」か「本文で消えた」。出典ありの行の法源が rounds/ に無ければ誤りとして出す。

**基準線**: `LICENSES/LEGAL-UNCERTAINTY.md` の BASELINE-DATA。`--pin` で今日の数を書き込む (書き換えは人が決めた日だけ)。
使い方:
    python3 .github/scripts/measure_legal_uncertainty.py          # 節ごとの表と、基準線からの増減
    python3 .github/scripts/measure_legal_uncertainty.py --pin    # 今日の数を基準線にする
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"
LEDGER = L / "LEGAL-UNCERTAINTY.md"
ROW = re.compile(r"^- §(\d+(?:\.\d+)?(?:\([a-z]\))?) \| 命題: (.+?) \| ([①②③]) \| 状態: (出典なし|出典あり|本文で消えた|法律家のみ)"
                 r"(?: \| 法源: (\S+))?\s*$", re.M)
KEYS = ("Q", "P", "J", "E", "R", "R①", "R②", "R③", "狭まった")


def sections(text: str) -> set[int]:
    """§ の参照を節番号の集合に畳む。"§12.1 to §12.5" と "Sections 3 to 8" は範囲として広げる。"""
    out = set()
    for a, b in re.findall(r"§\s?(\d+)(?:\.\d+)?(?:\([a-z]\))?\s*(?:to|〜|–|-)\s*§?\s?(\d+)", text):
        out |= set(range(int(a), int(b) + 1))
    out |= {int(n) for n in re.findall(r"§\s?(\d+)", text)}
    return {n for n in out if 1 <= n <= 16}


def count() -> tuple[dict[int, Counter], list[str]]:
    by: dict[int, Counter] = defaultdict(Counter)
    errs = []
    for fname, key in (("QUESTIONS-FOR-COUNSEL.md", "Q"), ("QUESTIONS-FOR-PRACTITIONERS.md", "P")):
        for h in re.findall(r"^## \d+\. .*$", (L / fname).read_text(encoding="utf-8"), re.M):
            for n in sections(h):
                by[n][key] += 1
    # jurisdictions は分けることがある (2026-11-16・30 が §9 / §9a を別ファイルへ移す相談)。分けた先も読む。ファイルごとに
    #   「本文の手当て」の段を引き継がない (分けた先の最初の「確立していない」が、元のファイルの最後の手当てを借りないように)
    paras = []
    for jf in sorted(L.glob("ACD-1.0.jurisdictions*.md")):
        paras += [""] + re.split(r"\n\s*\n", jf.read_text(encoding="utf-8"))
    last_fix = ""
    for p in paras:
        if p == "":
            last_fix = ""
            continue
        if "**本文の手当て**" in p:
            last_fix = p
        if "**確立していないこと**" in p:
            for n in (sections(p) or sections(last_fix)):
                by[n]["J"] += 1
    for line in (L / "ACD-1.0.errata.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|([^|]*)\|", line)
        if m and not re.search(r"\d+\.\d+ 草案で閉じた", line):
            for n in sections(m.group(2)):
                by[n]["E"] += 1
    third = L / "ACD-1.4-THIRD-CLARITY-TRIAL.md"
    t = third.read_text(encoding="utf-8") if third.exists() else ""
    s18 = re.search(r"^## (?:§)?18[ .].*?(?=^## (?:§)?\d+[ .]|\Z)", t, re.M | re.S)
    body18 = s18.group(0) if s18 else ""
    for m in ROW.finditer(body18):
        n = int(m.group(1).split(".")[0].split("(")[0])
        by[n]["R"] += 1
        by[n]["R" + m.group(3)] += 1
        if m.group(4) in ("出典あり", "本文で消えた"):
            by[n]["狭まった"] += 1
        if m.group(4) == "出典あり" and not (m.group(5) and (ROOT / "LICENSES" / m.group(5)).exists()):
            errs.append(f"§{m.group(1)} は「出典あり」だが法源の file が LICENSES/ の下に無い: {m.group(5)}")
    # 表の形 (50 の §18.3 と 1c の §18.1 が先に使った形・2026-11-16): `| §N.M … | 命題 | 当て | 分類 |`。分類の欄 (最後の欄)
    #   の最初の ①②③ を読み、行に rounds/ の file 名が在れば「狭まった」に数え、その file が無ければ ⚠。並べた条は最初の条の節に数える
    for line in body18.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("| §") else []
        cls = re.search(r"[①②③]", cells[-1]) if len(cells) >= 3 else None
        sec = re.match(r"§(\d+)", cells[0]) if cells else None
        if not (cls and sec):
            continue
        n = int(sec.group(1))
        by[n]["R"] += 1
        by[n]["R" + cls.group(0)] += 1
        srcs = re.findall(r"rounds/[\w.\-]+\.txt", line)
        if srcs:
            by[n]["狭まった"] += 1
            errs += [f"{cells[0][:30]} の法源の file が LICENSES/ の下に無い: {s}" for s in srcs if not (L / s).exists()]
    return by, errs


def baseline() -> dict[int, dict[str, int]]:
    if not LEDGER.exists():
        return {}
    m = re.search(r"<!-- BASELINE-DATA\n(.*?)-->", LEDGER.read_text(encoding="utf-8"), re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        f = line.split()
        if f and f[0].isdigit():
            out[int(f[0])] = dict(zip(KEYS, map(int, f[1:])))
    return out


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    by, errs = count()
    base = baseline()
    print("| 節 | " + " | ".join(KEYS) + " | 基準線からの増減 (Q+P+J+E) |")
    print("| :-- | " + " | ".join("--:" for _ in KEYS) + " | :-- |")
    tot, btot = Counter(), Counter()
    for n in range(1, 17):
        c = by.get(n, Counter())
        tot.update(c)
        b = base.get(n, {})
        btot.update(b)
        now, was = sum(c[k] for k in "QPJE"), sum(b.get(k, 0) for k in "QPJE")
        d = "" if not base else (f"{now - was:+d}" if now != was else "±0")
        print(f"| §{n} | " + " | ".join(str(c[k]) for k in KEYS) + f" | {d} |")
    now, was = sum(tot[k] for k in "QPJE"), sum(btot.get(k, 0) for k in "QPJE")
    print(f"| 計 | " + " | ".join(str(tot[k]) for k in KEYS) + f" | {'' if not base else f'{now - was:+d}'} |")
    print(f"\n# 開いている法的な問い (Q+P+J+E・節ごとに数えるので、2 つの節を名指す問いは 2 と数える): {now}"
          + (f"（基準線 {was}）" if base else "（基準線なし・--pin で今日の数を基準線にする）"))
    print(f"# §18 の記録: {tot['R']} 行 (① {tot['R①']} / ② {tot['R②']} / ③ {tot['R③']})・狭まった {tot['狭まった']}")
    for e in errs:
        print(f"# ⚠ {e}")
    if "--pin" in argv:
        block = "\n".join(f"{n} " + " ".join(str(by.get(n, Counter())[k]) for k in KEYS) for n in range(1, 17))
        text = LEDGER.read_text(encoding="utf-8")
        new = re.sub(r"<!-- BASELINE-DATA\n.*?-->", lambda _m: f"<!-- BASELINE-DATA\n{block}\n-->", text, flags=re.S)
        LEDGER.write_text(new, encoding="utf-8")
        print("# 基準線を書き込んだ")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
