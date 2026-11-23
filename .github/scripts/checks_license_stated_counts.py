"""checks_license_stated_counts.py — 自己申告の文が持つ 2 つ目の数 (498) と、入口の「最後に読んだ時刻」(499)、§1.N の重複 (500)、読んだ節の反映の欄 (501)、草案の投稿の状態 (502)

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
       (g) submission.md の "across N files" と、そこで名指す分冊 / (h) AS-OF の「未読スレッドの残り」の (h2 は候補の一覧の census の定義の指紋)
       「候補 N 本のうち M 本を読んだ。K 本は読んでいない」が N = M + K であり、N が THREAD-CANDIDATES.txt の
       会話の数、M が READ-THREADS.txt のうちそこに在る会話の数であること (後者 2 つは 2026-11-15・9b) /
       (j) 「1.0 から何が変わったか」の英文 (CHANGELIST の切り替えの日の節・切り替えた後は REVIEWERS) が述べる
       errata の件数・閉じた件数と版ごとの内訳・残る E-ID・節ごとの件数・語数と条の数が、
       prepare_version_freeze.py の errata_closures() / size() と一致すること (2026-11-11・portfolio-00 の依頼) /
       (k) 草案の CHANGELIST の「## 語数の内訳」が述べる前版の語数と差・束の表の合計・名指した N 束の和・1.0 の語数と差が、
       表と size() の実測に一致すること (2026-11-15・9b。50 が「増えた語の大半」の 263 ≠ 148 + 118 に気付いた) /
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
  500. **ドシエの §1.N 見出し (N >= 70) が全体で 1 か所にしか無いこと** (BLOCKING・2026-11-15・30 の問い):
       §1.70 以降は通し番号として文書の名を添えずに引かれる。未読の 285 本を 5 人で読むため節番号を帯で分けた日に、
       帯を越えた重複を止める (本体は _lib_dossier.section_heading_duplicates)。
  501. **§1.242 以降の各節が「**反映**: …」の行を 1 つ持ち、行き先を語彙で述べること** (BLOCKING・2026-11-15・2f の提案 (A)):
       オーナーの前提「未読があり、未反映のまま本申請は出せない」。against #N と errata E# は実在を照らす。「未定」は ADVISORY
       (本体は _lib_dossier.reflect_field_misses)。**501b** (2026-11-15・30 の案 (B)・50 の依頼): §1.242 より前の節は
       REFLECTION-BACKFILL.md の表の 1 行で満たしてよい。行は見出しと 1 対 1・語彙・番号の実在・grep と言うなら行き先が
       §1.N を引くこと (BLOCKING)。反映の無い古い節が在れば RED (2026-11-16 に 0 になり、ADVISORY から BLOCKING へ上げた)。
  502. **草案の冒頭の状態の箇条と、投稿した版の記録の節が食い違わないこと** (BLOCKING・2026-11-16・1c の依頼):
       "* It has not been posted to any list." と "Changes since the version posted on <日付>" が同時に在れば RED。投稿の後の
       箇条 "It was posted to license-discuss on <日付>" と節の日付が違えば RED、一方だけが在っても RED (草案が自分の状態に
       ついて嘘をつく形・安全網の規律 (1))。
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
    #   直した (portfolio-00)。同じ文の中の算術に加えて、N と M を一覧の file から導出して照合する
    #   (2026-11-15・9b。2f が気付き 50 が提案): 道具は 11-11 から候補を THREAD-CANDIDATES.txt に固定し
    #   (一度候補になった会話は外さない)、読了を READ-THREADS.txt だけから数え、どちらの行も日付を会話の
    #   始まりにそろえている。だから N = 候補の一覧の会話の数、M = 読了の行のうち候補の一覧に在る会話の数
    #   (件名の key と日付の組・key は道具と同じ title_key) で、アーカイブ無しに再現できる (11-15 に 800 / 486 で一致)。
    #   読了の行を足して AS-OF を直し忘れる形と、日付が会話の始まりでない行 (道具は会話に当て直すが、ここでは
    #   外れる) の両方を RED にする。読了の 519 行のうち 33 行は候補の外の会話で、M に入らないのが正しい
    m = re.search(r"候補 (\d+) 本のうち (\d+) 本を読んだ。(\d+) 本は読んでいない", text(L / "AS-OF.md"))
    if not m:
        bad.append("(h) AS-OF.md: 「候補 N 本のうち M 本を読んだ。K 本は読んでいない」が読めない")
    else:
        if int(m.group(1)) != int(m.group(2)) + int(m.group(3)):
            bad.append(f"(h) AS-OF.md の未読スレッド: 候補 {m.group(1)} ≠ 読んだ {m.group(2)} + 読んでいない {m.group(3)}")
        from census_decision_statements import READ_THREADS_SPLIT, _list_rows, candidate_rows, read_rows, split_file_for, split_files
        cand = {(k, d) for k, d, _t in candidate_rows(L)}
        read = {(k, d) for k, d, _t in read_rows(L)}
        # 読了の一覧は会話の始まりの年で 2 つの file に分けた (2026-11-16)。行が違う file に在ると、record_read の重複の
        #   照合 (書く file の中だけを見る) をすり抜けて同じ会話が 2 行になりうる
        _misfiled = [f"{_f.name}: {_d}" for _stem in ("READ-THREADS", "THREAD-CANDIDATES") for _f in split_files(_stem, L)
                     for _k, _d, _t in _list_rows(_f) if split_file_for(_stem, _d, L) != _f]
        if _misfiled:
            bad.append(f"(h) 読了の行が年の違う file に在る ({READ_THREADS_SPLIT} 年より前は READ-THREADS.txt): {_misfiled[:3]}")
        if not cand or not read:
            bad.append("(h) THREAD-CANDIDATES.txt か READ-THREADS.txt の行を読めない (導出できないなら照合は沈黙する)")
        elif (int(m.group(1)), int(m.group(2))) != (len(cand), len(read & cand)):
            bad.append(f"(h) AS-OF.md の未読スレッド: 候補 {m.group(1)} 本 / 読んだ {m.group(2)} 本 と述べるが、"
                       f"THREAD-CANDIDATES.txt の会話は {len(cand)}、READ-THREADS.txt のうちそこに在る会話は "
                       f"{len(read & cand)} (読了の行を足して AS-OF を直し忘れたか、行の日付が会話の始まりでない)")
        if cand and read:
            # 提出のゲート 6c の (i) を毎回見えるようにする (2026-11-16・ADVISORY): 確定の道具 (gate_6c) は手で回すときにしか
            #   鳴らないので、census が新しい候補を足して未読が 0 から動いても気づけない。BLOCKING にすると、候補が入るたびに
            #   全員の PR が止まるので ADVISORY に留める (写しの鮮度は CI に写しが無いので確定の道具だけが見る)
            _k498h = len(cand - read)
            check(_k498h == 0, "Check 498 (h) (ADVISORY): 提出のゲート 6c の (i) —— 候補の未読は 0",
                  f"Check 498 (h) (ADVISORY): 候補の未読が {_k498h} 本ある。提出のゲート 6c (未読 0・全て反映) を満たしていない。"
                  "読んで record_read.py で記録する (オーナー: 「全て読んで反映してこそ、出せるクオリティ」)", blocking=False)

    # (h2) 候補の一覧が、いまの census の定義で作られたこと (2026-11-23・BLOCKING): 一覧は --pin でだけ書き直されるので、
    #   決める側の照合 (DECIDERS) や閾値を変えて --pin を回さなければ、gate_6c と (h) は古い定義の一覧を読み「未読 0」を返し
    #   続ける (6d の指摘・「無いと黙る」gate と同じ形)。11-23 に d7 が、表示名が小文字・アドレスだけ・MIME 符号化の決める側の
    #   通 約 224 通が照合から落ちていたのを見つけ、直すと候補が 19 本増えた
    from census_decision_statements import FP_LINE, definition_fingerprint, split_files as _sf498
    _fps = {_f.name: next((l[len(FP_LINE):].split()[0] for l in text(_f).splitlines() if l.startswith(FP_LINE)), None)
            for _f in _sf498("THREAD-CANDIDATES", L)}
    _stale_fp = {n: v for n, v in _fps.items() if v != definition_fingerprint()}
    if _stale_fp:
        bad.append(f"(h2) 候補の一覧の census の定義の指紋 {_stale_fp} が、いまの定義 {definition_fingerprint()} と違う。"
                   "DOSSIER_ARCHIVE_CACHE=<写し> python3 .github/scripts/census_decision_statements.py threads <out> --pin で作り直し、"
                   "AS-OF の未読の行を直す")

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

    # (k) 草案の CHANGELIST の「語数の内訳」の数 (2026-11-15・9b。50 が気付いた): 束の表は 468s の範囲外で、
    #   「増えた語の大半（+N）」は 2 束の和として手で作られ、main で既に 263 ≠ 148 + 118 だった。1c が束の名前を
    #   文に書いたので (add2bdc4)、名指した束の和を表から導出して照合する。同じ節の「前版の N 語から +M 語」
    #   「束の表の合計」「1.0 の N 語から見ると M 語長い」も size() の実測と照合する。束の中身 (どの変更をどの束に
    #   入れるか) は判断なので照合しない
    drafts_k = [p for p in sorted(L.glob("ACD-*-DRAFT.txt")) if "HAS BEEN FROZEN" not in text(p).split("\n", 1)[0]]
    ver_k = re.match(r"ACD-(\d+\.\d+)-DRAFT", drafts_k[0].name).group(1) if len(drafts_k) == 1 else None
    cl_k = text(L / f"ACD-{ver_k}-CHANGELIST.md") if ver_k and (L / f"ACD-{ver_k}-CHANGELIST.md").exists() else ""
    sec_k = cl_k.split("\n## 語数の内訳", 1)[1].split("\n## ", 1)[0] if "\n## 語数の内訳" in cl_k else ""
    m_k = re.search(r"(\d+\.\d+) の ([\d,]+) 語から " + re.escape(str(ver_k)) + r" 草案は ([+−-]\d+) 語", sec_k)
    rows_k = re.findall(r"^\| ([^|]+?) ?\| ([+−-]\d+) \|", sec_k, re.M)
    sum_k = re.search(r"（([^（）]+?)の (\d+) 束で ([+−-]\d+)）", sec_k)
    old_k = re.search(r"1\.0 の ([\d,]+) 語から見ると (\d+) 語長い", sec_k)
    sn = lambda s: int(s.replace("−", "-").replace(",", ""))
    from _lib_draft_counts import draft_has_changes
    from _lib_draft_counts import with_changes as _wc_k
    if drafts_k and not draft_has_changes(_wc_k(drafts_k[0])):
        pass  # 確定の直後 (変更 0 件) は「語数の内訳」の節が空か雛形のままで正しい (2026-11-15 の確定の試走・11-23 に雛形を置いた)
    elif not (m_k and rows_k and sum_k and old_k and (L / f"ACD-{m_k.group(1)}.txt").exists()):
        bad.append(f"(k) ACD-{ver_k}-CHANGELIST.md の「## 語数の内訳」の文 (前版の語数と差・束の表・N 束の和・1.0 との差) が読めない")
    else:
        w_k, w_prev, w_10 = (size(text(p))[0] for p in (drafts_k[0], L / f"ACD-{m_k.group(1)}.txt", L / "ACD-1.0.txt"))
        tab_k = {n.strip(): sn(v) for n, v in rows_k if n.strip() != "束"}
        names_k = [n.strip() for n in re.split(r"、|，|,", sum_k.group(1)) if n.strip()]
        picked_k = [k for k in tab_k if any(k.startswith(n) for n in names_k)]
        for what, got, want in (("前版の語数", sn(m_k.group(2)), w_prev), ("前版からの差", sn(m_k.group(3)), w_k - w_prev),
                                ("束の表の合計", sum(tab_k.values()), w_k - w_prev),
                                ("名指した束の数", int(sum_k.group(2)), len(names_k)),
                                ("名指した束の和", sn(sum_k.group(3)), sum(tab_k[k] for k in picked_k) if len(picked_k) == len(names_k) else None),
                                ("1.0 の語数", sn(old_k.group(1)), w_10), ("1.0 からの差", int(old_k.group(2)), w_k - w_10)):
            if got != want:
                bad.append(f"(k) ACD-{ver_k}-CHANGELIST.md の語数の内訳: {what} {got} / 表と実測から {want}")
    check(not soft_j, "Check 498 (ADVISORY): 「1.0 から何が変わったか」の下書きの語数と条の数が草案と一致",
          f"Check 498 (ADVISORY): {soft_j}。下書きの語数は切り替えの日に prepare_version_freeze.py --report の値へ直す", blocking=False)

    check(
        not bad,
        "Check 498: 自己申告の文の 2 つ目の数と繰り返しが実測と一致 (errata / comparison / faq mirror / §4c / register / 逐条 / 分冊 / 未読スレッドの和と一覧 / 答えていない問いの件数 / 1.0 からの変化の数 / 語数の内訳)",
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

    # ── 500. ドシエの §1.N 見出しが全体で 1 か所にしか無いこと (BLOCKING) ──────────────────
    # 5 人が年の帯で別々の文書 (review-readings-2〜6) に節を足す (2026-11-15)。名を添えない「§1.N」の引用は
    #   見出しが 1 つでないと解決しない
    from _lib_dossier import SECTION_SERIES_FLOOR, section_heading_duplicates
    _n500, _bad500 = section_heading_duplicates(L)
    check(
        _n500 >= 100 and not _bad500,
        f"Check 500: ドシエの §1.N 見出し (N >= {SECTION_SERIES_FLOOR}) {_n500} 個がすべて 1 か所にしか無い",
        (f"Check 500: 同じ §1.N の見出しが 2 か所に在る: {_bad500 or f'見出しが {_n500} 個しか読めない'}。"
         "名を添えない「§1.N」の引用がどちらの節かを決められない。自分の帯 (review-readings-N の冒頭) の番号を使え"),
        blocking=True,
    )

    # ── 501. 読んだ節の「反映」の欄 (BLOCKING・未定は ADVISORY) ──────────────────────────────
    # 5 人で未読を読む日 (2026-11-15) から、節ごとに「どこへ効いたか」を書く。合成 (2f の提案 (C)) は B# を鍵に集める
    from _lib_dossier import REFLECT_FROM, reflect_field_misses
    _n501, _bad501, _pend501 = reflect_field_misses(L)
    check(not _bad501, f"Check 501: §1.{REFLECT_FROM} 以降の {_n501} 節がすべて反映の欄を語彙で持つ",
          (f"Check 501: 反映の欄が欠けるか誤る: {_bad501}。節の末尾に「**反映**: B# / against #N / errata E# / 1c 種 / 入口 / "
           "なし（理由）」を 1 行書く。**未反映のまま本申請は出せない** (オーナー・2026-11-15)"), blocking=True)
    # 501b: 古い節の反映の表 (REFLECTION-BACKFILL.md・30 の案 (B) と 50 の依頼・2026-11-15)。§1.242 より前の節は、節の末尾の欄か
    #   表の 1 行で満たす。表の行は見出しと 1 対 1・語彙・番号の実在・grep と言うなら行き先が §1.N を引く。反映の無い節の数は
    #   ADVISORY で毎回出し、0 になった日に BLOCKING へ上げる (提出のゲート 6c の (ii) を機械で測る)
    from _lib_dossier import BACKFILL_PENDING, backfill_table_misses
    _nb501, _badb501, _miss501 = backfill_table_misses(L)
    _pendb501 = list(BACKFILL_PENDING)
    check(not _badb501, f"Check 501b: REFLECTION-BACKFILL の {_nb501} 行が見出しと 1 対 1 で、反映先を語彙で名指す",
          (f"Check 501b: 反映の表の行が誤る: {_badb501[:8]}。行は「| 1.N | 反映 | 確かめ方 |」(床 70 の下は「| `<file>` 1.N | …」)。"
           "**未反映のまま本申請は出せない** (6c)"), blocking=True)
    # 2026-11-16 に BLOCKING へ上げた: 5 人の帯で 200 行を足し、反映の無い古い節が 0 になった (提出のゲート 6c の (ii) を
    #   満たした日)。以後は、§1.242 より前の節を新しく足す・表の行を消す、のどちらも反映の欠けとして止まる
    check(not _miss501, f"Check 501b: §1.242 より前の節はすべて欄か表の行で反映を述べる (表 {_nb501} 行)",
          f"Check 501b: 反映の無い古い節 {len(_miss501)} 件 (先頭: {_miss501[:6]})。表に行を足す。**未反映のまま本申請は出せない** (6c)",
          blocking=True)
    check(not _pendb501, "Check 501b (ADVISORY): 反映の表に「未定」の行は無い",
          f"Check 501b (ADVISORY): 反映の表に「未定」の行 {len(_pendb501)} 件: {_pendb501[:6]}。提出の前に決める (6c)",
          blocking=False)
    check(not _pend501, f"Check 501 (ADVISORY): 反映が「未定」の節は無い",
          f"Check 501 (ADVISORY): 反映が「未定」の節 {len(_pend501)} 件: {_pend501[:8]}。提出の前に決める", blocking=False)


    # ── 502. 草案の冒頭の状態の箇条と、投稿した版の記録の節が食い違わないこと (BLOCKING) ──────────────
    # 投稿の日に 1c が「Changes since the version posted on <日付>」の節を足し、状態の箇条を書き換える (2026-11-16 の合意)。片方だけを
    #   直すと、草案が自分の状態について嘘をつき、確定の道具 (gate_6b) は節の日付で 30 日を数える
    from prepare_version_freeze import RULE as _RULE502, working_draft as _wd502
    from _lib_draft_counts import with_changes as _wc502
    _h502 = _wc502(_wd502()).split(_RULE502, 1)[0]
    _sec502 = re.search(r"Changes since the version posted on (\d{4}-\d{2}-\d{2})", _h502)
    _not502 = "It has not been posted to any list." in _h502
    _was502 = re.search(r"It was posted to license-discuss on (\d{4}-\d{2}-\d{2})", _h502)
    _bad502 = []
    if _sec502 and _not502:
        _bad502.append("「It has not been posted to any list.」と「Changes since the version posted on」が同時に在る")
    if bool(_sec502) != bool(_was502):
        _bad502.append("投稿した版の記録の節と「It was posted to license-discuss on <日付>」の箇条の一方だけが在る")
    elif _sec502 and _sec502.group(1) != _was502.group(1):
        _bad502.append(f"節の日付 {_sec502.group(1)} と状態の箇条の日付 {_was502.group(1)} が違う")
    if not _sec502 and not _not502:
        _bad502.append("状態の箇条「It has not been posted to any list.」も、投稿した版の記録の節も無い (状態を述べていない)")
    check(not _bad502, "Check 502: 草案の冒頭の投稿の状態の箇条と、投稿した版の記録の節が食い違わない",
          f"Check 502: 草案が自分の投稿の状態について食い違う: {_bad502}。投稿の日は節と状態の箇条を同じ commit で直す (1c の合意)",
          blocking=True)

