"""ライセンス register の *構造* が機械可読であり続けることを守る Check 群。

   `checks_license_self_reporting.py` から 2026-09-27 に切り出した。**引き金は advisory 予算
   (800 行) だが、割る線は行数ではなく主題で選んだ** —— **あちらは「自己申告した *数* が実測と
   合うか」、ここは「自己申告した *構造* が使える形で在り続けるか」**（列挙・state token・
   反証表の状態）。**読み手も直し方も違う**: 数はふつう申告側を直し、構造は register 側を直す。

   469. 自己申告の「列挙」が、消化した項目で古くならないこと (BLOCKING)
        (a) 460 の face inventory ⟺ 実装 / (b) errata の E-ID ⟺ CHANGELIST /
        (c) READY-TO-SUBMIT.md の「Check N (M 部)」⟺ 実装の下位部 N[a-z] の種類数 (2026-11-03)
   474. 不利な事実の register が、潰すための backlog として機械可読であること (BLOCKING)
   475. 反証表の全行が日付つきの状態を宣言していること (BLOCKING)
  491. register の英語の索引が日本語の索引の写しであること (BLOCKING・2026-11-06)。審査者が読むのは英語の索引で、
        項目を足すと片方だけ増える形なので、ID の集合と重大度の一致を見る。
        あわせて objection-map が against.md の最大番号に追いついているかを ADVISORY で出す。読んで
        「足す反論は無い」と判断して数を上げるだけの増分も正当なので、止めない。
"""

import datetime
import re

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(ctx):
    check = ctx.check
    errors, warnings = ctx.errors, ctx.warnings
    warnings = ctx.warnings          # Check 385: bare append を使うので明示的に束縛する
    _L460 = ROOT / "LICENSES"        # 切り出し元と同じ名前を保つ (移した本文を書き換えないため)

    # ── 469. 自己申告の「列挙」が、消化した項目で古くならないこと (BLOCKING) ──────────────
    # Check 460 は「数」を、本 Check は「列挙」を実測と突き合わせる。列挙は減る側へ drift する
    # ので、「増えたか」を見る習慣では永久に検出できない。
    _bad469 = []
    _impl469, _erids = set(), set()

    # (a) face inventory (docstring) ⟺ 実装
    _self469 = (ROOT / ".github" / "scripts" / "checks_license_self_reporting.py")
    if not _self469.exists():
        warnings.append("Check 469: self-reporting module が無い — face 照合を skip")
    else:
        _src469 = _self469.read_text(encoding="utf-8")
        _doc469 = _src469.split('"""')[1] if _src469.count('"""') >= 2 else ""
        # 460 の inventory ブロックだけを見る (469 自身の (a)/(b) を拾わないため = 自己参照回避)
        _m469 = re.search(r"^  460\..*?(?=^  \d+\.)", _doc469, re.S | re.M)
        # **範囲の言及は entry ではない** —— 初版は `(a)〜(p)` の端点まで「宣言済み」と数え、
        # **(p) の記述を丸ごと消しても緑だった**（動機になった drift を素通り）。
        # 前後が波ダッシュのものを落とす。
        _decl469 = ({m.group(1) for m in re.finditer(r"(?<![〜～])\(([a-z])\)(?![〜～])",
                                                     _m469.group(0))} if _m469 else set())
        _impl469 = set(re.findall(r"^\s{8}# \(([a-z])\)", _src469, re.M))
        if not _m469:
            _bad469.append("(a) docstring から Check 460 の inventory ブロックを取り出せない")
        elif _decl469 != _impl469:
            _bad469.append(
                f"(a) face の列挙と実装が食い違う: 宣言のみ {sorted(_decl469 - _impl469)} / "
                f"実装のみ {sorted(_impl469 - _decl469)} "
                f"(宣言 {len(_decl469)} 面 / 実装 {len(_impl469)} 面)")

    # (b) errata の E-ID ⟺ CHANGELIST §1 表、かつ CHANGELIST 内部で状態が矛盾しないこと
    _er469 = _L460 / "ACD-1.0.errata.md"
    # **版を決め打ちしない（2026-09-18 に直した）。** 1.1 を確定させて作業場が 1.2 へ移ると、
    # **1.2 の表に載せた errata が「CHANGELIST に無い」と報告される。**
    # Check 464 と同じ形の欠陥で、**確定手順が列挙していた「版に紐づく Check」に両方とも
    # 入っていなかった** —— **列挙は、列挙した時点で見えていたものしか含まない。**
    _cls469 = sorted(_L460.glob("ACD-*-CHANGELIST.md"))
    if not (_er469.exists() and _cls469):
        # 必須文書の欠落を warning にしない (Check 460 と同じ理由・2026-11-01)。
        check(False, "Check 469: errata / changelist",
              "Check 469: errata か CHANGELIST が見つからない — (b) 状態照合が skip される。"
              "改名したなら本 Check の読み先も直せ", blocking=True)
    else:
        _ert = _er469.read_text(encoding="utf-8")
        _clt = "\n".join(_p.read_text(encoding="utf-8") for _p in _cls469)
        _erids = set(re.findall(r"^\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|", _ert, re.M))
        _rows469 = dict(re.findall(r"^\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|(.*)$", _clt, re.M))
        if not _erids:
            _bad469.append("(b) errata.md から E-ID を 1 件も取り出せない")
        if _erids != set(_rows469):
            _bad469.append(
                f"(b) errata.md と CHANGELIST の E-ID が対応しない: "
                f"errata のみ {sorted(_erids - set(_rows469))} / "
                f"CHANGELIST のみ {sorted(set(_rows469) - _erids)}")

        # 状態語彙: settled = もう動かないと述べたもの / pending = まだと述べたもの
        #   2026-11-09 (Check の監査 #7 / #19): CHANGELIST は同じ状態を「閉じた」(34 回)「入った」「未反映」とも書く
        _settled469 = ("反映済み", "直さないと決めた", "狭めないと決めた", "触らない", "閉じた", "入った")
        _pending469 = ("未着手", "まだ見ていない", "反映予定", "未反映")

        def _ids_on(line):
            """1 行が状態を述べている E-ID 集合 (E6〜E10 のような範囲も展開する)。"""
            # 前に英字が無いものだけを E-ID とする (2026-11-04・portfolio-25 の報告): bb の反例番号
            #   「CE10」の中の E10 を拾い、E10 が「反映済み」と「未着手」で矛盾していると誤って RED にした。
            got = set(re.findall(r"(?<![A-Za-z])E(\d+)", line))
            for a, b in re.findall(r"(?<![A-Za-z])E(\d+)\s*[〜～–-]\s*E?(\d+)", line):
                got |= {str(n) for n in range(int(a), int(b) + 1)}
            return {"E" + n for n in got}

        # 状態の語は、それを述べている E-ID にだけ割り当てる (2026-11-11・監査 #8)。行ごとに分類すると、
        #   両方の語を持つ行は行の全 E-ID が "both" になり、「E12 は未着手（E3 は反映済み）」の未着手が
        #   {both, settled} に埋もれて矛盾の組から消えた。E-ID を最初のセルに持つ行は、各セルの語を
        #   その行の E-ID に、セルの中で別の E-ID の後に続く語はその E-ID に割り当てる。
        #   それ以外の行は、片方の語彙だけなら従来どおり行の全 E-ID に、両方なら同じ規則で割り当てる。
        #   1 つの E-ID が同じ行で両方を受けたら "both" (「前の状態 / 当てた結果」の表の行)。
        _id469 = r"(?<![A-Za-z])E\d+(?:\s*[〜～–-]\s*E?\d+)?"
        _grp469 = re.compile(_id469 + r"(?:\s*(?:[/,、・+＋]|and|と|及び)?\s*" + _id469 + r")*")

        def _words469(seg):
            return ({"s"} if any(w in seg for w in _settled469) else set()) | (
                {"p"} if any(w in seg for w in _pending469) else set())

        def _states_on(line):
            """1 行について {E-ID: 受けた語彙 {'s','p'}}。"""
            _w = _words469(line)
            if not _w:
                return {}
            _key = re.match(r"^\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|", line)
            if not _key and len(_w) == 1:
                return {i: set(_w) for i in _ids_on(line)}
            _out = {}
            _cells = re.split(r"(?<!\\)\|", line) if line.startswith("|") else [line]
            if _key:
                _cells = _cells[2:]
            for _cell in _cells:
                _ms = list(_grp469.finditer(_cell))
                _owner = {_key.group(1)} if _key else (_ids_on(_ms[0].group(0)) if _ms else set())
                _pos = 0
                for _mm in _ms + [None]:
                    _seg = _cell[_pos:_mm.start()] if _mm else _cell[_pos:]
                    for i in _owner:
                        if _words469(_seg):
                            _out.setdefault(i, set()).update(_words469(_seg))
                    if _mm:
                        _owner, _pos = _ids_on(_mm.group(0)), _mm.end()
            return _out

        _claim469 = {}
        for raw in _clt.splitlines():
            line = raw.strip()
            if line.startswith(">"):      # 引用は現在の主張ではない (#977 と同じ線引き)
                continue
            for i, _w in _states_on(line).items():
                _claim469.setdefault(i, set()).add("both" if _w == {"s", "p"} else
                                                   "settled" if _w == {"s"} else "pending")
        for i in sorted(_claim469, key=lambda x: int(x[1:])):
            if _claim469[i] == {"settled", "pending"}:
                _bad469.append(
                    f"(b) {i} の状態が file 内で矛盾している (ある行は決着済み / 別の行は未着手)")
        # errata の冒頭が閉じたと述べる E-ID は、CHANGELIST で未着手だけを述べてはならない (2026-11-09・監査 #6):
        #   状態の行が 1 つしか無い E-ID は、それを未着手へ書き換えても矛盾の組が作れず黙って通った
        _cl469 = re.search(r"of them \(([^)]*)\) are closed", _ert)
        _closed469 = set(re.findall(r"E\d+", _cl469.group(1))) if _cl469 else set()
        if not _cl469:
            _bad469.append("(b) errata.md の冒頭の「N of them (E…) are closed」が読めない")
        for i in sorted((i for i in _claim469 if _claim469[i] == {"pending"} and i in _closed469), key=lambda x: int(x[1:])):
            _bad469.append(f"(b) {i} は errata が閉じたと述べるのに、CHANGELIST は未着手だけを述べている")

    # (c) READY-TO-SUBMIT.md の「Check N (M 部)」⟺ その Check の区間に現れる下位部 N[a-z] の種類数
    #   portfolio-25 の提案 (2026-11-03)。「機械的に担保されていること」と名乗る表が、451 に
    #   451d (10-17)・451e (11-01) を足したあとも「3 部」のままだった (#2331 で是正)。部の列挙は
    #   足されても申告側が追従しない —— 自分の数を機械で担保していない面だった。
    #   区間 = `# ── N.` から次の `# ── <数字>` まで (全 Check module を横断)。
    _rts469 = _L460 / "READY-TO-SUBMIT.md"
    # 全角の括弧も読む (2026-11-09・監査 #10): 日本語の文書は全角の括弧で書かれ、`Check 445（9 部）` の行は
    #   黙って落ち、行が減っても「1 行は在る」の床しか無かった。「部」の数を述べる行で読めないものも RED
    _rts469t = _rts469.read_text(encoding="utf-8") if _rts469.exists() else ""
    _rows469c = re.findall(r"Check (\d+) ?[(（](\d+) ?部[)）]", _rts469t)
    _stray469c = [_l[:40] for _l in _rts469t.splitlines() if re.search(r"Check \d+\D{0,4}\d+ ?部", _l)
                  and not re.search(r"Check \d+ ?[(（]\d+ ?部[)）]", _l)]
    if not _rows469c:
        _bad469.append("(c) READY-TO-SUBMIT.md から「Check N (M 部)」を 1 件も取り出せない")
    if _stray469c:
        _bad469.append(f"(c) READY-TO-SUBMIT.md に読めない部数の申告がある: {_stray469c}")
    _srcs469c = [ROOT / ".github" / "scripts" / "check_repository_consistency.py"] + sorted(
        (ROOT / ".github" / "scripts").glob("checks_*.py"))
    _txt469c = [_f.read_text(encoding="utf-8") for _f in _srcs469c if _f.exists()]
    for _n, _m in _rows469c:
        _parts = set()
        for _t in _txt469c:
            for _sec in re.finditer(r"^\s*# ── " + _n + r"\..*?(?=^\s*# ── \d|\Z)", _t, re.S | re.M):
                _parts |= set(re.findall(r"\b" + _n + r"([a-z])\b", _sec.group(0)))
        if len(_parts) != int(_m):
            _bad469.append(f"(c) READY-TO-SUBMIT.md は「Check {_n} ({_m} 部)」と述べるが、実装の区間に在る下位部は "
                           f"{len(_parts)} 種 {sorted(_parts)}")
    check(
        not _bad469,
        "Check 469: 自己申告の列挙が実装・現物と一致 "
        f"(Check 460 の face {len(_impl469)} 面 / errata {len(_erids)} 件 / 部数の申告 {len(_rows469c)} 行)",
        ("Check 469: 自己申告の「列挙」が古い: " + "; ".join(_bad469) +
         "。**列挙は項目を消化するたびに古くなり、消化しているその瞬間こそ列挙を見ていない。**"
         "数と違って減る側へ drift するので「増えたか」では検出できない ——"
         "**成果物から導出し直せ** (実測 2026-09-13: §0.7 が 7 件を『まだ見ていない』と述べ、"
         "うち 6 件は既に閉じていた)"),
        blocking=True,
    )

    # ── 474. 不利な事実の register が、潰すための backlog として機械可読であること ─────────
    #   **steward 明言（2026-09-23）: 「ライセンス全てを敵対的検証して貰ってるのは、全て潰す
    #   ためです。経過で増減するのは問題無いです。最終的に全て潰してください。」**
    #   **にもかかわらず 219 entry のどれにも状態欄が無く、開いている項目を導出できなかった。**
    #   実測すると `Status` 欄の判定語は **140 種**あり、**69 entry は太字ですらない** ——
    #   **散文からは確信を持って分類できない。無い field は作るしかない。**
    #   **⚠ 件数は宣言しない。** この Check の OK 行が唯一の集計であり、**現物から導出する。**
    #   宣言を置くと、消化しているその瞬間に古くなる（Check 469 が記録している class）。
    _V474 = ("CLOSED", "TEXT", "DOSSIER", "EXTERNAL", "TRADE", "OPEN", "UNTRIAGED")
    _p474 = ROOT / "LICENSES" / "ACD-1.0.against.md"
    if _p474.exists():
        _t474 = _p474.read_text(encoding="utf-8")
        # 行は「番号で始まる行」を全部拾い、`| N |` の形でなければ RED にする。太字の番号の行は
        #   以前の正規表現に見えず、状態の欄が無くても集計から黙って落ちていた (460 (e) と 491 も同じ形で数える)。
        #   セルは `\|` を除いて分ける。本文の `\|` で止まる `[^|]*` は #162 を 474b から外していた。
        #   番号の重複も RED: dict は後の行で前の行を上書きし、開いた entry が集計から消えていた。
        def _cells474(_row):
            _r = _row.strip()[1:]
            _r = _r[:-1] if _r.endswith("|") and not _r.endswith("\\|") else _r
            return [_x.strip() for _x in re.split(r"(?<!\\)\|", _r)]
        _bad474, _seen474, _rows474 = [], {}, []
        for _l in _t474.splitlines():
            _m = re.match(r"^\s{0,3}\|\s*\**\s*(\d+)\s*\**\s*\|", _l)
            if not _m:
                continue
            _n = _m.group(1)
            if not _l.startswith(f"| {_n} |"):
                _bad474.append(f"#{_n}: 番号のセルを `| {_n} |` と書いていない (460 (e) と 491 はこの形で数える)")
                continue
            if _n in _seen474:
                _bad474.append(f"#{_n}: 番号が重複している (後の行が前の行を集計から消す)")
                continue
            _c = _cells474(_l)
            _st = _c[2] if len(_c) >= 3 else ""
            _tok = re.findall(r"\*\*\[([A-Z]+)\]\*\*", " | ".join(_c[1:]))
            if len(_tok) != 1:
                _bad474.append(f"#{_n}: state token が {len(_tok)} 個 (ちょうど 1 個にせよ)")
                continue
            if not re.match(r"\*\*\[[A-Z]+\]\*\*", _st):
                _bad474.append(f"#{_n}: state token が Status 欄の先頭に無い")
                continue
            if _tok[0] not in _V474:
                _bad474.append(f"#{_n}: 未知の state token {_tok[0]!r} (語彙は {_V474})")
                continue
            _seen474[_n] = _tok[0]
            _rows474.append((_n, _tok[0], _st))
        # 番号は 1 から連番 (行を 900 へ書き換えると欠番と飛んだ最大が残り、460 (e) / 491 の「最新 #N」が狂う)
        _ints474 = sorted(int(_x) for _x in _seen474)
        if _ints474 and _ints474 != list(range(1, len(_ints474) + 1)):
            _bad474.append(f"番号が 1 から連番でない (欠番 {sorted(set(range(1, _ints474[-1] + 1)) - set(_ints474))[:5]} / 最大 {_ints474[-1]} / 行 {len(_ints474)})")
        # 凡例は語彙を過不足なく挙げる (使っていない OPEN / UNTRIAGED も、使ってよい語として載せる)
        _leg474 = set(re.findall(r"\*\*`\[([A-Z]+)\]`\*\*", _t474))
        if _leg474 != set(_V474):
            _bad474.append(f"凡例と語彙が食い違う: 凡例に無い {sorted(set(_V474) - _leg474)} / 語彙に無い {sorted(_leg474 - set(_V474))}")
        # ── 474b: `EXTERNAL` と `TRADE` は「我々に何ができるか」を必ず述べること ───────────
        #   **外部依存を「待ち」ではなく作業へ変える唯一の形は、各件に *我々にできることは
        #   ここまで* と書くことである**（steward 2026-09-23「最終的に全て潰してください」)。
        #   **書かれていない `EXTERNAL` は、記録の形をした「待ち」である。**
        #   `TRADE` は直すものが無い区分なので、代わりに**合否**（立場を述べ切れているか）を書く。
        #   ⚠ **初回の自動導出では 48 件が無記載だった**。埋める過程で、**5 件は分類そのものが
        #   誤っており（我々の側の作業を外部依存と読んでいた）**、そちらも訂正した ——
        #   **「外部依存」に見えるものの中に我々の作業が混じっていることが、待ちを作る。**
        _need474b = ("潰し方", "合否", "我々にできる", "我々の側でできる")
        _bad474b = [f"#{_n} ({_k})" for _n, _k, _st in _rows474
                    if _k in ("EXTERNAL", "TRADE") and not any(_w in _st for _w in _need474b)]
        if _bad474b:
            _bad474.append(
                f"`EXTERNAL` / `TRADE` なのに「我々に何ができるか」が書かれていない: {_bad474b}"
                " —— **書かれていない外部依存は、記録の形をした「待ち」である**")
        _cnt474 = {k: sum(1 for v in _seen474.values() if v == k) for k in _V474}
        _open474 = sum(v for k, v in _cnt474.items() if k != "CLOSED")
        check(
            not _bad474 and _seen474,
            ("Check 474: register が backlog として機械可読 —— "
             + " / ".join(f"{k} {_cnt474[k]}" for k in _V474)
             + f" (閉じていない = {_open474} / 全 {len(_seen474)})"),
            (f"Check 474: {_bad474}。**この register は記録ではなく潰すための backlog である**"
             "（steward 2026-09-23）。**各 entry は `Status` 欄の先頭に state token を"
             "ちょうど 1 つ持つこと。** 分類できないものを勝手に `CLOSED` にせず "
             "`[UNTRIAGED]` を使え ——**未分類の数を見せるほうが潰せる**"),
            blocking=True,
        )
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 474: 対象ファイル",
              f"Check 474: 検査対象 {_p474.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

    # ── 475. 反証表の全行が日付つきの状態を宣言していること (BLOCKING) ──────────────
    #   表自身が「観測が来たら、まずここを見る」と述べているのに、それを見る層が無かった。
    #   **強制できるのは「状態が宣言されていること」まで** —— 条件が満たされたかは世界に
    #   ついての判断で機械には見えない。鮮度の閾値は置かない（日数で赤くすると CI が腐る）。
    _as475 = ROOT / "LICENSES" / "AS-OF.md"
    if _as475.exists():
        _t475 = _as475.read_text(encoding="utf-8")
        # **表は 1 つではない** —— AS-OF.md は「何を測ったか」の在庫表も持つので、
        #   反証表の見出し行から次の空行までに限定する。**初版は file 全体の `| **` を
        #   拾って 65 行を誤検出した** ——走査の起点を決めずに書いた結果である。
        #   表は空行で終わる (GFM と同じ)。`|` で始まらない行で走査を止めると、先頭に空白が 1 つ入った行から
        #   下が黙って「全 N 行」から外れていた。印と日付は隣り合うものだけを状態と読む: 行のどこかの日付
        #   (引用の日付・訂正の日付) で、状態の日付を消した行が緑のままだった。日付は暦として読む。
        _rows475, _in475 = [], False
        for _l in _t475.splitlines():
            if _l.startswith("| いま採っている読み"):
                _in475 = True
                continue
            if _in475:
                if not _l.strip():
                    break
                if re.match(r"^\s*\|?[\s:|-]+$", _l):
                    continue
                _rows475.append(_l)
        _bad475 = []
        for _r475 in _rows475:
            _head = re.sub(r"\*\*|\*", "", (_r475.split("|") + ["", ""])[1]).strip()[:36]
            _st475 = re.findall(r"(?:\U0001F534|\U0001F7E1|\u26aa|\u26ab)\s*[^\s|（(<*]{0,8}\s*[（(]?\s*(20\d\d-\d\d-\d\d)", _r475)
            if not _r475.startswith("|"):
                _bad475.append(f"「{_head}」が `|` で始まらない")
            elif not re.search(r"(\U0001F534|\U0001F7E1|\u26aa|\u26ab)", _r475):
                _bad475.append(f"「{_head}」に状態の印が無い")
            elif not _st475:
                _bad475.append(f"「{_head}」の状態の印の隣に日付が無い")
            else:
                for _d475 in _st475:
                    try:
                        datetime.date.fromisoformat(_d475)
                    except ValueError:
                        _bad475.append(f"「{_head}」の状態の日付 {_d475} は暦に無い")
        check(
            bool(_rows475) and not _bad475,
            f"Check 475: 反証表の全 {len(_rows475)} 行が日付つきの状態を宣言",
            (f"Check 475: 反証表の行が状態を宣言していない: {_bad475 or '行が 0 件 —— 走査が対象を見失っている'}。"
             "**この表は「観測が来たら、まずここを見る」と自分で述べている**のに、"
             "見る層が無かった（#192: 条件が満たされてから 9 日間 / #225 の掃引で 2 例目）。"
             "**⚠ 本 Check が防ぐのは「行が無言のまま古くなる」ことだけで、「気づかない」ことは防げない。** "
             "状態の印と ISO 日付を置け"),
            blocking=True)
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 475: 対象ファイル",
              f"Check 475: 検査対象 {_as475.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

    # ── 491. register の英語の索引が日本語の索引の写しであること (BLOCKING) ───────────────
    #   英語の審査者が読むのは冒頭の索引で、日本語の索引は下に在る。項目を足すと片方だけ増える。
    _br491 = _L460 / "ACD-OSI-BOTTLENECKS.md"
    _t491 = _br491.read_text(encoding="utf-8") if _br491.exists() else ""
    #   ID の重複も RED: dict は後の行で前の行を上書きし、上に置いた古い行が差にも件数にも出なかった。
    _enl491 = re.findall(r"^\| (B\d+) \|[^|]*\| (Highest|High|Medium|Low) \|", _t491, re.M)
    _sev491 = {"最高": "Highest", "高": "High", "中": "Medium", "低": "Low"}
    _jal491 = [(_b, _sev491.get(_v.strip(" *"), _v.strip())) for _b, _v in
               re.findall(r"^\| \*\*(B\d+)\*\* \|[^|]*\| ([^|]+?) \|", _t491, re.M)]
    _en491, _ja491 = dict(_enl491), dict(_jal491)
    _dup491 = sorted({_b for _l491 in (_enl491, _jal491) for _b, _ in _l491 if [_x for _x, _ in _l491].count(_b) > 1})
    _diff491 = sorted((_b, _en491.get(_b), _ja491.get(_b)) for _b in set(_en491) | set(_ja491)
                      if _en491.get(_b) != _ja491.get(_b))
    check(
        len(_en491) >= 10 and not _diff491 and not _dup491,
        f"Check 491: register の英語の索引 {len(_en491)} 項目が日本語の索引と ID・重大度で一致",
        (f"Check 491: register の 2 つの索引が食い違う (項目 {len(_en491)} / 差 (ID, 英語, 日本語) {_diff491} / 重複した ID {_dup491})。"
         "**審査者が読むのは英語の索引である。** 項目を足したら両方へ書け"),
        blocking=True,
    )
    _om491 = _L460 / "ACD-1.0.objection-map.md"
    _mc491 = re.search(r"last caught up at #(\d+)", _om491.read_text(encoding="utf-8") if _om491.exists() else "")
    _ag491 = _L460 / "ACD-1.0.against.md"
    _top491 = max((int(_n) for _n in re.findall(r"^\| (\d+) \|", _ag491.read_text(encoding="utf-8"), re.M)), default=0) if _ag491.exists() else 0
    check(bool(_mc491), "Check 491: objection-map が追いついた番号を述べる",
          "Check 491: objection-map から \"last caught up at #N\" の文が消えた (鮮度を見られなくなる)", blocking=True)
    if _mc491:
        check(
            int(_mc491.group(1)) >= _top491,
            f"Check 491 (ADVISORY): objection-map は against.md の最新 #{_top491} まで追いついている",
            (f"Check 491 (ADVISORY): objection-map は #{_mc491.group(1)} までで、against.md は #{_top491} まで在る。"
             "読んで反論を足すか、足すものが無いと判断したなら数を上げよ (この表は 2 度古くなった)"),
            blocking=False,
        )
