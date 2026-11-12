"""_lib_draft_markers.py — 次版の草案の条に当てる一覧と、その当て方 (Check 468u / 468r と measure_clause_overlap.py --guard が共有)。

一覧は 1 か所に置く: Check と試作の道具が別々に持つと食い違う (468u の初版の取り決め)。2026-11-12 に
checks_license_draft.py から移した (468r を足すと Check の module が行の予算 900 を越えるため。読み手は 2 つ)。
"""
import re

# 468u の目印 (条, 句)。checks_license_draft.py (Check 468u) と measure_clause_overlap.py --guard が同じ一覧を import して
# 試作ファイルに当てる (2 か所に持つと食い違う)。§2.8 / §15.5 は CLARITY-TRIAL 試作 e の効果の保存、
# §8.4 / §8.2 は B10 の立証 (gap-measurements.md §1.133) が依拠する句。§5.1 の除外と §8.4 の "content" は §8.4 の
# 限定を支える (2026-11-06・portfolio-25 の依頼)。§5.1 の除外が落ちると、§8.4 が外した請求項まで不行使になる。
EFFECT_MARKERS_468U = (
    ("2.8", "nor Section 12.4 narrows this Section"),
    ("15.5", '"person" includes an entity'),
    ("8.4", "resulting from Computational Use of the Work"),
    ("8.4", "deliberately absent"),
    ("8.2", "not terminable by the Dedicator on any ground"),
    ("5.1", "other than for patent infringement"),
    ("8.4", "from the content of the Work"),
    # 2026-11-08 (T16〜T20・#2602): 許諾の目的語を請求項から行為へ移した結果、効果を運ぶ句になった
    ("8.1", "otherwise practise or transfer"),
    ("8.4", "Section 8.1 alone governs"),
    ("5.1", "for a use of the Work"),
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
    ("6.5", "silence on this subject has proved ambiguous in practice"),                # 過去の観察 (偽にならない)
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
