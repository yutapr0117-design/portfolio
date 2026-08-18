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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAIL = ROOT / ".github" / "scripts" / "mutation_samples.py"
ARCHIVE = ROOT / ".github" / "scripts" / "mutation_samples_e2e_archive2.py"
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
    if not over_advisory:
        print("rotate 不要。")
        return 0

    count = 6
    if "--count" in sys.argv:
        count = int(sys.argv[sys.argv.index("--count") + 1])

    src = TAIL.read_text(encoding="utf-8")
    start, end = _list_span(src, "_E2E_TAIL")
    entries = _split_entries(src[start:end])
    if len(entries) <= count:
        raise SystemExit(f"ERROR: tail に {len(entries)} 件しかない — rotate すると空になる")

    move, keep = entries[:count], entries[count:]
    TAIL.write_text(
        src[:start] + "\n" + "\n".join("    " + e.lstrip() + "," for e in keep) + "\n" + src[end:],
        encoding="utf-8",
    )
    arc = ARCHIVE.read_text(encoding="utf-8")
    k = arc.rindex("]")
    ARCHIVE.write_text(
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
    print(f"rotated {count} entries → {ARCHIVE.name}")
    print(f"  mutation_samples.py: {lines} → {after} 行")
    print(f"  総数は不変: E2E={e2e_after} / MUTATIONS={cons_after}")
    print("  ※ docs/architecture/file-size-budget.md の §2 実測行数を同期すること (Check 424)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
