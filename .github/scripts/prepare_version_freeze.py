#!/usr/bin/env python3
"""作業中の草案を確定する機械的な作業を、1 回で行う (手で回す道具・CI では走らせない)。

    python3 .github/scripts/prepare_version_freeze.py --date 2026-11-13

確定の日の手作業は約 50 file に及ぶ。2026-11-06 に使い捨ての worktree で 1.4 を確定して測ると、手作業の誤りの
多くが無音だった (Check 490 / 468v / 442d / 444k / 472h で閉じた)。この道具はその手順の機械的な部分を行う。

やること: 確定本文 (冒頭は §0.13 の型) / 草案の pointer / 次の草案 / 次の CHANGELIST / 記述子 / FREEZE-DATA /
mirror / 適用する面の版と日付 / binary の権利表示 / SPDX XML / 凍結件数 / 「いまの作業場」の行 / digest と STATUS.md。草案の冒頭は CHANGELIST の付録へ逐語で移す。

やらないこと: 判断。外向きの文書の書き換え、REVIEWERS.md の表、語数の申告の文、`measure_descriptor_carryover.py`
が出す条の読み直しは人が行う。走ったあとの consistency の RED が、次に直す場所の一覧である。

**2026-11-15 の試走 (9b・使い捨ての worktree で 1.4 を確定)**: 走ったあとの consistency の RED は 6 群で、うち 3 群
(459c・468x・498 (k): 変更 0 件の新しい草案を想定していなかった) と mutation の版の直書き 12 件は同じ日に直した。残る 3 群は
確定の日の作業である —— (1) 460 (x): B3 と SUBMISSION-MATERIALS の長さの行は「1.4 草案は」と書いており、確定後は
「1.5 草案は」の行が無くなる。出す版の名で書き直す。(2) 444m: 適用中の版を述べる行 (README・REVIEWERS・材料・1.0 の文書の
一部) を、適用する版を決めてから読み直す。(3) Check 362: 作業中の CHANGELIST の中身を打つ mutation (468x・498 (j) など
16 件) は、新しい CHANGELIST が空なので的を外す。確定した版の CHANGELIST を読む Check が無いので、付け替えずに退役させる
(archive へ移すか消す)。退役の候補の名前は、この道具が最後に一覧で出す (orphan_mutations)。退役させた後、その Check の面に
mutation が残るか (Check 479c / 479d) も確かめる。

⚠ 作業ツリーを書き換える。commit の前に差分を読むこと。LICENSE と llms 系は版を置換するだけなので、
過去の経緯を述べる文まで変わる (`ACD-1.1-CHANGELIST.md` §0.13「改名は一括置換しない」)。AIO 層の編集は
aio-guardian を通し、`update_aio_digests.py` を回す。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit("prepare_version_freeze.py requires Python 3.10+")

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"
MIRROR = ROOT / "docs" / "files" / "LICENSES"
DATED = re.compile(r"(?i)(?:re-?measured|measured|re-?run|as of|`wc -w`,)[^\n]{0,40}?\b20\d\d-\d\d-\d\d")
PINNED_COMMAND = re.compile(r"`(?:grep|shasum|wc)\b[^`]*ACD-\d+\.\d+\.txt[^`]*`")
RULE = "-" * 80 + "\n"
APPLY_FILES = (".well-known/agent-skills/index.json", ".well-known/aio-manifest.json", ".well-known/index.json",
               ".well-known/llms.txt", ".well-known/llms_well-known.txt", "LICENSE", "README.md", "index.html",
               "js/components.js", "llms-full.txt", "llms.txt", "llms_well-known.txt", "main.js", "robots.txt", "sitemap.xml",
               "REUSE.toml")


def bump_applied(text: str, old: str, new: str, old_date: str, date: str) -> str:
    """適用する版を上げる。版を述べる行の適用の日付も一緒に直す (版だけ置換すると公開面が偽の日付を述べる)。"""
    lines = []
    # shields のバッジは版の "-" を "--" と escape する (README の `license-ACD--1.3-blue`)。置換から漏れると確定後も
    #   バッジだけが前の版を述べる (2026-11-23・6d が確定の予行で見つけた)
    old_badge, new_badge = old.replace("-", "--"), new.replace("-", "--")
    for line in text.split("\n"):
        if old in line or f"Dedication {old[4:]}" in line or old_badge in line:
            line = line.replace(old_badge, new_badge).replace(old, new).replace(f"Dedication {old[4:]}", f"Dedication {new[4:]}")
            line = re.sub(r"\(ACD-\d+\.\d+ until \d{4}-\d{2}-\d{2}\)", f"({old} until {date})", line)
            line = re.sub(r"\d{4}-\d{2}-\d{2} までは ACD-\d+\.\d+", f"{date} までは {old}", line)
            line = line.replace(f"since {old_date}", f"since {date}").replace(f"{old_date} から", f"{date} から")
        lines.append(line)
    out = "\n".join(lines)
    # sitemap の lastmod は版を述べる <loc> の次の行にある。
    return re.sub(rf"({re.escape(new)}\.[a-z.]+</loc>\n\s*<lastmod>){re.escape(old_date)}", rf"\g<1>{date}", out)


def _and_list(names: list[str]) -> str:
    """["ACD-1.2", "ACD-1.3", "ACD-1.4"] → "ACD-1.2, ACD-1.3 and ACD-1.4" (重複は最初の 1 つだけ残す)。"""
    names = list(dict.fromkeys(names))
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def move_workplace(line: str, v: str, nxt: str, date: str) -> str:
    """「いまの作業場」の行を次版の草案へ向ける。日付つきの追記・訂正の中の名前は書き換えず、その後に追記を足す。

    2026-11-23 (cd が確定の予行で見つけた): 旧版は行の中の `ACD-{v}-DRAFT.txt` をすべて置換し、「**2026-10-29 追記**: 1.3 も
    確定したので、いまの作業場は `ACD-1.4-DRAFT.txt`」の歴史を「… `ACD-1.5-DRAFT.txt`」へ書き換えていた (その日には 1.5 は
    無かった)。468k は行の最後の名前しか見ないので緑のままだった。規則は 468k の docstring と `ACD-1.1-CHANGELIST.md` §0.13
    (歴史の文は書き換えず、日付つきの追記で最後に現在の名前を置く)。日付つきの印の無い行 (表の行・案内の行) は置換する。
    """
    name, new_name = f"ACD-{v}-DRAFT.txt", f"ACD-{nxt}-DRAFT.txt"
    at = line.rfind(name)
    if at < 0 or not re.search(r"\d{4}-\d{2}-\d{2}[^|]{0,12}?(追記|訂正)", line[:at]):
        return line.replace(name, new_name)
    end = at + len(name)
    stops = [i for i in (line.find("。", end), line.find("）", end)) if i >= 0]
    cut = min(stops) if stops else len(line)
    # 太字の中に挿すときは印を太字にしない (入れ子の ** は描画で閉じ位置がずれる・READY-TO-SUBMIT の「出す版は …」の行)
    mark = f"{date} 追記" if line.count("**", 0, at) % 2 else f"**{date} 追記**"
    note = f"{mark}: {v} も {date} に確定したので、いまの作業場は `{new_name}`"
    if cut < len(line) and line[cut] == "。":
        return line[:cut + 1] + note + "。" + line[cut + 1:]
    return line[:cut] + "。" + note + line[cut:]


def record_history(text: str, old: str, date: str) -> str:
    """適用の履歴へ前の版を足す。前の版の許諾は消えない (§2.2) ので、履歴から落とすと読み手が誤解する。"""
    m = re.search(r"Until\s+(\d{4}-\d{2}-\d{2})\s+this\s+repository\s+applied\s+(ACD-\d+\.\d+)(,\s+and\s+until)?", text)
    if m is None:
        raise SystemExit("ERROR: 適用の履歴の文が見つからない。文を読んで手で直す")
    joint = "until" if m.group(3) else "and until"
    out = text[:m.start()] + f"Until {date} this repository applied {old}, {joint} {m.group(1)} {m.group(2)}"
    return out + (", and until" if m.group(3) else "") + text[m.end():]


def para(text: str, indent: str = "  ", first: str | None = None) -> str:
    return textwrap.fill(" ".join(text.split()), width=78, initial_indent=first if first is not None else indent,
                         subsequent_indent=indent, break_long_words=False, break_on_hyphens=False)


def bullet(text: str) -> str:
    return para(text, indent="      ", first="    * ")


def size(text: str) -> tuple[int, int]:
    body = text.split(RULE, 1)[1] if RULE in text else text
    return len(body.split()), len(set(re.findall(r"^  (\d+\.\d+) ", body, re.M)))


def errata_closures() -> tuple[int, dict[str, list[str]], list[str], dict[str, int]]:
    """errata の表から (件数, {版: [閉じた E-ID]}, [印の無い E-ID], {節: 件数}) を導く。

    数え方は portfolio-00 / aa と決めたもの (2026-11-11): 閉鎖の印は最後の欄の「N.M 草案で閉じた」で、
    1 件は最初の印の版に数える (E24 は 1.2 と 1.3 の両方の印を持ち、1.2 に数える)。節は 2 列目の最初の §。
    切り替えの日に REVIEWERS の "Which text" と草案の冒頭が述べる数は、ここから出す (手で数えない)。
    """
    rows = [re.split(r"(?<!\\)\|", line) for line in (L / "ACD-1.0.errata.md").read_text(encoding="utf-8").split("\n")
            if re.match(r"^\|\s*\*{0,2}E\d+", line)]
    closed: dict[str, list[str]] = {}
    unmarked, sections = [], {}
    for c in rows:
        eid = c[1].strip().strip("*")
        m = re.search(r"(\d+\.\d+) 草案で閉じた", c[-2])
        if m:
            closed.setdefault(m.group(1), []).append(eid)
        else:
            unmarked.append(eid)
        sec = re.search(r"§(\d+)", c[2])
        key = sec.group(1) if sec else "—"
        sections[key] = sections.get(key, 0) + 1
    return len(rows), closed, unmarked, sections


def frozen_versions() -> list[str]:
    found = [re.match(r"ACD-(\d+\.\d+)\.txt$", p.name) for p in L.glob("ACD-*.txt")]
    return sorted((m.group(1) for m in found if m), key=lambda v: tuple(map(int, v.split("."))))


def working_draft() -> Path:
    cands = [p for p in sorted(L.glob("ACD-*-DRAFT.txt"))
             if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    if len(cands) != 1:
        sys.exit(f"作業中の草案が 1 つに定まらない: {[p.name for p in cands]}")
    return cands[0]


def appendix(head: str, header: str) -> str:
    """CHANGELIST の末尾に、確定時点の草案の冒頭を逐語で足した本文を返す。

    CHANGELIST に `<!-- APPENDIX-NOTE: … -->` があれば、その文を付録の見出しの直下に 1 段落で置く (2026-11-16・30 の案)。
    冒頭の一覧の形が草案の途中で変わったとき (1.4 では 11-16 に理由の句を外した・bd5d71e3) に、前の形がどこに在るかを
    付録が指せるようにする。文は版ごとに CHANGELIST が持ち、道具は版を決め打ちしない (逐語の付録の前に置くので、
    frozen_header の "keeps, word for word" は付録の本体についてそのまま真)。"""
    m = re.search(r"<!--\s*APPENDIX-NOTE:\s*(.*?)\s*-->", head, re.S)
    note = f"{' '.join(m.group(1).split())}\n\n" if m else ""
    return f"{head}\n\n## 付録: 確定時点の草案ヘッダ（逐語）\n\n{note}```\n{header.rstrip()}\n```\n"


def frozen_header(v: str, prev: str, nxt: str, date: str, pw: int, pc: int, w: int, c: int) -> str:
    return "\n\n".join([
        f"ACD-{v} -- FROZEN TEXT.",
        para(f"This file is a fixed text. It is pinned by SHA-256 in LICENSES/FROZEN.md and verified in CI, so that anyone "
             f"discussing it is discussing the same words. Work on the next version happens in LICENSES/ACD-{nxt}-DRAFT.txt, not here."),
        para("Everything above the line below describes this file. It is not part of the Dedication (Section 1.1), and a "
             "copy may leave it out."),
        "  Status of this version, stated plainly so that nobody has to infer it:",
        "\n".join([
            bullet(f"On the date this text was fixed ({date}), it had had no legal review, it had not been submitted to OSI "
                   "license-review, and it was not on the SPDX License List. A frozen text cannot be updated, so this line "
                   "describes that date only; LICENSES/FROZEN.md records what has happened since."),
            bullet(f"Clause numbers follow ACD-{prev}, not ACD-1.0. Citations to an earlier version must keep using that "
                   "version's text."),
            bullet(f"Every change from ACD-{prev}, with what it closes and what it cost in words, is recorded in "
                   f"LICENSES/ACD-{v}-CHANGELIST.md. That record is in Japanese; its appendix keeps, word for word and in "
                   "English, the change list this file carried while it was a draft."),
            bullet(f"ACD-{prev}: {pw:,} words, {pc} clauses. This version: {w:,} words, {c} clauses."),
        ]),
        "  The terms begin below.",
        "",
    ])


def next_draft_header(v: str, nxt: str, applied: str, versions: list[str], w: int, c: int, still_open: str) -> str:
    names = [f"ACD-{x}" for x in versions]
    pinned = ", ".join(names[:-1]) + " and " + names[-1]
    plain = ", ".join(versions[:-1]) + " and " + versions[-1]
    return "\n\n".join([
        f"ACD-{nxt} -- DRAFT. NOT IN FORCE. NOT SUBMITTED. NOT APPLIED TO THIS REPOSITORY.",
        para(f"This file is the successor text under construction. The latest frozen text is ACD-{v} (LICENSES/ACD-{v}.txt), "
             f"and the licence that covers this repository is {applied}. {pinned} are pinned by SHA-256 in LICENSES/FROZEN.md "
             "and verified in CI; nothing here changes any of them."),
        # 凍結版の frozen_header と同じ断り (2026-11-12・portfolio-aa が 1.4 草案の冒頭に足した段落): 次版の草案にも引き継ぐ
        para("Everything above the line below describes this file. It is not part of the Dedication (Section 1.1), and a "
             "copy may leave it out."),
        "  Status of this draft, stated plainly so that nobody has to infer it:",
        "\n".join([
            bullet(f"It has had no legal review, like {plain}."),
            bullet("It has not been posted to any list."),
            bullet(f"It is at present identical to ACD-{v} apart from the version number and the identifiers that name it. "
                   f"An empty list in LICENSES/CHANGES-ACD-{nxt}.txt means nothing has been changed yet -- not that the "
                   "record is missing; a list with entries in it is the whole of the difference."),
            bullet(f"Clause numbers follow ACD-{v}, not ACD-1.0. Citations to an earlier version must keep using that "
                   "version's text."),
            bullet(f"Changes are recorded in LICENSES/ACD-{nxt}-CHANGELIST.md."),
        ]),
        # 変更の一覧は草案の外 (CHANGES-ACD-N.M.txt) に置く (2026-11-20・案 A)。草案の冒頭は在りかだけを書く
        para(f"The list of changes from ACD-{v}, one entry per change with its word count, is in "
             f"LICENSES/CHANGES-ACD-{nxt}.txt."),
        para(still_open),
        "",
    ])


def next_changes(v: str, nxt: str, w: int, c: int) -> str:
    """次版の変更の一覧の雛形 (草案の外・CHANGES-ACD-N.M.txt)。要約の行だけを持ち、試作を採るたびに箇条を足す。"""
    return "\n\n".join([
        f"ACD-{nxt} -- CHANGES FROM ACD-{v} (DRAFT). Not part of the Dedication.",
        para(f"The reasons for each change are in LICENSES/ACD-{nxt}-CHANGELIST.md (in Japanese)."),
        f"  Changes in this draft, relative to ACD-{v}:",
        bullet(f"ACD-{v}: {w} words, {c} clauses. This draft: {w} words, {c} clauses."),
    ]) + "\n"


def pointer(v: str, nxt: str, prev: str, date: str) -> str:
    return "\n\n".join([
        f"ACD-{v}-DRAFT -- THIS DRAFT HAS BEEN FROZEN. THIS FILE IS A POINTER, NOT A LICENCE TEXT.",
        para(f"The draft that was kept here was frozen on {date} as LICENSES/ACD-{v}.txt. The next version is drafted in "
             f"LICENSES/ACD-{nxt}-DRAFT.txt; if that draft has since been frozen, that file says where work happens now."),
        para(f"This pointer exists because the frozen text LICENSES/ACD-{prev}.txt names this file as the place where work on "
             f"the next version happens, and a frozen text cannot be corrected. The editorial notes this draft carried are "
             f"kept, word for word, in LICENSES/ACD-{v}-CHANGELIST.md."),
        "",
    ])


# 次版の記述子の textRedistribution の注 (errata E10 を閉じる鍵・§16.4 の機械可読の写し)。Check 451g が、草案の §16.4 の鍵の語を
#   この注が落としていないかを照らす (2026-11-16・9b: 1.4 草案の §16.4 は「ACD- を含む・大文字小文字を問わない・前の Steward・
#   折り返しは改変でない」へ動いたが、注は「ACD- で始まる」のまま残っていた —— 確定すると記述子が本文と違うことを言う)
TEXT_REDISTRIBUTION_NOTE = (
    "The text of this Dedication may be copied and distributed verbatim by anyone. Making a modified text is not restricted; "
    "what is restricted is distributing one under any name that contains \"Autonomous Commons Dedication\", regardless of case, "
    "or under any identifier that contains \"ACD-\", regardless of case, followed by a digit, except by the Steward (section 16.5). "
    "That exception reaches only a new version under a version number and identifier that no earlier text the Steward or a "
    "former Steward has published, other than a draft identified as such, has borne. A modified text may be distributed under "
    "a different name. A translation identified as one that states that the English text prevails, and a re-encoding with the "
    "words unchanged that is identified as one, are not modified texts for this purpose; differences of line breaking, "
    "indentation, or markup are not modifications. This restriction concerns the text of this Dedication as a document; it is "
    "not a condition upon any use of the Work (sections 10.5 and 16.6).")
# 草案の §16.4 に在れば注にも在るべき語 (Check 451g)
#   語は「どの部分の語か」が分かる句にする: "contains" だけだと名前の側にも在り、識別子の側を「begins with」へ戻しても通った
#   (mutation で実測・2026-11-16)
TEXT_REDISTRIBUTION_TERMS = ("name that contains", "identifier that contains", "regardless of case", "former Steward",
                             "different name", "translation", "re-encoding", "line breaking", "draft identified as such")


def descriptor(v: str, prev: str, body: str, date: str) -> str:
    raw = (L / f"ACD-{prev}.machine.json").read_text(encoding="utf-8")
    d = json.loads(raw.replace(f"ACD-{prev}", f"ACD-{v}").replace(f'"{prev}"', f'"{v}"').replace(f"Dedication {prev}", f"Dedication {v}"))
    m = re.search(r"following form:\s*\n(.*?)\n\n  16\.2 ", body, re.S)
    d["notice"] = " ".join(m.group(1).split())
    # 状態の key は凍結すると承認の日に偽になるので、日付つきの記録へ移す (ACD-1.4-CHANGELIST.md「確定前検証（段 7）」)。
    if "osiApproved" in d:
        d["schemaVersion"] = 2
        d["$comment"] = d["$comment"].replace(
            "Every fact below cites the clause it comes from, and a blocking CI check verifies that each cited clause exists in the text.",
            "Every entry with a clause key cites the clause it comes from, and a blocking CI check verifies that each cited "
            "clause exists in the text. name, version, text, and steward identify this file; statusAtFixing records outside "
            "facts on the date this file was fixed and is not drawn from any clause.")
        out = {}
        for k, val in d.items():
            if k in ("osiApproved", "spdxListed"):
                continue
            out[k] = val
            if k == "steward":
                out["statusAtFixing"] = {"date": date, "osiApproved": False, "spdxListed": False, "legalReview": False,
                                         "note": "True on the date above. LICENSES/FROZEN.md records what has happened since."}
        d = out
        d["permissions"] = {**{k: x for k, x in d["permissions"].items() if k == "use"},
                            "studyAndAnalysis": {"value": True, "clause": "4.2"},
                            "reverseEngineering": {"value": True, "clause": "4.2"},
                            **{k: x for k, x in d["permissions"].items() if k != "use"}}
        d["reservationsAndLimits"]["textRedistribution"]["note"] = TEXT_REDISTRIBUTION_NOTE
        out = {}
        for k, val in d.items():
            out[k] = val
            if k == "reservationsAndLimits":
                out["covenants"] = {
                    "noAssertionOfCoveredRights": {"value": True, "clause": "5.1"},
                    "noCollateralObligationByDedicator": {"value": True, "clause": "5.2", "note": "Section 5.2, paragraph (b)."},
                    "noAssertionOfLicensedPatentClaims": {"value": True, "clause": "8.6"},
                }
                out["machineGeneratedMaterial"] = {
                    "rightAssertedByDedicator": {"value": False, "clause": "9.2"},
                    "recipientMustDetermineWhichParts": {"value": False, "clause": "9.3"},
                }
        d = out
    return json.dumps(d, ensure_ascii=False, indent=2) + "\n"


def _snippet(line: str, at: int) -> str:
    return " ".join(line[max(0, at - 50):at + 110].split())


def finish(v: str, prev: str, nxt: str, date: str, clauses: int) -> None:
    """機械で決まる残りを片付ける。文を読むもの (Check 444m) は人に残す。"""
    from checks_license_self_reporting import _NUM_WORDS

    pins = len(re.findall(r"(?m)^[0-9a-f]{64}  \S+", (L / "FROZEN.md").read_text(encoding="utf-8")))
    word = next(w for w, n in _NUM_WORDS.items() if n == pins)
    for name in ("REVIEWERS.md", "ACD-1.0.errata.md"):
        text = re.sub(r"\d+× OK", f"{pins}× OK", (L / name).read_text(encoding="utf-8"))
        text = re.sub(r"(pins the SHA-256 of|prints `OK` for all) [a-z-]+ files", rf"\1 {word} files", text)
        (L / name).write_text(re.sub(r"\(re-run \d{4}-\d{2}-\d{2},", f"(re-run {date},", text), encoding="utf-8")
    # 入口の「ドシエ全体は N 語・本文の M 倍」も機械で決まる。確定で増える file (凍結本文・次の草案・CHANGELIST・
    #   記述子・SPDX XML) で約 1 万語増え、Check 472m の 10% の幅を越えていた (2026-11-09 の予行)。
    rv = L / "REVIEWERS.md"
    rvt = rv.read_text(encoding="utf-8")
    lw = re.search(r"\(ACD-\d+\.\d+\.txt\) \| \*\*([\d,]+)\*\* \| the licence\b", rvt)
    if lw:
        total = sum(len(p.read_text(encoding="utf-8", errors="replace").split()) for p in L.rglob("*")
                    if p.is_file() and "rounds" not in p.relative_to(L).parts and not p.name.startswith("."))
        rv.write_text(re.sub(r"is \*\*[\d,]+ words\*\*, \*\*\d+ times the licence\*\*",
                             f"is **{total:,} words**, **{round(total / int(lw.group(1).replace(',', '')))} times the licence**",
                             re.sub(r"Measured \d{4}-\d{2}-\d{2}, the analysis in", f"Measured {date}, the analysis in", rvt)),
                    encoding="utf-8")

    # AS-OF の「Text frozen」の行も同じコマンドの期待値を述べる。Check 460 (q) が読む (2026-11-08 から)。
    asof = L / "AS-OF.md"
    asof.write_text(re.sub(r"(?m)^(\| Text frozen \| \*\*)\d{4}-\d{2}-\d{2}(\*\* \| Yes; )[a-z-]+( files pinned.*?→ )\d+(× OK)",
                           rf"\g<1>{date}\g<2>{word}\g<3>{pins}\g<4>", asof.read_text(encoding="utf-8")), encoding="utf-8")
    # 質問票は基準の版を述べる文と語だけを動かす。問いの順は `ACD-1.4-CHANGELIST.md` の切り替えの表が決める。
    counsel = L / "QUESTIONS-FOR-COUNSEL.md"
    text = re.sub(r"(?m)^(canonical-ref: LICENSES/)ACD-\d+\.\d+\.txt", rf"\g<1>ACD-{v}.txt", counsel.read_text(encoding="utf-8"), count=1)
    text = re.sub(r"Clause numbers are those of \*\*ACD-[\d.]+\*\* \(`ACD-[\d.]+\.txt`, fixed on \d{4}-\d{2}-\d{2},\s+\d+ clauses\),"
                  r"(\s+which is the version this repository applies\.)\s+(ACD-[\d.]+) and the successor draft\s+ACD-[\d.]+ use the same numbers;"
                  r" the draft differs only by the changes its header lists\.",
                  lambda m: f"Clause numbers are those of **ACD-{v}** (`ACD-{v}.txt`, fixed on {date}, {clauses} clauses),{m.group(1)} "
                            f"{m.group(2)} and ACD-{prev} use the same numbers.", text)
    # 確定の後の形 (2026-11-23・1.4 の確定で上の式が書いた形): 「… which is the version this repository applies. ACD-1.2 and ACD-1.3
    #   use the same numbers.」。上の式は草案を名乗る形しか読まないので、次の確定 (1.5) で基準の版が 1.4 のまま残り、予行で
    #   472h が一覧の外の RED になった。確定の後の形も読み、前の版を「同じ番号」の列に足す
    text = re.sub(r"Clause numbers are those of \*\*ACD-[\d.]+\*\* \(`ACD-[\d.]+\.txt`, fixed on \d{4}-\d{2}-\d{2},\s+\d+ clauses\),"
                  r"(\s+which is the version this repository applies\.)\s+((?:ACD-[\d.]+,? )+)and (ACD-[\d.]+) use the same numbers\.",
                  lambda m: f"Clause numbers are those of **ACD-{v}** (`ACD-{v}.txt`, fixed on {date}, {clauses} clauses),{m.group(1)} "
                            + _and_list(re.findall(r"ACD-[\d.]+", m.group(2)) + [m.group(3), f"ACD-{prev}"]) + " use the same numbers.", text)
    counsel.write_text(text.replace(f"the {v} draft", f"ACD-{v}").replace(f"The {v} draft", f"ACD-{v}"), encoding="utf-8")
    # 「いまの作業場」の行は Check 468k / 468t が場所を名指す。同じ規則を 2 か所に書かない。
    report = subprocess.run([sys.executable, ".github/scripts/check_repository_consistency.py"], cwd=ROOT, text=True, capture_output=True).stdout
    found = next((line for line in report.splitlines() if line.startswith("ERROR: Check 468:")), "")
    for path, n in re.findall(r"'([^':]+):(\d+) → ACD-[\d.]+-DRAFT\.txt'", found):
        lines = (ROOT / path).read_text(encoding="utf-8").split("\n")
        lines[int(n) - 1] = move_workplace(lines[int(n) - 1], v, nxt, date)
        (ROOT / path).write_text("\n".join(lines), encoding="utf-8")
    block = re.search(r"468t: [^\[]*\[([^\]]*)\]", found)
    for path in re.findall(r"'([^':]+) → ", block.group(1)) if block else []:
        target = f"ACD-{v}.txt" if f"ACD-{v}-" in path else f"ACD-{nxt}-DRAFT.txt"
        text = (ROOT / path).read_text(encoding="utf-8")
        (ROOT / path).write_text(re.sub(r"(?m)^canonical-ref:.*$", lambda m: m.group(0).replace(f"ACD-{v}-DRAFT.txt", target), text, count=1), encoding="utf-8")
    for tool in ("update_aio_digests.py", "generate_status.py", "sync_size_table.py"):
        subprocess.run([sys.executable, f".github/scripts/{tool}"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


def quotes_gone_from(version: str, target: Path) -> list[tuple[str, int, str]]:
    """同じ文で「{version} 草案 / {version} draft / ACD-{version}」を名乗り、どの版の本文には在るが target には無い語を引く行。

    Check 470 は 1.0 の地図で合えば通すので、草案から外した語を「1.4 草案は … と述べる」と引き続けても鳴らない。
    ADVISORY の Check として試作すると main で 4 件とも誤検出だった（地図 §2.9・2026-11-16）ので、確定の日に人が読む一覧として出す。
    merge 前の --compare は、その試作の後に書いた段落を拾わない。
    """
    def norm(s: str) -> str:
        return re.sub(r"\s+", " ", s).lower()
    texts = [norm(p.read_text(encoding="utf-8")) for p in sorted(L.glob("ACD-1.[0-9]*.txt"))]
    tgt = norm(target.read_text(encoding="utf-8").split("-" * 80, 1)[-1])
    named = re.compile(rf"(?<![\d.§])(?:ACD-{re.escape(version)}(?![\d\-])|{re.escape(version)}\s*(?:草案|draft))")
    quote = re.compile(r'\*"([^"]{6,300})"\*|"([A-Za-z][^"\u201c\u201d]{8,300})"|\u201c([^\u201d]{8,300})\u201d')
    out = []
    for f in sorted(L.glob("*.md")):
        if re.match(r"ACD-1\.[1-9]-", f.name) or re.match(r"ACD-1\.0\.(?:errata|against)", f.name):
            continue  # 版を名に持つ作業の文書は Before / After を並べ、errata と against は旧版の語を「草案で直した」と引く
        for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            for sent in re.split(r"(?<=。)", line):
                bare = quote.sub(" ", sent)
                # ほかの版も名乗る文 (「1.1 to 1.3 では …、1.4 草案は改めた」) は旧版の語を旧版として引く
                if not named.search(bare) or re.search(rf"(?<![\d.§])1\.(?!{re.escape(version[2:])}(?!\d))\d(?![\d.])", bare):
                    continue
                for m in quote.finditer(sent):
                    q = re.sub(r"\*\*|\\", "", next(g for g in m.groups() if g))
                    nq = re.sub(r"[.,;:]+$", "", norm(q)).strip()
                    if len(q.split()) >= 5 and nq not in tgt and any(nq in x for x in texts):
                        out.append((f.name, i, q))
    return out


def report(version: str) -> int:
    """提出対象を切り替える日に人が読む行を列挙する。何も書き換えない。"""
    from measure_citation_drift import CITE, FACES, FIRST_READ, cited_lines

    marker = re.search(r"<!-- SUBMISSION-TARGET: ACD-(\d+\.\d+) -->", (L / "ACD-1.0.submission.md").read_text(encoding="utf-8"))
    if marker is None:
        raise SystemExit("ERROR: submission.md に SUBMISSION-TARGET の marker が無い")
    base = marker.group(1)
    kinds, rows = cited_lines(base, version)
    print(f"# ACD-{base} から ACD-{version} へ切り替える日に読む行\n")
    print("## 番号が残って別の条になる / 無くなる条")
    print("  " + "  ".join(f"§{n} ({k})" for n, k in sorted(kinds.items(), key=lambda x: [int(p) for p in x[0].split(".")])))
    named = re.compile(rf"(?:ACD-)?{re.escape(base)}\b")
    top = [r for r in rows if FIRST_READ.search(r[0])]
    rest = [r for r in rows if not FIRST_READ.search(r[0])]
    unnamed = [r for r in rest if not named.search(r[3])]
    print(f"\n### 全部読む面: {len(top)} 行")
    for f, i, hit, line in top:
        print(f"  {f}:{i}  {' '.join('§' + n for n in hit)}  {_snippet(line, CITE.search(line).start())}")
    print(f"\n### 残りの面: {len(rest)} 行のうち ACD-{base} と名指していない {len(unnamed)} 行")
    for f, i, hit, line in unnamed:
        print(f"  {f}:{i}  {' '.join('§' + n for n in hit)}  {_snippet(line, CITE.search(line).start())}")
    print(f"\n## submission.md の §A が ACD-{base} を述べる行（送る本文は Check 472o が見る。履歴の文は残す）")
    head = (L / "ACD-1.0.submission.md").read_text(encoding="utf-8").split("\n## B. ")[0].split("\n")
    for i, line in enumerate(head, 1):
        if re.search(rf"(?<![\w-])ACD-{re.escape(base)}(?![.\w-]*\.md)", line) and not line.startswith(">"):
            print(f"  ACD-1.0.submission.md:{i}  {_snippet(line, line.index('ACD-'))}")
    print("\n## 日付つきの実測（走らせ直して値と日付を直す）")
    pinned = []
    for f in FACES:
        if not FIRST_READ.search(f) and f != "README.md":
            continue
        for i, line in enumerate((L / f).read_text(encoding="utf-8").split("\n"), 1):
            m = DATED.search(line)
            if m:
                print(f"  {f}:{i}  {_snippet(line, m.start())}")
            pinned += [(f, i, c.group(0)) for c in PINNED_COMMAND.finditer(line)]
    print("\n## 版を決め打ちした検証コマンド（確定の版へ向ける）")
    for f, i, command in pinned:
        print(f"  {f}:{i}  {command[:110]}")
    # 1.0 から何が変わったかの数 (portfolio-aa の依頼・2026-11-11)。REVIEWERS の "Which text" と草案の冒頭の
    #   英文は、この段の数を写す (使い捨ての計数で出すと、版の語の最初の一致を数えて 5・38 と誤った)
    total, closed, unmarked, sections = errata_closures()
    vers = sorted(closed, key=lambda x: tuple(map(int, x.split("."))))
    print(f"\n## 1.0 から何が変わったか（REVIEWERS の \"Which text\" と草案の冒頭が述べる数）")
    print(f"  errata {total} 件のうち閉じた {sum(map(len, closed.values()))} 件（最初の「N.M 草案で閉じた」の版に数える）: "
          + " / ".join(f"{v} {len(closed[v])}" for v in vers) + f"・印の無い行 {unmarked}")
    print("  節ごとの件数（表の 2 列目の最初の §）: "
          + " / ".join(f"§{k} {n}" for k, n in sorted(sections.items(), key=lambda kv: (-kv[1], kv[0]))))
    target = L / f"ACD-{version}.txt"
    if not target.exists():
        target = working_draft()
    gone = quotes_gone_from(version, target)
    print(f"\n## 「{version} 草案は … と述べる」の文が、{version} の本文に無い語を引いている行: {len(gone)}（外した語を引き続けていないか読む）")
    for f, i, q in gone:
        print(f"  {f}:{i}  \"{q[:80]}\"")
    for path in (L / "ACD-1.0.txt", target):
        w, c = size(path.read_text(encoding="utf-8"))
        print(f"  {path.name}: {w:,} 語・{c} 条（区切り線の後から数える。Check 468 と同じ数え方）")
    return 0


def _month_404_recently(lst: str, d, today) -> bool:
    """日次の取得 (fetch_osi_watch.py・~/osi-fetch/watch/<日付>/summary.json) が 3 日以内に、そのリストの今月を HTTP 404 と
    記録したか。pipermail は月の最初の投稿が来るまで月のページを作らない (2026-11-16: 両リストとも 11 月は 16 日間 404)。"""
    import datetime
    import json
    root = Path.home() / "osi-fetch" / "watch"
    for k in range(4):
        s = root / (today - datetime.timedelta(days=k)).isoformat() / "summary.json"
        if s.exists() and json.loads(s.read_text(encoding="utf-8")).get(f"license-{lst}_{d.strftime('%Y-%B')}.txt") == "HTTP 404":
            return True
    return False


def archive_cache_staleness(today: "datetime.date | None" = None) -> list[str]:
    """census の写しが提出の日に新しいか (6c の逆側「未読 0 は写しの上の数」を手順でなく止めにする・2026-11-16)。

    先月の両リストは月が終わった後に取ったもの、今月の両リストは 3 日以内に取ったものが写しに在ること。今月の初め 3 日は、
    投稿が無いと月の file が無い (404) ので今月を求めない。それより後でも、日次の取得が 3 日以内に今月を 404 と記録して
    いれば、投稿が無いとして満たす (_month_404_recently)。写しが無い機械では「写しが無い」と止まる。
    """
    import datetime
    import os
    today = today or datetime.date.today()
    cache = Path(os.environ.get("DOSSIER_ARCHIVE_CACHE", Path.home() / "osi-archive-cache"))
    if not cache.is_dir():
        return [f"census の写し {cache} が無い (未読 0 を確かめられない)"]
    first = today.replace(day=1)
    prev = first - datetime.timedelta(days=1)
    out = []
    for lst in ("review", "discuss"):
        for d, need_after in ((prev, first), (today, today - datetime.timedelta(days=3))):
            if d is today and today.day <= 3:
                continue
            f = cache / f"license-{lst}-{d.strftime('%Y-%B')}.txt"
            got = datetime.date.fromtimestamp(f.stat().st_mtime) if f.exists() else None
            if got is None and d is today and _month_404_recently(lst, d, today):
                continue  # 今月はまだ投稿が無い (日次の取得が 3 日以内に 404 と記録した)。置く物が無いのは古さではない
            if got is None or got < need_after:
                out.append(f"写しの {f.name} が{'無い' if got is None else f' {got} の取得で古い'} —— "
                           "fetch_osi_watch.py --to-cache で取り直し、census を --pin で回し直して未読を確かめる")
    return out


def gate_6b(today: "datetime.date | None" = None) -> list[str]:
    """段 6b (OSI-APPROVAL-PLAN.md §4・SUBMISSION-MATERIALS §0 の 0b): 出す版を license-discuss に少なくとも 30 日置いてから確定する。

    投稿の日は、草案の冒頭の節 "Changes since the version posted on <YYYY-MM-DD>" が記録する (50 と 1c の合意・2026-11-15)。
    日付は公開アーカイブに届いた日で、同じ節にその通の URL (license-discuss の pipermail・日付と同じ月) が要る (2026-11-16)。
    拒否の道: 同じ節に "Posting rejected by moderation on <日付>" と rounds/ の stub の path が在れば、stub の実在と在庫、
    FROZEN.md の <!-- STAGE-6B-DECISION: <日付> proceed … --> (拒否より後) を見て通す (段 6b の (3)・50 の提案)。
    その節が無ければ、窓はまだ始まっていない。根拠は Chestek 氏 2026-01-23 の "at least 30 days for feedback on
    license-discuss before submitting to license-review"。**逆側** (段 6b の行と同じ): 規則ではなく 1 人の助言で、30 日置いても
    議論が来る保証は無い。届いたかは公開アーカイブで確かめる (ゲート 10) —— この関数は日付しか見ない。
    """
    import datetime
    today = today or datetime.date.today()
    from _lib_draft_counts import with_changes
    head = with_changes(working_draft()).split(RULE, 1)[0]
    m = re.search(r"Changes since the version posted on (\d{4}-\d{2}-\d{2})", head)
    if not m:
        return ["段 6b: 出す版を license-discuss に出した記録が草案の冒頭に無い (\"Changes since the version posted on <日付>\")"
                " —— 30 日の窓が始まっていない。投稿はオーナーが自分の言葉で書く (B14)"]
    # 日付は投稿が公開アーカイブに届いた日で、同じ節にその通の URL を置く (50 の提案・2026-11-16): moderation で拒否された投稿は
    #   届いていないので、日付だけでは窓を数えられない。照らすのは URL の形と月の一致だけで、届いたことはゲート 10 で人が確かめる
    sec = head[m.start():]
    nxt = re.search(r"\n\s*\n\s*[*-] |\n\S", sec[1:])
    sec = sec[: nxt.start() + 1] if nxt else sec
    d = datetime.date.fromisoformat(m.group(1))
    rej = re.search(r"Posting rejected by moderation on (\d{4}-\d{2}-\d{2})", sec)
    if rej:
        # 拒否の道 (段 6b の (3)・50 の提案・2026-11-16): 拒否された投稿は届いていないので 30 日は数えない。拒否の stub
        #   (B14 の off-list の stub と同じ形・本文を置かない) が rounds/ に実在して在庫に載り、FROZEN.md の
        #   STAGE-6B-DECISION marker が拒否の日より後に「proceed」と決めていれば通す。判断が記録に残ることが条件
        bad = []
        stub = re.search(r"(LICENSES/rounds/[\w.\-]+\.txt)", sec)
        if not stub or not (ROOT / stub.group(1)).exists():
            bad.append("拒否の stub の path が節に無いか、file が無い")
        elif Path(stub.group(1)).name not in __import__("_lib_rounds_inventory").all_text(L / "rounds"):
            bad.append(f"拒否の stub {Path(stub.group(1)).name} が rounds/ の在庫表 (INVENTORY-*.md) に無い")
        dm = re.search(r"<!--\s*STAGE-6B-DECISION:\s*(\d{4}-\d{2}-\d{2})\s+(proceed|wait)\b", (L / "FROZEN.md").read_text(encoding="utf-8"))
        if not dm:
            bad.append("FROZEN.md に STAGE-6B-DECISION の marker が無い (拒否の後に進むかの決定の記録)")
        elif dm.group(1) < rej.group(1) or dm.group(2) != "proceed":
            bad.append(f"STAGE-6B-DECISION が {dm.group(1)} {dm.group(2)} —— 拒否 ({rej.group(1)}) より後の proceed でない")
        return [f"段 6b (拒否の道): {x}" for x in bad]
    u = re.search(r"https://lists\.opensource\.org/pipermail/license-discuss_lists\.opensource\.org/(\d{4}-[A-Z][a-z]+)/\d+\.html", sec)
    if not u:
        return [f"段 6b: {m.group(1)} の投稿の公開アーカイブの URL が同じ節に無い (届いた記録が無い・ゲート 10) —— 窓は始まらない"]
    if u.group(1) != d.strftime("%Y-%B"):
        return [f"段 6b: 投稿の日 {m.group(1)} と公開アーカイブの URL の月 {u.group(1)} が合わない"]
    left = (d + datetime.timedelta(days=30) - today).days
    return [f"段 6b: {m.group(1)} に届いた版の 30 日の窓が、あと {left} 日残っている"] if left > 0 else []


def gate_6c() -> list[str]:
    """提出のゲート 6c (REVISION-PROTOCOL.md §3.6・SUBMISSION-MATERIALS §0 の 0a): 未読が 0 で、読んだ節がすべて反映されている。

    オーナーの前提 (2026-11-15)「OSI スレッドに未読が有り、未反映で本申請なんて出せないでしょ。全て読んで反映してこそ、
    出せるクオリティになるはずです。」。確定 (この道具) は提出する版を作る手順なので、満たさなければ止まる。数え方は
    Check 498 (h) と Check 501 / 501b と同じ関数。**逆側** (6c の行と同じ): census の候補の外は未読 0 に入らない。
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_dossier import BACKFILL_PENDING, backfill_table_misses, reflect_field_misses
    from census_decision_statements import candidate_rows, read_rows
    cand = {(k, d) for k, d, _t in candidate_rows(L)}
    read = {(k, d) for k, d, _t in read_rows(L)} & cand
    out = []
    if len(cand) - len(read):
        out.append(f"未読のスレッドが {len(cand) - len(read)} 本ある (候補 {len(cand)} 本のうち {len(read)} 本を読んだ)")
    _n, bad, pending = reflect_field_misses(L)
    if bad or pending:
        out.append(f"§1.242 以降の節の反映の欄が欠けるか未定: {len(bad)} 件・未定 {len(pending)} 件")
    out += archive_cache_staleness()
    _n, bad_b, missing = backfill_table_misses(L)
    if bad_b or missing or BACKFILL_PENDING:
        out.append(f"古い節の反映: 表の誤り {len(bad_b)} 件・反映の無い節 {len(missing)} 件・未定の行 {len(BACKFILL_PENDING)} 件")
    return out


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="確定の日 (YYYY-MM-DD)")
    ap.add_argument("--not-for-submission", action="store_true",
                    help="提出しない版を確定する (提出のゲート 6c を見ない・1.1〜1.3 のように作業の区切りで凍結するとき)")
    ap.add_argument("--report", metavar="VERSION", help="提出対象を切り替える日に読む行を出す (確定はしない)")
    args = ap.parse_args()
    if args.report:
        return report(args.report)
    if not args.date:
        ap.error("--date か --report が要る")
    # Check 311 は sitemap の lastmod を CI の UTC の今日と比べる。JST の 0:00〜9:00 に JST の今日で確定すると、UTC ではまだ
    #   未来の日付になり、その間の CI は 311 で赤い (2026-11-23・1.4 の確定 #3864 で踏んだ・5e と 6d の帰属)。止めはしない
    #   (確定の日はオーナーの日付で記録する) が、赤が来ることを先に知らせる
    import datetime as _dt
    utc_today = _dt.datetime.now(_dt.timezone.utc).date().isoformat()
    if args.date > utc_today:
        print(f"NOTE: --date {args.date} は UTC の今日 ({utc_today}) より先。Check 311 (sitemap の lastmod が未来) が UTC の日付が "
              f"{args.date} になるまで CI で赤い (JST では 09:00)。その後に failed job を rerun すれば消える")
    if not args.not_for_submission:
        unmet = gate_6b() + gate_6c()
        if unmet:
            print("STOP: 提出の前提を満たしていない (段 6b の 30 日・ゲート 6c「全て読んで反映してこそ」・REVISION-PROTOCOL.md §3.6):")
            print("\n".join(f"  - {x}" for x in unmet))
            print("提出しない版を作業の区切りで凍結するなら --not-for-submission を付ける")
            return 2
    draft_path = working_draft()
    v = re.match(r"ACD-(\d+\.\d+)-DRAFT\.txt$", draft_path.name).group(1)
    major, minor = v.split(".")
    nxt = f"{major}.{int(minor) + 1}"
    versions = frozen_versions()
    prev = versions[-1]
    # 付録へ写す冒頭は、草案の外の変更の一覧 (CHANGES-ACD-N.M.txt) をもとの位置へ戻した文 (2026-11-20・30 の指摘: 草案のファイル
    #   だけを読むと付録から一覧が落ち、frozen_header の "its appendix keeps … the change list" が偽になる)
    from _lib_draft_counts import with_changes
    draft = with_changes(draft_path)
    changes_path = draft_path.with_name("CHANGES-" + draft_path.name.replace("-DRAFT.txt", ".txt"))
    prev_text = (L / f"ACD-{prev}.txt").read_text(encoding="utf-8")
    header, body = draft.split(RULE, 1)
    if "Changes in this draft" not in header:
        print("STOP: 草案の冒頭にも CHANGES-ACD-N.M.txt にも変更の一覧が無い (付録に写すものが無い)")
        return 1
    (pw, pc), (w, c) = size(prev_text), size(draft)

    (L / f"ACD-{v}.txt").write_text(frozen_header(v, prev, nxt, args.date, pw, pc, w, c) + RULE + body, encoding="utf-8")
    changelist = L / f"ACD-{v}-CHANGELIST.md"
    head = changelist.read_text(encoding="utf-8").rstrip("\n")
    changelist.write_text(appendix(head, header), encoding="utf-8")
    draft_path.write_text(pointer(v, nxt, prev, args.date), encoding="utf-8")
    # 草案の「Still open」は errata の状態と照合される (Check 468) ので、文を引き継ぎ、版の列だけ足す。
    still_open = " ".join(header[header.index("Still open in this draft"):].split())
    if len(versions) >= 3:
        listed = ", ".join(versions[1:-1]) + " and " + versions[-1]
        still_open = still_open.replace(listed, ", ".join(versions[1:]) + " and " + v)
    next_body = body.replace(f"ACD-{v}", f"ACD-{nxt}").replace(f"Version {v}", f"Version {nxt}").replace(f"Dedication {v}", f"Dedication {nxt}")
    (L / f"ACD-{nxt}-DRAFT.txt").write_text(
        next_draft_header(v, nxt, f"ACD-{v}", versions + [v], w, c, still_open) + RULE + next_body, encoding="utf-8")
    # 確定した版の一覧は付録に逐語で入ったので、草案の外の一覧は次版のものに置き換える (mirror も)
    (L / f"CHANGES-ACD-{nxt}.txt").write_text(next_changes(v, nxt, w, c), encoding="utf-8")
    if changes_path.exists():
        # 消さずに pointer にする (予算表・mirror の行を残す・2026-11-20 の予行で、消すと Check 424 が開けずに traceback で止まった)
        changes_path.write_text(
            f"ACD-{v} -- CHANGES FROM ACD-{prev}. THIS LIST HAS BEEN FROZEN WITH ACD-{v}.\n\n"
            + para(f"ACD-{v} was frozen on {args.date}. This list is kept word for word in the appendix of "
                   f"LICENSES/ACD-{v}-CHANGELIST.md. The list for the next version is LICENSES/CHANGES-ACD-{nxt}.txt.") + "\n",
            encoding="utf-8")
        old_mirror = MIRROR / f"{changes_path.name}.md"
        if old_mirror.exists():
            (MIRROR / f"CHANGES-ACD-{nxt}.txt.md").write_text(
                old_mirror.read_text(encoding="utf-8").replace(f"CHANGES-ACD-{v}.txt", f"CHANGES-ACD-{nxt}.txt")
                .replace(f"ACD-{v}-DRAFT.txt", f"ACD-{nxt}-DRAFT.txt").replace(f"ACD-{v}-CHANGELIST.md", f"ACD-{nxt}-CHANGELIST.md"),
                encoding="utf-8")
    (L / f"ACD-{nxt}-CHANGELIST.md").write_text(
        f"---\nfile: LICENSES/ACD-{nxt}-CHANGELIST.md\naudience: OSI license-discuss / license-review participants, licence "
        f"reviewers, a future drafter\nlast-updated: {args.date}\ncanonical-ref: LICENSES/ACD-{nxt}-DRAFT.txt (草案) / "
        f"LICENSES/ACD-{v}.txt (直前の確定テキスト)\n---\n\n# ACD-{nxt} で変えるもの\n\nACD-{v} は {args.date} に確定・凍結した。"
        f"草案 `ACD-{nxt}-DRAFT.txt` は、下の表の変更と版番号・識別子を除いて {v} の本文である。\n\n"
        "## 表（変更が入ったらここへ足す）\n\n| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |\n| :-- | :-- | :-- | :-- | :-- |\n\n"
        "## errata 由来（`ACD-1.0.errata.md` が一次記録）\n\n"
        # 語数の内訳と記述子の候補の節を最初から置く (2026-11-23・5e の依頼): 1.5 で 5e が表の節の中に記述子の候補の表を置いて
        #   468s に、同じ行に 2 つの数を書いて 460 (x) に当たった。置き場所と書き方を雛形が先に示す
        f"## 語数の内訳（{v} → {nxt} 草案・表から集計）\n\n"
        f"<!-- 最初の変更を入れたら、ここに 3 つを書く (Check 498 (k) が実測で照らす): 「{v} の <語数> 語から {nxt} 草案は <±差> 語"
        "である（<束名>の <K> 束で <±差>）。」、別の行に「1.0 の <語数> 語から見ると <差> 語長い。」、束の表 "
        "| 束 | 増減 | 何のための語か |。主表 (## 表) の外に置く表はここより下に置く (468s は ## 表 の最初の表だけを読む) -->\n\n"
        f"## 記述子の候補（{nxt} の確定の日に `ACD-{nxt}.machine.json` へ入れるかを決める）\n\n"
        "## Constraints\n\n## Change impact\n", encoding="utf-8")
    # 次版の CHANGELIST は audience が審査者なので、入口 (REVIEWERS.md) の CHANGELIST の行に並べる。無いと Check 459c の
    #   作業中の版の ADVISORY が確定の直後に鳴る (2026-11-23・6d が 1.4 の確定 #3864 で手で足した)
    rv = L / "REVIEWERS.md"
    link = f"[`ACD-{v}-CHANGELIST.md`](ACD-{v}-CHANGELIST.md)"
    if rv.exists() and f"ACD-{nxt}-CHANGELIST.md" not in rv.read_text(encoding="utf-8"):
        rv.write_text(rv.read_text(encoding="utf-8").replace(f"{link} |", f"{link} / [`ACD-{nxt}-CHANGELIST.md`](ACD-{nxt}-CHANGELIST.md) |", 1),
                      encoding="utf-8")
    (L / f"ACD-{v}.machine.json").write_text(descriptor(v, prev, body, args.date), encoding="utf-8")

    old = re.search(r"^SPDX-License-Identifier: (ACD-\d+\.\d+)$", (ROOT / "LICENSE").read_text(encoding="utf-8"), re.M).group(1)
    old_date = re.search(r"frozen on (\d{4}-\d{2}-\d{2})", " ".join((L / f"{old}-DRAFT.txt").read_text(encoding="utf-8").split())).group(1)
    for f in APPLY_FILES:
        p = ROOT / f
        p.write_text(bump_applied(p.read_text(encoding="utf-8"), old, f"ACD-{v}", old_date, args.date), encoding="utf-8")
    for f in ("LICENSE", "llms-full.txt"):
        (ROOT / f).write_text(record_history((ROOT / f).read_text(encoding="utf-8"), old, args.date), encoding="utf-8")
    lic = (ROOT / "LICENSE").read_text(encoding="utf-8")
    start = lic.index(f"Until {args.date} this repository")
    end = lic.index("\n\n", start)
    history = re.sub(r"Everything ACD-\d+\.\d+ gave away", "Everything those versions gave away", " ".join(lic[start:end].split()))
    history = re.sub(r"\(ACD-\d+\.\d+ §2\.2\)", "(§2.2 of each)", history)
    (ROOT / "LICENSE").write_text(lic[:start] + textwrap.fill(history, width=78) + lic[end:], encoding="utf-8")
    subprocess.run([sys.executable, ".github/scripts/update_binary_aio_rights.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, ".github/scripts/generate_spdx_license_xml.py", "--version", v], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    frozen = L / "FROZEN.md"
    lines = frozen.read_text(encoding="utf-8").split("\n")
    idx = max(k for k, line in enumerate(lines) if re.match(r"^[0-9a-f]{64}  LICENSES/", line))
    pins = [f"{hashlib.sha256((L / n).read_bytes()).hexdigest()}  LICENSES/{n}"
            for n in (f"ACD-{v}.txt", f"ACD-{v}.machine.json", f"ACD-{v}.spdx.xml") if (L / n).exists()]
    lines[idx + 1:idx + 1] = pins
    frozen.write_text("\n".join(lines), encoding="utf-8")

    for new, src in ((f"ACD-{v}.txt", f"ACD-{prev}.txt"), (f"ACD-{v}.machine.json", f"ACD-{prev}.machine.json"),
                     (f"ACD-{v}.spdx.xml", "ACD-1.0.spdx.xml"),
                     (f"ACD-{nxt}-DRAFT.txt", f"ACD-{v}-DRAFT.txt"), (f"ACD-{nxt}-CHANGELIST.md", f"ACD-{v}-CHANGELIST.md")):
        text = (MIRROR / f"{src}.md").read_text(encoding="utf-8").replace(src, new)
        (MIRROR / f"{new}.md").write_text(text.replace(f"ACD-{v}-DRAFT.txt", f"ACD-{nxt}-DRAFT.txt"), encoding="utf-8")
    index = L / "README.md"
    rows = index.read_text(encoding="utf-8").replace(f"[`ACD-{v}-DRAFT.txt`](ACD-{v}-DRAFT.txt) |", f"[`ACD-{nxt}-DRAFT.txt`](ACD-{nxt}-DRAFT.txt) |", 1)
    row = f"| **次版に反映するものの集約点（{v}）** | [`ACD-{v}-CHANGELIST.md`](ACD-{v}-CHANGELIST.md) |\n"
    if row in rows:
        rows = rows.replace(row, f"| **次版に反映するものの集約点（{nxt}）** | [`ACD-{nxt}-CHANGELIST.md`](ACD-{nxt}-CHANGELIST.md) |\n"
                            f"| {v} の変更の記録 | [`ACD-{v}-CHANGELIST.md`](ACD-{v}-CHANGELIST.md) |\n", 1)
    index.write_text(rows, encoding="utf-8")
    finish(v, prev, nxt, args.date, c)
    print(f"ACD-{v} を確定した ({w:,} 語・{c} 条)。次の草案は ACD-{nxt}-DRAFT.txt。git add のあと consistency の RED を順に直す。")
    print(f"提出対象を切り替える日に読む行は `prepare_version_freeze.py --report {v}` が出す。")
    # 道具が直さず、確定の日に人が直す RED (2026-11-16 の予行で実測・main の上で 1.4 を確定して consistency を回した)。
    #   道具が直せないのは、どちらも「どの版の数・どの版の適用か」を言い直す判断だから (書き換えの向きが 1 つに決まらない)
    print(f"確定の日に人が直す RED (2026-11-16 の予行で出たもの): "
          f"(1) Check 460 (x) —— B3 の見出しと SUBMISSION-MATERIALS の長さの行は「{v} 草案は」の形で書かれ、作業中の草案が "
          f"{nxt} になると 1 つも読めなくなる。「{v} 草案は」を「確定した ACD-{v} は」へ書き直す (50 の決め・460 (x) はこの形を "
          f"凍結した ACD-{v}.txt で測る)。{nxt} 草案の長さの行は、{nxt} 草案が変わるまで作らない。"
          f"(2) Check 444m —— 入口の FAQ・準備した答え・submission-osd・submission-reference が「適用している」と述べる版を、"
          f"ACD-{v} を適用した事実に合わせる (道具は機械の面だけを直す)。"
          "(3) Check 362 —— 下の mutation を退役させる。(4) Check 311 は --date が UTC の今日より先だと sitemap の lastmod で鳴る (JST の 0:00〜9:00 の確定では、UTC の日付が追いつくまで赤い。その後に rerun する)。")
    orphan_mutations()
    return 0


def orphan_mutations() -> None:
    """確定したあと、anchor が見つからなくなった mutation の名前を出す (退役させる候補・2026-11-15 の試走から)。

    作業中の CHANGELIST の中身を打つ mutation (468x・498 (j) など) は、新しい CHANGELIST が空なので的を外す。確定した版の
    CHANGELIST を読む Check は無いので、付け替えずに退役させる。mutation_samples は別の process で読み直す (この process は
    確定の前の CURRENT_DRAFT を import していないが、念のため子 process で数える)。
    """
    code = ("import mutation_samples as m\n"
            "for x in m.MUTATIONS + m.E2E_MUTATIONS:\n"
            "    t = x['file'].read_text(encoding='utf-8') if x['file'].exists() else ''\n"
            "    print(x['name'][:100]) if x['find'] not in t else None\n")
    r = subprocess.run([sys.executable, "-c", code], cwd=Path(__file__).resolve().parent, text=True, capture_output=True)
    names = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if names:
        print(f"anchor が見つからなくなった mutation {len(names)} 件 (退役させる候補・Check 362 が RED にする)。"
              "退役させた Check の面に mutation が残るか (Check 479c / 479d) も確かめる:")
        for n in names:
            print(f"  - {n}")


if __name__ == "__main__":
    raise SystemExit(main())
