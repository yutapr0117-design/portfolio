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
  26. aio-manifest.json archive role #1-#N matches AI2AI-archive.md max Session Record
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

    # ── 26. P1-02: AI2AI-archive.md max session record == aio-manifest.json role ─
    import re as _re
    archive_path = ROOT / "docs" / "session-records" / "AI2AI-archive.md"
    manifest_path = ROOT / ".well-known" / "aio-manifest.json"
    if archive_path.exists() and manifest_path.exists():
        try:
            archive_text = archive_path.read_text(encoding="utf-8")
            nums = [int(m) for m in _re.findall(r"\[HANDOFF\] Session Record #(\d+)", archive_text)]
            manifest_json = json.loads(manifest_path.read_text(encoding="utf-8"))
            archive_role = ""
            for entry in manifest_json.get("supporting_evidence", []):
                if "AI2AI-archive.md" in entry.get("path", ""):
                    archive_role = entry.get("role", "")
                    break
            m = _re.search(r"#1-#(\d+)", archive_role)
            if nums and m:
                expected_max = max(nums)
                manifest_max = int(m.group(1))
                check(
                    expected_max == manifest_max,
                    f"aio-manifest.json archive role #1-#{manifest_max} matches AI2AI-archive.md max Session Record #{expected_max}",
                    f"aio-manifest.json archive role says #1-#{manifest_max} but AI2AI-archive.md max is #{expected_max}",
                )
            else:
                warnings.append("P1-02: Could not parse session record numbers from archive or manifest role")
        except Exception as _e:
            warnings.append(f"P1-02: Archive session record check failed: {_e}")
    else:
        warnings.append("P1-02: AI2AI-archive.md or aio-manifest.json not found")

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
    _DEFER436 = ("裁可待ち", "裁可した時", "裁可を待", "C5（人間）の領域", "C5 (人間) の領域",
                 "要承認", "要オーケストレーター承認",
                 "orchestrator approval", "explicit written approval")
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
                     ROOT / "Claude2Claude.md"]
    _files436 = sorted((ROOT / "docs" / "architecture").glob("*.md")) + [_f for _f in _NORMATIVE436 if _f.exists()]

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

    _viol436 = []
    for _f in _files436:
        for _n, _line in _normative_lines436(_f):
            if any(_p in _line for _p in _DEFER436) and not any(_o in _line for _o in _OK436):
                _viol436.append(f"{_f.name}:{_n}")
    check(
        not _viol436,
        f"Check 436: 規範層 {len(_files436)} file (docs/architecture/ + canon/router/外部向け文書) に"
        f"「裁可待ち」型の defer 理由が無い",
        (f"Check 436: 規範層に canon が否定した defer 理由が残っている: {_viol436[:5]}。"
         "canon (AI2AI.md STEP 3 / CLAUDE.md §7) は「オーナー裁可が要る項目なんか一切無い」"
         "「C5 は『人間がコードを書かない』の意」「『裁可待ち』という作業カテゴリは存在しない」"
         "と明記している。規範文書に残ると**読み手が否定された規則を持ち帰る**。"
         "解決済みなら SUPERSEDED / 解決済み を、記録として残すなら『否定された』等を同じ行に"
         "書いて超越を明示せよ (歴史記録は対象外: docs/incident-artifacts/ 全体 / AI2AI.md の Session Record Archive 以降 / CLAUDE.md §7 の run 記録 bullet)"),
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
        _refs441 = set(_re441.findall(r"Sections? (\d+(?:\.\d+)?)", _src441))
        _refs441 |= set(_re441.findall(r"Sections \d+(?:\.\d+)? (?:to|and) (\d+(?:\.\d+)?)", _src441))
        _unres441 = sorted(_r for _r in _refs441 if _r not in set(_nums441) and _r not in _tops441)
        check(
            not _unres441,
            f"Check 441b: ACD-1.0 の相互参照 {len(_refs441)} 件がすべて実在条項へ解決",
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
    else:
        check(False, "", "Check 441e: root LICENSE が消失している", blocking=True)
