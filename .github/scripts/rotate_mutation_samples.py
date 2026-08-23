#!/usr/bin/env python3
"""rotate_mutation_samples.py — mutation_samples.py の hot log を archive へ rotate する。

【なぜ要るか】
mutation は増え続ける append-log で、`mutation_samples.py` は Check 52 の advisory
(975 行) と Check 365 の BLOCKING (1,000 行) を持つ。実運用では **advisory を素通りして
BLOCKING に当たる**事故が繰り返し起きた (#1067 / #1135 の 2 回)。原因は「毎回その場で
brace-aware な分割スクリプトを書き起こしていた」こと —— 手順が人の注意力に依存していた。

そこで rotate を 1 コマンドにする。閾値を跨いだら `npm run rotate-mutations` を叩くだけで、
最古の entry を archive へ移し、行数と総数を報告する。

【なぜ brace-aware か】
素朴に `s.index('\\n]')` で配列末尾を探すと、**entry の文字列リテラル内の `]`** に当たって
ファイルを壊す (実際に 982 → 197 行まで削った事故がある)。文字列の内外を追いながら
bracket depth を数えるのが唯一安全な方法。

【不変条件】
- rotate 前後で `E2E_MUTATIONS` / `MUTATIONS` の総数が変わらない (importlib で検証する)
- 移動は「最古 (list の先頭)」から。新規は tail へ append される規約なので、
  先頭が最も古い

使い方:
    python3 .github/scripts/rotate_mutation_samples.py            # 必要なら自動で rotate
    python3 .github/scripts/rotate_mutation_samples.py --count 8  # 件数を指定
    python3 .github/scripts/rotate_mutation_samples.py --check    # 判定のみ (rotate しない)
"""
import sys

if sys.version_info < (3, 10):
    # check_repository_consistency.py 等と同様 3.10+ 専用 (PEP 604 等)。明示エラーで早期停止。
    print("ERROR: rotate_mutation_samples.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAIL = ROOT / ".github" / "scripts" / "mutation_samples.py"
def _pick_archive(stem="mutation_samples_e2e_archive", list_base="E2E_MUTATIONS_ARCHIVE"):
    """rotate 先を **導出** する: 余裕のある最新 archive、無ければ次の番号を起こす。

    [FIX 2026-08-21] 従来は `..._archive2.py` をハードコードしていたが、archive 自身も
    append-only で伸びるので **いつか 1,000 行 (Check 365) に当たる**。実際に当たった
    (1,027 行)。そのとき rotate は「hot log を減らしたのに BLOCKING が別ファイルで出る」
    という分かりにくい形で止まる。受け皿はハードコードせず、**余裕を実測して選ぶ**。

    番号なし (`..._e2e_archive.py`) を 1 番目とし、以降 `2`, `3`, ... を順に見て
    「rotate 後も BLOCKING に収まる」最初のものを返す。全部埋まっていれば次の番号を
    新規作成する (AI2AI.md の archive rotation と同じ考え方)。
    """
    base = ROOT / ".github" / "scripts"
    n = 1
    while True:
        name = f"{stem}.py" if n == 1 else f"{stem}{n}.py"
        path = base / name
        if not path.exists():
            # 新しい受け皿を起こす (既存 archive と同じ最小構造) + **配線まで行う**。
            # [FIX 2026-08-21] `mutation_samples.py` は archive を **1 行ずつ明示 import** する
            #   ので、ファイルを作っただけでは繋がらず、移した entry が総数から消える。
            #   直後の不変条件チェック (総数不変) が落ちて気付けるが、**その時点で既にファイルを
            #   書いた後**なので中途半端な状態が残る。作ると同時に import と連結式へ足す。
            _wire_new_archive(n, name)
            path.write_text(
                '"""%s%d.py — rotate 先 (自動生成)。\n\n' % (stem, n)
                + 'rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。\n'
                  '**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。\n"""\n'
                  'from mutation_samples_common import ROOT\n\n'
                + "%s%d = [\n]\n" % (list_base, n),
                encoding="utf-8",
            )
            return path
        if len(path.read_text(encoding="utf-8").splitlines()) < BLOCKING - 60:
            return path
        n += 1


ARCHIVE = None          # main() で _pick_archive() から決める
ADVISORY = 975          # Check 52 (ADVISORY) の閾値
BLOCKING = 1000         # Check 365 (BLOCKING) の上限


def _totals() -> tuple[int, int]:
    """import して (E2E_MUTATIONS, MUTATIONS) の件数を返す。

    **キャッシュを必ず捨てること。** `mutation_samples.py` は archive 群を `import` するので、
    2 回目の呼び出しで `sys.modules` に残った **古い archive** が再利用され、rotate 直後の
    件数が更新前のまま返る。実測: archive へ 1 件足しても purge 無しでは 297 のまま
    (purge すると 298)。この状態で不変条件を検査すると **正しい rotate を「総数が変わった」と
    誤検出して落ちる** (実際に踏んだ)。
    """
    sys.path.insert(0, str(ROOT / ".github" / "scripts"))
    for name in [m for m in sys.modules if m.startswith("mutation_samples") or m == "_ms"]:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location("_ms", TAIL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return len(mod.E2E_MUTATIONS), len(mod.MUTATIONS)


def _list_span(src: str, name: str) -> tuple[int, int]:
    """`name = [` の中身の (start, end) を bracket depth で返す。

    文字列リテラル内の括弧を数えないことが要点 (素朴な検索はファイルを壊す)。
    """
    start = src.index(f"{name} = [") + len(f"{name} = [")
    depth, i, in_str, quote, esc = 1, start, False, "", False
    while i < len(src):
        ch = src[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
        else:
            if ch in "\"'":
                in_str, quote = True, ch
            elif ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
                if depth == 0:
                    return start, i
        i += 1
    raise SystemExit(f"ERROR: {name} の閉じ括弧が見つからない")


def _split_entries(body: str) -> list[str]:
    """トップレベルの `{...}` 単位で分割する (同じく文字列内を無視)。"""
    entries, depth, cur, in_str, quote, esc = [], 0, "", False, "", False
    for ch in body:
        cur += ch
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
            continue
        if ch in "\"'":
            in_str, quote = True, ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                entries.append(cur.strip("\n ,"))
                cur = ""
    return entries



# ── rotate 単位の抽出 ───────────────────────────────────────────────────────────
# [FIX 2026-08-23] 従来 rotate は `NAME = [ ... ]` の **literal だけ**を排出対象にしていた。
#   ところが新しい mutation は必ず `NAME.append({...})` で足す規約 (本 file の docstring と
#   mutation_samples.py の docstring が両方そう述べている) なので、**成長は append 経由・
#   排出は literal のみ**という非対称があった。literal が枯れると
#   「ERROR: tail に N 件しかない — rotate すると空になる」で止まり、**append で溜まった
#   entry には逃げ道が一つも無い**。実際 2026-08-23 に literal 6 件 / append 87 件の状態で
#   advisory を超え、ツールからは詰みになった。literal と append を同じ「rotate 単位」として
#   扱い、ファイル上の出現順 (= 時系列順) で古いものから排出する。
def _rotatable_units(src: str, name: str) -> list[tuple[int, int, str]]:
    """`name` の rotate 単位を (start, end, dict 本文) で、ファイル上の出現順に返す。

    単位は 2 種類:
      - `name = [ ... ]` の中のトップレベル `{...}`
      - `name.append({ ... })` ブロック全体 (削除時は行ごと消す)
    """
    units: list[tuple[int, int, str]] = []
    ls, le = _list_span(src, name)
    off = ls
    for e in _split_entries(src[ls:le]):
        i = src.index(e, off)
        off = i + len(e)
        # `_split_entries` は entry 直前のコメント行を巻き込む。**コメントは hot log 固有の
        # 注記** (例: 「この curated meta-mutation は敢えて…」) なので archive へ運ばない。
        brace = e.index("{")
        units.append((i + brace, i + len(e), e[brace:]))
    # append ブロックは brace 走査で閉じ位置を求める (文字列内の括弧は数えない)
    marker = f"{name}.append("
    pos = 0
    while True:
        i = src.find(marker, pos)
        if i == -1:
            break
        j = src.index("{", i)
        depth, k, in_str, quote, esc = 0, j, False, "", False
        while k < len(src):
            ch = src[k]
            if in_str:
                if esc: esc = False
                elif ch == "\\": esc = True
                elif ch == quote: in_str = False
            else:
                if ch in "\"'": in_str, quote = True, ch
                elif ch in "[{": depth += 1
                elif ch in "]}":
                    depth -= 1
                    if depth == 0:
                        break
            k += 1
        entry = src[j:k + 1]
        # 行頭から `)` の次の改行までを 1 ブロックとして消す
        blk_start = src.rindex("\n", 0, i) + 1
        blk_end = src.index("\n", src.index(")", k)) + 1
        units.append((blk_start, blk_end, entry))
        pos = blk_end
    units.sort(key=lambda u: u[0])
    return units


# ── archive の再配分 (rebalance) ─────────────────────────────────────────────────
# [ADD 2026-08-23] rotate は **hot log → archive** しか面倒を見ていなかった。archive 自身も
#   entry の編集 (WHY コメントの追記や anchor の付け替え) で伸びるので、いつか上限に当たる。
#   実際 2026-08-23 に `mutation_samples_archive.py` が 1,000 行を超え、**自動の逃げ道が
#   一つも無かった** (受け皿 archive2 に 130 行以上の余裕があったのに移す手段が無い)。
#   同じ chain の中で「溢れた archive の末尾 → 次の archive の先頭」へ移す。
#   末尾→先頭にするのは **時系列順を壊さない**ため (chain は 古い archive + 新しい archive の
#   連結なので、溢れた側の末尾が受け皿側の先頭に来るのが正しい隣接関係)。
CHAINS = [
    ("MUTATIONS_ARCHIVE", ["mutation_samples_archive.py", "mutation_samples_archive2.py"]),
    ("E2E_MUTATIONS_ARCHIVE", ["mutation_samples_e2e_archive.py",
                               "mutation_samples_e2e_archive2.py",
                               "mutation_samples_e2e_archive3.py"]),
]
REBALANCE_TARGET = 950   # Check 443 が要求する advisory (hard ceiling 未満)


def _list_name_for(filename: str, base_list: str) -> str:
    """file 名から中の list 名を導く (archive.py -> ...ARCHIVE / archive2.py -> ...ARCHIVE2)。"""
    stem = filename[:-3]
    n = ""
    while stem and stem[-1].isdigit():
        n = stem[-1] + n
        stem = stem[:-1]
    return base_list + n


def _render(prefix: str, entries: list, suffix: str) -> str:
    body = "\n".join("    " + e.lstrip() + "," for e in entries)
    out = prefix + "\n" + body + "\n" + suffix
    # [FIX 2026-08-23] 末尾改行を保証する。落とすと `wc -l` と `splitlines()` が 1 ずれ、
    #   Check 424 (§2 表 == 実測) と Check 52 (advisory) が**同じ file に違う行数を報告する**
    #   —— 本日その食い違いで §2 表を誤った値へ「修正」して CI を赤にした (Check 52 側を
    #   splitlines へ統一して解消済) ので、書き出す側でも再発させない。
    return out if out.endswith("\n") else out + "\n"


def _rebalance() -> bool:
    """上限を超えた archive の末尾 entry を、余裕のある次の archive の先頭へ移す。"""
    base = ROOT / ".github" / "scripts"
    moved_any = False
    for base_list, files in CHAINS:
        for i, fname in enumerate(files[:-1]):
            src_path = base / fname
            if not src_path.exists():
                continue
            n = len(src_path.read_text(encoding="utf-8").splitlines())
            if n <= REBALANCE_TARGET:
                continue
            dst_path = base / files[i + 1]
            if not dst_path.exists():
                print(f"  {fname}: {n} 行だが受け皿 {files[i+1]} が無い — 手動対応が必要")
                continue
            src_txt = src_path.read_text(encoding="utf-8")
            a, b = _list_span(src_txt, _list_name_for(fname, base_list))
            entries = _split_entries(src_txt[a:b])
            move = []
            while entries and len(
                _render(src_txt[:a], entries, src_txt[b:]).splitlines()
            ) > REBALANCE_TARGET:
                move.insert(0, entries.pop())
            if not move:
                continue
            src_path.write_text(_render(src_txt[:a], entries, src_txt[b:]), encoding="utf-8")
            dst_txt = dst_path.read_text(encoding="utf-8")
            c, _ = _list_span(dst_txt, _list_name_for(files[i + 1], base_list))
            inject = "\n".join("    " + e.lstrip() + "," for e in move)
            dst_path.write_text(dst_txt[:c] + "\n" + inject + dst_txt[c:], encoding="utf-8")
            after = len(src_path.read_text(encoding="utf-8").splitlines())
            print(f"  rebalance: {fname} {n} -> {after} 行 "
                  f"({len(move)} entry を {files[i+1]} の先頭へ)")
            moved_any = True
    return moved_any

def main() -> int:
    lines = len(TAIL.read_text(encoding="utf-8").splitlines())
    e2e_before, cons_before = _totals()
    over_blocking = lines >= BLOCKING
    over_advisory = lines > ADVISORY
    state = "BLOCKING 超過" if over_blocking else ("advisory 超過" if over_advisory else "余裕あり")
    print(f"mutation_samples.py: {lines} 行 (advisory {ADVISORY} / BLOCKING {BLOCKING}) — {state}")
    print(f"  E2E_MUTATIONS={e2e_before} / MUTATIONS={cons_before}")

    if "--check" in sys.argv:
        return 1 if over_advisory else 0

    # archive 自身の溢れ (entry 編集で伸びる) は hot log と独立に起きるので、先に均す
    e2e_b0, cons_b0 = _totals()
    if _rebalance():
        e2e_a0, cons_a0 = _totals()
        if (e2e_a0, cons_a0) != (e2e_b0, cons_b0):
            raise SystemExit(f"ERROR: rebalance で総数が変わった "
                             f"(E2E {e2e_b0}->{e2e_a0} / MUTATIONS {cons_b0}->{cons_a0})")
        print("  ※ docs/architecture/file-size-budget.md の §2 実測行数を同期すること (Check 424)")

    if not over_advisory:
        print("rotate 不要 (hot log)。")
        return 0

    count = 6
    if "--count" in sys.argv:
        count = int(sys.argv[sys.argv.index("--count") + 1])

    src = TAIL.read_text(encoding="utf-8")
    # rotate 元の tail は **単位数の多い方**を選ぶ。hot log は E2E と consistency の 2 本を
    # 抱えており、片方だけを排出対象にすると (旧実装) もう一方が上限まで伸びて詰む。
    TAILS = [
        ("_E2E_TAIL", "mutation_samples_e2e_archive", "E2E_MUTATIONS_ARCHIVE"),
        ("_MUTATIONS_TAIL", "mutation_samples_archive", "MUTATIONS_ARCHIVE"),
    ]
    cands = [(len(_rotatable_units(src, n)), n, stem, base) for n, stem, base in TAILS]
    cands.sort(reverse=True)
    n_units, tail_name, stem, list_base = cands[0]
    if n_units <= count:
        raise SystemExit(
            "ERROR: どの tail も rotate すると空になる: "
            + " / ".join(f"{n}={c}" for c, n, _, _ in cands)
        )

    units = _rotatable_units(src, tail_name)
    move = [u[2] for u in units[:count]]
    # 後ろから削ると前方の offset がずれない
    out = src
    for st, en, _ in reversed(units[:count]):
        out = out[:st] + out[en:]
    # literal から抜いた跡に残る空の `,` 行を掃除する (append ブロックは行ごと消えている)
    out = re.sub(r"\n\s*,(?=\n)", "", out)
    TAIL.write_text(out, encoding="utf-8")

    archive = _pick_archive(stem, list_base)
    arc = archive.read_text(encoding="utf-8")
    k = arc.rindex("]")
    archive.write_text(
        arc[:k] + "\n".join("    " + e.lstrip() + "," for e in move) + "\n" + arc[k:],
        encoding="utf-8",
    )

    # 不変条件: 総数が変わっていないこと (rotate は移動であって削除ではない)
    e2e_after, cons_after = _totals()
    if (e2e_after, cons_after) != (e2e_before, cons_before):
        raise SystemExit(
            f"ERROR: rotate で総数が変わった "
            f"(E2E {e2e_before}→{e2e_after} / MUTATIONS {cons_before}→{cons_after})"
        )

    after = len(TAIL.read_text(encoding="utf-8").splitlines())
    print(f"rotated {count} entries from {tail_name} → {archive.name}")
    print(f"  mutation_samples.py: {lines} → {after} 行")
    print(f"  総数は不変: E2E={e2e_after} / MUTATIONS={cons_after}")
    print("  ※ docs/architecture/file-size-budget.md の §2 実測行数を同期すること (Check 424)")
    return 0


if __name__ == "__main__":
    sys.exit(main())


def _wire_new_archive(n, filename):
    """新しい archive を `mutation_samples.py` の import と連結式へ足す。

    `mutation_samples.py` は `from mutation_samples_e2e_archiveN import E2E_MUTATIONS_ARCHIVEN`
    を **1 行ずつ明示** し、末尾で `E2E_MUTATIONS = ARCHIVE3 + ARCHIVE2 + ARCHIVE + _TAIL` の
    ように連結する。受け皿を増やすときは **両方**を更新しないと、移した entry が
    どこからも参照されず総数が減る (Check 430 が「連結式より後の append は死ぬ」を守るのと同族の
    「登録したつもりで実行されない」class)。
    """
    tail = TAIL.read_text(encoding="utf-8")
    mod = filename[:-3]
    var = f"E2E_MUTATIONS_ARCHIVE{n}"
    if var in tail:
        return
    anchor_imp = "from mutation_samples_e2e_archive import E2E_MUTATIONS_ARCHIVE\n"
    tail = tail.replace(anchor_imp, anchor_imp + f"from {mod} import {var}\n", 1)
    m = re.search(r"^E2E_MUTATIONS = (.+)$", tail, re.M)
    tail = tail.replace(m.group(0), f"E2E_MUTATIONS = {var} + " + m.group(1), 1)
    TAIL.write_text(tail, encoding="utf-8")
