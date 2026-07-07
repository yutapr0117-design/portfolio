"""
checks_shipped_structure.py — shipped-JS structural coherence & byte-weight budget checks
(extracted from check_repository_consistency.py — check.py split track・category "shipped structure").

This module owns the contiguous cluster of Checks 118-120 that guard the shipped-JS module
structure and asset size: PAGE_META route coverage (118), factory docstring dependency coherence
(119), and the shipped JS+CSS byte-weight budget (120). Each Check reads its own target files
directly (main.js, js/*.js, style.css) via Path.read_text(); none depends on the monolith's
global html/style/mainjs content, and a free-variable analysis confirms zero external `_`-vars,
so the cluster is self-contained and needs no ctx enrichment.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  118. PAGE_META route coverage: every shipped route in e2e ALL_ROUTES (normalized, the curated
       shipped-route authority tied to main.js by Check 58) must have a PAGE_META entry in
       js/page-meta.js. A route missing from PAGE_META makes applyMeta early-return, so that
       route ships with no <title>/description/JSON-LD — a silent AIO/SEO gap on the project's
       #1 mission. Closes the PAGE_META ↔ ALL_ROUTES ↔ main.js coherence triangle. (BLOCKING)
  119. factory docstring dependency coherence: every dependency a leaf factory
       `createX({ ...deps })` destructures from its argument must appear in that file's
       【依存（引数で注入）】 docstring section. Guards the factory-docstring-dep drift class
       hand-fixed in Session #20 (aidk-rails/apps/components/pages each had injected deps the
       docstring omitted). The docstring is the next AI's onboarding substrate (low onboarding
       cost = a pillar of token-sustained autonomy); a signature/docstring divergence makes the
       next AI read a wrong dependency contract — an onboarding tax that degrades the flywheel.
       Dep names are matched on word boundaries to avoid single-char (`h`) false positives.
       (BLOCKING)
  120. shipped JS+CSS byte-weight budget: the total bytes of the browser-downloaded payload
       (main.js + js/**/*.js + style.css) must stay <= the PERF-BUDGET-DATA ceiling in
       file-size-budget.md. §3(B) made the pixel screenshot advisory, thinning real page-weight
       protection; this byte-weight guard restores it on a different axis from Check 52's
       line-count budget (byte ≠ line). Catches runaway bloat (e.g. a huge file committed by
       mistake) that would inflate download/parse cost (LCP/CWV). Legitimate feature growth
       ratchets the ceiling up with a rationale, like the ESLint baseline. (BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 118. PAGE_META route coverage (BLOCKING) ──────────────────────────────────
    # 全 shipped route が js/page-meta.js の PAGE_META に metadata を持つことを保証する。route が
    # PAGE_META に無いと applyMeta が early-return し title/desc/JSON-LD が出ない silent AIO/SEO gap に
    # なる。shipped route 集合は e2e の ALL_ROUTES (Check 58 が main.js と結ぶ curated 権威) の name を
    # 正規化して用い、PAGE_META keys が全 route を網羅する (⊇) ことを機械強制する。
    _pm118 = ROOT / "js" / "page-meta.js"
    # ALL_ROUTES は e2e spec のテーマ別分割 (2026-07-07) で security-proxy.spec.js に移動したため、
    # e2e/*.spec.js 全体を連結して ALL_ROUTES ブロックを切り出す。
    _specs118 = sorted((ROOT / "e2e").glob("*.spec.js"))
    if _pm118.exists() and _specs118:
        _pmsrc118 = _pm118.read_text(encoding="utf-8")
        _pmkeys118 = set(re.findall(r"^\s*'?([a-z][a-z0-9-]*)'?\s*:\s*\{", _pmsrc118, re.MULTILINE))
        _ssrc118 = "\n".join(p.read_text(encoding="utf-8") for p in _specs118)
        _allm118 = re.search(r"const ALL_ROUTES\s*=\s*\[(.*?)\];", _ssrc118, re.DOTALL)
        _names118 = set(re.findall(r"name:\s*'([^']+)'", _allm118.group(1))) if _allm118 else set()
        _alias118 = {"not-found-fallback": "not-found"}
        _norm118 = {_alias118.get(n, n) for n in _names118}
        _missing118 = sorted(_norm118 - _pmkeys118)
        check(
            bool(_pmkeys118) and bool(_norm118) and not _missing118,
            f"Check 118: PAGE_META が全 {len(_norm118)} shipped route の metadata を網羅 (route 毎 AIO/SEO)",
            f"Check 118: PAGE_META に metadata 欠落の route: {_missing118} — applyMeta が early-return し title/desc/JSON-LD が出ない。js/page-meta.js に追加せよ",
            blocking=True,
        )
    else:
        check(False, "", "Check 118: js/page-meta.js または e2e/*.spec.js が見つからない — PAGE_META 網羅を検証できない", blocking=True)

    # ── 119. factory docstring dependency coherence (BLOCKING) ────────────────────
    # 各葉モジュールの factory `createX({ ...deps })` が引数で受け取る依存名のすべてが、その
    # ファイル冒頭 docstring の【依存（引数で注入）】節に列挙されていることを機械強制する。これは
    # Session #20 で手修正した factory docstring の依存 drift (aidk-rails に Theme/BGM/secureExternalLinks/
    # openDrawer/closeDrawer、apps に Storage、components に tokenize/CONSTANTS/clear/closeDrawer、pages に
    # ContactCTA が署名にあるのに docstring から欠落していた) の class を再発防止するもの。docstring は
    # 次の AI の onboarding substrate（低 onboarding コスト = トークン持続性の柱）であり、署名と docstring
    # の乖離は次の AI に誤った依存契約を読ませる onboarding 税＝flywheel 劣化要因。署名から派生して照合する
    # ことで「依存を増やしたのに docstring 更新を忘れた」drift を pre-commit で BLOCKING 検出する。
    # 照合は dep 名を word-boundary で 【依存】節テキストに探す (単一文字 dep `h` の部分一致誤検出を回避)。
    _dep_problems119 = []
    _checked119 = 0
    for _facfile119 in sorted((ROOT / "js").glob("*.js")):
        _facsrc119 = _facfile119.read_text(encoding="utf-8")
        _facm119 = re.search(r"export function create\w+\(\{\s*([^}]*?)\}\)", _facsrc119)
        if not _facm119:
            continue  # 依存注入 factory でないファイル (純データ等) は対象外
        _checked119 += 1
        _deps119 = [d.strip() for d in _facm119.group(1).replace("\n", " ").split(",") if d.strip()]
        _secm119 = re.search(r"【依存[^】]*】(.*?)(?:【|\*/)", _facsrc119, re.DOTALL)
        _sectext119 = _secm119.group(1) if _secm119 else ""
        _miss119 = [d for d in _deps119
                    if not re.search(r"(?<![\w$])" + re.escape(d) + r"(?![\w$])", _sectext119)]
        if _miss119:
            _dep_problems119.append(f"{_facfile119.name}: docstring【依存】節に欠落 {_miss119}")
    check(
        not _dep_problems119,
        f"Check 119: 全 {_checked119} factory の docstring【依存】節が署名の注入依存を網羅 (onboarding 精度 / flywheel 保護)",
        "Check 119: factory 署名の依存が docstring【依存】節に欠落 (依存契約 drift): "
        + "; ".join(_dep_problems119)
        + " — 署名に dep を足したら同ファイルの【依存（引数で注入）】節にも追記せよ",
        blocking=True,
    )

    # ── 120. shipped JS+CSS byte-weight budget (BLOCKING) ─────────────────────────
    # ブラウザが download/parse する shipped payload (main.js + js/**/*.js + style.css) の合計バイト数が
    # file-size-budget.md の PERF-BUDGET-DATA ceiling 以下であることを機械強制する。§3(B) で screenshot を
    # advisory 化し pixel ゲートを外したため、別軸の実 page-weight 保護が薄くなった。これを byte-weight で
    # 補う。行数予算 (Check 52) とは別軸 (byte ≠ line) で、実 download/parse 負荷 (LCP/CWV に影響) を守り、
    # 巨大ファイル誤コミット等の runaway bloat を BLOCKING 捕捉する。ceiling は ESLint baseline 同様、正当な
    # 機能成長で超えたら rationale 付きでラチェット更新する運用 (PERF-BUDGET-DATA コメントに記録)。
    _budget120 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    _perf_m120 = re.search(r"<!--\s*PERF-BUDGET-DATA\s+(\d+)\s+-->", _budget120.read_text(encoding="utf-8")) if _budget120.exists() else None
    if _perf_m120:
        _ceiling120 = int(_perf_m120.group(1))
        _shipped120 = 0
        _files120 = [ROOT / "main.js", ROOT / "style.css"] + sorted((ROOT / "js").rglob("*.js"))
        for _f120 in _files120:
            if _f120.exists():
                _shipped120 += len(_f120.read_bytes())
        check(
            _shipped120 <= _ceiling120,
            f"Check 120: shipped JS+CSS byte-weight {_shipped120} <= budget {_ceiling120} (page-weight / CWV 保護)",
            f"Check 120: shipped JS+CSS byte-weight {_shipped120} が budget {_ceiling120} を超過 — "
            f"runaway bloat か正当な機能成長かを判断し、後者なら file-size-budget.md の PERF-BUDGET-DATA を "
            f"rationale 付きでラチェット更新せよ (byte ≠ line ゆえ Check 52 とは別軸の page-weight 保護)",
            blocking=True,
        )
    else:
        check(
            False,
            "Check 120: file-size-budget.md PERF-BUDGET-DATA marker present",
            "Check 120: file-size-budget.md に `<!-- PERF-BUDGET-DATA <N> -->` が無い — "
            "shipped JS+CSS の page-weight 保護が消失。marker を追加せよ",
            blocking=True,
        )
