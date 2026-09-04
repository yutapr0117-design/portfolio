"""
checks_governance_sync.py — AIO / AI2AI / llms freshness & session-record governance sync checks
(extracted from check_repository_consistency.py — check.py split track・category "governance sync").

Contiguous cluster of Checks 21-27: llms alias Last-Updated sync (21), AI2AI Session Record ordering
(22), workflow/dependabot YAML syntax (23), llms-full freshness vs AI2AI (24), aio-monitoring-log
evidence_policy key (25), AI2AI-archive max session record == manifest role (26), llms-full no stale
C1-C6 in current-description (27). Each Check reads its own target files directly; no global-content
or cross-section var coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  21. llms alias files Last-Updated are in sync
  22. AI2AI.md Session Record headers are in ascending order
  23. .github/workflows/*.yml and dependabot.yml parse without YAML syntax errors
  24. llms-full.txt Last-Updated is within 7 days of AI2AI.md and >= v75-v78 floor
  25. aio-monitoring-log.json has an evidence_policy key (attempt_log_only honesty)
  26. AIO 層の Session Record archive 宣言 ⟺ 実体 (双方向): 26a 登録済み entry の role が
       宣言する範囲 ⟺ その file の実 Session Record の min/max、26b **disk 上の archive file が
       すべて manifest に登録されていること**。旧実装は `AI2AI-archive.md` 1 file 決め打ちで
       role を `#1-#N` 固定形で parse しており、その決め打ちが実 drift を生んだ —— archive は
       実際には 3 file (#1-#4 / #5-#14 / #15-#19) なのに登録は真ん中の 1 file だけで、
       **AI クローラから見ると証跡が #14 で途切れ、実体が #29 まである proof-of-work の
       3 分の 1 以上が discovery 層から欠落**していた (2026-08-23 に双方向へ一般化して是正)
  27. llms-full.txt has no stale C1–C6 in current-constraint context (should be C1–C7)
  441. ACD-1.0 ライセンス本文の構造整合と配線: 本 repo は独自ライセンス
       `LICENSES/ACD-1.0.txt` (Autonomous Commons Dedication 1.0) を適用しており、これを
       SPDX License List / OSI License Review へ提出する計画がある。SPDX の inclusion
       principles は「テキストが確定していること」と「収録後に steward が改変しないこと」を
       definitive requirement に置くため、**本文は壊れてはならない成果物**である。しかも
       ライセンス本文の欠陥は **CI のどの層にも出ない** —— behavior e2e もサイトも lint も
       ライセンスを読まないので、壊れても全部緑のまま提出まで到達しうる。
       実際 2026-08-23 の起草中に、条項を 1 つ挿入しただけで (a) §15.3 が重複し
       (b) 相互参照 (§12.5 → severability) が別条項を指し (c) §9.4 に "You must not say" と
       いう義務語が混入した —— **いずれも目視では見落とし、機械検査だけが捕捉した**。
       4 面を BLOCKING で強制する:
         441a: 条項番号が重複せず、各節内で 1 から連番であること。
         441b: 本文中の "Section N.M" 相互参照がすべて実在する条項へ解決すること。
         441c: §1 で定義した用語がすべて本文で使用されていること (未使用の定義は
               起草途中の残骸か、削除し忘れた条項の痕跡)。
         441d: "You must / You shall / You may not / provided that / on condition" 等の
               **利用者への義務語が本文に無い**こと。ACD-1.0 §10.1 は「利用者に一切の条件を
               課さない」と宣言しており、義務語の混入は**宣言と本文の自己矛盾**になる
               (このライセンスの中核主張がまさにそこなので、他のどの drift より重い)。
         441e: `LICENSE` が `SPDX-License-Identifier: ACD-1.0` を宣言し、全文ファイルの
               path を実際に参照していること (**存在 ≠ 配線** —— 全文があっても LICENSE が
               指していなければ、受領者はどの条項に従うのか判定できない)。
       441f = 本文が**純 ASCII** であること (あらゆる符号化のファイルへ埋め込まれる資産なので、非 ASCII 1 文字で latin-1 系の環境が mojibake になり byte 比較にも正規化の議論が要る)。441g = 本文に**プロジェクト固有の要素が無い**こと —— §16.3 が条文で「いかなるプロジェクトにも固有ではない」と主張し、SPDX の inclusion principles も同じことを要件にするので、主張と実態が乖離すれば提出はその一点で崩れる。

  447. **制約を「列挙する」機械可読面が正典の C1–C7 名を使うこと (BLOCKING)**:
       `.well-known/mcp.json` の `audit_architecture_constraints` prompt は、エージェントが
       展開して「このコードは制約に準拠しているか」を評価するためのテンプレート。そこに並ぶ
       制約名が正典とずれていると、**エージェントは存在しない制約を監査する**。
       実測 (2026-08-23): 「C1–C7: Vanilla JS / IIFE / ErrorBoundary / External Framework
       Independent / App Logic External Library Independent 等」と書かれており、後ろ 2 つは
       **正典に存在しない名前**、しかも **C5 (Human Writes Zero Code) / C6 (AIO Integrity) /
       C7 (KARTE CDN SRI Non-Application) —— このリポジトリを最も特徴づける 3 つが完全に欠落**
       していた。原因は履歴に残っている: 「mcp.json audit_architecture_constraints description
       updated C1–C6 → C1–C7」—— **範囲の表記だけ更新して列挙の中身を更新しなかった**。
       **射程は「列挙を名乗る面」に限る。** `llms-full.txt` の「C1–C7 に違反する構文を拒否せよ」
       のような**参照**や、index.html / README.md の `Architecture-Keywords:`
       (アーキテクチャの説明であって制約の列挙ではない) は正当なので対象外 ——
       広げると**正しい記述を RED にする**。正典名は AI2AI.md の C1–C7 表から**導出**する。
  436. 規範層 (docs/architecture/) に「オーナー裁可待ち」型の defer 理由が残らない: canon
       (AI2AI.md STEP 3 / CLAUDE.md §7) は 2026-08-18 に「**オーナー裁可が要る項目なんか一切
       無い**」「C5 は『人間がコードを書かない』の意であって設計判断を defer する根拠ではない」
       「**「裁可待ち」という作業カテゴリは存在しない**」と明記した。しかし canon を直しても、
       **その canon を根拠に書かれた下流の規範文書は自動では直らない**。実際 2026-08-20 の
       棚卸しで research-application-policy.md が「適用条件: オーナーが配色変更を裁可した時」
       を現行ガイダンスとして保持しており、しかもその項目は既に #1158 で解決済みだった ——
       読み手は**否定された規則を持ち帰る**。scope を `docs/architecture/` (規範層) に限るのは、
       `docs/incident-artifacts/` が**性質上の歴史記録**で、そこへ注記を強制すると履歴を
       濁す圧力になるため (#977 の「書き換えれば履歴を偽る」判断と同じ線引き)。
       否定・超越を明示する行 (SUPERSEDED / 否定された / 存在しない 等) は違反にしない。 (BLOCKING)

  450. Tracked text files carry no stray non-Japanese script (Cyrillic / Hangul / Arabic / Thai /
       Devanagari / Hebrew): an LLM writing Japanese can emit a homoglyph-adjacent character from
       another script mid-word, producing text that *looks* almost right but is corrupt — and no
       layer sees it (spell-check does not run, lint reads only JS, and prose is not compared to
       anything). Real example found 2026-08-23: in the Japanese word for "authoritative text",
       the leading three characters had been replaced by Cyrillic while the trailing katakana
       survived; it had lived on in `repository-maintainability-map.md` (normative layer,
       describing C6) and in a decision record. Greek is deliberately NOT flagged — it is legitimate in mathematical
       and scientific prose. The pattern is written with escape sequences so this file does not
       match itself, and for the same reason the description cannot quote an instance.
       Measured across 573 tracked text files: zero false positives. (BLOCKING)
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
       嘘にする**。3 面を検査する: (a) 提出パケットの worked entries / short answers ↔
       想定問答 3 分冊の `### ` 見出しと短答表の実測、(b) 索引の「使う側 N 問 / プロセス M 問」
       ↔ FAQ の `### AN.` / `### BN.` の実測、(c) 逐条リファレンスの「全 X 節 Y 条」↔
       ACD-1.0.txt から抽出した節数・条数。Check 413b（内訳の和 = 合計）と同じ
       「**書いた数は数えて確かめる**」族。(BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract
    warnings = ctx.warnings

    # ── 21. llms alias files Last-Updated sync ───────────────────────────────────
    llms_date_pattern = r"Last-Updated: ([0-9-]+)"
    llms_check_paths = ["llms.txt", ".well-known/llms.txt", "llms_well-known.txt", ".well-known/llms_well-known.txt"]
    llms_dates = {}
    for p in llms_check_paths:
        fpath = ROOT / p
        if fpath.exists():
            d = extract(llms_date_pattern, fpath.read_text(encoding="utf-8"))
            if d:
                llms_dates[p] = d
    if len(set(llms_dates.values())) > 1:
        check(
            False,
            "llms alias files Last-Updated are in sync",
            f"llms alias files Last-Updated mismatch: {llms_dates}",
        )
    else:
        d = list(llms_dates.values())[0] if llms_dates else "N/A"
        print(f"OK: llms alias files Last-Updated are in sync ({d})")

    # ── 22. AI2AI.md Session Record order: no #10 before #9 ──────────────────────
    ai2ai_text = read("AI2AI.md")
    import re as _re
    header_records = _re.findall(r'^## \[HANDOFF\] Session Record #(\d+)', ai2ai_text, _re.MULTILINE)
    record_nums = [int(n) for n in header_records]
    order_ok = len(record_nums) == 0 or all(record_nums[i] <= record_nums[i+1] for i in range(len(record_nums)-1))
    check(
        order_ok,
        f"AI2AI.md Session Record headers are in ascending order: {record_nums}",
        f"AI2AI.md Session Record headers out of order: {record_nums}",
    )

    # ── 23. YAML syntax: .github/workflows/*.yml and dependabot.yml ───────────────
    try:
        import yaml as _yaml
        yaml_targets = list((ROOT / ".github" / "workflows").glob("*.yml"))
        dep_yml = ROOT / ".github" / "dependabot.yml"
        if dep_yml.exists():
            yaml_targets.append(dep_yml)
        yaml_errors = []
        for ypath in sorted(yaml_targets):
            try:
                _yaml.safe_load(ypath.read_text(encoding="utf-8"))
            except Exception as ye:
                yaml_errors.append(f"{ypath.name}: {ye}")
        check(
            len(yaml_errors) == 0,
            f"All GitHub Actions YAML files parse successfully ({len(yaml_targets)} files)",
            "YAML parse errors: " + "; ".join(yaml_errors),
        )
    except ImportError:
        print("WARNING: PyYAML not available — YAML syntax check skipped")
        warnings.append("PyYAML not available — YAML syntax check skipped")

    # ── 24. P1-01: llms-full.txt Last-Updated freshness vs AI2AI.md ──────────────
    import re as _re2, datetime as _dt
    ai2ai_lu_m = _re2.search(r'^Last-Updated\s*:\s*([0-9-]+)', read("AI2AI.md"), _re2.MULTILINE)
    llms_full_lu_m = _re2.search(r'^## Last-Updated\n+(\d{4}-\d{2}-\d{2})', read("llms-full.txt"), _re2.MULTILINE | _re2.DOTALL)
    # also check header line
    llms_full_header_m = _re2.search(r'Last-Updated:\*\*\s*([0-9-]+)', read("llms-full.txt"))
    if ai2ai_lu_m and llms_full_lu_m:
        ai2ai_date = _dt.date.fromisoformat(ai2ai_lu_m.group(1))
        llms_full_date = _dt.date.fromisoformat(llms_full_lu_m.group(1))
        diff_days = abs((ai2ai_date - llms_full_date).days)
        check(
            diff_days <= 7,
            f"llms-full.txt Last-Updated ({llms_full_date}) is within 7 days of AI2AI.md Last-Updated ({ai2ai_date})",
            f"llms-full.txt Last-Updated ({llms_full_date}) differs from AI2AI.md Last-Updated ({ai2ai_date}) by {diff_days} days (>7)"
        )
        llms_full_text = read("llms-full.txt")
        has_maintenance = any(f"v{n}" in llms_full_text for n in ["75", "76", "77", "78"])
        if has_maintenance:
            check(
                llms_full_date >= _dt.date(2026, 5, 28),
                f"llms-full.txt Last-Updated ({llms_full_date}) >= 2026-05-28 (v75-v78 content detected)",
                f"llms-full.txt Last-Updated ({llms_full_date}) is stale: v75-v78 content detected but date < 2026-05-28"
            )
    else:
        warnings.append("P1-01: Could not parse Last-Updated from AI2AI.md or llms-full.txt")

    # ── 25. P1-04: aio-monitoring-log.json evidence_policy key ──────────────────
    aio_log_path = ROOT / "docs" / "evidence" / "aio-monitoring-log.json"
    if aio_log_path.exists():
        try:
            aio_log = json.loads(aio_log_path.read_text(encoding="utf-8"))
            check(
                "evidence_policy" in aio_log,
                "aio-monitoring-log.json: evidence_policy key present",
                "aio-monitoring-log.json: evidence_policy key missing — add to clarify attempt_log_only status"
            )
        except Exception as _e:
            warnings.append(f"P1-04: Could not parse aio-monitoring-log.json: {_e}")
    else:
        warnings.append("P1-04: docs/evidence/aio-monitoring-log.json not found")

    # ── 26. AIO 層の Session Record archive 宣言 ⟺ 実体 (双方向・BLOCKING) ────────
    # 旧実装は **`AI2AI-archive.md` 1 file 決め打ち**で、role を `#1-#(\d+)` という固定形で
    # parse し「最大番号だけ」を突き合わせていた。この決め打ちがまさに実 drift を生んだ:
    # archive は実際には 3 file に分かれている (#1-#4 / #5-#14 / #15-#19) のに、
    # **manifest に登録されていたのは真ん中の 1 file だけ**で、しかもその role は自分が
    # 持たない #1-#4 まで含むと主張していた。結果、AI クローラから見ると **proof-of-work の
    # 証跡が #14 で途切れ、実体が #29 まである証跡の 3 分の 1 以上が discovery 層から欠落**
    # していた —— AIO を最優先に据えたリポジトリで、中核資産が見えていなかった。
    # 「埋めるには C6 承認が要る」と記録して放置されていたが、承認は恒久的に与えられており
    # (AI2AI.md STEP 3)、これは待機項目ではなく **放置された実 drift** だった (2026-08-23 是正)。
    #
    # したがって決め打ちを捨て、**双方向**で機械強制する:
    #   26a: 登録済みの各 archive entry の role が宣言する範囲 ⟺ その file の実 Session Record
    #        の min/max (宣言 ⟹ 実体)
    #   26b: disk 上に存在する archive file がすべて manifest に登録されていること
    #        (実体 ⟹ 宣言。**今回の欠落を捕捉する方向**で、旧実装に無かったのはこちら)
    import re as _re26
    _sess_dir26 = ROOT / "docs" / "session-records"
    _manifest26 = ROOT / ".well-known" / "aio-manifest.json"
    if _sess_dir26.is_dir() and _manifest26.exists():
        try:
            _mj26 = json.loads(_manifest26.read_text(encoding="utf-8"))
            _reg26 = {}
            for _e26 in _mj26.get("supporting_evidence", []):
                _p26 = _e26.get("path", "")
                if "session-records/AI2AI-archive" in _p26:
                    _reg26[_p26] = _e26.get("role", "")

            def _range26(_path):
                _n = [int(_x) for _x in _re26.findall(
                    r"\[HANDOFF\] Session Record #(\d+)", _path.read_text(encoding="utf-8"))]
                return (min(_n), max(_n)) if _n else None

            # 26a — 宣言 ⟹ 実体
            _bad26 = []
            for _p26, _role26 in sorted(_reg26.items()):
                _f26 = ROOT / _p26
                if not _f26.exists():
                    _bad26.append(f"{_p26}: 登録されているが file が無い")
                    continue
                _act26 = _range26(_f26)
                _m26 = _re26.search(r"#(\d+)-#(\d+)", _role26)
                if not _act26:
                    _bad26.append(f"{_p26}: Session Record が 1 件も無い")
                elif not _m26:
                    _bad26.append(f"{_p26}: role が '#lo-#hi' 形式で範囲を宣言していない")
                elif (int(_m26.group(1)), int(_m26.group(2))) != _act26:
                    _bad26.append(
                        f"{_p26}: role は #{_m26.group(1)}-#{_m26.group(2)} と宣言するが実体は "
                        f"#{_act26[0]}-#{_act26[1]}")
            check(
                _reg26 and not _bad26,
                f"Check 26a: AIO manifest の archive role {len(_reg26)} 件が実体の Session Record 範囲と一致",
                (f"Check 26a: manifest の archive 宣言が実体とずれている: {_bad26}。"
                 "archive を rotate したら manifest の role も同一 commit で更新し、"
                 "digest を再生成せよ (C6 の A2 派生値例外)"),
                blocking=True,
            )

            # 26b — 実体 ⟹ 宣言 (今回の欠落を捕捉する方向)
            _on_disk26 = sorted(
                str(_f.relative_to(ROOT)) for _f in _sess_dir26.glob("AI2AI-archive*.md"))
            _unreg26 = [_p for _p in _on_disk26 if _p not in _reg26]
            check(
                not _unreg26,
                f"Check 26b: disk 上の archive {len(_on_disk26)} file がすべて AIO manifest に登録済",
                (f"Check 26b: AIO 層に登録されていない archive がある: {_unreg26}。"
                 "**登録漏れは AI クローラから見て proof-of-work の証跡が途切れることを意味する** —— "
                 "実際 2026-08-23 まで 3 file 中 2 file が未登録で、証跡が #14 で途切れて見えていた。"
                 "aio-manifest.json の supporting_evidence へ追加し digest を再生成せよ"),
                blocking=True,
            )
        except Exception as _e26:
            check(False, "", f"Check 26: archive 宣言の検証に失敗: {_e26}", blocking=True)
    else:
        check(False, "", "Check 26: docs/session-records/ または aio-manifest.json が無い", blocking=True)

    # ── 27. P1-03: llms-full.txt has no stale C1–C6 in current-description context
    llms_full_path = ROOT / "llms-full.txt"
    if llms_full_path.exists():
        lf_text = llms_full_path.read_text(encoding="utf-8")
        # Stale C1–C6 patterns that should now read C1–C7 (current constraint envelope)
        stale_patterns = [
            "violates C1\u2013C6",         # "Reject any syntax or pattern that violates C1–C6"
            "C1\u2013C6 constraint envelope",  # "remain within the C1–C6 constraint envelope"
        ]
        found_stale = [p for p in stale_patterns if p in lf_text]
        check(
            len(found_stale) == 0,
            "llms-full.txt: no stale C1\u2013C6 in current-constraint context",
            f"llms-full.txt: stale C1\u2013C6 found (should be C1\u2013C7): {found_stale}",
        )

    # ── 436. 規範層に「オーナー裁可待ち」型の defer 理由を残さない (BLOCKING) ────────
    # canon を直しても、その canon を根拠に書かれた**下流の規範文書は自動では直らない**。
    # 2026-08-20 の棚卸しで research-application-policy.md が「適用条件: オーナーが配色変更を
    # 裁可した時」を現行ガイダンスとして保持しており、しかもその項目は #1158 で解決済みだった。
    # 歴史記録 (docs/incident-artifacts/) は対象外 —— そこへ注記を強制すると履歴を濁す。
    # 検出語は**同じ意味の別綴り**まで列挙する。2026-08-23 の実測で、旧リストは "要承認" は見るのに
    # "承認必要" / "承認必須" / "承認なしに" という**このリポジトリで実際に使われていた日本語表現**を
    # 一つも見ていなかった (「静的 Check は自分が見ている綴りしか見ていない」class)。
    _DEFER436 = ("裁可待ち", "裁可した時", "裁可を待", "C5（人間）の領域", "C5 (人間) の領域",
                 "要承認", "要オーケストレーター承認",
                 "承認必要", "承認必須", "承認が必要", "承認なしに", "承認なしで",
                 "承認を待", "承認の有無", "承認下では",
                 "orchestrator approval", "explicit written approval", "approval required",
                 "requires approval", "without approval")
    _OK436 = ("SUPERSEDED", "否定された", "存在しない", "読み違い", "解決済み", "誤りだった",
              "承認ゲートではない", "是正", "standing approval", "撤回")

    # 走査対象 = 規範層。docs/architecture/ に加え、**最も規範的な canon と router そのもの**を含める。
    # 2026-08-23 に射程を広げた理由: 旧 scope は docs/architecture/ だけを見ており、canon (AI2AI.md) と
    # router (CLAUDE.md) は**射程外だった**。つまり「規範層から裁可待ち文言を排除する」Check が、
    # 規範の中心を一度も見ていなかった。実測で見落としが 1 件出た —— AI2AI.md の
    # **KERNEL Handoff prompt テンプレート**の中に C6 が
    # "immutable without explicit orchestrator approval" と書かれており、**他の AI エージェントへ
    # 制約として能動的に配信され続けていた**（受け取った側は否定された規則を持ち帰る）。
    _NORMATIVE436 = [ROOT / "AI2AI.md", ROOT / "CLAUDE.md", ROOT / ".claude" / "CLAUDE.md",
                     ROOT / "CONTRIBUTING.md", ROOT / "LICENSE", ROOT / "README.md",
                     ROOT / "Claude2Claude.md", ROOT / "CODEOWNERS"]
    # `.claude/` の agent 定義 / slash command / skill は**エージェントの挙動を実際に駆動する層**で、
    # 規範文書より直接的に効く。2026-08-23 の実測で `.claude/agents/aio-guardian.md` が
    # 「Orchestrator approval recorded? … If not, REFUSE.」と指示しており、AIO 編集を通すたびに
    # **canon が存在しないと明記した「裁可待ち」を再生産していた**。旧 scope はここを一度も見ていない。
    _AGENTIC436 = (sorted((ROOT / ".claude" / "agents").glob("*.md"))
                   + sorted((ROOT / ".claude" / "commands").glob("*.md"))
                   + sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md")))
    # `docs/files/` の mirror doc も規範として読まれる (「この file を編集するとき何を満たすか」を
    # 述べる面)。2026-08-23 に手作業で 9 枚を掃引したが、**綴りを 3 つ見落として 4 枚が残った** ——
    # per-instance の掃引では閉じない class だと実測で判ったので構造封じへ昇華する。
    # ただし**歴史記録の mirror は対象外**: incident-artifacts / session-records は過去を記述する
    # ものなので、超越注記を強制すると履歴を濁す (本 Check が既に採っている線引きの mirror 面)。
    _MIRROR_HIST436 = ("docs/files/docs/incident-artifacts/", "docs/files/docs/session-records/")
    _mirror436 = [
        _f for _f in sorted((ROOT / "docs" / "files").rglob("*.md"))
        if not str(_f.relative_to(ROOT)).startswith(_MIRROR_HIST436)
    ]
    _files436 = (sorted((ROOT / "docs" / "architecture").glob("*.md"))
                 + [_f for _f in _NORMATIVE436 if _f.exists()] + _AGENTIC436 + _mirror436)

    def _normative_lines436(_path):
        """歴史記録を除いた規範部分だけを (行番号, 行) で返す。

        歴史記録へ超越注記を強制すると履歴を濁すので対象外にする (#977 と同じ線引き)。
        除外するのは 2 種類だけで、いずれも**構造で判別できる**ものに限る:
          - AI2AI.md の `## Session Record Archive` 以降 (過去 Session の記録)
          - CLAUDE.md §7 の run 記録 bullet (`- **「終わりなき改善」…run (…)。**` 形式の 1 行)
        判別できない「たぶん歴史」を除外し始めると Check が骨抜きになるので広げないこと。
        """
        _out, _hist = [], False
        for _n, _line in enumerate(_path.read_text(encoding="utf-8").splitlines(), 1):
            if _path.name == "AI2AI.md" and _line.startswith("## Session Record Archive"):
                _hist = True
            if _hist:
                continue
            if _line.startswith("- **「終わりなき改善」"):
                continue
            _out.append((_n, _line))
        return _out

    # 照合は **case-insensitive**。2026-08-23 の非 vacuity 検証で、scope 拡張の動機そのもの
    # (`.claude/agents/aio-guardian.md` の "**Orchestrator approval recorded?** … REFUSE") が
    # **先頭大文字ゆえに素通り**した —— scope は届いていたのに照合が届いていなかった。
    _viol436 = []
    for _f in _files436:
        for _n, _line in _normative_lines436(_f):
            _lo = _line.lower()
            if any(_p.lower() in _lo for _p in _DEFER436) and not any(
                _o.lower() in _lo for _o in _OK436
            ):
                _viol436.append(f"{_f.relative_to(ROOT)}:{_n}")
    check(
        not _viol436,
        f"Check 436: 規範層 {len(_files436)} file (docs/architecture/ + canon/router/外部向け文書"
        f" + .claude/ の agent 定義/slash command/skill + docs/files/ mirror) に"
        f"「裁可待ち」型の defer 理由が無い",
        (f"Check 436: 規範層に canon が否定した defer 理由が残っている: {_viol436[:5]}。"
         "canon (AI2AI.md STEP 3 / CLAUDE.md §7) は「オーナー裁可が要る項目なんか一切無い」"
         "「C5 は『人間がコードを書かない』の意」「『裁可待ち』という作業カテゴリは存在しない」"
         "と明記している。規範文書に残ると**読み手が否定された規則を持ち帰る**。"
         "解決済みなら SUPERSEDED / 解決済み を、記録として残すなら『否定された』等を同じ行に"
         "書いて超越を明示せよ (歴史記録は対象外: docs/incident-artifacts/ 全体 とその mirror / docs/files/docs/session-records/ / AI2AI.md の Session Record Archive 以降 / CLAUDE.md §7 の run 記録 bullet)"),
        blocking=True,
    )

    # ── 441. ACD-1.0 ライセンス本文の構造整合と配線 (BLOCKING) ────────────────────
    # なぜ機械強制するか: ライセンス本文は **CI のどの層にも読まれない**。behavior e2e も
    # サイトも lint も consistency の他 Check も触らないので、壊れても全部緑のまま
    # SPDX / OSI 提出まで到達しうる。SPDX は「確定したテキスト」を収録要件に置くため、
    # 構造が壊れた本文の提出は却下に直結する。
    # 動機となった実例 (2026-08-23 起草中): 条項を 1 つ挿入しただけで §15.3 が重複し、
    # §12.5 の相互参照が別条項を指し、§9.4 に義務語が混入した。目視では 3 件とも
    # 見落としており、機械検査だけが捕捉した。
    import re as _re441
    _lic441 = ROOT / "LICENSES" / "ACD-1.0.txt"
    _proj441 = ROOT / "LICENSE"
    if _lic441.exists():
        _src441 = _lic441.read_text(encoding="utf-8")
        # 操作条項のみを対象にする (PREAMBLE は informative で条項番号を持たない)
        _nums441 = _re441.findall(r"^  (\d+\.\d+)\s", _src441, _re441.M)
        _tops441 = set(_re441.findall(r"^(\d+)\.\s+[A-Z]", _src441, _re441.M))

        # 441a — 番号の重複と連番
        _dup441 = sorted({_n for _n in _nums441 if _nums441.count(_n) > 1})
        _by441 = {}
        for _n in _nums441:
            _by441.setdefault(_n.split(".")[0], []).append(int(_n.split(".")[1]))
        _gap441 = {_k: _v for _k, _v in _by441.items() if _v != list(range(1, len(_v) + 1))}
        check(
            not _dup441 and not _gap441,
            f"Check 441a: ACD-1.0 の条項番号が重複なし・節内連番 ({len(_tops441)} 節 / {len(_nums441)} 項)",
            (f"Check 441a: ACD-1.0 の条項番号が壊れている — 重複: {_dup441} / 連番崩れ: {_gap441}。"
             "条項を挿入・削除したら同一 commit で以降を再採番し、相互参照 (441b) も追従させよ"),
            blocking=True,
        )

        # 441b — 相互参照の解決性
        # 集合なので数えるのは **参照先の種類**であって出現回数ではない。OK メッセージを
        # 「相互参照 N 件」と書いていたのは誤解を招く (2026-08-24 是正) —— 新しい参照を足しても
        # 参照先が既出なら数は動かないので、読み手が「参照は N 個しか無い」と誤読しうる。
        _occ441 = _re441.findall(r"Sections? (\d+(?:\.\d+)?)", _src441)
        _refs441 = set(_occ441)
        _refs441 |= set(_re441.findall(r"Sections \d+(?:\.\d+)? (?:to|and) (\d+(?:\.\d+)?)", _src441))
        _unres441 = sorted(_r for _r in _refs441 if _r not in set(_nums441) and _r not in _tops441)
        check(
            not _unres441,
            f"Check 441b: ACD-1.0 の相互参照 {len(_occ441)} 箇所 "
            f"(参照先 {len(_refs441)} 種) がすべて実在条項へ解決",
            (f"Check 441b: ACD-1.0 の相互参照が解決しない: {_unres441}。"
             "再採番したら本文中の 'Section N.M' 参照も同一 commit で追従させよ "
             "(実例: 2026-08-23 に §12.5 が severability を指していたが、条項挿入で番号がずれ別条項を指した)"),
            blocking=True,
        )

        # 441c — 定義語が本文で使われているか
        _def441 = set(_re441.findall(r'^  1\.\d+\s+"([^"]+)"\s+means', _src441, _re441.M))
        _body441 = _src441.split("2. SCOPE AND EFFECT", 1)[-1]
        _unused441 = sorted(_d for _d in _def441 if _d not in _body441)
        check(
            _def441 and not _unused441,
            f"Check 441c: ACD-1.0 の定義語 {len(_def441)} 件がすべて本文で使用されている",
            (f"Check 441c: ACD-1.0 に本文で使われていない定義がある: {_unused441}。"
             "未使用の定義は起草途中の残骸か、削除した条項の痕跡 — どちらも提出前に解消せよ"),
            blocking=True,
        )

        # 441d — 利用者への義務語が無いこと (§10.1 との自己矛盾防止)
        # 「このライセンスは条件を一切課さない」が中核主張なので、義務語の混入は
        # 他のどの drift よりも重い (主張そのものが偽になる)。
        _oblig441 = (r"You must\b", r"You shall\b", r"You may not\b", r"You are required\b",
                     r"provided that\b", r"on condition\b", r"You agree\b")
        _hits441 = []
        for _ln, _line in enumerate(_body441.splitlines(), 1):
            for _pt in _oblig441:
                if _re441.search(_pt, _line):
                    _hits441.append(f"{_pt}: {_line.strip()[:70]}")
        check(
            not _hits441,
            "Check 441d: ACD-1.0 に利用者への義務語が無い (§10.1 の無条件宣言と整合)",
            (f"Check 441d: ACD-1.0 に利用者への義務語が混入している: {_hits441[:3]}。"
             "§10.1 は『利用者に一切の条件・義務・制限を課さない』と宣言しており、"
             "義務語は**宣言と本文の自己矛盾**になる。起草者側の不作為義務として書き直すか "
             "(§5.2 の形)、Dedication の射程外である旨の記述へ改めよ (§11.3 の形)"),
            blocking=True,
        )
    else:
        check(False, "", "Check 441: LICENSES/ACD-1.0.txt が消失している", blocking=True)

    # 441e — LICENSE が全文へ配線されているか (存在 ≠ 配線)
    if _proj441.exists():
        _psrc441 = _proj441.read_text(encoding="utf-8")
        _wired441 = {
            "SPDX identifier": "SPDX-License-Identifier: ACD-1.0" in _psrc441,
            "full-text path": "LICENSES/ACD-1.0.txt" in _psrc441,
        }
        _miss441 = [_k for _k, _v in _wired441.items() if not _v]
        check(
            not _miss441,
            "Check 441e: LICENSE が ACD-1.0 の識別子と全文 path を配線している",
            (f"Check 441e: LICENSE の配線が欠けている: {_miss441}。"
             "全文ファイルが存在しても LICENSE がそれを指していなければ、受領者は"
             "どの条項に従うのか判定できない (#133/#134/#135 の silent-critical 配線 class の権利面)"),
            blocking=True,
        )

        # 441f — 本文が純 ASCII であること。
        # ライセンス本文は **あらゆる符号化のファイルへ埋め込まれる**ことを前提にした資産で、
        # 非 ASCII が 1 文字あるだけで latin-1 系の環境で mojibake になり、byte 比較にも
        # 正規化の議論が要る。2026-08-24 に em dash 3 箇所を ASCII へ置換して純 ASCII 化した
        # (英語としても non-restrictive clause なのでカンマの方が自然だった)。
        _nonascii441 = sorted({_c for _c in _src441 if ord(_c) > 127})
        check(
            not _nonascii441,
            "Check 441f: ACD-1.0 本文が純 ASCII (あらゆる符号化のファイルへ埋め込める)",
            (f"Check 441f: ACD-1.0 本文に非 ASCII 文字がある: {_nonascii441[:8]}。"
             "本文は**あらゆる符号化のファイルへ埋め込まれる**ことを前提にした資産で、"
             "非 ASCII が 1 文字あるだけで latin-1 系の環境で mojibake になり、byte 比較にも"
             "正規化の議論が要る。ASCII の等価表現へ置換せよ"),
            blocking=True,
        )

        # 441g — 本文に特定プロジェクト固有の要素が入り込まないこと。
        # §16.3 は「本 Dedication はいかなるプロジェクト・人・組織・法域・事業分野にも固有では
        # ない」と**条文で主張している**。SPDX の inclusion principles も「特定のプロジェクト・
        # 団体・企業に固有でないこと」を要件にする。主張と実態が乖離すれば、提出はその一点で
        # 崩れる。プロジェクト固有の記述は `LICENSE` 側 (適用の宣言) が持つ。
        _proj441 = []
        for _pat441, _label441 in [
            (r"portfolio", "プロジェクト名"),
            (r"Yokoi|Yuta|\u6a2a\u4e95", "個人名"),
            (r"https?://", "URL"),
            (r"github", "リポジトリ参照"),
            (r"Nihon Keiei|nkgr", "組織名"),
        ]:
            if re.search(_pat441, _src441, re.I):
                _proj441.append(_label441)
        check(
            not _proj441,
            "Check 441g: ACD-1.0 本文にプロジェクト固有の要素が無い (§16.3 の主張が真)",
            (f"Check 441g: ACD-1.0 本文にプロジェクト固有の要素がある: {_proj441}。"
             "**§16.3 は条文で「いかなるプロジェクトにも固有ではない」と主張しており**、"
             "SPDX の inclusion principles も同じことを要件にする。主張と実態が乖離すれば"
             "提出はその一点で崩れる。プロジェクト固有の記述は `LICENSE` 側 (適用の宣言) へ"),
            blocking=True,
        )
    else:
        check(False, "", "Check 441e: root LICENSE が消失している", blocking=True)

    # ── 447. 制約を「列挙する」機械可読面が正典の C1–C7 名を使う (BLOCKING) ─────────────
    # mcp.json の audit_architecture_constraints prompt はエージェントが展開して
    # 「このコードは制約に準拠しているか」を評価するテンプレート。名前が正典とずれていると
    # **エージェントは存在しない制約を監査する**。実測 (2026-08-23): 正典に無い名前を 2 つ並べ、
    # C5/C6/C7 が完全に欠落していた。原因は「範囲の表記だけ C1–C6 → C1–C7 へ更新して
    # 列挙の中身を更新しなかった」こと (履歴に残っている)。
    # **射程は「列挙を名乗る面」に限る** —— 参照 (llms-full.txt) や Architecture-Keywords
    # (index.html / README.md) は正当なので対象外。広げると正しい記述を RED にする。
    import json as _json447
    _canon447 = _re.findall(r"^\| (C[1-7]) \| \*\*([^*]+)\*\*",
                            (ROOT / "AI2AI.md").read_text(encoding="utf-8"), _re.M)
    _mcp447 = ROOT / ".well-known" / "mcp.json"
    if len(_canon447) != 7:
        check(False, "", f"Check 447: AI2AI.md から C1–C7 を導出できない (取得 {len(_canon447)} 件) — "
                         "C1–C7 表の記載形式を保つこと", blocking=True)
    elif not _mcp447.is_file():
        check(False, "", "Check 447: .well-known/mcp.json が無い", blocking=True)
    else:
        try:
            _mj447 = _json447.loads(_mcp447.read_text(encoding="utf-8"))
        except Exception as _e447:
            _mj447 = {}
        _descs447 = [_p.get("description", "") for _p in _mj447.get("prompts", [])
                     if isinstance(_p, dict) and "constraint" in (_p.get("name") or "")]
        if not _descs447:
            check(False, "", "Check 447: mcp.json に constraint 系 prompt が無い — "
                             "prompt を rename したなら本 Check の抽出条件も同一 commit で更新せよ",
                  blocking=True)
        else:
            _blob447 = "\n".join(_descs447)
            _missing447 = [f"{_k} {_v}" for _k, _v in _canon447 if _v not in _blob447]
            check(
                not _missing447,
                f"Check 447: mcp.json の制約列挙が正典の C1–C7 名を網羅 ({len(_canon447)} 件)",
                (f"Check 447: mcp.json の制約列挙に正典名が欠けている: {_missing447}。"
                 "**エージェントはこの prompt を展開して監査するので、名前がずれていると"
                 "存在しない制約を監査する**。実測 2026-08-23: 範囲の表記だけ C1–C6 → C1–C7 へ"
                 "更新され、列挙の中身は古いまま C5/C6/C7 が欠落していた。"
                 "正典は AI2AI.md の C1–C7 表 (本 Check が導出しているので、名前を変えれば追従が要る)"),
                blocking=True,
            )

    # ── 450. tracked text file に非日本語スクリプトの混入が無い (BLOCKING) ──────────
    # 日本語を書く LLM は、語の途中で別スクリプトの字形近似文字を出すことがある。結果は
    # 「ほぼ正しく見えるが壊れている」テキストで、**どの層も見ていない** (spell-check は
    # 走らず、lint は JS しか読まず、prose は何とも比較されない)。2026-08-23 の実測で
    # 「権威テキスト」の前半 3 字だけがキリル文字に置き換わった語が、規範層 (C6 を説明する行) と decision
    # record に残存していた。ギリシャ文字は数学/科学表記で正当なので**意図的に対象外**。
    # 正規表現は escape sequence で書く —— 文字を直接書くと本 file 自身がマッチする。
    _SCRIPTS450 = (
        "\u0400-\u04FF"    # Cyrillic
        "\u0590-\u05FF"    # Hebrew
        "\u0600-\u06FF"    # Arabic
        "\u0900-\u097F"    # Devanagari
        "\u0E00-\u0E7F"    # Thai
        "\u1100-\u11FF"    # Hangul Jamo
        "\u3130-\u318F"    # Hangul Compatibility Jamo
        "\uAC00-\uD7AF"    # Hangul Syllables
    )
    _re450 = re.compile("[" + _SCRIPTS450 + "]")
    import subprocess as _sp450
    try:
        _tracked450 = [
            _ln.strip()
            for _ln in _sp450.run(
                ["git", "ls-files"], cwd=str(ROOT), capture_output=True, text=True, check=True
            ).stdout.splitlines()
            if _ln.strip()
        ]
    except (OSError, _sp450.CalledProcessError):
        _tracked450 = []      # git 不在環境では Check 434 が視界不完全を BLOCKING で受ける
    _hits450 = []
    for _rel450 in _tracked450:
        _p450 = ROOT / _rel450
        try:
            _txt450 = _p450.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue          # binary は対象外 (decode できない時点で prose ではない)
        for _n450, _line450 in enumerate(_txt450.splitlines(), 1):
            _m450 = _re450.search(_line450)
            if _m450:
                _hits450.append(f"{_rel450}:{_n450} ({_m450.group()!r})")
    check(
        not _hits450,
        "Check 450: tracked text file に非日本語スクリプトの混入が無い",
        (f"Check 450: 日本語テキストに別スクリプトの文字が混入している: {_hits450[:5]}。"
         "字形が近いため目視では気付けず、spell-check も lint も prose を見ないので"
         "**どの層も検出しない**。該当箇所を正しい日本語文字へ置換せよ "
         "(ギリシャ文字は数学/科学表記で正当なので対象外)"),
        blocking=True,
    )

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
