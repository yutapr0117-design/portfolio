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

# 新しい側の curated mutation (新規追記は本リスト末尾へ / 上記「追記規約」参照)。
_MUTATIONS_TAIL = [
    # 注: Check 362 (mutation anchor resolution) の curated meta-mutation は敢えて置かない。
    # anchor を orphan 化する mutation は mutation_samples.py 自身の `"find":` 行を quote する
    # 自己参照になり、mutation_probe の replace(find, replace, 1) が先頭 (= その mutation 自身の
    # find 値) に当たって挙動が不安定になるため。Check 362 の非 vacuous 性は手動で実証済
    # (mutation の file を誤り先へ変えると Check 362 が RED・restore で緑)。
    {
        "name": "Check 366: ContactPage LinkedIn の rel:'noopener noreferrer' から noreferrer を除去 (source drift 再発・静的 source 軸の防止層の回帰)",
        "file": ROOT / "js" / "components.js",
        "find": "                            h('a', { href: profile.linkedin, target: '_blank', rel: 'noopener noreferrer' }, profile.linkedin)",
        "replace": "                            h('a', { href: profile.linkedin, target: '_blank', rel: 'noopener' }, profile.linkedin)",
        "test": "Check 366: shipped JS target='_blank' に ±2行以内で noreferrer あり",
    },
    {
        "name": "Check 367: projects-page.js の h('select') に value: cat を再注入 → h('select') attrs に value: キーが禁止であることの BLOCKING 検証",
        "file": ROOT / "js" / "projects-page.js",
        "find": "                    h('select', {\n                        class: 'input',\n                        'aria-label': 'カテゴリフィルター',",
        "replace": "                    h('select', {\n                        class: 'input',\n                        value: cat,\n                        'aria-label': 'カテゴリフィルター',",
        "test": "Check 367: shipped JS h('select') の attrs に value: キーなし",
    },
    {
        "name": "Check 369: store.js の AI 履歴 slice を CONSTANTS.LIMITS.AI_HISTORY からマジック -80 へ戻す → 履歴上限 drift の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": ".slice(-CONSTANTS.LIMITS.AI_HISTORY);",
        "replace": ".slice(-80);",
        "test": "Check 369: store.js / ai-page.js / pomodoro-page.js が履歴保持件数上限を CONSTANTS.LIMITS.*_HISTORY 経由で参照",
    },
    {
        "name": "Check 370: store.js の pomodoro 既定 settings を CONSTANTS からマジック {work:25...} へ戻す → 既定状態 drift の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": "settings: { ...CONSTANTS.POMODORO_DEFAULT_SETTINGS },",
        "replace": "settings: { work: 25, short: 5, long: 15 },",
        "test": "Check 370: state.js / store.js が pomodoro 既定状態を CONSTANTS.POMODORO_DEFAULT_* 経由で参照",
    },
    {
        "name": "Check 371: state.js.md に volatile 現在行数引用 (**Check 52**: N 行 ≤ M) を再注入 → mirror-doc line-count drift-magnet の BLOCKING 検証",
        "file": ROOT / "docs" / "files" / "js" / "state.js.md",
        "find": "**Check 52**: 行数予算 ≤ 320 行",
        "replace": "**Check 52**: 219 行 ≤ 320",
        "test": "Check 371: mirror doc の Check 52 制約が volatile な現在行数を hardcode しない",
    },
    {
        "name": "Check 372: quiz-renderer.js.md の factory signature を stale 形へ戻し quiz data 依存 (awsQuizData 等) を落とす → mirror-doc factory-dep drift の BLOCKING 検証",
        "file": ROOT / "docs" / "files" / "js" / "quiz-renderer.js.md",
        "find": "createQuizRenderer({ h, createIcon, Toast, Router, State, awsQuizData, pmQuizData, qualityQuizData, architectureQuizData })",
        "replace": "createQuizRenderer({ h, createIcon, Store, State, quizData: {} })",
        "test": "Check 372: 各 js/*.js factory の全注入依存が対応 mirror doc に言及されている",
    },
    {
        "name": "Check 364: store.js の Array.isArray ガードを unsafe な `(raw.tech || []).filter` idiom へ戻す → ingestion-crash class 構造防止の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": "tech: (Array.isArray(raw.tech) ? raw.tech : []).filter(Boolean).slice(0, 12),",
        "replace": "tech: (raw.tech || []).filter(Boolean).slice(0, 12),",
        "test": "Check 364: store.js の正規化子に unsafe `(X || []).<throwing array-method>` idiom が無い",
    },
    {
        "name": "Check 368: store.js の notes 上限を CONSTANTS.LIMITS.NOTES_TEXT からマジック 20000 へ戻す → notes 上限 drift の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": "result.notes = data.notes.slice(0, CONSTANTS.LIMITS.NOTES_TEXT);",
        "replace": "result.notes = data.notes.slice(0, 20000);",
        "test": "Check 368: apps.js / store.js が notes 上限を CONSTANTS.LIMITS.NOTES_TEXT 経由で参照",
    },
    {
        "name": "Check 373 (appsData persist round-trip): drop quizSearch preserve from normalizeAppsData → reload で検索語が silent に失われる producer/consumer drift (#294/#568 class)",
        "file": ROOT / "js" / "store.js",
        "find": "        if (typeof data.quizSearch === 'string') {\n            result.quizSearch = data.quizSearch.slice(0, CONSTANTS.LIMITS.QUIZ_SEARCH);\n        }",
        "replace": "        // [mutation-probe] quizSearch preserve removed to exercise Check 373",
    },
    {
        "name": "Check 374 (importJSON normalize-before-adopt): commit を State.update へ戻す → 生 ingestion が render に届く normalize-before-adopt 違反 (#295/#561 class)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                    State.set(Store.validateAndNormalize(merged));",
        "replace": "                    State.update(s => { Object.assign(s, Store.validateAndNormalize(merged)); });",
    },
    {
        "name": "Check 375 (createIcon icon-registry resolution): 既存 createIcon('trash') を未定義 name へ typo → silent 空アイコン wiring gap (icon-only ボタンが不可視化)",
        "file": ROOT / "js" / "apps.js",
        "find": "                                        }, createIcon('trash', 14))",
        "replace": "                                        }, createIcon('trsah', 14))",
    },
    {
        "name": "Check 376 (data-action → ActionDelegator resolution): 既存 data-action='drawer:open' を未登録 action へ typo → silent no-op wiring gap (menu ボタン無反応)",
        "file": ROOT / "index.html",
        "find": 'data-action="drawer:open"',
        "replace": 'data-action="drawr:open"',
    },
    {
        "name": "Check 377 (非 app route.name → main.js case): main.js の case 'project-detail' を typo → router が解決する route が silent 404 化 (project-detail は Check 58 除外ゆえ 377 を isolate)",
        "file": ROOT / "main.js",
        "find": "case 'project-detail':",
        "replace": "case 'project-detailX':",
    },
    {
        "name": "Check 378 (MOBILE_BREAKPOINT JS↔CSS coherence): JS MOBILE_BREAKPOINT を CSS @media(920) から drift → sidebar+topbar 同時表示の broken responsive layout gap",
        "file": ROOT / "js" / "constants.js",
        "find": "MOBILE_BREAKPOINT: 920,",
        "replace": "MOBILE_BREAKPOINT: 960,",
    },
    {
        "name": "Check 395 (Router.navigate literal target → router route-segment): home-page.js の Router.navigate('role-split') を typo 'rolesplit' へ → router が未知 segment を home として parse し nav ボタンが silent にホームへ誤誘導する dead-nav wiring gap (producer 面の used⟹defined)",
        "file": ROOT / "js" / "home-page.js",
        "find": "Router.navigate('role-split')",
        "replace": "Router.navigate('rolesplit')",
    },
    # NOTE: Check 379 (E2E_MUTATIONS test-field resolution) には consistency mutation を登録しない。
    # 本 Check は mutation_samples.py 自身の E2E_MUTATIONS `test` フィールドを検証するため、それを狙う
    # mutation は「find 文字列が自 entry の find フィールドにも現れる」self-reference になり、
    # mutation_probe の `replace(find, replace, 1)` (first-only) が実 E2E entry でなく自 mutation の find
    # を先に打って実 target を無傷にする＝機能しない。ゆえに Check 379 の非 vacuity は手動検証で担保
    # (実 test フィールドを replace-all で typo→check RED→保存コピーから復元。commit メッセージに記録)。
    # 118 の Check が mutation 未保有ゆえ mutation 不在は規約違反ではない。
    {
        "name": "Check 381 (main.js import ⟹ _modules47 registration): checks_esm.py の _modules47 から command-palette.js 登録行を除去 → main.js が静的 import するのに未登録 = modulepreload 漏れ drift (#706 class) を Check 381/57 mesh が捕捉。checks_esm.py は mutation_samples.py と別 file ゆえ self-reference trap 無し",
        "file": ROOT / ".github" / "scripts" / "checks_esm.py",
        "find": '        ("./js/command-palette.js",       ROOT / "js" / "command-palette.js"),\n',
        "replace": "",
    },
    {
        "name": "Check 370 (settings fallback magic): store.js の pomodoro settings normalize clamp fallback を CONSTANTS 参照からマジック || 25 へ戻す → runtime remainingSec は定数参照するのに settings fallback だけ magic だった非対称 gap の再発を拡張 Check 370 が捕捉。checks_shipped_hygiene.py は mutation_samples.py と別 file ゆえ self-reference trap 無し",
        "file": ROOT / "js" / "store.js",
        "find": "Number(data.pomodoro.settings.work) || CONSTANTS.POMODORO_DEFAULT_SETTINGS.work",
        "replace": "Number(data.pomodoro.settings.work) || 25",
        "test": "Check 370: state.js / store.js が pomodoro 既定状態を CONSTANTS.POMODORO_DEFAULT_* 経由で参照",
    },
    {
        "name": "Check 103 (prefers-contrast block presence): 実 @media (prefers-contrast: more) ブロックの開き波括弧を壊す → 修正後の Check 103 (`) {` 要求) が実ブロック不在を検出。修正前はコメント言及にマッチして vacuous に pass していた #278/#283 class の gate バグを封じたことの回帰防止 (checks_css.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "@media (prefers-contrast: more) {",
        "replace": "@media (prefers-contrast: BROKEN) {",
    },
    {
        "name": "Check 101 (forced-colors focus block presence): 実 @media (forced-colors: active) ブロックの開き波括弧を壊す → 修正後の Check 101 (`) {` 要求) が実ブロック不在を検出。コメント言及を first-match していた fragility を `{` 要求で解消したことの回帰防止 (checks_css.py は別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "@media (forced-colors: active) {",
        "replace": "@media (forced-colors: BROKEN) {",
    },
    {
        "name": "Check 385 (checks_*.py ctx.warnings/errors unpack): checks_aio_config.py の `warnings = ctx.warnings` unpack 行を除去 → bare warnings.append を持つのに unpack が無くなり Check 385 が検出。error-path NameError crash の latent bug (dependabot.yml 削除で Check 68 が NameError 化した実バグ) を封じた回帰防止 (Check 385 は checks_maintainability.py・本 mutation target は checks_aio_config.py ゆえ self-reference trap 無し)",
        "file": ROOT / ".github" / "scripts" / "checks_aio_config.py",
        "find": "    warnings = ctx.warnings",
        "replace": "    _warnings_unpack_removed = None",
    },
    {
        "name": "Check 68 (dependabot dual-ecosystem coverage): dependabot.yml の npm ecosystem 宣言を壊す → Check 68 が npm coverage 欠落を検出。file-missing パス (skip→fail 修正) は file 削除ゆえ mutation 不可で手動検証、本 mutation は content-check (npm/github-actions 両 ecosystem 必須) の非 vacuity を institutionalize",
        "file": ROOT / ".github" / "dependabot.yml",
        "find": 'package-ecosystem: "npm"',
        "replace": 'package-ecosystem: "BROKEN"',
    },
    {
        "name": "Check 139 (AppsPage↔router bijection・逆方向): AppsPage の `const apps = [...]` に router 未登録の phantom app card を注入 → 「開く」が apps/<id> へ navigate し not-found 解決 = 開くと 404 の dead card。旧 Check は router⊆AppsPage の片側のみ強制で本方向 (AppsPage⊆router) を素通していた gap を bijection 化したことの回帰防止 (checks_app_route.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "components.js",
        "find": "            { id: 'notes', title: 'Markdown ノート', desc: 'innerHTML 不使用の安全 MD ライブプレビュー', icon: 'edit' },",
        "replace": "            { id: 'phantomzz', title: 'Phantom', desc: 'router 未登録 dead card', icon: 'edit' },\n            { id: 'notes', title: 'Markdown ノート', desc: 'innerHTML 不使用の安全 MD ライブプレビュー', icon: 'edit' },",
    },
    {
        "name": "Check 128 (cmdk↔router bijection・逆方向): command-palette NAV に router 未登録の apps/phantomzz entry を注入 → Cmd+K 選択で apps/phantomzz へ navigate し not-found = 開くと 404 の dead entry。旧 Check は router⊆palette の片側のみで本方向 (palette⊆router) を素通していた gap を bijection 化した回帰防止 (checks_behavioral.py は別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        { label: 'Markdown ノート', hash: 'apps/notes' },",
        "replace": "        { label: 'Markdown ノート', hash: 'apps/notes' },\n        { label: 'Phantom', hash: 'apps/phantomzz' },",
    },
    {
        "name": "Check 138 (sidebar↔router bijection・逆方向): sidebar labItems に router 未登録の path:'apps/phantomzz' link を注入 → クリックで apps/phantomzz へ navigate し not-found = 404 の dead link。旧 Check は router⊆sidebar の片側のみで本方向 (sidebar⊆router) を素通していた gap を bijection 化した回帰防止 (checks_app_route.py は別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "components.js",
        "find": "            { icon: 'edit',        label: 'Markdown ノート', path: 'apps/notes',       active: route.name === 'app-notes' },",
        "replace": "            { icon: 'edit',        label: 'Markdown ノート', path: 'apps/notes',       active: route.name === 'app-notes' },\n            { icon: 'edit', label: 'Phantom', path: 'apps/phantomzz', active: false },",
    },
    {
        "name": "Check 382 (palette↔router 静的 route bijection・逆方向): command-palette NAV に router case 未登録の phantom 静的 hash を注入 → Cmd+K 選択で not-found へ飛ぶ dead entry。旧 Check は router⊆palette の片側のみで本方向 (palette static ⊆ router) を素通していた gap を bijection 化した回帰防止 (#790 で budget 枯渇のため保留していた逆方向 mutation を archive2 rotate 後に登録・checks_behavioral.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        { label: 'Settings（設定）', hash: 'settings' },",
        "replace": "        { label: 'Settings（設定）', hash: 'settings' },\n        { label: 'Phantom Static', hash: 'phantomstatic' },",
    },
    {
        "name": "Check 391 (getElementById→id definition wiring): home-page.js の id: 'evidence-heading' 定義を rename → getElementById('evidence-heading') (同 file) が未定義 id を指す dead DOM lookup 化。id をリネームして getElementById('old') を残すと DOM lookup が null を返し button/feature が silent no-op 化する class (#257/#262 wiring 系の DOM-id 面・Check 375/376/377 の used⟹defined wiring twin。checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "home-page.js",
        "find": "id: 'evidence-heading'",
        "replace": "id: 'evidence-headingZZ'",
    },
    {
        "name": "Check 392 (aria idref→id definition wiring): home-page.js の id: 'aio-series-heading' 定義を rename → aria-labelledby: 'aio-series-heading' が dangling 化 = accessible name の関連付けが assistive tech 上で切れる WCAG 1.3.1/4.1.2 欠陥。id を片方でリネームすると screen reader が label 無しの control をアナウンスするが visual 無変化・behavior e2e 素通りで silent (#563/#728 class。aio-series-heading は getElementById 非対象ゆえ Check 391 と隔離・checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "home-page.js",
        "find": "id: 'aio-series-heading'",
        "replace": "id: 'aio-series-headingZZ'",
    },
    {
        "name": "Check 393 (CONSTANTS.* reference→definition wiring): store.js の CONSTANTS.LIMITS.MAX_TODOS 参照を typo (MAX_TODOSXX) へ → js/constants.js に未定義の key を指す silent-undefined 化。typo は合法な property access ゆえ throw せず undefined へ評価され、.slice(0, undefined) が切り詰めを無効化 (DoS/bloat ガード沈黙) / setTimeout(fn, undefined) 即発火する silent bug (Check 375/376/377/391/392 の used⟹defined wiring レンズの CONSTANTS-access 面。checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "store.js",
        "find": "CONSTANTS.LIMITS.MAX_TODOS",
        "replace": "CONSTANTS.LIMITS.MAX_TODOSXX",
    },
    {
        "name": "Check 390 (router route.name ⊆ PAGE_META・param-route coverage): page-meta.js の about entry キーを rename (aboutXX) → router が emit する route.name 'about' が PAGE_META から欠落 → applyMeta が `if (!meta) return` で early-return し about ページの title/desc/JSON-LD/route アナウンスが消失する silent AIO/SEO 回帰 (Check 118 は ALL_ROUTES 経由ゆえ param route を守れない盲点を 390 が補完・checks_shipped_structure.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "page-meta.js",
        "find": "    about: { title: 'About',",
        "replace": "    aboutXX: { title: 'About',",
    },
    {
        "name": "Check 383 (prefers-reduced-motion global reset): style.css の universal reset から transition-duration を除去 → @media (prefers-reduced-motion: reduce) の global motion reset が不完全化し、前庭障害配慮 (WCAG 2.3.3) の CSS-layer 主防御が silent に破れる (behavior e2e は動きを検査せず screenshot advisory ゆえ無検出)。101/103 と同じ a11y-CSS presence class の mutation coverage を完成させる (checks_css.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "transition-duration: 0.001ms !important;",
        "replace": "transition-property: all !important;",
    },
    {
        "name": "Check 384 (base :focus-visible outline): style.css の base :focus-visible の outline を none 化 → 通常モードのキーボード focus indicator (WCAG 2.4.7) が silent に消失する (101/103 は forced-colors/prefers-contrast の @media 変種のみ守り base outline は無保護)。behavior e2e は focus ring を検査せず screenshot advisory ゆえ無検出。101/103/383 と同じ a11y-CSS presence class の mutation coverage を完成 (checks_css.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "outline: 2px solid var(--color-primary);",
        "replace": "outline: none;",
    },
    {
        "name": "Check 396 (route.name ⟹ PAGE_META entry): js/page-meta.js から 'contact' の PAGE_META エントリを除去 → router.js が emit する route.name 'contact' が PAGE_META に不在になり、meta-management.js applyMeta が早期 return して contact ルートの <title>/SEO meta/route announcer (a11y 2.4.2) が silent 欠落する。新ルート追加時の PAGE_META 登録漏れ class を BLOCKING で捕捉する Check 396 の非 vacuity 検証 (page-meta.js からのエントリ除去は Check 377=main.js case を trip せず 396 単独で捕捉する。checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "page-meta.js",
        "find": "    contact: { title: 'Contact', desc: 'お問い合わせ。メール・GitHub・LinkedIn。' },",
        "replace": "    /* contact removed */",
    },
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。
MUTATIONS = MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

E2E_MUTATIONS = [
    {
        "name": "behavior: cross-tab が別 schema/欠損 store を raw 採用して crash (#93 class)",
        "file": ROOT / "js" / "state.js",
        "find": "                    if (incoming.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {return;}\n                    data = Store.validateAndNormalize(incoming);",
        "replace": "                    data = incoming;",
        "test": "Cross-tab sync ignores a foreign-schema",
    },
    {
        "name": "behavior: quiz 検索が section 見出しを対象外 (#285 class)",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "                    if (sectionMatch) {return true;}\n",
        "replace": "",
        "test": "section-header",
    },
    {
        "name": "behavior: drawer 再 open の scroll-clobber (#262 class)",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "        if (drawer.getAttribute('aria-hidden') === 'false') {return;}\n\n",
        "replace": "",
        "test": "scroll-clobber regression",
    },
    {
        "name": "behavior: 安全網が正常な FatalPage を覆う (silent-failure 限定の喪失)",
        "file": ROOT / "js" / "fatal-overlay.js",
        "find": "\n                    && !document.getElementById('fallback-details')",
        "replace": "",
        "test": "safety net does not cover",
    },
    {
        "name": "behavior: 外部リンク noopener 強制 (tabnabbing 防御) の喪失",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "                if (!rel.includes('noopener')) {rel.push('noopener');}\n",
        "replace": "",
        "test": "External target=_blank links are hardened",
    },
    {
        "name": "behavior: AIO/SEO の route 毎 document.title 注入の喪失 (リポジトリ中核 bet)",
        "file": ROOT / "js" / "meta-management.js",
        "find": "        document.title = fullTitle;\n",
        "replace": "",
        "test": "Each route updates document.title",
    },
    {
        "name": "behavior: resilience — corrupt localStorage 耐性 (storage.parse の JSON 例外ガード) の喪失",
        "file": ROOT / "js" / "storage.js",
        "find": "        try {\n            return JSON.parse(data);\n        } catch {\n            return null;\n        }",
        "replace": "        return JSON.parse(data);",
        "test": "App recovers gracefully from corrupt localStorage",
    },
    {
        "name": "behavior: resilience — schema 不一致時の旧データ退避+default リセットの喪失",
        "file": ROOT / "js" / "store.js",
        "find": "if (data.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {",
        "replace": "if (data.schemaVersion === CONSTANTS.SCHEMA_VERSION) {",
        "test": "Store migrates safely on schema version mismatch",
    },
    {
        "name": "behavior: IME composition guard の喪失 (日本語変換確定 Enter の誤 submit・主対象言語)",
        "file": ROOT / "js" / "apps.js",
        "find": "if (e.key === 'Enter' && !e.isComposing) {\n                                addTask(e.target.value);",
        "replace": "if (e.key === 'Enter') {\n                                addTask(e.target.value);",
        "test": "Task input ignores Enter during IME composition",
    },
    {
        "name": "behavior: live-input focus-loss guard の喪失 (oninput が全再描画で focus を破棄)",
        "file": ROOT / "js" / "apps.js",
        "find": "State.updateSilently(s => { s.appsData.notes = val.slice(0, CONSTANTS.LIMITS.NOTES_TEXT); });",
        "replace": "State.update(s => { s.appsData.notes = val.slice(0, CONSTANTS.LIMITS.NOTES_TEXT); });",
        "test": "Notes textarea retains focus while typing",
    },
    {
        "name": "behavior: a11y route-focus (WCAG 2.4.3) の喪失 (route 遷移で新ページ h1 へ focus 移らず)",
        "file": ROOT / "main.js",
        "find": "if (isRouteChange && content && _focusWasLost) {",
        "replace": "if (!isRouteChange && content && _focusWasLost) {",
        "test": "Route change moves focus to the new page heading",
    },
    {
        "name": "behavior: resilience — localStorage quota 超過の握り潰し (storage.set try/catch) の喪失",
        "file": ROOT / "js" / "storage.js",
        "find": "        try {\n            // codeql[js/clear-text-storage-of-sensitive-data] - False positive:\n            // Stores portfolio UI state (task list, theme, pomodoro history).\n            // No credentials, tokens, or PII are stored in localStorage.\n            localStorage.setItem(key, value);\n            return true;\n        } catch {\n            return false;\n        }",
        "replace": "        localStorage.setItem(key, value);\n        return true;",
        "test": "Task app degrades gracefully when localStorage write quota",
    },
    {
        "name": "behavior: a11y — mobile drawer focus-trap (WCAG modal) の喪失 (Tab が背景へ漏れる)",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "if (e.key !== 'Tab') {return;}",
        "replace": "if (e.key !== 'Tab-DISABLED') {return;}",
        "test": "Mobile drawer traps focus within the dialog",
    },
    {
        "name": "behavior: a11y — command palette focus-trap の喪失 (Tab が背景へ漏れる)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }",
        "replace": "else if (!e.shiftKey && document.activeElement === last) { /* trap disabled */ }",
        "test": "Command palette traps Tab focus inside the modal",
    },
    {
        "name": "behavior: pomodoro complete (#121) — getRemaining の stale-closure 化で timer が永遠に未完了",
        # 2026-07-04 bloat-reduction: PomodoroPage は js/apps.js → js/pomodoro-page.js へ分離した
        # (#558)。find-anchor もそこへ移動したため file を追従させる (抽出で anchor が orphan 化した
        # 実例・mutation-probe --e2e が検出)。
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "            const rt = State.get().appsData.pomodoro.runtime;\n            if (rt.isActive && rt.endAtMs) {",
        "replace": "            const rt = pomo.runtime;\n            if (rt.isActive && rt.endAtMs) {",
        "test": "Pomodoro completes at zero",
    },
    {
        "name": "behavior: snapshot 復元が正規化を通さず生採用して schema 不一致/欠損で crash (#93/#295 class)",
        # 2026-07-05: SettingsPage を js/apps.js → js/settings-page.js へ分離したため anchor file を追従 (#558 class)
        "file": ROOT / "js" / "settings-page.js",
        "find": "            State.set(Store.validateAndNormalize(snap.data));",
        "replace": "            State.set(snap.data);",
        "test": "Snapshot restore normalizes",
    },
    {
        "name": "behavior: TodoPage が ErrorBoundary a11y 属性を leak (role=alert / dangling aria-errormessage)",
        "file": ROOT / "js" / "apps.js",
        "find": "        return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },\n            h('header', { class: 'flex items-center gap-3' },\n                createIcon('list', 28),",
        "replace": "        return h('div', { class: 'flex flex-col gap-4 max-w-2xl error-boundary-fallback', role: 'alert', 'aria-errormessage': 'fallback-details' },\n            h('header', { class: 'flex items-center gap-3' },\n                createIcon('list', 28),",
        "test": "carries no leaked ErrorBoundary",
    },
    {
        "name": "behavior: normalizeAppsData の ai.history Array.isArray ガード喪失 (非配列 .filter で TypeError → 全 ingestion 経路 crash・#93/#295/#561 class)",
        "file": ROOT / "js" / "store.js",
        "find": "        if (Array.isArray(data.ai?.history)) {",
        "replace": "        if (data.ai?.history) {",
        "test": "normalizeAppsData tolerates a non-array",
    },
    {
        "name": "behavior: normalizeProject の tech Array.isArray ガード喪失 (非配列 project field .filter で TypeError → import/ingestion crash・#93/#295/#561/#568 class)",
        "file": ROOT / "js" / "store.js",
        "find": "            tech: (Array.isArray(raw.tech) ? raw.tech : []).filter(Boolean).slice(0, 12),",
        "replace": "            tech: (raw.tech || []).filter(Boolean).slice(0, 12),",
        "test": "normalizeProject tolerates a non-array",
    },
    {
        "name": "behavior: normalizeAppsData の task.tags Array.isArray ガード喪失 (非配列 tags .filter で TypeError → import/ingestion crash・#93/#295/#561/#568/#572 class)",
        "file": ROOT / "js" / "store.js",
        "find": "                    tags: (Array.isArray(t.tags) ? t.tags : []).filter(Boolean).slice(0, 10),",
        "replace": "                    tags: (t.tags || []).filter(Boolean).slice(0, 10),",
        "test": "normalizeAppsData tolerates a non-array",
    },
    {
        "name": "behavior: ProjectDetailPage の !project null-guard 喪失 (非存在 slug で guard が発火せず undefined への property access で crash → 「プロジェクトが見つかりません」未描画)",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "        if (!project) {",
        "replace": "        if (false) {",
        "test": "ProjectDetailPage shows not-found message and returns to list for nonexistent slug",
    },
    {
        "name": "behavior: ProjectsPage URL deep-link ?q= 復元の喪失 (route.query.q を無視して常に空文字を初期 q にする → 直接到達時に検索状態が復元されず input が空)",
        "file": ROOT / "js" / "projects-page.js",
        "find": "        let q = route.query.q || '';",
        "replace": "        let q = '';",
        "test": "Projects page restores search query from URL deep-link (?q=)",
    },
    {
        "name": "behavior: ProjectsPage URL deep-link ?cat= 復元の喪失 (route.query.cat を無視して常に 'All' を初期 cat にする → 直接到達時にカテゴリフィルタが復元されず select が 'All')",
        "file": ROOT / "js" / "projects-page.js",
        "find": "        let cat = route.query.cat || 'All';",
        "replace": "        let cat = 'All';",
        "test": "Projects page restores category filter from URL deep-link (?cat=)",
    },
    {
        "name": "fix regression: h() textarea value — el.value 設定を el.setAttribute に戻す → reload 後に notes textarea が空 (el.value は IDL property、content attribute 経由では設定不能)",
        "file": ROOT / "js" / "ui-components.js",
        "find": "        } else if (key === 'value' && tag === 'textarea') {",
        "replace": "        } else if (key === 'value' && tag === 'NEVER_MATCH_INTENTIONAL_BREAK') {",
        "test": "Markdown notes app live-previews (innerHTML-free) and persists",
    },
    {
        "name": "fix regression: settings import mode select visual selection — selected 条件を除去すると再描画後に 'append' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                                        h('option', { value: 'upsert', selected: settingsImportMode === 'upsert' ? true : undefined }, 'upsert（更新+追加）'),",
        "replace": "                                        h('option', { value: 'upsert' }, 'upsert（更新+追加）'),",
        "test": "Settings import mode select retains visual selection after re-render",
    },
    {
        "name": "fix regression: task priority filter select visual selection — selected 条件を除去すると再描画後に 'all' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "apps.js",
        "find": "                        h('option', { value: 'high', text: 'High', selected: taskFilter.priority === 'high' ? true : undefined }),",
        "replace": "                        h('option', { value: 'high', text: 'High' }),",
        "test": "Task priority filter select retains visual selection after re-render",
    },
    {
        "name": "fix regression: task per-card priority select visual selection — selected 条件を除去すると再描画後に 'high' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "apps.js",
        "find": "                                            h('option', { value: 'low', text: 'Low', selected: task.priority === 'low' ? true : undefined })",
        "replace": "                                            h('option', { value: 'low', text: 'Low' })",
        "test": "Task per-card priority select retains visual selection after re-render",
    },
    {
        "name": "fix regression: todo filter select visual selection — selected 条件を除去すると再描画後に 'all' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "apps.js",
        "find": "                            h('option', { value: 'active', text: '未完了', selected: todoFilter === 'active' ? true : undefined }),",
        "replace": "                            h('option', { value: 'active', text: '未完了' }),",
        "test": "Todo filter select retains visual selection after re-render",
    },
    {
        "name": "behavior: quiz 検索語の reload 跨ぎ復元の喪失 (normalizeAppsData が quizSearch を preserve せず reload で空になる producer/consumer drift・#294/#568 class)",
        "file": ROOT / "js" / "store.js",
        "find": "        if (typeof data.quizSearch === 'string') {\n            result.quizSearch = data.quizSearch.slice(0, CONSTANTS.LIMITS.QUIZ_SEARCH);\n        }",
        "replace": "        // quizSearch preserve removed (mutation)",
        "test": "Quiz search term persists across reload",
    },
    {
        "name": "behavior: pomodoro 休憩時間 live-update の喪失 (short 設定 onchange の remainingSec 即更新を除去 → 休憩モード idle で設定変更しても表示が古いまま・work との非対称)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "                                        if (!s.appsData.pomodoro.runtime.isActive && s.appsData.pomodoro.runtime.mode === 'short-break') {\n                                            s.appsData.pomodoro.runtime.remainingSec = s.appsData.pomodoro.settings.short * 60;\n                                        }\n",
        "replace": "",
        "test": "Pomodoro break-duration change updates the idle timer display",
    },
    {
        "name": "behavior: AI keyword routing の breakdown 分岐喪失 (analyzeInput から breakdown keyword を除去 → 「分解して」が general に倒れ専用応答が出ない・#718 で追加した routing の非 vacuity 検証)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "            if (p.includes('分解') || p.includes('タスク') || p.includes('手順') || p.includes('ステップ') || p.includes('段取り')) {return 'breakdown';}",
        "replace": "",
        "test": "AI assist routes prompts to troubleshoot/design/breakdown/writing/general",
    },
    {
        "name": "a11y: contact form の autocomplete=name 喪失 (nameInput から autocomplete 除去 → WCAG 1.3.5 の Identify Input Purpose 退行・#722 で追加した属性の非 vacuity 検証)",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": 'placeholder: "お名前", autocomplete: "name",',
        "replace": 'placeholder: "お名前",',
        "test": "Quiz contact form shows validation error on empty submit",
    },
    {
        "name": "a11y: route アナウンスの over-announce gate 喪失 (isRouteChange ガードを外し無条件 announce に戻す → 同一ページ State.update 再描画で route 名を繰り返しアナウンス・WCAG 4.1.3 退行・#727 で追加した gate の非 vacuity 検証)",
        "file": ROOT / "js" / "meta-management.js",
        "find": "        if (isRouteChange) { announceRouteForAccessibility(title); }",
        "replace": "        announceRouteForAccessibility(title);",
        "test": "Same-page State.update does not re-announce the route",
    },
    {
        "name": "a11y: settings 手動追加フォーム 名前入力の label 関連付け喪失 (input の id を除去 → visible <label for> と結び付かず getByLabel が解決不能・WCAG 3.3.2/4.1.2 退行・#728 で追加した関連付けの非 vacuity 検証)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "h('input', { id: 'settingsNewName', class: 'input'",
        "replace": "h('input', { class: 'input'",
        "test": "accessible names via associated labels",
    },
    {
        "name": "a11y: project-detail 先頭セクション見出しの h2 喪失 (先頭 <h2 課題> を <h3> に戻す → h1(project.name)→h3 の見出しレベルスキップ・WCAG 1.3.1 / axe heading-order 退行・#731 で是正した見出しの非 vacuity 検証。first-only replace は先頭 = 課題 見出しに当たる)",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "h('h2', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },",
        "replace": "h('h3', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },",
        "test": "project detail (#/projects/:slug)",
    },
    {
        "name": "behavior: pomodoro 稼働中モード切替が停止しない (switchMode の isActive=false→true) → 切替後もタイマー稼働表示のまま countdown が続く running-timer-with-wrong-mode 退行 (#747 の非 vacuity 検証。mode=mode 行を含む find で switchMode 限定)",
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "                s.appsData.pomodoro.runtime.mode = mode;\n                s.appsData.pomodoro.runtime.isActive = false;",
        "replace": "                s.appsData.pomodoro.runtime.mode = mode;\n                s.appsData.pomodoro.runtime.isActive = true;",
        "test": "switching mode while running",
    },
    {
        "name": "behavior: notes Markdown ## → h4 の 2 段 demote 喪失 (## を h2 要素へ戻す) → preview 内に note 由来 h2 が現れ heading-order/WCAG 1.3.1 崩れ (#748 の 3 レベル demote 非 vacuity 検証)",
        "file": ROOT / "js" / "apps.js",
        "find": "else if (h2) { flushList(); out.push(h('h4', { class: 'h2' }, ..._renderMarkdownInline(h2[1]))); }",
        "replace": "else if (h2) { flushList(); out.push(h('h2', { class: 'h2' }, ..._renderMarkdownInline(h2[1]))); }",
        "test": "demotes all three heading",
    },
    {
        "name": "behavior: brand sanitize の ALLOWED ガード喪失 (return ALLOWED.has(v)?v:DEFAULT を return v へ) → 不正 brand 値 'garbage-not-json' が data-brand にそのまま残り DEFAULT へ fallback しない (#754 の非 vacuity 検証)",
        "file": ROOT / "js" / "brand.js",
        "find": "        return ALLOWED.has(v) ? v : DEFAULT;",
        "replace": "        return v;",
        "test": "recovers gracefully from corrupt",
    },
    {
        "name": "behavior: theme cycle 三項遷移順の破壊 (system?dark:dark?light:system を system?light:... へ) → cycle が system→dark→light→system の順に一周しない (#755 の完全 cycle 順 非 vacuity 検証)",
        "file": ROOT / "js" / "theme.js",
        "find": "const next = current === 'system' ? 'dark' : current === 'dark' ? 'light' : 'system';",
        "replace": "const next = current === 'system' ? 'light' : current === 'dark' ? 'system' : 'dark';",
        "test": "3-state cycle order",
    },
    {
        "name": "behavior: settings upsert import が更新も新規追加も反映しない data-loss (upsert 分岐の Array.from(map.values()) を base.projects.slice() へ) → import した既存更新 + 新規 project が両方消える (#192 data-loss 実バグ regression の非 vacuity 検証)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                            merged.projects = Array.from(map.values());",
        "replace": "                            merged.projects = base.projects.slice();",
        "test": "upsert import updates existing",
    },
    {
        "name": "behavior: FatalPage『ホームへ』復旧の window.render() 明示呼び喪失 (home-route の同一 hash では Router.navigate('') が hashchange 不発火のため再描画されず FatalPage から復旧不能に戻る) → home で fatal 発生時『ホームへ』を押しても FatalPage が残る (#269 実バグ regression の非 vacuity 検証)",
        "file": ROOT / "js" / "components.js",
        "find": "if (typeof window.render === 'function') { window.render(); }",
        "replace": "if (typeof window.render === 'function') { /* #269 mutation: render 抑止 */ }",
        "test": "recovers (home-route)",
    },
    {
        "name": "behavior: pomodoro remainingSec=0 の ingestion round-trip fidelity — store.js normalize の 0 保持を `Number(x) || DEFAULT` footgun へ戻す → valid な remainingSec=0 (pause-at-zero / export・snapshot・cross-tab 由来) が DEFAULT(1500=25:00) に化け、リロード後に 00:00 が 25:00 へ silent に破壊される (0 は falsy ゆえ `||` が正当値を捨てる data-fidelity 実バグ regression の非 vacuity 検証)",
        "file": ROOT / "js" / "store.js",
        "find": "remainingSec: clamp(Number.isFinite(rt.remainingSec) ? rt.remainingSec : CONSTANTS.POMODORO_DEFAULT_REMAINING_SEC, 0, 86400),",
        "replace": "remainingSec: clamp(Number(rt.remainingSec) || CONSTANTS.POMODORO_DEFAULT_REMAINING_SEC, 0, 86400),",
        "test": "restores a persisted remainingSec of 0",
    },
    {
        "name": "behavior: task priority の normalize round-trip — store.js normalizeAppsData の priority 保持を `priority: 'med'` ハードコードへ戻す → 非デフォルト priority (high/low) が reload 後に silent に med へ default される (#294/#568/#684 = normalize が reload で field を drop/default する同 class。add-persist は既定 med・visual retention は同一セッションゆえ素通りする穴の非 vacuity 検証)",
        "file": ROOT / "js" / "store.js",
        "find": "priority: ['low', 'med', 'high'].includes(t.priority) ? t.priority : 'med',",
        "replace": "priority: 'med',",
        "test": "priority change persists across reload",
    },
    {
        "name": "behavior: todo completed の normalize round-trip — store.js normalizeAppsData の `completed: Boolean(t.completed)` を `completed: false` へ戻す → 完了 todo が reload 後に全て active へ silent に戻る (#294/#568/#684/#796 = normalize が reload で field を drop/default する同 class。add-persist/filter/disabled/clear は完了状態を reload 跨ぎで検証しないゆえ素通りする穴の非 vacuity 検証)",
        "file": ROOT / "js" / "store.js",
        "find": "completed: Boolean(t.completed),",
        "replace": "completed: false,",
        "test": "completed state persists across reload",
    },
    {
        "name": "behavior: ai.history の normalize round-trip — store.js normalizeAppsData の ai.history 読み戻し guard を skip させる (`if (Array.isArray(data.ai?.history))` を false && で無効化) → 会話履歴が reload 後に silent 消失する (#294/#568/#684/#796/#797 = normalize が reload で field を drop する同 class。生成テストは同一セッション描画のみゆえ素通りする穴の非 vacuity 検証)",
        "file": ROOT / "js" / "store.js",
        "find": "if (Array.isArray(data.ai?.history)) {",
        "replace": "if (false && Array.isArray(data.ai?.history)) {",
        "test": "conversation history persists across reload",
    },
    {
        "name": "behavior: pomodoro settings.work の normalize round-trip — store.js の `work: clamp(Number(...) || DEFAULT.work, 1, 180)` を `work: DEFAULT.work` ハードコードへ戻す → ユーザ設定の非デフォルト集中時間が reload 後に既定 25 へ silent に戻る (#294/#568/#684/#796/#797/#798 = normalize が reload で field を drop/default する同 class。mode/countdown/reset/interval-resume は非デフォルト settings 値の reload を検証しないゆえ素通りする穴の非 vacuity 検証)",
        "file": ROOT / "js" / "store.js",
        "find": "work: clamp(Number(data.pomodoro.settings.work) || CONSTANTS.POMODORO_DEFAULT_SETTINGS.work, 1, 180),",
        "replace": "work: CONSTANTS.POMODORO_DEFAULT_SETTINGS.work,",
        "test": "non-default settings persist across reload",
    },
    {
        "name": "behavior: h() boolean 子 skip の喪失 — ui-components.js の h() children ループから `typeof child === 'boolean'` skip を除去 → `cond && h(...)` が false のとき createTextNode('false') でリテラル 'false' が描画される実バグ (TodoPage の `filtered.length === 0 && h('p',…)` が todo 存在時に false → リスト末尾に可視 'false'。screenshot は advisory ゆえ素通りしていた) の非 vacuity 検証",
        "file": ROOT / "js" / "ui-components.js",
        "find": "if (child === undefined || child === null || typeof child === 'boolean') {return;}",
        "replace": "if (child === undefined || child === null) {return;}",
        "test": "does not render a literal",
    },
    {
        "name": "behavior: MAX_TASKS 件数上限切り詰めの喪失 — store.js normalizeAppsData の tasks `.slice(0, CONSTANTS.LIMITS.MAX_TASKS)` を除去 → import/cross-tab/snapshot 経由の巨大タスク配列が上限 500 で切り詰められず localStorage を bloat させ描画を重くする DoS ガードの喪失。文字列長 bound(#230) は test 済だが件数上限(MAX_TASKS/MAX_TODOS/MAX_PROJECTS)は未被覆だった穴の非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": "                .slice(0, CONSTANTS.LIMITS.MAX_TASKS);",
        "replace": "                ;",
        "test": "truncates tasks to MAX_TASKS",
    },
    {
        "name": "behavior: MAX_TODOS 件数上限切り詰めの喪失 — store.js normalizeAppsData の todos `.slice(0, CONSTANTS.LIMITS.MAX_TODOS)` を除去 → 巨大 todo 配列が上限 1000 で切り詰められず bloat/描画劣化 DoS を招く。tasks(#801) と別の distinct slice 行ゆえ独立に regress しうる穴の非 vacuity 検証",
        "file": ROOT / "js" / "store.js",
        "find": "                .slice(0, CONSTANTS.LIMITS.MAX_TODOS);",
        "replace": "                ;",
        "test": "truncates todos to MAX_TODOS",
    },
    {
        "name": "behavior: settings import の対象 checkbox 選択的 gate の喪失 — settings-page.js の import が `settingsIncludeProjects && Array.isArray(parsed.projects)` から checkbox ガードを外し常時取り込みへ → Projects を OFF にしても import されユーザが意図的に除外したデータを上書きする (#825 で追加した選択的 gate の非 vacuity 検証。gate 除去で skippedProj が公開一覧に出現し count 0 が RED。テストは keptProject visible を先に待ち grid 描画を確定してから absence 検査する非 vacuous 順序)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "if (settingsIncludeProjects && Array.isArray(parsed.projects)) {",
        "replace": "if (Array.isArray(parsed.projects)) {",
        "test": "selective gate",
    },
    {
        "name": "behavior: nav-lab collapse 状態の reload 復元喪失 — components.js isLabOpen() の localStorage 読み戻し `=== 'true'` を常時 false 化 → reload 後に Lab 展開状態が失われ collapsed へ戻る (#826 で追加した field-persist reload round-trip の非 vacuity 検証。read-back 喪失で展開→reload→展開維持が RED)",
        "file": ROOT / "js" / "components.js",
        "find": "return localStorage.getItem(labKey) === 'true';",
        "replace": "return false;",
        "test": "restores from localStorage across reload",
    },
    {
        "name": "behavior: brand セレクタ UI の localStorage 書き込み喪失 — settings-page.js brand <select> の onchange から Brand.set を除去し window.render() のみへ → UI で選んだ brand が localStorage に書かれず reload 後に復元されない (#828 で追加した producer 側 round-trip の非 vacuity 検証。write 喪失で classic 選択→reload→data-brand 復元が RED)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "onchange: (e) => { Brand.set(e.target.value); window.render(); }",
        "replace": "onchange: (e) => { window.render(); }",
        "test": "UI write round-trip",
    },
    {
        "name": "behavior: notes Markdown inline renderer の複数マーカー逐次処理の喪失 — apps.js _renderMarkdownInline の while ループを if 化し 1 個目のマーカーのみ処理 → 同一行の 2 個目以降の **bold**/`code` とマーカー間/末尾の平文が preview から欠落する (#832 後継の markdown edge coverage。既存テストは 1 bold + 1 code のみで複数マーカー行を未検証だった穴の非 vacuity 検証)",
        "file": ROOT / "js" / "apps.js",
        "find": "while ((m = token.exec(rest)) !== null) {",
        "replace": "if ((m = token.exec(rest)) !== null) {",
        "test": "multiple bold/code markers with interleaved text",
    },
    {
        "name": "behavior: AI analyzeInput の troubleshoot 優先分岐の喪失 — ai-page.js の troubleshoot チェック行を除去 → 「エラー」+「設計」を含む入力が design へ倒れ first-match 優先順位 (troubleshoot>design) が壊れる (複数キーワード一致時の優先順位を pin するテストの非 vacuity 検証。単独キーワードテストは順序入替を素通しする穴を埋める)",
        "file": ROOT / "js" / "ai-page.js",
        "find": "            if (p.includes('エラー') || p.includes('バグ') || p.includes('失敗')) {return 'troubleshoot';}\n",
        "replace": "",
        "test": "first-match priority order",
    },
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
        "find": "email: String(data.profile.email || store.profile.email).slice(0, 254)",
        "replace": "email: String(data.profile.email || store.profile.email)",
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
        "find": "State.updateSilently(s => { s.appsData.quizSearch = val; });",
        "replace": "State.update(s => { s.appsData.quizSearch = val; });",
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
        "find": "if (lastFocused && lastFocused.focus) { try { lastFocused.focus(); } catch (e) { /* noop */ } }",
        "replace": "if (lastFocused && lastFocused.focus) { try { /* focus removed */ } catch (e) { /* noop */ } }",
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
]
