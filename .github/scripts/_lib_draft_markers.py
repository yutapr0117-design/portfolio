"""_lib_draft_markers.py — 次版の草案の条に当てる一覧と、その当て方 (Check 468u / 468r と measure_clause_overlap.py --guard が共有)。

一覧は 1 か所に置く: Check と試作の道具が別々に持つと食い違う (468u の初版の取り決め)。2026-11-12 に
checks_license_draft.py から移した (468r を足すと Check の module が行の予算 900 を越えるため。読み手は 2 つ)。
"""
import re

# 適用の通知を定める条・本文の再頒布を定める条は、番号でなく書き出しの文で探す (2026-11-24: 1.5 の書き直しで §16.1 → §10.1、
#   §16.4 → §10.5 へ動き、番号を直書きした 7 か所が一度に外れた)。凍結版 (1.0〜1.4) と作業中の版が同じ関数で読める。
NOTICE_LEAD = "To apply this Dedication"
TEXT_RULE_LEADS = ("The text of this Dedication may be copied", "Anyone may copy and distribute this text")


def clause_by_lead(text, leads):
    """書き出しが leads のどれかに一致する条の (番号, 条の原文 [次の条の手前まで])。無ければ (None, "")。"""
    for m in re.finditer(r"(?ms)^  (\d+\.\d+) (.*?)(?=^  \d+\.\d+ |^\d+\. [A-Z]|^END OF TERMS|\Z)", text):
        if " ".join(m.group(2).split()).startswith((leads,) if isinstance(leads, str) else leads):
            return m.group(1), m.group(0)
    return None, ""


# 468u の目印 (条, 句)。checks_license_draft.py (Check 468u) と measure_clause_overlap.py --guard が同じ一覧を import して
# 試作ファイルに当てる (2 か所に持つと食い違う)。2026-11-24 に 1.5 の書き直し (議題 15) の番号と文へ付け替えた ——
# 左が旧い目印 (1.4 の条)、右が同じ働きを運ぶ 1.5 の文。付け替え先の無い目印は無い。
EFFECT_MARKERS_468U = (
    # 1.4 §5.3・§12.4・§2.8 (承継と限度が 1 つ) / §2.9 の "under its terms" (T89)
    ("7.2", "to the fullest extent the law permits"),
    ("7.2", "after the Dedicator's death"),
    ("7.3", "Under its terms, nothing this Dedication gives"),
    # 1.4 §15.5
    ("1.12", '"person" includes an entity'),
    # 1.4 §8.4 (§6.4 の成果物の定義を含む): 因果で限り、量で限らない
    ("1.8", "in each case resulting, directly or indirectly, from automated processing of the Work"),
    ("1.8", "A copy of the Work in any form, including object code compiled from it and a copy contained in a Result, is not itself a Result"),
    ("2.3", "in whole or in part, from the content of the Work"),
    ("2.3", "however much or little of it was used"),
    ("2.3", "teaches or embodies is treated as resulting from that content"),
    ("2.3", "that a modified version of the Work has, and that the Work itself did not teach or embody, is governed by paragraph (a) alone"),
    # 1.4 §8.1 (T16〜T20)・§8.3・§8.5
    ("2.3", "otherwise practise or transfer the Work, anything derived from it, and any Result"),
    ("2.3", "caused by subject matter in the Work, including, where the Work is a Contribution, by its combination with the material it was submitted for inclusion in"),
    ("1.7", "if, and only if"),
    # 1.4 §8.2・§10.4: 特許訴訟でも終わらない
    ("4.1", "for any reason, including litigation by You against anyone"),
    # 1.4 §4.6・§5.3: 受け手は Dedicator から直接
    ("2.4", "from anyone, holds them directly from the Dedicator"),
    # 1.4 §5.1・§5.2(d)・§8.6・§12.2: 第三者を通じた主張と、行使 (T115)
    ("2.5", "not to authorise or assist any other person to assert or exercise"),
    ("2.5", "any Patent Claim that Section 2.3 reaches"),
    ("2.5", "as wrongful, or as without legal basis, whether by reason of its being a use of the Work"),
    ("2.5", "that another person holds through the Dedicator"),
    ("5.4", "Sections 2.5(d) and 5.1 do not reach"),
    ("5.5", "Sections 2.5(d), 5.1, and 5.2 do not reach"),
    ("5.4", "claim for patent infringement outside what Section 2.3 reaches"),
    # 1.4 §5.2 末段 (E67)
    ("5.5", "rights in material, other than the Work, that the Dedicator makes or makes available, including a Result"),
    ("5.5", "to a service through which the Dedicator runs the Work for others"),
    ("5.6", "nothing in Section 5.5 lets the terms it names restrict what may be done with that copy"),
    ("6.2", "does not restrict nominative reference, including stating truthfully"),
    ("6.3", "accompanied or was contained in the Work"),
    ("9.2", "invalid or unenforceable"),
    # 1.4 §2.4・§8.6・§12.2 の独立 (E18 / E26 / E42)
    ("2.7", "cumulatively, for every jurisdiction, and to the fullest extent the law permits, whether or not another is effective"),
    ("2.7", "need not determine which of them is effective"),
    # 1.4 §12.2・§11.4: 下流の受け手まで / 約束と与えないものの境
    ("2.6", "anyone who receives the Work or anything derived from it"),
    ("6.4", "Section 2.5(d) is a promise not to assert; it grants no such permission"),
    ("6.5", "nothing in it reduces what any other Section gives"),
    # 1.4 §10.1 (T120)・§2.6 (T116)・§14.2
    ("4.1", "other than in Your capacity as a Dedicator"),
    ("10.4", "That undertaking binds that Dedicator, is subject to Section 8.2, and imposes nothing upon You"),
    ("8.2", "TO THE FULLEST EXTENT THE LAW PERMITS"),
    ("8.2", "that the law does not permit to be limited"),
    # 1.4 §15.2 (T129)・§16.3 (E2)
    ("9.2", "treated as severed there only"),
    ("10.3", "rights of their own"),
    ("10.3", "the authors of this Dedication"),
    # 1.4 §16.2 (T109・H-02・REUSE の粒度)
    ("10.2", "sufficient notice of this Dedication"),
    ("10.2", "applies this Dedication to the material it identifies"),
    ("10.2", "in a comment within a file"),
    # errata E90: 他人の notice を渡す・記録する・名を挙げるだけでは適用でない
    ("10.2", "nor mentioning this Dedication otherwise than to apply it, applies it to anything"),
    # 回帰で閉じた句 (5.4 の列)
    ("5.4", "a term about a Contribution, other than one restricting use of the Work, asked of the person submitting it"),
)

# 468r の語と除外 (条, 句)。除外は語ではなく句で持つ: 同じ語を別の構文で使えば鳴り、句を書き換えたら読み直しの合図になる。
#   語の一覧に無い言い方 (remains to be seen など) は漏れる。前文は作用の条ではないので対象外 (確定の日に読み直す)
STATE_WORDS_468R = (r"unresolved|unsettled|uncertain|currently|presently|at present|today|in practice|has proved|is unclear"
                    r"|not yet|so far|now fails|increasingly|in most jurisdictions|common use|remains? open|open question"
                    r"|undecided|not (?:been )?(?:settled|decided)|to date|at the time of writing|for now|recent(?:ly)?|nowadays|still")
STATE_EXEMPT_468R = (
    ("5.4", "so far as they impose nothing"), ("4.1", "so far as Section 7.2 binds You"), ("5.3", "so far as the law allows"), ("7.4", "so far as the law permits"),  # 範囲の語
    ("1.6", "whether or not presently known or subsisting"),   # 範囲の語
)


def state_hits(clauses):
    """468r: {条: 本文} から (「いまの状態」の語の出現 [(条, 語)], 条に無い除外の句 [(条, 句)])。空白は畳んで読む。"""
    miss = [(c, x) for c, x in STATE_EXEMPT_468R if x.lower() not in " ".join(clauses.get(c, "").split()).lower()]
    hits = []
    for c, body in clauses.items():
        f = " ".join(body.split())
        for cx, x in STATE_EXEMPT_468R:
            f = re.sub(re.escape(x), " ", f, flags=re.I) if cx == c else f
        hits += [(c, m.group(0)) for m in re.finditer(r"\b(?:" + STATE_WORDS_468R + r")\b", f, re.I)]
    return hits, miss


# 468d の目印: gap を担う中身 (機械学習・特許・機械生成の 3 つ) を「その節が何をするか」の句で見る。言い回しを変えても残る句を
# 選ぶ。1.4 までは §6 / §8.4 / §9 が担い、2026-11-24 の書き直し (議題 15) から §1.8〜§1.10 / §2.2〜§2.3 / §3 が担う。
# measure_clause_overlap.py --guard も同じ一覧を試作に当てる
GAP_MARKERS_468D = {
    1: ("train, fine-tune, evaluate, align, distil",
        "the making, distribution, and use of a Result",
        "permission for text and data mining or for the development of a machine learning model"),
    2: ("The licence includes any Computational Use of the Work",
        "licence under the Patent Claims to make any Computational Use of the Work",
        "however much or little of it was used"),
    3: ("makes no Reservation",
        "is to be read as a Reservation",
        "withdraws any Reservation",
        "disclaims reliance",
        "makes no representation that any right subsists",
        "asserts none in it",
        "need not determine which parts of the Work",
        "depends on the answer"),
    4: ("imposes no condition, obligation, or restriction upon You in respect of the Work or of any Result",),
}
GAP_WORDS_468D = ("model", "parameter set", "weight", "embedding", "output")


def gap_losses(draft_body):
    """草案の本文 (区切り線の後) から、gap を担う節の目印か gap の核の語が消えていれば、その一覧を返す。"""
    def sec(txt, n):
        m = re.search(r"^%d\. [A-Z].*?(?=^\d+\. [A-Z])" % n, txt, re.M | re.S)
        return re.sub(r"\s+", " ", m.group(0)).strip() if m else ""
    lost = [f"§{n} から gap の中身が消えている: {mk!r}"
            for n, ms in GAP_MARKERS_468D.items() for mk in ms if mk not in sec(draft_body, n)]
    lost += [f"gap の核の語 {kw!r} が草案から消えている" for kw in GAP_WORDS_468D if kw not in draft_body.lower()]
    return lost
