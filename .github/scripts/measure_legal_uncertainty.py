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
  表の形では、分類の欄 (最後の欄) の最初の ①②③ を読み、行に rounds/ の file 名が在るか、分類の欄に「T84 で入った」
  「本文で消えた」と書いてあれば「狭まった」に数える。§19 (語の割れ) の数え方は section19() の docstring。行の形:
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
KEYS = ("Q", "P", "J", "E", "R", "R①", "R②", "R③", "狭まった", "J出典")  # J出典 は末尾に足した (基準線の列の位置を変えない)


def sections(text: str) -> set[int]:
    """§ の参照を節番号の集合に畳む。"§12.1 to §12.5" と "Sections 3 to 8" は範囲として広げる。"""
    out = set()
    for a, b in re.findall(r"§\s?(\d+)(?:\.\d+)?(?:\([a-z]\))?\s*(?:to|〜|–|-)\s*§?\s?(\d+)", text):
        out |= set(range(int(a), int(b) + 1))
    out |= {int(n) for n in re.findall(r"§\s?(\d+)", text)}
    return {n for n in out if 1 <= n <= 16}


SNIP: dict[str, str] = {}  # 鍵 → 段の先頭 (表示だけに使う・比べるのは鍵)


def open_items(read) -> set[tuple[str, int, str]]:
    """開いている法的な問い Q / P / J / E を (種類, 節, 鍵) の集合で返す。read(相対 path) は本文 (無ければ "")。
    鍵: Q/P は見出しの文、J は段の先頭 60 字、E は errata の番号。基準線の後に足した問いと消えた問いを分けるため (2f の依頼)。"""
    items = set()
    for fname, key in (("QUESTIONS-FOR-COUNSEL.md", "Q"), ("QUESTIONS-FOR-PRACTITIONERS.md", "P")):
        # 鍵は問いの番号 (見出しの文にすると、見出しに § を足しただけで「消えた + 足された」と出た・2026-11-16 の問い 1)
        for num, h in re.findall(r"^## (\d+)\. (.*)$", read(fname), re.M):
            items |= {(key, n, f"{key}{num}") for n in sections(h)}
    jfiles = sorted({"ACD-1.0.jurisdictions.md"} | {p.name for p in L.glob("ACD-1.0.jurisdictions*.md")})
    for jf in jfiles:
        last_fix, head, nth = "", "", 0
        for p in re.split(r"\n\s*\n", read(jf)):
            # 鍵は「ファイル・直前の見出し・その見出しの下で何番目の段か」(2026-11-17): 段の文の先頭を鍵にすると、30 が法源で
            #   段を狭めて書き換えたとき、同じ段が「消えた + 足された」と出た
            hm = re.match(r"#{2,4} (.+)", p.strip())
            if hm:
                head, nth = hm.group(1)[:40], 0
            if "**本文の手当て**" in p:
                last_fix = p
            if "**確立していないこと**" in p:
                nth += 1
                k = f"{jf.replace('ACD-1.0.', '')} {head} #{nth}"
                SNIP[k] = " ".join(p.split("**確立していないこと**", 1)[1].split())[:50]
                items |= {("J", n, k) for n in (sections(p) or sections(last_fix))}
    for line in read("ACD-1.0.errata.md").splitlines():
        m = re.match(r"\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|([^|]*)\|", line)
        if m and not re.search(r"\d+\.\d+ 草案で閉じた", line):
            items |= {("E", n, m.group(1)) for n in sections(m.group(2))}
    return items


def baseline_items() -> tuple[str, set] | tuple[None, set]:
    """基準線を置いた commit (LEGAL-UNCERTAINTY.md を足した commit) の時点の開いている問い。浅い clone では None。"""
    import subprocess
    try:
        h = subprocess.run(["git", "-C", str(ROOT), "log", "--diff-filter=A", "--format=%h", "--",
                            "LICENSES/LEGAL-UNCERTAINTY.md"], capture_output=True, text=True, check=True).stdout.split()
        if not h:
            return None, set()

        def read(rel):
            r = subprocess.run(["git", "-C", str(ROOT), "show", f"{h[-1]}:LICENSES/{rel}"], capture_output=True, text=True)
            return r.stdout if r.returncode == 0 else ""
        return h[-1], open_items(read)
    except (OSError, subprocess.CalledProcessError):
        return None, set()


DEST = re.compile(r"問い ?\d+|jurisdictions|法律家|QUESTIONS|PRACTITIONERS|確立していない")
NO_DEST: list[str] = []  # ③ の行で行き先 (問い N / jurisdictions / 法律家) を書いていない行 (count() が埋める)
NO_SRC: list[str] = []   # ③ の行で法源 (rounds/) も試作の着地も無い行 —— 30 と 2f が次に取りに行く法源の一覧 (2026-11-18)


def count() -> tuple[dict[int, Counter], list[str]]:
    by: dict[int, Counter] = defaultdict(Counter)
    errs = []
    NO_DEST.clear()
    NO_SRC.clear()
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
                # 段が法源 (rounds/ の file) を挙げていれば、問いは残るが狭まった (30 の提案・2026-11-16): 件数の増えが
                #   「新しく見えた問い」か「法源で狭めた問い」かを分けて読む
                if re.search(r"rounds/[\w.\-]+\.txt", p):
                    by[n]["J出典"] += 1
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
        # ③ は語では消せないので、法律家への問いか jurisdictions の段に置かれて初めて扱える (2026-11-16)。行き先が無い ③ は
        #   第 18 節にだけ在って、台帳の Q / J に数えられない不確実性になる
        if m.group(3) == "③" and m.group(4) != "法律家のみ" and not DEST.search(m.group(0)):
            NO_DEST.append(f"§{m.group(1)}（行の形）")
        if m.group(3) == "③" and m.group(4) not in ("出典あり", "本文で消えた"):
            NO_SRC.append(f"§{m.group(1)} —— {m.group(2)[:60]}")
        if m.group(4) in ("出典あり", "本文で消えた"):
            by[n]["狭まった"] += 1
        # 法源は「・」「,」で複数つないでよい (2026-11-16・30 が §12.2・§12.4 で 3 つの file をつないだ・2f の報告)
        if m.group(4) == "出典あり":
            for src in [s for s in re.split(r"[・,、]\s*", m.group(5) or "") if s] or [""]:
                if not (src and (L / src).exists()):
                    errs.append(f"§{m.group(1)} は「出典あり」だが法源の file が LICENSES/ の下に無い: {src or '(空)'}")
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
        if cls.group(0) == "③" and not DEST.search(cells[-1]):
            NO_DEST.append(f"{cells[0][:40]}（表の形）")
        srcs = re.findall(r"rounds/[\w.\-]+\.txt", line)
        # 試作で本文が変わり、命題が要らなくなった行も「狭まった」(行の形の「本文で消えた」と同じ・2026-11-16): 分類の欄に
        #   「T84 で入った」「T84〜T88 で入った」「本文で消えた」と書く
        trial = re.search(r"T\d+(?:〜T\d+)?\s*で入った|本文で消えた", cells[-1])
        if cls.group(0) == "③" and not (srcs or trial):
            NO_SRC.append(f"{cells[0][:40]} —— {cells[1][:60] if len(cells) > 1 else ''}")
        if srcs or trial:
            by[n]["狭まった"] += 1
            errs += [f"{cells[0][:30]} の法源の file が LICENSES/ の下に無い: {s}" for s in srcs if not (L / s).exists()]
    return by, errs


ROW19 = re.compile(r"^- §(\d+(?:\.\d+)?(?:\([a-z]\))?)[^|]*\| 別の読み: (.+?) \| (一意|試作|法の側)([^|]*)\| 根拠: (.+)$", re.M)


def section19() -> tuple[Counter, list[str]]:
    """THIRD §19 (本文の語が 2 通り以上に読める所・2026-11-18 のオーナーの依頼「法的解釈が一意に定まるように」) の行を数える。
    行の形 (2f の案で 5 人が決めた): `- §x.y | 別の読み: … | 一意 / 試作 Tnn / 法の側 | 根拠: …`。
      一意   —— 他の条が既に一方に閉じている。根拠に閉じている条 (§N.M) を名指す
      試作   —— 語を変えれば定まる。T 番号を書き、本文に入ったら「Tnn で入った」、退けたら「退けた」と書く (開いている ② に当たる)
      法の側 —— 語では定まらず法が決める。根拠に問い N か §18 の行か jurisdictions を名指す
    返り値: (数, 直すべき行)。"""
    third = L / "ACD-1.4-THIRD-CLARITY-TRIAL.md"
    t = third.read_text(encoding="utf-8") if third.exists() else ""
    s19 = re.search(r"^## (?:§)?19[ .].*?(?=^## (?:§)?\d+[ .]|\Z)", t, re.M | re.S)
    c, bad = Counter(), []
    for m in ROW19.finditer(s19.group(0) if s19 else ""):
        kind, rest, why = m.group(3), m.group(4), m.group(5)
        c["行"] += 1
        c[kind] += 1
        if kind == "一意" and not re.search(r"§\d+", why):
            bad.append(f"§{m.group(1)}: 一意 だが根拠に閉じている条 (§N.M) が無い")
        if kind == "試作":
            if not re.search(r"T\d+", rest + why):
                bad.append(f"§{m.group(1)}: 試作 だが T 番号が無い")
            if re.search(r"で入った|退けた", rest + why):
                c["試作で閉じた"] += 1
            else:
                c["試作で開いている"] += 1
        if kind == "法の側" and not re.search(r"問い ?\d+|§18|jurisdictions|法律家", why):
            bad.append(f"§{m.group(1)}: 法の側 だが行き先 (問い N / §18 / jurisdictions) が無い")
    return c, bad


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
    print(f"# jurisdictions の「確立していないこと」{tot['J']} のうち、段の中に法源 (rounds/) を挙げて狭めたもの {tot['J出典']}")
    print(f"# §18 の記録: {tot['R']} 行 (① {tot['R①']} / ② {tot['R②']} / ③ {tot['R③']})・狭まった {tot['狭まった']}")
    # 基準線の後に足した問いと消えた問い (2f の依頼): 数の増減を「問いを分けた・足した」と「消えた・閉じた」に分ける
    bh, before = baseline_items()
    if bh:
        after = open_items(lambda rel: (L / rel).read_text(encoding="utf-8") if (L / rel).exists() else "")
        added, gone = sorted(after - before), sorted(before - after)
        print(f"# 基準線の commit {bh} の後に足された問い {len(added)}・消えた問い {len(gone)}（種類, 節, 鍵）")
        for x in added:
            print(f"#   + {x[0]} §{x[1]} {x[2][:50]} {SNIP.get(x[2], '')[:40]}")
        for x in gone:
            print(f"#   − {x[0]} §{x[1]} {x[2][:50]} {SNIP.get(x[2], '')[:40]}")
    print(f"# ③ の行で行き先（問い N / jurisdictions / 法律家）を書いていない行: {len(NO_DEST)}"
          "（語では消せない不確実性が第 18 節にだけ在り、台帳の Q / J に数えられない）")
    for x in NO_DEST:
        print(f"#   ・ {x}")
    print(f"# ③ の行で法源（rounds/）がまだ無い行: {len(NO_SRC)}（30 = 独・英・仏・日、2f = 米国・EU が次に取りに行く候補）")
    for x in NO_SRC:
        print(f"#   ・ {x}")
    c19, bad19 = section19()
    print(f"# §19（本文の語の割れ）: {c19['行']} 行 —— 一意 {c19['一意']} / 試作 {c19['試作']}（本文に入ったか退けた {c19['試作で閉じた']}・"
          f"開いている {c19['試作で開いている']}）/ 法の側 {c19['法の側']}。合格の線: 開いている試作 0、一意の行がすべて閉じている条を名指す")
    for x in bad19:
        print(f"#   ⚠ {x}")
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
