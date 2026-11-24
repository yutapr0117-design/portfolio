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
  (l) 同じ条の中の "X or Y" と "X and Y" —— 同じ 2 語を一方で or、他方で and で並べると、and が「両方が揃ったときだけ」と
      読まれる余地が出る (2026-11-18・T98 の §5.2 の "terms or measures" と "those terms and measures")。
  (m) "may not" —— 禁止 (許されない) か、可能性 (しないかもしれない) かで割れる (2026-11-18・2f の §1.266・Cowan 氏「may not は
      読み違えられやすい」)。文の中に禁止を示す語 (restricted / prohibited / no … may) が在れば読みは閉じやすいが、候補として出す。
  (n) 指示の限定詞 (these / those / such + 名詞) の名詞が、同じ条のその前に無い所 —— 先行詞が条の外にあるか、別の語で呼ばれていて、
      指し先が割れる (2026-11-19・1c の掃引: §16.2 の "these terms" と §8.5 の "these licences")。"those invited" のような分詞と
      "these or any other …" は数えない。
  (o) 同じ働きの除外が片方にだけ在る所 —— 同じ節の Dedicator の約束の項どうしで、除外の句 ("other than for / under …") の集合を比べ、
      他の項が持つ除外を持たない項を出す (2026-11-19・30 の 2 巡目の型: §5.1 と §5.2(d) は §11.3 を外し §5.2(b) は外さなかった)。
      除外が無いのが正しい項 (技術的手段・§15.1 の読み) も出るので、候補として読む。
  (q) 一般の条を特定の条だけに言い直す所 —— §2.8 は Dedication の全体で承継人を縛るのに、§5.3・§12.4 が一部の約束だけを
      「the persons Section 2.8 names」を縛ると言い直すと、言い直しの無い約束は承継人を縛らない、の反対解釈が立つ
      (2026-11-19・9b の 2 巡目 §1〜§4)。Dedicator の約束の条のうち、その言い直しの文に名指されないものを出す。
  (r) 否定の条件が "X or Y" に掛かる所 —— "Where … does not permit the exclusion or limitation …" は「どちらも許さない場合」と
      「片方を許さない場合」に割れ、条件の真偽が場面で変わる (2026-11-20・1c の 4 巡目・T126 の §14.2)。条件の句 (Where / If /
      Unless / To the extent / So far as) の中に否定と or / nor が在るものを出す。"whether or not" は数えない。

**--law** (2026-11-16・50 の方法の (a)): 条ごとに「法に頼る句」(to the extent / applicable law / where … permits /
in a jurisdiction / held invalid / takes effect / is not / does not …) を抜き、5 人の帯 (1c §1〜4・30 §5〜7・50 §8〜10・
2f §11〜13・9b §14〜16) に分けて出す。各人が THIRD の第 18 節に「命題」を書き出すときの入力。

**--split** (2026-11-18・オーナーの依頼「法的解釈が一意に定まるように」・THIRD §19 の入力): 本文の語が 2 通りに読める候補を、
5 人の帯に分けて出す。(p) 代名詞 (it / its / they / them / their) の文の中に、その前に先行詞の候補が 2 つ以上ある所。(m) 3 項
以上の列挙の後ろの修飾 (resulting from / derived from / in respect of / that / which / held by / made by …) —— 最後の項だけに掛かるか、
列挙の全体に掛かるかで割れる。どちらも候補で、各帯の人が §19 に「別の読み」として書くか、立たないと判断する。

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


ANTE_SG = ("the Work", "this Dedication", "the Dedicator", "the licence", "a licence", "the permission", "a permission",
           "the covenant", "a covenant", "the right", "a right", "the claim", "a claim", "the notice", "a notice", "the text",
           "the model", "the material", "the Reservation", "a Reservation", "the identifier", "the name")
LIST_MOD = re.compile(r"((?:[\w\-]+(?: [\w\-]+){0,3}, ){2,}(?:and |or )[\w\-]+(?: [\w\-]+){0,3}) "
                      r"(resulting from|derived from|in respect of|arising from|arising out of|held by|made by|owned or controlled by|"
                      r"that|which|of the Work|in the Work)\b", re.I)  # 全大文字の条 (§13・§14) も読む (初版は §14.1 を取りこぼした)


def split_candidates(cl: dict[str, str]) -> None:
    """--split: 本文の語が 2 通りに読める候補 (代名詞の先行詞・列挙の後の修飾の掛かり先) を帯ごとに出す。"""
    for who, lo, hi in BANDS:
        rows = []
        for k, v in cl.items():
            if "." not in k or not (lo <= int(k.split(".")[0]) <= hi):
                continue
            flat = " ".join(v.split())
            for sent in re.split(r"(?<=[.;:])\s+", flat):
                for m in re.finditer(r"\b(it|its)\b", sent):
                    before = sent[:m.start()]
                    cands = sorted({a for a in ANTE_SG if a.lower() in before.lower()})
                    if len(cands) >= 2:
                        rows.append(f"§{k} (p) '{m.group(1)}' の先行詞の候補 {cands}: …{sent[max(0, m.start() - 70):m.end() + 30]}…")
                for m in LIST_MOD.finditer(sent):
                    rows.append(f"§{k} (m) 列挙「{m.group(1)[-60:]}」の後の '{m.group(2)}' —— 最後の項だけか、全体か")
        print(f"\n## {who}（§{lo}〜§{hi}）: {len(rows)} 件")
        for r in rows:
            print(f"- {r[:260]}")


def law_phrases(cl: dict[str, str]) -> None:
    """--law: 条ごとに法に頼る句を抜き、5 人の帯に分けて出す。"""
    for who, lo, hi in BANDS:
        rows = [(k, sorted({" ".join(m.group(0).split()).lower() for m in LAW.finditer(" ".join(v.split()))}))
                for k, v in cl.items() if "." in k and lo <= int(k.split(".")[0]) <= hi]
        rows = [(k, ps) for k, ps in rows if ps]
        print(f"\n## {who}（§{lo}〜§{hi}）: {len(rows)} 条・{sum(len(p) for _k, p in rows)} 句")
        for k, ps in rows:
            print(f"- §{k}: " + " / ".join(f"「{p}」" for p in ps))


def this_section_hits(flat: dict[str, str]) -> list[tuple[str, str]]:
    """(h) 小項 (N.M) の中の "this Section" —— 節か小項かが割れる。Check 468ab が 0 を保つ (T84〜T88 で 0 にした)。"""
    out = []
    for k, v in flat.items():
        if "." in k:
            for m in re.finditer(r"\b[Tt]his Section\b", v):  # 文頭の "This Section" も同じく割れる
                out.append((k, v[max(0, m.start() - 40):m.end() + 40]))
    return out


def negated_condition_hits(flat: dict[str, str]) -> list[tuple[str, str]]:
    """(r) 条件の句 (Where / If / Unless / To the extent / So far as) の中に否定と or / nor が在るもの。Check 468ab が 0 を保つ
    (T126 で §14.2 を 0 にした・2026-11-20)。"whether or not" は条件の句に数えない。"""
    out = []
    for k, v in flat.items():
        for m in re.finditer(r"(?:^|[.;:]\s+|,\s+|\(\w\)\s+)((?:[Ww]here|[Ii]f|[Uu]nless|[Tt]o the extent(?: that)?|[Ss]o far as)\b[^,.;]{0,160}?)(?=,|\.|;)", v):
            c = m.group(1)
            if re.search(r"\b(?:not|no|neither|never|without)\b", c) and re.search(r"\b(?:or|nor)\b", c):
                out.append((k, c))
    return out


def limiter_gaps(flat: dict[str, str]) -> list[tuple[str, str, list[str]]]:
    """(k) 責任を外す条が、同じ節のどの条も例外として名指していない Dedicator の約束の条 (問い 9 (a) の型)。
    Check 468ab が 0 を保つ (T83・T88 で 0 にした)。"""
    out = []
    # 責任を外す条だけ (保証の否認と依拠の否認は約束の違反の責任を外さないので数えない・初版は §6.3 と §13.2 で 26 件の雑音)
    limiters = [k for k, v in flat.items() if re.search(r"NOT LIABLE|is not liable", v) and re.search(r"this dedication", v, re.I)]
    # 約束の主語が Dedicator の文だけ (他の条の約束を名指すだけの条 —— §4.6・§11.4 —— は約束ではない・2026-11-16 に 2 件の雑音)
    promises = [k for k, v in flat.items()
                if re.search(r"\bDedicator(?:'s)?(?: further| also| irrevocably)? (?:covenants?|will not|undertakes?|agrees? not)\b", v)
                # 名詞の「undertaking」で Dedicator を縛る条も約束 (2026-11-19・2f: §2.6 "This undertaking binds that Dedicator" を見落とした)
                or re.search(r"\b(?:undertaking|covenant|promise) binds (?:only )?(?:that|the) Dedicator\b", v)]
    for lk in limiters:
        # 同じ節の他の条が置く例外も数える (T83 は §14.1 の免責の例外を §14.2 に置いた)。"Section 5, 8.6, or 12.2" も読む
        sib = " ".join(v for c, v in flat.items() if c.split(".")[0] == lk.split(".")[0])
        named = set()
        for grp in re.findall(r"(?:Section|SECTION)S? (\d+(?:\.\d+)?(?:(?:, | or | and |, or |, and )\d+(?:\.\d+)?)*)", sib):
            named |= set(re.findall(r"\d+(?:\.\d+)?", grp))
        # 約束の条の側が免責の節を名指して扱いを決めていれば、割れは閉じている (「This undertaking is subject to Section 14」など)
        top = lk.split(".")[0]
        open_ = [pk for pk in promises if pk != lk and pk not in named and pk.split(".")[0] not in named
                 and not re.search(r"\bSections? " + re.escape(top) + r"(?:\.\d+)?\b", flat[pk])]
        if open_:
            m = re.search(r"arising out of this dedication[^,.]*|this dedication", flat[lk], re.I)
            out.append((lk, m.group(0)[:60], open_))
    return out


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    law = "--law" in argv
    split = "--split" in argv
    argv = [a for a in argv if a not in ("--law", "--split")]
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
    if split:
        print(f"# {path.name}: 本文の語が 2 通りに読める候補 (代名詞の先行詞・列挙の後の修飾・5 人の帯・THIRD §19 の入力)")
        split_candidates(cl)
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
        for _k, ctx in this_section_hits({k: v}):
            found["h"].append(f"§{k}: …{ctx}… —— §{k.split('.')[0]} か §{k} か")
        for m in re.finditer(r"\band/or\b", v):
            found["i"].append(f"§{k}")
    for lk, phrase, open_ in limiter_gaps(flat):
        found["k"].append(f"§{lk} の射程「{phrase}」が、Dedicator の約束の条 {len(open_)} を名指して外していない: "
                          + ", ".join("§" + x for x in open_))
    # (l) 同じ条の中の "X or Y" と "X and Y"
    for k, v in flat.items():
        def _pairs(conj):
            return {tuple(sorted(w.lower().rstrip("s") for w in m)) for m in re.findall(r"\b([a-z]{4,}s?) " + conj + r" ([a-z]{4,}s?)\b", v)}
        for a, b in sorted(_pairs("or") & _pairs("and")):
            found["l"].append(f"§{k}: \"{a} or {b}\" と \"{a} and {b}\" が同じ条に在る")
    # (m) "may not"
    for k, v in flat.items():
        for m in re.finditer(r"\bmay not\b", v):
            found["m"].append(f"§{k}: …{v[max(0, m.start() - 50):m.end() + 40]}…")
    # (n) 指示の限定詞の名詞が同じ条のその前に無い
    for k, v in flat.items():
        for m in re.finditer(r"\b(these|those|such)\s+([a-z]+)", v):
            noun = m.group(2)
            if noun in ("as", "a", "an", "the", "that", "who", "whom", "which", "of", "to", "in", "or", "and") or noun.endswith("ed"):
                continue
            stem = noun[:-1] if noun.endswith("s") else noun
            if not re.search(r"\b" + re.escape(stem) + r"s?\b", v[:m.start()].lower()):
                found["n"].append(f"§{k}: '{m.group(0)}' —— 同じ条のその前に '{stem}' が無い: …{v[max(0, m.start() - 50):m.end() + 30]}…")
    # (o) 同じ節の約束の項どうしの除外の食い違い
    PROM_O = re.compile(r"\bcovenants? (?:not|that)\b|\bwill not\b|\bnot to assert\b")
    def _excl_o(u):
        out = []
        for m in re.finditer(r"\bother than ((?:for|under) .+?)(?:\.\s|;|, (?:impose|assert)\b|$)", u):
            # 並びはカンマか、括弧の後の "or" で区切る (T112 の §5.2(b) "(Section 11.1) or for a payment …" はカンマが無い)
            for part in re.split(r"(?:,\s*(?:or\s+)?|(?<=\))\s+or\s+)(?=(?:for|under)\b)", m.group(1)):
                r = re.search(r"\(Sections? ([\d.]+)\)", part)
                out.append("§" + r.group(1) if r else " ".join(part.split()[:4]))
        return out
    groups_o = {}
    for k, v in flat.items():
        units = re.split(r"\s(?=\([a-z]\)\s)", v)
        lead_prom = bool(PROM_O.search(units[0]))
        for i, u in enumerate(units):
            if i == 0 and len(units) > 1 and u.rstrip().endswith(":"):
                continue  # 列挙の導入の句は項に約束を渡すだけ
            if (i and lead_prom) or (i == 0 and PROM_O.search(u)):
                lab = f"§{k}" + (re.match(r"\(([a-z])\)", u).group(0) if i else "")
                groups_o.setdefault(k.split(".")[0], []).append((lab, _excl_o(u)))
    for sec, items in groups_o.items():
        union = sorted({x for _, e in items for x in e})
        for lab, e in items:
            miss = [x for x in union if x not in e]
            if union and miss:
                found["o"].append(f"{lab}: 除外 {e or '無し'} —— 同じ節の他の約束が持つのに無い除外 {miss}")
    # (q) 承継人を縛る言い直しに名指されない約束
    restated, prom_q = set(), []
    for k, v in flat.items():
        if (re.search(r"\bDedicator(?:'s)?(?: further| also| irrevocably)? (?:covenants?|will not|undertakes?|agrees? not|consents?)\b", v)
                or re.search(r"\b(?:undertaking|covenant|promise) binds (?:that|the) Dedicator\b", v)):
            prom_q.append(k)
        for s in re.split(r"(?<=[.;])\s+", v):
            if re.search(r"\bthe persons Section 2\.8 names\b", s):
                restated |= set(re.findall(r"\d+\.\d+", s.split(" bind")[0]))
    if restated:
        for k in prom_q:
            if k not in restated:
                found["q"].append(f"§{k}: Dedicator の約束の条なのに、承継人を縛ると言い直す文（{', '.join('§' + x for x in sorted(restated))} を名指す）に無い")
    # (r) 否定の条件が or の並びに掛かる (Check 468ab が 0 を保つ)
    for k, c in negated_condition_hits(flat):
        found["r"].append(f"§{k}: 「{c[:120]}」 —— 否定が or の並びの両方に掛かるか片方か")
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
             "k": "免責・制限の条が同じ文書の約束を呑むか (問い 9 (a) の型)",
             "l": "同じ条の中の \"X or Y\" と \"X and Y\"",
             "m": "\"may not\" —— 禁止か可能性か",
             "n": "指示の限定詞 (these / those / such) の名詞が同じ条のその前に無い",
             "o": "同じ働きの除外が片方にだけ (同じ節の約束の項どうしの除外の食い違い)",
             "q": "承継人を縛ると言い直す文 (the persons Section 2.8 names) に名指されない約束",
             "r": "否定の条件が \"X or Y\" に掛かる (両方か片方か)"}
    for typ, name in names.items():
        xs = found.get(typ, [])
        print(f"\n## ({typ}) {name}: {len(xs)}")
        for x in xs:
            print(f"- {x}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
