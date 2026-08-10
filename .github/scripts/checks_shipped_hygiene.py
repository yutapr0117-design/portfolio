"""
checks_shipped_hygiene.py — shipped-JS/HTML security & hygiene checks — eval/setTimeout-string/document.write/console/loose-eq etc. (242-249, 366, 367, 368)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  242. index.html inline `on*=` event handlers are restricted to the
       documented CSP-allowlisted pattern: every `on*=` attribute outside
       of HTML comments MUST match exactly `onload="this.media='all'"`
       (the documented async font-loading pattern that is whitelisted via
       CSP `'unsafe-hashes'`). Drift introduces an XSS entry vector that
       bypasses CSP `script-src` (inline event handlers execute as
       scripts). Sibling of Check 239/240/241 (eval/Function/timer/
       document.write) for the inline-event-handler surface. (BLOCKING)

  243. main.js SITE_CONFIG.LAST_UPDATED + ai:last-modified are NOT in the
       future: both date fields (synced via Check 17/180) MUST be on or
       before today. Drift to a future date silently corrupts AI/SEO
       recency-weighted retrieval (entity ranked as "from the future")
       and reveals temporal model integrity issues. This site does not
       schedule pre-publish dates; future is always a bug. Sibling of
       Check 36 (sitemap lastmod future WARNING) for the canonical-version
       date surface — BLOCKING here because LAST_UPDATED is the entity's
       primary canonical-version anchor. (BLOCKING)

  244. Every top-level node in JSON-LD `@graph` has `@type`: in index.html
       JSON-LD blocks, every direct top-level element of any `@graph`
       array MUST have a non-empty `@type` field. Drift (anonymous node)
       silently makes AI/SEO consumers ignore the node (no type → cannot
       reason about entity) and breaks Schema.org graph traversal.
       Sibling of Check 217 (top-level @id uniqueness) for the top-level
       @type presence axis. (BLOCKING)

  245. JSON-LD FAQPage `mainEntity[]` Q&A structure validity: every
       FAQPage node's `mainEntity` array MUST contain non-empty Question
       entries, each with `@type == "Question"` + non-empty `name` + an
       `acceptedAnswer` object with `@type == "Answer"` + non-empty
       `text`. Drift would silently break Google FAQ rich-result
       eligibility + AI search FAQ ingestion. Sibling of Check 235
       (Article required fields) for the FAQPage required-structure
       surface. (BLOCKING)

  246. JSON-LD BreadcrumbList `itemListElement` Schema.org structure:
       every BreadcrumbList's `itemListElement` array MUST contain
       ListItem entries, each with `@type == "ListItem"`, an integer
       `position`, a non-empty `name`, and an `item` (URL or @id ref).
       Drift would silently break Google breadcrumb rich-result and AI
       site-structure ingestion. Sibling of Check 245 (FAQPage Q&A) for
       the BreadcrumbList required-structure surface. (BLOCKING)

  247. JSON-LD ImageObject/AudioObject/VideoObject have required fields:
       every node with `@type in {ImageObject, AudioObject, VideoObject}`
       MUST have `name` AND at least one of `contentUrl` / `url`. Drift
       (e.g. silent strip of name) would silently break Google Image/
       Audio rich-result and AI/SEO entity-asset linkage. Sibling of
       Check 245 (FAQPage) / Check 246 (BreadcrumbList) for the
       MediaObject required-structure surface. (BLOCKING)

  248. `<meta charset>` value is `utf-8` (case-insensitive): the index
       .html `<meta charset>` attribute MUST resolve to `utf-8` exactly
       (case-insensitive accepts UTF-8 / utf-8). Drift to e.g.
       `shift_jis` or `iso-8859-1` silently mojibake Japanese content and
       break canonical entity name display. Check 157 enforces presence;
       Check 248 enforces value canonicality. (BLOCKING)

  249. `<meta name="viewport">` content has mobile baseline directives:
       the index.html `<meta name="viewport">` content MUST contain
       `width=device-width` AND `initial-scale=1`. Drift (e.g. fixed
       `width=900`) silently breaks mobile rendering (zoom locked,
       content cropped). Check 157 enforces presence; Check 249 enforces
       canonical mobile-baseline content. (BLOCKING)

  366. shipped JS (js/*.js non-recursive) の h() props で `target: '_blank'`
       を含む行の ±2 行以内に `noreferrer` が現れることを BLOCKING 強制。
       runtime は ui-components.js:h() が全 a[target=_blank] に
       noopener+noreferrer を付与する二重防御だが、source レベルの省略は
       「意図的に noreferrer を省いた」と誤読されるコード drift を生む
       (実例: ContactPage LinkedIn #322 が rel:'noopener' のみで push)。
       secureExternalLinks の mutation test (mutation_samples.py) とは独立した
       静的ソース軸の防止層。(BLOCKING)

  367. shipped JS (js/*.js 非再帰) の h('select', ...) 呼び出しで第2引数の
       attrs オブジェクトに `value:` キーが現れないことを BLOCKING 強制。
       `<select>` 要素には HTML 仕様上 `value` content attribute が存在しない。
       h('select', { value: x }) は el.setAttribute('value', x) を呼び、
       <select> の選択状態には一切反映されない (#7cbc4d9 class)。
       正しい実装は各 <option> に `selected: val === cur ? true : undefined`
       を付与すること (h() の undefined-skip line 128 が非選択 option に
       属性追加するのを防ぐ)。apps.js / settings-page.js / projects-page.js の
       全 h('select') を #668〜#670 + 本 increment で修正済。本 Check は
       再発防止の構造封じ。(BLOCKING)

  368. shipped JS の apps.js と store.js が notes 上限を CONSTANTS.LIMITS.NOTES_TEXT
       経由で参照し、マジックナンバー `20000` を直接持たないことを BLOCKING 強制。
       apps.js (NotesPage oninput) と store.js (validateAndNormalize) の両方が同じ
       20000 という値を参照しており、一方だけ変更した場合に silently drift する
       class (#672)。NOTES_TEXT を constants.js の LIMITS に定数化して二者を単一
       ソースへ集約した。本 Check は再発防止の構造封じ。(BLOCKING)
  369. shipped JS の AI / pomodoro 履歴保持件数上限がマジックナンバーで
       drift しないことを BLOCKING 強制。AI 履歴の 80 は store.js (normalize) と
       ai-page.js (add) の 2 箇所、pomodoro 履歴の 200 は store.js (normalize) と
       pomodoro-page.js (complete) の 2 箇所で同じ値を参照する。一方だけ変更すると
       履歴保持件数が silently drift する (Check 368 の NOTES_TEXT と同型 class)。
       AI_HISTORY / POMODORO_HISTORY を constants.js の LIMITS に定数化して各ペアを
       単一ソースへ集約した。本 Check は `.slice(-80)` / `.slice(-200)` マジックの
       再注入を構造的に禁止する。(BLOCKING)
  370. shipped JS の pomodoro 既定状態 (settings {work:25,short:5,long:15} +
       runtime remainingSec 1500) が state.js (clone fallback) と store.js
       (default + normalize clamp fallback) にマジックリテラルで重複せず
       CONSTANTS.POMODORO_DEFAULT_SETTINGS / POMODORO_DEFAULT_REMAINING_SEC 経由で
       参照されることを BLOCKING 強制。両ファイルが同じ既定値を独立に持つと片方だけ
       変更した際に既定状態が silently drift する (Check 369 の履歴上限と同型の
       cross-file default-object drift class)。定数化して単一ソースへ集約した後、
       本 Check が `work: 25` / `remainingSec: 1500` / `|| 1500` (runtime) および settings
       normalize clamp fallback `settings.work) || 25` / `settings.short) || 5` /
       `settings.long) || 15` マジックの再注入を構造的に禁止する。(BLOCKING)
  394. pomodoro settings clamp *range* (work=[1,180] / short=[1,60] / long=[1,120])
       が pomodoro-page.js (UI input onchange の即時 clamp) と store.js
       (normalizeAppsData の ingestion clamp) の 2 レイヤで field 毎に一致することを
       BLOCKING 強制。Check 370 は既定値 (25/5/15) のマジック再注入を禁止するが range
       (180/60/120) は magic literal のまま両ファイルに重複しており未カバーだった。片方
       だけ range を変えると (例: UI work max を 240 にしたが store は 180 のまま) UI で
       入力できる値が reload/import 後に store normalize で再 clamp され silently 変わる
       (2 層 clamp-range drift)。UI/store 双方から work/short/long の (min,max) を抽出し
       一致を強制する (Check 370 default-object drift の clamp-range twin)。(BLOCKING)
  414. shipped leaf JS (`js/**/*.js`) が **組み込み prototype を書き換えない**ことを
       BLOCKING 強制。`X.prototype.y = ...` / `Object.defineProperty(X.prototype, ...)` /
       `Object.assign(X.prototype, ...)` の形で `Element` / `Node` / `HTMLElement` /
       `CSSStyleDeclaration` / `EventTarget` / `Document` / `Array` / `Object` / `String` /
       `Function` / `Promise` 等の組み込みを差し替えると、DOM/JS の意味論がサイト内だけ
       非標準になる。これは「壊れる」形ではなく「黙って別物になる」形で効くため、
       全 gate (consistency / behavior e2e / screenshot) を素通りする。実害の実例:
       かつて perf-guards.js が `CSSStyleDeclaration.prototype.setProperty` と
       `Element.prototype.setAttribute('style', …)` を rAF まで遅延バッチしていたため、
       e2e で候補 CSS を当てて同期で読む診断が **全て偽陰性**になり (書き込み前の値が返る)、
       レイアウト調査 1 サイクル分が無効化された (2026-08-10)。しかも shipped JS は例外なく
       直接代入 (`el.style.x = …`) を使うので hook は **一度も発火しておらず利益はゼロ**だった。
       main.js の保護領域 (innerHTML sanitizer / eventListener registry・Check 43 が別途強制) は
       対象外で、葉モジュールのみを縛る。(BLOCKING)

  417. `js/store.js` (外部 ingestion の正規化チョークポイント) が、**untrusted な生値を
       `String()` へ直接渡さない**ことと、**必須テキストの filter が型判定 `isText()` を
       通す**ことを BLOCKING 強制する。動機は 2026-08-10 の 3 連続実バグで、いずれも
       `String(v || fallback)` / `filter(t => t && t.title)` が **truthy な非文字列**
       (`[]` / `{}`) を素通りさせたもの:
         - profile (#968): `String([]) === ''` で email が空になり、ContactPage から宛先が
           消え「メールを作成」が宛先の無い `mailto:` を開いた
         - projects (#969): `String({})` が **"[object Object]" を一覧 3 箇所 / 詳細 4 箇所へ描画**
         - appsData (#970): 同じ形で task/todo 一覧へ描画 (さらに壊れた entry が落ちずに残る)
       いずれも fatal を出さないため ErrorBoundary に掛からず、視覚 baseline は ADVISORY ゆえ
       **behavior test 以外に捕捉層が無い**。per-instance で 3 回潰した class は構造防止 Check へ
       昇華する (Check 364 が `(X || []).<throwing method>` で同じ昇華をした ingestion-safety の
       文字列面)。走査前にコメントを除去し、機構を説明する記述自体を違反と誤検出しない。(BLOCKING)

  421. shipped JS (`js/**/*.js` ∪ `main.js`) で **スクロールの `behavior` を `'smooth'` と
       明示するファイルは、同じファイルで `prefers-reduced-motion` を問い合わせる**ことを
       BLOCKING 強制する。CSSOM-View では **`behavior` を明示した時点で CSS の
       `scroll-behavior` は参照されない**ため、style.css の
       `@media (prefers-reduced-motion: reduce) { scroll-behavior: auto !important }` は
       `scrollIntoView({behavior:'smooth'})` / `scrollTo({behavior:'smooth'})` には**効かない**。
       動機は実測 (#993): home の「ケースを見る →」が reduce 環境でも no-preference と
       **同一のアニメーション曲線** (t0=0 → t150≈475 → t600≈1075) で 1,000px 超をスクロール
       していた。前庭障害のユーザーに影響する WCAG 2.3.3 の欠陥だが、**視覚 baseline は
       ADVISORY・fatal も出ない**ので behavior test 以外に捕捉層が無い。CSS 側の reduce
       override が「効いているように見える」ことが誤解を強める —— 同じ実測の中で
       `window.scrollTo(0, 0)` は reduce のとき即時に完了しており、CSS override 自体は
       正しく働いていた。効かないのは **behavior を明示した呼び出しだけ**である。走査前に
       コメントを除去するので、機構を説明する記述が違反にも充足にもならない (Check 112 の
       「コメント中の語で file 単位判定が GREEN 化する」失敗の回避)。(BLOCKING)

  422. shipped JS の **`onchange` を持つ `<select>` / checkbox / number input は `id` を持つ**
       ことを BLOCKING 強制する。これらのハンドラは `State.update` / `window.render()` で
       `#content` を作り直す＝**コントロールが自分自身を DOM ごと消す**ため、focus が body へ
       落ちる。main.js `_renderCore` は「clear の前に控えた id」で focus を復元するので、
       **id を持たないコントロールだけが復元対象から漏れる**。実測 (#994) では task/todo の
       絞り込み・タスクの優先度・TODO の完了チェック・ポモドーロの設定・Settings の
       インポート対象がすべて change 後に activeElement=BODY だった (id を既に持っていた
       `brandSelect` だけが復元されており、id の有無がそのまま分岐になっていた)。
       number input は特に重く、ArrowUp の 1 回目で focus を失うため **2 回目以降が効かない**
       (値を 1 段しか動かせない = 実質キーボード操作不能・WCAG 2.1.1)。
       対象は「同じコントロールを続けて操作する」ものに限る —— `type='file'` は 1 回限りの
       アクションなので除外する。走査はプロパティオブジェクトを brace-match して行い、事前に
       コメントを除去する (説明コメント中の `id:` で vacuous PASS しない)。(BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 242. index.html inline on*= handlers are restricted to allowlist (BLOCKING) ─
    # index.html の全 `on*="..."` 属性 (HTML comment 外) が CSP unsafe-hashes で
    # whitelist された 1 パターン `onload="this.media='all'"` のみであることを
    # BLOCKING 強制。drift は CSP script-src を bypass する XSS entry vector。
    _ALLOWED_INLINE_HANDLERS242 = {"onload=\"this.media='all'\""}
    _idx242 = ROOT / "index.html"
    if _idx242.exists():
        _isrc242 = _idx242.read_text(encoding="utf-8")
        _stripped242 = re.sub(r"<!--.*?-->", "", _isrc242, flags=re.DOTALL)
        _handlers242 = re.findall(r'\bon[a-z]+\s*=\s*"[^"]*"', _stripped242)
        _bad242 = [h for h in _handlers242 if h not in _ALLOWED_INLINE_HANDLERS242]
        _ok242 = len(_handlers242) > 0 and not _bad242
        check(
            _ok242,
            f"Check 242: index.html inline on*= handlers {len(_handlers242)} 件全て allowlist 内",
            (f"Check 242: allowlist 外 inline handler: {_bad242!r} — CSP script-src "
             "bypass の XSS vector。allowlist は onload=\"this.media='all'\" のみ"
             if _bad242 else
             "Check 242: inline handler 0 件 — vacuous-fail (font async load の期待値は 2 件)"),
            blocking=True,
        )
    else:
        check(False, "Check 242: index.html present",
              "Check 242: index.html が無い", blocking=True)

    # ── 243. SITE_CONFIG.LAST_UPDATED + ai:last-modified NOT future (BLOCKING) ────
    # main.js SITE_CONFIG.LAST_UPDATED と <meta name="ai:last-modified"> content が
    # 共に today より未来でないことを BLOCKING 強制。Check 36 (sitemap lastmod 未来
    # WARNING) と異なり本サイトは pre-schedule しない設計のため BLOCKING。
    from datetime import date as _date243
    _main243 = ROOT / "main.js"
    _idx243 = ROOT / "index.html"
    if _main243.exists() and _idx243.exists():
        _msrc243 = _main243.read_text(encoding="utf-8")
        _isrc243 = _idx243.read_text(encoding="utf-8")
        _site243_m = re.search(r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc243)
        _ai_lm243_m = re.search(
            r'<meta\s+name=["\']ai:last-modified["\']\s+content=["\']([^"\']+)["\']', _isrc243
        )
        _site243 = _site243_m.group(1) if _site243_m else None
        _ai_lm243 = _ai_lm243_m.group(1) if _ai_lm243_m else None
        _today243 = _date243.today()
        _futures243: list[str] = []
        for _label, _v in (("SITE_CONFIG.LAST_UPDATED", _site243), ("ai:last-modified", _ai_lm243)):
            if not isinstance(_v, str):
                _futures243.append(f"{_label}=抽出不可")
                continue
            try:
                _d = _date243.fromisoformat(_v[:10])
            except ValueError:
                # Check 215 が format を担う。本 check は format violation で fail せず skip。
                continue
            if _d > _today243:
                _futures243.append(f"{_label}={_v!r} (today={_today243.isoformat()} より未来)")
        _ok243 = not _futures243
        check(
            _ok243,
            f"Check 243: SITE_CONFIG.LAST_UPDATED + ai:last-modified 共に today ({_today243.isoformat()}) 以前",
            (f"Check 243: 未来日 detected: {_futures243!r} — AI/SEO recency が "
             "「未来から来た content」と誤認し ranking corruption。today 以下へ修正"),
            blocking=True,
        )
    else:
        check(False, "Check 243: main.js + index.html present",
              "Check 243: main.js もしくは index.html が無い", blocking=True)

    # ── 244. JSON-LD @graph 全 top-level node has @type (BLOCKING) ────────────────
    # index.html の各 JSON-LD <script> block の top-level `@graph` 配列の全 element に
    # 非空 `@type` がある (anonymous node 不在) ことを BLOCKING 強制。drift で AI/SEO
    # が無 type node を無視し Schema.org graph traversal 不能。
    _idx244 = ROOT / "index.html"
    if _idx244.exists():
        _isrc244 = _idx244.read_text(encoding="utf-8")
        _blocks244 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc244,
            flags=re.DOTALL,
        )
        _violations244: list[str] = []
        _total244 = 0
        for _bi, _blk in enumerate(_blocks244):
            try:
                _data244 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _g244 = _data244.get("@graph") if isinstance(_data244, dict) else None
            if not isinstance(_g244, list):
                continue
            for _j, _n in enumerate(_g244):
                _total244 += 1
                if not isinstance(_n, dict) or not isinstance(_n.get("@type"), str) or not _n.get("@type"):
                    _violations244.append(f"block{_bi}.@graph[{_j}] missing/empty @type")
        _ok244 = _total244 > 0 and not _violations244
        check(
            _ok244,
            f"Check 244: JSON-LD @graph top-level node {_total244} 件全て @type 保有",
            (f"Check 244: @type 不在 node: {_violations244!r} — AI/SEO 無視されて "
             "Schema.org graph traversal 破壊。各 top-level node に @type を付与せよ"
             if _violations244 else
             "Check 244: @graph top-level node 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 244: index.html present",
              "Check 244: index.html が無い", blocking=True)

    # ── 245. JSON-LD FAQPage mainEntity Q&A structure validity (BLOCKING) ─────────
    # index.html JSON-LD の全 FAQPage node の `mainEntity` 配列が Schema.org Q&A 構造
    # (Question + name + acceptedAnswer(Answer + text)) を満たすことを BLOCKING 強制。
    # drift は SILENT に Google FAQ rich-result 失格 + AI search FAQ ingestion 破壊。
    _idx245 = ROOT / "index.html"
    if _idx245.exists():
        _isrc245 = _idx245.read_text(encoding="utf-8")
        _blocks245 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc245,
            flags=re.DOTALL,
        )
        _violations245: list[str] = []
        _q_count245 = 0
        def _walk245(node: object, path: str) -> None:
            nonlocal _q_count245
            if isinstance(node, dict):
                if node.get("@type") == "FAQPage":
                    _me = node.get("mainEntity")
                    if not isinstance(_me, list) or not _me:
                        _violations245.append(f"{path}: FAQPage.mainEntity 欠落/空")
                    else:
                        for _i, _q in enumerate(_me):
                            _q_count245 += 1
                            if not isinstance(_q, dict):
                                _violations245.append(f"{path}.mainEntity[{_i}] non-dict")
                                continue
                            if _q.get("@type") != "Question":
                                _violations245.append(f"{path}.mainEntity[{_i}] @type != Question")
                            _n = _q.get("name")
                            if not isinstance(_n, str) or not _n.strip():
                                _violations245.append(f"{path}.mainEntity[{_i}] name 欠落/空")
                            _a = _q.get("acceptedAnswer")
                            if not isinstance(_a, dict):
                                _violations245.append(f"{path}.mainEntity[{_i}] acceptedAnswer 欠落")
                            else:
                                if _a.get("@type") != "Answer":
                                    _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer @type != Answer")
                                _t = _a.get("text")
                                if not isinstance(_t, str) or not _t.strip():
                                    _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer.text 欠落/空")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk245(item, f"{path}.{k}")
                    else:
                        _walk245(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk245(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks245):
            try:
                _data245 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk245(_data245, f"block{_bi}")
        _ok245 = _q_count245 > 0 and not _violations245
        check(
            _ok245,
            f"Check 245: FAQPage mainEntity Q&A {_q_count245} 件全て Schema.org 構造正",
            (f"Check 245: 違反: {_violations245!r} — Google FAQ rich-result 失格 + "
             "AI FAQ ingestion 破壊。Question+name+acceptedAnswer(Answer+text) 構造へ揃えよ"
             if _violations245 else
             "Check 245: FAQPage mainEntity Q 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 245: index.html present",
              "Check 245: index.html が無い", blocking=True)

    # ── 246. JSON-LD BreadcrumbList itemListElement Schema.org 構造 (BLOCKING) ────
    # index.html JSON-LD 全 BreadcrumbList の `itemListElement` 配列が ListItem +
    # position(int) + name(非空 str) + item(URL/string) を満たすことを BLOCKING 強制。
    # drift で Google breadcrumb rich-result + AI site-structure ingestion 破壊。
    _idx246 = ROOT / "index.html"
    if _idx246.exists():
        _isrc246 = _idx246.read_text(encoding="utf-8")
        _blocks246 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc246,
            flags=re.DOTALL,
        )
        _violations246: list[str] = []
        _items_count246 = 0
        def _walk246(node: object, path: str) -> None:
            nonlocal _items_count246
            if isinstance(node, dict):
                if node.get("@type") == "BreadcrumbList":
                    _ile = node.get("itemListElement")
                    if not isinstance(_ile, list) or not _ile:
                        _violations246.append(f"{path}: itemListElement 欠落/空")
                    else:
                        for _i, _it in enumerate(_ile):
                            _items_count246 += 1
                            if not isinstance(_it, dict):
                                _violations246.append(f"{path}.itemListElement[{_i}] non-dict")
                                continue
                            if _it.get("@type") != "ListItem":
                                _violations246.append(f"{path}.itemListElement[{_i}] @type != ListItem")
                            if not isinstance(_it.get("position"), int):
                                _violations246.append(f"{path}.itemListElement[{_i}] position not int")
                            _n = _it.get("name")
                            if not isinstance(_n, str) or not _n.strip():
                                _violations246.append(f"{path}.itemListElement[{_i}] name 欠落/空")
                            if "item" not in _it:
                                _violations246.append(f"{path}.itemListElement[{_i}] item 欠落")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk246(item, f"{path}.{k}")
                    else:
                        _walk246(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk246(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks246):
            try:
                _data246 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk246(_data246, f"block{_bi}")
        _ok246 = _items_count246 > 0 and not _violations246
        check(
            _ok246,
            f"Check 246: BreadcrumbList itemListElement {_items_count246} 件全て Schema.org 構造正",
            (f"Check 246: 違反: {_violations246!r} — Google breadcrumb rich-result 失格 "
             "+ AI site-structure ingestion 破壊。ListItem+position+name+item へ揃えよ"
             if _violations246 else
             "Check 246: BreadcrumbList items 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 246: index.html present",
              "Check 246: index.html が無い", blocking=True)

    # ── 247. JSON-LD ImageObject/AudioObject/VideoObject 必須 fields (BLOCKING) ───
    # index.html JSON-LD で `@type in {ImageObject, AudioObject, VideoObject}` の
    # node が `name` AND (`contentUrl` OR `url`) を持つことを BLOCKING 強制。drift で
    # Google Image/Audio rich-result 失格 + AI/SEO entity-asset linkage 破壊。
    _MEDIA_TYPES247 = {"ImageObject", "AudioObject", "VideoObject"}
    _idx247 = ROOT / "index.html"
    if _idx247.exists():
        _isrc247 = _idx247.read_text(encoding="utf-8")
        _blocks247 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc247,
            flags=re.DOTALL,
        )
        _violations247: list[str] = []
        _media_count247 = 0
        def _walk247(node: object, path: str) -> None:
            nonlocal _media_count247
            if isinstance(node, dict):
                _t = node.get("@type")
                if isinstance(_t, str) and _t in _MEDIA_TYPES247:
                    _media_count247 += 1
                    _missing = []
                    if not isinstance(node.get("name"), str) or not node.get("name", "").strip():
                        _missing.append("name")
                    if "contentUrl" not in node and "url" not in node:
                        _missing.append("contentUrl|url")
                    if _missing:
                        _violations247.append(f"{path} {_t}: missing {_missing!r}")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk247(item, f"{path}.{k}")
                    else:
                        _walk247(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk247(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks247):
            try:
                _data247 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk247(_data247, f"block{_bi}")
        _ok247 = _media_count247 > 0 and not _violations247
        check(
            _ok247,
            f"Check 247: MediaObject {_media_count247} 件全て name + contentUrl|url 保有",
            (f"Check 247: 違反: {_violations247!r} — Google Image/Audio rich-result 失格 "
             "+ AI/SEO entity-asset linkage 破壊。name + contentUrl|url を揃えよ"
             if _violations247 else
             "Check 247: MediaObject 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 247: index.html present",
              "Check 247: index.html が無い", blocking=True)

    # ── 248. <meta charset> value is utf-8 (case-insensitive) (BLOCKING) ──────────
    # index.html `<meta charset="...">` の値が utf-8 (case-insensitive) であることを
    # BLOCKING 強制。drift で Japanese mojibake → canonical entity 名表示破壊。
    # Check 157 は presence、Check 248 は value canonicality 軸。
    _idx248 = ROOT / "index.html"
    if _idx248.exists():
        _isrc248 = _idx248.read_text(encoding="utf-8")
        _cm248 = re.search(r'<meta\s+charset\s*=\s*["\']?([^"\'\s>]+)', _isrc248, re.IGNORECASE)
        _cv248 = _cm248.group(1) if _cm248 else None
        _ok248 = isinstance(_cv248, str) and _cv248.lower() == "utf-8"
        check(
            _ok248,
            f"Check 248: <meta charset>={_cv248!r} == utf-8 (case-insensitive)",
            (f"Check 248: charset 値違反: {_cv248!r} — Japanese mojibake で canonical "
             "entity 名表示破壊。utf-8 (case-insensitive) へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 248: index.html present",
              "Check 248: index.html が無い", blocking=True)

    # ── 249. <meta name=viewport> content has mobile baseline (BLOCKING) ──────────
    # index.html `<meta name="viewport">` content が `width=device-width` AND
    # `initial-scale=1` を含むことを BLOCKING 強制。drift で mobile rendering 破壊
    # (zoom 固定 / content cropped)。Check 157 (presence) の value 軸補完。
    _idx249 = ROOT / "index.html"
    if _idx249.exists():
        _isrc249 = _idx249.read_text(encoding="utf-8")
        _vm249 = re.search(
            r'<meta\s+name=["\']viewport["\'][^>]*content=["\']([^"\']+)["\']', _isrc249
        )
        _vv249 = _vm249.group(1) if _vm249 else None
        _missing249: list[str] = []
        if not isinstance(_vv249, str):
            _missing249.append("viewport 抽出不可")
        else:
            if "width=device-width" not in _vv249:
                _missing249.append("width=device-width 不在")
            if not re.search(r"initial-scale\s*=\s*1(\.0+)?\b", _vv249):
                _missing249.append("initial-scale=1 不在")
        _ok249 = not _missing249
        check(
            _ok249,
            f"Check 249: <meta name=viewport> content has mobile baseline ({_vv249!r})",
            (f"Check 249: viewport content 違反: {_missing249!r} — mobile rendering 破壊"
             " (zoom 固定/content cropped)。width=device-width + initial-scale=1 を付与"),
            blocking=True,
        )
    else:
        check(False, "Check 249: index.html present",
              "Check 249: index.html が無い", blocking=True)

    # ── 366. shipped JS target='_blank' に ±2行以内で noreferrer あり (BLOCKING) ────
    # js/*.js (非再帰・main.js 含む) の h() props 内で `target: '_blank'` を含む行の
    # ±2 行以内に `noreferrer` が現れることを強制。runtime 多重防御 (ui-components.js
    # h() 全 a[target=_blank] 強制 + secureExternalLinks patcher) はあるが source の
    # 省略は「意図的 noreferrer 省略」と誤読されるコード drift を生む。
    _violations366: list[str] = []
    _hit_count366 = 0
    for _f366 in sorted((ROOT / "js").glob("*.js")):
        _lines366 = _f366.read_text(encoding="utf-8", errors="replace").splitlines()
        for _li366, _ln366 in enumerate(_lines366):
            if "target: '_blank'" not in _ln366:
                continue
            _hit_count366 += 1
            _window366 = _lines366[max(0, _li366 - 2): _li366 + 3]
            if any("noreferrer" in _wl for _wl in _window366):
                continue
            _violations366.append(f"{_f366.relative_to(ROOT)}:{_li366 + 1}")
    check(
        not _violations366,
        f"Check 366: shipped JS {_hit_count366} 件の target='_blank' 全てに ±2行以内で noreferrer あり",
        (f"Check 366: noreferrer 欠落 {len(_violations366)} 件: {_violations366!r} — "
         "source drift は intentional 省略と誤読される。rel:'noopener noreferrer' へ揃えよ"
         if _violations366 else
         "Check 366: target='_blank' が shipped JS に 0 件 — vacuous-fail"),
        blocking=True,
    )

    # ── 367. shipped JS h('select', ...) に value: attr を禁止 (HTML 仕様違反) ──────
    # `<select>` 要素には HTML 仕様上 `value` content attribute が存在しない。
    # h('select', { value: x }) は el.setAttribute('value', x) を呼び、<select> の
    # 選択状態には一切反映されない (#7cbc4d9 class)。修正: 各 <option> に
    # `selected: val === cur ? true : undefined` を付与する (h() の undefined-skip
    # line 128 が非選択 option に属性追加するのを防ぐ)。
    # apps.js / settings-page.js / projects-page.js の全 h('select') を
    # #668〜#670 + 本 increment で修正済。本 Check は再発防止の構造封じ。
    #
    # 手法: h('select', の直後から最初の h('option', までのテキストに
    # `(?<![.\w])value\s*:` (オブジェクトキーとしての value:) を探す。
    # `e.target.value` は `;` で終わり `:` が後続しないため false-positive にならない。
    _violations367: list[tuple[str, int]] = []
    _select_pat367 = re.compile(r"h\('select'")
    _value_key_pat367 = re.compile(r"(?<![.\w])value\s*:")
    _option_pat367 = re.compile(r"h\('option'")
    _js_files367 = sorted((ROOT / "js").glob("*.js"))
    for _f367 in _js_files367:
        _src367 = _f367.read_text(encoding="utf-8", errors="replace")
        for _m367 in _select_pat367.finditer(_src367):
            _pos367 = _m367.end()
            _tail367 = _src367[_pos367:]
            _opt_m367 = _option_pat367.search(_tail367)
            _before_option367 = _tail367[:_opt_m367.start()] if _opt_m367 else _tail367[:300]
            if _value_key_pat367.search(_before_option367):
                _line367 = _src367[:_m367.start()].count("\n") + 1
                _violations367.append((str(_f367.relative_to(ROOT)), _line367))
    check(
        not _violations367,
        f"Check 367: shipped JS h('select') の attrs に value: キーなし "
        f"({len(_js_files367)} files scanned)",
        (f"Check 367: h('select') に value: attr が {len(_violations367)} 件: "
         f"{_violations367!r} — <select> に value content attribute は HTML 仕様上存在しない "
         "(el.setAttribute('value', x) は選択状態に反映されない #7cbc4d9 class)。"
         "各 <option> に `selected: val === cur ? true : undefined` を付与せよ"),
        blocking=True,
    )

    # ── 368. notes 上限マジックナンバー禁止 (CONSTANTS.LIMITS.NOTES_TEXT 経由必須) ────────
    # apps.js (NotesPage oninput) と store.js (validateAndNormalize) が両方 20000 を
    # 直接 hardcode していた。片方だけ変更すると silently drift する class (#672)。
    # NOTES_TEXT を LIMITS に定数化して両者を単一ソースへ集約した後、
    # 本 Check が再注入を BLOCKING で防ぐ。
    _notes_magic_files368 = [ROOT / "js" / "apps.js", ROOT / "js" / "store.js"]
    _notes_violations368: list[str] = []
    for _f368 in _notes_magic_files368:
        _src368 = _f368.read_text(encoding="utf-8", errors="replace")
        # slice(0, 20000) or val.slice(0,20000) patterns (notes 上限としての 20000 直接使用)
        if re.search(r"\.slice\(\s*0\s*,\s*20000\s*\)", _src368):
            _notes_violations368.append(_f368.name)
    check(
        not _notes_violations368,
        "Check 368: apps.js / store.js が notes 上限を CONSTANTS.LIMITS.NOTES_TEXT 経由で参照"
        " (マジックナンバー 20000 不在)",
        (f"Check 368: notes 上限 20000 のマジックナンバーが {_notes_violations368} に残存。"
         "CONSTANTS.LIMITS.NOTES_TEXT 経由に統一せよ (drift 防止 #672 class)"),
        blocking=True,
    )

    # ── 369. AI/pomodoro 履歴上限マジックナンバー禁止 (CONSTANTS.LIMITS.*_HISTORY 経由必須) ──
    # AI 履歴の 80 は store.js (normalize) + ai-page.js (add) の 2 箇所、pomodoro 履歴の 200 は
    # store.js (normalize) + pomodoro-page.js (complete) の 2 箇所で同じ値を参照する。片方だけ
    # 変更すると履歴保持件数が silently drift する (Check 368 の NOTES_TEXT と同型 class)。
    # AI_HISTORY / POMODORO_HISTORY を LIMITS に定数化して各ペアを単一ソースへ集約した後、
    # 本 Check が `.slice(-80)` / `.slice(-200)` マジックの再注入を BLOCKING で防ぐ。
    _hist_magic369 = {
        r"\.slice\(\s*-\s*80\s*\)": ("80", "CONSTANTS.LIMITS.AI_HISTORY"),
        r"\.slice\(\s*-\s*200\s*\)": ("200", "CONSTANTS.LIMITS.POMODORO_HISTORY"),
    }
    _hist_files369 = [ROOT / "js" / "store.js", ROOT / "js" / "ai-page.js", ROOT / "js" / "pomodoro-page.js"]
    _hist_violations369: list[str] = []
    for _f369 in _hist_files369:
        _src369 = _f369.read_text(encoding="utf-8", errors="replace")
        for _pat369, (_val369, _const369) in _hist_magic369.items():
            if re.search(_pat369, _src369):
                _hist_violations369.append(f"{_f369.name}: .slice(-{_val369}) → {_const369} 経由に統一せよ")
    check(
        not _hist_violations369,
        "Check 369: store.js / ai-page.js / pomodoro-page.js が履歴保持件数上限を "
        "CONSTANTS.LIMITS.AI_HISTORY / POMODORO_HISTORY 経由で参照 (マジックナンバー 80/200 不在)",
        (f"Check 369: 履歴上限マジックナンバーが残存: {_hist_violations369} "
         "(履歴保持件数の drift 防止・Check 368 と同型 class)"),
        blocking=True,
    )

    # ── 370. pomodoro 既定状態マジックリテラル禁止 (CONSTANTS.POMODORO_DEFAULT_* 経由必須) ──
    # pomodoro 既定状態 (settings {work:25,short:5,long:15} + runtime remainingSec 1500) は
    # state.js (clone fallback) と store.js (default + normalize clamp fallback) の 2 ファイルで
    # 同じ既定値を独立に持っていた。片方だけ変更すると既定状態が silently drift する (Check 369 の
    # 履歴上限と同型の cross-file default-object drift class)。POMODORO_DEFAULT_SETTINGS /
    # POMODORO_DEFAULT_REMAINING_SEC に定数化して単一ソースへ集約した後、本 Check が
    # `work: 25` / `remainingSec: 1500` / `|| 1500` (runtime) および settings normalize clamp
    # fallback `settings.work) || 25` / `settings.short) || 5` / `settings.long) || 15` マジックの
    # 再注入を BLOCKING で防ぐ (runtime remainingSec は POMODORO_DEFAULT_REMAINING_SEC を参照するのに
    # settings fallback だけ magic が残っていた非対称 gap を後から閉じた)。
    # 注: 共有定数オブジェクトの参照共有 mutation を避けるため利用側は必ず spread する
    # ({ ...CONSTANTS.POMODORO_DEFAULT_SETTINGS })。
    _pomo_magic370 = [
        r"work:\s*25\b",                       # settings {work:25,...} リテラルの再注入
        r"remainingSec:\s*1500\b",             # runtime 既定 remainingSec の再注入
        r"\|\|\s*1500\b",                      # runtime remainingSec normalize clamp fallback の再注入
        r"settings\.work\)\s*\|\|\s*\d",       # settings.work normalize clamp fallback magic (|| 25) の再注入
        r"settings\.short\)\s*\|\|\s*\d",      # settings.short normalize clamp fallback magic (|| 5) の再注入
        r"settings\.long\)\s*\|\|\s*\d",       # settings.long normalize clamp fallback magic (|| 15) の再注入
    ]
    _pomo_files370 = [ROOT / "js" / "state.js", ROOT / "js" / "store.js"]
    _pomo_violations370: list[str] = []
    for _f370 in _pomo_files370:
        _src370 = _f370.read_text(encoding="utf-8", errors="replace")
        for _pat370 in _pomo_magic370:
            if re.search(_pat370, _src370):
                _pomo_violations370.append(f"{_f370.name}: /{_pat370}/")
    check(
        not _pomo_violations370,
        "Check 370: state.js / store.js が pomodoro 既定状態を CONSTANTS.POMODORO_DEFAULT_SETTINGS / "
        "POMODORO_DEFAULT_REMAINING_SEC 経由で参照 (マジックリテラル {work:25...} / 1500 不在)",
        (f"Check 370: pomodoro 既定状態マジックが残存: {_pomo_violations370} "
         "(cross-file default-object drift 防止・Check 369 と同型 class)"),
        blocking=True,
    )

    # ── 394. pomodoro settings clamp *range* の UI↔store 2 層一致 (cross-layer clamp-range drift 防止) ──
    # pomodoro の集中/短休憩/長休憩の設定値は 2 レイヤで独立に clamp される: pomodoro-page.js の
    # input onchange (UI 入力の即時 clamp) と store.js の normalizeAppsData (load/import/cross-tab/
    # snapshot ingestion の clamp)。両者は field 毎に同じ range を持つ必要がある (work=[1,180] /
    # short=[1,60] / long=[1,120])。Check 370 は既定値 (25/5/15) のマジック再注入を禁止するが range
    # (180/60/120) は magic literal のまま両ファイルに重複しており未カバーだった。もし片方だけ range を
    # 変更すると (例: UI work max を 240 にしたが store は 180 のまま)、UI で 240 を入力できるのに reload/
    # import 後に store normalize が 180 へ再 clamp し、ユーザ設定が silently 変わる (2 層 clamp-range
    # drift)。behavior e2e は特定の境界値しか検査せず中間帯の range 差は捕捉しない。UI と store の
    # 各 field の clamp range を抽出して一致を BLOCKING 強制する (Check 370 default-object drift の
    # clamp-range twin・Check 378 の JS↔CSS cross-layer coherence と同じ 2 レイヤ一致軸)。
    _clamp_ui_re394 = re.compile(r"settings\.(work|short|long) = clamp\([^;]*?,\s*(\d+),\s*(\d+)\)")
    _clamp_store_re394 = re.compile(r"(work|short|long): clamp\([^;]*?,\s*(\d+),\s*(\d+)\)")
    _ui_src394 = (ROOT / "js" / "pomodoro-page.js").read_text(encoding="utf-8", errors="replace")
    _store_src394 = (ROOT / "js" / "store.js").read_text(encoding="utf-8", errors="replace")
    _ui_ranges394 = {m.group(1): (m.group(2), m.group(3)) for m in _clamp_ui_re394.finditer(_ui_src394)}
    _store_ranges394 = {m.group(1): (m.group(2), m.group(3)) for m in _clamp_store_re394.finditer(_store_src394)}
    _fields394 = {"work", "short", "long"}
    # 両ファイルから 3 field すべてを抽出できること (regex が code 形と乖離したら発見漏れ防止) +
    # 各 field の (min, max) が UI↔store で一致すること。
    _mismatch394 = [
        f"{_f}: UI{_ui_ranges394.get(_f)} != store{_store_ranges394.get(_f)}"
        for _f in _fields394 if _ui_ranges394.get(_f) != _store_ranges394.get(_f)
    ]
    check(
        _fields394 <= set(_ui_ranges394) and _fields394 <= set(_store_ranges394) and not _mismatch394,
        "Check 394: pomodoro settings clamp range が pomodoro-page.js(UI) ↔ store.js(normalize) で "
        f"field 毎に一致 (work/short/long: {_ui_ranges394})",
        ("Check 394: pomodoro clamp-range が UI↔store で drift または抽出漏れ: "
         f"UI={_ui_ranges394} store={_store_ranges394} mismatch={_mismatch394} "
         "(2 層 clamp-range drift 防止・Check 370 の range twin)"),
        blocking=True,
    )

    # ── 414. shipped leaf JS が組み込み prototype を書き換えない (非標準 DOM 意味論の禁止) ──
    # 「壊れる」のではなく「黙って別物になる」変更は全 gate を素通りする。実例: perf-guards.js が
    # CSSStyleDeclaration.prototype.setProperty / Element.prototype.setAttribute('style', …) を
    # rAF 遅延バッチしていたため、e2e で style を書いて同期で読む診断が全て偽陰性になり
    # (書き込み前の値が返る) レイアウト調査 1 サイクルが無効化された (2026-08-10)。しかも shipped JS
    # は例外なく直接代入を使うので hook は一度も発火せず利益はゼロだった。同型の再混入を構造的に
    # 禁止する。main.js の保護領域 (Check 43 が別途強制) は対象外＝葉モジュールのみを縛る。
    _BUILTINS414 = (
        "Element", "HTMLElement", "Node", "EventTarget", "Document", "DocumentFragment",
        "CSSStyleDeclaration", "CSSStyleSheet", "Window", "Array", "Object", "String",
        "Number", "Function", "Promise", "Map", "Set", "JSON", "Date", "RegExp",
    )
    _proto_assign414 = re.compile(
        r"\b(" + "|".join(_BUILTINS414) + r")\.prototype\.[A-Za-z_$][\w$]*\s*=(?!=)"
    )
    _proto_define414 = re.compile(
        r"\b(?:Object\.defineProperty|Object\.defineProperties|Object\.assign)\s*\(\s*"
        r"(?:" + "|".join(_BUILTINS414) + r")\.prototype\b"
    )
    _viol414 = []
    for _f414 in sorted(list((ROOT / "js").glob("*.js")) + list((ROOT / "js").glob("**/*.js"))):
        _rel414 = _f414.relative_to(ROOT).as_posix()
        _src414 = _f414.read_text(encoding="utf-8", errors="replace")
        # 行コメント / ブロックコメントを除去してから走査する (docstring で機構を説明している
        # 記述そのものを違反と誤検出しない = comment-match による false RED の回避)。
        _code414 = re.sub(r"/\*.*?\*/", "", _src414, flags=re.S)
        _code414 = re.sub(r"(?<!:)//[^\n]*", "", _code414)
        for _m414 in list(_proto_assign414.finditer(_code414)) + list(_proto_define414.finditer(_code414)):
            _viol414.append(f"{_rel414}: {_m414.group(0).strip()}")
    check(
        not _viol414,
        f"Check 414: shipped leaf JS ({len(list((ROOT / 'js').glob('**/*.js')))} file) が組み込み prototype を書き換えていない",
        ("Check 414: shipped leaf JS が組み込み prototype を書き換えている: "
         + "; ".join(sorted(set(_viol414))[:5])
         + " — DOM/JS の意味論がサイト内だけ非標準になり、全 gate (consistency / behavior e2e / "
           "screenshot) を素通りしたまま e2e の測定を偽陰性にする (2026-08-10 に実際 1 サイクル無効化)。"
           "必要なら main.js の保護領域 (Check 43 の管轄) で行い、葉モジュールには置かない"),
        blocking=True,
    )

    # ── 417. store.js の untrusted 生値を String() へ直接渡さない (ingestion 文字列ガード) ──
    # 2026-08-10 に profile / projects / appsData で 3 連続の実バグを出した class。
    # `String(v || fallback)` は `[]` / `{}` のような **truthy な非文字列** に対して fallback が
    # 効かず、`String([]) === ''` (フィールドが空になる) / `String({}) === "[object Object]"`
    # (そのまま描画される) を生む。同様に `filter(t => t && t.title)` は `{}` を素通りさせ、
    # 本文の無い entry を残す。per-instance で 3 回潰したので構造防止へ昇華する
    # (Check 364 が `(X || []).<throwing method>` でやった昇華の文字列面)。
    _src417 = (ROOT / "js" / "store.js").read_text(encoding="utf-8", errors="replace")
    _code417 = re.sub(r"/\*.*?\*/", "", _src417, flags=re.S)
    _code417 = re.sub(r"(?<!:)//[^\n]*", "", _code417)
    # (a) untrusted な生値 (raw. / data. / 個々の entry t.) を String() へ直接渡さない
    _direct417 = re.findall(r"String\(\s*(?:raw|data|t)\.[\w.?\[\]]*", _code417)
    # (b) 必須テキストの filter は isText() を通す (truthy 判定だけの形を禁止)
    _weak_filter417 = re.findall(r"filter\(\s*(\w+)\s*=>\s*\1\s*&&\s*\1\.(?:title|text)\s*\)", _code417)
    _viol417 = [f"String() へ直接: {_m}" for _m in sorted(set(_direct417))] + \
               [f"必須テキストの filter が isText() を通していない (変数 {_v})" for _v in sorted(set(_weak_filter417))]
    check(
        not _viol417,
        "Check 417: js/store.js が untrusted 生値を String() へ直接渡さず、必須テキスト filter が isText() を通す",
        ("Check 417: js/store.js の ingestion 文字列ガードが崩れている: " + "; ".join(_viol417)
         + " — truthy な非文字列 ([] / {}) が素通りし、フィールドが空になる (ContactPage の宛先が消える) か "
           "\"[object Object]\" がそのまま描画される。fatal を出さないので ErrorBoundary に掛からず、"
           "視覚 baseline は ADVISORY ゆえ behavior test 以外に捕捉層が無い。safeStr / safeStrList / isText を通せ"),
        blocking=True,
    )

    # ── 421. behavior:'smooth' を明示する file は prefers-reduced-motion を問い合わせる ──
    # CSSOM-View: `behavior` を明示すると CSS の scroll-behavior は参照されない。つまり
    # style.css の reduce override (`scroll-behavior: auto !important`) は明示呼び出しには
    # 効かない。実測 (#993) では reduce / no-preference でスクロール曲線が完全に一致していた。
    # 'smooth' の綴りは三項 (`behavior: reduce ? 'auto' : 'smooth'`) にも現れるため、
    # `behavior:` の直後だけを見る形にすると **正しく直した後のコードを見落として vacuous
    # PASS する**。ゆえに検出は「その file に 'smooth' リテラルがあるか」で広く取り、
    # 充足条件を「同 file が prefers-reduced-motion を問い合わせるか」に置く。
    _files421 = sorted(list((ROOT / "js").glob("**/*.js"))) + [ROOT / "main.js"]
    _viol421 = []
    _guarded421 = []
    for _f421 in _files421:
        _rel421 = _f421.relative_to(ROOT).as_posix()
        _src421 = _f421.read_text(encoding="utf-8", errors="replace")
        # コメントを除去してから両方を判定する。除去しないと (a) 説明コメント中の 'smooth' が
        # false RED を生み、(b) コメント中の prefers-reduced-motion が実装なしで GREEN にする。
        _code421 = re.sub(r"/\*.*?\*/", "", _src421, flags=re.S)
        _code421 = re.sub(r"(?<!:)//[^\n]*", "", _code421)
        if not re.search(r"['\"]smooth['\"]", _code421):
            continue
        if re.search(r"prefers-reduced-motion", _code421):
            _guarded421.append(_rel421)
        else:
            _viol421.append(_rel421)
    check(
        not _viol421,
        f"Check 421: 明示 behavior:'smooth' を持つ shipped JS {len(_guarded421)} file が prefers-reduced-motion を問い合わせている",
        ("Check 421: スクロールの behavior を 'smooth' と明示しているのに prefers-reduced-motion を "
         "問い合わせていない shipped JS: " + ", ".join(_viol421)
         + " — CSSOM-View では behavior を明示した時点で CSS の scroll-behavior は参照されないため、"
           "style.css の @media (prefers-reduced-motion: reduce) { scroll-behavior: auto !important } は "
           "この呼び出しに効かない (実測 #993: reduce と no-preference でスクロール曲線が同一)。"
           "前庭障害のユーザーに影響する WCAG 2.3.3 の欠陥で、fatal も視覚差分も出ないため "
           "behavior test 以外に捕捉層が無い。matchMedia('(prefers-reduced-motion: reduce)').matches を "
           "見て behavior を 'auto' へ落とせ"),
        blocking=True,
    )

    # ── 422. onchange を持つ select / checkbox / number input は focus 復元用の id を持つ ──
    # これらのハンドラは State.update / window.render() で #content を作り直す = コントロールが
    # 自分自身を DOM ごと消す。main.js _renderCore は「clear の前に控えた id」で focus を復元する
    # ため、id を持たないコントロールだけが復元対象から漏れて focus が body へ落ちる (#994)。
    def _props_span422(src, start):
        """`h('tag', {` の `{` からプロパティオブジェクトの終端までを返す (文字列内の brace は無視)。"""
        depth, i, n = 0, start, len(src)
        quote = None
        while i < n:
            ch = src[i]
            if quote:
                if ch == "\\":
                    i += 2
                    continue
                if ch == quote:
                    quote = None
            elif ch in "'\"`":
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return src[start:i + 1]
            i += 1
        return ""

    _viol422 = []
    _ok422 = 0
    for _f422 in sorted((ROOT / "js").glob("**/*.js")):
        _rel422 = _f422.relative_to(ROOT).as_posix()
        _code422 = re.sub(r"/\*.*?\*/", "", _f422.read_text(encoding="utf-8", errors="replace"), flags=re.S)
        _code422 = re.sub(r"(?<!:)//[^\n]*", "", _code422)
        for _m422 in re.finditer(r"h\(\s*['\"](select|input)['\"]\s*,\s*(?=\{)", _code422):
            _tag422 = _m422.group(1)
            _props422 = _props_span422(_code422, _m422.end())
            if "onchange" not in _props422:
                continue
            if _tag422 == "input":
                # 「同じコントロールを続けて操作する」ものだけが対象。file は 1 回限りのアクション。
                if not re.search(r"type\s*:\s*['\"](checkbox|number)['\"]", _props422):
                    continue
            if re.search(r"(^|[{,\s])id\s*:", _props422):
                _ok422 += 1
            else:
                _label422 = re.search(r"'aria-label'\s*:\s*([^,\n]+)", _props422)
                _viol422.append(f"{_rel422}: h('{_tag422}') " + (_label422.group(1).strip() if _label422 else "(aria-label 無し)"))
    check(
        not _viol422,
        f"Check 422: onchange を持つ select / checkbox / number input {_ok422} 件が focus 復元用の id を持つ",
        ("Check 422: onchange を持つのに focus 復元用の id が無いコントロール: " + "; ".join(_viol422)
         + " — これらのハンドラは #content を作り直すので、コントロールが自分自身を DOM ごと消して "
           "focus が body へ落ちる。main.js _renderCore の復元は id を鍵にしているため、id が無いものだけ "
           "取り残される (実測 #994: id を持つ brandSelect だけが復元され、他は全て BODY だった)。"
           "number input は ArrowUp の 1 回目で focus を失い 2 回目以降が効かない = 実質キーボード操作不能 "
           "(WCAG 2.1.1)。一意で安定した id を付けよ (リスト項目は id を含めて一意化する)"),
        blocking=True,
    )
