"""
checks_license_self_reporting.py — ドシエが自分について述べる数字を、実測と突き合わせる Check
(extracted from checks_license_dossier.py — check.py split track・category "self-reporting").

このモジュールは **「自分の状態について書いた文は、いま真か」** という 1 つの invariant だけを
所有する。ライセンス・ドシエは自分の規模を数字で述べる（「全 82 条」「198 worked entries」
「All 110 adverse facts」）。**読み手はその数字を根拠に「網羅されている」と判断する**ので、
古い数字は網羅の主張を嘘にする。

**この class の失敗は 2 種類ある。** (1) 動く数（一覧が伸びる・日付が進む）と、
(2) **書いた時点で誤り**（入力が凍結されていて drift しようがない）。**再確認は「前と変わったか」
しか見ないので (2) を永久に見つけない** —— 唯一の対処は**成果物から導出し直す**ことであり、
本モジュールの各面はすべてそう書かれている。

**分割の理由**: 面は増える一方で（2026-09-09 時点で 12 面）、`checks_license_dossier.py` は
「ライセンス文書群の自己整合」という別テーマの Check（458 / 459 / 463〜466）を持つ。
2026-09-09 に同 file が advisory (800) を越えたので、**いま触っているクラスタ**を切り出した
（`checks_mutation_integrity.py` を `checks_maintainability.py` から切り出したのと同じ手）。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/warnings by reference (exec 不使用) so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  460. **ドシエが自己申告する件数が実測と一致すること** (BLOCKING): ライセンス文書群は
       「全 82 条」「38 worked entries」「使う側 21 問」のように**自分の規模を数字で述べる**。
       この数字は**書いた当日に drift する** —— 実測 (2026-08-27): FAQ に 9 問足した結果、
       索引と mirror が「使う側 12 問」のまま残り、逆引き表の行数も 2 箇所でずれていた。
       読み手は数字を根拠に「網羅されている」と判断するので、**古い数字は網羅の主張を
       嘘にする**。面は増える一方なので**数を書かずに列挙する**（この docstring 自身が
       「3 面」と述べたまま 7 面へ育っていた —— 本 Check が禁じている当のこと）: (a) 提出パケットの worked entries / short answers ↔
       想定問答 3 分冊の `### ` 見出しと短答表の実測、(b) 索引の「使う側 N 問 / プロセス M 問」
       ↔ FAQ の `### AN.` / `### BN.` の実測、(c) 逐条リファレンスの「全 X 節 Y 条」↔
       ACD-1.0.txt から抽出した節数・条数、(d) FAQ mirror の件数、(e) against.md が
       自分の規模について述べる数字、(f) QUESTION-INDEX の worked entry 総数、
       (k) **ドシエ内の `#N` / `E<n>` 参照がすべて解決すること** —— 実測 (2026-09-06) で
       1 件だけ `#885`（**リポジトリの PR 番号**）が混ざっていた。同じ記法に 2 つの採番体系が
       あると審査者は存在しない不利な事実を探しに行く。`#N` を 1 つの意味に限定する。
       (j) **`comparison.md` §1.35 の「N のうち M」が下の 2 つの列挙と一致すること** ——
       実測 (2026-09-06): 「six / remaining two」と書きながら列挙は 4 + 3 = 7 だった。宣言と
       列挙が同じ commit で入っており、書いた時点の誤り。宣言ではなく**列挙から導く**。
       (i) **提出パケット §4c の「機械的に確かめたこと」の数値** —— face (a) は同じ file の
       別の 1 文しか見ておらず §4c の表は素通りだった。実測 (2026-09-06): 「50 entries, 1–50」
       （実体 63）と「29 / 29 clause pointers」（実体 33）。**§4c は「弁護士が読んでいない」への
       答えで、価値は機械で確かめられること**にあるため、数字が合わないと節ごと逆の証拠になる。
       (h) **`docs/files/LICENSES/` の mirror が規模を数字で述べないこと** —— (a)〜(g) は
       捕まるたびに 1 面ずつ後付けした比較なので、被覆は「drift を目撃した場所」であって
       「drift しうる場所」ではない。実測 (2026-09-06): 柵の外に 4 件残っていた。mirror は
       規模を述べる読者価値が無いので、比較ではなく**禁止**で守る。
       (g) **入口ページ `REVIEWERS.md` と `READY-TO-SUBMIT.md` が述べる規模**
       —— 2026-09-05 に 5 件 stale で見つかった面で、しかも 3 つとも**過少**申告
       だった（「All 14 adverse facts」に対し実体 57）。**最後に書かれ最初に読まれるページ**が
       (a)〜(f) のどこにも入っていなかった。Check 413b（内訳の和 = 合計）と同じ
       「**書いた数は数えて確かめる**」族。(BLOCKING)
"""

import json
import re
from types import SimpleNamespace  # noqa: F401  (ctx の型を読者に示すためだけの import)

# NOTE: `re` と `json` は本 module が自分で import する。monolith から切り出したとき **これを
# 忘れて NameError を出した** —— そして run() の途中で例外が上がると **その Check は一度も
# 走らないまま、後続の Check もすべて skip される**（#885 / Check 400 と同じ形）。
# エラーは「ERROR:」ではなく traceback として出るので、`grep '^ERROR'` は空を返し、
# **「非 vacuity 検証で何も出なかった＝壊れていない」と読み違えかけた。**
# **抽出したモジュールは、まず「意図した Check が実際に走ったか」を OK 行で確かめること。**


def run(ctx):
    """Run the self-reporting Check against the repository described by `ctx`."""
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings  # noqa: F841  (Check 385: error/skip 枝が bare append しても NameError にしない)
    errors = ctx.errors      # noqa: F841

    # ── 460. ドシエが自己申告する件数が実測と一致すること (BLOCKING) ────────────────────
    # 数字は書いた当日に drift する。読み手は数字を根拠に「網羅されている」と判断するので、
    # 古い数字は網羅の主張を嘘にする。
    _L460 = ROOT / "LICENSES"
    _bad460 = []

    def _read460(name):
        p = _L460 / name
        return p.read_text(encoding="utf-8") if p.exists() else None

    _rr460 = _read460("ACD-1.0.review-responses.md")
    _rc460 = _read460("ACD-1.0.review-responses-clauses.md")
    _rm460 = _read460("ACD-1.0.review-responses-meta.md")
    _fq460 = _read460("ACD-1.0.faq.md")
    _sb460 = _read460("ACD-1.0.submission.md")
    _cr460 = _read460("ACD-1.0.clause-reference.md")
    _tx460 = _read460("ACD-1.0.txt")

    if None in (_rr460, _rc460, _rm460, _fq460, _sb460, _cr460, _tx460):
        warnings.append("Check 460: ライセンス文書の一部が無い — 件数照合を skip")
    else:
        # (a) 提出パケットの worked entries / short answers
        _entries460 = sum(len(re.findall(r"^### ", t, re.M)) for t in (_rr460, _rc460, _rm460))
        _sec7 = re.search(r"^## 7\..*?(?=^## )", _rr460, re.S | re.M)
        _short460 = (len(re.findall(r"^\| ", _sec7.group(0), re.M)) - 1) if _sec7 else -1
        _m = re.search(r"\((\d+) worked entries plus a table of (\d+) short answers", _sb460)
        if not _m:
            _bad460.append("submission.md: worked entries の申告が見つからない")
        else:
            if int(_m.group(1)) != _entries460:
                _bad460.append(f"submission.md worked entries: 申告 {_m.group(1)} / 実測 {_entries460}")
            if int(_m.group(2)) != _short460:
                _bad460.append(f"submission.md short answers: 申告 {_m.group(2)} / 実測 {_short460}")

        # (b) 索引の「使う側 N 問 / プロセス M 問」
        _fa460 = len(re.findall(r"^### A\d+\.", _fq460, re.M))
        _fb460 = len(re.findall(r"^### B\d+\.", _fq460, re.M))
        _m2 = re.search(r"使う側 (\d+) 問 / プロセス (\d+) 問", _rr460)
        if not _m2:
            _bad460.append("review-responses.md: FAQ 件数の申告が見つからない")
        else:
            if int(_m2.group(1)) != _fa460:
                _bad460.append(f"索引の使う側: 申告 {_m2.group(1)} / 実測 {_fa460}")
            if int(_m2.group(2)) != _fb460:
                _bad460.append(f"索引のプロセス: 申告 {_m2.group(2)} / 実測 {_fb460}")

        # (c) 逐条リファレンスの「全 X 節 Y 条」
        _secs460 = len(re.findall(r"^\d+\.\s+\S", _tx460, re.M))
        _cls460 = len(re.findall(r"^\s{2}\d+\.\d+\s+", _tx460, re.M))
        _m3 = re.search(r"全 (\d+) 節 (\d+) 条", _cr460)
        if not _m3:
            _bad460.append("clause-reference.md: 節数・条数の申告が見つからない")
        else:
            if int(_m3.group(1)) != _secs460 or int(_m3.group(2)) != _cls460:
                _bad460.append(f"逐条リファレンス: 申告 {_m3.group(1)} 節 {_m3.group(2)} 条 / "
                               f"実測 {_secs460} 節 {_cls460} 条")

        # (d) mirror doc の申告。**stale だった 4 件のうち 2 件は mirror 側**だった ——
        #   本体だけ縛ると、doc-about-doc が古い数字を主張し続ける。
        _mir460 = ROOT / "docs" / "files" / "LICENSES" / "ACD-1.0.faq.md.md"
        if _mir460.exists():
            _m4 = re.search(r"\*\*A\. 使う側\*\*（(\d+) 問）", _mir460.read_text(encoding="utf-8"))
            if not _m4:
                _bad460.append("faq mirror: 使う側の件数申告が見つからない")
            elif int(_m4.group(1)) != _fa460:
                _bad460.append(f"faq mirror の使う側: 申告 {_m4.group(1)} / 実測 {_fa460}")

        # (e) against.md が自分の規模について述べる数字。**2026-09-05 に 3 件 stale で見つかった** ——
        #   「43 entries」「14 から 33 へ」「33 adverse facts」と書いてあり実測は 51 だった。
        #   append-only の一覧を持つ文書は、**自分の規模を本文で述べた瞬間に古くなる**。
        _ag460 = ROOT / "LICENSES" / "ACD-1.0.against.md"
        if _ag460.exists():
            _agt = _ag460.read_text(encoding="utf-8")
            _rows460 = len(re.findall(r"^\| \d+ \|", _agt, re.M))
            for _m5 in re.finditer(r"grown from \d+ entries to \*\*(\d+)\*\*", _agt):
                if int(_m5.group(1)) != _rows460:
                    _bad460.append(f"against.md の規模: 申告 {_m5.group(1)} / 実測 {_rows460}")
            for _m6 in re.finditer(r"produced \*\*(\d+) adverse facts", _agt):
                if int(_m6.group(1)) != _rows460:
                    _bad460.append(f"against.md の総括: 申告 {_m6.group(1)} / 実測 {_rows460}")
            _er460 = ROOT / "LICENSES" / "ACD-1.0.errata.md"
            if _er460.exists():
                _ercnt = len(re.findall(r"^\| E\d+ \|", _er460.read_text(encoding="utf-8"), re.M))
                for _m7 in re.finditer(r"(\d+) errata", _agt):
                    if int(_m7.group(1)) != _ercnt:
                        _bad460.append(f"against.md の errata 数: 申告 {_m7.group(1)} / 実測 {_ercnt}")

        # (f) QUESTION-INDEX が述べる worked entry の総数。**索引は手で加算していたため 2 ずれていた**。
        _qi460 = ROOT / "LICENSES" / "QUESTION-INDEX.md"
        if _qi460.exists():
            # **番号行は `against.md` からのみ数える。** 2026-09-06 まではこの区別が無く、
            # `LICENSES/*.md` 全体の `| N |` を数えていた —— **たまたま番号付きの表が
            # against.md にしか無かったので正しく見えていただけ**である。実際、
            # REVISION-PROTOCOL に 7 行の番号付きゲート表を足した瞬間に総数が 152→159 へ跳ね、
            # 「worked entries（答えのある項目）」でないものが混ざった。**指標の正しさが
            # 偶然に依存していた**ので、意図（Q&A の項目 ∪ 不利な事実）に合わせて限定する。
            _tot460 = 0
            for _f in sorted((ROOT / "LICENSES").glob("*.md")):
                _ft = _f.read_text(encoding="utf-8")
                _tot460 += len(re.findall(r"^\*\*Q\.|^### (?:Q|A|B)\d+", _ft, re.M))
                if _f.name == "ACD-1.0.against.md":
                    _tot460 += len(re.findall(r"^\| \d+ \|", _ft, re.M))
            _m8 = re.search(r"There are \*\*(\d+)\*\* worked entries", _qi460.read_text(encoding="utf-8"))
            if not _m8:
                _bad460.append("QUESTION-INDEX.md: worked entry 総数の申告が見つからない")
            elif int(_m8.group(1)) != _tot460:
                _bad460.append(f"索引の総数: 申告 {_m8.group(1)} / 実測 {_tot460}")

        # (g) 入口ページと readiness が述べる規模。**2026-09-05 に 5 件 stale で見つかった** ——
        #   REVIEWERS.md は「118 worked entries」「All 14 adverse facts」「Five imprecisions」と
        #   書き、実体は 144 / 57 / 9 だった。**最後に書かれ最初に読まれるページ**が (a)〜(f) の
        #   どの面にも入っていなかった。しかも 3 つとも**過少**申告で、「全部開示する」と述べる
        #   ドシエが開示量を小さく言うのは、間違える向きとして最悪である（"All" は完全性の主張）。
        _erp460 = _L460 / "ACD-1.0.errata.md"
        _ern460 = len(re.findall(r"^\| E\d+ \|", _erp460.read_text(encoding="utf-8"), re.M)) if _erp460.exists() else -1
        _agp460 = _L460 / "ACD-1.0.against.md"
        _agn460 = len(re.findall(r"^\| \d+ \|", _agp460.read_text(encoding="utf-8"), re.M)) if _agp460.exists() else -1
        _rvp = _L460 / "REVIEWERS.md"
        if _rvp.exists():
            _rvt = _rvp.read_text(encoding="utf-8")
            for _pat, _want, _label in (
                (r"(\d+) worked entries, indexed by the question", _tot460, "REVIEWERS.md worked entries"),
                (r"All (\d+) adverse facts", _agn460, "REVIEWERS.md adverse facts"),
                (r"(\d+) known imprecisions", _ern460, "REVIEWERS.md errata"),
            ):
                _mg = re.search(_pat, _rvt)
                if not _mg:
                    _bad460.append(f"{_label}: 申告が見つからない (規模を述べる文を消すか、数を書くなら数えられる形で書く)")
                elif int(_mg.group(1)) != _want:
                    _bad460.append(f"{_label}: 申告 {_mg.group(1)} / 実測 {_want}")
        _rsp = _L460 / "READY-TO-SUBMIT.md"
        if _rsp.exists():
            _rst = _rsp.read_text(encoding="utf-8")
            _mg2 = re.search(r"\*\*(\d+) 件の不利な事実\*\*と \*\*(\d+) 件の errata\*\*", _rst)
            if not _mg2:
                _bad460.append("READY-TO-SUBMIT.md: 凍結後の発見件数の申告が見つからない")
            else:
                if int(_mg2.group(1)) != _agn460:
                    _bad460.append(f"READY-TO-SUBMIT.md の不利な事実: 申告 {_mg2.group(1)} / 実測 {_agn460}")
                if int(_mg2.group(2)) != _ern460:
                    _bad460.append(f"READY-TO-SUBMIT.md の errata: 申告 {_mg2.group(2)} / 実測 {_ern460}")

        # (h) **維持できない場所では、申告そのものを禁じる。** (a)〜(g) は「申告 vs 実測」を
        #   比較する形で、**捕まるたびに 1 面ずつ後付けで足してきた**。だから被覆は「これまでに
        #   drift を目撃した場所」であって「drift しうる場所」ではない。実測 (2026-09-06・外部から
        #   「まだ一致していない自己申告がある」とだけ指摘を受けて掃引): **4 件が柵の外に残って
        #   いた** —— `docs/files/LICENSES/` の mirror 3 件（不利な事実「14 件」/ errata「5 件」/
        #   「54 件の不利な事実」）と CLAUDE.md §7（「10 次元 / 候補 10 件」→ 実体 17 / 3）。
        #   mirror は「その file が何であるか」を説明する文書で、**規模を述べる読者価値が無い**の
        #   に対し drift は確実に起きる。よって比較ではなく**禁止**で守る（LICENSES/ 本体では
        #   規模の申告に読者価値があるので (a)〜(g) の比較で守り続ける）。
        _mir460 = ROOT / "docs" / "files" / "LICENSES"
        if _mir460.exists():
            _pat460h = re.compile(
                r"[0-9]+\s*件の(?:不利な事実|errata)"
                r"|不正確さ\s*[0-9]+\s*件"
                r"|[0-9]+\s*件のうち"
                r"|E1〜E[0-9]+"
                r"|All\s+[0-9]+\s+adverse"
                r"|[0-9]+\s+worked\s+entries"
                r"|[0-9]+\s+imprecisions")
            for _fm in sorted(_mir460.glob("*.md")):
                for _n, _ln in enumerate(_fm.read_text(encoding="utf-8").splitlines(), 1):
                    _hit = _pat460h.search(_ln)
                    if _hit:
                        _bad460.append(f"{_fm.name}:{_n}: mirror がドシエの規模を数字で述べている "
                                       f"({_hit.group(0)!r}) — 本体を指すだけにせよ")

        # (i) **提出パケット §4c が述べる「機械的に確かめたこと」の数値。** face (a) は同じ file の
        #   別の 1 文（worked entries / short answers）しか見ておらず、§4c の表は素通りしていた。
        #   実測 (2026-09-06): 「**50 entries, 1–50**」（実体 63）と「**29 / 29** clause pointers」
        #   （実体 33 —— Check 451a が同じ値を毎回数えている）。**§4c は「弁護士が読んでいない」に
        #   対する我々の答え**であり、その価値は「機械が確かめられる」ことにある。審査者が同じ
        #   コマンドを走らせて別の数字が出るなら、その節は逆の証拠になる。
        # 2026-09-09: §4c は ACD-1.0.submission-reference.md へ移った（送る文面と参考資料の
        # 分割）。**節番号は変えていない**ので申告の形は同じだが、読む先は変える必要がある ——
        # path を直さずに message だけ直すと、Check は存在しない節を探して黙る。
        _sbm460 = _L460 / "ACD-1.0.submission-reference.md"
        if _sbm460.exists() and _ag460.exists():
            _st = _sbm460.read_text(encoding="utf-8")
            _mi1 = re.search(r"\*\*(\d+) entries, 1–(\d+), no gaps", _st)
            if not _mi1:
                _bad460.append("submission-reference.md §4c: 不利な事実の件数申告が見つからない")
            elif int(_mi1.group(1)) != _rows460 or int(_mi1.group(2)) != _rows460:
                _bad460.append(f"submission-reference.md §4c の不利な事実: 申告 {_mi1.group(1)}–{_mi1.group(2)} / "
                               f"実測 {_rows460}")
            _md_i = _L460 / "ACD-1.0.machine.json"
            if _md_i.exists():
                try:
                    _dj = json.loads(_md_i.read_text(encoding="utf-8"))
                except ValueError:
                    _dj = None
                if _dj is not None:
                    _cnt = []

                    def _walk_i(o):
                        if isinstance(o, dict):
                            if isinstance(o.get("clause"), str):
                                _cnt.append(o["clause"])
                            for _v in o.values():
                                _walk_i(_v)
                        elif isinstance(o, list):
                            for _v in o:
                                _walk_i(_v)

                    _walk_i(_dj)
                    _mi2 = re.search(r"\*\*(\d+) / (\d+)\*\*", _st)
                    if not _mi2:
                        _bad460.append("submission-reference.md §4c: clause pointer の件数申告が見つからない")
                    elif int(_mi2.group(1)) != len(_cnt) or int(_mi2.group(2)) != len(_cnt):
                        _bad460.append(f"submission-reference.md §4c の clause pointer: 申告 "
                                       f"{_mi2.group(1)}/{_mi2.group(2)} / 実測 {len(_cnt)}/{len(_cnt)}")

            # 定義語の最小使用回数。**「Contribution at 4」と書いてあり実測は 3（しかも
            # Machine-Generated Material と同値）だった** —— 本文は凍結されているので drift では
            # なく**書いた時点で誤り**で、29/29 と同じ形。数え方は表の文言どおり
            # 「その語を定義する条を除いた本文での出現」に固定する。
            _txt_i = (_L460 / "ACD-1.0.txt")
            if _txt_i.exists():
                _lines_i = _txt_i.read_text(encoding="utf-8").split("\n")
                _defs_i = []
                for _i2, _l2 in enumerate(_lines_i):
                    _m2 = re.match(r'^\s+1\.\d+\s+"([^"]+)"', _l2)
                    if _m2:
                        _defs_i.append((_m2.group(1), _i2))
                _ends_i = [i for i, l in enumerate(_lines_i) if l.startswith("2. ")]
                if _defs_i and _ends_i:
                    _counts_i = []
                    for _k, (_term, _i) in enumerate(_defs_i):
                        _j = _defs_i[_k + 1][1] if _k + 1 < len(_defs_i) else _ends_i[0]
                        _rest = "\n".join(_lines_i[:_i] + _lines_i[_j:])
                        _counts_i.append((len(re.findall(r"\b" + re.escape(_term) + r"s?\b", _rest)), _term))
                    _min_i = min(c for c, _ in _counts_i)
                    _mt = re.search(r"the lowest is \*\*(\d+)\*\*", _st)
                    if not _mt:
                        _bad460.append("submission-reference.md §4c: 定義語の最小使用回数の申告が見つからない")
                    elif int(_mt.group(1)) != _min_i:
                        _bad460.append(f"submission-reference.md §4c の定義語 最小使用回数: 申告 {_mt.group(1)} / "
                                       f"実測 {_min_i}")
        # (j) **`comparison.md` §1.35 の「N のうち M」が、その下の 2 つの列挙と一致すること。**
        #   実測 (2026-09-06): 「Four of ... six ... the remaining two」と書きながら、上の表は 4 行、
        #   下の番号付き列挙は **3 件**で合計 7 だった。**宣言と列挙が同じ commit で入っている**ので
        #   drift ではなく書いた時点の誤りで、同日 3 件目の同型（29/29・Contribution at 4）。
        #   審査者が「なぜ Apache ではいけないのか」を確かめに来る節なので、そこの算数が合わないのは
        #   主張そのものより先に信用を削る。宣言ではなく**列挙から導く**。
        #   **初版は走査範囲を切らずに file 全体の `> | a | b |` を数え、他の引用表まで拾って 8 と
        #   報告した** —— 検出器を書いたら、それが正しい対象だけを掴んでいるかを先に確かめること。
        _cmp460 = _L460 / "ACD-1.0.comparison.md"
        if _cmp460.exists():
            _ct = _cmp460.read_text(encoding="utf-8")
            _m_j = re.search(r"\*\*Four of ACD-1\.0's (\w+) distinguishing features", _ct)
            _h1 = _ct.find("### Differences an amendment closes")
            _h2 = _ct.find("### Differences an amendment does not close")
            if not _m_j or _h1 < 0 or _h2 < 0:
                _bad460.append("comparison.md §1.35: 差別化の宣言または 2 つの見出しが見つからない")
            else:
                _sec_end = _ct.find("\n## ", _h2)
                _sec_end = len(_ct) if _sec_end < 0 else _sec_end
                _closes_blk = _ct[_h1:_h2]
                _open_blk = _ct[_h2:_sec_end]
                _tbl = len([l for l in _closes_blk.splitlines()
                            if re.match(r"^> \|", l) and not re.match(r"^> \|\s*(Difference|-)", l)])
                _open_j = len(re.findall(r"^> \*\*\d+\. ", _open_blk, re.M))
                _WORD = {"four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
                _decl = _WORD.get(_m_j.group(1).lower())
                if _decl is None:
                    _bad460.append(f"comparison.md §1.35: 総数の語 {_m_j.group(1)!r} を解釈できない")
                elif _decl != _tbl + _open_j:
                    _bad460.append(f"comparison.md §1.35 の差別化総数: 申告 {_m_j.group(1)} ({_decl}) / "
                                   f"実測 {_tbl + _open_j} (閉じる {_tbl} + 閉じない {_open_j})")

        # (k) **ドシエ内の `#N` 参照が、必ず不利な事実の行番号へ解決すること。** ドシエは自分の
        #   主張を `#N` と `E<n>` で相互参照しており、**その解決性がこの文書群の信用の土台**である
        #   （提出パケット §4c も「every cross-reference between the dossier documents resolves」と
        #   述べている）。実測 (2026-09-06): 65 件の `#N` と 10 件の `E<n>` はすべて解決したが
        #   **1 件だけ `#885`** があり、これは**リポジトリの PR 番号**だった —— 同じ記法で 2 つの
        #   採番体系が混ざると、審査者は存在しない不利な事実 #885 を探しに行く。番号の由来を
        #   説明するのではなく、**ドシエ内では `#N` を 1 つの意味に限定する**方が確実である。
        if _ag460.exists() and _erp460.exists():
            _nums_k = {int(_m) for _m in re.findall(r"^\| (\d+) \|", _agt, re.M)}
            _ers_k = set(re.findall(r"^\| (E\d+) \|", _erp460.read_text(encoding="utf-8"), re.M))
            for _fk in sorted(_L460.glob("*.md")):
                for _n, _ln in enumerate(_fk.read_text(encoding="utf-8").splitlines(), 1):
                    for _m in re.finditer(r"(?<![\w/])#(\d{1,4})\b", _ln):
                        if int(_m.group(1)) not in _nums_k:
                            _bad460.append(f"{_fk.name}:{_n}: `#{_m.group(1)}` が不利な事実へ解決しない "
                                           f"(PR 番号など別の採番を `#N` で書かない)")
                    for _m in re.finditer(r"(?<![\w])E(\d{1,2})\b", _ln):
                        if f"E{_m.group(1)}" not in _ers_k:
                            _bad460.append(f"{_fk.name}:{_n}: `E{_m.group(1)}` が errata へ解決しない")
        # (l) **`errata.md` 自身の冒頭が述べる件数が、その下の表の行数と一致すること。**
        #   実測 (2026-09-09): 冒頭は「**Seven** items are recorded: five imprecisions … **All five**
        #   are unrepaired」と述べ、表には **10 行**あった。**自分の既知欠陥を列挙するページが、
        #   いくつ知っているかを過少に申告していた** —— #58 と同じ「開示量を小さく言う」向きで、
        #   これは間違える向きとして最悪である。REVIEWERS / READY-TO-SUBMIT 側の申告は face (a) が
        #   既に見ていたが、**当のページ自身の申告だけが無検査だった** —— 「最後に書かれ最初に
        #   読まれるページ」が抜ける #58 の構造がそのまま繰り返されている。
        if _erp460.exists():
            _et_l = _erp460.read_text(encoding="utf-8")
            _rows_l = len(re.findall(r"^\| (E\d+) \|", _et_l, re.M))
            _WORDS_L = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                        "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
                        "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
                        "eighteen": 18, "nineteen": 19, "twenty": 20}
            _m_l = re.search(r"\*?\*?([A-Za-z]+|\d+)\*?\*? items are recorded", _et_l)
            if not _m_l:
                _bad460.append("errata.md: 冒頭の件数申告 (\"N items are recorded\") が見つからない")
            else:
                _raw_l = _m_l.group(1)
                _decl_l = int(_raw_l) if _raw_l.isdigit() else _WORDS_L.get(_raw_l.lower())
                if _decl_l is None:
                    _bad460.append(f"errata.md: 件数の語 {_raw_l!r} を解釈できない")
                elif _decl_l != _rows_l:
                    _bad460.append(f"errata.md の冒頭 件数申告: 申告 {_raw_l} ({_decl_l}) / 実測 {_rows_l}")
        # (m) **`ACD-OSI-BOTTLENECKS.md` の集計行が、その上の表から導出できること。**
        #   実測 (2026-09-10): 集計行は「OSI 判断依存 **3** (B4・B10・B11 の一部)」と述べ、
        #   OSI 列に ○ が付いている行は **6** だった (B4/B5/B7/B10/B11/B14)。
        #   **項目を足すたび列は増えるのに、集計行は最初に書いた数のまま動かない。**
        #   しかも**過少**申告で、#58 / face (l) と同じ「開示量を小さく言う」向きである。
        #   register は「今どこが詰まっているか」の単一 canonical なので、
        #   **その要約が実態より小さいと、読み手は残作業を少なく見積もる。**
        _bp460 = _L460 / "ACD-OSI-BOTTLENECKS.md"
        if _bp460.exists():
            _bt460 = _bp460.read_text(encoding="utf-8")
            _rows_m = re.findall(r"^\| \*\*B\d+\*\* \|(.*)$", _bt460, re.M)
            if not _rows_m:
                _bad460.append("ACD-OSI-BOTTLENECKS.md: 索引の表が見つからない")
            else:
                # 各行の末尾 3 列が 人間 / 弁護士 / OSI
                _need = {"人間": 0, "弁護士": 0, "OSI": 0}
                for _r in _rows_m:
                    _cols = [c.strip() for c in _r.split("|")]
                    _cols = [c for c in _cols if c != ""]
                    if len(_cols) >= 3:
                        _h, _l, _o = _cols[-3], _cols[-2], _cols[-1]
                        if "○" in _h: _need["人間"] += 1
                        if "○" in _l: _need["弁護士"] += 1
                        if "○" in _o: _need["OSI"] += 1
                for _label, _pat in (("主要", r"主要\s*(\d+)"),
                                     ("OSI", r"OSI の判断が要る\s*(\d+)"),
                                     ("弁護士", r"弁護士が要る\s*(\d+)"),
                                     ("人間", r"人間が要る\s*(\d+)")):
                    _mm = re.search(_pat, _bt460)
                    _want = len(_rows_m) if _label == "主要" else _need[_label]
                    if not _mm:
                        _bad460.append(f"ACD-OSI-BOTTLENECKS.md: 集計行に「{_label}」の申告が無い")
                    elif int(_mm.group(1)) != _want:
                        _bad460.append(
                            f"ACD-OSI-BOTTLENECKS.md の集計 {_label}: 申告 {_mm.group(1)} / 実測 {_want}")

        # (n) **`submission-reference.md` §4c の「機械的に確かめた」欄が、いま現物と一致すること。**
        #   §4c は審査者向けに「弁護士がいなくても機械で確かめられること」を数字で並べる表である。
        #   **その表自身が「Repeat the pass if the descriptor changes; nothing enforces it」と
        #   書いていた** —— つまり **drift しうると自認しながら、強制する層が無かった。**
        #   実際 2026-09-06 の再導出では **3 行が誤っていた**（表の中にそう書いてある）。
        #   ここで縛るのは**機械的に導出できる 5 つ**だけで、手読みの行（pointer が主張を支えるか等）は
        #   対象にしない ——**機械で確かめられないものを機械が確かめたことにしない。**
        _srp460 = _L460 / "ACD-1.0.submission-reference.md"
        _txp460 = _L460 / "ACD-1.0.txt"
        _mjp460 = _L460 / "ACD-1.0.machine.json"
        if _srp460.exists() and _txp460.exists() and _mjp460.exists():
            _lic460 = _txp460.read_text(encoding="utf-8")
            _srt460 = _srp460.read_text(encoding="utf-8")
            _terms460 = len(re.findall(r'^  \d+\.\d+\s+"[^"]+"\s+means', _lic460, re.M))
            _cl460n = len(re.findall(r"^  \d+\.\d+\s", _lic460, re.M))
            _sec460n = len(re.findall(r"^\d+\. [A-Z]", _lic460, re.M))
            _nonascii460 = sum(1 for _b in _txp460.read_bytes() if _b > 127)
            _ptr460 = []

            def _walk460(_o):
                if isinstance(_o, dict):
                    for _k, _v in _o.items():
                        if _k == "clause" and isinstance(_v, str):
                            _ptr460.append(_v)
                        else:
                            _walk460(_v)
                elif isinstance(_o, list):
                    for _v in _o:
                        _walk460(_v)

            try:
                _walk460(json.loads(_mjp460.read_text(encoding="utf-8")))
            except Exception as _e460n:
                _bad460.append(f"§4c: machine.json を parse できない: {_e460n}")
            for _pat460, _want460, _lab460 in (
                (r"\| (\d+) terms, all in §1\.1", _terms460, "§4c 定義語数"),
                (r"\| (\d+) sections, numbered 1", _sec460n, "§4c 節数"),
                (r"\| \*\*(\d+)\*\* non-ASCII bytes", _nonascii460, "§4c 非 ASCII バイト"),
                (r"\*\*(\d+) / \d+\*\*, machine-checked", len(_ptr460), "§4c clause pointer 数"),
                (r"\*\*(\d+) / \d+\*\*, no gaps either way", _cl460n, "§4c 条数"),
            ):
                _m460n = re.search(_pat460, _srt460)
                if not _m460n:
                    _bad460.append(f"{_lab460}: §4c の申告が見つからない (行を消して黙らせない)")
                elif int(_m460n.group(1)) != _want460:
                    _bad460.append(f"{_lab460}: 申告 {_m460n.group(1)} / 実測 {_want460}")

        # (o) **入口ページが register について述べる「最高 severity は N 件」が、register の表と一致すること。**
        #   2026-09-10 に **同じ日のうちに 4 度**「数えられるものを、数える前に書いた」——
        #   削減見積もり (42% 過大) / register の集計行 (3 対 6) / worked entries (215 対 219) /
        #   入口の "two of the three heaviest" (実際は 4 件)。**最後のものだけが無検査だった**
        #   ((m) は register 自身の集計行、(a)/(g) は件数の申告を見るが、**入口の散文は見ていない**)。
        _bp460o = _L460 / "ACD-OSI-BOTTLENECKS.md"
        _rv460o = _L460 / "REVIEWERS.md"
        if _bp460o.exists() and _rv460o.exists():
            _rows460o = re.findall(r"^\| \*\*B\d+\*\* \|[^|]*\|([^|]*)\|", _bp460o.read_text(encoding="utf-8"), re.M)
            _top460o = sum(1 for _c in _rows460o if "最高" in _c)
            _WORDS460o = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                          "seven": 7, "eight": 8, "nine": 9, "ten": 10}
            _m460o = re.search(r"\*\*([a-z]+|\d+) are marked highest severity", _rv460o.read_text(encoding="utf-8"))
            if not _m460o:
                _bad460.append("REVIEWERS.md: register の最高 severity 件数の申告が見つからない "
                               "(消して黙らせない。数を書くなら数えられる形で書く)")
            else:
                _raw460o = _m460o.group(1)
                _decl460o = int(_raw460o) if _raw460o.isdigit() else _WORDS460o.get(_raw460o)
                if _decl460o is None:
                    _bad460.append(f"REVIEWERS.md: 件数の語 {_raw460o!r} を解釈できない")
                elif _decl460o != _top460o:
                    _bad460.append(f"REVIEWERS.md の最高 severity: 申告 {_raw460o} ({_decl460o}) / 実測 {_top460o}")

        # (p) **§B.0 の見出しが述べる語数が、その file に書いてある instrument で数え直したものと一致すること。**
        #   §B.0 は **実際にメールへ貼られる文面**で、長さは B3（最重要 bottleneck の一つ）そのものである。
        #   file 自身が instrument を明記している ——**`**Subject:**` の行から署名までの空白区切りトークン**。
        #   **にもかかわらず、2026-09-11 に一段落を足したとき、申告 1048 は動かず何も落ちなかった**
        #   （実測 1098）。**数の申告のうち、いちばん外へ出る面が無検査だった。**
        _sb460p = _L460 / "ACD-1.0.submission.md"
        if _sb460p.exists():
            _t460p = _sb460p.read_text(encoding="utf-8")
            _h460p = re.search(r"### B\.0 [^\n]*?\(\*\*([\d,]+) words\*\*", _t460p)
            _s460p = [m.start() for m in re.finditer(r"(?m)^\*\*Subject:\*\*", _t460p)]
            _e460p = _t460p.find("### B.1")
            if not _h460p:
                _bad460.append("submission.md: §B.0 の見出しに語数の申告が無い "
                               "(消して黙らせない —— 長さは B3 そのものなので、数えられる形で書く)")
            elif _s460p and _e460p > _s460p[0]:
                _occ460p = [m.start() for m in re.finditer("Yuta Yokoi", _t460p[_s460p[0]:_e460p])]
                if _occ460p:
                    _end460p = _t460p.find("\n", _s460p[0] + _occ460p[-1])
                    _n460p = len(re.findall(r"\S+", _t460p[_s460p[0]:_end460p]))
                    _d460p = int(_h460p.group(1).replace(",", ""))
                    if _d460p != _n460p:
                        _bad460.append(f"submission.md §B.0 の語数: 申告 {_d460p} / 実測 {_n460p} "
                                       "(instrument は file 自身が書いている: Subject 行から署名まで)")

        check(
            not _bad460,
            f"Check 460: ドシエの自己申告件数が実測と一致 "
            f"(想定問答 {_entries460} + 短答 {_short460} / FAQ {_fa460}+{_fb460} / 本文 {_secs460} 節 {_cls460} 条)",
            (f"Check 460: 自己申告と実測がずれている: {_bad460}。**読み手は数字を根拠に"
             "「網羅されている」と判断する**ので、古い数字は網羅の主張を嘘にする。"
             "文書を足したら申告も直せ (実測 2026-08-27: FAQ に 9 問足した結果、索引と mirror が"
             "「使う側 12 問」のまま残っていた)"),
            blocking=True,
        )
