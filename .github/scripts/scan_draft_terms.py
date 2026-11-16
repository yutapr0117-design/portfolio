#!/usr/bin/env python3
"""scan_draft_terms.py — 草案の条どうしの語の揺れを掃引する (読む候補を出す道具・2026-11-16・1c の依頼)。

**なぜ在るか**: §15.11・§15.12 (THIRD) は、同じものを 2 つの語で呼ぶ揺れと、ほぼ同じ列挙の 1 項だけの違いを人の目で見つけた。
T74〜T76 は、ある条が他の条の定義を借りる語 (names / reaches / binds / to the extent Section N) が、人・範囲・限度のどれを借りる
かの食い違いだった。どれも 1 か所ずつ直したが、草案全体を同じ型で掃引する道具が無かった。

**出すもの** (どれも読む候補で、欠陥の証拠ではない):
  (a) 3 項以上の列挙 ("x, y, and z" / "x, y, or z") のうち、別の条の列挙と項の 6 割以上が重なるのに一致しないもの。
  (b) 他の条を指す句 ("… Section 8 reaches" / "… that Sections 8.1 and 8.4 reach" / "the persons Section 2.8 names") を、
      指し先の条ごとにまとめ、言い方が 2 通り以上あるもの。
  (c) 定義を借りる語の一覧: 指し先の条ごとに、借りる動詞 (names = 人 / reaches・describes = 範囲 / to the extent = 限度 /
      binds = 拘束の相手) と、使っている条。同じ指し先から違う種類を借りていれば、人が読む。
  (d) 英米の綴りの混在 (2026-11-16・T82 の "WILFUL" を読んで足した): 綴りの対 (wilful / willful・authorise / authorize・
      endeavour / endeavor …) のうち、草案に両方の綴りがある語。草案は英国綴りで書かれている (licence は名詞・license は動詞)。
      license / licence は名詞と動詞を分けられないので数えない。

**測っていないもの**: 揺れが効果の違いを生むか。語が違っても同じ働きのこともあり、同じ語でも働きが違うこともある。

使い方:
    python3 .github/scripts/scan_draft_terms.py                     # いまの草案
    python3 .github/scripts/scan_draft_terms.py LICENSES/ACD-1.3.txt   # ほかの本文
"""
from __future__ import annotations

import itertools
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from measure_clause_overlap import clauses  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LIST = re.compile(r"(?<![\w'’])((?:[A-Za-z][\w\- ]{1,40}?, ){2,}(?:and|or) [A-Za-z][\w\- ]{1,40}?)(?=[,.;:)]| (?:of|in|to|for|by|that|which|are|is|and|or)\b)")
REF = re.compile(r"((?:[a-z][\w\-]* ){0,3}?(?:that |which |whom |those )?Sections? (\d+(?:\.\d+)?(?:(?:, | and | or | to )\d+(?:\.\d+)?)*) "
                 r"(names?|reach(?:es)?|describes?|binds?|covers?|governs?))\b")
EXTENT = re.compile(r"to the (?:fullest )?extent (?:that )?(?:Sections? (\d+(?:\.\d+)?)|the law permits|a jurisdiction)")
SPELL = (("wilful", "willful"), ("authoris", "authoriz"), ("organis", "organiz"), ("recognis", "recogniz"),
         ("characteris", "characteriz"), ("minimis", "minimiz"), ("endeavour", "endeavor"), ("favour", "favor"),
         ("behaviour", "behavior"), ("labour", "labor"), ("judgement", "judgment"), ("defence", "defense"),
         ("offence", "offense"), ("practis", "practic"), ("programme", "program"), ("analys", "analyz"))
KIND = {"name": "人", "names": "人", "reach": "範囲", "reaches": "範囲", "describe": "範囲", "describes": "範囲",
        "bind": "拘束の相手", "binds": "拘束の相手", "cover": "範囲", "covers": "範囲", "govern": "範囲", "governs": "範囲"}


def items(lst: str) -> list[str]:
    parts = re.split(r", (?:and |or )?| (?:and|or) ", lst)
    return [re.sub(r"^(?:the|a|an|any|its|their|his|her) ", "", p.strip().lower()) for p in parts if p.strip()]


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    path = Path(argv[0]) if argv else next(p for p in sorted((ROOT / "LICENSES").glob("ACD-*-DRAFT.txt"))
                                          if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0])
    cl = clauses(path.read_text(encoding="utf-8"))
    lists = [(k, m.group(1), items(m.group(1))) for k, v in cl.items() for m in LIST.finditer(v)]
    lists = [x for x in lists if len(x[2]) >= 3]
    print(f"# {path.name}: 条 {len(cl)}・3 項以上の列挙 {len(lists)}")
    print("\n## (a) ほぼ同じ列挙の 1 項以上の違い（項の 6 割以上が重なり、一致しない）")
    seen = set()
    for (k1, s1, a), (k2, s2, b) in itertools.combinations(lists, 2):
        sa, sb = set(a), set(b)
        if sa == sb or k1 == k2:
            continue
        j = len(sa & sb) / len(sa | sb)
        key = (frozenset(sa), frozenset(sb))
        if j >= 0.6 and key not in seen:
            seen.add(key)
            print(f"- §{k1} 「{s1}」 / §{k2} 「{s2}」 —— 片方だけ: {sorted(sa ^ sb)}")
    refs = defaultdict(list)
    for k, v in cl.items():
        for m in REF.finditer(v):
            refs[m.group(2)].append((k, " ".join(m.group(1).split()), KIND.get(m.group(3), "?")))
        for m in EXTENT.finditer(v):
            if m.group(1):
                refs[m.group(1)].append((k, m.group(0), "限度"))
    print("\n## (b) 同じ指し先を指す句の言い方が 2 通り以上")
    for tgt, rs in sorted(refs.items()):
        phr = sorted({re.sub(r"^(?:(?:and|or|the|a|any|every|against|under|of|in|to|for|by|bind|You) )+", "", p) for _k, p, _w in rs})
        if len(phr) >= 2:
            print(f"- Section {tgt}: " + " / ".join(f"「{p}」" for p in phr) + f"（{', '.join(sorted({'§' + k for k, _p, _w in rs}))}）")
    print("\n## (c) 定義を借りる語 —— 指し先ごとに、借りる種類（人・範囲・限度・拘束の相手）")
    for tgt, rs in sorted(refs.items()):
        kinds = sorted({w for _k, _p, w in rs})
        mark = "⚠" if len(kinds) >= 2 else "・"
        print(f"{mark} Section {tgt}: {', '.join(kinds)} —— " + "; ".join(f"§{k} 「{p}」" for k, p, _w in rs)[:300])
    print("\n## (d) 英米の綴りの混在（同じ語に両方の綴りがあるもの・数は出現の数）")
    low = " ".join(cl.values()).lower()
    mixed = 0
    for uk, us in SPELL:
        # practic は practice（名詞・英米共通）に当たるので、英国の動詞 practise と対にするときは動詞の形だけを数える
        a = len(re.findall(r"\b" + uk + r"\w*", low))
        b = len(re.findall(r"\b" + (r"practic(?:ed|ing)\b" if us == "practic" else us + r"\w*"), low))
        if a and b:
            mixed += 1
            print(f"⚠ {uk}… {a} / {us}… {b}")
    if not mixed:
        print("・ 混在なし")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
