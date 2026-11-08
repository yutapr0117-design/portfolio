"""checks_license_stated_counts.py — 自己申告の文が持つ 2 つ目の数の Check (498)

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
       (g) submission.md の "across N files" と、そこで名指す分冊。
       文が読めないことも RED にする（言い換えると黙る形を残さない）。
"""
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

    check(
        not bad,
        "Check 498: 自己申告の文の 2 つ目の数と繰り返しが実測と一致 (errata / comparison / faq mirror / §4c / register / 逐条 / 分冊)",
        (f"Check 498: 自己申告の文の 2 つ目の数が実測と合わない: {bad}。1 つ目の数 (Check 460) だけを直すと、"
         "同じ文の 2 つ目と隣の繰り返しが偽のまま残る"),
        blocking=True,
    )
