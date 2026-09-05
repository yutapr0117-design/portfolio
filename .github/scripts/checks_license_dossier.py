"""
checks_license_dossier.py — ACD-1.0 ドシエ (LICENSES/) の自己整合を守る Check 群

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES

**なぜ独立した module なのか**: `checks_governance_sync.py` (統治文書の同期) から 2026-09-05 に
切り出した。同日にドシエ側の Check が育って元 module が 966 行に達し Check 52 の advisory (950)
が鳴ったため —— **圧縮で黙らせず、いま触っている塊を切り出す**（CLAUDE.md §7 に繰り返し
記録されている応答）。守っている invariant は 1 つの族である: **ドシエは自分自身について
事実を述べており、その事実は実測と一致する**（投稿先 / 到達性 / 入口の言語 / 自己申告の件数 /
日付の鮮度）。

  458. **投稿先 (venue) の記録が単一ソースと一致すること** (BLOCKING): ライセンスの
       「いまどこへ出しているか」は `LICENSES/FROZEN.md` の `VENUE-DATA` marker を単一ソースと
       し、状態を述べる各ファイルがそれと一致することを強制する。2026-08-26 の 1 日で venue の
       記録が **2 度 drift した** (「SPDX / OSI へ申請」→ `license-review` と誤記 →
       実際は `license-discuss`)。状態の記述が 10 ファイルに散らばっているため、1 箇所直しても
       残りが古いまま残る。**しかも venue の取り違えには実害がある** —— `license-discuss` は
       OSI の一般的な議論リストで**承認申請の窓口ではない**ので、「申請済み」と記録すると
       **まだ何も申請していない**ことに誰も気付けなくなる。
       458a = 宣言された venue が各 status ファイルに現れること。
       458b = **別の venue へ「投稿済み」と主張していないこと** (手順の記述や将来の窓口として
       名前が出るのは正当なので、`投稿済み` / `submitted` と同一行で結ばれている場合だけを
       違反とする)。(BLOCKING)
  459b. **索引の冒頭に英語の入口案内があること** (BLOCKING): `LICENSES/README.md` は GitHub が
       ディレクトリを開いたときに**自動描画する landing page** でありながら、実測 (2026-09-05) で
       **英語の文が 1 つも無かった**。英語の入口 `REVIEWERS.md` への言及は日本語の表のセルの中に
       あり、日本語を読めない審査者はそのセルを他と区別できない。#53 が同じ誤りを 1 階層下で
       直したのに、**審査者が実際に着地するページは誰も見ていなかった**。全訳はしない方針なので
       冒頭 20 行に英語ブロックが 1 つあることだけを縛る。(BLOCKING)

  459. **`LICENSES/*.md` が索引から到達できること** (BLOCKING): `LICENSES/README.md` を
       入口とし、同ディレクトリの `*.md` がすべてそこに現れることを強制する。
       **到達できない文書は無いのと同じ**である —— ライセンス周辺文書は「疑問がリポジトリを
       見れば潰せる」ことを目的に増えており、**入口に載らない文書はその目的を果たさない**。
       実測 (2026-08-27) では orphan は 0 件だったが、**入口が存在しないため将来 orphan が
       生まれても誰も気付けない**状態だった。Check 361 / 408 / 454 と同じ
       「実在 ⟹ 登録」族の、ライセンス文書面。(BLOCKING)
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
       (g) **入口ページ `REVIEWERS.md` と `READY-TO-SUBMIT.md` が述べる規模**
       —— 2026-09-05 に 5 件 stale で見つかった面で、しかも 3 つとも**過少**申告
       だった（「All 14 adverse facts」に対し実体 57）。**最後に書かれ最初に読まれるページ**が
       (a)〜(f) のどこにも入っていなかった。Check 413b（内訳の和 = 合計）と同じ
       「**書いた数は数えて確かめる**」族。(BLOCKING)
"""
import re
import json
import subprocess
import datetime as _dt461


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings

    # ── 458. 投稿先 (venue) の記録が単一ソースと一致すること (BLOCKING) ────────────────
    # FROZEN.md の `VENUE-DATA` marker を単一ソースにする。venue が変われば marker を変える
    # だけで、残りは CI が「ここも直せ」と指す。
    _frozen458 = ROOT / "LICENSES" / "FROZEN.md"
    if not _frozen458.exists():
        warnings.append("Check 458: LICENSES/FROZEN.md が無い (凍結解除済み?) — venue 整合を skip")
    else:
        _ftxt458 = _frozen458.read_text(encoding="utf-8")
        _m458 = re.search(r"<!--\s*VENUE-DATA:\s*(\S+?)\s*-->", _ftxt458)
        if not _m458:
            check(False, "", "Check 458: FROZEN.md に VENUE-DATA marker が無い "
                             "(投稿先の単一ソースが失われている)", blocking=True)
        else:
            _venue458 = _m458.group(1)
            _status458 = [
                "LICENSES/FROZEN.md",
                "LICENSES/READY-TO-SUBMIT.md",
                "LICENSES/ACD-1.0.submission.md",
                "LICENSES/ACD-1.0.review-responses.md",
                "CLAUDE.md",
            ]
            _missing458, _false458 = [], []
            _others458 = {"license-discuss", "license-review"} - {_venue458}
            for _rel458 in _status458:
                _p458 = ROOT / _rel458
                if not _p458.is_file():
                    _missing458.append(f"{_rel458} (file 不在)")
                    continue
                _t458 = _p458.read_text(encoding="utf-8", errors="replace")
                if _venue458 not in _t458:
                    _missing458.append(_rel458)
                # 別 venue の名前が出ること自体は正当 (手順の記述・将来の窓口・対比)。
                # 違反は「別 venue **のすぐ後ろに**『投稿済み』が続く」形だけに限る。
                #
                # [FIX] 初版は「同一行に別 venue と『投稿済み』があり、行内に否定語が無ければ違反」
                #   としていたが、**非 vacuity 検証で素通りした** —— 誤 venue を『投稿済み』と
                #   書いた行に、無関係な否定語 (別の節の「でもない」) が同居していたため抑止された。
                #   行という単位が粗すぎたのが原因なので、**近接** (venue の直後 40 字以内) で見る。
                #   間に否定語が挟まる `license-review へはまだ出していない` は違反にしない。
                _neg458 = re.compile(r"まだ|出していない|未実施|未投稿|ではない|でもない"
                                     r"|not sent|not yet|has not|Not sent|へは")
                _claim458 = re.compile(r"投稿済み|提出済|submitted")
                for _o458 in _others458:
                    for _mo458 in re.finditer(re.escape(_o458), _t458):
                        _win458 = _t458[_mo458.end():_mo458.end() + 40]
                        _mc458 = _claim458.search(_win458)
                        if not _mc458:
                            continue
                        if _neg458.search(_win458[:_mc458.start()]):
                            continue
                        _ctx458 = _t458[max(0, _mo458.start() - 20):_mo458.end() + 40]
                        _false458.append(f"{_rel458}: …{_ctx458.strip()[:70]}…")
            check(
                not _missing458,
                f"Check 458a: 宣言された投稿先 '{_venue458}' が status を述べる "
                f"{len(_status458)} ファイルすべてに現れる",
                (f"Check 458a: 投稿先 '{_venue458}' を述べていないファイルがある: {_missing458}。"
                 "状態の記述が散らばっていると 1 箇所直しても残りが古いまま残る "
                 "(2026-08-26 に 2 度 drift した)。FROZEN.md の VENUE-DATA を単一ソースとして揃えよ"),
                blocking=True,
            )
            check(
                not _false458,
                f"Check 458b: 宣言外の venue へ「投稿済み」と主張しているファイルが無い",
                (f"Check 458b: 宣言された投稿先は '{_venue458}' なのに、別の venue へ投稿済みだと"
                 f" 述べている箇所がある: {_false458[:3]}。**venue の取り違えには実害がある** —— "
                 "`license-discuss` は議論リストで承認申請の窓口ではないので、「申請済み」と"
                 "記録すると**まだ何も申請していない**ことに誰も気付けなくなる"),
                blocking=True,
            )

    # ── 459. LICENSES/*.md が索引 (README) から到達できること (BLOCKING) ───────────────
    # 到達できない文書は無いのと同じ。周辺文書は「疑問がリポジトリを見れば潰せる」ために
    # 増えており、入口に載らなければその目的を果たさない。
    import subprocess as _sp459
    _idx459 = ROOT / "LICENSES" / "README.md"
    if not _idx459.exists():
        check(False, "", "Check 459: LICENSES/README.md (索引) が無い — "
                         "周辺文書への入口が失われている", blocking=True)
    else:
        _txt459 = _idx459.read_text(encoding="utf-8")
        try:
            _ls459 = _sp459.run(["git", "ls-files", "LICENSES"], cwd=str(ROOT),
                                capture_output=True, text=True, check=True)
            _docs459 = [ln.strip() for ln in _ls459.stdout.splitlines()
                        if ln.strip().endswith(".md")]
            _miss459 = [d for d in _docs459
                        if d != "LICENSES/README.md" and d.split("/")[-1] not in _txt459]
            check(
                not _miss459,
                f"Check 459: LICENSES/*.md {len(_docs459) - 1} 件がすべて索引 (README.md) から到達できる",
                (f"Check 459: 索引に載っていないライセンス文書がある: {_miss459}。"
                 "**到達できない文書は無いのと同じ**で、「疑問がリポジトリを見れば潰せる」という"
                 "目的を果たさない。LICENSES/README.md の表に行を足せ"),
                blocking=True,
            )
        except (OSError, _sp459.CalledProcessError) as _e459:
            warnings.append(f"Check 459: LICENSES の走査に失敗 ({_e459}) — 索引到達性を skip")

    # ── 459b. 索引の冒頭に英語の入口案内があること (BLOCKING) ─────────────────────────
    # **459 は「索引に載っているか」しか見ない。** 実測 (2026-09-05): LICENSES/README.md は
    # GitHub がディレクトリを開いたときに自動描画する landing page でありながら、**英語の文が
    # 1 つも無かった** (日本語 885 字 / Latin 1,248 字はすべて識別子・ファイル名)。英語の入口
    # `REVIEWERS.md` への言及は 30 行目の**日本語の表のセル**の中にあり、日本語を読めない審査者は
    # そのセルを他のセルと区別できない —— ファイル名から当てるしかない。
    # against.md #53 が「入口が『読める文書を読めない言語だ』と案内していた」を 1 階層下で
    # 直したのに、**審査者が実際に着地するページは誰も見ていなかった**。全訳はしない方針なので、
    # 冒頭に英語の 1 ブロックだけを要求する。
    _hd459 = "\n".join(_txt459.splitlines()[:20]) if _idx459.exists() else ""
    check(
        ("REVIEWERS.md" in _hd459) and ("English" in _hd459),
        "Check 459b: 索引の冒頭 20 行に英語の入口案内がある",
        ("Check 459b: LICENSES/README.md の冒頭 20 行に、英語で REVIEWERS.md を指す案内が無い。"
         "**このファイルはディレクトリを開いた審査者が最初に見る自動描画ページ**であり、"
         "日本語しか無ければ英語の入口があること自体を伝えられない (#53 の 1 階層上・#60)"),
        blocking=True,
    )

    # ── 461b. LICENSES/*.md の last-updated が極端に古くないこと (ADVISORY) ──
    # **初版は BLOCKING で「git の最終更新日以上」を要求し、CI で落ちた。** 設計が誤って
    # いた —— 日付を直す commit 自身が git 日付を進めるので、**書いた瞬間に 1 日ずれる**。
    # さらに全ファイルへ footer を足すような一括変更は、内容を変えていないファイルの git
    # 日付まで進めるため、**触っていない文書が「古い」と報告される**。
    #
    # 直す方向は 2 つあった。(a) 許容差を設ける (b) BLOCKING をやめる。**両方採った** ——
    # frontmatter の日付が意味するのは「**内容を最後に見直した日**」であって「最後に
    # 1 バイト変わった日」ではない。footer の追加で見直し日が動くのは誤りである。
    # よって **14 日以上の乖離のみ ADVISORY** で報せる。実害（#55: 最大 10 日ずれ）は
    # 検出できるが、機械的な一括変更では鳴らない。
    _lu461 = []
    _lic461 = ROOT / "LICENSES"
    if _lic461.exists():
        for _f461 in sorted(_lic461.glob("*.md")):
            _m461 = re.search(r"^last-updated:\s*(\d{4}-\d{2}-\d{2})\s*$",
                              _f461.read_text(encoding="utf-8"), re.M)
            if not _m461:
                continue
            try:
                _git461 = subprocess.run(
                    ["git", "log", "-1", "--format=%ad", "--date=short", "--", str(_f461)],
                    capture_output=True, text=True, cwd=str(ROOT), timeout=20).stdout.strip()
            except Exception:
                continue
            if not _git461:
                continue
            try:
                _d1 = _dt461.date.fromisoformat(_m461.group(1))
                _d2 = _dt461.date.fromisoformat(_git461)
            except ValueError:
                continue
            if (_d2 - _d1).days >= 14:
                _lu461.append(f"{_f461.name}: 申告 {_m461.group(1)} / 実際の最終更新 {_git461} "
                              f"({(_d2 - _d1).days} 日)")
    check(
        not _lu461,
        f"Check 461b (ADVISORY): LICENSES/*.md の last-updated が 14 日以上 stale でない",
        f"Check 461b (ADVISORY): last-updated が 14 日以上古いファイルがある: {_lu461[:6]}。"
        f"**古い日付は「更新されていない文書」に見せる**。内容を見直したら日付も直せ "
        f"(1〜13 日の乖離は一括変更で普通に起きるので鳴らさない — 初版が BLOCKING で "
        f"これを見落として CI を落とした)",
        blocking=False,
    )

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
            _tot460 = 0
            for _f in sorted((ROOT / "LICENSES").glob("*.md")):
                _tot460 += len(re.findall(r"^\*\*Q\.|^### (?:Q|A|B)\d+|^\| \d+ \|",
                                          _f.read_text(encoding="utf-8"), re.M))
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
