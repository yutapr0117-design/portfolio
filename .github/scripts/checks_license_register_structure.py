"""ライセンス register の *構造* が機械可読であり続けることを守る Check 群。

   `checks_license_self_reporting.py` から 2026-09-27 に切り出した。**引き金は advisory 予算
   (800 行) だが、割る線は行数ではなく主題で選んだ** —— **あちらは「自己申告した *数* が実測と
   合うか」、ここは「自己申告した *構造* が使える形で在り続けるか」**（列挙・state token・
   反証表の状態）。**読み手も直し方も違う**: 数はふつう申告側を直し、構造は register 側を直す。

   469. 自己申告の「列挙」が、消化した項目で古くならないこと (BLOCKING)
   474. 不利な事実の register が、潰すための backlog として機械可読であること (BLOCKING)
   475. 反証表の全行が日付つきの状態を宣言していること (BLOCKING)
"""

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
        warnings.append("Check 469: errata / changelist が無い — 状態照合を skip")
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
        _settled469 = ("反映済み", "直さないと決めた", "狭めないと決めた", "触らない")
        _pending469 = ("未着手", "まだ見ていない", "反映予定")

        def _ids_on(line):
            """1 行が状態を述べている E-ID 集合 (E6〜E10 のような範囲も展開する)。"""
            got = set(re.findall(r"E(\d+)", line))
            for a, b in re.findall(r"E(\d+)\s*[〜～–-]\s*E?(\d+)", line):
                got |= {str(n) for n in range(int(a), int(b) + 1)}
            return {"E" + n for n in got}

        _claim469 = {}
        for raw in _clt.splitlines():
            line = raw.strip()
            if line.startswith(">"):      # 引用は現在の主張ではない (#977 と同じ線引き)
                continue
            hit_s = any(w in line for w in _settled469)
            hit_p = any(w in line for w in _pending469)
            if not (hit_s or hit_p):
                continue
            for i in _ids_on(line):
                _claim469.setdefault(i, set()).add("settled" if hit_s and not hit_p else
                                                   "pending" if hit_p and not hit_s else "both")
        for i in sorted(_claim469, key=lambda x: int(x[1:])):
            if _claim469[i] == {"settled", "pending"}:
                _bad469.append(
                    f"(b) {i} の状態が file 内で矛盾している (ある行は決着済み / 別の行は未着手)")

    check(
        not _bad469,
        "Check 469: 自己申告の列挙が実装・現物と一致 "
        f"(Check 460 の face {len(_impl469)} 面 / errata {len(_erids)} 件)",
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
        _bad474, _seen474 = [], {}
        for _l in _t474.splitlines():
            _m = re.match(r"^\| (\d+) \|[^|]*\|\s*(.*)$", _l)
            if not _m:
                continue
            _n, _rest = _m.group(1), _m.group(2)
            _tok = re.findall(r"\*\*\[([A-Z]+)\]\*\*", _rest)
            if len(_tok) != 1:
                _bad474.append(f"#{_n}: state token が {len(_tok)} 個 (ちょうど 1 個にせよ)")
                continue
            if _tok[0] not in _V474:
                _bad474.append(f"#{_n}: 未知の state token {_tok[0]!r} (語彙は {_V474})")
                continue
            _seen474[_n] = _tok[0]
        # 凡例が、実際に使われている token を過不足なく列挙していること（Check 469 の class）
        _leg474 = set(re.findall(r"\*\*`\[([A-Z]+)\]`\*\*", _t474))
        _used474 = set(_seen474.values())
        if _used474 - _leg474:
            _bad474.append(f"凡例に無い token が使われている: {sorted(_used474 - _leg474)}")
        if _leg474 - set(_V474):
            _bad474.append(f"凡例が語彙に無い token を挙げている: {sorted(_leg474 - set(_V474))}")
        # ── 474b: `EXTERNAL` と `TRADE` は「我々に何ができるか」を必ず述べること ───────────
        #   **外部依存を「待ち」ではなく作業へ変える唯一の形は、各件に *我々にできることは
        #   ここまで* と書くことである**（steward 2026-09-23「最終的に全て潰してください」)。
        #   **書かれていない `EXTERNAL` は、記録の形をした「待ち」である。**
        #   `TRADE` は直すものが無い区分なので、代わりに**合否**（立場を述べ切れているか）を書く。
        #   ⚠ **初回の自動導出では 48 件が無記載だった**。埋める過程で、**5 件は分類そのものが
        #   誤っており（我々の側の作業を外部依存と読んでいた）**、そちらも訂正した ——
        #   **「外部依存」に見えるものの中に我々の作業が混じっていることが、待ちを作る。**
        _need474b = ("潰し方", "合否", "我々にできる", "我々の側でできる")
        _bad474b = []
        for _l474 in _t474.splitlines():
            _m474 = re.match(r"^\| (\d+) \|[^|]*\|\s*\*\*\[(EXTERNAL|TRADE)\]\*\*(.*)$", _l474)
            if not _m474:
                continue
            if not any(_k in _m474.group(3) for _k in _need474b):
                _bad474b.append(f"#{_m474.group(1)} ({_m474.group(2)})")
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
        _rows475, _in475 = [], False
        for _l in _t475.splitlines():
            if _l.startswith("| いま採っている読み"):
                _in475 = True
                continue
            if _in475:
                if not _l.startswith("|"):
                    break
                if _l.startswith("|---") or set(_l) <= set("|- "):
                    continue
                _rows475.append(_l)
        _bad475 = []
        for _r475 in _rows475:
            _head = re.sub(r"\*\*|\*", "", _r475.split("|")[1]).strip()[:36]
            if not re.search(r"(\U0001F534|\U0001F7E1|\u26aa|\u26ab)", _r475):
                _bad475.append(f"「{_head}」に状態の印が無い")
            elif not re.search(r"20\d\d-\d\d-\d\d", _r475):
                _bad475.append(f"「{_head}」に日付が無い")
        check(
            bool(_rows475) and not _bad475,
            f"Check 475: 反証表の全 {len(_rows475)} 行が日付つきの状態を宣言",
            (f"Check 475: 反証表の行が状態を宣言していない: {_bad475 or '行が 0 件 —— 走査が対象を見失っている'}。"
             "**この表は「観測が来たら、まずここを見る」と自分で述べている**のに、"
             "見る層が無かった（#192: 条件が満たされてから 9 日間 / #225 の掃引で 2 例目）。"
             "**⚠ 本 Check が防ぐのは「行が無言のまま古くなる」ことだけで、「気づかない」ことは防げない。** "
             "状態の印と ISO 日付を置け"),
            blocking=True)

