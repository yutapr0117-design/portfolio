"""checks_license_stated_counts.py — 自己申告の文が持つ 2 つ目の数 (498) と、入口の「最後に読んだ時刻」(499)

2026-11-08 に足した。Check 460 は自己申告の文の最初の数を実測と照合する面を多く持つが、同じ文の
2 つ目の数と、隣の文が繰り返す同じ数は読んでいなかった（Check の監査 findings #114〜#123）。
どれも「1 つ目を直して 2 つ目を残す」と緑のまま偽の数が残る形である。checks_license_self_reporting.py
は予算 (advisory 875) の縁にあるので、別の module に置く。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  498. **自己申告の文の 2 つ目の数が、1 つ目と同じ実測に一致すること** (BLOCKING・2026-11-08):
       (a) errata 冒頭の "all N are unrepaired" / (b) comparison §1.35 の "Four of" と
       "the remaining N" / "those N carry" / (c) FAQ mirror の「B. プロセス（N 問）」/
       (d) submission-reference §4c の "**X / Y**, no gaps either way" の両辺 / (e) register の
       集計行の「解消済み N」「構造的拒否候補 N」(分類の列の `12`) / (f) 逐条リファレンスが繰り返す「N 条すべてを収録」「抽出した N 条」/
       (g) submission.md の "across N files" と、そこで名指す分冊 / (h) AS-OF の「未読スレッドの残り」の
       「候補 N 本のうち M 本を読んだ。K 本は読んでいない」が N = M + K であること /
       (j) 「1.0 から何が変わったか」の英文 (CHANGELIST の切り替えの日の節・切り替えた後は REVIEWERS) が述べる
       errata の件数・閉じた件数と版ごとの内訳・残る E-ID・節ごとの件数・語数と条の数が、
       prepare_version_freeze.py の errata_closures() / size() と一致すること (2026-11-11・portfolio-00 の依頼) /
       (i) AS-OF の「答えていない問い」の行の「**N 件**」が、状態の欄の「**Q1**」「**Q2**」… の数と
       一致し、番号が 1 から N まで欠けず、各件が「；」で終わり、届いた日・`rounds/<file>`（実在）・§（私信の stub を
       指す件は § を書かず「—」）と、
       「未回答」か「オーナーが回答」を持つこと (2026-11-11・portfolio-00 の依頼。0 件のうちに置く)。
       文が読めないことも RED にする（言い換えると黙る形を残さない）。
  499. **入口の「最後に読んだ時刻」が、OSI-EVENTS が記録する最新の取得と合うこと** (BLOCKING・2026-11-09・
       portfolio-aa の提案): REVIEWERS.md の Status は "No responses in the archive when last read, <時刻> UTC"
       と述べ、取得のたびに書き換えないと、古い時刻のまま「返信は無い」と言い続ける。記録の無い取得
       (最新の取得より後の時刻) と、最新の取得より 48 時間以上古い時刻を RED、48 時間以内の遅れを ADVISORY にする
       (取得の当日に入口を直す余裕を残す)。
"""
import datetime
import re

from checks_license_self_reporting import _NUM_WORDS


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    L = ROOT / "LICENSES"
    bad = []

    def num(w):
        w = w.lower().strip("*")
        return int(w) if w.isdigit() else _NUM_WORDS.get(w)

    def text(p):
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ── 498. 自己申告の文の 2 つ目の数が、1 つ目と同じ実測に一致すること (BLOCKING) ─────────────
    # (a) errata 冒頭: 460 (l) は "N items are recorded" の N だけを見ていた。動機の失敗は 2 つ目の数だった
    er = text(L / "ACD-1.0.errata.md")
    rows_e = len(re.findall(r"^\| E\d+ \|", er, re.M))
    m = re.search(r"items are recorded, and all \**([A-Za-z]+(?:-[A-Za-z]+)?|\d+)\** are unrepaired", er)
    if not m:
        bad.append("(a) errata.md: 冒頭の \"all N are unrepaired\" が読めない")
    elif num(m.group(1)) != rows_e:
        bad.append(f"(a) errata.md の \"all {m.group(1)} are unrepaired\" / 表 {rows_e} 行")

    # (b) comparison §1.35: 460 (j) は総数の語だけを見て、"Four" と "the remaining N" は読んでいなかった
    ct = text(L / "ACD-1.0.comparison.md")
    h1, h2 = ct.find("### Differences an amendment closes"), ct.find("### Differences an amendment does not close")
    if h1 < 0 or h2 < 0:
        bad.append("(b) comparison.md §1.35: 2 つの見出しが見つからない")
    else:
        end = ct.find("\n## ", h2)
        end = len(ct) if end < 0 else end
        tbl = len([ln for ln in ct[h1:h2].splitlines()
                   if re.match(r"^> \|", ln) and not re.match(r"^> \|\s*(Difference|-)", ln)])
        opn = len(re.findall(r"^> \*\*\d+\. ", ct[h2:end], re.M))
        for pat, want, what in ((r"\*\*(\w+) of ACD-1\.0's \w+ distinguishing features", tbl, "閉じる差の数"),
                                (r"narrows to the remaining (\w+)", opn, "残る差の数"),
                                (r"those (\w+) carry the argument", opn, "残る差の数")):
            mm = re.search(pat, ct)
            if not mm:
                bad.append(f"(b) comparison.md §1.35: {what}の文 ({pat}) が読めない")
            elif num(mm.group(1)) != want:
                bad.append(f"(b) comparison.md §1.35 の{what}: 申告 {mm.group(1)} / 実測 {want}")

    # (c) FAQ mirror: 460 (d) は「A. 使う側」だけを見て、次の行の「B. プロセス」は読んでいなかった
    fb = len(re.findall(r"^### B\d+\.", text(L / "ACD-1.0.faq.md"), re.M))
    m = re.search(r"\*\*B\. プロセス\*\*（(\d+) 問）", text(ROOT / "docs" / "files" / "LICENSES" / "ACD-1.0.faq.md.md"))
    if not m:
        bad.append("(c) faq mirror: 「B. プロセス（N 問）」が読めない")
    elif int(m.group(1)) != fb:
        bad.append(f"(c) faq mirror のプロセス: 申告 {m.group(1)} / 実測 {fb}")

    # (d) §4c の条の行: 460 (n) は分子だけを掴み、分母は \d+ で読み捨てていた
    cls = len(re.findall(r"^  \d+\.\d+\s", text(L / "ACD-1.0.txt"), re.M))
    m = re.search(r"\*\*(\d+) / (\d+)\*\*, no gaps either way", text(L / "ACD-1.0.submission-reference.md"))
    if not m:
        bad.append("(d) submission-reference.md §4c: \"**X / Y**, no gaps either way\" が読めない")
    elif (int(m.group(1)), int(m.group(2))) != (cls, cls):
        bad.append(f"(d) submission-reference.md §4c の条の行: 申告 {m.group(1)} / {m.group(2)} / 本文の条 {cls}")

    # (e) register の集計行: 460 (m) は 4 つの数を見て、「解消済み」は読んでいなかった（有利な向きの偽が通る）
    bt = text(L / "ACD-OSI-BOTTLENECKS.md")
    sts = [re.sub(r"\*", "", c.split("|")[4]).strip() for c in re.findall(r"^\| \*\*B\d+\*\* \|.*$", bt, re.M)
           if len(c.split("|")) > 5]
    m = re.search(r"解消済み\s*(\d+)", bt)
    if not m:
        bad.append("(e) ACD-OSI-BOTTLENECKS.md: 集計行の「解消済み N」が読めない")
    elif int(m.group(1)) != sum(1 for s in sts if s.startswith("解消済み")):
        bad.append(f"(e) register の集計行の解消済み: 申告 {m.group(1)} / status が「解消済み」で始まる行 "
                   f"{sum(1 for s in sts if s.startswith('解消済み'))}")

    # 構造的拒否候補 = 分類の列に `12`（凡例「構造的に両立不能の可能性」）を持つ行 (portfolio-00 の定義・2026-11-08)
    cls_e = [c.split("|")[4] for c in re.findall(r"^\| \*\*B\d+\*\* \|.*$", bt, re.M) if len(c.split("|")) > 5]
    n12 = sum(1 for c in cls_e if re.search(r"(?<![\d.])12(?![\d.])", c))
    m = re.search(r"構造的拒否候補\s*(\d+)", bt)
    if not m:
        bad.append("(e) ACD-OSI-BOTTLENECKS.md: 集計行の「構造的拒否候補 N」が読めない")
    elif int(m.group(1)) != n12:
        bad.append(f"(e) register の集計行の構造的拒否候補: 申告 {m.group(1)} / 分類に 12 を持つ行 {n12}")

    # (f) 逐条リファレンス: 460 (c) は題の「全 X 節 Y 条」だけを見て、次の行の繰り返しは読んでいなかった
    cr = text(L / "ACD-1.0.clause-reference.md")
    reps = re.findall(r"(\d+) 条すべてを収録|抽出した (\d+) 条", cr)
    if not reps:
        bad.append("(f) clause-reference.md: 「N 条すべてを収録」「抽出した N 条」が読めない")
    for a, b in reps:
        if int(a or b) != cls:
            bad.append(f"(f) clause-reference.md の繰り返し: 申告 {a or b} 条 / 本文の条 {cls}")

    # (g) submission.md: 460 (a) は glob で 4 file を数えるのに、文は "three files" と書き 2 つの分冊しか名指さなかった
    sb = text(L / "ACD-1.0.submission.md")
    rr = sorted(L.glob("ACD-1.0.review-responses*.md"))
    m = re.search(r"short answers, across (\w+) files\) are in\s+(.{0,240})", sb, re.S)
    if not m:
        bad.append("(g) submission.md: \"across N files\" が読めない")
    else:
        if num(m.group(1)) != len(rr):
            bad.append(f"(g) submission.md の分冊の数: 申告 {m.group(1)} / 実測 {len(rr)}")
        unnamed = [p.name for p in rr if p.name != "ACD-1.0.review-responses.md"
                   and f"`-{p.stem.rsplit('-', 1)[-1]}`" not in m.group(2)]
        if unnamed:
            bad.append(f"(g) submission.md が名指さない分冊: {unnamed}")

    # (h) AS-OF の未読スレッドの行: 候補・読了・残りを手で数えており、2026-11-08 に 362 / 409 を 368 / 403 へ
    #   直した (portfolio-00)。候補の数は道具 (census_decision_statements.py threads) がアーカイブを読んで出すので
    #   CI では再現できない。CI で守れるのは同じ文の中の算術だけである
    m = re.search(r"候補 (\d+) 本のうち (\d+) 本を読んだ。(\d+) 本は読んでいない", text(L / "AS-OF.md"))
    if not m:
        bad.append("(h) AS-OF.md: 「候補 N 本のうち M 本を読んだ。K 本は読んでいない」が読めない")
    elif int(m.group(1)) != int(m.group(2)) + int(m.group(3)):
        bad.append(f"(h) AS-OF.md の未読スレッド: 候補 {m.group(1)} ≠ 読んだ {m.group(2)} + 読んでいない {m.group(3)}")

    # (i) AS-OF の「答えていない問い」の行: 件数「**N 件**」を手で書き、問いが届くたびに状態の欄へ
    #   「**Qn** 届いた日・発言者・`rounds/<file>`・§N・未回答｜YYYY-MM-DD にオーナーが回答」を「；」で
    #   足す (portfolio-00 が 2026-11-11 に決めた形)。件を足して件数を直し忘れると、答えていない問いを
    #   「0 件」と言い続ける。0 件のうちに置けば、最初の 1 件が届いた日に食い違いが出ない
    m = re.search(r"^\|\s*\*\*答えていない問い\*\*.*$", text(L / "AS-OF.md"), re.M)
    cells = re.split(r"(?<!\\)\|", m.group(0))[1:] if m else []
    n_i = re.fullmatch(r"\s*\*\*(\d+) 件\*\*\s*", cells[2]) if len(cells) > 3 else None
    if not n_i:
        bad.append("(i) AS-OF.md: 「答えていない問い」の行か、その件数の欄「**N 件**」が読めない")
    else:
        qs = list(re.finditer(r"\*\*Q(\d+)\*\*", cells[3]))
        nums = [int(q.group(1)) for q in qs]
        if len(qs) != int(n_i.group(1)) or nums != list(range(1, len(qs) + 1)):
            bad.append(f"(i) AS-OF.md の答えていない問い: 件数 {n_i.group(1)} / 状態の欄の番号 {nums}"
                       " (1 から欠けずに並び、数が件数と一致すること)")
        for k, q in enumerate(qs):
            item = cells[3][q.end():qs[k + 1].start() if k + 1 < len(qs) else len(cells[3])]
            # 件は「；」で終わる。終わりを切らないと、最後の件が行の説明文 (§ も「未回答」も日付も持つ) まで
            #   伸び、件に足りないものがあっても説明文が満たしていた
            if "；" not in item:
                bad.append(f"(i) AS-OF.md の Q{q.group(1)}: 件の終わりの「；」が無い (件のあとに行の説明文が続く)")
                continue
            item = item.split("；", 1)[0]
            rf = re.search(r"`rounds/([^`]+)`", item)
            rp = L / "rounds" / rf.group(1) if rf else None
            # 私信の stub (本文を撤去した off-list の file) を指す件は、問われた条を「—」で書いてよい
            #   (portfolio-00・2026-11-11): 条を書くと私信の中身の一部を公開の文書に出しうる。stub の目印は
            #   Check 473c の側 (checks_license_provenance.py) と同じ本文の一文で読む
            stub = bool(rp and rp.is_file() and "THE TEXT HAS BEEN WITHDRAWN" in rp.read_text(encoding="utf-8", errors="replace"))
            miss = [w for w, ok in (("届いた日", re.search(r"\d{4}-\d{2}-\d{2}", item)),
                                    ("rounds の file", rp and rp.is_file()),
                                    ("§ (stub なら —)", "§" in item or (stub and "—" in item)),
                                    ("状態", re.search(r"未回答|オーナーが回答", item))) if not ok]
            if miss:
                bad.append(f"(i) AS-OF.md の Q{q.group(1)}: {' / '.join(miss)} が無い (rounds の file は実在すること)")
            # stub を指す件は § を書かない (portfolio-00・2026-11-11): 私信で問われた条は私信の中身の一部で、
            #   B14 の規律は出さない側に倒す。同じ問いが後でリストに出たら、その通を逐語で置いた別の件にする
            if stub and "§" in item:
                bad.append(f"(i) AS-OF.md の Q{q.group(1)}: 私信の stub を指す件が問われた条 (§) を書いている —— 「—」にする")

    # (j) 「1.0 から何が変わったか」の英文の数 (portfolio-00 / aa・2026-11-11)。使い捨ての計数で 1.3 を 5・1.4 を 38 と
    #   書いた (閉鎖の印でなく版の語の最初の一致を数えた)。数え方は prepare_version_freeze.py の errata_closures() と
    #   size() に 1 か所だけ置き、--report とここが同じ関数を使う
    #   語数と条の数は草案を直すたびに動くので、CHANGELIST の下書き (「当日に数え直す」) では ADVISORY、
    #   REVIEWERS に移した後は BLOCKING。errata の数は errata を閉じる commit で一緒に直すので両方で BLOCKING
    from prepare_version_freeze import errata_closures, size
    total_j, closed_j, unmarked_j, sections_j = errata_closures()
    hits_j, soft_j = 0, []
    for p in sorted(L.glob("ACD-*-CHANGELIST.md")) + [L / "REVIEWERS.md"]:
        quote = " ".join(" ".join(x[1:].strip() for x in text(p).split("\n") if x.startswith(">")).split())
        for m in re.finditer(r"Of the (\d+) defects recorded against 1\.0 .{0,80}?, (\d+) are closed: (\d+) in 1\.1 to "
                             r"(\d+\.\d+) \(([\d, and]+)\) and (\d+) for the first time in (\d+\.\d+)\.(.{0,900})", quote):
            hits_j += 1
            tgt, rest = m.group(7), m.group(8)
            olds = sorted((v for v in closed_j if v != tgt), key=lambda x: tuple(map(int, x.split("."))))
            want = [total_j, sum(map(len, closed_j.values())), sum(len(closed_j[v]) for v in olds),
                    [len(closed_j[v]) for v in olds], len(closed_j.get(tgt, []))]
            got = [int(m.group(1)), int(m.group(2)), int(m.group(3)),
                   [int(x) for x in re.findall(r"\d+", m.group(5))], int(m.group(6))]
            if got != want:
                bad.append(f"(j) {p.name}: errata の数 {got} / errata の閉鎖の印から {want} (件数・閉じた・{tgt} より前・版ごと・{tgt})")
            if [e for e in unmarked_j if not re.search(rf"\b{e}\b", rest[:200])]:
                bad.append(f"(j) {p.name}: 閉鎖の印の無い {unmarked_j} を英文が名指していない")
            for sec, n in re.findall(r"§(\d+) \([^()]*?, (\d+)\)", rest):
                if sections_j.get(sec) != int(n):
                    bad.append(f"(j) {p.name}: §{sec} の件数 {n} / errata の表から {sections_j.get(sec)}")
            mw = re.search(r"([\d,]+) words from the title to \*?END OF TERMS\*? against 1\.0's ([\d,]+), in (\d+) clauses against (\d+)", rest)
            tp = L / f"ACD-{tgt}.txt" if (L / f"ACD-{tgt}.txt").exists() else L / f"ACD-{tgt}-DRAFT.txt"
            if not mw or not tp.exists():
                bad.append(f"(j) {p.name}: 語数と条の数の文が読めない、または {tp.name} が無い")
            else:
                (w1, c1), (w0, c0) = size(text(tp)), size(text(L / "ACD-1.0.txt"))
                if [int(mw.group(1).replace(",", "")), int(mw.group(2).replace(",", "")), int(mw.group(3)), int(mw.group(4))] != [w1, w0, c1, c0]:
                    (bad if p.name == "REVIEWERS.md" else soft_j).append(
                        f"(j) {p.name}: 語数と条の数 {mw.groups()} / 実測 {tp.name} {w1} 語 {c1} 条・1.0 {w0} 語 {c0} 条")
    if not hits_j:
        bad.append("(j) 「1.0 から何が変わったか」の英文 (Of the N defects recorded against 1.0 …) が CHANGELIST にも REVIEWERS にも読めない")
    check(not soft_j, "Check 498 (ADVISORY): 「1.0 から何が変わったか」の下書きの語数と条の数が草案と一致",
          f"Check 498 (ADVISORY): {soft_j}。下書きの語数は切り替えの日に prepare_version_freeze.py --report の値へ直す", blocking=False)

    check(
        not bad,
        "Check 498: 自己申告の文の 2 つ目の数と繰り返しが実測と一致 (errata / comparison / faq mirror / §4c / register / 逐条 / 分冊 / 未読スレッドの和 / 答えていない問いの件数 / 1.0 からの変化の数)",
        (f"Check 498: 自己申告の文の 2 つ目の数が実測と合わない: {bad}。1 つ目の数 (Check 460) だけを直すと、"
         "同じ文の 2 つ目と隣の繰り返しが偽のまま残る"),
        blocking=True,
    )

    # ── 499. 入口の「最後に読んだ時刻」が、記録する最新の取得と合うこと (BLOCKING) ──────────────────
    # 取得の行は `| YYYY-MM-DD（[YYYY-MM-DD ]HH:MM[〜HH:MM] UTC・… 取得 …` の形 (時刻の無い行は数えない)
    _fetch499 = []
    for _f499 in sorted(L.glob("OSI-EVENTS-*.md")):
        for _m499 in re.finditer(r"(?m)^\| (\d{4}-\d{2}-\d{2})（(?:(\d{4}-\d{2}-\d{2}) )?(\d{2}:\d{2})(?:〜\d{2}:\d{2})? UTC・[^|]*取得", text(_f499)):
            _fetch499.append(datetime.datetime.fromisoformat(f"{_m499.group(2) or _m499.group(1)}T{_m499.group(3)}"))
    _rv499 = re.search(r"when last read, (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC", text(L / "REVIEWERS.md"))
    if not _fetch499 or not _rv499:
        check(False, "", f"Check 499: 取得の記録 ({len(_fetch499)} 行) か入口の \"when last read, … UTC\" が読めない", blocking=True)
    else:
        _last499 = max(_fetch499)
        _said499 = datetime.datetime.fromisoformat(f"{_rv499.group(1)}T{_rv499.group(2)}")
        _lag499 = (_last499 - _said499).total_seconds() / 3600
        check(
            _said499 <= _last499 and _lag499 <= 48,
            f"Check 499: 入口の最後に読んだ時刻 {_said499:%Y-%m-%d %H:%M} UTC が、最新の取得 {_last499:%Y-%m-%d %H:%M} UTC から 48 時間以内",
            (f"Check 499: 入口の最後に読んだ時刻 {_said499:%Y-%m-%d %H:%M} UTC が、最新の取得の記録 {_last499:%Y-%m-%d %H:%M} UTC と合わない ("
             + ("記録の無い取得を名乗っている" if _said499 > _last499 else f"{_lag499:.0f} 時間古い") + ")。取得したら OSI-EVENTS と入口を同じ日に直す"),
            blocking=True,
        )
        check(
            _said499 == _last499 or _said499 > _last499 or _lag499 > 48,
            "Check 499 (ADVISORY): 入口の最後に読んだ時刻が最新の取得と一致",
            f"Check 499 (ADVISORY): 入口の最後に読んだ時刻が最新の取得より {_lag499:.0f} 時間古い (48 時間を越えると RED)",
            blocking=False,
        )
