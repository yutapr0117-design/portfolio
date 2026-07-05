"""
checks_css.py — style.css / CSS contract checks (glob-content: style)
(extracted from check_repository_consistency.py — check.py split track・category "CSS contract"・first ctx-enrich module).

Non-contiguous cluster of Checks 6/73/101/103/135/174/321/322/323/344/356 that read the pre-loaded
`style.css` content (the monolith's `style` global). This is the FIRST split module to consume a
shared global-content value via ctx-enrichment: the monolith attaches `_ctx.style = style` after the
globals load, and this module unpacks `style = ctx.style` in run(). Themes: forced-colors / HCM /
prefers-contrast a11y support (101/103), theme-color literals (174), a11y/CWV attribute contract
(73), @import absence / inline-style absence / @layer allowlist (321/322/323/344), Google-Fonts CSP
pair (356), and the design-token / stylesheet baseline (6/135). No other cross-section var coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/style by reference (exec 不使用), byte-equivalent.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  6.  style.css has no stale "Current release: v73" or "NEXT_PLANNED_RELEASE" markers
  73. index.html accessibility/CWV HTML-attribute contract: index.html の HTML 属性のみで
      完結する WCAG 2.2 / Core Web Vitals 契約を機械強制する。Playwright visual baseline
      不変が前提のため、pixel diff を発生させない HTML 属性のみを対象とする (現状の good
      practice を契約化して drift 防止): (73a) 全 <link rel="preload"> に as= 属性必須
      (preload 仕様で as 無指定は無効); (73b) 全 <img> 要素に alt= 属性必須 (WCAG 1.1.1
      Level A); (73c) hero 画像の preload に fetchpriority="high" 指定 (LCP 改善契約の
      固定)。Plan B の HTML 属性スコープを BLOCKING 化。(BLOCKING)
  101. style.css Windows High Contrast Mode (forced-colors) focus support: style.css contains a
       `@media (forced-colors: active)` block that restores a visible outline-based focus indicator
       for focus selectors. WHY: in forced-colors mode (Windows High Contrast Mode) box-shadow is
       NOT painted, so any focus indicator expressed only via box-shadow (e.g. `.skip-link:focus`,
       which sets `outline: none; box-shadow: var(--focus-ring)`) disappears, failing WCAG 2.4.7
       (Focus Visible) / 1.4.1 for HCM users. This Check locks in the forced-colors fallback so a
       future edit cannot silently strip it. The block is render-neutral (inert outside HCM), so it
       never affects the Playwright visual baseline — i.e. it is exempt from the §3 baseline gate.
       Discovered + systematized during the why-only comment-injection track (same pattern as
       Check 100). (BLOCKING)
  103. style.css prefers-contrast (higher-contrast preference) support: style.css contains a
       `@media (prefers-contrast: more)` block that strengthens borders / muted text / focus for
       users who request higher contrast (WCAG 1.4.11 Non-text Contrast 強化). Like Check 101
       (forced-colors), the block is render-neutral — inert unless the OS preference is active — so
       it never affects the Playwright visual baseline (§3 gate exempt). This Check locks in the
       higher-contrast fallback so a future edit cannot silently strip it. (BLOCKING)
  135. Stylesheet wiring: index.html must keep loading the local stylesheet style.css via a
       <link rel="stylesheet" href="./style.css">. This is the highest-impact member of the same
       "file exists ⟹ file wired" class as Checks 133/134 — if the link is removed, the ENTIRE site
       renders unstyled, yet the loss is silent to every gate: the behavior e2e only asserts content
       presence / routes (an unstyled page still has its text), the screenshot e2e is ADVISORY per
       §3(B), and no consistency check covered the link. style.css existence (Check 108 mirror) and
       byte-budget (Check 52/120) were enforced, but never its <link> wiring. External font
       stylesheets are intentionally NOT required (their loss degrades gracefully to fallback
       fonts). This makes "style.css exists ⟹ it is linked in index.html" an enforced invariant.
       (BLOCKING)
  174. `<meta name="theme-color">` values exist as literals in style.css: every theme-color content
       value in index.html (multiple media-scoped variants permitted) must appear as a literal
       string somewhere in style.css, ensuring the mobile address bar / OS card chrome color
       matches a real brand color present in the stylesheet. Drift silently desyncs the OS chrome
       from the visual brand (the address bar shows a color the site no longer uses anywhere).
       (BLOCKING)
  321. `style.css` MUST contain zero CSS `@import` statements. Boring
       Technology contract (C1) forbids external CSS library loading; an
       `@import url(...)` would pull an external stylesheet at parse time
       and introduce render-blocking network dependency + CSP surface
       expansion. Sibling of Check 1 (no external framework CSS `<link>`
       tags) / Check C1 baseline for the CSS surface no-external-load
       axis. (BLOCKING)

  322. `index.html` MUST contain zero inline `<style>` element blocks
       (single-stylesheet contract). Drift = a snippet of CSS crept into
       HTML, silently violating:
       (a) the "single canonical style.css" invariant used by Check 52
           (byte budget) / Check 174 (theme-color literals) — those
           checks scan only style.css, so inline styles bypass them,
       (b) CSP `style-src` hardening — inline `<style>` requires either
           `'unsafe-inline'` (dangerous) or a per-block SHA-256 hash.
       Note: inline `style="..."` HTML attributes are covered by
       Check 323 (per-element style attribute). Sibling of Check 321
       (CSS @import) / Check 52 (style.css byte budget) for the CSS
       shipping-surface single-source-of-truth axis. (BLOCKING)

  323. `index.html` MUST contain zero `style="..."` HTML attributes
       (per-element inline style). Drift = a scoped style attribute
       drifts into the shipped HTML, bypassing style.css SSoT (Check 52
       byte budget / Check 174 theme-color literals don't scan HTML) and
       requiring CSP `style-src 'unsafe-inline'` hash exceptions.
       Check 242 covers `on*=` inline handlers; Check 322 covers `<style>`
       element blocks; this Check completes the trio for zero-tolerance
       inline CSS. Sibling of Check 322 (`<style>` block) / Check 242
       (`on*=` handler) for the HTML inline-CSS zero-tolerance axis.
       (BLOCKING)

  344. Every `@layer <name> { ... }` block in style.css MUST use a name
       that appears in the top-level `@layer a, b, c;` declaration
       statement. CSS cascade layers get their precedence from that
       declaration order; a block that references an UNDECLARED layer
       silently creates it at first-use position (appended after all
       declared layers), reordering the cascade and causing style
       precedence regressions (a `components` rule losing to a stray
       undeclared layer). Screenshot is advisory and behavior e2e does
       not diff computed styles, so this drift is otherwise silent.
       Sibling of Check 321 (no @import) for the CSS cascade-integrity
       axis. (BLOCKING)

  356. Google Fonts CSP pair: every external `<link rel="stylesheet"
       href="https://host">` host in index.html MUST be in CSP
       `style-src` (currently `fonts.googleapis.com`), AND — because the
       Google Fonts CSS `@font-face src` points at `fonts.gstatic.com` —
       `font-src` MUST include `https://fonts.gstatic.com`. Drift =
       dropping googleapis from style-src CSP-blocks the font stylesheet
       (no @font-face at all), or dropping gstatic from font-src
       CSP-blocks the woff2 fetches (text falls back to system fonts).
       Both are silent (screenshot advisory; behavior e2e does not diff
       computed font-family). Font twin of Check 354/355 (script CSP).
       Sibling of Check 301 (Google Fonts preconnect) for the
       external-font CSP-authorization axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    style = ctx.style
    read = ctx.read
    extract = ctx.extract

    # ── 6. style.css stale markers ───────────────────────────────────────────────
    check(
        "Current release: v73" not in style,
        "style.css: no stale 'Current release: v73' marker",
        "style.css: stale 'Current release: v73' marker found",
    )
    check(
        "NEXT_PLANNED_RELEASE" not in style,
        "style.css: no 'NEXT_PLANNED_RELEASE' marker",
        "style.css: stale 'NEXT_PLANNED_RELEASE' marker found",
    )

    # ── 73. index.html accessibility/CWV HTML-attribute contract (BLOCKING) ──────
    # index.html の機械強制 HTML accessibility / Core Web Vitals 契約。Plan B の HTML
    # 属性のみで完結する範囲を BLOCKING 化することで、style.css に触れずに WCAG 2.2 /
    # CWV シグナルを構造的に固定する。Playwright visual baseline 不変が前提のため、
    # pixel diff を発生させない HTML 属性のみを対象とする (現状の good practice を
    # 契約化して drift 防止):
    #   (73a) 全 <link rel="preload"> に `as=` 属性必須 (preload 仕様で as 無指定は無効)
    #   (73b) 全 <img> 要素に `alt=` 属性必須 (WCAG 1.1.1 Level A)
    #   (73c) hero 画像 (yuta-yokoi-ai-pm-orchestration-system.webp) に
    #         `fetchpriority="high"` を指定 (LCP 改善契約の固定)
    _html73 = read("index.html")
    # HTML コメント (<!-- ... -->) を pre-strip。コメント内に literal `<img>` や preload tag を
    # 記述している可能性があり、それらは実際の DOM 要素ではない (browser は描画しない) ため
    # accessibility / CWV 契約の対象外。Check 7b/7c が同じ pattern で comment-strip 済み。
    _html_no_comments73 = re.sub(r"<!--.*?-->", "", _html73, flags=re.DOTALL)

    _preload73 = re.findall(r"<link[^>]*\brel=\"preload\"[^>]*>", _html_no_comments73)
    _preload_no_as73 = [p for p in _preload73 if not re.search(r"\bas=", p)]
    check(
        not _preload_no_as73,
        f"Check 73a: all {len(_preload73)} <link rel=\"preload\"> tags have an `as=` attribute (WCAG/CWV)",
        f"Check 73a: <link rel=\"preload\"> without `as=` attribute: {_preload_no_as73} — "
        f"preload は as 無指定だと無効 (Chrome は warning を出す)。as=script/style/image/font 等を指定せよ",
    )

    _img73 = re.findall(r"<img\b[^>]*>", _html_no_comments73)
    _img_no_alt73 = [t for t in _img73 if not re.search(r"\balt=", t)]
    check(
        not _img_no_alt73,
        f"Check 73b: all {len(_img73)} <img> tags have an `alt=` attribute (WCAG 1.1.1 Level A)",
        f"Check 73b: <img> without `alt=` attribute: {_img_no_alt73} — "
        f"WCAG 1.1.1 Level A 違反。装飾画像は alt=\"\" でも明示せよ",
    )

    _HERO_IMG_73 = "yuta-yokoi-ai-pm-orchestration-system.webp"
    _hero_pattern73 = re.compile(
        rf"<link[^>]*href=\"[./]*{re.escape(_HERO_IMG_73)}\"[^>]*>",
        re.IGNORECASE,
    )
    _hero_tags73 = _hero_pattern73.findall(_html_no_comments73)
    _hero_has_fp73 = any("fetchpriority=\"high\"" in t for t in _hero_tags73)
    check(
        _hero_has_fp73 and len(_hero_tags73) > 0,
        f"Check 73c: hero image ({_HERO_IMG_73}) preload has fetchpriority=\"high\" (LCP 契約)",
        f"Check 73c: hero image preload missing fetchpriority=\"high\" — "
        f"Core Web Vitals LCP 改善契約。<link rel=\"preload\" href=\"./{_HERO_IMG_73}\" "
        f"as=\"image\" fetchpriority=\"high\"> を維持せよ",
    )

    # ── 101. style.css forced-colors (HCM) focus support (BLOCKING) ──────────────
    # Windows High Contrast Mode (`@media (forced-colors: active)`) では box-shadow が描画されず
    # author color が system color に置換される。focus 表示を box-shadow のみに依存している箇所
    # (.skip-link:focus は outline:none + box-shadow) は HCM で消え WCAG 2.4.7 / 1.4.1 違反になる。
    # style.css に forced-colors 専用の outline-based focus fallback が存在することを BLOCKING で
    # 固定し、将来の編集で silently strip されるのを防ぐ。このブロックは forced-colors モードでのみ
    # 有効で通常描画 (CI baseline) に非影響ゆえ §3 baseline ゲート非該当 (render-neutral)。
    # why-only comment-injection track で発見・systematize (Check 100 と同 pattern)。
    _css101 = ROOT / "style.css"
    if _css101.exists():
        _src101 = _css101.read_text(encoding="utf-8")
        _fc101 = re.search(r"@media\s*\(\s*forced-colors\s*:\s*active\s*\)", _src101)
        _focus_in_fc101 = False
        if _fc101:
            # forced-colors at-rule 開始から十分な window を見て、focus selector + outline 復帰を確認。
            _window101 = _src101[_fc101.start():_fc101.start() + 800]
            _focus_in_fc101 = (":focus" in _window101) and ("outline" in _window101)
        check(
            bool(_fc101) and _focus_in_fc101,
            "Check 101: style.css has a forced-colors (HCM) block restoring outline-based focus (WCAG 2.4.7/1.4.1)",
            "Check 101: style.css is missing the @media (forced-colors: active) focus fallback — "
            "High Contrast Mode users lose the focus indicator (box-shadow is not painted in HCM)",
            blocking=True,
        )
    else:
        check(
            False,
            "",
            "Check 101: style.css not found — forced-colors focus support を検証できない",
            blocking=True,
        )

    # ── 103. style.css prefers-contrast (higher-contrast) support (BLOCKING) ─────
    # ユーザーが OS で「より高いコントラスト」を要求した時のみ有効化する fallback (境界線/補助
    # テキスト/focus を濃く・太く) が style.css に存在することを固定。WCAG 1.4.11 Non-text Contrast
    # 強化。Check 101 (forced-colors) と同じく render-neutral (当該設定が非アクティブな通常描画 =
    # CI baseline には非影響) ゆえ §3 baseline ゲート非該当。将来 silently strip されるのを防ぐ。
    _css103 = ROOT / "style.css"
    if _css103.exists():
        _src103 = _css103.read_text(encoding="utf-8")
        _pc103 = re.search(r"@media\s*\(\s*prefers-contrast\s*:\s*more\s*\)", _src103)
        check(
            bool(_pc103),
            "Check 103: style.css has a prefers-contrast: more block (WCAG 1.4.11 higher-contrast support)",
            "Check 103: style.css is missing the @media (prefers-contrast: more) fallback — "
            "higher-contrast-preference users lose the strengthened borders/focus contrast",
            blocking=True,
        )
    else:
        check(
            False,
            "",
            "Check 103: style.css not found — prefers-contrast support を検証できない",
            blocking=True,
        )

    # ── 135. Stylesheet wiring (BLOCKING) ─────────────────────────────────────────
    # index.html がローカル stylesheet style.css を <link rel="stylesheet" href="./style.css">
    # で load し続けることを BLOCKING 強制する。これは Check 133/134 と同じ「file 存在 ⟹ file 配線」
    # class の中で最も影響が大きい: link を消すとサイト全体が未スタイルで描画されるが、損失は全
    # gate に対し silent — behavior e2e は content presence / route しか検査せず (未スタイルでも
    # テキストは存在)、screenshot e2e は §3(B) で advisory、consistency check も link を被覆して
    # いなかった。style.css の存在 (Check 108 mirror) と byte 予算 (Check 52/120) は強制済だが
    # <link> 配線は未強制だった。外部 font stylesheet は対象外 (除去しても fallback font へ graceful
    # degradation するため)。「style.css 存在 ⟹ index.html に link 済」を invariant 化する。
    _index135 = ROOT / "index.html"
    if _index135.exists():
        _html135 = _index135.read_text(encoding="utf-8")
        _linked135 = re.search(
            r'<link\b[^>]*\brel\s*=\s*["\']stylesheet["\'][^>]*\bhref\s*=\s*["\']\.?/?style\.css["\']'
            r'|<link\b[^>]*\bhref\s*=\s*["\']\.?/?style\.css["\'][^>]*\brel\s*=\s*["\']stylesheet["\']',
            _html135,
        )
        check(
            bool(_linked135),
            "Check 135: index.html が style.css を <link rel=stylesheet> 配線 (unstyled site 防止)",
            "Check 135: index.html に <link rel=\"stylesheet\" href=\"./style.css\"> が無い — "
            "link を消すとサイト全体が未スタイルになるが behavior e2e は content しか見ず "
            "screenshot は advisory ゆえ silent。index.html へ stylesheet link を戻せ",
            blocking=True,
        )
    else:
        check(False, "Check 135: index.html present",
              "Check 135: index.html が無い — stylesheet の配線を検証できない", blocking=True)

    # ── 174. <meta name=theme-color> values exist in style.css (BLOCKING) ──────────
    # index.html の全 theme-color content 値が style.css に literal で存在することを
    # BLOCKING 強制する。drift は SILENT に OS chrome (モバイルアドレスバー / OS card)
    # を visual brand から desync させ、アドレスバーが site が使わない色を表示する。
    _idx174 = ROOT / "index.html"
    _css174 = ROOT / "style.css"
    if _idx174.exists() and _css174.exists():
        _isrc174 = _idx174.read_text(encoding="utf-8")
        _csrc174 = _css174.read_text(encoding="utf-8")
        _colors174 = re.findall(
            r'<meta\s+name=["\']theme-color["\']\s+content=["\']([^"\']+)["\']', _isrc174
        )
        _missing174 = [c for c in _colors174 if c not in _csrc174]
        check(
            bool(_colors174) and not _missing174,
            f"Check 174: theme-color 値 {_colors174} 全て style.css に literal で存在",
            (f"Check 174: theme-color drift: {_missing174} が style.css に literal で存在しない — "
             "モバイルアドレスバー色が visual brand と desync。index.html theme-color を style.css の "
             "実 brand 色に揃えよ"
             if _colors174 else
             "Check 174: theme-color meta が見つからない (vacuous; Check 157 と一致確認)"),
            blocking=True,
        )
    else:
        check(False, "Check 174: index.html + style.css present",
              "Check 174: index.html もしくは style.css が無い", blocking=True)

    # ── 321. style.css has zero @import statements (BLOCKING) ────────────────────
    _css321 = ROOT / "style.css"
    if _css321.exists():
        _css_src321 = _css321.read_text(encoding="utf-8")
        # /* @import */ のようなコメント内は除外して数える
        _stripped321 = re.sub(r"/\*.*?\*/", "", _css_src321, flags=re.DOTALL)
        _imports321 = re.findall(r"(?m)^\s*@import\b", _stripped321)
        _count321 = len(_imports321)
        _ok321 = _count321 == 0
        check(
            _ok321,
            "Check 321: style.css @import 0 件 (Boring Technology 契約遵守)",
            (f"Check 321: style.css に @import が {_count321} 件検出 — "
             "外部 CSS load = 実装時の render-blocking / CSP 拡張。"
             "Boring Technology (C1) 契約違反。@import を削除せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 321: style.css present",
              "Check 321: style.css が無い", blocking=True)

    # ── 322. index.html has zero inline <style> element blocks (BLOCKING) ────────
    _html322 = ROOT / "index.html"
    if _html322.exists():
        _hs322 = _html322.read_text(encoding="utf-8")
        # HTML コメント除去 (<!-- ... -->) してからスキャン
        _stripped322 = re.sub(r"<!--.*?-->", "", _hs322, flags=re.DOTALL)
        _style_blocks322 = re.findall(r"(?is)<style\b[^>]*>.*?</style>", _stripped322)
        _count322 = len(_style_blocks322)
        _ok322 = _count322 == 0
        check(
            _ok322,
            "Check 322: index.html inline <style> block 0 件 (single-stylesheet 契約遵守)",
            (f"Check 322: index.html に inline <style> block が {_count322} 件検出 — "
             "single canonical style.css 契約違反 / Check 52・174 が bypass される / "
             "CSP style-src 'unsafe-inline' or per-hash 必要。inline <style> を "
             "style.css へ移せ"),
            blocking=True,
        )
    else:
        check(False, "Check 322: index.html present",
              "Check 322: index.html が無い", blocking=True)

    # ── 323. index.html has zero style="..." attributes (BLOCKING) ───────────────
    _html323 = ROOT / "index.html"
    if _html323.exists():
        _hs323 = _html323.read_text(encoding="utf-8")
        # HTML コメントを除外してからスキャン
        _stripped323 = re.sub(r"<!--.*?-->", "", _hs323, flags=re.DOTALL)
        _style_attrs323 = re.findall(r'\bstyle\s*=\s*"[^"]*"', _stripped323)
        _count323 = len(_style_attrs323)
        _ok323 = _count323 == 0
        check(
            _ok323,
            "Check 323: index.html style=\"...\" attribute 0 件 (single-stylesheet 契約完全遵守)",
            (f"Check 323: index.html に style=\"...\" attribute が {_count323} 件検出: "
             f"{[a[:80] for a in _style_attrs323[:3]]!r} — style.css SSoT 破綻 / "
             "CSP style-src 'unsafe-inline' 要求。スタイルを style.css へ移せ"),
            blocking=True,
        )
    else:
        check(False, "Check 323: index.html present",
              "Check 323: index.html が無い", blocking=True)

    # ── 344. style.css @layer blocks ⊆ declared layer list (BLOCKING) ────────────
    _css344 = ROOT / "style.css"
    if _css344.is_file():
        _csrc344 = _css344.read_text(encoding="utf-8")
        # 宣言文 `@layer a, b, c;` (block を伴わない) を抽出
        _decl_m344 = re.search(r"@layer\s+([a-z][a-z0-9,\s-]*?)\s*;", _csrc344, re.IGNORECASE)
        _declared344: set[str] = set()
        if _decl_m344:
            _declared344 = {x.strip() for x in _decl_m344.group(1).split(",") if x.strip()}
        # 使用ブロック `@layer name {` を抽出
        _used344 = set(re.findall(r"@layer\s+([a-z][a-z0-9-]*)\s*\{", _csrc344, re.IGNORECASE))
        _undeclared344 = sorted(_used344 - _declared344)
        _ok344 = bool(_declared344) and not _undeclared344
        check(
            _ok344,
            f"Check 344: style.css @layer block {sorted(_used344)} すべて宣言 {sorted(_declared344)} 内",
            (f"Check 344: 未宣言 @layer block: {_undeclared344!r} — "
             f"宣言文 = {sorted(_declared344)}。未宣言 layer は first-use 位置 (末尾) で "
             "生成され cascade 順序が壊れ style precedence 回帰。宣言文へ追加せよ"
             if _declared344 else
             "Check 344: style.css に @layer 宣言文が無い"),
            blocking=True,
        )
    else:
        check(False, "Check 344: style.css present",
              "Check 344: style.css が無い", blocking=True)

    # ── 356. Google Fonts CSP pair: style-src + font-src (BLOCKING) ──────────────
    # 354/355 の font 版: 外部 font stylesheet host は style-src、woff2 host
    # (fonts.gstatic.com) は font-src で許可される必要がある。片方欠落で font 破綻。
    _idx356 = ROOT / "index.html"
    if _idx356.is_file():
        _h356 = _idx356.read_text(encoding="utf-8")
        _h356_nc = re.sub(r"<!--.*?-->", "", _h356, flags=re.DOTALL)
        _csp_m356 = re.search(r'Content-Security-Policy"\s+content="([^"]*)"',
                              _h356_nc, re.DOTALL)
        _style_src356 = ""
        _font_src356 = ""
        if _csp_m356:
            for _d in _csp_m356.group(1).split(";"):
                _ds = _d.strip()
                if _ds.startswith("style-src"):
                    _style_src356 = _d
                elif _ds.startswith("font-src"):
                    _font_src356 = _d
        # 外部 stylesheet host (data: 除く https://) を抽出
        _ext_css_hosts356 = set(re.findall(
            r'<link[^>]*rel="stylesheet"[^>]*href="https://([^/"]+)', _h356_nc))
        _problems356: list[str] = []
        for _host in sorted(_ext_css_hosts356):
            if f"https://{_host}" not in _style_src356:
                _problems356.append(f"style-src に {_host} 不在")
        # Google Fonts を使う場合、woff2 の gstatic を font-src に要求
        if "fonts.googleapis.com" in _ext_css_hosts356:
            if "https://fonts.gstatic.com" not in _font_src356:
                _problems356.append("font-src に fonts.gstatic.com 不在 (woff2 fetch が block)")
        _ok356 = (not _problems356) and bool(_style_src356)
        check(
            _ok356,
            f"Check 356: 外部 font stylesheet host {sorted(_ext_css_hosts356)} が style-src + gstatic が font-src で authorize",
            (f"Check 356: font CSP wiring drift: {_problems356!r} — "
             "style-src から font stylesheet host が消えると @font-face 全滅、font-src から "
             "gstatic が消えると woff2 が block されシステムフォント fallback。silent (screenshot "
             "advisory)。CSP を復元せよ"
             if _style_src356 else
             "Check 356: CSP style-src directive が見つからない"),
            blocking=True,
        )
    else:
        check(False, "Check 356: index.html present",
              "Check 356: index.html が無い", blocking=True)
