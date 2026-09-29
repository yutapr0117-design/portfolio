"""mutation_samples_archive3.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE3 = [
    {
        "name": "Check 414: 葉モジュールへの組み込み prototype 書き換えの再混入 — perf-guards.js に Element.prototype への代入を戻す → DOM の意味論がサイト内だけ非標準になる。かつて実在した hook (setProperty / setAttribute(\'style\') の rAF 遅延バッチ) は shipped JS が全て直接代入を使うため一度も発火せず利益ゼロだった一方、e2e で style を書いて同期で読む診断を全て偽陰性にし、レイアウト調査 1 サイクルを無効化した実害がある。この class は「壊れる」のではなく「黙って別物になる」ため consistency 以外のどの gate も捕捉しない",
        "file": ROOT / "js" / "perf-guards.js",
        "find": "    return { installMediaLifecycleGuard };",
        "replace": "    Element.prototype.__reintroduced = 1;\n    return { installMediaLifecycleGuard };",
    },
    {
        # NOTE (honest): この mutation は Check 415 と Check 121 の **両方** を RED にする
        # (STATUS.md を書き換えるので regenerate-compare も落ちる)。Check 415 が *単独で* 効く
        # ケース = 「生成器が取りこぼし、その出力で STATUS.md も再生成されたので両者は一致して
        # いるが監査面は不完全」は **2 ファイル同時の変更**であり find/replace 1 箇所では表現できない。
        # そのケースの非 vacuity は手動で実証済 (生成器の走査を先頭 800 文字へ戻して `npm run status`
        # で再生成 → Check 121 は緑のまま Check 415 が RED → 復元で緑)。
        "name": "Check 415: 定期実行 workflow が監査面から欠落 — STATUS.md から mutation-probe.yml のバッジ行を削る → 週次で走る安全網の自己検証が赤くなってもオーナーに届かない。定期実行は PR を止めないため、STATUS.md の監査節が唯一の気付ける場所であり、そこから漏れると失敗が恒久的に不可視になる",
        "file": ROOT / "STATUS.md",
        "find": "- ![mutation-probe.yml](https://github.com/yutapr0117-design/portfolio/actions/workflows/mutation-probe.yml/badge.svg?branch=main)",
        "replace": "",
    },
    {
        "name": "Check 416: behavior ゲートの第三者 CDN 切り離しが外れる — playwright.config.cjs の host-resolver-rules を無効化 → BLOCKING ゲートが再び KARTE / Google Fonts の可用性に依存する。実測で 1 ナビゲーションごとに 6 ホストへ 9 リクエストが飛び goto の既定 waitUntil='load' がそれを待つため、外部が遅い/落ちるだけでコードが正しくてもゲートが赤くなる (2026-08-10 に .hero-section の 30s timeout として実際に flake 化)",
        "file": ROOT / "playwright.config.cjs",
        "find": "host-resolver-rules",
        "replace": "host-disabled-rules",
    },
    {
        "name": "Check 417: ingestion 文字列ガードの再混入 — store.js の project name を旧実装 `String(raw.name || 'Untitled')` へ戻す → truthy な非文字列 ({}) が素通りし \"[object Object]\" が一覧・詳細へ描画される。2026-08-10 に profile/projects/appsData で 3 連続の実バグを出した class を構造防止へ昇華したもの (Check 364 の文字列面の対)",
        "file": ROOT / "js" / "store.js",
        "find": "            name: safeStr(raw.name, 'Untitled', CONSTANTS.LIMITS.PROJECT_NAME),",
        "replace": "            name: String(raw.name || 'Untitled').slice(0, CONSTANTS.LIMITS.PROJECT_NAME),",
    },
    {
        "name": "Check 418: 到達不能な ActionDelegator handler の再混入 — 発火経路の無い handler を _handlers へ足す → その handler のためだけに依存 (factory 引数 / late-binding holder) を引きずる死にコードが蓄積する。icon 面 (Check 375b) と同じ定義⟹使用ガードの action 面",
        "file": ROOT / "js" / "aidk-rails.js",
        "find": "            'theme:cycle':    () => { if (typeof Theme !== 'undefined') { Theme.cycle(); } },",
        "replace": "            'ghost:action':   () => {},\n            'theme:cycle':    () => { if (typeof Theme !== 'undefined') { Theme.cycle(); } },",
    },
    {
        "name": "Check 419: mirror doc の canonical-ref が行き止まりになる — sitemap.xml.md の参照先を存在しないパスへ変える → 「この file を理解するには次を読め」という読者の導線が解決しなくなる。参照は本文でなく frontmatter にあるため人の目に触れにくく、リネーム/移動で silent に腐る (実測で 511 参照中 7 件が裸のファイル名のまま解決していなかった)",
        "file": ROOT / "docs" / "files" / "sitemap.xml.md",
        "find": ".well-known/aio-manifest.json",
        "replace": ".well-known/NO-SUCH-manifest.json",
    },
    {
        "name": "Check 421: 明示 behavior:'smooth' の reduced-motion ガードが外れる — home-page.js の matchMedia 問い合わせを false へ潰す → CSSOM-View では behavior を明示した時点で CSS の scroll-behavior が参照されないため、style.css の reduce override では止まらず、前庭障害のユーザーにも 1,000px 超のアニメーションが走る (WCAG 2.3.3)。fatal も視覚差分も出ないので静的にはこの Check だけが捕捉する",
        "file": ROOT / "js" / "home-page.js",
        "find": "window.matchMedia('(prefers-reduced-motion: reduce)').matches",
        "replace": "false",
    },
    {
        "name": "Check 415: 公開サイトのデプロイ本体 (pages-build-deployment) が監査導線から消える — STATUS.md はオーナーの唯一の監査導線で、Pages デプロイはリポジトリに file が無いため generate_status.py の走査には出てこない。全 PR ゲートが緑でもこれだけ落ちればサイトは古いまま残るので、リテラルで固定して消えないようにする",
        "file": ROOT / "STATUS.md",
        "find": "/actions/workflows/pages/pages-build-deployment/badge.svg",
        "replace": "/actions/workflows/pages/REMOVED/badge.svg",
    },
    {
        "name": "Check 423: 公開サイト版数検証の配線が切れる — script file を残したまま workflow の 1 行を消せば silent に無効化でき、mirror-bijection (Check 108) は file の存在しか見ないので気付けない。この配線が切れると『Pages が古い成果物を配信し続けている』状態が全ゲート緑のまま成立する",
        "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
        "find": "        run: python3 .github/scripts/check_deployed_freshness.py",
        "replace": "        run: echo skipped",
    },
    {
        "name": "Check 422: 再描画で消えるコントロールから focus 復元用の id が外れる — apps.js の絞り込み select から id を落とす → main.js _renderCore の復元は id を鍵にしているため、そのコントロールだけが取り残されて change のたび focus が body へ落ちる。マウスでは気付きにくく fatal も視覚差分も出ないので、静的にはこの Check だけが捕捉する",
        "file": ROOT / "js" / "apps.js",
        "find": "                        id: 'task-filter-priority',\n",
        "replace": "",
    },
    {
        "name": "Check 424: file-size-budget.md §2 表の実測行数が実測とズレても検出しない — §2 は人間可読な要約ゆえ長らく『一致は人間レビューで保つ』とだけ書かれ誰も検証しておらず、実測すると 62 行中 44 行が stale (最大 366 行ズレ) だった。cold-start の読者はこの表で headroom を判断するため間違った数値は無いより悪い",
        "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
        "find": "| `js/identity.js` | 36 |",
        "replace": "| `js/identity.js` | 37 |",
    },
    {
        "name": "Check 425: data-action と onclick が併存しても検出しない — ActionDelegator は data-action を単一の delegated リスナーで処理するので、同じ要素に onclick を足すと 1 クリックで必ず二重発火する (#262 の実バグ = theme 2 段送り / drawer scroll 先頭ジャンプ / BGM 二重 toggle)。Check 129 は main.js の topbar 3 ボタンしか見ないため他 file では素通りしていた",
        "file": ROOT / "js" / "components.js",
        "find": "                    dataset: { bgmBtn: '' },",
        "replace": "                    dataset: { bgmBtn: '' },\n                    'data-action': 'bgm:toggle',",
    },
    {
        "name": "Check 426: 2 つのバイナリ資産の entity 帰属が食い違っても検出しない — asset:image:entity / asset:audio:entity は WebP と MP3 の帰属先を AI クローラへ宣言する meta で、片方だけ変えても視覚にも behavior にも一切出ない。実測 (2026-08-17) ではこの entity 宣言を見ている層が皆無で、書き換えても全 gate が緑だった (#930 と同じ『宣言はあるが見ている層がゼロ』class)。単独 mutation で 426c だけが発火することを確認済み",
        "file": ROOT / "index.html",
        "find": 'name="asset:audio:entity" content="Yuta Yokoi (横井雄太 / Yokoi Yuta)"',
        "replace": 'name="asset:audio:entity" content="Someone Else"',
    },
    {
        "name": "Check 429: import \u3055\u308c\u3066\u3044\u308b\u3060\u3051\u3067\u4e00\u5ea6\u3082\u4f7f\u308f\u308c\u306a\u3044 pure-utils export \u3092\u691c\u51fa\u3057\u306a\u3044 \u2014\u2014 Check 47 \u306f\u300cexport \u21d4 import\u300d\u306e bijection \u3057\u304b\u898b\u306a\u3044\u305f\u3081\u3001import \u306f\u3055\u308c\u3066\u3044\u308b\u304c\u547c\u3070\u308c\u306a\u3044 export \u3092\u7d20\u901a\u308a\u3055\u305b\u308b\u3002ESLint \u3082 main.js \u304c\u5fc5\u305a import \u3059\u308b\u4ee5\u4e0a\u300c\u4f7f\u7528\u6e08\u307f\u300d\u3068\u898b\u306a\u3059\u3002\u5b9f\u4f8b: safeFetchJSON \u304c\u547c\u3073\u51fa\u3057 0 \u4ef6\u306e never-wired \u6b8b\u9ab8\u3068\u3057\u3066\u6b8b\u3063\u3066\u3044\u305f",
        "file": ROOT / "main.js",
        "find": "debounce(syncMobileDrawer, CONSTANTS.DEBOUNCE_DELAY)",
        "replace": "syncMobileDrawer",
    },
    {
        "name": "Check 427: BLOCKING の behavior gate が main で走らなくなり監査バッジが空白へ戻る — playwright-regression.yml から push(main) トリガを外すと、その workflow の run は PR の head 側にしか記録されず main に残らないため、STATUS.md の ?branch=main バッジが永久に 'no status' の空白になる。オーナーの唯一の監査導線に『緑』ではなく『何も分からない』が出るが、Check 415 は『バッジが在るか』しか見ないので素通りする",
        "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
        "find": "  push:\n    branches: [ \"main\" ]\n    paths:",
        "replace": "  push_disabled:\n    branches: [ \"main\" ]\n    paths:",
    },
    {
        "name": "Check 142b: BLOCKING gate が自身の定義変更を検証しなくなる — playwright-regression.yml の paths から自己参照を外すと、job 構成 / env / step を書き換えても behavior gate が一度も走らずに merge できる (実測 #1099: この workflow を書き換えた PR で playwright-validation が起動しなかった)。package.json を trigger に入れているのと同一 class",
        "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
        "find": "      - '.github/workflows/playwright-regression.yml'\n",
        "replace": "",
    },
    {
        "name": "Check 142c: push / pull_request の paths が非対称になる — 片方だけに path を足すと『PR では走るのに main では走らない』(逆も) 状態ができ、merge ゲートと監査バッジ (Check 427) の守備範囲がずれる。2 ブロック構成は #1099 で導入したもので、以後どちらか一方だけを編集する事故が起こりうる",
        "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
        "find": "  pull_request:\n    branches: [ \"main\" ]\n    paths:\n      - 'index.html'",
        "replace": "  pull_request:\n    branches: [ \"main\" ]\n    paths:\n      - 'README.md'\n      - 'index.html'",
    },
    {
        "name": "Check 428: 未定義のカスタムプロパティをフォールバック無しで参照しても検出しない — `var(--x)` の `--x` が未定義だと宣言ごと invalid at computed-value time になり **プロパティが初期値へ落ちる**。実測では hover 背景が透明になり『持ち上げて強調する』はずの操作でカードが表面を失っていた。エラーも警告も出ず stylelint も通り screenshot は ADVISORY なので、この Check だけが捕捉層",
        "file": ROOT / "style.css",
        "find": "            background: var(--surface-hover);",
        "replace": "            background: var(--card-bg);",
    },
    {
        "name": "Check 431: \u767b\u9332\u6e08\u307f\u306a\u306e\u306b\u5b9f\u884c\u3055\u308c\u306a\u3044 Check module \u3092\u691c\u51fa\u3057\u306a\u3044 \u2014\u2014 run(_ctx) \u306e 1 \u884c\u3092\u5916\u3059\u3068\u3001\u305d\u306e module \u306e Check \u306f runbook \u00a79 \u306e\u7dcf\u6570\u306b\u6570\u3048\u3089\u308c Check 45 \u306b\u3082\u691c\u8a3c\u3055\u308c\u308b\u306e\u306b **\u4e00\u5ea6\u3082\u5b9f\u884c\u3055\u308c\u306a\u3044**\u3002\u300cN \u500b\u306e Check \u304c\u5b88\u3063\u3066\u3044\u308b\u300d\u3068\u3044\u3046\u8a18\u8ff0\u304c\u5618\u306b\u306a\u308b\u304c\u3001\u5931\u6557\u306f\u4e00\u5207\u306e signal \u3092\u51fa\u3055\u306a\u3044",
        "file": ROOT / ".github" / "scripts" / "check_repository_consistency.py",
        "find": "_checks_css.run(_ctx)",
        "replace": "pass  # mutated",
    },
    {
        "name": "Check 432: \u5ba3\u8a00\u7684\u306a test.skip \u3092\u691c\u51fa\u3057\u306a\u3044 \u2014\u2014 test( \u3092 test.skip( \u306b\u5909\u3048\u308b\u3060\u3051\u3067\u305d\u306e\u30c6\u30b9\u30c8\u306f\u5b8c\u5168\u306b\u7121\u52b9\u5316\u3055\u308c\u308b\u306e\u306b CI \u306f\u7dd1\u306e\u307e\u307e\u3067\u3001\u8986\u3063\u3066\u3044\u305f\u6319\u52d5\u304c\u7121\u9632\u5099\u306b\u306a\u3063\u305f\u3053\u3068\u306b\u8ab0\u3082\u6c17\u4ed8\u3051\u306a\u3044 (Check 114 \u306e .only \u306e\u88cf\u8fd4\u3057)",
        "file": ROOT / "e2e" / "print.spec.js",
        "find": "test('\u5370\u5237\u6642\u306f\u30ca\u30d3 chrome \u304c\u6d88\u3048",
        "replace": "test.skip('\u5370\u5237\u6642\u306f\u30ca\u30d3 chrome \u304c\u6d88\u3048",
    },
    {
        "name": "Check 433: \u610f\u5473\u3092\u6301\u3064\u30af\u30e9\u30b9\u306b CSS \u5ba3\u8a00\u304c\u7121\u3044\u72b6\u614b\u3092\u691c\u51fa\u3057\u306a\u3044 \u2014\u2014 .alert-error \u306e\u5ba3\u8a00\u3092\u524a\u308b\u3068\u3001\u30b3\u30fc\u30c9\u306f\u7a2e\u5225\u3092\u9078\u3073\u5206\u3051\u3066\u3044\u308b\u306e\u306b\u5b9f\u969b\u306f\u5168\u3066\u540c\u3058\u306b\u63cf\u304b\u308c\u308b\u72b6\u614b\u3078\u623b\u308b (#1160 / #1166 \u3067\u5b9f\u30d0\u30b0\u5316\u3057\u305f class)",
        "file": ROOT / "style.css",
        "find": "        .alert-error   { border-left-color: var(--on-tint-danger); }\n",
        "replace": "",
    },
    {
        "name": "Check 434: verify \u304c\u672a\u8ffd\u8de1\u30d5\u30a1\u30a4\u30eb\u3092\u898b\u843d\u3068\u3057\u305f\u307e\u307e\u7dd1\u306b\u306a\u308b\u306e\u3092\u6b62\u3081\u3089\u308c\u306a\u304f\u306a\u308b \u2014\u2014 \u7d71\u6cbb\u5bfe\u8c61\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u306e\u5224\u5b9a\u3092\u7a7a\u306b\u3059\u308b\u3068\u4f55\u3082\u691c\u51fa\u3057\u306a\u304f\u306a\u308a\u3001git add \u524d\u306e\u65b0\u898f\u30d5\u30a1\u30a4\u30eb\u306b\u95a2\u3059\u308b invariant \u3092\u4e00\u3064\u3082\u691c\u67fb\u3057\u306a\u3044\u307e\u307e\u7dd1\u306b\u306a\u308b (#1169 \u3067\u5b9f\u969b\u306b\u8e0f\u3093\u3060)",
        "file": ROOT / ".github" / "scripts" / "checks_tracked_files.py",
        "find": "    _governed434 = (\"js/\", \"e2e/\", \".github/scripts/\", \"docs/\", \"LICENSES/\")",
        "replace": "    _governed434 = (\"__never_matches__/\",)",
    },
    {
    "name": "Check 435: quiz の模範解答フォームが実行不能な長さの mailto を作れるようになる —— タイトルを少し伸ばすだけで Windows の約 2,048 文字上限を silent に超え、本文が切られるかメールソフトが開かない (利用者には何も伝わらない)",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "quality: '\u54c1\u8cea\u30fb\u30d7\u30ed\u30bb\u30b9\u554f\u984c\u96c6'",
    "replace": "quality: '\u54c1\u8cea\u30fb\u30d7\u30ed\u30bb\u30b9\u554f\u984c\u96c6\uff08\u7dcf\u5408\u6f14\u7fd2\u7de8\uff09'",
    "check": CHECK,
},
    {
    "name": "Check 435b: mailto を組む面が増えても気付けなくなる —— 435 は quiz-renderer.js を決め打ちで長さ検証するため、新しい mailto 経路は長さを一切検査されないまま「約 2,048 文字で silent に失敗する」class を素通しする (Check 124/411/434b と同じ scope-drift)",
    "file": ROOT / "js" / "apps.js",
    "find": "export function createApps(",
    "replace": "const _probe = () => { location.href = `mailto:x@y.z?subject=${'a'}&body=${'b'}`; };\n\nexport function createApps(",
    "check": CHECK,
},
    {
    "name": "Check 436: 規範層に canon が否定した「裁可待ち」型の defer 理由が再混入しても気付けなくなる —— canon を直しても下流の規範文書は自動では直らず、読み手は否定された規則を持ち帰る (2026-08-20 に research-application-policy.md で実際に起きた)",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    "find": "## 9.",
    "replace": "\u3053\u306e\u9805\u76ee\u306f\u30aa\u30fc\u30ca\u30fc\u304c\u88c1\u53ef\u3057\u305f\u6642\u306b\u7740\u624b\u3059\u308b\u3002\n\n## 9.",
    "check": CHECK,
},
    {
    "name": "Check 437: install の step timeout が単一ソースから外れ、赤の帰属メッセージが古い分数を出しても気付けなくなる —— このメッセージは CI が赤いときにこそ読まれるので、古い値は誤診に直結する (2026-08-20 に message だけ 8 分のまま drift していた)",
    "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
    "find": "INSTALL_TIMEOUT_MIN: 11",
    "replace": "INSTALL_TIMEOUT_MIN: 14",
    "check": CHECK,
},
    {
    "name": "Check 438: 葉モジュールの docstring が宣言する export と実際の return が drift しても気付けなくなる —— 宣言されていないメンバーは「再利用してよいか」を判断する人から見えず、散文は誰も読まないので放置され続ける (2026-08-20 に抽出増分の中で 2 件同時に drift した)",
    "file": ROOT / "js" / "settings-page.js",
    "find": "    return { SettingsPage, getImportOptions };",
    "replace": "    return { SettingsPage, getImportOptions, extra: 1 };",
    "check": CHECK,
},
    {
    "name": "Check 439: e2e の走査ルート一覧に存在しないハッシュが混ざる —— その entry は NotFound へ解決するため gate は淡々と緑を返し、本物のページが一度も走査されない (#96-99 の vacuous-hash class の a11y 版)",
    "file": ROOT / "e2e" / "a11y-axe.spec.js",
    "find": "'/#/apps/pomodoro', '/#/settings', '/#/quiz'",
    "replace": "'/#/apps/pomodoro', '/#/apps/settings', '/#/quiz'",
},
    {
    "name": "Check 440: コード側から docs/ への参照が腐る —— 「詳細はこの doc を読め」という読者の導線が行き止まりになるが、コメントなので lint も test も気付かない",
    "file": ROOT / "playwright.config.cjs",
    "find": "docs/files/playwright.config.cjs.md",
    "replace": "docs/files/playwright.config.cjs.MISSING.md",
},
    {
    "name": "Check 46d: JS 構文 gate が名ばかりへ戻る —— bare `node --check <file>` は ESM file の構文エラーを報告せず exit 0 するため、shipped JS 40 file 中 35 file が silent に無検査になる (2026-08-22 実測: js/brand.js に `let let = 1;` を植えても rc=0)",
    "file": ROOT / "package.json",
    "find": "\"lint:js\": \"node .github/scripts/check_js_syntax.mjs main.js",
    "replace": "\"lint:js\": \"node --check main.js && node .github/scripts/check_js_syntax.mjs main.js",
},
    {
    "name": "Check 46c: JS 構文 gate が存在するのに配線されない —— runner を残したまま lint:js から呼び出しを外すと、gate は「在る」のに一度も走らず全 shipped JS が無検査になる (存在 ≠ 配線)",
    "file": ROOT / "package.json",
    "find": "node .github/scripts/check_js_syntax.mjs main.js sw.js",
    "replace": "node .github/scripts/check_js_syntax.UNWIRED.mjs main.js sw.js",
},
    {
    "name": "Check 413b: 「数値の真値」を名乗る runbook §9 の行が自分自身と矛盾する —— 1 つの数値だけ更新して内訳を忘れると、同じ行が複数の総数を同時に主張する状態になり、読み手はどれを信じるか決められない (2026-08-22 実測: 総数 530 / source 264 / mirror 250 / = 490 の 3 通りが同居し、Check 413 は 6 個中 2 個しか git と突き合わせないため緑だった)",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    # anchor は **不変の定数**「README + _template の 2」を狙う。総数/source/mirror の 3 つは
    # file を 1 つ足すだけで動くので、そこを anchor にすると **増分のたび Check 362 が orphan を
    # 報告する**（2026-08-23 に実際に発生）。**2** は docs/files の 2 つの非 mirror file を数えた
    # 値で、file 数が動いても変わらない。2→3 にすると和が総数を 1 超えて 413b が RED になる。
    "find": "`docs/files/_template.md` の **2**",
    "replace": "`docs/files/_template.md` の **3**",
},
    {
    "name": "Check 441a (ライセンス本文の条項番号): 節内で番号を重複させる —— 条項を挿入・削除して "
            "再採番を忘れると起きる。ライセンスは CI のどの層にも読まれないので壊れても全部緑のまま "
            "SPDX / OSI 提出まで到達しうる (起草中に実際に踏んだ)",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": "  15.8 English is the authoritative",
    "replace": "  15.7 English is the authoritative",
},
    {
    "name": "Check 441b (ライセンス本文の相互参照): 存在しない条項を指させる —— 再採番したのに "
            "本文中の 'Section N.M' を追従させ忘れると、読み手は別の条項へ飛ばされる",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": "Section 15.4 applies, and the invalidity",
    "replace": "Section 15.99 applies, and the invalidity",
},
    {
    "name": "Check 441c (ライセンス本文の定義語): 定義だけ改名して本文の使用箇所を残す —— "
            "定義が本文で一度も使われない状態は、起草途中の残骸か削除した条項の痕跡",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": '"Reservation" means any act',
    "replace": '"ReservationX" means any act',
},
    {
    "name": "Check 441d (ライセンス本文の義務語): 利用者への義務を混入させる —— §10.1 は「利用者に "
            "一切の条件を課さない」と宣言しており、義務語の混入は**このライセンスの中核主張そのものを "
            "偽にする**。しかも混入先が「表示は不要」と述べる §10.2 なので、本文が自分と逆のことを言い出す",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": "  10.2 In particular, You need not give attribution",
    "replace": "  10.2 You must give attribution. In particular, You need not",
},
    {
    "name": "Check 441e (LICENSE の配線): 全文 path への参照を外す —— 全文ファイルが存在しても "
            "LICENSE が指していなければ、受領者はどの条項に従うのか判定できない (存在 ≠ 配線)",
    "file": ROOT / "LICENSE",
    "find": "Full text: LICENSES/ACD-1.0.txt",
    "replace": "Full text: see the LICENSES directory",
},
    {
    "name": "Check 443 (advisory 予算 < hard ceiling): 予算を hard ceiling と同値へ戻す —— "
            "その file の早期警告が構造的に一度も出なくなり (OK からいきなり BLOCKING へ飛ぶ)、"
            "「advisory は BLOCKING を踏む前に効かせる」という本リポジトリの標準規律が働かない状態に戻る",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": ".github/scripts/mutation_samples_archive.py | 950 | advisory",
    "replace": ".github/scripts/mutation_samples_archive.py | 1000 | advisory",
},
    {
    "name": "Check 444 (ライセンス宣言の cross-surface coherence): HTML 標準の license リンクを外す —— "
            "ACD-1.0 §6.5 は「自動化システムが判定できない許諾は、学習されるための著作物にとっては "
            "許諾ではない」と述べているので、宣言が 1 面でも欠けるとその経路の agent は学習可否を判定できない",
    "file": ROOT / "index.html",
    "find": '<link rel="license" href="/portfolio/LICENSES/ACD-1.0.txt" />',
    "replace": '<!-- license link removed by mutation probe -->',
},
    {
    "name": "Check 445 (SPDX 提出物の同期): 提出用 XML を手で書き換える —— 提出物は本文から "
            "導出しているので、手編集は「本文と食い違う XML を提出する」ことを意味する。"
            "XML は普段誰も読まないため drift に気付く経路が無く、いつか嘘を提出することになる",
    "file": ROOT / "LICENSES" / "ACD-1.0.spdx.xml",
    "find": 'licenseId="ACD-1.0"',
    "replace": 'licenseId="ACD-1.1"',
},
    {
    "name": "Check 446 (WebMCP ツールの宣言): capabilities.tools を false へ戻す —— 実行可能な "
            "ツールが登録されているのに「ツールは無い」と宣言する状態。2026-08-23 まで実際に"
            "そうなっており、静的 discovery しかしない agent はツールの存在を知りようがなかった",
    "file": ROOT / ".well-known" / "mcp.json",
    "find": '"tools": true,',
    "replace": '"tools": false,',
},
    {
    "name": "Check 447 (制約列挙の正典一致): C6 を列挙から落とす —— エージェントはこの prompt を "
            "展開して監査するので、名前が欠けると**存在しない制約セットを監査する**。"
            "2026-08-23 まで実際に C5/C6/C7 が欠落していた (範囲の表記だけ更新され中身が古いまま)",
    "file": ROOT / ".well-known" / "mcp.json",
    "find": "C6 AIO Integrity / ",
    "replace": "",
},
    {
    "name": "Check 448 (Agent Skills 仕様適合): 必須 field `description` を落とす —— 仕様の設計は "
            "「agent は起動時に name と description だけを読んで関連性を判断する」progressive "
            "disclosure なので、欠けると **agent は中身を取ってみるまで用途が判らない**。"
            "2026-08-23 まで実際に全 entry で欠落しており、宣言した $schema で検証する agent は "
            "index ごと拒否していた",
    "file": ROOT / ".well-known" / "agent-skills" / "index.json",
    "find": '"description": "Read the authoritative machine-readable context',
    "replace": '"_description_removed_by_probe": "Read the authoritative machine-readable context',
},
    {
    "name": "Check 449a (RFC 9727 関係型): カタログのメンバーを `item` ではなく `api-catalog` "
            "関係で列挙する —— RFC 9727 でこの関係は「**別の API カタログへの入れ子**」を意味する "
            "ので、`llms-full.txt` などカタログでないリソースを「これらは全てカタログだ」と偽って "
            "宣言することになり、**仕様に従う agent はそれらを linkset として parse しようとして "
            "失敗する**。2026-08-23 まで実際に 7 件すべてがこの状態で、Check 165 は JSON 構造と "
            "anchor しか見ないため検出層が存在しなかった",
    "file": ROOT / ".well-known" / "api-catalog",
    "find": '"item": [',
    "replace": '"api-catalog": [',
},
    {
    "name": "Check 450 (非日本語スクリプト混入): 規範層の「権威テキスト」前半 3 字をキリル文字へ "
            "戻す —— 字形が近いため目視では気付けず、spell-check は走らず lint は JS しか読まず "
            "prose は何とも比較されないので **どの層も検出しない**。2026-08-23 まで実際に規範層 "
            "(C6 を説明する行) と decision record の 2 箇所に残存していた",
    "file": ROOT / "docs" / "architecture" / "repository-maintainability-map.md",
    "find": "\u6a29\u5a01\u30c6\u30ad\u30b9\u30c8",
    "replace": "\u6a29\u5a01\u0442\u0435\u043a\u30b9\u30c8",
},
    {
    "name": "Check 436 (裁可待ち文言・scope + 綴り拡張): agent 定義の pre-edit checklist を "
            "「承認が記録されていなければ REFUSE」へ戻す —— `.claude/agents/` は**エージェントの "
            "挙動を実際に駆動する層**で、ここに承認ゲートがあると AIO 編集を通すたびに canon が "
            "存在しないと明記した「裁可待ち」を再生産する。旧 scope は `.claude/` を一度も見て "
            "おらず、しかも照合が case-sensitive だったため先頭大文字の実在文言を素通りしていた",
    "file": ROOT / ".claude" / "agents" / "aio-guardian.md",
    "find": "1. **Is every claim true and non-fabricated?**",
    "replace": "1. **Orchestrator approval recorded?** If not, REFUSE.",
},
    {
    "name": "Check 436 (mirror 面 scope): docs/files/ mirror の C6 記述を承認ゲート型へ戻す —— "
            "mirror doc は「この file を編集するとき何を満たすか」を述べる規範面として読まれる。"
            "2026-08-23 に手作業で 9 枚を掃引したが **綴りを 3 つ見落として 4 枚が残った** ゆえ、"
            "per-instance では閉じない class として構造封じへ昇華した",
    "file": ROOT / "docs" / "files" / "llms-full.txt.md",
    "find": "semantic \u7de8\u96c6\u306f C6 \u306e 3 \u4e0d\u5909\u6761\u4ef6",
    "replace": "semantic \u7de8\u96c6\u306f orchestrator \u660e\u793a\u627f\u8a8d\u5fc5\u9808",
},
    {
    "name": "Check 454 (危険域 file の予算登録): BUDGET-DATA から check_repository_consistency.py の "
            "登録行を除去 → その file は Check 52 の advisory 対象から外れ、**早期警告が一度も出ないまま** "
            "Check 365 の 1,000 行 BLOCKING へ飛ぶ状態へ戻る。導入時に実在の未登録 5 file を検出した "
            "class の回帰防止 (帰属実測済: 発火するのは 454 のみ。52/59/365 は緑のまま —— "
            "エラー本文中の参照を grep が拾って 4 件と誤読しかけたので、先頭の Check 番号で帰属し直した)。"
            "\n\n    NOTE: **この mutation の前提はデータ条件** (対象 file が >800 行であること) である。"
            "対象を分割・圧縮すると Check 454 が対象外と判断し、mutation は **silent に vacuous 化する**。"
            "実際 2026-08-26 に checks_behavioral.py (924 → 589 行) を指しており、同じセッションの後続 PR で"
            "分割した結果 probe が SURVIVED を報告した。**Check 362 (anchor 解決) も 420 (一意性) も"
            "これを捕捉しない** —— anchor は解決するし一意でもあり、ただ load-bearing でなくなるだけだから。"
            "捕捉層は probe だけである。SURVIVED になったら、危険域に残っている file へ**指し直す**こと"
            "(対象は `git ls-files` で >800 行の登録済み file を数えれば分かる)。"
            "現在の対象は分割トラック完遂後の薄い dispatcher なので、これ以上縮む予定は無い",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": ".github/scripts/check_repository_consistency.py | 950 | advisory\n",
    "replace": "",
},
    {
    "name": "Check 455 (strong-advisory の tightness): main.js の予算を Stage 5 前の 6,400 へ戻す —— "
            "実測 1,356 に対し 4.7 倍で **advisory が永久に鳴らない**状態。main.js は Check 365 の "
            "hard ceiling 対象外ゆえ、この予算が**唯一のサイズ信号**であり、緩めた瞬間にサイズの "
            "観測手段が完全に失われる。§1 の分類表が strong-advisory に与えた定義 "
            "(「現行行数に近い tight な上限」) と実態が真逆になる drift の回帰防止 "
            "(帰属実測済: 発火するのは 455 のみ)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "\nmain.js | 1500 | strong-advisory\n",
    "replace": "\nmain.js | 6400 | strong-advisory\n",
},
    {
    "name": "Check 456 (__main__ ガード後の def): rotate ツールのガード直後に関数定義を足す —— "
            "ガード本体 (sys.exit(main())) はその場で実行されるので、後ろの def は"
            "**スクリプト実行時にはまだ束縛されていない**。import すると定義されるため "
            "import 経由のテストでは動くのに CLI では NameError になる非対称。実測 (2026-08-26): "
            "`_wire_new_archive` がこの位置にあり「受け皿が埋まったら次を起こす」機能が "
            "npm run rotate-mutations からは一度も動いていなかった (帰属実測済: 456 のみ発火)",
    "file": ROOT / ".github" / "scripts" / "rotate_mutation_samples.py",
    "find": "if __name__ == \"__main__\":\n    sys.exit(main())\n",
    "replace": "if __name__ == \"__main__\":\n    sys.exit(main())\n\n\ndef _unreachable_after_guard():\n    return None\n",
},
    {
    "name": "Check 457 (配線 ⟹ 配信面の照合): freshness tool の照合対象を index.html 由来の "
            "導出からハードコード 3 件へ戻す —— **aio-guard.js / theme-init.js / karte-init.js / "
            "error-suppressor.js が配信面で一度も検証されない**状態へ回帰する。Check 133/134/135 は "
            "リポジトリ内の配線しか見ないので、公開されているのが古い/壊れた版という失敗モードは "
            "原理的に見えない (帰属実測済: 発火するのは 457 のみ)",
    "file": ROOT / ".github" / "scripts" / "check_deployed_freshness.py",
    "find": "    return sorted(set(root_js) | set(root_css) | {\"sw.js\", \"index.html\"}) + sorted(",
    "replace": "    return [\"style.css\", \"main.js\", \"sw.js\"] + sorted(",
},
    {
    "name": "Check 457b (導出の起点の検証): 照合対象から index.html だけを外す —— "
            "版数 (ai:version / ai:last-modified) は**中身が変わっても動かない** "
            "(実測: 直近 30 日で index.html は 7 commit 変更・版数 bump は 0 件) ので、"
            "外した瞬間に **JSON-LD / CSP / meta / script 配線 / sr-only entity anchor を載せる "
            "最も影響の大きい file** が配信面で silent に古いままになりうる状態へ戻る "
            "(帰属実測済: 発火するのは 457b のみ)",
    "file": ROOT / ".github" / "scripts" / "check_deployed_freshness.py",
    "find": "{\"sw.js\", \"index.html\"}",
    "replace": "{\"sw.js\"}",
},
    {
    "name": "Check 457c (機械向け宣言面の配信検証): discovery 照合対象から .well-known/** の "
            "導出を外す —— **200 が返ることと中身が最新であることは別**で、古い robots.txt は "
            "クローラの到達範囲を変え、古い .well-known/* は agent が読む契約そのものを変え、"
            "古い aio-manifest.json は agent へ誤った digest を宣言する。しかも人間には"
            "何も見えない。実測 (2026-08-26): 導入前は discovery 層 13 件中 10 件が"
            "存在確認どまりだった (帰属実測済: 発火するのは 457c のみ)",
    "file": ROOT / ".github" / "scripts" / "check_deployed_freshness.py",
    "find": "    out = set(_wellknown_paths())",
    "replace": "    out = set()",
},
    {
    "name": "Check 458b (venue の誤主張): CLAUDE.md §7 の投稿先を `license-review` へ投稿済みと"
            "書き換える —— **取り違えには実害がある**。`license-discuss` は OSI の一般的な議論"
            "リストで承認申請の窓口ではないので、「申請済み」と記録すると **まだ何も申請して"
            "いない**ことに誰も気付けなくなる。2026-08-26 の 1 日で 2 度 drift した class "
            "(帰属実測済: 発火するのは 458b のみ)",
    "file": ROOT / "CLAUDE.md",
    "find": "OSI `license-discuss` へ投稿済み・結果待ち",
    "replace": "OSI `license-review` へ投稿済み・結果待ち",
},
    {
    "name": "Check 461: 予算ラチェットの累積記録を stale に戻す —— 個々のラチェットに理由を書いても、"
            "累積が更新されなければ「今日で合計いくら増えたか」が視界に入らない。予算は自分で上げられる"
            "ので、歯止めは累積を見ることにしかない (2026-08-27 に実際 5 回分 stale 化していた)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    # [FIX] anchor をラチェットのたび動く値から不変部分へ移す。旧 anchor は `current=726300` を
    #   直接掴んでおり、**次のラチェットで必ず orphan 化**した (実際に 2026-09-06 に Check 362 が検出)。
    #   末尾に数字を足すだけで current が別値になり Check 461 が RED になる。
    "find": "session-start=716800 current=",
    "replace": "session-start=716800 current=9",
    "check": CHECK,
},
    {
    "name": "Check 462: Zenn 記事数の自己申告だけを動かす —— 記事の増減で文言が取り残されると、"
            "公開面が silent に嘘の本数を名乗る。機械可読な権威シグナルを正しく保つことが主眼の"
            "リポジトリで、公開文言の事実誤りは中核の毀損にあたる",
    "file": ROOT / "js" / "components.js",
    "find": "全11本の記事",
    "replace": "全12本の記事",
    "check": CHECK,
},
    {
    "name": "Check 460 (g): 入口ページから規模の申告そのものを消す —— REVIEWERS.md は "
            "reviewer が最初に読む英語ページで、そこが 'All N adverse facts' と完全性を主張する。"
            "2026-09-05 に実測すると 118/14/Five と書いてあり実体は 144/57/9 で、3 つとも過少だった。"
            "「全部開示する」と述べるドシエが開示量を小さく言うのは、間違える向きとして最悪である",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    # anchor は **数字を含めない** —— 件数は増分ごとに動くので、数字を釘にすると
    # 次の増分で Check 362 が orphan として RED にする (本 mutation で実際に踏んだ)。
    # "All " を落として申告そのものを消す形にすると、face (g) の「申告が見つからない」
    # 枝を突ける —— 維持が面倒になった誰かが文ごと消す、という現実的な退行でもある。
    # 2026-09-09 再アンカー (2 度目)。前の釘は "**Read this first.** All " で、#120 が
    # その一文を書き換えた瞬間 orphan になった。**教訓は「数字を釘にするな」だけでは
    # 足りない —— 説明文そのものが動く。** そこで今度は **Check 460 (g) が探す正規表現の
    # 文字列そのもの**を釘にする: face (g) は `(\d+) worked entries, indexed by the question`
    # を探すので、その語順を壊せば「申告が見つからない」枝が必ず発火する。
    # **釘と検査対象が同一なので、検査が在る限り釘も在る。**
    "find": "worked entries, indexed by the question",
    "replace": "worked entries, listed by the question",
    "check": CHECK,
},
    {
    "name": "Check 464: 次版の変更リストから errata を 1 件落とす —— 1.0 は凍結中で「欠陥は直さず"
            "記録する」運用なので、記録が集約点に載らなければそのまま忘れられる。1.1 の入力は "
            "errata / review-responses-meta / review-responses-clauses / discussion-log の 4 か所に"
            "散っており、議論後に回って集める手順は必ず落とす",
    # [FIX 2026-09-29] 旧 anchor は 1.1 の表の E9 だった。Check 464 は 2026-09-18 から全版の変更リストを
    # 横断して見るので、E9 が 1.2 の対応表にも現れる限り 464 は発火せず、460 / 469 が拾うだけの
    # 帰属違いだった。全変更リストで 1 回しか現れない E23 に付け替え、464 が RED になるのを実測した。
    "file": ROOT / "LICENSES" / "ACD-1.2-CHANGELIST.md",
    "find": "| E23 | §2.8 |",
    "replace": "| X23 | §2.8 |",
    "check": CHECK,
},
    {
    "name": "Check 465: rounds/ の在庫申告を実測より小さくする —— 記録が drift しないためだけに"
            "在るディレクトリの入口が、中身の量について偽を述べる形。2026-09-06 まで実際に"
            "「いまの状態: 空である」と書かれ続けており (against.md #89)、審査者は証拠の量を"
            "その入口から受け取るので、小さく言うのは開示の主張を嘘にする",
    "file": ROOT / "LICENSES" / "rounds" / "README.md",
    # [FIX] 初版は find を「…7 ファイル」に釘付けしていた。**件数は増分のたびに動く値**なので、
    #   翌日 8 件目を置いた時点で anchor が消え Check 362 が orphan として RED にした
    #   (CLAUDE.md §7「安全網の anchor は『たまたま近くにある文字列』を掴みやすい」の 6 度目)。
    #   在庫表の先頭行 —— **最初の送信であり、以後動かない** —— の行頭 `|` を落として
    #   「行として数えられない」状態を作る形へ移した。件数見出しではなく行数の面を打つ。
    "find": "\n| 2026-08-26 | ",
    "replace": "\n2026-08-26 | ",
    "check": CHECK,
},
    {
    "name": "Check 466: 表紙から審査者への案内を消す —— 送った文面は GitHub リポジトリを指すので "
            "README.md は審査者の入口である。案内が無ければ、`LICENSES/` の 24 文書は在っても"
            "到達されない。2026-09-07 まで実際にこの案内は 214 行下にあり、手前は AI 向けブロックと"
            "日本語の節だった (against.md #94)",
    "file": ROOT / "README.md",
    "find": "> **[`LICENSES/REVIEWERS.md`](LICENSES/REVIEWERS.md)** \u2014 it is in English and states the",
    "replace": "> **the reviewer guide in this repository** \u2014 it is in English and states the",
    "check": CHECK,
},
    {
    "name": "Check 463: 送る文面から OSD 3/5/6/9 の名指しを落とす —— OSI の review-process は"
            "「OSD に準拠する」ではなく「**3, 5, 6, 9 を満たすと specifically 明言する**」を求める。"
            "2026-09-07 に Carlo Piana 氏が別の提出へ『required information が無いので解決するまで"
            "コメントしない』と述べた (against.md #97) ため、欠落は議論の遅れではなく不成立を招く",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "**OSD 5 and OSD 6**",
    "replace": "**OSD 5/6**",
    "check": CHECK,
},
    {
    "name": "Check 467: 単一ソースだけ `paused` へ戻す —— 状態は面に散らばっており、**両方向に危険である**。"
            "止めたのに面が残っていなければ次のセッションが送りかねず、再開したのにバナーが残れば"
            "送れるのに送らない。marker と面が食い違ったら必ず RED になること。"
            "**2026-09-17 に発信が再開したので、mutation の向きを逆にした** ——"
            "**anchor が解決することは、正しい向きを打っている証拠ではない**",
    "file": ROOT / "LICENSES" / "FROZEN.md",
    "find": "<!-- POSTING-STATUS: active -->",
    "replace": "<!-- POSTING-STATUS: paused 2026-09-09 -->",
    "check": CHECK,
},
    {
    "name": "Check 460 (m): register の集計行を古い値に戻す —— 項目を足すたび列は増えるのに集計行は"
            "動かない。**しかも過少申告は #58 と同じ向きの誤りで、読み手は残作業を少なく見積もる**",
    "file": ROOT / "LICENSES" / "ACD-OSI-BOTTLENECKS.md",
    # **anchor は可変値に釘付けにしない。** 初版は宣言側の数 ("… 要る 6") を find にしていたが、
    # **その数は項目を足すたび動く**ので、2026-09-13 に B2 へ OSI の ○ を足した瞬間 orphan 化した
    # (Check 362 が捕捉)。**表の側の不変なラベルを打ち、○ を落として導出値を 1 減らす** ——
    # 宣言と導出がずれるので Check 460 (m) は同じように RED になり、**anchor は数から独立する。**
    # **⚠ 最初の書き直しは、解決するのに発火しなかった。** 行の途中に列を挿し込んだため、
    # face (m) が見る「末尾 3 列」がずれず導出値が動かなかった ——**anchor が解決することは、
    # 正しい対象を打っていることを意味しない** (Check 362 / 420 はどちらも前者しか見ない)。
    # **○ そのものを落とす形にして RED を実測した。**
    # 2026-09-28: B5 の status 文を E11 の実態（1.1 で閉じた）へ訂正したので anchor を追従 (Check 362 が捕捉)。
    "find": "1.0 には文が残る。**2026-09-28 訂正**）| — | — | ○ |",
    "replace": "1.0 には文が残る。**2026-09-28 訂正**）| — | — | — |",
    "check": CHECK,
},
    {
    "name": "Check 460 (n): §4c の「機械的に確かめた」数字を 1 つずらす —— この表は審査者に"
            "「弁護士がいなくても機械で確かめられること」を示す面で、**表自身が『nothing enforces it』と"
            "書いていた**（2026-09-06 の再導出では実際に 3 行が誤っていた）",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-reference.md",
    "find": "| 10 terms, all in §1.1",
    "replace": "| 11 terms, all in §1.1",
    "check": CHECK,
},
]
