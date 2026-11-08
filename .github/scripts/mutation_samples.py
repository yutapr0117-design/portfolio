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

from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER, NEXT_CHECK, APPLIED_ID, APPLIED_DATE, SUBMISSION_TARGET, FROZEN_PREVIOUS  # noqa: F401 (entry 内で参照)
from mutation_samples_archive import MUTATIONS_ARCHIVE
from mutation_samples_archive5 import MUTATIONS_ARCHIVE5
from mutation_samples_archive4 import MUTATIONS_ARCHIVE4
from mutation_samples_archive3 import MUTATIONS_ARCHIVE3
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
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。










# ── Check 441 (ACD-1.0 ライセンス本文の構造整合と配線) ──────────────────────────
# NOTE: **Check 442 (binary metadata の到達可能性) には mutation を登録できない。**
#   mutation_probe は対象 file を `read_text(encoding="utf-8")` で読むので、WebP / MP3 は
#   UnicodeDecodeError になり適用そのものが成立しない。非 vacuity は 2026-08-23 に手動で
#   実測済 (COMM の size を過大値へ戻す → 442a/442b が RED / RIFF size を 1 ずらす → 442c が RED)。
#   RED を実測できない mutation を安全網に混ぜないための非登録であって、被覆漏れではない。

























































































































































































































_MUTATIONS_TAIL.append({
    "name": "Check 495b: advisory を ceiling より上にする —— 早期警告が鳴らず、いきなり BLOCKING へ飛ぶ",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "LICENSES/AS-OF.md | 130000 | 200000",
    "replace": "LICENSES/AS-OF.md | 210000 | 200000",
})
_MUTATIONS_TAIL.append({
    "name": "Check 495c: 長い行の大きな file を予算から外す —— その file は行数の上限にも当たらず無制限に伸びる",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "LICENSES/ACD-1.0.errata.md | 160000 | 250000\n",
    "replace": "",
})
_MUTATIONS_TAIL.append({
    "name": "Check 495d: 1 つの行に 64 KiB を超えて積む —— runbook §9 のセルが 222 KB になった形",
    "file": ROOT / "docs" / "session-records" / "runbook-check-history.md",
    "find": "# runbook §9「consistency Check 総数」の行にあった追加の経緯（アーカイブ）",
    "replace": "# " + "x" * 70000,
})

_MUTATIONS_TAIL.append({
    "name": "Check 124a: 画面の見出しに実名をローマ字で出す —— 漢字の完全一致だけを見ていた頃は通った (2026-11-08 の監査で実測)",
    "file": ROOT / "js" / "components.js",
    "find": "h('div', { class: 'h4' }, AUTHOR.DISPLAY_NAME),",
    "replace": "h('div', { class: 'h4' }, 'Yuta Yokoi'),",
})

_MUTATIONS_TAIL.append({
    "name": "Check 124a: quiz の設問に実名を書く —— quiz のデータは画面に描画されるのに、js/ 直下しか見ていなかった",
    "file": ROOT / "js" / "quiz" / "aws-quiz-data.js",
    "find": '"title": "Q1. ステータスチェックの厳密な切り分け",',
    "replace": '"title": "Q1. 横井 雄太のステータスチェック",',
})

_MUTATIONS_TAIL.append({
    "name": "Check 124a: aria-label を持つ要素の可視テキストに実名を書く —— 行に aria- があるだけで行全体を許していた",
    "file": ROOT / "js" / "home-page.js",
    "find": "h('ul', { class: 'hero-value-list', 'aria-label': 'Value Points' },",
    "replace": "h('ul', { class: 'hero-value-list', 'aria-label': 'Value Points' }, '横井雄太',",
})

_MUTATIONS_TAIL.append({
    "name": "Check 124a: JS 無効時の説明に実名を出す —— <noscript> は JS を切った読み手に見えるのに走査の外だった",
    "file": ROOT / "index.html",
    "find": "<h1>JavaScript を有効にしてください</h1>",
    "replace": "<h1>Yokoi Yuta のポートフォリオ</h1>",
})

_MUTATIONS_TAIL.append({
    "name": "Check 444k: 画面のフッターのライセンスへのリンクをコメントにする —— 画面から消えるのに、コメントの中の URL で通っていた",
    "file": ROOT / "js" / "components.js",
    "find": (f"            h('div', {{ class: 'p-3' }},\n                h('a', {{\n                    class: 'text-xs text-muted',\n"
             f"                    href: '/portfolio/LICENSES/{APPLIED_ID}.txt',\n                    rel: 'license noopener noreferrer',\n"
             f"                    target: '_blank'\n                }}, 'License: {APPLIED_ID}')\n            )"),
    "replace": (f"            null /* h('div', {{ class: 'p-3' }},\n                h('a', {{\n                    class: 'text-xs text-muted',\n"
                f"                    href: '/portfolio/LICENSES/{APPLIED_ID}.txt',\n                    rel: 'license noopener noreferrer',\n"
                f"                    target: '_blank'\n                }}, 'License: {APPLIED_ID}')\n            ) */"),
})
_MUTATIONS_TAIL.append({
    "name": "Check 123a: 運用モデルの節の見出しから「現在の運用モデル」を外す —— 直前の行コメントがその語を持つので通っていた",
    "file": ROOT / "js" / "ai-knowhow-page.js",
    "find": "                class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': '現在の運用モデル：AI自走運用への進化'\n            },\n                h('div', { class: 'card-body flex flex-col gap-3' },\n                    sectionHeader('🔄', '現在の運用モデル — 対話型から AI 自走運用への進化', C.primary),",
    "replace": "                class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': '運用の記録：AI自走運用への進化'\n            },\n                h('div', { class: 'card-body flex flex-col gap-3' },\n                    sectionHeader('🔄', '運用の記録 — 対話型から AI 自走運用への進化', C.primary),",
})

_MUTATIONS_TAIL.append({
    "name": "Check 463: 送る文面の法的レビューの段落を HTML コメントに隠す —— 描画されず送られないのに、生の markdown で照合して通っていた",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "**Legal review: none.** No lawyer has drafted or read it.",
    "replace": "<!-- **Legal review: none.** No lawyer has drafted or read it. -->",
})

_MUTATIONS_TAIL.append({
    "name": "Check 463: 送る文面から「新規か legacy か」の行を消す —— 申請日の 1 枚は要件に持つのに、§B.0 の照合には無かった",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "Legacy or New:                  New License\nDrafted By Lawyer:              No\nApproved or Used by Projects:   One — my own repository",
    "replace": "Drafted By Lawyer:              No\nDrafted By Lawyer:              No\nApproved or Used by Projects:   One — my own repository",
})

_MUTATIONS_TAIL.append({
    "name": "Check 468: §8.4 から「Section 8.1 alone governs」の alone を落とす —— 付け足した機能に §8.4 が及ぶかの線が消える (468u の目印)",
    "file": CURRENT_DRAFT,
    "find": "remove. Section 8.1 alone governs a feature added to the Work, by",
    "replace": "remove. Section 8.1 governs a feature added to the Work, by",
})

_MUTATIONS_TAIL.append({
    "name": "Check 444n: REUSE.toml の全 file への宣言を前の版へ戻す —— 2026-09-23〜11-08 に実際にこの状態だった (どの Check も読んでいなかった)",
    "file": ROOT / "REUSE.toml",
    "find": f'SPDX-License-Identifier = "LicenseRef-{APPLIED_ID}"',
    "replace": 'SPDX-License-Identifier = "LicenseRef-ACD-1.0"',
})

_MUTATIONS_TAIL.append({
    "name": "Check 238: og:image の 2 本目を属性の順序を変えて足す —— 先頭しか読まない Check 153 には見えず、旧 238 は属性順を固定していた",
    "file": ROOT / "index.html",
    "find": '    <meta property="og:image" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />',
    "replace": ('    <meta property="og:image" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />'
                '<meta content="https://example.com/other.webp" property="og:image" />'),
})
_MUTATIONS_TAIL.append({
    "name": "Check 238: ai:canonical の 2 本目を別の URL で足す —— 先頭しか読まない Check 282 には見えない",
    "file": ROOT / "index.html",
    "find": '    <meta name="ai:canonical" content="https://yutapr0117-design.github.io/portfolio/" />',
    "replace": ('    <meta name="ai:canonical" content="https://yutapr0117-design.github.io/portfolio/" />'
                '<meta name="ai:canonical" content="https://example.com/" />'),
})

_MUTATIONS_TAIL.append({
    "name": "Check 17: SITE_CONFIG の直前のコメントに旧い値を残したまま LAST_UPDATED を進める —— コメント込みの先頭一致で読むと、コメントの値が比べられて通っていた (値は v74 の間は変わらない)",
    "file": ROOT / "main.js",
    "find": "        const SITE_CONFIG = {\n            VERSION:       'v74',\n            LAST_UPDATED:  '2026-05-31',",
    "replace": "        // 旧: LAST_UPDATED:  '2026-05-31', VERSION:       'v74',\n        const SITE_CONFIG = {\n            VERSION:       'v74',\n            LAST_UPDATED:  '2026-06-01',",
})
_MUTATIONS_TAIL.append({
    "name": "Check 2: SITE_CONFIG の直前のコメントに旧い値を残したまま VERSION を進める —— 同じ形で版数の同期が見えなかった (Check 177 も同じ理由で発火する)",
    "file": ROOT / "main.js",
    "find": "        const SITE_CONFIG = {\n            VERSION:       'v74',",
    "replace": "        // 旧: VERSION:       'v74',\n        const SITE_CONFIG = {\n            VERSION:       'v75',",
})

_MUTATIONS_TAIL.append({
    "name": "Check 444a: 旧い版を指す rel=license を先頭に足す —— 先頭の 1 本が実 file へ解決するかだけを見ていた頃は通った (1.0 の全文も実在する)",
    "file": ROOT / "index.html",
    "find": f'<link rel="license" href="/portfolio/LICENSES/{APPLIED_ID}.txt" />',
    "replace": f'<link rel="license" href="/portfolio/LICENSES/ACD-1.0.txt" /><link rel="license" href="/portfolio/LICENSES/{APPLIED_ID}.txt" />',
})
_MUTATIONS_TAIL.append({
    "name": "Check 444c: manifest の SPDX 式だけを前の版へ戻す —— spdx_id と url しか比べず、同じブロックの中で版が 2 つになっても通った",
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": f'"conforming_spdx_expression": "LicenseRef-{APPLIED_ID}",',
    "replace": '"conforming_spdx_expression": "LicenseRef-ACD-1.0",',
})
_MUTATIONS_TAIL.append({
    "name": "Check 444d: robots.txt で全文を Disallow する —— 全文は sitemap の <loc> しか見ておらず、robots を読まなかった",
    "file": ROOT / "robots.txt",
    "find": f"Allow: /portfolio/LICENSES/{APPLIED_ID}.txt\n",
    "replace": f"Disallow: /portfolio/LICENSES/{APPLIED_ID}.txt\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 444e: llms-full.txt の宣言の文だけを別の版にする —— 識別子が file のどこかに 1 回あれば通った",
    "file": ROOT / "llms-full.txt",
    "find": f"Dedication {APPLIED_ID.split('-')[1]} ({APPLIED_ID})**",
    "replace": "Dedication 1.0 (ACD-1.0)**",
})
_MUTATIONS_TAIL.append({
    "name": "Check 444f: route 追従ノードの license を前の版にする —— SITE_CONFIG の定義行が常に満たしたので、ノードの値は見られていなかった",
    "file": ROOT / "main.js",
    "find": f"'license': SITE_BASE + 'LICENSES/{APPLIED_ID}.txt',",
    "replace": "'license': SITE_BASE + 'LICENSES/ACD-1.0.txt',",
})
_MUTATIONS_TAIL.append({
    "name": "Check 444h: sitemap の唯一の <image:license> を消す —— 0 件のとき else が無く、画像のライセンス宣言が消えても通った",
    "file": ROOT / "sitemap.xml",
    "find": f"<image:license>https://yutapr0117-design.github.io/portfolio/LICENSES/{APPLIED_ID}.txt</image:license>",
    "replace": "",
})
_MUTATIONS_TAIL.append({
    "name": "Check 451c: manifest の attribution_required の鍵を改名する —— manifest 側が欠けると比較を飛ばし、答えが消えても OK だった",
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '"attribution_required": false,',
    "replace": '"attribution_required_x": false,',
})

_MUTATIONS_TAIL.append({
    "name": "Check 441b: 草案の Section 11 への参照を存在しない Section 19 にする —— 凍結した 1.0 しか読まず、動く唯一の本文を見ていなかった",
    "file": CURRENT_DRAFT,
    "find": "Nothing in Section 11 reduces what any other Section of this",
    "replace": "Nothing in Section 19 reduces what any other Section of this",
})

_MUTATIONS_TAIL.append({
    "name": "Check 441c: 草案の定義語を改名して未使用にする —— 定義が残骸になっても、1.0 だけを読む頃は通った",
    "file": CURRENT_DRAFT,
    "find": '  1.2  "Moral Rights" means',
    "replace": '  1.2  "Author Rights" means',
})

_MUTATIONS_TAIL.append({
    "name": "Check 441g: 草案に組織名を英語の通称で書く —— Nihon Keiei / nkgr の綴りしか見ていなかった",
    "file": CURRENT_DRAFT,
    "find": "and Section 10.5 applies.",
    "replace": "and Japan Management applies.",
})

_MUTATIONS_TAIL.append({
    "name": "Check 441g: 草案に複数語の置換テキスト <your name> を入れる —— 置換テキストの照合が空白で止まり、§16.1 の例外も正規表現の偶然で通っていた",
    "file": CURRENT_DRAFT,
    "find": "except by the Steward (Section 16.5), and by",
    "replace": "except by <your name> (Section 16.5), and by",
})

_MUTATIONS_TAIL.append({
    "name": "Check 468: §16.2 の通知の主語「a Dedicator」を落とす —— タグを残しただけの取り込み手まで通知の適用に入る (468u の目印)",
    "file": CURRENT_DRAFT,
    "find": "accompanies the work. A notice a Dedicator places applies this",
    "replace": "accompanies the work. A notice placed applies this",
})

_MUTATIONS_TAIL.append({
    "name": "Check 496: CHANGELIST の表の見出しから「件数」の列を外す —— 行は 4 セルのままなので、GFM は 4 列目を描かずに捨てる (2026-11-08 まで実際にこの状態だった)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md",
    "find": "| レンズ | やったこと | 結果 | 件数 |",
    "replace": "| レンズ | やったこと | 結果 |",
})

_MUTATIONS_TAIL.append({
    "name": "Check 472n: register の英語の索引で、B1 を述べる Piana 氏の引用を読みやすく動かす —— register は入口の照合の外だった (2026-11-08 に加えた)",
    "file": ROOT / "LICENSES" / "ACD-OSI-BOTTLENECKS.md",
    "find": '*"OSI requires prior review by a lawyer"*',
    "replace": '*"OSI requires a prior review by a lawyer"*',
})

MUTATIONS = MUTATIONS_ARCHIVE5 + MUTATIONS_ARCHIVE4 + MUTATIONS_ARCHIVE3 + MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。




























































_E2E_TAIL.append({
    "name": "HTML 標準の license リンクが消える —— rel=license は権利宣言の最も標準的な入口で、"
            "JSON-LD を読まないツール (ライセンススキャナ等) にとっては唯一の手掛かり",
    "file": ROOT / "index.html",
    "find": f'<link rel="license" href="/portfolio/LICENSES/{APPLIED_ID}.txt" />',
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

_E2E_TAIL.append({
    "name": "sidebar の nav リンクが指すルートを 1 つ router から落とす —— 利用者にはナビを押すと "
            "NotFound が出るだけに見える。この gate は 2026-08-24 まで **前ルートの DOM に対して "
            "不在アサーションを評価**しており、自分が名乗っている「壊れた nav リンク」を一度も "
            "検出できなかった (遷移直後の NotFound 見出し 0 件で PASS・settle 後は 1 件)",
    "file": ROOT / "js" / "router.js",
    "find": "            case 'role-split':\n                route.name = 'role-split';",
    "replace": "            case 'role-split-DISABLED':\n                route.name = 'role-split';",
    "test": "All sidebar nav links resolve to valid",
})

_E2E_TAIL.append({
    "name": "quiz の章見出しを h2 -> h4 にして heading-order を壊す —— 長い読み物の見出し階層が"
            "飛ぶと、スクリーンリーダーの主要移動手段である見出しジャンプで本文を辿れなくなる。"
            "この違反は 2026-08-24 まで **ダーク走査から構造的に見えなかった**: ループの待ちが汎用で"
            "前ルートの DOM で成立していたため、axe はちょうど 1 つ前のルートを走査しており "
            "`#/quiz` (最大のコンテンツページ) は一度も走査されていなかった (実測: 同じ違反を"
            "注入して旧待ちでは PASS・新待ちでは `#/quiz: heading-order(1)` で FAIL)",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"h2\", { class: \"quiz-section-title\" }, section));",
    "replace": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"h4\", { class: \"quiz-section-title\" }, section));",
    "test": "ダークテーマの全ルート",
})

_E2E_TAIL.append({
    "name": "quiz の章カードに min-width を与えて 320px であふれさせる (WCAG 1.4.10)。この違反は "
            "2026-08-24 まで **reflow の走査から構造的に見えなかった**: ループの待ちが汎用で前ルートの "
            "DOM で成立していたため、6 ルート全てが `#/role-split` を測っており、#962 で直した実バグの "
            "対象 (quiz / hiring-risk / pomodoro) は一度も測られていなかった",
    "file": ROOT / "style.css",
    "find": ".quiz-section-card {",
    "replace": ".quiz-section-card { min-width: 420px;",
    "test": "320px 幅でどのルートも横スクロールしない",
})

_E2E_TAIL.append({
    "name": "AI 応答到着時のルート判定を潰す —— 応答は submit の 300ms 後に非同期で届くので、"
            "その間に別アプリへ移っているのは普通にある。ルートを見ずに State.update すると "
            "notify → #content の全再描画が起き、**操作していない画面の未送信入力が消える** "
            "(実測: AI-INTERRUPT-DRAFT → \"\")。#994 の focus 復元が id で働くぶん "
            "**activeElement は残って値だけ消える**ので、利用者は原因に見当がつかない。"
            "#982 / #1055 / #1056 と同じ class",
    "file": ROOT / "js" / "ai-page.js",
    "find": "if (onAiRoute) { State.update(applyResponse); }",
    "replace": "if (true) { State.update(applyResponse); }",
    "test": "別アプリで入力中のテキストを消さない",
})

_E2E_TAIL.append({
    "name": "「全リセット」を appsData だけ戻す部分リセットへ退行させる —— projects / profile / "
            "theme / projectPrefs が残る。**「全」と名乗る操作が一部しか戻さない**のは、利用者が"
            "「初期化した」と信じて元データを捨てうる silent failure。実測 (2026-08-26): "
            "pomodoro/quiz/notes を見る multi-app リセット test も、AI 応答待ち中のリセット test も"
            "**appsData しか見ないので素通り**する。捕捉層は apps-settings-io の 2 件だけだった",
    "file": ROOT / "js" / "settings-page.js",
    "find": "State.set(Store.createDefaultStore());",
    "replace": "State.set({ ...State.get(), appsData: Store.createDefaultStore().appsData });",
    "test": "表示テーマが export → import で復元され",
})

_E2E_TAIL.append({
    "name": "theme を「値が変わらなくても applied に数える」形へ戻す —— フルバックアップには "
            "**必ず theme が入る**ので、この 1 行だけで #1040 の「0 セクションなら成功と言わない」"
            "ガードが最も一般的なファイル形式に対して丸ごと無効化される。実測 (2026-08-26): "
            "対象 3 つを全て外して読み込むと state は前後で完全に同一なのに「完了しました」と出る。"
            "既存の #1040 test は theme を含まない `AppsDataのみ` を使うためこの枝を踏めない",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (parsed.theme !== base.theme) { applied = true; }",
    "replace": "                    applied = true;",
    "test": "フルバックアップでも、対象を全部外したら成功と report しない",
})


_E2E_TAIL.append({
    "name": "`Projectsのみ` の書き出しを projects の素の配列へ戻す —— 既定プロジェクトは削除できず "
            "**「非表示」が唯一の非公開手段** (#886) なのに、このファイルから復元すると "
            "隠したプロジェクトが黙って再公開される。フルバックアップは #1037 で projectPrefs を "
            "含むよう直したのに、部分 export だけ取り残されていた形 (実測 2026-08-26)",
    "file": ROOT / "js" / "settings-io.js",
    "find": "downloadJSON({ projects: s.projects, projectPrefs: s.projectPrefs },",
    "replace": "downloadJSON(s.projects,",
    "test": "Projectsのみ の往復で非表示設定が戻る",
})


_E2E_TAIL.append({
    "name": "貼り付けが maxlength で切られたことを黙らせる (通知条件を殺す) —— **打鍵は「入らなく"
            "なる」のが見えるが貼り付けは無反応**。実測 (2026-08-26): タスク入力へ 500 文字を貼ると "
            "200 文字だけ残り 300 文字が通知ゼロで消えた。既定動作は妨げず報告だけを足す設計なので、"
            "この条件を殺すと**元の silent な消失に戻る**",
    "file": ROOT / "js" / "ui-components.js",
    "find": "        if (dropped > 0) {",
    "replace": "        if (false) {",
    "test": "上限を超える貼り付けは、消えた文字数を通知する",
})


_E2E_TAIL.append({
    "name": "スナップショットの上書き確認を無効化する —— スロットは**単一**なので 2 度目の「保存」は "
            "前の内容を消して現在の状態で置き換える = **削除と同じく不可逆**。clearSnapshot は "
            "#1185 で confirm を得たのに**上書きだけ取り残されていた** (実測 2026-08-26: 2 回目の "
            "クリックで dialog ゼロのまま保存日時が置き換わった)。壊れた状態を実験したあと反射的に "
            "「保存」を押すと、**戻るはずだった良い状態を自分で消す**",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (_prev) {",
    "replace": "            if (false) {",
    "test": "スナップショットの上書きは確認を求め、キャンセルすると元が残る",
})


_E2E_TAIL.append({
    "name": "全置換 (strict) モードの取り込み確認を無効化する —— **最も破壊的な経路**なのに、"
            "プロジェクト 1 件の削除も全リセットもスナップショットの削除・上書きも confirm を通すのに"
            "ここだけ素通りしていた (実測 2026-08-26: dialog ゼロで既存タスクが消えた)。"
            "**モードは遷移を跨いで残る**ので、一度 strict にした利用者が後で別のファイルを"
            "取り込むときに選択を覚えていない、という現実的な経路がある",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                if (settingsImportMode === 'strict') {\n                    if (!confirm(",
    "replace": "                if (false) {\n                    if (!confirm(",
    "test": "全置換モードの取り込みは確認を求め、キャンセルすると既存データが残る",
})


_E2E_TAIL.append({
    "name": "プロジェクト削除の確認文から**対象の名前**を落とす —— 成功 Toast は名前を出すのに "
            "確認が「本当に削除しますか？」だけだと、**一覧で行を押し間違えても気付けない** "
            "(名前が出るのは消えた後)。#1185 が「文言は何を失うかを明示する」と原則を書いたのに、"
            "その比較対象だった当の削除が取り残されていた",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (!confirm(_target && _target.name",
    "replace": "            if (!confirm(false && _target && _target.name",
    "test": "Deleting a user project (confirm accepted) removes it everywhere",
})


_E2E_TAIL.append({
    "name": "全リセットの確認文から「元に戻せません／スナップショットは残ります」を落とす —— "
            "**何を失い何が残るかを言わない確認は判断材料にならない**。残るものを伝えるほうが"
            "利用者は判断できる (消える恐れで踏みとどまる必要が無くなる)。#1185 が書いた"
            "「文言は何を失うかを明示する」原則の、全リセット面",
    "file": ROOT / "js" / "settings-page.js",
    "find": "                + '元に戻せません。スナップショットは残ります。')) {return;}",
    "replace": "                + '')) {return;}",
    "test": "全リセットの確認文は、元に戻せないことと残るものを伝える",
})


_E2E_TAIL.append({
    "name": "取り込み失敗の文言から**受け付ける形式の案内**を落とす —— 利用者はこのアプリ自身が"
            "書き出したファイルを読み込もうとして失敗しており、「失敗した」だけでは**次の一手が"
            "無い行き止まり**になる。受け付ける 4 形式はアプリ自身が知っているのだから伝える",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    Toast.show('認識できない形式のファイルです。'",
    "replace": "                    Toast.show('認識できない形式のファイルです', 'error'); if (0) Toast.show('x'",
    "test": "認識できない形式の JSON は成功と report しない",
})

_E2E_TAIL.append({
    "name": "スキーマ移行の通知を落とす —— 版数が変わったデプロイで**全データが既定へ戻る**のに、"
            "消えたことも復元できることも伝えない状態に戻す。退避先は作られているので救えるのに、"
            "利用者からは「開いたら全部消えていた」としか見えず復元導線へ辿り着けない",
    "file": ROOT / "js" / "state.js",
    "find": "const _migration = Store.takeMigrationNotice ? Store.takeMigrationNotice() : null;",
    "replace": "const _migration = null;",
    "test": "Schema migration tells the user what was reset",
})

_E2E_TAIL.append({
    "name": "スナップショットの由来判定を潰す —— 移行時の自動退避を「手動で保存」と表示させる。"
            "自動退避は load 時に走るため確認を挟めず手動保存を黙って上書きするので、由来を"
            "誤って表示すると利用者は自分の復元点が残っていると誤解したまま別物を復元する",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (snap.reason === 'schema-mismatch') {",
    "replace": "            if (false) {",
    "test": "自動退避されたスナップショットは移行元と移行先を示す",
})

_E2E_TAIL.append({
    "name": "brand の取り込みを落とす —— 「フルバックアップ」に配色が入っていても復元されない"
            "状態に戻す。brand は store の外なので merged に載せても normalize が落とす。theme が"
            "戻るのに brand だけ戻らない非対称は利用者から見て「フル」の約束破り",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                if (typeof parsed.brand === 'string' && Brand && Brand.set) {",
    "replace": "                if (false) {",
    "test": "配色 (brand) が export → import で復元される",
})

_E2E_TAIL.append({
    "name": "書き出しの成功通知を落とす —— ファイルは落ちるのに何も報告しない状態に戻す。"
            "他の操作は全て報告するのに書き出しだけ黙る非対称で、SR 利用者は成否を知る手段が"
            "無い (WCAG 4.1.3)。バックアップは「取れたつもり」が最も危ない",
    "file": ROOT / "js" / "settings-io.js",
    "find": "            Toast.show(`${filename} を書き出しました`);",
    "replace": "            void filename;",
    "test": "書き出しは成功を報告する",
})
_E2E_TAIL.append({
    "name": "書き出しの失敗を握り潰さず再送出する —— 修正前の挙動に戻す。例外がそのまま致命"
            "エラーへ昇格し FatalPage と全画面オーバーレイで Settings が消える＝**バックアップを"
            "取ろうとして画面を失う**。失敗の伝え方として最悪の形",
    "file": ROOT / "js" / "settings-io.js",
    "find": "            Toast.show('書き出しに失敗しました。ブラウザのダウンロード設定を確認してください。', 'error', 5000);",
    "replace": "            throw e;",
    "test": "書き出しが失敗しても致命エラーにせず理由を伝える",
})

_E2E_TAIL.append({
    "name": "リセットの通知を落とす —— 押してもボタン名は変わらず、タイマーは意図的に非 live"
            "なので、結果だけ変わって無音になる。見えない利用者にはリセットできたのかどうかが"
            "分からない (開始/一時停止はラベル、モード切替は aria-pressed が変化を伝える)",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "            announce(`${label}のタイマーをリセットしました。残り ${formatTime(duration)}`);",
    "replace": "            void label;",
    "test": "リセットは結果を支援技術へ伝える",
})



_E2E_TAIL.append({
    "name": "nav リンク自身の closeDrawer を落とす —— 別ルートへの遷移は hashchange の配線 (#998) が"
            "閉じるので気付けないが、**今いるページのリンクを押したとき**は hash が変わらず hashchange が"
            "発火しないため drawer が開いたまま残る。モバイルでは画面を覆うので、メニューを閉じるつもりの"
            "普通の操作で閉じなくなる",
    "file": ROOT / "js" / "components.js",
    "find": "                    if (isDrawer) { closeDrawer(); }",
    "replace": "                    if (false) { closeDrawer(); }",
    "test": "今いるページの nav リンクを押しても drawer は閉じる",
})
_E2E_TAIL.append({
    "name": "詳細ページの「一覧に戻る」が絞り込みを捨てる —— router が戻り先を query 込みで保持する"
            "単一ソース (#951) を潰す。1 件に絞り込んだ状態から戻ると全件に戻り、利用者は同じ意味の"
            "操作 (ブラウザの戻る) との食い違いに気付けない",
    "file": ROOT / "js" / "router.js",
    "find": "        if (raw === 'projects' || raw.startsWith('projects?')) { _lastListPath = raw; }",
    "replace": "        if (raw === 'projects' || raw.startsWith('projects?')) { _lastListPath = 'projects'; }",
    "test": "In-page \"back to list\" preserves the active filter",
})

_E2E_TAIL.append({
    "name": "カテゴリ絞り込みの URL 同期を落とす —— 画面上は絞り込まれるのに URL に残らないので、"
            "共有したリンクや再読み込みで全件へ戻る。絞り込みは「今見ている範囲」そのものなので、"
            "URL に出ないと共有も復元もできない",
    "file": ROOT / "js" / "projects-page.js",
    "find": "                if (cat !== 'All') {params.set('cat', cat);}",
    "replace": "                if (false) {params.set('cat', cat);}",
    "test": "Projects category filter narrows the list and syncs to the URL",
})
_E2E_TAIL.append({
    "name": "nav リンクの aria-current を落とす —— 支援技術に「今どのページにいるか」が伝わらなくなる"
            "(WCAG 2.4.8)。視覚的な強調は class で別に付くので**目では気付けない**。sidebar と drawer は"
            "同じ実装を共有するが、mobile では drawer が唯一のナビなので両方が守られる必要がある",
    "file": ROOT / "js" / "components.js",
    "find": "                'aria-current': item.active ? 'page' : undefined",
    "replace": "                'aria-current': undefined",
    "test": "モバイルの drawer が現在ルートに aria-current を付け、遷移に追従する",
})

_E2E_TAIL.append({
    "name": "初回描画の route-focus ガードを外す —— ページを開いただけで h1 へ focus が移り、2px の枠が出て、"
            "最初の Tab が skip-link とナビを飛ばして本文へ着地する (2026-11-02 まで全ルートでこの状態だった)",
    "file": ROOT / "main.js",
    "find": "            if (isRouteChange && _hasRenderedOnce && content && _focusWasLost) {",
    "replace": "            if (isRouteChange && content && _focusWasLost) {",
    "test": "初回表示では focus を動かさず、最初の Tab は skip-link に届く",
})

_E2E_TAIL.append({
    "name": "about の Speakable が幻セレクタ [data-speakable] を宣言し直す — その属性は home の hero にしか無く、他ルートでは一度も対象を持たない (2026-11-03 まで実際にそうだった)。機械向けの面なので視覚にも他のテストにも出ない",
    "file": ROOT / "js" / "meta-management.js",
    "find": "            'about':       ['h1', '.sr-only'],",
    "replace": "            'about':       ['h1', '[data-speakable]', '.sr-only'],",
    "test": "Every non-home Speakable cssSelector resolves to real elements (AIO accuracy)",
})
_E2E_TAIL.append({
    "name": "quiz の未知 ?type= で title だけ汎用「Quiz」へ戻る —— 描画 (AWS 問題集) / sidebar nav (AWS active) と title が食い違う 2026-11-03 以前の状態",
    "file": ROOT / "js" / "page-meta.js",
    "find": "            return Object.prototype.hasOwnProperty.call(map, type) ? map[type] : map.aws;",
    "replace": "            return Object.prototype.hasOwnProperty.call(map, type) ? map[type] : 'Quiz';",
    "test": "Quiz document.title stays in the known-safe set for ?type=",
})
E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE3 + E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL
