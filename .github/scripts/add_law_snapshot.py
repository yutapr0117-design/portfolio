#!/usr/bin/env python3
"""add_law_snapshot.py — 法令の条を取得した結果を、LICENSES/rounds/ に写しとして置く一式 (2026-11-20・5 人の分担「関連法令の一次資料を読む」)。

**なぜ在るか**: 2026-11-16〜18 に 30・2f が法令の写しを手で 20 本ほど置いた。ヘッダの書き方 (Source / Retrieved / Form)・mirror doc・
rounds/README の在庫表の 1 行・runbook §9 の数を毎回手で揃えていて、取得の日時 (UTC) と取得した条の範囲と本文の sha256 は書いて
いなかった。「どの版の文を、いつ、どの条だけ取ったか」が後から確かめられないと、§18 の「法源を当てた」が測れない。

**取得はこの道具の外で行う**: このリポジトリの自走では curl などの直接取得が許されていないので、各自が WebFetch で 1 条ずつ取得し、
返った逐語の片を本文ファイルに書いてから、この道具で置く。だから写しは **バイト単位の写しではない** (道具がモデルを通して返す)。
ヘッダの Form にそう書き、本文の sha256 は「この写しの本文」の hash (原文の hash ではない) と明記する。

**本文ファイルの形**: 条ごとに `===== <法令の名> <条> (<見出し>) =====` の行で区切り、続く行に逐語の片を「」か "…" で置く。
道具は区切りの数を数え、`--articles` に挙げた条と区切りの見出しを照らす (挙げたのに無い条・無いのに在る条を出して止まる)。
注記の行 (道具が言い換えで返した部分を書き残す行など) は、行頭を `（注）` か `(Note)` で始める。逐語の片の数に入れず、ヘッダに
「逐語の片 N 行・注記 M 行」と分けて書く (2026-11-20・30: 特許法 94 条 1 項の後半の言い換えの注記が逐語と同じに数えられた)。

**書くもの**: `LICENSES/rounds/<YYYY-MM-DD>-<slug>-snapshot.txt` (既に在れば止まる)・mirror doc・rounds/ の在庫表 (分冊) の 1 行。
最後に git add して `sync_stated_counts.py --apply` を回す。--dry-run は何も書かない。

使い方:
    python3 .github/scripts/add_law_snapshot.py --slug us-17-usc-203-1201 --law "17 U.S.C. (United States Code, Title 17)" \\
        --url "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title17-section203" --url "…section1201" \\
        --articles "§203" "§1201" --by portfolio-9b --body /path/to/body.txt \\
        --why "§2.2・§4.1 の irrevocable と §5.2(a) の技術的手段が当たる米国の法源。" --clauses "2.2" "4.1" "5.2" \\
        --row "**観測（17 U.S.C. §203・§1201・WebFetch の逐語の片で、バイト単位の写しではない）**" --who "米国法典" [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUNDS = ROOT / "LICENSES" / "rounds"
DIV = re.compile(r"^===== (.+?) =====$", re.M)


def norm(s: str) -> str:
    return re.sub(r"[\s§第条]", "", s).lower()


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--law", required=True, help="法令の名 (公式の名と番号)")
    ap.add_argument("--url", action="append", required=True)
    ap.add_argument("--articles", nargs="+", required=True, help="取得した条 (本文の区切りの見出しに在ること)")
    ap.add_argument("--by", required=True, help="取得したセッション (portfolio-30 など)")
    ap.add_argument("--body", required=True, help="条ごとに ===== 見出し ===== で区切った逐語の片のファイル")
    ap.add_argument("--why", required=True)
    ap.add_argument("--clauses", nargs="+", required=True, help="この写しを当てる 1.4 草案の条 (2.2 4.1 …)")
    ap.add_argument("--row", required=True, help="rounds/README の在庫表の 3 列目")
    ap.add_argument("--who", required=True, help="rounds/README の在庫表の 2 列目 (出所の種類)")
    ap.add_argument("--dry-run", action="store_true")
    o = ap.parse_args(argv)

    body = Path(o.body).read_text(encoding="utf-8").strip("\n") + "\n"
    heads = DIV.findall(body)
    if not heads:
        print("STOP: 本文に `===== <法令の名> <条> (<見出し>) =====` の区切りが無い")
        return 1
    missing = [a for a in o.articles if not any(norm(a) in norm(h) for h in heads)]
    extra = [h for h in heads if not any(norm(a) in norm(h) for a in o.articles)]
    if missing or extra:
        print(f"STOP: --articles と本文の区切りが合わない —— 挙げたのに区切りが無い: {missing} / 区切りが在るのに挙げていない: {extra}")
        return 1
    NOTE = re.compile(r"^\s*(?:（注）|\(Note\))")
    parts = DIV.split(body)[2::2]
    verb_lines = sum(1 for part in parts for ln in part.split("\n") if re.search(r"「|\"|“", ln) and not NOTE.match(ln))
    note_lines = sum(1 for part in parts for ln in part.split("\n") if NOTE.match(ln))
    empty = [h for h, part in zip(heads, parts)
             if not any(re.search(r"「|\"|“", ln) and not NOTE.match(ln) for ln in part.split("\n"))]
    if empty:
        print(f"STOP: 逐語の片 (「」か \"…\") が無い区切り: {empty} —— 道具が要約した条は置かず、外したと Form に書く")
        return 1
    clauses = sorted(set(o.clauses), key=lambda x: tuple(map(int, re.findall(r"\d+", x))))
    # 凍結した版の草案 (1 行目に HAS BEEN FROZEN) は外し、作業中の版を使う (初版は 1.2 の草案を拾った)
    draft = next(p for p in sorted((ROOT / "LICENSES").glob("ACD-1.*-DRAFT.txt"))
                 if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0])
    dtext = draft.read_text(encoding="utf-8").split("-" * 80, 1)[-1]
    unknown = [c for c in clauses if not re.search(r"^  " + re.escape(c) + r" ", dtext, re.M)]
    if unknown:
        print(f"STOP: --clauses の条が草案 ({draft.name}) に無い: {unknown}")
        return 1

    now = datetime.datetime.now(datetime.timezone.utc)
    today = now.strftime("%Y-%m-%d")
    out = ROUNDS / f"{today}-{o.slug}-snapshot.txt"
    if out.exists():
        print(f"STOP: {out.name} は既に在る (同じ日に同じ slug)")
        return 1
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    urls = "\n".join(("Source: " if i == 0 else "        ") + u for i, u in enumerate(o.url))
    text = (f"{urls}\n"
            f"Law: {o.law}\n"
            f"Articles: {', '.join(o.articles)} ({len(heads)} sections below; {verb_lines} lines of verbatim passages, {note_lines} note lines)\n"
            f"Retrieved: {now.strftime('%Y-%m-%d %H:%M')} UTC by {o.by}, with the WebFetch tool, one page at a time.\n"
            "Form: NOT A BYTE COPY. The fetch tool returns the text through a model. Only passages it returned as verbatim\n"
            "        quotes are kept; anything it summarised is left out. Re-fetch and compare before relying on the exact wording.\n"
            f"Body-SHA256: {digest} (of this file's text below the rule, not of the official source)\n"
            f"Applied to: {draft.name.replace('-DRAFT.txt', '')} draft Sections {', '.join(clauses)}\n\n"
            "WHAT THIS FILE IS NOT. It is not legal advice and not a statement about ACD.\n\n"
            "----- begin fetched passages -----\n" + body)
    lines = text.count("\n")
    if lines > 1000:
        print(f"STOP: {lines} 行で 1,000 行 (Check 365) を越える。条で 2 つに分けて置く")
        return 1
    rel = out.relative_to(ROOT)
    mirror = ROOT / "docs" / "files" / f"{rel}.md"
    doc = (f"---\nfile: {rel}\naudience: ai, human (新卒), 監査人, 第三者全般\nlast-updated: {today}\n"
           f"canonical-ref: LICENSES/rounds/README.md (置き方の規約)\n---\n\n# {rel}\n\n## What\n\n"
           f"{o.law} の {', '.join(o.articles)} を {today} に WebFetch で取得した結果（{o.by}）。バイト単位の写しではない。\n\n"
           f"## Why\n\n{o.why}（当てる 1.4 草案の条: {', '.join('§' + c for c in clauses)}）\n\n"
           "## How\n\n各条を 1 度ずつ取得し、道具が逐語で返した片だけを置いた（`add_law_snapshot.py`）。ヘッダに取得の日時 (UTC)・URL・"
           "取得した条・本文の sha256 を書いてある。\n\n## Constraints\n\n写しは道具を通ったもので、片と片の間に語が無いとは保証しない。"
           "法源は ACD を扱っていない。本文を直さない（`rounds/README.md`）。\n\n## Change impact\n\nこの写しを引く節（§18 の行・jurisdictions）"
           "を直すときは、引用が本文に在るかを確かめる。版が改められたら取り直して新しい日付の写しを置く。\n\n"
           "## Audience-specific notes\n\n- **監査人**: ヘッダの URL を開き、片を原文に当てて確かめられる。\n")
    # 在庫表は年の帯ごとの分冊 (2026-11-23)。差し込みの規則は _lib_rounds_inventory が 1 つだけ持つ
    from _lib_rounds_inventory import insert_row
    row = f"| {today} | {o.who} | {o.row} | `{out.name}` |"
    inv, at_line = insert_row(ROUNDS, today, row, write=False)
    print(f"{rel}: {len(heads)} 条・逐語の片 {verb_lines} 行・注記 {note_lines} 行・{lines} 行・本文の sha256 {digest[:16]}…・当てる条 {clauses}")
    print(f"在庫表 ({inv.name}): {row[:100]}… を {at_line} 行目の後へ")
    if o.dry_run:
        print("dry-run: 何も書かない")
        return 0
    out.write_text(text, encoding="utf-8")
    mirror.write_text(doc, encoding="utf-8")
    insert_row(ROUNDS, today, row)
    subprocess.run(["git", "add", str(out), str(mirror)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / ".github/scripts/sync_stated_counts.py"), "--apply"], cwd=ROOT)
    print("書いた。§18 の行・jurisdictions の段に写しの名を書き、verify を回す")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
