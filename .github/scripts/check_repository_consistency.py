#!/usr/bin/env python3
"""
check_repository_consistency.py — P0-23 / Cross-file consistency check (BLOCKING)

Verifies that key version, date, and structural invariants hold across the repository.

Checks performed (the numbering is historical/incremental; this list is the
authoritative inventory and is kept in sync with the implementation below):
  45. This check file's self-documentation matches its implementation: the numbered
      entries in THIS module docstring (the "N. ..." inventory above) and the numbered
      "# ── N." section-header comments in the code body describe the same set of checks,
      are contiguous 1..N with no gaps or duplicates on each side, and agree with each
      other. The inventory and the section headers are two hand-maintained descriptions of
      the same checks; until now nothing stopped them from silently drifting apart (a new
      check added in the body but forgotten in the inventory, or renumbered on one side
      only), which would make this file's own documentation lie about what it enforces.
      This is a self-referential meta-check: it is true precisely because anyone adding a
      check updates BOTH descriptions together — exactly the discipline it exists to keep.
      It asserts structural agreement of the documentation, not the behaviour of any
      individual check. (BLOCKING)
  70. total-check-runbook.md §9 check-count cross-reference: docs/architecture/total-check-
      runbook.md §9 の「consistency Check 総数」行に記述された Check 件数 (`**N**`) が
      check_repository_consistency.py の実装上の Check 番号最大値と一致することを機械強制する。
      Check 45 が docstring inventory ↔ section header の bijection を見るのに対し、本 Check
      は「実装ファイル ↔ runbook §9」の cross-document 整合性を担う。新 Check 追加時に runbook
      を更新し忘れる drift を pre-commit で構造的に閉じる。(BLOCKING)
  105. check-repository-consistency-map.md ↔ implementation Check-number bijection: the map
       documents EXACTLY the set of check numbers the implementation defines (section headers
       1..N, alpha sub-checks like 73a normalized to 73). The cross-document counterpart of
       Check 45 (docstring ↔ section bijection): it catches the "added a Check but forgot the
       map row" drift class structurally, so the human-facing check inventory can never fall
       silently behind the implementation. (BLOCKING)
"""

import ast
import base64
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# stale-.pyc false-RED 防止: check.py は多数の checks_*.py sibling module を import するが、
# それらの __pycache__/*.pyc が旧ロジックをキャッシュして現行 .py を上書き実行し、ローカルで
# 既存ファイル無変更のまま BLOCKING が偽 RED になる事故が複数回起きた (例: Check 337 webp
# magic bytes 判定が旧 re ベース版でキャッシュされ、無傷の webp を誤検知)。CI は clean checkout
# ゆえ無影響だが、ローカル自走の調査時間を浪費する。以降の import で .pyc を一切書かせないことで
# 「今後 .pyc が生成されない ⟹ stale 化しえない」を構造的に保証する (実行速度への影響は無視可)。
sys.dont_write_bytecode = True

# 純 I/O helper は sibling module `_lib_io.py` に抽出 (check-repository-consistency-
# map.md §4 で予告された helper-first 抽出の第一歩)。sibling import は Python が
# 実行スクリプトのディレクトリを自動 sys.path に含めるため、特別な path 操作不要。
# 既存呼出インターフェース (`read(path)` / `read_bytes(path)` / `extract(pat, text)`)
# は保持し、ROOT を bind した薄い wrapper で公開する。
from _lib_io import csp_sri_hash as _lib_csp_sri_hash
from _lib_io import extract
from _lib_io import read as _lib_read
from _lib_io import read_bytes as _lib_read_bytes

# Python version guard: these verification scripts use 3.10+ syntax (PEP 604
# `str | None` union annotations, e.g. `root_lastmod: str | None` below). On
# Python 3.9 (the macOS system interpreter at /usr/bin/python3) a module-level
# union annotation raises an opaque `TypeError: unsupported operand type(s) for |`
# at import time, which is hard to diagnose. Fail fast with an actionable message
# instead. The repo targets Python 3.12 (CI setup-python pin). Held in place by
# Check 104 so it cannot be silently removed.
if sys.version_info < (3, 10):
    sys.exit(
        "ERROR: this repository's verification scripts require Python 3.10+ "
        f"(found {sys.version.split()[0]}). Use python3.12 — see CLAUDE.md / .zprofile."
    )

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warnings: list[str] = []

# All source files that contribute numbered Check sections. The self-integrity Checks
# (45 docstring↔section bijection / 70 runbook count / 105 map bijection) aggregate the
# section headers AND the docstring inventory across ALL of these files, so the 4800-line
# monolith can be split into domain modules (each carrying its own checks + their docstring
# N. lines) without breaking self-integrity. Today: just this file. Extracting a module =
# append it here + move its sections + their docstring lines into it.
CHECK_SOURCE_FILES: list = [
    ROOT / ".github" / "scripts" / "check_repository_consistency.py",
    ROOT / ".github" / "scripts" / "checks_maintainability.py",  # split: maintainability/test-health/file-size
    ROOT / ".github" / "scripts" / "checks_structural.py",  # split: structural / CI wiring / tooling (48-51)
    ROOT / ".github" / "scripts" / "checks_esm.py",  # split: ESM contract cluster (47/56/57/61)
    ROOT / ".github" / "scripts" / "checks_tooling.py",  # split: dev-tooling/.claude config cluster (74-80)
    ROOT / ".github" / "scripts" / "checks_entity.py",  # split: entity/Organization cross-surface cluster (81-90)
    ROOT / ".github" / "scripts" / "checks_docs_mirror.py",  # split: docs/files mirror-doc governance (96-99)
    ROOT / ".github" / "scripts" / "checks_aio_derived.py",  # split: AIO C6 derived-value & date tooling (91-95)
    ROOT / ".github" / "scripts" / "checks_app_route.py",  # split: app-route whitelist coherence-mesh (136-140)
    ROOT / ".github" / "scripts" / "checks_ci_supply.py",  # split: CI/workflow coverage & supply-chain (142-145)
    ROOT / ".github" / "scripts" / "checks_behavioral.py",  # split: shipped-JS behavioral regression guards (128-131)
    ROOT / ".github" / "scripts" / "checks_shipped_structure.py",  # split: shipped-JS structural coherence & byte budget (118-120)
    ROOT / ".github" / "scripts" / "checks_wiring.py",  # split: shipped-asset & AIO wiring/discoverability (132-134)
    ROOT / ".github" / "scripts" / "checks_aio_entity.py",  # split: AIO manifest entity-field & identity coherence (167-173)
    ROOT / ".github" / "scripts" / "checks_seo_coherence.py",  # split: AIO/SEO URL-canonical-format coherence (273-302)
    ROOT / ".github" / "scripts" / "checks_seo_coherence_b.py",  # split: seo_coherence part B (288-302・module 自身の 2 分割で ≤1,000)
    ROOT / ".github" / "scripts" / "checks_sitemap_manifest.py",  # split: 311-320
    ROOT / ".github" / "scripts" / "checks_html_standards.py",  # split: 324-337
    ROOT / ".github" / "scripts" / "checks_jsonld_entity.py",  # split: 191-200
    ROOT / ".github" / "scripts" / "checks_jsonld_meta.py",  # split: 221-235
    ROOT / ".github" / "scripts" / "checks_meta_url.py",  # split: 175-180
    ROOT / ".github" / "scripts" / "checks_canonical_https.py",  # split: 202-214
    ROOT / ".github" / "scripts" / "checks_shipped_hygiene.py",  # split: 242-249, 366-368
    ROOT / ".github" / "scripts" / "checks_jsonld_primary.py",  # split: 256-261
    ROOT / ".github" / "scripts" / "checks_jsonld_refs.py",  # split: 216-219
    ROOT / ".github" / "scripts" / "checks_sw_pwa.py",  # split: 251-254
    ROOT / ".github" / "scripts" / "checks_csp_security.py",  # split: 351-355
    ROOT / ".github" / "scripts" / "checks_ci_verify.py",  # split: 345-347
    ROOT / ".github" / "scripts" / "checks_meta_validity.py",  # split: 341-343
    ROOT / ".github" / "scripts" / "checks_asset_resolve.py",  # split: 357-359
    ROOT / ".github" / "scripts" / "checks_binary_dims.py",  # split: 338/339/340/348
    ROOT / ".github" / "scripts" / "checks_misc_governance.py",  # split: 9/10/12/13/15/121/141/201/215/349/360
    ROOT / ".github" / "scripts" / "checks_safety_guards.py",  # split: 123/124/125/126/127
    ROOT / ".github" / "scripts" / "checks_shipped_content.py",  # split: 236/238/266/267/268
    ROOT / ".github" / "scripts" / "checks_canon_config.py",  # split: canon-policy / config / meta-governance (100/102/104/106/107/109/112/113)
    ROOT / ".github" / "scripts" / "checks_tracked_files.py",  # split: tracked-files mirror bijection + private-document guard (108/122・ctx-enrich _member_paths)
    ROOT / ".github" / "scripts" / "checks_eslint_budget.py",  # split: ESLint warning-baseline & file-size-budget governance trio (59/60/72)
    ROOT / ".github" / "scripts" / "checks_structural_ci.py",  # split: kernel/canary structural integrity + CI lint-coupling (43/44/46/53/54/55/58)
    ROOT / ".github" / "scripts" / "checks_repo_hygiene.py",  # split: repository hygiene / doc-dating / artifact / lock-sync (31-41 minus 37)
    ROOT / ".github" / "scripts" / "checks_residual_coherence.py",  # split: residual project/Speakable/route + theme-color/sitemap/manifest (146-148/304-309)
    ROOT / ".github" / "scripts" / "checks_seo_baseline.py",  # split: SEO/AIO date-ISO + URL-resolution + HTTPS/meta baseline (181-189 minus 187)
    ROOT / ".github" / "scripts" / "checks_aio_config.py",  # split: AIO entity/crawler identity + CI/config governance (62-69)
    ROOT / ".github" / "scripts" / "checks_governance_sync.py",  # split: AIO/AI2AI/llms freshness & governance sync (21-27)
    ROOT / ".github" / "scripts" / "checks_seo_meta.py",  # split: AIO/SEO meta + canonical URL + resource-resolution (149-166 minus 152)
    ROOT / ".github" / "scripts" / "checks_source_coherence.py",  # split: cross-file source coherence + CSP-hash (7/11/14/350・ctx-enrich)
    ROOT / ".github" / "scripts" / "checks_version.py",  # split: app-version cross-surface coherence (1/2/3/19・ctx-enrich)
    ROOT / ".github" / "scripts" / "checks_html.py",  # split: index.html document/meta baseline & lang coherence (8/20/115/152/187/220/250/255/303/306・ctx-enrich html)
    ROOT / ".github" / "scripts" / "checks_css.py",  # split: style.css / CSS contract (6/73/101/103/135/174/321-323/344/356・ctx-enrich style)
    ROOT / ".github" / "scripts" / "checks_shipped_static.py",  # split: shipped-JS static analysis + byte budgets (237/239-241/262-265/269-272/310)
    ROOT / ".github" / "scripts" / "checks_e2e_infra.py",  # split: e2e/Playwright test-infra hygiene (110/111/114/116/117)
    ROOT / ".github" / "scripts" / "checks_file_aliases.py",  # split: file alias byte-equality & required-presence (4/5/190)
    ROOT / ".github" / "scripts" / "checks_date_sync.py",  # split: date-sync coherence (17/18)
    ROOT / ".github" / "scripts" / "checks_csp_hashes.py",  # split: inline-script CSP hash verification (7b/7c)
    ROOT / ".github" / "scripts" / "checks_artifact_scan.py",  # split: generated/cache artifact tracking guard (37)
]


def _aggregate_check_numbers():
    """(inventory_nums, section_nums) sorted, aggregated across CHECK_SOURCE_FILES.

    inventory_nums = `  N. ` lines in each file's module docstring (first triple-quoted block).
    section_nums   = the `# <box-drawing> N.` section-header numbers in each file's body.
    Self-integrity Checks 45/70/105 use this so the bijection spans every split check module.
    NOTE: leading whitespace is tolerated on the section header so an extracted module can keep
    its `# ── N.` headers inside `def run(ctx):` (indented) — see checks_maintainability.py.
    """
    _sec_re = re.compile(r'^\s*#\s*──\s*(\d+)\.', re.MULTILINE)
    _inv_re = re.compile(r'^\s{2}(\d+)\.\s', re.MULTILINE)
    _doc_re = re.compile(r'"""(.*?)"""', re.DOTALL)
    inv: list = []
    sec: list = []
    for _src in CHECK_SOURCE_FILES:
        if not _src.exists():
            continue
        _txt = _src.read_text(encoding="utf-8")
        _dm = _doc_re.search(_txt)
        _doc = _dm.group(1) if _dm else ""
        _body = _txt[_dm.end():] if _dm else _txt
        inv.extend(int(n) for n in _inv_re.findall(_doc))
        sec.extend(int(n) for n in _sec_re.findall(_body))
    return sorted(inv), sorted(sec)


def check(condition: bool, msg_ok: str, msg_fail: str, blocking: bool = True) -> None:
    if condition:
        print(f"OK: {msg_ok}")
    else:
        tag = "ERROR" if blocking else "WARNING"
        print(f"{tag}: {msg_fail}")
        (errors if blocking else warnings).append(msg_fail)


def read(path: str) -> str:
    """ROOT 基準で text ファイルを読む (互換 wrapper)."""
    return _lib_read(path, root=ROOT)


def read_bytes(path: str) -> bytes:
    """ROOT 基準で binary ファイルを読む (互換 wrapper)."""
    return _lib_read_bytes(path, root=ROOT)


# ── Shared check context for extracted check modules (Phase 1 check.py split) ──
# checks_maintainability.run(_ctx) 等の抽出 module に「monolith と同一の」check()/errors/warnings/
# ROOT/read 等を明示注入する。errors/warnings は同一 list オブジェクトを参照で渡すため、抽出 module の
# check() 呼び出しも同じ errors/warnings に append する = 挙動 byte-equivalent。exec() を使わず module-
# global 結合も無いので #253 が指摘した net-negative (自由変数の静的解決不能・未定義グローバル参照) を回避。
import types as _types
_ctx = _types.SimpleNamespace(
    ROOT=ROOT, check=check, read=read, read_bytes=read_bytes,
    extract=extract, errors=errors, warnings=warnings,
)


# ── Load files ──────────────────────────────────────────────────────────────
html       = read("index.html")
ai2ai      = read("AI2AI.md")
mainjs     = read("main.js")
style      = read("style.css")
aio_mon    = read(".github/scripts/aio_monitoring.py")

mcp_data   = json.loads(read(".well-known/mcp.json"))

# ── ctx enrichment for split modules that read shared global content (check.py split track) ──
# split-out checks_* modules that need the pre-loaded style.css (etc.) content unpack it from ctx
# (avoids re-reading). Added AFTER the globals load so the value already exists on _ctx. Only the
# content actually consumed by an extracted module is attached here — extend as further glob-
# dependent categories (html / mainjs / ai2ai / mcp_data) are split out in later phases.
_ctx.style = style
_ctx.html = html
_ctx.ai2ai = ai2ai
_ctx.mainjs = mainjs
_ctx.mcp_data = mcp_data
_ctx.aio_mon = aio_mon

# ── setup: repository member-paths producer (relocated from Check 37 for consumer sharing) ──
# `_member_paths` (git ls-files / pruned walk) は Check 37(artifact scan) が producer だが 108/122 等の
# consumer も参照する共有 setup-global。checks 実行前に一度計算し `_ctx._member_paths` へ attach する
# (byte-equivalent: git ls-files はいつ呼んでも同結果)。分割 module は `_member_paths = ctx._member_paths` で unpack。
FORBIDDEN_GENERATED_PATH_PARTS = {
    "__pycache__",
    "node_modules",
    "test-results",
    "playwright-report",
    "blob-report",
    ".pytest_cache",
}
FORBIDDEN_GENERATED_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    "npm-debug.log",
}
FORBIDDEN_GENERATED_SUFFIXES = (".pyc", ".pyo")


def _repo_member_paths() -> list[str]:
    """Repo-relative POSIX paths that constitute the repository.

    Prefer `git ls-files` (authoritative: excludes untracked/ignored runtime dirs).
    Fall back to a pruned filesystem walk for ZIP/zipball contexts without .git."""
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=str(ROOT), capture_output=True, timeout=30,
        )
        if proc.returncode == 0 and proc.stdout:
            return [p for p in proc.stdout.decode("utf-8", "replace").split("\0") if p]
    except (OSError, subprocess.SubprocessError):
        pass
    import os as _os37
    _prune = {".git"} | FORBIDDEN_GENERATED_PATH_PARTS
    out: list[str] = []
    for dirpath, dirnames, filenames in _os37.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in _prune]
        for fn in filenames:
            out.append((Path(dirpath) / fn).relative_to(ROOT).as_posix())
    return out


_member_paths = _repo_member_paths()
_ctx._member_paths = _member_paths

# ── 1/2/3/19. app-version cross-surface coherence → checks_version.py ──
# (check.py split track・ctx-enrich module。html/ai2ai/mainjs/mcp_data を _ctx 経由で消費。ai:version==
#  Pipeline-Version(1)/main.js VERSION(2)/mcp.json server.version(3)/sw.js CACHE_NAME(19)。共有=html_v
#  (Check 1 で extract・2/3/19 が再利用)。1 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で横断集約。)
import checks_version as _checks_version
_checks_version.run(_ctx)

# ── 4/5/190. file alias byte-equality & required-presence → checks_file_aliases.py ──
# (check.py split track・self-contained cluster: ROOT/check/read_bytes のみ必要・global content 依存なし。
#  llms alias 一致(4) / .well-known/index.json alias 一致(5) / .nojekyll 存在(190)。
#  Check 190 は元位置(762行)から本 import へ引き取り (独立・下流への共有値なし・位置無関係)。
#  4 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_file_aliases as _checks_file_aliases
_checks_file_aliases.run(_ctx)

# ── 6/73/101/103/135/174/321-323/344/356. style.css / CSS contract → checks_css.py ──
# (check.py split track・first ctx-enrich module。style glob を _ctx.style 経由で消費。forced-colors/HCM/
#  prefers-contrast a11y(101/103)/theme-color(174)/a11y-CWV attr(73)/@import·inline·@layer(321-323/344)/
#  Google-Fonts CSP(356)/token baseline(6/135)。非連続・style 以外の cross-section 結合なし。6 位置で
#  list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_css as _checks_css
_checks_css.run(_ctx)

# ── 7/11/14/350. cross-file source coherence + CSP-hash → checks_source_coherence.py ──
# (check.py split track・ctx-enrich。html/ai2ai/aio_mon を _ctx 経由・_lib_io.csp_sri_hash helper 同梱。
#  CSP meta 順序(7)/AIO-monitoring shape(11)/v1→v74 transitions(14)/CSP inline hash(350)。date-sync 17/18
#  は html_date+root_lastmod 共有ゆえ別 mini-cluster に残置。7 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_source_coherence as _checks_source_coherence
_checks_source_coherence.run(_ctx)

# ── 7b/7c. inline-script CSP hashes → checks_csp_hashes.py ──────────────────
# (check.py split track・ctx-enrich。html を _ctx.html 経由・_lib_io.csp_sri_hash を module 内 import。
#  suppressor(7b)/speculationrules(7c)の 2 件を re + csp_sri_hash で検証する自己完結 cluster。
#  7b 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_csp_hashes as _checks_csp_hashes
_checks_csp_hashes.run(_ctx)

# ── 8/20/115/152/187/220/250/255/303/306. index.html document/meta baseline & lang coherence → checks_html.py ──
# (check.py split track・ctx-enrich module。html glob を _ctx.html 経由で消費。security meta(8/115)/
#  og:image dims(20)/<html lang> coherence(152/187/220/250)/doc structure(255/306)/data-attr(303)。
#  Check 7 は _lib_io.csp_sri_hash helper 依存ゆえ除外。8 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_html as _checks_html
_checks_html.run(_ctx)

# ── 9/10/12/13/15/121/141/201/215/349/360. misc AIO/SEO/governance singletons (9/10/12/13/15/121/141/201/215/349/360) → checks_misc_governance.py ──
# (check.py split track. 連続/非連続 self-contained クラスタ・各 Check 自前 read。9 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_misc_governance as _checks_misc_governance
_checks_misc_governance.run(_ctx)

# ── 17/18. date-sync coherence (ai:last-modified / SITE_CONFIG.LAST_UPDATED / sitemap root lastmod) → checks_date_sync.py ──
# (check.py split track・ctx-enrich. Check 17 が html_date を定義し Check 18 が消費する coupled-var
#  cluster。html (ctx.html) / mainjs (ctx.mainjs) / ROOT / warnings の 4 依存を ctx 経由で取得。
#  17 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_date_sync as _checks_date_sync
_checks_date_sync.run(_ctx)

# ── 21-27. AIO/AI2AI/llms freshness & session-record governance sync → checks_governance_sync.py ──
# (check.py split track. llms alias Last-Updated(21)/AI2AI record order(22)/YAML syntax(23)/llms-full
#  freshness(24)/monitoring-log evidence_policy(25)/archive record==manifest role(26)/no stale C1-C6(27)。
#  連続 self-contained・各 Check 自前 read。21 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で横断集約。)
import checks_governance_sync as _checks_governance_sync
_checks_governance_sync.run(_ctx)

# ── 31-41 (minus 37). repository hygiene / doc-dating / artifact / lock-sync → checks_repo_hygiene.py ──
# (check.py split track. Claude2Claude↔AI2AI(31)/JSON-LD valid(32)/Zenn slug(33)/doc dating(34)/
#  robots↔sitemap(35)/no-future-date(36)/lock sync(38)/loc→file(39)/CSS lint(40)/monitoring↔manifest(41)。
#  Check 37 は _member_paths の producer(後続 consumer と結合)ゆえ残置。31 位置で list 順連続実行。)
import checks_repo_hygiene as _checks_repo_hygiene
_checks_repo_hygiene.run(_ctx)

# ── 37: No generated/cache artifacts are tracked in the repository → checks_artifact_scan.py ──
# (check.py split track。ctx._member_paths を消費。FORBIDDEN_* 定数は module 内に複製 (安定定数・
#  単一責任。Check 45/70/105 で整合が機械強制される)。37 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_artifact_scan as _checks_artifact_scan
_checks_artifact_scan.run(_ctx)

# ── 43/44/46/53/54/55/58/60. kernel/canary structural integrity + CI lint-coupling → checks_structural_ci.py ──
# (check.py split track. AIDK kernel(43)/canary(44)/lint scripts(46)/modulepreload(53)/eslint major(54)/
#  CI lint-target(55)/e2e routes↔switch(58)/ESLint baseline(60)。45 は self-integrity aggregator ゆえ残置。
#  59+72 は ESLint producer/consumer pair ゆえ残置。43 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_structural_ci as _checks_structural_ci
_checks_structural_ci.run(_ctx)

# ── 45. This file's self-documentation matches its implementation (BLOCKING) ──
# Two hand-maintained descriptions of the check set live in this file: the numbered
# inventory inside the module docstring ("N. ...") and the numbered section-header
# comments in the code body ("# ── N."). They are currently in agreement, but nothing
# stops them from drifting — e.g. a future check added to the body whose inventory line
# is forgotten, or a renumber applied on one side only. If they drift, this file's own
# documentation starts lying about what it enforces, and no other check notices. This
# meta-check makes their agreement an invariant.
#
# Why this is not circular reasoning: we deliberately parse the docstring and the body
# SEPARATELY and compare them to EACH OTHER. The check passes only when the two
# independent descriptions coincide; it cannot pass by "describing itself", because
# Check 45 must appear as a line in BOTH the docstring inventory AND as a body section
# header to be counted on both sides. The assertion is about structural agreement of the
# documentation, never about the behaviour of any individual check.
#
# We read the check source files from disk (not via introspection) so the check sees exactly
# the committed bytes a reviewer would read. CHECK_SOURCE_FILES lets the inventory/section
# bijection span multiple modules once check.py is split into cohesive files.
_inv45, _sec45 = _aggregate_check_numbers()
if _inv45 or _sec45:
    def _contiguous(seq):
        # True when seq is exactly [1, 2, ..., max] with no gaps and no duplicates.
        return bool(seq) and seq == list(range(1, seq[-1] + 1))

    # 45a — the docstring inventory is a clean contiguous 1..N with no gaps/dupes.
    check(_contiguous(_inv45),
          f"Check 45a: docstring check inventory is contiguous 1..{_inv45[-1] if _inv45 else 0} "
          "(no gaps or duplicate numbers)",
          f"Check 45a: docstring check inventory is not a clean 1..N sequence ({_inv45}) — "
          "a check number is missing, duplicated, or out of order in the module docstring",
          blocking=True)
    # 45b — the body section headers are a clean contiguous 1..N with no gaps/dupes.
    check(_contiguous(_sec45),
          f"Check 45b: code section headers are contiguous 1..{_sec45[-1] if _sec45 else 0} "
          "(no gaps or duplicate numbers)",
          f"Check 45b: code section headers are not a clean 1..N sequence ({_sec45}) — "
          "a '# ── N.' header is missing, duplicated, or out of order in the code body",
          blocking=True)
    # 45c — the two descriptions agree: same set of check numbers on both sides.
    check(set(_inv45) == set(_sec45),
          f"Check 45c: docstring inventory and code section headers describe the same "
          f"{len(_sec45)} checks (self-documentation matches implementation)",
          "Check 45c: docstring inventory and code section headers have drifted apart — "
          f"only in docstring: {sorted(set(_inv45) - set(_sec45))}; "
          f"only in code body: {sorted(set(_sec45) - set(_inv45))}",
          blocking=True)
else:
    check(False, "",
          "Check 45: could not locate this file's module docstring to self-verify "
          "documentation/implementation agreement",
          blocking=True)

# ── 47 / 56 / 57 / 61. main.js ⇄ js/ leaf-module ESM contract & factory coherence → checks_esm.py ──
# (check.py split track・category "ESM contract". These four Checks share the `_modules47`
#  leaf-module source-of-truth list + `_main_src47` (main.js source); extracting the list together
#  with all its consumers (47 import/export bijection・56 factory params・57 modulepreload set・61
#  factory docstring) resolves the coupling that kept them in the monolith through Phase 5. Executed
#  at 47's original position; 56/57/61 now run adjacent to 47 rather than interleaved with 53-60 —
#  order-independent since each Check only appends to the shared errors/warnings. CHECK_SOURCE_FILES
#  registration makes self-integrity 45/70/105 aggregate across this module.)
import checks_esm as _checks_esm
_checks_esm.run(_ctx)

# ── 48-51. structural / CI wiring / tooling checks → checks_structural.py ──────
# (check.py split track. 元の実行位置=47 の後・53 の前を保持して ctx で呼ぶ。CHECK_SOURCE_FILES 登録で
#  自己整合 Check 45/70/105 が横断集約。48-51 は _NN 接尾辞 local + file fresh read の self-contained cluster。
#  47/56/57/61 (_modules47 共有クラスタ) は checks_esm.py へ抽出済 (直上)。)
import checks_structural as _checks_structural
_checks_structural.run(_ctx)

# ── 59/60/72. ESLint warning-baseline & file-size-budget governance (producer/consumer trio) → checks_eslint_budget.py ──
# (check.py split track. 59=file-size-budget §2↔§4 集合(PRODUCER of _bsrc59/_budget59)/60=ESLint warning
#  baseline(ADVISORY・consumer)/72=ESLint absolute-ceiling(consumer)。59 が _bsrc59/_budget59 を定義し 60/72 が
#  消費する full-set 一括抽出(部分 slice は _budget59 NameError で crash)。59 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_eslint_budget as _checks_eslint_budget
_checks_eslint_budget.run(_ctx)

# ── 62-69. AIO entity/crawler identity + CI/config governance → checks_aio_config.py ──
# (check.py split track. AIO entity canonical_url(62)/crawler origin(63)/check-map uniqueness(64)/
#  doc Last-Updated(65)/title entity-id(66)/workflow permissions(67)/dependabot(68)/engines.node(69)。
#  連続 self-contained・各 Check 自前 read。72(ESLint baseline)は _bsrc59 共有で 59+72 pair ゆえ残置。
#  62 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_aio_config as _checks_aio_config
_checks_aio_config.run(_ctx)

# ── 70. total-check-runbook.md §9 check-count cross-reference (BLOCKING) ──────
# docs/architecture/total-check-runbook.md §9 の「consistency Check 総数」行に記述された
# Check 件数 (`**N**`) が、check_repository_consistency.py の実際の Check 番号最大値と
# 一致することを機械強制する。Check 45 が docstring inventory ↔ section header の bijection
# を見るのに対し、本 Check は「実装ファイル ↔ runbook §9」の cross-document 整合性を担う。
# 新 Check 追加時に runbook を更新し忘れる drift を pre-commit で構造的に閉じる。
_runbook70 = ROOT / "docs" / "architecture" / "total-check-runbook.md"
if _runbook70.exists() and CHECK_SOURCE_FILES:
    _, _section_nums70 = _aggregate_check_numbers()
    _actual_max70 = max(_section_nums70) if _section_nums70 else 0
    _runbook_src70 = _runbook70.read_text(encoding="utf-8")
    _runbook_match70 = re.search(r"consistency Check 総数\s*\|\s*\*\*(\d+)\*\*", _runbook_src70)
    _runbook_n70 = int(_runbook_match70.group(1)) if _runbook_match70 else 0
    check(
        _runbook_n70 == _actual_max70 and _actual_max70 > 0,
        f"Check 70: total-check-runbook.md §9 records {_runbook_n70} checks == implementation max {_actual_max70}",
        f"Check 70: total-check-runbook.md §9 records {_runbook_n70} but implementation has {_actual_max70}. "
        f"runbook §9 の「consistency Check 総数」を `**{_actual_max70}**` に同期せよ",
    )
else:
    warnings.append("Check 70: runbook or check script not found — count cross-reference skipped")

# ── 74-80. dev-tooling / .claude config-file integrity checks → checks_tooling.py ──
# (check.py split track・category "dev-tooling/.claude config". _lib_io helper API (74) /
#  incident README inventory (75) / .claude settings baseline (76) / commands (77) / agents (78)
#  frontmatter / .mcp.json parsability (79) / skills SKILL.md frontmatter (80). Contiguous
#  self-contained cluster — each Check reads its own target file directly (no global content dep),
#  so no ctx enrich needed. 元の実行位置 (73 の後・81 の前) を保持。CHECK_SOURCE_FILES 登録で
#  自己整合 Check 45/70/105 が横断集約。)
import checks_tooling as _checks_tooling
_checks_tooling.run(_ctx)


# ── 81-90. AIO entity / employer-Organization cross-surface coherence → checks_entity.py ──
# (check.py split track・category "entity/Organization". WebP XMP (81) / MP3 ID3 (82) binary
#  Organization fields / aio-manifest affiliation (83) + entity full-set (86) / README (84) /
#  Claude2Claude (85) Organization mention / CLAUDE.md cold-start entity (87) / LICENSE (88) /
#  governance-file presence (89) / .claude entity (90). Contiguous self-contained cluster —
#  READ-ONLY presence assertions reading their own target files directly (no global content dep,
#  no C6 edit). 元の実行位置 (80 の後・91 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_entity as _checks_entity
_checks_entity.run(_ctx)


# ── 91-95. AIO C6 derived-value & date-sync tooling integrity → checks_aio_derived.py ──
# (check.py split track・category "AIO derived-value". binary date freshness (91) / C6 canon
#  presence (92) / manifest last_metadata_update (93) / update_aio tools integrity (94) /
#  _lib_io date helpers (95). Contiguous self-contained cluster — READ-ONLY assertions reading
#  their own files directly (no global content dep, no C6 edit). 元の実行位置 (90 の後・96 の前)
#  を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_aio_derived as _checks_aio_derived
_checks_aio_derived.run(_ctx)


# ── 96-99. docs/files 1-to-1 mirror-doc governance → checks_docs_mirror.py ──
# (check.py split track・category "docs-mirror". shipped-code 1-to-1 docs bijection (96) /
#  frontmatter integrity (97) / 5-axis section presence (98) / README + _template presence (99).
#  Contiguous self-contained cluster reading docs/files/** directly (no global content dep).
#  Check 108 (full tracked-files bijection) は非連続ゆえ monolith 残置。元の実行位置 (95 の後・
#  100 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_docs_mirror as _checks_docs_mirror
_checks_docs_mirror.run(_ctx)


# ── 100/102/104/106/107/109/112/113. canon-policy / config / meta-governance → checks_canon_config.py ──
# (check.py split track. theme-init keys(100)/operating-model canon(102)/py 3.10 guard(104)/nvmrc(106)/
#  runbook §11 CI(107)/check-count drift(109)/IME guard(112)/commit-PR discipline(113)。連続 self-contained。
#  100 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_canon_config as _checks_canon_config
_checks_canon_config.run(_ctx)

# ── 105. check-repository-consistency-map.md ↔ implementation bijection (BLOCKING) ─
# check-repository-consistency-map.md is the human-facing inventory of every Check. It is
# hand-maintained in parallel with the implementation, so it can silently fall behind when a
# Check is added but the map row is forgotten (or vice-versa). Check 45 already guards the
# docstring↔section bijection WITHIN this file; this is its cross-document counterpart. We
# extract the integer check-numbers from the map's table rows (`| N |` / `| Na |`, alpha
# sub-checks normalized to their integer) and from this file's `# ── N.` section headers,
# and require the two sets to coincide exactly — so the inventory a reviewer reads can never
# drift from what the script actually enforces.
_map105 = ROOT / "docs" / "architecture" / "check-repository-consistency-map.md"
if _map105.exists() and CHECK_SOURCE_FILES:
    _mapsrc105 = _map105.read_text(encoding="utf-8")
    _map_nums105 = {int(m) for m in re.findall(r"^\|\s*(\d+)[a-z]?\s*\|", _mapsrc105, re.MULTILINE)}
    _, _impl_sec105 = _aggregate_check_numbers()
    _impl_nums105 = set(_impl_sec105)
    _only_map105 = sorted(_map_nums105 - _impl_nums105)
    _only_impl105 = sorted(_impl_nums105 - _map_nums105)
    check(
        bool(_impl_nums105) and _map_nums105 == _impl_nums105,
        f"Check 105: check-repository-consistency-map.md documents exactly the {len(_impl_nums105)} implemented checks (map ↔ implementation bijection)",
        f"Check 105: check-map and implementation have drifted — only in map: {_only_map105}; "
        f"missing a map row (implemented but undocumented): {_only_impl105}. "
        "新 Check 追加時に map へ行を足し忘れる drift を防ぐ (Check 45 の docstring↔section bijection の cross-document 版)",
        blocking=True,
    )
else:
    check(False, "", "Check 105: check-map or implementation script not found — bijection を検証できない", blocking=True)

# ── 108/122. tracked-files mirror bijection + private-document guard → checks_tracked_files.py ──
# (check.py split track・ctx-enrich _member_paths。108=docs/files mirror↔tracked-files FULL bijection /
#  122=private-source-document guard。両者とも setup-global _member_paths(Phase 46 で 37 から setup 領域へ
#  移設し _ctx._member_paths attach)を消費。Check 37(artifact scan)は FORBIDDEN 定数も使うため残置。
#  108 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_tracked_files as _checks_tracked_files
_checks_tracked_files.run(_ctx)

# ── 110/111/114/116/117. e2e / Playwright test-infra hygiene → checks_e2e_infra.py ──
# (check.py split track・category "e2e/test-infra". A11Y_ROUTES↔ALL_ROUTES (110) / no-networkidle
#  (111) / no-.only (114) / reuseExistingServer=false (116) / screenshot tolerance ceiling (117)。
#  非連続クラスタ (112 IME / 113 canon / 115 CSP は monolith 残置)。各 Check は e2e spec /
#  playwright.config を自前 read_text (no global content dep)。110 位置で連続実行 (order-independent)。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_e2e_infra as _checks_e2e_infra
_checks_e2e_infra.run(_ctx)

# ── 118-120. shipped-JS structural coherence & byte budget → checks_shipped_structure.py ──
# (check.py split track・category "shipped structure". PAGE_META route coverage (118) / factory
#  docstring dependency coherence (119) / shipped JS+CSS byte-weight budget (120)。連続 self-
#  contained クラスタ (free-var 分析で外部 _var ゼロ確認)・自前 read_text (no global content dep)。
#  元の実行位置 (117 の後・121 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_shipped_structure as _checks_shipped_structure
_checks_shipped_structure.run(_ctx)


# ── 123/124/125/126/127. shipped-JS/AIO safety guards — operating-model coherence / anonymity / dead-const / ESLint safety-net / digest re-bake guard (123-127) → checks_safety_guards.py ──
# (check.py split track. 連続/非連続 self-contained クラスタ・各 Check 自前 read。123 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_safety_guards as _checks_safety_guards
_checks_safety_guards.run(_ctx)

# ── 128-131, 373, 374. shipped-JS behavioral regression guards → checks_behavioral.py ──
# (check.py split track・category "behavioral guards". command-palette↔router coherence (128) /
#  topbar data-action double-fire (129) / live-input oninput focus-loss (130) / sw
#  decodeURIComponent try/catch (131) / store default-appsData field ⟹ normalizeAppsData preserve
#  round-trip (373・quizSearch reload persist drop fix) / settings importJSON normalize-before-adopt
#  ingestion guard (374)。各 Check は shipped-JS (js/*.js / main.js / sw.js) を自前 read_text
#  (no global content dep)。元の実行位置 (127 の後・132 の前) を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_behavioral as _checks_behavioral
_checks_behavioral.run(_ctx)


# ── 132-134. shipped-asset & AIO wiring / discoverability → checks_wiring.py ──
# (check.py split track・category "wiring/discovery". AIO evidence↔sitemap discoverability (132) /
#  aio-guard.js script wiring (133) / root-script wiring completeness (134)。連続 self-contained
#  クラスタ (free-var ゼロ確認)・自前 read_text (no global content dep)。135 (stylesheet wiring) は
#  global style 依存ゆえ monolith 残置。元の実行位置 (131 の後・135 の前) を保持。CHECK_SOURCE_FILES 登録。)
import checks_wiring as _checks_wiring
_checks_wiring.run(_ctx)


# ── 136-140. app-route whitelist coherence-mesh → checks_app_route.py ──
# (check.py split track・category "app-route mesh". js/router.js の app whitelist を single
#  source of truth に、demoRoute (136) / main.js render switch (137) / Sidebar app-nav (138) /
#  AppsPage app index (139) / Settings demo selector (140) の全 producer/consumer 整合を強制。
#  連続 self-contained クラスタ — 各 Check は対象 file を自前 read_text (no global content dep)。
#  元の実行位置 (135 の後・141 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_app_route as _checks_app_route
_checks_app_route.run(_ctx)


# ── 142-145. CI / workflow-coverage & supply-chain hardening → checks_ci_supply.py ──
# (check.py split track・category "CI/supply-chain". Playwright e2e gate covers its toolchain
#  (142) / auto-digest workflow covers every digested manifest file (143) / digest-regen tool
#  file-map == manifest (144) / GitHub Actions full-SHA pin (145). Contiguous self-contained
#  cluster reading workflow YAML / tool / manifest directly (no global content dep). 元の実行
#  位置 (141 の後・146 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_ci_supply as _checks_ci_supply
_checks_ci_supply.run(_ctx)


# ── 146-148 / 304-309. residual project/Speakable/route + theme-color/sitemap/manifest → checks_residual_coherence.py ──
# (check.py split track. 2 小 self-contained 群: 146(relatedProjectIds)/147(Speakable selectors)/
#  148(ARTICLE_ROUTES⊆PAGE_META) + 304-305(theme-color)/307-308(sitemap XML)/309(manifest HTTPS)。
#  146 位置で list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_residual_coherence as _checks_residual_coherence
_checks_residual_coherence.run(_ctx)

# ── 149-166 (minus 152). AIO/SEO meta + canonical URL + resource-resolution coherence → checks_seo_meta.py ──
# (check.py split track. canonical-URL/og·twitter meta/SEO baseline/resource resolve の 17 Check。連続
#  self-contained (152 は checks_html.py へ抽出済ゆえ除外)。各 Check は対象 file を自前 read。149 位置で
#  list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_seo_meta as _checks_seo_meta
_checks_seo_meta.run(_ctx)

# ── 167-173. AIO manifest entity-field & identity coherence → checks_aio_entity.py ──
# (check.py split track・category "AIO entity coherence". aio-monitoring schedule (167) /
#  entity.architecture C1/C2/C3 (168) / entity.role (169) / disambiguation (170) / ai:* meta
#  canonical prefix (171) / entity name variants (172) / identity.js AUTHOR values (173)。連続
#  self-contained クラスタ (annotation-aware free-var 分析でゼロ確認・READ-ONLY・no global content dep)。
#  元の実行位置 (166 の後・174 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_aio_entity as _checks_aio_entity
_checks_aio_entity.run(_ctx)


# ── 175-180. index.html meta/asset URL resolution & AIO routing coherence checks (175-180) → checks_meta_url.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_meta_url as _checks_meta_url
_checks_meta_url.run(_ctx)


# ── 181-189 (minus 187). SEO/AIO date-ISO + URL-resolution + HTTPS/meta baseline → checks_seo_baseline.py ──
# (check.py split track. LAST_UPDATED ISO(181)/ai:* URL resolve(182)/sitemap lastmod(183)/sw AIO_FILES(184)/
#  canonical HTTPS(185)/meta author(186)/robots Sitemap resolve(188)/meta robots(189)。連続 self-contained。
#  187 は checks_html.py 抽出済・190 は setup-global _assets 依存ゆえ残置。181 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_seo_baseline as _checks_seo_baseline
_checks_seo_baseline.run(_ctx)

# ── 191-200. JSON-LD Person/WebSite/WebPage/Organization canonical entity coherence checks (191-200) → checks_jsonld_entity.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_jsonld_entity as _checks_jsonld_entity
_checks_jsonld_entity.run(_ctx)


# ── 202-214. canonical URL, HTTPS-only & manifest/icon path coherence checks (202-214) → checks_canonical_https.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_canonical_https as _checks_canonical_https
_checks_canonical_https.run(_ctx)


# ── 216-219. JSON-LD referential integrity checks — @id refs resolve / @id unique / datePublished<=dateModified / manifest paths (216-219) → checks_jsonld_refs.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 1 箇所。)
import checks_jsonld_refs as _checks_jsonld_refs
_checks_jsonld_refs.run(_ctx)


# ── 221-235. JSON-LD ref-type + meta length + sitemap value coherence checks (221-235) → checks_jsonld_meta.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 1 箇所。)
import checks_jsonld_meta as _checks_jsonld_meta
_checks_jsonld_meta.run(_ctx)


# ── 236/238/266/267/268. shipped-JS content-scan + JSON-LD length checks (236/238/266/267/268) → checks_shipped_content.py ──
# (check.py split track. 連続/非連続 self-contained クラスタ・各 Check 自前 read。236 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_shipped_content as _checks_shipped_content
_checks_shipped_content.run(_ctx)

# ── 237/239/240/241/262-265/269-272/310. shipped-JS static analysis + byte budgets → checks_shipped_static.py ──
# (check.py split track. shipped-JS lint(237/239-241/262-265)+ byte budgets(269-272)+ total weight(310)。
#  非連続 tightly-coupled unit・共有: glob import(_glob237)/_eval_targets239 list/_HERO_WEBP269·_BGM_MP3_269。
#  310 は 269 の binary path を消費するため同梱(部分 slice は 2 度 crash)。238/266-268 は非使用で残置。
#  237 位置で list 順に連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_shipped_static as _checks_shipped_static
_checks_shipped_static.run(_ctx)

# ── 242-249, 366-368. shipped-JS/HTML security & hygiene checks — eval/setTimeout-string/document.write/console/loose-eq etc. (242-249, 366-368) → checks_shipped_hygiene.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 3 箇所。)
import checks_shipped_hygiene as _checks_shipped_hygiene
_checks_shipped_hygiene.run(_ctx)


# ── 251-254. service-worker & PWA registration + potentialAction structure checks (251-254) → checks_sw_pwa.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 1 箇所。)
import checks_sw_pwa as _checks_sw_pwa
_checks_sw_pwa.run(_ctx)


# ── 256-261. JSON-LD primary-node required-field completeness checks — WebPage/Person/WebSite/Org/hero/BGM (256-261) → checks_jsonld_primary.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 6 箇所。)
import checks_jsonld_primary as _checks_jsonld_primary
_checks_jsonld_primary.run(_ctx)


# ── 273-287 / 288-302. AIO/SEO cross-surface URL/canonical/format coherence → checks_seo_coherence.py + _b.py ──
# (module 自身が 30-check で >1,000 行だったため 273-287(part A)/288-302(part B)の 2 module に分割し各 ≤1,000 に)
# (check.py split track・category "SEO/URL coherence". canonical URL / HTTPS-only / manifest↔JSON-LD
#  entity equality / strict format (VERSION/CACHE_NAME/manifest_version) / og/twitter/meta coherence の
#  30 Check。連続 self-contained (annotation+def-aware free-var 分析でゼロ確認・READ-ONLY)。nested walker の
#  section-local accumulator は module-level の global を run() 内で nonlocal に機械変換 (意味等価)。
#  元の実行位置 (272 の後・303 の前) を保持。CHECK_SOURCE_FILES 登録で横断集約。)
import checks_seo_coherence as _checks_seo_coherence
_checks_seo_coherence.run(_ctx)
import checks_seo_coherence_b as _checks_seo_coherence_b
_checks_seo_coherence_b.run(_ctx)


# ── 311-320. sitemap & manifest format/validity coherence checks (311-320) → checks_sitemap_manifest.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_sitemap_manifest as _checks_sitemap_manifest
_checks_sitemap_manifest.run(_ctx)


# ── 324-337. index.html standards/safety hygiene + webmanifest + asset integrity checks (324-337) → checks_html_standards.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_html_standards as _checks_html_standards
_checks_html_standards.run(_ctx)


# ── 338/339/340/348. binary asset dimension/format + gate-workflow trigger checks (338/339/340/348) → checks_binary_dims.py ──
# (check.py split track. 連続/非連続 self-contained クラスタ・各 Check 自前 read。338 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_binary_dims as _checks_binary_dims
_checks_binary_dims.run(_ctx)

# ── 341-343. og/twitter meta non-empty + robots safety + .well-known JSON validity checks (341-343) → checks_meta_validity.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_meta_validity as _checks_meta_validity
_checks_meta_validity.run(_ctx)


# ── 345-347. CI verification-chain wiring checks — verify layers / consistency guard / behavior e2e gate (345-347) → checks_ci_verify.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_ci_verify as _checks_ci_verify
_checks_ci_verify.run(_ctx)


# ── 351-355. shipped-JS security + CSP script authorization checks — sitemap loc / innerHTML fail-closed / DOMParser absence / script-src+connect-src host authz (351-355) → checks_csp_security.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_csp_security as _checks_csp_security
_checks_csp_security.run(_ctx)


# ── 357-359. shipped-asset resolution wiring checks — preload href / sitemap image:loc + og:image / BGM audio (357-359) → checks_asset_resolve.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_asset_resolve as _checks_asset_resolve
_checks_asset_resolve.run(_ctx)


# ── 361-364. maintainability/test-health checks → checks_maintainability.py ──
# (extracted Phase 1 PoC. Registered in CHECK_SOURCE_FILES so self-integrity Checks 45/70/105
#  aggregate its inventory + sections. Runs here — same position/order as before — via ctx.)
import checks_maintainability as _checks_maintainability
_checks_maintainability.run(_ctx)

# ── Result ────────────────────────────────────────────────────────────────────
print()
if errors:
    print(f"REPOSITORY CONSISTENCY CHECK FAILED — {len(errors)} error(s):")
    for e in errors:
        print(f"  ::error::{e}")
    sys.exit(1)

if warnings:
    print(f"Repository consistency check passed with {len(warnings)} warning(s).")
else:
    print("Repository consistency check passed — all invariants hold.")

sys.exit(0)
