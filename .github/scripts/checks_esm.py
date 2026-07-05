"""
checks_esm.py — main.js ⇄ js/ leaf-module ESM contract & factory-pattern coherence checks
(extracted from check_repository_consistency.py — check.py split track・category "ESM contract").

This module owns the four Checks that share the `_modules47` leaf-module source-of-truth list
(and `_main_src47`, main.js's source): 47 (import/export bijection + leaf-ness), 56 (factory
parameter coverage), 57 (index.html modulepreload ↔ _modules47 set equality), 61 (factory
docstring marker). They were kept in the monolith through Phase 5 precisely because they are
coupled through `_modules47`; extracting them together (list + all consumers in one module)
resolves that coupling cleanly — the shared list is now module-local and every consumer sits
beside it.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/errors/warnings by reference (exec 不使用),
so append semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  47. main.js ⇄ js/ module ESM import/export contract: for each local module main.js imports
      from (js/brand.js, js/constants.js, js/identity.js, js/meta-management.js,
      js/page-meta.js, js/pages.js, js/pure-utils.js, js/router.js, js/state.js, js/storage.js,
      js/store.js, js/theme.js, js/ui-components.js and js/quiz/{architecture,aws,pm,quality}-
      quiz-data.js — 17 modules), every name main.js imports is actually exported by that
      module, and (symmetrically) every name the module exports is imported by main.js — an
      exact bijection per module. This guards the physical module split (v80+ Stage 2 pure
      utilities, Stage 3/3-b static quiz data, Stage 4 UI components, Stage 5 Router+PAGE_META,
      Stage 5-b page components, Stage 5-c Safe Storage, Stage 5-d CONSTANTS, Stage 5-e AUTHOR
      identity, Stage 5-f Brand factory, Stage 5-g Store factory, Stage 5-h State factory,
      Stage 5-i Theme factory, Stage 5-l Meta Management factory). Because the site is
      build-free
      and served directly, a mismatch is a *runtime* failure: importing a name a module does
      not export throws a module-load error and the whole SPA fails to boot, while a
      left-behind unused export signals the split has drifted. (This check is exactly what
      would have caught the Stage 3 near-miss where main.js referenced four quiz datasets but
      an early draft of the module exported only two.) The import lists carry inline `//`
      comments, so the parser strips per-line comments before extracting identifiers, and it
      matches each `import {…} from '<module>'` block in isolation (the captured brace group
      excludes braces so a match cannot span an adjacent import block). The export-side parser
      recognises three forms — (1) `export function name()`, (2) `export const|let|var name`,
      and (3) `export { name1, name2, ... };` named-list (with optional `as` aliasing) — so a
      module that re-exports already-declared identifiers at file tail (e.g. js/pages.js) is
      correctly inventoried. Each module must also stay import-free (a dependency-free leaf).
      This turns the hand-maintained cross-file contract into a machine-enforced invariant.
      (BLOCKING)
  56. js/ leaf module factory-pattern parameter coverage: for each js/ module that uses the
      factory pattern (`export function createFoo({deps})` — note: the leading argument MUST
      be a destructured object `{...}` so that a plain utility named `createXxx` like
      `createIcon(name, size)` is correctly NOT classified as a factory), main.js MUST invoke
      the factory `createFoo({...})` at least once. A factory exported but never invoked is
      the Stage 5-j bug class: the module compiles fine, ESLint passes, Check 47 passes
      (import/export bijection holds), but at runtime any caller of the page/manager hits
      ReferenceError because the dependency identifiers are never bound. This check converts
      that latent runtime failure into a pre-commit BLOCKING error. (BLOCKING)
  57. index.html modulepreload ↔ _modules47 set equality: index.html の
      `<link rel="modulepreload" href="./js/<name>.js">` の集合と check_repository_
      consistency.py の `_modules47` リストの集合が完全一致することを機械強制する。これにより、
      新しい葉モジュールを抽出したが modulepreload に追加し忘れた場合（初期ロード遅延）や、
      modulepreload に存在するが _modules47 から脱落した場合（lint カバレッジ漏れ）の
      drift を pre-commit でブロックする。Check 47（import/export bijection）と Check 53
      （modulepreload href 解決）を補完する「集合カバレッジ」検査。(BLOCKING)
  61. js/*.js factory documentation marker: 各 js/ 葉モジュールが factory pattern を export
      する場合（`export function createXxx`）、ファイル先頭の docstring に "factory pattern"
      キーワードが含まれていることを機械強制する。これは「factory として抽出した経緯」を
      後続 AI / 人間レビュアーが file 単体を読むだけで認識できることを保証し、抽出経緯の
      ドキュメント drift を構造的に閉じる。(BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings

    # ── 47. main.js ⇄ js/ module ESM import/export contract (BLOCKING) ────────────
    # The v80+ staged split physically extracted layers of main.js into local ES modules
    # (Stage 2: js/pure-utils.js — pure utilities; Stage 3: js/quiz-data.js — static quiz
    # datasets). main.js now `import`s specific names from each module, and each module
    # `export`s a set of names. Those lists are a hand-maintained cross-file contract spread
    # across three files. Because the site is build-free and served directly by GitHub Pages,
    # a mismatch is a *runtime* failure, not a lint nit:
    #   - importing a name a module does NOT export → the browser throws a module-load error
    #     (e.g. "does not provide an export named 'foo'") and the ENTIRE SPA fails to boot. No
    #     other check catches this: node --check validates each file's syntax in isolation; it
    #     never cross-checks one file's import names against another file's exports.
    #   - an export nothing imports → a harmless but real signal that the split has drifted (a
    #     name was removed from main.js's import list but left in the module, or added to the
    #     module speculatively). We require an exact bijection per module so the split stays
    #     intentional. NOTE: this is precisely the guard that would have caught the Stage 3
    #     near-miss in which main.js referenced four quiz datasets (aws/pm/quality/architecture)
    #     while an early draft of js/quiz-data.js exported only two — the dangling references
    #     would have failed this check immediately.
    # Parsing notes (both learned from real bugs while authoring this check):
    #   (a) the import lists carry one inline `//` comment per name, so we strip per-line
    #       comments BEFORE extracting identifiers — a naive split would read a comment fragment
    #       as a name; and
    #   (b) the captured brace group is [^{}]*? so each `import {…} from '<module>'` block is
    #       matched in isolation and a match cannot span across an adjacent import block (with a
    #       greedy/dotall group, the pure-utils block bled into the quiz-data match).
    # We also assert each module stays import-free: it is a dependency-free leaf of the module
    # graph (Boring Technology — the utility/data layers depend on nothing), so an accidental
    # import into one is itself a regression.
    # This is a configuration/wiring invariant (it checks the module contract, not the JS
    # behaviour, which node --check and the browser cover).
    _main_src47 = (ROOT / "main.js").read_text(encoding="utf-8")
    # Each tuple: (import specifier as written in main.js, module file path on disk).
    # v80+ Stage 3-b: the single js/quiz-data.js was split into four domain leaf modules under
    # js/quiz/, each exporting exactly one dataset. The check loops over all module specs, so the
    # per-module import/export bijection (47a/47b) and leaf-ness (47c) now cover all four — adding
    # or removing a quiz module without wiring main.js's import would fail this check immediately.
    # v80+ Stage 4: js/ui-components.js added — DOM builder (h), SVG icon helper (createIcon),
    # Toast notification system, and BGM manager extracted as a single leaf module (no local imports).
    # All four exports are used in main.js's IIFE; Check 47b enforces bijection.
    # v80+ Stage 5: js/router.js (hash-based SPA router) and js/page-meta.js (per-page SEO metadata)
    # extracted as leaf modules. Router had one closure dep (CONSTANTS.DEBUG, production dead code)
    # which was removed. PAGE_META's dynamic entries are pure functions that accept state/params as
    # arguments — no closure deps. Both are leaves (no local imports).
    # v80+ Stage 5-b → 5-j fix: js/pages.js (HiringRiskPage / RoleSplitPage / NotFoundPage + 4 helpers)
    # was originally extracted with IMPLICIT GLOBAL references to h/createIcon/Router (Stage 5-b).
    # That was a hidden ReferenceError bug — ESM module scope doesn't see main.js IIFE bindings,
    # so calling the page functions at runtime would throw. Playwright never visited /#/hiring-risk
    # or /#/role-split, so CI stayed green and the bug latent. Stage 5-j refactored to the same
    # factory pattern as Brand/Store/State/Theme: `createPages({h, createIcon, Router})` accepts
    # the dependencies as injected arguments and the closure binds them for the returned page
    # functions. main.js destructures the result: `const { HiringRiskPage, RoleSplitPage,
    # NotFoundPage } = createPages({ h, createIcon, Router })`. Public usage sites unchanged.
    # v80+ Stage 5-c: js/storage.js (Safe localStorage wrapper) extracted as a leaf module. The
    # four methods (get/set/remove/parse) operate purely on the (key, value) arguments and the
    # global localStorage API — no IIFE closure state, no DOM, no CONSTANTS dependency. The earlier
    # extraction-map §3.5 classification "Safe Storage = mid/high risk (schema backward-compat)"
    # referred to the callers' contract over localStorage keys/values, not to module-level closure
    # deps, so the module itself extracts cleanly. The schema backward-compat responsibility stays
    # with the callers (main.js controls all key/value formats).
    # v80+ Stage 5-d: js/constants.js (application runtime constants: STORAGE_KEY / LIMITS /
    # timing / DEBUG / TAB_ID) extracted as a leaf module. SITE_CONFIG.VERSION/LAST_UPDATED stay
    # in main.js (Check 2 / 17 extract them by name from main.js). CONSTANTS only references
    # browser globals (crypto, sessionStorage, location, URLSearchParams, Date, Math) — no IIFE
    # closure deps. TAB_ID's IIFE side-effect (one-time sessionStorage write) executes once at
    # module load, equivalent to its prior one-time evaluation inside main.js's IIFE.
    # v80+ Stage 5-e: js/identity.js (AUTHOR: DISPLAY_NAME / AUTHORITATIVE_NAME / JAPANESE_NAME)
    # extracted as a leaf module. Pure data with closure-deps = none. Values are byte-equivalent
    # and main.js is not in the AIO digest chain, so AI citation / entity identity is unaffected.
    # The UI vs AIO dependency-direction contract (UI → DISPLAY_NAME only / AIO → AUTHORITATIVE_NAME)
    # stays enforced by the values themselves, not by module location.
    # v80+ Stage 5-f: js/brand.js (Brand: primary palette/font manager) extracted via the factory
    # pattern. The module exports `createBrand(storage)` rather than a pre-built Brand object —
    # main.js composes `const Brand = createBrand(Storage)` to inject the Storage dependency
    # while the module itself stays a dependency-free leaf (Check 47c: zero imports). This is the
    # canonical pattern for extracting service-rail modules that have logical dependencies on
    # other extracted modules without forming a cross-module import graph.
    # v80+ Stage 5-g: js/store.js (Store: default data + load/validate/normalize/similarity) extracted
    # via the same factory pattern. createStore({AUTHOR, CONSTANTS, Storage, generateId, deepClone,
    # slugify, sanitizeUrl, clamp}) accepts all dependencies as injected arguments. The 488-line
    # Store IIFE body (defaultProfile / defaultProjects / defaultAppsData + helpers + validation +
    # tokenizeForSimilarity local) is preserved byte-equivalent inside the factory. Public API
    # {load, createDefaultStore, validateAndNormalize, autoRelatedCandidates} unchanged.
    # v80+ Stage 5-h: js/state.js (State: Proxy type-safety monitor + subscriber + cross-tab sync +
    # auto-save) extracted via the factory pattern. createState({CONSTANTS, Store, Storage, Toast})
    # accepts dependencies as injected arguments. The 209-line State IIFE body (Proxy wrapper /
    # subscribe-notify / save debounce / cross-tab storage event listener) is preserved
    # byte-equivalent. Public API {get, set, update, subscribe, saveNow} unchanged.
    # v80+ Stage 5-i: js/theme.js (Theme: system/dark/light cycle + matchMedia listener) extracted
    # via the factory pattern. createTheme({State, Toast}) accepts the State and Toast dependencies.
    # The 38-line Theme IIFE body (apply/cycle/init + DOM data-theme attribute + meta theme-color
    # + window.matchMedia subscription) is preserved byte-equivalent. Public API {apply, cycle, init}
    # unchanged.
    # v80+ Stage 5-l: js/meta-management.js (4 SRP sub-functions: updateDocumentHead /
    # announceRouteForAccessibility / injectRouteEntityAnchor / injectStructuredData + applyMeta
    # facade) extracted via the factory pattern. createMetaManagement({SITE_CONFIG, AUTHOR,
    # PAGE_META, Router, State}) accepts dependencies as injected arguments. The 165-line Meta
    # Management block (document.head/title/meta/OG/Twitter/canonical/robots + aria-live +
    # AIO entity anchor + Article/Speakable JSON-LD) is preserved byte-equivalent. Public API
    # {applyMeta} unchanged. EffectRails dispatch and renderer (_renderCore) both call applyMeta
    # through the same closure binding.
    _modules47 = [
        ("./js/aidk-rails.js",                  ROOT / "js" / "aidk-rails.js"),
        ("./js/apps.js",                        ROOT / "js" / "apps.js"),
        ("./js/brand.js",                       ROOT / "js" / "brand.js"),
        ("./js/components.js",                  ROOT / "js" / "components.js"),
        ("./js/constants.js",                   ROOT / "js" / "constants.js"),
        ("./js/fatal-overlay.js",               ROOT / "js" / "fatal-overlay.js"),
        ("./js/identity.js",                    ROOT / "js" / "identity.js"),
        ("./js/meta-management.js",             ROOT / "js" / "meta-management.js"),
        ("./js/mobile-drawer.js",               ROOT / "js" / "mobile-drawer.js"),
        ("./js/page-meta.js",                   ROOT / "js" / "page-meta.js"),
        ("./js/pages.js",                       ROOT / "js" / "pages.js"),
        ("./js/perf-guards.js",                 ROOT / "js" / "perf-guards.js"),
        ("./js/pure-utils.js",                  ROOT / "js" / "pure-utils.js"),
        ("./js/quiz-renderer.js",               ROOT / "js" / "quiz-renderer.js"),
        ("./js/router.js",                      ROOT / "js" / "router.js"),
        ("./js/state.js",                       ROOT / "js" / "state.js"),
        ("./js/storage.js",                     ROOT / "js" / "storage.js"),
        ("./js/store.js",                       ROOT / "js" / "store.js"),
        ("./js/theme.js",                       ROOT / "js" / "theme.js"),
        ("./js/ui-components.js",               ROOT / "js" / "ui-components.js"),
        ("./js/quiz/architecture-quiz-data.js", ROOT / "js" / "quiz" / "architecture-quiz-data.js"),
        ("./js/quiz/aws-quiz-data.js",          ROOT / "js" / "quiz" / "aws-quiz-data.js"),
        ("./js/quiz/pm-quiz-data.js",           ROOT / "js" / "quiz" / "pm-quiz-data.js"),
        ("./js/quiz/quality-quiz-data.js",      ROOT / "js" / "quiz" / "quality-quiz-data.js"),
    ]
    for _spec47, _mpath47 in _modules47:
        if not _mpath47.exists():
            check(False, "",
                  f"Check 47: {_spec47} is missing while main.js may still import from it "
                  "(the staged-split module was removed without updating main.js)",
                  blocking=True)
            continue
        _msrc47 = _mpath47.read_text(encoding="utf-8")

        # ── Names main.js imports from THIS module ──
        # [^{}]*? keeps the match inside a single import block (cannot span an adjacent block).
        _imp_m47 = re.search(r"import\s*\{([^{}]*?)\}\s*from\s*'" + re.escape(_spec47) + r"'",
                             _main_src47, re.DOTALL)
        _imported47 = set()
        if _imp_m47:
            _block_nc47 = re.sub(r"//[^\n]*", "", _imp_m47.group(1))  # strip inline comments first
            for _tok47 in re.split(r"[,\n]", _block_nc47):
                _name47 = _tok47.strip()
                if re.fullmatch(r"[A-Za-z_$][\w$]*", _name47):
                    _imported47.add(_name47)

        # ── Names THIS module exports (function / const / let / var / named-list) ──
        # Supports three ECMAScript export forms:
        #   1. `export function name() ...` / `export async function name() ...`
        #   2. `export const name = ...` / `export let name = ...` / `export var name = ...`
        #   3. `export { name1, name2, name3 };` (named-list, optionally with `as` aliasing)
        # The named-list form is the canonical way to export multiple already-declared
        # identifiers in one statement — js/pages.js uses it at the file tail. Failing to
        # parse it would silently mask import/export drift (this exact gap was caught when
        # js/pages.js was first added to _modules47: Check 47a flagged HiringRiskPage /
        # RoleSplitPage / NotFoundPage as "not exported" because only forms (1) and (2)
        # were recognised). The parser strips per-line comments inside the brace block,
        # handles `as`-aliased re-exports by taking the exposed (right-hand) name, and
        # only accepts valid identifier tokens.
        _exported47 = set(re.findall(r"^export\s+(?:async\s+)?function\s+([A-Za-z_$][\w$]*)",
                                     _msrc47, re.MULTILINE))
        _exported47 |= set(re.findall(r"^export\s+(?:const|let|var)\s+([A-Za-z_$][\w$]*)",
                                      _msrc47, re.MULTILINE))
        for _named_block47 in re.findall(r"^export\s*\{([^{}]*)\}\s*;?", _msrc47, re.MULTILINE):
            _block_nc47 = re.sub(r"//[^\n]*", "", _named_block47)  # strip inline comments
            for _tok47 in re.split(r"[,\n]", _block_nc47):
                _name47 = _tok47.strip()
                # `export { foo as bar }` — bar is the exposed external name
                if re.search(r"\bas\b", _name47):
                    _name47 = re.split(r"\s+as\s+", _name47)[-1].strip()
                if re.fullmatch(r"[A-Za-z_$][\w$]*", _name47):
                    _exported47.add(_name47)

        _short47 = _spec47.replace("./", "")

        # 47a — every imported name is actually exported (else the SPA fails to boot).
        _missing47 = _imported47 - _exported47
        check(not _missing47,
              f"Check 47a [{_short47}]: every name main.js imports is exported by the module "
              f"({len(_imported47)} names)",
              f"Check 47a [{_short47}]: main.js imports name(s) the module does NOT export: "
              f"{sorted(_missing47)} — this throws a module-load error and the SPA fails to boot",
              blocking=True)

        # 47b — every export is imported (exact bijection; no drifted/orphan exports).
        _orphan47 = _exported47 - _imported47
        check(not _orphan47,
              f"Check 47b [{_short47}]: every name the module exports is imported by main.js "
              "(exact import/export bijection — no orphan exports)",
              f"Check 47b [{_short47}]: the module exports name(s) main.js does not import: "
              f"{sorted(_orphan47)} — the split has drifted; remove the unused export or wire it up",
              blocking=True)

        # 47c — the module stays a dependency-free leaf (no imports of its own).
        _leaf_imports47 = re.findall(r"^\s*import\b", _msrc47, re.MULTILINE)
        check(not _leaf_imports47,
              f"Check 47c [{_short47}]: the module is a dependency-free leaf (imports nothing)",
              f"Check 47c [{_short47}]: the module has {len(_leaf_imports47)} import statement(s) "
              "— extracted leaf layers must not depend on other modules (Boring Technology)",
              blocking=True)

    # ── 56. js/ leaf modules: factory pattern parameter coverage (BLOCKING) ───────
    # Stage 5-j で発見した js/pages.js (元 Stage 5-b) の hidden ReferenceError は、
    # 葉モジュール内の関数本体が IIFE 外スコープのバインディング (h, createIcon,
    # Router) を未定義の暗黙グローバルとして参照していたために起きた。
    # factory pattern (createFoo({deps}) → instance) で抽出すれば、deps が
    # factory 引数で bind されるため安全だが、これは構造的に強制されていなかった。
    #
    # 本 Check は js/ 配下の各葉モジュール（_modules47）について、main.js での
    # 使用パターンが以下のいずれかに該当することを検査する:
    #   (A) 値 export (`export const Foo = ...` / `export function Foo() {...}` /
    #       `export { Foo }`) → main.js は `import { Foo }` で取得・直接使用
    #   (B) factory export (`export function createFoo(deps)` / `export function
    #       createXxx(deps)`) → main.js は `import { createFoo }` で取得し
    #       `const Foo = createFoo({...})` で合成
    #
    # (A) は closure-deps = none が前提（葉契約 = Check 47c で機械強制）。
    # (B) は deps を引数で受けるため、葉契約を破らずに service-rail 結合を表現できる。
    #
    # 本 Check は「main.js の使用形式と module の export 形式の一致」を検査する:
    # - module が `createFoo` を export しているのに main.js が `const X = createFoo(...)`
    #   していない → 引数注入忘れ → 関数実行時 ReferenceError 危険
    # - 逆に module が `Foo` を直接 export しているのに main.js が `createFoo(...)`
    #   している → 構文 error (call on object)
    _factory_usage_mismatches = []
    for _spec56, _mpath56 in _modules47:
        if not _mpath56.exists():
            continue
        _msrc56 = _mpath56.read_text(encoding="utf-8")
        # factory pattern? `export function createXxx({ ... })` がある
        # 「createXxx」かつ「先頭引数が destructured object `{`」のもののみを factory とみなす。
        # 単純な純粋関数 `export function createIcon(name, size)` は factory ではない（false positive 防止）。
        _factory_re56 = re.search(r"^export\s+function\s+(create[A-Z][A-Za-z0-9_]*)\s*\(\s*\{",
                                  _msrc56, re.MULTILINE)
        _short56 = _spec56.replace("./", "")
        if _factory_re56:
            _factory_name56 = _factory_re56.group(1)
            # main.js で `const ... = createXxx(...)` という使用形式があるはず
            _usage_re56 = re.search(
                r"\b" + re.escape(_factory_name56) + r"\s*\(",
                _main_src47,
            )
            if not _usage_re56:
                _factory_usage_mismatches.append(
                    f"{_short56}: exports factory `{_factory_name56}` but main.js never calls it"
                )
    _factory_count56 = sum(
        1 for _spec, _path in _modules47
        if _path.exists()
        and re.search(r"^export\s+function\s+create", _path.read_text(encoding="utf-8"), re.MULTILINE)
    )
    check(
        not _factory_usage_mismatches,
        f"Check 56: factory-pattern modules in js/ are all invoked from main.js "
        f"({_factory_count56} factories detected)",
        f"Check 56: factory-pattern module(s) exported but not invoked from main.js: "
        f"{_factory_usage_mismatches} — this is the Stage 5-j class of bug (extracted module's "
        f"functions would throw ReferenceError when called because dependencies are never bound). "
        f"Either invoke the factory in main.js or remove the orphan export.",
    )

    # ── 57. index.html modulepreload ↔ _modules47 set equality (BLOCKING) ─────────
    # 葉モジュール抽出が進むほど、(a) index.html の modulepreload リスト、(b) _modules47
    # リスト、(c) package.json の lint/lint:js リスト、の 3 つの集合を同期させ続ける運用
    # 規律が重要になる。Check 46 が (b) ↔ (c) を、Check 53 が (a) の href 解決を機械強制して
    # いるが、(a) ↔ (b) の集合一致は未強制だった。本 Check で (a) と (b) の対称差を 0 に
    # 機械強制し、modulepreload 漏れ／余計 preload を pre-commit で即検出する。
    _idx57 = ROOT / "index.html"
    if _idx57.exists():
        _html57 = _idx57.read_text(encoding="utf-8")
        _preload57 = set(re.findall(r'<link\s+rel="modulepreload"\s+href="\.?/?(js/[^"]+\.js)"', _html57))
        _modules57 = {spec.replace("./", "") for spec, _ in _modules47}
        _only_preload57 = sorted(_preload57 - _modules57)
        _only_modules57 = sorted(_modules57 - _preload57)
        check(
            # _modules57 非空ガード: 両集合が空 (main.js が import を失い、index.html も preload ゼロ)
            # のとき対称差 0 で vacuous pass するのを防ぐ。葉モジュール集合は常に非空であるべき。
            bool(_modules57) and not _only_preload57 and not _only_modules57,
            f"Check 57: index.html modulepreload ({len(_preload57)}) and _modules47 ({len(_modules57)}) "
            f"are exact set-equal",
            f"Check 57: modulepreload ↔ _modules47 drift — only in modulepreload: "
            f"{_only_preload57}; only in _modules47: {_only_modules57}",
        )
    else:
        warnings.append("Check 57: index.html not found — modulepreload set check skipped")

    # ── 61. js/*.js factory documentation marker (BLOCKING) ───────────────────────
    # 各 js/ 葉モジュールが factory pattern (`export function createXxx({...})`) を export する
    # 場合、ファイル先頭の docstring に "factory pattern" キーワードが含まれていることを機械
    # 強制する。これは「factory として抽出した経緯」を後続 AI / 人間レビュアーが file 単体を
    # 読むだけで認識できることを保証し、抽出経緯のドキュメント drift を構造的に閉じる。
    _doc_drift61 = []
    _factory_count61 = 0
    _FACTORY_RE61 = re.compile(r"^export\s+function\s+create[A-Z][A-Za-z0-9_]*\s*\(\s*\{", re.MULTILINE)
    for _spec61, _path61 in _modules47:
        if not _path61.exists():
            continue
        _src61 = _path61.read_text(encoding="utf-8")
        if _FACTORY_RE61.search(_src61):
            _factory_count61 += 1
            # docstring (ファイル先頭の /** ... */) に "factory pattern" を含むか
            _docstring61 = re.match(r"\s*/\*\*([\s\S]*?)\*/", _src61)
            if not _docstring61 or "factory pattern" not in _docstring61.group(1).lower():
                _doc_drift61.append(_spec61.replace("./", ""))
    check(
        not _doc_drift61,
        f"Check 61: all factory-pattern modules in js/ contain 'factory pattern' marker "
        f"in their docstring ({_factory_count61} factory modules)",
        f"Check 61: factory-pattern modules missing 'factory pattern' marker in docstring: "
        f"{_doc_drift61} — add a header comment noting that the module uses the factory pattern, "
        f"for the benefit of future readers (AI or human).",
    )
