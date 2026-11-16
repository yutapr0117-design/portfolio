#!/usr/bin/env python3
"""list_open_items.py — ACD の OSI 承認に向けて「開いている項目」を、ドシエ全体から 1 つの一覧に集める (洗い出しの道具)。

**なぜ在るか (2026-11-16・オーナーの依頼)**: 「5 人全員に全委任しているので、ACD の OSI 承認に向けての全ての改善項目を
洗い出し尽くした上で行い続けて」。開いている項目は register・errata・B の表・確定のゲート・AS-OF・ADVISORY に散らばっており、
人が文書ごとに拾うと漏れる。拾い方を 1 つの道具に置き、5 人で分ける一覧にする。

**集めるもの** (どれも現物から導く。件数を宣言しない):
  1. register (against.md / against-2.md) の行のうち状態が CLOSED でも TRADE (受け入れた費用) でもないもの。
     TEXT / DOSSIER / OPEN / UNTRIAGED は我々が手を打てる、EXTERNAL は外部 (OSI・オーナー・法律家) に依る。
  2. errata のうち、どの版でも閉じた印の無いもの (prepare_version_freeze.errata_closures の unmarked)。
  3. B の表 (ACD-OSI-BOTTLENECKS.md の英語の表) のうち、状態が Decided / Checked and kept でないもの。
  4. 確定のゲート (gate_6b・gate_6c) の満たしていない条件。
  5. AS-OF の「答えていない問い」の件数。
  6. 合成の文書 (READINGS-SYNTHESIS.md) の §6「本申請の前に残っていること」の番号つきの項目 (2f の合成・読みの側の残り)。
  7. --advisory を付けると、consistency を回して ADVISORY の警告を足す (重い・約 2 分)。
**担当の候補** は、本文 = 1c、register と B = 30、入口と手順 = 50、未読と合成 = 2f、機械層 = 9b の割り振りから付ける (目安)。

**集めないもの (重要)**: 「改善の余地」そのもの。ここに載るのは、ドシエが自分で「開いている」と書いた項目と、道具が
数えられる欠けだけである。誰も書いていない欠陥は載らない —— 洗い出しの残りは、読み・反例・模擬委員会が見つける。

使い方:
    python3 .github/scripts/list_open_items.py              # 一覧 (markdown)
    python3 .github/scripts/list_open_items.py --advisory   # ADVISORY の警告も足す
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib_dossier import against_text  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"
OURS = {"TEXT": "1c", "DOSSIER": "30", "OPEN": "30", "UNTRIAGED": "30"}


def register_items() -> tuple[list[tuple[str, str, str, str]], list[tuple[str, str, str, str]]]:
    ours, external = [], []
    for line in against_text(L).splitlines():
        m = re.match(r"^\| (\d+) \|\s*(.*)$", line)
        if not m:
            continue
        st = re.findall(r"\*\*\[([A-Z]+)\]\*\*", line)
        state = st[0] if st else "NONE"
        if state in ("CLOSED", "TRADE"):
            continue
        title = re.sub(r"\*\*", "", m.group(2).split("|")[0]).strip()
        item = (f"against #{m.group(1)}", state, title[:110], OURS.get(state, "30"))
        (external if state == "EXTERNAL" else ours).append(item)
    return ours, external


def errata_items() -> list[tuple[str, str, str, str]]:
    from prepare_version_freeze import errata_closures
    _t, _c, unmarked, _s = errata_closures()
    text = (L / "ACD-1.0.errata.md").read_text(encoding="utf-8")
    out = []
    for e in unmarked:
        m = re.search(rf"^\| {e} \|\s*([^|]*)\|", text, re.M)
        out.append((f"errata {e}", "未閉", re.sub(r"\*\*", "", m.group(1)).strip()[:110] if m else "", "1c"))
    return out


def b_items() -> list[tuple[str, str, str, str]]:
    out = []
    for line in (L / "ACD-OSI-BOTTLENECKS.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (B\d+) \| ([^|]+)\| ([^|]+)\| ([^|]+)\|", line)
        if m and not re.search(r"Decided|Checked and kept", m.group(4)):
            out.append((m.group(1), m.group(3).strip(), f"{m.group(2).strip()} —— {m.group(4).strip()}"[:110], "30"))
    return out


def gate_items() -> list[tuple[str, str, str, str]]:
    import prepare_version_freeze as p
    return [("gate_6b", "未充足", x[:110], "50") for x in p.gate_6b()] + [("gate_6c", "未充足", x[:110], "2f") for x in p.gate_6c()]


def asof_items() -> list[tuple[str, str, str, str]]:
    m = re.search(r"\*\*答えていない問い\*\*[^|]*\|[^|]*\| \*\*(\d+) 件\*\*", (L / "AS-OF.md").read_text(encoding="utf-8"))
    return [("答えていない問い", "未回答", f"{m.group(1)} 件 (AS-OF)", "オーナー (B14) / 材料は 50")] if m and m.group(1) != "0" else []


def synthesis_items() -> list[tuple[str, str, str, str]]:
    p = L / "READINGS-SYNTHESIS.md"
    if not p.exists():
        return []
    m = re.search(r"^## 6\..*?(?=^## \d|\Z)", p.read_text(encoding="utf-8"), re.M | re.S)
    out = []
    for n, head, rest in re.findall(r"^(\d+)\. \*\*(.+?)\*\*[:：]?\s*(.*)$", m.group(0) if m else "", re.M):
        who = re.findall(r"portfolio-(\w\w)", rest)
        out.append((f"合成 §6 の {n}", "残り", f"{head} —— {rest}"[:110], who[0] if who else "2f"))
    return out


def advisory_items() -> list[tuple[str, str, str, str]]:
    r = subprocess.run([sys.executable, str(ROOT / ".github/scripts/check_repository_consistency.py")], cwd=ROOT,
                       capture_output=True, text=True)
    seen, out = set(), []
    for ln in r.stdout.splitlines():
        m = re.match(r"\s*::warning::(Check [\w ()]+?)(?: \(ADVISORY\))?: (.*)$", ln)
        if m and m.group(2) not in seen:
            seen.add(m.group(2))
            out.append((m.group(1), "ADVISORY", m.group(2)[:110], "9b"))
    return out


def table(title: str, rows: list[tuple[str, str, str, str]]) -> None:
    print(f"\n## {title}（{len(rows)} 件）\n")
    if not rows:
        print("なし")
        return
    print("| 項目 | 状態 | 内容 | 担当の候補 |\n| :-- | :-- | :-- | :-- |")
    for r in rows:
        print("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    ours, external = register_items()
    groups = [("我々が手を打てる register の行（TEXT・DOSSIER・OPEN・UNTRIAGED）", ours),
              ("閉じていない errata", errata_items()), ("決着していない B", b_items()),
              ("確定のゲートの満たしていない条件", gate_items()), ("答えていない問い", asof_items()),
              ("合成の文書 §6 の残り（読みの側）", synthesis_items())]
    if "--advisory" in argv:
        groups.append(("ADVISORY の警告", advisory_items()))
    groups.append(("外部に依る register の行（EXTERNAL・我々の側でできることは行の「潰し方」に在る）", external))
    print("# ACD の開いている項目（list_open_items.py の出力・現物から導いた数）")
    print("\n" + " / ".join(f"{t.split('（')[0]} {len(r)}" for t, r in groups))
    for t, r in groups:
        table(t, r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
