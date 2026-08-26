"""
checks_shipped_structure.py — shipped-JS structural coherence & byte-weight budget checks
(extracted from check_repository_consistency.py — check.py split track・category "shipped structure").

This module owns the cluster of Checks 118-120 (+ 390) that guard the shipped-JS module
structure and asset size: PAGE_META route coverage (118), factory docstring dependency coherence
(119), the shipped JS+CSS byte-weight budget (120), and router→PAGE_META direct coverage that
closes Check 118's param-route blind spot (390). Each Check reads its own target files
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
       119a is the signature ⟹ docstring direction; 119b is the REVERSE (docstring ⟹ signature):
       a docstring must not declare a dependency the factory never receives. 119 alone let that
       drift through — measured in #908, where an edit script failed midway so the docstring
       already declared `announce` while the signature did not, and the Check stayed GREEN.
       The next AI reads the docstring as its onboarding substrate, so a phantom dependency
       teaches a wrong contract that is only discoverable by reading the implementation.
       119b only reads the bullet-leading identifiers (` *   - a, b: description`), so
       parenthetical notes about REMOVED deps and non-identifier bullets ("window グローバル経由")
       are ignored — false-positive count on the current repo was measured as 0 before adopting.
  120. shipped JS+CSS byte-weight budget: the total bytes of the browser-downloaded payload
       (main.js + js/**/*.js + style.css) must stay <= the PERF-BUDGET-DATA ceiling in
       file-size-budget.md. §3(B) made the pixel screenshot advisory, thinning real page-weight
       protection; this byte-weight guard restores it on a different axis from Check 52's
       line-count budget (byte ≠ line). Catches runaway bloat (e.g. a huge file committed by
       mistake) that would inflate download/parse cost (LCP/CWV). Legitimate feature growth
       ratchets the ceiling up with a rationale, like the ESLint baseline. (BLOCKING)
  461. PERF-BUDGET の累積記録 (session-start → current) が現在の PERF-BUDGET-DATA と一致すること
  390. router route.name ⊆ PAGE_META (param-route coverage): every route.name js/router.js's
       `_parseRoute` can emit — literal `route.name = 'X'` assignments, the initial `{ name:
       'home' }`, and the `['task','todo',...].includes(app)` whitelist expanded to `app-<x>` —
       must be a top-level key in PAGE_META (js/page-meta.js). Check 118 derives its route set
       from e2e ALL_ROUTES, which structurally omits param routes like `project-detail`, so that
       entry was guarded by no Check: dropping it makes applyMeta early-return and every project
       detail page (Case Study — the portfolio's #1 mission) ships with no title/desc/JSON-LD and
       (since #773 made announceRouteForAccessibility the sole a11y announcer) no route
       announcement. This ties router↔PAGE_META directly, bypassing ALL_ROUTES, machine-enforcing
       page-meta.js:15's "不一致は MetaMgmt で silent fallback" invariant. (BLOCKING)
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
        f"Check 119a: 全 {_checked119} factory の docstring【依存】節が署名の注入依存を網羅 (署名 ⟹ docstring)",
        "Check 119a: factory 署名の依存が docstring【依存】節に欠落 (依存契約 drift): "
        + "; ".join(_dep_problems119)
        + " — 署名に dep を足したら同ファイルの【依存（引数で注入）】節にも追記せよ",
        blocking=True,
    )

    # 119b — 逆方向 (docstring ⟹ 署名)。119a は「署名にあるのに docstring に無い」だけを見るため、
    # **docstring が実在しない依存を宣言している** drift は素通りしていた (実測: #908 で編集スクリプトが
    # 途中で失敗し docstring だけ先に announce を宣言、署名は未更新のまま — 119 は GREEN だった)。
    # 次の AI は docstring を onboarding substrate として読むので、存在しない依存の宣言は誤った依存契約を
    # 教える (実装を読むまで気付けない)。判定対象は【依存】節の **箇条書き先頭の識別子** のみ
    # (` *   - name1, name2: 説明` 形式)。除去済み依存を説明する括弧書きや「window グローバル経由」等の
    # 非識別子は対象外 = 現行 repo で false-positive 0 を実測してから導入した。
    _phantom119 = []
    for _facfile119b in sorted((ROOT / "js").glob("*.js")):
        _facsrc119b = _facfile119b.read_text(encoding="utf-8")
        _facm119b = re.search(r"export function create\w+\(\{\s*([^}]*?)\}\)", _facsrc119b)
        if not _facm119b:
            continue
        _sig119b = {d.strip() for d in _facm119b.group(1).replace("\n", " ").split(",") if d.strip()}
        _secm119b = re.search(r"【依存[^】]*】(.*?)(?:【|\*/)", _facsrc119b, re.DOTALL)
        _declared119b = set()
        if _secm119b:
            for _line119b in _secm119b.group(1).split("\n"):
                _b119b = re.match(r"\s*\*\s*-\s*([^:：]+)[:：]", _line119b)
                if not _b119b:
                    continue
                for _name119b in _b119b.group(1).split(","):
                    _name119b = _name119b.strip()
                    if re.fullmatch(r"[A-Za-z_$][\w$]*", _name119b):
                        _declared119b.add(_name119b)
        _extra119b = sorted(_declared119b - _sig119b)
        if _extra119b:
            _phantom119.append(f"{_facfile119b.name}: docstring が宣言する非実在依存 {_extra119b}")
    check(
        not _phantom119,
        "Check 119b: docstring【依存】節が宣言する依存はすべて factory 署名に実在 (docstring ⟹ 署名)",
        "Check 119b: docstring が factory 署名に無い依存を宣言している (逆方向の依存契約 drift): "
        + "; ".join(_phantom119)
        + " — 次の AI は docstring を onboarding substrate として読むため、存在しない依存の宣言は誤った"
        " 契約を教える。署名へ追加するか docstring から除去せよ",
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
        # [FIX 2026-08-21] **クリティカルパスだけを測る。** この Check の宣言された目的は
        #   「実 download/parse 負荷の保護」だが、実装は **ディスク上の全 shipped ファイル**を
        #   足しており、遅延読み込みしても数字が減らなかった。実際 quiz の問題集データ
        #   (4 ファイル計 130,595 bytes) を動的 import へ移して**訪問者が取得しなくなった**のに、
        #   この Check の値は逆に増えた (loader の分)。それでは「上げるか削るか」の判断材料に
        #   ならないので、main.js が **静的 import する** モジュールだけを対象にする。
        #   除外集合はハードコードせず main.js から導出する (次の遅延化でも自動的に追従する)。
        _mainsrc120 = (ROOT / "main.js").read_text(encoding="utf-8")
        _static120 = set(re.findall(r"from\s+'\./(js/[^']+\.js)'", _mainsrc120))
        _files120 = [ROOT / "main.js", ROOT / "style.css"] + [
            ROOT / _rel120 for _rel120 in sorted(_static120)
        ]
        for _f120 in _files120:
            if _f120.exists():
                _shipped120 += len(_f120.read_bytes())
        check(
            _shipped120 <= _ceiling120,
            f"Check 120: クリティカルパスの JS+CSS byte-weight {_shipped120} <= budget {_ceiling120} (静的 import のみ・遅延モジュールは対象外)",
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

    # ── 461. PERF-BUDGET の累積記録が現在値と一致する (BLOCKING) ──
    # 予算は超過するたび自分で上げられる。個々のラチェットには rationale を書く運用だが、それだけでは
    # 「今日で合計いくら増えたのか」が視界に入らない。実際 2026-08-27 に累積行が
    # 「716,800 → 722,400」のまま **その後 5 回上げられていた** —— 歯止めのための行が、上げた本人に
    # よって更新されない形で stale 化していた。marker の current を PERF-BUDGET-DATA と照合し、
    # 予算を上げたら累積も同じ commit で更新することを強制する (session-start は据え置き = 差分が残る)。
    _cum = re.search(r"<!--\s*PERF-BUDGET-CUMULATIVE\s+session-start=(\d+)\s+current=(\d+)\s*-->",
                     _budget120.read_text(encoding="utf-8")) if _budget120.exists() else None
    if _cum and _perf_m120:
        _cur_declared, _cur_actual = int(_cum.group(2)), int(_perf_m120.group(1))
        check(
            _cur_declared == _cur_actual,
            "Check 461: PERF-BUDGET-CUMULATIVE current == PERF-BUDGET-DATA",
            f"Check 461: 累積記録の current={_cur_declared} が PERF-BUDGET-DATA={_cur_actual} と一致しない — "
            f"予算を上げたら累積行 (session-start={_cum.group(1)} からの合計) も同じ commit で更新せよ。"
            f"個々の rationale だけでは『今日で合計いくら増えたか』が視界に入らず、"
            f"歯止めが効かなくなる (2026-08-27 に 5 回分 stale 化していた)",
            blocking=True,
        )
    else:
        check(
            False,
            "Check 461: PERF-BUDGET-CUMULATIVE marker present",
            "Check 461: file-size-budget.md に `<!-- PERF-BUDGET-CUMULATIVE session-start=<N> current=<N> -->` "
            "が無い — 予算ラチェットの累積が追えなくなる。marker を追加せよ",
            blocking=True,
        )

    # ── 390. router route.name ⊆ PAGE_META (param-route coverage・Check 118 盲点補完) (BLOCKING) ──
    # Check 118 は e2e ALL_ROUTES を権威に PAGE_META 網羅を強制するが、ALL_ROUTES は param 必須の動的
    # route (project-detail) を構造的に含まないため、project-detail の PAGE_META エントリはどの Check にも
    # 守られていない盲点だった。project-detail が PAGE_META から落ちると applyMeta が early-return し、
    # 全プロジェクト詳細ページ (Case Study = ポートフォリオ #1 mission) が title/desc/JSON-LD なしで ship
    # される silent AIO/SEO 回帰になる (#773 で announceRouteForAccessibility を唯一の a11y announcer に
    # したため、PAGE_META 欠落は route アナウンス完全欠落も意味する)。本 Check は router.js `_parseRoute`
    # が emit しうる全 route.name を直接 parse し、各々が PAGE_META の key に存在することを強制する
    # — ALL_ROUTES を経由せず router↔PAGE_META を直結し param route を含む全 route を被覆する。
    _router390 = ROOT / "js" / "router.js"
    _pm390 = ROOT / "js" / "page-meta.js"
    if _router390.exists() and _pm390.exists():
        _rsrc390 = _router390.read_text(encoding="utf-8")
        _pmsrc390 = _pm390.read_text(encoding="utf-8")
        # (a) `route.name = 'X'` の literal 代入 (projects/project-detail/apps/settings/.../not-found)
        _names390 = set(re.findall(r"route\.name\s*=\s*'([^']+)'", _rsrc390))
        # (b) 初期 route オブジェクトの `{ name: 'home', ... }`
        _init390 = re.search(r"route\s*=\s*\{\s*name:\s*'([^']+)'", _rsrc390)
        if _init390:
            _names390.add(_init390.group(1))
        # (c) app whitelist `['task','todo',...].includes(app)` → `app-${app}` テンプレート展開
        _wl390 = re.search(r"\[([^\]]*)\]\.includes\(app\)", _rsrc390)
        if _wl390:
            for _a390 in re.findall(r"'([^']+)'", _wl390.group(1)):
                _names390.add(f"app-{_a390}")
        # PAGE_META の top-level key (Check 118 と同じ抽出ロジック)
        _pmkeys390 = set(re.findall(r"^\s*'?([a-z][a-z0-9-]*)'?\s*:\s*\{", _pmsrc390, re.MULTILINE))
        _missing390 = sorted(_names390 - _pmkeys390)
        check(
            bool(_names390) and bool(_pmkeys390) and not _missing390,
            f"Check 390: router が emit する全 {len(_names390)} route.name が PAGE_META に存在 (param route 含む・Check 118 盲点補完)",
            f"Check 390: router.js が emit する route に PAGE_META 欠落: {_missing390} — applyMeta が early-return し title/desc/JSON-LD/route アナウンスが消失。js/page-meta.js に追加せよ (project-detail 等の param route は ALL_ROUTES 非経由ゆえ Check 118 では守れない)",
            blocking=True,
        )
    else:
        check(
            False,
            "",
            "Check 390: js/router.js または js/page-meta.js が見つからない — router↔PAGE_META coherence を検証できない",
            blocking=True,
        )
