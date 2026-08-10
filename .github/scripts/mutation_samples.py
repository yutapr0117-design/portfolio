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
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。
MUTATIONS = MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
    {
        "name": "behavior: task move の done 境界 disabled affordance の喪失 — apps.js の「次のステータスへ進める」ボタン `disabled: task.status === 'done'` を false へ → done 列でも next が有効に見え「これ以上進めない」UX affordance が壊れる (moveStatus の clamp はデータを守るが disabled 属性は別レイヤーの affordance。backlog 境界と対称の done 境界被覆の非 vacuity 検証)",
        "file": ROOT / "js" / "apps.js",
        "find": "disabled: task.status === 'done',",
        "replace": "disabled: false,",
        "test": "disabled at the done boundary",
    },
    {
        "name": "behavior: pomodoro 集中時間 input の範囲外 clamp の喪失 — pomodoro-page.js work onchange の clamp(...,1,180) を外し生 parseInt へ → 999 分等の範囲外値がそのまま settings.work に入り不正 duration の timer になる (number input max=180 は programmatic/paste を防がず JS clamp が実防御。上限/下限境界の非 vacuity 検証)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "s.appsData.pomodoro.settings.work = clamp(parseInt(e.target.value, 10) || 25, 1, 180);",
        "replace": "s.appsData.pomodoro.settings.work = parseInt(e.target.value, 10) || 25;",
        "test": "clamps out-of-range values",
    },
    {
        "name": "behavior: pomodoro 短休憩 input の範囲外 clamp[1,60] の喪失 — pomodoro-page.js short onchange の clamp(...,1,60) を外し生 parseInt へ → 999 分等が settings.short に入り work とは別 range の境界が壊れる (#838 work とは独立の range・独立 regress の非 vacuity 検証)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "s.appsData.pomodoro.settings.short = clamp(parseInt(e.target.value, 10) || 5, 1, 60);",
        "replace": "s.appsData.pomodoro.settings.short = parseInt(e.target.value, 10) || 5;",
        "test": "short/long break inputs clamp",
    },
    {
        "name": "behavior: pomodoro 長休憩 input の範囲外 clamp[1,120] の喪失 — pomodoro-page.js long onchange の clamp(...,1,120) を外し生 parseInt へ → 999 分等が settings.long に入り short(60) とも別 range の上限 120 境界が壊れる (独立 regress の非 vacuity 検証)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "s.appsData.pomodoro.settings.long = clamp(parseInt(e.target.value, 10) || 15, 1, 120);",
        "replace": "s.appsData.pomodoro.settings.long = parseInt(e.target.value, 10) || 15;",
        "test": "short/long break inputs clamp",
    },
    {
        "name": "behavior: AI submit の空/空白プロンプトガードの喪失 — ai-page.js submit の `!input.trim() ||` を外し aiLoading のみ残す → 空文字/空白のみの送信が握り潰されず空の会話を ai.history に積み UI/localStorage を汚す (settings の空入力バリデーションは test 済だが AI 空プロンプトガードは未被覆だった穴の非 vacuity 検証)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "if (!input.trim() || aiLoading) {return;}",
        "replace": "if (aiLoading) {return;}",
        "test": "ignores empty and whitespace",
    },
    {
        "name": "behavior: task addTask の空/空白タイトルガードの喪失 — apps.js addTask の `if (!title.trim())` を常時 false 化 → 空文字/空白のみの Enter が空タイトル task を backlog に積む (AI #841 と同 class の入力バリデーションガード・task 面の非 vacuity 検証)",
        "file": ROOT / "js" / "apps.js",
        "find": "if (!title.trim()) {return;}",
        "replace": "if (false) {return;}",
        "test": "ignore empty/whitespace-only input",
    },
    {
        "name": "behavior: todo addTodo の空/空白テキストガードの喪失 — apps.js addTodo の `if (!text.trim())` を常時 false 化 → 空文字/空白のみの Enter が空テキスト todo を積む (task addTask とは別 function・独立 regress の非 vacuity 検証)",
        "file": ROOT / "js" / "apps.js",
        "find": "if (!text.trim()) {return;}",
        "replace": "if (false) {return;}",
        "test": "ignore empty/whitespace-only input",
    },
    {
        "name": "behavior: snapshot 復元ボタンの未保存時 disabled affordance の喪失 — settings-page.js の 復元ボタン `disabled: !snap` を除去 → snapshot 未保存でも復元ボタンが有効に見え「復元するものが無い」affordance が壊れる (restoreSnapshot は no-op guard 済だが disabled 属性は別レイヤーの UX affordance。#836 task done 境界と同 class・snapshot 面の非 vacuity 検証)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "onclick: restoreSnapshot, disabled: !snap",
        "replace": "onclick: restoreSnapshot",
        "test": "disabled until a snapshot exists",
    },
    {
        "name": "behavior: router の unknown-app whitelist else 分岐の喪失 — router.js の `apps/<app>` で whitelist 外を 'not-found' にする else を 'app-task' へ → 存在しない app サブルート (apps/nonexistent) が task ページを描画し NotFound に落ちない (top-level unknown route とは別 code path の非 vacuity 検証)",
        "file": ROOT / "js" / "router.js",
        "find": ": 'not-found';",
        "replace": ": 'app-task';",
        "test": "Unknown app subroute",
    },
    {
        "name": "behavior: profile email の ingestion 文字列長 bound の喪失 — store.js normalize の email `.slice(0, 254)` を除去 → 巨大 email が truncate されず href/表示に載り localStorage/DOM を bloat させる (AI history 文字列 bound #230 / MAX_TASKS 件数 bound #801 と同じ ingestion bloat-guard class・profile email 面の非 vacuity 検証)",
        "file": ROOT / "js" / "store.js",
        "find": "email: safeStr(data.profile.email, store.profile.email, 254),",
        "replace": "email: safeStr(data.profile.email, store.profile.email, 1e9),",
        "test": "email is length-bounded",
    },
    {
        "name": "behavior: 同名プロジェクト追加時の slug 一意化 (#154) の喪失 — settings-page.js addProjectManual の `while (existing.has(slug))` を while(false) へ → 同名 2 件が同一 slug になり ProjectDetailPage の find(p.slug===slug) が先頭のみ返して片方の詳細が到達不能になる実バグ regression (既存の unique-slugs test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "while (existing.has(slug)) {",
        "replace": "while (false) {",
        "test": "same name yields unique slugs",
    },
    {
        "name": "behavior: profile github/linkedin の URL スキームサニタイズ (#139 XSS) の喪失 — store.js safeUrl の http(s) スキームチェックを外し raw 値をそのまま返す → import した javascript:/data: 等の危険スキーム URL が ContactPage の href に載り XSS ベクタになる (既存 URL-sanitized test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証)",
        "file": ROOT / "js" / "store.js",
        "find": "return /^https?:\\/\\//i.test(s) ? s.slice(0, 500) : String(fallback || '');",
        "replace": "return s;",
        "test": "URL-sanitized",
    },
    {
        "name": "behavior: pomodoro getDuration の live-state 参照 (#134) の喪失 — pomodoro-page.js getDuration の `State.get()...settings` を render 毎キャプチャの stale closure `pomo.settings` へ戻す → 稼働中に集中時間を変えても complete() の remainingSec リセットが旧設定値を使う (getRemaining #121 と同根の stale-closure バグ。既存 mid-run test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "const settings = State.get().appsData.pomodoro.settings;",
        "replace": "const settings = pomo.settings;",
        "test": "completion uses the latest focus-duration",
    },
    {
        "name": "behavior: AI 入力の IME composition ガード (#152) の喪失 — ai-page.js の Enter ハンドラから `&& !e.isComposing` を外す → 日本語入力で IME 変換確定の Enter が未確定テキストを誤 submit する (task IME #299 とは別 function・ai-input 独立の実バグ。日本語が主対象の本サイトで既存 test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "if (e.key === 'Enter' && !e.isComposing) {",
        "replace": "if (e.key === 'Enter') {",
        "test": "AI input ignores Enter during IME composition",
    },
    {
        "name": "behavior: TODO 入力の IME composition ガード (todoComposing flag) の喪失 — apps.js todo の Enter ハンドラから `&& !todoComposing` を外す → 日本語 IME 変換確定 Enter が未確定テキストを誤 submit する。task(e.isComposing)/ai(e.isComposing) とは異なり todo は手動 compositionstart/end フラグ機構ゆえ独立 regress しうる。既存 test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "apps.js",
        "find": "if (e.key === 'Enter' && !todoComposing) {",
        "replace": "if (e.key === 'Enter') {",
        "test": "Todo input ignores Enter during IME composition",
    },
    {
        "name": "behavior: quiz 検索 live-input の focus-loss guard (#258) の喪失 — quiz-renderer.js の oninput を updateSilently から State.update へ戻す → 全再描画で input が破棄され 1 文字ごとに focus を失い検索が使えなくなる実バグ。既存 focus-regression test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証 (Check 130 の静的封じと behavior 面の二層)",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "State.updateSilently(s => { s.appsData.quizSearch = val; s.appsData.quizSearchType = quizType; });",
        "replace": "State.update(s => { s.appsData.quizSearch = val; s.appsData.quizSearchType = quizType; });",
        "test": "Quiz search input retains focus",
    },
    {
        "name": "behavior: projects 検索 live-input の focus-loss guard (#258) の喪失 — projects-page.js の oninput を部分更新 renderGrid() から全再描画 window.render() へ戻す → #content が作り直され検索 input が破棄されて 1 文字ごとに focus を失い検索使用不能になる実バグ。既存 focus-regression test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証 (quiz #258 と同 class・別 surface)",
        "file": ROOT / "js" / "projects-page.js",
        "find": "renderGrid(); // 部分更新でフォーカスを死守",
        "replace": "window.render();",
        "test": "retains focus during filtering",
    },
    {
        "name": "behavior: command-palette close 時の opener への focus 復元 (#700 WCAG 2.4.3) の喪失 — command-palette.js close() の lastFocused.focus() を除去 → palette を閉じても起動元へ focus が戻らず SR/キーボード利用者が文脈を失う a11y 退行。既存 focus-restore test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "command-palette.js",
        "find": "            try { lastFocused.focus({ preventScroll: true }); } catch (e) { /* noop */ }",
        "replace": "            try { /* focus removed */ } catch (e) { /* noop */ }",
        "test": "restores focus to the opener on close",
    },
    {
        "name": "behavior: ProjectsPage の無効 ?cat= 正規化 (control↔filter desync guard) の喪失 — projects-page.js の `cat = 'All'` 再代入を除去 → 無効 URL query cat が正規化されず、<select> は option 不在で 'All' 表示なのに filter は無効値で 0 件 = 「All なのに空」desync が復活 (#93/#295 と同族の外部入力 validate discipline)。既存 desync-guard test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "projects-page.js",
        "find": "if (cat !== 'All' && !categories.includes(cat)) { cat = 'All'; }",
        "replace": "if (cat !== 'All' && !categories.includes(cat)) { /* normalize removed */ }",
        "test": "normalizes an invalid ?cat= to All",
    },
    {
        "name": "behavior: skip-link の native-nav 抑止 (#779 WCAG 2.4.1) の喪失 — main.js skip-link click ハンドラの e.preventDefault() を除去 → native fragment 挙動で location.hash が '#main-content' に変わり router が非-'#/' hash を home 扱いで再描画 → 非 home ページ(#/projects)で「本文へスキップ」がユーザーを home へ誤遷移させる実バグ復活。main.js に preventDefault は 1 個(skip-link 専用)。既存 skip-link test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "main.js",
        "find": "e.preventDefault();",
        "replace": "/* preventDefault removed (#779 skip-link native-nav regression) */",
        "test": "Skip link moves focus to #main-content",
    },
    {
        "name": "behavior: quiz architecture 検索の stakeholder 被覆 (#285 visible-but-unsearchable) の喪失 — quiz-renderer.js _filterBy の return から `|| stakeholderMatch` を除去 → 画面に描画される stakeholder の name/quote (例 CTO の GAFA 発言) が検索対象外に戻り「見えるのに 0 件」drift が復活。既存 stakeholder-search test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "return titleMatch || idMatch || contentMatch || situationMatch || questionMatch || stakeholderMatch;",
        "replace": "return titleMatch || idMatch || contentMatch || situationMatch || questionMatch;",
        "test": "matches stakeholder quote text",
    },
    {
        "name": "behavior: cross-tab storage 取り込みの schema guard (#295/#93) の喪失 — state.js storage リスナーの `if (incoming.schemaVersion !== SCHEMA_VERSION) return` を除去 → デプロイ跨ぎ (別バージョン) の異 schema / 欠損 store が別タブから来ると採用見送りされず validateAndNormalize を通って現タブの正常 state を上書き → own task 消失 (欠損時は FatalPage crash もありうる #93 class)。既存 foreign-schema-ignore test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "state.js",
        "find": "if (incoming.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {return;}",
        "replace": "/* cross-tab schema guard removed (#295) */",
        "test": "foreign-schema/malformed store",
    },
    {
        "name": "behavior: quiz 検索の section 章タイトル被覆 (#296 visible-but-unsearchable) の喪失 — quiz-renderer.js _filterBy の `sectionMatch = !query || section.includes(query)` から section 一致項を除去 → 画面描画される section 章タイトル (例「第4章：可用性とFinOps…」) が検索対象外に戻り、タイトルにのみ含まれる語 (FinOps) で「見えるのに 0 件」drift が復活。既存 section-header-search test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "const sectionMatch = !query || section.toLowerCase().includes(query);",
        "replace": "const sectionMatch = !query;",
        "test": "section-header (chapter title)",
    },
    {
        "name": "behavior: drawer の desktop リサイズ stuck-state guard の喪失 — mobile-drawer.js syncMobileDrawer の !isMobile 分岐で開放中 drawer を閉じる条件を無効化 → drawer 開放中に mobile→desktop へリサイズすると inline display:block が media query に勝って drawer/overlay が残り、__setAppInert(true)+__lockBodyScroll(true) のまま app が inert・scroll lock された stuck 状態 (topbar=display:none で menuBtn も隠れ overlay/Escape でしか脱出不能な broken UX) が復活。既存 stuck-state-guard test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "if (drawer && drawer.getAttribute('aria-hidden') === 'false') {",
        "replace": "if (false && drawer && drawer.getAttribute('aria-hidden') === 'false') {",
        "test": "resize to desktop",
    },
    {
        "name": "behavior: snapshot restore の正規化 (#561/#93/#295) の喪失 — settings-page.js restoreSnapshot の `State.set(Store.validateAndNormalize(snap.data))` を生 `State.set(snap.data)` に戻す → 旧版が保存した schema 不一致/projects・appsData 欠落 snapshot を復元すると renderer が state.projects.map 等で未定義参照し FatalPage crash (外部入力 ingestion は全て正規化を通せ class・importJSON は通すのに restore だけ生採用していた未被覆経路)。既存 snapshot-restore-normalize test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "settings-page.js",
        "find": "State.set(Store.validateAndNormalize(snap.data));",
        "replace": "State.set(snap.data);",
        "test": "Snapshot restore normalizes a foreign-schema/partial snapshot",
    },
    {
        "name": "behavior: store.js の非配列 ai.history ingestion guard (#568/#93) の喪失 — normalizeAppsData の `if (Array.isArray(data.ai?.history))` を旧 truthy 判定 `if (data.ai?.history)` に戻す → 別 schema/破損 store が ai.history を非配列 (文字列等) で持つと `.filter` が TypeError → validateAndNormalize 例外 → load()/cross-tab/import/snapshot-restore の全 ingestion 経路が FatalPage crash (normalizeAppsData の総関数契約違反)。既存 non-array-history-tolerance test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": "if (Array.isArray(data.ai?.history)) {",
        "replace": "if (data.ai?.history) {",
        "test": "tolerates a non-array ai/pomodoro history",
    },
    {
        "name": "behavior: pomodoro 短休憩 onchange の idle 表示即更新 (#692 work との対称性) の喪失 — pomodoro-page.js short-break onchange の `remainingSec = settings.short * 60` を除去 → 短休憩モードで idle 中に短休憩時間を変えても表示中の remainingSec が古い duration のまま (start すると旧設定長で始まる)。従来 work だけこの即更新があり short/long は欠落していた asymmetry 実バグ。既存 break-symmetry test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "s.appsData.pomodoro.runtime.remainingSec = s.appsData.pomodoro.settings.short * 60;",
        "replace": "/* #692 short-break symmetry update removed */",
        "test": "break-duration change updates the idle timer",
    },
    {
        "name": "behavior: store.js の ingestion 側 ai.history prompt 文字列 bound (#230 class) の喪失 — normalizeAppsData の `prompt: String(h.prompt).slice(0, CONSTANTS.LIMITS.AI_MESSAGE)` から `.slice(0, AI_MESSAGE)` を外し生 `String(h.prompt)` に戻す → 巨大 prompt (20000 字) を含む store を load/import/cross-tab で取り込むと prompt が切り詰められず localStorage を bloat させる (write 側 apps.js は AI_MESSAGE で bound 済だが ingestion 側正規化が個々文字列長を bound しない未閉じ枝)。既存 length-bounded-on-normalize test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": "prompt: String(h.prompt).slice(0, CONSTANTS.LIMITS.AI_MESSAGE),",
        "replace": "prompt: String(h.prompt),",
        "test": "AI history strings are length-bounded on normalize ingestion",
    },
    {
        "name": "behavior: drawer overlay(背景)クリック close の喪失 — main.js init の `#overlay` click→closeDrawer 直接リスナー配線を no-op function に差し替え → モバイルドロワーを開いたまま背景 overlay をクリックしても閉じない (モーダル標準の backdrop dismiss が壊れる)。Escape/nav-link close は別経路ゆえ独立に regress しうる。既存 overlay-backdrop-click test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "main.js",
        "find": "document.getElementById('overlay')?.addEventListener('click', closeDrawer);",
        "replace": "document.getElementById('overlay')?.addEventListener('click', function () {});",
        "test": "Mobile drawer closes on overlay (backdrop) click",
    },
    {
        "name": "behavior: relatedProjectIds 要素の String 正規化 (#782 id-coercion) の喪失 — store.js normalizeProject の `relatedProjectIds: (...).filter(Boolean).map(String).slice(0, 20)` から `.map(String)` を外す → import データが数値 id の relatedProjectIds を持つと、normalizeProject が id 自体は `String(raw.id)` で文字列化する一方 relatedProjectIds 要素は数値のまま残り、ProjectDetailPage の `relatedProjectIds.includes(p.id)` (p.id=文字列) と strict 不一致 → 関連プロジェクトリンクが silent に消える (#93/#295 の外部 ingestion 全経路正規化 class の relatedProjectIds 版)。既存 numeric-relatedProjectIds test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": "relatedProjectIds: (Array.isArray(raw.relatedProjectIds) ? raw.relatedProjectIds : []).filter(Boolean).map(String).slice(0, 20),",
        "replace": "relatedProjectIds: (Array.isArray(raw.relatedProjectIds) ? raw.relatedProjectIds : []).filter(Boolean).slice(0, 20),",
        "test": "Imported numeric relatedProjectIds resolve to string ids",
    },
    {
        "name": "behavior: pomodoro reload auto-resume (#121 frozen-timer guard) の喪失 — pomodoro-page.js の `if (isActive && !pomodoroTimer) { startTimer(); }` 条件を `false && ...` で無効化 → reload 後に isActive=true (endAtMs>now を normalize が保持) でも interval が再起動されず、「一時停止ボタン表示だが countdown が frozen で complete() が永遠に発火しない」stuck 状態が復活 (pomodoroTimer は factory 変数ゆえ reload で null に戻り start() ボタン経由でしか起動されなかった元バグ)。既存 frozen-timer-guard test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "if (isActive && !pomodoroTimer) {",
        "replace": "if (false && isActive && !pomodoroTimer) {",
        "test": "resumes ticking after a reload mid-run",
    },
    {
        "name": "behavior: settings のプロジェクト並べ替え (moveProject up/down) の喪失 — settings-page.js moveProject の境界ガード `if (idx + dir < 0 || idx + dir >= s.projects.length) {return;}` を `if (true || ...)` で常に return させ swap を無効化 → ↑↓ ボタンを押しても順序が変わらず、並べ替えが localStorage に反映されない (State.update の swap が dead になる)。既存 reorder test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "settings-page.js",
        "find": "if (idx + dir < 0 || idx + dir >= s.projects.length) {return;}",
        "replace": "if (true || idx + dir < 0 || idx + dir >= s.projects.length) {return;}",
        "test": "Projects can be reordered with the up/down controls",
    },
    {
        "name": "behavior: default プロジェクト並べ替えの reload 永続 (mergeProjectsWithDefaults 順序保持) の喪失 — store.js の incoming 順優先 merge を default 定義順優先へ戻す (`for (const p of normalizedIncoming)` ループを `for (const d of normalizedDefaults)` へ) → settings ↑↓ で default project 同士を並べ替えても reload の normalize round-trip で元の定義順へ silent に戻る data-fidelity バグが復活 (user 追加 project は incoming 順 append で保持されるため default だけが失われる)。回帰 e2e に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": "        // 1. incoming(保存済み)順を保持 — default field は id で backfill し incoming の値を優先。\n        for (const p of normalizedIncoming) {\n            const d = defaultsById.get(p.id);\n            merged.push(d ? ({ ...d, ...p, id: d.id }) : p);\n            mergedIds.add(p.id);\n        }",
        "replace": "        // MUTATION: revert to default-definition order (drops reorder persistence).\n        for (const d of normalizedDefaults) {\n            const p = normalizedIncoming.find(x => x.id === d.id);\n            merged.push(p ? ({ ...d, ...p, id: d.id }) : d);\n            mergedIds.add(d.id);\n        }",
        "test": "Default project reorder persists across reload",
    },
    {
        "name": "behavior: TODO の「完了をクリア」ボタンの affordance ガード (disabled until a todo is completed) の喪失 — apps.js TodoPage の `disabled: !todos.some(t => t.completed)` を `disabled: false` にし常時活性化 → 完了 todo が 1 件も無い状態でもボタンが押せてしまい、空 filter 操作 (実質 no-op だが誤操作導線) を許す affordance 契約の喪失。既存 clear-completed-disabled test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "apps.js",
        "find": "disabled: !todos.some(t => t.completed),",
        "replace": "disabled: false,",
        "test": "Todo clear-completed button is disabled until a todo is completed",
    },
    {
        "name": "behavior: task カンバンの status 遷移 (moveStatus) の喪失 — apps.js moveStatus の `updateTask(task.id, { status: statuses[newIdx] })` を `statuses[idx]` に変え遷移先を現在 status に固定 → ←/→ ボタンを押してもカードが列を移動せず status が変わらない (backlog→in-progress→done の遷移が dead)。既存 kanban-move-persist test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "apps.js",
        "find": "updateTask(task.id, { status: statuses[newIdx] });",
        "replace": "updateTask(task.id, { status: statuses[idx] });",
        "test": "moves across kanban columns and persists the status",
    },
    {
        "name": "behavior: task の優先度フィルタ (getFilteredTasks) の喪失 — apps.js の `taskFilter.priority === 'all' || t.priority === taskFilter.priority` を `true` に変え全タスクを常に通す → 優先度フィルタを high/low に絞ってもボードが絞り込まれず全件表示のまま (フィルタが no-op 化)。既存 priority-filter-narrows test に対応する mutation が未登録だった safety-net 補強の非 vacuity 検証",
        "file": ROOT / "js" / "apps.js",
        "find": "taskFilter.priority === 'all' || t.priority === taskFilter.priority",
        "replace": "true",
        "test": "priority filter narrows the board by priority",
    },
    {
        "name": "behavior: pomodoro 完了時の history エントリの session type 記録の喪失 — pomodoro-page.js complete() の history push で `type: s.appsData.pomodoro.runtime.mode` を固定リテラル `type: 'break'` に変え、記録される session type が実 mode を反映しなくなる → 完了した work セッションが 'break' として履歴に残り、集計/表示が誤る。新設 completion-history-record test に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "type: s.appsData.pomodoro.runtime.mode,",
        "replace": "type: 'break',",
        "test": "records a history entry with the session type and duration",
    },
    {
        "name": "behavior: projectPrefs.hiddenIds の normalize round-trip 保持の喪失 — store.js validateAndNormalize の projectPrefs 読み戻しガード `if (data.projectPrefs && ... Array.isArray(data.projectPrefs.hiddenIds))` を `if (false && ...)` で無効化 → reload の normalize で hiddenIds が drop され、非表示にしたプロジェクトが公開一覧へ silent に復活する (#294/#568/#684/#871 の persist-drift class の projectPrefs 版)。新設 hidden-persist test に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": "if (data.projectPrefs && typeof data.projectPrefs === 'object' && Array.isArray(data.projectPrefs.hiddenIds)) {",
        "replace": "if (false && data.projectPrefs && typeof data.projectPrefs === 'object' && Array.isArray(data.projectPrefs.hiddenIds)) {",
        "test": "Hidden project stays hidden on the public list across reload",
    },
    {
        "name": "a11y: ProjectsPage の検索 landmark (role='search') の喪失 — projects-page.js の検索 wrapper から `role: 'search'` を外す → 検索入力が ARIA search landmark でなくなり、SR ユーザーが landmark ナビゲーションで検索領域へジャンプできなくなる (WCAG 1.3.1・ARIA APG search landmark の退行)。新設 search-landmark test に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "projects-page.js",
        "find": "h('div', { class: 'relative', role: 'search' },",
        "replace": "h('div', { class: 'relative' },",
        "test": "Projects search is exposed as an ARIA search landmark",
    },
    {
        "name": "a11y: QuizPage の検索 landmark (role='search') の喪失 — quiz-renderer.js の検索 wrapper から `role: \"search\"` を外す → 検索入力が ARIA search landmark でなくなり SR ユーザーが landmark ナビで検索領域へジャンプできなくなる (WCAG 1.3.1・ARIA APG・ProjectsPage #879 と同型)。新設 quiz-search-landmark test に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "h(\"div\", { class: \"relative\", role: \"search\" },",
        "replace": "h(\"div\", { class: \"relative\" },",
        "test": "Quiz search is exposed as an ARIA search landmark",
    },
    {
        "name": "a11y: ProjectsPage 件数表示の live region (WCAG 4.1.3) の喪失 — projects-page.js の countDisplay から `role: 'status', 'aria-live': 'polite'` を外す → 検索/カテゴリ絞り込みで `合計 N 件` が変わっても SR ユーザーへ通知されなくなる (非 0 件の件数変化が silent に戻る Status Messages 退行)。新設 count-live-region test に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "projects-page.js",
        "find": "countDisplay = h('p', { class: 'text-muted', role: 'status', 'aria-live': 'polite' }, '')",
        "replace": "countDisplay = h('p', { class: 'text-muted' }, '')",
        "test": "Projects result count is an aria-live status region",
    },
    {
        "name": "a11y: quiz 模範解答フォームの email 必須マーク (WCAG 3.3.2) の喪失 — quiz-renderer.js emailInput の `'aria-required': 'true'` を外す → submit の JS バリデーションで必須の メールアドレスが SR ユーザーに必須と露出されず、送信してエラー Toast が出るまで必須と分からない (Labels or Instructions の退行)。新設 form-required test に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "'aria-label': 'メールアドレス', 'aria-required': 'true' }",
        "replace": "'aria-label': 'メールアドレス' }",
        "test": "Quiz contact form marks name and email as aria-required",
    },
    {
        "name": "behavior: 自動推薦の明示-related 除外の喪失 — store.js autoRelatedCandidates の候補 filter から `&& !fixed.has(p.id)` を外す → target.relatedProjectIds に既にある明示 related が推薦候補へ戻り、プロジェクト詳細の「関連プロジェクト」節と「おすすめ（自動）」節に同じプロジェクトが二重表示される (推薦枠 8 件が既知の関連で埋まり新規発見価値が失われる)。新設 auto-recommendation exclusion test に対応する mutation で safety-net を institutionalize する非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": ".filter(p => p && p.id && p.id !== target.id && !fixed.has(p.id))",
        "replace": ".filter(p => p && p.id && p.id !== target.id)",
        "test": "Auto-recommendations exclude self and explicitly-related projects",
    },
    {
        "name": "behavior: hidden project が home の注目枠へ漏れる — home-page.js の featured 選定を visibleProjects から素の state.projects へ戻す → 非表示にした default project (削除不可＝非表示が唯一の非公開手段) がトップページ最上位の注目枠に出続け、詳細/デモ導線も残る (公開一覧からは消えているため owner は気づけない listing 面 mesh の漏れ)",
        "file": ROOT / "js" / "home-page.js",
        "find": "const featured = visibleProjects.find(p => p.demoRoute === 'task') || visibleProjects[0] || null;",
        "replace": "const featured = state.projects.find(p => p.demoRoute === 'task') || state.projects[0] || null;",
        "test": "Hidden project disappears from home featured",
    },
    {
        "name": "behavior: hidden project が詳細ページの推薦へ漏れる — project-detail-page.js の related 算出を listable(非表示除外済) から素の state.projects へ戻す → 非表示にしたプロジェクトが「関連プロジェクト」カードとして出続け、そこから詳細ページへ到達できる (listing 面 mesh の漏れ)",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "const related = listable.filter(p =>",
        "replace": "const related = state.projects.filter(p =>",
        "test": "Hidden project disappears from home featured",
    },
    {
        "name": "behavior: hidden project が Cmd+K 候補へ漏れる — command-palette.js の候補 filter から `&& !_hidden.has(String(p.id))` を落とす → 公開一覧から消したプロジェクトが palette で検索・到達でき、非表示が「一覧だけの部分的な隠蔽」に退行する (listing 面 mesh の漏れ)",
        "file": ROOT / "js" / "command-palette.js",
        "find": " && !_hidden.has(String(p.id))",
        "replace": "",
        "test": "Hidden project disappears from home featured",
    },
    {
        "name": "behavior: hiring-risk CTA が AWS フォールバックへ着地 — quiz-renderer.js の QUIZ_DATA_MAP から 'pm' キーを rename → URL は #/quiz?type=pm のままなのに `|| QUIZ_DATA_MAP.aws` が効き、「PM問題集を見る」ボタンから AWS 問題集が黙って描画される silent wrong-content (throw も console error も無く、直接 URL で開く既存 quiz e2e も CTA 経路を通らないため素通りする)。Check 401a が静的に守る面の behavioral 対",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "            pm: { title: 'PM問題集', data: pmQuizData },",
        "replace": "            pmX: { title: 'PM問題集', data: pmQuizData },",
        "test": "Hiring-risk CTAs land on the quiz named on the button",
    },
    {
        "name": "behavior: sr-only AIO entity anchor の silent removal — index.html の <div class=\"sr-only\" id=\"aio-footer-entity\"> の id を rename → 著作権/entity/canonical ブロックが DOM から消える。旧テストは `if (await entity.count())` の skip-on-missing で黙って PASS する vacuous gate だった (実測で確認し presence 必須へ是正)。是正版が実際に RED になることの検証",
        "file": ROOT / "index.html",
        "find": '<div class="sr-only" id="aio-footer-entity" aria-hidden="true">',
        "replace": '<div class="sr-only" id="aio-footer-entity-renamed" aria-hidden="true">',
        "test": "sr-only content (route announcer + AIO entity anchor) stays visually hidden",
    },
    {
        "name": "behavior: quiz 検索語の種別スコープ喪失 — quiz-renderer.js の initialSearch を quizSearchType 一致条件から素の quizSearch へ戻す → ある種別で検索したまま別種別へ切り替えると語が持ち越され、切替先が「一致する問題は見つかりませんでした」の空ページになる (sidebar の種別リンク / hiring-risk の CTA はどちらも主要導線)。実測で architecture の 'CAP' が PM へ持ち越され PM が 0 件表示になっていた実バグの回帰防止",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "        const initialSearch = (state.appsData.quizSearchType === quizType)\n            ? (state.appsData.quizSearch || \"\")\n            : \"\";",
        "replace": "        const initialSearch = state.appsData.quizSearch || \"\";",
        "test": "Quiz search term does not leak across quiz types",
    },
    {
        "name": "behavior: プロジェクト詳細のデモ起動導線が壊れる — project-detail-page.js の「アプリを起動」を apps/<demoRoute> から誤 route (projects) へ差し替え → 閲覧者が作品を触るまでの主要ジャーニーが切れる。Check 136 は demoRoute 値が router whitelist にあることしか見ず、ボタンが実際に遷移してアプリが描画されるかは未被覆だった",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "onclick: () => Router.navigate(`apps/${project.demoRoute}`)",
        "replace": "onclick: () => Router.navigate(`projects`)",
        "test": "Project demo launch buttons open the embedded app",
    },
    {
        "name": "resilience: crypto.randomUUID 不在環境で項目追加が壊れる — js/pure-utils.js の generateId のフォールバック本体 (Math.random ベースの RFC 4122 テンプレート) を潰す → randomUUID はセキュアコンテキスト限定 API ゆえ http:// の LAN プレビュー (PC の http-server をスマホから開く等) で undefined になり、その閲覧経路でだけ項目追加が例外になる。なお feature-detection (typeof crypto...) を外すだけでは外側の try/catch が TypeError を吸収してフォールバックが働くため mutation として no-op = vacuous になる (実測済)。フォールバック本体を潰す形が正しい非 vacuity 検証",
        "file": ROOT / "js" / "pure-utils.js",
        "find": "    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {",
        "replace": "    return crypto.randomUUID();\n    // eslint-disable-next-line no-unreachable\n    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {",
        "test": "Item creation still works when crypto.randomUUID is unavailable",
    },
    {
        "name": "resilience: localStorage 不在環境での白画面化 — js/storage.js の get() から try/catch を外し素の localStorage アクセスへ → プライベートブラウジング等で localStorage アクセス自体が SecurityError を投げる環境の全ユーザーがコンテンツ非描画 (白画面) になる。quota 超過 (書き込み失敗) とは別クラスの堅牢性の回帰防止",
        "file": ROOT / "js" / "storage.js",
        "find": "        try {\n            return localStorage.getItem(key);",
        "replace": "        {\n            return localStorage.getItem(key);",
        "test": "SPA still renders when localStorage access itself throws",
    },
    {
        "name": "a11y: settings 追加フォームの検証フィールド特定喪失 — settings-page.js の addProjectManual から aria-invalid の付与と focus 移動を除去 → SR 利用者は Toast のエラーだけ聞かされ「どの入力が不正か」を判別できない (WCAG 3.3.1 / 2.4.3・quiz フォーム #913 と同 class の残り 1 面)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                if (nameEl) { nameEl.setAttribute('aria-invalid', 'true'); nameEl.focus(); }",
        "replace": "",
        "test": "Settings add-project form marks the empty name aria-invalid",
    },
    {
        "name": "a11y: quiz フォーム検証のフィールド特定喪失 — quiz-renderer.js の送信ハンドラから最初の不正フィールドへの focus 移動を除去 → SR 利用者は Toast のエラーだけ聞かされ「どのフィールドが不正か」を自力で探す羽目になる (WCAG 3.3.1 Error Identification / 2.4.3)。aria-invalid + focus 移動による識別の回帰防止",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "                    (!name ? nameInput : emailInput).focus();",
        "replace": "",
        "test": "Quiz contact form marks the offending field aria-invalid",
    },
    {
        "name": "a11y: 分担表の ARIA table 構造の喪失 — pages.js splitRow のカテゴリセルから `role: 'rowheader'` を外す → 行見出しが失われ、SR はセル読み上げ時にどのカテゴリ行かの文脈を得られなくなる (分担表は div グリッドで table 要素を持たないため ARIA role が唯一の構造露出手段・WCAG 1.3.1)。axe は role の妥当性しか見ず role 除去は違反にならないため behavior e2e が唯一の gate。新設 table-semantics test の非 vacuity 検証",
        "file": ROOT / "js" / "pages.js",
        "find": "class: 'cell-category', role: 'rowheader'",
        "replace": "class: 'cell-category'",
        "test": "Role-split division table exposes ARIA table semantics",
    },
    {
        "name": "behavior: 検索×カテゴリの AND 合成の喪失 — projects-page.js の getFilteredProjects で category 絞り込みを「検索語が無いときだけ」に狭める → カテゴリ選択中に検索するとカテゴリが無視され、選択中の <select> 表示と実際の結果が desync する (control↔filter desync・#350 と同族)。cat 単独 / q 単独の既存テストは通り続けるため、併用を検証する新テストだけが捕捉できる",
        "file": ROOT / "js" / "projects-page.js",
        "find": "            if (cat !== 'All') {\n                list = list.filter(p => p.category === cat);",
        "replace": "            if (cat !== 'All' && !q) {\n                list = list.filter(p => p.category === cat);",
        "test": "Search and category filters compose",
    },
    {
        "name": "behavior: notes editor の silent data-loss 再混入 — apps.js の textarea から maxlength を外す → 保存側は LIMITS.NOTES_TEXT で slice するのに UI は無制限に受け付け、超過分は textarea にもライブプレビューにも表示され続けたまま保存されない (リロードして初めて消失が判明する silent data-loss)。UI 上限と永続化上限の一致 (Check 410 の behavioral 面) の回帰防止",
        "file": ROOT / "js" / "apps.js",
        "find": "            maxlength: CONSTANTS.LIMITS.NOTES_TEXT,",
        "replace": "",
        "test": "Notes editor cannot hold more text than it persists",
    },
    {
        "name": "behavior: quiz の外部入力 ?type= がプロトタイプ継承キーで crash する回帰 — quiz-renderer.js の hasOwnProperty ガードを素の `MAP[type] || fallback` へ戻す → 'constructor' 等は truthy な非 config 値 (Object コンストラクタ) を返して fallback を素通りし、sourceData が undefined のまま Object.keys(undefined) が throw → FatalPage でページ全体が表示不能になる (実測)。外部入力を object 添字に使う際の own-key 検証の回帰防止",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "        const quizConfig = Object.prototype.hasOwnProperty.call(QUIZ_DATA_MAP, quizType)\n            ? QUIZ_DATA_MAP[quizType]\n            : QUIZ_DATA_MAP.aws;",
        "replace": "        const quizConfig = QUIZ_DATA_MAP[quizType] || QUIZ_DATA_MAP.aws;",
        "test": "prototype-inherited",
    },
    {
        "name": "behavior: route-render gate 自体の非 vacuity — main.js render の case 'role-split' から page = RoleSplitPage() の代入を落とす (葉抽出で配線を落とす回帰 class) → page が undefined のまま appendChild され TypeError で #content 空 + pageerror。全ルートの描画健全性を守る中核 gate (security-proxy の ALL_ROUTES loop) が実際に RED になることの検証。この loop は題名が backtick テンプレートで、Check 379/397 が引用符リテラルしか parse しなかった間は mutation を登録できなかった",
        "file": ROOT / "main.js",
        "find": "                        case 'role-split':\n                            page = RoleSplitPage();\n",
        "replace": "                        case 'role-split':\n",
        "test": "renders without runtime errors",
    },
    {
        "name": "a11y: quiz 章アイコンの装飾絵文字が SR に読み上げられる回帰 — quiz-renderer.js の quiz-section-icon から aria-hidden を外す → アクセシビリティツリーに 🏛️ 等が露出し、SR は全章で章題の前に「classical building」等の無意味な語を読む (WCAG 1.1.1・axe は装飾テキスト露出をルール化しないため behavior e2e が唯一の gate)",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "{ class: \"quiz-section-icon\", 'aria-hidden': 'true' }, icons[sIdx]",
        "replace": "{ class: \"quiz-section-icon\" }, icons[sIdx]",
        "test": "decorative emoji are hidden from the accessibility tree",
    },
    {
        "name": "behavior: WebMCP の DOM 抽出契約の喪失 — js/pages.js splitRow の human 列から機械向けフック data-ai-role を外す → WebMCP ツールが役割分担表の human/ai を区別して抽出できなくなる (agentic 面の contract 破壊)",
        "file": ROOT / "js" / "pages.js",
        "find": "class: 'cell-human', role: 'cell', 'data-ai-role': 'human'",
        "replace": "class: 'cell-human', role: 'cell'",
        "test": "WebMCP role-split extraction selector resolves",
    },
    {
        "name": "behavior: ルート追従 JSON-LD の silent 喪失 — main.js の _installSemanticDriftGuard から MutationObserver の observe 配線を落とす → script[data-ld='dynamic-route'] がルート遷移で更新されなくなり、AI クローラは初期状態の structured data しか見なくなる。視覚に一切出ないため screenshot も他の e2e も consistency も捕捉できなかった silent-critical な AIO 配線 (#133/#134/#135 と同 class) の回帰防止",
        "file": ROOT / "main.js",
        "find": "                    _observer.observe(contentEl, { childList: true, subtree: false });",
        "replace": "                    void _observer;",
        "test": "dynamic JSON-LD is injected and tracks the current route",
    },
    {
        "name": "behavior: aio-guard の自己修復が働かなくなる回帰 — aio-guard.js の MutationObserver 監視対象を document.body から document.head へ変える → hidden な AIO アンカーが削除されても復元されない。script 配線は残るため Check 133 は緑のまま (= 「配線はあるが機能しない」class・#929 WebMCP と同じレンズ)。視覚に出ない要素ゆえ screenshot も他の e2e も気付けない",
        "file": ROOT / "aio-guard.js",
        "find": "        _observer.observe(document.body, { childList: true, subtree: true });\n    }\n\n    // Attach to DOMContentLoaded",
        "replace": "        _observer.observe(document.head, { childList: true, subtree: true });\n    }\n\n    // Attach to DOMContentLoaded",
        "test": "aio-guard restores the hidden AIO anchor after it is removed",
    },
    {
        "name": "behavior: cross-app 状態の clobber — store.js normalizeAppsData の notes 読み戻しを落とす → task/todo は残るのに notes だけリロードで消える。単体テストは各アプリを独立に見るため、4 アプリを 1 セッションで触ってから 1 回リロードする統合 e2e だけがこの「片方の経路だけ巻き戻る」class を捕捉する (静的面は Check 373)",
        "file": ROOT / "js" / "store.js",
        "find": "            result.notes = data.notes.slice(0, CONSTANTS.LIMITS.NOTES_TEXT);",
        "replace": "            result.notes = '';",
        "test": "four apps in one session all survives a single reload",
    },
    {
        "name": "behavior: cross-tab 更新が編集中の入力を破壊する回帰 — state.js の storage リスナーから編集中の採用延期ガードを外す → 別タブがタスクを 1 件追加しただけで、こちらのタブで書きかけの notes が巻き戻り focus が body へ落ちる (#258 の『再描画が focused input を破棄する』class の外部イベント起点版・実測済)",
        "file": ROOT / "js" / "state.js",
        "find": "                    if (_deferIfEditing(incoming)) {return;}",
        "replace": "                    if (false) {return;}",
        "test": "Cross-tab update does not destroy an in-progress edit",
    },
    {
        "name": "behavior: 二重モーダル (drawer + command palette) の再発 — command-palette.js の open() から closeDrawer() 呼び出しを除去 → mobile drawer が開いたまま Cmd/Ctrl+K を押すと aria-modal='true' の領域が 2 つ同時に有効になり、SR にはどちらが現在のモーダルか判別できない。さらに両者の Escape ハンドラが同じ document keydown で走るため Escape 1 回で両方閉じる (#262 の二重発火と同族・実測済)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        if (typeof closeDrawer === 'function') { closeDrawer(); }\n",
        "replace": "",
        "test": "Opening the command palette closes the mobile drawer",
    },
    {
        "name": "behavior: 二重モーダルの逆方向 — mobile-drawer.js の openDrawer() から closePalette() 呼び出しを除去 → command palette 表示中に menuBtn (topbar は #app の inert 対象外ゆえクリック可能) を押すと drawer が重なって開き aria-modal='true' が 2 つ同時に有効になる。片方向だけ塞ぐと『1 ケースだけ処理して他を忘れる』非対称バグとして残る class の回帰防止",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "        if (typeof closePalette === 'function') { closePalette(); }\n",
        "replace": "",
        "test": "Opening the drawer closes the command palette",
    },
    {
        "name": "a11y: palette 表示中の背景 inert の喪失 — command-palette.js の open() から setAppInert(true) を除去 → 背景 (#app) が AT からもポインタからも生きたままになり、aria-modal='true' の解釈が揺れる AT では背景コンテンツを読み進められる。drawer は同じ状況で inert 化しており、**同じモーダルなのに背景の扱いが非対称**だった class の回帰防止",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        if (typeof setAppInert === 'function') { setAppInert(true); }\n",
        "replace": "",
        "test": "Command palette makes the background inert while open",
    },
    {
        "name": "behavior: closeDrawer の idempotency ガード喪失による scroll-clobber — mobile-drawer.js の closeDrawer から『閉じているなら早期 return』を外す → 末尾の __lockBodyScroll(false) が window.scrollTo(0, __drawerScrollY=0) を実行し、**閉じている drawer を閉じるだけでページ先頭へ飛ぶ**。二重モーダル防止で palette が open 時に無条件 closeDrawer() を呼ぶため、スクロール中に Cmd/Ctrl+K を押すと先頭ジャンプになる (#297 の openDrawer 側ガードの対・実測済)",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "        if (drawer.getAttribute('aria-hidden') !== 'false') { return; }\n",
        "replace": "",
        "test": "Opening and closing the command palette preserves the scroll position",
    },
    {
        "name": "behavior: フィルタ操作が履歴を汚す回帰 — projects-page.js の syncURL を Router.replaceSilently から Router.navigate へ変える → 検索語 1 文字ごとに history entry が積まれ、3 文字打つと『戻る』を 3 回押さないとページを離れられない典型的な SPA 退行になる (replaceSilently は history.replaceState でこれを防いでいる)",
        "file": ROOT / "js" / "projects-page.js",
        "find": "Router.replaceSilently('projects' + ",
        "replace": "Router.navigate('projects' + ",
        "test": "Browser back/forward moves between routes and filtering does not pollute history",
    },
    {
        "name": "behavior: 詳細ページの『一覧に戻る』が絞り込みを捨てる回帰 — project-detail-page.js の戻り先を Router.getLastListPath() から 'projects' ハードコードへ戻す → ?q= / ?cat= を落として全件表示へ戻る。ブラウザの Back は履歴の query 付き URL へ復帰するため『同じ意味の操作なのに結果が違う』不整合になる (実測: 1 件に絞って詳細を開き in-page back → 18 件)",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "Router.navigate(Router.getLastListPath ? Router.getLastListPath() : 'projects')",
        "replace": "Router.navigate('projects')",
        "test": "In-page \"back to list\" preserves the active filter",
    },
    {
        "name": "a11y: topbar テーマボタンのラベル同期の喪失 — theme.js apply() から #themeBtnTop の aria-label 更新を除去 → mobile 利用者には『テーマを切り替える（現在: …）』が初期値のまま固定され、現在テーマが SR に露出しなくなる (WCAG 4.1.2)。sidebar 側は render 毎の再構築という **別機構** で更新されるため、desktop 前提の既存テストでは検出できなかった (実測: 削除しても既存 10 件は全緑) 未被覆面の回帰防止",
        "file": ROOT / "js" / "theme.js",
        "find": "            topBtn.setAttribute('aria-label', themeToggleAriaLabel(theme));",
        "replace": "            void themeToggleAriaLabel;",
        "test": "Topbar theme button exposes the current theme in its label on mobile",
    },
    {
        "name": "behavior: スナップショット削除の確認ガード喪失 — settings-page.js clearSnapshot から confirm を除去 → ユーザー唯一の復元点が無確認で消える。プロジェクト 1 件の削除と全リセットは confirm を通すのに、より影響の大きいスナップショット削除だけ無確認だった非対称 (CLAUDE.md §7 の反復 class) の回帰防止",
        "file": ROOT / "js" / "settings-page.js",
        "find": "            if (!confirm(_at",
        "replace": "            if (false && !confirm(_at",
        "test": "Deleting the snapshot asks for confirmation",
    },
    {
        "name": "behavior: タスク 0 件の説明表示の喪失 — apps.js の空状態ブロックを無効化 → 優先度フィルタで 0 件になっても 3 列に『0』が並ぶだけで、フィルタが隠しているのか本当に空なのか判別できない状態へ戻る (TodoPage は同じ状況でメッセージを出しており task 側だけ欠けていた非対称) の回帰防止",
        "file": ROOT / "js" / "apps.js",
        "find": "            if (allTasks.length === 0) {",
        "replace": "            if (false) {",
        "test": "Task board explains why it is empty",
    },
    {
        "name": "behavior: ポモドーロ当日要約の集計誤り — pomodoro-page.js の当日フィルタ (timestamp >= 当日 0 時) を外す → 昨日以前の完了セッションまで『今日の実績』に数え、利用者が今日の進捗を誤認する。記録しているのに画面に出していなかった history を要約表示した増分の回帰防止",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "e.type === 'work' && e.timestamp >= _start).length",
        "replace": "e.type === 'work').length",
        "test": "Pomodoro shows today",
    },
    {
        "name": "behavior: 320px 幅の横あふれ再発 — style.css の mobile media query から `max-width: 100%` を外す → .app が column flex になった際に .main-content の左右 auto margin が cross 軸 auto margin となり stretch が無効化され、fit-content が min-content を下回れず item が viewport より広くなる (WCAG 1.4.10 違反・実測 role-split +51px)。screenshot は 1280x720 clip でこの media query に到達しないため、捕捉できるのは behavior test だけ",
        "file": ROOT / "style.css",
        "find": "は非到達。 */\n                max-width: 100%;",
        "replace": "は非到達。 */",
        "test": "WCAG 1.4.10: 320px 幅でどのルートも横スクロールしない",
    },
    {
        "name": "behavior: profile 正規化の型ガード喪失 — store.js の safeStr を旧実装 `String(v || fallback)` に戻す → `[]` や `{}` のような truthy な非文字列が `||` を素通りし String([]) === '' でフィールドが空になる。email が空になると ContactPage から宛先表示が消え「メールを作成」が宛先の無い mailto: を開く (fatal を出さないので ErrorBoundary にも掛からず、視覚 baseline は ADVISORY ゆえ behavior test 以外に捕捉層が無い)",
        "file": ROOT / "js" / "store.js",
        "find": "        const s = (v && cand.trim() !== '') ? cand : String(fallback || '');",
        "replace": "        const s = String(v || fallback || '');",
        "test": "Hostile profile import: a truthy non-string must not blank a field",
    },
    {
        "name": "behavior: project 正規化の型ガード喪失 — store.js の name を旧実装 `String(raw.name || 'Untitled')` に戻す → `{}` が truthy なので fallback が働かず \"[object Object]\" が一覧カードと詳細ページへそのまま描画される (実測で一覧 3 箇所 / 詳細 4 箇所)。fatal を出さないので ErrorBoundary に掛からず、視覚 baseline は ADVISORY ゆえ behavior test 以外に捕捉層が無い",
        "file": ROOT / "js" / "store.js",
        "find": "            name: safeStr(raw.name, 'Untitled', CONSTANTS.LIMITS.PROJECT_NAME),",
        "replace": "            name: String(raw.name || 'Untitled').slice(0, CONSTANTS.LIMITS.PROJECT_NAME),",
        "test": "Hostile project import: non-string fields must not render as [object Object]",
    },
    {
        "name": "behavior: appsData の必須テキスト型ガード喪失 — normalizeAppsData の task filter を `isText(t.title)` から旧 `t.title` へ戻す → `{}` は truthy なので entry が落ちず、本文の無い空カードとして残る (旧実装ではさらに String(t.title) が \"[object Object]\" を描画していた)。NOTE: 描画側の検査だけでは捕捉できず (safeStr により空文字になるため)、永続化された appsData に壊れた entry が残っていないことの検査が本 mutation を捕捉する",
        "file": ROOT / "js" / "store.js",
        "find": "                .filter(t => t && isText(t.title))",
        "replace": "                .filter(t => t && t.title)",
        "test": "Hostile appsData import: non-string title/text must not render as [object Object]",
    },
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。
E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE + _E2E_TAIL
