#!/usr/bin/env python3
"""mutation_samples.py — Curated mutation DATA for mutation_probe.py (runner is separate).

mutation_probe.py (runner / completeness-critic) から**データのみ**を分離した葉モジュール。
肥大化解消 (自走効率 + 保守性): runner ロジックと curated mutation データを分ける。さらに
データ自体も log-rotation 方式で分割した (1000 行しきい値対応):

- MUTATIONS_ARCHIVE  : mutation_samples_archive.py (最古 / rotated part 1)。
- MUTATIONS_ARCHIVE2 : mutation_samples_archive2.py (次に古い / rotated part 2, 2026-07-28 新設)。
- 本ファイル tail    : 新しい側の entries (新規追記は常に本ファイルの MUTATIONS 末尾へ)。
- MUTATIONS          : ARCHIVE + ARCHIVE2 + tail の連結 (mutation_probe が import する公開 API・不変)。
- E2E_MUTATIONS      : behavior e2e 安全網用 (--e2e モード)。

【追記規約 (生じないように / 恒久)】新規 mutation は本ファイルの MUTATIONS 末尾 (tail) に追記する。
本ファイルが ~900 行を超えたら、最古の tail entries を最新の archive part へ移して rotate する。
part 1/2 が Check 365 の 1,000 cap に近接したら part をさらに増やす (mutation_samples_archive3.py 等)。

各 mutation の意味・非 vacuous 保証・実行機構は mutation_probe.py の docstring を参照。
本ファイルはデータ (dict の list) のみで、副作用も実行ロジックも持たない。
"""
from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    print("ERROR: mutation_samples.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

from mutation_samples_common import ROOT, CHECK  # noqa: F401 (entry 内で参照)
from mutation_samples_archive import MUTATIONS_ARCHIVE
from mutation_samples_archive2 import MUTATIONS_ARCHIVE2
from mutation_samples_e2e_archive import E2E_MUTATIONS_ARCHIVE
from mutation_samples_e2e_archive3 import E2E_MUTATIONS_ARCHIVE3
from mutation_samples_e2e_archive2 import E2E_MUTATIONS_ARCHIVE2

# 新しい側の curated mutation (新規追記は本リスト末尾へ / 上記「追記規約」参照)。
_MUTATIONS_TAIL = [
    # 注: Check 362 (mutation anchor resolution) の curated meta-mutation は敢えて置かない。
    # anchor を orphan 化する mutation は mutation_samples.py 自身の `"find":` 行を quote する
    # 自己参照になり、mutation_probe の replace(find, replace, 1) が先頭 (= その mutation 自身の
    # find 値) に当たって挙動が不安定になるため。Check 362 の非 vacuous 性は手動で実証済
    # (mutation の file を誤り先へ変えると Check 362 が RED・restore で緑)。
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
        "find": "    _governed434 = (\"js/\", \"e2e/\", \".github/scripts/\", \"docs/\")",
        "replace": "    _governed434 = (\"__never_matches__/\",)",
    },
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。
_MUTATIONS_TAIL.append({
    "name": "Check 435: quiz の模範解答フォームが実行不能な長さの mailto を作れるようになる —— タイトルを少し伸ばすだけで Windows の約 2,048 文字上限を silent に超え、本文が切られるかメールソフトが開かない (利用者には何も伝わらない)",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "quality: { title: '\u54c1\u8cea\u30fb\u30d7\u30ed\u30bb\u30b9\u554f\u984c\u96c6'",
    "replace": "quality: { title: '\u54c1\u8cea\u30fb\u30d7\u30ed\u30bb\u30b9\u554f\u984c\u96c6\uff08\u7dcf\u5408\u6f14\u7fd2\u7de8\uff09'",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 435b: mailto を組む面が増えても気付けなくなる —— 435 は quiz-renderer.js を決め打ちで長さ検証するため、新しい mailto 経路は長さを一切検査されないまま「約 2,048 文字で silent に失敗する」class を素通しする (Check 124/411/434b と同じ scope-drift)",
    "file": ROOT / "js" / "apps.js",
    "find": "export function createApps(",
    "replace": "const _probe = () => { location.href = `mailto:x@y.z?subject=${'a'}&body=${'b'}`; };\n\nexport function createApps(",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 436: 規範層に canon が否定した「裁可待ち」型の defer 理由が再混入しても気付けなくなる —— canon を直しても下流の規範文書は自動では直らず、読み手は否定された規則を持ち帰る (2026-08-20 に research-application-policy.md で実際に起きた)",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    "find": "## 9.",
    "replace": "\u3053\u306e\u9805\u76ee\u306f\u30aa\u30fc\u30ca\u30fc\u304c\u88c1\u53ef\u3057\u305f\u6642\u306b\u7740\u624b\u3059\u308b\u3002\n\n## 9.",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 437: install の step timeout が単一ソースから外れ、赤の帰属メッセージが古い分数を出しても気付けなくなる —— このメッセージは CI が赤いときにこそ読まれるので、古い値は誤診に直結する (2026-08-20 に message だけ 8 分のまま drift していた)",
    "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
    "find": "INSTALL_TIMEOUT_MIN: 11",
    "replace": "INSTALL_TIMEOUT_MIN: 14",
    "check": CHECK,
})

MUTATIONS = MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
    {
        "name": "security: URL サニタイズが素朴な前方一致へ退行する — `startsWith('javascript:')` だと **大文字混在 (JaVaScRiPt:) や前後空白** ですり抜け、`data:` / `vbscript:` も素通りする。許可リスト方式 (^https?://) でなければ回避手口を塞げない",
        "file": ROOT / "js" / "store.js",
        "find": "                return /^https?:\\/\\//i.test(s) ? s.slice(0, 500) : String(fallback || '');",
        "replace": "                return s.startsWith('javascript:') ? String(fallback || '') : s.slice(0, 500);",
        "test": "URL サニタイズが大文字混在・前後空白・data:/vbscript: を弾く",
    },
    {
        "name": "behavior: 模範解答フォームのメッセージ上限が外れる — 入力は mailto の URL へ percent-encode されるので日本語 1 文字が 9 文字になる (実測: 500 文字で URL 4,852)。Windows の mailto は約 2,048 文字で切られるため、**本文が欠けるか、そもそもメールソフトが開かない** silent failure になる",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "placeholder: \"メッセージ（任意）\", maxlength: 120,",
        "replace": "placeholder: \"メッセージ（任意）\",",
        "test": "模範解答フォームの入力上限が mailto の実行限界を超えない",
    },
    {
        "name": "a11y: ルート遷移のアナウンスが空になる — SPA はページ全体が入れ替わっても『ページが変わった』ことが SR に伝わらない。polite な #page-announcement へタイトルを書くのが唯一の通知経路で、失われると利用者は今どこにいるか分からないまま操作を続けることになる",
        "file": ROOT / "js" / "meta-management.js",
        "find": "            pageAnnouncer.textContent = title + 'ページを表示しています。';",
        "replace": "            pageAnnouncer.textContent = '';",
        "test": "Route changes announce the PAGE_META title (not the internal route slug) to the polite aria-live region",
    },
    {
        "name": "a11y: TODO 削除の完了通知が失われる — 視覚利用者は項目が消えたことで分かるが、SR 利用者には何も伝わらない。task 側と対で持つべき通知で、片方だけ欠けると『1 ケースだけ処理して他を忘れる』非対称になる (#901 で一本化した通知チャネル)",
        "file": ROOT / "js" / "apps.js",
        "find": "            Toast.show('TODOを削除しました', 'success');",
        "replace": "",
        "test": "Todo add and delete announce to the assertive aria-live region (WCAG 4.1.3, task symmetry)",
    },
    {
        "name": "behavior: プロジェクト検索の 0 件表示が空になる — 一覧が消えただけの画面になり、『絞り込まれた結果ゼロ』なのか『読み込みに失敗した』のか判別できない。empty-state は role=status なので SR にも件数の変化として伝わる唯一の手掛かり",
        "file": ROOT / "js" / "projects-page.js",
        "find": "                        h('div', { class: 'card-body text-center text-muted' }, '条件に一致するプロジェクトはありません。')",
        "replace": "                        h('div', { class: 'card-body text-center text-muted' }, '')",
        "test": "Projects search shows an empty state when nothing matches",
    },
    {
        "name": "a11y: 並べ替えボタンの名前からプロジェクト名が消える — 36 個のボタンが『↑』『↓』の 2 種類の名前しか持たなくなり、SR 利用者はどれを操作するのか区別できない (WCAG 4.1.2)。視覚利用者には行の位置で自明なので目視では気付けない。同じ行の削除・非表示は既に一意化されており、並べ替えだけ取り残されていた非対称",
        "file": ROOT / "js" / "settings-page.js",
        "find": ", 'aria-label': '上へ移動：' + p.name }",
        "replace": " }",
        "test": "並べ替えボタンの名前がプロジェクトごとに一意になる",
    },
    {
        "name": "a11y: アプリ一覧のボタン名から行き先が消える — 5 個すべてが『開く』になり、SR 利用者がボタンだけを辿ると行き先を区別できない (WCAG 4.1.2)。カードの見出しは文脈を与えるが、リポジトリの慣習は名前側に対象を含める形 (#1085) で統一されている",
        "file": ROOT / "js" / "components.js",
        "find": "                                'aria-label': app.title + 'を開く',\n",
        "replace": "",
        "test": "アプリ一覧のボタン名が行き先ごとに一意になる",
    },
    {
        "name": "a11y: home の CTA が可視テキストを含まないアクセシブル名に戻る — 音声入力の利用者が"
                "見えているとおり『分担表を見る』と発話しても起動できない (WCAG 2.5.3 Level A)。"
                "axe の label-content-name-mismatch は enabled:false (experimental) ゆえ既存の"
                "withTags スキャンでは走らず、この SC は専用テストを書くまで完全に未検査だった",
        "file": ROOT / "js" / "home-page.js",
        "find": "'aria-label': '分担表を見る：Human vs AI 分担表ページへ移動'",
        "replace": "'aria-label': 'Human vs AI 分担表ページへ移動'",
        "test": "可視テキストがアクセシブル名に含まれる (WCAG 2.5.3) — 全ルート",
    },
    {
        "name": "a11y: 既定で無効な axe ルールの違反が混入する — `aria-roledescription` を"
                "semantic role の無い div に付けると、SR は要素の役割を独自名で読み上げるのに"
                "ロールが無く意味が通らない (WCAG 4.1.2)。axe の該当ルールは enabled:false ゆえ"
                "既存の withTags スキャンでは走らず、この専用テストだけが捕捉層",
        "file": ROOT / "js" / "home-page.js",
        "find": "h('div', { class: 'evidence-grid' }",
        "replace": "h('div', { class: 'evidence-grid', 'aria-roledescription': 'グリッド' }",
        "test": "既定で無効な axe ルール (Level A/AA) を全ルートで走らせる",
    },
    {
        "name": "🔴 稼働中ポモドーロの復帰が描画に紐付き直す — main.js init の resumeIfActive() を外すと、リロード後に別ページにいる利用者の interval が誰にも作られず、25 分集中し続けても完了が history に記録されない。リロードしなければ裏で完了する (#1056 が扱った経路) ため『リロードを跨いだときだけ』挙動が違う非対称で、利用者から見ると原因に見当がつかない",
        "file": ROOT / "main.js",
        "find": "            resumeIfActive();\n",
        "replace": "",
        "test": "稼働中ポモドーロはリロード後どのページに着地しても完了が記録される",
    },
    {
        "name": "保存 flush が外れて書きかけが失われる — 保存は debounce (150ms) 越しなので、最後の打鍵から 150ms 以内にリロード/タブ終了すると書きかけが消える。それを防ぐのは state.js の visibilitychange(hidden) → saveNow() の 1 本だけ。失われ方が『エラー』ではなく『戻ったら数文字前の状態』なので利用者は自分の打ち間違いと区別できず、fatal も視覚差分も出ないため behavior test 以外に捕捉層が無い",
        "file": ROOT / "js" / "state.js",
        "find": "        if (document.visibilityState === 'hidden') {saveNow();}",
        "replace": "",
        "test": "debounce 前にリロードしても書きかけのノートが失われない",
    },
    {
        "name": "a11y: startViewTransitionProxy の reduced-motion 判定が外れる — proxy は『executeSafeTransition を経由せず素の document.startViewTransition を直接呼ぶ実装』でも reduce を尊重するための層 (Check 43b が名前を BLOCKING 監視)。ここが抜けると、その経路から前庭障害のユーザーへページ全体のクロスフェードが漏れる (WCAG 2.3.3)。render() 側のガードは別経路なのでこの穴を塞げない",
        "file": ROOT / "main.js",
        "find": "                if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {\n                    try { if (typeof callback === 'function') callback(); }",
        "replace": "                if (false) {\n                    try { if (typeof callback === 'function') callback(); }",
        "test": "WCAG 2.3.3: 素の startViewTransition を直接呼んでも reduced-motion では実遷移しない",
    },
    {
        "name": "🔴 theme-color の更新が先頭 1 本だけに戻る — index.html は media 付きの theme-color を 2 本宣言しており、querySelector は先頭 (light 用) しか返さない。OS が dark のときは書き換えた meta の media が一致せず適用されないので、選んだテーマがモバイルのアドレスバー色に届かない。**変わるのはページの pixel ではなくブラウザ chrome の色なので screenshot では原理的に捕捉できない**",
        "file": ROOT / "js" / "theme.js",
        "find": "        document.querySelectorAll('meta[name=\"theme-color\"]').forEach((meta) => {\n            meta.content = isDark ? '#0b0f19' : '#ffffff';\n        });",
        "replace": "        const _m = document.querySelector('meta[name=\"theme-color\"]');\n        if (_m) { _m.content = isDark ? '#0b0f19' : '#ffffff'; }",
        "test": "theme-color の実効値が OS=dark でもサイトのテーマと一致する",
    },
    {
        "name": "Markdown プレビューが大きいノートで途中打ち切りになる — renderMarkdown を先頭 500 行までに制限すると、宣言上限 (NOTES_TEXT = 20,000 文字) のノートで末尾が描画されなくなる。**エラーは出ない**ので利用者には「書いたはずの下の方が消えている」としか見えず、短いノートしか流さない既存テストでは検出できない",
        "file": ROOT / "js" / "apps.js",
        "find": "        const lines = String(src || '').split('\\n');",
        "replace": "        const lines = String(src || '').split('\\n');\n        lines.length = Math.min(lines.length, 500);",
        "test": "上限いっぱいのノートでもプレビューが末尾まで描画される",
    },
    {
        "name": "JavaScript 無効時の説明が消える — noscript の利用者向けブロックを外すと、JS を切った環境では #content が空・可視の見出し 0 個で **説明の無い白紙**に戻る (可視テキストは sr-only の AIO アンカーだけ)。SPA が動かないこと自体は設計どおりだが、§3(B) が死守すると定めた機能性は loads/displays/**comprehensible**",
        "file": ROOT / "index.html",
        "find": "                    <h1>JavaScript を有効にしてください</h1>",
        "replace": "",
        "test": "JavaScript 無効時に説明メッセージが表示される",
    },
    {
        "name": "normalize が非冪等になり保存のたび slug が伸びる — slug 重複解消の seen 集合を『取り込み中の全 slug』で初期化すると、各プロジェクトが**自分自身**と衝突したとみなされ、保存のたび `-2` が付く。既存のブックマークや共有リンクが全部 404 になるが、fatal は出ず一覧は普通に見えるので気付けない (#154 の slug 一意化と同じ面の非冪等版)",
        "file": ROOT / "js" / "store.js",
        "find": "        const _seenSlugs = new Set();",
        "replace": "        const _seenSlugs = new Set(merged.map((x) => x.slug));",
        "test": "既定プロジェクトの詳細が保存と読み戻しを跨いで変質しない",
    },
    {
        "name": "theme-color がテーマに関わらず常に暗色になる — `isDark ? A : B` を片方に潰す色の取り違えは、ライトテーマを選んだ利用者のモバイルのアドレスバーだけが暗いままになる。**変わるのはページの pixel ではなくブラウザ chrome の色なので screenshot では原理的に捕捉できない**。OS=dark 側のテストは同じ値のまま通るので、OS=light 側の対のテストだけが捕捉する",
        "file": ROOT / "js" / "theme.js",
        "find": "            meta.content = isDark ? '#0b0f19' : '#ffffff';",
        "replace": "            meta.content = '#0b0f19';",
        "test": "theme-color の実効値が OS=light でもサイトのテーマと一致する",
    },
    {
        "name": "noscript ラッパーが外れて JS 有効時にも説明が描画される — `<noscript>` を素の要素へ置き換えると、**全ページの本文先頭に「JavaScript を有効にしてください」が常時出る**。screenshot は ADVISORY なので気付けず、behavior e2e も『中身がある』ことしか見ていなければ通ってしまう (この対のテストだけが漏れを見る)",
        "file": ROOT / "index.html",
        "find": "            <noscript>\n                <div class=\"container\">",
        "replace": "            <div>\n                <div class=\"container\">",
        "test": "JavaScript 有効時に noscript の内容が漏れない",
    },
    {
        "name": "タスクのステータス移動が SR へ無音に戻る — カードは別の列へ動くが、ボタンのアクセシブル名 (「次のステータスへ進める：<タスク名>」) は変わらないので、SR 利用者には **クリックが効いたのかどうかも分からない** (WCAG 4.1.3)。追加・削除は Toast 経由で通知されるのに移動だけ無音、という非対称だった",
        "file": ROOT / "js" / "apps.js",
        "find": "                announce(`\u300c${task.title}\u300d\u3092${TASK_STATUS_LABEL[next]}\u3078\u79fb\u52d5\u3057\u307e\u3057\u305f`);\n",
        "replace": "",
        "test": "タスクのステータス移動がスクリーンリーダーに通知される",
    },
    {
        "name": "プロジェクト並べ替えの SR 通知が無音に戻る — ボタンのアクセシブル名 (「下へ移動：<名前>」) は移動後も変わらず focus も同じボタンへ戻るので、SR 利用者には **押しても何も起きていないのと区別がつかない** (WCAG 4.1.3)。一覧を見渡せない利用者にとって「何番目へ動いたか」は唯一の手がかり",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                moved = { name: temp.name, pos: idx + dir + 1, total: s.projects.length };\n",
        "replace": "",
        "test": "プロジェクトの並べ替えがスクリーンリーダーに通知される",
    },
    {
        "name": "Speakable の cssSelector が実在しない要素を指す — 音声アシスタント向けの構造化データで、解決しないセレクタを宣言すると **読み上げる箇所が無い**まま「ここを読め」と主張することになる。視覚にも behavior にも一切出ないので、この AIO 精度テスト以外に捕捉層が無い (#929 の『機械向け宣言が一度も成功していなかった』class)",
        "file": ROOT / "js" / "meta-management.js",
        "find": "            'home':        ['h1', '[data-speakable]', '.sr-only[data-ai-entity]'],",
        "replace": "            'home':        ['h1', '.hero-tagline-missing', '.sr-only[data-ai-entity]'],",
        "test": "Home Speakable cssSelectors all resolve to real elements (AIO accuracy)",
    },
    {
        "name": "AIO asset anchor が可視化する — hidden を外すと、AI クローラ向けの生のエンティティ記述 (Canonical Entity: … / Role: … など 1,300 文字超) が **全ページの本文として利用者に見えてしまう**。screenshot は ADVISORY なので気付けない",
        "file": ROOT / "index.html",
        "find": '<div id="aio-asset-anchor" hidden aria-hidden="true"',
        "replace": '<div id="aio-asset-anchor" aria-hidden="true"',
        "test": "AIO asset anchor must be hidden (non-visual)",
    },
    {
        "name": "テーマ選択が永続化されなくなる — cycle() の updateSilently を外すと、切り替えた直後は正しく見えるのに **reload すると元に戻る**。「設定したのに戻っている」という形で出るので、利用者は自分の操作ミスと区別できない",
        "file": ROOT / "js" / "theme.js",
        "find": "        State.updateSilently(s => s.theme = next);",
        "replace": "",
        "test": "Theme toggle cycles data-theme and persists across reload",
    },
    {
        "name": "theme='system' が OS のテーマ変更に追従しなくなる — matchMedia の change リスナーが state を見なくなると、OS をダークへ切り替えてもサイトはライトのまま。**リロードするまで直らない**ので、利用者からは「追従が壊れている」ではなく「たまに合わない」と見える",
        "file": ROOT / "js" / "theme.js",
        "find": "            if (State.get().theme === 'system') {",
        "replace": "            if (false) {",
        "test": "Theme \"system\" follows runtime OS color-scheme changes",
    },
    {
        "name": "startViewTransition proxy が install されなくなる — proxy は『executeSafeTransition を経由せず素の API を直接呼ぶ実装』でも try/catch + timeout + reduced-motion が効くようにするための層 (Check 43b が名前の存在を BLOCKING 監視するが、**install されているかまでは見ない**)。抜けると ErrorBoundary (C3) の保証がその経路から漏れる",
        "file": ROOT / "main.js",
        "find": "            if (!document.startViewTransition) { return; } // 未対応環境はスキップ",
        "replace": "            return;",
        "test": "5-layer proxy: document.startViewTransition is overridden by proxy",
    },
    {
        "name": "プロジェクト削除が何も消さなくなる — confirm を通したのに一覧から消えない。**破壊的操作は「効かない」方も実害**で、利用者は削除できたと思って別の作業へ移る (次に開いたとき残っていて初めて気付く)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                s.projects = s.projects.filter(p => p.id !== id);",
        "replace": "",
        "test": "Deleting a user project (confirm accepted) removes it everywhere",
    },
    {
        "name": "全リセットが何も戻さなくなる — 最も破壊的な操作の逆で、**「初期化しました」と報告するのに何も初期化されない**。壊れたデータを直すために押した利用者は、直ったと信じて同じ問題を踏み続ける (silent no-op に成功メッセージを付ける #1039/#1040 と同じ class)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            State.set(Store.createDefaultStore());",
        "replace": "",
        "test": "Reset data restores defaults after confirm (destructive)",
    },
    {
        "name": "タグをクリックしても絞り込まれなくなる — 検索語の設定を落とすと、カテゴリだけリセットされて一覧は全件のまま。**クリックは効いている (URL も検索欄も変わる) のに結果だけ変わらない**ので、利用者にはタグが壊れているのか一致が無いのか区別できない",
        "file": ROOT / "js" / "projects-page.js",
        "find": "                                            q = tag; cat = 'All';",
        "replace": "                                            cat = 'All';",
        "test": "Clicking a project card tag filters projects by that tag",
    },
    {
        "name": "本文中のリンクが色だけで判別される状態に戻る (WCAG 1.4.1) — hero-meta のインラインリンクから下線を外すと、周囲の文と **色でしか区別できなくなる**。色覚特性のある利用者やモノクロ表示では「そこがリンクだと分からない」。screenshot は ADVISORY なので pixel が変わっても止まらず、この computed-style テストだけが捕捉層",
        "file": ROOT / "style.css",
        "find": "        .hero-meta a {\n            text-decoration: underline;\n        }",
        "replace": "        .hero-meta a {\n            text-decoration: none;\n        }",
        "test": "Hero-meta inline link is distinguishable by underline (WCAG 1.4.1, not color-only)",
    },
    {
        "name": "AI 入力の名前が placeholder だけに戻る (WCAG 4.1.2) — aria-label を外すと、SR は placeholder を名前として読む実装もあれば読まない実装もあり、**入力すると placeholder が消えるので名前まで消える**。「何を入力する欄か」が操作の途中で失われる",
        "file": ROOT / "js" / "ai-page.js",
        "find": "                                'aria-label': 'AI アシスタントへの依頼を入力',\n",
        "replace": "",
        "test": "AI assist main input exposes an accessible name (not placeholder-only)",
    },
    {
        "name": "ポモドーロ設定の label が宙に浮く — `for` を外すと **ラベル文字をクリック/タップしても何も起きず**、タップ標的も縮む。入力欄側に aria-label があるため **axe は緑のまま**で、#1014 で 6 個まとめて直した class の再混入をこのテストだけが捕捉する",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": ", for: 'pomo-setting-work' }",
        "replace": " }",
        "test": "ポモドーロに宙に浮いた label が無い",
    },
    {
        "name": "壊れた JSON の取り込みが無言で失敗する — catch の通知を消すと、パースに失敗しても **何も起きない**。利用者はファイルを選んだのに成功も失敗も告げられず、取り込めたのか分からないまま放置される (silent failure。crash しないこと自体は保たれるので FatalPage 検査では捕捉できない)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                } catch (err) {\n                    Toast.show('JSON\u306e\u30d1\u30fc\u30b9\u306b\u5931\u6557\u3057\u307e\u3057\u305f', 'error');\n                }",
        "replace": "                } catch (err) {\n                }",
        "test": "Settings import shows an error for malformed JSON file without crashing",
    },
    {
        "name": "quiz 検索の空状態が消える — 一致ゼロのとき何も描画されなくなり、**真っ白な一覧**になる。利用者には「検索が壊れた」のか「一致が無い」のか区別できず、0 件であることすら分からない (#892 で実バグ化した『切替先が空ページ』と同じ面)",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "                listHost.appendChild(h(\"div\", { class: 'card panel-empty' },\n                    '\u300c' + query + '\u300d\u306b\u4e00\u81f4\u3059\u308b\u554f\u984c\u306f\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f\u3002'));",
        "replace": "",
        "test": "Quiz search filters question blocks and shows empty state on no match",
    },
    {
        "name": "architecture quiz の stakeholder ゾーンが描画されなくなる — 最大のコンテンツ面 (24,500 文字) の構造化ゾーンが消えても、他の章は普通に見えるので **一覧としては壊れて見えない**。#285 で『画面に見えるのに検索できない』を直した面そのもので、今度は『検索できるのに画面に無い』方向の退行を捕捉する",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": '                        const shList = h("div", { role: "list", style: "display: contents;" });',
        "replace": '                        const shList = h("div", { style: "display: none;" });',
        "test": "Quiz architecture type renders structured stakeholder/question zones (?type query)",
    },
    {
        "name": "role-split Speakable が dead class へ戻る — `#role-split-table` (実在 id) を `.role-split-table` (どこにも無い class) へ戻すと、音声アシスタントに『この表を読め』と指しながら **解決先が存在しない**。#929 で実際に見つかった「機械向け宣言が一度も成功していなかった」class そのもので、視覚にも behavior にも一切出ない",
        "file": ROOT / "js" / "meta-management.js",
        "find": "            'role-split':  ['h1', '#role-split-table', '[data-speakable]', '.sr-only'],",
        "replace": "            'role-split':  ['h1', '.role-split-table', '[data-speakable]', '.sr-only'],",
        "test": "Role-split Speakable references the actual table via #role-split-table (not a dead class)",
    },
    {
        "name": "ai-knowhow の Speakable セレクタが解決しなくなる — home / role-split と**別のルート**の宣言で、独立に腐りうる (ページ側の class 名を変えれば片方だけ dead になる)。AIO 精度は route ごとに独立した契約なので、1 ルート被覆では他が守られない",
        "file": ROOT / "js" / "meta-management.js",
        "find": "            'ai-knowhow':  ['h1', '.ai-summary-block', '[data-speakable]', '.sr-only'],",
        "replace": "            'ai-knowhow':  ['h1', '.ai-summary-block-missing', '[data-speakable]', '.sr-only'],",
        "test": "ai-knowhow/about Speakable cssSelectors (non-baseline) resolve to real elements (AIO accuracy)",
    },
    {
        "name": "絞り込み select の focus 復元用 id が外れる — main.js _renderCore の復元は **id を鍵にする**ので、id を失ったコントロールだけが取り残されて change のたび focus が body へ落ちる。キーボード利用者は絞り込みを 1 段変えるたびに文書先頭へ戻され、**2 回目以降の操作ができない**。Check 422 は静的に id の存在を守るが、こちらは復元が実際に働くことを見る",
        "file": ROOT / "js" / "apps.js",
        "find": "                        id: 'task-filter-priority',\n",
        "replace": "",
        "test": "WCAG 2.1.1: 絞り込み select を変更しても focus が select に残る",
    },
    {
        "name": "AI 送信の連打ガードが外れる — `aiLoading` を条件から落とすと、キーリピートや連打で **描画が追いつく前に次の keydown が届き**、同じ会話が複数回 history に積まれる。1 回の送信が history エントリと 300ms の生成を伴うので、**会話ログが壊れ localStorage も無駄に膨らむ** (#1061 の task/todo Enter 連打と同 class の AI 面)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "            if (!input.trim() || aiLoading) {return;}",
        "replace": "            if (!input.trim()) {return;}",
        "test": "AI 送信の連打で同じ会話が二重に積まれない",
    },
    {
        "name": "import の append 分岐が新規プロジェクトを取り込まなくなる — 既定モードは 'append' で、**バックアップからの復旧はこの経路を通る**。取り込みが no-op になっても「インポートが完了しました」とだけ出るので、利用者は復元できたと信じて元データを捨てうる (#1039/#1040 の silent no-op と同じ形の、既定経路版)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                            parsed.projects.forEach(p => { if (!existing.has(p.id)) { appended.push(p); } });",
        "replace": "",
        "test": "Settings import (valid JSON) appends projects and persists (data recovery)",
    },
    {
        "name": "window.addEventListener が直接上書きされる — main.js は listener registry を **prototype/API を書き換えずに**実装している (書き換えると DOM の意味論がサイト内だけ非標準になり、他コードや e2e の診断が壊れる・#963 で perf-guards の style hook を除去したのと同じ理由)。この不変条件はどの静的 Check も見ておらず、この security test だけが捕捉層",
        "file": ROOT / "main.js",
        "find": "        (function _installEventListenerRegistry() {",
        "replace": "        (function _installEventListenerRegistry() {\n            window.addEventListener = window.addEventListener.bind(window);",
        "test": "5-layer proxy: window.addEventListener is not directly overwritten",
    },
    {
        "name": "home の注目枠が非表示を無視して戻る (#886) — 既定プロジェクトは削除できず「非表示」が唯一の非公開手段なので、隠したはずのものがトップの注目枠に出続けるのは **公開/非公開の意思**の喪失。ProjectsPage だけ塞いでも home が漏れる listing mesh の一角",
        "file": ROOT / "js" / "home-page.js",
        "find": "        const visibleProjects = state.projects.filter(p => !hiddenIds.has(String(p.id)));",
        "replace": "        const visibleProjects = state.projects;",
        "test": "非表示は home と Cmd+K にも効き、解除で両方に戻る",
    },
    {
        "name": "Cmd+K 候補が非表示を無視して戻る (#886) — home とは**別 file の別フィルタ**なので独立に腐る。パレットは全ルートから開ける横断導線ゆえ、ここが漏れると非表示にしたプロジェクトへ誰でも到達できてしまう",
        "file": ROOT / "js" / "command-palette.js",
        "find": "            .filter(p => p && p.slug && p.name && !_hidden.has(String(p.id)))",
        "replace": "            .filter(p => p && p.slug && p.name)",
        "test": "非表示は home と Cmd+K にも効き、解除で両方に戻る",
    },
    {
        "name": "詳細ページの推薦が非表示を無視して戻る (#886) — 隠したプロジェクトが「関連」「おすすめ」として他ページから提示され続ける。**推薦は利用者が自分で探していない経路**なので、隠したはずのものが向こうから出てくる形になる",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "        const listable = state.projects.filter(p => !hiddenIds.has(String(p.id)));",
        "replace": "        const listable = state.projects;",
        "test": "非表示は詳細の推薦とカテゴリ選択肢にも効く",
    },
    {
        "name": "カテゴリ選択肢が非表示を無視して戻る (#886) — そのカテゴリの project を全部隠しても選択肢が残り、**選ぶと 0 件になる死んだ選択肢**が生まれる。1 件だけ隠しても変化しない面なので、カテゴリを空にするまで setup しないと検査できない",
        "file": ROOT / "js" / "projects-page.js",
        "find": "            .filter(p => !_hiddenForCats.has(String(p.id)))\n",
        "replace": "",
        "test": "非表示は詳細の推薦とカテゴリ選択肢にも効く",
    },
    {
        "name": "一覧カードのデモが常に同じアプリへ飛ぶ — `apps/${p.demoRoute}` を固定値へ潰すと、どのカードのデモを押しても同じアプリが開く。**一覧は「作品を触る」までの最短導線**なので、閲覧者が最初に試す経路が死ぬ。Check 136 は demoRoute の値が router whitelist に含まれることを静的に守るが、**ボタンが正しいアプリへ遷移するか**は見ない",
        "file": ROOT / "js" / "projects-page.js",
        "find": "onclick: () => Router.navigate(`apps/${p.demoRoute}`) }, 'デモ')",
        "replace": "onclick: () => Router.navigate('apps/task') }, 'デモ')",
        "test": "一覧カードのデモボタンが対応する内蔵アプリを開く",
    },
    {
        "name": "ブランド選択が保存されなくなる — `set()` から `storage.set` だけ落とすと **適用は効くのにリロードで既定へ戻る**。既存のブランド関連テストは localStorage を直接 seed する pre-paint 検証と `data-brand` を直接書き換えるコントラスト検査だけで、**write 面が未被覆**だったため素通りしていた (#294 の producer/consumer class)。配色の単一ソースなので「設定したのに戻っている」形で出る",
        "file": ROOT / "js" / "brand.js",
        "find": "        const b = apply(brand);\n        storage.set(KEY, b);",
        "replace": "        apply(brand);",
        "test": "Settings のブランド選択がリロードを跨いで保持される",
    },
    {
        "name": "QUIZ_DATA_MAP の data 取り違え — pm の `data:` を別の問題集へ差し替えると、**見出しは QUIZ_DATA_MAP の `title` から出るので「PM問題集」のまま**で、中身だけ別の問題集になる。旧テストは見出しとブロックの存在しか見ておらず **緑のまま通っていた** (実測)。map 内の copy-paste 事故で現実に起こりうる形",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "            pm: { title: 'PM問題集', data: pmQuizData },",
        "replace": "            pm: { title: 'PM問題集', data: awsQuizData },",
        "test": "Quiz pm and quality types render their data files",
    },
    {
        "name": "Cmd+K からプロジェクトが検索できなくなる — 候補生成でプロジェクトを落とすと、パレットは**全ルートから開ける横断導線**なので「どこからでもプロジェクトへ飛べる」経路が丸ごと死ぬ。ナビ項目は残るので**パレット自体は正常に見える**",
        "file": ROOT / "js" / "command-palette.js",
        "find": "            .filter(p => p && p.slug && p.name && !_hidden.has(String(p.id)))",
        "replace": "            .filter(() => false)",
        "test": "Command palette searches projects and jumps to a project detail",
    },
    {
        "name": "矢印移動で aria-activedescendant が active option へ同期しなくなる — palette は focus を input に留めて ↑↓ で listbox を操作する combobox なので、**SR には activedescendant だけが「今どれが選ばれているか」を伝える**。視覚的なハイライトは残るため目視では気付けない (WCAG 4.1.2・#699)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        if (inputEl && activeLi && activeLi.id) { inputEl.setAttribute('aria-activedescendant', activeLi.id); }",
        "replace": "",
        "test": "Command palette input tracks active option via aria-activedescendant",
    },
    {
        "name": "手動追加したプロジェクトが state に入らない — フォームは受け付けて成功を報告するのに一覧へ出ない。**利用者が入力した内容がどこにも残らない** silent no-op で、入力し直しても同じ結果になるため原因に辿り着けない",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                s.projects.unshift({",
        "replace": "                if (false) s.projects.unshift({",
        "test": "Settings can add a project manually and it appears on the Projects page",
    },
    {
        "name": "スナップショットが保存されないのに成功と報告する — `Storage.set` を握り潰すと「保存しました」が出て保存済み表示にもなるが、**復元しようとすると何も無い**。バックアップ機能で「成功したと報告するのに実際は保存されていない」のは最も危険な形 (#1039/#1040 の silent no-op と同 class)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            const success = Storage.set(CONSTANTS.SNAPSHOT_KEY, JSON.stringify(snap));",
        "replace": "            const success = true;",
        "test": "Settings app saves a snapshot and reflects the saved-at status",
    },
    {
        "name": "自動推薦 (autoRelated) が空になる — 詳細ページの「おすすめ」導線が消え、**閲覧者が次のプロジェクトへ回遊する経路**が死ぬ。明示的な関連 (relatedProjectIds) は残るのでセクション自体は表示され、**壊れて見えない**",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "        const autoRelated = Store.autoRelatedCandidates(project, listable, 8);",
        "replace": "        const autoRelated = [];",
        "test": "Project detail \"auto-recommended\" card navigates to another project (autoRelated)",
    },
    {
        "name": "AI 応答が空になる — `generateResponse` が空文字を返すようにすると、**利用者が受け取るもの (応答本文) が消える**のに prompt のエコーは残るので画面は動いて見える。旧テストは prompt の描画しか見ておらず緑のまま通っていた (#1126 の quiz と同じ『題名が主張していることを検証していない』class)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "        function generateResponse(input, type) {",
        "replace": "        function generateResponse(input, type) {\n            return '';",
        "test": "AI assist app generates and renders a response for a prompt",
    },
    {
        "name": "正規化ボタンが初期化になる — `validateAndNormalize` を `createDefaultStore` に置き換えると、**「正規化」を押しただけで利用者のデータが全部消える**。Toast は「正規化を完了しました」と出るので、消えたことに気付くのは次に一覧を開いたとき",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            const norm = Store.validateAndNormalize(State.get());",
        "replace": "            const norm = Store.createDefaultStore();",
        "test": "Settings normalize button runs validateAndNormalize without data loss",
    },
    {
        "name": "Toast が自動消滅しなくなる — 通知が画面に残り続け、**操作するたび積み上がって本文を覆う**。出ること自体は正常に見えるので、消えないことに気付くのは画面が埋まってから (focus 中は消さない #903 の一時停止契約とは別で、こちらは無条件に消えなくなる)",
        "file": ROOT / "js" / "ui-components.js",
        "find": "        const schedule = () => { if (duration > 0 && !timer) { timer = setTimeout(() => remove(el), duration); } };",
        "replace": "        const schedule = () => {};",
        "test": "Toast auto-dismisses after its duration (deterministic clock)",
    },
    {
        "name": "TODO の絞り込みが効かなくなる — 「未完了」を選んでも完了済みが混ざったまま。**選択状態は変わる**ので操作は効いて見え、利用者には「絞り込みが壊れている」のか「該当が多い」のか区別できない",
        "file": ROOT / "js" / "apps.js",
        "find": "            if (todoFilter === 'active') {return !t.completed;}",
        "replace": "            if (false) {return !t.completed;}",
        "test": "Todo filter switches the visible set by active/completed/all",
    },
    {
        "name": "Not Found ページの復旧導線が no-op になる — 存在しない URL に迷い込んだ利用者が **そこから抜け出せなくなる**。ページ自体は「見つかりません」と正しく出るので、**壊れているのはボタンだけ**で目視では気付けない (#269 で home の FatalPage 復旧が同じ形で壊れていた)",
        "file": ROOT / "js" / "pages.js",
        "find": "                h('button', { class: 'btn btn-secondary', onclick: () => Router.navigate('') }, 'ホームへ'),",
        "replace": "                h('button', { class: 'btn btn-secondary', onclick: () => {} }, 'ホームへ'),",
        "test": "Unknown route shows a comprehensible Not Found page with working recovery nav",
    },
    {
        "name": "\u4e0a\u9650\u8d85\u904e\u306e import \u304c\u9ed9\u3063\u3066\u5207\u308a\u6368\u3066\u308b \u2014\u2014 \u6b63\u898f\u5316\u306f\u4ef6\u6570\u4e0a\u9650 (MAX_TASKS 500) \u3067 entry \u3092\u843d\u3068\u3059\u304c\u3001\u5831\u544a\u3092\u7d20\u306e\u300c\u5b8c\u4e86\u3057\u307e\u3057\u305f\u300d\u306b\u623b\u3059\u3068\u3001\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u304b\u3089\u5fa9\u5143\u3057\u305f\u5229\u7528\u8005\u306f\u5931\u308f\u308c\u305f\u3053\u3068\u306b\u6c17\u4ed8\u304b\u306a\u3044\u307e\u307e\u5143\u30c7\u30fc\u30bf\u3092\u6368\u3066\u3046\u308b (#1039/#1040 \u306e \u90e8\u5206\u9069\u7528 \u7248)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "if (dropped > 0) { parts.push(",
        "replace": "if (false && dropped > 0) { parts.push(",
        "test": "Over-limit import reports how many entries were dropped",
    },
    {
        "name": "BGM \u306e\u518d\u751f\u5931\u6557\u304c\u7121\u8a00\u306b\u623b\u308b \u2014\u2014 play() \u62d2\u5426\u6642\u306e Toast \u3092\u5916\u3059\u3068 console.warn \u3060\u3051\u304c\u6b8b\u308b\u3002console \u306f\u958b\u767a\u8005\u5411\u3051\u306e\u4fe1\u53f7\u3067\u5229\u7528\u8005\u306b\u306f\u898b\u3048\u305a\u3001\u30dc\u30bf\u30f3\u3092\u62bc\u3057\u3066\u3082\u4f55\u3082\u8d77\u304d\u306a\u3044\u72b6\u614b\u306b\u623b\u308b (BGM \u306f topbar = mobile \u5c02\u7528\u3067\u3001\u901a\u4fe1\u304c\u4e0d\u5b89\u5b9a\u306a\u74b0\u5883\u307b\u3069 audio \u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u3084\u3059\u3044)",
        "file": ROOT / "js" / "ui-components.js",
        "find": "Toast.show('BGM \u3092\u518d\u751f\u3067\u304d\u307e\u305b\u3093\u3067\u3057\u305f', 'error');",
        "replace": "/* mutated */",
        "test": "BGM reports a failed playback attempt",
    },
    {
        "name": "\u4e0a\u9650\u6642\u306e\u8ffd\u52a0\u304c\u6700\u53e4\u306e\u9805\u76ee\u3092\u7121\u901a\u77e5\u3067\u6368\u3066\u308b\u5f62\u3078\u623b\u308b \u2014\u2014 \u4e0a\u9650\u30ac\u30fc\u30c9\u3092\u5916\u3059\u3068 unshift \u5f8c\u306e\u6b63\u898f\u5316 slice(0, MAX) \u304c\u672b\u5c3e\uff1d\u6700\u53e4\u3092\u843d\u3068\u3059\u306e\u306b\u300c\u30bf\u30b9\u30af\u3092\u8ffd\u52a0\u3057\u307e\u3057\u305f\u300d\u3068\u3060\u3051\u4f1d\u3048\u308b\u305f\u3081\u3001\u5229\u7528\u8005\u306f\u81ea\u5206\u304c\u6d88\u3057\u305f\u306e\u3067\u306f\u306a\u3044\u9805\u76ee\u304c\u6e1b\u3063\u305f\u3053\u3068\u306b\u6c17\u4ed8\u3051\u306a\u3044",
        "file": ROOT / "js" / "apps.js",
        "find": "if (State.get().appsData.tasks.length >= CONSTANTS.LIMITS.MAX_TASKS) {",
        "replace": "if (false) {",
        "test": "Adding a task at the limit is refused with a reason",
    },
    {
        "name": "\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u8ffd\u52a0\u306e\u4e0a\u9650\u30ac\u30fc\u30c9\u55b6\u5931 \u2014\u2014 task/todo (#1152) \u3068\u540c\u5f62\u3067\u3001\u5916\u3059\u3068 unshift \u5f8c\u306e\u6b63\u898f\u5316 slice(0, MAX_PROJECTS) \u304c\u6700\u53e4\u306e\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u7121\u901a\u77e5\u3067\u6368\u3066\u308b",
        "file": ROOT / "js" / "settings-page.js",
        "find": "if (State.get().projects.length >= CONSTANTS.LIMITS.MAX_PROJECTS) {",
        "replace": "if (false) {",
        "test": "Adding a project at the limit is refused",
    },
    {
        "name": "\u975e\u65e2\u5b9a\u30d6\u30e9\u30f3\u30c9 (classic = Inter \u3067\u7d04 5.9% \u5e45\u5e83) \u3067\u306e 320px \u30ea\u30d5\u30ed\u30fc\u5951\u7d04\u304c\u5931\u308f\u308c\u308b \u2014\u2014 920px media \u5185\u306e max-width \u3092\u5916\u3059\u3068 cross \u8ef8 auto margin \u306b\u3088\u308a fit-content \u304c viewport \u3092\u8d85\u3048\u308b\u3002\u65e2\u5b9a\u30d6\u30e9\u30f3\u30c9\u3060\u3051\u3092\u901a\u3059 gate \u3060\u3068\u3001\u5e45\u5e83\u306a\u30d5\u30a9\u30f3\u30c8\u3067\u3060\u3051\u3042\u3075\u308c\u308b\u56de\u5e30\u3092\u7d20\u901a\u308a\u3055\u305b\u308b",
        "file": ROOT / "style.css",
        "find": "                   \u306f\u975e\u5230\u9054\u3002 */\n                max-width: 100%;",
        "replace": "                   \u306f\u975e\u5230\u9054\u3002 */\n                max-width: none;",
        "test": "classic \u30d6\u30e9\u30f3\u30c9 (\u3088\u308a\u5e45\u5e83\u306a\u30d5\u30a9\u30f3\u30c8) \u3067\u3082\u3042\u3075\u308c\u306a\u3044",
    },
    {
        "name": "\u6de1\u3044\u30c1\u30c3\u30d7\u306e\u4e0a\u306e\u6587\u5b57\u304c AA \u3092\u5272\u308b\u5f62\u3078\u623b\u308b \u2014\u2014 --on-tint-primary \u3092 --color-primary \u306b\u623b\u3059\u3068\u3001badge / active nav / hero-eyebrow \u306a\u3069 10% alpha \u306e\u80cc\u666f\u306e\u4e0a\u306e\u6587\u5b57\u304c 3.67\u301c4.48 \u3078\u843d\u3061\u308b (WCAG 1.4.3 AA)",
        "file": ROOT / "style.css",
        "find": "--on-tint-primary: var(--color-primary-dark);",
        "replace": "--on-tint-primary: var(--color-primary);",
        "test": "indigo \u30e9\u30a4\u30c8\u306e\u5168\u30da\u30fc\u30b8\u3067 color-contrast \u9055\u53cd\u304c\u30bc\u30ed",
    },
    {
        "name": "\u958b\u3044\u305f\u72b6\u614b\u3067\u3057\u304b\u63cf\u753b\u3055\u308c\u306a\u3044\u9762\u306e contrast \u9000\u884c \u2014\u2014 command palette \u306e active \u9805\u76ee\u306e\u6587\u5b57\u8272\u3092\u4e2d\u9593\u30b0\u30ec\u30fc\u3078\u843d\u3068\u3059\u3002\u30eb\u30fc\u30c8\u3092\u5DE1\u308b\u9759\u7684\u8d70\u67fb\u306f\u9589\u3058\u3066\u3044\u308b\u9593 palette \u3092\u898b\u306a\u3044\u306e\u3067\u7dd1\u306e\u307e\u307e\u3067\u3001\u3053\u306e\u72b6\u614b\u9762\u306e test \u3060\u3051\u304c\u6355\u6349\u3059\u308b",
        "file": ROOT / "style.css",
        "find": ".cmdk-item.is-active, .cmdk-item:hover { background: var(--color-primary, #6366f1); color: #fff; }",
        "replace": ".cmdk-item.is-active, .cmdk-item:hover { background: var(--color-primary, #6366f1); color: #9aa0b8; }",
        "test": "\u30e9\u30a4\u30c8\u306e drawer / palette / toast \u306b color-contrast \u9055\u53cd\u304c\u30bc\u30ed",
    },
    {
        "name": "\u691c\u8a3c\u30a8\u30e9\u30fc\u306e\u8996\u899a\u7684\u8b58\u5225\u304c\u5931\u308f\u308c\u308b \u2014\u2014 [aria-invalid] \u306e\u5883\u754c\u7dda\u3092\u901a\u5e38\u3078\u623b\u3059\u3068\u3001\u4e0d\u6b63\u306a\u6b04\u304c\u6709\u52b9\u306a\u6b04\u3068\u898b\u5206\u3051\u4ed8\u304b\u306a\u304f\u306a\u308b\u3002Toast \u306f duration \u3067\u6d88\u3048\u308b\u306e\u3067\u3001\u6d88\u3048\u305f\u5f8c\u306f\u300c\u3069\u306e\u6b04\u304c\u4e0d\u6b63\u304b\u300d\u306e\u624b\u304c\u304b\u308a\u304c\u7121\u304f\u306a\u308b (WCAG 3.3.1 / 1.4.1)",
        "file": ROOT / "style.css",
        "find": "            border-color: var(--color-danger);\n            border-width: 2px;",
        "replace": "            border-color: var(--border-color);",
        "test": "Invalid form fields are visually distinguishable",
    },
    {
        "name": "palette \u306e\u8996\u899a\u306e\u9078\u629e\u304c ARIA \u3068\u305a\u308c\u308b \u2014\u2014 is-active \u3092\u5148\u982d\u56fa\u5b9a\u306b\u3059\u308b\u3068\u3001SR \u306f 2 \u756a\u76ee\u3092\u8aad\u3080\u306e\u306b\u753b\u9762\u306f 1 \u756a\u76ee\u3092\u5149\u3089\u305b\u308b\u72b6\u614b\u306b\u306a\u308b\u3002\u65e2\u5b58\u306e activedescendant \u30c6\u30b9\u30c8\u306f ARIA \u540c\u58eb\u306e\u6574\u5408\u3057\u304b\u898b\u306a\u3044\u305f\u3081\u7dd1\u306e\u307e\u307e\u7d20\u901a\u308a\u3059\u308b",
        "file": ROOT / "js" / "command-palette.js",
        "find": "            li.classList.toggle('is-active', on);",
        "replace": "            li.classList.toggle('is-active', i === 0);",
        "test": "Command palette keeps visual, ARIA and activedescendant selection in sync",
    },
    {
        "name": "\u7573\u3093\u3060\u30ca\u30d3\u7fa4\u306e\u4e2d\u8eab\u304c tab \u9806\u306b\u623b\u308b \u2014\u2014 visibility:hidden \u3092\u5916\u3059\u3068 max-height:0 \u3060\u3051\u306b\u306a\u308a\u3001\u9ad8\u3055 0 \u306e\u9818\u57df\u306e\u4e2d\u3078 focus \u304c\u5165\u308b (\u5b9f\u6e2c: 11 \u500b\u306e\u30ea\u30f3\u30af\u30fb\u30dc\u30bf\u30f3\u304c focus \u53ef\u80fd)\u3002\u5229\u7528\u8005\u304b\u3089\u306f focus \u304c\u6d88\u3048\u305f\u3088\u3046\u306b\u898b\u3048\u308b (WCAG 2.4.3 / 2.4.7)",
        "file": ROOT / "style.css",
        "find": "            visibility: hidden;\n            transition: max-height 0.25s ease, visibility 0s linear 0.25s;",
        "replace": "",
        "test": "Collapsed nav group content is removed from the tab order",
    },
    {
        "name": "\u898b\u3048\u306a\u3044\u306e\u306b focus \u3067\u304d\u308b\u8981\u7d20\u306e\u6c4e\u7528\u30b2\u30fc\u30c8 \u2014\u2014 \u7573\u3093\u3060\u30ca\u30d3\u7fa4\u306e visibility \u3092\u5916\u3059\u3068\u3001\u5168\u30eb\u30fc\u30c8\u8d70\u67fb\u3067 tab \u9806\u306b\u6b8b\u3063\u305f\u4e0d\u53ef\u8996\u8981\u7d20\u3092\u691c\u51fa\u3059\u308b (\u500b\u5225 test \u3060\u3051\u3060\u3068\u540c\u3058\u5f62\u304c\u5225\u306e\u5834\u6240\u3067\u518d\u767a\u3057\u3066\u3082\u6c17\u4ed8\u3051\u306a\u3044)",
        "file": ROOT / "style.css",
        "find": "            visibility: hidden;\n            transition: max-height 0.25s ease, visibility 0s linear 0.25s;",
        "replace": "",
        "test": "No element is invisible yet still focusable across all routes",
    },
    {
        "name": "\u30ce\u30fc\u30c8\u306e\u4fdd\u5b58\u304c\u5165\u529b\u306e\u305f\u3073\u306b\u8d70\u3089\u306a\u304f\u306a\u308b \u2014\u2014 updateSilently \u3092\u6761\u4ef6\u4ed8\u304d\u306b\u3059\u308b\u3068\u3001debounce \u7a93\u3067\u96e2\u8131\u3057\u305f\u5165\u529b\u304c\u4fdd\u5b58\u3055\u308c\u305a\u300c\u66f8\u3044\u305f\u306e\u306b\u6b21\u306b\u958b\u3044\u305f\u3089\u6d88\u3048\u3066\u3044\u308b\u300d silent \u306a\u30c7\u30fc\u30bf\u640d\u5931\u306b\u306a\u308b",
        "file": ROOT / "js" / "apps.js",
        "find": "                State.updateSilently(s => { s.appsData.notes = val.slice(0, CONSTANTS.LIMITS.NOTES_TEXT); });",
        "replace": "                if (val.length % 1000 === 999) { State.updateSilently(s => { s.appsData.notes = val; }); }",
        "test": "Notes survive navigating away immediately after typing",
    },
    {
        "name": "\u72b6\u614b\u3092\u4f5c\u3089\u306a\u3044\u3068\u73fe\u308c\u306a\u3044\u9762\u306e contrast \u9000\u884c \u2014\u2014 badge-green (\u975e\u8868\u793a\u306b\u3057\u305f\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u306b\u3060\u3051\u51fa\u308b) \u3092\u751f\u306e\u610f\u5473\u8272\u3078\u623b\u3059\u3068 light \u3067 4.38 < 4.5 \u306e AA \u9055\u53cd\u306b\u306a\u308b\u3002\u65e2\u5b9a\u30c7\u30fc\u30bf\u3092\u5DE1\u308b\u30eb\u30fc\u30c8\u8d70\u67fb\u3067\u306f\u4e00\u5ea6\u3082\u63cf\u753b\u3055\u308c\u306a\u3044\u9762",
        "file": ROOT / "style.css",
        "find": "            background: rgba(var(--color-success-rgb), 0.1);\n            color: var(--on-tint-success);\n            border-color: rgba(var(--color-success-rgb), 0.2);",
        "replace": "            background: rgba(var(--color-success-rgb), 0.1);\n            color: var(--color-success);\n            border-color: rgba(var(--color-success-rgb), 0.2);",
        "test": "\u30e9\u30a4\u30c8\u306e drawer / palette / toast \u306b color-contrast \u9055\u53cd\u304c\u30bc\u30ed",
    },
    {
        "name": "\u901a\u77e5\u306e\u7a2e\u5225\u304c\u898b\u5206\u3051\u3089\u308c\u306a\u304f\u306a\u308b \u2014\u2014 alert-error \u306e\u5e2f\u3092\u4e2d\u7acb\u8272\u3078\u623b\u3059\u3068\u3001\u5931\u6557\u901a\u77e5\u3068\u6210\u529f\u901a\u77e5\u304c\u540c\u3058\u898b\u305f\u76ee\u306b\u306a\u308b\u3002Toast.show \u306f 21 \u7b87\u6240\u304c\u7a2e\u5225\u3092\u9078\u3073\u5206\u3051\u3066\u547c\u3093\u3067\u3044\u308b\u306e\u306b\u5168\u3066\u540c\u4e00\u63cf\u753b\u3060\u3063\u305f\u306e\u3092\u76f4\u3057\u305f\u9762",
        "file": ROOT / "style.css",
        "find": "        .alert-success { border-left-color: var(--on-tint-success); }",
        "replace": "        .alert-success { border-left-color: var(--on-tint-danger); }",
        "test": "Toasts have a surface and are visually distinguishable by type",
    },
    {
        "name": "\u901a\u77e5\u304c\u7a4d\u307f\u4e0a\u304c\u3063\u3066\u753b\u9762\u5916\u3078\u51fa\u308b \u2014\u2014 \u540c\u6642\u8868\u793a\u6570\u306e\u4e0a\u9650\u3092\u5916\u3059\u3068\u3001\u9023\u7d9a\u64cd\u4f5c\u3067\u30b3\u30f3\u30c6\u30ca\u304c viewport \u3092\u8d85\u3048\u3001position:fixed \u306a\u306e\u3067\u30b9\u30af\u30ed\u30fc\u30eb\u3057\u3066\u8ffd\u3046\u3053\u3068\u3082\u3067\u304d\u306a\u3044 (\u5b9f\u6e2c: 12 \u4ef6\u3067 bottom=904 vs viewport 720)",
        "file": ROOT / "js" / "ui-components.js",
        "find": "        while (container.children.length > MAX_VISIBLE) {",
        "replace": "        while (false) {",
        "test": "Toasts do not stack past the viewport during rapid actions",
    },
    {
        "name": "\u901a\u77e5\u304c topbar \u306e\u30dc\u30bf\u30f3\u3092\u899a\u3046 \u2014\u2014 \u30e2\u30d0\u30a4\u30eb\u306e top \u30aa\u30d5\u30bb\u30c3\u30c8\u3092\u5916\u3059\u3068\u3001\u901a\u77e5\u8868\u793a\u4e2d\u306f\u30c6\u30fc\u30de\u5207\u66ff / BGM \u30dc\u30bf\u30f3\u304c elementFromPoint \u3067 .alert \u3092\u8fd4\u3057\u64cd\u4f5c\u4e0d\u80fd\u306b\u306a\u308b (\u5b9f\u6e2c 2026-08-20)",
        "file": ROOT / "style.css",
        "find": "                top: calc(64px + 0.75rem);\n                right: 0.75rem;",
        "replace": "                right: 0.75rem;",
        "test": "Toasts never cover the topbar controls on mobile",
    },
    {
        "name": "\u65e2\u5b9a\u72b6\u614b\u3067\u56fa\u5b9a\u8981\u7d20\u304c\u64cd\u4f5c\u8981\u7d20\u3092\u899a\u3046 \u2014\u2014 drawer \u306e overlay \u3092\u65e2\u5b9a\u3067\u53ef\u8996\u306b\u3059\u308b\u3068\u3001\u4f55\u3082\u64cd\u4f5c\u3057\u3066\u3044\u306a\u3044\u306e\u306b\u5168\u30eb\u30fc\u30c8\u3067\u30dc\u30bf\u30f3\u304c\u62bc\u305b\u306a\u304f\u306a\u308b (#1171 \u3068\u540c\u3058 \u300c\u56fa\u5b9a\u8981\u7d20\u304c\u899a\u3046\u300d class \u306e\u65e2\u5b9a\u72b6\u614b\u9762)",
        "file": ROOT / "style.css",
        "find": "        .overlay {\n            display: none;",
        "replace": "        .overlay {\n            display: block;",
        "test": "No fixed overlay covers an interactive element on any route",
    },
    {
        "name": "\u30d5\u30eb\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u304c state \u5168\u4f53\u3092\u542b\u307e\u306a\u304f\u306a\u308b \u2014\u2014 exportFull \u304c projects \u3060\u3051\u3092\u66f8\u304d\u51fa\u3059\u5f62\u3078\u623b\u308b\u3068\u3001\u5229\u7528\u8005\u306f\u300c\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u3092\u53d6\u3063\u305f\u300d\u3068\u4fe1\u3058\u3066\u5143\u30c7\u30fc\u30bf\u3092\u6368\u3066\u3046\u308b (\u5fa9\u5143\u6642\u306b tasks / notes / profile \u304c\u5168\u90e8\u6d88\u3048\u308b)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "function exportFull() { downloadJSON(State.get(),",
        "replace": "function exportFull() { downloadJSON({ projects: State.get().projects },",
        "test": "Settings app exports a full backup as a valid JSON download",
    },
    {
        "name": "profile.email \u306e\u9577\u3055\u4e0a\u9650\u304c\u5916\u308c\u308b \u2014\u2014 import \u306f\u5916\u90e8\u304b\u3089\u6765\u308b\u4fe1\u7528\u3067\u304d\u306a\u3044\u5165\u529b\u306a\u306e\u3067\u3001bound \u3092\u5916\u3059\u3068\u5DE8\u5927\u306a\u6587\u5b57\u5217\u304c\u305d\u306e\u307e\u307e localStorage \u3078\u5165\u308a\u3001\u5bb9\u91cf\u3092\u98df\u3044\u3064\u3076\u3057\u3066\u4ed6\u306e\u4fdd\u5b58\u3092\u58ca\u3059 (ingestion bloat guard)",
        "file": ROOT / "js" / "store.js",
        "find": "                const ok = t.length <= 254",
        "replace": "                const ok = t.length <= 100000",
        "test": "Profile email is length-bounded to 254 on import",
    },
    {
        "name": "AI \u30d7\u30ed\u30f3\u30d7\u30c8\u306e\u9577\u3055 bound \u304c\u5916\u308c\u308b \u2014\u2014 ai.history \u306f\u4fdd\u6301\u4ef6\u6570 (80) \u3067\u3057\u304b\u5207\u3089\u308c\u306a\u3044\u306e\u3067\u30011 \u4ef6\u3042\u305f\u308a\u304c\u7121\u5236\u9650\u3060\u3068\u5DE8\u5927\u306a\u5165\u529b\u304c 80 \u4ef6\u3076\u3093\u7a4d\u307f\u4e0a\u304c\u308a localStorage \u3092\u98df\u3044\u3064\u3076\u3059\u3002**\u3053\u306e\u914d\u7dda\u306f\u4e00\u5ea6\u5931\u308f\u308c\u305f\u7d4c\u7def\u304c\u3042\u308b** (Check 125 \u304c\u691c\u51fa\u3057\u3066\u518d\u914d\u7dda)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "prompt: input.slice(0, CONSTANTS.LIMITS.AI_MESSAGE),",
        "replace": "prompt: input,",
        "test": "AI prompt is bounded by AI_MESSAGE when stored",
    },
    {
        "name": "\u624b\u52d5\u8ffd\u52a0\u3067 Tech \u304c\u9ed9\u3063\u3066\u843d\u3061\u308b \u2014\u2014 \u5207\u308a\u6368\u3066\u306e\u5831\u544a\u3092\u7d20\u306e\u300c\u8ffd\u52a0\u3057\u307e\u3057\u305f\u300d\u3078\u623b\u3059\u3068\u300112 \u4ef6\u8d85\u904e / \u6587\u5b57\u6570\u8d85\u904e\u304c\u7121\u901a\u77e5\u3067\u5931\u308f\u308c\u308b (\u5b9f\u6e2c: 16 \u4ef6\u6295\u5165 \u2192 12 \u4ef6\u4fdd\u5b58\u30fb1 \u4ef6\u76ee 120 \u2192 80 \u6587\u5b57)\u3002\u4ef6\u6570\u4e0a\u9650\u306f maxlength \u3067\u306f\u8868\u73fe\u3067\u304d\u306a\u3044",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            Toast.show(_dropped || _truncated",
        "replace": "            Toast.show(false",
        "test": "Manual project add reports dropped or truncated tech entries",
    },
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。
_E2E_TAIL.append({
    "name": "\u4fdd\u5b58\u5931\u6557\u306e\u8b66\u544a\u304c\u5229\u7528\u8005\u306b\u5c4a\u304b\u306a\u304f\u306a\u308b \u2014\u2014 notifyStorageError() \u304b\u3089 Toast.show() \u3092\u843d\u3068\u3059\u3068 console.error \u3060\u3051\u304c\u6b8b\u308b\u3002\u305d\u308c\u306f\u958b\u767a\u8005\u5411\u3051\u306e\u4fe1\u53f7\u3067\u5229\u7528\u8005\u306b\u306f\u4e00\u5207\u898b\u3048\u305a\u3001\u300c\u4fdd\u5b58\u3067\u304d\u3066\u3044\u306a\u3044\u300d\u3068\u77e5\u3089\u306a\u3044\u307e\u307e\u30bf\u30d6\u3092\u9589\u3058\u305f\u5229\u7528\u8005\u306f\u4f5c\u696d\u3092\u4e38\u3054\u3068\u5931\u3046 (silent \u306a\u30c7\u30fc\u30bf\u640d\u5931)\u3002\u5f93\u6765\u306e quota \u30c6\u30b9\u30c8\u306f console.error \u3057\u304b\u898b\u3066\u304a\u3089\u305a\u3053\u306e\u9000\u5316\u3092\u7d20\u901a\u308a\u3055\u305b\u3066\u3044\u305f",
    "file": ROOT / "js" / "state.js",
    "find": "Toast.show('\u30b9\u30c8\u30ec\u30fc\u30b8\u4e0a\u9650\u306e\u305f\u3081\u4fdd\u5b58\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002\u4e0d\u8981\u306a\u30c7\u30fc\u30bf\u3092\u524a\u9664\u3057\u3066\u304f\u3060\u3055\u3044\u3002', 'error', 5000);",
    "replace": "/* mutated */",
    "test": "localStorage write quota is exceeded",
})

_E2E_TAIL.append({
    "name": "取り込んだ entry の中身が上限で削られた分が報告されなくなる —— 項目内フィールド (tech/tags/highlights/task.tags) の切り捨て件数を通知から落とすと、entry は一覧に残るため利用者には「戻った」ように見えるまま中身だけが消える。#1143 の entry 単位カウントでは 0 のままなので素の「完了しました」に戻る",
    "file": ROOT / "js" / "settings-page.js",
    "find": "if (trimmed > 0) { parts.push(",
    "replace": "if (false && trimmed > 0) { parts.push(",
    "test": "取り込んだ project の中身が上限で削られたら件数を報告する",
})

_E2E_TAIL.append({
    "name": "文字数上限で短縮された項目が報告されなくなる —— name/summary/title 等が上限で切られても通知が素の「完了しました」に戻る。list の件数を数える _trimmed では 0 のままなので、この面だけが silent に戻る (#1177 は手動追加で既に報告しており、取り込み経路だけが取り残されていた非対称)",
    "file": ROOT / "js" / "settings-page.js",
    "find": "if (shortened > 0) { parts.push(",
    "replace": "if (false && shortened > 0) { parts.push(",
    "test": "取り込んだ項目が文字数上限で短縮されたら件数を報告する",
})

_E2E_TAIL.append({
    "name": "前後の空白の trim を「短縮」と誤報する —— profile の email/github は safeEmail/safeUrl が trim 後の値を返すため、比較元を trim しないと空白があるだけの普通のファイルで毎回「短縮されました」と出る。本物の切り捨て警告が信用されなくなる",
    "file": ROOT / "js" / "settings-page.js",
    "find": "&& a[k].length < b[k].trim().length ? 1 : 0), 0);",
    "replace": "&& a[k].length < b[k].length ? 1 : 0), 0);",
    "test": "前後の空白を落としただけでは短縮として報告しない",
})

_E2E_TAIL.append({
    "name": "履歴 (ai/pomodoro) の件数上限で落ちた entry が報告されなくなる —— tasks/todos/projects だけを数えていた元の非対称に戻る。落ちたことは利用者に見えないまま履歴が欠ける",
    "file": ROOT / "js" / "settings-page.js",
    "find": "+ ['ai', 'pomodoro'].reduce((n, k) => n + Math.max(0,",
    "replace": "+ 0 * ['ai', 'pomodoro'].reduce((n, k) => n + Math.max(0,",
    "test": "ノートの切り詰めと履歴の件数落ちを報告する",
})

_E2E_TAIL.append({
    "name": "Markdown ノートの切り詰めが報告されなくなる —— notes は単一ドキュメントで上限 (20,000) 超過時に末尾がまるごと消えるが entry も件数も減らないため、報告を外すと全カウンタ 0 のまま素の「完了しました」に戻る",
    "file": ROOT / "js" / "settings-page.js",
    "find": "+ shortenedObj({ notes: apps(before).notes }, { notes: apps(after).notes });",
    "replace": "+ 0 * shortenedObj({ notes: apps(before).notes }, { notes: apps(after).notes });",
    "test": "ノートの切り詰めと履歴の件数落ちを報告する",
})

_E2E_TAIL.append({
    "name": "「対象」モードが appsData に効かなくなる —— 既定の「追加のみ」を選んでいても丸ごと置き換わり、利用者の既存タスク・TODO・ノート・履歴が全部消える。最も安全なつもりの選択が最も破壊的になる旧挙動への退行",
    "file": ROOT / "js" / "settings-page.js",
    "find": "                        if (settingsImportMode === 'strict') {\n                            merged.appsData = inc;",
    "replace": "                        if (true) {\n                            merged.appsData = inc;",
    "test": "「追加のみ」の import は既存タスクを消さない",
})

_E2E_TAIL.append({
    "name": "append と upsert の区別が消える —— id が衝突したとき「追加のみ」でも既存 entry を上書きしてしまう (追加のみ = 既存を更新しない、の契約破り)",
    "file": ROOT / "js" / "settings-page.js",
    "find": "if (!map.has(x.id) || settingsImportMode === 'upsert') { map.set(x.id, x); }",
    "replace": "map.set(x.id, x);",
    "test": "「追加のみ」の import は既存タスクを消さない",
})

_E2E_TAIL.append({
    "name": "プロジェクト削除が無音に戻る —— 破壊的な単体操作なのに結果を伝えず、通知領域には直前の「プロジェクトを追加しました」が残る。SR 利用者には無音どころか誤った内容が読まれる (並べ替え #1108 / タスク移動 #1107 と同じ class の最後の面)",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (removed) { Toast.show(`\u300c${removed}\u300d\u3092\u524a\u9664\u3057\u307e\u3057\u305f`); }",
    "replace": "",
    "test": "プロジェクトの削除が結果を伝える",
})

_E2E_TAIL.append({
    "name": "削除の confirm ガードが外れる —— 「考え直してキャンセルを押した」利用者のプロジェクトが消える。最悪の silent failure で、しかも default 以外は復元手段が無い",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (!confirm('\u672c\u5f53\u306b\u524a\u9664\u3057\u307e\u3059\u304b\uff1f')) {return;}\n            let removed = null;",
    "replace": "            confirm('\u672c\u5f53\u306b\u524a\u9664\u3057\u307e\u3059\u304b\uff1f');\n            let removed = null;",
    "test": "削除の確認をキャンセルしたら削除を報告しない",
})

_E2E_TAIL.append({
    "name": "snapshot 復元が損失を報告しなくなる —— 復元は import と同じ正規化を通し entry / 中身を失うのに無条件で「復元しました」と言う旧挙動へ。snapshot は単一スロット = 利用者の唯一の復元点なので、import 経路より無防備なのは筋が通らない",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            const _parts = lossParts(snap.data, _norm);",
    "replace": "            const _parts = [];",
    "test": "snapshot の復元で失われた分を報告する",
})

_E2E_TAIL.append({
    "name": "「追加のみ」の既存優先レポートが過剰報告に戻る —— 内容が同じで何も失っていなくても警告を出す。失っていないのに警告を出すと本物の切り捨て警告が信用されなくなる",
    "file": ROOT / "js" / "settings-page.js",
    "find": "                                    && _stable(inc[k]) !== _stable(baseApps[k])).length;",
    "replace": "                                    ).length;",
    "test": "内容が同じなら",
})

_E2E_TAIL.append({
    "name": "「追加のみ」の既存優先レポートが出なくなる —— 実際に取り込まなかった項目があっても黙る (過少報告)。上の過剰報告 mutation と対で、両方向を固定する",
    "file": ROOT / "js" / "settings-page.js",
    "find": "                                _keptOwn = Object.keys(inc).filter(k => k !== 'tasks' && k !== 'todos'",
    "replace": "                                _keptOwn = 0 * Object.keys(inc).filter(k => k !== 'tasks' && k !== 'todos'",
    "test": "内容が違えば",
})

_E2E_TAIL.append({
    "name": "「追加のみ」の取り込みが稼働中のポモドーロを止める —— appsData を常に全置換する旧挙動へ戻ると、既存を壊さないはずのモードで稼働状態まで置き換わる (利用者からは「勝手に止まった」)",
    "file": ROOT / "js" / "settings-page.js",
    "find": "                        if (settingsImportMode === 'strict') {\n                            merged.appsData = inc;",
    "replace": "                        if (true) {\n                            merged.appsData = inc;",
    "test": "「追加のみ」の取り込みは稼働中のポモドーロを止めない",
})

_E2E_TAIL.append({
    "name": "描画完了後に aria-busy が false へ戻らない —— agentic surface が「ずっとローディング中」を宣言し続ける。視覚に一切出ないので screenshot も他の behavior テストも緑のまま (このテストだけが捕捉層)",
    "file": ROOT / "main.js",
    "find": "                if (content) {content.setAttribute('aria-busy', 'false');}",
    "replace": "                if (content) { /* mutated */ }",
    "test": "content div transitions aria-busy correctly during navigation",
})

_E2E_TAIL.append({
    "name": "router の hashchange 購読が外れる —— SPA の遷移機構そのものが止まり、文書内の hash 変更で route が切り替わらなくなる。従来この test は全遷移を page.goto (フルナビゲーション) で行っており、題名が名指しする hashchange 経路を一度も通っていなかった",
    "file": ROOT / "js" / "router.js",
    "find": "    window.addEventListener('hashchange', _dispatchRouteChange);",
    "replace": "    /* mutated */",
    "test": "Hash routing transitions correctly between routes",
})

_E2E_TAIL.append({
    "name": "project-detail の slug 解決が壊れ、既知の slug でも NotFound へ落ちる —— 一覧にはカードが出るのに詳細へ到達できない (#154 の slug 衝突と同じ「到達不能」class)。共有リンクが全部 404 相当になるが、一覧側は正常に見えるため気付きにくい",
    "file": ROOT / "js" / "project-detail-page.js",
    "find": "        const project = state.projects.find(p => p.slug === slug);",
    "replace": "        const project = state.projects.find(p => p.slug === slug + '-x');",
    "test": "Route project-detail renders for a known slug without errors",
})

_E2E_TAIL.append({
    "name": "SR 通知の assertive チャネルが aria-hidden で a11y ツリーから外れる —— 削除 / 取り込み結果 / 並べ替え / フィルタ件数の通知が SR に一切届かなくなる。通知系 e2e は textContent を読むため表示状態に依存せず素通りし、sr-only は元々不可視なので screenshot でも目視でも気付けない",
    "file": ROOT / "index.html",
    "find": '<div id="action-announcement" class="sr-only" aria-live="assertive"',
    "replace": '<div id="action-announcement" class="sr-only" aria-hidden="true" aria-live="assertive"',
    "test": "sr-only content",
})

_E2E_TAIL.append({
    "name": "プロジェクト検索が絞り込まなくなる —— スコア 0 (どの語にも一致しない) の項目まで残り、何を検索しても全件が出る。一覧は「正常に描画されている」ように見えるため、検索が効いていないことに気付きにくい",
    "file": ROOT / "js" / "projects-page.js",
    "find": ".filter(x => x.s > 0)",
    "replace": ".filter(x => x.s >= 0)",
    "test": "Projects search filters to a subset then clears back to the full list",
})

_E2E_TAIL.append({
    "name": "絞り込み中の残り件数アナウンスが全体数になる —— 「未完了」で絞って片付ける使い方では消えた項目は見えなくなるので、残り何件かを伝える唯一の手がかりがこの status 領域。全体数を出すと完了させても数が減らず、SR 利用者には「押したが何件残っているか分からない」状態になる",
    "file": ROOT / "js" / "apps.js",
    "find": "return `TODO: ${label} ${getFilteredTodos().length} 件`;",
    "replace": "return `TODO: ${label} ${State.get().appsData.todos.length} 件`;",
    "test": "絞り込み中に完了させると残り件数のアナウンスが追随する",
})

_E2E_TAIL.append({
    "name": "task の絞り込み中の残り件数アナウンスが全体数になる —— todo 側 (完了で消える) と対称の面。優先度で絞って作業していると変更した項目はビューから消えるため、残り何件かを伝える唯一の手がかりがこの status 領域",
    "file": ROOT / "js" / "apps.js",
    "find": "return `優先度: ${label} ${getFilteredTasks().length} 件`;",
    "replace": "return `優先度: ${label} ${State.get().appsData.tasks.length} 件`;",
    "test": "絞り込み中に優先度を変えると残り件数のアナウンスが追随する",
})

_E2E_TAIL.append({
    "name": "main の tabindex=-1 が外れ、skip-link の着地点が失われる —— WCAG 2.4.1 のバイパス手段が黙って壊れる。sr-only でも screenshot でもない構造の欠落なので、視覚には一切出ない",
    "file": ROOT / "index.html",
    "find": '<main id="main-content" class="main-content" tabindex="-1"',
    "replace": '<main id="main-content" class="main-content"',
    "test": "全ルートで main ランドマークが一意で、名前と skip-link 着地点を保つ",
})

E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE3 + E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL


