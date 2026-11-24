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
# 試作ファイルに当てる (2 か所に持つと食い違う)。§2.8 / §15.5 は CLARITY-TRIAL 試作 e の効果の保存、
# §8.4 / §8.2 は B10 の立証 (gap-measurements.md §1.133) が依拠する句。§5.1 の除外と §8.4 の "content" は §8.4 の
# 限定を支える (2026-11-06・portfolio-25 の依頼)。§5.1 の除外が落ちると、§8.4 が外した請求項まで不行使になる。
EFFECT_MARKERS_468U = (
    # 2026-11-16 (T74〜T76): §5.3 と §12.4 は人を §2.8 から借り、限度を §2.8 と同じ語で持つ。限度と人が 1 つなので、
    # どの条も §2.8 を狭めない（§2.8 の末文「Section 12.4 does not narrow this Section.」は T76 で要らなくなった）
    ("5.3", "bind the persons Section 2.8 names, to the fullest extent the law permits"),
    ("12.4", "after the Dedicator's death, to the fullest extent the law permits."),
    ("15.5", '"person" includes an entity'),
    ("8.4", "resulting from Computational Use of the Work"),
    ("8.4", "deliberately absent"),
    ("8.2", "not terminable by the Dedicator under this Dedication on any ground"),
    ("5.1", "other than for patent infringement"),
    ("8.4", "from the content of the Work"),
    # 2026-11-08 (T16〜T20・#2602): 許諾の目的語を請求項から行為へ移した結果、効果を運ぶ句になった
    ("8.1", "otherwise practise or transfer"),
    ("8.4", "Section 8.1 alone governs"),
    ("5.1", "or as without legal basis, a use of the Work"),  # 2026-11-16 T90: for a use → that treats as wrongful, or as without legal basis, a use
    # 2026-11-08 (#2615): 特許の reach の定義と、通知が適用される範囲の主語
    ("8.3", "only as to the acts they describe"),
    ("16.2", "A notice a Dedicator places"),
    # 2026-11-08 (#2630): 特許の「controlled」の双条件と、ファイルの中のタグが及ぶ範囲
    ("8.5", "if, and only if"),
    ("16.2", "in a comment within a file"),
    # 2026-11-08 (#2655): §5.2 が覆う素材とサービスの範囲、§6.4 が「何について」負わないか
    ("5.2", "other than the Work, that the Dedicator itself makes or makes available"),
    ("5.2", "without providing a copy of the Work"),  # 2026-11-12 T60: "of it" を名指しへ
    ("6.4", "under this Dedication in respect of any"),
)

# 468r の語と除外 (条, 句)。除外は語ではなく句で持つ: 同じ語を別の構文で使えば鳴り、句を書き換えたら読み直しの合図になる。
#   語の一覧に無い言い方 (remains to be seen など) は漏れる。前文は作用の条ではないので対象外 (確定の日に読み直す)
STATE_WORDS_468R = (r"unresolved|unsettled|uncertain|currently|presently|at present|today|in practice|has proved|is unclear"
                    r"|not yet|so far|now fails|increasingly|in most jurisdictions|common use|remains? open|open question"
                    r"|undecided|not (?:been )?(?:settled|decided)|to date|at the time of writing|for now|recent(?:ly)?|nowadays|still")
STATE_EXEMPT_468R = (
    ("1.5", "whether or not presently known and whether or not presently subsisting"),   # 範囲の語
    ("6.1", "so far as"), ("6.2", "So far as"), ("7.2", "so far as"),                   # 範囲の語
    ("6.4", "is not decided here and does not need to be"),                             # 決めないことの宣言 (恒久)
    # §6.5 の "has proved ambiguous in practice" は 2026-11-16 の T79 で "leaves permission to be inferred" に替えた (出典の無い経験の言明)
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


# 468d の目印: gap を担う条 (§6 / §9) の中身を「その条が何をするか」の句で見る。言い回しを変えても残る句を選ぶ
# (byte 等価は 2026-09-11 に E4 の正当な改訂まで止めた)。§8.4 は 2026-09-10 に因果の限定 (E15) を入れたので、
# gap の核の語が草案のどこかに残ることだけを見る。2026-11-16 に checks_license_draft.py から移した (module の行の予算
# 900 の手前・886 行)。measure_clause_overlap.py --guard も同じ一覧を試作に当てる
GAP_MARKERS_468D = {
    6: ("Computational Use of the Work is expressly permitted",
        "without condition",
        "makes no Reservation",
        "expressly declines to make one",
        "withdraws it and disclaims reliance",
        "no permission at all"),
    9: ("makes no representation that any right subsists",
        "asserts no right in Machine-Generated Material",
        "are not required to determine",
        "depends on that"),
}
GAP_WORDS_468D = ("model", "parameter set", "weight", "embedding", "output")


def gap_losses(draft_body):
    """草案の本文 (区切り線の後) から、gap を担う条の目印か §8.4 の gap 語が消えていれば、その一覧を返す。"""
    def sec(txt, n):
        m = re.search(r"^%d\. [A-Z].*?(?=^\d+\. [A-Z])" % n, txt, re.M | re.S)
        return re.sub(r"\s+", " ", m.group(0)).strip() if m else ""
    lost = [f"§{n} から gap の中身が消えている: {mk!r}"
            for n, ms in GAP_MARKERS_468D.items() for mk in ms if mk not in sec(draft_body, n)]
    lost += [f"§8.4 の gap 語 {kw!r} が草案から消えている" for kw in GAP_WORDS_468D if kw not in draft_body.lower()]
    return lost
