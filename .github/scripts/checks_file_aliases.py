"""
checks_file_aliases.py — file alias byte-equality & required-presence checks (4/5/190)
(extracted from check_repository_consistency.py — check.py split track・category "file aliases &
presence"・self-contained cluster).

Contiguous/non-contiguous but all self-contained: each check reads its own file(s) directly and
requires only ctx.ROOT / ctx.check / ctx.read_bytes — no global pre-loaded content dependency.
Executed at Check 4's position in list order (Checks 4 and 5 are contiguous; 190 is pulled
forward from its original position but feeds no shared state, so position is irrelevant for
correctness).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read_bytes.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  4.   llms alias files are byte-identical (llms.txt / .well-known/llms.txt / llms_well-known.txt /
       .well-known/llms_well-known.txt)
  5.   .well-known/index.json == .well-known/agent-skills/index.json (agent-skills alias)
  190. .nojekyll file presence (GitHub Pages Jekyll bypass) (BLOCKING)
"""


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read_bytes = ctx.read_bytes

    # ── 4. llms alias files byte-identical ───────────────────────────────────────
    llms_paths = [
        "llms.txt",
        ".well-known/llms.txt",
        "llms_well-known.txt",
        ".well-known/llms_well-known.txt",
    ]
    llms_bytes = [(p, read_bytes(p)) for p in llms_paths if (ROOT / p).exists()]
    if len(llms_bytes) >= 2:
        ref_path, ref_bytes = llms_bytes[0]
        for p, b in llms_bytes[1:]:
            check(
                b == ref_bytes,
                f"{p} is byte-identical to {ref_path}",
                f"llms alias mismatch: {p} differs from {ref_path}",
            )

    # ── 5. .well-known/index.json == agent-skills/index.json ─────────────────────
    idx_bytes = read_bytes(".well-known/index.json")
    ask_bytes = read_bytes(".well-known/agent-skills/index.json")
    check(
        idx_bytes == ask_bytes,
        ".well-known/index.json == .well-known/agent-skills/index.json",
        ".well-known/index.json and .well-known/agent-skills/index.json differ",
    )

    # ── 190. .nojekyll file presence (GitHub Pages Jekyll bypass) (BLOCKING) ──────
    # repo root の `.nojekyll` file 存在を BLOCKING 強制。GitHub Pages は本 file が
    # 無いと Jekyll 処理を稼働させ、`_` 始まりの file/directory (例
    # `docs/files/_template.md`、`_assets/`) を silent に skip する。本 site は
    # underscore-prefix path を含むため本 file 欠落は invisible 破壊 (homepage は
    # 描画されるが特定 path が 404 化)。presence-only (file は空でも OK)。
    _nj190 = ROOT / ".nojekyll"
    _ok190 = _nj190.exists() and _nj190.is_file()
    check(
        _ok190,
        "Check 190: .nojekyll file presence (GitHub Pages Jekyll bypass)",
        "Check 190: .nojekyll file が repo root に無い — GitHub Pages が Jekyll 処理を "
        "稼働させ _-prefix path (例 _template.md / _assets/) が silent に 404 化。"
        "`touch .nojekyll` で空 file を作成し commit せよ",
        blocking=True,
    )
