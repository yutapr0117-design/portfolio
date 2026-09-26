"""LICENSES/ の次版草案についての consistency Check 群.

**このファイルが分かれている理由**: `checks_license_submission.py` が 801 行になり
Check 52 の advisory (800) を越えた。**予算を上げず、テーマで分けた** ——
`checks_license_submission.py` が守るのは**審査者がいま受け取る面**（送る文面・提出対象の
版への引用・入口ページ・来歴の開示）で、ここが守るのは**まだ誰にも渡していない次版の草案**
である。壊れたときの損害も違う: 前者は「審査者が誤った物を読む」、後者は「確定の日に、
誤った状態の草案から版を切る」。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  468. **次版の草案が、自分が何であるかを述べ、内部的に健全であること** (BLOCKING): 2026-09-10 に
       オーナーが「現行は保持、次版を作って改善し続けるのは問題ない」と述べたので
       次版の草案 (**現在は `LICENSES/ACD-1.2-DRAFT.txt`**) を置いた。**草案は確定版と紛らわしい** —— 同じ書式・同じ節見出しで、
       条番号だけが §1（定義の並べ替え・E13）と §15 以降でずれている。**読み手が取り違えると、凍結中の提出物について
       誤った条番号を引くことになる。** 3 つを強制する: **(a)** 冒頭が **NOT IN FORCE /
       NOT SUBMITTED / NOT APPLIED** を述べること、**(b)** 純 ASCII・節が連番・`Section N.M` の
       参照がすべて実在すること（**1.0 について §4c が測っている性質を、草案でも同じ形で保つ**）、
       **(c)** 冒頭が申告する語数・条数が実測と一致すること。**(c) が要るのは、本日 6 回
       「数えられるものを、数える前に書いた」からである。**
       **468d は別の危険を見る** —— **この instrument が新規である理由は §6 / §8.4 / §9 の 3 点**
       であり（register B10）、**次版で「短くする」圧力がかかったとき最初に削られうるのがここである。**
       §6 と §9 は 1.0 と等価であること、§8.4 は射程語（model / parameter set / weight /
       embedding / output）が残っていることを求める。**正当な改訂は止めず、静かな喪失だけを止める。**
       **468e は「まだ open な errata」の宣言を errata の現物と照合し、468f は冒頭が主張する
       「1.1 との同一性」をすぐ下の変更一覧と照合する** ——**どちらも「やることリストは項目を
       消化した瞬間に古くなり、消化しているその瞬間こそ一覧を見ていない」class** で、
       468f は **2026-09-22 に外部の AI レビューが見つけた** (`against.md` #207)。 (BLOCKING)
"""
import json
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 468. 次版の草案が自分を述べ、内部的に健全であること (BLOCKING) ─────────────────────
    #   草案は 1.0 と書式が同じで、条番号だけ §15 以降がずれている。**取り違えは実害を生む**
    #   (凍結中の提出物について誤った条番号を引く)。だから「自分が何か」を本文に述べさせる。
    _dr468 = ROOT / "LICENSES" / "ACD-1.2-DRAFT.txt"
    if _dr468.exists():
        _t468 = _dr468.read_text(encoding="utf-8")
        _bad468 = []
        for _phrase in ("NOT IN FORCE", "NOT SUBMITTED", "NOT APPLIED"):
            if _phrase not in _t468:
                _bad468.append(f"冒頭に {_phrase!r} が無い (草案は自分の身分を述べること)")
        _na468 = sum(1 for _b in _dr468.read_bytes() if _b > 127)
        if _na468:
            _bad468.append(f"非 ASCII が {_na468} バイトある (1.0 の §4c が測る性質を草案でも保つ)")
        _sep468 = "-" * 80
        _lic468 = _t468.split(_sep468, 1)[1] if _sep468 in _t468 else _t468
        _secs468 = [int(_m) for _m in re.findall(r"^(\d+)\. [A-Z]", _lic468, re.M)]
        if _secs468 != list(range(1, len(_secs468) + 1)):
            _bad468.append(f"節番号が連番でない: {_secs468}")
        _cl468 = set(re.findall(r"^  (\d+\.\d+) ", _lic468, re.M))
        _refs468 = set(re.findall(r"Sections?\s+(\d+\.\d+)", _lic468))
        _dang468 = sorted(_r for _r in _refs468 if _r not in _cl468)
        if _dang468:
            _bad468.append(f"解決しない参照: {_dang468} (**行をまたぐ参照は素の置換では当たらない**)")

        # ── 468g. 草案の**本文側**に義務語 (`shall` / `must`) が現れないこと ─────────────
        # WHY: 提出パケットは「ACD-1.0 は measurably not proscriptive —— `shall` と `must` は
        #   **0 回**」を #116 への緩和として publish している。
        #   **⚠ 初版のこのコメントは「1.0 は凍結されているのでその性質を検査する Check は
        #   定義により発火しえない」と書いていた。誤りである（#193）** ——**Check 441d が
        #   ACD-1.0 に対して BLOCKING でまさにこれを検査している。** 凍結は byte を守るが、
        #   441d は 1.0 が凍結される前から在り、いまも走っている。
        #   **真なのは草案の側だけだった**: 441d の対象は `ACD-1.0.txt` に限られ、
        #   **次に提出する版を守るものは 1 つも無かった。**
        #   パターンは 441d と同じ 7 つに、`shall` / `must` の裸形を足したものにしてある ——
        #   **草案の被覆が、凍結された 1.0 の被覆より狭くてはならない。**
        # ⚠ **射程を正直に書く（2026-09-22 の vacuity 掃引で実測）**: この face は**綴りで見る**ので、
        #   *"did not **steer** the drafting"* のような**同義語の言い換えは素通りする**（実測で確認）。
        #   **同義語を投機的に足さないのは、開示文が steward 本人の言葉として固定されており、
        #   言い換えが現れる経路が無いからである。** 経路ができたら（例えば要約文を別に置くなら）
        #   そのときに広げる。**「広げなかった」ことと「見ている」ことを混同しない。**
        # ⚠ **ヘッダは対象外**である —— 実測 (2026-09-22) で草案の `must` 2 件はどちらも
        #   「1.0 への引用は 1.0 の本文を使うこと」等の**草案についての注記**で、条文ではない。
        #   `_lic468`（セパレータ以降）で見るのはそのためで、**file 全体で数えると
        #   ヘッダの散文が条文の性質として報告される。**
        _pat468g = (r"\b(shall|must)\b", r"You are required\b", r"provided that\b",
                    r"on condition\b", r"You agree\b", r"You may not\b")
        _deon468 = sorted({_m.group(0).lower()
                           for _p in _pat468g
                           for _m in re.finditer(_p, _lic468, re.I)})
        if _deon468:
            _bad468.append(
                f"本文側に義務語がある: {_deon468} "
                "(#116 の緩和は「shall と must は 0 回」を測った値に依っている。"
                "1.0 は凍結が守るが、草案は誰も守らない)")
        _mw468 = re.search(r"This draft: ([\d,]+) words, (\d+) clauses", _t468)
        if not _mw468:
            _bad468.append("冒頭に語数/条数の申告が無い (消して黙らせない)")
        else:
            _dw468 = int(_mw468.group(1).replace(",", ""))
            _dc468 = int(_mw468.group(2))
            _aw468 = len(_lic468.split())
            _ac468 = len(_cl468)
            if _dw468 != _aw468:
                _bad468.append(f"語数: 申告 {_dw468} / 実測 {_aw468}")
            if _dc468 != _ac468:
                _bad468.append(f"条数: 申告 {_dc468} / 実測 {_ac468}")
        # ── 468f. 草案ヘッダの箇条書きが壊れていないこと ─────────────────────────────
        #   **468 は区切り線より*後*（ライセンス本文）しか読まない。** 語数も条数も ASCII も
        #   参照の解決も、すべて本文についての検査である。**区切り線より前の編集用ヘッダは、
        #   どの Check も一度も読んでいなかった。**
        #   **2026-09-20 に実害**: 同日の reflow で `* A new Section 15.5 restores …` が
        #   **`* w Section 15.5 restores …` に化けた**（`block[len('    * '):]` が、既に
        #   空白正規化されて `* A new …` で始まる文字列から 6 文字を削り、`* A ne` を落とした）。
        #   **`npm run verify` は緑のまま**で、**その状態の草案が外部レビュー 2 件へ渡った。**
        #   **ヘッダは「この草案が何であるか」を読み手に説明する唯一の面**であり、
        #   本文と同じ重みで壊れてはならない。
        #   **検査は最小の字面規約 1 つに絞る** ——英文の箇条書きは大文字か数字で始まる。
        #   意味は見ない（見ようとすると brittle gate になる・§2.9 の線）。
        _headbad468 = []
        _head468 = _t468.split(_sep468, 1)[0] if _sep468 in _t468 else ""
        for _hm468 in re.finditer(r"^\s*\* (.+)$", _head468, re.M):
            _first468 = _hm468.group(1).strip()
            if not _first468[:1].isupper() and not _first468[:1].isdigit():
                _headbad468.append(_first468[:48])
        if _headbad468:
            _bad468.append(f"ヘッダの箇条書きが大文字/数字で始まっていない: {_headbad468}")

        # ── 468d. gap を担う条項が successor でも生き残っていること ──────────────────────
        #   **この instrument が新規である理由は §6 / §8.4 / §9 の 3 点である** (register B10)。
        #   **次版で「短くする」圧力がかかったとき、最初に削られうるのがここである** ——
        #   実際 B3 の測定は「機構部だけを削る」と明記しているが、**明記は強制ではない。**
        #   §6 と §9 は 1.0 と byte 等価 (空白正規化後) であることを求める。
        #   **§8.4 は 2026-09-10 に因果の限定 (E15) を入れたので等価ではない** ——
        #   代わりに **gap の核となる語** (model / parameter set / weight / embedding / output) が
        #   すべて残っていることを見る。**正当な改訂を止めず、静かな喪失だけを止める。**
        _10_468 = ROOT / "LICENSES" / "ACD-1.0.txt"
        if _10_468.exists():
            _t10 = _10_468.read_text(encoding="utf-8")
            _draft_lic = _t468.split(_sep468, 1)[1] if _sep468 in _t468 else _t468

            def _sec468(_txt, _n):
                _m = re.search(r"^%d\. [A-Z].*?(?=^\d+\. [A-Z])" % _n, _txt, re.M | re.S)
                return re.sub(r"\s+", " ", _m.group(0)).strip() if _m else ""

            # **byte 等価では厳しすぎる。** 2026-09-11 に E4 (§6.4 の "is not encumbered" →
            # "no enforceable claim arises") で実際に発火した —— **記録済みの欠陥を直す正当な改訂**
            # まで止めてしまう。守りたいのは**文面の同一性ではなく gap の生存**なので、
            # **各 gap 条項が担っている中身を marker で見る**形へ変えた。
            # **marker は「その条項が何をするか」を一言で表す語句**であり、言い回しを変えても残る。
            _lost468 = []
            _markers468 = {
                6: ["Computational Use of the Work is expressly permitted",
                    "without condition",
                    "makes no Reservation",
                    "expressly declines to make one",
                    "withdraws it and disclaims reliance",
                    "no permission at all"],
                9: ["makes no representation that any right subsists",
                    "asserts no right in Machine-Generated Material",
                    "are not required to determine",
                    "depends on that"],
            }
            for _n468, _ms468 in _markers468.items():
                _sec_txt468 = _sec468(_draft_lic, _n468)
                for _mk468 in _ms468:
                    if _mk468 not in _sec_txt468:
                        _lost468.append(f"§{_n468} から gap の中身が消えている: {_mk468!r}")
            for _kw468 in ("model", "parameter set", "weight", "embedding", "output"):
                if _kw468 not in _draft_lic.lower():
                    _lost468.append(f"§8.4 の gap 語 {_kw468!r} が草案から消えている")
            check(
                not _lost468,
                "Check 468d: gap を担う条項 (§6 / §9 / §8.4 の射程語) が successor でも生きている",
                (f"Check 468d: 次版で gap が失われている: {_lost468}。**この instrument が新規である"
                 "理由は §6 / §8.4 / §9 の 3 点であり、短くする圧力がかかったとき最初に削られうるのが"
                 "ここである。** 意図的に変えるなら `ACD-1.1-CHANGELIST.md` に記録し、"
                 "**register B10 の主張も同時に書き換えること**"),
                blocking=True,
            )

        # ── 468e: 草案が宣言する「まだ open な errata」が、errata の現物と一致すること ────
        # Check 468 は語数・条数・参照の解決を見るが、**草案が自分の*状態*について述べる文**は
        # 見ていなかった。実測 (2026-09-14): preamble の status block が
        # 「Still open in this draft, deliberately: E11 / E13 / E15 / E16」と述べ、
        # **4 件とも errata では閉じていた** —— E13 は 2026-09-10、E15 は 09-11、E16 は 09-13 から
        # 誤っており、**4 日間、提出される文書が自分の状態について偽の宣言を持っていた**。
        # **しかも「They are not oversights」と*意図的である*ことまで主張していた** ——
        # 直した項目について「わざと残した」と述べるのは、単に古いより悪い。
        # **これは「やることリストは、項目を消化した瞬間に古くなる」class の最も外へ出る面である**
        # (Check 469 が CHANGELIST について守っているのと同じ invariant を、**本文側**で守る)。
        _st468 = re.search(r"Still open in this draft[^:]*:(.*?)(?:cost\.|\n\n)", _t468, re.S)
        if _st468 is None:
            _bad468.append("preamble に「Still open in this draft」の宣言が無い "
                           "(宣言しないなら本 face を外すこと。黙って消さない)")
        else:
            _declared468 = set(re.findall(r"\bE\d+\b", _st468.group(1)))
            _erp468 = ROOT / "LICENSES" / "ACD-1.0.errata.md"
            if _erp468.exists():
                _ert468 = _erp468.read_text(encoding="utf-8")
                _openset468 = set()
                for _ln468 in _ert468.splitlines():
                    _m468 = re.match(r"\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|", _ln468)
                    if not _m468:
                        continue
                    # **「確定手順へ回した」は「閉じた」ではない。** E10 は 1.1 の descriptor が
                    # 存在しないので*ここでは*閉じられないだけで、欠陥としては残っている。
                    # 初版はこれを closed 扱いにし、**本 face が導入直後に自分の誤りを指摘した。**
                    # **版番号を決め打ちしない。** 1.1 を確定させた時点で作業場は 1.2 へ移り、
                    # **1.2 で閉じた entry が「まだ open」と読まれた**（2026-09-18 に実際に発火）。
                    if re.search(r"\d+\.\d+ 草案で閉じた", _ln468):
                        continue
                    _openset468.add(_m468.group(1))
                if _declared468 != _openset468:
                    _bad468.append(
                        f"preamble の「Still open」が errata と食い違う: "
                        f"宣言のみ {sorted(_declared468 - _openset468)} / "
                        f"errata のみ {sorted(_openset468 - _declared468)}")

        # ── 468h: 版ごとの機械可読 descriptor が、この instrument の*唯一の制限*を述べること ──
        #   **`against.md` #59 / errata E10。** `reservationsAndLimits` は「しないこと」を 6 つ
        #   並べる一方、**この文書が現に持つ 1 つの制限**（改変テキストを名称・識別子の下で
        #   頒布しないこと・§16.4）に key が無かった。**descriptor だけを読む消費者は
        #   「何も制限しない」と結論する** ——著作物については真で、テキストについては偽である。
        #   **§6.5 の理由は両刃**（自動化システムが判定できない制限は、知らずに破られる）。
        #   1.1 では `reservationsAndLimits.textRedistribution` で閉じた。
        #   ⚠ **E10 は「版ごとに閉じ直す」種類**なので、**新しい版の descriptor を作る瞬間が
        #   再発の瞬間である。** そこを機械で押さえる。
        #   ⚠ **`ACD-1.0.machine.json` は対象外** —— **凍結された欠陥そのもの**であり
        #   （Check 453 が byte を pin している）、直すことは凍結の趣旨に反する。
        _desc468h = [p for p in sorted((ROOT / "LICENSES").glob("ACD-*.machine.json"))
                     if p.name != "ACD-1.0.machine.json"]
        _bad468h = []
        for _d in _desc468h:
            try:
                _j = json.loads(_d.read_text(encoding="utf-8"))
            except Exception as _e:
                _bad468h.append(f"{_d.name}: JSON として読めない ({type(_e).__name__})")
                continue
            _r = _j.get("reservationsAndLimits")
            if not isinstance(_r, dict):
                _bad468h.append(f"{_d.name}: reservationsAndLimits が無い")
                continue
            _tr = _r.get("textRedistribution")
            if not isinstance(_tr, dict):
                _bad468h.append(f"{_d.name}: textRedistribution が無い "
                                "(§16.4 —— この文書が現に持つ唯一の制限)")
            elif str(_tr.get("clause", "")) != "16.4":
                _bad468h.append(f"{_d.name}: textRedistribution.clause が "
                                f"{_tr.get('clause')!r} (16.4 であること)")
        if _bad468h:
            _bad468.append(f"descriptor が唯一の制限を述べていない: {_bad468h}")

        # ── 468f: 草案の冒頭が主張する「1.1 との同一性」が、すぐ下の変更一覧と整合すること ──
        # **2026-09-22 に外部の AI レビューが見つけた** (`against.md` #207)。status block が
        # *"It is at present identical to ACD-1.1 apart from the version number and the
        # identifiers that name it"* と述べたまま、**すぐ下に E22〜E30 の 9 件が並び、同じ
        # ヘッダが 5,051→5,207 語・78→80 条と申告していた。**
        # **468c は申告した数を守り、468e は open な errata の一覧を守っていたが、
        # 「自分は前版と同一である」という文だけは、どの face も見ていなかった。**
        # 害は文言ではない ——`ACD-1.1-SELF-AUDIT.md` の同一性監査が **この文を根拠として引いて
        # おり**、偽になった文の上に「§16.2 の変更は宣言済み」という結論が載っていた。
        # **⚠ 片側だけ禁じない。** 変更一覧が空のときに同一性の主張を*消して*黙らせるのも
        # 同じ drift なので、両向きで要求する（空なら述べよ・空でないなら述べるな）。
        _hdr468f = _t468.split(_sep468, 1)[0] if _sep468 in _t468 else _t468
        _blk468f = re.search(r"Changes in this draft[^:]*:(.*?)(?:\n  Still open|\Z)",
                             _hdr468f, re.S)
        if _blk468f is None:
            _bad468.append("冒頭に「Changes in this draft」の一覧が無い "
                           "(空でも見出しは残すこと。消して黙らせない)")
        else:
            # 末尾の語数・条数 bullet は変更ではないので数えない。
            _items468f = [_b for _b in re.findall(r"^    \* (.*)$", _blk468f.group(1), re.M)
                          if not re.search(r"words, \d+ clauses", _b)]
            _claim468f = re.search(r"is (?:at present )?identical to ACD-1\.\d", _hdr468f)
            if _items468f and _claim468f:
                _bad468.append(
                    f"冒頭が「1.1 と同一」と述べているのに変更一覧に {len(_items468f)} 件ある "
                    f"({_claim468f.group(0)!r})。**同一性の主張は一覧が空のときだけ真である。** "
                    "一覧に項目が在るなら「下に列挙した変更と版数識別子を除いて 1.1 の本文である」"
                    "の形にすること (`against.md` #207)")
            if not _items468f and not _claim468f:
                _bad468.append(
                    "変更一覧が空なのに、冒頭が 1.1 との同一性を述べていない。"
                    "**空であることは黙っていてよい理由ではない** ——読み手には "
                    "「まだ変えていない」と「記録が無い」の区別がつかない")

        check(
            not _bad468,
            f"Check 468: 次版草案が自分を述べ内部的に健全 ({len(_cl468)} 条 / {len(_lic468.split())} 語)",
            (f"Check 468: 次版草案に問題がある: {_bad468}。**草案は 1.0 と書式が同じで条番号だけ"
             "ずれているので、取り違えると凍結中の提出物について誤った条番号を引くことになる。**"
             "自分が何であるかを本文に述べ、1.0 について測っている性質を同じ形で保つこと"),
            blocking=True,
        )
    else:
        # **2026-09-26: 草案が無いとき、Check 468 は OK も ERROR も出さずに消えていた。**
        # `ACD-1.1-CHANGELIST.md` §0.13 は「確定して DRAFT を消すと file が無くなる」ので RED になると
        # 書いていたが、実装は `if exists` だけで else が無く、**確定の日に次版の検査が黙って止まる**
        # 形だった（草案を退避して実測: 468 の行が出力から消え、他の Check が参照切れを偶然拾うだけ）。
        # 決めてあること（§0.13）は「次版の作業場は常に 1 つ」なので、無いことは誤りとして止める。
        # 確定したら、この path を次の草案へ向け直すこと。
        check(
            False,
            "",
            ("Check 468: 次版の草案 `LICENSES/ACD-1.2-DRAFT.txt` が無い。**版を確定したなら、"
             "この Check（と 468d/468e）の対象 path を次の草案へ向け直すこと**"
             "（`ACD-1.1-CHANGELIST.md` §0.13）。**黙って検査を止めない** ——草案が無いと "
             "468 は以前 OK も ERROR も出さずに消えていた"),
            blocking=True,
        )
