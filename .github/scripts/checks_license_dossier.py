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
  461c. **`LICENSES/*.md` がすべて `last-updated` を宣言していること** (BLOCKING):
       461b（stale 検査）の被覆は「その項目を持つファイル」で定義されており、
       frontmatter を持たないファイルは**黙って対象外**になる。実測 (2026-09-05):
       20 件中 3 件が frontmatter を持たず、それが提出物そのもの / 凍結と venue の
       単一ソース / 提出可否の判断という、**最も鮮度が load-bearing な 3 件**だった。
       461b は 17 件しか見ずに「stale なし」と緑を出す —— skip-on-missing が被覆の穴を
       無音にする形。被覆は時間で動かない静的な性質なので BLOCKING にできる。(BLOCKING)

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
                # **`LICENSE` が「rationale はここ」と指している先**であり、header block で
                # status を述べている。2026-09-06 まで走査対象に入っておらず、その header は
                # **「本文はまだ freeze していない」と書いたまま**だった —— 同じ文書の本文が
                # 「凍結中で一切変更していない」と述べているのに、である。採用を検討する人が
                # `LICENSE` から辿る唯一の設計文書なので、status を述べる面として縛る。
                "docs/architecture/acd-license-rationale.md",
                # **リポジトリの表紙**。バッジ直下の呼びかけが「OSI の `license-discuss` の
                # スレッドから来たなら」と現在の venue を名指ししている。venue が動けばこの 1 行は
                # stale になり、**新しい窓口から来た審査者が、来ていないスレッドの名前を読む**。
                # 最も読まれるページなので、状態を述べる面として縛る。
                "README.md",
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

    # ── 461c. LICENSES/*.md がすべて last-updated を宣言していること (BLOCKING) ──────
    # **461b の被覆は「その項目を持つファイル」で定義されていた。** `if not _m461: continue`
    # なので、frontmatter を持たないファイルは**黙って対象外**になる。実測 (2026-09-05):
    # 20 件中 3 件が frontmatter 自体を持っておらず、しかもそれが
    # `ACD-1.0.submission.md`（提出物そのもの）/ `FROZEN.md`（凍結と venue の単一ソース）/
    # `READY-TO-SUBMIT.md`（提出可否の判断）という、**最も鮮度が load-bearing な 3 件**だった。
    # 461b は 17 件しか見ていないのに「stale なし」と緑を出す —— #885 と同型の
    # 「skip-on-missing が被覆の穴を無音にする」形である。
    # 被覆そのものは時間で動かない静的な性質なので BLOCKING にできる（461b を BLOCKING に
    # 戻すのではない —— 動くのは日付の側であって、項目の有無ではない）。
    _nofm461 = []
    if _lic461.exists():
        for _f461c in sorted(_lic461.glob("*.md")):
            if not re.search(r"^last-updated:\s*\d{4}-\d{2}-\d{2}\s*$",
                             _f461c.read_text(encoding="utf-8"), re.M):
                _nofm461.append(_f461c.name)
    check(
        not _nofm461,
        f"Check 461c: LICENSES/*.md がすべて last-updated を宣言 (461b の被覆が完全)",
        (f"Check 461c: last-updated を持たないライセンス文書がある: {_nofm461}。"
         "**461b は項目を持つファイルしか見ない**ので、宣言が無いファイルは stale 検査から"
         "黙って外れる (実測 2026-09-05: 提出物・凍結マーカー・提出可否判断の 3 件が"
         "そうなっていた)。鮮度を見せない文書は「更新されていない」とも「されている」とも"
         "読めない"),
        blocking=True,
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
        _sbm460 = _L460 / "ACD-1.0.submission.md"
        if _sbm460.exists() and _ag460.exists():
            _st = _sbm460.read_text(encoding="utf-8")
            _mi1 = re.search(r"\*\*(\d+) entries, 1–(\d+), no gaps", _st)
            if not _mi1:
                _bad460.append("submission.md §4c: 不利な事実の件数申告が見つからない")
            elif int(_mi1.group(1)) != _rows460 or int(_mi1.group(2)) != _rows460:
                _bad460.append(f"submission.md §4c の不利な事実: 申告 {_mi1.group(1)}–{_mi1.group(2)} / "
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
                        _bad460.append("submission.md §4c: clause pointer の件数申告が見つからない")
                    elif int(_mi2.group(1)) != len(_cnt) or int(_mi2.group(2)) != len(_cnt):
                        _bad460.append(f"submission.md §4c の clause pointer: 申告 "
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
                        _bad460.append("submission.md §4c: 定義語の最小使用回数の申告が見つからない")
                    elif int(_mt.group(1)) != _min_i:
                        _bad460.append(f"submission.md §4c の定義語 最小使用回数: 申告 {_mt.group(1)} / "
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
