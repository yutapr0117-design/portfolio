"""_lib_dossier.py — ドシエの不利な事実の register (against) を読む場所を 1 か所にする。

against.md はバイトの予算 (Check 495) に近づいており、BLOCKING の手前で #N の番号を続けたまま 2 つ目の file へ分ける
(portfolio-00 と portfolio-9b の合意・2026-11-12)。その日に読み手を何か所も直さずに済むよう、file の一覧をここだけに置く。
分けた日は AGAINST_FILES に 2 つ目の file 名を足す (番号の範囲は file の順)。
"""
import re
from pathlib import Path

AGAINST_FILES = ("ACD-1.0.against.md",)


def against_paths(licenses_dir: Path) -> list[Path]:
    """register の file を順に (在るものだけ)。"""
    return [licenses_dir / n for n in AGAINST_FILES if (licenses_dir / n).exists()]


def against_text(licenses_dir: Path) -> str:
    """register の全 file の本文をつないだもの (無ければ空)。"""
    return "\n".join(p.read_text(encoding="utf-8") for p in against_paths(licenses_dir))


def is_against(name: str) -> bool:
    """file 名が register の file か。"""
    return name in AGAINST_FILES


# ── 草案の逐語の照合 (Check 468w / 468a が使う) ──────────────────────────────────────
def _parts(quote: str, minlen: int) -> list[str]:
    q = " ".join(quote.replace('\\"', '"').split())
    return [p for p in (" ".join(x.split()).strip(" ,;.:") for x in re.split(r"…|\.\.\.", q)) if len(p) > minlen]


def errata_draft_quote_misses(licenses_dir: Path, working_draft: Path) -> tuple[int, list[str]]:
    """468w: errata の各行が「N.M draft」として引く逐語が、その版の本文 (作業中ならその草案・凍結済みなら凍結した本文) に在るか。
    "draft" の後 200 字以内の最初の *"…"* を取り、"…" で切った 15 字を超える断片がすべて在ること。"as adopted"・行番号・
    "earlier version" の説明は除く (2026-11-11 に checks_license_draft.py で作り、2026-11-12 にここへ移した)。"""
    texts, n, miss = {}, 0, []
    for line in (licenses_dir / "ACD-1.0.errata.md").read_text(encoding="utf-8").split("\n"):
        me = re.match(r"^\|\s*\*{0,2}(E\d+)", line)
        if not me:
            continue
        for m in re.finditer(r"(?<![\d.])(\d+\.\d+) draft", line):
            v, tail = m.group(1), line[m.end():m.end() + 200]
            if re.match(r"\s*as adopted|\s*lines?\s+\d", tail) or "earlier version" in tail[:60] or '*"' not in tail:
                continue
            q = re.match(r'\*"(.+?)"\*', line[m.end() + tail.index('*"'):])
            if not q:
                continue
            if v not in texts:
                d, f = licenses_dir / f"ACD-{v}-DRAFT.txt", licenses_dir / f"ACD-{v}.txt"
                src = d if d == working_draft else f if f.exists() else None
                texts[v] = " ".join(src.read_text(encoding="utf-8").split()) if src else None
            n += 1
            lack = [x for x in _parts(q.group(1), 15) if texts[v] is None or x not in texts[v]]
            if lack:
                miss.append(f"{me.group(1)} ({v} draft): {lack[0][:60]!r}")
    return n, miss


_PAST_468A = re.compile(r"as adopted on|の前の形|T\d+ の前|旧い|旧文|\bwas\b|だった|外した|外れ|より前|earlier|formerly|used to|no longer")
_SKIP_468A = re.compile(r"CHANGELIST|TRIAL|SELF-AUDIT|ADVERSARIAL|RESEARCH-RECORDS|errata|BLIND-SPOTS|AUDIT-LEDGER|discussion-log")


def dossier_draft_quote_misses(licenses_dir: Path, version: str, draft_text: str) -> tuple[int, list[str]]:
    """468a: ドシエ (作業記録と errata を除く LICENSES/*.md) が「N.M draft / N.M 草案 / N.M の草案」の後 80 字以内に引く
    逐語が、いまの草案に在るか (2026-11-12・portfolio-00 の提案: 日付つきの注記が後の試作で古くなる)。前後に過去の形の印が
    あれば除き、草案の語と引用の間に「氏」があれば審査者の文として除く。"…" で切った 8 字を超える断片を当てる。"""
    flat_draft = " ".join(draft_text.split())
    n, miss = 0, []
    for f in sorted(licenses_dir.glob("*.md")):
        if _SKIP_468A.search(f.name):
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            for m in re.finditer(re.escape(version) + r" (?:draft|草案|の草案)", line):
                tail = line[m.end():m.end() + 80]
                qm = re.search(r'\*"(.{12,}?)"\*', tail)
                if not qm or '*"' in tail[:qm.start()] or "氏" in tail[:qm.start()]:
                    continue
                n += 1
                if all(p in flat_draft for p in _parts(qm.group(1), 8)):
                    continue
                if not _PAST_468A.search(line[max(0, m.start() - 200):m.end() + 300]):
                    miss.append(f"{f.name}:{i} {qm.group(1)[:50]!r}")
    return n, miss
