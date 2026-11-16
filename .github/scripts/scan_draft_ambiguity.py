#!/usr/bin/env python3
"""scan_draft_ambiguity.py — 草案の文のうち、法的な読みが割れうる型を洗い出す (読む候補を出す道具・2026-11-16)。

**なぜ在るか**: オーナーの依頼 (2026-11-16)「ACD-1.4-DRAFT.txt の法的解釈の不確実性を『５人』で減らし続けてください」。
`scan_draft_terms.py` は条どうしの語の揺れを、`measure_clause_overlap.py --compare` は試作の差分を見る。どちらも、変えていない
文に元から在る「読みが割れる型」を全体で数えてはいなかった。候補を型ごとに出し、1c が試作に、30 が反例に、50 が法律家への問いに、
2f が先例の読みに回す。

**型** (どれも読む候補で、欠陥の証拠ではない):
  (a) 定義語の小文字の使用 —— "the work" のように、定義した語 (Work) を冠詞の後で小文字にした所。定義の内か外かが割れる。
  (b) 定義の無い大文字の語 —— 文中で大文字なのに §1 などで定義していない語。定義語に見えて定義が無い。
  (c) 使われない定義 —— 定義したのに本文の他の条で使っていない語。
  (d) §15.5 が既に覆う語の重ね書き —— §15.5 は "person" が entity を含むと言うので、"person or entity" は「person だけの所は
      entity を含まない」と反対解釈される余地を作る (expressio unius)。同じく単数・複数の重ね書き。
  (e) 基準の語 —— reasonable / substantial / material / appropriate / significant など、事実の評価に委ねる語。
  (f) 義務の助動詞 —— shall / must / will。ACD は受け手に条件を課さないので、これらが受け手を主語にしていないかを読む。
  (g) 古い指示語 —— herein / hereunder / hereby / thereof / therein / aforesaid / said。指し先が条か文書全体かで割れる。
  (h) "this Section" —— 小項 (N.M) の中の "this Section" は、節 (N) と小項 (N.M) のどちらを指すかで割れる (草案は Section の
      粒度を定義していない)。
  (i) "and/or"。
  (j) 優先の連鎖 —— "subject to Section X" / "notwithstanding Section X" / "Section X prevails" の向きを並べ、循環を出す。
  (k) 免責・制限の条が同じ文書の約束を呑むか —— 射程を "this Dedication" で言う免責・制限の条 (§13・§14 など) と、Dedicator が
      約束する条 (covenants / will not) の組で、免責の条がその約束を名指して外していないもの (1c の依頼・問い 9 (a) の型)。

**--law** (2026-11-16・50 の方法の (a)): 条ごとに「法に頼る句」(to the extent / applicable law / where … permits /
in a jurisdiction / held invalid / takes effect / is not / does not …) を抜き、5 人の帯 (1c §1〜4・30 §5〜7・50 §8〜10・
2f §11〜13・9b §14〜16) に分けて出す。各人が THIRD の第 18 節に「命題」を書き出すときの入力。

使い方:
    python3 .github/scripts/scan_draft_ambiguity.py                    # いまの草案
    python3 .github/scripts/scan_draft_ambiguity.py --law              # 法に頼る句を帯ごとに
    python3 .github/scripts/scan_draft_ambiguity.py LICENSES/ACD-1.3.txt
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from measure_clause_overlap import clauses  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RULE = "-" * 80
# 定義語ではないが大文字で書く語 (固有名・見出しの語・文書の語)
PROPER = {"Section", "Sections", "Article", "Directive", "EU", "English", "SPDX", "ACD", "AS", "IS", "Autonomous",
          "Commons", "Dedication", "License", "Identifier", "List", "LicenseRef", "Steward", "I", "The", "This",
          "Where", "If", "No", "Nothing", "A", "An", "In", "Any", "Each", "For", "To", "Neither", "Except", "Subject",
          "Without", "Paragraph", "Annex", "Union", "European", "Regulation", "Council", "Parliament", "Act",
          "Convention", "Berne", "Treaty", "WIPO", "United", "States", "Code", "Copyright", "Office"}
STANDARD = re.compile(r"\b(reasonabl[ey]|substantial(?:ly)?|material(?:ly)?(?= (?:part|change|breach|respect))|appropriate(?:ly)?|"
                      r"significant(?:ly)?|promptly|unreasonabl[ey]|adequate(?:ly)?|sufficient(?:ly)?|similar effect|"
                      r"of a personal character|in good faith)\b", re.I)
MODAL = re.compile(r"\b(shall|must|will)\b", re.I)
ARCHAIC = re.compile(r"\b(herein|hereunder|hereby|hereto|thereof|therein|thereunder|aforesaid|aforementioned|said(?= [a-z]+\b(?! that)))\b", re.I)
PRIORITY = re.compile(r"\b(subject to|notwithstanding|despite|prevails? over|takes? precedence over|does not (?:narrow|limit|affect|reduce))"
                      r" (?:anything in |any provision of |the |)Sections? (\d+(?:\.\d+)?)", re.I)


def defined_terms(text: str) -> dict[str, str]:
    """{語: 定義した条}。'"X" means' / '"X" includes' / '(the "X")' の形。"""
    out = {}
    for k, v in clauses(text).items():
        for m in re.finditer(r'(?:^|\(|[\s;])(?:the )?"([A-Z][A-Za-z\- ]+)" (?:means|includes|is|refers to)|\((?:the |each, a |a |an )?"([A-Z][A-Za-z\- ]+)"\)', v):
            out.setdefault(m.group(1) or m.group(2), k)
    return out


LAW = re.compile(r"\b(to the (?:fullest |greatest |maximum )?extent(?: (?:that |permitted by |the law |a jurisdiction |applicable law )[^,.;]{0,40})?|"
                 r"applicable law|under (?:the )?(?:applicable )?law|the law of [a-z ]+?(?=[,.;])|where (?:the |applicable )?law [^,.;]{0,40}|"
                 r"in (?:a|any|each) jurisdiction[^,.;]{0,30}|held (?:invalid|unenforceable|ineffective)|"
                 r"takes? effect[^,.;]{0,30}|is (?:effective|ineffective|valid|void|enforceable)[^,.;]{0,30}|"
                 r"as a matter of (?:law|fact)|by operation of law|whether or not [^,.;]{0,40}(?:subsist|recogni|known)[^,.;]{0,20}|"
                 r"irrevocabl[ey]|perpetual|worldwide|cannot be (?:waived|excluded|limited)[^,.;]{0,20}|"
                 r"(?:intended|third-party) beneficiar(?:y|ies)|consideration|estoppel|covenants?(?= not)|waives?|"
                 # 取りこぼしを減らす受け皿: 法・法域・裁判所・権利の存否を名指す句 (前後 30 字)
                 r"[^,.;]{0,30}\b(?:laws?|jurisdictions?|courts?|statutes?|subsists?|enforce(?:able|d)?|revocab\w+|terminat\w+)\b[^,.;]{0,30})", re.I)
BANDS = (("1c", 1, 4), ("30", 5, 7), ("50", 8, 10), ("2f", 11, 13), ("9b", 14, 16))


def law_phrases(cl: dict[str, str]) -> None:
    """--law: 条ごとに法に頼る句を抜き、5 人の帯に分けて出す。"""
    for who, lo, hi in BANDS:
        rows = [(k, sorted({" ".join(m.group(0).split()).lower() for m in LAW.finditer(" ".join(v.split()))}))
                for k, v in cl.items() if "." in k and lo <= int(k.split(".")[0]) <= hi]
        rows = [(k, ps) for k, ps in rows if ps]
        print(f"\n## {who}（§{lo}〜§{hi}）: {len(rows)} 条・{sum(len(p) for _k, p in rows)} 句")
        for k, ps in rows:
            print(f"- §{k}: " + " / ".join(f"「{p}」" for p in ps))


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    law = "--law" in argv
    argv = [a for a in argv if a != "--law"]
    path = Path(argv[0]) if argv else sorted((ROOT / "LICENSES").glob("ACD-*-DRAFT.txt"),
                                             key=lambda p: len(p.read_text(encoding="utf-8")))[-1]
    text = path.read_text(encoding="utf-8")
    cl = clauses(text)
    flat = {k: " ".join(v.split()) for k, v in cl.items()}
    terms = defined_terms(text)
    if law:
        print(f"# {path.name}: 法に頼る句 (条ごと・5 人の帯)")
        law_phrases(cl)
        return 0
    print(f"# {path.name}: 条 {len(cl)}・定義語 {len(terms)} ({', '.join(sorted(terms))})")
    found: dict[str, list[str]] = defaultdict(list)

    for k, v in flat.items():
        # (a) 定義語の小文字 —— 冠詞・限定詞の後だけ (一般の "a work" は数えない)
        for t in terms:
            if " " in t or t in ("You", "Your"):
                continue
            for m in re.finditer(r"\b(the|this|that|such|each|any|every)( " + re.escape(t.lower()) + r"s?)\b", v):
                found["a"].append(f"§{k} 「{m.group(0)}」 —— 定義語 {t} (§{terms[t]}) を小文字で")
        # (b) 定義の無い大文字の語 (文頭と引用符の中と全大文字の文を除く)
        if not re.search(r"[A-Z]{6,}", v[:40]):
            body = re.sub(r'"[^"]*"', '""', v)
            for tm in sorted(terms, key=len, reverse=True):  # 定義語 (複数語を含む) を先に消す
                body = re.sub(r"\b" + re.escape(tm) + r"s?\b", "x", body)
            for m in re.finditer(r"(?<=[a-z,;] )([A-Z][a-z]+(?: [A-Z][a-z]+)*)", body):
                w = m.group(1)
                if not any(w == t or w.startswith(t) or t.startswith(w) for t in terms) and w.split()[0] not in PROPER:
                    found["b"].append(f"§{k} 「{w}」")
        # (d) §15.5 が覆う重ね書き
        for m in re.finditer(r"\bperson or entity\b|\bpersons or entities\b|\bperson\(s\)|\bentity or person\b", v):
            found["d"].append(f"§{k} 「{m.group(0)}」 —— §15.5 は person が entity を含むと言う")
        for rx, typ in ((STANDARD, "e"), (MODAL, "f"), (ARCHAIC, "g")):
            for m in rx.finditer(v):
                s = max(0, m.start() - 45)
                found[typ].append(f"§{k} 「{m.group(0)}」: …{v[s:m.end() + 45]}…")
        # (h) 小項の中の "this Section"
        if "." in k:
            for m in re.finditer(r"\bthis Section\b", v):
                s = max(0, m.start() - 40)
                found["h"].append(f"§{k}: …{v[s:m.end() + 40]}… —— §{k.split('.')[0]} か §{k} か")
        for m in re.finditer(r"\band/or\b", v):
            found["i"].append(f"§{k}")
    # (k) 免責・制限の条が同じ文書の約束を呑むか (2026-11-16・1c の依頼・問い 9 (a))
    # 責任を外す条だけ (保証の否認と依拠の否認は約束の違反の責任を外さないので数えない・初版は §6.3 と §13.2 で 26 件の雑音)
    limiters = [k for k, v in flat.items() if re.search(r"NOT LIABLE|is not liable", v) and re.search(r"this dedication", v, re.I)]
    promises = [k for k, v in flat.items() if re.search(r"\bcovenants?\b|\bwill not\b|\bundertakes?\b|\bagrees? not\b", v)]
    for lk in limiters:
        named = set(re.findall(r"(?:Section|SECTION)S? (\d+(?:\.\d+)?)", flat[lk]))
        open_ = [pk for pk in promises if pk != lk and pk not in named and pk.split(".")[0] not in named]
        if open_:
            m = re.search(r"arising out of this dedication[^,.]*|this dedication", flat[lk], re.I)
            found["k"].append(f"§{lk} の射程「{m.group(0)[:60]}」が、Dedicator の約束の条 {len(open_)} を名指して外していない: "
                              + ", ".join("§" + x for x in open_))
    # (c) 使われない定義
    for t, k in terms.items():
        uses = [c for c, v in flat.items() if c != k and re.search(r"\b" + re.escape(t) + r"s?\b", v)]
        if not uses:
            found["c"].append(f"「{t}」 (§{k} で定義・他の条で使われない)")
    # (j) 優先の連鎖
    edges = defaultdict(set)
    for k, v in flat.items():
        for m in PRIORITY.finditer(v):
            edges[k].add(m.group(2))
            found["j"].append(f"§{k} 「{m.group(1)} Section {m.group(2)}」")

    def reach(a, b, seen=()):
        return any(n == b or (n not in seen and reach(n, b, seen + (n,))) for n in edges.get(a, ()))
    cyc = sorted({tuple(sorted((a, b))) for a in edges for b in edges[a] if reach(b, a)})
    for a, b in cyc:
        found["j"].append(f"⚠ 循環: §{a} ⇄ §{b}")

    names = {"a": "定義語の小文字の使用", "b": "定義の無い大文字の語", "c": "使われない定義",
             "d": "§15.5 が覆う語の重ね書き (person or entity)", "e": "事実の評価に委ねる基準の語",
             "f": "義務の助動詞 (shall / must / will) —— 受け手を主語にしていないか", "g": "古い指示語",
             "h": "小項の中の \"this Section\" —— 節か小項か", "i": "and/or", "j": "優先の連鎖 (subject to / notwithstanding …)",
             "k": "免責・制限の条が同じ文書の約束を呑むか (問い 9 (a) の型)"}
    for typ, name in names.items():
        xs = found.get(typ, [])
        print(f"\n## ({typ}) {name}: {len(xs)}")
        for x in xs:
            print(f"- {x}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
