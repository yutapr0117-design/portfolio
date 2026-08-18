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
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。
MUTATIONS = MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
    {
        "name": "behavior: 絞り込み件数の polite status が失われる (#1031 の回帰) — status role/aria-live を外すと件数変化が SR へ伝わらなくなる。従来は assertive 領域へ書いて読み上げを割り込んでいた非対称を、ProjectsPage/QuizPage と同じ polite なローカル status へ揃えたもの",
        "file": ROOT / "js" / "apps.js",
        "find": "h('div', { class: 'sr-only', role: 'status', 'aria-live': 'polite', id: 'task-filter-status' },",
        "replace": "h('div', { class: 'sr-only', id: 'task-filter-status' },",
        "test": "絞り込みの件数が polite な status でアナウンスされる",
    },
    {
        "name": "behavior: #content が再び live region になる (#1032 の回帰) — ページ本文そのもの (quiz では 24,500 文字) が live region になり、ルート遷移や State 更新のたびにスクリーンリーダーが本文全体を読み直す chatty なアンチパターンへ戻る。ポモドーロ稼働中は毎秒再描画されるため特に害が大きい",
        "file": ROOT / "index.html",
        "find": '<div class="container" id="content" aria-busy="false"></div>',
        "replace": '<div class="container" id="content" aria-busy="false" aria-live="polite"></div>',
        "test": "#content は live region ではなく、通知は専用領域が担う",
    },
    {
        "name": "behavior: full export が 1 フィールド落とす (#1035) — フル export は利用者にとって **バックアップ**なので、export 側で notes が落ちる (あるいは import が無視する) だけで黙ってデータが失われる。部分 export のテストも手書き JSON の import テストもこの経路を通らないため、往復させる test だけが捕捉層",
        "file": ROOT / "js" / "settings-page.js",
        "find": "function exportFull() { downloadJSON(State.get(), ",
        "replace": "function exportFull() { downloadJSON({ ...State.get(), appsData: { ...State.get().appsData, notes: '' } }, ",
        "test": "full export → 全リセット → import で状態が再現する",
    },
    {
        "name": "behavior: import が theme を復元しなくなる (#1036 の回帰) — theme は full export に含まれるのに import が無視すると、フルバックアップを復元しても表示テーマの設定だけが黙って失われる (#139 の profile strip と同じ data-fidelity class)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                    if (typeof parsed.theme === 'string') { merged.theme = parsed.theme; applied = true; }\n",
        "replace": "",
        "test": "表示テーマが export → import で復元され",
    },
    {
        "name": "behavior: DOM がテーマ state に追随しなくなる (#1036 の回帰) — import / 全リセット / snapshot 復元は Theme.cycle を通らないため、data-theme と .dark が古いまま残り reload するまで切り替わらない",
        "file": ROOT / "main.js",
        "find": "                if (_wantTheme && document.documentElement.getAttribute('data-theme') !== _wantTheme) {",
        "replace": "                if (false && _wantTheme && document.documentElement.getAttribute('data-theme') !== _wantTheme) {",
        "test": "表示テーマが export → import で復元され",
    },
    {
        "name": "behavior: import が projectPrefs を復元しなくなる (#1037 の回帰) — backup を戻すと **意図的に隠したプロジェクトが再び公開状態になる**。既定プロジェクトは削除できず『非表示』が唯一の非公開手段 (#886) なので、単なる表示設定ではなく公開/非公開の意思が失われる",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                        if (parsed.projectPrefs && Array.isArray(parsed.projectPrefs.hiddenIds)) {",
        "replace": "                        if (false && parsed.projectPrefs && Array.isArray(parsed.projectPrefs.hiddenIds)) {",
        "test": "非表示にしたプロジェクトが export → import 後も非表示のまま",
    },
    {
        "name": "behavior: 部分 export した素の配列を import が受け付けなくなる (#1038 の回帰) — `Projectsのみ` は projects の素の配列を書き出すので、full-state 形しか見ないと **何も起きないのに『インポートが完了しました』**と報告する。戻せないファイルを作って成功したと言うのは失敗するより悪い",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            if (Array.isArray(raw)) { return { projects: raw }; }",
        "replace": "            if (false && Array.isArray(raw)) { return { projects: raw }; }",
        "test": "部分 export (Projectsのみ) を import で戻せる",
    },
    {
        "name": "behavior: 認識できない形式を silent no-op として成功報告する (#1038 の回帰) — 形式判定が null を返さなくなると、何も適用されないまま『インポートが完了しました』が出る。利用者は復元できたと信じてしまう",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            if (has('name', 'title', 'bio', 'email', 'github', 'linkedin', 'location')) { return { profile: raw }; }\n            return null;",
        "replace": "            if (has('name', 'title', 'bio', 'email', 'github', 'linkedin', 'location')) { return { profile: raw }; }\n            return raw;",
        "test": "認識できない形式の JSON は成功と report しない",
    },
    {
        "name": "behavior: 対象から全部落ちても成功と報告する (#1040 の回帰) — 形は認識できるのに『対象』チェックボックスの選択で中身が全部落ちる場合、1 セクションも適用していないのに『インポートが完了しました』が出る。#1038 で塞いだ silent-lie の残り半分で、利用者からは同じく『バックアップを戻したのに戻っていない』としか見えない",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                    let applied = false;",
        "replace": "                    let applied = true;",
        "test": "対象から外した形の import を成功と report しない",
    },
    {
        "name": "behavior: AppsDataのみ の形を import が受け付けなくなる (#1040) — `AppsDataのみ` は素の appsData オブジェクトを書き出す。この枝が落ちると素の配列 (Projectsのみ) だけが戻せる非対称になり、apps のバックアップだけが黙って戻らない",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            if (has('tasks', 'todos', 'pomodoro', 'ai', 'notes', 'quizSearch')) { return { appsData: raw }; }",
        "replace": "            if (false && has('tasks', 'todos', 'pomodoro', 'ai', 'notes', 'quizSearch')) { return { appsData: raw }; }",
        "test": "対象から外した形の import を成功と report しない",
    },
    {
        "name": "behavior: 全リセットの confirm ガードが消える — キャンセルしても全データが初期化される。破壊操作の確認は『押し間違い』ではなく『考え直した』を守るためのもので、これが効かないとキャンセルを押した利用者がデータを失う。最悪の silent failure なのに安全網の非 vacuity が未実証だった",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            if (!confirm('すべてのデータを初期化しますか？')) {return;}\n",
        "replace": "",
        "test": "Canceling the reset confirm keeps data (data-safety)",
    },
    {
        "name": "behavior: プロジェクト削除の confirm ガードが消える — キャンセルしても削除される。既定プロジェクトは削除できないため対象はユーザーが自分で追加したものだけで、復元手段は backup しか無い",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            if (!confirm('本当に削除しますか？')) {return;}\n",
        "replace": "",
        "test": "Canceling the delete confirm keeps the project (data-safety)",
    },
    {
        "name": "behavior: MAX_PROJECTS の件数上限が緩む — import/cross-tab/snapshot 経由で巨大な projects 配列が localStorage を bloat させ描画を重くする DoS ガードの喪失。NOTE: 切り詰めは mergeProjectsWithDefaults 内で **二重に適用**されている (normalizedIncoming の slice と最終 merged の slice) ため、**片方の slice を消すだけでは RED にならない** (もう片方が受ける)。意味のある mutation は上限値そのものを緩めること",
        "file": ROOT / "js" / "constants.js",
        "find": "        MAX_PROJECTS: 1000,",
        "replace": "        MAX_PROJECTS: 100000,",
        "test": "Import truncates projects to MAX_PROJECTS (bloat/DoS ingestion guard)",
    },
    {
        "name": "behavior: Markdown ノートの XSS 境界が innerHTML へ退行する — ノート本文はユーザーが自由に書ける唯一の長文入力で、innerHTML で描くと <script>/onerror が実行される。C1 の『ライブラリを入れない』制約を feature 化した innerHTML-free レンダラの中核契約であり、壊れても視覚的にはむしろ『markdown が効いた』ように見えるため気付けない",
        "file": ROOT / "js" / "apps.js",
        "find": "            else { flushList(); out.push(h('p', { class: 'text-prewrap' }, ..._renderMarkdownInline(line))); }",
        "replace": "            else { flushList(); const _p = h('p', { class: 'text-prewrap' }); _p.innerHTML = line; out.push(_p); }",
        "test": "Markdown notes renders HTML/script as literal text (innerHTML-free XSS boundary)",
    },
    {
        "name": "behavior: cross-tab の storage リスナーが発火しなくなる — 複数タブで開いた時に片方の変更がもう片方へ伝わらず、後から保存したタブが相手の変更を上書きする (last-writer-wins が壊れ、利用者からは『さっき足したタスクが消えた』に見える)",
        "file": ROOT / "js" / "state.js",
        "find": "        if (e.key === CONSTANTS.STORAGE_KEY && e.newValue) {",
        "replace": "        if (false && e.key === CONSTANTS.STORAGE_KEY && e.newValue) {",
        "test": "Cross-tab sync: a task added in one tab appears in another tab",
    },
    {
        "name": "behavior: localStorage への保存が no-op になる — reload で全データが消える最大級のデータ喪失。NOTE: 保存経路は debounce (scheduleSave) と visibilitychange (saveNow) の **二重**で、reload は後者も通るため **scheduleSave 側だけを潰しても RED にならない**。意味のある mutation は唯一の choke point である Storage.set の書き込みそのもの",
        "file": ROOT / "js" / "storage.js",
        "find": "            localStorage.setItem(key, value);",
        "replace": "            void key; void value;",
        "test": "Task app adds a task and persists it across reload",
    },
    {
        "name": "behavior: Speakable の cssSelector がルート追従しなくなる — 全ルートで既定セレクタを返すと、AI 音声アシスタントは role-split の表 (#role-split-table) や ai-knowhow の要約ブロックを読み上げ対象として認識できない。視覚に一切出ない AIO 面ゆえ screenshot も behavior の描画検査も素通りする",
        "file": ROOT / "js" / "meta-management.js",
        "find": "        const cssSel = SPEAKABLE_SELECTORS[routeName] || ['h1', '[data-speakable]', '.sr-only'];",
        "replace": "        const cssSel = ['h1', '[data-speakable]', '.sr-only'];",
        "test": "Speakable JSON-LD updates cssSelector per route (AIO voice)",
    },
    {
        "name": "behavior: silent な URL 更新で data-ai-state の route が汚れる — 絞り込みの query が route 名に混ざると、agentic surface を読むエージェントが 'projects?q=...' を route 名だと解釈する (#765 の drift class)。NOTE: main.js 側も data-ai-state を書くため、**通常のルート遷移を見るテストではこの mutation は隠れる**。router 経路だけを通る silent-filter のテストと対にすること",
        "file": ROOT / "js" / "router.js",
        "find": "                route: _r.name || 'home',",
        "replace": "                route: 'projects?q=zzz',",
        "test": "Body data-ai-state keeps a clean route name after a silent projects filter",
    },
    {
        "name": "behavior: theme-init.js の theme 復元が効かなくなる — pre-paint に data-theme/.dark を付けられず、dark 利用者に **一瞬 light が見えてから切り替わる FOUC** が出る。main.js が後から適用するので最終状態は正しく、screenshot は ADVISORY ゆえ **この e2e 以外に捕捉層が無い**",
        "file": ROOT / "theme-init.js",
        "find": "                const rawState = localStorage.getItem('portfolio_enhanced_v45');",
        "replace": "                const rawState = null;",
        "test": "theme-init.js applies stored dark theme on initial load (FOUC prevention)",
    },
    {
        "name": "behavior: theme-init.js の brand 復元が効かなくなる — pre-paint に data-brand を付けられず、既定ブランド色が一瞬見えてから切り替わる FOUC が出る (theme 側と同 class)",
        "file": ROOT / "theme-init.js",
        "find": "                const rawBrand = localStorage.getItem('portfolio_brand_v45');",
        "replace": "                const rawBrand = null;",
        "test": "theme-init.js applies stored brand on initial load (brand FOUC prevention)",
    },
    {
        "name": "behavior: slug 衝突の一意化が効かなくなる (#154 の回帰) — 同名プロジェクトを追加/取り込みすると slug が重複し、**片方の詳細ページへ到達できなくなる** (ルーターは先勝ちで解決するため後の 1 件が事実上消える)。一覧には両方出るので画面上は正常に見える",
        "file": ROOT / "js" / "store.js",
        "find": "            if (_seenSlugs.has(s)) {",
        "replace": "            if (false && _seenSlugs.has(s)) {",
        "test": "Importing projects with colliding slugs yields unique slugs (detail reachability)",
    },
    {
        "name": "behavior: テーマ切替の巡回順が壊れる (#262 の症状面) — 1 クリックで 2 段進む / 逆順になる等。#262 は data-action の delegation と直接リスナーの二重発火が原因だったが、症状は『押した段数と表示が一致しない』で同じ。巡回順そのものを入れ替えて、段数を数える assertion が実際に効くことを実証する",
        "file": ROOT / "js" / "theme.js",
        "find": "        const next = current === 'system' ? 'dark' : current === 'dark' ? 'light' : 'system';",
        "replace": "        const next = current === 'system' ? 'light' : current === 'dark' ? 'system' : 'dark';",
        "test": "Topbar theme button advances exactly one step per click (double-fire regression)",
    },
    {
        "name": "behavior: FatalPage の『ホームへ』が __fatalError を解除しなくなる (#298 の回帰面) — フラグが立ったままだと 2 秒毎に走る Shadow DOM 安全網が **復旧できた正常なページを覆い直す**。利用者は一度は復旧できたのに再びエラー画面へ戻され、脱出手段が無くなる",
        "file": ROOT / "js" / "components.js",
        "find": "                    window.__fatalError = null;",
        "replace": "",
        "test": "FatalPage ホームへ recovers from a non-home route too",
    },
    {
        "name": "behavior: drawer が背景 (#app) を inert にしなくなる (#947 の対) — 開いている drawer の裏のリンクやボタンがキーボード/支援技術から操作でき、aria-modal の主張と実態が食い違う。視覚的には drawer が被さって見えるので目視では気付けない",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "        __setAppInert(true);",
        "replace": "",
        "test": "Mobile drawer opens with ARIA, isolates background, and closes on Escape",
    },
    {
        "name": "behavior: silent URL 更新後に currentRoute が stale になる (#765 の内部 route state 版) — 絞り込み中に任意の再描画 (cross-tab sync / State.update) が走ると、ProjectsPage が q='' で描き直されて **検索が消えるのに URL は ?q=.. のまま残る** desync。利用者には『勝手に全件へ戻った』と見える",
        "file": ROOT / "js" / "router.js",
        "find": "            currentRoute = _r;",
        "replace": "",
        "test": "Projects filter survives a full re-render after a silent URL update (getRoute stays in sync)",
    },
    {
        "name": "behavior: 候補ゼロの palette で aria-activedescendant が消えない (#699 の回帰) — input が存在しない option (cmdk-opt-0) を指したままになり、支援技術はその関連付けを黙って無視する。画面上は何も変わらず axe にも該当ルールが無いため、実行時の idref 走査以外に捕捉層が無い",
        "file": ROOT / "js" / "command-palette.js",
        "find": "            if (inputEl) { inputEl.removeAttribute('aria-activedescendant'); }",
        "replace": "",
        "test": "palette / drawer / 検証エラーの一過性状態でも aria-* id 参照が解決する",
    },
    {
        "name": "behavior: 「対象」トグルが全再描画を起こす (#1040/#1053 の根本原因) — #content ごと作り直されて隣の file input が差し替わり、『対象を変えてすぐファイルを選ぶ』操作で change が古い input に飛んで import が起きない。結果だけ見れば同じなので目視でも通常のテストでも観測できず、要素の同一性を直接見る test だけが捕捉層",
        "file": ROOT / "js" / "settings-page.js",
        "find": "onchange: (e) => { settingsIncludeApps = !!e.target.checked; }",
        "replace": "onchange: (e) => { settingsIncludeApps = !!e.target.checked; window.render(); }",
        "test": "モード / 対象の切替でページが作り直されない (file input の同一性が保たれる)",
    },
    {
        "name": "behavior: タスクの絞り込みが全再描画へ戻る — 表示だけの操作なのに #content を作り直すため、『新しいタスク』に打ちかけた未送信テキストが巻き添えで消える (#982 のテーマ切替 / #258 の oninput と同じ class)。絞り込んで確認してから続きを打つのは自然な操作なので実害が大きい",
        "file": ROOT / "js" / "apps.js",
        "find": "                            renderTaskList();",
        "replace": "                            window.render();",
        "test": "タスクの絞り込みを変えても未送信の入力が消えない",
    },
    {
        "name": "behavior: TODO の絞り込みが全再描画へ戻る — task 側と同じ巻き添えで未送信テキストが消える。片方だけ直すと「1 ケースだけ処理して他を忘れる」非対称になるため対で守る",
        "file": ROOT / "js" / "apps.js",
        "find": "                                renderTodoList();",
        "replace": "                                window.render();",
        "test": "TODO の絞り込みを変えても未送信の入力が消えない",
    },
    {
        "name": "behavior: 裏で走るタイマーの完了が全再描画へ戻る — ポモドーロは別アプリを開いていても走り続けるため、完了の State.update が #content を作り直して **利用者が何も操作していないのに** 別ページの未送信入力を消す。自分の操作が引き金でない分、#982 (テーマ切替) や #1055 (絞り込み) より驚きが大きい",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "        if (onPomodoroRoute) { State.update(applyCompletion); }\n        else { State.updateSilently(applyCompletion); }",
        "replace": "        State.update(applyCompletion);",
        "test": "裏でタイマーが完了しても別アプリの未送信入力が消えない",
    },
    {
        "name": "behavior: 取り込んだタスクの id 一意化が失われる — 同 id の項目が並ぶと削除の filter が同 id を全て落とし、**1 件消したつもりが両方消える**。逆に更新は find が先頭しか拾わずもう片方に効かない。DOM 側でも task-delete-<id> 等が重複し focus 復元が別カードを掴む (#154 の slug 一意化と同型)",
        "file": ROOT / "js" / "store.js",
        "find": "            uniquifyIds(result.tasks);\n",
        "replace": "",
        "test": "同じ id のタスクを取り込んでも片方だけ削除できる",
    },
    {
        "name": "behavior: 取り込んだプロジェクトの id 一意化が失われる — 削除・非表示が id で引くため同 id の別プロジェクトまで巻き添えになる。task 側と対で守らないと『1 ケースだけ処理して他を忘れる』非対称になる",
        "file": ROOT / "js" / "store.js",
        "find": "        uniquifyIds(merged);\n",
        "replace": "",
        "test": "同じ id のプロジェクトを取り込んでも片方だけ削除できる",
    },
    {
        "name": "behavior: notes の型ガードが truthy 判定へ緩む — `{}` は slice を持たないため TypeError → validateAndNormalize 例外 → 取り込み経路で FatalPage crash。`[]` なら crash しないが notes が配列のまま描画へ流れる (#568/#572 と同じ truthy 判定の穴)",
        "file": ROOT / "js" / "store.js",
        "find": "        if (typeof data.notes === 'string') {",
        "replace": "        if (data.notes) {",
        "test": "残りの appsData フィールドに敵対的な型を流しても各ページが描画される",
    },
    {
        "name": "behavior: 非表示プロジェクトの除外が効かなくなる (#886 の回帰) — 既定プロジェクトは削除できず『非表示』が唯一の非公開手段なので、これは単なる表示設定でなく **公開/非公開の意思** が無視されること",
        "file": ROOT / "js" / "projects-page.js",
        "find": "            const hiddenIds = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));",
        "replace": "            const hiddenIds = new Set();",
        "test": "Hiding a project removes it from the public Projects list, unhide restores it",
    },
    {
        "name": "behavior: 完了済み削除が何も消さなくなる — ボタンは押せてトーストも出るのに一覧が変わらない。利用者からは『押しても効かない』にしか見えず、失敗も表示されない",
        "file": ROOT / "js" / "apps.js",
        "find": "                s.appsData.todos = s.appsData.todos.filter(t => !t.completed);",
        "replace": "                s.appsData.todos = s.appsData.todos.slice();",
        "test": "Todo app add, complete-toggle, then clear-completed removes the item",
    },
    {
        "name": "behavior: タスク入力の同期クリアが失われ Enter 連打で二重登録される — 入力欄が空になるのは再描画の副作用で、その再描画は非同期 (await yieldToMain)。連打やキーリピートでは e.target.value がまだ元の文字列を持つため同じ値が何度も登録される (実測: 3 回押して 3 件)",
        "file": ROOT / "js" / "apps.js",
        "find": "                                const _v = e.target.value;\n                                e.target.value = '';\n                                addTask(_v);",
        "replace": "                                addTask(e.target.value);",
        "test": "タスク入力の Enter 連打で同じタスクが二重登録されない",
    },
    {
        "name": "behavior: TODO 入力の同期クリアが失われ Enter 連打で二重登録される — task 側と同じ機構。片方だけ守ると『1 ケースだけ処理して他を忘れる』非対称になる",
        "file": ROOT / "js" / "apps.js",
        "find": "                                const _v = e.target.value;\n                                e.target.value = '';\n                                addTodo(_v);",
        "replace": "                                addTodo(e.target.value);",
        "test": "TODO 入力の Enter 連打で同じ TODO が二重登録されない",
    },
    {
        "name": "behavior: Cmd+K の候補に非表示プロジェクトが混ざる (#886 の read 面 mesh の回帰) — 既定プロジェクトは削除できず『非表示』が唯一の非公開手段なので、palette に残ると一覧から隠したはずのものへ到達できてしまう",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        const _hidden = new Set((((_st.projectPrefs && _st.projectPrefs.hiddenIds) || [])).map(String));",
        "replace": "        const _hidden = new Set();",
        "test": "Command palette reflects project add and hide immediately",
    },
    {
        "name": "behavior: 手動追加の名前入力から上限が外れる — normalizeProject が name を LIMITS.PROJECT_NAME で切るので、長い名前は追加直後は全部見えているのに **リロード後に黙って短くなる** (#924 と同じ silent truncation)。Check 410 は同一 file 内の slice を条件にするため、上限が store.js 側にあるこのケースは静的検査の射程外",
        "file": ROOT / "js" / "settings-page.js",
        "find": "maxlength: CONSTANTS.LIMITS.PROJECT_NAME, ",
        "replace": "",
        "test": "手動追加のプロジェクト名が入力上限と保存上限で一致する",
    },
    {
        "name": "behavior: 手動追加が正規化を通さなくなる — normalizeProject は name を LIMITS.PROJECT_NAME、tech を『12 項目・各 LIMITS.CATEGORY 文字』で切るので、通さないと **追加直後は入力どおりに見えるのにリロードで黙って減る** (実測: Tech 20 個 → 12 個)。件数の制限は maxlength では表現できないため入力欄側だけでは揃えられない",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            State.set(Store.validateAndNormalize(State.get()));\n            settingsNewName = '';",
        "replace": "            settingsNewName = '';",
        "test": "手動追加の Tech が件数上限どおりに保存される",
    },
    {
        "name": "behavior: 2 つのルートが同じ title を名乗る — PAGE_META へエントリを足すとき既存をコピーして書き換え忘れると起きる。AI クローラや検索には『同じページが複数ある』と見え、AIO を中核に据えたこのサイトでは実害が大きい。しかも画面の内容は正しく変わるので **見た目には一切出ない**",
        "file": ROOT / "js" / "page-meta.js",
        "find": "    resume: { title: 'Resume',",
        "replace": "    resume: { title: 'About',",
        "test": "All routes expose a unique, non-empty title and description (AIO)",
    },
    {
        "name": "behavior: スナップショット復元が state を採用しなくなる — ボタンは押せてトーストも出るのに何も戻らない。スナップショットは単一スロットの『唯一の復元点』なので、効かないことに気付くのは戻したい場面 = 最悪のタイミングになる",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            State.set(Store.validateAndNormalize(snap.data));",
        "replace": "            void snap;",
        "test": "Settings snapshot restore reverts state to the saved point",
    },
    {
        "name": "behavior: Storage.parse の try/catch が外れる — localStorage が壊れた JSON を持っていると起動時に throw し、**サイトが真っ白で何もできない**最悪の壊れ方になる。localStorage は devtools でも別バージョンでも拡張機能でも書き換わりうる『アプリが最初に読む外部入力』",
        "file": ROOT / "js" / "storage.js",
        "find": "        try {\n            return JSON.parse(data);\n        } catch {\n            return null;\n        }",
        "replace": "        return JSON.parse(data);",
        "test": "localStorage がどんな形で壊れていても既定 store で起動する",
    },
    {
        "name": "behavior: upsert import が新規 project を取り込まなくなる (#192 の回帰) — 既存 id の更新だけが効き、未知 id は黙って捨てられる。取り込んだつもりのプロジェクトが 1 件も増えないのに成功メッセージは出る",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                            parsed.projects.forEach(p => map.set(p.id, p));\n",
        "replace": "",
        "test": "Settings JSON import (upsert) adds a new project and preserves profile fields (round-trip)",
    },
    {
        "name": "behavior: strict import が置換しなくなる — 『全置換』を選んだのに現状のまま。モード選択が効かないので、利用者は取り込んだ内容が反映されない理由を特定できない",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                            merged.projects = parsed.projects;",
        "replace": "                            merged.projects = base.projects;",
        "test": "Settings strict import replaces user-added layer but preserves defaults",
    },
    {
        "name": "behavior: タスク削除が何も消さなくなる — 削除ボタンは押せてトーストも出るのにカードが残る。利用者からは『押しても効かない』としか見えない",
        "file": ROOT / "js" / "apps.js",
        "find": "                s.appsData.tasks = s.appsData.tasks.filter(t => t.id !== id);",
        "replace": "                void id;",
        "test": "Task can be deleted from the board",
    },
    {
        "name": "behavior: 詳細ページの未入力 placeholder が失われる — 手動追加のプロジェクトは problem/approach/tech が空なので、**見出しだけで中身が無いセクション**が並ぶ。自分で追加したものを開くのはこのアプリを試す人が最初にやることなので印象面でも実害がある",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "project.problem || '(未登録)'",
        "replace": "project.problem",
        "test": "手動追加したプロジェクトの詳細に空の見出しが残らない",
    },
    {
        "name": "a11y: ポモドーロのモードボタンが選択状態を露出しなくなる — aria-pressed が常に false だと、支援技術の利用者には **今どのモードなのかが分からない**。視覚的には色で分かるので目視では気付けない (WCAG 4.1.2)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "                                    'aria-pressed': String(pomo.runtime.mode === m.id),",
        "replace": "                                    'aria-pressed': 'false',",
        "test": "Pomodoro mode buttons expose selected state via aria-pressed",
    },
    {
        "name": "a11y: 残り時間が role=timer でなくなる — role=status だと更新のたびに読み上げが割り込む (毎秒)。timer は『時間の表示』として扱われ chatty にならない。視覚表示は同じなので目視では区別できない",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "                            role: 'timer',",
        "replace": "                            role: 'status',",
        "test": "Pomodoro countdown exposes role=timer with a contextual aria-label for screen readers",
    },
    {
        "name": "a11y: AI の応答完了がアナウンスされなくなる — 応答は非同期に履歴へ足されるだけなので、SR 利用者は **生成が終わったことに気付けない** (入力欄の再有効化は非 focus 要素では分からない・WCAG 4.1.3)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "                    announce('AI が応答しました');",
        "replace": "",
        "test": "AI response completion announces to the assertive aria-live region (WCAG 4.1.3)",
    },
    {
        "name": "a11y: ステークホルダー意見のリスト意味論が失われる — 1 問に 2〜3 人分の意見が並ぶのに listitem が無いと、SR 利用者は『意見が何件あるか』も『どこからどこまでが 1 人の発言か』も掴めず項目単位で移動もできない。視覚的には引用の体裁で区切りが分かるので目視では気付けず、axe にも該当ルールが無い",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "class: \"quiz-stakeholder-quote\", role: \"listitem\"",
        "replace": "class: \"quiz-stakeholder-quote\"",
        "test": "設計判断 quiz のステークホルダー意見がリストとして公開される",
    },
    {
        "name": "a11y: 記事シリーズのリスト意味論が失われる — 同じ形式の記事が 11 本並ぶのに listitem が無いと、SR 利用者は『何本あるか』も分からず項目単位で移動もできない。視覚的にはカードの体裁で区切りが分かるので目視では気付けず、axe にも該当ルールが無い",
        "file": ROOT / "js" / "home-page.js",
        "find": "h('div', { class: 'aio-article-card', role: 'listitem' },",
        "replace": "h('div', { class: 'aio-article-card' },",
        "test": "同質な項目の並びがリストとして公開される (記事シリーズ / Settings のプロジェクト行)",
    },
    {
        "name": "a11y: 役割分担表のセル内箇条書きからリスト意味論が失われる — 各セルに 3〜4 件並ぶのに listitem が無いと、SR 利用者は『このセルに何項目あるか』も項目の切れ目も掴めない。視覚的には ✦ の記号で分かるので目視では気付けず、axe にも該当ルールが無い",
        "file": ROOT / "js" / "pages.js",
        "find": "class: 'cell-bullet-row', role: 'listitem'\n                            },\n                                h('span', { class: 'text-bullet-human'",
        "replace": "class: 'cell-bullet-row'\n                            },\n                                h('span', { class: 'text-bullet-human'",
        "test": "役割分担表のセル内箇条書きがリストとして公開される",
    },
    {
        "name": "security: メールアドレスの検証が外れ mailto へパラメータを注入できる — profile は import で外部から来るので、細工した『バックアップ』を取り込んだ利用者が **『メールで相談する』を押しただけで攻撃者に BCC を送る**。`mailto:` は URL なので `?bcc=...` がそのまま効く",
        "file": ROOT / "js" / "store.js",
        "find": "                email: safeEmail(data.profile.email, store.profile.email),",
        "replace": "                email: safeStr(data.profile.email, store.profile.email, 254),",
        "test": "細工したメールアドレスが mailto へ注入されない",
    },
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
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。
_E2E_TAIL.append({
    "name": "\u4fdd\u5b58\u5931\u6557\u306e\u8b66\u544a\u304c\u5229\u7528\u8005\u306b\u5c4a\u304b\u306a\u304f\u306a\u308b \u2014\u2014 notifyStorageError() \u304b\u3089 Toast.show() \u3092\u843d\u3068\u3059\u3068 console.error \u3060\u3051\u304c\u6b8b\u308b\u3002\u305d\u308c\u306f\u958b\u767a\u8005\u5411\u3051\u306e\u4fe1\u53f7\u3067\u5229\u7528\u8005\u306b\u306f\u4e00\u5207\u898b\u3048\u305a\u3001\u300c\u4fdd\u5b58\u3067\u304d\u3066\u3044\u306a\u3044\u300d\u3068\u77e5\u3089\u306a\u3044\u307e\u307e\u30bf\u30d6\u3092\u9589\u3058\u305f\u5229\u7528\u8005\u306f\u4f5c\u696d\u3092\u4e38\u3054\u3068\u5931\u3046 (silent \u306a\u30c7\u30fc\u30bf\u640d\u5931)\u3002\u5f93\u6765\u306e quota \u30c6\u30b9\u30c8\u306f console.error \u3057\u304b\u898b\u3066\u304a\u3089\u305a\u3053\u306e\u9000\u5316\u3092\u7d20\u901a\u308a\u3055\u305b\u3066\u3044\u305f",
    "file": ROOT / "js" / "state.js",
    "find": "Toast.show('\u30b9\u30c8\u30ec\u30fc\u30b8\u4e0a\u9650\u306e\u305f\u3081\u4fdd\u5b58\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002\u4e0d\u8981\u306a\u30c7\u30fc\u30bf\u3092\u524a\u9664\u3057\u3066\u304f\u3060\u3055\u3044\u3002', 'error', 5000);",
    "replace": "/* mutated */",
    "test": "localStorage write quota is exceeded",
})

E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL


