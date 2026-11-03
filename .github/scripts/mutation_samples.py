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

from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER  # noqa: F401 (entry 内で参照)
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
    "name": "Check 487b: STATUS の「AIO 監視の実測」が監視スクリプトの書かない status を数える (2026-11-02 の初版そのもの)",
    "file": ROOT / ".github" / "scripts" / "generate_status.py",
    "find": '_MEASURED_STATUSES = ("ok",)',
    "replace": '_MEASURED_STATUSES = ("cited", "not_cited")',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 468s: CHANGELIST の変更表に語数 +1 の行が 1 つ増える —— 表と草案の申告がずれても 468n は見ない",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |\n| :-- | :-- | :-- | :-- | :-- |",
    "replace": "| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |\n| :-- | :-- | :-- | :-- | :-- |\n| (mutation) | x | x | +1 | x |",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 469 (c): READY-TO-SUBMIT の部数申告が実装に追従しない —— 451d / 451e を足したあとも「3 部」のままだった 2026-11-03 以前の状態 (469 (c) が捕捉)",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "| Check 451 (",
    "replace": "| Check 451 (9 部) (",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (b): 索引が FAQ の「使う側」の問数を 1 つ多く申告する (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.review-responses.md",
    "find": "問 / プロセス",
    "replace": "問 ／ プロセス",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (c): 逐条リファレンスが条数を 1 つ多く申告する (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.clause-reference.md",
    "find": "全 16 節 82 条",
    "replace": "全 16 節 83 条",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (d): FAQ の mirror が「使う側」の問数を 1 つ少なく申告する (face 単位の帰属・2026-11-03)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "ACD-1.0.faq.md.md",
    "find": "**A. 使う側**（",
    "replace": "**A. 使う側** （",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (f): QUESTION-INDEX が worked entry の総数を手で足し引きしてずれる (実際に 2 ずれていた形) (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "QUESTION-INDEX.md",
    "find": "There are **",
    "replace": "There are  **",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (h): mirror がドシエの規模を数字で述べる (mirror の数は維持できないので禁止) (face 単位の帰属・2026-11-03)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "ACD-1.0.faq.md.md",
    "find": "**A. 使う側**（",
    "replace": "All 99 adverse facts. **A. 使う側**（",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (i): §4c が不利な事実の件数を 1 つ少なく述べる (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-reference.md",
    "find": " entries, 1–",
    "replace": " entries 1–",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (j): §1.35 の「N のうち M」が下の列挙と合わない (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.comparison.md",
    "find": " distinguishing features",
    "replace": " distinguishing  features",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (k): ドシエの #N 参照が不利な事実のどの行にも解決しない (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "#195",
    "replace": "#9195",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (l): errata 冒頭の件数が表の行数と合わない (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.errata.md",
    # find は件数の語に釘付けにしない —— 件数は errata を足すたびに変わり anchor が orphan になる
    # (2026-11-03 に E59 で実際に orphan 化)。動かない E2 の行頭を崩して表の行数を 1 減らす。
    "find": "\n| E2 | ",
    "replace": "\n|E2 | ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (o): 入口ページの最高 severity の件数が register の表と合わない (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": " are marked highest severity",
    "replace": " are marked as highest severity",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (p): §B.0 の見出しの語数が本文の実測と合わない (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "### B.0 The message as it should actually be sent (**",
    "replace": "### B.0 The message as it should actually be sent (~**",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (q): 審査者に示す検証コマンドの期待値が実際の出力件数と合わない (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": "× OK",
    "replace": "× OK (and 99× OK)",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (r): §B.0 の語数を日付も「見出しが権威」の断りも無い現在形で写す (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "**したがって §B.0 は",
    "replace": "**したがって §B.0（1,703 語）は",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (s): 散文が Check 463 の強制項目数を実装と違う数で述べる (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.review-rules.md",
    "find": "Check 463（**",
    "replace": "Check 463（**99 項目 / ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (a): 提出パケットが worked entries の件数を 1 つ多く申告する (face 単位の帰属・2026-11-03)",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": " worked entries plus a table of ",
    "replace": " worked entries and a table of ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 424c: §2 表に同じ path の行が 2 つになる —— 予算列や理由が食い違い、rotate と照合で片方が必ず古くなる (2026-11-03 まで e2e_archive3 がそうだった)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "| `.github/scripts/mutation_samples_common.py` |",
    "replace": "| `.github/scripts/mutation_samples_common.py` | 28 | 60 | `advisory` | mutation_samples / archive 共有パス定数 (ROOT / CHECK)。循環回避 |\n| `.github/scripts/mutation_samples_common.py` |",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 469 (b): errata の E-ID が CHANGELIST の表と対応しなくなる (E58 → E59) —— 閉じた / 未着手の照合から 1 件が黙って外れる",
    "file": ROOT / "LICENSES" / "ACD-1.0.errata.md",
    "find": "| E58 |",
    "replace": "| E59 |",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 479c: Check 460 に face を 1 つ足し、その face を名指す mutation を足さない —— 週次 probe はその面を一度も壊して確かめない",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": "        # (w) 質問集を名指す行",
    "replace": "        # (z) (mutation)\n        # (w) 質問集を名指す行",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 479d: Check 424 に下位部 424z を足し、それを名指す mutation を足さない —— 週次 probe はその下位部を一度も壊して確かめない",
    "file": ROOT / ".github" / "scripts" / "checks_size_budget.py",
    "find": "        # 424c: §2 の path は一意。",
    "replace": "        # Check 424z (mutation)\n        # 424c: §2 の path は一意。",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 50b: package.json の lint script に eslintrc 時代のフラグを戻す —— ESLint 9.x はそのフラグを持たず lint が config 無しで走る / 落ちる",
    "file": ROOT / "package.json",
    "find": "\"lint\": \"eslint ",
    "replace": "\"lint\": \"eslint --no-eslintrc ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 50d: eslint.config.mjs から no-dupe-keys が消える —— recommended を継承しない方針なので、明示しないと重複キーの bug-catcher が CI から黙って抜ける (#186 の class)",
    "file": ROOT / "eslint.config.mjs",
    "find": "      'no-dupe-keys': 'error',",
    "replace": "      'no-dupe-keys-x': 'error',",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 449b: api-catalog の link object に関係型 (service-desc) を attribute として混ぜる —— RFC 9264 では関係型は attribute ではなく、仕様に従う agent は別の意味に読む",
    "file": ROOT / ".well-known" / "api-catalog",
    "find": "          \"type\": \"text/plain\"\n",
    "replace": "          \"type\": \"text/plain\",\n          \"service-desc\": \"x\"\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 449c: api-catalog の link object の href が文字列でなくなる —— 解決できない link を agent に渡す",
    "file": ROOT / ".well-known" / "api-catalog",
    "find": "          \"href\": \"https://yutapr0117-design.github.io/portfolio/llms-full.txt\",\n          \"type\": \"text/plain\"",
    "replace": "          \"href\": 1,\n          \"type\": \"text/plain\"",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 426a: portfolio:identity:canonical-url が ai:canonical と食い違う —— どの Check も e2e も見ていなかった meta (#1093)",
    "file": ROOT / "index.html",
    "find": "<meta name=\"portfolio:identity:canonical-url\" content=\"https://yutapr0117-design.github.io/portfolio/\">",
    "replace": "<meta name=\"portfolio:identity:canonical-url\" content=\"https://yutapr0117-design.github.io/portfolio/x/\">",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 426b: 画像資産の権威コンテキスト URL が ai:context と食い違う",
    "file": ROOT / "index.html",
    "find": "<meta name=\"asset:image:ai-context\" content=\"https://yutapr0117-design.github.io/portfolio/llms-full.txt\" />",
    "replace": "<meta name=\"asset:image:ai-context\" content=\"https://yutapr0117-design.github.io/portfolio/llms.txt\" />",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 426c: 2 つのバイナリ資産の帰属先 (entity) が食い違う",
    "file": ROOT / "index.html",
    "find": "<meta name=\"asset:audio:entity\" content=\"Yuta Yokoi (横井雄太 / Yokoi Yuta)\" />",
    "replace": "<meta name=\"asset:audio:entity\" content=\"Yuta Yokoi\" />",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 73a: preload から as= が外れる —— ブラウザは as の無い preload を正しい優先度で取得できず、二重取得になる",
    "file": ROOT / "index.html",
    "find": "<link rel=\"preload\" as=\"style\" href=\"https://fonts.googleapis.com/css2?family=Inter",
    "replace": "<link rel=\"preload\" href=\"https://fonts.googleapis.com/css2?family=Inter",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 73b: alt の無い <img> が index.html に入る —— 静的な <img> は今 0 件で 73b は対象 0 件のまま OK を返していた。入ってきたときに捕まえることを確かめる (WCAG 1.1.1)",
    "file": ROOT / "index.html",
    "find": "    <link rel=\"preload\" href=\"./yuta-yokoi-ai-pm-orchestration-system.webp\" as=\"image\" fetchpriority=\"high\" />\n",
    "replace": "    <link rel=\"preload\" href=\"./yuta-yokoi-ai-pm-orchestration-system.webp\" as=\"image\" fetchpriority=\"high\" />\n    <img src=\"./yuta-yokoi-ai-pm-orchestration-system.webp\">\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 73c: hero 画像の preload から fetchpriority=\"high\" が外れる —— LCP 要素が他の取得と同じ優先度に落ちる",
    "file": ROOT / "index.html",
    "find": "as=\"image\" fetchpriority=\"high\" />",
    "replace": "as=\"image\" />",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 100a: theme-init.js の保存キーが constants.js の STORAGE_KEY と食い違う —— pre-paint で前回のテーマが読めず FOUC が戻る",
    "file": ROOT / "theme-init.js",
    "find": "localStorage.getItem('portfolio_enhanced_v45')",
    "replace": "localStorage.getItem('portfolio_enhanced_v44')",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 100b: theme-init.js のブランドキーが brand.js の KEY と食い違う —— pre-paint で前回のブランドが読めない",
    "file": ROOT / "theme-init.js",
    "find": "localStorage.getItem('portfolio_brand_v45')",
    "replace": "localStorage.getItem('portfolio_brand_v44')",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 434b: 未追跡ファイル走査の範囲から e2e/ が外れる —— git add 前の verify は「緑」の意味を失い、新しい spec を足し忘れても CI で初めて 3 つの Check が落ちる",
    "file": ROOT / ".github" / "scripts" / "checks_tracked_files.py",
    "find": "    _governed434 = (\"js/\", \"e2e/\", ",
    "replace": "    _governed434 = (\"js/\", ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 40a: devDependencies から stylelint が消える —— CSS lint の local binary が無くなり、npx の網越し取得に頼る (CI が外部に依存する)",
    "file": ROOT / "package.json",
    "find": "\"stylelint\": \"17.16.0\"",
    "replace": "\"stylelint-x\": \"17.16.0\"",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 46a: lint:js (構文検査) から theme-init.js が抜け、ESLint の lint と別の file 集合を見るようになる —— pre-paint の script だけ構文検査されない",
    "file": ROOT / "package.json",
    "find": "error-suppressor.js theme-init.js",
    "replace": "error-suppressor.js",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 124b: 視覚 renderer が実名系の entity 定数を参照する —— UI は DISPLAY_NAME (匿名の yuta) だけを使う契約で、識別子経由で実名が画面に出うる",
    "file": ROOT / "js" / "home-page.js",
    "find": "export function createHomePage({ h, Router, State, ContactCTA, langOfText }) {\n",
    "replace": "export function createHomePage({ h, Router, State, ContactCTA, langOfText }) {\n    const _leak = CONSTANTS.AUTHORITATIVE_NAME;\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 44b: AIO 監視が canary token をハードコードしなくなる —— 値の食い違い (44c) ではなく、監視が何を探すかがリポジトリから読めなくなる形",
    "file": ROOT / ".github" / "scripts" / "aio_monitoring.py",
    "find": "CANARY_TOKEN = \"SAKURA-AIO-PROVENANCE-CANARY-2026-A7F3C9E1\"",
    "replace": "CANARY_TOKEN = os.environ.get(\"AIO_CANARY\", \"\")",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 26a: AIO manifest が宣言する archive の Session Record 範囲が実体と食い違う —— 証跡の一部が discovery 層から欠ける (#14 で止まっていた実害と同形)",
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": "#15-#30",
    "replace": "#15-#29",
    "check": CHECK,
})
MUTATIONS = MUTATIONS_ARCHIVE5 + MUTATIONS_ARCHIVE4 + MUTATIONS_ARCHIVE3 + MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。




























































_E2E_TAIL.append({
    "name": "HTML 標準の license リンクが消える —— rel=license は権利宣言の最も標準的な入口で、"
            "JSON-LD を読まないツール (ライセンススキャナ等) にとっては唯一の手掛かり",
    "file": ROOT / "index.html",
    "find": '<link rel="license" href="/portfolio/LICENSES/ACD-1.3.txt" />',
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
