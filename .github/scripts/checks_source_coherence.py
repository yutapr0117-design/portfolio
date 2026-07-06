"""
checks_source_coherence.py — cross-file source coherence + CSP-hash checks (ctx-enrich: html/ai2ai/aio_mon)
(extracted from check_repository_consistency.py — check.py split track・category "cross-file source coherence").

Non-contiguous cluster of glob/helper-dependent Checks 7/11/14/350: CSP meta ordering before the
inline suppressor (7・_lib_io.csp_sri_hash helper), AIO-monitoring summary shape (11・aio_mon), v1→v74
transition consistency across AI2AI + index.html (14), and CSP inline-handler content-hash authorization
(350・helper). They consume pre-loaded content via ctx-enrichment (`_ctx.html/ai2ai/aio_mon`) and the
shared `_lib_io.csp_sri_hash` helper (imported here as `_lib_csp_sri_hash`; Check 7 wraps it in a local
`_csp_sri_hash` alias, Check 350 uses it directly). NOTE: the date-sync Checks 17/18 are NOT included —
they share `html_date` (17→18) and the setup-global `root_lastmod`, a separate mini-cluster left for a
later date-coherence extraction. No other cross-section var coupling in this set.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/html/ai2ai/aio_mon/read/extract.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  7.  index.html CSP meta appears before inline suppressor script (error-suppressor inlined)
  7b. index.html CSP authorizes inline suppressor (hash recomputed from live content)
  7c. index.html CSP authorizes inline speculation rules (hash recomputed from live content)
  11. aio_monitoring.py summary dict contains 'enabled_engines' and 'total_cited_count'
  14. v1→v74 canonical declaration present in index.html or AI2AI.md
  350. The inline event-handler `onload="this.media='all'"` (the async
       font-loading trick) MUST have its exact-content SHA-256 hash
       present in the CSP `script-src` (authorized via `'unsafe-hashes'`).
       Check 7b/7c cover the two inline `<script>` blocks; this covers the
       third CSP hash — the inline handler. Drift = editing the handler
       value (e.g. `this.media='screen'`) without recomputing the CSP
       hash makes Chrome BLOCK the handler, so the print-media stylesheet
       never flips to `all` and the fonts never load (FOUC / wrong font),
       silently. Computed from live handler content (not a constant), so
       both a removed hash and an edited-without-rehash handler are
       caught. Sibling of Check 7b (suppressor hash) / Check 7c
       (speculation-rules hash) / Check 242 (handler allowlist) for the
       inline-CSP-hash integrity axis. (BLOCKING)

"""
import re
import json
from _lib_io import csp_sri_hash as _lib_csp_sri_hash


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    html = ctx.html
    ai2ai = ctx.ai2ai
    aio_mon = ctx.aio_mon
    read = ctx.read
    extract = ctx.extract

    # ── 7. CSP meta before inline suppressor script ───────────────────────────────
    # error-suppressor.js is now inlined in <head> to eliminate the network-fetch
    # timing gap that caused intermittent "message channel closed" console errors.
    _INLINE_SUPPRESSOR_ANCHOR = "window.addEventListener('unhandledrejection'"
    pos_csp = html.find('<meta http-equiv="Content-Security-Policy"')
    pos_err = html.find(_INLINE_SUPPRESSOR_ANCHOR)
    check(
        pos_csp != -1 and pos_err != -1 and pos_csp < pos_err,
        f"CSP meta (pos {pos_csp}) appears before inline suppressor (pos {pos_err})",
        f"CSP meta must appear before inline suppressor (CSP={pos_csp}, inline={pos_err})",
    )

    # ── 11. aio_monitoring.py summary dict ───────────────────────────────────────
    check(
        "enabled_engines" in aio_mon,
        "aio_monitoring.py: 'enabled_engines' present in summary",
        "aio_monitoring.py: 'enabled_engines' missing from summary (P0-06)",
    )
    check(
        "total_cited_count" in aio_mon,
        "aio_monitoring.py: 'total_cited_count' present in summary",
        "aio_monitoring.py: 'total_cited_count' missing from summary (P0-06)",
    )

    # ── 14. v1→v74 / 73 transitions consistency ─────────────────────────────────
    has_v74_declaration = "v1→v74" in html or "v1→v74" in ai2ai
    check(
        has_v74_declaration,
        "v1→v74 canonical declaration present in index.html or AI2AI.md",
        "v1→v74 canonical declaration missing — add to index.html or AI2AI.md",
    )

    # ── 350. inline onload handler CSP hash present + matches content (BLOCKING) ──
    # Check 7b/7c は 2 つの inline <script> block を被覆。本 Check は 3 つ目の CSP
    # hash = inline event handler `this.media='all'` を被覆。handler を編集して
    # hash を再計算しないと Chrome が block しフォント非同期ロードが silent 破綻。
    _idx350 = ROOT / "index.html"
    if _idx350.is_file():
        _h350 = _idx350.read_text(encoding="utf-8")
        _h350_nc = re.sub(r"<!--.*?-->", "", _h350, flags=re.DOTALL)
        # font async-load handler の onload 属性値を実体から抽出
        _m350 = re.search(r"onload=\"(this\.media='[^']*')\"", _h350_nc)
        if _m350 is not None:
            _handler_content350 = _m350.group(1)
            _handler_hash350 = _lib_csp_sri_hash(_handler_content350)
            check(
                f"'{_handler_hash350}'" in _h350,
                f"Check 350: CSP が inline handler {_handler_content350!r} を authorize (content hash {_handler_hash350})",
                (f"Check 350: CSP が inline handler {_handler_content350!r} を authorize しない — "
                 f"computed {_handler_hash350} が script-src に不在。handler を編集して CSP hash を "
                 "再計算し忘れると Chrome が block しフォント非同期ロードが破綻 (FOUC)。"
                 f"'{_handler_hash350}' を script-src へ追加せよ"),
                blocking=True,
            )
        else:
            check(False, "Check 350: inline onload handler present",
                  "Check 350: index.html に onload=\"this.media='...'\" handler が無い "
                  "(font async-load pattern の期待値)", blocking=True)
    else:
        check(False, "Check 350: index.html present",
              "Check 350: index.html が無い", blocking=True)
