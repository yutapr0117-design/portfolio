"""mutation_samples_archive3.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT

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
]
