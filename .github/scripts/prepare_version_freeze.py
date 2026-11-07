#!/usr/bin/env python3
"""作業中の草案を確定する機械的な作業を、1 回で行う (手で回す道具・CI では走らせない)。

    python3 .github/scripts/prepare_version_freeze.py --date 2026-11-13

確定の日の手作業は約 50 file に及ぶ。2026-11-06 に使い捨ての worktree で 1.4 を確定して測ると、手作業の誤りの
多くが無音だった (Check 490 / 468v / 442d / 444k / 472h で閉じた)。この道具はその手順の機械的な部分を行う。

やること: 確定本文 (冒頭は §0.13 の型) / 草案の pointer / 次の草案 / 次の CHANGELIST / 記述子 / FREEZE-DATA /
mirror / 適用する面の版 / binary の権利表示 / SPDX XML。草案の冒頭は CHANGELIST の付録へ逐語で移す。

やらないこと: 判断。外向きの文書の書き換え、REVIEWERS.md の表、語数の申告の文、`measure_descriptor_carryover.py`
が出す条の読み直しは人が行う。走ったあとの consistency の RED が、次に直す場所の一覧である。

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
               "js/components.js", "llms-full.txt", "llms.txt", "llms_well-known.txt", "main.js", "robots.txt", "sitemap.xml")


def bump_applied(text: str, old: str, new: str, old_date: str, date: str) -> str:
    """適用する版を上げる。版を述べる行の適用の日付も一緒に直す (版だけ置換すると公開面が偽の日付を述べる)。"""
    lines = []
    for line in text.split("\n"):
        if old in line or f"Dedication {old[4:]}" in line:
            line = line.replace(old, new).replace(f"Dedication {old[4:]}", f"Dedication {new[4:]}")
            line = re.sub(r"\(ACD-\d+\.\d+ until \d{4}-\d{2}-\d{2}\)", f"({old} until {date})", line)
            line = re.sub(r"\d{4}-\d{2}-\d{2} までは ACD-\d+\.\d+", f"{date} までは {old}", line)
            line = line.replace(f"since {old_date}", f"since {date}").replace(f"{old_date} から", f"{date} から")
        lines.append(line)
    out = "\n".join(lines)
    # sitemap の lastmod は版を述べる <loc> の次の行にある。
    return re.sub(rf"({re.escape(new)}\.[a-z.]+</loc>\n\s*<lastmod>){re.escape(old_date)}", rf"\g<1>{date}", out)


def para(text: str, indent: str = "  ", first: str | None = None) -> str:
    return textwrap.fill(" ".join(text.split()), width=78, initial_indent=first if first is not None else indent,
                         subsequent_indent=indent, break_long_words=False, break_on_hyphens=False)


def bullet(text: str) -> str:
    return para(text, indent="      ", first="    * ")


def size(text: str) -> tuple[int, int]:
    body = text.split(RULE, 1)[1] if RULE in text else text
    return len(body.split()), len(set(re.findall(r"^  (\d+\.\d+) ", body, re.M)))


def frozen_versions() -> list[str]:
    found = [re.match(r"ACD-(\d+\.\d+)\.txt$", p.name) for p in L.glob("ACD-*.txt")]
    return sorted((m.group(1) for m in found if m), key=lambda v: tuple(map(int, v.split("."))))


def working_draft() -> Path:
    cands = [p for p in sorted(L.glob("ACD-*-DRAFT.txt"))
             if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    if len(cands) != 1:
        sys.exit(f"作業中の草案が 1 つに定まらない: {[p.name for p in cands]}")
    return cands[0]


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
                   f"LICENSES/ACD-{v}-CHANGELIST.md, which also keeps, word for word, the change list this file carried "
                   "while it was a draft."),
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
        "  Status of this draft, stated plainly so that nobody has to infer it:",
        "\n".join([
            bullet(f"It has had no legal review, like {plain}."),
            bullet("It has not been posted to any list."),
            bullet(f"It is at present identical to ACD-{v} apart from the version number and the identifiers that name it. "
                   "An empty change list below means nothing has been changed yet -- not that the record is missing; a list "
                   "with entries in it is the whole of the difference."),
            bullet(f"Clause numbers follow ACD-{v}, not ACD-1.0. Citations to an earlier version must keep using that "
                   "version's text."),
            bullet(f"Changes are recorded in LICENSES/ACD-{nxt}-CHANGELIST.md."),
        ]),
        f"  Changes in this draft, relative to ACD-{v}:",
        bullet(f"ACD-{v}: {w} words, {c} clauses. This draft: {w} words, {c} clauses."),
        para(still_open),
        "",
    ])


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
        d["reservationsAndLimits"]["textRedistribution"]["note"] = (
            "The text of this Dedication may be copied and distributed verbatim by anyone. What is restricted is distributing "
            "a MODIFIED text under the name \"Autonomous Commons Dedication\" or under any identifier that begins with \"ACD-\" "
            "followed by a digit, except by the Steward (section 16.5), and by the Steward only as a new version under a version "
            "number and identifier that no earlier text, other than a draft identified as such, has borne. A modified text may be "
            "distributed under a different name. A translation identified as one that states that the English text prevails, and "
            "a re-encoding with the words unchanged that is identified as one, are not modified texts for this purpose. This "
            "restriction concerns the text of this Dedication as a document; it is not a condition upon any use of the Work "
            "(sections 10.5 and 16.6).")
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
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="確定の日 (YYYY-MM-DD)")
    ap.add_argument("--report", metavar="VERSION", help="提出対象を切り替える日に読む行を出す (確定はしない)")
    args = ap.parse_args()
    if args.report:
        return report(args.report)
    if not args.date:
        ap.error("--date か --report が要る")
    draft_path = working_draft()
    v = re.match(r"ACD-(\d+\.\d+)-DRAFT\.txt$", draft_path.name).group(1)
    major, minor = v.split(".")
    nxt = f"{major}.{int(minor) + 1}"
    versions = frozen_versions()
    prev = versions[-1]
    draft = draft_path.read_text(encoding="utf-8")
    prev_text = (L / f"ACD-{prev}.txt").read_text(encoding="utf-8")
    header, body = draft.split(RULE, 1)
    (pw, pc), (w, c) = size(prev_text), size(draft)

    (L / f"ACD-{v}.txt").write_text(frozen_header(v, prev, nxt, args.date, pw, pc, w, c) + RULE + body, encoding="utf-8")
    changelist = L / f"ACD-{v}-CHANGELIST.md"
    head = changelist.read_text(encoding="utf-8").rstrip("\n")
    changelist.write_text(f"{head}\n\n## 付録: 確定時点の草案ヘッダ（逐語）\n\n```\n{header.rstrip()}\n```\n", encoding="utf-8")
    draft_path.write_text(pointer(v, nxt, prev, args.date), encoding="utf-8")
    # 草案の「Still open」は errata の状態と照合される (Check 468) ので、文を引き継ぎ、版の列だけ足す。
    still_open = " ".join(header[header.index("Still open in this draft"):].split())
    if len(versions) >= 3:
        listed = ", ".join(versions[1:-1]) + " and " + versions[-1]
        still_open = still_open.replace(listed, ", ".join(versions[1:]) + " and " + v)
    next_body = body.replace(f"ACD-{v}", f"ACD-{nxt}").replace(f"Version {v}", f"Version {nxt}").replace(f"Dedication {v}", f"Dedication {nxt}")
    (L / f"ACD-{nxt}-DRAFT.txt").write_text(
        next_draft_header(v, nxt, f"ACD-{v}", versions + [v], w, c, still_open) + RULE + next_body, encoding="utf-8")
    (L / f"ACD-{nxt}-CHANGELIST.md").write_text(
        f"---\nfile: LICENSES/ACD-{nxt}-CHANGELIST.md\naudience: OSI license-discuss / license-review participants, licence "
        f"reviewers, a future drafter\nlast-updated: {args.date}\ncanonical-ref: LICENSES/ACD-{nxt}-DRAFT.txt (草案) / "
        f"LICENSES/ACD-{v}.txt (直前の確定テキスト)\n---\n\n# ACD-{nxt} で変えるもの\n\nACD-{v} は {args.date} に確定・凍結した。"
        f"草案 `ACD-{nxt}-DRAFT.txt` は、下の表の変更と版番号・識別子を除いて {v} の本文である。\n\n"
        "## 表（変更が入ったらここへ足す）\n\n| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |\n| :-- | :-- | :-- | :-- | :-- |\n\n"
        "## errata 由来（`ACD-1.0.errata.md` が一次記録）\n\n## Constraints\n\n## Change impact\n", encoding="utf-8")
    (L / f"ACD-{v}.machine.json").write_text(descriptor(v, prev, body, args.date), encoding="utf-8")

    old = re.search(r"^SPDX-License-Identifier: (ACD-\d+\.\d+)$", (ROOT / "LICENSE").read_text(encoding="utf-8"), re.M).group(1)
    old_date = re.search(r"frozen on (\d{4}-\d{2}-\d{2})", " ".join((L / f"{old}-DRAFT.txt").read_text(encoding="utf-8").split())).group(1)
    for f in APPLY_FILES:
        p = ROOT / f
        p.write_text(bump_applied(p.read_text(encoding="utf-8"), old, f"ACD-{v}", old_date, args.date), encoding="utf-8")
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
    subprocess.run([sys.executable, ".github/scripts/sync_size_table.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    print(f"ACD-{v} を確定した ({w:,} 語・{c} 条)。次の草案は ACD-{nxt}-DRAFT.txt。git add のあと consistency の RED を順に直す。")
    print(f"提出対象を切り替える日に読む行は `prepare_version_freeze.py --report {v}` が出す。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
