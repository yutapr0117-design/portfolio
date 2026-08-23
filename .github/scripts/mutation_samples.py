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
    "find": "quality: '\u54c1\u8cea\u30fb\u30d7\u30ed\u30bb\u30b9\u554f\u984c\u96c6'",
    "replace": "quality: '\u54c1\u8cea\u30fb\u30d7\u30ed\u30bb\u30b9\u554f\u984c\u96c6\uff08\u7dcf\u5408\u6f14\u7fd2\u7de8\uff09'",
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

_MUTATIONS_TAIL.append({
    "name": "Check 438: 葉モジュールの docstring が宣言する export と実際の return が drift しても気付けなくなる —— 宣言されていないメンバーは「再利用してよいか」を判断する人から見えず、散文は誰も読まないので放置され続ける (2026-08-20 に抽出増分の中で 2 件同時に drift した)",
    "file": ROOT / "js" / "settings-page.js",
    "find": "    return { SettingsPage, getImportOptions };",
    "replace": "    return { SettingsPage, getImportOptions, extra: 1 };",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 439: e2e の走査ルート一覧に存在しないハッシュが混ざる —— その entry は NotFound へ解決するため gate は淡々と緑を返し、本物のページが一度も走査されない (#96-99 の vacuous-hash class の a11y 版)",
    "file": ROOT / "e2e" / "a11y-axe.spec.js",
    "find": "'/#/apps/pomodoro', '/#/settings', '/#/quiz'",
    "replace": "'/#/apps/pomodoro', '/#/apps/settings', '/#/quiz'",
})

_MUTATIONS_TAIL.append({
    "name": "Check 440: コード側から docs/ への参照が腐る —— 「詳細はこの doc を読め」という読者の導線が行き止まりになるが、コメントなので lint も test も気付かない",
    "file": ROOT / "playwright.config.cjs",
    "find": "docs/files/playwright.config.cjs.md",
    "replace": "docs/files/playwright.config.cjs.MISSING.md",
})

_MUTATIONS_TAIL.append({
    "name": "Check 46d: JS 構文 gate が名ばかりへ戻る —— bare `node --check <file>` は ESM file の構文エラーを報告せず exit 0 するため、shipped JS 40 file 中 35 file が silent に無検査になる (2026-08-22 実測: js/brand.js に `let let = 1;` を植えても rc=0)",
    "file": ROOT / "package.json",
    "find": "\"lint:js\": \"node .github/scripts/check_js_syntax.mjs main.js",
    "replace": "\"lint:js\": \"node --check main.js && node .github/scripts/check_js_syntax.mjs main.js",
})

_MUTATIONS_TAIL.append({
    "name": "Check 46c: JS 構文 gate が存在するのに配線されない —— runner を残したまま lint:js から呼び出しを外すと、gate は「在る」のに一度も走らず全 shipped JS が無検査になる (存在 ≠ 配線)",
    "file": ROOT / "package.json",
    "find": "node .github/scripts/check_js_syntax.mjs main.js sw.js",
    "replace": "node .github/scripts/check_js_syntax.UNWIRED.mjs main.js sw.js",
})

_MUTATIONS_TAIL.append({
    "name": "Check 413b: 「数値の真値」を名乗る runbook §9 の行が自分自身と矛盾する —— 1 つの数値だけ更新して内訳を忘れると、同じ行が複数の総数を同時に主張する状態になり、読み手はどれを信じるか決められない (2026-08-22 実測: 総数 530 / source 264 / mirror 250 / = 490 の 3 通りが同居し、Check 413 は 6 個中 2 個しか git と突き合わせないため緑だった)",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    # anchor は **不変の定数**「README + _template の 2」を狙う。総数/source/mirror の 3 つは
    # file を 1 つ足すだけで動くので、そこを anchor にすると **増分のたび Check 362 が orphan を
    # 報告する**（2026-08-23 に実際に発生）。**2** は docs/files の 2 つの非 mirror file を数えた
    # 値で、file 数が動いても変わらない。2→3 にすると和が総数を 1 超えて 413b が RED になる。
    "find": "`docs/files/_template.md` の **2**",
    "replace": "`docs/files/_template.md` の **3**",
})

# ── Check 441 (ACD-1.0 ライセンス本文の構造整合と配線) ──────────────────────────
# NOTE: **Check 442 (binary metadata の到達可能性) には mutation を登録できない。**
#   mutation_probe は対象 file を `read_text(encoding="utf-8")` で読むので、WebP / MP3 は
#   UnicodeDecodeError になり適用そのものが成立しない。非 vacuity は 2026-08-23 に手動で
#   実測済 (COMM の size を過大値へ戻す → 442a/442b が RED / RIFF size を 1 ずらす → 442c が RED)。
#   RED を実測できない mutation を安全網に混ぜないための非登録であって、被覆漏れではない。

_MUTATIONS_TAIL.append({
    "name": "Check 441a (ライセンス本文の条項番号): 節内で番号を重複させる —— 条項を挿入・削除して "
            "再採番を忘れると起きる。ライセンスは CI のどの層にも読まれないので壊れても全部緑のまま "
            "SPDX / OSI 提出まで到達しうる (起草中に実際に踏んだ)",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": "  15.8 English is the authoritative",
    "replace": "  15.7 English is the authoritative",
})

_MUTATIONS_TAIL.append({
    "name": "Check 441b (ライセンス本文の相互参照): 存在しない条項を指させる —— 再採番したのに "
            "本文中の 'Section N.M' を追従させ忘れると、読み手は別の条項へ飛ばされる",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": "Section 15.4 applies, and the invalidity",
    "replace": "Section 15.99 applies, and the invalidity",
})

_MUTATIONS_TAIL.append({
    "name": "Check 441c (ライセンス本文の定義語): 定義だけ改名して本文の使用箇所を残す —— "
            "定義が本文で一度も使われない状態は、起草途中の残骸か削除した条項の痕跡",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": '"Reservation" means any act',
    "replace": '"ReservationX" means any act',
})

_MUTATIONS_TAIL.append({
    "name": "Check 441d (ライセンス本文の義務語): 利用者への義務を混入させる —— §10.1 は「利用者に "
            "一切の条件を課さない」と宣言しており、義務語の混入は**このライセンスの中核主張そのものを "
            "偽にする**。しかも混入先が「表示は不要」と述べる §10.2 なので、本文が自分と逆のことを言い出す",
    "file": ROOT / "LICENSES" / "ACD-1.0.txt",
    "find": "  10.2 In particular, You need not give attribution",
    "replace": "  10.2 You must give attribution. In particular, You need not",
})

_MUTATIONS_TAIL.append({
    "name": "Check 441e (LICENSE の配線): 全文 path への参照を外す —— 全文ファイルが存在しても "
            "LICENSE が指していなければ、受領者はどの条項に従うのか判定できない (存在 ≠ 配線)",
    "file": ROOT / "LICENSE",
    "find": "Full text: LICENSES/ACD-1.0.txt",
    "replace": "Full text: see the LICENSES directory",
})

_MUTATIONS_TAIL.append({
    "name": "Check 443 (advisory 予算 < hard ceiling): 予算を hard ceiling と同値へ戻す —— "
            "その file の早期警告が構造的に一度も出なくなり (OK からいきなり BLOCKING へ飛ぶ)、"
            "「advisory は BLOCKING を踏む前に効かせる」という本リポジトリの標準規律が働かない状態に戻る",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": ".github/scripts/mutation_samples_archive.py | 950 | advisory",
    "replace": ".github/scripts/mutation_samples_archive.py | 1000 | advisory",
})

_MUTATIONS_TAIL.append({
    "name": "Check 444 (ライセンス宣言の cross-surface coherence): HTML 標準の license リンクを外す —— "
            "ACD-1.0 §6.5 は「自動化システムが判定できない許諾は、学習されるための著作物にとっては "
            "許諾ではない」と述べているので、宣言が 1 面でも欠けるとその経路の agent は学習可否を判定できない",
    "file": ROOT / "index.html",
    "find": '<link rel="license" href="/portfolio/LICENSES/ACD-1.0.txt" />',
    "replace": '<!-- license link removed by mutation probe -->',
})

_MUTATIONS_TAIL.append({
    "name": "Check 445 (SPDX 提出物の同期): 提出用 XML を手で書き換える —— 提出物は本文から "
            "導出しているので、手編集は「本文と食い違う XML を提出する」ことを意味する。"
            "XML は普段誰も読まないため drift に気付く経路が無く、いつか嘘を提出することになる",
    "file": ROOT / "LICENSES" / "ACD-1.0.spdx.xml",
    "find": 'licenseId="ACD-1.0"',
    "replace": 'licenseId="ACD-1.1"',
})

_MUTATIONS_TAIL.append({
    "name": "Check 446 (WebMCP ツールの宣言): capabilities.tools を false へ戻す —— 実行可能な "
            "ツールが登録されているのに「ツールは無い」と宣言する状態。2026-08-23 まで実際に"
            "そうなっており、静的 discovery しかしない agent はツールの存在を知りようがなかった",
    "file": ROOT / ".well-known" / "mcp.json",
    "find": '"tools": true,',
    "replace": '"tools": false,',
})

_MUTATIONS_TAIL.append({
    "name": "Check 447 (制約列挙の正典一致): C6 を列挙から落とす —— エージェントはこの prompt を "
            "展開して監査するので、名前が欠けると**存在しない制約セットを監査する**。"
            "2026-08-23 まで実際に C5/C6/C7 が欠落していた (範囲の表記だけ更新され中身が古いまま)",
    "file": ROOT / ".well-known" / "mcp.json",
    "find": "C6 AIO Integrity / ",
    "replace": "",
})

_MUTATIONS_TAIL.append({
    "name": "Check 448 (Agent Skills 仕様適合): 必須 field `description` を落とす —— 仕様の設計は "
            "「agent は起動時に name と description だけを読んで関連性を判断する」progressive "
            "disclosure なので、欠けると **agent は中身を取ってみるまで用途が判らない**。"
            "2026-08-23 まで実際に全 entry で欠落しており、宣言した $schema で検証する agent は "
            "index ごと拒否していた",
    "file": ROOT / ".well-known" / "agent-skills" / "index.json",
    "find": '"description": "Read the authoritative machine-readable context',
    "replace": '"_description_removed_by_probe": "Read the authoritative machine-readable context',
})

_MUTATIONS_TAIL.append({
    "name": "Check 449a (RFC 9727 関係型): カタログのメンバーを `item` ではなく `api-catalog` "
            "関係で列挙する —— RFC 9727 でこの関係は「**別の API カタログへの入れ子**」を意味する "
            "ので、`llms-full.txt` などカタログでないリソースを「これらは全てカタログだ」と偽って "
            "宣言することになり、**仕様に従う agent はそれらを linkset として parse しようとして "
            "失敗する**。2026-08-23 まで実際に 7 件すべてがこの状態で、Check 165 は JSON 構造と "
            "anchor しか見ないため検出層が存在しなかった",
    "file": ROOT / ".well-known" / "api-catalog",
    "find": '"item": [',
    "replace": '"api-catalog": [',
})

_MUTATIONS_TAIL.append({
    "name": "Check 450 (非日本語スクリプト混入): 規範層の「権威テキスト」前半 3 字をキリル文字へ "
            "戻す —— 字形が近いため目視では気付けず、spell-check は走らず lint は JS しか読まず "
            "prose は何とも比較されないので **どの層も検出しない**。2026-08-23 まで実際に規範層 "
            "(C6 を説明する行) と decision record の 2 箇所に残存していた",
    "file": ROOT / "docs" / "architecture" / "repository-maintainability-map.md",
    "find": "\u6a29\u5a01\u30c6\u30ad\u30b9\u30c8",
    "replace": "\u6a29\u5a01\u0442\u0435\u043a\u30b9\u30c8",
})

_MUTATIONS_TAIL.append({
    "name": "Check 436 (裁可待ち文言・scope + 綴り拡張): agent 定義の pre-edit checklist を "
            "「承認が記録されていなければ REFUSE」へ戻す —— `.claude/agents/` は**エージェントの "
            "挙動を実際に駆動する層**で、ここに承認ゲートがあると AIO 編集を通すたびに canon が "
            "存在しないと明記した「裁可待ち」を再生産する。旧 scope は `.claude/` を一度も見て "
            "おらず、しかも照合が case-sensitive だったため先頭大文字の実在文言を素通りしていた",
    "file": ROOT / ".claude" / "agents" / "aio-guardian.md",
    "find": "1. **Is every claim true and non-fabricated?**",
    "replace": "1. **Orchestrator approval recorded?** If not, REFUSE.",
})

_MUTATIONS_TAIL.append({
    "name": "Check 436 (mirror 面 scope): docs/files/ mirror の C6 記述を承認ゲート型へ戻す —— "
            "mirror doc は「この file を編集するとき何を満たすか」を述べる規範面として読まれる。"
            "2026-08-23 に手作業で 9 枚を掃引したが **綴りを 3 つ見落として 4 枚が残った** ゆえ、"
            "per-instance では閉じない class として構造封じへ昇華した",
    "file": ROOT / "docs" / "files" / "llms-full.txt.md",
    "find": "semantic \u7de8\u96c6\u306f C6 \u306e 3 \u4e0d\u5909\u6761\u4ef6",
    "replace": "semantic \u7de8\u96c6\u306f orchestrator \u660e\u793a\u627f\u8a8d\u5fc5\u9808",
})

MUTATIONS = MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
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
    "file": ROOT / "js" / "settings-io.js",
    "find": "if (trimmed > 0) { parts.push(",
    "replace": "if (false && trimmed > 0) { parts.push(",
    "test": "取り込んだ project の中身が上限で削られたら件数を報告する",
})

_E2E_TAIL.append({
    "name": "文字数上限で短縮された項目が報告されなくなる —— name/summary/title 等が上限で切られても通知が素の「完了しました」に戻る。list の件数を数える _trimmed では 0 のままなので、この面だけが silent に戻る (#1177 は手動追加で既に報告しており、取り込み経路だけが取り残されていた非対称)",
    "file": ROOT / "js" / "settings-io.js",
    "find": "if (shortened > 0) { parts.push(",
    "replace": "if (false && shortened > 0) { parts.push(",
    "test": "取り込んだ項目が文字数上限で短縮されたら件数を報告する",
})

_E2E_TAIL.append({
    "name": "前後の空白の trim を「短縮」と誤報する —— profile の email/github は safeEmail/safeUrl が trim 後の値を返すため、比較元を trim しないと空白があるだけの普通のファイルで毎回「短縮されました」と出る。本物の切り捨て警告が信用されなくなる",
    "file": ROOT / "js" / "settings-io.js",
    "find": "&& a[k].length < b[k].trim().length ? 1 : 0), 0);",
    "replace": "&& a[k].length < b[k].length ? 1 : 0), 0);",
    "test": "前後の空白を落としただけでは短縮として報告しない",
})

_E2E_TAIL.append({
    "name": "履歴 (ai/pomodoro) の件数上限で落ちた entry が報告されなくなる —— tasks/todos/projects だけを数えていた元の非対称に戻る。落ちたことは利用者に見えないまま履歴が欠ける",
    "file": ROOT / "js" / "settings-io.js",
    "find": "+ ['ai', 'pomodoro'].reduce((n, k) => n + Math.max(0,",
    "replace": "+ 0 * ['ai', 'pomodoro'].reduce((n, k) => n + Math.max(0,",
    "test": "ノートの切り詰めと履歴の件数落ちを報告する",
})

_E2E_TAIL.append({
    "name": "Markdown ノートの切り詰めが報告されなくなる —— notes は単一ドキュメントで上限 (20,000) 超過時に末尾がまるごと消えるが entry も件数も減らないため、報告を外すと全カウンタ 0 のまま素の「完了しました」に戻る",
    "file": ROOT / "js" / "settings-io.js",
    "find": "+ shortenedObj({ notes: apps(before).notes }, { notes: apps(after).notes });",
    "replace": "+ 0 * shortenedObj({ notes: apps(before).notes }, { notes: apps(after).notes });",
    "test": "ノートの切り詰めと履歴の件数落ちを報告する",
})

_E2E_TAIL.append({
    "name": "「対象」モードが appsData に効かなくなる —— 既定の「追加のみ」を選んでいても丸ごと置き換わり、利用者の既存タスク・TODO・ノート・履歴が全部消える。最も安全なつもりの選択が最も破壊的になる旧挙動への退行",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (settingsImportMode === 'strict') {\n                        merged.appsData = inc;",
    "replace": "                        if (true) {\n                            merged.appsData = inc;",
    "test": "「追加のみ」の import は既存タスクを消さない",
})

_E2E_TAIL.append({
    "name": "append と upsert の区別が消える —— id が衝突したとき「追加のみ」でも既存 entry を上書きしてしまう (追加のみ = 既存を更新しない、の契約破り)",
    "file": ROOT / "js" / "settings-io.js",
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
    "file": ROOT / "js" / "settings-io.js",
    "find": "                                && _stable(inc[k]) !== _stable(baseApps[k])).length;",
    "replace": "                                    ).length;",
    "test": "内容が同じなら",
})

_E2E_TAIL.append({
    "name": "「追加のみ」の既存優先レポートが出なくなる —— 実際に取り込まなかった項目があっても黙る (過少報告)。上の過剰報告 mutation と対で、両方向を固定する",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                            _keptOwn = Object.keys(inc).filter(k => k !== 'tasks' && k !== 'todos'",
    "replace": "                                _keptOwn = 0 * Object.keys(inc).filter(k => k !== 'tasks' && k !== 'todos'",
    "test": "内容が違えば",
})

_E2E_TAIL.append({
    "name": "「追加のみ」の取り込みが稼働中のポモドーロを止める —— appsData を常に全置換する旧挙動へ戻ると、既存を壊さないはずのモードで稼働状態まで置き換わる (利用者からは「勝手に止まった」)",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (settingsImportMode === 'strict') {\n                        merged.appsData = inc;",
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

_E2E_TAIL.append({
    "name": "Markdown ノートの見出しが固定 2 段 demote へ戻り、### から書き始めた note で h2 の直後に h5 が来て見出しが飛ぶ (WCAG 1.3.1) —— 既定 note が # 始まりなので出荷状態では見えず、利用者の書き方次第で見出しナビが壊れる",
    "file": ROOT / "js" / "apps.js",
    "find": "                if (_mdBase === null) { _mdBase = _md; }",
    "replace": "                _mdBase = 1;",
    "test": "Markdown ノートの見出しは書き始めのレベルに関わらず preview 階層へ接続する",
})

_E2E_TAIL.append({
    "name": "検索 0 件のとき role=list の中へ空状態カード (role=status) が入り、リストの意味論が壊れる (WCAG 1.3.1) —— 既定状態では 0 件にならないので全ルート axe 走査では一度も踏まれない「既定値だけが偶然 clean」class",
    "file": ROOT / "js" / "projects-page.js",
    "find": "                    gridContainer.removeAttribute('role');\n                    gridContainer.appendChild(h('div', { class: 'card card--full-col', role: 'status'",
    "replace": "                    gridContainer.appendChild(h('div', { class: 'card card--full-col', role: 'status'",
    "test": "検索 0 件でもリストの意味論が壊れない",
})

_E2E_TAIL.append({
    "name": "TODO 一覧に role=list を付けて listitem でない子 (空状態の p) を含ませる —— 非既定状態 (空) にしか現れないリスト意味論の破れ。既定内容で走る全ルート axe 走査では到達しない class (#1213/#1214 と同型)",
    "file": ROOT / "js" / "apps.js",
    "find": "            todoListHost = h('section', { class: 'flex flex-col gap-2', id: 'todo-list-host' },",
    "replace": "            todoListHost = h('section', { class: 'flex flex-col gap-2', id: 'todo-list-host', role: 'list' },",
    "test": "空の状態でも構造 a11y が壊れない",
})

_E2E_TAIL.append({
    "name": "別タブの更新が稼働中のポモドーロを止める —— cross-tab 採用が受信 store を丸ごと採用し、別タブが持つ「未起動」の runtime で稼働状態を上書きする。利用者からは「別タブで作業していたらポモドーロが消えていた」としか見えず原因に見当がつかない (#940 と同じ『自タブで進行中のものを守る』class)",
    "file": ROOT / "js" / "state.js",
    "find": "        if (_running && data.appsData && data.appsData.pomodoro) {",
    "replace": "        if (false && data.appsData && data.appsData.pomodoro) {",
    "test": "別タブの更新が稼働中のポモドーロを止めない",
})

_E2E_TAIL.append({
    "name": "Cmd+K の候補 0 件で listbox の中へ空状態が入り意味論が壊れる —— 既定状態 (入力なし) では全候補が出るので通常の a11y 走査では一度も踏まれない (#1213/#1214 と同じ『既定値だけが偶然 clean』class)",
    "file": ROOT / "js" / "command-palette.js",
    "find": "            listEl.removeAttribute('role');\n",
    "replace": "",
    "test": "Cmd+K の候補 0 件で listbox 意味論が壊れず",
})

_E2E_TAIL.append({
    "name": "壊れた projects entry (null / 文字列) が正規化の型ガードを素通りし、後段の dereference で FatalPage crash する —— 取り込みは untrusted 入力の最外周なので、entry 単位のガードが最初の防波堤 (#93/#295/#561 の ingestion 正規化 class)",
    "file": ROOT / "js" / "store.js",
    "find": "        const normalizedIncoming = (Array.isArray(incomingProjects) ? incomingProjects : [])\n            .filter(p => p && typeof p === 'object')",
    "replace": "        const normalizedIncoming = (Array.isArray(incomingProjects) ? incomingProjects : [])\n            .filter(p => true)",
    "test": "strict import of malformed projects stays graceful",
})

_E2E_TAIL.append({
    "name": "部分 export (Projectsのみ) が別のスライスを書き出す —— バックアップの土台が壊れ、利用者は「戻せないファイル」を作る。しかも export 時点では成功に見えるので、復元しようとして初めて判る",
    "file": ROOT / "js" / "settings-io.js",
    "find": "function exportProjects() { downloadJSON(State.get().projects,",
    "replace": "function exportProjects() { downloadJSON(State.get().appsData,",
    "test": "partial export buttons download the correct State slice",
})

_E2E_TAIL.append({
    "name": "AIO asset anchor (#aio-asset-anchor) が DOM から消える —— 機械可読な資産アンカーは視覚に一切出ないので、消えても screenshot でも目視でも気付けない。本プロジェクトの中核である AIO 面が silent に失われる",
    "file": ROOT / "index.html",
    "find": '<div id="aio-asset-anchor" hidden aria-hidden="true"',
    "replace": '<div id="aio-asset-anchor-removed" hidden aria-hidden="true"',
    "test": "AIO anchor persists in DOM after initial load",
})

_E2E_TAIL.append({
    "name": "ProjectsPage の role='list' を毎描画で付け直すのをやめる —— 空状態分岐が role を外すため、0 件を一度でも経由すると復帰せず listitem が親のいない孤児になる。既定状態では 0 件にならないので全ルート axe 走査では永久に踏まれない",
    "file": ROOT / "js" / "projects-page.js",
    "find": "                gridContainer.setAttribute('role', 'list');\n\n                if (projects.length === 0) {",
    "replace": "                if (projects.length === 0) {",
    "test": "0 件を経由して結果が戻るとリストが復帰する",
})

_E2E_TAIL.append({
    "name": "新しい best-practice 違反が silent に入る —— home のヒーローカードの role を region から listitem へ変えると ARIA in HTML 非適合 (article に listitem は許されない) になるが、WCAG タグの allowlist ゲートは best-practice を丸ごと捨てるため、この baseline 層が無いと永久に無音",
    "file": ROOT / "js" / "home-page.js",
    "find": "h('article', { class: 'card card--accent-top', role: 'region', 'aria-label': ",
    "replace": "h('article', { class: 'card card--accent-top', role: 'listitem', 'aria-label': ",
    "test": "best-practice 違反は既知の 1 パターンだけ",
})

_E2E_TAIL.append({
    "name": "agentic surface の filter を単一ソースから切り離す —— router の getFilterString が常に空を返すと、URL に絞り込みがあっても body[data-ai-state] は「絞り込みなし」と宣言する。視覚には一切出ないため screenshot も目視も気付けない",
    "file": ROOT / "js" / "router.js",
    "find": "        return i === -1 ? '' : raw.slice(i + 1);",
    "replace": "        return '';",
    "test": "data-ai-state.filter は確定後も URL の絞り込みを表す",
})

_E2E_TAIL.append({
    "name": "hero 画像の entity 属性 (data-ai-context) が render から落ちる —— llms-full.txt は Layer 3 として `<audio>` と hero `<img>` が同じ 4 属性を持つと宣言しているが、属性は視覚に出ず hero は JS 描画ゆえ静的 grep でも守れない。落ちても llms-full.txt だけが嘘を言い続ける",
    "file": ROOT / "js" / "home-page.js",
    "find": "                                'data-ai-context':",
    "replace": "                                'data-ai-ctx-typo':",
    "test": "llms-full.txt が宣言する資産の entity 属性が実際の DOM に載っている",
})

_E2E_TAIL.append({
    "name": "ポモドーロの reset が満了値へ復帰しなくなる —— 稼働中の残りは endAtMs から計算されるので、一時停止で remainingSec が drift した状態でしか観測できない。drift の無い経路だけを見ていると『壊れていても緑』になる",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "                s.appsData.pomodoro.runtime.remainingSec = duration;\n            });\n        }\n\n\n        function switchMode(mode) {",
    "replace": "            });\n        }\n\n\n        function switchMode(mode) {",
    "test": "Pomodoro reset button restores full duration and stops",
})

_E2E_TAIL.append({
    "name": "「全リセット」が appsData しか戻さない部分リセットへ退行 —— 利用者は全領域の初期化を求めているのに projects / projectPrefs / profile が残る。非表示は既定プロジェクト唯一の非公開手段なので、戻らないと意図的に隠したものが公開状態のまま残る",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            State.set(Store.createDefaultStore());",
    "replace": "            State.update(s => { s.appsData = Store.createDefaultStore().appsData; });",
    "test": "Reset data restores defaults after confirm",
})

_E2E_TAIL.append({
    "name": "quiz フォームの aria-invalid が入力しても外れなくなる —— SR 利用者は正しく直した欄を「不正」と読まれ続け、修正が効いたか判別できない。視覚には一切出ない属性なので screenshot でも目視でも気付けない",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "                if (el.value.trim()) { el.removeAttribute('aria-invalid'); }",
    "replace": "                /* removed */",
    "test": "Quiz contact form clears aria-invalid as soon as the field is corrected",
})

_E2E_TAIL.append({
    "name": "Settings のプロジェクト追加フォームで aria-invalid が入力しても外れなくなる —— quiz #1232 と同じ非対称。SR 利用者は正しく直した欄を「不正」と読まれ続ける。視覚に出ない属性なので screenshot でも目視でも気付けない",
    "file": ROOT / "js" / "settings-page.js",
    "find": "if (settingsNewName.trim()) { e.target.removeAttribute('aria-invalid'); } } })",
    "replace": "} })",
    "test": "Settings add-project form clears aria-invalid as soon as the name is typed",
})

_E2E_TAIL.append({
    "name": "quiz 検索欄の maxlength が消える —— 超過分は入力欄にも検索結果にも出たまま reload で初めて消えるので、利用者には「同じ語で検索しているのに結果が違う」としか見えない silent truncation",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "            maxlength: CONSTANTS.LIMITS.QUIZ_SEARCH,\n",
    "replace": "",
    "test": "Quiz search input cannot hold more text than it persists",
})

_E2E_TAIL.append({
    "name": "BGM ボタンに aria-label と競合する sr-only テキストが再混入 —— aria-label が上書きするので一度も読み上げられず、しかも状態同期の対象外なので再生中も『再生する』のまま。誰かが aria-label を消すと名前が永久に古い文言で固定される latent trap",
    "file": ROOT / "index.html",
    "find": '<button class="icon-btn" data-bgm-btn id="bgm-btn-top" data-action="bgm:toggle" aria-pressed="false" aria-label="BGMを再生・停止する">',
    "replace": '<button class="icon-btn" data-bgm-btn id="bgm-btn-top" data-action="bgm:toggle" aria-pressed="false" aria-label="BGMを再生・停止する"><span class="sr-only">BGMを再生する</span>',
    "test": "BGM toggle syncs aria-pressed and aria-label with playback state",
})

_E2E_TAIL.append({
    "name": "タスク移動ボタンの矢印が装飾 (aria-hidden) でなくなる —— 可視ラベルが「→」になり accessible name (aria-label) に含まれない不一致 (WCAG 2.5.3)。axe は記号を flag しないので a11y スキャンでは永久に出ない",
    "file": ROOT / "js" / "apps.js",
    "find": "}, h('span', { 'aria-hidden': 'true' }, '\u2192'))",
    "replace": "}, '\u2192')",
    "test": "Task move buttons expose an aria-label describing their purpose",
})

_E2E_TAIL.append({
    "name": "quiz データの遅延読み込みが「まとめ取り」へ退行 —— 開いた種別以外まで取りに行くと、クリティカルパスから 130,595 bytes を外した意味が消える。取得は視覚に出ないので目視でも screenshot でも気付けない",
    "file": ROOT / "main.js",
    "find": "                type === 'pm' ? import('./js/quiz/pm-quiz-data.js').then(m => m.pmQuizData)",
    "replace": "                type === 'pm' ? Promise.all([import('./js/quiz/aws-quiz-data.js'), import('./js/quiz/quality-quiz-data.js')]).then(() => import('./js/quiz/pm-quiz-data.js')).then(m => m.pmQuizData)",
    "test": "Quiz data is fetched only when the quiz is opened",
})

_E2E_TAIL.append({
    "name": "quiz の読み込み中 aria-busy が消える —— 視覚的には「読み込んでいます…」と見えるが SR には「まだ来ていない」ことが伝わらない。遅延読み込み化で生まれた窓なので、遅延を作らないと検証すらできない面",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "        listHost.setAttribute('aria-busy', 'true');\n",
    "replace": "",
    "test": "Quiz announces the loading window with aria-busy",
})

_E2E_TAIL.append({
    "name": "quiz データの読み込み失敗が無音になる —— 遅延読み込み化で新しく生まれた経路。何も出さないと利用者には「問題が 0 件の問題集」と区別が付かず、通信を直せば直る話なのに壊れているのか判らない",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": """            listHost.appendChild(h("div", { class: 'card panel-empty', role: 'alert' },
                '問題の読み込みに失敗しました。通信状況を確認して再読み込みしてください。'));""",
    "replace": "            /* silent */",
    "test": "Quiz reports a failed data load",
})

_E2E_TAIL.append({
    "name": "quiz 一覧コンテナの契約フック data-quiz-list が消える —— これが無いと「データが届いた」ことを検証できない。#content h2 は同期描画される問い合わせ見出しに一致するため、データが来なくても通る vacuous な待ちに戻る",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "const listHost = h(\"div\", { 'data-quiz-list': 'true' });",
    "replace": "const listHost = h(\"div\", {});",
    "test": "Quiz data is fetched only when the quiz is opened",
})

_E2E_TAIL.append({
    "name": "quiz データ到着時に「描画開始時点の語」で描く —— 読み込み中に入力した検索語が捨てられ、入力欄には語が残ったまま一覧は絞り込み前になる。利用者には「検索したのに効いていない」としか見えない",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "            renderList(searchInput.value);",
    "replace": "            renderList(initialSearch);",
    "test": "Quiz applies a search typed while the data was still loading",
})

_E2E_TAIL.append({
    "name": "quiz が「まだ届いていない」を「見つかりませんでした」と偽る —— データ未着で検索すると 0 件になるが、それを not-found として出すと嘘になる。読み込み中は読み込み中として見せ続ける",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": """            if (!sourceData) {
                listHost.appendChild(h("div", { class: 'card panel-empty', 'data-quiz-loading': 'true' },
                    '問題を読み込んでいます…'));
                return;
            }
""",
    "replace": "",
    "test": "Quiz applies a search typed while the data was still loading",
})

_E2E_TAIL.append({
    "name": "hiring-risk の英語見出しから lang=\"en\" が外れる —— 日本語 SR が英語を日本語の音韻で読み上げる (WCAG 3.1.2)。axe には該当ルールが無く、視覚にも一切出ないので捕捉層はこの e2e だけ",
    "file": ROOT / "js" / "hiring-risk-page.js",
    "find": "h('h2', { class: 'h3', lang: 'en' }, '\U0001F4CB Executive Summary')",
    "replace": "h('h2', { class: 'h3' }, '\U0001F4CB Executive Summary')",
    "test": "全ルートで英語だけの文に lang=",
})

_E2E_TAIL.append({
    "name": "settings の aria-labelledby が dangling になる —— 支援技術がその参照を辿ると存在しない要素へ着地し、グループ名が失われる。視覚には一切出ないので screenshot でも目視でも気付けない",
    "file": ROOT / "js" / "settings-page.js",
    "find": "'aria-labelledby': 'settingsIncludeGroupLabel'",
    "replace": "'aria-labelledby': 'settingsIncludeGroupLabelZZ'",
    "test": "全ルートの aria-* id 参照が実在要素へ解決する",
})

_E2E_TAIL.append({
    "name": "data-ai-state を JSON.stringify でなく文字列連結で組む —— filter は URL の query をそのまま echo するので、引用符を含む query 1 つで属性全体が壊れた JSON になり agent は route も loading も読めなくなる。視覚に一切出ない機械可読面の silent failure",
    "file": ROOT / "main.js",
    "find": """                document.body.setAttribute('data-ai-state', JSON.stringify({
                    route: route.name || 'home',
                    // [FIX] 従来は `''` 決め打ちで絞り込みを宣言できなかった (router の単一ソースへ)。""",
    "replace": """                document.body.setAttribute('data-ai-state', '{"route":"' + (route.name || 'home') + '","filter":"' + Router.getFilterString() + '","loading":false}'); void JSON.stringify({
                    route: route.name || 'home',
                    // [FIX] 従来は `''` 決め打ちで絞り込みを宣言できなかった (router の単一ソースへ)。""",
    "test": "data-ai-state は敵対的な query でも valid JSON であり続ける",
})

_E2E_TAIL.append({
    "name": "quiz の動的 import に cache-buster が付く —— ESM のモジュールキャッシュが効かなくなり、開くたびに 83KB を再ダウンロードする。体感は速いままなので気付きにくいが通信量とバッテリーには効く",
    "file": ROOT / "main.js",
    "find": "import('./js/quiz/aws-quiz-data.js').then(m => m.awsQuizData)",
    "replace": "import('./js/quiz/aws-quiz-data.js?v=' + Date.now()).then(m => m.awsQuizData)",
    "test": "Revisiting the quiz does not re-download the question set",
})

_E2E_TAIL.append({
    "name": "「全リセット」が appsData を戻さなくなる —— 稼働中タイマー / quiz 検索語 / 未送信ノートが取り残され、「初期化したのに前の状態が残っている」一貫性の破れになる",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            State.set(Store.createDefaultStore());",
    "replace": "            State.update(s => { s.projects = Store.createDefaultStore().projects; });",
    "test": "Full reset clears pomodoro / quiz search / notes together",
})

_E2E_TAIL.append({
    "name": "ダークテーマの前景トークン (--on-tint-success) が暗背景に暗い色になる —— 全ブランド x ダークの全ページでコントラストが落ちるが、既定のライトでは何も起きないので気付きにくい",
    "file": ROOT / "style.css",
    "find": """                --on-tint-success: #4ade80;""",
    "replace": """                --on-tint-success: #1f3d2a;""",
    "test": "indigo ダークの全ページで color-contrast",
})

_E2E_TAIL.append({
    "name": "nav リンクの aria-current が付かなくなる —— SR 利用者は「今どこにいるか」を失う。視覚は active スタイルが残るので目視でも screenshot でも気付けない (sidebar と drawer が同じ navLink を共有するため両方が同時に壊れる)",
    "file": ROOT / "js" / "components.js",
    "find": "'aria-current': item.active ? 'page' : undefined",
    "replace": "'aria-current': undefined",
    "test": "aria-current marks exactly the active nav item",
})

_E2E_TAIL.append({
    "name": "Lab トグルの開閉状態が永続化されなくなる —— 開いておいた利用者はルート遷移やリロードのたびに畳まれた状態へ戻る。1 回の操作では気付けず「たまに閉じている」としか見えない",
    "file": ROOT / "js" / "components.js",
    "find": "            try { localStorage.setItem(labKey, String(next)); } catch { /* ignore */ }",
    "replace": "            /* persistence removed */",
    "test": "toggle flips aria-expanded",
})

_E2E_TAIL.append({
    "name": "ダーク実効の --text-muted が暗背景に暗い色になる —— drawer / palette / toast など**開いた状態でしか見えない面**のコントラストが落ちる。既定の閉じた状態では何も起きないので通常の a11y 走査では踏まれない",
    "file": ROOT / "style.css",
    "find": """                --text-muted: #9aa4b5;""",
    "replace": """                --text-muted: #2b3444;""",
    "test": "ダークの drawer / palette / toast",
})

_E2E_TAIL.append({
    "name": "nav リンクから href が外れる —— マウスの click ハンドラは残るので**見た目も挙動も変わらず**、キーボード利用者だけがナビゲーションへ到達できなくなる (WCAG 2.1.1)。Googlebot のリンク発見も同時に失われる",
    "file": ROOT / "js" / "components.js",
    "find": "                href: '#/' + item.path,",
    "replace": "                'data-href': '#/' + item.path,",
    "test": "Sidebar nav link is keyboard-operable",
})

_E2E_TAIL.append({
    "name": "上限で断られたときに打った文字が消える —— 追加できたときだけクリアする復元を外すと、"
            "「不要なタスクを削除してください」と言われた時点で入力欄が既に空になっており、"
            "削除して戻っても打ち直しになる (クリア自体は #1061 の二重登録ガードとして必要)",
    "file": ROOT / "js" / "apps.js",
    "find": "if (!addTask(_v)) { e.target.value = _v; }",
    "replace": "addTask(_v);",
    "test": "keeps the typed text when the add is refused by the cap",
})

_E2E_TAIL.append({
    "name": "一時的な通信断から quiz が回復しなくなる —— 失敗した動的 import は module map に "
            "キャッシュされ、以降の import はネットワークへ行かず即 reject する。別 URL での "
            "再取得を外すと、開き直しても永久に失敗表示のまま (完全リロードしか直らない)",
    "file": ROOT / "main.js",
    "find": ").catch(() => _retryQuizData(type))",
    "replace": ")",
    "test": "recovers from a transient load failure by refetching under a new URL",
})

_E2E_TAIL.append({
    "name": "JSON-LD の CreativeWork ノードから license が落ちる —— schema.org で license は "
            "CreativeWork に定義される。1 ノードでも欠けると、その経路から来た agent は "
            "「学習してよいか」を判定できない (ACD-1.0 §6.5)。**視覚には一切出ない**",
    "file": ROOT / "js" / "meta-management.js",
    "find": "'license': SITE_CONFIG.LICENSE_URL,\n                'dateModified'",
    "replace": "'dateModified'",
    "test": "レンダリング後の全 CreativeWork ノードが同一のライセンスを宣言する",
})

_E2E_TAIL.append({
    "name": "HTML 標準の license リンクが消える —— rel=license は権利宣言の最も標準的な入口で、"
            "JSON-LD を読まないツール (ライセンススキャナ等) にとっては唯一の手掛かり",
    "file": ROOT / "index.html",
    "find": '<link rel="license" href="/portfolio/LICENSES/ACD-1.0.txt" />',
    "replace": '<!-- removed by mutation probe -->',
    "test": "HTML 標準の license リンクが全ルートで解決可能な形で存在する",
})

_E2E_TAIL.append({
    "name": "runtime の speakable ノードが canonical と同じ @id にルート固有の name を載せる —— "
            "JSON-LD では同一 @id = 同一エンティティなので property が merge され、"
            "**1 つのエンティティが 2 つの名前を主張**する。「このクエリはこのエンティティにのみ "
            "解決すべき」という中核宣言と真っ向から矛盾する (2026-08-23 の実バグ)",
    "file": ROOT / "js" / "meta-management.js",
    "find": "            'license': SITE_CONFIG.LICENSE_URL,\n            'speakable': {",
    "replace": "            'license': SITE_CONFIG.LICENSE_URL,\n            'name': fullTitle,\n            'speakable': {",
    "test": "同一 @id が矛盾する property 値を宣言しない",
})

_E2E_TAIL.append({
    "name": "取り込みモード「全置換」が appsData に効かなくなる —— #1183 の実バグそのもの。"
            "モードは projects にしか効いておらず、appsData はどのモードでも丸ごと置き換えていた "
            "(既定の「追加のみ」で AppsData を含むファイルを取り込むと**既存のタスク・やること・"
            "ノート・履歴が全部消えた**)。**最も安全なつもりの選択が最も破壊的**で、しかもそれが既定値",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (settingsImportMode === 'strict') {\n                        merged.appsData = inc;",
    "replace": "                    if (false) {\n                        merged.appsData = inc;",
    "test": "「全置換」の import は宣言どおり丸ごと置き換える",
})

_E2E_TAIL.append({
    "name": "取り込みモード「更新+追加」が既存 id を更新しなくなる —— append との差が消え、"
            "3 モードのうち 2 つが同じ挙動になる。**利用者は宣言どおりに動いたと信じて元データを"
            "捨てうる**ので、モード間の意味論の差は e2e で固定しておく必要がある",
    "file": ROOT / "js" / "settings-io.js",
    "find": "if (!map.has(x.id) || settingsImportMode === 'upsert') { map.set(x.id, x); }",
    "replace": "if (!map.has(x.id)) { map.set(x.id, x); }",
    "test": "「更新+追加」の import は既存を残しつつ取り込む",
})

_E2E_TAIL.append({
    "name": "slug 一意化を無効化する —— #154 の実バグ。同名プロジェクトを追加すると slug が衝突し、"
            "ProjectDetailPage の find(p.slug===slug) が先頭のみ返すため**片方の詳細ページへ"
            "到達不能**になる。一覧には両方出るので気付く手掛かりが薄い",
    "file": ROOT / "js" / "store.js",
    "find": "            if (_seenSlugs.has(s)) {\n                let n = 2;",
    "replace": "            if (false) {\n                let n = 2;",
    "test": "Adding two projects with the same name yields unique slugs",
})

E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE3 + E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL
