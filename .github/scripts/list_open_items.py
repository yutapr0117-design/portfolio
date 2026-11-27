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
  7. オーナーにしかできない行為の表 (OSI-APPROVAL-PLAN.md・30 の依頼)。
  8. 法律家と実務家への問い (QUESTIONS-FOR-COUNSEL / -PRACTITIONERS の `## N.` の節・どれも未回答)。
  9. register の行のうち「**合否の状態（日付）**: 無い / まだ」と書いた行 (合否の基準を書いて、まだ満たしていない・30 の依頼)。
  10. SELF-AUDIT の 🔴 の項で「**1.4 草案で閉じた（…）**」の印の無いもの (「**起草では閉じない**」は起草の外として別の状態)、
     試作の文書の「先に登録する反例」で「**反例の結果**」の段の無いもの (印の語は 1c が決めた・2026-11-16)。
  11. --advisory を付けると、consistency を回して ADVISORY の警告を足す (重い・約 2 分)。
**担当の候補** は役の名で出す (目安): 本文・ドシエ (register と B と反例)・統合 (入口と手順)・採掘 (未読と合成)・機械層。
内部の割り振りは 2026-11-15 の 5 人のセッションの名 (本文 = 1c、ドシエ = 30、統合 = 50、採掘 = 2f、機械層 = 9b) で書かれているが、
セッションの名はセッションが替わるたびに古くなるので、表に出す所 (table) で担当の欄だけを役の名へ読み替える (2026-11-27・7e の依頼)。

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
    # 作業中の版の CHANGELIST の「N.M から持ち越したもの」が名指す against の番号は、確定の日に (記述子など) 閉じるもので、
    #   いま手を打てる作業ではない (2026-11-20・30: #269 は 1.4 の記述子に §9 のキーを足すだけで、Check 451e が強制済み)
    carried = set()
    for cl in sorted(L.glob("ACD-1.*-CHANGELIST.md"))[-1:]:
        sec = re.search(r"^## \d+\.\d+ から持ち越したもの\n(.*?)(?=^## |\Z)", cl.read_text(encoding="utf-8"), re.M | re.S)
        carried = set(re.findall(r"against\.md`?\s*#(\d+)", sec.group(1))) if sec else set()
    for line in against_text(L).splitlines():
        m = re.match(r"^\| (\d+) \|\s*(.*)$", line)
        if not m:
            continue
        st = re.findall(r"\*\*\[([A-Z]+)\]\*\*", line)
        state = st[0] if st else "NONE"
        if state in ("CLOSED", "TRADE"):
            continue
        title = re.sub(r"\*\*", "", m.group(2).split("|")[0]).strip()
        item = (f"against #{m.group(1)}", f"{state}・確定の日に閉じる（待ち）" if m.group(1) in carried else state, title[:110],
                OURS.get(state, "30"))
        (external if state == "EXTERNAL" else ours).append(item)
    return ours, external


def errata_items() -> list[tuple[str, str, str, str]]:
    """閉じた印の無い errata。草案の冒頭の "Still open in this draft: E6 (…) and E10 (…)" の括弧を読み、種類を分ける
    (1c の依頼・2026-11-16: E6 は検証して狭めないと決めた問い、E10 は版ごとの記述子で確定の日に閉じ直すもの —— 一律に「未閉」と
    出すと、閉じ忘れと誤読される)。宣言に無い E は「未閉 (宣言なし)」で、Check 468 が宣言と errata を照らす。"""
    from prepare_version_freeze import RULE, errata_closures, working_draft
    _t, _c, unmarked, _s = errata_closures()
    text = (L / "ACD-1.0.errata.md").read_text(encoding="utf-8")
    from _lib_draft_counts import with_changes
    head = " ".join(with_changes(working_draft()).split(RULE, 1)[0].split())
    still = head[head.find("Still open in this draft"):]
    out = []
    for e in unmarked:
        m = re.search(rf"^\| {e} \|\s*([^|]*)\|", text, re.M)
        why = re.search(rf"\b{e} \(([^()]*)\)", still)
        if not why:
            kind = "未閉（草案の宣言なし）"
        elif re.search(r"descriptor|each new version|closed again", why.group(1)):
            kind = "開いている（確定の日に閉じる）"
        elif re.search(r"not narrowed|deliberately|examined", why.group(1)):
            kind = "開いている（問いとして残す）"
        else:
            kind = "開いている"
        title = re.sub(r"\*\*", "", m.group(1)).strip() if m else ""
        out.append((f"errata {e}", kind, f"{title} —— {why.group(1) if why else ''}"[:110], "1c"))
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


def owner_items() -> list[tuple[str, str, str, str]]:
    t = (L / "OSI-APPROVAL-PLAN.md").read_text(encoding="utf-8")
    m = re.search(r"オーナーにしかできない行為の一覧.*?\n(\|.*?)(?:\n\n|\Z)", t, re.S)
    out = []
    for row in (m.group(1).splitlines() if m else []):
        c = [x.strip() for x in row.strip("|").split("|")]
        if len(c) >= 3 and c[0].isdigit():
            out.append((f"オーナーの行為 {c[0]}", f"段 {c[2]}", c[1][:110], "オーナー (B14) / 材料は 50"))
    return out


def question_items() -> list[tuple[str, str, str, str]]:
    out = []
    for name in ("QUESTIONS-FOR-COUNSEL.md", "QUESTIONS-FOR-PRACTITIONERS.md"):
        p = L / name
        for n, title in re.findall(r"^## (\d+)\. (.*)$", p.read_text(encoding="utf-8") if p.exists() else "", re.M):
            out.append((f"{name.split('.')[0]} {n}", "未回答", title[:110], "オーナー (B1) / 材料は 30"))
    return out


def legal_uncertainty_items() -> list[tuple[str, str, str, str]]:
    """法的解釈の不確実性の台帳から、手を打てる行 (2026-11-16・オーナーの依頼の 9b の持ち分・50 の「list_open_items の拡張」):
    ② (語で消せる) のうち試作でまだ閉じていない第 18 節の行と、③ なのに行き先 (問い / jurisdictions / 法律家) の無い行。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import measure_legal_uncertainty as mlu
    mlu.count()
    out = [(x.split("（")[0], "③ の行き先なし", "問い N / jurisdictions / 法律家 のどこへ運ぶかを分類の欄に書く", "その帯の人")
           for x in mlu.NO_DEST]
    third = L / "ACD-1.4-THIRD-CLARITY-TRIAL.md"
    t = third.read_text(encoding="utf-8") if third.exists() else ""
    s18 = re.search(r"^## (?:§)?18[ .].*?(?=^## (?:§)?\d+[ .]|\Z)", t, re.M | re.S)
    for line in (s18.group(0) if s18 else "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("| §") else []
        if len(cells) >= 3 and (m := re.search(r"[①②③]", cells[-1])) and m.group(0) == "②" \
                and not re.search(r"T\d+(?:〜T\d+)?\s*で入った|本文で消えた|rounds/", line):
            out.append((cells[0][:40], "② 未着手", cells[-1][:100], "1c (試作)"))
        mm = mlu.ROW.match(line)
        if mm and mm.group(3) == "②" and mm.group(4) not in ("本文で消えた",):
            out.append((f"§{mm.group(1)}", "② 未着手", mm.group(2)[:100], "1c (試作)"))
    # §19 (本文の語の割れ・2026-11-18): 開いている試作と、形の足りない行
    f19 = sorted(L.glob("ACD-1.*-UNIQUE-READING.md"))  # §19 は 2026-11-18 に THIRD から移した
    for m in mlu.ROW19.finditer(f19[-1].read_text(encoding="utf-8") if f19 else ""):
        if m.group(3) == "試作" and not re.search(r"で入った|退けた", m.group(4) + m.group(5)):
            out.append((f"§{m.group(1)}", "§19 試作で開いている", m.group(2)[:100], "1c (試作)・30 (反例)"))
    for x in mlu.section19()[1]:
        out.append((x.split(":")[0], "§19 形が足りない", x.split(": ", 1)[-1], "その帯の人"))
    # §18 に残る「未取得」の法源と、どの条にも当たっていない法令の写し (2026-11-20・法令の一次資料を 5 人で読む分担)
    import measure_law_coverage as mlc
    band = {k: w for a, b, w in mlu.BAND for k in range(a, b + 1)}
    for c, line in mlc.s18_rows():
        for mu in re.finditer(r"[^（(、。；|]{0,40}未取得", line):
            u = mu.group(0)
            # 取った後の行が「取得経路が閉じている（403 など）」と書いていれば、手を打てる行でなく経路待ちとして出す (2026-11-20・30 と
            #   9b: BAILII・parliament.uk が 403 の英国の判決)。読み手が「残りの作業」と取り違えないため
            after = line[mu.end():mu.end() + 60]
            closed = re.search(r"取得経路|403|404", after)
            out.append((f"§{c}", "§18 法源の取得経路が閉じている（待ち）" if closed else "§18 法源が未取得", u.strip(" ・（(")[:100],
                        f"{band.get(int(c.split('.')[0]), '?')} (取得は add_law_snapshot.py)"))
    for s, c in mlc.unapplied():
        out.append((f"§{c}", "法令の写しを取ったが、その条の読みに当てていない", s[:60],
                    f"{band.get(int(c.split('.')[0]), '?')} (§18 の行か jurisdictions の段か §19 の行に写しの名を書いて読む)"))
    # §19 の行・問い・逐条リファレンスが、試作で変わる前の草案の文を引いたまま (Check 470 の ADVISORY と同じ数え方・2026-11-20)
    from _lib_draft_counts import stale_draft_quotes
    for f, head, fr in stale_draft_quotes(ROOT):
        h = re.match(r"- §(\d+)\.", head)
        who = next((w for a, b, w in mlu.BAND if a <= int(h.group(1)) <= b), "?") if h else "50"
        lab = re.match(r"- (§[\d.]+(?:\([a-z]\))?)", head)
        out.append((lab.group(1) if lab else f[:30], "いまの草案に無い文を引いている（試作の前の文）", fr[:90],
                    f"{who} (いまの文に揃えるか、引用の前で「Tnn の前の文」と名乗る)"))
    snaps = mlc.snapshots()
    for s, cs in snaps.items():
        if not cs and mlc.LAW_HOST.search((L / "rounds" / s).read_text(encoding="utf-8")[:1500]):
            out.append((s[:40], "法令の写しが条に当たっていない", "§18 の行か jurisdictions の段に写しの名を書く", "置いた人"))
    return out


def pass_fail_items() -> list[tuple[str, str, str, str]]:
    out = []
    for line in against_text(L).splitlines():
        m = re.match(r"^\| (\d+) \|", line)
        if m:
            for d, rest in re.findall(r"\*\*合否の状態（([^）]+)）\*\*[:：]\s*([^|]{0,90})", line):
                if re.match(r"\s*(無い|まだ)", rest):
                    out.append((f"against #{m.group(1)}", f"合否 {d}", rest.strip()[:110], "30"))
    return out


def candidate_items() -> list[tuple[str, str, str, str]]:
    """SELF-AUDIT の 🔴 の項と、試作の文書の「先に登録する反例」のうち、閉じた印・答えの段が無いもの (1c が印の語を決めた・2026-11-16)。

    SELF-AUDIT: 項の本文に「**N.M 草案で閉じた（…）**」(errata の印と同じ語・どの版でも) が在れば閉じた、「**起草では閉じない**」が在れば
    起草の外 (別の状態で出す)。反例: 段の後、次の「**先に登録」か見出しまでに「**反例の結果**」が在れば答えた。
    """
    out = []
    # 2026-11-27 に §3e〜§3m を ACD-1.1-SELF-AUDIT-2.md へ切り出した (Check 52)。1 file だけ読むと、移した節の 🔴 が
    # 一覧から黙って消える (件数が減って「閉じた」に見える)。分割した file を全部、file ごとに読む
    for sa in sorted(L.glob("ACD-1.1-SELF-AUDIT*.md")):
        out.extend(_self_audit_items(sa.read_text(encoding="utf-8")))
    return out + _trial_items()


def _self_audit_items(st: str) -> list[tuple[str, str, str, str]]:
    out = []
    heads = list(re.finditer(r"^### 🔴 (.*)$", st, re.M))
    for i, h in enumerate(heads):
        end = re.search(r"^#{2,3} (?!⚠)", st[h.end():], re.M)
        body = st[h.end(): h.end() + end.start()] if end else st[h.end():]
        if re.search(r"\*\*\d+\.\d+ 草案で閉じた（", body):  # どの版で閉じた印も (errata・prepare_version_freeze と同じ形・1c)
            continue
        state = "起草の外" if "**起草では閉じない**" in body else "未閉"
        out.append(("SELF-AUDIT 🔴", state, h.group(1)[:110], "1c"))
    return out


def _trial_items() -> list[tuple[str, str, str, str]]:
    out = []
    for p in sorted(L.glob("ACD-1.4-*TRIAL.md")):
        lines = p.read_text(encoding="utf-8").splitlines()
        for i, ln in enumerate(lines):
            if ln.startswith("**先に登録する反例"):
                rest = []
                for nx in lines[i + 1:]:
                    if nx.startswith(("**先に登録", "#")):
                        break
                    rest.append(nx)
                if "**反例の結果**" not in "\n".join([ln] + rest):  # 同じ行の末尾に足した印も読む (1c・SECOND は行を増やせない)
                    out.append((f"{p.name}:{i + 1}", "答えの記録なし", re.sub(r"\*\*", "", ln)[:110], "30 (反例) / 1c"))
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


# 2026-11-15〜18 の割り振りの記録 (この file・measure_legal_uncertainty.BAND・合成の文書) はセッションの名で書かれている。
# 名を書き換えると記録の側 (BAND は 1 巡目に誰が当たったかの記録) が偽になるので、出す所でだけ役の名へ読み替える
ROLE_OF = {"1c": "本文", "30": "ドシエ", "50": "統合", "2f": "採掘", "9b": "機械層"}
_ROLE_RE = re.compile(r"(?<![0-9A-Za-z#§.])(" + "|".join(ROLE_OF) + r")(?![0-9A-Za-z.])")


def as_role(who: str) -> str:
    """担当の欄のセッションの名を役の名へ (「材料は 30」→「材料は ドシエ」)。項目や内容の欄には当てない (30 日・§30 などを壊す)。"""
    return _ROLE_RE.sub(lambda m: ROLE_OF[m.group(1)], who)


def table(title: str, rows: list[tuple[str, str, str, str]]) -> None:
    print(f"\n## {title}（{len(rows)} 件）\n")
    if not rows:
        print("なし")
        return
    print("| 項目 | 状態 | 内容 | 担当の候補 |\n| :-- | :-- | :-- | :-- |")
    for r in rows:
        r = (*r[:3], as_role(r[3]))
        print("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    ours, external = register_items()
    groups = [("我々が手を打てる register の行（TEXT・DOSSIER・OPEN・UNTRIAGED）", ours),
              ("閉じていない errata", errata_items()), ("決着していない B", b_items()),
              ("確定のゲートの満たしていない条件", gate_items()), ("答えていない問い", asof_items()),
              ("合成の文書 §6 の残り（読みの側）", synthesis_items()),
              ("合否の基準を書いて、まだ満たしていない register の行", pass_fail_items()),
              ("オーナーにしかできない行為", owner_items()), ("法律家と実務家への問い（未回答）", question_items()),
              ("法的解釈の台帳で手を打てる行（§18 の ② の未着手・③ の行き先なし、§19 の開いている試作）", legal_uncertainty_items()),
              ("閉じた印の無い SELF-AUDIT の 🔴 と、答えの記録の無い先に登録した反例", candidate_items())]
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
