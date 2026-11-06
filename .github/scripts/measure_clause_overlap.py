#!/usr/bin/env python3
"""measure_clause_overlap.py — ACD の草案と試作文について、条の重複と効果を運ぶ語の差分を数える。

**なぜ在るか (2026-11-04)**: オーナーが共有した別の AI の見解 (B3 / B13 —— 法的な明瞭さ・解釈の負荷を、
許諾の範囲・主体・効果を保ったまま、重複と読みの分岐を減らして下げる) を材料に、3 人が判断して進めた検証の、
5a の受け持ち (KPI を機械で数える / 試作への敵対的な反例探しの起点を作る)。課題設定は別の AI のもので、
オーナーの指示ではない (オーナー本人の依頼は「3 人で連携して承認に近づける自走」)。人の目は「同じ働きを
言い直している」箇所を拾うが、拾い漏れを数えられない —— この道具はその**対照**である。

**測っているもの**:
  - 条 (`  N.M  …` の形) ごとの語数と全体の語数 (空白で区切った語・本文は区切り線 `-`×80 の後)
  - 条をまたいで **6 語以上一致する言い回し** (空白を正規化・大文字小文字は区別しない) の全数。
    重なる 6-gram を条の組ごとに最長の連なりへまとめ、条番号の組・語数・本文を出す
  - 比較モード: 2 つの版の条ごとの語数の差と、**効果を運ぶ語** (主体・許諾の動詞・範囲・除外・条件) の
    出現回数の差。試作で消えた語は、元では許され試作では許されない (またはその逆の) 利用の候補になる
  - 比較モード: 外した語に**ドシエの外向きの文書が依拠していないか** (LICENSES/*.md・rounds/ と作業記録を除く)。
    外した 5 語の連なりの引用と、「§N.N gives」「Section N.N's own text」「§N.N 自身が述べ」の形を拾い、
    審査者向けの文書 (その版を対象にするなら書き換えが要る) と記録 (当時の本文を引く) に分けて出す

**測っていないもの (重要)**: **法的効果**。語の一致は同じ働きの証拠ではなく、語の消失は効果の消失の
証拠ではない。この道具が出すのは「人が読んで確かめるべき箇所の一覧」までで、効果が保たれたかは
人 (と、最終的には弁護士と審査者) が判断する。

使い方:
    python3 .github/scripts/measure_clause_overlap.py LICENSES/ACD-1.4-DRAFT.txt
    python3 .github/scripts/measure_clause_overlap.py --min 8 LICENSES/ACD-1.4-DRAFT.txt
    python3 .github/scripts/measure_clause_overlap.py --compare BEFORE.txt AFTER.txt
    python3 .github/scripts/measure_clause_overlap.py --guard TRIAL.txt   # 468u の目印が残っているか
    python3 .github/scripts/measure_clause_overlap.py --uses DRAFT.txt Work "Computational Use"   # 定義語を使う条
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


# 先行詞を要する指示語。同じ条の中で、それより前に条番号 ("Section 5.3" / "Sections 5.3 and 12.4") が
# 無ければ宙に浮いている。2026-11-04、§2.8 の理由の文を外す私の試算版で末文の "those Sections" が
# 先行詞を失ったのを、25 が読んで見つけた (道具は見ていなかった)。
# 番号が続く形 ("claims that Sections 8.1 and 8.4 reach") は関係節であって指示語ではない (2026-11-06 に誤検出した)。
_ANAPHORA = re.compile(r"\b(those|these|that|such|the said) (Sections?|provisions?|clauses?|paragraphs?)\b(?! \d)", re.I)
_SECREF = re.compile(r"\bSections? \d+\.\d+")


def dangling(cl: dict[str, str]) -> list[tuple[str, str]]:
    out = []
    for k, v in cl.items():
        for m in _ANAPHORA.finditer(v):
            if not _SECREF.search(v[:m.start()]):
                out.append((k, v[max(0, m.start() - 40):m.end() + 20]))
    return out


# 条の参照。"Section 6.5" / "Sections 5.3 and 12.4" / "(Section 6.5)" の条番号を拾う。
_REF = re.compile(r"\bSections? (\d+\.\d+)((?:(?:,| and| or|,? and|,? or) \d+\.\d+)*)")
# 参照先の**内容を述べる**形 (参照先に意味のある文が残っているかを読む必要がある)。単なる指し先 "(Section 6.5)" と区別する。
_DESCRIPTIVE = re.compile(r"\b(purpose|reason|rule|principle|limit|result|question|test|meaning|definition|"
                          r"stated in|states|given in|described in|set out in|explains?|says|why|as .{0,30}provides?)\b", re.I)


def refs_to(cl: dict[str, str], target: str) -> list[tuple[str, str, bool]]:
    """target 条を参照している箇所: (参照する条, 前後の文脈, 内容を述べる形か)。"""
    out = []
    for k, v in cl.items():
        if k == target:
            continue
        for m in _REF.finditer(v):
            nums = [m.group(1)] + re.findall(r"\d+\.\d+", m.group(2) or "")
            if target in nums:
                ctx = v[max(0, m.start() - 70):m.end() + 25]
                # 内容を述べる語は参照の前にも後ろにも来る ("the purpose stated in Section 6.5" /
                #   "Section 6.5 states why it matters")。前だけを見た初版は後者を単なる指し先にした。
                _win = v[max(0, m.start() - 45):m.start()] + " " + v[m.end():m.end() + 35]
                out.append((k, ctx, bool(_DESCRIPTIVE.search(_win))))
    return out


# 文書をまたぐ依拠 (2026-11-04・bb の提案): 外した文を、ドシエの外向きの文書が引用・言い換えしていないか。
#   本文の中の参照だけを見ると、試作 h1 (§6.5 前半) は通るが、提出文 submission.md §B.0 がまさにその前半を
#   根拠に引いていた。条番号は版ごとにずれうる (1.0 §1.2 = 1.4 §1.3) ので、**外した文の 5 語の連なり**で
#   照合するのを主にし、条番号の形 ("§6.5 gives" / "Section 8.4's own text") は版の注意つきで補助に出す。
_ROOT = Path(__file__).resolve().parents[2]
_XDOC_SKIP = re.compile(r"(^|/)rounds/|CHANGELIST\.md$|CLARITY-TRIAL\.md$|ADVERSARIAL-TRIAGE\.md$")
# 理由を本文に帰す形。日本語の「§8.4 自身が述べ」も同じ依拠 (SUBMISSION-MATERIALS.md の表が実例)。
# 構造を自分の言葉で言い直すだけの文 (faq.md A8「because Covered Rights exclude patents」) は外した文に
# 依拠しないので拾わない —— §1.5 が特許を除くことは、理由の文を外しても真のまま。
_REASON_REF = (r"(?:§|Section )({n})(?!\d)(?:'s own text| gives| explains| states why|'s reason| says why|"
               r"\s*自身が述べ|\s*が述べる理由|\s*が理由を述べ)")


# 審査者・採用者に本文を説明する文書。外した文に依拠していれば、その版を対象にするとき書き換えが要る。
# それ以外 (errata / BLIND-SPOTS* / SELF-AUDIT / discussion-log / review-corpus 等) は当時の本文を引く記録で、
# 書き換えると履歴を偽る (#977 と同じ線引き) —— 出すが「記録」として分ける。
# against.md はファイル単位で外向き: 入口が審査者に読ませる全ラウンド通しの一覧で、版を付けない現在形の行
# (#133 "ours is stated in the licence itself") は出す版が変わると偽になる。行単位に分けないのは、日付の有無で
# 近似すると日付を含む #133 を落とすから —— 余分に拾う誤りは 1 行読めば済むが、見落としは偽の主張を提出する。
_OUTWARD = re.compile(r"(submission[^/]*|review-responses[^/]*|clause-reference|faq|comparison|against|objection-map|REVIEWERS|"
                      r"SUBMISSION-MATERIALS|READY-TO-SUBMIT|QUESTIONS-FOR-COUNSEL|README)\.md$")


def _toks(s: str) -> list[str]:
    return [w.strip(".,;:()\"'*_`—–").lower() for w in s.split() if w.strip(".,;:()\"'*_`—–")]


def _gram_list(text: str, k: int) -> list[str]:
    """文の中だけで作る。文をまたぐと、文末に語を足しただけの試作 i で "holds. Where" の連なりが「外した」になる。"""
    out = []
    for seg in re.split(r"(?<=[.;:!?])\s+", " ".join(text.split())):
        t = _toks(seg)
        out += [" ".join(t[i:i + k]) for i in range(len(t) - k + 1)]
    return out


def _grams(text: str, k: int) -> set[str]:
    return set(_gram_list(text, k))


def external_reliance(changed: dict[str, tuple[str, str]], after_all: str,
                      k: int = 5) -> list[tuple[str, int, str, str]]:
    """(file, line, 種類, 文脈)。changed = {条番号: (変更前の条, 変更後の条)}、after_all = 変更後の本文全体。

    照合する k 語の連なりは 2 段:
    - **強**: 変更前の条にあって、変更後の本文の**どこにも**無い句。常に出す。
    - **弱**: その条からは消えたが、本文の他所 (PREAMBLE や別の条) には残る句。**行がその条番号を名指すとき
      だけ**出す。名指さない引用は、本文に残る同じ句に依拠していると読める。
    比較の経緯 (2026-11-04): 文単位で比べると、文の前半を外したときに残った後半まで「外した」と数えた
    (初版で 29 件中ほぼ全部が誤検出)。強だけにすると試作 f の誤検出 8 件は消えたが、clause-reference.md の
    「| **8.4** | … 1.4 草案は "as to the Covered Rights" へ改めた」(本物の依拠・句は他の条にも在る) を落とした。
    """
    rest = _grams(after_all, k)
    grams = {}
    for sec, (b, a) in changed.items():
        gone = _grams(b, k) - _grams(a, k)
        for g in gone:
            grams[g] = (sec, g not in rest)
    out = []
    for f in sorted((_ROOT / "LICENSES").rglob("*.md")):
        rel = f.relative_to(_ROOT).as_posix()
        if _XDOC_SKIP.search(rel):
            continue
        for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            hit = None
            for g in _gram_list(line, k):
                if g in grams:
                    sec, strong = grams[g]
                    if strong or re.search(r"(?<![\d.])" + re.escape(sec) + r"(?![\d])", line):
                        hit = (g, sec, strong)
                        break
            if hit:
                g, sec, strong = hit
                tier = "外した語の引用" if strong else "条から外した語 (本文の他所に残る) を、条番号つきで引く"
                out.append((rel, ln, f"§{sec} {tier}: 「{g}」", line.strip()[:140]))
                continue
            for sec in changed:
                if re.search(_REASON_REF.format(n=re.escape(sec)), line):
                    out.append((rel, ln, f"§{sec} を根拠として指す (版の条番号に注意)", line.strip()[:140]))
                    break
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
    db, da = set(dangling(cb)), set(dangling(ca))
    print(f"# 先行詞の無い指示語: Before {len(db)} / After {len(da)}")
    for k, ctx in sorted(da - db):
        print(f"#   ⚠ 新たに宙に浮いた: §{k}: …{ctx}…")
    # 参照の宙づり (2026-11-04・25 の依頼): 内容が変わった条を参照している箇所を全部挙げる。
    #   参照先の内容を述べる形 ("the purpose stated in Section 6.5") は、外した文がまさにその内容だった
    #   可能性があるので、After の参照先にその内容が残っているかを人が読む。単なる指し先は件数だけ。
    _chg = [c for c in sorted(set(cb) | set(ca), key=lambda c: tuple(int(x) for x in c.split("."))) if cb.get(c) != ca.get(c)]
    _all = [(t, k, ctx, d) for t in _chg for k, ctx, d in refs_to(ca, t)]
    print(f"# 変更された条を参照する箇所: {len(_all)} (内容を述べる形 {sum(d for *_, d in _all)}) —— "
          "括弧の指し先も中身に依拠しうるので、全件を読む")
    for t, k, ctx, d in _all:
        print(f"#   {'⚠' if d else '・'} §{k} → §{t}: …{ctx}…")
    _xd = (external_reliance({c: (cb.get(c, ""), ca.get(c, "")) for c in _chg}, after.read_text(encoding="utf-8"))
           if _chg else [])
    _out = [x for x in _xd if _OUTWARD.search(x[0])]
    print(f"# 外した文に依拠するドシエの箇所 (LICENSES/*.md・rounds/ と作業記録を除く): {len(_xd)}"
          f" —— 外向き {len(_out)} (この版を対象にするなら書き換えが要る) / 記録 {len(_xd) - len(_out)}")
    for rel, ln, kind, ctx in sorted(_xd, key=lambda x: not _OUTWARD.search(x[0])):
        mark = "⚠ 外向き" if _OUTWARD.search(rel) else "・記録 "
        print(f"#   {mark} {rel}:{ln} [{kind}] {ctx}")
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


def guard(path: Path) -> int:
    """468u の目印 (効果を運ぶ句) が、草案や試作ファイルの該当条に在るかを出す。一覧は Check と同じ 1 か所から読む。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from checks_license_draft import EFFECT_MARKERS_468U
    cl = clauses(path.read_text(encoding="utf-8"))
    lack = [(s, mk) for s, mk in EFFECT_MARKERS_468U if mk not in cl.get(s, "")]
    print(f"# {path.name}: 468u の目印 {len(EFFECT_MARKERS_468U)} 件のうち欠けているもの {len(lack)} 件")
    for s, mk in lack:
        print(f"#   ⚠ §{s}: {mk!r}")
    return 1 if lack else 0


def uses(path: Path, terms: list[str]) -> int:
    """定義語ごとに、それを使う条と回数を出す (大文字小文字を区別・語の境界で数える)。

    定義を狭める試作 (例: §1.3 の "Work") の前に、到達範囲が変わりうる条を一覧にするため (2026-11-04・B15)。
    """
    cl = clauses(path.read_text(encoding="utf-8"))
    key = lambda c: tuple(int(x) for x in c.split("."))
    for t in terms:
        rx = re.compile(r"(?<![A-Za-z-])" + re.escape(t) + r"(?![A-Za-z-])")
        hits = [(c, len(rx.findall(v))) for c, v in sorted(cl.items(), key=lambda kv: key(kv[0])) if rx.search(v)]
        print(f"## {t!r}: {len(hits)} 条 / {sum(n for _, n in hits)} 回")
        print("- " + " / ".join(f"§{c} ×{n}" for c, n in hits))
    return 0


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--guard" and len(argv) == 2:
        return guard(Path(argv[1]))
    if argv and argv[0] == "--uses" and len(argv) >= 3:
        return uses(Path(argv[1]), argv[2:])
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
