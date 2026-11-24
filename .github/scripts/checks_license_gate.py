"""
checks_license_gate.py — 出す版を替える前の最後の門 (LICENSES/ACD-<版>-GATE.md) の固定が保たれていることを守る Check

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES

  504. **出す版を替える前の門の固定が、いまの草案・変更の一覧・門の文・読み手へ渡す指示文と一致すること** (BLOCKING・2026-11-25・議題 31):
       議題 29 の丁 = 「門を次の読みの前に固定し、一覧の漏れを埋めて 7 日置き、未使用の読み手 2 体で 1 回だけ読む。落ちたら 1.4 のまま」。
       本文・一覧・指示文・門の文のどれかを動かしたのに日数を数え直していない形、結果を見た後に固定し直す形 (2 回目の読み)、
       門の文を薄めた形を RED にする。数え直しは `moved_clauses.py --pin` が印を書き直すので差分に必ず出る。
       GATE.md の無い版では何も見ない (門を置いたときだけ働く)。落ちた門 (HIGH か PARTLY LISTED の HIGH が 1 以上) の後は、草案は次の版の
       ために動いてよいので sha は照らさず、確定の道具 (`_lib_gate_pin.gate_problems`) が確定を止め続ける。
       **逆側**: 誤字 1 つの直しでも日数が数え直しになる (丁の趣旨)。印の since だけを昔へ書き換える形は、浅い履歴の CI からは見えず、
       確定の道具が git の履歴で見る。
"""


def run(ctx):
    check = ctx.check

    # ── 504. 出す版を替える前の門の固定が、いまの草案・一覧・文と一致すること (BLOCKING) ─────────
    from _lib_gate_pin import gate_file, pin_problems
    from moved_clauses import working_draft
    _v504 = working_draft().name.split("-")[1]
    _bad504 = pin_problems(_v504)
    _pend504 = _bad504 is not None and "<!-- GATE-PIN: pending -->" in gate_file(_v504).read_text(encoding="utf-8")
    check(
        not _bad504,
        (f"Check 504: ACD-{_v504} の門 (GATE.md) は置かれていない" if _bad504 is None
         else f"Check 504: ACD-{_v504} の門は置かれているが、固定の印はまだ打たれていない (日数を数えていない)" if _pend504
         else f"Check 504: ACD-{_v504} の門の固定が、草案の本文・変更の一覧・門の文・指示文と一致する"),
        (f"Check 504: ACD-{_v504}-GATE.md の固定が破れている: {_bad504}。動かすなら `python3 .github/scripts/moved_clauses.py --pin` で"
         "日数を数え直し、同じ commit に入れよ (結果が在れば数え直せない —— 読みは 1 回だけ)"),
        blocking=True,
    )
