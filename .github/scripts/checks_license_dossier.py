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
  463. **提出パケットの「送る文面」が、OSI が求める項目をすべて含むこと** (BLOCKING):
       `submission.md` §B.0 は**実際にメールへ貼られる ~600 語**である。OSI の
       review-process ページは提出時に 10 項目を求めるが、**2026-09-06 まで packet はそのうち
       3 件を欠いていた**（OSD 準拠の積極的言明 / ScanCode 識別子 / 提案 tag —— #77）。
       欠落の原因は「要件表を隣人の提出から再構成し、出典で読んでいなかった」ことで、
       **同じ形は静かに再発する** —— 文面は増分のたびに書き換えられ、項目は 1 つずつ落ちる。
       10 個の marker が §B.0 に存在することを機械強制する。**中身の質は検査しない**
       （それは散文の判断である）。守るのは「**項目が消えていないこと**」だけ。(BLOCKING)

  466. **審査者への案内が、表紙の先頭に在ること** (BLOCKING): 送った文面は GitHub リポジトリを
       指しているので `README.md` は審査者の入口である。その「どこから読めばよいか」の案内は
       2026-09-07 まで **11,024 文字・214 行下**にあり、手前は 30 秒要約・日本語の実績節・
       AI エージェント向け 4 ブロック・宣言だった —— **どれもその読み手のために書かれていない**
       (`against.md` #94)。この族 (#58 / #66 / #93 / #94) は 2 日で 4 例出ており、機序が毎回同じ
       である: **入口ページは最後に書かれて最初に読まれ、読者層を 1 つ足すたびに前の読者層の
       pointer が下へ押される**。位置は宣言ではなく副作用として動くので人の注意では止まらない。
       **marker の有無と byte offset だけ**を見る (文言の質もリンク先の中身も見ない)。

  465. **`rounds/` の在庫申告が、実際に置かれている file と一致すること** (BLOCKING):
       `LICENSES/rounds/` は「何と言われたか / 何と言ったか」の記録が drift しないためだけに
       在るディレクトリなのに、その README は 2026-09-06 まで **「いまの状態: 空である」** と
       書き続けていた —— 送信文を置いた当日から偽で、記録の入口が中身について偽を述べていた
       (`against.md` #89)。原因は状態を *宣言* して *導出* していなかったことなので、文言では
       なく**導出との照合**で守る。見出しの件数と在庫表の行数の**両方**を実 file 数と突き合わせ、
       中身があるのに「空である」と述べていないことも見る。file 名の列挙までは求めない
       (在庫表は日付と相手で引けることに意味があり、列挙は読者価値のない列を増やす)。

  464. **`errata.md` の全 `E<n>` が、次版の変更リストに現れること** (BLOCKING):
       1.0 は凍結中で、欠陥を見つけても直さず記録する運用である。**その記録の行き先が
       4 か所以上に散っていた**（errata / review-responses-meta の「1.1 で足すかもしれない候補」/
       review-responses-clauses の「1.1 候補」/ discussion-log の帰結値）。オーナーの運用方針は
       「**届いた議論をそのまま全部取り込んだ改善版を出す**」で、**議論中に貯めたものも同じ入力**
       である。議論が終わってから 4 か所を回って集める手順は必ず落とすので、
       `ACD-1.1-CHANGELIST.md` を単一の集約点とし、**errata の全件がそこに現れること**を強制する。
       内容の複製は要求しない（複製は drift する）—— **落ちていないこと**だけを見る。(BLOCKING)

  461c. **`LICENSES/*.md` がすべて `last-updated` を宣言していること** (BLOCKING):
       461b（stale 検査）の被覆は「その項目を持つファイル」で定義されており、
       frontmatter を持たないファイルは**黙って対象外**になる。実測 (2026-09-05):
       20 件中 3 件が frontmatter を持たず、それが提出物そのもの / 凍結と venue の
       単一ソース / 提出可否の判断という、**最も鮮度が load-bearing な 3 件**だった。
       461b は 17 件しか見ずに「stale なし」と緑を出す —— skip-on-missing が被覆の穴を
       無音にする形。被覆は時間で動かない静的な性質なので BLOCKING にできる。(BLOCKING)

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

    # ── 463. 提出パケットの「送る文面」が OSI の要求項目をすべて含むこと (BLOCKING) ──────
    # §B.0 は**実際に貼られる文面**で、§B.1 以降は貼らない参考資料である。#77 で 3 件の欠落を
    # 埋めたが、**文面は増分のたびに書き換えられる**ので、同じ欠落は静かに再発する。
    # marker の存在だけを見る —— 中身の質は散文の判断であって Check の仕事ではない。
    # **`_L460` に依存しない。** それは Check 460 の分岐内で定義される名前で、本 Check は
    # 460 より前に走る。他の Check の局所名を借りると、順序を変えた瞬間に NameError で
    # suite ごと止まる —— それは「Check が働いた」ではなく「Check が一度も走らなかった」
    # である（#885 と同型）。実際、初版はそれで落ちた。
    _sb463 = ROOT / "LICENSES" / "ACD-1.0.submission.md"
    if _sb463.exists():
        _t463 = _sb463.read_text(encoding="utf-8")
        _i463 = _t463.find("### B.0 The message as it should actually be sent")
        _j463 = _t463.find("### B.1 Reference material", _i463 + 1) if _i463 >= 0 else -1
        _bad463 = []
        if _i463 < 0 or _j463 < 0:
            _bad463.append("§B.0 / §B.1 の見出しが見つからない (送る文面と参考資料の境界が失われている)")
        else:
            _b0 = _t463[_i463:_j463]
            _req463 = [
                ("attachment", r"attached as plain text"),
                ("OSD affirmation", r"I affirm that ACD-1\.0 complies with the Open Source Definition"),
                # **要件は「OSD に準拠する」ではなく「OSD 3, 5, 6, 9 を満たすと specifically 明言する」**。
                # 原文: "Affirmatively state that the license complies with the Open Source Definition,
                # including specifically affirming it meets OSD 3, 5, 6 and 9."
                # 一般的な準拠宣言だけでは要件を満たさない。2026-09-07 に Carlo Piana 氏が別の提出に対し
                # 「required information が無いので**解決するまでコメントしない**」と述べており
                # (`against.md` #97)、欠落は議論の遅れではなく**議論の不成立**を招く。
                ("OSD 3/5/6/9 specific", r"OSD 3\*\*[\s\S]{0,400}?OSD 5 and OSD 6\*\*[\s\S]{0,400}?OSD 9\*\*"),
                ("projects using it", r"Approved or Used by Projects"),
                ("steward contact", r"Steward:.*@"),
                ("name and version", r"License Name:"),
                ("SPDX / ScanCode", r"SPDX / ScanCode Identifier"),
                ("proposed tags", r"Proposed Tags:"),
                ("gap statement", r"\*\*The gap\.\*\*"),
                ("nearest approved licences", r"\*\*Nearest approved licences\.\*\*"),
                ("legal review", r"\*\*Legal review: none\.\*\*"),
            ]
            _miss463 = [_n for _n, _r in _req463 if not re.search(_r, _b0, re.M)]
            if _miss463:
                _bad463.append(f"§B.0 に OSI 要求項目が欠けている: {_miss463}")
        check(
            not _bad463,
            "Check 463: 送る文面 (§B.0) が OSI の要求 11 項目をすべて含む",
            (f"Check 463: {_bad463}。要件の単一ソースは "
             "https://opensource.org/licenses/review-process。**§B.0 は実際にメールへ貼られる文面**で、"
             "§B.1 以降は貼らない参考資料である。#77 で 3 件の欠落を埋めたが、文面は増分のたび"
             "書き換えられるので同じ欠落は静かに再発する"),
            blocking=True,
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

    # ── 464. errata の全件が次版の変更リストに現れること (BLOCKING) ─────────────────────
    # 凍結中の運用は「直さず記録する」であり、**記録の行き先が散ると議論の最後に落ちる**。
    # 集約点を 1 つにしても、人手で同期するかぎり必ずずれるので機械強制する。
    # 内容は複製しない (複製は drift する) —— `E<n>` の**出現**だけを見る。
    _er464 = ROOT / "LICENSES" / "ACD-1.0.errata.md"
    _cl464 = ROOT / "LICENSES" / "ACD-1.1-CHANGELIST.md"
    if _er464.exists():
        check(
            _cl464.exists(),
            "Check 464: 次版の変更リスト (ACD-1.1-CHANGELIST.md) が存在する",
            ("Check 464: `LICENSES/ACD-1.1-CHANGELIST.md` が無い。凍結中に見つけた欠陥の"
             "**行き先が無いと、議論の最後に 4 か所を回って集めることになり落ちる**"),
            blocking=True,
        )
        if _cl464.exists():
            _ers = set(re.findall(r"^\| (E\d+) \|", _er464.read_text(encoding="utf-8"), re.M))
            _clt = _cl464.read_text(encoding="utf-8")
            _missing464 = sorted(_e for _e in _ers if not re.search(rf"(?<![A-Za-z0-9]){_e}(?![0-9])", _clt))
            check(
                not _missing464,
                f"Check 464: errata {len(_ers)} 件すべてが次版の変更リストに現れる",
                (f"Check 464: 次版の変更リストから errata が落ちている: {_missing464}。"
                 "**1.0 は凍結中で「直さず記録する」運用なので、記録が集約点に載らなければ"
                 "そのまま忘れられる**。errata に entry を足したら "
                 "`ACD-1.1-CHANGELIST.md` にも同じ `E<n>` を足せ (内容の複製は不要・落ちていないことだけを見る)"),
                blocking=True,
            )

    # ── 465. rounds/ の在庫申告が、実際に置かれている file と一致すること (BLOCKING) ──────
    # `LICENSES/rounds/` は「何と言われたか / 何と言ったか」の記録が drift しないためだけに
    # 存在するディレクトリである。にもかかわらず、その README は 2026-09-06 まで
    # **「いまの状態: 空である」** と書き続けていた —— 2026-08-26 の送信文が置かれた時点で
    # 偽になっており、記録の入口が中身について偽を述べていた (`against.md` #89)。
    #
    # 原因は「状態を *宣言* していて *導出* していなかった」ことなので、対処は文言の修正では
    # なく**導出との照合**に置く。README が名乗る件数と、実際の file 数を突き合わせる。
    #
    # なぜ 2 通りで測るか: 見出しの `N ファイル` だけを見ると「数字は直したが表は古い」形を
    # 素通りする (Check 460 が別の面で実際に踏んだ class)。表の行数も同時に照合する。
    #
    # 射程を README の在庫節に限る理由: file 名そのものの出現までは求めない。**在庫表は日付と
    # 相手で引けることに意味がある**ので、file 名の列挙を強制すると読者価値のない列が増える
    # (`docs/files/` mirror に規模の申告を禁じたのと同じ判断 — Check 460 face (h))。
    _rd465 = ROOT / "LICENSES" / "rounds"
    _rm465 = _rd465 / "README.md"
    if not _rm465.exists():
        check(False, "", "Check 465: LICENSES/rounds/README.md が無い — "
                         "REVISION-PROTOCOL.md が 3 箇所で指す先の入口が失われている", blocking=True)
    else:
        _files465 = sorted(p.name for p in _rd465.iterdir()
                           if p.is_file() and p.name != "README.md")
        _t465 = _rm465.read_text(encoding="utf-8")
        _bad465 = []
        _mh465 = re.search(r"##\s*いまの状態[^\n]*?(\d+)\s*ファイル", _t465)
        if not _mh465:
            _bad465.append("README に「## いまの状態（… N ファイル）」の在庫見出しが無い "
                           "(件数を導出と照合できない)")
        elif int(_mh465.group(1)) != len(_files465):
            _bad465.append(f"在庫見出しの申告 {_mh465.group(1)} / 実測 {len(_files465)}")
        # 在庫表の行数 — 見出し行と区切り行を除いた `| ... |` の数
        _sec465 = _t465[_mh465.start():] if _mh465 else ""
        _sec465 = _sec465.split("\n## ")[0]
        _rows465 = [ln for ln in _sec465.splitlines()
                    if ln.startswith("| ") and not ln.startswith("|---")
                    and not ln.startswith("| 日付 |")]
        if _mh465 and len(_rows465) != len(_files465):
            _bad465.append(f"在庫表の行数 {len(_rows465)} / 実測 file 数 {len(_files465)}")
        # 中身があるのに不在を主張していないか (#89 の literal)
        if _files465 and re.search(r"いまの状態[^\n]*\n+[^\n]*空である", _t465):
            _bad465.append("file が置かれているのに「空である」と述べている")
        check(
            not _bad465,
            f"Check 465: rounds/ の在庫申告が実測と一致 ({len(_files465)} file)",
            (f"Check 465: rounds/ の在庫申告が実測とずれている: {_bad465}。**このディレクトリは"
             "記録が drift しないためだけに在る**ので、その入口が中身について誤ると、"
             "審査者は証拠の量を誤って受け取る (2026-09-06: 送信文を置いた当日から README が"
             "「空である」と述べ続けていた = against.md #89)"),
            blocking=True,
        )

    # ── 466. 審査者への案内が、表紙の先頭に在ること (BLOCKING) ───────────────────────────
    # 送った文面は GitHub リポジトリを指しているので、`README.md` は審査者にとっての入口である。
    # その「どこから読めばよいか」の案内は 2026-09-07 まで **11,024 文字・214 行下**にあり、
    # 手前は 30 秒要約・日本語の実績節・AI エージェント向け 4 ブロック・宣言 —— **どれもその
    # 読み手のために書かれていない** (`against.md` #94)。
    #
    # なぜ Check にするか: この族 (#58 / #66 / #93 / #94) は 2 日で 4 例出ており、機序が毎回同じ
    # である —— **入口ページは最後に書かれて最初に読まれ、読者層を 1 つ足すたびに前の読者層の
    # pointer が下へ押される**。位置は宣言ではなく副作用として動くので、人の注意では止まらない。
    #
    # 何を見て、何を見ないか: **marker の有無と、その byte offset だけ**を見る。文言の質も、
    # リンク先の中身も見ない (それは Check 459 / 444 の担当)。閾値は「H1 と空行と callout」が
    # 収まる程度に緩く取り、**前に節を 1 つ足したら必ず超える**大きさにしてある。
    _rm466 = ROOT / "README.md"
    if not _rm466.exists():
        check(False, "", "Check 466: README.md が無い — 審査者の入口が失われている", blocking=True)
    else:
        _t466 = re.sub(r"<!--.*?-->", "", _rm466.read_text(encoding="utf-8"), flags=re.S)
        _MARK466 = "LICENSES/REVIEWERS.md"
        _LIMIT466 = 1500
        _i466 = _t466.find(_MARK466)
        check(
            _i466 != -1 and _i466 <= _LIMIT466,
            f"Check 466: 審査者への案内が README.md の先頭 {_LIMIT466} 字以内に在る "
            f"(実測 {_i466} 字)",
            (f"Check 466: README.md の審査者向け案内 (`{_MARK466}` への導線) が "
             + ("見つからない" if _i466 == -1 else f"{_i466} 字目にあり、先頭 {_LIMIT466} 字を超えている")
             + "。**位置は開示の一部である** —— 214 行下の pointer は、同じ文言でも上にあるものより"
             "開示していない (against.md #94)。読者層を足すときは、前の読者層の pointer を"
             "下へ押さないこと"),
            blocking=True,
        )
