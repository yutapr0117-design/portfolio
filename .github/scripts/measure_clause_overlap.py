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
  - 比較モード: **そろえ残し** —— 試作が A を「A and B」/「neither A nor B」へ増やしたとき、変わった条を参照する文や
    A を含む 3 つ以上の列挙で、A だけが残り B が無い文 (2026-11-15・T67 で §12.3 と §2.4 を人が見つけた型)
  - 比較モード: **前文の変化** —— 前文は作用しないが意図の判断に使われうるので、変わった文と、外した語を引くドシエの
    箇所を条と同じに出す (2026-11-15・T72 は前文だけを変え、条の比較が全部 0 になった)
  - 比較モード: **新しく入った全称の句** ("every other provision" など) と、同じ条が名指す条 —— 全称は同じ条が
    限定している条も呑む (2026-11-15・T70 の §5.3 で、50 が反例で見つけた型)
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
    python3 .github/scripts/measure_clause_overlap.py --sentences DRAFT.txt [N]   # 作用の条の長い文 (上位 N)
    python3 .github/scripts/measure_clause_overlap.py --sync BEFORE.txt AFTER.txt   # 採る commit で直す場所
    python3 .github/scripts/measure_clause_overlap.py --it-subject DRAFT.txt   # 主語が条・文書の文の中の it / its
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
    # 約束 (§5・§8.6・§12) が「しない」と定める行為 (2026-11-15・9b): T64 が §5.2(a) から "apply, or" を外し、
    #   DRM を「かけない」約束が消えたが、この語彙に無かったので --compare は減った語として出さなかった
    "約束が止める行為": ["apply", "assert", "invoke", "impose", "enforce", "seek", "bring", "claim", "sue",
                  "restrict", "require", "condition", "terminate", "revoke", "withdraw", "charge", "object"],
}


def body(text: str) -> str:
    return text.split(SEP, 1)[1] if SEP in text else text


def clauses(text: str) -> dict[str, str]:
    return {k: " ".join(v.split()) for k, v in CLAUSE_RX.findall(body(text))}


def preamble(text: str) -> str:
    """本文の区切り線の後、最初の節の見出し (`1. DEFINITIONS`) の前 —— 題名と前文 (空白を 1 つに)。"""
    b = body(text)
    m = re.search(r"^1\. [A-Z]", b, re.M)
    return " ".join((b[:m.start()] if m else "").split())


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


# 先行詞が動きうる代名詞 (2026-11-12・portfolio-aa の依頼): T56 は E71 で直前の文を複数形にした結果、§8.6 の "them" の
#   先行詞が「許諾」と読める側へ動いた型だった。文そのものが変わったか、直前の文が変わった文の代名詞を挙げる。
#   先行詞を決めるのは読む人で、道具は読む場所を絞るだけ (It の形式主語なども出る)
_PRONOUN = re.compile(r"\b(they|them|their|theirs|it|its|those|these|such)\b", re.I)
_SENT = re.compile(r"(?<=[.;:])\s+(?=[A-Z(])")


# 比較・照応の相手を前に求める句と、許可の声 (2026-11-12・portfolio-00 の報告): T59 の "to the same extent" は比較の相手が
#   書かれず 2 通りに読めた。T57 の "Such distribution by the Steward is permitted" は制限の例外から許可の付与へ声が変わった
_COMPARE = re.compile(r"\b(?:the same|same|such|similar(?:ly)?|likewise|equally|correspondingly|to that extent|to the same extent|"
                      r"as aforesaid|thereof|therein|thereto)\b", re.I)
# may は許可を与える声だけを数える。比較の句 ("as a notice may identify …"・T69) と、関係節・名詞節の中の may
#   ("what may be done with any copy"・T65 / "in which they hold or may hold rights"・§16.3) は何も許していないので数えない
#   (2026-11-15・3 つとも誤検知だった。1.3 → 1.4 草案の全差分で 3 → 0 件、T57 の "is permitted" は引き続き数える)
_PERMIT = re.compile(r"\b(?:is|are) (?:permitted|allowed|entitled|authori[sz]ed)\b|(?<!\bwhat )(?<!\bwhich )(?<!\bor )\bmay\b", re.I)
_AS_MAY = re.compile(r"\bas (?:an? |the )?\w+(?: \w+)? may\b", re.I)


def permit_count(s: str) -> int:
    """許可の声の数。比較の句 "as <名詞句> may …" を先に外してから数える。"""
    return len(_PERMIT.findall(_AS_MAY.sub(" ", s)))


def changed_sentences(cb: dict[str, str], ca: dict[str, str]) -> list[tuple[str, str]]:
    """(条, 文)。After の文のうち Before の同じ条に無い文。"""
    out = []
    for c in ca:
        if cb.get(c) == ca[c]:
            continue
        sb = {" ".join(x.split()) for x in _SENT.split(" ".join(cb.get(c, "").split()))}
        out += [(c, x) for x in (" ".join(y.split()) for y in _SENT.split(" ".join(ca[c].split()))) if x and x not in sb]
    return out


def pronoun_shift(cb: dict[str, str], ca: dict[str, str]) -> list[tuple[str, str, str, str]]:
    """(条, 代名詞, 文の抜粋, 理由)。理由は「文が変わった」か「直前の文が変わった」。"""
    out = []
    for c in ca:
        if cb.get(c) == ca[c]:
            continue
        sb = [" ".join(x.split()) for x in _SENT.split(" ".join(cb.get(c, "").split())) if x.strip()]
        sa = [" ".join(x.split()) for x in _SENT.split(" ".join(ca[c].split())) if x.strip()]
        for j, sent in enumerate(sa):
            if sent not in sb:
                why = "文が変わった"
            else:
                i = sb.index(sent)
                prev_b, prev_a = (sb[i - 1] if i else None), (sa[j - 1] if j else None)
                if prev_b == prev_a:
                    continue
                why = "直前の文が変わった"
            for m in _PRONOUN.finditer(sent):
                out.append((c, m.group(0), sent[max(0, m.start() - 50):m.end() + 30], why))
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
                      r"SUBMISSION-MATERIALS|READY-TO-SUBMIT|QUESTIONS-FOR-COUNSEL|QUESTION-INDEX|README|ADOPTING)\.md$")  # QUESTION-INDEX は 2026-11-23 (cd の報告)


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


def sibling_overlap(cb: dict[str, str], ca: dict[str, str], k: int = 4) -> list[tuple[str, str, str, str]]:
    """(変えた条, 同じ節の他の条, 句, 他の条の文脈)。変えた条に新しく入った k 語の連なりで、同じ節 (§N.x) の変えていない条にも在るもの。

    T82 (2026-11-16) は §14.1 に「法が除外を許さない責任 … は第 14 節の何物も制限しない」を足し、同じ節の §14.2 の「法が除外または
    制限を許さない責任は、法の許す限り制限する」と同じ対象に逆を言った。機械の網はどれも緑で、人の読みで見つけた。同じ限定の句
    (applicable law does not permit …) を同じ節の 2 つの条が持つときに出す。機能語だけの連なりは除く。"""
    out = []
    for c, a in ca.items():
        if cb.get(c) == a or "." not in c:
            continue
        new = _grams(a, k) - _grams(cb.get(c, ""), k)
        top = c.split(".")[0]
        for s, other in ca.items():
            if s == c or s.split(".")[0] != top or cb.get(s) != other:
                continue
            for g in sorted(new & _grams(other, k)):
                if sum(w not in _FUNCTION_WORDS and len(w) >= 3 and w not in ("the", "and", "any", "for") for w in g.split()) < 2:
                    continue
                i = " ".join(other.split()).lower().find(g.split()[0])
                out.append((c, s, g, " ".join(other.split())[max(0, i - 30):i + 90]))
    # 同じ (条, 他の条) の組は最初の 3 句まで (長い句は 4 語の連なりが重なって並ぶ)
    seen, res = {}, []
    for x in out:
        seen[(x[0], x[1])] = seen.get((x[0], x[1]), 0) + 1
        if seen[(x[0], x[1])] <= 3:
            res.append(x)
    return res


_FUNCTION_WORDS = {"which", "that", "this", "with", "from", "into", "upon", "than", "when", "where", "there", "those", "these",
                   "their", "they", "them", "what", "whom", "whose", "have", "been", "were", "will", "would", "does", "under",
                   "over", "about", "after", "before", "only", "also", "such", "each", "every", "other", "against", "within",
                   # 接続詞も機能語に入れる (2026-11-16・T77): "reaches, because it was never …" の "because it" が、ドシエの
                   #   無関係な "because Section 16.3 …" に 4 件当たった。接続詞の後の名詞は言い換えの手がかりにならない
                   "because", "since", "unless", "while", "though", "although", "whether", "where", "once"}


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
    # 外した句の代名詞を先行詞へ置き換えた言い換え (2026-11-12・portfolio-aa が T56 で見つけた穴): 記録は
    #   "alongside them" を "alongside the licences" と書く。代名詞の直前の語 + (冠詞) + 変更前の条にある複数名詞
    _pron = {}
    for sec, (b, a) in changed.items():
        nouns = {w.rstrip("s") for w in _toks(b) if len(w) >= 6 and w.isalpha()}   # 単数でも複数でも当てる
        for g in _grams(b, 3) - _grams(a, 3):
            t = g.split()
            # 直前が機能語 (which / that / with …) だと、その語に続く任意の名詞に当たって雑音になる (T60 の "through which it" で 25 件)
            if (t[-1] in ("them", "it", "those", "they", "these") and len(t[-2]) >= 4 and nouns
                    and t[-2] not in _FUNCTION_WORDS):
                _pron[re.compile(r"\b" + re.escape(t[-2]) + r" (?:the |those |these |its |their )?(?:"
                                 + "|".join(map(re.escape, sorted(nouns))) + r")s?\b", re.I)] = (sec, g)
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
            else:
                for rx, (sec, g) in _pron.items():
                    m = rx.search(line)
                    if m:
                        out.append((rel, ln, f"§{sec} 外した「{g}」の代名詞を解いた言い換え: 「{m.group(0)}」", line.strip()[:140]))
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


# 冠詞を両方に持つ対だけを見る ("the covenant and the consent" / "neither the covenant nor the consent")。冠詞の無い
#   並び ("the scale of use, and the number of users") は偶然の隣り合わせで、1.3 → 1.4 草案で 23 件の誤検知を出した
_PAIR = re.compile(r"\bthe ([a-z]+) (?:and|or|nor) the ([a-z]+)\b")
_STOP = {"the", "a", "an", "any", "this", "that", "of", "to", "in", "or", "and", "nor", "by", "for", "is", "it", "its"}


def coordination_gaps(cb: dict, ca: dict) -> list[tuple[str, str, str, str]]:
    """試作が「A」を「A and B」/「neither A nor B」へ増やしたとき、本文の他の場所に A だけが残る文 (そろえ残し)。

    2026-11-15、T67 は §12.2 に consent を足し §12.4 / §12.5 を "the covenant and the consent" に揃えたが、§12.3 の
    "The covenant in Section 12.2 is limited to the Work" と §2.4 の列挙 "grant, permission, and covenant" が残った
    (9b と 30 が人の目で見つけた)。語を 1 か所だけ揃えると、揃えていない場所との対比が「B は含まれない」と読ませる。
    候補は 2 種: (i) A と、B を足した条への参照 ("Section 12.2") を同じ文に持ち B を持たない文、(ii) A を含む 3 つ以上の
    列挙 ("x, y, and A") で B を持たない文。どちらも読む候補であって欠陥の証拠ではない。
    返り値: [(条, A, B, 文の抜粋)]
    """
    new_pairs = set()
    for k in ca:
        if ca[k] == cb.get(k):
            continue
        for m in _PAIR.finditer(ca[k].lower()):
            a, b = m.group(1), m.group(2)
            if a in _STOP or b in _STOP or a == b:
                continue
            before = cb.get(k, "").lower()
            if re.search(rf"\b{a}\b", before) and not re.search(rf"\b{a}\b (?:and|or|nor) (?:the |any )?{b}\b", before):
                new_pairs.add((a, b, k))
    out = []
    changed = [k for k in ca if ca[k] != cb.get(k)]
    for a, b in sorted({(a, b) for a, b, _k in new_pairs}):
        # 試作で変わった条のどれかを参照する文 (B は §12.2 に動詞で入り、対の形は §12.4 / §12.5 に在った)
        ref = re.compile(r"\bsections? (?:[\d.]+(?:, | and | or ))*(?:" + "|".join(re.escape(c) for c in changed) + r")\b")
        for k, text in ca.items():
            for s in re.split(r"(?<=[.;:])\s+(?=[A-Z(])", text):
                sl = s.lower()
                if not re.search(rf"\b{a}s?\b", sl) or re.search(rf"\b{b[:-1] if b.endswith('s') else b}", sl):
                    continue
                listed = re.search(rf"(?:\b[a-z]+, ){{2,}}(?:and |or )?{a}s?\b|\b{a}s?, (?:[a-z]+, )+(?:and |or )?[a-z]+\b", sl)
                if (ref.search(sl) and not re.search(rf"\b{a}\b (?:and|or|nor) (?:the |any )?{b}", sl)) or listed:
                    item = (k, a, b, " ".join(s.split())[:140])
                    if item not in out:
                        out.append(item)
    return out


_UNIVERSAL = re.compile(r"\b(?:every|each|any|all|no)(?: other)? (?:provision|section)s?\b(?: of this dedication)?|\bnothing in this dedication\b", re.I)
_SECTIONS = re.compile(r"\bSections? (\d+(?:\.\d+)?(?:(?:, (?:and |or )?| and | or | to )\d+(?:\.\d+)?)*)")
_EXCEPT = re.compile(r"\b(?:other than|save that|except|excluding|apart from)\b", re.I)


def universal_scope(cb: dict[str, str], ca: dict[str, str]) -> list[tuple[str, str, list[str], bool, str]]:
    """変わった文に新しく入った全称の句 ("every other provision" / "nothing in this Dedication" …) と、同じ条が名指す条。

    2026-11-15、T70 は §5.3 末文の列挙 "Sections 3, 4, 8.1, and 8.4 operate in their favour independently of this
    Section" を "Every other provision of this Dedication operates …" へ一般化した。"other" が外すのは §5.3 自身だけで、
    §5.3 が縛る約束 (§5.1・§5.2・§8.6) も「他の条」に入り、「この条と独立に働く」と読めた (50 の反例・ab54c5a5 で
    "other than those covenants" へ直した)。全称は同じ条が限定している条も呑むので、同じ条が名指す条を並べて人が読む。
    返り値: [(条, 全称の句, 同じ条が名指す条, 除外の句が同じ文に在るか, 文の抜粋)]
    """
    out = []
    for k, s in changed_sentences(cb, ca):
        before_hits = {m.group(0).lower() for m in _UNIVERSAL.finditer(" ".join(cb.get(k, "").split()))}
        for m in _UNIVERSAL.finditer(s):
            if m.group(0).lower() in before_hits:
                continue
            named = sorted({x for g in _SECTIONS.findall(" ".join(ca[k].split()))
                            for x in re.findall(r"\d+(?:\.\d+)?", g)} - {k},
                           key=lambda c: tuple(int(x) for x in c.split(".")))
            out.append((k, m.group(0), named, bool(_EXCEPT.search(s)), s[max(0, m.start() - 40):m.end() + 60]))
    return out


_ALL_PROVISIONS = re.compile(r"\b(?:every|each|all)(?: other)? (?:provision|section)s?\b", re.I)


def universal_mark(w: str, named: list[str], exc: bool) -> tuple[str, str]:
    """全称の句の印。⚠ は肯定の全称 (every / each / all) が
    "provision" / "Section" という**型を問わない名詞**を量化する —— 除外の句があっても、免責 (§13)・責任の制限 (§14)・
    文書の規律 (§16.4) まで入る (1c の提案・2026-11-15。T70 の 3 つ目の形 "Every provision … other than those
    covenants operates in their favour" は除外の句を持ったまま §13・§14・§16.4 を「受領者のために働く」と述べ、30 の反例で
    退けた・#3196)。除外の句が無く同じ条が名指す条があれば、それも入ることを添える (T70 の 2 つ目の形)。否定の全称
    ("Nothing in this Dedication …"・"any other Section" が "Nothing" の下にある形) は「減らさない」「求めない」を
    述べるので「・」。1.0〜1.3 と 2026-11-15 の草案に ⚠ の形は 0 件。"""
    if _ALL_PROVISIONS.fullmatch(w.split(" of this")[0].strip()):
        return "⚠", "全条を量化 —— 免責・責任の制限・文書の規律も含む" + ("" if exc else "・同じ条が名指す条も入る" if named else "")
    # (a) は肯定の全称だけに当てる: 草案の 121 commit を照らすと、否定の下の any (§11.1 "Nothing in this Section reduces
    #   what any other Section … gives"・b9966b06) が (a) の唯一の ⚠ で、1c の見立てどおり無害だった
    return "・", ""


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
    _cs = changed_sentences(cb, ca)
    _cmp = [(k, m.group(0), sent[max(0, m.start() - 50):m.end() + 40]) for k, sent in _cs for m in _COMPARE.finditer(sent)]
    print(f"# 変わった文の比較・照応の句 (相手が書かれているか読む): {len(_cmp)}")
    for k, w, ctx in _cmp:
        print(f"#   ・ §{k} {w!r}: …{ctx}…")
    _pv = [(k, permit_count(cb.get(k, "")), permit_count(ca[k])) for k in ca if cb.get(k) != ca[k]]
    _pv = [x for x in _pv if x[2] > x[1]]
    print(f"# 許可の声 (is permitted / may / is entitled …) が増えた条: {len(_pv)} (制限の例外が許可の付与へ変わっていないか読む)")
    for k, b_, a_ in _pv:
        print(f"#   ⚠ §{k}: {b_} → {a_}")
    _ps = pronoun_shift(cb, ca)
    print(f"# 文が変わったか直前の文が変わった文の代名詞: {len(_ps)} (先行詞を読み直す・形式主語の it も出る)")
    for k, w, ctx, why in _ps:
        print(f"#   ・ §{k} [{why}] {w!r}: …{ctx}…")
    # 参照の宙づり (2026-11-04・25 の依頼): 内容が変わった条を参照している箇所を全部挙げる。
    #   参照先の内容を述べる形 ("the purpose stated in Section 6.5") は、外した文がまさにその内容だった
    #   可能性があるので、After の参照先にその内容が残っているかを人が読む。単なる指し先は件数だけ。
    _chg = [c for c in sorted(set(cb) | set(ca), key=lambda c: tuple(int(x) for x in c.split("."))) if cb.get(c) != ca.get(c)]
    _all = [(t, k, ctx, d) for t in _chg for k, ctx, d in refs_to(ca, t)]
    print(f"# 変更された条を参照する箇所: {len(_all)} (内容を述べる形 {sum(d for *_, d in _all)}) —— "
          "括弧の指し先も中身に依拠しうるので、全件を読む")
    for t, k, ctx, d in _all:
        print(f"#   {'⚠' if d else '・'} §{k} → §{t}: …{ctx}…")
    _cg = coordination_gaps(cb, ca)
    print(f"# そろえ残し (A を「A and B」へ増やした試作で、A だけが残る文): {len(_cg)} —— 揃えていない場所は"
          "「B は含まれない」と読ませうる (2026-11-15・T67 の §12.3 と §2.4)")
    for k, a, b, ctx in _cg:
        print(f"#   ⚠ §{k} [{a} だけ・{b} が無い]: …{ctx}…")
    _sib = sibling_overlap(cb, ca)
    print(f"# 新しく入った句と、同じ節の他の条が持つ同じ句 (4 語の連なり): {len(_sib)} —— 同じ対象に 2 つの条が別のことを"
          "言っていないか読む (2026-11-16・T82 の §14.1「NOTHING IN SECTION 14 LIMITS」と §14.2 の「limited to the greatest extent」)")
    for k, s, g, ctx in _sib:
        print(f"#   ・ §{k} の新しい句「{g}」は §{s} にも在る: …{ctx}…")
    _us = universal_scope(cb, ca)
    print(f"# 新しく入った全称の句 (every other provision / nothing in this Dedication …): {len(_us)} —— 肯定の全称が"
          "条を量化すると、免責・責任の制限・文書の規律と、同じ条が限定する条も呑む (2026-11-15・T70 の §5.3)")
    for k, w, named, exc, ctx in _us:
        mark, why = universal_mark(w, named, exc)
        print(f"#   {mark} §{k} {w!r} (同じ条が名指す条: {', '.join('§' + x for x in named) or '無し'}"
              f"{'・除外の句あり' if exc else ''}{'・' + why if why else ''}): …{ctx}…")
    # 前文 (2026-11-15・1c の T72 で見えた穴): 前文は作用の条ではない (*"This preamble is not, and nothing in it qualifies
    #   them"*) が、意図の判断に使われる (review-readings-6 §1.450・Nelson 氏 2002)。条だけを比べると、T72 のように前文だけを
    #   変えた試作は全項目 0 になり、前文の語を引くドシエの箇所も出なかった。前文を擬似の条「前文」として比べる
    pb, pa = preamble(before.read_text(encoding="utf-8")), preamble(after.read_text(encoding="utf-8"))
    if pb != pa:
        _sb = set(_SENT.split(pb))
        _new = [s for s in _SENT.split(pa) if s and s not in _sb]
        print(f"# 前文が変わった: {len(words(pb))} → {len(words(pa))} 語・変わった文 {len(_new)} (前文は作用しないが、意図の判断に使われうる)")
        for s in _new:
            print(f"#   ・ 前文: …{s[:150]}…")
    _pre = {"前文": (pb, pa)} if pb != pa else {}
    _xd = (external_reliance({**{c: (cb.get(c, ""), ca.get(c, "")) for c in _chg}, **_pre}, after.read_text(encoding="utf-8"))
           if _chg or _pre else [])
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
    """468u の目印 (効果を運ぶ句) が該当条に在るか、468r の「いまの状態」の語が条に無いかを、草案や試作ファイルに
    当てて出す。一覧は Check と同じ 1 か所 (_lib_draft_markers.py) から読む (468r は 2026-11-12 に足した)。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_draft_markers import EFFECT_MARKERS_468U, gap_losses, state_hits
    from _lib_draft_counts import with_changes
    _txt = with_changes(path)  # 外へ出した変更の一覧も冒頭として読む (2026-11-20・案 A の準備)
    cl = clauses(_txt)
    lack = [(s, mk) for s, mk in EFFECT_MARKERS_468U if mk not in cl.get(s, "")]
    print(f"# {path.name}: 468u の目印 {len(EFFECT_MARKERS_468U)} 件のうち欠けているもの {len(lack)} 件")
    for s, mk in lack:
        print(f"#   ⚠ §{s}: {mk!r}")
    hits, miss = state_hits(cl)
    print(f"# {path.name}: 468r の「いまの状態」の語 {len(hits)} 件・条に無い除外の句 {len(miss)} 件")
    for s, w in hits:
        print(f"#   ⚠ §{s}: {w!r}")
    for s, x in miss:
        print(f"#   ⚠ 除外の句が §{s} に無い: {x!r}")
    # 468d の gap の目印も当てる (2026-11-16): 試作が §6 / §9 の中身か §8.4 の gap 語を落とすと、merge の後に 468d が RED に
    #   なるまで気付かなかった
    gone = gap_losses(_txt.split("-" * 80, 1)[-1])
    print(f"# {path.name}: 468d の gap の目印のうち消えたもの {len(gone)} 件")
    for g in gone:
        print(f"#   ⚠ {g}")
    # 冒頭の変更一覧の箇条に書いた理由の句 (2026-11-16・1c の依頼): 一覧の前置きは「理由は CHANGELIST に在る」と言い、
    #   1c が 17 の理由の句を外して 917 → 894 行にした。試作の箇条に so that / since / because を書くとまた伸びる。
    #   引用符の中 (本文の語) は数えない。結果を述べる so that もあるので、読む候補として出すだけ (止めない)
    _hdr = _txt.split("-" * 80, 1)[0] if "-" * 80 in _txt else ""
    _bul = re.findall(r"^    \* (.*(?:\n      .*)*)", _hdr, re.M)
    _why = [(re.sub(r"\s+", " ", b)[:70], m.group(0)) for b in _bul
            for m in re.finditer(r"\b(?:so that|since|because|in order to|which was untrue|which could be read)\b",
                                 re.sub(r'"[^"]*"', '""', re.sub(r"\s+", " ", b)), re.I)]
    print(f"# {path.name}: 冒頭の箇条の理由の句 {len(_why)} 件 (理由は CHANGELIST へ・結果を述べる so that は残してよい)")
    for head, w in _why:
        print(f"#   ・ {w!r}: {head}")
    return 1 if lack or hits or miss or gone else 0


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


def sentences(path: Path, top: int = 15) -> int:
    """作用の条の文を語数の多い順に出す (2026-11-12・portfolio-aa の依頼: 長文を分ける試作の起点)。"""
    rows = []
    for c, v in clauses(path.read_text(encoding="utf-8")).items():
        for sent in _SENT.split(" ".join(v.split())):
            rows.append((len(sent.split()), c, sent))
    rows.sort(key=lambda r: -r[0])
    print(f"# {path.name}: 作用の条の文 {len(rows)} 文・上位 {top} (語数は split())")
    for n, c, sent in rows[:top]:
        print(f"  {n:3d} 語  §{c}: {sent[:110]}{'…' if len(sent) > 110 else ''}")
    return 0


def it_subject(path: Path) -> int:
    """主語が条や文書 (Section N / This Section / This Dedication / Nothing in …) の文の中の it / its を全数出す
    (2026-11-12・portfolio-aa の T60 の型: 文の主語と違うもの —— Dedicator や Work —— を指す it)。先行詞は読む人が決める。"""
    rows = []
    subj = re.compile(r"^(?:Sections? \d|This Section|This Dedication|Nothing in (?:this|Section)|Section \d)")
    for c, v in clauses(path.read_text(encoding="utf-8")).items():
        for sent in _SENT.split(" ".join(v.split())):
            if subj.match(sent):
                rows += [(c, m.group(0), sent[max(0, m.start() - 50):m.end() + 30]) for m in re.finditer(r"\b(?:it|its)\b", sent)]
    print(f"# {path.name}: 主語が条・文書の文の中の it / its: {len(rows)}")
    for c, w, ctx in rows:
        print(f"  §{c} {w!r}: …{ctx}…")
    return 0


def sync(before: Path, after: Path) -> int:
    """試作を採る commit で直す場所を出す (2026-11-12・portfolio-aa の依頼)。

    冒頭の "This draft:"・変わった条を名指す CHANGELIST / 逐条の下書き / errata の行・変更前の総語数を書いた行。
    出すのは場所で、直すかどうか (記録として残す行もある) は読む人が決める。
    """
    tb, ta = before.read_text(encoding="utf-8"), after.read_text(encoding="utf-8")
    cb, ca = clauses(tb), clauses(ta)
    chg = [c for c in sorted(set(cb) | set(ca), key=lambda c: tuple(int(x) for x in c.split("."))) if cb.get(c) != ca.get(c)]
    sep = "-" * 80
    wb, wa = (len((t.split(sep, 1)[1] if sep in t else t).split()) for t in (tb, ta))
    print(f"# 変わった条: {', '.join('§' + c for c in chg) or 'なし'}・題名から END までの語数 {wb} → {wa}")
    m = re.search(r"This draft: [\d,]+ words, \d+ clauses", ta)
    print(f"  冒頭: {m.group(0) if m else '(This draft の行が無い)'} → {wa:,} words に")
    print("  CHANGELIST: 主表に行を足し、費用の内訳 (Check 468s が照合) を直す。試作の節に採否を書く")
    for f in sorted((_ROOT / "LICENSES").glob("*-CLAUSE-REFERENCE-DRAFT.md")):
        for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            hit = [c for c in chg if line.startswith(f"| **{c}**")]
            if hit:
                print(f"  逐条の下書き {f.name}:{ln} [§{hit[0]}] {line.strip()[:100]}")
    # 変わった条を名指す、いまの草案を述べる外向きの文書の行 (2026-11-15・9b)。T67 で §12.2 を変えたあと、材料 §1b の
    #   「§12.2（放棄できない法域での不行使）」が古いまま残り、50 が手で拾った (#3144)。条の中身の言い換えは機械で正誤を
    #   決められないので、読み直す候補として出す。ACD-1.0.* は 1.0 を述べる文書なので出さない
    cur = ("SUBMISSION-MATERIALS.md", "REVIEWERS.md", "READY-TO-SUBMIT.md", "QUESTIONS-FOR-PRACTITIONERS.md", "ADOPTING.md",
           "OSI-APPROVAL-PLAN.md")
    docs = [f for f in sorted((_ROOT / "LICENSES").glob("*.md")) if f.name in cur or f.name.startswith("ACD-OSI-BOTTLENECKS")]
    rx = re.compile(r"(?:§|Section |Sections? (?:[\d.]+, )*)(" + "|".join(re.escape(c) for c in chg) + r")(?![\d.]\d)") if chg else None
    hits = [(f.name, ln, line) for f in docs for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1)
            if rx and rx.search(line)]
    print(f"  変わった条を名指す外向きの行 (読み直す候補・{len(hits)} 行): いまの草案を述べる文書だけ")
    for name, ln, line in hits[:40]:
        print(f"    {name}:{ln} {line.strip()[:110]}")
    if len(hits) > 40:
        print(f"    … ほか {len(hits) - 40} 行")
    pats = {f"{wb:,}", str(wb)}
    for f in sorted((_ROOT / "LICENSES").glob("*.md")):
        for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if any(re.search(r"(?<![\d,])" + re.escape(p) + r"(?![\d,])", line) for p in pats):
                print(f"  語数 {wb:,} を書いた行: {f.name}:{ln} {line.strip()[:100]}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    if argv and argv[0] == "--guard" and len(argv) == 2:
        return guard(Path(argv[1]))
    if argv and argv[0] == "--uses" and len(argv) >= 3:
        return uses(Path(argv[1]), argv[2:])
    if argv and argv[0] == "--sentences" and len(argv) in (2, 3):
        return sentences(Path(argv[1]), int(argv[2]) if len(argv) == 3 else 15)
    if argv and argv[0] == "--it-subject" and len(argv) == 2:
        return it_subject(Path(argv[1]))
    if argv and argv[0] == "--sync" and len(argv) == 3:
        return sync(Path(argv[1]), Path(argv[2]))
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
