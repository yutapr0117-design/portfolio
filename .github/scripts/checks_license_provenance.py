"""checks_license_provenance.py — 来歴の開示の Check 群 (473 / 473b / 473c)

2026-11-08 に checks_license_submission.py から切り出した。Check の監査で 473 / 473b を強めた結果、
元の file が 914 行になり Check 52 の advisory 900 を超えた。来歴の開示 (誰が起草し、誰が方向を
決めたか) を見る塊で、他の Check と変数を共有しない。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  473. **来歴の開示が、否定の半分だけで現れないこと** (BLOCKING): steward は
       *"the drafting was not directed by me, **but the direction of the licence was mine**"*
       と述べており、2026-09-14 (#125) に開示を**両方の半分を持つ形**へ訂正した。
       **にもかかわらず、短い写しを載せている面は列挙されなかった** —— 2026-09-22 の実測で
       **`LICENSE`・入口 2 面（#187）に続き、`submission.md` §B.0（実際に送る本文そのもの）と
       Q10 の日英 2 面（#189）**が否定の半分だけを述べていた。**同じ族の 4 回目**
       （#66 送る文面に開示が無い / #67 採用者が開く `LICENSE` に無い / #125 / #187）なので、
       per-instance をやめて構造で縛る。**開示を薄める向きではなく、*人間の関与を過少に述べる*
       向きの誤り**であり、moderator が AI の関与度をまさに問うている最中 (B14) に最も不利である。
       **検出器の設計が本体である**（今日 3 回外した）: (1) **行の折り返しを潰す** ——
       `I did\nnot commission` は素の正規表現では一致しない。(2) **`>` の引用マーカーを剥がす**
       —— 剥がさないと `the direction of the licence\n> was mine` が語として繋がらない。
       (3) **段落粒度で見る** —— file 粒度の集合演算は、**訂正済みの写しと未訂正の写しを
       同じ file に持つ**場合を必ず取り逃がす（`submission.md` が実例で、#187 はこれで
       「一覧は 3 項目」と誤って完全性を主張した）。(BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 473. 来歴の開示が、否定の半分だけで現れないこと (BLOCKING) ─────────────────────
    # WHY: steward 本人の言葉は 2 つの半分から成る ——
    #   *"the drafting was not directed by me, but the direction of the licence was mine"*。
    #   2026-09-14 (#125) に開示を訂正したが、**短い写しを載せている面は列挙されなかった**。
    #   2026-09-22 に 5 段落が否定の半分だけを述べており、その中に
    #   **実際に送る本文 (§B.0)** と **不利な一覧の来歴 entry (#5)** が入っていた。
    #   誤りの向きは「AI をより自律的に見せる」側で、B14 の最中に最も不利である。
    # 検出器の設計 (今日 3 回外したので、外し方を実装に残す):
    #   (1) 行の折り返しを潰す —— `I did\nnot commission` は素の正規表現に当たらない。
    #   (2) `>` の引用マーカーを剥がす —— 剥がさないと語が繋がらない。
    #   (3) **段落粒度**で見る —— file 粒度の集合演算は、訂正済みと未訂正の写しを
    #       同じ file に持つ場合を必ず取り逃がす (#187 がこれで完全性を誤主張した)。
    _NEG473 = re.compile(
        r"(did not (ask for|commission|direct)|not commissioned or directed"
        r"|not directed by me|was(?:n't| not) directed by|指示してもいない|指示していない|起草に関与していない)", re.I)
    _DIR473 = re.compile(
        r"(direction of the licen[cs]e was (mine|his)|direction was (mine|his)"
        r"|involved in determining the direction|nonetheless his"
        # [2026-11-08] 素の「方向づけ」は、方向を AI に帰す文でも満たされた (監査で実測)。人が方向を
        #   決めたことを述べる形に限る
        r"|(本人|人間|オーナー|steward|私)[^。|]{0,25}方向|方向[^。|]{0,15}(本人|人間|オーナー|steward)"
        r"|外部承認を目指|aim (at|for) external approval)", re.I)
    # この欠陥そのものを記録している段落は対象外。記録を禁じると、
    # **欠陥の記録が Check に消される**という逆向きの害が出る (#977 と同じ線引き)。
    # [2026-11-08] 免除は「この欠陥の記録」に限る。訂正 / corrected / 初版 / 旧文 は、来歴と無関係な日付つきの
    #   訂正の注にも現れ、その段落なら否定の半分だけを書けた (監査で実測)
    _META473 = re.compile(r"(#18[5-9]|#12[45]|#6[67]|#216|BLIND|Check 473|訂正された文)")
    _SUBJ473 = re.compile(r"(drafting|drafted|起草|licen[cs]e|ライセンス)", re.I)

    def _norm473(s):
        s = re.sub(r"(?m)^\s*>+\s?", "", s)   # (2) 引用マーカー
        return re.sub(r"\s+", " ", s)          # (1) 折り返し

    # ⚠ **初版はここで ctx の `read()` を呼び、module に bind されていないので NameError を投げ、
    #    それを裸の `except Exception: continue` が握り潰して 79 file すべてを読み飛ばした。**
    #    **動機となった欠陥を戻しても GREEN のまま**で、非 vacuity 検証だけがそれを教えた
    #    （`BLIND-SPOTS.md`「crash は grep をすり抜ける」の 2 例目）。
    #    **対処は 2 つとも要る**: (i) 未 bind の名前に依存せず Path から直接読む、
    #    (ii) **例外を握り潰さない** ——読めない file は数え、0 件でないなら RED にする。
    _paths473 = sorted(
        list((ROOT / "LICENSES").glob("*.md"))
        + list((ROOT / "docs" / "files" / "LICENSES").glob("*.md"))
        + [ROOT / "LICENSE"]
    )
    _files473 = [str(q) for q in _paths473]
    _bad473 = []
    _unread473 = []
    for _q473 in _paths473:
        try:
            _t473 = _q473.read_text(encoding="utf-8")
        except Exception as _e473:          # (ii) 握り潰さない
            _unread473.append(f"{_q473.name}: {type(_e473).__name__}")
            continue
        _f473 = str(_q473)
        for _para473 in re.split(r"\n\s*\n|\n(?=\| )", _t473):   # (3) 段落粒度
            _p473 = _norm473(_para473)
            if not _NEG473.search(_p473):
                continue
            if not _SUBJ473.search(_p473):
                continue
            if _META473.search(_p473):
                continue
            if _DIR473.search(_p473):
                continue
            _bad473.append(f"{_f473.split('portfolio/')[-1]}: {_p473.strip()[:90]}")

    # ── 473b: 2026-09-23 に事実として否定された文が、現在形の言明として残らないこと ────────
    # **`against.md` #216。** steward の 2026-09-14 の手紙（`rounds/2026-09-15-…round3.txt`）は
    # *"I then told the AI that I wanted my own license to aim for external approval …
    # I gave the goal, and the AI generated and developed the license"* と述べており、
    # **我々が 8 日間 publish していた「人間は作る判断をしていない」「頼んでいない」
    # 「AI がリポジトリにライセンスが要ると判断した」は誤りだった。**
    # **473 本体は「否定の半分だけで現れるな」を守るが、否定そのものが偽になった場合は見ない。**
    #
    # ⚠ **初版は射程を 4 面に決め打ちし、`review-responses-meta.md` の Q10 English を
    #   見逃した**（オーナー指摘・2026-09-23）——**同じ Q10 の日本語だけが直り、英語が
    #   訂正前の説明を現行の回答として載せたままだった。** 決め打ちをやめて導出に変える。
    # ⚠ **是正史は禁じない。** `against.md` や Q&A の訂正記録は、これらの句を**歴史として**
    #   引く。全面禁止は履歴を消す圧力になる（#977 の線引き）ので、**473 本体と同じ手で
    #   「訂正の印が近くに在るか」で分ける。** `rounds/` は無改変保存ゆえ対象外。
    _dead473b = ("did not ask for it", "not commissioned", "did not commission it",
                 "determined that the repository needed a licence",
                 "I did not direct the drafting",
                 "判断自体、人間は出していない")
    _mark473b = re.compile(r"(#216|#125|#187|#191|訂正|corrected|誤りだった|旧文|是正|history|"
                           r"Check 473|superseded|歴史として)")
    # ⚠ **mirror 層を射程に入れる（2026-09-23・`against.md` #218）。** 初版は `LICENSES/` だけを
    #   見ており、**`docs/files/` の mirror は同じ主張を写しているのに一度も射程に入っていなかった。**
    #   実測でそこに 3 件残っていた。**「本体を直した」は「写しも直った」ではない。**
    _scope473b = ([ROOT / "LICENSE"] + sorted((ROOT / "LICENSES").rglob("*.md"))
                  + sorted((ROOT / "docs" / "files" / "LICENSES").rglob("*.md")))
    _bad473b, _unread473b, _read473b = [], [], 0
    for _f473b in _scope473b:
        # 無改変保存は `LICENSES/rounds/` だけ (2026-11-12・監査 #47): 旧版は path のどこかに "rounds" が在れば
        #   外し、`docs/files/LICENSES/rounds/` の mirror (AI が書く通常の散文) まで射程から落としていた
        if _f473b.is_relative_to(ROOT / "LICENSES" / "rounds"):
            continue
        _read473b += 1
        try:
            _raw473b = _f473b.read_text(encoding="utf-8")
        except Exception:
            _unread473b.append(str(_f473b.relative_to(ROOT)))
            continue
        # **粒度が本体である。** 初版は正規化後の ±300 字の窓で見て、
        # **`against.md` の 1 行 3,000 字の entry 内に在る訂正印に届かなかった。**
        # 単位は「その句を含む*行*」または「その句を含む*段落*」——どちらかに印が在れば可。
        # 行は register の 1 entry に、段落は折り返された散文に対応する。
        _paras473b = _raw473b.split("\n\n")
        _units473b = _raw473b.splitlines() + _paras473b
        # 単位の正規化は句に依存しないので file ごとに 1 回だけ (2026-09-29: 旧実装は句 × 単位で
        # 毎回 re.sub し、1 回の gate で約 18 万回・gate 全体の約 2 割を使っていた)。
        # [2026-11-08] 473 と同じく引用マーカーを外し、大文字小文字と licence / license を区別しない
        #   (文頭の Not commissioned や米綴りの license、引用の中で折り返した句が通っていた)
        _norm_units473b = [(_u, re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>+\s?", "", _u)).lower().replace("license", "licence"))
                           for _u in _units473b]
        for _d in _dead473b:
            _dn = re.sub(r"\s+", " ", _d).lower()
            for _u, _un in _norm_units473b:
                if _dn not in _un:
                    continue
                if not _mark473b.search(_u):
                    _bad473b.append(f"{_f473b.relative_to(ROOT)}: 否定済みの句 {_d!r} が"
                                    "訂正の印なしで現れる")
                    break
    # 肯定側（目的の出所）が、現在形で読まれる主要 4 面に在ること。**消して黙らせる経路も塞ぐ。**
    for _rel473b in ("LICENSE", "LICENSES/REVIEWERS.md", "LICENSES/ACD-1.0.submission.md",
                     "LICENSES/ACD-1.0.submission-reference.md"):
        _p473b = ROOT / _rel473b
        if not _p473b.exists():
            _bad473b.append(f"{_rel473b}: 存在しない (射程が drift したら Check を直せ)")
            continue
        _t473b = re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>+\s?", "", _p473b.read_text(encoding="utf-8")))
        if "aim at external approval" not in _t473b and "aim for external approval" not in _t473b:
            _bad473b.append(f"{_rel473b}: 目的の出所（人間が外部承認を目指すと述べたこと）が無い")
        # [2026-11-08] 来歴の段落 (**Provenance.**) が複数あるなら、その全てが目的の出所を持つこと。
        #   submission.md は送る §B.0 と注の §E.1 に 1 つずつ持ち、送る方だけを変えても file 全体の照合は通った
        for _pv473b in re.findall(r"\*\*Provenance\.\*\*(.{0,1200})", _t473b):
            if "aim at external approval" not in _pv473b and "aim for external approval" not in _pv473b:
                _bad473b.append(f"{_rel473b}: Provenance の段落の 1 つが目的の出所を持たない")
    # ── 473c: `rounds/` の運用規約と、実際の file の状態が食い違わないこと ────────────────
    # **`against.md` #219。** 2026-09-23 に off-list 私信 5 件を stub 化したが、
    # **`rounds/README.md` / `REVISION-PROTOCOL.md` / `CLAUDE.md` は「無改変で本文そのものを
    # 置く」と規定したままだった** ——**規則と現物が真っ向から食い違い、しかも 473b は
    # 「否定済みフレーズ」しか見ないので原理的に検出しない**（オーナー指摘）。
    # **両向きで強制する** ——stub が在るなら例外を述べよ / 例外を述べるなら stub が在ること
    # （**死んだ規則を作らない**）。
    _stub473c = [p for p in sorted((ROOT / "LICENSES" / "rounds").glob("*.txt"))
                 if "THE TEXT HAS BEEN WITHDRAWN" in p.read_text(encoding="utf-8", errors="replace")]
    _conv473c = ("LICENSES/rounds/README.md", "LICENSES/REVISION-PROTOCOL.md", "CLAUDE.md")
    _bad473c = []
    for _rel in _conv473c:
        _p = ROOT / _rel
        if not _p.exists():
            _bad473c.append(f"{_rel}: 存在しない"); continue
        # 語の在否ではなく、その語を持つ行が例外を述べているかで見る (2026-11-12・監査 #43): 旧版は
        #   "off-list correspondence" の 2 語が在れば例外を述べたと数え、「例外ではない」と逆を書いても緑だった
        _ol473c = [_l for _l in _p.read_text(encoding="utf-8", errors="replace").splitlines()
                   if "off-list correspondence" in _l]
        _neg473c = [_l for _l in _ol473c if re.search(r"例外では(?:な|あり)|例外にし(?:な|ませ)|not an exception|"
                                                      r"no exception|stub に(?:は)?しな|本文を置く(?!か)", _l)]
        _has = any(re.search(r"例外|stub|exception", _l) for _l in _ol473c) and not _neg473c
        if _neg473c:
            _bad473c.append(f"{_rel}: off-list correspondence の例外を打ち消す文がある: {_neg473c[0].strip()[:60]!r}")
        if _stub473c and not _has:
            _bad473c.append(f"{_rel}: stub が {len(_stub473c)} 件在るのに例外が書かれていない")
        if not _stub473c and _has:
            _bad473c.append(f"{_rel}: 例外を述べているが stub が 1 件も無い (死んだ規則)")
    check(
        not _bad473c,
        f"Check 473c: rounds/ の規約と現物が整合 (stub {len(_stub473c)} 件 / 規約 {len(_conv473c)} 面)",
        (f"Check 473c: {_bad473c}。**`rounds/` は「無改変で本文を置く」場所だと 3 面が規定して"
         "いる。第三者との private off-list correspondence を stub 化するなら、その例外を同じ "
         "3 面に書かなければ、規則と現物が食い違ったまま公開される**"
         " (`against.md` #219・オーナー指摘 2026-09-23)。**逆に、例外を書いて stub が 1 件も"
         "無ければ死んだ規則である**"),
        blocking=True,
    )

    check(
        not _bad473b and not _unread473b,
        f"Check 473b: 来歴 {_read473b} 面に否定済みの句 0 件（訂正の印つきは可・LICENSES/rounds/ の受領文は除く）",
        (f"Check 473b: {_bad473b}。**2026-09-23 に steward 本人が訂正した** —— "
         "ライセンスを持つ判断と上位の方向づけは人間発であり、"
         "*\"the agent determined that the repository needed a licence\"* 等は事実として誤り "
         "(`against.md` #216)。**順序は 3 段** —— 人間発の目的・上位設計 → "
         "AI による具体的な法的設計と起草 → 委任下の自走による発展・一般化。"
         "**「後から知った」を書くなら対象を 3 段目に明示せよ。** "
         "歴史として引くなら、同じ段落に訂正の印（#216 等）を置くこと"
         f" / 読めなかった file: {_unread473b}"),
        blocking=True,
    )

    check(
        not _bad473 and not _unread473,
        f"Check 473: 来歴の開示 {len(_files473)} file、否定の半分だけで現れる段落 0 件",
        (f"Check 473: 来歴の開示が否定の半分だけで現れている: {_bad473}。**steward 本人は "
         "*\"the drafting was not directed by me, but the direction of the licence was mine\"* と "
         "述べている。**「指示していない」だけを書くと、人間の関与を実際より小さく述べることになり、"
         "moderator が AI の関与度を問うている最中 (B14) には最も不利な向きである。"
         "同じ段落に肯定の半分を置け (`submission.md` §E.1 が権威)"
         f" / 読めなかった file: {_unread473}"),
        blocking=True,
    )
