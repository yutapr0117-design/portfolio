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
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。
MUTATIONS = MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
    {
        "name": "behavior: テーマ切替が入力途中のテキストを巻き添えにする回帰 — js/theme.js の cycle を updateSilently から State.update へ戻す → notify で全再描画 (#content を clear) が走り、未送信の入力が消える (実測: task 8 文字 → 0 / ai 6 文字 → 0)。テーマはページ内容と無関係な chrome 操作なので巻き添えにしてはならない (#258 / #684 と同じ全再描画回避の規律)",
        "file": ROOT / "js" / "theme.js",
        "find": "        State.updateSilently(s => s.theme = next);",
        "replace": "        State.update(s => s.theme = next);",
        # NOTE: 題名はテンプレートリテラル (`... on ${route}`) で 3 ルート分ループ生成される。
        #   Check 379/397 は静的セグメントを parse するので、**動的部分を含まない前半**を指定する
        #   (3 インスタンス全てが同じコード経路を検証するため、どれが落ちても捕捉として妥当)。
        "test": "Theme toggle does not discard in-flight input on",
    },
    {
        "name": "behavior: 既定プロジェクトの並べ替えが reload で失われる回帰 — mergeProjectsWithDefaults が incoming(保存済み)順の default を採らず、末尾補完だけにする旧実装へ戻す → settings の ↑↓ で既定プロジェクトを並べ替えても reload の normalize round-trip で定義順へ silent に戻る。画面表示順 = state.projects 順なので利用者の操作そのものが失われる。user 追加分は incoming 順で append され保持されるため **default だけが戻る非対称**で気付きにくい",
        "file": ROOT / "js" / "store.js",
        "find": "            merged.push(d ? ({ ...d, ...p, id: d.id }) : p);\n            mergedIds.add(p.id);",
        "replace": "            if (!d) { merged.push(p); mergedIds.add(p.id); }",
        "test": "Default-project reorder survives a reload (normalize round-trip)",
    },
    {
        "name": "behavior: 無効な ?cat= の正規化喪失 — projects-page.js の `cat` 妥当性チェックを外す → stale bookmark / 削除済みカテゴリの deep-link で <select> は option 不在ゆえ 'All' 表示なのにフィルタは無効値のまま = 「全カテゴリーと表示されているのに 0 件」の control↔content desync (#781 と同族)。既存テストは有効カテゴリの選択と URL 同期しか見ておらず未被覆だった",
        "file": ROOT / "js" / "projects-page.js",
        "find": "        if (cat !== 'All' && !categories.includes(cat)) { cat = 'All'; }",
        "replace": "        if (false) { cat = 'All'; }",
        "test": "An unknown ?cat= deep-link normalizes to All (no control-content desync)",
    },
    {
        "name": "behavior: Speakable が宣言するセレクタの実体喪失 — js/pages.js の role-split 表から id を rename → Speakable JSON-LD は `#role-split-table` を宣言し続けるのに要素が存在しなくなり、AI 音声アシスタント向けの機械向け宣言が実態と乖離する (#929 の WebMCP 幻セレクタと同 class)。視覚に一切出ないため screenshot も通常の behavior test も素通りする",
        "file": ROOT / "js" / "pages.js",
        "find": "id: 'role-split-table'",
        "replace": "id: 'role-split-table-RENAMED'",
        # NOTE: 題名はテンプレートリテラルでルート毎に生成される。Check 379/397 は静的セグメントを
        #   parse するので動的部分を含まない前半を指定する (3 インスタンスが走るが、role-split の
        #   1 件が落ちれば suite 全体が FAIL = 捕捉として妥当)。
        "test": "Speakable route selector resolves on",
    },
    {
        "name": "behavior: quiz title の own-key ガード喪失 (#926 の回帰) — page-meta.js の hasOwnProperty 検証を `map[type] ||` へ戻す → `?type=constructor` などプロトタイプ継承キーで **関数オブジェクトが返り** document.title が「function Object() { [native code] }」に化ける。title はタブ名・履歴・AI クローラが受け取る機械可読面で、視覚の主要部には出ないため screenshot でも気付けない",
        "file": ROOT / "js" / "page-meta.js",
        "find": "            return Object.prototype.hasOwnProperty.call(map, type) ? map[type] : 'Quiz';",
        "replace": "            return map[type] || 'Quiz';",
        "test": "Quiz document.title stays in the known-safe set for ?type=",
    },
    {
        "name": "behavior: agentic な描画完了信号の喪失 — main.js の data-ai-state を最終状態も loading:true のままにする → AI エージェントが「永遠に読み込み中」と誤解して待ち続ける。data-ai-state は {route, filter, loading} を公開する機械可読面で、route/filter は既存テストが見ていたが loading のライフサイクルは未被覆だった。視覚に一切出ないため screenshot も通常の behavior test も素通りする",
        "file": ROOT / "main.js",
        "find": "                    loading: false",
        "replace": "                    loading: true",
        "test": "data-ai-state exposes a true->false loading lifecycle per route",
    },
    {
        "name": "behavior: WebMCP の走査セレクタが実描画に解決しなくなる (#929 の再発) — main.js の [data-ai-role] を、リポジトリのどこにも描画されていない .role-split-item へ戻す → ツールは「現在の DOM 状態から抽出します」と謳いながら常に静的フォールバックを返す。WebMCP は実ブラウザに未実装で登録すらされないため、API を shim して execute() を実行する e2e が唯一の捕捉層",
        "file": ROOT / "main.js",
        "find": "document.querySelectorAll('[data-ai-role]')",
        "replace": "document.querySelectorAll('.role-split-item')",
        "test": "WebMCP tool extracts from the live DOM on its route and falls back off-route",
    },
    {
        "name": "behavior: home の in-page ジャンプが reduced-motion を無視する (#993 の回帰) — home-page.js の三項を `behavior: 'smooth'` へ戻す → reduce 環境でも no-preference と同一のアニメーション曲線で 1,000px 超スクロールする。CSS の reduce override は behavior 明示呼び出しには効かない (同じ実測で scrollTo(0,0) は reduce のとき即時＝CSS 側は正常に働いていた) ため、誤って「守られている」と読みやすい",
        "file": ROOT / "js" / "home-page.js",
        "find": "el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });",
        "replace": "el.scrollIntoView({ behavior: 'smooth' });",
        "test": "WCAG 2.3.3: reduced-motion では in-page ジャンプが即時になる",
    },
    {
        "name": "behavior: in-page ジャンプ後に focus が移らなくなる (#993 の回帰) — home-page.js の focus() を潰す → viewport だけが 1,000px 動き、移動先が見えないユーザーには何も起きず、キーボードユーザーの次の Tab は画面外へ去ったボタンから続く (WCAG 2.4.3)",
        "file": ROOT / "js" / "home-page.js",
        "find": "el.focus({ preventScroll: true });",
        "replace": "void 0;",
        "test": "WCAG 2.4.3: in-page ジャンプが移動先へ focus を移す",
    },
    {
        "name": "behavior: 再描画後の focus 復元機構が失われる (#994 の回帰) — main.js _renderCore の復元条件を潰す → change のたびコントロールが自分自身を DOM ごと消して focus が body へ落ちる。number input は ArrowUp の 1 回目で focus を失い 2 回目以降が効かない (値を 1 段しか動かせない = 実質キーボード操作不能)",
        "file": ROOT / "main.js",
        "find": "            if (_restoreFocusId && _focusWasLost) {",
        "replace": "            if (false && _restoreFocusId && _focusWasLost) {",
        "test": "WCAG 2.1.1: ポモドーロの設定を ArrowUp で連続操作できる",
    },
    {
        "name": "behavior: 再描画前の focus 控えが失われる (#994 の回帰・復元の対) — main.js _renderCore が clear の前に控える id を常に null にする → 復元条件は残るが鍵が無くなり、同じく focus が body へ落ちる。Todo の完了チェックは 1 件チェックするたび focus を失い、次の項目を Space で続けてチェックできない",
        "file": ROOT / "main.js",
        "find": "                ? _prevActive.id : null;",
        "replace": "                ? null : null;",
        "test": "WCAG 2.1.1: TODO の完了チェックを Space で連続操作できる",
    },
    {
        "name": "behavior: ポモドーロ開始ボタンの focus 復元 id が外れる (#995 の回帰) — 開始した瞬間に focus が body へ落ち、稼働中は毎秒再描画されるため復帰の機会も無く『開始したらキーボードでは止められない』状態になる",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "                                id: 'pomo-toggle',\n",
        "replace": "",
        "test": "WCAG 2.1.1: ポモドーロを開始した後もキーボードで一時停止できる",
    },
    {
        "name": "behavior: タスク移動ボタンの focus 復元 id が外れる (#995 の回帰) — ステータスを 1 段動かすたび focus が body へ落ち、backlog→進行中→done と続けて動かせない (毎回ドキュメント先頭から Tab し直しになる)",
        "file": ROOT / "js" / "apps.js",
        "find": "                                                id: 'task-move-next-' + task.id,\n",
        "replace": "",
        "test": "WCAG 2.1.1: タスクをキーボードだけで連続してステータス移動できる",
    },
    {
        "name": "behavior: 復元先が消えた時の #content 退避が失われる (#995 の回帰) — 削除ボタンは自分自身を消すので元の要素へ戻せない。退避が無いと focus は body に残り、続きの Tab がドキュメント先頭からやり直しになる",
        "file": ROOT / "main.js",
        "find": "                if (content && (!_now || _now === document.body || _now === document.documentElement)) {",
        "replace": "                if (false && content && (!_now || _now === document.body || _now === document.documentElement)) {",
        "test": "WCAG 2.1.1: 項目を削除しても focus が本文内に残る",
    },
    {
        "name": "behavior: プロジェクトのタグ絞り込みが focus を捨てる (#995 の回帰) — このボタンは grid 内に居るので renderGrid() が自分自身を消す。_renderCore の復元経路を通らない手動再描画ゆえ、個別の focus 移動が無いと body へ落ちる",
        "file": ROOT / "js" / "projects-page.js",
        "find": "                                            if (inputEl) { inputEl.focus({ preventScroll: true }); }",
        "replace": "                                            void 0;",
        "test": "WCAG 2.1.1: プロジェクトのタグ絞り込みは検索欄へ focus を移す",
    },
    {
        "name": "behavior: サイドバー nav の focus 復元 id が外れる (#997 の回帰) — _renderCore は #content だけでなく sidebar も毎回作り直すため、id が無いと同一ルート再描画のたびに nav の focus が body へ落ちる。ポモドーロ稼働中は毎秒再描画されるので、キーボード利用者はタイマーが動いている間サイドバーに focus を留めておけない",
        "file": ROOT / "js" / "components.js",
        "find": "                id: navId(item),\n",
        "replace": "",
        "test": "WCAG 2.1.1: ポモドーロ稼働中でもサイドバーに focus を留められる",
    },
    {
        "name": "behavior: sidebar と drawer の Lab 本体 id が再び衝突する (#997 の回帰) — drawer を開くと同一 id の要素が 2 つ DOM 上に存在し、sidebar 側トグルの aria-controls が drawer 側を指す (支援技術が視覚的に隠れた別グループへ着地する)。focus 復元も getElementById を鍵にするので復元先が別物になりうる",
        "file": ROOT / "js" / "components.js",
        "find": "        const labBodyId = isDrawer ? 'drawer-nav-lab-body' : 'nav-lab-body';",
        "replace": "        const labBodyId = 'nav-lab-body';",
        "test": "sidebar と drawer の nav が id を衝突させない",
    },
    {
        "name": "behavior: Lab トグルがハードコード id を掴む (#997 の回帰) — 自分の aria-controls を辿らずに getElementById('nav-lab-body') すると、sidebar と drawer が同時に存在する mobile で相手側の本体を開閉する。どちらが動くかが構築順という偶然に委ねられる",
        "file": ROOT / "js" / "components.js",
        "find": "                    const body = document.getElementById(e.currentTarget.getAttribute('aria-controls'));",
        "replace": "                    const body = document.getElementById('nav-lab-body');",
        "test": "drawer の Lab トグルは drawer 側の本体だけを開閉する",
    },
    {
        "name": "behavior: 履歴移動で drawer が開いたまま残る (#998 の回帰) — drawer 内 nav リンク以外の経路でルートが変わると drawer が閉じず、背後のページだけが切り替わって #app は inert / body は scroll lock のまま残る。Android の戻るボタンは『開いているモーダルを閉じる』操作として使われるのに、実際には見えない場所でページが遷移する",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "    window.addEventListener('hashchange', () => { closeDrawer(); });",
        "replace": "    void 0;",
        "test": "drawer 開放中にブラウザの戻るでルートが変わったら drawer が閉じる",
    },
    {
        "name": "behavior: 履歴移動で command palette が開いたまま残る (#999 の回帰・#998 の drawer 版と対) — _choose 以外の経路でルートが変わると palette が閉じず、背後のページだけが切り替わって #app は inert のまま残る。両者は同じ『モーダル』なので片方だけ直すと #947 と同じ非対称が残る",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        window.addEventListener('hashchange', () => { close(); });",
        "replace": "        void 0;",
        "test": "palette 開放中にブラウザの戻るでルートが変わったら palette が閉じる",
    },
    {
        "name": "behavior: close() の再入ガードが外れる (#999 の回帰) — hashchange に繋いだ結果、閉じている palette へも close() が走り、末尾の lastFocused.focus() がルート遷移のたびに過去の要素へ focus を引き戻す。生き残る要素 (#menuBtn 等) が lastFocused だと新ページ h1 への route-focus (#267) が毎回打ち消される",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        if (!isOpen()) { return; }\n        // 背景の inert を必ず解除する",
        "replace": "        // 背景の inert を必ず解除する",
        "test": "palette を一度使った後もルート遷移で新ページの見出しへ focus が移る",
    },
    {
        "name": "behavior: Settings 並べ替えボタンの focus 復元 id が外れる (#1000 の回帰) — 1 回押すたびに focus が外れ 2 回目以降が効かない。プロジェクトを何段も動かすのが本来の用途なので、実質キーボードでは使えなくなる",
        "file": ROOT / "js" / "settings-page.js",
        "find": "id: 'settings-move-down-' + p.id, ",
        "replace": "",
        "test": "WCAG 2.1.1: プロジェクトの並べ替えをキーボードで連続実行できる",
    },
    {
        "name": "behavior: 並べ替えの focus 復元鍵を p.id から idx へ戻す (#1000 の回帰) — 移動後にその位置へ来た **別のプロジェクト**のボタンへ focus が移り、続けて押すと違う行が動く (実測では往復して元の順序に戻った)。リスト項目の復元鍵は位置ではなく同一性で作れ",
        "file": ROOT / "js" / "settings-page.js",
        "find": "id: 'settings-move-down-' + p.id,",
        "replace": "id: 'settings-move-down-' + idx,",
        "test": "WCAG 2.1.1: プロジェクトの並べ替えをキーボードで連続実行できる",
    },
    {
        "name": "behavior: Settings 表示切替ボタンの focus 復元 id が外れる (#1000 の回帰) — 切り替えるたびに focus が body へ落ち、元に戻すのに毎回ドキュメント先頭から Tab し直しになる",
        "file": ROOT / "js" / "settings-page.js",
        "find": "id: 'settings-toggle-hidden-' + p.id, ",
        "replace": "",
        "test": "WCAG 2.1.1: 表示切替ボタンは押した後も focus が残る",
    },
    {
        "name": "behavior: 再描画後のキャレット復元が失われる (#1001 の回帰) — focus は id で戻るがキャレットは末尾へ飛ぶため、文章の途中を編集中に外部要因の再描画 (ポモドーロ完了) が起きると次に打った 1 文字が末尾へ着弾する。値もフォーカスも正しいので気付きにくい",
        "file": ROOT / "main.js",
        "find": "                    if (_restoreFocusSel && typeof _again.setSelectionRange === 'function') {",
        "replace": "                    if (false && _restoreFocusSel && typeof _again.setSelectionRange === 'function') {",
        "test": "Markdown ノート編集中の再描画でもキャレットが保たれる",
    },
    {
        "name": "behavior: @media print が丸ごと無効化される — 印刷時にナビ chrome が残り、暗色テーマのまま紙に出る。screenshot は screen media で撮るので到達せず、consistency は CSS の存在しか見ないため、この spec を書くまで捕捉層がゼロだった (#133/#134/#135 と同じ silent-critical class)",
        "file": ROOT / "style.css",
        "find": "        @media print {",
        "replace": "        @media print-disabled {",
        "test": "印刷時はナビ chrome が消え、本文が全幅で横あふれしない",
    },
    {
        "name": "behavior: 印刷時の外部リンク URL 併記が失われる — 紙にはクリックできる要素が無いので、リンク先が本文に出ていないと参照できない。視覚 (screen) には一切出ないため print emulation 以外では観測できない",
        "file": ROOT / "style.css",
        "find": '                content: " (" attr(href) ")";',
        "replace": '                content: "";',
        "test": "印刷時は外部リンクの URL が紙面に併記される",
    },
    {
        "name": "behavior: forced-colors (HCM) のフォーカスリング fallback が失われる — Chromium はブランド色を強制変換して rgba(5, 0, 73, 0.8) = **半透明**の暗い青を描く (実測)。HCM で最も困る『薄くて見えない』状態そのもの。Check 101 はブロックの存在を静的に強制するだけで効果は見ず、screenshot は通常モードで撮るので到達しない",
        "file": ROOT / "style.css",
        "find": "        @media (forced-colors: active) {",
        "replace": "        @media (forced-colors: nope) {",
        "test": "ハイコントラストモードでフォーカスリングが system color になる",
    },
    {
        "name": "behavior: prefers-contrast: more の token 上書きが失われる — 境界線と補助テキストが薄いグレーのまま残り、高コントラストを要求したユーザーに何も返さない。静的にも動的にも無被覆だった面",
        "file": ROOT / "style.css",
        "find": "        @media (prefers-contrast: more) {",
        "replace": "        @media (prefers-contrast: nope) {",
        "test": "高コントラスト設定で境界線と補助テキストが濃くなる",
    },
    {
        "name": "behavior: 詳細ページの not-found ガードが外れる — 開いている詳細ページの project が別画面 (Settings の削除 / 別タブ / import) から消える経路があり、無条件に dereference すると FatalPage になる。#93/#295/#561/#568 で繰り返した ingestion-crash の『参照側』版",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "        if (!project) {",
        "replace": "        if (false) {",
        "test": "開いている詳細ページのプロジェクトを削除しても FatalPage にならない",
    },
    {
        "name": "behavior: 読み物ページの節タイトルが見出し要素でなくなる (#1011 の回帰) — 4,000 文字・9 セクションの本文に見出しが H1 の 1 個だけになり、スクリーンリーダーの見出しジャンプで一切辿れない。axe は『長い本文に小見出しが無い』をルール化していないので a11y スキャンは緑のまま",
        "file": ROOT / "js" / "ai-knowhow-page.js",
        "find": "                h('h2', { class: 'text-head-lg' }, title)",
        "replace": "                h('span', { class: 'text-head-lg' }, title)",
        "test": "ai-knowhow の節タイトルが実際の見出し要素である",
    },
    {
        "name": "behavior: quiz の章題が見出し要素でなくなる (#1012 の回帰) — 本文 24,500 文字のページに見出しが H1 の 1 個だけになり、スクリーンリーダーの見出しジャンプで 7 章のどこにも飛べない。NOTE: `quiz-section-title` の行は file 内に 2 箇所あり (architecture quiz 用と既存問題集用)、**既定の aws quiz が通るのは後者**。1 行だけの find だと前者に当たって偽 PASS するので、直前の icon 行を含めて一意にしている (Check 420 の要求そのもの)",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"h2\", { class: \"quiz-section-title\" }, section));",
        "replace": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-title\" }, section));",
        "test": "quiz の章題が実際の見出し要素である",
    },
    {
        "name": "behavior: プロジェクト一覧のリスト意味論が失われる (#1013 の回帰) — 18 件の同列カードが SR に「リスト・18 項目」とアナウンスされなくなり、リスト単位のジャンプ操作も効かなくなる。視覚には一切出ないので screenshot でも通常の behavior test でも捕捉できない",
        "file": ROOT / "js" / "projects-page.js",
        "find": "            gridContainer.setAttribute('role', 'list');",
        "replace": "            void 0;",
        "test": "プロジェクト一覧がリストとしてアナウンスされる",
    },
    {
        "name": "behavior: アプリ一覧の listitem が失われる (#1013 の回帰) — role=list の中身が listitem でなくなり、項目数のアナウンスもリスト内移動も壊れる (axe の aria-required-children でも捕捉されうるが、こちらは項目数の一致まで見る)",
        "file": ROOT / "js" / "components.js",
        "find": "h('article', { class: 'card', role: 'listitem' },",
        "replace": "h('article', { class: 'card' },",
        "test": "アプリ一覧がリストとしてアナウンスされる",
    },
    {
        "name": "behavior: ポモドーロ設定ラベルの for 結線が失われる (#1014 の回帰) — ラベル文字をクリック/タップしても入力欄が活性化せず、タップ標的も入力欄だけに縮む。入力欄側に aria-label があるため **axe は緑のまま** (axe は『label 要素が孤立していること』をルール化していない)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": ", for: 'pomo-setting-long' }, '長休憩'),",
        "replace": " }, '長休憩'),",
        "test": "ポモドーロはラベル文字のクリックで入力欄が活性化する",
    },
    {
        "name": "behavior: Settings の checkbox グループ名が宙に浮いた label へ戻る (#1014 の回帰) — 「対象」は 3 つの checkbox をまとめるグループ名で、単一 control を指す for は使えない。label のままだとどの control にも結び付かず、グループとしての関連付けも失われる",
        "file": ROOT / "js" / "settings-page.js",
        "find": "h('span', { class: 'text-sm text-muted', id: 'settingsIncludeGroupLabel' }, '対象'),",
        "replace": "h('label', { class: 'text-sm text-muted' }, '対象'),",
        "test": "Settings に宙に浮いた label が無い",
    },
    {
        "name": "behavior: CSP 違反検出ゲートが機能するかの自己検証 (#1016) — index.html に `data:` スクリプトを注入して **本物の CSP 違反**を起こす。旧実装は『メッセージ全体に karte が含まれるか』で除外していたが、CSP 違反メッセージには違反した directive の全文が載り、この CSP は KARTE ホストを許可しているため **あらゆる違反が除外され gate が絶対に落ちない**状態だった。ブロック対象 URL のホスト名で判定する形へ是正済み",
        "file": ROOT / "index.html",
        "find": "</head>",
        "replace": "<script src=\"data:text/javascript,void 0\"></script>\n</head>",
        "test": "No Trusted Types or CSP violations in console",
    },
    {
        "name": "behavior: soft-404 の noindex が外れる — 存在しないルートが index 可能になり、AI/検索クローラが『中身の無いページ』を実在ページとして取り込む。視覚には一切出ないため screenshot でも通常の behavior test でも捕捉できない AIO 面",
        "file": ROOT / "js" / "meta-management.js",
        "find": "            robotsEl.setAttribute('content', 'noindex, nofollow');",
        "replace": "            robotsEl.setAttribute('content', 'index, follow');",
        "test": "Robots meta protects against soft-404",
    },
    {
        "name": "behavior: og:type のルート追従が失われる — article ルートでも og:type が website のまま残り、SNS/クローラが記事として解釈しなくなる。head の meta なので視覚ゲートは一切反応しない",
        "file": ROOT / "js" / "meta-management.js",
        "find": "        document.querySelector('meta[property=\"og:type\"]')?.setAttribute('content', ogType);",
        "replace": "        void ogType;",
        "test": "Article routes inject JSON-LD Article",
    },
    {
        "name": "behavior: ルート entity anchor から曖昧性排除の宣言が消える — 同名の学術研究者等との混同を防ぐ文が失われ、AIO の中核である『エンティティを正しく解釈させる』賭けが弱まる。sr-only なので視覚には出ない",
        "file": ROOT / "js" / "meta-management.js",
        "find": "            ' Not affiliated with any academic researcher.';",
        "replace": "            '';",
        "test": "Route entity anchor declares entity authority",
    },
    {
        "name": "behavior: 英語だけの行への lang=en 付与が失われる (#1020 の回帰) — html lang=ja の文書内で英語が日本語の音韻で読み上げられる (WCAG 3.1.2)。quiz だけで 49 箇所あり、うち 34 回は同じラベル。axe には該当ルールが無く (html-lang-valid は文書全体の lang しか見ない) 視覚にも出ないため、捕捉層は behavior test だけ",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "                                lang: langOfText(line)",
        "replace": "                                lang: undefined",
        "test": "quiz の英語だけの塊に lang=",
    },
    {
        "name": "behavior: 固定英語文字列の lang=en が外れる (#1021 の回帰) — html lang=ja の文書内で英語キャプションが日本語の音韻で読み上げられる。axe に該当ルールが無く視覚にも出ないため behavior test だけが捕捉層",
        "file": ROOT / "js" / "home-page.js",
        "find": "                                class: 'text-caption', lang: 'en'",
        "replace": "                                class: 'text-caption'",
        "test": "固定の英語文字列に lang=",
    },
    {
        "name": "behavior: data 由来テキストの lang 判定が外れる (#1022 の回帰) — profile.title のような利用者編集データは静的に言語を決められないため描画時に判定している。外れると html lang=ja の文書内で英語が日本語の音韻で読み上げられる (WCAG 3.1.2)",
        "file": ROOT / "js" / "components.js",
        "find": ", lang: langOfText(State.get().profile.title) }",
        "replace": " }",
        "test": "data 由来のテキストにも lang=",
    },
    {
        "name": "behavior: hiring-risk の問題集 CTA の query type が typo る (#1027) — route は存在するので Check 395 は緑のまま、実際には既定の AWS 問題集が silent に表示される (#926 の own-key ガードで crash はせず falls back するだけ)。採用担当が辿る導線で「PM 問題集を見る」が別の問題集を出す",
        "file": ROOT / "js" / "hiring-risk-page.js",
        "find": "path: 'quiz?type=pm',",
        "replace": "path: 'quiz?type=pmm',",
        "test": "hiring-risk の問題集 CTA が宣言どおりの問題集へ着地する",
    },
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
        "find": "            if (onPomodoroRoute) { State.update(applyCompletion); }\n            else { State.updateSilently(applyCompletion); }",
        "replace": "            State.update(applyCompletion);",
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
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。
E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL
