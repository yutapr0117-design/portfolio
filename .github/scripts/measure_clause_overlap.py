#!/usr/bin/env python3
"""measure_clause_overlap.py — ACD の草案と試作文について、条の重複と効果を運ぶ語の差分を数える。

**なぜ在るか (2026-11-04)**: オーナーの依頼「B3 / B13 (法的な明瞭さ・解釈の負荷) を、許諾の範囲・主体・
効果を保ったまま、重複と読みの分岐を減らして改善する」に対する 3 人の分担のうち、5a の受け持ち
(KPI を機械で数える / 試作への敵対的な反例探しの起点を作る)。目で拾う洗い出しの**対照**として使う ——
人の目は「同じ働きを言い直している」箇所を拾うが、拾い漏れを数えられない。

**測っているもの**:
  - 条 (`  N.M  …` の形) ごとの語数と全体の語数 (空白で区切った語・本文は区切り線 `-`×80 の後)
  - 条をまたいで **6 語以上一致する言い回し** (空白を正規化・大文字小文字は区別しない) の全数。
    重なる 6-gram を条の組ごとに最長の連なりへまとめ、条番号の組・語数・本文を出す
  - 比較モード: 2 つの版の条ごとの語数の差と、**効果を運ぶ語** (主体・許諾の動詞・範囲・除外・条件) の
    出現回数の差。試作で消えた語は、元では許され試作では許されない (またはその逆の) 利用の候補になる

**測っていないもの (重要)**: **法的効果**。語の一致は同じ働きの証拠ではなく、語の消失は効果の消失の
証拠ではない。この道具が出すのは「人が読んで確かめるべき箇所の一覧」までで、効果が保たれたかは
人 (と、最終的には弁護士と審査者) が判断する。

使い方:
    python3 .github/scripts/measure_clause_overlap.py LICENSES/ACD-1.4-DRAFT.txt
    python3 .github/scripts/measure_clause_overlap.py --min 8 LICENSES/ACD-1.4-DRAFT.txt
    python3 .github/scripts/measure_clause_overlap.py --compare BEFORE.txt AFTER.txt
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

SEP = "-" * 80
CLAUSE_RX = re.compile(r"^  (\d+\.\d+)\s+(.*?)(?=^  \d+\.\d+\s|^\d+\.\s|\Z)", re.M | re.S)

# 効果を運ぶ語。**網羅ではない** —— 反例探しの起点を作るための語彙で、ここに無い語の消失は拾わない。
OPERATIVE = {
    "主体": ["you", "your", "dedicator", "licensor", "contributor", "steward", "any person", "anyone",
           "everyone", "recipient", "successors", "assigns", "heirs"],
    "許諾の動詞": ["grant", "grants", "granted", "waive", "waives", "waived", "dedicate", "dedicates",
               "release", "releases", "license", "licence", "permit", "permits", "may", "covenant",
               "agree", "agrees", "promise", "not assert", "not to assert", "surrender"],
    "範囲": ["all", "any", "every", "each", "worldwide", "perpetual", "irrevocable", "royalty-free",
           "unconditional", "non-exclusive", "including", "without limitation", "whether or not",
           "to the maximum extent", "in any medium", "for any purpose"],
    "除外・限定": ["except", "excluding", "exclude", "excludes", "only", "solely", "not", "no ", "nothing",
               "does not", "do not", "shall not", "neither", "nor", "unless", "limited to", "other than"],
    "条件・時点": ["if", "where", "when", "provided", "subject to", "notwithstanding", "to the extent",
               "regardless", "even if", "in the event", "until", "upon", "before", "after"],
}


def body(text: str) -> str:
    return text.split(SEP, 1)[1] if SEP in text else text


def clauses(text: str) -> dict[str, str]:
    return {k: " ".join(v.split()) for k, v in CLAUSE_RX.findall(body(text))}


def words(s: str) -> list[str]:
    return s.split()


def overlaps(cl: dict[str, str], n: int) -> list[tuple[str, str, int, str]]:
    """条の組ごとに、共有する n-gram を最長の連なりへまとめて返す: (条 A, 条 B, 語数, 本文)。"""
    toks = {k: [w.lower().strip(".,;:()\"'") for w in words(v)] for k, v in cl.items()}
    orig = {k: words(v) for k, v in cl.items()}
    idx: dict[tuple, list[tuple[str, int]]] = defaultdict(list)
    for k, t in toks.items():
        for i in range(len(t) - n + 1):
            idx[tuple(t[i:i + n])].append((k, i))
    pair_hits: dict[tuple[str, str], set[tuple[int, int]]] = defaultdict(set)
    for g, occ in idx.items():
        ks = {k for k, _ in occ}
        if len(ks) < 2:
            continue
        for a, ia in occ:
            for b, ib in occ:
                if a < b:
                    pair_hits[(a, b)].add((ia, ib))
    out = []
    for (a, b), hits in pair_hits.items():
        seen = set()
        for ia, ib in sorted(hits):
            if (ia, ib) in seen:
                continue
            ln = n
            while (ia + ln - n + 1, ib + ln - n + 1) in hits:
                seen.add((ia + ln - n + 1, ib + ln - n + 1))
                ln += 1
            out.append((a, b, ln, " ".join(orig[a][ia:ia + ln])))
    key = lambda c: tuple(int(x) for x in c.split("."))
    return sorted(out, key=lambda r: (-r[2], key(r[0]), key(r[1])))


def phrase_families(ov: list[tuple[str, str, int, str]]) -> list[tuple[str, set[str]]]:
    """言い回しごとの族: 同じ本文 (小文字・句読点を落として比較) を共有する条の集合。

    連結成分 (families) は汎用の言い回しが多くの条を数珠つなぎにし、1.4 草案では 37 条が 1 族になる。
    人が「同じ働きを言い直しているか」を読むのは言い回しの単位なので、こちらを主に使う。
    """
    norm = lambda t: " ".join(w.lower().strip(".,;:()\"'") for w in t.split())
    fam: dict[str, set[str]] = defaultdict(set)
    rep: dict[str, str] = {}
    for a, b, _, txt in ov:
        k = norm(txt)
        fam[k] |= {a, b}
        rep.setdefault(k, txt)
    # 他の言い回しに丸ごと含まれ、条の集合も同じものは落とす (同じ一致の短い切れ端)
    keys = sorted(fam, key=len, reverse=True)
    out = []
    for k in keys:
        if any(k != o and k in o and fam[k] <= fam[o] for o in keys):
            continue
        out.append((rep[k], fam[k]))
    return sorted(out, key=lambda r: (-len(r[1]), -len(r[0].split())))


def families(ov: list[tuple[str, str, int, str]]) -> list[set[str]]:
    """共有する言い回しで結ばれた条の連結成分 (族の候補)。"""
    parent: dict[str, str] = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b, _, _ in ov:
        parent[find(a)] = find(b)
    groups: dict[str, set[str]] = defaultdict(set)
    for x in list(parent):
        groups[find(x)].add(x)
    return sorted(groups.values(), key=lambda g: (-len(g), sorted(g)))


# 許諾の動詞の語が名詞として使われる形 ("the grants themselves" / "any licence") を数えない。
# 2026-11-04、§2.8 の理由の文を外す試算で「grants 1→0」と出たが、それは名詞だった (誤検出)。
_NOUN_DET = r"(?<!\bthe )(?<!\bthese )(?<!\bthose )(?<!\bits )(?<!\bany )(?<!\bevery )(?<!\beach )(?<!\ba )"


def operative_counts(s: str) -> dict[str, dict[str, int]]:
    low = " " + " ".join(s.lower().split()) + " "
    out = {}
    for cat, ws in OPERATIVE.items():
        pre = _NOUN_DET if cat == "許諾の動詞" else ""
        out[cat] = {w: len(re.findall(pre + r"(?<![a-z-])" + re.escape(w.strip()) + r"(?![a-z-])", low)) for w in ws}
    return out


def report(path: Path, n: int) -> None:
    cl = clauses(path.read_text(encoding="utf-8"))
    tot = sum(len(words(v)) for v in cl.values())
    ov = overlaps(cl, n)
    fam = families(ov)
    print(f"# {path.name}: {len(cl)} 条 / 本文 {tot} 語 (条の本文のみ・見出しを含まない)")
    print(f"# 条をまたいで {n} 語以上一致する言い回し: {len(ov)} 箇所 / 関わる条 {len({x for r in ov for x in r[:2]})} / "
          f"言い回しごとの族 {len(phrase_families(ov))} (連結成分 {len(fam)})")
    print()
    pf = phrase_families(ov)
    key = lambda c: tuple(int(x) for x in c.split("."))
    print(f"## 言い回しごとの族 ({len(pf)} 個・共有する条の数が多い順) —— 人が読む単位はこちら")
    for txt, g in pf:
        print(f"- [{len(g)} 条] {', '.join('§' + c for c in sorted(g, key=key))}: {txt}")
    print()
    print("## 連結成分 (参考) —— 汎用の言い回しが数珠つなぎにするので、族の数としては使わない")
    for g in fam:
        print("- " + ", ".join(sorted(g, key=key)))
    print()
    print(f"## {n} 語以上の一致 (長い順)")
    for a, b, ln, txt in ov:
        print(f"- §{a} ⟷ §{b} ({ln} 語): {txt}")


def compare(before: Path, after: Path, n: int) -> None:
    cb, ca = clauses(before.read_text(encoding="utf-8")), clauses(after.read_text(encoding="utf-8"))
    tb, ta = sum(len(words(v)) for v in cb.values()), sum(len(words(v)) for v in ca.values())
    ob, oa = overlaps(cb, n), overlaps(ca, n)
    print(f"# Before {before.name}: {len(cb)} 条 / {tb} 語 / 重複 {len(ob)} 箇所 / 族 {len(phrase_families(ob))}")
    print(f"# After  {after.name}: {len(ca)} 条 / {ta} 語 / 重複 {len(oa)} 箇所 / 族 {len(phrase_families(oa))}")
    print(f"# 差: 条 {len(ca) - len(cb):+d} / 語 {ta - tb:+d} / 重複 {len(oa) - len(ob):+d}")
    print()
    key = lambda c: tuple(int(x) for x in c.split("."))
    print("## 条ごとの語数と、効果を運ぶ語の増減 (減った語は反例探しの起点)")
    for c in sorted(set(cb) | set(ca), key=key):
        b, a = cb.get(c, ""), ca.get(c, "")
        if b == a:
            continue
        wb, wa = len(words(b)), len(words(a))
        state = "削除" if not a else "新設" if not b else "変更"
        print(f"### §{c} ({state}: {wb} → {wa} 語)")
        ob_, oa_ = operative_counts(b), operative_counts(a)
        for cat in OPERATIVE:
            diffs = [f"{w.strip()} {ob_[cat][w]}→{oa_[cat][w]}" for w in OPERATIVE[cat] if ob_[cat][w] != oa_[cat][w]]
            if diffs:
                print(f"- {cat}: " + " / ".join(diffs))


def main(argv: list[str]) -> int:
    n = 6
    if "--min" in argv:
        i = argv.index("--min")
        n = int(argv[i + 1])
        del argv[i:i + 2]
    if argv and argv[0] == "--compare" and len(argv) == 3:
        compare(Path(argv[1]), Path(argv[2]), n)
        return 0
    if len(argv) == 1:
        report(Path(argv[0]), n)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        sys.exit("python 3.10+ が要る")
    sys.exit(main(sys.argv[1:]))
